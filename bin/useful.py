#!/usr/local/bin/python

# Things that are generally useful but require nothing other
# than standard libraries.

import copy, filecmp, glob, itertools, os, pprint, random, re, stat, string, urllib, urllib2
import config  # bleagh
import jinja2

#html_done = False

alnum = string.digits + string.ascii_lowercase

if os.getenv('REQUEST_METHOD'):  # is this apache?  # pragma: no cover
    import cgitb; cgitb.enable()


class DelayedRedirect(Exception):
    def __init__(self, value, delay=10):
        self.value = value
	self.delay = delay

    def __str__(self):
        return repr(self.value)


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
	if isinstance(lord, int) or isinstance(lord, long):
	    return str(lord)
	return unicode(lord, errors='ignore')
    for ent in lord:
	for key, val in ent.items():
	    if isinstance(val, str):
		val = unicode(val, errors='ignore')
	    else:
		val = str(val)
	    ent[key] = val
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
#    c = n.count('.')
#    if c > 0:
#       n = n.replace('.', '_', c - 1)
    return n


def is_good(fname, v=True):
    fname = os.path.normpath(fname)
    if not fname:
        if v:
            write_comment("is_good B", os.getcwd(), fname)
        return False
    try:
	if not os.path.exists(fname):
	    if v:
		write_comment("is_good N", os.getcwd(), fname)
	    return False
    except:
	write_comment("is_good X1", os.getcwd(), fname)
	return False
    try:
	st = os.stat(fname)
    except:
	write_comment("is_good X2", os.getcwd(), fname)
	return False
    if (st[stat.ST_MODE] & 0x004) == 0:
        if v:
            write_comment("is_good S", os.getcwd(), fname)
        return False
    if v:
        write_comment("is_good +", os.getcwd(), fname)
    return True


def render_file(fname):
    if is_good(fname):
        return open(fname).read()


def img_src(pth, alt=None, also={}):
    return '<img src="../' + pth + '"' + fmt_also({'alt': alt}, also) + '>'


def plural(thing):
    return 's' if len(thing) != 1 else ''


def make_alnum(thing):
    output = []
    for ch in list(thing):
	if ch not in alnum:
	    break
	output.append(ch)
    return ''.join(output)


def generate_token(number_digits=10):
    return ''.join([alnum[random.randrange(len(alnum))] for x in range(0, number_digits)])


id_re = re.compile('[-/\w.]+')  # 0-9 A-Z a-z underscore dash slash dot
def clean_id(str_id):
    id_m = id_re.match(str_id)
    return id_m.group(0) if id_m else ''


def dump_dict_comment(t, d, keys=None):
    ostr = "<!-- dump %s:\n" % t
    ostr += pprint.pformat(d, indent=1, width=132)
    return ostr + '\n-->\n'


def dump_dict(t, d, keys=None):
    return '%s<br>\n%s\n' % (t, pprint.pformat(d, indent=1, width=132))


def fmt_also(also={}, style={}):
    nalso = dict(style)
    nalso.update(also)
    ostr = ''
    for tag in nalso:
        if nalso.get(tag):
            ostr = ostr + ' %s="%s"' % (tag, nalso[tag])
    return ostr


def dict_merge(*dicts):
    out_dict = dict()
    for in_dict in dicts:
        out_dict.update(in_dict)
    return out_dict


def set_and_add_list(d, k, l):
    d.setdefault(k, [])
    d[k].extend(l)


def any_char_match(t1, t2):
    return bool(set(list(t1)) & set(list(t2)))


def bit_list(val, format="%02x"):
    olst = []
    bit = 1
    while val:
        if val & 1:
            olst.append(format % bit)
        val >>= 1
        bit *= 2
    return olst


def reflect(in_iter, columns, pad=None):
    '''Reflects an interator carved up into chunks, padding with None.

    >>> reflect([0,1,2,3], 3)
    [0, 2, 1, 3, None, None]
    '''
    nents = len(in_iter)
    if nents < columns:
	return in_iter
    colsize = (len(in_iter) - 1) / columns + 1
    return itertools.chain(*itertools.izip_longest(*[in_iter[x:x + colsize] for x in range(0,
	colsize * columns,
	#len(in_iter),
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


def file_touch(dst):
    os.utime(dst, None)


def file_mover(src, dst, mv=False, ov=False, inc=False, trash=False):  # pragma: no cover
    warn("file_mover", src, dst, "mv=", mv, "ov=", ov, "inc=", inc, "trash=", trash)
    addon = 0
    if dst and inc:
        root, ext = dst.rsplit('.', 1)  # for inc
    while 1:
        if src and dst and os.path.exists(src) and os.path.exists(dst) and os.path.samefile(src, dst):
            if not trash:
                warn("What? (trash)")
            return False
        if not os.path.exists(src):
            if not trash:
                warn(src, "- source not found")
        elif dst is None:
            if mv:
                file_delete(src)
            else:
                if not trash:
                    warn("Eh?")
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
                    warn(src, "- source removed")
            else:
                if not trash:
                    warn("files are identical")
        elif ov:
            #os.remove(dst)
            path, filename = dst.rsplit('/', 1)
            file_mover(dst, relpath('.', config.TRASH_DIR, filename), mv=True, inc=True, trash=True)
            if not trash:
                warn(dst, "- old file overwritten")
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
                warn("- destination exists")
            return False
        return True


def file_move(src, dst, ov=False, trash=False):  # pragma: no cover
    if not trash:
        warn("mv", src, dst)
    os.rename(src, dst)
    return True


def file_delete(src, trash=False):  # pragma: no cover
    if not trash:
        warn("rm", src)
    if not os.path.exists(src):
        if not trash:
            warn("- not found")
    else:
        try:
            os.unlink(src)
            if not trash:
                warn("- removed")
        except:
            if not trash:
                warn("- failed")
            return False
    return True


def file_copy(src, dst, trash=False):  # pragma: no cover
    if not trash:
        warn("copy", src, dst)
    try:
        open(dst, 'w').write(open(src).read())
    except:
        if not trash:
            warn("- failed")
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

    c = ["/usr/bin/file", "-b", pdir + '/' + fn]
    p = subprocess.Popen(c, stdout=subprocess.PIPE, stderr=None, close_fds=True)
    l = p.stdout.readlines()
    if not l:
        return fn
    l = l[0].strip()

    for typ in types:
        if l.startswith(typ[0]):
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
    if not os.path.exists(pdir):
        os.mkdir(pdir, 0775)
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
    open(pdir + '/' + fn, 'w').write(contents)
    return fn


def show_error():
    import traceback
    print traceback.format_exc()


# File-level globals.  Not to be imported by any other file.
_format_web = True
_pending_comments = list()
_header_done_flag = False
_partial_comment = None

def is_header_done(new_set=False):
    global _header_done_flag
    if new_set:
	_header_done_flag = True
    return _header_done_flag

def header_done(is_web=True, silent=False):
    global _format_web, _pending_comments
    _format_web = is_web
    is_header_done(True)
    ostr = '\n'.join([format_string(*x) for x in _pending_comments])
    _pending_comments = list()
    if silent:
	return ostr
    if ostr:
	print ostr

def warn(*args, **kwargs):
    write_string(*args, nonl=kwargs.get('nonl', False), warning=True, comment=False)

def write_message(*args, **kwargs):
    write_string(*args, nonl=kwargs.get('nonl', False), warning=False, comment=False)

def write_comment(*args, **kwargs):
    write_string(*args, nonl=kwargs.get('nonl', False), warning=False, comment=True)

def write_string(*args, **kwargs):
    ostr = format_string(*args, **kwargs)
    if ostr:
	print ostr

def format_string(*args, **kwargs):
    global _pending_comments, _partial_comment, _format_web
    partial = kwargs.get('nonl')
    warning = kwargs.get('warning', False)
    comment = kwargs.get('comment', False)
    if args and not _partial_comment:
	if warning:
	    args = ('!',) + args
	if comment:
	    args = ('#',) + args
    if partial:
        if _partial_comment is None:  # separate from empty list
            _partial_comment = list()
        _partial_comment.extend(args)
        args = []
    elif _partial_comment:
        args = _partial_comment + list(args)
        _partial_comment = None
    if args:
        if not is_header_done():
            _pending_comments.append(args)
	elif not _format_web:
            return ' '.join([str(x) for x in args])
        elif args[0] == '#':
	    return '<!-- ' + ' '.join([str(x) for x in args[1:]]) + ' -->'
        elif args[0] == '!':
	    return '<div class="warning">%s</div>' % ' '.join([str(x) for x in args[1:]])
	else:
	    return ' '.join([str(x) for x in args]) + '<br>'
    return ''

def read_comments():
    global _pending_comments
    comments = '\n'.join([' '.join([str(arg) for arg in args]) for args in _pending_comments])
    _pending_comments = list()
    return comments


def render_template(template, **kwargs):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader('../templates'))
    tpl = env.get_template(template)
    return tpl.render(comments=read_comments(), **kwargs)


def url_fetch(url, data=None):
    #fn = os.path.basename(url)
    #url = urllib.quote(url, ':/')
    img = ''
    finished_len = 0
    tries = 3
    retry = 0
    content_len = None
    if data:
	data = urllib.urlencode(data)
    while retry < tries:
	retry += 1
	try:
	    url_file = urllib2.urlopen(url, data, 90)
	    img = ''
	    if content_len == None and 'content-length' in url_file.info():
		content_len = int(url_file.info()['content-length'])
	    img_add = ''
	    while 1:
		buf = url_file.read()
		if not buf:
		    break
		img_add += buf
	    img += img_add
	    finished_len = len(img)
	    if not content_len or (finished_len >= content_len):
		break
	    else:
		pass
	except KeyboardInterrupt:
	    raise
	except urllib2.HTTPError:
	    img = ''
	    break
	except:
	    img = ''
	time.sleep(2)
    return img


def command_help(script, cmds):
    # cmds is list of (cmd, function, help message)
    write_message("./%s [%s] ..." % (script, '|'.join([x[0] for x in cmds])))
    for cmd in cmds:
	write_message("  %s for %s" % (cmd[0], cmd[2]))


def cmd_proc(pif, script, cmds):
    if pif.filelist:
	lup = {x[0]: x[1] for x in cmds}
	lup.get(pif.filelist[0], command_help)(pif, *pif.filelist[1:])
    else:
	command_help(script, cmds)
