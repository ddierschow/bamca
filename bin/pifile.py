#!/usr/local/bin/python

import cgi, copy, datetime, getopt, os, stat, sys, time
if os.getenv('REQUEST_METHOD'):  # is this apache?  # pragma: no cover
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
        self.args = args  # this is for unittest only!
        self.argv = []  # this is for command line only!
        self.unittest = bool(args)
        self.form = self.get_form()
        self.page_id = self.get_page_id(page_id, form_key, defval)
        self.page_name = self.page_id[self.page_id.rfind('.') + 1:]
        self.time_start = datetime.datetime.now().strftime('%Y%m%d.%H%M%S')
        self.request_uri = os.environ.get('REQUEST_URI', 'unknown')
        self.remote_host = os.environ.get('REMOTE_HOST', 'host_unset')
        self.remote_addr = os.environ.get('REMOTE_ADDR', '127.0.0.1')
        self.set_server_env()
        self.secure = secure.Security()
        self.htdocs = self.secure.docroot
        self.format_type = 'python'
        self.render = render.Presentation(self.page_id, self.form_int('verbose'))
        self.render.secure = self.secure
        self.render.comment('form', self.form)
        self.rawcookies = self.secure.get_cookies()
        self.id = int(self.rawcookies.get('id', '0'))
        self.privs = self.rawcookies.get('pr', '')
        self.secure.cookies = self.rawcookies.get('co')
        if self.is_allowed(dbedit):
            self.secure.set_config('edit')

        os.chdir(self.secure.docroot)
        self.cwd = os.getcwd()
        self.render.isbeta = self.secure.isbeta
        self.cgibin = '../cgi-bin'
        self.render.simple = int(self.form_int("simple"))

        self.dbh = dbhand.DBHandler(self.secure.config, self.id, self.render.verbose)
        self.dbh.dbi.nowrites = self.unittest
        self.render.set_page_info(self.dbh.fetch_page(self.page_id))
        self.render.not_released = (self.render.flags & self.dbh.FLAG_PAGE_INFO_NOT_RELEASED) != 0
        self.render.hide_title = (self.render.flags & self.dbh.FLAG_PAGE_INFO_HIDE_TITLE) != 0
        self.log_start()

    def set_server_env(self):
        self.server_name = os.environ.get('SERVER_NAME', 'unset.server.name')
        parts = self.server_name.split('.')
        if len(parts) > 2:
            config.ENV = parts[-3]
        elif len(parts) == 2:
            config.ENV = 'www'

    def log_start(self):
        if not self.is_allowed('m') and not self.args:
            self.dbh.increment_counter(self.page_id)
            log_name = os.path.join(config.LOG_ROOT, config.ENV + datetime.datetime.now().strftime('.url%Y%m.log'))
            try:
                open(log_name, 'a').write('%s %s %s\n' % (self.time_start, self.remote_addr, self.request_uri))
            except:
                pass

    def get_page_id(self, page_id, form_key, defval):
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

    def get_form(self):
        '''Reads the cgi form and puts it into this object.'''
        form = dict()
        if 'REQUEST_METHOD' in os.environ:  # is this apache?
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
                elif 'filename' in self.cgiform[field].__dict__:
                    fn = self.cgiform[field].filename
                    form[field + '.name'] = fn
                    form[field] = self.cgiform[field].value
                else:
                    form[field] = self.cgiform[field].value

        elif self.args:  # faking for unit tests
            for fl in self.args.split():
                if '=' in fl:
                    spl = fl.split('=')
                    form[spl[0]] = spl[1]

        else:  # faking from command line
            self.argv = sys.argv[1:]  # command line utils will use this and ignore form.
            for fl in sys.argv:
                if '=' in fl:
                    spl = fl.split('=')
                    form[spl[0]] = spl[1]

        return form

    def form_set(self, key, val):
        self.form[key] = val

    def form_def(self, key, val):
        self.form.setdefault(key, val)

    def form_del(self, key):
        if key in self.form:
            del self.form[key]

    def form_has(self, key):
        return key in self.form

    def form_int(self, key, defval=0):
        try:
            return int(self.form[key])
        except:
            return int(defval)

    def form_bool(self, key, defval=False):
        try:
            return bool(self.form[key])
        except:
            return bool(defval)

    def form_str(self, key, defval=''):
        try:
            return str(self.form[key])
        except:
            return str(defval)

    def form_list(self, key, defval=None):
        val = self.form.get(key, defval)
        if val is None:
            return list()
        if not isinstance(val, list):
            return [val]
        return val

    def form_keys(self, start='', end='', has=''):
        return filter(lambda x: x.startswith(start) and x.endswith(end) and has in x, self.form.keys())

    def form_find(self, field):
        keys = list()
        for key in self.form.keys():
            if key == field or key.startswith(field + '.'):
                keys.append(key)
        return keys

    def form_reformat(self, fields):
        return '&'.join(['%s=%s' % (x, self.form_str(x)) for x in fields])

    def form_where(self, cols=None, prefix=""):
        if not cols:
            cols = self.form.keys()
        wheres = list()
        for col in cols:
            if prefix + col in self.form:
                wheres.append(col + "='" + str(self.form_str(prefix + col)) + "'")
        return ' and '.join(wheres)

    def form_search(self, key):
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
            print '<meta http-equiv="refresh" content="0;url=..">'
            sys.exit(0)

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
        import traceback
        print traceback.format_exc()

#---- -------------------------------------------------------------------

if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
