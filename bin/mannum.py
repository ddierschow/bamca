#!/usr/local/bin/python

import copy, glob, os, re
import basics
import config
import mbdata
import mflags
import models
import single
import useful

# This file could use a complete rewrite.
# Add: order by

#---- manlist stuff -------------------------

vt_cols = [
	[ 'img', 'pic' ],
	[ 'name', 'name' ],
	[ 'sel', 'sel' ],
]
vt_fmtb = reduce(lambda x,y: x+'<td>%('+y[0]+')s</td>', vt_cols, '<tr>') + '</tr>'
vt_fmth = reduce(lambda x,y: x+'<th>%('+y[0]+')s</th>', vt_cols, '<tr>') + '</tr>'
admin_cols = [
	[ 'own', 'X' ],
	[ 'vid', 'ID' ],
	[ 'unlicensed', '' ],
	[ 'nl', 'Name' ],
	[ 'first_year', 'Year' ],
	[ 'fvyear', 'First' ],
	[ 'lvyear', 'Last' ],
	[ 'scale', 'Scale' ],
	[ 'country', 'CC' ],
	[ 'make', 'Make' ],
	[    '9', 'X'],
	[   '13', 'H'],
	[   '17', 'V'],
	[   '90', 'F'],
	[   '96', 'D'],
	[  '100', 'P'],
	[  '365', 'S'],
	[ '7881', 'F'],
	[ '7187', 'B'],
	[ '7379', 'W'],
	[ '4560', 'D'],
	[   '27', 'P'],
	[ '7783', 'V'],
	[ 'description', 'Description' ],
	[ 'mydesc', 'Mine' ],
]
a_links = ['9', '13', '17', '90', '96', '100', '365', '7881', '7187', '7379', '4560', '27', '7783']
admin_fmtb = reduce(lambda x,y: x+'<td>%('+y[0]+')s</td>', admin_cols, '<tr>') + '</tr>'
admin_fmth = reduce(lambda x,y: x+'<th>%('+y[0]+')s</th>', admin_cols, '<tr>') + '</tr>'
picture_cols = [
	[ 'vid', 'ID' ],
	[ 'unlicensed', '' ],
	[ 'nl', 'Name' ],
	[ 'first_year', 'Year' ],
	[ 'l_', 'L' ],
	[ 'm_', 'M' ],
	[ 's_', 'S' ],
	[ 't_', 'T' ],
	[ 'z_', 'I' ],
	[ 'b_', 'B' ],
	[ 'r_', 'R' ],
	[ 'a_', 'A' ],
	[ 'd_', 'D' ],
	[ 'i_', 'I' ],
	[ 'p_', 'P' ],
	[ 'pic_a', 'All' ],
	[ 'pic_c', 'Core' ],
	[ 'pic_1', 'Code1' ],
	[ 'pic_2', 'Code2' ],
	[ 'pic_f', 'VarF' ],
	#[percent_a, percent_c, percent_1, percent_2, percent_f]
	[ 'description', 'Description' ],
]
picture_fmtb = reduce(lambda x,y: x+'<td>%('+y[0]+')s</td>', picture_cols, '<tr>') + '</tr>'
picture_fmth = reduce(lambda x,y: x+'<th>%('+y[0]+')s</th>', picture_cols, '<tr>') + '</tr>'
mades = {False : '<i>%(name)s</i>', True : '%(name)s'}
prefixes = [
	[ 'a_', config.imgdirAdd ],
	[ 'b_', config.imgdirAdd ],
	[ 'd_', config.imgdirAdd ],
	[ 'i_', config.imgdirAdd ],
	[ 'h_', config.imgdir175 ],
	[ 'l_', config.imgdir175 ],
	[ 'm_', config.imgdir175 ],
	[ 'p_', config.imgdirAdd ],
	[ 'r_', config.imgdirAdd ],
	[ 's_', config.imgdir175 ],
	[ 't_', config.imgdir175 ],
	[ 'z_', config.imgdir175 + '/icon' ],
]

#---- the manno object ----------------------

class MannoFile:
    def __init__(self, pif, withaliases=False):
	self.section = None
	self.start = 1
	self.end = 9999
	self.firstyear = 1
	self.lastyear = 9999
	self.nodesc = pif.FormInt('nodesc')
	vtypes = pif.dbh.FetchVehicleTypes()
	self.tdict = {x['vehicle_type.ch']: x['vehicle_type.name'] for x in vtypes}
	self.types = {'y':"", 'n':"", 'm': "".join(self.tdict.keys())}
	self.plist = ['manno', 'manls'] # [x['page_info.id'] for x in pif.dbh.FetchPages({'format_type' : 'manno'})]
	if pif.FormStr('section', 'all') != 'all':
	    slist = pif.dbh.FetchSections({'id' : pif.FormStr('section')})#, 'page_id' : pif.page_id})
	else:
	    slist = pif.dbh.FetchSections({'page_id' : pif.page_id})
	self.mdict = dict()
	self.sdict = dict()
	self.slist = list()
	for section in slist:
	    if section['section.page_id'] in self.plist and (not self.section or section['id'] == self.section):
		section = pif.dbh.DePref('section', section)
		section.setdefault('model_ids', list())
		self.sdict[section['id']] = section
		self.slist.append(section)
	self.totalvars = self.totalpics = 0
	self.corevars = self.corepics = 0
	self.c2vars = self.c2pics = 0

	for key in pif.FormKeys(start='type_'):
	    val = pif.FormStr(key)
	    t = key[-1]
	    self.types.setdefault(val, list())
	    self.types[val] += t

	self.section = pif.FormStr('section')
	if self.section == 'all':
	    self.section = ''
	self.start = pif.FormInt('start', 1)
	self.end = pif.FormInt('end', 9999)
	self.firstyear = pif.FormInt('syear', 1)
	self.lastyear = pif.FormInt('eyear', 9999)
	if pif.FormStr('range', 'all') == 'all':
	    self.start = self.end = None

	for casting in pif.dbh.FetchCastingList():#(page_id=pif.page_id):
	    self.AddCasting(pif, casting)
	if withaliases:
	    for alias in pif.dbh.FetchAliases(where="section_id != ''"):
		#self.AddCasting(pif, alias)
		self.AddAlias(pif, alias)

    def AddCasting(self, pif, casting):
	manitem = pif.dbh.ModifyManItem(casting)
	if manitem['section_id'] in self.sdict and manitem['id'] not in self.sdict[manitem['section_id']]['model_ids']:
	    self.AddItem(manitem)

    def AddAlias(self, pif, alias):
	manitem = pif.dbh.ModifyManItem(alias)
	if manitem['alias.section_id'] in self.sdict:
	    manitem['id'] = manitem['alias.id']
	    if 'ref_id' in manitem:
		refitem = copy.deepcopy(self.mdict[manitem['ref_id']])
		if manitem['first_year']:
		    refitem['first_year'] = manitem['first_year']
		refitem['id'] = manitem['id']
		refitem['descs'] = manitem['descs']
		refitem['descs'].append('same as ' + manitem['ref_id'])
		manitem = refitem
	    self.AddItem(manitem)

    def AddItem(self, manitem):
	if self.IsItemShown(manitem):
	    manitem['nodesc'] = self.nodesc
	    manitem['type_desc'] = self.Types(manitem['vehicle_type'])
	    self.sdict[manitem['section_id']]['model_ids'].append(manitem['id'])
	    self.mdict[manitem['id']] = manitem

    def Types(self, typespec):
	return  ', '.join(filter(None, [self.tdict.get(t) for t in typespec]))

    def RunThing(self, pif, FunctionShowSection):
	sections = list()
	for sec in self.slist:
	    if sec['model_ids']:
		sec['model_ids'].sort()
		sections.append(FunctionShowSection(pif, sec))
	return sections

    def IsItemShown(self, mod):
	'''Makes decision of whether to show based on vehicle type, # range, and year range.'''
	if self.start and self.end:
	    modno = 0
	    for c in mod['id']:
		if c.isdigit():
		    modno = 10 * modno + int(c)
	    if modno < self.start or modno > self.end:
		return False

	if mod['first_year'] and (self.firstyear > int(mod['first_year']) or self.lastyear < int(mod['first_year'])):
	    return False

	if self.types.get('y') or self.types.get('n'):
	    if useful.AnyCharMatch(self.types['n'], mod['vehicle_type']):
		return False
	    if self.types['y'] and not useful.AnyCharMatch(self.types['y'], mod['vehicle_type']):
		return False
	return True

    # ----- castings --------------------------------------------

    def ShowSectionManno(self, pif, sect):
	sect['anchor'] = sect['id']
	sect['id'] = ''
	sect['range'] = [{'entry' : models.GenerateModelTablePicLink(pif, self.mdict, sect['model_ids'])}]
	return sect

    def RunMannoList(self, pif):
	llineup = dict(columns=4)
	llineup['section'] = self.RunThing(pif, self.ShowSectionManno)
	return pif.render.FormatLineup(llineup) + \
	    pif.render.FormatButtonComment(pif, 'sel=%s&ran=%s&start=%s&end=%s' %
		(pif.FormStr('selection'), pif.FormStr('range'), pif.FormStr('start'), pif.FormStr('end')))

    def Run(self, pif):
	llineup = {'section' : list(), 'columns' : 4}
	llineup['section'] = self.RunThing(pif, self.ShowSectionManno)
	return llineup

    # ----- check list ------------------------------------------

    def ShowSectionList(self, pif, sect):
	cols = 3
	ostr = '<a name="'+sect['id']+'_list"></a>\n'
	ostr += '<tr><td colspan=%d style="text-align: center; font-weight: bold;">%s</td></tr>' % (4 * cols, sect['name'])
	mods = list()
	smods = sect['model_ids']
	mpc = len(smods) / cols
	if len(smods) % cols:
	    mpc += 1
	for col in range(0, cols):
	    mods.append(smods[col * mpc:(col + 1) * mpc])

	while True:
	    ostr += ' <tr>\n'
	    found = False
	    for col in range(0, cols):
		if mods[col]:
		    slist = self.mdict[mods[col].pop(0)]
		    ostr += models.AddModelTableListEntry(pif, slist)
		    found = True
	    ostr += ' </tr>\n'
	    if not found:
		break
	ostr += '<tr>'
	for col in range(0, cols):
	    ostr += '<td colspan=4 width=%d%%>&nbsp;</td>' % (100 / cols)
	ostr += '</tr>'
	return ostr

    def RunChecklist(self, pif):
	ostr = '<table class="smallprint" width=100%>\n'
	ostr += '\n'.join(self.RunThing(pif, self.ShowSectionList))
	ostr += "</table>\n\n"
	return ostr

    # ----- thumbnails ------------------------------------------

    def ShowSectionThumbs(self, pif, sect):
	sect['range'] = list()
	sect['anchor'] = sect['id']
	sect['id'] = ''
	sect['columns'] = 6
	ran = {'entry' : list()}
	for mod_id in sect['model_ids']:
	    mdict = self.mdict[mod_id]
	    mdict['nodesc'] = 1
	    mdict['prefix'] = 't'
	    ran['entry'].append({'text' : models.AddModelTablePicLink(pif, mdict)})
	sect['range'].append(ran)
	return sect

    def RunThumbnails(self, pif):
	llineup = {'section' : list(), 'columns' : 4}
	llineup['section'] = self.RunThing(pif, self.ShowSectionThumbs)
	ostr = pif.render.FormatLineup(llineup)
	ostr += pif.render.FormatButtonComment(pif, 'sel=%s&ran=%s&start=%s&end=%s' %
	    (pif.FormStr('selection', ''), pif.FormStr('range', ''), pif.FormStr('start', ''), pif.FormStr('end', '')))

	return ostr

    # ----- admin list ------------------------------------------

    def ShowListPic(self, pif, prefix, id, txt):
	if glob.glob(prefix[1]+'/'+prefix[0]+id.lower()+'.jpg'):
	    return [prefix[0], pif.render.FormatImageAsLink([prefix[0]+id.lower()], txt.upper(), prefix[1])]
	if glob.glob(prefix[1]+'/'+prefix[0]+id.lower()+'-*.jpg'):
	    return [prefix[0], pif.render.FormatImageAsLink([prefix[0]+id.lower()], txt.upper(), prefix[1])]
	if glob.glob(prefix[1]+'/'+prefix[0]+id.lower()+'.gif'):
	    return [prefix[0], pif.render.FormatImageAsLink([prefix[0]+id.lower()], txt.upper(), prefix[1])]
	if glob.glob(prefix[1]+'/'+prefix[0]+id.lower()+'-*.gif'):
	    return [prefix[0], pif.render.FormatImageAsLink([prefix[0]+id.lower()], txt.upper(), prefix[1])]
	return [prefix[0], '-']

    def ShowListVarPics(self, pif, mod_id):
	vars = pif.dbh.FetchVariations(mod_id)
	cpics = cfound = pics = found = 0
	for var in vars:
	    is_c2 = False
	    if var['variation.var'].startswith('f'):
		continue
	    if not var['variation.picture_id']:
		fn = mod_id + '-' + var['variation.var']
	    elif var['variation.picture_id'] == var['variation.var']:
		fn = mod_id + '-' + var['variation.picture_id']
	    else:
		continue
	    self.totalvars += 1
	    if not var['variation.category']:
		self.corevars += 1
		cpics += 1
	    if var['variation.category'] in mbdata.code2_categories:
		self.c2vars += 1
		is_c2 = True
	    else:
		pics += 1
	    #pif.render.Comment(config.imgdirVar + '/' + fn + '.jpg')
	    if os.path.exists(config.imgdirVar + '/s_' + fn.lower() + '.jpg'):
		if is_c2:
		    self.c2pics += 1
		    continue
		self.totalpics += 1
		found += 1
		if not var['variation.category']:
		    self.corepics += 1
		    cfound += 1
	af = '%d/%d' % (found, pics)
	cf = '%d/%d' % (cfound, cpics)
	if found != pics:
	    af = '<font color="red">%s</font>' % af
	if cfound != cpics:
	    cf = '<font color="red">%s</font>' % cf
	return af + ' ' + cf


    def ShowListVarYears(self, pif, mod_id):
	fy = ly = None
	vars = pif.dbh.FetchVariations(mod_id)
	for var in vars:
	    dt = var['variation.date'].split('/')
	    if len(dt) > 1:
		yr = dt[1].strip()
		if yr.isdigit():
		    yr = int(yr) + 1900
		    if yr < 1953:
			yr += 100
		    if not fy:
			fy = yr
		    if not ly:
			ly = yr
		    fy = min(fy, yr)
		    ly = max(ly, yr)
	return {'fvyear': fy, 'lvyear': ly}

    # ----- admin -----------------------------------------------

    def ShowAdminModelTable(self, pif, mdict):
	mdict.update({x : '-' for x in a_links})
	for lnk in pif.dbh.FetchLinkLines("single." + mdict['id']):
	    mdict[str(lnk['link_line.associated_link'])] = pif.render.FormatLink(lnk['link_line.url'], 'X')
	mdict['name'] = mades[int(mdict['made'])] % mdict
	mdict.update({'img': self.ShowListPic(pif, ['', config.imgdir175], mdict['id'], 's')[1],
	    'fvyear': '', 'lvyear': '',
	    'vid': '<a href="vars.cgi?list=1&mod=%(id)s">%(id)s</a>' % mdict,
	    'nl': '<a href="%(link)s=%(id)s">%(name)s</a>' % mdict})
	mdict.update(dict([self.ShowListPic(pif, x, mdict['id'], x[0][0]) for x in prefixes]))
	mdict.update(self.ShowListVarYears(pif, mdict['id']))
	mdict.setdefault('own', '')
	mdict.setdefault('mydesc', '')
	return admin_fmtb % mdict


    def ShowSectionAdmin(self, pif, sect):
	sect['cols'] = len(admin_cols)
	ostr = '<tr><th colspan=%(cols)d><a name="%(id)s">%(name)s</a></th></tr>\n' % sect
	ostr += admin_fmth % dict(admin_cols) + '\n'
	for mod in sect['model_ids']:
	    ostr += self.ShowAdminModelTable(pif, self.mdict[mod]) + '\n'
	return ostr


    def RunAdminList(self, pif):
	ostr = pif.render.FormatTableStart()
	ostr += '\n'.join(self.RunThing(pif, self.ShowSectionAdmin))
	ostr += pif.render.FormatTableEnd()
	self.totalvars = max(self.totalvars, 1)
	self.corevars = max(self.corevars, 1)
	self.c2vars = max(self.c2vars, 1)
	ostr += 'Pictures found: %d of %d (%d%%)<br>' % (self.totalpics, self.totalvars, (100 * self.totalpics / self.totalvars))
	ostr += 'Core pictures found: %d of %d (%d%%)<br>' % (self.corepics, self.corevars, (100 * self.corepics / self.corevars))
	ostr += 'Code 2 pictures found: %d of %d (%d%%)<br>' % (self.c2pics, self.c2vars, (100 * self.c2pics / self.c2vars))
	return ostr

    # ----- picture -----------------------------------------------

    def ShowPictureModelTable(self, pif, mdict):
	var_pic_keys = ['pic_a', 'pic_c', 'pic_1', 'pic_2', 'pic_f']
	mdict['first_year'] = '<a href="traverse.cgi?g=1&d=%s">%s</a>' % (os.path.join(config.libmandir, mdict['id'].lower()), mdict['first_year'])
	mdict['name'] = mades[int(mdict['made'])] % mdict
	mdict.update({'img': self.ShowListPic(pif, ['', config.imgdir175], mdict['id'], 's')[1],
	    'vid': '<a href="vars.cgi?list=1&mod=%(id)s">%(id)s</a>' % mdict,
	    'nl': '<a href="%(link)s=%(id)s">%(name)s</a>' % mdict})
	mdict.update(dict([self.ShowListPic(pif, x, mdict['id'], x[0][0]) for x in prefixes]))
	icon = self.ShowListPic(pif, [ 'i_', config.imgdir175 + '/icon' ], mdict['id'], 'i')
	mdict['z_'] = icon[1]
	#mdict['varpic'] = self.ShowListVarPics(pif, mdict['id'])
	vp = single.ShowListVarPics(pif, mdict['id'])
	mdict.update({var_pic_keys[x]: vp[x] for x in range(0,5)})
	#[percent_a, percent_c, percent_1, percent_2, percent_f]
	return picture_fmtb % mdict


    def ShowSectionPicture(self, pif, sect):
	sect['cols'] = len(picture_cols)
	ostr = '<tr><th colspan=%(cols)d><a name="%(id)s">%(name)s</a></th></tr>\n' % sect
	ostr += picture_fmth % dict(picture_cols) + '\n'
	for mod in sect['model_ids']:
	    ostr += self.ShowPictureModelTable(pif, self.mdict[mod]) + '\n'
	return ostr


    def RunPictureList(self, pif):
	self.totals = [[0,0]] * 5
	ostr = pif.render.FormatTableStart()
	ostr += '\n'.join(self.RunThing(pif, self.ShowSectionPicture))
	ostr += pif.render.FormatTableEnd()
	ostr += str(self.totals) + '<br>'
	return ostr

    def GetMine(self, dblist, mans):
	dats = dict()
	mine = dict()
	for mdict in dblist:
	    if not mdict:
		pass
	    #elif llist[0] == 'data':
		#dats[llist[1]] = llist[2].split(',')
	    else:
		#mdict = dict(zip(dats[llist[0]], llist[1:]))
		mine[mdict['id']] = mdict

	for man in mans:
	    for mod_id in man['model_ids']:
		mod = self.mdict[mod_id]
		mod.setdefault('own', '')
		mod.setdefault('mydesc', '')
		if mod['id'] in mine:
		    mod['own'] = mine[mod['id']].get('own', '')
		    mod['mydesc'] = mine[mod['id']].get('mydesc', '')
	return mine

    # ----- vehicle types ---------------------------------------

    def ShowVTModelTable(self, pif, mdict):
	img = ['s_' + mdict['id']]
	if mdict.get('picture_id'):
	    img = ['s_' + mdict['picture_id']]
	for s in mdict['descs']:
	    if s.startswith('same as '):
		img.append('s_' + s[8:])
	mdict['name'] = mdict['id'] + '<br>' + mdict['rawname']
	mdict['img'] = pif.render.FormatImageRequired(img, None, made=mdict['made'])
	mdict['sel'] = pif.render.FormatCheckbox('vt_' + mdict['id'], 
		[[x, mbdata.model_types[x]] for x in list(mbdata.model_type_chars[:13])],
		checked=mdict['vehicle_type']) + '<br>'
	mdict['sel'] += pif.render.FormatCheckbox('vt_' + mdict['id'], 
		[[x, mbdata.model_types[x]] for x in list(mbdata.model_type_chars[13:])],
		checked=mdict['vehicle_type']) + '<br>'
	mdict['sel'] += 'make: ' + pif.render.FormatTextInput('vm_' + mdict['id'], 3, 3, value=mdict['make'])
	mdict['sel'] += 'country: ' + pif.render.FormatTextInput('co_' + mdict['id'], 2, 2, value=mdict['country'])
	return vt_fmtb % mdict

    def ShowSectionVehicleType(self, pif, sect):
	sect['cols'] = len(vt_cols)
	ostr = '<tr><th colspan=%(cols)d><a name="%(id)s">%(name)s</a></th></tr>\n' % sect
	ostr += vt_fmth % dict(vt_cols) + '\n'
	for mod in sect['model_ids']:
	    ostr += self.ShowVTModelTable(pif, self.mdict[mod]) + '\n'
	return ostr

    def RunVehicleTypeList(self, pif):
	ostr = '<form method="post">\n'
	ostr += '<input type="hidden" name="vtset" value="1">\n'
	ostr += pif.render.FormatTableStart()
	ostr += '\n'.join(self.RunThing(pif, self.ShowSectionVehicleType))
	ostr += pif.render.FormatTableEnd()
	ostr += pif.render.FormatButtonInput()
	ostr += '</form>\n'
	return ostr

    # ----- csv -------------------------------------------------

    def ShowSectionMan2CSV(self, pif, sect):

	def NumFormat(t):
	    return '"=""%s"""' % t

	def TextFormat(t):
	    if '"' in t or ',' in t:
		t = '"' + t.replace('"', '""') + '"'
	    return t

	ret = list()
	for mod_id in sect['model_ids']:
	    mod = self.mdict[mod_id]
	    ret.append(",".join([mod_id, NumFormat(mod['first_year']), NumFormat(mod['scale']), TextFormat(mod['name']), TextFormat(', '.join(mod['descs']))]))
	return '\r\n'.join(ret) + '\r\n'

    def RunMan2CSV(self, pif):
	out_file = open('pages/man.csv', 'w')
	out_file.write("MAN #,Year,Scale,Name,Notes\r\n")
	secs = self.RunThing(pif, self.ShowSectionMan2CSV)
	out_file.write(''.join(secs))

#---- useful stuff --------------------------

def RenameBaseID(pif, old_mod_id, new_mod_id, force=False):
    rec = pif.dbh.FetchBaseID(new_mod_id)
    if rec:
	if not force:
	    print new_mod_id, "exists"
	    return
    else:
	pif.dbh.RenameBaseID(old_mod_id, new_mod_id)

    # If we're renaming, I'd like to also rename the pictures.
    filename_re = re.compile('(?P<path>.*/)(?P<p>[a-z]_)?(?P<m>[^-.]*)(?P<s>-[^.]*)?(?P<e>\..*)')
    none_blank = {None : ''}
    patts = [
	config.imgdir175 + '/?_%s.*' % old_mod_id,
	config.imgdir175 + '/%s.*' % old_mod_id,
	config.imgdirVar + '/?_%s-*.*' % old_mod_id,
	config.imgdirVar + '/%s-*.*' % old_mod_id,
	config.imgdir175 + '/icon/?_%s-*.*' % old_mod_id,
	config.imgdirAdd + '/?_%s.*' % old_mod_id,
	config.imgdirCat + '/?_%s.*' % old_mod_id,
	config.imgdirCat + '/%s.*' % old_mod_id,
	config.imgdirPack + '/?_%s.*' % old_mod_id,
	config.imgdirPack + '/%s.*' % old_mod_id,
    ]
    pics = reduce(lambda x, y: x + glob.glob(y.lower()), patts, list())
    for pic in pics:
#	pic_m = filename_re.match(pic)
#	if pic_m:
#	    pic_new = ''.join([
#		pic_m.group('path'),
#		none_blank.get(pic_m.group('p'), pic_m.group('p')),
#		pic_m.group('m'),
#		none_blank.get(pic_m.group('s'), pic_m.group('s')),
#		pic_m.group('e'),
#	    ])
#	    print "rename", pic, pic_new, "<br>"
#	    #os.rename(pic, pic_new)
#	else:
#	    print "can't resolve name:", pic
	pic_new = pic.replace(old_mod_id.lower(), new_mod_id.lower())
	print "rename", pic, pic_new, "<br>"
	os.rename(pic, pic_new)


def WriteVehicleTypes(pif):
    for key in pif.FormKeys(start='vt_'):
	val = ''.join(pif.FormList(key))
	print key[3:], 'type', val, '<br>'
	pif.dbh.WriteCasting(values={'vehicle_type' : val}, id=key[3:])
    for key in pif.FormKeys(start='vm_'):
	print key[3:], 'make', pif.FormStr(key), '<br>'
	pif.dbh.WriteCasting(values={'make' : pif.FormStr(key)}, id=key[3:])
    for key in pif.FormKeys(start='co_'):
	print key[3:], 'country', pif.FormStr(key), '<br>'
	pif.dbh.WriteCasting(values={'country' : pif.FormStr(key)}, id=key[3:])

#---- main ----------------------------------

@basics.WebPage
def Main(pif):
    pif.render.hierarchy.append(('/', 'Home'))
    pif.render.hierarchy.append(('/database.php', 'Database'))
    pif.render.hierarchy.append((pif.request_uri, 'Manufacturing Numbers'))
    pif.render.PrintHtml()
    if pif.FormStr('num'):
	print '<meta http-equiv="refresh" content="0;url=single.cgi?id=%s">' % pif.FormStr('num')
	return
    print pif.render.FormatHead()
    models.flago = mflags.FlagList(pif)
    if pif.FormHas('vtset'):
	WriteVehicleTypes(pif)
    elif not pif.FormHas('section'):
	print "Please select a range to display."
    else:
	listtype = pif.FormStr('listtype')
	manf = MannoFile(pif, withaliases=True)
	if listtype == 'adl':
	    print manf.RunAdminList(pif)
	elif listtype == 'pxl':
	    print manf.RunPictureList(pif)
	elif listtype == 'ckl':
	    print manf.RunChecklist(pif)
	elif listtype == 'thm':
	    print manf.RunThumbnails(pif)
	elif listtype == 'vtl':
	    print manf.RunVehicleTypeList(pif)
	else:
	    print manf.RunMannoList(pif)
    print pif.render.FormatTail()

#---- play ----------------------------------

@basics.WebPage
def PlayMain(pif):
    pif.render.PrintHtml()
    print pif.render.FormatHead()
    manf = MannoFile(pif)
    llineup = manf.Run(pif)
    llineup['section'][0]['range'][0]['entry'][0].update({'rowspan':2, 'colspan':2})
    print pif.render.FormatLineup(llineup)
    print pif.render.FormatTail()

#---- compare -------------------------------

def Comparisons(pif, diffs):
    ostr = ''
    imod = 0
    for sec in diffs:

	modsets = {}
	for mod in sec['mods']:
	    if mod['c2.rawname']:
		mod['name'] = mod['c2.rawname'].replace(';', ' ')
		mod['mod_id'] = mod['cc.compare_id']
	    else:
		mod['name'] = mod['c1.rawname'].replace(';', ' ')
		mod['mod_id'] = mod['cc.mod_id']
	    modsets.setdefault(mod['cc.mod_id'], [])
	    modsets[mod['cc.mod_id']].append((mod['mod_id'], mod['name'], mod['cc.description'].split(';')))
	    #print mod,'<br>'
	keys = modsets.keys()
	keys.sort()

	ostr += pif.render.FormatTableStart()
	ostr += pif.render.FormatSection(sec['section.name'], also={'colspan' : 3})
	ostr += pif.render.FormatRowStart()
	ostr += pif.render.FormatCell(0, sec['section.note'], also={'colspan' : 3})
	ostr += pif.render.FormatRowEnd()
	for main_id in keys:
	    modset = modsets[main_id]
	    ostr += pif.render.FormatRowStart(ids=[x[0] for x in modset])
	    ostr += pif.render.FormatCellStart(imod, hdr=True, also={'colspan' : 3})
	    names = list()
	    for id, name, descs in modset:
		#ostr += pif.render.FmtAnchor(id)
		if name not in names:
		    names.append(name)
	    ostr += ", ".join(names)
	    ostr += pif.render.FormatCellEnd(hdr=True)
	    ostr += pif.render.FormatRowEnd()
	    pic = pif.render.FormatImageOptional(main_id, prefix='z_')
	    for id, name, descs in modset:
		desc = pif.render.FormatBulletList(descs)
		ostr += pif.render.FormatRowStart()
		ostr += pif.render.FormatCell(imod, models.AddModelPicLinkShort(pif, id),
				also={'style' : 'text-align: center;'})
		if pic:
		    if desc:
			ostr += pif.render.FormatCell(imod, desc)
		    if id == main_id:
			ostr += pif.render.FormatCell(imod, pif.render.FormatImageOptional(main_id, prefix='z_'),
				    also={'rowspan' : len(modsets[main_id])})
		else:
		    if desc:
			ostr += pif.render.FormatCell(imod, desc, also={'colspan' : 2})
		    else:
			ostr += pif.render.FormatCell(imod, '&nbsp;', also={'colspan' : 2})
		ostr += pif.render.FormatRowEnd()
	    imod = (imod + 1) % 2
	ostr += pif.render.FormatTableEnd()
    return ostr


@basics.WebPage
def CompareMain(pif):
    pif.render.PrintHtml()
    secs = pif.dbh.FetchSections({'page_id' : pif.page_id})
    mods = pif.dbh.FetchCastingCompares()
    for sec in secs:
	sec['mods'] = filter(lambda x: x['cc.section_id'] == sec['section.id'], mods)

    print pif.render.FormatHead()
    print Comparisons(pif, secs)
    print pif.render.FormatButtonComment(pif)
    print pif.render.FormatTail()

#---- ---------------------------------------

@basics.CommandLine
def Commands(pif):
    if pif.argv and pif.argv[0] == 'd':
	print "delete not yet implemented"
	pass # DeleteCasting(pif, pif.argv[1], pif.argv[2])
    elif pif.argv and pif.argv[0] == 'r':
	RenameBaseId(pif, pif.argv[1], pif.argv[2], True)
    elif pif.argv and pif.argv[0] == 'f':
	RunSearch(pif, pif.argv[1:])
    else:
	print "./mannum.py [f|d|r] ..."
	print "  f for find: search-criterion"
	print "  d for delete: mod_id"
	print "  r for rename: old_mod_id new_mod_id"


def SearchName(pif, targ):
    where = map(lambda x: "base_id.rawname like '%%%s%%'" % x, targ)
    return pif.dbh.FetchCastingList(page_id='manno', where=where, verbose=False) + \
	    pif.dbh.FetchCastingList(page_id='manls', where=where, verbose=False)


def RunSearch(pif, args):
    mods = map(pif.dbh.ModifyManItem, SearchName(pif, args))
    mods.sort(key=lambda x:x['id'])
    for mod in mods:
	print '%(id)-8s|%(first_year)4s|%(scale)-5s|%(country)2s|%(name)s' % mod


if __name__ == '__main__': # pragma: no cover
    Commands('vars')
