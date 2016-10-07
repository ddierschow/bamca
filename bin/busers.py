#!/usr/local/bin/python

import os, random, string, subprocess, sys, urllib

import basics
import useful

# ------ user

# todo
#  password clearing - how?
#  acct verification

user_cols = [('id', 'Id'), ('name', 'User Name'), ('privs', 'Priveleges'), ('state', 'State'), ('email', 'Email Address'),
        ('vkey', 'Verification Key')]


def print_users(pif):
    entries = []
    for user in pif.dbh.fetch_users():
        pif.dbh.depref('user', user)
	user['name'] = '<a href="user.cgi?id=%s">%s</a>' % (user['id'], user['name'])
	entries.append(user)

    lrange = dict(entry=entries, note='')
    lsection = dict(columns=[x[0] for x in user_cols], headers=user_cols, range=[lrange], note='')
    llineup = dict(section=[lsection])
    return pif.render.format_template('simplelistix.html', llineup=llineup)


def print_user_form(pif, id):
    users = pif.dbh.fetch_user(id)
    if not users:
	return print_users(pif)

    user = pif.dbh.depref('user', users[0])
    cols = ['title', 'value']
    heads = dict(zip(cols, ['Titles', 'Values']))
    entries = []
    for col in user_cols:
	title = col[1]
        if col[0] == 'id':
            value = '<input type="hidden" name="id" value="%s"><div class="lefty">%s</div>' % (user[col[0]], user[col[0]])
            value += '<a href="user.cgi?delete=1&id=%s">%s</a>' % \
                    (id, pif.render.format_button('delete', also={'style': 'float:right'}))
        elif col[0] == 'email':
            value = '<input type="text" name="%s" value="%s" size=60>' % (col[0], user[col[0]])
        else:
            value = '<input type="text" name="%s" value="%s">' % (col[0], user[col[0]])
	entries.append({'title': title, 'value': value})
    entries.append({'title': 'Password', 'value': '<input type="checkbox" name="%s">' % col[0]})

    lrange = dict(entry=entries, note='')
    lsection = dict(columns=cols, headers=heads, range=[lrange], note='')
    llineup = dict(section=[lsection], header='<form name="userform">',
	footer=pif.render.format_button_input("save changes", "submit") + ' -' + pif.render.format_button_reset("userform") + '</form>')
    return pif.render.format_template('simplelistix.html', llineup=llineup)


def delete_user(pif):
    pif.dbh.delete_user(pif.form.get_str('id'))


def update_user(pif):
    pif.dbh.update_user(pif.form.get_str('id'),
			email=pif.form.get_str('email'),
			state=pif.form.get_str('state'),
			name=pif.form.get_str('name'),
                        privs=pif.form.get_str('privs'))


@basics.web_page
def user_main(pif):
    pif.render.set_button_comment(pif)
    pif.restrict('a')
    pif.render.set_page_extra(pif.render.reset_button_js)
    pif.render.print_html()
    if pif.form.has('id'):
        return print_user_form(pif, pif.form.get_str('id'))

    if pif.form.has('name'):
        update_user(pif)
    elif pif.form.has('delete'):
        delete_user(pif)
    return print_users(pif)


# ------ login


@basics.web_page
def login_main(pif):
    if pif.form.has('n'):
	id, privs = pif.dbh.login(pif.form.get_str('n'), pif.form.get_str('p'))
	if id:
	    pif.render.set_cookie(pif.render.secure.make_cookie(id, privs, expires=15 * 12 * 60 * 60))
	    raise useful.Redirect(pif.form.get_str('dest', '/index.php'))
	useful.warn("Login Failed!")

    pif.render.print_html()
    return pif.render.format_template('login.html', dest=pif.form.get_str('dest', '/index.php'))


# ------ logout


@basics.web_page
def logout_main(pif):
    pif.render.set_cookie(pif.render.secure.clear_cookie(['id']))
    raise useful.Redirect(pif.form.get_str('dest', '/'))


# ------ signup


def create(pif):
    os.environ['PYTHON_EGG_CACHE'] = '/var/tmp'
    n = pif.form.get_str('n')
    p = pif.form.get_str('p')
    p2 = pif.form.get_str('p2')
    e = pif.form.get_str('e')
    if not n or not p or p != p2 or not e:
        pif.render.print_html()
	return pif.render.format_template('signup.html', dest=pif.form.get_str('dest'))

    vkey = gen_key()
    id = pif.dbh.create_user(n, p, e, vkey)
    if id:
        gen_email(n, e, vkey)
	pif.render.set_cookie(pif.render.secure.make_cookie(id, '', expires=15 * 12 * 60 * 60))
        useful.warn("Your account has been created.  Please check your email for the verification.")
	raise useful.Redirect("/cgi-bin/login.cgi")

    pif.render.print_html()
    return pif.render.format_template('signup.html', dest=pif.form.get_str('dest'))


def gen_key():
    s = string.digits + string.ascii_lowercase
    return ''.join([s[random.randrange(len(s))] for x in range(0, 10)])


def gen_email(name, email, vkey):
    msg = '''To: "%(name)s" <%(email)s>
From: "Account Verification" <webmaster@%(host)s>
Subject: Verify your account
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit

You have registered for an account on %(host)s.  Please verify your new account
by visiting the following link:

<a href="http://%(host)s/cgi-bin/signup.cgi?u=%(name)s&k=%(vkey)s">http://%(host)s/cgi-bin/signup.cgi?u=%(name)s&k=%(vkey)s</a>

Thank you!
''' % {'name': urllib.quote_plus(name), 'email': email, 'vkey': vkey, 'host': os.environ['SERVER_NAME']}
    proc = subprocess.Popen(['/usr/sbin/sendmail', '-t'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None,
                            close_fds=True)
    o, e = proc.communicate(msg)


def verify(pif, name, vkey):
    userrec = pif.dbh.fetch_user(vkey=vkey, name=name)
    if userrec:
        userrec = userrec[0]
        id = userrec['user.id']
        pif.dbh.update_user(id, state=1)
        useful.warn("Your account has been verified!  Now please log in.<br><hr>")
	raise useful.Redirect("/cgi-bin/login.cgi")

    useful.warn("You have not verified your account.  Please contact staff@bamca.org for help.")
    raise useful.Redirect("/")


@basics.web_page
def register_main(pif):
    if pif.form.get_str('n'):
        return create(pif)
    elif pif.form.get_str('k'):
        u = pif.form.get_str('u')
        k = pif.form.get_str('k')
        verify(pif, u, k)

    pif.render.print_html()
    return pif.render.format_template('signup.html', dest=pif.form.get_str('dest'))


# ------ chpass


@basics.web_page
def change_password_main(pif):
    if not pif.form.get_str('n'):
	pif.render.print_html()
	return pif.render.format_template('chpass.html', dest=pif.form.get_str('dest'))

    if not pif.form.get_str('p1') or pif.form.get_str('p1') != pif.form.get_str('p2'):
        pif.render.print_html()
	return pif.render.format_template('chpass.html', dest=pif.form.get_str('dest'))

    id, privs = pif.dbh.login(pif.form.get_str('n'), pif.form.get_str('op'))
    if id and pif.form.get_str('p1') == pif.form.get_str('p2', -1):
        pif.dbh.update_user(id, email=pif.form.get_str('em'), passwd=pif.form.get_str('p1'))
	pif.render.set_cookie(pif.render.secure.make_cookie(id, privs, expires=15 * 12 * 60 * 60))
	raise useful.Redirect(pif.form.get_str('dest', '/index.php'))

    cookie = pif.render.secure.clear_cookie(['id'])
    pif.render.print_html()
    return pif.render.format_template('chpass.html', dest=pif.form.get_str('dest'))


# ------


if __name__ == '__main__':  # pragma: no cover
    basics.goaway()
