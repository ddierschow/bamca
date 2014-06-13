#!/usr/local/bin/python

import os, sys
import Cookie
import Crypto.Cipher.DES


class Security:
    def __init__(self):
	self.cgibin = '../cgi-bin'
	self.isbeta = False
	self.read_version()
	self.set_env()
	self.read_config()
	self.cipher = Crypto.Cipher.DES.new(self.crypkey, Crypto.Cipher.DES.MODE_ECB)

    def read_version(self):
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

    def set_env(self):
	self.host = os.getenv('SERVER_NAME')
	if not self.host:
	    self.host = self.root + '.bamca.org'
	    os.putenv('SERVER_NAME', self.host)
	self.docroot = os.getenv('DOCUMENT_ROOT')
	if not self.docroot:
	    self.docroot = '/usr/local/www/bamca/' + self.root + '/htdocs'
	    os.putenv('DOCUMENT_ROOT', self.docroot)

    def read_config(self):
	cfgfile = open(self.htdocs_path + '/' + self.cgibin + '/.config').readlines()
	self.config = dict(map(lambda x: [x[0], dict(map(lambda y: y.split(','), x[1:]))], map(lambda x: x.strip().split('|'), cfgfile)))['.'.join(self.host.split('.')[-2:])]
	for c in self.config:
	    self.__dict__[c] = self.config[c].strip()

    def cookie_decode(self, val):
	return self.cipher.decrypt(Cookie._unquote(val)).strip()

    def cookie_encode(self, val):
	strval = str(val)
	strval += ' ' * (8 - len(strval) % 8)
	return Cookie._quote(self.cipher.encrypt(strval))



if __name__ == '__main__': # pragma: no cover
    pass
