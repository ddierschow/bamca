#!/usr/local/bin/python

import cgi
import datetime
import os
import re
import sys
import time
import uuid

import config
import crawls
import dbhand
import logger
import mbdata
import render
import secure
import useful

if os.getenv('REQUEST_METHOD'):  # is this apache?  # pragma: no cover
    import cgitb
    cgitb.enable()

# The file environ.py modifies the environment upon first import.
# It sets PYTHON_EGG_CACHE; it adds /usr/local/bin to PATH;
# and it sets DOCUMENT_ROOT and SERVER_NAME if this is being run
# from the command line.  Since those change based on environment,
# environ.py has not been checked into github.
import enviro   # noqa


class BaseForm(object):
    def __init__(self, cgi_form=None, args=None, initform=None):
        '''Reads the cgi form and puts it into this object.'''
        if initform:
            self.form = initform
            return
        form = dict()
        if 'REQUEST_METHOD' in os.environ:  # is this apache?
            for key in cgi_form:
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
                elif hasattr(field, 'filename') and field.filename:
                    form[key + '.name'] = field.filename
                    form[key] = field.file.read() if field.file else None
                else:
                    form[key] = field.value

        else:
            for fl in args:
                if '=' in fl:
                    spl = fl.split('=')
                    form[spl[0]] = spl[1]
                else:
                    form[fl] = True
        self.form = form

    def __repr__(self):
        return self.form.__repr__()

    def __str__(self):
        return self.form.__str__()

    def __len__(self):
        return self.form.__len__()

    def __iter__(self):
        return self.form.__iter__()

    def __contains__(self, x):
        return self.form.__contains__(x)

    def set_val(self, key, val):
        self.form[key] = val

    def default(self, key, val):
        self.form.setdefault(key, val)

    def delete(self, key):
        if key in self.form:
            del self.form[key]

    def change_key(self, oldkey, newkey):
        if oldkey in self.form:
            self.form[newkey] = self.form[oldkey]
            self.delete(oldkey)

    def has(self, key):
        return key in self.form

    def has_any(self, keys):
        return any([key in self.form for key in keys])

    def get_form(self):
        return self.form

    def get(self, key, defval=None):
        return self.form.get(key, defval)

    def get_int(self, key, defval=0):
        try:
            return int(self.form[key])
        except Exception:
            return int(defval)

    def get_bool(self, key, defval=False):
        try:
            return bool(int(self.form[key]))
        except Exception:
            return bool(defval)

    def get_exists(self, key):
        return key in self.form

    def get_str(self, key, defval=''):
        try:
            return str(self.form[key])
        except Exception:
            return str(defval)

    def get_dir(self, key, defval=''):
        return mbdata.dirs.get(self.get_str(key, defval), self.get_str(key, defval))

    ALFA_RE = re.compile('[^-A-Za-z0-9_ ]+')

    def get_alnum(self, key, defval=''):
        return self.ALFA_RE.sub('', self.get_str(key, defval))

    def get_stru(self, key, defval=''):
        return self.get_str(key, defval).upper()

    def get_strl(self, key, defval=''):
        return self.get_str(key, defval).lower()

    def get_radio(self, key, value):
        return self.get_str(key) == value

    def get_id(self, key, limit=99, defval=''):
        try:
            return useful.clean_id(str(self.form[key][:limit]))
        except Exception:
            return useful.clean_id(str(defval[:limit]))

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

    def get_bits(self, key, start=None, base=16, defval=0):
        val = self.get_list(key, start, '0')
        return sum([int(x, base) for x in val]) if val else defval

    def keys(self, keylist=None, start='', end='', has='', sort=None):
        keylist = keylist if keylist else self.form.keys()
        keylist = [x for x in keylist if (x.startswith(start) and x.endswith(end) and has in x)]
        if sort is True:
            keylist.sort()
        elif sort:
            keylist.sort(key=sort)
        return keylist

    def roots(self, start='', end='', has=''):
        if end:
            return [x[len(start):-len(end)] for x in self.keys(start=start, end=end, has=has)]
        return [x[len(start):] for x in self.keys(start=start, end=end, has=has)]

    def get_dict(self, keylist=None, start='', end=''):
        lstart = len(start) if start else None
        lend = -len(end) if end else None
        return {key[lstart:lend]: self.get_str(key) for key in self.keys(keylist, start=start, end=end)}

    def find(self, field):
        return [key for key in self.form if key == field or key.startswith(field + '.')]

    def reformat(self, fields):
        return '&'.join(['%s=%s' % (x, self.get_str(x)) for x in fields])

    def where(self, cols=None, prefix=""):
        wheres = list()
        for col in cols if cols else self.form.keys():
            if prefix + col in self.form:
                wheres.append(col + "='" + str(self.get_str(prefix + col)) + "'")
        return ' and '.join(wheres)

    def search(self, key):
        obj = self.get_alnum(key, "").split()
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


class PageInfoFile(object):
    def __init__(self, page_id, form_key='', defval='', args='', dbedit=None):
        self.start_seconds = time.time()
        self.render = self.dbh = None
        self.secure = secure.Security()
        self.htdocs = self.secure.docroot
        config.IS_ALPHA = self.secure.is_alpha
        config.IS_BETA = self.secure.is_beta
        self.rawcookies = self.secure.get_cookies()
        self.unittest = bool(args)  # args comes from unittest only!
        self.argv = args.split() if args else sys.argv[1:]  # argv comes from command line only!
        self.form = BaseForm(cgi.FieldStorage(), self.argv)
        self.page_id = self.get_page_id(page_id, form_key, defval)
        self.page_name = self.page_id[self.page_id.rfind('.') + 1:]
        self.time_start = datetime.datetime.now().strftime('%Y%m%d.%H%M%S')
        self.request_uri = os.environ.get('REQUEST_URI', 'unknown')
        self.remote_host = os.environ.get('REMOTE_HOST', 'host_unset')
        self.remote_addr = os.environ.get('REMOTE_ADDR', '127.0.0.1')
        self.secure_host = 'https://' + self.secure.host
        self.secure_prod = self.secure_host.replace('beta', 'www')
        self.secure_prod = self.secure_host.replace('alpha', 'www')
        self.is_web = 'REQUEST_METHOD' in os.environ  # is apache!
        self.set_server_env()
        self.log = logger.Logger()
        self.format_type = 'python'
        self.render = render.Presentation(self.page_id, self.form.get_int('verbose'))
        self.render.secure = self.secure
        self.render.unittest = self.unittest
        self.render.comment('form', self.form.get_form())
        self.secure.cookies = self.rawcookies.get('co')
        self.privs = set()

        os.chdir(self.secure.docroot)
        self.cwd = os.getcwd()
        self.render.is_beta = self.secure.is_beta
        self.render.is_alpha = self.secure.is_alpha
        self.cgibin = '../cgi-bin'

        dbqlog = self.log.devnull if self.unittest else self.log.dbq
        self.dbh = dbhand.DBHandler(self.secure.config, 0, dbqlog, self.render.verbose)
        self.dbh.dbi.nowrites = self.unittest
        user_id = self.rawcookies.get('id', 0)
        if user_id:
            cookie = self.dbh.fetch_cookie(ckey=user_id)
            if cookie:
                user_id = cookie.user.id
                self.privs = set(cookie['user.privs']) & set(self.form.get_str('tprivs', 'bvuma'))
            else:
                user_id = 0
        config.USER_ID = self.user_id = user_id
        if self.is_allowed(dbedit):
            self.secure.set_config('edit')
            self.dbh.set_config(self.secure.config)
        self.render.is_admin = self.is_allowed('a')
        self.render.is_moderator = self.is_allowed('m')
        self.render.is_user = self.is_allowed('u')
        self.render.is_viewer = self.is_allowed('v')
        self.render.is_basic = self.is_allowed('b')

    def start(self):
        # self.log_start()
        self.set_user_info(self.user_id)
        self.set_page_info(self.page_id)
        if not self.is_web:
            useful.header_done(is_web=False)
        self.duplicate_form = self.form.has('token') and not self.dbh.insert_token(self.form.get_str('token'))

    def set_page_info(self, page_id):
        page_info = self.dbh.fetch_page(page_id)
        if not page_info:
            raise useful.SimpleError(
                'Your request is incorrect (bad page id, %s).  Please try something else.' % self.page_id,
                status=404)
        self.render.set_page_info(page_info)
        if self.render.flags & config.FLAG_PAGE_INFO_ADMIN_ONLY:
            self.restrict('a')
        if config.LOCKDOWN and not (self.render.flags & config.FLAG_PAGE_INFO_PUBLIC):
            self.restrict('b')
        self.render.not_released = (self.render.flags & config.FLAG_PAGE_INFO_HIDDEN) != 0
        self.render.hide_title = (self.render.flags & config.FLAG_PAGE_INFO_HIDE_TITLE) != 0

    def set_user_info(self, user_id):
        self.user = user = self.dbh.fetch_user(user_id)
        if not user:
            self.user_id = 0

    def set_server_env(self):
        self.server_name = os.environ.get('SERVER_NAME', 'unset.server.name')
        parts = self.server_name.split('.')
        if len(parts) > 2:
            config.ENV = parts[-3]
        elif len(parts) == 2:
            config.ENV = 'www'

    def is_external_referrer(self):
        refer = os.environ.get('HTTP_REFERER', '')
        return (refer and
                not refer.startswith('http://www.bamca.org') and
                not refer.startswith('http://bamca.org') and
                not refer.startswith('http://beta.bamca.org') and
                not refer.startswith('http://alpha.bamca.org') and
                not refer.startswith('https://www.bamca.org') and
                not refer.startswith('https://bamca.org') and
                not refer.startswith('https://beta.bamca.org') and
                not refer.startswith('https://alpha.bamca.org'))

    def log_start(self):
        if not self.argv and not self.is_allowed('m'):
            if os.getenv('HTTP_USER_AGENT', '') in crawls.crawlers:
                self.log.bot.info('%s %s' % (self.remote_addr, self.request_uri))
            else:
                self.dbh.increment_counter(self.page_id)
                self.log.count.info(self.page_id)
                self.log.url.info('%s %s' % (self.remote_addr, self.request_uri))
                if os.getenv('HTTP_USER_AGENT'):
                    self.log.debug.info(os.getenv('HTTP_USER_AGENT'))
                refer = os.environ.get('HTTP_REFERER', '')
                if self.is_external_referrer():
                    self.log.refer.info(refer)

    def get_page_id(self, page_id, form_key, defval):
        return useful.clean_id(self.calc_page_id(page_id, form_key, defval)[:20])

    def calc_page_id(self, page_id, form_key, defval):
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

    def create_token(self, name="token"):
        token = self.dbh.create_token()
        return self.render.format_form_token(token, name)

    # -- access control -------------------------------------------------

    def is_allowed(self, priv):
        if priv is None:  # None = never allowed
            return False
        if priv == '':  # '' = always allowed
            return True
        if set(priv) & self.privs:
            self.render.comment('is_allowed', priv, ''.join(self.privs), 'YES')
            return True
        return False

    def restrict(self, priv):  # pragma: no cover
        if not self.is_allowed(priv):
            raise useful.Redirect('/')
        if priv and self.user and not(self.user.flags & config.FLAG_USER_VERIFIED):
            raise useful.Redirect('/cgi-bin/validate.cgi')

    def create_cookie(self, user=None):
        user = user or self.user
        expire = (15 * 12 * 60 * 60) if ('a' in user.privs) else (60 * 365 * 24 * 60 * 60)
        ckey = str(uuid.uuid4())
        self.dbh.delete_cookie(user.id, ip=os.environ.get('REMOTE_ADDR', 'unset'))
        self.dbh.insert_cookie(user.id, ckey=ckey, ip=os.environ.get('REMOTE_ADDR', 'unset'),
                               expires=datetime.datetime.now() + datetime.timedelta(seconds=expire))
        self.render.set_cookie(self.render.secure.make_cookie(ckey, user.privs, expires=expire))

    # -- debugging and error handling -----------------------------------

    def error_report(self):
        import pprint
        ostr = 'pifile = ' + pprint.pformat(self.__dict__, indent=2, width=132) + "\n"
        ostr += 'render = ' + self.render.error_report() + '\n'
        ostr += 'dbh = ' + self.dbh.error_report() + '\n'
        return ostr

    def show_error(self):
        useful.show_error()
