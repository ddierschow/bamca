#!/usr/local/bin/python

# Things that are generally useful but require nothing other
# than standard libraries.

import copy, filecmp, glob, os, stat
os.environ['PYTHON_EGG_CACHE'] = '/var/tmp'
if os.getenv('REQUEST_METHOD'): # pragma: no cover
    import cgitb; cgitb.enable()

def FormInt(val, defval=0):
    try:
	return int(val)
    except:
	return int(defval)


def ReadDir(patt, tdir):
    odir = os.getcwd()
    os.chdir(tdir)
    flist = glob.glob(patt.strip())
    os.chdir(odir)
    return flist


def RootExt(fn):
    root, ext = os.path.splitext(fn)
    if ext:
	ext = ext[1:]
    return root,ext


def CleanName(f, morebad=''):
    badlist = [',', '#']

    n = f.strip()
    for b in badlist + list(morebad):
	n = n.replace(b[0], '_')
#    c = n.count('.')
#    if c > 0:
#	n = n.replace('.', '_', c - 1)
    return n


def IsGood(fname, v=True):
    fname = os.path.normpath(fname)
    if not fname:
	if v:
	    WriteComment("IsGood B", os.getcwd(), fname)
	return False
    if not os.path.exists(fname):
	if v:
	    WriteComment("IsGood N", os.getcwd(), fname)
	return False
    st = os.stat(fname)
    if (st[stat.ST_MODE] & 0x004) == 0:
	if v:
	    WriteComment("IsGood S", os.getcwd(), fname)
	return False
    if v:
	WriteComment("IsGood +", os.getcwd(), fname)
    return True


def Render(fname):
    if IsGood(fname):
	print file(fname).read()


def ImgSrc(pth, alt=None, also={}):
    if 1:#IsGood(pth):
	return '<img src="../' + pth + '"' + Also({'alt':alt}, also) + '>'
    return ''


def Plural(thing):
    if len(thing) != 1:
	return 's'
    return ''


def DumpDictComment(t, d, keys={}):
    print "<!-- Dump",t,":"
    if not keys:
	keys = d.keys()
    keys.sort()
    for k in keys:
	print '   ', k, ':', d[k]
    print '-->'


def DumpDict(t, d, keys={}):
    print "<p><h3>",t,"</h3><p>"
    print '<dl>'
    if not keys:
	keys = d.keys()
    keys.sort()
    for k in keys:
	print '<dt>', k, '<dd>', d[k]
    print '</dl>'


def Also(also={}, style={}):
    nalso = DictMerge(style, also)
    ostr = ''
    for tag in nalso:
	if nalso.get(tag):
	    ostr = ostr + ' %s="%s"' % (tag, nalso[tag])
    return ostr


def DictMerge(*dicts):
    out_dict = dict()
    for in_dict in dicts:
	out_dict.update(in_dict)
    return out_dict


def SetAndAddList(d, k, l):
    d.setdefault(k, [])
    d[k].extend(l)


def AnyCharMatch(t1, t2):
    for c in t2:
	if c in t1:
	    return True
    return False


def BitList(val, format="%02x"):
    olst = []
    bit = 1
    while val:
	if val & 1:
	    olst.append(format % bit)
	val >>= 1
	bit *= 2
    return olst


# sobj is a list of word-like things, targ is a string
def SearchMatch(sobj, targ):
    if not targ:
	return False
    if not sobj or type(targ) != str:
	return True
    targ = targ.lower()
    for s in sobj:
	if not (targ.find(s.lower()) >= 0):
	    return False
    return True


def FileMover(src, dst, mv=False, ov=False, inc=False, trash=False): # pragma: no cover
    #print "FileMover", src, dst, mv, ov, inc, '<br>'
    addon = 0
    if dst and inc:
	root, ext = dst.rsplit('.', 1) # for inc
    while 1:
	if src and dst and os.path.exists(src) and os.path.exists(dst) and os.path.samefile(src, dst):
	    if not trash:
		print "What?"
	    return False
	if not os.path.exists(src):
	    if not trash:
		print src, "- source not found"
	elif dst == None:
	    if mv:
		FileDelete(src)
	    else:
		if not trash:
		    print "Eh?"
		return False
	elif not os.path.exists(dst):
	    if mv:
		FileMove(src, dst)
	    else:
		FileCopy(src, dst)
	elif filecmp.cmp(src, dst, False):
	    if mv:
		os.remove(src)
		if not trash:
		    print src, "- source removed"
	    else:
		if not trash:
		    print "files are identical"
	elif ov:
	    #os.remove(dst)
	    path, filename = dst.rsplit('/', 1)
	    FileMover(dst, 'lib/trash/' + filename, mv=True, inc=True, trash=True)
	    if not trash:
		print dst, "- old file overwritten"
	    if mv:
		FileMove(src, dst)
	    else:
		FileCopy(src, dst)
	elif inc:
	    addon += 1
	    dst = root + '-' + str(addon) + '.' + ext
	    continue
	else:
	    if not trash:
		print "- destination exists"
	    return False
	return True


def FileMove(src, dst, ov=False, trash=False): # pragma: no cover
    if not trash:
	print "mv", src, dst
    os.rename(src, dst)
    return True


def FileDelete(src, trash=False): # pragma: no cover
    if not trash:
	print "rm", src
    if not os.path.exists(src):
	if not trash:
	    print "- not found"
    else:
	try:
	    os.unlink(src)
	    if not trash:
		print "- removed"
	except:
	    if not trash:
		print "- failed"
	    return False
    return True


def FileCopy(src, dst, trash=False): # pragma: no cover
    if not trash:
	print "copy", src, dst
    try:
	open(dst, 'w').write(open(src).read())
    except:
	if not trash:
	    print "- failed"
    return False


pending_comments = list()
header_done = False
def HeaderDone():
    global header_done, pending_comments
    header_done = True
    map(lambda x: WriteComment(*x), pending_comments)
    pending_comments = list()

def WriteComment(*args):
    global header_done, pending_comments
    if header_done:
	print '<!--', ' '.join(map(lambda x: str(x), args)), '-->'
    else:
	pending_comments.append(args)


#---- -------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
