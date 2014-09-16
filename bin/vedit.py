#!/usr/local/bin/python
# -*- coding: latin-1 -*-

"""Variation Importer

This modules (with vdata) imports variations from the Word files
that are kept on mbxforum.nl.

This was grown over the course of several years, and at this point
I'm not completely sure how it works.  If you go forward from here
and try to understand it, I take no responsibility for your sanity.

Everything happens in two contexts: doing the index, and doing the
individual model editor.  So you'll see very similar looking functions
in some cases.

Good luck.
"""

import glob, itertools, os, re, sys, time

import basics
import config
import tables
import useful
import vars
import vdata

IS_GOOD = 0
IS_NO_MODEL = 1
IS_DIFFERENT_NUMBER = 2
IS_CHANGED_SCHEMA = 3
IS_CHANGED = 4
IS_INVALID = 5
IS_NEW_VAR = 6

file_list_class = {
    IS_GOOD : 'good',
    IS_CHANGED_SCHEMA : 'changed_schema',
    IS_CHANGED : 'changed',
    IS_INVALID : 'changed',
    IS_NEW_VAR : 'changed',
    IS_NO_MODEL : 'no_model',
    IS_DIFFERENT_NUMBER : 'different',
}

var_record_cols = ['var', 'body', 'base', 'windows', 'interior', 'category', 'area', 'date', 'note', 'manufacture', 'imported_from', 'imported_var']

# ----- general helpers ------------------------------------------------

def ParseFile(pif, fdir, fn, args=''):
    modids, fitabs = ReadFile(pif, fdir, fn)
    varfile = {
	'filename' : fn,
	'stat' : {IS_GOOD},
	'modids' : [x for x in modids],
	'tabs' : list(),
	'var_lup' : dict(),
    }
    if not modids:
	varfile['stat'].add(IS_NO_MODEL)
	return varfile

    for arg in args.split(' '):
	if '=' in arg:
	    ovar, nvar = arg.split('=')
	    varfile['var_lup'][ovar] = nvar

    mod = dict()
    for rawfitab in fitabs:
	fitab = {
	    'stat' : set(),
	    'is_valid' : False,
	    'modid' : None,
	    'preface' : '',
	    'filehead' : [],
	    'gridhead' : [],
	    'body' : list(),
	    'epilog' : '',
	    'dbvars' : [],
	    'attrs' : [],
	    'casting' : {}
	}
	varfile['tabs'].append(fitab)
	if not rawfitab:
	    fitab['stat'].add(IS_NO_MODEL)
	    continue
	fitab['preface'] = rawfitab[0]
	if len(rawfitab) < 2 or not len(rawfitab[1]):
	    fitab['stat'].add(IS_NO_MODEL)
	    continue
	modtab = rawfitab[1]
	if len(rawfitab) > 2:
	    fitab['epilog'] = rawfitab[2]

	hdrs = [vid.TransformHeader(x) for x in modtab[0]]
	if hdrs[0] != 'var' or fitab['preface'].find("BOX TYPES") >= 0:
	    fitab['stat'].add(IS_NO_MODEL)
	    fitab['body'] = modtab
	    continue
	fitab['filehead'] = hdrs
	fitab['is_valid'] = True
	num_file_hdrs = len(hdrs) # not including imported_from
	hdrs.append('imported_from')
	fitab['gridhead'] = nhdrs = vid.HeaderColumnChange(fn, hdrs)

	mn = modids.pop(0)
	fitab['modid'] = mn
	mod = GetModelRec(pif, mn)
	fitab['casting'] = mod
	if not mod:
	    fitab['stat'].add(IS_NO_MODEL)
	    continue
	fitab['attrs'] = pif.dbh.FetchAttributes(mod['id'])
	attr_names = var_record_cols + [x['attribute.attribute_name'] for x in fitab['attrs']]

	for hdr in nhdrs:
	    if not hdr in attr_names:
		varfile['stat'].add(IS_CHANGED_SCHEMA)

	varis = pif.dbh.FetchVariations(mod['id'], nodefaults=True)
	varis = pif.dbh.DePref('variation', varis)
	dbvars = {x['var']: x for x in varis}
	fitab['dbvars'] = dbvars

	for row in modtab[1:]:
	    row = vid.TransformRow(row)
	    if not reduce(lambda x,y: x or bool(y), row[1:], False):
		continue
	    rowd = dict(itertools.izip_longest(hdrs, row, fillvalue=""))
	    nrow = vid.RowColumnChange(fn, rowd)
	    if nrow.get('is_valid'):
		fitab['body'].append(nrow)

    return varfile


def ReadFile(pif, fdir, fn):
    modids, fitabs = list(), list()
    if os.path.exists(fdir + '/' + fn + '.html'):
	modids, fitabs = ReadHtmlFile(pif, fdir, fn)
    elif os.path.exists(fdir + '/' + fn + '.htm'):
	modids, fitabs = ReadHtmlFile(pif, fdir, fn)
    elif os.path.exists(fdir + '/' + fn + '.dat'):
	modids, fitabs = ReadDatFile(pif, fdir, fn)
    return modids, fitabs


def ReadHtmlFile(pif, fdir, fn):
    modids = vid.GetModelIDs(fn)
    fitabs = list(), ''
    if not modids:
	pass
    elif os.path.exists(fdir + '/' + fn + '.html'):
	fitabs = vid.GetHtmlTables(fdir + '/' + fn + '.html')
    elif os.path.exists(fdir + '/' + fn + '.htm'):
	fitabs = vid.GetHtmlTables(fdir + '/' + fn + '.htm')
    return modids, fitabs


def ReadDatFile(pif, fdir, fn):
    fn = fdir + '/' + fn + '.dat'
    modids = list()
    fitabs = list()
    fitab = list()
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
	    fitab = list()
	else:
	    fitab.append(ln[1:])
    if fitab:
	fitabs.append((fidesc, fitab))
    return modids, fitabs


def ShowFileLink(fn, ft, show_as):
    fp = os.path.join('src/mbxf', fn + '.' + ft.lower())
    if os.path.exists(fp):
	print '<a href="/%s">%s</a>' % (fp, show_as)


def GetModelRec(pif, mn):
    modrec = pif.dbh.FetchCasting(mn)
    modrec = pif.dbh.DePref('casting', modrec)

    #debug("FetchCasting", mn, modrec)
    if not modrec:
	modrec = pif.dbh.FetchAlias(mn)
	#debug("FetchAlias", mn, modrec)
	if modrec:
	    modrec = pif.dbh.DePref('alias', modrec)
	    modrec = pif.dbh.DePref('casting', modrec)
	    modrec = pif.dbh.DePref('base_id', modrec)
	    modrec['id'] = modrec['ref_id']

    #debug('GetModRec', modrec)
    return modrec


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
    return dict()

# ----- overview functions ---------------------------------------------

def CheckFile(pif, fdir, fn):
    varfile = ParseFile(pif, fdir, fn)

    for fitab in varfile['tabs']:
	if not fitab.get('is_valid'):
	    continue
	for row in fitab['body']:
	    dbvar = FindRec(fn, fitab['dbvars'], row, fitab['gridhead'])
	    if dbvar:
		for col in fitab['gridhead']:
		    if col != 'var' and row.get(col, '') != dbvar.get(col, ''):
			#pif.render.Comment('changed', col, row.get(col, ''), dbvar.get(col, ''))
			varfile['stat'].add(IS_CHANGED)
		if dbvar['var'] != row['var'] and row['var'][0] != 'f':
		    #pif.render.Comment('diff#', dbvar['var'], row['var'])
		    varfile['stat'].add(IS_DIFFERENT_NUMBER)
	    else:
		varfile['stat'].add(IS_NEW_VAR)
		break

    return varfile


def GetFileList(fdir):
    dats = list()
    for ext in ['htm', 'html', 'dat']:
	dats += [x[x.rfind('/') + 1:x.rfind('.')] for x in glob.glob(fdir + '/*.' + ext)]
    dats = list(set(dats))
    dats.sort()
    return dats


# ff: 0 = all, 1 = changed or differing var id, 2 = changed only
def ShowIndex(pif, fdir, start=None, num=100, ff=0):
    cols = 4
    dats = GetFileList(fdir)
    if not dats:
	print "no files?"
	return
    print pif.render.FormatLink("?ff=1&d=" + fdir + "&s=" + start + "&n=" + str(num), 'Diff-ID'), '-'
    print pif.render.FormatLink("?ff=2&d=" + fdir + "&s=" + start + "&n=" + str(num), 'Diff'), '-'
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
	    varfile = CheckFile(pif, fdir, fn)
	    mod_update = max(varfile['stat'])
	    if ff and (mod_update == IS_GOOD or mod_update == IS_NO_MODEL):
		continue
	    if ff == 2 and mod_update == IS_DIFFERENT_NUMBER:
		continue
	    sclass = ' '.join([file_list_class[x] for x in varfile['stat']])
	    print '<a href="?d=%s&f=%s"><span class="%s">%s</span></a>' % (fdir, fn, sclass, fn)
	    ShowFileLink(fn, 'doc', 'w')
	    ShowFileLink(fn, 'htm', 'h')
	    ShowFileLink(fn, 'html', 'h')
	    #print list(varfile['stat'])
	    print '<br>'
	    irow += 1
	    sys.stdout.flush()
	    if irow == rows:
		break
	print '</td>'
    print "</tr></table>"
    print 'done'

# ----- single file importer -------------------------------------------

#{'definition': 'varchar(64)', 'mod_id': 'MB652', 'attribute_name': 'dump', 'id': 1L}
def ShowAttrs(pif, file_id, mod, hdrs, var_desc):
    mod_id = mod['id']
    attrs = pif.dbh.FetchAttributes(mod_id)
    attrs = pif.dbh.DePref('attribute', attrs)
    print '<form method="post">'
    print '<input type="hidden" name="mod_id" value="%s">' % mod_id
    det = pif.dbh.FetchDetails(mod_id, "").get('', dict())
    det = pif.dbh.DePref('detail', det)
    print "<table border=1>"
    print "<tr><th>ID</th><th>Name</th><th>Definition</th><th>Title</th><th>V</th><th>Default</th></tr>"
    for attr in attrs:
	visuals = {True: ['visual.%(id)d' % attr], False: list()}
	#pif.render.Comment(attr, visuals)
	print "<tr>"
	print '<td style="background-color: %s">' % bg_color[attr['attribute_name'] in hdrs + var_record_cols]
	print '<a href="%s">%s</a></td>' % (pif.dbh.GetEditorLink('attribute', {'id' : attr['id']}), attr['id'])
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
	trailer = chr(ord(trailer) + 1) if trailer else 'a'


def CastingHelp(pif, col, mod):
    if col == 'rawname':
	return ' | '.join(mod.get('iconname', list()))
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


text_color = {True : '#0000FF', False : '#FF0000'}
bg_color = {True : '#FFFFFF', False : '#FFCCCC'}
paren_re = re.compile(r'\((?P<len>\d*)\)')
def ShowFile(pif, fdir, fn, args):
    varfile = ParseFile(pif, fdir, fn, args)
    #modids, fitabs = ReadFile(pif, fdir, fn)
    if not varfile['modids']:
	print "Huh?"
	return

    print '<h3>File Settings</h3>'
    vid.ShowFileSettings(fn)
    print '<br>'
    print list(varfile['stat']), '-'

    ShowFileLink(fn, 'html', 'HTML')
    ShowFileLink(fn, 'htm', 'HTM')
    ShowFileLink(fn, 'doc', 'DOC')
    ShowFileLink(fn, 'dat', 'DAT')
    print '-'
    for id in varfile['modids']:
	print '<a href="#%s">%s</a>' % (id, id)
    varfile['var_desc'] = dict([(x['field'], x['type']) for x in pif.dbh.DescribeDict('variation').values()])

    for fitab in varfile['tabs']:
	if fitab['casting']:
	    ShowModelTable(pif, varfile, fitab)
	else:
	    ShowNoModel(pif, varfile, fitab)
	print fitab['epilog']


def ShowNoModel(pif, varfile, fitab):
    print fitab['preface'], "<br>"
    print "<table border=1>"
    for row in [fitab['gridhead']] + fitab['body']:
	print "<tr>"
	for cel in row:
	    print "<td>" + cel + "</td>"
	print "</tr>"
    print "</table>"


def ShowModelTable(pif, varfile, fitab):
    # casting form
    print '<a name="%s"></a>' % fitab['modid']
    mod = fitab['casting']

    for vf in filter(None, [x['imported_from'] for x in pif.dbh.FetchVariationFiles(mod['id'])]):
	print '<a href="?f=%s">%s</a>' % (vf, vf)
    print '<br>'
    print '<center><h2><a href="single.cgi?id=%s">%s</a>' % (mod['id'], mod['id'])
    print "<h3>", mod.get('rawname', 'no rawname?'), "</h3></center>"

    # base id form
    ShowBaseID(pif, mod)

    # casting form
    ShowCasting(pif, mod)

    print fitab['preface'], "<br>"

    # attributes form
    print "<h3>Attributes</h3>"
    ShowAttrs(pif, varfile['filename'], mod, fitab['gridhead'], varfile['var_desc'])

    # variations form
    print "<h3>Variations</h3>"
    dbvars = fitab['dbvars']
    print '<form method="post">'
    print '<input type="hidden" name="current_file" value="%s">' % varfile['filename']
    print '<input type="hidden" name="mod_id" value="%s">' % mod['id']
    print "<table border=1><tr><th></th>"
    for hdr in fitab['gridhead']:
	print "<th>" + hdr + "</th>"
    print "</tr>"
    print "<tr><th></th>"
    for hdr in fitab['gridhead']:
	print "<td>" + varfile['var_desc'][hdr] + "</td>"
    print "</tr>"
    ids_used = list()
    for rec in fitab['body']:
	is_new = False
	orignum = rec['var']
	if rec["var"] in varfile['var_lup']:
	    rec["var"] = varfile['var_lup'].get(rec["var"], rec["var"])
	    dbvar = dbvars.get(rec['var'], dict())
	else:
	    dbvar = FindRec(varfile['filename'], dbvars, rec, fitab['gridhead'])
	if not dbvar:
	    dbvar = {'var' : FindVarID(dbvars, rec, ids_used)}
	    is_new = True
	else: # gray
	    del dbvars[dbvar['var']] # gray
	ids_used.append(dbvar['var'])
	pic = config.imgdirVar + '/s_' + mod['id'].lower() + '-' + dbvar.get('var', '') + '.jpg'
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
	for hdr in fitab['gridhead']:
	    dbdet = str(dbvar.get(hdr, ''))
	    fidet = rec.get(hdr, '')
	    print '<td style="color: %s; background-color: %s">' % (text_color[dbdet == fidet], bg_color[dbdet == fidet])
	    print str(dbvar.get(hdr, '')) + "<br>"
	    if dbdet != fidet or hdr == 'var':
		if fidet:
		    print pif.render.FormatTextInput(rec['var'] + '.' + hdr, int(varfile['var_desc'][hdr][8:-1]), 16, fidet)
		else:
		    print pif.render.FormatTextInput(rec['var'] + '.' + hdr, int(varfile['var_desc'][hdr][8:-1]), 16, "\\b")
	    elif hdr == 'imported_from':
		print '<input type="hidden" name="%s.imported_from" value="%s">' % (rec['var'], varfile['filename'])
		print dbvar.get('imported_var', 'unset')
	    print "</td>"
	print "</tr>"
    dbvarkeys = dbvars.keys()
    dbvarkeys.sort()
    for varid in dbvarkeys:
	dbvar = dbvars[varid]
	is_same_file = dbvar.get('imported_from') == varfile['filename']
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
	for hdr in fitab['gridhead']:
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

# ----- mainlike functions ---------------------------------------------

@basics.WebPage
def HandleForm(pif):
    pif.render.PrintHtml()
    mod_id = pif.FormStr('mod_id')
    if mod_id:
	pif.render.title = 'Variations - ' + mod_id
    elif pif.FormHas('f'):
	pif.render.title = 'Variations - ' + pif.FormStr('f')
    print pif.render.FormatHead()
    if not pif.IsAllowed('a'):
	return

    pif.dbh.SetVerbose(True)
    global vid # for now.  restructuring one thing at a time.
    vid = vdata.VariationImportData()
    vid.verbose = pif.render.verbose
    nvars = list()
    file_dir = pif.FormStr('d', 'src/mbxf')

    if pif.FormHas("recalc"):  # doesn't really fit the pattern
	print "recalc<br>"
	for k in pif.FormKeys(end='.var'):
	    nvars.append(k[0:-4] + "=" + pif.FormStr(k))
    else:
	DoAction(pif, mod_id)
    print "<br><hr>"

    args = ''
    if pif.FormHas('f'):
	ShowFile(pif, file_dir, pif.FormStr('f'), ' '.join(nvars))
    else:
	ShowIndex(pif, file_dir, start=pif.FormStr('s'), num=pif.FormInt('n', 100), ff=int(pif.FormInt('ff')))

    print pif.render.FormatTail()


def SaveAttribute(pif, attr_id):
    attr = pif.dbh.FetchAttribute(attr_id)
    attr = pif.dbh.DePref('attribute', attr)
    if len(attr) == 1:
	attr = attr[0]
	for key in attr.keys():
	    if pif.FormHas(key + '.%d' % attr_id):
		attr[key] = pif.FormStr(key + '.%d' % attr_id)
	pif.dbh.UpdateAttribute(attr, attr_id)

	if pif.FormStr("description.%d" % attr_id) != "":
	    rec = {"mod_id" : attr['mod_id'], "var_id" : "", "attr_id" : attr_id, "description" : pif.FormStr("description.%d" % attr_id)}
	    where = {"mod_id" : attr['mod_id'], "var_id" : "", "attr_id" : attr_id}
	    pif.dbh.Write("detail", rec, where)
    else:
	print '%d attributes returned!' % len(attr)


def DoAction(pif, mod_id):
    if pif.FormHas("add"):
	print "add<br>"
	for k in pif.FormKeys(end='n.definition'): # pretty sure these are the new guys
	    attr = k[0:-12]
	    print "n_def", k, attr
	    rec = {"mod_id" : mod_id, "attribute_name" : pif.FormStr(attr + "n.attribute_name"),
			"title" : pif.FormStr(attr + "n.attribute_name").replace('_', ' ').title(),
			"definition" : pif.FormStr(k)}
	    pif.dbh.Write("attribute", rec, {"mod_id" : mod_id, "attribute_name" : pif.FormStr(attr + "n.attribute_name")})
	for k in pif.FormKeys(start='definition.'):
	    attr = k[11:]
	    print "def", k, attr
	    rec = {"mod_id" : mod_id, "attribute_name" : pif.FormStr('attribute_name.' + attr), "title" : pif.FormStr('title.' + attr),
			"definition" : pif.FormStr(k), "visual" : pif.FormStr("visual." + attr, '1')}
	    pif.dbh.Write("attribute", rec, {"id" : attr}, modonly=True)
	    if pif.FormStr("description." + attr, '') != "":
		rec = {"mod_id" : mod_id, "var_id" : "", "attr_id" : attr, "description" : pif.FormStr("description." + attr)}
		where = {"mod_id" : mod_id, "var_id" : "", "attr_id" : attr}
		pif.dbh.Write("detail", rec, where)
    elif pif.FormHas("add_new"):
	print "add new<br>"
	pif.dbh.Write("attribute", {"mod_id" : mod_id}, list())
    elif pif.FormFind('renattr'):
	keys = pif.FormFind('renattr')
	print "renattr", keys, "<br>"
	for key in keys:
	    attr_id = int(key[8:])
	    SaveAttribute(pif, attr_id)
    elif pif.FormHas("save_base_id"):
	print "save base_id<br>"
	rec = dict()
	for k in pif.FormKeys(start='base_id.'):
	    rec[k[8:]] = pif.FormStr(k)
	pif.dbh.Write("base_id", rec, {"id" : pif.FormStr("base_id.id")})
    elif pif.FormHas("save_casting"):
	print "save casting<br>"
	rec = dict()
	for k in pif.FormKeys(start='casting.'):
	    rec[k[8:]] = pif.FormStr(k)
	pif.dbh.Write("casting", rec, {"id" : pif.FormStr("casting.id")})
    elif pif.FormHas("save"):
	print "save"
	pif.dbh.UpdateVariation({'imported_from' : 'was ' + pif.FormStr('current_file')}, {'imported_from' : pif.FormStr('current_file'), 'mod_id' : mod_id})
	attrs = pif.dbh.FetchAttributes(mod_id)
	attr_lup = dict()
	for attr in attrs:
	    print attr, '<br>'
	    attr_lup[attr['attribute.attribute_name']] = attr.get('attribute.id')
	var_cols = pif.dbh.Columns("variation")
	for k in pif.FormKeys(end='.var'):
	    rec = {"mod_id" : mod_id}
	    rec["imported"] = time.time()
	    det = dict()
	    for vk in pif.FormKeys(start=pif.FormStr(k)):
		vv = pif.FormStr(vk)
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
    elif pif.FormHas("delete_orphans"):
	print "delete orphans<br>"
	orphans = pif.FormList('orphan', list())
	for var_id in orphans:
	    print 'deleting', mod_id, var_id, '<br>'
	    vars.DeleteVariation(pif, mod_id, var_id)
    elif pif.FormHas("delete_all"):
	print "delete all<br>"
	pif.dbh.DeleteDetail(where = {"mod_id" : mod_id})
	pif.dbh.DeleteVariation(where = {"mod_id" : mod_id})
    elif pif.FormHas("delattr"):
	print "delattr<br>"
	pif.dbh.DeleteAttribute({"id" : pif.FormStr('delattr')})
    elif pif.FormHas("fix_numbers"):
	print "fix numbers<br>"
	for k in pif.FormKeys(end='.orignum'):
	    if pif.FormStr(k) != k[0:-8]:
		retvar = -999
		vars.RenameVariation(pif, mod_id, pif.FormStr(k), k[0:-8])

# ----- ----------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''

