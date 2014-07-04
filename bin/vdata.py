#!/usr/local/bin/python
# -*- coding: utf8 -*-

import os, re, sys
import config
import mbdata

'''
CleanHeader
GetModelRec
HeaderColumnChange
Initialize
RowColumnChange
TransformRow
GetFileList
GetModelIDs
'''

#------- html ------------------------------------------------

cm_re = re.compile(r'<!--.*?-->', re.S)
hl_re = re.compile(r'\\hline')
ml_re = re.compile(r'<[^>]*>', re.S)
tab_re = re.compile(r'<table[^>]*>(?P<c>.*?)</table>', re.S)
row_re = re.compile(r'<tr[^>]*>(?P<c>.*?)</tr>', re.S)
cel_re = re.compile(r'<t(?P<t>[hd])[^>]*>(?P<c>.*?)</t[hd]>', re.S)
div_re = re.compile('</?div.*?>', re.S | re.M)

def GetHtmlTables(fn):
    f = open(fn).read()
    f = cm_re.sub('', f)
    f = hl_re.sub('', f)
    f = div_re.sub('', f)

    tables = list()
    while 1:
	fitab = tab_re.search(f)
	if not fitab:
	    rest = f
	    break

	pred = f[:fitab.start()]
	tab_con = fitab.group('c')
	rows = list()
	while 1:
	    row = row_re.search(tab_con)
	    if not row:
		break

	    row_con = row.group('c')
	    cels = list()
	    while 1:
		cel = cel_re.search(row_con)
		if not cel:
		    break

		cel_con = ml_re.sub('', cel.group('c'))
		cels.append(cel_con)

		row_con = row_con[cel.end():]
	    tab_con = tab_con[row.end():]
	    rows.append(cels)
	f = f[fitab.end():]
	tables.append([pred, rows, ''])
    if tables:
	tables[-1][-1] = rest
    else:
	tables.append(['', list(), rest])
    return tables

#------- data ------------------------------------------------

column_change = []
pre_cell_change = {}
post_cell_change = {}
fnlookup = []

column_split_delim = {
	'body_license_plate' : ' ',
	'windows_rear_side_window_corners' : ',',
}

htrans = [
	[ "^\s*#\s*$", "var" ],
	[ "&amp;", "&" ],
	[ "&nbsp;", "_" ],
	[ "&nbsp", "_" ],
	[ '&#169', "copyright" ],
	[ '\xa9', "copyright" ],
	[ '\s+', '_'],
	[ '''["$%&'()*+,/:;<=>?Z[\\^`{|}~.]''', '_' ],
	[ ']', '_' ],
	[ '!', '_' ],
	[ '/', '_' ],
	[ '--*', '-' ],
	[ '__*', '_' ],
	[ "-_", '-' ],
	[ "_-", '-' ],
	[ '#', 'number' ],
	[ "_hub_s", "_hubs" ],
	[ "\\bare_a", "area" ],
	[ "\\bar_ea", "area" ],
	[ "\\ba_rea", "area" ],
	[ "\\bd_ate", "date" ],
	[ "\\bb_ase", "base" ],
	[ "_b_ase", "_base" ],
	[ "_beh_", "_behind_" ],
	[ "_betw_", "_between_" ],
	[ "\\bb_ody", "body" ],
	[ "_b_ody", "_body" ],
	[ "_compart_", "_compartment_" ],
	[ "\\bc_ontainer", "container" ],
	[ "\\bd_ump", "dump" ],
	[ "\\be_xhaust", "exhaust" ],
	[ "\\bengine_s", "engines" ],
	[ "_eng_", "_engine_" ],
	[ "_engine_s", "_engines" ],
	[ "_equip_", "_equipment_" ],
	[ "\\bf_ork", "fork" ],
	[ "_frt_", "_front_" ],
	[ "\\bfrt", "front" ],
	[ "\\bf_ront", "front" ],
	[ "\\bfrt_eng_", "front_engine_" ],
	[ "\\bhub_s", "hubs" ],
	[ "\\binter_", "interior" ],
	[ "_ins_", "_inside_" ],
	[ "\\bl_ic", "lic" ],
	[ "\\blic_", "license_" ],
	[ "\\bl_ight", "light" ],
	[ "_l_ight", "_light" ],
	[ "_lts_", "_lights_" ],
	[ "\\bl_ower", "lower" ],
	[ "\\blabe_l", "label" ],
	[ "\\blabel_s", "labels" ],
	[ "_num_", "_number_" ],
	[ "\\bpat_", "patent_" ],
	[ "_pl_", "_plate_" ],
	[ "_platf_", "_platform_" ],
	[ "\\bp_r_opeller", "propeller" ],
	[ "\\br_ear", "rear" ],
	[ "_reinf_", "_reinforcement_" ],
	[ "_reinf$", "_reinforcement" ],
	[ "_rider_s_", "_riders_" ],
	[ "\\br_oof", "roof" ],
	[ "\\broller_s", "rollers" ],
	[ "_squ_", "_square_" ],
	[ "_supp_", "_support_" ],
	[ "\\bt_ampo", "tampo" ],
	[ "\\btailg_", "tailgate_" ],
	[ "\\btriang_", "triangle_" ],
	[ "\\bu_pper", "upper" ],
	[ "\\bw_heels", "wheels" ],
	[ "\\bw_ind", "wind" ],
	[ "\\bw_in_d", "wind" ],
	[ "_w_ind", "wind" ],
	[ "\\bwind_", "window" ],
	[ "_win_", "_window_" ],
	[ "\\bwin_", "_window_" ],
	[ "\\bw_indow", "window" ],
	[ "\\bw_ings", "wings" ],
	[ "_w_ings", "_wings" ],
	[ "\\bwh_eels", "wheels" ],
	[ "_wh_eels", "_wheels" ],
	[ "_wheel_s", "_wheels" ],
	[ "\\bwheel_s", "wheels" ],
	[ "_no_", "_number_" ],
	[ "_reinforcem_*$", "_reinforcement" ],
	[ "_lic_pl_*$", "_license_plate_" ],
	[ "_lic_", "_license_" ],
	[ "_pat_", "_patent_" ],
	[ "tempa", "tampo" ],
	[ "^_+", "" ],
	[ "_+$", "" ],
	[ "-", "" ]
]

trans1 = [
	[ "\s\s*", " " ],
	[ "\.\.\.*", "." ],
	[ "\\bw/", "with " ],
	[ "\\bwo/", "without " ],
	[ "/", " / " ],
	[ ",\\s*$", " " ],
	[ "/\\s*/", "// " ],
	[ "&amp;", "and " ],
	[ '&nbsp;', ' ' ],
]

trans2 = []    # trans2 comes from the file

trans3 = [
	[ ", none$", "" ],
	[ ", none,", "," ],
	[ "\\bnone\\b", "no " ],
	[ ", - ", ", no " ],
	[ ", no *$", "" ],
	[ ", no *,", "," ],
	[ "  *-", "-" ],
	[ "-  *", "-" ],
	[ "  *,  *", ", " ],
	[ "\( *", " (" ],
	[ " *\)", ") " ],
	[ " *\| *", "|" ],
	[ "\s*,\s*", ", " ],
	[ "   *", " " ], # do these two last
	[ "^  *", "" ],
	#[ "  *$", "" ]
]

ctrans = []

#api

specialchars = {
	'\xa0' : ' ',
	'&#169' : '\xc2\xa9',
	'&#174' : '\xc2\xae',
	'&#178' : '\xc2\xb2',
	'&#188' : '\xc2\xbc',
	'&#195' : '\xc3\x83',
	'&#196' : '\xc3\x84',
	'&#201' : '\xc3\x89',
	'&#204' : '\xc3\x8c',
	'&#209' : '\xc3\x91',
	'&#214' : '\xc3\x96',
	'&#220' : '\xc3\x9c',
	'&#8221' : '\xe2\x80\x9d',
	'&quot;' : '"',
	'&#8230' : '\xe2\x80\xa6',
	'&#1640' : '\xd9\xa8',
	'&#9829' : '\xe2\x99\xa5',
}

#------- support ---------------------------------------------

def InterpretBase(obase, omanuf):
    plant = ''
    nbase = obase
    for plant_re in plants:
	m = plant_re.search(obase)
	if m:
	    plant = obase[m.start():m.end()].strip()
	    nbase = TransformCell(plant_re.sub(' ', obase, 1).strip())
	    #debug('IB', plant_re.pattern, obase[m.start():m.end()])
	    break
    if omanuf:
	if plant:
	    plant = ', '.join([omanuf, plant])
	else:
	    plant = omanuf
    return nbase, plant

comment_pending = False
def debug(*arg, **kwargs):
    return
    if not comment_pending:
	print '<!--',
    if kwargs.get('nonl'):
	print ' '.join([str(x) for x in arg]),
	comment_pending = True
    else:
	print ' '.join([str(x) for x in arg]), '-->'
	comment_pending = False

#------- api -------------------------------------------------

def RowColumnChange(file_id, row):
    debug('RCC 1', row)
    for chg_ent in base_change.get(file_id, []):
	hdr, nhdr = chg_ent
	row[nhdr[0]] = row[hdr[0]]
	row[hdr[0]] = ''
    debug('RCC 2', row)
    for hdr in pre_cell_change.get(file_id, []) + pre_cell_change.get('', []):
	if hdr[0] in row and hdr[1].search(row[hdr[0]]):
	    debug('RCC 2b', hdr)
	    debug('  from', row[hdr[0]], nonl=True)
	    row[hdr[0]] = hdr[1].sub(hdr[2], row[hdr[0]]).strip()
	    debug('to', row[hdr[0]])
    debug('RCC 3', row)
    row['base'], row['manufacture'] = InterpretBase(row.get('base', ''), row.get('manufacture'))
    if 'base_insert' in row and not row['manufacture']:
	row['base_insert'], row['manufacture'] = InterpretBase(row.get('base_insert', ''), row.get('manufacture'))
    debug('RCC 4', row)
    for chg_ent in column_change.get('', []) + column_change.get(file_id, []):
	hdr, nhdrs = chg_ent
	debug('RCC 4a', chg_ent)
	if len(hdr) == 1:  # 1 to 1 or 1 to N split
	    hdr = hdr[0]
	    if not hdr in row:
		debug('RCC 4b -->')
		continue
	    if hdr in column_split_delim:
		debug('RCC 4c -->')
		flds = row[hdr].rsplit(column_split_delim[hdr], len(nhdrs) - 1)
		if len(flds) < len(nhdrs):
		    flds.append('')
	    else:
		debug('RCC 4d', nonl=True)
		flds = row[hdr].split('/', len(nhdrs) - 1)
		debug(flds)
	    if len(flds) == len(nhdrs):
		row[hdr] = ''
		for nhdr in nhdrs:
		    debug('RCC 4e', nhdr, nonl=True)
		    fldadd = ''
		    if '+' in nhdr:
			fldadd = nhdr[nhdr.find('+') + 1:]
			nhdr = nhdr[:nhdr.find('+')]
		    debug(row.get(nhdr), nonl=True)
		    row[nhdr] = (row.get(nhdr, '') + ' ' + flds.pop(0).strip() + fldadd).strip()
		    debug('to', row[nhdr])
	    else:
		debug('RCC 4f -->')
		for nhdr in nhdrs:
		    fldadd = ''
		    if '+' in nhdr:
			fldadd = nhdr[nhdr.find('+') + 1:]
		    row[nhdr] = row[hdr] + fldadd
	else:  # N to 1 join
	    debug('RCC 4g -->')
	    nhdr = nhdrs[0]
	    nvals = []
	    for shdr in hdr:
		debug('RCC 4h', shdr, row.get(shdr))
		if shdr in row:
		    if row[shdr] != 'no' and row[shdr] not in nvals:
			nvals.append(row[shdr])
	    if nvals:
		row[nhdr] = ', '.join(nvals)
	    else:
		row[nhdr] = 'no'
    debug('RCC 5', row)
    for key in row:
	if row[key].endswith(' ' + key.replace('_', ' ')):
	    row[key] = row[key][:-len(key)].strip()
    debug('RCC 6', row)
    for hdr in post_cell_change.get(file_id, []) + post_cell_change.get('', []):
	debug('RCC 6b', hdr, nonl=True)
	if hdr[0] in row:
	    debug('yes', nonl=True)
	    row[hdr[0]] = hdr[1].sub(hdr[2], row[hdr[0]]).strip()
	for pp in trans3:
	    row[hdr[0]] = pp[0].sub(pp[1], row[hdr[0]])
	debug('-->')
    debug('RCC 7', row)
#    if row.get('note') in mbdata.code2_categories and row.get('category', None) == '':
#	row['category'] = row['note']
#	row['note'] = ''
    debug('RCC 8', row)
    return row


def HeaderColumnChange(file_id, hdrs):
    #debug('HCC0', column_change.get(file_id, []))
    #debug('HCC1', hdrs)
    nhdrs = []
    for hdr in hdrs:
	#debug('HCC3', hdr)
	for ent in base_change.get(file_id, []):
	    if hdr == ent[0][0]:
		hdr = ent[1][0]
		break
	#debug('HCC4', hdr)
	found = False
	for ent in column_change.get('', []) + column_change.get(file_id, []):
	    #debug('HCC5', hdr, ent)
	    if len(ent[0]) == 1:  # 1 to 1 or 1 to N split
		#debug('HCC6')
		if not hdr == ent[0][0]:
		    continue
		found = True
		hdr = ent[0][0]
		newhdrs = ent[1]
		for nhdr in newhdrs:
		    if nhdr.find('+') >= 0:
			nhdr = nhdr[:nhdr.find('+')]
		    if not nhdr in nhdrs:
			nhdrs.append(nhdr)
	    else:
		#debug('HCC7')
		if hdr == ent[0][0]:
		    nhdrs.append(ent[1][0])
		    found = True
		elif hdr in ent[0][1:]:
		    found = True
	if not found and not hdr in nhdrs:
	    #debug('HCC8', hdr)
	    nhdrs.append(hdr)
    if 'manufacture' not in nhdrs:
	nhdrs.append('manufacture')
    #debug('HCC9', nhdrs)
    return nhdrs


def TransformRow(row, num_file_hdrs):
    row = [TransformCell(x) for x in row]
    while len(row) < num_file_hdrs:
	row.append('')
    return row


def TransformCell(txt):
    global specialchars, ctrans
    for k in specialchars:
	txt = txt.replace(k, specialchars[k])
    for pp in ctrans:
	txt = pp[0].sub(pp[1], txt)
    return txt.strip()


def CleanHeader(txt):
    global htrans
    txt = txt.replace('\xa0', ' ').strip()
    #debug('CleanHeader', '"%s"' % txt, nonl=True)
    for pp in htrans:
	txt = pp[0].sub(pp[1], txt)
	#debug('[%s] "%s"' % (pp[0].pattern, txt), nonl=True)
    #debug("-->")
    return txt


def GetModelIDs(omn):
    global fnlookup
    mn = omn
    for fnl in fnlookup:
	if fnl[0] == omn:
	    return fnl[1]
	elif isinstance(fnl[0], str):
	    continue
	else:
	    fnl_m = fnl[0].match(omn)
	    if fnl_m:
		mn = fnl[1][0] % fnl_m.group('n')
		break
    return [mn]


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


def ShowSettings(sets, cols):
    if sets:
	debug('<table border=1 width=100%>')
	for row in sets:
	    debug('<tr>')
	    for col in row:
		if isinstance(col, list):
		    debug('<td>%s</td>' % '; '.join(col))
		elif isinstance(col, str):
		    debug('<td>%s</td>' % col)
		else:
		    debug('<td>%s</td>' % col.pattern)
	    debug('</tr>')
	debug('</table>')


def ShowFileSettings(fn):
    debug('<table border=1 width=100%><tr><th width=33%>Bases</th><th width=33%>Columns</th><th width=33%>Cells</th></tr>')
    debug('<tr><td valign=top>')
    ShowSettings(base_change.get(fn), 2)
    debug('</td><td valign=top>')
    ShowSettings(column_change.get(fn), 2)
    debug('</td><td valign=top>')
    ShowSettings(pre_cell_change.get(fn), 3)
    debug('</td><td valign=top>')
    ShowSettings(post_cell_change.get(fn), 3)
    debug('</td></tr>')
    debug('</table>')


def ReadDat(fn):
    return open(os.path.join(config.srcdir, fn + '.dat')).readlines()


init_done = False
def Initialize(pif):
    global fnlookup, trans1, trans2, trans3, ctrans, htrans, plants, base_change, column_change, pre_cell_change, post_cell_change, init_done
    if not init_done:
	fnlookup = ReadFilenames(ReadDat('vfilename'))
	plants = ReadPlants(ReadDat('vplants'))
	trans1 = [[re.compile(x[0] + '\s*'), x[1]] for x in trans1]
	trans2 = ReadTrans(ReadDat('vtrans'))
	trans3 = [[re.compile(x[0] + '\s*'), x[1]] for x in trans3]
	ctrans = trans1 + trans2 + trans3
	htrans = [[re.compile(x[0], re.S|re.M), x[1]] for x in htrans]
	base_change = ReadColumnChange(ReadDat('vbases'))
	column_change = ReadColumnChange(ReadDat('vcolumns'))
	pre_cell_change = ReadCellChange(ReadDat('vpre'))
	post_cell_change = ReadCellChange(ReadDat('vpost'))
	pif.dbh.SetVerbose(True)
	init_done = True

#------- initialize data -------------------------------------

def ReadColumnChange(fil):
    changes = {}
    for ln in fil:
	ln = ln.strip()
	if ln and not ln.startswith('#'):
	    mn, col, colto = ln.split('|')
	    changes.setdefault(mn, [])
	    changes[mn].append([col.split(';'), colto.split(';')])
    return changes


def ReadPlants(fil):
    changes = []
    i = 0
    for ln in fil:
	ln = ln.strip()
	i += 1
	if ln and not ln.startswith('#'):
	    changes.append(re.compile(ln))
    return changes


def ReadCellChange(fil):
    changes = {}
    for ln in fil:
	ln = ln.strip()
	if ln and not ln.startswith('#'):
	    mn, col, replfrom, replto = ln.split('|')[0:4]
	    changes.setdefault(mn, [])
	    changes[mn].append([col, re.compile(replfrom), replto])
    return changes


def ReadTrans(fil):
    changes = []
    for ln in fil:
	ln = ln.strip()
	if ln and not ln.startswith('#'):
	    transfrom, transto = ln.split('|')[:2]
	    transfrom = '\\b' + transfrom.replace('.', '\\.').replace(' ', '\\s').replace('>', '\\b')
	    changes.append([re.compile(transfrom), transto])
    return changes


def ReadFilenames(fil):
    changes = []
    for ln in fil:
	ln = ln.strip()
	if ln and not ln.startswith('#'):
	    transfrom, transto = ln.split('|')[:2]
	    if transfrom.find('?') >= 0:
		transfrom = re.compile('^%s$' % transfrom)
	    changes.append([transfrom, transto.split(';')])
    return changes

#------- whew ------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''

