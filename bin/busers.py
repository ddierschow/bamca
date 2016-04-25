#!/usr/local/bin/python

import os, random, string, subprocess, sys, urllib

import basics
import useful

# ------ user

# todo
#  password clearing - how?
#  acct verification

cols = [('id', 'Id'), ('name', 'User Name'), ('privs', 'Priveleges'), ('state', 'State'), ('email', 'Email Address'),
        ('vkey', 'Verification Key')]


def print_users(pif):
    users = pif.dbh.fetch_users()
    print pif.render.format_table_start(also={'border': 1})

    print pif.render.format_row_start()
    for col in cols:
        print pif.render.format_cell(0, col[1], hdr=True)
    print pif.render.format_row_end()

    for user in users:
        user = pif.dbh.depref('user', user)
        print pif.render.format_row_start()
        for col in cols:
            if col[0] == 'name':
                print pif.render.format_cell(0, '<a href="user.cgi?id=%s">%s</a>' % (user['id'], user[col[0]]))
            else:
                print pif.render.format_cell(0, user[col[0]])
        print pif.render.format_row_end()

    print pif.render.format_table_end()


def print_user_form(pif, id):
    user = pif.dbh.depref('user', pif.dbh.fetch_user(id)[0])
    print '<form name="userform">'
    print pif.render.format_table_start(also={'border': 1})

    for col in cols:
        print pif.render.format_row_start()
        print pif.render.format_cell(0, col[1], hdr=True)
        if col[0] == 'id':
            cell = '<input type="hidden" name="id" value="%s"><div class="lefty">%s</div>' % (user[col[0]], user[col[0]])
            cell += '<a href="user.cgi?delete=1&id=%s">%s</a>' % \
                    (id, pif.render.format_button('delete', also={'style': 'float:right'}))
        elif col[0] == 'email':
            cell = '<input type="text" name="%s" value="%s" size=60>' % (col[0], user[col[0]])
        else:
            cell = '<input type="text" name="%s" value="%s">' % (col[0], user[col[0]])
        print pif.render.format_cell(0, cell)
        print pif.render.format_row_end()

    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'Password', hdr=True)
    cell = '<input type="checkbox" name="%s">' % col[0]
    print pif.render.format_cell(0, cell)
    print pif.render.format_row_end()

    print pif.render.format_table_end()
    print pif.render.format_button_input("save changes", "submit") + ' -'
    print pif.render.format_button_reset("userform")
    print '</form>'


def delete_user(pif):
    pif.dbh.delete_user(pif.form.get_str('id'))


def update_user(pif):
    pif.dbh.update_user(pif.form.get_str('id'), email=pif.form.get_str('email'), state=pif.form.get_str('state'), name=pif.form.get_str('name'),
                        privs=pif.form.get_str('privs'))


@basics.web_page
def user_main(pif):
    pif.render.print_html()
    pif.restrict('a')
    pif.render.set_page_extra(pif.render.reset_button_js)
    print pif.render.format_head()
    useful.header_done()
    if pif.form.has('name'):
        update_user(pif)
        print_users(pif)
    elif pif.form.has('delete'):
        delete_user(pif)
        print_users(pif)
    elif pif.form.has('id'):
        print_user_form(pif, pif.form.get_str('id'))
    else:
        print_users(pif)
    print pif.render.format_tail()


# ------ login


def print_login_form(pif):
    print 'Please log in.'
    print '<form method="post" action="login.cgi">'
    if pif.form.has('dest'):
        print '<input type="hidden" name="dest" value="%s">' % pif.form.get_str('dest')
    print '<table><tr><td>'
    print 'Name:</td><td>'
    print '<input type="text" name="n"></td></tr>'
    print '<tr><td>'
    print 'Password:</td><td>'
    print '<input type="password" name="p"></td></tr>'
    print '<tr><td></td><td>'
#    print '<input type="image" name="submit" src="../pic/gfx/but_log_in.gif" class="img">'
    print pif.render.format_button_input("log in", "submit")
#    print '<input type="hidden" name="dest" value="%s">' % pif.form.get_str('dest', '/index.php')
    print '</form>'
    print '</td></tr><tr><td></td><td>'
    print '<p><a href="signup.cgi?dest=%s">%s</a>' % (pif.form.get_str('dest', '/index.php'), pif.render.format_button('register'))
    print '</td></tr></table>'


def login(pif):
    id = None
    id, privs = pif.dbh.login(pif.form.get_str('n'), pif.form.get_str('p'))
    if id:
        cookie = pif.render.secure.make_cookie(id, privs, expires=15 * 12 * 60 * 60)
        pif.render.print_html(cookie=cookie)
        #print '<meta http-equiv="refresh" content="1;url=%s">' % pif.form.get_str('dest', '/index.php')
	raise useful.Redirect(pif.form.get_str('dest', '/index.php'))
    else:
        pif.render.print_html()
        print pif.render.format_head()
	useful.header_done()
        print 'Login Failed!<br>'
        print_login_form(pif)


@basics.web_page
def login_main(pif):
    if pif.form.has('n'):
        login(pif)
    else:
        pif.render.print_html()
        print pif.render.format_head()
	useful.header_done()
        print_login_form(pif)

    print pif.render.format_tail()


# ------ logout


@basics.web_page
def logout_main(pif):
    cookie = pif.render.secure.clear_cookie(['id'])
    pif.render.print_html(cookie=cookie)
    #print '<meta http-equiv="refresh" content="0;url=%s>' % pif.form.get_str('dest', '../')
    raise useful.Redirect(pif.form.get_str('dest', '../'))
#    print '<meta http-equiv="refresh" content="0;url=%s>' % '/index.php'


# ------ signup


def print_signup_form(pif):
    print pif.render.format_head()
    useful.header_done()
    print 'You are registering to receive an account on this system.'
    print '<form method="post">'
    print pif.render.format_table_start()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'Name:')
    print pif.render.format_cell(1, '<input type="text" name="n">')
    print pif.render.format_row_end()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'Password:')
    print pif.render.format_cell(1, '<input type="password" name="p">')
    print pif.render.format_row_end()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'Retry password:')
    print pif.render.format_cell(1, '<input type="password" name="p2">')
    print pif.render.format_row_end()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'EMail:')
    print pif.render.format_cell(1, '<input type="text" name="e" size=60>')
    print pif.render.format_row_end()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, pif.render.format_button_input("register", "submit"))
    print pif.render.format_row_end()
    print pif.render.format_table_end()
    print '<input type="hidden" name="dest" value="%s">' % pif.form.get_str('dest', '/index.php')
    print '</form>'
    print pif.render.format_tail()


def create(pif):
    os.environ['PYTHON_EGG_CACHE'] = '/var/tmp'
    n = pif.form.get_str('n')
    p = pif.form.get_str('p')
    p2 = pif.form.get_str('p2')
    e = pif.form.get_str('e')
    if not n or not p or p != p2 or not e:
        pif.render.print_html()
        print_signup_form(pif)
        return

    vkey = gen_key()
    id = pif.dbh.create_user(n, p, e, vkey)
    if id:
        gen_email(n, e, vkey)
        cookie = pif.render.secure.make_cookie(id, '', expires=15 * 12 * 60 * 60)
        pif.render.print_html(cookie=cookie)
        print pif.render.format_head()
	useful.header_done()
        print "Your account has been created.  Please check your email for the verification."
    else:
        pif.render.print_html()
        print_signup_form(pif)


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
    pif.render.print_html()
    print pif.render.format_head()
    useful.header_done()
    userrec = pif.dbh.fetch_user(vkey=vkey, name=name)
    if userrec:
        userrec = userrec[0]
        id = userrec['user.id']
        pif.dbh.update_user(id, state=1)
        print "Your account has been verified!  Now please log in.<br><hr>"
        print_login_form(pif)
    else:
        print "You have not verified your account.  Please contact staff@bamca.org for help."
    print pif.render.format_tail()


# ------ signup


@basics.web_page
def register_main(pif):
    if pif.form.get_str('n'):
        create(pif)
    elif pif.form.get_str('k'):
        u = pif.form.get_str('u')
        k = pif.form.get_str('k')
        verify(pif, u, k)
    else:
        pif.render.print_html()
        print_signup_form(pif)


# ------ chpass


def print_change_password_form(pif):
    print pif.render.format_head()
    useful.header_done()
    print 'You have requested to change your password.'
    print '<form method="post">'
    print '<table><tr><td>'
    print 'Name:</td><td>'
    print '<input type="text" name="n"></td></tr>'
    print '<tr><td>'
    print 'Old password:</td><td>'
    print '<input type="password" name="op"></td></tr>'
    print '<tr><td>'
    print 'New password:</td><td>'
    print '<input type="password" name="p1"></td></tr>'
    print '<tr><td>'
    print 'Retry new password:</td><td>'
    print '<input type="password" name="p2"></td></tr>'
    print '<tr><td>'
    print 'Change email address:</td><td>'
    print '<input type="text" name="em" size=60></td></tr>'
    print '<tr><td></td><td>'
#    print '<input type="image" name="submit" src="../pic/gfx/but_save_changes.gif" class="img">'
    print pif.render.format_button_input("save changes", "submit")
    print '</td></tr></table>'
    print '<input type="hidden" name="dest" value="%s">' % pif.form.get_str('dest', '/index.php')
    print '</form>'
    print pif.render.format_tail()


def change_pass(pif):
    if not pif.form.get_str('p1') or pif.form.get_str('p1') != pif.form.get_str('p2'):
        pif.render.print_html()
        print_change_password_form(pif)
        return

    id, privs = pif.dbh.login(pif.form.get_str('n'), pif.form.get_str('op'))
    if id and pif.form.get_str('p1') == pif.form.get_str('p2', -1):
        pif.dbh.update_user(id, email=pif.form.get_str('em'), passwd=pif.form.get_str('p1'))
        cookie = pif.render.secure.make_cookie(id, privs, expires=15 * 12 * 60 * 60)
        pif.render.print_html(cookie=cookie)
        #print '<meta http-equiv="refresh" content="0;url=%s>' % pif.form.get_str('dest', '/index.php')
	raise useful.Redirect(pif.form.get_str('dest', '/index.php'))
    else:
        cookie = pif.render.secure.clear_cookie(['id'])
        pif.render.print_html()
        print_change_password_form(pif)


@basics.web_page
def change_password_main():
    pif = basics.get_page_info('user')
    if pif.form.get_str('n'):
        change_pass(pif)
    else:
        pif.render.print_html()
        print_change_password_form(pif)


# ------


if __name__ == '__main__':  # pragma: no cover
    basics.goaway()
