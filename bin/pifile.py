#!/usr/local/bin/python

import cgi, copy, datetime, getopt, os, stat, sys, time
if os.getenv('REQUEST_METHOD'):  # is this apache?  # pragma: no cover
    import cgitb; cgitb.enable()

import config
import dbhand
import logger
import render
import secure
import useful

# The file environ.py modifies the environment upon first import.
# It sets PYTHON_EGG_CACHE; it adds /usr/local/bin to PATH;
# and it sets DOCUMENT_ROOT and SERVER_NAME if this is being run
# from the command line.  Since those change based on environment,
# environ.py has not be checked into github.
import environ

crawlers = [  # precluded from normal url tracking
    'Java/1.8.0_40',
    'Mozilla/5.0 (compatible; AhrefsBot/5.0; +http://ahrefs.com/robot/)',
    'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
    'Mozilla/5.0 (compatible; DotBot/1.1; http://www.opensiteexplorer.org/dotbot, help@moz.com)',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; MJ12bot/v1.4.5; http://www.majestic12.co.uk/bot.php?+)',
    'Mozilla/5.0 (compatible; MegaIndex.ru/2.0; +http://megaindex.com/crawler)',
    'Mozilla/5.0 (compatible; SeznamBot/3.2-test1; +http://fulltext.sblog.cz/)',
    'Mozilla/5.0 (compatible; SeznamBot/3.2; +http://fulltext.sblog.cz/)',
    'Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)',
    'Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)',
    'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53 (compatible; bingbot/2.0;  http://www.bing.com/bingbot.htm)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'SAMSUNG-SGH-E250/1.0 Profile/MIDP-2.0 Configuration/CLDC-1.1 UP.Browser/6.2.3.3.c.1.101 (GUI) MMP/2.0 (compatible; Googlebot-Mobile/2.1; +http://www.google.com/bot.html)',
    'bhcBot',
    'ia_archiver',
    'tbot-nutch/Nutch-1.10',
]

class BaseForm:
    def __init__(self, cgi_form, args):
        '''Reads the cgi form and puts it into this object.'''
        form = dict()
        if 'REQUEST_METHOD' in os.environ:  # is this apache?
            for key in cgi_form.keys():
		field = cgi_form[key]
                if isinstance(field, list):
                    form.setdefault(key, list())
		    form[key].extend([elem.value for elem in field])
                elif key.endswith('.x'):
                    key_root = key[:-2]
                    if key_root + '.y' in cgi_form:
                        form[key_root] = (field.value, cgi_form[key_root + '.y'].value)
                    else:
                        form[key] = field.value
                elif key.endswith('.y'):
                    if key[:-2] + '.x' not in cgi_form:
                        form[key] = field.value
                elif 'filename' in field.__dict__:
                    form[key + '.name'] = field.filename
                    form[key] = field.value
                else:
                    form[key] = field.value

	else:
            for fl in args:
                if '=' in fl:
                    spl = fl.split('=')
                    form[spl[0]] = spl[1]
	self.form = form

    def __repr__(self):
	return self.form.__repr__()

    def __str__(self):
	return self.form.__str__()

    def set_val(self, key, val):
        self.form[key] = val

    def default(self, key, val):
        self.form.setdefault(key, val)

    def delete(self, key):
        if key in self.form:
            del self.form[key]

    def has(self, key):
        return key in self.form

    def get_form(self):
	return self.form

    def get(self, key, defval=None):
	return self.form.get(key, defval)

    def get_int(self, key, defval=0):
        try:
            return int(self.form[key])
        except:
            return int(defval)

    def get_bool(self, key, defval=False):
        try:
            return bool(self.form[key])
        except:
            return bool(defval)

    def get_str(self, key, defval=''):
        try:
            return str(self.form[key])
        except:
            return str(defval)

    def get_list(self, key=None, start=None, defval=None):
	ret = list()
	if key:
	    val = self.form.get(key, defval)
	    if isinstance(val, list):
		ret.extend(val)
	    elif val is not None:
		ret.append(val)
	if start:
	    ret.extend([(x[len(start):], self.get_str(x)) for x in self.keys(start=start)])
	return ret

    def keys(self, start='', end='', has=''):
        return filter(lambda x: x.startswith(start) and x.endswith(end) and has in x, self.form.keys())

    def find(self, field):
        keys = list()
        for key in self.form.keys():
            if key == field or key.startswith(field + '.'):
                keys.append(key)
        return keys

    def reformat(self, fields):
        return '&'.join(['%s=%s' % (x, self.get_str(x)) for x in fields])

    def where(self, cols=None, prefix=""):
        if not cols:
            cols = self.form.keys()
        wheres = list()
        for col in cols:
            if prefix + col in self.form:
                wheres.append(col + "='" + str(self.get_str(prefix + col)) + "'")
        return ' and '.join(wheres)

    def search(self, key):
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

    def checks(self, *args):
	return [self.get_bool(x) for x in args]


class PageInfoFile:
    def __init__(self, page_id, form_key='', defval='', args='', dbedit=None):
        self.render = self.dbh = None
        self.secure = secure.Security()
        self.htdocs = self.secure.docroot
        config.IS_BETA = self.secure.is_beta
        self.rawcookies = self.secure.get_cookies()
        user_id = self.rawcookies.get('id', '0')
	if isinstance(user_id, str):
	    user_id = eval(user_id)
	if isinstance(user_id, (int, long)):
	    self.id = user_id
	elif isinsance(user_id, tuple):
	    user_id = user_id[0]
	config.USER_ID = self.user_id = user_id
        self.args = args  # this is for unittest only!
	if not args:
	    self.argv = sys.argv[1:]  # this is for command line only!
        self.unittest = bool(args)
        self.form = BaseForm(cgi.FieldStorage(), args.split() if args else self.argv)
        self.page_id = self.get_page_id(page_id, form_key, defval)
        self.page_name = self.page_id[self.page_id.rfind('.') + 1:]
        self.time_start = datetime.datetime.now().strftime('%Y%m%d.%H%M%S')
        self.request_uri = os.environ.get('REQUEST_URI', 'unknown')
        self.remote_host = os.environ.get('REMOTE_HOST', 'host_unset')
        self.remote_addr = os.environ.get('REMOTE_ADDR', '127.0.0.1')
        self.set_server_env()
	self.log = logger.Logger()
        self.format_type = 'python'
        self.render = render.Presentation(self.page_id, self.form.get_int('verbose'))
        self.render.secure = self.secure
        self.render.comment('form', self.form.get_form())
        self.privs = self.rawcookies.get('pr', '')
        self.secure.cookies = self.rawcookies.get('co')
        if self.is_allowed(dbedit):
            self.secure.set_config('edit')

        os.chdir(self.secure.docroot)
        self.cwd = os.getcwd()
        self.render.is_beta = self.secure.is_beta
        self.cgibin = '../cgi-bin'
        self.render.simple = int(self.form.get_int("simple"))

        self.dbh = dbhand.DBHandler(self.secure.config, self.user_id, self.log.dbq, self.render.verbose)
        self.dbh.dbi.nowrites = self.unittest
        self.render.set_page_info(self.dbh.fetch_page(self.page_id))
        self.render.not_released = (self.render.flags & self.dbh.FLAG_PAGE_INFO_NOT_RELEASED) != 0
        self.render.hide_title = (self.render.flags & self.dbh.FLAG_PAGE_INFO_HIDE_TITLE) != 0
	self.render.is_admin = self.is_allowed('a')
	self.render.is_moderator = self.is_allowed('m')
	self.render.is_user = self.is_allowed('u')
	self.render.is_viewer = self.is_allowed('v')
        self.log_start()
        if 'REQUEST_METHOD' not in os.environ:  # not apache!
	    useful.header_done(is_web=False)

    def set_server_env(self):
        self.server_name = os.environ.get('SERVER_NAME', 'unset.server.name')
        parts = self.server_name.split('.')
        if len(parts) > 2:
            config.ENV = parts[-3]
        elif len(parts) == 2:
            config.ENV = 'www'

    def log_start(self):
        if not self.is_allowed('m') and not self.args:
	    if os.getenv('HTTP_USER_AGENT', '') in crawlers:
		self.log.bot.info('%s %s' % (self.remote_addr, self.request_uri))
	    else:
		self.dbh.increment_counter(self.page_id)
		self.log.count.info(self.page_id)
		self.log.url.info('%s %s' % (self.remote_addr, self.request_uri))
		self.log.debug.info(os.getenv('HTTP_USER_AGENT'))
		refer = os.environ.get('HTTP_REFERER', '')
		if refer and not refer.startswith('http://www.bamca.org') and \
			     not refer.startswith('http://bamca.org') and \
			     not refer.startswith('http://beta.bamca.org'):
		    self.log.refer.info(refer)

    def get_page_id(self, page_id, form_key, defval):
        if form_key:
            if self.form.get_str(form_key):
                if self.form.get_str(form_key).startswith(page_id + '.'):
                    return self.form.get_str(form_key)
                else:
                    return page_id + '.' + self.form.get_str(form_key)
            elif defval:
                return page_id + '.' + defval
        elif not form_key and self.form.has('page'):
            return self.form.get_str('page')
        return page_id

    # -- access control -------------------------------------------------

    def is_allowed(self, priv):
        if priv is None:  # None = never allowed
            return False
        if priv == '':  # '' = always allowed
            return True
        if set(priv) & set(self.privs):
            self.render.comment('is_allowed', priv, self.privs, 'YES')
            return True
        return False

    def restrict(self, priv):  # pragma: no cover
        if not self.is_allowed(priv):
	    raise useful.Redirect('/')

    # -- debugging and error handling -----------------------------------

    def dump(self, verbose=False):
        if self.render.verbose or verbose:
            useful.dump_dict_comment('pifile', self.__dict__)
            useful.dump_dict_comment('pifile.render', self.render.__dict__)
            useful.dump_dict_comment('pifile.dbh', self.dbh.__dict__)

    def error_report(self):
        ostr = 'pifile = ' + str(self.__dict__) + '\n'
        ostr += 'render = ' + self.render.error_report() + '\n'
        ostr += 'dbh = ' + self.dbh.error_report() + '\n'
        return ostr

    def show_error(self):
	useful.show_error()

#---- -------------------------------------------------------------------

if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
