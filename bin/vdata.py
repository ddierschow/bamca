#!/usr/local/bin/python
# -*- coding: utf8 -*-

import os, re, sys
import config
import useful

'''
VariationImportData
GetFileList
GetModelIDs
GetHtmlTables
ShowFileSettings

TransformHeader
HeaderColumnChange
TransformRow
RowColumnChange
'''

class VariationImportData:
    verbose = False

    #------- html ------------------------------------------------

    cmt_re = re.compile(r'<!--.*?-->', re.S)
    hln_re = re.compile(r'\\hline')
    mup_re = re.compile(r'<[^>]*>', re.S)
    tab_re = re.compile(r'<table[^>]*>(?P<c>.*?)</table>', re.S)
    row_re = re.compile(r'<tr[^>]*>(?P<c>.*?)</tr>', re.S)
    cel_re = re.compile(r'<t(?P<t>[hd])[^>]*>(?P<c>.*?)</t[hd]>', re.S)
    div_re = re.compile('</?div.*?>', re.S | re.M)

    def __init__(self):
	self.InitData()
	self.fnlookup = self.ReadFilenames(self.ReadDat('vfilename'))
	self.plants = self.ReadPlants(self.ReadDat('vplants'))
	self.trans1 = [[re.compile(x[0] + '\s*'), x[1]] for x in self.trans1]
	self.trans2 = self.ReadTrans(self.ReadDat('vtrans'))
	self.trans3 = [[re.compile(x[0] + '\s*'), x[1]] for x in self.trans3]
	self.ctrans = self.trans1 + self.trans2 + self.trans3
	self.htrans = [[re.compile(x[0], re.S|re.M), x[1]] for x in self.htrans]
	self.base_change = self.ReadColumnChange(self.ReadDat('vbases'))
	self.column_change = self.ReadColumnChange(self.ReadDat('vcolumns'))
	self.pre_cell_change = self.ReadCellChange(self.ReadDat('vpre'))
	self.post_cell_change = self.ReadCellChange(self.ReadDat('vpost'))

    #------- data ------------------------------------------------

    def InitData(self):

	self.column_split_delim = {
		'body_license_plate' : ' ',
		'windows_rear_side_window_corners' : ',',
	}

	self.htrans = [
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

	self.trans1 = [
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

	self.trans3 = [
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

	self.specialchars = {
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


    def GetHtmlTables(self, fn):
	f = open(fn).read()
	f = self.cmt_re.sub('', f)
	f = self.hln_re.sub('', f)
	f = self.div_re.sub('', f)

	tables = list()
	while 1:
	    fitab = self.tab_re.search(f)
	    if not fitab:
		rest = f
		break

	    pred = f[:fitab.start()]
	    tab_con = fitab.group('c')
	    rows = list()
	    while 1:
		row = self.row_re.search(tab_con)
		if not row:
		    break

		row_con = row.group('c')
		cels = list()
		while 1:
		    cel = self.cel_re.search(row_con)
		    if not cel:
			break

		    cel_con = self.mup_re.sub('', cel.group('c'))
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

    #------- support ---------------------------------------------

    def InterpretBase(self, obase, omanuf):
	plant = other = ''
	if '/' in obase:
	    obase, other = obase.split('/', 1)
	    other = ' / ' + other
	nbase = obase
	for plant_re in self.plants:
	    m = plant_re.search(obase)
	    if m:
		plant = obase[m.start():m.end()].strip()
		nbase = self.TransformCell(plant_re.sub(' ', obase, 1).strip())
		#self.debug('IB', plant_re.pattern, obase[m.start():m.end()])
		break
	if omanuf:
	    if plant:
		plant = ', '.join([omanuf, plant])
	    else:
		plant = omanuf
	return nbase + other, plant

    def debug(self, *arg, **kwargs):
	if self.verbose:
	    useful.WriteComment(*arg, **kwargs)
	return
    #    if not comment_pending:
    #	print '<!--',
    #    if kwargs.get('nonl'):
    #	print ' '.join([str(x) for x in arg]),
    #	comment_pending = True
    #    else:
    #	print ' '.join([str(x) for x in arg]), '-->'
    #	comment_pending = False
    #comment_pending = False

    #------- api -------------------------------------------------

    # 1. base_change
    # 2. pre_cell_change
    # 3. InterpretBase
    # 4. column_change
    # 5. strip column name
    # 6. post_cell_change
    def RowColumnChange(self, file_id, row):
	self.debug('RCC 1', row)
	row['imported_from'] = file_id
	for chg_ent in self.base_change.get(file_id, []):
	    hdr, nhdr = chg_ent
	    row[nhdr[0]] = row[hdr[0]]
	    row[hdr[0]] = ''
	    del row[hdr[0]]
	self.debug('RCC 2', row)
	for hdr in self.pre_cell_change.get(file_id, []) + self.pre_cell_change.get('', []):
	    if hdr[0] in row and hdr[1].search(row[hdr[0]]):
		self.debug('RCC 2b', hdr)
		self.debug('  from', row[hdr[0]], nonl=True)
		row[hdr[0]] = hdr[1].sub(hdr[2], row[hdr[0]]).strip()
		self.debug('to', row[hdr[0]])
	self.debug('RCC 3', row)
	row['base'], row['manufacture'] = self.InterpretBase(row.get('base', ''), row.get('manufacture'))
	if 'base_insert' in row and not row['manufacture']:
	    row['base_insert'], row['manufacture'] = self.InterpretBase(row.get('base_insert', ''), row.get('manufacture'))
	self.debug('RCC 4', row)
	for chg_ent in self.column_change.get('', []) + self.column_change.get(file_id, []):
	    hdr, nhdrs = chg_ent
	    self.debug('RCC 4a', chg_ent)
	    if len(hdr) == 1:  # 1 to 1 or 1 to N split
		hdr = hdr[0]
		if not hdr in row:
		    self.debug('RCC 4b -->')
		    continue
		if hdr in self.column_split_delim:
		    self.debug('RCC 4c -->')
		    flds = row[hdr].rsplit(self.column_split_delim[hdr], len(nhdrs) - 1)
		    if len(flds) < len(nhdrs):
			flds.append('')
		else:
		    self.debug('RCC 4d', nonl=True)
		    flds = row[hdr].split('/', len(nhdrs) - 1)
		    self.debug(flds)
		if len(flds) == len(nhdrs):
		    row[hdr] = ''
		    for nhdr in nhdrs:
			self.debug('RCC 4e', nhdr, nonl=True)
			fldadd = ''
			if '+' in nhdr:
			    fldadd = nhdr[nhdr.find('+') + 1:]
			    nhdr = nhdr[:nhdr.find('+')]
			self.debug(row.get(nhdr), nonl=True)
			row[nhdr] = (row.get(nhdr, '') + ' ' + flds.pop(0).strip() + fldadd).strip()
			self.debug('to', row[nhdr])
		else:
		    self.debug('RCC 4f -->')
		    for nhdr in nhdrs:
			fldadd = ''
			if '+' in nhdr:
			    fldadd = nhdr[nhdr.find('+') + 1:]
			row[nhdr] = row[hdr] + fldadd
	    else:  # N to 1 join
		self.debug('RCC 4g -->')
		nhdr = nhdrs[0]
		nvals = list()
		for shdr in hdr:
		    self.debug('RCC 4h', shdr, row.get(shdr))
		    if shdr in row:
			if row[shdr] != 'no' and row[shdr] not in nvals:
			    nvals.append(row[shdr])
		if nvals:
		    row[nhdr] = ', '.join(nvals)
		else:
		    row[nhdr] = 'no'
	self.debug('RCC 5', row)
	for key in row:
	    if row[key].endswith(' ' + key.replace('_', ' ')):
		row[key] = row[key][:-len(key)].strip()
	self.debug('RCC 6', row)
	for hdr in self.post_cell_change.get(file_id, []) + self.post_cell_change.get('', []):
	    self.debug('RCC 6b', hdr, nonl=True)
	    if hdr[0] in row:
		self.debug('yes', nonl=True)
		row[hdr[0]] = hdr[1].sub(hdr[2], row[hdr[0]]).strip()
	    for pp in self.trans3: # WTF?
		row[hdr[0]] = pp[0].sub(pp[1], row[hdr[0]])
	    self.debug('-->')
    #    self.debug('RCC 7', row)
    #    import mbdata
    #    if row.get('note') in mbdata.code2_categories and row.get('category', None) == '':
    #	row['category'] = row['note']
    #	row['note'] = ''
	self.debug('RCC X', row)
	row['is_valid'] = True
	return row


    def HeaderColumnChange(self, file_id, hdrs):
	#self.debug('HCC0', self.column_change.get(file_id, []))
	#self.debug('HCC1', hdrs)
	nhdrs = list()
	for hdr in hdrs:
	    #self.debug('HCC3', hdr)
	    for ent in self.base_change.get(file_id, []):
		if hdr == ent[0][0]:
		    hdr = ent[1][0]
		    break
	    #self.debug('HCC4', hdr)
	    found = False
	    for ent in self.column_change.get('', []) + self.column_change.get(file_id, []):
		#self.debug('HCC5', hdr, ent)
		if len(ent[0]) == 1:  # 1 to 1 or 1 to N split
		    #self.debug('HCC6')
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
		    #self.debug('HCC7')
		    if hdr == ent[0][0]:
			nhdrs.append(ent[1][0])
			found = True
		    elif hdr in ent[0][1:]:
			found = True
	    if not found and not hdr in nhdrs:
		#self.debug('HCC8', hdr)
		nhdrs.append(hdr)
	if 'manufacture' not in nhdrs:
	    nhdrs.append('manufacture')
	#self.debug('HCC9', nhdrs)
	return nhdrs


    def TransformRow(self, row):
	row = [self.TransformCell(x) for x in row]
	return row


    def TransformCell(self, txt):
	for k in self.specialchars:
	    txt = txt.replace(k, self.specialchars[k])
	for pp in self.ctrans:
	    txt = pp[0].sub(pp[1], txt)
	return txt.strip()


    def TransformHeader(self, txt):
	txt = txt.replace('\xa0', ' ').strip()
	for pp in self.htrans:
	    txt = pp[0].sub(pp[1], txt)
	return txt


    def GetModelIDs(self, omn):
	mn = omn
	for fnl in self.fnlookup:
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


    def ShowSettings(self, sets, cols):
	if sets:
	    print '<table border=1 width=100%>'
	    for row in sets:
		print '<tr>'
		for col in row:
		    if isinstance(col, list):
			print '<td>%s</td>' % '; '.join(col)
		    elif isinstance(col, str):
			print '<td>%s</td>' % col
		    else:
			print '<td>%s</td>' % col.pattern
		print '</tr>'
	    print '</table>'


    def ShowFileSettings(self, fn):
	print '<table border=1 width=100%><tr><th width=33%>Bases</th><th width=33%>Columns</th><th width=33%>Cells</th></tr>'
	print '<tr><td valign=top>'
	self.ShowSettings(self.base_change.get(fn), 2)
	print '</td><td valign=top>'
	self.ShowSettings(self.column_change.get(fn), 2)
	print '</td><td valign=top>'
	self.ShowSettings(self.pre_cell_change.get(fn), 3)
	print '</td><td valign=top>'
	self.ShowSettings(self.post_cell_change.get(fn), 3)
	print '</td></tr>'
	print '</table>'

    #------- initialize data -------------------------------------

    def ReadColumnChange(self, fil):
	changes = dict()
	for ln in fil:
	    mn, col, colto = ln.split('|')
	    changes.setdefault(mn, list())
	    changes[mn].append([col.split(';'), colto.split(';')])
	return changes

    def ReadCellChange(self, fil):
	changes = dict()
	for ln in fil:
	    mn, col, replfrom, replto = ln.split('|')[0:4]
	    changes.setdefault(mn, list())
	    changes[mn].append([col, re.compile(replfrom), replto])
	return changes

    def ReadPlants(self, fil):
	return [re.compile(ln) for ln in fil]

    def ReadTrans(self, fil):
	changes = list()
	for ln in fil:
	    transfrom, transto = ln.split('|')[:2]
	    transfrom = '\\b' + transfrom.replace('.', '\\.').replace(' ', '\\s').replace('>', '\\b')
	    changes.append([re.compile(transfrom), transto])
	return changes

    def ReadFilenames(self, fil):
	changes = list()
	for ln in fil:
	    transfrom, transto = ln.split('|')[:2]
	    if transfrom.find('?') >= 0:
		transfrom = re.compile('^%s$' % transfrom)
	    changes.append([transfrom, transto.split(';')])
	return changes

    def ReadDat(self, fn):
	dat = open(os.path.join(config.srcdir, fn + '.dat')).readlines()
	dat = filter(lambda x: x and not x.startswith('#'), [ln.strip() for ln in dat])
	return dat

#------- whew ------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''

