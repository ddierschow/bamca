#!/usr/local/bin/python
# -*- coding: latin-1 -*-


import glob, os, re, sys, time

import basics
import config
import vdata
import tables
import vars

IS_GOOD = 0
IS_CHANGED_SCHEMA = 1
IS_CHANGED = 2
IS_NEW_VAR = 3
IS_NO_MODEL = 4
IS_DIFFERENT_NUMBER = 5

file_list_class = {
    IS_GOOD : 'good',
    IS_CHANGED_SCHEMA : 'changed_schema',
    IS_CHANGED : 'changed',
    IS_NEW_VAR : 'changed',
    IS_NO_MODEL : 'no_model',
    IS_DIFFERENT_NUMBER : 'different',
}

var_record_cols = ['var', 'body', 'base', 'windows', 'interior', 'category', 'area', 'date', 'note', 'manufacture', 'imported_from', 'imported_var']



#{'definition': 'varchar(64)', 'mod_id': 'MB652', 'attribute_name': 'dump', 'id': 1L}
def ShowAttrs(pif, file_id, mod, hdrs, var_desc):
    mod_id = mod['id']
    attrs = pif.dbh.FetchAttributes(mod_id)
    attrs = pif.dbh.DePref('attribute', attrs)
    print '<form method="post">'
    print '<input type="hidden" name="mod_id" value="%s">' % mod_id
    det = pif.dbh.FetchDetails(mod_id, "").get('', {})
    det = pif.dbh.DePref('detail', det)
    print "<table border=1>"
    print "<tr><th>ID</th><th>Name</th><th>Definition</th><th>Title</th><th>V</th><th>Default</th></tr>"
    for attr in attrs:
	visuals = {True: ['visual.%(id)d' % attr], False: []}
	#pif.render.Comment(attr, visuals)
	print "<tr>"
	print '<td style="background-color: %s">' % bg_color[attr['attribute_name'] in hdrs + var_record_cols]
	print '<a href="%s">%s</a></td>' % (pif.dbh.GetEditorLink(pif, 'attribute', {'id' : attr['id']}), attr['id'])
	print "<td>%s</td>" % pif.render.FormatTextInput("attribute_name.%(id)d" % attr, 32, 32, attr["attribute_name"])
	print "<td>%s</td>" % pif.render.FormatTextInput("definition.%(id)d" % attr, 32, 32, attr["definition"])
	print "<td>%s</td>" % pif.render.FormatTextInput("title.%(id)d" % attr, 32, 32, attr["title"])
	print "<td>%s</td>" % pif.render.FormatCheckbox("visual.%(id)d" % attr, [(1, '')], [attr['visual']])
	print "<td>%s</td>" % pif.render.FormatTextInput("description.%(id)d" % attr, 64, 32, det.get(attr["attribute_name"], ""))
	print "<td>%s</td>" % (pif.render.FormatButton("delete", "?f=%s&delattr=%d" % (file_id, attr['id'])) + \
			      pif.render.FormatButtonInput(bname="save", name='renattr.%d' % attr['id']))
	print "</tr>"
	var_desc[attr["attribute_name"]] = attr["definition"]
    cnt = 1
    for hdr in hdrs:
	if not hdr in var_record_cols and not hdr in [x['attribute_name'] for x in attrs]:
	    print "<tr>"
	    print "<td>new</td>"
	    print "<td>%s</td>" % pif.render.FormatTextInput("%dn.attribute_name" % cnt, 32, 32, hdr)
	    print "<td>%s</td>" % pif.render.FormatTextInput("%dn.definition" % cnt, 32, 32, "varchar(64)")
	    print "</tr>"
	    cnt += 1
	    var_desc[hdr] = "varchar(64)"
    print "</table>"
    print pif.render.FormatButtonInput('add')
    print pif.render.FormatButtonInput('add new')
    print "</form>"


def SaveAttribute(pif, attr_id):
    attr = pif.dbh.FetchAttribute(attr_id)
    attr = pif.dbh.DePref('attribute', attr)
    if len(attr) == 1:
	attr = attr[0]
	for key in attr.keys():
	    if key + '.%d' % attr_id in pif.form:
		attr[key] = pif.FormStr(key + '.%d' % attr_id)
	pif.dbh.UpdateAttribute(attr, attr_id)

	if pif.form.get("description.%d" % attr_id, '') != "":
	    rec = {"mod_id" : attr['mod_id'], "var_id" : "", "attr_id" : attr_id, "description" : pif.FormStr("description.%d" % attr_id)}
	    where = {"mod_id" : attr['mod_id'], "var_id" : "", "attr_id" : attr_id}
	    pif.dbh.Write("detail", rec, where)
    else:
	print '%d attributes returned!' % len(attr)


def ShowBaseID(pif, mod):
    # base id form
    print "<h3>Base ID</h3>"
    print pif.render.FormatImageOptional(mod['id'], prefix=['m_', 's_'], pdir='pic/man', also={'align':'right'})
    base_id_info = pif.dbh.DescribeDict('base_id')
    print '<form method="post" name="base_id">'
    print "<table border=1>"
    print "<tr><th>Column</th><th>Value</th></tr>"
    for col in tables.table_info['base_id']['columns']:
	flen = int(paren_re.search(base_id_info[col]['type']).group('len'))
	print "<tr><td>%s</td><td>%s</td>" \
	    % (col, pif.render.FormatTextInput("base_id." + col, flen, flen, mod[col]))
	print "</tr>"
    print "</table>"
    #print '<input type="image" src="../pic/gfx/but_save.gif" name="save_base_id">'
    print pif.render.FormatButtonInput('save', 'save base id')
    print "</form>"


def ShowCasting(pif, mod):
    # casting form
    print "<h3>Casting</h3>"
    casting_info = pif.dbh.DescribeDict('casting')
    print '<form method="post" name="casting">'
    print "<table border=1>"
    print "<tr><th>Column</th><th>Value</th><th>&nbsp;</th></tr>"
    for col in tables.table_info['casting']['columns']:
	flen = int(paren_re.search(casting_info[col]['type']).group('len'))
	print "<tr><td>%s</td><td>%s</td>" \
	    % (col, pif.render.FormatTextInput("casting." + col, flen, flen, mod[col]))
	print "<td>%s</td></tr>" % CastingHelp(pif, col, mod)
    print "</table>"
    print '<input type="image" src="../pic/gfx/but_save.gif" name="save_casting">'
    print "</form>"

    if vars.CheckFormatting(pif, mod['id']):
	vars.CheckFormatting(pif, mod['id'], True, '<br>')
    print '<br>'


def ReadFile(pif, fdir, fn):
    modids, fitabs = [], []
    if os.path.exists(fdir + '/' + fn + '.html'):
	modids, fitabs = ReadHtmlFile(pif, fdir, fn)
    elif os.path.exists(fdir + '/' + fn + '.htm'):
	modids, fitabs = ReadHtmlFile(pif, fdir, fn)
    elif os.path.exists(fdir + '/' + fn + '.dat'):
	modids, fitabs = ReadDatFile(pif, fdir, fn)
    return modids, fitabs


def CheckFile(pif, fdir, fn):
    mod = {}
    ret = IS_GOOD
    modids, fitabs = ReadFile(pif, fdir, fn)
    if not modids:
	return IS_NO_MODEL
    for fitab in fitabs:
	if len(fitab) < 2 or not len(fitab[1]):
	    return IS_NO_MODEL
	hdrs = [vdata.CleanHeader[x] for x in fitab[1][0]]
	num_file_hdrs = len(hdrs)
	if hdrs[0] == 'var' and fitab[0].find("BOX TYPES") < 0:
	    nhdrs = vdata.HeaderColumnChange(fn, hdrs)

	    mn = modids.pop(0)
	    mod = vdata.GetModelRec(pif, mn)
	    if not mod:
		continue
	    attrs = pif.dbh.FetchAttributes(mod['id'])
	    attrs = pif.dbh.DePref('attribute', attrs)
	    attr_names = var_record_cols + [x['attribute_name'] for x in attrs]

	    for hdr in nhdrs:
		if not hdr in attr_names:
		    return IS_CHANGED_SCHEMA

	    varis = pif.dbh.FetchVariations(mod['id'], nodefaults=True)
	    varis = pif.dbh.DePref('variation', varis)
	    dbvars = dict([(x['var'], x) for x in varis])

	    for row in fitab[1][1:]:
		row = vdata.TransformRow(row, num_file_hdrs)
		if not reduce(lambda x,y: x or not not y, row[1:], False):
		    continue
		rec = vdata.RowColumnChange(fn, dict(zip(hdrs, row)))
		dbvar = FindRec(fn, dbvars, rec, nhdrs)
		if dbvar:
		    for col in nhdrs:
			if col != 'var' and rec.get(col, '') != dbvar.get(col, ''):
			    #pif.render.Comment('changed', col, rec.get(col, ''), dbvar.get(col, ''))
			    ret = IS_CHANGED
		    if dbvar['var'] != rec['var'] and rec['var'][0] != 'f':
			#pif.render.Comment('diff#', dbvar['var'], rec['var'])
			ret = IS_DIFFERENT_NUMBER
		else:
		    return IS_NEW_VAR

    if mod:
	return ret
    return IS_NO_MODEL


def CheckRow(dbrow, firow, fihdrs):
    #pif.render.Comment("db", dbrow)
    for hdr in fihdrs:
	dbdet = str(dbrow.get(hdr, ''))
	fidet = firow.get(hdr, '')
	if hdr == 'var':
	    continue # doesn't figure in
	elif dbdet != fidet:
	    #pif.render.Comment('#', hdr, ':', dbdet, '|', fidet)
	    return False
	#pif.render.Comment('=', hdr, ':', dbdet, '|', fidet)
    #pif.render.Comment("match found")
    return True


def FindRec(fn, dbvars, firow, fihdrs):
    # match up to existing record
    #pif.render.Comment("fh", fihdrs)
    #pif.render.Comment("fi", firow)
    for dbvar in dbvars:
	imported_var = dbvars[dbvar].get('imported_var', dbvars[dbvar]['var'])
	if dbvars[dbvar].get('imported_from', '') == fn and imported_var == firow['var']:
	    return dbvars[dbvar]
    for dbvar in dbvars:
	if CheckRow(dbvars[dbvar], firow, fihdrs):
	    return dbvars[dbvar]
    return {}


def FindVarID(dbvars, firow, ids_used):
    # fabricate unique id with no record
    varid = firow['var']
    if varid not in dbvars:
	return varid
    if varid[-1] >= 'A':
	varid = varid[:-1]
    trailer = ''
    while 1:
	if not ((varid + trailer) in ids_used):
	    for dbvar in dbvars:
		if dbvar == varid + trailer:
		    break
	    else:
		return varid + trailer
	if trailer:
	    trailer = chr(ord(trailer) + 1)
	else:
	    trailer = 'a'


def GetFileList(fdir):
    dats = []
    for ext in ['htm', 'html', 'dat']:
	dats += [x[x.rfind('/') + 1:x.rfind('.')] for x in glob.glob(fdir + '/*.' + ext)]
    dats = list(set(dats))
    dats.sort()
    return dats


def ShowFiles(pif, fdir, start=None, num=100, ff=False):
    cols = 4
    dats = GetFileList(fdir)
    if not dats:
	print "no files?"
	return
    for i in range(0, len(dats), num):
	if start == dats[i]:
	    print '<b>' + pif.render.FormatLink("?s=" + dats[i] + "&n=" + str(num), str(i / num + 1)) + '</b>', '-'
	else:
	    print pif.render.FormatLink("?d=" + fdir + "&s=" + dats[i] + "&n=" + str(num), str(i / num + 1)), '-'
    prev = dats[0]
    if start in dats:
	i = dats.index(start)
	if i - num > 0:
	    prev = dats[i - num]
	dats = dats[i:]
    if len(dats) >= num:
	next = dats[num]
    else:
	next = dats[-1]
    #dats = dats[:num]
    rows = (num - 1) / cols + 1
    print pif.render.FormatButton("next", "?d=" + fdir + "&s=" + next + "&n=" + str(num)), '-'
    print pif.render.FormatButton("previous", "?d=" + fdir + "&s=" + prev + "&n=" + str(num))
    print '<table width="100%"><tr>'
    for col in range(0, cols):
	irow = 0
	print '<td valign="top" width="%d%%">' % (100/cols)
	while 1:
	    if not dats:
		break
	    fn = dats.pop(0)
	    mod_update = CheckFile(pif, fdir, fn)
	    if ff and (mod_update == IS_GOOD or mod_update == IS_NO_MODEL):
		continue
	    if ff == 2 and mod_update == IS_DIFFERENT_NUMBER:
		continue
	    print '<a href="?d=%s&f=%s"><span class="%s">%s</span></a>' % (fdir, fn, file_list_class[mod_update], fn)
	    ShowFileLink(fn, 'doc', 'w')
	    ShowFileLink(fn, 'htm', 'h')
	    ShowFileLink(fn, 'html', 'h')
	    print '<br>'
	    irow += 1
	    sys.stdout.flush()
	    if irow == rows:
		break
	print '</td>'
    print "</tr></table>"
    print 'done'


def CastingHelp(pif, col, mod):
    if col == 'rawname':
	return ' | '.join(mod.get('iconname', []))
    if col == 'vehicle_type':
	return pif.render.FormatButton("help", "../pages/types.php", lalso={'target':'_blank'})
    if col == 'country':
	return pif.render.FormatButton("help", "../pages/countries.php", lalso={'target':'_blank'})
    if col == 'make':
	return pif.render.FormatButton("help", "../pages/makes.php", lalso={'target':'_blank'})
    if col == 'flags':
	return "NOT_MADE = 1";
    if col == 'section_id':
	return "man - rwr - mi - orig - promo - wr - fea - sf - rn - rw";
    return "&nbsp;"


def ReadHtmlFile(pif, fdir, fn):
    modids = vdata.GetModelIDs(fn)
    fitabs = [], ''
    if not modids:
	pass
    elif os.path.exists(fdir + '/' + fn + '.html'):
	fitabs = vdata.GetHtmlTables(fdir + '/' + fn + '.html')
    elif os.path.exists(fdir + '/' + fn + '.htm'):
	fitabs = vdata.GetHtmlTables(fdir + '/' + fn + '.htm')
    return modids, fitabs


def ReadDatFile(pif, fdir, fn):
    fn = fdir + '/' + fn + '.dat'
    modids = []
    fitabs = []
    fitab = []
    fidesc = ''
    for ln in open(fn).readlines():
	ln = ln.strip()
	if not ln:
	    continue
	if ln[0] == '#':
	    continue
	ln = ln.split('|')
	if ln[0] == 't':
	    if fitab:
		fitabs.append((fidesc, fitab))
	    ln = ln + ['', '', '']
	    modids.append(ln[1])
	    fidesc = 'Name: %s\nYear: %s\n' % (ln[2].title(), ln[3])
	    fitab = []
	else:
	    fitab.append(ln[1:])
    if fitab:
	fitabs.append((fidesc, fitab))
    return modids, fitabs


def ShowFileLink(fn, ft, show_as):
    fp = os.path.join('src/mbxf', fn + '.' + ft.lower())
    if os.path.exists(fp):
	print '<a href="/%s">%s</a>' % (fp, show_as)


text_color = {True : '#0000FF', False : '#FF0000'}
bg_color = {True : '#FFFFFF', False : '#FFCCCC'}
paren_re = re.compile(r'\((?P<len>\d*)\)')
def ShowFile(pif, fdir, fn, args):
    modids, fitabs = ReadFile(pif, fdir, fn)
    if not modids:
	print "Huh?"
	return

    var_lup = {}
    for arg in args.split(' '):
	if arg:
	    ovar, nvar = arg.split('=')
	    var_lup[ovar] = nvar
    #print 'args', args, "<br>", 'var_lup', var_lup, "<br>"

    print '<h3>File Settings</h3>'
    vdata.ShowFileSettings(fn)
    print '<br>'

    ShowFileLink(fn, 'html', 'HTML')
    ShowFileLink(fn, 'htm', 'HTM')
    ShowFileLink(fn, 'doc', 'DOC')
    ShowFileLink(fn, 'dat', 'DAT')
    print '-'
    if len(modids) > 1:
	for id in modids:
	    print '<a href="#%s">%s</a>' % (id, id)
    var_desc = dict([(x['field'], x['type']) for x in pif.dbh.DescribeDict('variation').values()])

    for fitab in fitabs:
	ShowModelTable(pif, modids, fitab, fn, var_lup, var_desc)


dat_name_re = re.compile(r'Name: (?P<n>.*)')
dat_year_re = re.compile(r'Year: (?P<y>.*)')
def ShowModelTable(pif, modids, fitab, fn, var_lup, var_desc):
    #print fitab[1][0], '<br>'
    hdrs = [vdata.CleanHeader[x] for x in fitab[1][0]]
    num_file_hdrs = len(hdrs)
    hdrs.append('imported_from')
    if hdrs[0] == 'var' and fitab[0].find("BOX TYPES") < 0:
	nhdrs = vdata.HeaderColumnChange(fn, hdrs)

	# casting form
	mn = modids.pop(0)
	print '<a name="%s"></a>' % mn
	mod = vdata.GetModelRec(pif, mn)
	if not mod:
	    print 'no model<br>'
	    return

	varfiles = [x['imported_from'] for x in pif.dbh.FetchVariationFiles(mod['id'])]
	for vf in varfiles:
	    if vf:
		print '<a href="?f=%s">%s</a>' % (vf, vf)
	print '<br>'
	print '<center><h2><a href="single.cgi?id=%s">%s</a>' % (mod['id'], mod['id'])
	print "<h3>", mod.get('rawname', 'no rawname?'), "</h3></center>"

	# base id form
	ShowBaseID(pif, mod)

	# casting form
	ShowCasting(pif, mod)

	print fitab[0], "<br>"

	# attributes form
	print "<h3>Attributes</h3>"
	ShowAttrs(pif, fn, mod, nhdrs, var_desc)

	# variations form
	print "<h3>Variations</h3>"
	varis = pif.dbh.FetchVariations(mod['id'], nodefaults=True)
	varis = pif.dbh.DePref('variation', varis)
	dbvars = dict([[x['var'], x] for x in varis])
	print '<form method="post">'
	print '<input type="hidden" name="current_file" value="%s">' % fn
	print '<input type="hidden" name="mod_id" value="%s">' % mod['id']
	print "<table border=1><tr><th></th>"
	for hdr in nhdrs:
	    print "<th>" + hdr + "</th>"
	print "</tr>"
	print "<tr><th></th>"
	for hdr in nhdrs:
	    print "<td>" + var_desc[hdr] + "</td>"
	print "</tr>"
	ids_used = []
	for row in fitab[1][1:]:
	    is_new = False
	    row = vdata.TransformRow(row, num_file_hdrs)
	    pif.render.Comment('first', row[0])
	    if not reduce(lambda x,y: x or not not y, row[1:], False):
		continue
	    row.append(fn)
	    rec = vdata.RowColumnChange(fn, dict(zip(hdrs, row)))
	    orignum = rec['var']
	    pif.render.Comment('second', orignum)
	    if rec["var"] in var_lup:
		pif.render.Comment('VARLUP', rec['var'], var_lup[rec['var']])
		rec["var"] = var_lup.get(rec["var"], rec["var"])
		dbvar = dbvars.get(rec['var'], {})
	    else:
		dbvar = FindRec(fn, dbvars, rec, nhdrs)
	    if not dbvar:
		dbvar = {'var' : FindVarID(dbvars, rec, ids_used)}
		is_new = True
	    else: # gray
		del dbvars[dbvar['var']] # gray
	    ids_used.append(dbvar['var'])
	    pif.render.Comment(str(dbvar))
	    pic = config.imgdirVar + '/s_' + mod['id'].lower() + '-' + dbvar.get('var', '') + '.jpg'
	    #pif.render.Comment("pic", pic)
	    print '<tr><td style="font-weight: bold; color: %s">' % (text_color[rec['var'] == dbvar.get('var')])
	    print '<input type="hidden" name="%s.orignum" value="%s">' % (rec['var'], dbvar.get('var'))
	    if dbvar.get('var'):
		print '<a href="/cgi-bin/vars.cgi?mod=%s&edit=1&var=%s" style="color: %s">%s</a>' % (mod['id'], dbvar['var'], text_color[rec['var'] == dbvar.get('var')], rec['var'])
	    else:
		print rec['var']
	    if os.path.exists(pic):
		print '<br><a href="../%s">PIC</a>' % pic
	    elif is_new:
		print '<br>new'
	    print '</td>'
	    rec['var'] = dbvar.get('var', rec.get('var', ''))
	    print '<input type="hidden" name="%s.imported_var" value="%s">' % (rec['var'], orignum)
	    for hdr in nhdrs:
		dbdet = str(dbvar.get(hdr, ''))
		fidet = rec.get(hdr, '')
		print '<td style="color: %s; background-color: %s">' % (text_color[dbdet == fidet], bg_color[dbdet == fidet])
		print str(dbvar.get(hdr, '')) + "<br>"
		if dbdet != fidet or hdr == 'var':
		    if fidet:
			print pif.render.FormatTextInput(rec['var'] + '.' + hdr, int(var_desc[hdr][8:-1]), 16, fidet)
		    else:
			print pif.render.FormatTextInput(rec['var'] + '.' + hdr, int(var_desc[hdr][8:-1]), 16, "\\b")
		elif hdr == 'imported_from':
		    print '<input type="hidden" name="%s.imported_from" value="%s">' % (rec['var'], fn)
		    #print '<input type="hidden" name="%s.imported_var" value="%s">' % (dbvar.get('imported_var', orignum), fn)
		    print dbvar.get('imported_var', 'unset')
		print "</td>"
	    print "</tr>"
	dbvarkeys = dbvars.keys()
	dbvarkeys.sort()
	for varid in dbvarkeys:
	    dbvar = dbvars[varid]
	    is_same_file = dbvar.get('imported_from') == fn
	    #pif.render.Comment(str(dbvar))
	    pic = config.imgdirVar + '/s_' + mod['id'].lower() + '-' + dbvar.get('var', '') + '.jpg'
	    #pif.render.Comment("pic", pic)
	    if is_same_file:
		print '<input type="hidden" name="orphan" value="%s">' % varid
	    print '<tr><th style="background-color: #CCCCCCC">'
	    if dbvar.get('var'):
		print '<a href="/cgi-bin/vars.cgi?mod=%s&edit=1&var=%s" style="color: #000000">%s</a>' % (mod['id'], dbvar['var'], dbvar['var'])
	    else:
		print '%s' % dbvar['var']
	    if os.path.exists(pic):
		print '<br><a href="../%s">PIC</a>' % pic
	    print '</th>'
	    for hdr in nhdrs:
		dbdet = str(dbvar.get(hdr, ''))
		if is_same_file:
		    print '<td style="color: %s; background-color: %s">' % ('#990000', '#CCCCCC')
		else:
		    print '<td style="color: %s; background-color: %s">' % ('#000000', '#CCCCCC')
		print str(dbvar.get(hdr, '')) + "<br>"
		print "</td>"
	    print "</tr>"
	print "</table>"

	print pif.render.FormatButtonInput('save')
	print pif.render.FormatButtonInput('recalc')
	print pif.render.FormatButtonInput('delete all')
	print pif.render.FormatButtonInput('fix numbers')
	print pif.render.FormatButtonInput('delete orphans')
	print '</form>'

    else:
	print fitab[0], "<br>"
	print "<table border=1>"
	for row in fitab[1]:
	    print "<tr>"
	    for cel in row:
		print "<td>" + cel + "</td>"
	    print "</tr>"
	print "</table>"

    print fitab[2]


@basics.WebPage
def HandleForm(pif):
    pif.render.PrintHtml()
    if 'mod_id' in pif.form:
	mod_id = pif.FormStr('mod_id')
	pif.render.title = 'Variations - ' + mod_id
    elif 'f' in pif.form:
	pif.render.title = 'Variations - ' + pif.FormStr('f')
    print pif.render.FormatHead()
    if not pif.IsAllowed('a'):
	return

    pif.render.Comment(pif.form)
    import vdata
    vdata.Initialize(pif)
    nvars = []
    if "add" in pif.form:
	print "add<br>"
	for k in pif.form:
	    if k.endswith("n.definition"): # pretty sure these are the new guys
		attr = k[0:-12]
		print "n_def", k, attr
		rec = {"mod_id" : mod_id, "attribute_name" : pif.FormStr(attr + "n.attribute_name"),
			    "title" : pif.FormStr(attr + "n.attribute_name").replace('_', ' ').title(),
			    "definition" : pif.FormStr(k)}
		pif.dbh.Write("attribute", rec, {"mod_id" : mod_id, "attribute_name" : pif.FormStr(attr + "n.attribute_name")})
	    elif k[0:11] == "definition.":
		attr = k[11:]
		print "def", k, attr
		rec = {"mod_id" : mod_id, "attribute_name" : pif.FormStr('attribute_name.' + attr), "title" : pif.FormStr('title.' + attr),
			    "definition" : pif.FormStr(k), "visual" : pif.form.get("visual." + attr, '1')}
		pif.dbh.Write("attribute", rec, {"id" : attr}, modonly=True)
		if pif.form.get("description." + attr, '') != "":
		    rec = {"mod_id" : mod_id, "var_id" : "", "attr_id" : attr, "description" : pif.FormStr("description." + attr)}
		    where = {"mod_id" : mod_id, "var_id" : "", "attr_id" : attr}
		    pif.dbh.Write("detail", rec, where)
    elif "add_new" in pif.form:
	print "add new<br>"
	pif.dbh.Write("attribute", {"mod_id" : mod_id}, [])
    elif pif.FormFind('renattr'):
	keys = pif.FormFind('renattr')
	print "renattr", keys, "<br>"
	for key in keys:
	    SaveAttribute(pif, int(key[8:]))
    elif "save_base_id" in pif.form:
	print "save base_id<br>"
	rec = {}
	for k in pif.form:
	    if k[0:8] == "base_id.":
		rec[k[8:]] = pif.FormStr(k)
	pif.dbh.Write("base_id", rec, {"id" : pif.FormStr("base_id.id")})
    elif "save_casting" in pif.form:
	print "save casting<br>"
	rec = {}
	for k in pif.form:
	    if k[0:8] == "casting.":
		rec[k[8:]] = pif.FormStr(k)
	pif.dbh.Write("casting", rec, {"id" : pif.FormStr("casting.id")})
    elif "save" in pif.form:
	print "save"
	pif.dbh.UpdateVariation({'imported_from' : 'was ' + pif.FormStr('current_file')}, {'imported_from' : pif.FormStr('current_file'), 'mod_id' : mod_id})
	attrs = pif.dbh.FetchAttributes(mod_id)
	attr_lup = {}
	for attr in attrs:
	    print attr, '<br>'
	    attr_lup[attr['attribute.attribute_name']] = attr.get('attribute.id')
	var_cols = pif.dbh.Columns("variation")
	for k in pif.form:
	    if k[-4:] == ".var":
		rec = {"mod_id" : mod_id}
		rec["imported"] = time.time()
		det = {}
		for vk in pif.form:
		    vv = pif.FormStr(vk)
		    if vk[0:len(pif.FormStr(k))] == pif.Formstr(k):
			kk = vk[len(pif.FormStr(k)) + 1:]
			if vv == '\\b':
			    vv = ''
			if kk == 'orignum':
			    pass
			elif kk in var_cols:
			    rec[kk] = vv
			else:
			    det[kk] = vv
		pif.dbh.Write("variation", rec, {"mod_id" : mod_id, "var" : k[0:-4]})
		print 'variation', rec, '<br>'
		for dk in det:
		    if dk in attr_lup:
			detrec = {"mod_id" : mod_id, "var_id" : k[0:-4], "attr_id" : attr_lup[dk], "description" : det[dk]}
			pif.dbh.Write("detail", detrec, {"mod_id" : mod_id, "var_id" : k[0:-4], "attr_id" : attr_lup[dk]})
			print 'detail', detrec, '<br>'
	print "done"
    elif "delete_orphans" in pif.form:
	print pif.form, '<br>'
	print "delete orphans<br>"
	orphans = pif.form.get('orphan', [])
	if type(orphans) == str:
	    orphans = [orphans]
	for var_id in orphans:
	    print 'deleting', mod_id, var_id, '<br>'
	    vars.DeleteVariation(pif, mod_id, var_id)
    elif "recalc" in pif.form:
	print "recalc<br>"
	for k in pif.form:
	    if k[-4:] == ".var":
		nvars.append(k[0:-4] + "=" + pif.FormStr(k))
    elif "delete_all" in pif.form:
	print "delete all<br>"
	pif.dbh.DeleteDetail(where = {"mod_id" : mod_id})
	pif.dbh.DeleteVariation(where = {"mod_id" : mod_id})
    elif "delattr" in pif.form:
	print "delattr<br>"
	pif.dbh.DeleteAttribute({"id" : pif.FormStr('delattr')})
    elif "fix_numbers" in pif.form:
	print "fix numbers<br>"
	for k in pif.form:
	    if k[-8:] == ".orignum":
		if pif.FormStr(k) != k[0:-8]:
		    retvar = -999
		    vars.RenameVariation(pif, mod_id, pif.FormStr(k), k[0:-8])
    print "<br><hr>"

    args = ''
    if 'f' in pif.form:
	ShowFile(pif, pif.form.get('d', 'src/mbxf'), pif.FormStr('f'), ' '.join(nvars))
    else:
	ShowFiles(pif, pif.form.get('d', 'src/mbxf'), start=pif.form.get('s'), num=pif.FormInt('n', 100), ff=int(pif.form.get('ff', 0)))

    print pif.render.FormatTail()

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''

