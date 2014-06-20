#!/usr/local/bin/python

import os, sys
import Cookie
import Crypto.Cipher.DES


class Security:
    cfgfile = None
    def __init__(self, siteid=None):
	self.cgibin = '../cgi-bin'
	self.isbeta = False
	self.ReadVersion()
	self.SetEnv(siteid)
	self.ReadConfig(siteid)
	self.cipher = Crypto.Cipher.DES.new(self.crypkey, Crypto.Cipher.DES.MODE_ECB)
	self.cookies = None

    def ReadVersion(self):
	if os.path.exists('version.txt'):
	    self.htdocs_path = '.'
	elif os.path.exists('../version.txt'):
	    self.htdocs_path = '..'
	elif os.path.exists('../htdocs/version.txt'):
	    self.htdocs_path = '../htdocs'
	else:
	    self.htdocs_path = os.environ['DOCUMENT_ROOT']
	ver = open(self.htdocs_path + '/version.txt')
	for ln in ver.readlines():
	    if '=' in ln:
		key, val = ln.strip().split('=')
		if key.startswith('$'):
		    key = key[1:]
		if val.endswith(';'):
		    val = val[:-1]
		self.__dict__[key.strip()] = eval(val.strip())
	if self.root == 'beta':
	    self.isbeta = True

    def SetEnv(self, siteid):
	self.host = os.getenv('SERVER_NAME')
	if not self.host:
	    self.host = self.root + '.bamca.org'
	    os.putenv('SERVER_NAME', self.host)
	if siteid:
	    self.host = siteid + '.' + self.host
	self.docroot = os.getenv('DOCUMENT_ROOT')
	if not self.docroot:
	    self.docroot = '/usr/local/www/bamca/' + self.root + '/htdocs'
	    os.putenv('DOCUMENT_ROOT', self.docroot)

    def ReadConfig(self, siteid):
	self.cfgfile = open(self.htdocs_path + '/' + self.cgibin + '/.config').readlines()
	self.SetConfig(siteid)

    def SetConfig(self, siteid):
	cfgkey = '.'.join(self.host.split('.')[-2:])
	if siteid:
	    cfgkey = siteid + '.' + cfgkey
	self.config = dict(map(lambda x: [x[0], dict(map(lambda y: y.split(','), x[1:]))], map(lambda x: x.strip().split('|'), self.cfgfile)))[cfgkey]
	for c in self.config:
	    self.__dict__[c] = self.config[c].strip()

    #---- cookieish code

    def ClearCookie(self, keys=[]):
	cookie = Cookie.SimpleCookie()
	for key in keys:
	    cookie[key] = ''
	    cookie[key]['expires'] = -1
	    cookie[key]['domain'] = self.CookieDomain()
	    cookie[key]['path'] = '/'
	return cookie

    def CookieDomain(self):
	return '.'.join(os.environ['SERVER_NAME'].split('.')[-2:])

    def MakeCookie(self, id, privs, expires=6000):
	cookie = Cookie.SimpleCookie()
	cryp_str = self.CookieEncode(str(id) + '/' + os.environ['REMOTE_ADDR'] + '/' + privs)
	cookie['id'] = cryp_str
	cookie['id']['expires'] = expires
	cookie['id']['domain'] = self.CookieDomain()
	cookie['id']['path'] = '/'
	return cookie

    def CookieDecode(self, val):
	return self.cipher.decrypt(Cookie._unquote(val)).strip()

    def CookieEncode(self, val):
	strval = str(val)
	strval += ' ' * (8 - len(strval) % 8)
	return Cookie._quote(self.cipher.encrypt(strval))

    def GetCookies(self):
	cookie = None
	if os.environ.get('HTTP_COOKIE'):
	    rawcookie = os.environ['HTTP_COOKIE']
	    cookie = Cookie.SimpleCookie()
	    try:
		cookie.load(rawcookie)
	    except:
		pass#sys.stderr.write("cookie decode error\n")
	else:
	    pass#sys.stderr.write("cookie missing error\n")
	if not cookie:
	    return {}
	if not cookie.get('id'):
	    #sys.stderr.write("cookie empty error\n")
	    return {}
	cookieval = self.CookieDecode(cookie['id'].value)
	if not '/' in cookieval:
	    #sys.stderr.write("cookie format error\n")
	    return {}
	try:
	    ret = dict(zip(['id','ip','pr'], self.CookieDecode(cookie['id'].value).split('/')))
	except:
	    #sys.stderr.write("cookie split error\n")
	    #sys.stderr.write("  '%s' -> '%s'\n" % (cookie['id'].value, self.CookieDecode(cookie['id'].value)))
	    return {}
	ret['co'] = cookie
	return ret



if __name__ == '__main__': # pragma: no cover
    sec = Security()
    cook = sec.GetCookies()
    if sys.argv:
	if sys.argv[1] == 'id':
	    sys.exit(int(cook.get('id', 0)))
	elif sys.argv[1] in 'vuma':
	    if sys.argv[1] in cook.get('pr', ''):
		sys.exit(1)
    sys.exit(0)
