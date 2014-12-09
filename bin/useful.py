#!/usr/local/bin/python

# Things that are generally useful but require nothing other
# than standard libraries.

import copy, filecmp, glob, os, pprint, stat
import config  # bleagh

if os.getenv('REQUEST_METHOD'):  # is this apache?  # pragma: no cover
    import cgitb; cgitb.enable()

#def form_int(val, defval=0):
#    try:
#       return int(val)
#    except:
#       return int(defval)


def read_dir(patt, tdir):
    odir = os.getcwd()
    os.chdir(tdir)
    flist = glob.glob(patt.strip())
    os.chdir(odir)
    return flist


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
    if ext:
        ext = ext[1:]
    return root, ext


def clean_name(f, morebad=''):
    badlist = [',', '#']

    n = f.strip()
    for b in badlist + list(morebad):
        n = n.replace(b[0], '_')
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
    if not os.path.exists(fname):
        if v:
            write_comment("is_good N", os.getcwd(), fname)
        return False
    st = os.stat(fname)
    if (st[stat.ST_MODE] & 0x004) == 0:
        if v:
            write_comment("is_good S", os.getcwd(), fname)
        return False
    if v:
        write_comment("is_good +", os.getcwd(), fname)
    return True


def render(fname):
    if is_good(fname):
        print open(fname).read()


def img_src(pth, alt=None, also={}):
    if 1:  #is_good(pth):
        return '<img src="../' + pth + '"' + fmt_also({'alt': alt}, also) + '>'
    return ''


def plural(thing):
    if len(thing) != 1:
        return 's'
    return ''


def dump_dict_comment(t, d, keys=None):
    print "<!-- dump", t, ":"
#    if not keys:
#       keys = d.keys()
#    keys.sort()
#    for k in keys:
#       print '   ', k, ':', d[k]
    pprint.pprint(d, indent=1, width=132)
    print '-->'


def dump_dict(t, d, keys=None):
    print "<p><h3>", t, "</h3><p>"
    print '<dl>'
    if not keys:
        keys = d.keys()
    keys.sort()
    for k in keys:
        print '<dt>', k, '<dd>', d[k]
    print '</dl>'


def fmt_also(also={}, style={}):
    nalso = dict_merge(style, also)
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
    for c in t2:
        if c in t1:
            return True
    return False


def bit_list(val, format="%02x"):
    olst = []
    bit = 1
    while val:
        if val & 1:
            olst.append(format % bit)
        val >>= 1
        bit *= 2
    return olst


# sobj is a list of word-like things, targ is a string
def search_match(sobj, targ):
    if not targ:
        return False
    if not sobj or not isinstance(targ, str):
        return True
    targ = targ.lower()
    for s in sobj:
        if not (targ.find(s.lower()) >= 0):
            return False
    return True


def warn(*message):
    print '<div class="warning">%s</div>' % ' '.join(message)


def file_mover(src, dst, mv=False, ov=False, inc=False, trash=False):  # pragma: no cover
    #print "file_mover", src, dst, mv, ov, inc, '<br>'
    addon = 0
    if dst and inc:
        root, ext = dst.rsplit('.', 1)  # for inc
    while 1:
        if src and dst and os.path.exists(src) and os.path.exists(dst) and os.path.samefile(src, dst):
            if not trash:
                warn("What?")
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
            file_mover(dst, os.path.join(config.LIB_DIR, 'trash', filename), mv=True, inc=True, trash=True)
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


# File-level globals.  Not to be imported by any other file.
pending_comments = list()
header_done_flag = False
def is_header_done():
    global header_done_flag
    return header_done_flag

def header_done():
    global header_done_flag, pending_comments
    header_done_flag = True
    map(lambda x: write_comment(*x), pending_comments)
    pending_comments = list()

partial_comment = None
def write_comment(*args, **kwargs):
    global header_done_flag, pending_comments, partial_comment
    partial = kwargs.get('nonl')
    if partial:
        if partial_comment is None:  # separate from empty list
            partial_comment = list()
        partial_comment.extend(args)
        args = ''
    elif partial_comment:
        args = partial_comment + list(args)
        partial_comment = None
    if args:
        if header_done_flag:
            print '<!--', ' '.join([str(x) for x in args]), '-->'
        else:
            pending_comments.append(args)

#---- -------------------------------------------------------------------

if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
