#!/usr/local/bin/python

import os, random, string, sys, urllib

# ------ user

# todo
#  password clearing - how?
#  acct verification

cols = [('id', 'Id'), ('name', 'User Name'), ('privs', 'Priveleges'), ('state', 'State'), ('email', 'Email Address'), ('vkey', 'Verification Key')]


def PrintUsers(pif):
    users = pif.dbh.FetchUsers()
    print pif.render.FormatTableStart(also={'border':1})

    print pif.render.FormatRowStart()
    for col in cols:
	print pif.render.FormatCell(0, col[1], hdr=True)
    print pif.render.FormatRowEnd()

    for user in users:
	print pif.render.FormatRowStart()
	for col in cols:
	    if col[0] == 'name':
		print pif.render.FormatCell(0, '<a href="user.cgi?id=%s">%s</a>' % (user['id'], user[col[0]]))
	    else:
		print pif.render.FormatCell(0, user[col[0]])
	print pif.render.FormatRowEnd()

    print pif.render.FormatTableEnd()


def PrintUserForm(pif, id):
    user = pif.dbh.FetchUser(id)[0]
    print '<form name="userform">'
    print pif.render.FormatTableStart(also={'border':1})

    for col in cols:
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, col[1], hdr=True)
	if col[0] == 'id':
	    cell = '<input type="hidden" name="id" value="%s"><div class="lefty">%s</div>' % (user[col[0]], user[col[0]])
	    cell += '<a href="user.cgi?delete=1&id=%s">%s</a>' % (id, pif.render.FormatButton('delete', also={'style':'float:right'}))
	elif col[0] == 'email':
	    cell = '<input type="text" name="%s" value="%s" size=60>' % (col[0], user[col[0]])
	else:
	    cell = '<input type="text" name="%s" value="%s">' % (col[0], user[col[0]])
	print pif.render.FormatCell(0, cell)
	print pif.render.FormatRowEnd()

    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, 'Password', hdr=True)
    cell = '<input type="checkbox" name="%s">' % col[0]
    print pif.render.FormatCell(0, cell)
    print pif.render.FormatRowEnd()

    print pif.render.FormatTableEnd()
    print pif.render.FormatButtonInput("save changes", "submit") + ' -'
    print pif.render.FormatButtonReset("userform")
    print '</form>'


def DeleteUser(pif):
    pif.dbh.DeleteUser(pif.form['id'])


def UpdateUser(pif):
    pif.dbh.UpdateUser(pif.form.get('id', ''), email=pif.form.get('email'), state=pif.form.get('state'), name=pif.form.get('name'), privs=pif.form.get('privs'))


def UserMain(pif):
    pif.render.PrintHtml()
    pif.Restrict('a')
    print pif.render.FormatHead(extra=pif.render.reset_button_js)
    if 'name' in pif.form:
	UpdateUser(pif)
	PrintUsers(pif)
    elif 'delete' in pif.form:
	DeleteUser(pif)
	PrintUsers(pif)
    elif 'id' in pif.form:
	PrintUserForm(pif, pif.form['id'])
    else:
	PrintUsers(pif)
    print pif.render.FormatTail()

# ------ login

def PrintLoginForm(pif):
    print 'Please log in.'
    print '<form method="post" action="login.cgi">'
    if pif.form.get('dest'):
	print '<input type="hidden" name="dest" value="%s">' % pif.form['dest']
    print '<table><tr><td>'
    print 'Name:</td><td>'
    print '<input type="text" name="n"></td></tr>'
    print '<tr><td>'
    print 'Password:</td><td>'
    print '<input type="password" name="p"></td></tr>'
    print '<tr><td></td><td>'
    #print '<input type="image" name="submit" src="../pic/gfx/but_log_in.gif" class="img">'
    print pif.render.FormatButtonInput("log in", "submit")
    #print '<input type="hidden" name="dest" value="%s">' % pif.form.get('dest', '/index.php')
    print '</form>'
    print '</td></tr><tr><td></td><td>'
    print '<p><a href="signup.cgi?dest=%s">%s</a>' % (pif.form.get('dest', '/index.php'), pif.render.FormatButton('register'))
    print '</td></tr></table>'


def Login(pif):
    id = None
    id, privs = pif.dbh.Login(pif.form['n'], pif.form['p'])
    if id:
	cookie = pif.render.MakeCookie(id, privs, expires=15 * 12 * 60 * 60)
	pif.render.PrintHtml(cookie)
	print '<meta http-equiv="refresh" content="1;url=%s">' % pif.form.get('dest', '/index.php')
	#print cookie , '<br>'
	#print {'id' : str(id) + ';' + os.environ['REMOTE_ADDR'] + ';' + privs}, '<br>'
	#print "'''"+os.environ.get('HTTP_COOKIE')+"'''", '<br>'
    else:
	#cookie = pif.render.ClearCookie(['id'])
	pif.render.PrintHtml()
	print pif.render.FormatHead()
	PrintLoginForm(pif)


def LoginMain(pif):
    if pif.form.get('n'):
	Login(pif)
    else:
	pif.render.PrintHtml()
	print pif.render.FormatHead()
	PrintLoginForm(pif)

    print pif.render.FormatTail()

# ------ logout

def LogoutMain(pif):
    cookie = pif.render.ClearCookie(['id'])
    pif.render.PrintHtml(cookie)
    print '<meta http-equiv="refresh" content="0;url=%s>' % pif.form.get('dest', '../')
    #print '<meta http-equiv="refresh" content="0;url=%s>' % '/index.php'

# ------ signup

def PrintSignupForm(pif):
    print pif.render.FormatHead()
    print 'You are registering to receive an account on this system.'
    print '<form method="post">'
    print pif.render.FormatTableStart()
    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, 'Name:')
    print pif.render.FormatCell(1, '<input type="text" name="n">')
    print pif.render.FormatRowEnd()
    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, 'Password:')
    print pif.render.FormatCell(1, '<input type="password" name="p">')
    print pif.render.FormatRowEnd()
    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, 'Retry password:')
    print pif.render.FormatCell(1, '<input type="password" name="p2">')
    print pif.render.FormatRowEnd()
    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, 'EMail:')
    print pif.render.FormatCell(1, '<input type="text" name="e" size=60>')
    print pif.render.FormatRowEnd()
    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, pif.render.FormatButtonInput("register", "submit"))
    print pif.render.FormatRowEnd()
    print pif.render.FormatTableEnd()
    print '<input type="hidden" name="dest" value="%s">' % pif.form.get('dest', '/index.php')
    print '</form>'
    print pif.render.FormatTail()


def Create(pif):
    os.environ['PYTHON_EGG_CACHE'] = '/var/tmp'
    n = pif.form.get('n')
    p = pif.form.get('p')
    p2 = pif.form.get('p2')
    e = pif.form.get('e')
    if not n or not p or p != p2 or not e:
	pif.render.PrintHtml()
	PrintSignupForm(pif)
	return

    vkey = GenKey()
    id = pif.dbh.CreateUser(n, p, e, vkey)
    if id:
	GenEmail(n, e, vkey)
	cookie = pif.render.MakeCookie(id, privs, expires=15 * 12 * 60 * 60)
	pif.render.PrintHtml(cookie)
	print pif.render.FormatHead()
	print "Your account has been created.  Please check your email for the verification."
    else:
	#cookie = pif.render.ClearCookie(['id'])
	pif.render.PrintHtml()
	PrintSignupForm(pif)
	#pif.render.PrintHtml(cookie)


def GenKey():
    s = string.digits + string.ascii_lowercase
    return ''.join(map(lambda x:s[random.randrange(len(s))], range(0,10)))


def GenEmail(name, email, vkey):
    msg = '''To: "%(name)s" <%(email)s>
From: "Account Verification" <webmaster@%(host)s>
Subject: Verify your account
Content-Type: text/plain; charset=us-ascii
Content-Transfer-Encoding: 7bit

You have registered for an account on %(host)s.  Please verify your new account
by visiting the following link:

<a href="http://%(host)s/cgi-bin/signup.cgi?u=%(name)s&k=%(vkey)s">http://%(host)s/cgi-bin/signup.cgi?u=%(name)s&k=%(vkey)s</a>

Thank you!
''' % {'name' : urllib.quote_plus(name), 'email' : email, 'vkey' : vkey, 'host' : os.environ['SERVER_NAME']}
    import subprocess
    proc = subprocess.Popen(['/usr/sbin/sendmail', '-t'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None, close_fds=True)
    o, e = proc.communicate(msg)


def Verify(pif, name, vkey):
    pif.render.PrintHtml()
    print pif.render.FormatHead()
    userrec = pif.dbh.FetchUser(vkey=vkey, name=name)
    if userrec:
	userrec = userrec[0]
	id = userrec['id']
	pif.dbh.UpdateUser(id, state=1)
	print "Your account has been verified!  Now please log in.<br><hr>"
	PrintLoginForm(pif)
    else:
	print "You have not verified your account.  Please contact staff@bamca.org for help."
    print pif.render.FormatTail()

# ------ signup

def RegisterMain(pif):
    if pif.form.get('n'):
	user.Create(pif)
    elif pif.form.get('k'):
	u = pif.form['u']
	k = pif.form['k']
	user.Verify(pif, u, k)
    else:
	pif.render.PrintHtml()
	user.PrintSignupForm(pif)

# ------ chpass

def PrintChangePasswordForm(pif):
    print pif.render.FormatHead()
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
    #print '<input type="image" name="submit" src="../pic/gfx/but_save_changes.gif" class="img">'
    print pif.render.FormatButtonInput("save changes", "submit")
    print '</td></tr></table>'
    print '<input type="hidden" name="dest" value="%s">' % pif.form.get('dest', '/index.php')
    print '</form>'
    print pif.render.FormatTail()


def ChangePass(pif):
    if not pif.form.get('p1') or pif.form.get('p1') != pif.form.get('p2'):
	pif.render.PrintHtml()
	PrintChangePasswordForm(pif)
	return

    id, privs = pif.dbh.Login(pif.form['n'], pif.form['op'])
    if id and pif.form.get('p1') == pif.form.get('p2', -1):
	pif.dbh.UpdateUser(id, email=pif.form.get('em'), passwd=pif.form.get('p1'))
	cookie = pif.render.MakeCookie(id, privs, expires=15 * 12 * 60 * 60)
	pif.render.PrintHtml(cookie)
	print '<meta http-equiv="refresh" content="0;url=%s>' % pif.form.get('dest', '/index.php')
    else:
	cookie = pif.render.ClearCookie(['id'])
	pif.render.PrintHtml()
	PrintChangePasswordForm(pif)


def ChangePasswordMain():
    import basics
    pif = basics.GetPageInfo('user')
    if pif.form.get('n'):
	ChangePass(pif)
    else:
	pif.render.PrintHtml()
	PrintChangePasswordForm(pif)

# ------ 

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
