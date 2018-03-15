#!/usr/local/bin/python

import datetime, filecmp, glob, os, re, stat, subprocess, sys
import basics
import bfiles
import config
import images
import imglib
import mannum
import useful



def show_list(title, tdir, fl, view=False):
    if not fl:
        return ''
    #mlen = reduce(lambda x, y: max(x, len(y)), fl, 0)
    mlen = max([len(x) for x in fl])
    cols = max(1, 160/max(1, mlen))
    clen = (len(fl) - 1) / cols + 1
    ffl = [fl[(x*clen):((x+1)*clen)] for x in range(0, cols)]
    ostr = '<h4>%s (%d)</h4>\n' % (title, len(fl))
    ostr += "<table width=100%><tr valign=top>\n"
    for cl in ffl:
        ostr += "<td width=%d%%>\n" % (100/cols)
        for f in cl:
            root, ext = useful.root_ext(f.strip())
            fst = os.stat(tdir + '/' + f)
            perms = fst[stat.ST_MODE]
            if f[0] == '.':
                ostr += '<i>%s</i><br>\n' % f
            elif stat.S_ISDIR(perms):
                ostr += '<a href="/cgi-bin/traverse.cgi?d=%s">%s/</a><br>\n' % (tdir + '/' + f, f)
            elif tdir.startswith('../'):
                ostr += '<a href="/cgi-bin/traverse.cgi?d=%s&f=%s">%s</a><br>\n' % (tdir, f, f)
            elif f[-4:] == '.dat':
                ostr += '<a href="/cgi-bin/traverse.cgi?d=%s&f=%s">%s</a><br>\n' % (tdir, f, f)
            elif (perms & 5) == 0:
                ostr += '%s<br>\n' % f
            elif ext in imglib.itypes:
		if view:
		    ostr += '<a href="/%s/%s">%s</a><br>\n' % (tdir, f, f)
		else:
		    ostr += '<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s">%s</a><br>\n' % (tdir, f, f)
            else:
                ostr += '<a href="../%s">%s</a><br>\n' % (tdir + '/' + f, f)
        ostr += "</td>\n"
    ostr += "</tr></table>\n"
    ostr += '<br><hr>\n'
    return ostr


def show_dir(pif, tform):
    if not os.path.exists(tform.tdir):
        raise useful.SimpleError('Path does not exist.')

    ostr = '<hr>\n'
    #dl, gl, ol, sl, xl = imglib.get_dir(tform.tdir)
    files = imglib.get_dir(tform.tdir, name_has=tform.has)

    ostr += show_list(files['titles']['dir'], tform.tdir, files['dir'], tform.view)

    if files['graf']:
        if tform.graf:
            ostr += '<h4>%s (%d)</h4><div class="glist">\n' % (files['titles']['graf'], len(files['graf']))
            for f in files['graf']:
                perms = os.stat(tform.tdir + '/' + f)[stat.ST_MODE]
                if (perms & 4) == 0:
                    ostr += '%s<br>\n' % f
                elif tform.graf:
                    #ostr += '<a href="/cgi-bin/traverse.cgi?d=%s&f=%s"><img src="../%s" border=0>%s</a><br>' % (tform.tdir, f, tform.tdir + '/' + f, f)
                    ostr += '<a href="imawidget.cgi?d=%s&f=%s&man=%s&newvar=%s&cy=0&suff=%s"><img src="../%s" border=0>%s</a><br>\n' % (tform.tdir, f, tform.mod, tform.var, tform.suff, tform.tdir + '/' + f, f)
                else:
                    ostr += '<a href="../%s">%s</a><br>\n' % (tform.tdir + '/' + f, f)
            ostr += '</div><hr>\n'
        else:
            ostr += show_list(files['titles']['graf'], tform.tdir, files['graf'], tform.view)

    ostr += show_list(files['titles']['log'], tform.tdir, files['log'], tform.view)
    ostr += show_list(files['titles']['dat'], tform.tdir, files['dat'], tform.view)
    ostr += show_list(files['titles']['exe'], tform.tdir, files['exe'], tform.view)
    ostr += show_list(files['titles']['other'], tform.tdir, files['other'], tform.view)

    if pif.render.is_admin:
	ostr += '<a href="upload.cgi?d=%s">%s</a>\n' % (tform.tdir, pif.render.format_button('upload'))

    if files['graf']:
        ostr += '<form action="traverse.cgi">\n' + pif.create_token()
        ostr += '<a href="traverse.cgi?g=1&d=%s">%s</a> or \n' % (tform.tdir, pif.render.format_button('show all pictures'))
        ostr += 'Pattern <input type="text" name="p">\n'
        ostr += '<input type="hidden" name="d" value="%s">\n' % tform.tdir
        ostr += '<input type="checkbox" name="du" value="1"> Dupes\n'
        ostr += '<input type="checkbox" name="co" value="1"> Compact\n'
        ostr += '<input type="checkbox" name="si" value="1"> Sized\n'
	if pif.render.is_admin:
	    ostr += '<br><input type="radio" name="lty" value="nrm" checked> Normal\n'
	    ostr += '<input type="radio" name="lty" value="shc"> Categorize\n'
	    ostr += '<input type="radio" name="lty" value="mss"> Mass\n'
	    ostr += '<input type="radio" name="lty" value="shm"> Shelve\n'
	    ostr += '<input type="radio" name="lty" value="suf"> Resuffix\n'
	    ostr += '<input type="radio" name="lty" value="crd"> Credit\n'
        ostr += pif.render.format_button_input()
	ostr += '<br>\n'
        ostr += 'Size X <input type="text" name="sx">\n'
        ostr += 'Size Y <input type="text" name="sy">\n'
        ostr += '</form>\n'
    return ostr


def check_image(pif, targs, src):
    ostr = '</td><td>'
    ssize = os.stat(src).st_size
    for tf in targs:
	if tf[1] == ssize and filecmp.cmp(tf[0], src):
	    ostr += tf[0][tf[0].rfind('/') + 1:] + '<br>'
    return ostr


imginputs = '''<input type="checkbox" name="rm" value="%(f)s"> rm<input type="checkbox" name="mv" value="%(f)s %(b)s"> mv'''
imginput = '''<input type="checkbox" name="rm" value="%(f)s"> rm
<input type="text" name="ren.%(f)s"> rename
'''
def img(pif, args, base='', shlv=False, cate=False, rsuf=False, sx=0, sy=0, mss=False, cred=False, targs=[]):
    also = {'border': 0}
    if sx:
	also['width'] = sx
    if sy:
	also['height'] = sy
    ostr = '<tr>\n'
    args.sort()
    for arg in args:
	f_st = os.stat(os.path.join(pif.render.pic_dir, arg))
	f_date = str(datetime.datetime.fromtimestamp(f_st.st_mtime))
        root, ext = useful.root_ext(arg.strip())
        inp = ''
        if shlv or cate:
            inp += '''<input type="text" name="lib.%s"> lib''' % arg
            ostr += pif.render.format_cell(0, '%s<br>%s%s %s' % (pif.render.format_image_required([root], suffix=ext, also=also), arg, inp, f_date))
            continue
	elif mss:
            inp += '''<br><input type="text" name="var.%s"> var''' % arg
            ostr += pif.render.format_cell(0, '%s<br>%s%s %s' % (pif.render.format_image_required([root], suffix=ext, also=also), arg, inp, f_date))
	    ostr += check_image(pif, targs, os.path.join(pif.render.pic_dir, arg))
            continue
	elif rsuf:
            inp += '''<input type="text" name="rsfx.%s"> rsfx''' % arg
            ostr += pif.render.format_cell(0, '%s<br>%s%s %s' % (pif.render.format_image_required([root], suffix=ext, also=also), arg, inp, f_date))
            continue
	elif cred:
	    fn = arg[:arg.find('.')] if '.' in arg else arg
	    fn = fn[2:] if (fn[0] in 'sml' and fn[1] == '_') else fn
            inp += '''<input type="text" name="cred.%s" size="12" value="%s"> cred''' % (fn, cred.get(fn, ''))
            ostr += pif.render.format_cell(0, '%s<br>%s%s' % (pif.render.format_image_required([root], suffix=ext, also=also), arg, inp))
            continue
        if arg == base:
            inp = imginputs % {'f': arg, 'b': root + 'z.' + ext}
        elif base:
            inp = imginputs % {'f': arg, 'b': base}
        else:
            inp = imginput % {'f': arg}
        #inp += ' <a href="imawidget.cgi?d=%s&f=%s&cy=0">' % (pif.render.pic_dir, arg) + pif.render.format_button('edit') + '</a>'
        #inp += ' ' + pif.render.format_button('edit', 'imawidget.cgi?d=%s&f=%s&cy=0' % (pif.render.pic_dir, arg))
        #inp += ' ' + pif.render.format_button('stitch', 'stitch.cgi?fn_0=%s&submit=1&q=&fc=1' % (pif.render.pic_dir + '/' + arg))
        #ostr += pif.render.format_cell(0, '<a href="../%s/%s">%s</a><br>%s%s' % (pif.render.pic_dir, arg, pif.render.format_image_required([root], suffix=ext, also=also), arg, inp))
        ostr += pif.render.format_cell(0, '<a href="imawidget.cgi?d=%s&f=%s&cy=0">%s</a><br>%s%s' % (pif.render.pic_dir, arg, pif.render.format_image_required([root], suffix=ext, also=also), arg, inp))
    ostr += '</tr>\n'
    return ostr


def flist_sort(flist, tform):
    if tform.sizd:
	flist.sort(key=lambda x: (x[2:], x[:2]))
    else:
	flist.sort()

def show_imgs(pif, tform):
    print '<hr>'
    print '<form action="traverse.cgi" method="post">' + pif.create_token()
    plist = tform.patt.split(',')
    img_args = {'shlv': tform.shlv, 'cate': tform.cate, 'sx': tform.szx, 'sy': tform.szy, 'mss': tform.mss}
    if tform.mss:
	print 'Credit ' + pif.render.format_text_input('credit', 4)
	print '<br>'
	img_args['targs'] = [(x, os.stat(x).st_size) for x in sorted(glob.glob('.' + config.IMG_DIR_VAR + '/l_' + tform.dirname + '-*.*'))]
    for pent in plist:
        flist = useful.read_dir(pent, tform.tdir)
        flist_sort(flist, tform)
	if tform.cred:
	    img_args['cred'] = {x['photo_credit.name']: x['photographer.id'] for x in pif.dbh.fetch_photo_credits(path=tform.tdir)}
	if tform.cpct:
	    for fn in flist:
		print pif.render.format_link(
		    "imawidget.cgi?d=%s&f=%s" % (tform.tdir, fn),
		    pif.render.fmt_img_src(os.path.join(tform.tdir, fn))) + '\n'
	else:
	    print '<table class="glist">'
	    for fn in flist:
		if tform.dups:
		    root, ext = useful.root_ext(fn)
		    flist = useful.read_dir(root + '*' + ext, pif.render.pic_dir)
		    flist_sort(flist, tform)
		    if len(flist) > 1:
			print img(pif, flist, fn, **img_args)
		else:
		    print img(pif, [fn], rsuf=tform.rsuf, **img_args)
	    print '</table>'
	    print '<hr>'
    print '<input type="hidden" name="d" value="%s">' % tform.tdir
    print '<input type="hidden" name="sc" value="1">'
    if tform.cate:
	print '<input type="hidden" name="pre" value="">'
	print '<input type="hidden" name="lty" value="shc">'
    elif tform.shlv:
	print '<input type="hidden" name="pre" value="man">'
	print '<input type="hidden" name="lty" value="shm">'
    elif tform.rsuf:
	print '<input type="hidden" name="lty" value="suf">'
    elif tform.mss:
	print '<input type="hidden" name="lty" value="mss">'
	print 'promote <input type="text" name="msspromote">'
    elif tform.cred:
	print '<input type="hidden" name="lty" value="crd">'
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
    if tform.cred:
	for fn, cred in pif.form.get_list(start='cred.'):
	    print fn, cred, '<br>'
	    pif.dbh.write_photo_credit(cred, tform.tdir, fn, verbose=False)
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
        if not os.path.exists(useful.relpath('.', config.LIB_DIR, tform.pre, dest)):
            os.mkdir(useful.relpath('.', config.LIB_DIR, tform.pre, dest))
        useful.file_mover(os.path.join(tform.tdir, lb[0]), useful.relpath('.', config.LIB_DIR, tform.pre, dest, lb[0]), mv=True, inc=True)
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
	eform.mass_resize(pif)
    var_id = pif.form.get('msspromote')
    if var_id:
	mod_id = eform.calc_man()
	imglib.promote_picture(pif, mod_id, var_id)


def show_file(pif, tform):
    print pif.render.format_button('delete', link=pif.request_uri + '&delete=1&act=1')
    if os.path.exists(os.path.join(tform.tdir, 'archive')):
	print pif.render.format_button('archive', link=pif.request_uri + '&archive=1&act=1')
    if os.path.exists(os.path.join(tform.tdir, 'fixed')):
	print pif.render.format_button('fixed', link=pif.request_uri + '&fixed=1&act=1')
    root, ext = useful.root_ext(tform.fnam)
    if ext in imglib.itypes:
#       if tform.tdir.startswith('..'):
#           print '<img src="/cgi-bin/image.cgi?d=%s&f=%s">' % (tform.tdir, tform.fnam)
#       else:
            show_picture(pif, tform.fnam)
#    elif ext == 'dat':
#        show_table(pif, tform)
    elif tform.tdir == '../../logs':
        print '<p><div style="font-family: monospace;">'
        fil = open(tform.tdir + '/' + tform.fnam).readlines()
        for i in range(len(fil)):
            if fil[i].startswith('uri = '):
                fil[i] = """uri = <a href="%s">%s</a>\n""" % (fil[i][9:-4], fil[i][9:-4])
                break
	print '<pre>'
        print ''.join(fil)
	print '</pre>'
	print '</div>'
    elif os.path.exists(tform.tdir + '/' + tform.fnam):
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
#def show_table(pif, tform):
#    tablefile = bfiles.SimpleFile(tform.tdir + '/' + tform.fnam)
#    cols = ''  # pif.form.get_str('cols')
#    h = 0  # pif.form.get_int('h')
#
#    print pif.render.format_table_start()
#    hdr = ''
#    if h:
#        hdr = tablefile.dblist[0]
#        table = tablefile.dblist[1:]
#    else:
#        table = tablefile.dblist
#
#    if tform.sorty:
#        table.sort(key=lambda x: x[tform.sorty].lower())
#
#    row = 0
#    icol = irow = 0
#    if 'y' in cols:
#        icol = cols.find('y')
#    id = ''
#    for line in table:
#        if line[icol] != id:
#            id = line[icol]
#            irow = (irow + 1) % 2
#        if not row:
#            row = h
#            iarg = 0
#            print '<tr>'
#            for ent in range(0, len(hdr)):
#                if ent >= len(cols) or cols[ent].lower() != 'n':
#                    #print "<th>"+hdr[ent]+"</th>"
#                    print '<th bgcolor="#FFFFCC"><a href="table.cgi?page=%s&sort=%d&h=%d&cols=%s">%s</th>' % (tform.fnam, iarg, h, cols, hdr[ent])
#                iarg = iarg + 1
#            print "</tr>\n<tr>"
#        print '<tr bgcolor="%s">' % colors[irow]
#        row = row - 1
#        for ent in range(0, len(line)):
#            if ent >= len(cols) or cols[ent].lower() != 'n':
#                print "<td>"+line[ent]+"</td>"
#        print "</tr>"
#    print pif.render.format_table_end()


def do_action(pif, tform):
    print '<div class="warning">'
    #nfn = images.action(pif, tform.tdir, tform.fnam, tform.act)
    nfn = imglib.ActionForm(pif).read(pif.form).action(pif, tform.tdir, tform.fnam)['fn']
    print '</div><br>'
    if nfn:
        show_picture(pif, nfn)
    else:
	tform.graf = 0
        print show_dir(pif, tform)


class TraverseForm(object):
    def __init__(self):
	pass

    def read(self, pif):
	pif.render.pic_dir = self.tdir = pif.form.get_str('d', '.')
	if self.tdir.endswith('/'):
	    self.dirname = self.tdir[self.tdir[:-1].rfind('/') + 1:-1]
	elif '/' in self.tdir:
	    self.dirname = self.tdir[self.tdir.rfind('/') + 1:]
	else:
	    self.dirname = self.tdir
	self.libl = pif.form.get_list(start='lib.', defval='')
	self.renl = pif.form.get_list(start='ren.', defval='')
	self.rsfx = pif.form.get_list(start='rsfx.', defval='')
	#cols = ''  # pif.form.get_str('cols')
	#h = 0  # pif.form.get_int('h')
	self.sorty = pif.form.get_int('sort')
	#pif.render.title = '<a href="traverse.cgi?d=%s">%s</a>' % (pif.form.get_str("d", '.'), pif.form.get_str("d", '.'))
	self.view = pif.form.get_bool("v")
	self.graf = pif.form.get_int("g")
	self.fnam = pif.form.get_str("f")
	self.patt = pif.form.get_str("p")
	self.has = pif.form.get_str("has")
	self.suff = pif.form.get_str("suff")
	self.dups = pif.form.get_int("du")
	self.cpct = pif.form.get_int("co")
	self.cate = pif.form.get_radio("lty", "shc")
	self.mss = pif.form.get_radio("lty", "mss")
	self.shlv = pif.form.get_radio("lty", "shm")
	self.rsuf = pif.form.get_radio("lty", "suf")
	self.cred = pif.form.get_radio("lty", "crd")
	self.sizd = pif.form.get_int("si")
	self.scrt = pif.form.get_int('sc')
	self.act = pif.form.get_int('act')
	self.cycle = pif.form.get_int("cy")  # srsly?
	self.mvl = pif.form.get_list('mv')
	self.rml = pif.form.get_list('rm')
	self.pre = pif.form.get_str('pre')
	self.mod = pif.form.get_str('mod')
	if not self.mod:
	    self.mod = pif.form.get_str('man')
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

    pif.render.set_page_extra(pif.render.increment_js)
    print pif.render.format_head()
    useful.header_done()
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
        print show_dir(pif, tform)
    print pif.render.format_tail()


# ----- updcommits -----------------------------------------------------

'''
This script takes commits from the git log and puts them
into the site activity table in the database.

It also does some other housekeeping: man2csv, and writing
the config file for php's use.
'''


def read_commits(endtime):
    p = subprocess.Popen(["/usr/local/bin/git", "log"], stdout=subprocess.PIPE, stderr=None, close_fds=True)
    l = p.stdout.read()
    commits = list()
    #Date:   Fri Jun 13 19:26:34 2014 +0200
    date_re = re.compile('Date:\s*(?P<d>... ... \d+ \d+:\d+:\d+ \d+)')
    for log_msg in re.compile('\ncommit ', re.M).split(l):
        if log_msg.find('Merge: ') >= 0:
            continue
        m = date_re.search(log_msg)
        if not m:
            continue
        s = m.group('d')
        commit = dict()
        commit['by_user_id'] = 1
        commit['name'] = 'commit'
        commit['description'] = log_msg.split('\n', 4)[4].strip()
        commit['timestamp'] = datetime.datetime.strptime(s, '%a %b %d %X %Y')
        if commit['timestamp'] <= endtime:
            continue
        commits.append(commit)
    commits.sort(key=lambda x: x['timestamp'])
    return commits


def write_php_config_file(pif):
    print "Writing PHP config file."
    configs = []
    fout = open('../bin/config.py').readlines()
    fout[0] = '<?php\n// Generated file.  Do not modify.\n'
    for idx in range(1, len(fout)):
        if fout[idx][0] == '#':
            fout[idx] = '//' + fout[idx][1:]
        elif fout[idx].find('=') >= 0:
	    configs.append(fout[idx][:fout[idx].find('=')].strip())
            fout[idx] = '$' + fout[idx].replace('\n', ';\n')
    fout.append('?>\n')
    open('../htdocs/config.php', 'w').writelines(fout)
    print


def write_jinja2_config_file(pif):
    print "Writing Jinja2 config file."
    fout = open('../bin/config.py').readlines()
    fout[0] = '{# Generated file.  Do not modify. #}\n'
    for idx in range(1, len(fout)):
        if fout[idx][0] == '#':
            fout[idx] = '{# ' + fout[idx][1:] + fout[idx].replace('\n', ' #}\n')
        elif fout[idx].find('=') >= 0:
            fout[idx] = '{% set ' + fout[idx].replace('\n', ' %}\n')
    open('../templates/config.html', 'w').writelines(fout)
    print


cmds = [
    ('p', write_php_config_file, "write php config"),
    ('j', write_jinja2_config_file, "write jinja2 config"),
]

@basics.command_line
def commands(pif):
    useful.cmd_proc(pif, './filsys.py', cmds)


if __name__ == '__main__':  # pragma: no cover
    commands('editor', dbedit='')
