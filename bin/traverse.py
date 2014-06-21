#!/usr/local/bin/python

import os, stat
import basics
import files
import images
import useful


cols = 5

def ShowList(title, tdir, fl):
    if not fl:
	return
    clen = (len(fl) - 1) / cols + 1
    ffl = map(lambda x: fl[(x*clen):((x+1)*clen)], range(0, cols))
    print '<h4>%s (%d)</h4>' % (title, len(fl))
    print "<table width=100%><tr valign=top>"
    for cl in ffl:
	print "<td width=%d%%>" % (100/cols)
	for f in cl:
	    root,ext = useful.RootExt(f.strip())
	    fst = os.stat(tdir + '/' + f)
	    perms = fst[stat.ST_MODE]
	    if f[0] == '.':
		print '<i>%s</i><br>' % f
	    elif stat.S_ISDIR(perms):
		print '<a href="/cgi-bin/traverse.cgi?d=%s">%s</a><br>' % (tdir + '/' + f, f)
	    elif tdir.startswith('../'):
		#print '%s<br>' % f
		print '<a href="/cgi-bin/traverse.cgi?d=%s&f=%s">%s</a><br>' % (tdir, f, f)
	    elif f[-4:] == '.dat':
		#print '<a href="/cgi-bin/table.cgi?page=%s">%s</a><br>' % (tdir + '/' + f, f)
		print '<a href="/cgi-bin/traverse.cgi?d=%s&f=%s">%s</a><br>' % (tdir, f, f)
	    elif (perms & 5) == 0:
		print '%s<br>' % f
	    elif ext in images.itypes:
		#print '<a href="/cgi-bin/traverse.cgi?d=%s&f=%s">%s</a><br>' % (tdir, f, f)
		print '<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s">%s</a><br>' % (tdir, f, f)
	    else:
		print '<a href="../%s">%s</a><br>' % (tdir + '/' + f, f)
	print "</td>"
    print "</tr></table>"
    print '<br><hr>'


def ShowDir(pif, tdir, grafs=0):
    print '<hr>'

    dl, gl, ol, sl, xl = images.GetDir(tdir)

    ShowList("Directories", tdir, dl)

    if gl:
	if grafs:
	    print '<h4>Graphics (%d)</h4>' % len(gl)
	    for f in gl:
		perms = os.stat(tdir + '/' + f)[stat.ST_MODE]
		if (perms & 4) == 0:
		    print '%s<br>' % f
		elif grafs:
		    #print '<a href="/cgi-bin/traverse.cgi?d=%s&f=%s"><img src="../%s" border=0>%s</a><br>' % (tdir, f, tdir + '/' + f, f)
		    print '<a href="imawidget.cgi?d=%s&f=%s&cy=0"><img src="../%s" border=0>%s</a><br>' % (tdir, f, tdir + '/' + f, f)
		else:
		    print '<a href="../%s">%s</a><br>' % (tdir + '/' + f, f)
	    print '<br><hr>'
	else:
	    ShowList("Graphics", tdir, gl)

    ShowList("Data Files", tdir, sl)
    ShowList("Executable Files", tdir, xl)
    ShowList("Other Files", tdir, ol)

    if gl:
	print '<form action="traverse.cgi">'
	print '<a href="traverse.cgi?g=1&d=%s">%s</a> or ' % (tdir, pif.render.FormatButton('show all pictures'))
	print 'Pattern <input type="text" name="p">'
	print '<input type="hidden" name="d" value="%s">' % tdir
	print '<input type="checkbox" name="du" value="1"> Dupes'
	print '<input type="checkbox" name="sh" value="1"> Shelve'
	print pif.render.FormatButtonInput()
	print '</form>'

    print '<a href="upload.cgi?d=%s&m=%s">%s</a>' % (tdir, tdir[7:], pif.render.FormatButton('upload'))


def CheckDupes(pif, fn, shlv):
    root,ext = useful.RootExt(fn)
    flist = useful.ReadDir(root + '*' + ext, pif.render.pic_dir)
    flist.sort()
    if len(flist) > 1:
	Img(pif, flist, fn, shlv=shlv)


imginputs = '''<input type="checkbox" name="rm" value="%(f)s"> rm<input type="checkbox" name="mv" value="%(f)s %(b)s"> mv'''
imginput = '''<input type="checkbox" name="rm" value="%(f)s"> rm
<input type="text" name="ren.%(f)s"> rename
'''
def Img(pif, args, base='', shlv=False):
    print '<tr>'
    args.sort()
    for arg in args:
	root,ext = useful.RootExt(arg.strip())
	inp = ''
	if shlv:
	    inp += '''<input type="text" name="lib.%s"> lib''' % arg
	    print pif.render.FormatCell(0, '%s<br>%s%s' % (pif.render.FormatImageRequired([root], suffix=ext, also={"border":0}), arg, inp))
	    continue
	if arg == base:
	    inp = imginputs % {'f':arg,'b':root + 'z.' + ext}
	elif base:
	    inp = imginputs % {'f':arg,'b':base}
	else:
	    inp = imginput % {'f':arg}
	#inp += ' <a href="imawidget.cgi?d=%s&f=%s&cy=0">' % (pif.render.pic_dir, arg) + pif.render.FormatButton('edit') + '</a>'
	inp += ' ' + pif.render.FormatButton('edit', 'imawidget.cgi?d=%s&f=%s&cy=0' % (pif.render.pic_dir, arg))
	inp += ' ' + pif.render.FormatButton('stitch', 'stitch.cgi?fn_0=%s&submit=1&q=&fc=1' % (pif.render.pic_dir + '/' + arg))
	print pif.render.FormatCell(0, '<a href="../%s/%s">%s</a><br>%s%s' % (pif.render.pic_dir, arg, pif.render.FormatImageRequired([root], suffix=ext, also={"border":0}), arg, inp))
    print '</tr>'


def ShowImgs(pif, patt, dups, shlv):
    print '<hr>'
    print '<form action="traverse.cgi" method="post">'
    plist = patt.split(',')
    for pent in plist:
	flist = useful.ReadDir(pent, pif.render.pic_dir)
	flist.sort()
	print '<table>'
	for f in flist:
	    if dups:
		CheckDupes(pif, f, shlv)
	    else:
		Img(pif, [f], shlv=shlv)
	print '</table>'
	print '<hr>'
    print '<input type="hidden" name="d" value="%s">' % pif.render.pic_dir
    print '<input type="hidden" name="sc" value="1">'
    print pif.render.FormatButtonInput()
    print '<a href="upload.cgi?d=%s">%s</a>' % (pif.form.get('d', '.'), pif.render.FormatButton('upload'))
    print '</form>'


def ShowScript(pif, mvl, rml):
    pdir = pif.render.pic_dir
    if type(mvl) != type([]):
	mvl = [mvl]
    if type(rml) != type([]):
	rml = [rml]
    libl = map(lambda x: (x[4:], pif.form[x]), filter(lambda x: x.startswith('lib.'), pif.form.keys()))
    renl = map(lambda x: (x[4:], pif.form[x]), filter(lambda x: x.startswith('ren.'), pif.form.keys()))
    rend = dict(renl)
    print '<pre>'
    for ren in renl:
	fn = ren[1]
	if not '.' in fn:
	    fn += ren[0][ren[0].rfind('.'):]
	if not os.path.exists(fn):
	    #print 'ren', os.path.join(pdir, ren[0]) os.path.join(pdir, fn)
	    #os.rename(os.path.join(pdir, ren[0]) os.path.join(pdir, fn))
	    useful.FileMover(os.path.join(pdir, ren[0]), os.path.join(pdir, fn), mv=True, inc=True)
	else:
	    print '#ren', os.path.join(pdir, ren[0], os.path.join(pdir, fn))
    for lb in libl:
	dest = lb[1] # we might have renamed this...
	if lb[0] in rend:
	    lb[0] = rend[lb[0]]
	if not os.path.exists('lib/' + dest):
	    os.mkdir('lib/' + dest)
	#print 'lb', os.path.join(pdir, lb[0]), os.path.join('lib', dest, lb[0])
	#os.rename(os.path.join(pdir, lb[0]) os.path.join('lib', dest, lb[0]))
	useful.FileMover(os.path.join(pdir, lb[0]), os.path.join('lib', dest, lb[0]), mv=True, inc=True)
    for rm in rml:
	#print 'rm', rm
	if os.path.exists(os.path.join(pdir, rm)):
	    #os.unlink(os.path.join(pdir, rm))
	    useful.FileMover(os.path.join(pdir, rm), None, mv=True)
    for mv in mvl:
	#print 'mv', mv
	fsp = mv.split(' ')
	if os.path.exists(os.path.join(pdir, fsp[0])):
	    #os.rename(os.path.join(pdir, fsp[0]), os.path.join(pdir, fsp[1]))
	    useful.FileMover(os.path.join(pdir, fsp[0]), os.path.join(pdir, fsp[1]), mv=True, inc=True)
    print '</pre>'


def ShowFile(pif, fn):
    root, ext = useful.RootExt(fn)
    if ext == 'dat':
	ShowTable(pif, fn)
    elif ext in images.itypes:
	images.ShowPicture(pif, fn)
    else:
	print '<p>'
	print open(pif.render.pic_dir + '/' + fn).read().replace('\n', '<br>\n')



colors = ["#FFFFFF", "#CCCCCC"]


class TableFile(files.ArgFile):
    def __init__(self, fname):
	self.dblist = []
	files.ArgFile.__init__(self, fname)

    def ParseElse(self, llist):
	self.dblist.append(llist)



#print '<a href="/cgi-bin/table.cgi?page=%s">%s</a><br>' % (tdir + '/' + f, f)
def ShowTable(pif, pagename):
    tablefile = TableFile(pif.render.pic_dir + '/' + pagename)
    cols = '' # pif.form.get('cols', '')
    h = 0 # pif.FormInt('h')
    sorty = pif.form.get('sort')

    print pif.render.FormatTableStart()
    hdr = ''
    if h:
	hdr = tablefile.dblist[0]
	table = tablefile.dblist[1:]
    else:
	table = tablefile.dblist

    if sorty:
	global sortfield
	sortfield = int(sorty)
	table.sort(lambda x, y: cmp(x[sortfield].lower(), y[sortfield].lower()))

    row = 0
    icol = irow = 0
    if 'y' in cols:
	icol = cols.find('y')
    id = ''
    for line in table:
	if line[icol] != id:
	    id = line[icol]
	    irow = (irow + 1) % 2
	if not row:
	    row = h
	    iarg = 0
	    print '<tr>'
	    for ent in range(0,len(hdr)):
		if ent >= len(cols) or cols[ent].lower() != 'n':
		    #print "<th>"+hdr[ent]+"</th>"
		    print '<th bgcolor="#FFFFCC"><a href="table.cgi?page=%s&sort=%d&h=%d&cols=%s">%s</th>' % (pagename, iarg, h, cols, hdr[ent])
		iarg = iarg + 1
	    print "</tr>\n<tr>"
	print '<tr bgcolor="%s">' % colors[irow]
	row = row - 1
	for ent in range(0,len(line)):
	    if ent >= len(cols) or cols[ent].lower() != 'n':
		print "<td>"+line[ent]+"</td>"
	print "</tr>"
    print pif.render.FormatTableEnd()


def DoAction(pif, tdir, fn, act):
    print '<div class="warning">'
    nfn = images.Action(pif, tdir, fn, act)
    print '</div><br>'
    if nfn:
	images.ShowPicture(pif, nfn)
    else:
	ShowDir(pif, tdir, 0)


def Main(pif):
    global cols
    os.environ['PATH'] += ':/usr/local/bin'
    pif.render.PrintHtml()
    pif.Restrict('a')
    #pif.render.title = '<a href="traverse.cgi?d=%s">%s</a>' % (pif.form.get("d", '.'), pif.form.get("d", '.'))
    pif.render.title = pif.render.pic_dir = pif.form.get("d", '.')
    pif.render.title += '/' + pif.form.get("f", "")
    graf = pif.FormInt("g")
    fnam = pif.form.get("f", '')
    patt = pif.form.get("p", '')
    cols = pif.FormInt("c", 5)
    dups = pif.FormInt("du")
    shlv = pif.FormInt("sh")
    scrt = pif.FormInt('sc')
    act = pif.FormInt('act')
    images.cycle = pif.FormInt("cy")

    print pif.render.FormatHead(extra=pif.render.increment_js)
    print pif.form
    if patt:
	ShowImgs(pif, patt, dups, shlv)
    elif scrt:
	ShowScript(pif, pif.form.get('mv', []), pif.form.get('rm', []))
    elif act:
	DoAction(pif, pif.render.pic_dir, fnam, act)
    elif fnam:
	ShowFile(pif, fnam)
    else:
	ShowDir(pif, pif.render.pic_dir, graf)
    print pif.render.FormatTail()


if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
