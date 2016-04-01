#!/usr/local/bin/python

import os, stat
import basics
import bfiles
import config
import images
import imglib
import useful



def show_list(title, tdir, fl):
    if not fl:
        return
    #mlen = reduce(lambda x, y: max(x, len(y)), fl, 0)
    mlen = max([len(x) for x in fl])
    cols = max(1, 160/max(1, mlen))
    clen = (len(fl) - 1) / cols + 1
    ffl = [fl[(x*clen):((x+1)*clen)] for x in range(0, cols)]
    print '<h4>%s (%d)</h4>' % (title, len(fl))
    print "<table width=100%><tr valign=top>"
    for cl in ffl:
        print "<td width=%d%%>" % (100/cols)
        for f in cl:
            root, ext = useful.root_ext(f.strip())
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
            elif ext in imglib.itypes:
                #print '<a href="/cgi-bin/traverse.cgi?d=%s&f=%s">%s</a><br>' % (tdir, f, f)
                print '<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s">%s</a><br>' % (tdir, f, f)
            else:
                print '<a href="../%s">%s</a><br>' % (tdir + '/' + f, f)
        print "</td>"
    print "</tr></table>"
    print '<br><hr>'


def show_dir(pif, tform):
    print '<hr>'
    if not os.path.exists(tform.tdir):
        raise useful.SimpleError('Path does not exist.')

    #dl, gl, ol, sl, xl = imglib.get_dir(tform.tdir)
    files = imglib.get_dir(tform.tdir)

    show_list(files['titles']['dir'], tform.tdir, files['dir'])

    if files['graf']:
        if tform.graf:
            print '<h4>%s (%d)</h4>' % (files['titles']['graf'], len(files['graf']))
            for f in files['graf']:
                perms = os.stat(tform.tdir + '/' + f)[stat.ST_MODE]
                if (perms & 4) == 0:
                    print '%s<br>' % f
                elif tform.graf:
                    #print '<a href="/cgi-bin/traverse.cgi?d=%s&f=%s"><img src="../%s" border=0>%s</a><br>' % (tform.tdir, f, tform.tdir + '/' + f, f)
                    print '<a href="imawidget.cgi?d=%s&f=%s&man=%s&newvar=%s&cy=0"><img src="../%s" border=0>%s</a><br>' % (tform.tdir, f, tform.mod, tform.var, tform.tdir + '/' + f, f)
                else:
                    print '<a href="../%s">%s</a><br>' % (tform.tdir + '/' + f, f)
            print '<br><hr>'
        else:
            show_list(files['titles']['graf'], tform.tdir, files['graf'])

    show_list(files['titles']['log'], tform.tdir, files['log'])
    show_list(files['titles']['dat'], tform.tdir, files['dat'])
    show_list(files['titles']['exe'], tform.tdir, files['exe'])
    show_list(files['titles']['other'], tform.tdir, files['other'])

    if pif.render.is_admin:
	print '<a href="upload.cgi?d=%s">%s</a>' % (tform.tdir, pif.render.format_button('upload'))

    if files['graf']:
        print '<form action="traverse.cgi">'
        print '<a href="traverse.cgi?g=1&d=%s">%s</a> or ' % (tform.tdir, pif.render.format_button('show all pictures'))
        print 'Pattern <input type="text" name="p">'
        print '<input type="hidden" name="d" value="%s">' % tform.tdir
        print '<input type="checkbox" name="du" value="1"> Dupes'
        print '<input type="checkbox" name="co" value="1"> Compact'
	if pif.render.is_admin:
	    print '<input type="checkbox" name="shc" value="1"> Categorize'
	    print '<input type="checkbox" name="mss" value="1"> Mass'
	    print '<input type="checkbox" name="shm" value="1"> Shelve'
	    print '<input type="checkbox" name="suf" value="1"> Resuffix'
        print '<input type="checkbox" name="si" value="1"> Sized'
        print pif.render.format_button_input()
	print '<br>'
        print 'Size X <input type="text" name="sx">'
        print 'Size Y <input type="text" name="sy">'
        print '</form>'


imginputs = '''<input type="checkbox" name="rm" value="%(f)s"> rm<input type="checkbox" name="mv" value="%(f)s %(b)s"> mv'''
imginput = '''<input type="checkbox" name="rm" value="%(f)s"> rm
<input type="text" name="ren.%(f)s"> rename
'''
def img(pif, args, base='', shlv=False, cate=False, rsuf=False, sx=0, sy=0, mss=False):
    also = {'border': 0}
    if sx:
	also['width'] = sx
    if sy:
	also['height'] = sy
    print '<tr>'
    args.sort()
    for arg in args:
        root, ext = useful.root_ext(arg.strip())
        inp = ''
        if shlv or cate:
            inp += '''<input type="text" name="lib.%s"> lib''' % arg
            print pif.render.format_cell(0, '%s<br>%s%s' % (pif.render.format_image_required([root], suffix=ext, also=also), arg, inp))
            continue
	elif mss:
            inp += '''<input type="text" name="var.%s"> var''' % arg
            print pif.render.format_cell(0, '%s<br>%s%s' % (pif.render.format_image_required([root], suffix=ext, also=also), arg, inp))
            continue
	elif rsuf:
            inp += '''<input type="text" name="rsfx.%s"> rsfx''' % arg
            print pif.render.format_cell(0, '%s<br>%s%s' % (pif.render.format_image_required([root], suffix=ext, also=also), arg, inp))
            continue
        if arg == base:
            inp = imginputs % {'f': arg, 'b': root + 'z.' + ext}
        elif base:
            inp = imginputs % {'f': arg, 'b': base}
        else:
            inp = imginput % {'f': arg}
        #inp += ' <a href="imawidget.cgi?d=%s&f=%s&cy=0">' % (pif.render.pic_dir, arg) + pif.render.format_button('edit') + '</a>'
        inp += ' ' + pif.render.format_button('edit', 'imawidget.cgi?d=%s&f=%s&cy=0' % (pif.render.pic_dir, arg))
        inp += ' ' + pif.render.format_button('stitch', 'stitch.cgi?fn_0=%s&submit=1&q=&fc=1' % (pif.render.pic_dir + '/' + arg))
        print pif.render.format_cell(0, '<a href="../%s/%s">%s</a><br>%s%s' % (pif.render.pic_dir, arg, pif.render.format_image_required([root], suffix=ext, also=also), arg, inp))
    print '</tr>'


def flist_sort(flist, tform):
    if tform.sizd:
	flist.sort(key=lambda x: (x[2:], x[:2]))
    else:
	flist.sort()

def show_imgs(pif, tform):
    print '<hr>'
    print '<form action="traverse.cgi" method="post">'
    plist = tform.patt.split(',')
    for pent in plist:
        flist = useful.read_dir(pent, tform.tdir)
        flist_sort(flist, tform)
	if tform.cpct:
	    for fn in flist:
		print pif.render.format_link(
		    "imawidget.cgi?d=%s&f=%s" % (tform.tdir, fn),
		    pif.render.fmt_img_src(os.path.join(tform.tdir, fn))) + '\n'
	else:
	    print '<table>'
	    for fn in flist:
		if tform.dups:
		    root, ext = useful.root_ext(fn)
		    flist = useful.read_dir(root + '*' + ext, pif.render.pic_dir)
		    flist_sort(flist, tform)
		    if len(flist) > 1:
			img(pif, flist, fn, shlv=tform.shlv, cate=tform.cate, sx=tform.szx, sy=tform.szy, mss=tform.mss)
		else:
		    img(pif, [fn], shlv=tform.shlv, cate=tform.cate, rsuf=tform.rsuf, sx=tform.szx, sy=tform.szy, mss=tform.mss)
	    print '</table>'
	    print '<hr>'
    print '<input type="hidden" name="d" value="%s">' % tform.tdir
    print '<input type="hidden" name="sc" value="1">'
    if tform.cate:
	print '<input type="hidden" name="pre" value="">'
	print '<input type="hidden" name="shc" value="1">'
    elif tform.shlv:
	print '<input type="hidden" name="pre" value="man">'
	print '<input type="hidden" name="shm" value="1">'
    elif tform.rsuf:
	print '<input type="hidden" name="suf" value="1">'
    elif tform.mss:
	print '<input type="hidden" name="mss" value="1">'
    print pif.render.format_button_input()
    print '<a href="upload.cgi?d=%s&r=unset">%s</a>' % (tform.tdir, pif.render.format_button('upload'))
    print '</form>'


def show_script(pif, tform):
    if tform.mss:
	do_masses(pif, tform)
	return
    if tform.rsuf:
	for fn, suf in tform.rsfx:
	    root, ext = os.path.splitext(fn)
	    if '-' in root:
		root = root[:root.find('-')]
	    nfn = root + '-' + suf + ext
	    print fn, root + '-' + suf + ext, '<br>'
	    useful.file_mover(os.path.join(tform.tdir, fn), os.path.join(tform.tdir, nfn), mv=True, inc=True)
	return
    rend = dict(tform.renl)
    print '<pre>'
    for ren in tform.renl:
        fn = ren[1]
        if '.' not in fn:
            fn += ren[0][ren[0].rfind('.'):]
        if not os.path.exists(fn):
            useful.file_mover(os.path.join(tform.tdir, ren[0]), os.path.join(tform.tdir, fn), mv=True, inc=True)
        else:
            print '#ren', os.path.join(tform.tdir, ren[0], os.path.join(tform.tdir, fn))
    for lb in tform.libl:
        dest = lb[1]  # we might have renamed this...
        if lb[0] in rend:
            lb[0] = rend[lb[0]]
        if not os.path.exists(os.path.join(config.LIB_DIR, tform.pre, dest)):
            os.mkdir(os.path.join(config.LIB_DIR, tform.pre, dest))
        useful.file_mover(os.path.join(tform.tdir, lb[0]), os.path.join(config.LIB_DIR, tform.pre, dest, lb[0]), mv=True, inc=True)
    for rm in tform.rml:
        if os.path.exists(os.path.join(tform.tdir, rm)):
            useful.file_mover(os.path.join(tform.tdir, rm), None, mv=True)
    for mv in tform.mvl:
        fsp = mv.split(' ')
        if os.path.exists(os.path.join(tform.tdir, fsp[0])):
            useful.file_mover(os.path.join(tform.tdir, fsp[0]), os.path.join(tform.tdir, fsp[1]), mv=True, inc=True)
    print '</pre>'


def do_masses(pif, tform):
    for fn, var in pif.form.get_list(start='var.'):
	print '<hr>'
	print fn, var, '<br>'
	eform = images.EditForm(pif, tdir=pif.render.pic_dir, fn=fn)
	eform.ot = 'jpg'
	eform.tysz = 's'
	eform.read_file('')
	eform.man = eform.calc_man()
	eform.var = eform.nvar = var
	eform.mass_resize()


def show_file(pif, tform):
    print pif.render.format_button('delete', link=pif.request_uri + '&delete=1&act=1')
    if os.path.exists(os.path.join(tform.tdir, 'archive')):
	print pif.render.format_button('archive', link=pif.request_uri + '&archive=1&act=1')
    root, ext = useful.root_ext(tform.fnam)
    if ext == 'dat':
        show_table(pif, tform)
    elif ext in imglib.itypes:
#       if tform.tdir.startswith('..'):
#           print '<img src="/cgi-bin/image.cgi?d=%s&f=%s">' % (tform.tdir, tform.fnam)
#       else:
            show_picture(pif, tform.fnam)
    elif tform.tdir == '../../logs':
        print '<p><div style="font-family: monospace;">'
        fil = open(tform.tdir + '/' + tform.fnam).readlines()
        for i in range(len(fil)):
            if fil[i].startswith('uri = '):
                fil[i] = """uri = <a href="%s">%s</a>\n""" % (fil[i][9:-4], fil[i][9:-4])
                break
        print '<br>'.join(fil)
	print '</div>'
    else:
        print '<p>'
        fil = open(tform.tdir + '/' + tform.fnam).readlines()
        for i in range(len(fil)):
            if fil[i].startswith('uri = '):
                fil[i] = """uri = <a href="%s">%s</a>\n""" % (fil[i][9:-4], fil[i][9:-4])
                break
        print '<br>'.join(fil)


# for things out of http space:
#print '<img src="/cgi-bin/image.cgi?d=%s&f=%s">' % (pif.render.pic_dir, fn)
def show_picture(pif, fn, pdir=None):
    if pdir:
	pif.render.pic_dir = pdir
    #picker(pif, form, fn)
    root, ext = useful.root_ext(fn.strip())
    pif.render.comment(root, ext)
    print '<table><tr><td></td><td>' + pif.render.format_image_art('hruler.gif') + '</td></tr>'
    print '<tr><td valign="top">' + pif.render.format_image_art('vruler.gif') + '</td><td valign="top">'
    print '<a href="/cgi-bin/image.cgi?d=%s&f=%s"><img src="/cgi-bin/image.cgi?d=%s&f=%s"></a>' % (pif.render.pic_dir, fn, pif.render.pic_dir, fn)
    print '</td></tr></table>'


colors = ["#FFFFFF", "#CCCCCC"]


#print '<a href="/cgi-bin/table.cgi?page=%s">%s</a><br>' % (tdir + '/' + f, f)
def show_table(pif, tform):
    tablefile = bfiles.SimpleFile(tform.tdir + '/' + tform.fnam)
    cols = ''  # pif.form.get_str('cols')
    h = 0  # pif.form.get_int('h')

    print pif.render.format_table_start()
    hdr = ''
    if h:
        hdr = tablefile.dblist[0]
        table = tablefile.dblist[1:]
    else:
        table = tablefile.dblist

    if tform.sorty:
        table.sort(key=lambda x: x[tform.sorty].lower())

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
            for ent in range(0, len(hdr)):
                if ent >= len(cols) or cols[ent].lower() != 'n':
                    #print "<th>"+hdr[ent]+"</th>"
                    print '<th bgcolor="#FFFFCC"><a href="table.cgi?page=%s&sort=%d&h=%d&cols=%s">%s</th>' % (tform.fnam, iarg, h, cols, hdr[ent])
                iarg = iarg + 1
            print "</tr>\n<tr>"
        print '<tr bgcolor="%s">' % colors[irow]
        row = row - 1
        for ent in range(0, len(line)):
            if ent >= len(cols) or cols[ent].lower() != 'n':
                print "<td>"+line[ent]+"</td>"
        print "</tr>"
    print pif.render.format_table_end()


def do_action(pif, tform):
    print '<div class="warning">'
    #nfn = images.action(pif, tform.tdir, tform.fnam, tform.act)
    nfn = imglib.ActionForm(pif).read(pif.form).action(pif, tform.tdir, tform.fnam)['fn']
    print '</div><br>'
    if nfn:
        show_picture(pif, nfn)
    else:
	tform.graf = 0
        show_dir(pif, tform)


class TraverseForm(object):
    def __init__(self):
	pass

    def read(self, pif):
	pif.render.pic_dir = self.tdir = pif.form.get_str('d', '.')
	self.libl = pif.form.get_list(start='lib.', defval='')
	self.renl = pif.form.get_list(start='ren.', defval='')
	self.rsfx = pif.form.get_list(start='rsfx.', defval='')
	#cols = ''  # pif.form.get_str('cols')
	#h = 0  # pif.form.get_int('h')
	self.sorty = pif.form.get_int('sort')
	#pif.render.title = '<a href="traverse.cgi?d=%s">%s</a>' % (pif.form.get_str("d", '.'), pif.form.get_str("d", '.'))
	self.graf = pif.form.get_int("g")
	self.fnam = pif.form.get_str("f")
	self.patt = pif.form.get_str("p")
	self.dups = pif.form.get_int("du")
	self.cpct = pif.form.get_int("co")
	self.mss = pif.form.get_int("mss")
	self.shlv = pif.form.get_int("shm")
	self.rsuf = pif.form.get_int("suf")
	self.cate = pif.form.get_int("shc")
	self.sizd = pif.form.get_int("si")
	self.scrt = pif.form.get_int('sc')
	self.act = pif.form.get_int('act')
	self.cycle = pif.form.get_int("cy")  # srsly?
	self.mvl = pif.form.get_list('mv')
	self.rml = pif.form.get_list('rm')
	self.pre = pif.form.get_str('pre')
	self.mod = pif.form.get_str('mod')
	self.var = pif.form.get_str('var')
	self.szx = pif.form.get_int("sx")
	self.szy = pif.form.get_int("sy")

	pif.render.title = self.tdir
	if self.fnam:
	    pif.render.title += '/' + self.fnam
	return self


@basics.web_page
def main(pif):
    os.environ['PATH'] += ':/usr/local/bin'
    pif.render.print_html()
    pif.restrict('vma')
    tform = TraverseForm().read(pif)

    print pif.render.format_head(extra=pif.render.increment_js)
    print pif.form.get_form(), '<br>'
    if tform.patt:
        show_imgs(pif, tform)
    elif tform.scrt:
        show_script(pif, tform)
    elif tform.act:
        do_action(pif, tform)
    elif tform.fnam:
        show_file(pif, tform)
    else:
        show_dir(pif, tform)
    print pif.render.format_tail()


if __name__ == '__main__':  # pragma: no cover
    basics.goaway()
