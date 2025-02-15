#!/usr/local/bin/python

import string
import uuid

import basics
import config
import render
import useful


# ------ user editor


def print_users(pif):
    table_data = pif.dbh.get_table_data('user')
    entries = []
    for user in pif.dbh.fetch_users():
        user['user_id'] = '<a href="user.cgi?id={}">{}</a>'.format(user.id, user.user_id)
        flags = [x[1] for x in table_data.bits.get('flags', []) if (user['flags'] & int(x[0], 16))]
        user['flags'] = '<br>'.join(flags)
        entries.append(user)

    llistix = render.Listix(section=[
        render.Section(colist=table_data.columns, headers=table_data.title, range=[render.Range(entry=entries)])])
    return pif.ren.format_template('simplelistix.html', llineup=llistix)


def print_user_form(pif, id):
    user = pif.dbh.fetch_user(id)
    if not user:
        return print_users(pif)

    cols = ['title', 'value']
    heads = dict(zip(cols, ['Titles', 'Values']))
    entries = []
    table_data = pif.dbh.get_table_data('user')
    for col in table_data.columns:
        title = table_data.title[col]
        if col == 'id':
            value = '<input type="hidden" name="id" value="{}"><div class="lefty">{}</div>'.format(user[col], user[col])
            value += '<a href="user.cgi?delete=1&id={}">{}</a>'.format(
                id, pif.form.put_text_button('delete', also={'style': 'float:right'}))
        elif col in table_data.bits:
            value = pif.form.put_checkbox(col, table_data.bits[col], useful.bit_list(user[col], format='{:04x}'))
        elif col == 'email':
            value = '<input type="text" name="{}" value="{}" size=60>'.format(col, user[col])
        else:
            value = pif.form.put_text_input(col, 80, value=user[col])
        entries.append({'title': title, 'value': value})

    lrange = render.Range(entry=entries, note='')
    lsection = render.Section(colist=cols, headers=heads, range=[lrange],
                              header=pif.form.put_form_start(action='/cgi-bin/user.cgi',
                                                             name='userform', method='post', token=True),
                              footer='{} -\n{} -\n{}</form>'.format(
        pif.form.put_button_input("save changes", "submit"),
        pif.form.put_button_reset("userform"),
        pif.ren.format_button_link("change password", pif.secure_host + "/cgi-bin/chpass.cgi?id={}".format(id))))
    llistix = render.Listix(section=[lsection])
    return pif.ren.format_template('simplelistix.html', llineup=llistix)


def delete_user(pif):
    pif.dbh.delete_user(pif.form.get_str('id'))


def update_user(pif):
    newuser = pif.dbh.fetch_user(user_id=pif.form.get_str('user_id'))
    if newuser and newuser.id != pif.form.get_int('id'):
        raise useful.SimpleError('The requested user ID is already in use.')
    pif.form.set_val('flags', pif.form.get_bits('flags'))
    pif.dbh.update_user(pif.form.get_int('id'), **pif.form.get_dict(keylist=pif.dbh.get_table_data('user').columns))


@basics.web_page
def user_main(pif):
    pif.ren.set_button_comment(pif)
    pif.restrict('a')
    pif.ren.set_page_extra(pif.ren.reset_button_js)
    pif.ren.print_html()
    if pif.form.has('user_id'):
        update_user(pif)
    elif pif.form.has('delete'):
        delete_user(pif)
    elif pif.form.has('id'):
        return print_user_form(pif, pif.form.get_str('id'))
    return print_users(pif)


# ------ login


@basics.web_page
def login_main(pif):
    if pif.form.has('user_id') and pif.form.has('p'):
        user = pif.dbh.fetch_user(user_id=pif.form.get_str('user_id'), passwd=pif.form.get_str('p'))
        if user:
            pif.dbh.update_user_last_login(user.id)
            pif.create_cookie(user)
            if not user.flags & config.FLAG_USER_VERIFIED:
                raise useful.Redirect('/cgi-bin/validate.cgi')
            raise useful.Redirect(pif.form.get_str('dest', '/index.php'))
        useful.warn("Login Failed!")

    pif.ren.print_html()
    return pif.ren.format_template('login.html', dest=pif.form.get_str('dest', '/index.php'),
                                   register='signup.cgi?dest=' + pif.form.get_str('dest', '/index.php'),
                                   forgot='recover.cgi')


# ------ logout


@basics.web_page
def logout_main(pif):
    pif.dbh.delete_cookie(pif.user_id, ip=pif.remote_addr)
    pif.ren.set_cookie(pif.ren.secure.clear_cookie(['id']))
    raise useful.Redirect(pif.form.get_str('dest', '/'))


# ------ signup


def create(pif):
    # os.environ['PYTHON_EGG_CACHE'] = '/var/tmp'
    user_id = pif.form.get_str('user_id')
    p1 = pif.form.get_str('p')
    p2 = pif.form.get_str('p2')
    email = pif.form.get_str('email')
    if not user_id or (set(user_id) - set(string.ascii_letters + string.digits + '._')):
        raise useful.SimpleError('That is not a legal user ID.')
    if pif.dbh.fetch_user(user_id=user_id):
        raise useful.SimpleError('That ID is already in use.')
    if not email:
        raise useful.SimpleError('Please specify an email address.')
    if not p1 or p1 != p2:
        raise useful.SimpleError('Please specify the same password in both password boxes.')

    vkey = useful.generate_token(10)
    rec_id = pif.dbh.create_user(passwd=p1, vkey=vkey, privs='b', **pif.form.form)
    if rec_id:
        user = pif.dbh.fetch_user(id=rec_id)
        generate_signup_email(pif, user)
        useful.warn("Your account has been created.  Please check your email for the verification.")
        raise useful.Redirect("/cgi-bin/validate.cgi")

    return pif.ren.format_template('signup.html', dest=pif.form.get_str('dest'))


def generate_signup_email(pif, user):
    user['host'] = pif.server_name
    user['secure_host'] = pif.secure_host
    user['validate'] = "{secure_host}/cgi-bin/validate.cgi?user_id={user_id}&vkey={vkey}".format(**user.todict())
    # user = {k: useful.url_quote(str(v), plus=True) for k, v in user.todict().items()}
    msg = '''To: "{user_id}" <{email}>
From: "Account Verification" <webmaster@{host}>
Subject: Verify your account
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit

Dear {first_name} {last_name},

You have registered for an account on {host}.  Please verify your new account
by visiting the following link:

<a href="{validate}">{validate}</a>

Or, the next time you log in, you will be taken to the verification page.
Enter this code to verify your account.

                 {vkey}

Thank you!
'''.format(**user.todict())
    useful.simple_process(('/usr/sbin/sendmail', '-t',), msg)


@basics.web_page
def register_main(pif):
    pif.ren.print_html()
    if pif.form.get_str('user_id'):
        return create(pif)

    return pif.ren.format_template('signup.html', dest=pif.form.get_str('dest'))


# ------ chpass


@basics.web_page
def change_password_main(pif):
    pif.ren.title = 'Change Password'
    pif.ren.hide_title = False
    pif.ren.print_html()

    if not pif.user_id:
        raise useful.SimpleError("It doesn't look like you're logged in!")
    if pif.form.has('id') and pif.is_allowed('a') and pif.form.get_int('id') != pif.user_id:
        user = pif.dbh.fetch_user(pif.form.get_int('id'))
    else:
        user = pif.user
    if not user:
        raise useful.SimpleError('That user record ({}) was not found.'.format(pif.user_id))

    if pif.is_allowed('a') and 'p1' in pif.form:
        user_id = pif.form.get_int('id')
        if pif.form.get_str('p1') != pif.form.get_str('p2'):
            useful.warn("The new passwords don't match!")
        else:
            pif.dbh.update_password(user_id, pif.form.get_str('p2'))
            useful.warn("This password has been changed.")
    elif 'op' in pif.form:
        newuser = pif.dbh.fetch_user(user_id=pif.user_id, passwd=pif.form.get_str('op'))
        if not newuser:
            useful.warn("That password isn't correct!")
        elif pif.form.get_str('p1') != pif.form.get_str('p2'):
            useful.warn("The new passwords don't match!")
        else:
            pif.dbh.update_password(pif.user_id, pif.form.get_str('p2'))
            pif.dbh.update_user(pif.user_id, ckey=uuid.uuid4())
            pif.create_cookie()
            useful.warn("Your password has been changed.")

    entries = [
        {'title': 'Old password:', 'value': '<input type="password" name="op">'},
        {'title': 'New password:', 'value': '<input type="password" name="p1">'},
        {'title': 'Retry new password:', 'value': '<input type="password" name="p2">'},
    ]
    lsection = render.Section(
        colist=['title', 'value'],
        range=[render.Range(entry=entries)],
        noheaders=True,
        header=pif.form.put_form_start(method='post', token=pif.dbh.create_token()),
        footer=pif.form.put_hidden_input(id=user['id']) + pif.form.put_button_input() + "</form>",
    )
    return pif.ren.format_template(
        'simplelistix.html',
        header='''<br>You have requested to change your password.<br>''',
        llineup=render.Listix(section=[lsection]), nofooter=True)


# ------ validate


@basics.web_page
def validate_main(pif):

    pif.ren.print_html()
    if not pif.user_id:
        raise useful.Redirect("/cgi-bin/login.cgi")
    user = pif.user
    if 'vkey' in pif.form:
        if user and user.vkey == pif.form.get_str('vkey'):
            rec_id = user.id
            pif.dbh.verify_user(rec_id)
            useful.warn("Your account has been verified!")
            raise useful.Redirect("/", delay=5)
        else:
            useful.warn("That code is not correct.  Please try again.")

    if 'resend' in pif.form:
        generate_signup_email(pif, pif.user)
        useful.warn("The code has been resent.")

    return pif.ren.format_template('validate.html', user_id=pif.user.user_id, dest=pif.form.get_str('dest'))


# def verify(pif, user_id, vkey):
#     user = pif.dbh.fetch_user(vkey=vkey, user_id=user_id)
#     if user:
#         rec_id = user.id
#         pif.dbh.verify_user(rec_id)
#         useful.warn("Your account has been verified!  Now please log in.<br><hr>")
#         raise useful.Redirect("/cgi-bin/login.cgi", delay=5)
#
#     useful.warn("You have not verified your account.  Please contact staff@bamca.org for help.")
#     raise useful.Redirect("/", delay=5)


# ------ recover


@basics.web_page
def recover_main(pif):
    pif.ren.print_html()
    hide_vkey = recovering = False
    user_id = None
    if pif.form.has('user_id'):
        if pif.form.has('vkey'):
            user = pif.dbh.fetch_user(user_id=pif.form.get_alnum('user_id'), vkey=pif.form.get_alnum('vkey'))
            if user:
                if pif.form.has('p1') and pif.form.get_str('p1') == pif.form.get_str('p2'):
                    pif.dbh.update_password(user.id, pif.form.get_str('p2'))
                    pif.dbh.update_user(rec_id=user.id, flags=user.flags & ~config.FLAG_USER_PASSWORD_RECOVERY)
                    pif.ren.set_cookie(pif.ren.secure.clear_cookie(['id']))
                    useful.warn("Your password has been changed.")
                    raise useful.Redirect('/cgi-bin/login.cgi', delay=5)
                else:
                    user_id = user.user_id
                    recovering = hide_vkey = True
        else:
            user = pif.dbh.fetch_user(email=pif.form.get_str('user_id'))
            if not user:
                user = pif.dbh.fetch_user(user_id=pif.form.get_alnum('user_id'))
            if user:
                pif.dbh.update_user(rec_id=user.id, flags=user.flags | config.FLAG_USER_PASSWORD_RECOVERY)
                generate_recovery_email(pif, user)
                recovering = True
                user_id = user.user_id
    return pif.ren.format_template('recover.html', recovering=recovering, user_id=user_id, show_vkey=not hide_vkey)


def generate_recovery_email(pif, user):
    user['host'] = pif.server_name
    user['secure_host'] = pif.secure_host
    user['recover'] = "{secure_host}/cgi-bin/recover.cgi?user_id={user_id}&vkey={vkey}".format(**user.todict())
    # user = {k: useful.url_quote(str(v), plus=True) for k, v in user.todict().items()}
    msg = '''To: "{user_id}" <{email}>
From: "Account Verification" <webmaster@{host}>
Subject: Reset your password
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit

Dear {first_name} {last_name},

A request has been made to reset your password on {host}.  Please verify that you
made this request by visiting the following link:

<a href="{recover}">{recover}</a>

Or, the page where you requested to change your password will now ask for a verification code.
Enter this code in the verification input as you change your password.

                 {vkey}

Thank you!
'''.format(**user.todict())
    useful.simple_process(('/usr/sbin/sendmail', '-t',), msg)


# ------ user profile


@basics.web_page
def profile_main(pif):
    pif.ren.title = 'User Profile'
    pif.ren.hide_title = False
    pif.ren.print_html()

    if not pif.user_id:
        raise useful.SimpleError("It doesn't look like you're logged in!")
    table_data = pif.dbh.get_table_data('user')
    user = pif.user
    if not user:
        raise useful.SimpleError('That user record ({}) was not found.'.format(pif.user_id))
    if 'user_id' in pif.form:
        newuser = pif.dbh.fetch_user(user_id=pif.form.get_str('user_id'))
        if newuser and newuser.id != pif.form.get_int('id'):
            raise useful.SimpleError('Sorry, but that user ID is already in use.')
        if pif.dbh.update_profile(user, **pif.form.form):
            useful.warn('Your profile has been updated.')
        else:
            useful.warn('Updating your profile failed.')
    # if email changed, clear verified

    header = pif.form.put_form_start(method='post', token=pif.dbh.create_token())
    rows = table_data.editable
    desc = pif.dbh.describe_dict('user')

    def prof_row(row):
        return {'title': table_data.title[row], 'value': pif.form.put_text_input(
            row, desc[row]['length'], 80, value=user[row]) + (
            '<br>If you change your email address, you will have to verify the new one.' if row == 'email' else '')}

    entries = [prof_row(row) for row in rows]
    if user['flags'] & config.FLAG_USER_BAMCA_MEMBER:
        entries[0]['value'] += ' ' + pif.ren.fmt_art('bamca_member')
    footer = pif.form.put_hidden_input(id=user['id'])
    footer += pif.form.put_button_input() + "</form>"
    footer += pif.ren.format_button_link('change password', '/cgi-bin/chpass.cgi')
    if user['photographer_id']:
        footer += pif.ren.format_button_link(
            'your pictures', '/cgi-bin/photogs.cgi?id={}'.format(user['photographer_id']))
    lsection = render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)],
                              noheaders=True, header=header, footer=footer)
    return pif.ren.format_template(
        'simplelistix.html',
        header=('''<br>Currently this information is only available to administrators of this website.  We're '''
                '''looking at possibly doing more in the future though.<br><br>'''),
        llineup=render.Listix(section=[lsection]), nofooter=True)


# ------


def user_list(pif):
    print(pif.dbh.fetch_users())


cmds = [
    ('l', user_list, "list users"),
]


if __name__ == '__main__':  # pragma: no cover
    basics.process_command_list(cmds=cmds)
