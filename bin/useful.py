#!/usr/local/bin/python

# Things that are generally useful but require nothing other
# than standard libraries.

import filecmp
import glob
from io import open
import itertools
import jinja2
import os
import pprint
import random
import re
import stat
import string
import subprocess
from subprocess import PIPE
import urllib

import config  # bleagh

alnum = string.digits + string.ascii_lowercase
verbose = False

if os.getenv('REQUEST_METHOD'):  # is this apache?  # pragma: no cover
    import cgitb
    cgitb.enable()


class Redirect(Exception):
    def __init__(self, value, delay=0):
        self.value = value
        self.delay = delay

    def __str__(self):
        return repr(self.value)


class SimpleError(Exception):
    def __init__(self, value, status=404):
        self.value = value
        self.status = status

    def __str__(self):
        return repr(self.value)


class SimpleOjbect(object):
    def __init__(self, args):
        for key, value in args.items():
            self.setattr(key, value)


def relpath(*args):
    if len(args) == 0:
        return '.'
    if len(args) == 1:
        if args[0].startswith('/'):
            return args[0][1:]
        return args[0]
    if args[0] == '.':
        args = args[1:]
    if args[0].startswith('/'):
        args = (args[0][1:],) + args[1:]
    return os.path.join(*args)


def read_dir(patt, tdir):
    odir = os.getcwd()
    os.chdir(tdir)
    flist = glob.glob(patt.strip())
    os.chdir(odir)
    return flist


# still a work in progress
def printablize(lord):
    if lord is None:
        return '(None)'
    if isinstance(lord, dict):
        lord = [lord]
    elif not isinstance(lord, list):
        if isinstance(lord, int):
            return str(lord)
        return lord
    for ent in lord:
        for key, val in ent.items():
            ent[key] = str(val)
    return lord


def defang(thing):
    return str(thing).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def root_ext(fn):
    '''Split fn into root and ext.  In this case, ext has no dot.

    >>> root_ext('abc.def')
    ('abc', 'def')
    >>> root_ext('.abc')
    ('.abc', '')
    >>> root_ext('abc.')
    ('abc', '')
    >>> root_ext('abc')
    ('abc', '')
    >>> root_ext('')
    ('', '')
    '''
    root, ext = os.path.splitext(fn)
    if ext.startswith('.'):
        ext = ext[1:]
    return root, ext


def clean_name(f, morebad=''):
    badlist = [',', '#']

    n = f.strip()
    for b in badlist + list(morebad):
        n = n.replace(b, '_')
    # c = n.count('.')
    # if c > 0:
    #     n = n.replace('.', '_', c - 1)
    return n


def is_good(fname, v=False):
    fname = os.path.normpath(fname)
    if not fname:
        if v:
            msg.comment("is_good B", os.getcwd(), fname)
        return False
    try:
        if not os.path.exists(fname):
            if v:
                msg.comment("is_good N", os.getcwd(), fname)
            return False
    except Exception:
        msg.comment("is_good X1", os.getcwd(), fname)
        return False
    try:
        st = os.stat(fname)
    except Exception:
        msg.comment("is_good X2", os.getcwd(), fname)
        return False
    if (st[stat.ST_MODE] & 0x004) == 0:
        if v:
            msg.comment("is_good S", os.getcwd(), fname)
        return False
    if v:
        msg.comment("is_good +", os.getcwd(), fname)
    return True


def render_file(fname):
    if is_good(fname):
        return open(fname).read()


def img_src(pth, alt=None, also={}):
    pth = pth[1:] if pth.startswith('/') else pth
    return '<img src="../' + pth + '"' + fmt_also({'alt': alt}, also) + '>'


def plural(thing):
    val = thing if isinstance(thing, int) else len(thing)
    return 's' if val != 1 else ''


def make_alnum(thing):
    output = []
    for ch in list(thing):
        if ch not in alnum:
            break
        output.append(ch)
    return ''.join(output)


def generate_token(number_digits=10):
    return ''.join([alnum[random.randrange(len(alnum))] for x in range(0, number_digits)])


def pick(from_these):
    return random.choice(from_these)


def clean_id(str_id, limit=255):
    id_re = re.compile(r'[-/\w.]+')  # 0-9 A-Z a-z underscore dash slash dot
    id_m = id_re.match(str(str_id)[:limit])
    return id_m.group(0) if id_m else ''


def dump_dict_comment(t, d, keys=None):
    return ''
    return f"<!-- dump {t}:\n{pprint.pformat(d, indent=1, width=132)}\n-->\n"


def dump_dict(t, d, keys=None):
    return f'{t}<br>\n{pprint.pformat(d, indent=1, width=132)}\n'


def fmt_also(also={}, style={}):
    nalso = dict(style)
    nalso.update(also)
    return ''.join([f' {tag}="{val}"' for tag, val in nalso.items() if val])


def dict_merge(*dicts):
    out_dict = dict()
    for in_dict in dicts:
        out_dict.update(in_dict)
    return out_dict


def set_and_add_list(d, k, ln):
    d.setdefault(k, [])
    d[k].extend(ln)


def any_char_match(t1, t2):
    return bool(set(list(t1 or '')) & set(list(t2 or '')))


def bit_list(val, format="{:02x}"):
    olst = []
    bit = 1
    while val:
        if val & 1:
            olst.append(format.format(bit))
        val >>= 1
        bit *= 2
    return olst


def expand_number_list(lst):
    olst = []
    for n in lst:
        if '-' in n:
            s, e = n.split('-', 1)
            if s.isdigit() and e.isdigit():
                pat = '%%0%ds' % len(s)
                for n in range(int(s), int(e) + 1):
                    olst.append(pat % n)
                continue
        olst.append(n)
    return olst


def collapse_number_list(lst):
    intlist = []
    strlist = []
    maxlen = 0
    for ent in lst:
        try:
            val = int(ent)
        except Exception:
            pass
        else:
            maxlen = max(maxlen, len(str(ent)))
            intlist.append(val)
            continue

        try:
            ents = ent.split('-', 1)
            val1 = int(ents[0])
            val2 = int(ents[1])
        except Exception:
            pass
        else:
            maxlen = max(maxlen, len(str(ent[0])))
            maxlen = max(maxlen, len(str(ent[1])))
            intlist.extend(range(val1, val2 + 1))
            continue

        strlist.append(ent)

    str1 = "%%0%dd" % maxlen
    str2 = str1 + '-' + str1
    intlist.sort()
    start = None
    prev = None
    for val in intlist:
        if start is None:
            start = prev = val
        elif val == prev + 1:
            prev = val
        elif start == prev:
            strlist.append(str1 % start)
            start = prev = val
        else:
            strlist.append(str2 % (start, prev))
            start = prev = val
    if start is not None:
        if start == prev:
            strlist.append(str1 % start)
            start = None
        else:
            strlist.append(str2 % (start, prev))
            start = None

    return strlist


def reflect(in_iter, columns, pad=None):
    '''Reflects an interator carved up into chunks, padding with None.

    >>> reflect([0,1,2,3], 3)
    [0, 2, 1, 3, None, None]
    '''
    nents = len(in_iter)
    if nents < columns:
        return in_iter
    colsize = (len(in_iter) - 1) // columns + 1
    return itertools.chain(*itertools.zip_longest(*[in_iter[x:x + colsize] for x in range(
        0, colsize * columns,  # len(in_iter),
        colsize)], fillvalue=pad))


# sobj is a list of word-like things, targ is a string
def search_match(sobj, targ):
    if not targ:
        return False
    if not sobj or not isinstance(targ, str):
        return True
    targ = targ.lower()
    for s in sobj:
        if s.lower() not in targ:
            return False
    return True


def make_dir(dst, perms):
    if not os.path.exists(dst):
        msg.warn('making', dst)
        try:
            os.mkdir(dst, perms)
        except Exception as e:
            msg.warn('- failed -', e)


def file_touch(dst):
    os.utime(dst, None)


def file_mover(src, dst, mv=False, ov=False, inc=False, trash=False):  # pragma: no cover
    msg.warn("file_mover", src, dst, "mv=", mv, "ov=", ov, "inc=", inc, "trash=", trash)
    addon = 0
    if dst and inc:
        root, ext = dst.rsplit('.', 1)  # for inc
    while 1:
        if src and dst and os.path.exists(src) and os.path.exists(dst) and os.path.samefile(src, dst):
            if not trash:
                msg.warn("What? (trash)")
            return False
        if not os.path.exists(src):
            if not trash:
                msg.warn(src, "- source not found")
        elif dst is None:
            if mv:
                file_delete(src)
            else:
                if not trash:
                    msg.warn("Eh?")
                return False
        elif not os.path.exists(dst):
            if mv:
                file_move(src, dst)
            else:
                file_copy(src, dst)
        elif filecmp.cmp(src, dst, False):
            if mv:
                os.remove(src)
                if not trash:
                    msg.warn(src, "- source removed")
            else:
                if not trash:
                    msg.warn("files are identical")
        elif ov:
            # os.remove(dst)
            path, filename = dst.rsplit('/', 1)
            file_mover(dst, relpath('.', config.TRASH_DIR, filename), mv=True, inc=True, trash=True)
            if not trash:
                msg.warn(dst, "- old file overwritten")
            if mv:
                file_move(src, dst)
            else:
                file_copy(src, dst)
        elif inc:
            addon += 1
            dst = root + '-' + str(addon) + '.' + ext
            continue
        else:
            if not trash:
                msg.warn("- destination exists")
            return False
        return True


def file_move(src, dst, ov=False, trash=False):  # pragma: no cover
    if not trash:
        msg.warn("mv", src, dst)
    try:
        os.rename(src, dst)
    except Exception as e:
        msg.warn("- failed -", e)
    return True


def file_delete(src, trash=False):  # pragma: no cover
    if not trash:
        msg.warn("rm", src)
    if os.path.exists(src):
        try:
            os.unlink(src)
            if not trash:
                msg.warn("- removed")
        except Exception as e:
            if not trash:
                msg.warn("- failed -", e)
            return False
    elif not trash:
        msg.warn("- not found")
    return True


def file_copy(src, dst, trash=False):  # pragma: no cover
    if not trash:
        msg.warn("copy", src, dst)
    try:
        open(dst, 'wb').write(open(src, 'rb').read())
    except Exception as e:
        if not trash:
            msg.warn("- failed -", e)
    return False


def fix_file_type(pif, pdir, fn):
    types = [
        ('JPEG', 'jpg'),
        ('GIF', 'gif'),
        ('PC bitmap', 'bmp'),
        ('PNG', 'png'),
    ]
    if '.' in fn:
        root, ext = fn.rsplit('.', 1)
    else:
        root = fn
        ext = ''

    p = simple_process(("/usr/bin/file", "-b", pdir + '/' + fn,))
    lns = p.stdout.readlines()
    if not lns:
        return fn
    ln = lns[0].strip()

    for typ in types:
        if ln.startswith(typ[0]):
            ext = typ[1]

    nfn = root + '.' + ext
    if nfn == fn:
        return fn
    if os.path.exists(pdir + '/' + nfn):
        addon = 1
        while os.path.exists(pdir + '/' + root + '_' + str(addon) + '.' + ext):
            addon += 1
        root += '_' + str(addon)
    nfn = root + '.' + ext
    os.rename(pdir + '/' + fn, pdir + '/' + nfn)
    return nfn


def file_save(pdir, fn, contents, overwrite=False):
    make_dir(pdir, 0o775)
    if '.' in fn:
        root, ext = fn.rsplit('.', 1)
    else:
        root = fn
        ext = ''
    ext = ext.lower()
    root = clean_name(root, '!@$%^&*()[]{}~`<>"+/')
    ext = clean_name(ext, '!@$%^&*()[]{}~`<>"+/')
    fn = root + '.' + ext
    if os.path.exists(pdir + '/' + fn):
        if overwrite:
            file_mover(pdir + '/' + fn, relpath('.', config.TRASH_DIR, fn), mv=True, inc=True, trash=True)
        else:
            addon = 1
            while os.path.exists(pdir + '/' + root + '_' + str(addon) + '.' + ext):
                addon += 1
            root += '_' + str(addon)
    fn = root + '.' + ext
    open(pdir + '/' + fn, 'wb' if isinstance(contents, bytes) else 'wt').write(contents)
    return fn


class Messenger(object):

    def __init__(self):
        self._format_web = True
        self._pending_comments = list()
        self._header_done_flag = False
        self._partial_comment = None

    def reset(self):
        self._partial_comment = None

    def show_error(self):
        import traceback
        if self._format_web:
            print('<pre>')
        print(traceback.format_exc())
        if self._format_web:
            print('</pre>')

    def is_header_done(self, new_set=False):
        self._header_done_flag = self._header_done_flag or new_set
        return self._header_done_flag

    def header_done(self, is_web=True, silent=False):
        self._format_web = is_web
        self.is_header_done(True)
        ostr = '\n'.join([self._format_string(*x) for x in self._pending_comments])
        self._pending_comments = list()
        if silent:
            return ostr
        if ostr:
            print(ostr)

    def warn(self, *args, **kwargs):
        self._write_string(*args, nonl=kwargs.get('nonl', False), warning=True, comment=False)

    def write(self, *args, **kwargs):
        self._write_string(*args, nonl=kwargs.get('nonl', False), warning=False, comment=False)

    def write_debug(self, *args, **kwargs):
        if verbose:
            self._write_string(*args, nonl=kwargs.get('nonl', False), warning=False, comment=False)

    def comment(self, *args, **kwargs):
        self._write_string(*args, nonl=kwargs.get('nonl', False), warning=False, comment=True)

    def _write_string(self, *args, **kwargs):
        ostr = self._format_string(*args, **kwargs)
        if ostr:
            print(ostr)

    def _format_string(self, *args, **kwargs):
        partial = kwargs.get('nonl')
        warning = kwargs.get('warning', False)
        comment = kwargs.get('comment', False)
        if args and not self._partial_comment:
            if warning:
                args = ('!',) + args
            if comment:
                args = ('#',) + args
        if partial:
            if self._partial_comment is None:  # separate from empty list
                self._partial_comment = list()
            self._partial_comment.extend(args)
            args = []
        elif self._partial_comment:
            args = self._partial_comment + list(args)
            self._partial_comment = None
        if args:
            if not self.is_header_done():
                self._pending_comments.append(args)
            elif not self._format_web:
                return ' '.join([str(x) for x in args])
            elif args[0] == '#':
                return '<!-- ' + ' '.join([str(x) for x in args[1:]]) + ' -->'
            elif args[0] == '!':
                return '<div class="warning">{}</div>'.format(' '.join([str(x) for x in args[1:]]))
            else:
                return ' '.join([str(x) for x in args]) + '<br>'
        return ''

    def _read_comments(self):
        comments = '\n'.join([' '.join([str(arg) for arg in args]) for args in self._pending_comments])
        self._pending_comments = list()
        return comments


msg = Messenger()


def show_error():
    msg.show_error()


def is_header_done(new_set=False):
    return msg.is_header_done(new_set=new_set)


def header_done(is_web=True, silent=False):
    return msg.header_done(is_web=is_web, silent=silent)


def warn(*args, **kwargs):
    return msg.warn(*args, **kwargs)


def write_message(*args, **kwargs):
    return msg.write(*args, **kwargs)


def write_debug_message(*args, **kwargs):
    return msg.write_debug(*args, **kwargs)


def write_comment(*args, **kwargs):
    return msg.comment(*args, **kwargs)


def render_template(template, **kwargs):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('../templates'))
    tpl = env.get_template(template)
    return tpl.render(comments=msg._read_comments(), **kwargs)


def command_help(script, cmds):
    # cmds is list of (cmd, function, help message)
    msg.write("{} [{}] ...".format(script, '|'.join([x[0] for x in cmds])))
    for cmd, func, hlp in cmds:
        msg.write(f"  {cmd} for {hlp}")


def cmd_proc(pif, script, cmds):
    msg.header_done(False)
    if pif.filelist:
        lup = {x[0]: x[1] for x in cmds}
        if pif.filelist[0] in lup:
            return lup[pif.filelist[0]](pif, *pif.filelist[1:])
    command_help(script, cmds)


def pipe_chain(inp, pipes, stderr=None, verbose=True):
    procs = []
    ch = '%'
    for cmd in pipes:
        if verbose:
            msg.write(ch, ' '.join(cmd), nonl=True)
        ch = '|'
        procs.append(subprocess.Popen(cmd, stdin=inp, stdout=PIPE, stderr=stderr))
        # , text=True
        inp = procs[-1].stdout
    if verbose:
        msg.write()
    output = b''
    while True:
        o, e = procs[-1].communicate()
        output += o
        if procs[-1].returncode is not None:
            break
    return output


def simple_process(cmd, msg='', inp=PIPE, stderr=None, verbose=False):
    ch = '%'
    if verbose:
        msg.write(ch, ' '.join(cmd), nonl=True)
    proc = subprocess.Popen(cmd, stdin=inp, stdout=PIPE, stderr=stderr, text=True)
    output = ''
    o, e = proc.communicate(msg)
    while proc.returncode is None:
        output += o
        o, e = proc.communicate()
    return output


def url_quote(value, safe=None, plus=False):
    safe = safe if safe is not None else '' if plus else '/'
    return urllib.parse.quote_plus(value, safe) if plus else urllib.parse.quote(value, safe)


def make_button_name(name):
    return name.replace('<br>', '_').replace(' ', '_').lower()


def make_button_label(name):
    return name.replace('_', ' ').upper()


def setlist(wheat):
    # can't do list(set(dict)) so this effectively does it
    retval = list()
    for x in wheat:
        if x not in retval:
            retval.append(x)
    return retval


def count_exist(items):
    return len([1 for x in items if x])
