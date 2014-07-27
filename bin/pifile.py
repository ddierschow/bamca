#!/usr/local/bin/python

import cgi, copy, datetime, getopt, os, stat, sys, time
if os.getenv('REQUEST_METHOD'): # is this apache? # pragma: no cover
    import cgitb; cgitb.enable()

import config
import dbhand
import render
import secure
import useful

# The file environ.py modifies the environment upon first import.  
# It sets PYTHON_EGG_CACHE; it adds /usr/local/bin to PATH;
# and it sets DOCUMENT_ROOT and SERVER_NAME if this is being run
# from the command line.  Since those change based on environment,
# environ.py has not be checked into github.
import environ

class PageInfoFile():
    def __init__(self, page_id, form_key='', defval='', args='', dbedit=None):
	self.render = self.dbh = None
	self.args = args # this is for unittest only!
	self.argv = [] # this is for command line only!
	self.unittest = bool(args)
	self.form = self.GetForm()
	self.page_id = self.GetPageID(page_id, form_key, defval)
	self.page_name = self.page_id[self.page_id.rfind('.') + 1:]
	self.time_start = datetime.datetime.now().strftime('%Y%m%d.%H%M%S')
	self.request_uri = os.environ.get('REQUEST_URI', 'unknown')
	self.remote_host = os.environ.get('REMOTE_HOST', 'host_unset')
	self.remote_addr = os.environ.get('REMOTE_ADDR', '127.0.0.1')
	self.SetServerEnv()
	self.secure = secure.Security()
	self.htdocs = self.secure.docroot
	self.format_type = 'python'
	self.render = render.Presentation(self.page_id, self.FormInt('verbose'))
	self.render.secure = self.secure
	self.render.Comment('form', self.form)
	self.rawcookies = self.secure.GetCookies()
	self.id = int(self.rawcookies.get('id', '0'))
	self.privs = self.rawcookies.get('pr', '')
	self.secure.cookies = self.rawcookies.get('co')
	if self.IsAllowed(dbedit):
	    self.secure.SetConfig('edit')

	os.chdir(self.secure.docroot)
	self.cwd = os.getcwd()
	self.render.isbeta = self.secure.isbeta
	self.cgibin = '../cgi-bin'
	self.render.simple = int(self.FormInt("simple"))

	self.dbh = dbhand.dbhandler(self.secure.config, self.id, self.render.verbose)
	self.dbh.dbi.nowrites = self.unittest
	self.render.SetPageInfo(self.dbh.FetchPage(self.page_id))
	self.render.not_released = (self.render.flags & self.dbh.FLAG_PAGE_INFO_NOT_RELEASED) != 0
	self.render.hide_title = (self.render.flags & self.dbh.FLAG_PAGE_INFO_HIDE_TITLE) != 0
	self.LogStart()

    def SetServerEnv(self):
	self.server_name = os.environ.get('SERVER_NAME', 'unset.server.name')
	parts = self.server_name.split('.')
	if len(parts) > 2:
	    config.env = parts[-3]
	elif len(parts) == 2:
	    config.env = 'www'

    def LogStart(self):
	if not self.IsAllowed('m') and not self.args:
	    self.dbh.IncrementCounter(self.page_id)
	    log_name = os.path.join(config.logroot, config.env + datetime.datetime.now().strftime('.url%Y%m.log'))
	    try:
		open(log_name, 'a').write('%s %s %s\n' % (self.time_start, self.remote_addr, self.request_uri))
	    except:
		pass

    def GetPageID(self, page_id, form_key, defval):
	if form_key:
	    if self.form.get(form_key):
		if self.form[form_key].startswith(page_id + '.'):
		    return self.form[form_key]
		else:
		    return page_id + '.' + self.form[form_key]
	    elif defval:
		return page_id + '.' + defval
	elif not form_key and 'page' in self.form:
	    return self.form['page']
	return page_id

    # -- form stuff -----------------------------------------------------

    def GetForm(self):
	'''Reads the cgi form and puts it into this object.'''
	form = dict()
	if os.environ.has_key('REQUEST_METHOD'): # is this apache?
	    self.cgiform = cgi.FieldStorage()
	    for field in self.cgiform.keys():
		if isinstance(self.cgiform[field], list):
		    form.setdefault(field, [])
		    for elem in self.cgiform[field]:
			form[field].append(elem.value)
		elif field.endswith('.x') or field.endswith('.y'):
		    field_root = field[:-2]
		    if field_root + '.x' in self.cgiform and field_root + '.y' in self.cgiform:
			form[field_root] = (self.cgiform[field_root + '.x'].value, self.cgiform[field_root + '.y'].value)
		    else:
			form[field] = self.cgiform[field].value
		elif self.cgiform[field].__dict__.has_key('filename'):
		    fn = self.cgiform[field].filename
		    form[field + '.name'] = fn
		    form[field] = self.cgiform[field].value
		else:
		    form[field] = self.cgiform[field].value

	elif self.args: # faking for unit tests
	    for fl in self.args.split():
		if '=' in fl:
		    spl = fl.split('=')
		    form[spl[0]] = spl[1]

	else: # faking from command line
	    self.argv = sys.argv[1:] # command line utils will use this and ignore form.
	    for fl in sys.argv:
		if '=' in fl:
		    spl = fl.split('=')
		    form[spl[0]] = spl[1]

	return form

    def FormSet(self, key, val):
	self.form[key] = val

    def FormDef(self, key, val):
	self.form.setdefault(key, val)

    def FormDel(self, key):
	if key in self.form:
	    del self.form[key]

    def FormHas(self, key):
	return self.form.has_key(key)

    def FormInt(self, key, defval=0):
	try:
	    return int(self.form[key])
	except:
	    return int(defval)

    def FormBool(self, key, defval=False):
	try:
	    return bool(self.form[key])
	except:
	    return bool(defval)

    def FormStr(self, key, defval=''):
	try:
	    return str(self.form[key])
	except:
	    return str(defval)

    def FormList(self, key, defval=None):
	val = self.form.get(key, defval)
	if val == None:
	    return list()
	if not isinstance(val, list):
	    return [val]
	return val

    def FormKeys(self, start='', end='', has=''):
	return filter(lambda x: x.startswith(start) and x.endswith(end) and has in x, self.form.keys())

    def FormFind(self, field):
	keys = list()
	for key in self.form.keys():
	    if key == field or key.startswith(field + '.'):
		keys.append(key)
	return keys

    def FormReformat(self, fields):
	return '&'.join(['%s=%s' % (x, self.FormStr(x)) for x in fields])

    def FormWhere(self, cols=None, prefix=""):
	if not cols:
	    cols = self.form.keys()
	wheres = list()
	for col in cols:
	    if prefix + col in self.form:
		wheres.append(col + "='" + str(self.FormStr(prefix + col)) + "'")
	return ' and '.join(wheres)

    def FormSearch(self, key):
	obj = self.form.get(key, "").split()
	nob = []
	col = ''
	for w in obj:
	    if col:
		col = col + ' ' + w
		if col[-1] == '"':
		    nob.append(col[1:-1])
		    col = ''
	    elif w[0] == '"' and w[-1] != '"':
		col = w
	    else:
		nob.append(w)
	if col:
	    nob.append(col[1:])
	return nob

    # -- access control -------------------------------------------------

    def IsAllowed(self, priv):
	if priv == None: # None = never allowed
	    return False
	if priv == '': # '' = always allowed
	    return True
	if set(priv) & set(self.privs):
	    self.render.Comment('IsAllowed', priv, self.privs, 'YES')
	    return True
	return False

    def Restrict(self, priv): # pragma: no cover
	if not self.IsAllowed(priv):
	    print '<meta http-equiv="refresh" content="0;url=..">'
	    sys.exit(0)

    # -- debugging and error handling -----------------------------------

    def Dump(self, verbose=False):
	if self.render.verbose or verbose:
	    useful.DumpDictComment('pifile', self.__dict__)
	    useful.DumpDictComment('pifile.render', self.render.__dict__)
	    useful.DumpDictComment('pifile.dbh', self.dbh.__dict__)

    def ErrorReport(self):
	ostr = 'pifile = ' + str(self.__dict__) + '\n'
	ostr += 'render = ' + self.render.ErrorReport() + '\n'
	ostr += 'dbh = ' + self.dbh.ErrorReport() + '\n'
	return ostr

    def ShowError(self):
	import traceback
	print traceback.format_exc()

#---- -------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
