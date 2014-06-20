#!/usr/local/bin/python

import copy, os, sys
import config
import flags
import images
import mbdata
import models
import useful

width = [600, 600, 300, 200, 150, 100]

'''
| X.01 | Packaging
| X.02 | Catalogs
| X.03 | Advertisements
| X.21 | Major Packs
| X.22 | King Size
| X.23 | Real Working Rigs
| X.24 | Accessory Packs
| X.31 | Models of Yesteryear
| X.41 | Buildings
| X.61 | Presentation Sets
| X.62 | Gift Sets
| X.63 | 5-Packs
| X.64 | Licensed 5-Packs
| X.65 | 10-Packs
| X.71 | Roadways
'''

def VerNo(rank):
    if rank:
	return chr(96 + rank)
    return ' '

#--------- lineup ----------------------------------

def ShowLineupModel(pif, mdict, comments, verbose=0, unroll=0):
    ostr = ''

    pif.render.Comment('ShowLineupModel',mdict)

    if not mdict: # pragma: no cover
	return ostr

    mdict = pif.dbh.DePref('base_id', mdict)

    # want to add a yellow star here if the picture is from another model
    mdict.setdefault('make', '')
    mdict['name'] = str(mdict.get('rawname', '')).replace(';', ' ')
    mdict['iconname'] = pif.dbh.IconName(mdict['rawname'])
    mdict['unlicensed'] = {'unl': '-', '': '?'}.get(mdict.get('casting.make', ''), ' ')
    mdict.setdefault('description', '')
    mdict['descs'] = filter(lambda x:x, str(mdict['description']).split(';'))
    if not mdict['flags']:
	mdict['flags'] = 0
    mdict['made'] = not (mdict['flags'] & pif.dbh.FLAG_MODEL_NOT_MADE)
    mdict['notmade'] = {True: '', False: '*'}[mdict['made']]
    mdict['casting_type'] = mbdata.casting_types.get(mdict.get('model_type', 'SF'), 'Casting')
    mdict['name'] = mdict['lineup_model.name']
    mdict['mod_id'] = mdict['lineup_model.mod_id']
    mdict['ref_id'] = mdict['vs.ref_id']
    # won't work.  still figuring it out.
    if pif.render.verbose:
	print 'ShowLineupModel', mdict['lineup_model.number']
	print mdict.get('rank_id'), mdict.get('sub_id'), mdict.get('vs.rank_id'), mdict.get('vs.sub_id')
    if mdict['vs.sub_id'] and mdict['vs.sub_id'].isdigit():
	mdict['rank_id'] = mdict['vs.sub_id']
	mdict['sub_id'] = ''
	if pif.render.verbose:
	    print 'isdig'
    elif mdict.get('vs.rank_id'):
	mdict['sub_id'] = mdict['vs.rank_id']
	if pif.render.verbose:
	    print 'rank_id'
    else:
	mdict['rank_id'] = 0
	mdict['sub_id'] = mdict['vs.sub_id']
	if pif.render.verbose:
	    print 'normal'
    if pif.render.verbose:
	print '<hr>'
    mdict['href'] = ""
    mdict['product'] = ''
    mdict['no_variation'] = mdict['is_product_picture'] = 0

    mdict['cvarlist'] = []
    mdict.setdefault('vars', [])
    mdict['vars'].sort()
    for var in mdict['vars']:
	if var[0]:
	    found = False
	    for cvar in mdict['cvarlist']:
		if var[1] == cvar[1]:
		    if var[2] and var[2] not in cvar[0]:
			cvar[0].append(var[2])
		    if var[0] not in cvar[0]:
			cvar[0].append(var[0])
		    found = True
		    break
	    if not found:
		mdict['cvarlist'].append([[var[0]], var[1]])
		if var[2]:
		    mdict['cvarlist'][-1][0].append(var[2])

    if mdict['casting.id']:
	# modify this if rank_id exists
	if mdict['lineup_model.picture_id']:
	    mdict['product'] = mdict['lineup_model.picture_id']
	    mdict['is_reused_product_picture'] = 1
	elif mdict.get('image_format'):
	    mdict['product'] = mdict['image_format'] % mdict['lineup_model.number']
	if pif.render.FindImageFile([mdict['product']], suffix='jpg', pdir=mdict['pdir']):
	    mdict['is_product_picture'] = 1
	    comments.add('c')
	mdict['href'] = "single.cgi?dir=%(pdir)s&pic=%(product)s&ref=%(ref_id)s&sub=%(sub_id)s&id=%(mod_id)s" % mdict
    elif mdict['pack.id']:
	if mdict['lineup_model.picture_id']:
	    mdict['product'] = mdict['lineup_model.picture_id']
	    mdict['is_reused_product_picture'] = 1
	elif mdict.get('image_format'):
	    mdict['product'] = mdict['image_format'] % mdict['pack.id']
	if pif.render.FormatImageSized([mdict['product']], pdir=mdict['pdir'], largest='g'):
	    mdict['is_product_picture'] = 1
	    comments.add('c')
	mdict['href'] = "packs.cgi?page=%(pack.page_id)s&id=%(pack.id)s" % mdict
    elif mdict['publication.id']:
	mdict['product'] = mdict['publication.id'] + '_01'
	if pif.render.FormatImageSized([mdict['product']], pdir=mdict['pdir'], largest='g'):
	    mdict['is_product_picture'] = 1
	    comments.add('c')
	mdict['href'] = "pub.cgi?id=%(publication.id)s" % mdict

    if pif.form.get('large'):
	ostr += '<table><tr><td width=400>'
	#def FormatLink(self, url, txt, args={}, nstyle=None, also={}):
	img = pif.render.FormatImageRequired(mdict['product'], suffix='jpg', pdir=mdict['pdir'], also={'class':'largepic'})
	ostr += pif.render.FormatLink('upload.cgi?d=%s&r=%s' % (mdict['pdir'], mdict['product']), img)
	ostr += '</td><td><center>'
    if unroll and mdict.get('casting.id') and mdict['cvarlist']:
	for desc in mdict['cvarlist']:
	    ostr += ShowLineupModelVar(pif, mdict, comments, show_var=desc[0][0], verbose=verbose)
    else:
	ostr += ShowLineupModelVar(pif, mdict, comments, verbose=verbose)
    if pif.form.get('large'):
	ostr += '</center></td></tr></table>'
    return ostr


def ShowLineupModelVar(pif, mdict, comments, show_var=None, verbose=0):
    ostr = ''

    imglist = []
    mdict['varlist'] = []
    if mdict.get('lineup_model.flags', 0) & pif.dbh.FLAG_MODEL_NOT_MADE:
	mdict['not_made'] = True
	imglist.append(mdict['lineup_model.mod_id'])
	comments.add('n')
    elif mdict.get('lineup_model.mod_id'):
	imglist.append(mdict['lineup_model.mod_id'])
	if show_var:
	    for var in mdict['cvarlist']:
		if show_var in var[0]:
		    mdict['varlist'].extend(var[0])
	else:
	    for var in mdict['vars']:
		if var[2]:
		    mdict['varlist'].append(var[2])
		elif var[0]:
		    mdict['varlist'].append(var[0])
    pif.render.Comment('varlist', mdict['varlist'])
    mdict['imgstr'] = pif.render.FormatImageRequired(imglist, prefix='s_', vars=mdict['varlist'], pdir=config.imgdir175)

    if show_var:
	mdict['descriptions'] = map(lambda x: x[1], filter(lambda x: show_var in x[0], mdict['cvarlist']))
    else:
	mdict['descriptions'] = map(lambda x: x[1], mdict['vars'])

    mdict['no_specific_image'] = 0
    if mdict['casting.id'] and not mdict.get('not_made'):
	if mdict['imgstr'].find('-') < 0:
	    comments.add('i')
	    mdict['no_specific_image'] = 1
	if len(mdict['varlist']) < 1: # pragma: no cover
	    comments.add('v')
	    mdict['no_variation'] = 1
	# also if there is no description string

    #mdict: imgstr name number pdir product vars
    ostr += models.AddModelTableProductLink(pif, mdict)
    return ostr


def SetVars(llineup, mods, regions, ref_id, verbose=0):
    done = False
    for cregion in regions:
	if verbose: # pragma: no cover
	    pass#print '<p><b>SetVars cregion', cregion, ref_id, '</b><br>'
	for mod in mods:
	    mod['number'] = mod['lineup_model.number']
	    SetVar(mod, llineup, cregion, ref_id, verbose=verbose)
#	    if mod['number'] in llineup:
#		done = True
	if done:
	    break
    if verbose: # pragma: no cover
	print '<hr>'


def SetVar(mod, llineup, region, ref_id, verbose=0):
    sub_id = region
    rank_id = 0
    if region == 'W':
	sub_id = ''
    if verbose: # pragma: no cover
	pass#print '<hr width=90%> SetVar #', mod['number'], 'reg', region, 'ref', ref_id, 'sub', sub_id, 'done', mod['number'] in llineup, 'modreg', mod['lineup_model.region']
	#print 'VS', mod.get('vs.ref_id'), ':', mod.get('vs.rank_id', 'unset'), '/', mod.get('vs.sub_id', 'unset'), '<br>'
	#print mod, '<br>'
    num = mod['number']
    lmod = llineup.get(num)
    mod.setdefault('vs.rank_id', '')
    if lmod and lmod['lineup_model.mod_id'] != mod['lineup_model.mod_id']: # already done?
	if verbose: # pragma: no cover
	    print "skipdiff<br>"
    elif not mod['vs.sub_id']:
	mod['vs.sub_id'] = ''
    elif mod['vs.sub_id'].isdigit():
	mod['vs.rank_id'] = mod['vs.sub_id']
	mod['vs.sub_id'] = ''
	if verbose: # pragma: no cover
	    print "rank-limited", '<br>'
    if mod['vs.sub_id'] != sub_id:
	if verbose: # pragma: no cover
	    print "skip0", '<br>'
    elif not num in llineup:
	mod = copy.deepcopy(mod)
	mod['vars'] = [(mod['v.var'], mod['v.text_description'], mod['v.picture_id'])]
	llineup[num] = mod
	if verbose: # pragma: no cover
	    print "new", '<br>'
    elif not lmod['vs.ref_id'] or \
		(lmod['vs.ref_id'] == ref_id): # and (lmod['vs.sub_id'] == sub_id or not lmod['vs.sub_id'])):
	lmod['vars'].append((mod['v.var'], mod['v.text_description'], mod['v.picture_id']))
	#lmod['vs.ref_id'] = mod['vs.ref_id']
	#lmod['vs.sub_id'] = mod['vs.sub_id']
	if verbose: # pragma: no cover
	    print "add", '<br>'
    elif mod['lineup_model.region'] == region:
	mod = copy.deepcopy(mod)
	mod['vars'] = [(mod['v.var'], mod['v.text_description'], mod['v.picture_id'])]
	llineup[num] = mod
	if verbose: # pragma: no cover
	    print "repl", '<br>'
    else:
	pass
	if verbose: # pragma: no cover
	    print "skip1", '<br>'


def CreateLineup(mods, parents, year, region, verbose=0):
    if verbose: # pragma: no cover
	pass#print 'CreateLineup', len(mods), parents, year, region, '<br>'
#    if region == 'X':
#	return dict(map(lambda x: (x['lineup_model.number'], x), mods))

    rankmods = dict()
    reg_list = []
    cregion = region
    while cregion:
	reg_list.append(cregion)

	for mod in mods:
	    if cregion == mod['lineup_model.region']:
		if verbose: # pragma: no cover
		    pass#print 'CreateLinup', mod['lineup_model.number'], 'sub', mod['vs.sub_id'], '<br>'
		    #print mod
		mod['number'] = mod['lineup_model.number']
		rankmods.setdefault(mod['number'], [])
		if rankmods[mod['number']] and mod['lineup_model.mod_id'] != rankmods[mod['number']][0]['lineup_model.mod_id']:
		    if verbose: # pragma: no cover
			print 'dumped'
		elif not mod['vs.sub_id'] or not mod['vs.sub_id'].isdigit() or mod['number'] == int(mod['vs.sub_id']):
		    rankmods[mod['number']].append(mod)
		    if verbose: # pragma: no cover
			print 'kept'
		elif verbose: # pragma: no cover
		    print 'dropped'
		if verbose: # pragma: no cover
		    print '<hr>'

	cregion = parents.get(cregion)

    ref_id = 'year.%s' % year
    llineup = dict()

    for rank in rankmods:
	SetVars(llineup, rankmods[rank], reg_list, ref_id, verbose=verbose)

    return llineup


def GetManSections(pif, year, region):
    while 1:
	wheres = ["page_id='year.%s'" % year]
	if region:
	    wheres.append("id like '%s%%'" % region)
	wheres.append("not id like 'X%'")
	if not pif.render.isbeta:
	    wheres.append("not flags & %d" % pif.dbh.FLAG_SECTION_HIDDEN)
	secs = pif.dbh.DePref('section', pif.dbh.FetchSections(wheres))
	if secs:
	    break
	if not region in mbdata.regionparents:
	    return '', dict(), []
	region = mbdata.regionparents[region]
    return region, secs[0], secs[1:]


def GetExtraSections(pif, year):
    where = ["page_id='year.%s'" % year, "id like 'X%'"]
    if not (pif.render.isbeta or pif.form.get('hidden')):
	where.append(' and not flags & %d' % pif.dbh.FLAG_SECTION_HIDDEN)
    return pif.dbh.DePref('section', pif.dbh.FetchSections(where))


def GetLineupModels(pif, year, region):
    line_regions = mbdata.GetRegionTree(region)
    lmodlist = pif.dbh.FetchLineupModels(str(year), line_regions)
    lmodlist.sort(key=lambda x: x['lineup_model.number'])
    for mod in lmodlist:
	pif.render.Comment('GetLineupModels:', mod)
    #print 'GetLineupModels', len(lmodlist), '<br>'
    return lmodlist


def GenerateManLineup(pif, year, region):
    pif.render.Comment('lineup.GenerateManLineup', year, region)

    if region:
	moddict = CreateLineup(GetLineupModels(pif, year, region),
			mbdata.regionparents, year, region, verbose=pif.render.verbose)

	keylist = moddict.keys()
	keylist.sort()
	#print 'keylist', keylist,'<br>'
	for key in keylist:
	    #print 'mod', moddict[key], '<br>'
	    moddict[key]['lineup_model.picture_id'] = moddict[key]['lineup_model.picture_id'].replace('W', region)
	    yield moddict[key]


def CreateExtraLineup(pif, year, secs, verbose=0): # currently unimplemented # pragma: no cover
    line_regions = map(lambda x: x['id'], secs)
    lmods = pif.dbh.FetchLineupModels(str(year), line_regions)
    if verbose: # pragma: no cover
	print 'CreateExtraLineup', year, len(lmods), '<br>'

    ref_id = 'year.%s' % year
    for sec in secs:
	if verbose: # pragma: no cover
	    print '<p>sec', sec, '<br>'
	rankmods = dict()
	for mod in lmods:
	    if mod['lineup_model.region'] == sec['id']:
		mod['number'] = mod['lineup_model.number']
		rankmods.setdefault(mod['number'], [])
		rankmods[mod['number']].append(mod)
		if verbose: # pragma: no cover
		    print 'mod', mod['lineup_model.mod_id'], '<br>'

	moddict = dict()
	for rank in rankmods:
	    SetVars(moddict, rankmods[rank], [sec['id'], 'W'], ref_id, verbose=verbose)

	sec['mods'] = []
	keylist = moddict.keys()
	keylist.sort()
	#print 'keylist', keylist,'<br>'
	for key in keylist:
	    #print 'mod', moddict[key], '<br>'
	    sec['mods'].append(moddict[key])


def CorrectRegion(region, year):
    if type(year) == str:
	year = int(''.join(filter(lambda x: x.isdigit(), year)))
    if year < 1982:
	region = 'W'
    elif region == 'D':
	if not year in (1999,2000,2001):
	    region = 'R'
    elif region == 'B':
	if not year in (2000,2001):
	    region = 'R'
    elif region == 'A':
	if year >= 2002: # ???
	    region = 'U'
	if not year in (2000,2001):
	    region = 'R'
    elif region == 'L':
	if year < 2008 or year > 2011:
	    region = 'R'
    return region, year


def ShowSection(pif, lsec, lran, mods, lup_region, year, comments):
    pif.render.Comment("ShowSection: range", lran)
    multivars = list()
    unroll = int(pif.form.get('unroll', 0))
    if lran['flags'] & pif.dbh.FLAG_SECTION_HIDDEN:
	lran['name'] = '<i>' + lran['name'] + '</i>'
    for mdict in mods:
	mdict['disp_format'] = lran.get('disp_format', '')
	if lran['flags'] & pif.dbh.FLAG_SECTION_DEFAULT_IDS:
	    mdict['shown_id'] = pif.dbh.DefaultID(mdict['lineup_model.mod_id'])
	    mdict['disp_format'] = '%s.'
	else:
	    mdict['shown_id'] = mdict['lineup_model.number']
	mdict['image_format'] = lran['img_format']
	pdir = pif.render.pic_dir
	if lran.get('pic_dir'):
	    pdir = lran['pic_dir']
	mdict['pdir'] = pdir
	if lup_region == 'X':
	    mdict['anchor'] = 'X%d' % mdict['number']
	else:
	    mdict['anchor'] = '%d' % mdict['number']
	pif.render.Comment('mdict2', mdict)
	ent = {
	    'text' : ShowLineupModel(pif, mdict, comments, unroll=unroll), 
	    'display_id' : mdict.get('lineup_model.style_id', 0),
	    'st_suff' : '', 'style' : ''
	}
	if len(mdict['cvarlist']) > 1:
	    multivars.append(str(mdict['number']))
	if not (lran['flags'] & pif.dbh.FLAG_SECTION_NO_FIRSTS) and year == mdict['first_year']:
	    ent['class'] = 'newcasting'
	lran['entry'].append(ent)
    lran['multivars'] = multivars
    lsec['range'].append(lran)


def RunFile(pif, region, year):
    pif.render.Comment('lineup.RunFile', region, year)
    lup_region, year = CorrectRegion(region, year)
    llineup = {'id' : lup_region, 'section' : [], 'name' : '', 'tail' : []}

    lup_region, lsec, secs = GetManSections(pif, year, region)
    if not lup_region:
	return llineup

    modlist = list(GenerateManLineup(pif, year, lup_region))
    if not modlist:
	return llineup

    endv = len(modlist)
    for sec in reversed(secs):
	sec['end'] = endv
	endv = sec['start']

    img = pif.render.FormatImageOptional(['%ss' % year])
    if img[0] == '<':
	lsec['name'] += '<br>' + img
    lsec['id'] = lup_region
    lsec['range'] = []
    hdr = lsec['name']

    if pif.form.get('large'):
	lsec['columns'] = 1

    comments = set()
    multivars = list()

    if secs:
	for lran in secs:
	    lran.update({
		'id' : lup_region + '_' + str(lran['display_order']),
		'entry' : [],
		'graphics' : [lran['img_format'][:4] + lup_region + 's%02d' % lran['display_order']]
	    })
	    ShowSection(pif, lsec, lran, modlist[lran['start']:lran['end']], lup_region, year, comments)
	    multivars.extend(lran['multivars'])
    else:
	lran = copy.deepcopy(lsec)
	lran.update({'id' : lup_region + '_1', 'name' : '', 'entry' : [], 'note' : '', 'graphics' : []})
	ShowSection(pif, lsec, lran, modlist, lup_region, year, comments)
	multivars.extend(lran['multivars'])

    #==================================

    secs = GetExtraSections(pif, year)
    CreateExtraLineup(pif, year, secs, verbose=pif.render.verbose)

    for lran in secs:
	lran['anchor'] = 'S' + lran['id'].replace('.', '')
	lran.update({
	    'id' : 'X_' + str(lran['display_order']),
	    'entry' : [],
	    'graphics' : [lran['img_format'][:2] + lup_region + 's%02d' % lran['display_order']]
	})
	ShowSection(pif, lsec, lran, lran['mods'], 'X', year, comments)

    llineup['section'].append(lsec)
    llineup['tail'] = [pif.render.FormatImageArt('bamca_sm', also={'class' : 'centered'}), '']
    llineup['tail'][1] += pif.render.FormatButtonComment(pif, 'yr=%s&rg=%s' % (pif.form.get('year'), pif.form.get('region')))
    for comment in comments:
	llineup['tail'][1] += mbdata.comment_designation[comment] + '<br>'
#    if int(year) > config.yearstart:
#	llineup['tail'][1] += pif.render.FormatButton("previous_year", link='http://www.bamca.org/cgi-bin/lineup.cgi?year=%s&region=%s' % (int(year) - 1, region))
#    if int(year) > config.yearend:
#	llineup['tail'][1] += pif.render.FormatButton("following_year", link='http://www.bamca.org/cgi-bin/lineup.cgi?year=%s&region=%s' % (int(year) + 1, region))
    if pif.IsAllowed('a'): # pragma: no cover
	llineup['tail'][1] += 'multivars %s %s ' % (year, region) + ' '.join(multivars) + '<br>'
    return llineup


def RunMultiFile(pif, year, region, nyears):
    pif.render.Comment('lineup.RunMultiFile', region, year, nyears)
    pages = pif.dbh.FetchPages('id in (' + ','.join(map(lambda x: "'year.%d'" % x, range(int(year), int(year) + nyears))) + ')')

    modlistlist = []
    max_mods = 0
    y = int(year)
    nyears = len(pages)
    for page in pages:
	page['year'] = str(y)
	reg, lsec, secs = GetManSections(pif, str(y), region)
	page['region'] = reg
	page['sec'] = lsec
	page['img_format'] = lsec['img_format']
	page['mods'] = list(GenerateManLineup(pif, str(y), region))
	max_mods = max(max_mods, len(page['mods']))
	#print 'page', y, region, max_mods, '<br>'
	y += 1

    llineup = {'id' : pif.page_id, 'section' : [], 'name' : '', 'tail':''}
    lsec = pages[0]['sec']
    lsec['columns'] = nyears
    lsec['id'] = 'lineup'
    lsec['range'] = []
    hdr = lsec['name']

    #keylist = list(set(reduce(lambda x,y: x + y.keys(), modlistlist, [])))
    #keylist.sort()
    comments = set()

    lran = {'id' : 'range', 'name' : '', 'entry' : [], 'note' : '', 'graphics' : []}
    pif.render.Comment("RunFile: range", lran)
    for inum in range(0, max_mods):
	#print 'mod num', inum, '<br>'
	for iyr in range(0, nyears):
	    #print 'year', iyr, '<br>'
	    pdir = pages[iyr]['page_info.pic_dir']
	    ent = {'text' : '', 'display_id' : '', 'style' : ''}
	    if pages[iyr]['mods']:
		mdict = pages[iyr]['mods'].pop(0)
		mdict['disp_format'] = lsec.get('disp_format', '')
		mdict['shown_id'] = mdict['lineup_model.number']
		mdict['image_format'] = pages[iyr]['img_format']
		mdict['pdir'] = pdir
		mdict['anchor'] = '%d' % mdict['number']
		ent['text'] = ShowLineupModel(pif, mdict, comments)
		ent['display_id'] = mdict.get('lineup_model.style_id', 0)
		if int(year) + iyr == int(mdict['first_year']):
		    ent['class'] = 'newcasting'
	    #print ent, '<br>'
	    lran['entry'].append(ent)
    lsec['range'].append(lran)

    llineup['section'].append(lsec)
    llineup['tail'] += pif.render.FormatButtonComment(pif, 'yr=%s&rg=%s' % (pif.form.get('year'), pif.form.get('region')))
    for comment in comments:
	llineup['tail'] += mbdata.comment_designation[comment] + '<br>'
    #llineup['tail'] += pif.render.FormatButton("comment_on_this_page", link='../pages/comment.php?page=%s&yr=%s&rg=%s' % (pif.page_id, pif.form.get('year'), pif.form.get('region')), also={'class' : 'comment'}, lalso=dict())
    return llineup


'''
# a lineup consists of a header (outside of the table) plus a set of sections, each in its own table.
#     id, name, section
# a section consists of a header (inside the table) plus a set of ranges.
#     id, name, anchor, columns, note, range
# a range consists of a header plus a set of entries.
#     id, name, anchor, note, entry
'''

def SelectLineup(pif, region, year):
    pif.Dump(True)
    regs = 'URDBAL'
    checked = {True : ' CHECKED', False : ''}
    ostr = '<form>\n'
    #ostr = '<input type="hidden" name="verbose" value="1">\n'
    ostr += pif.render.FormatTableStart()
    irow = 0
    ostr += pif.render.FormatRowStart()
    ostr += pif.render.FormatCellStart()
    years = pif.dbh.FetchLineupYears()
    for yr in years:
	y = int(yr['year'])
	ostr += '<input type="radio" name="year" value="%d"%s>%d<br>\n' % (y, checked[int(year) == y], y)
	irow += 1
	if irow == 15:
	    irow = 0
	    ostr += pif.render.FormatCellEnd()
	    ostr += pif.render.FormatCellStart()
    ostr += pif.render.FormatCellEnd()
    ostr += pif.render.FormatCellStart()
    for reg in regs:
	ostr += '<input type="radio" name="region" value="%s"%s>%s<br>\n' % (reg, checked[reg == region], mbdata.regions[reg])
    ostr += '<p>' + pif.render.FormatButtonInput()
    ostr += pif.render.FormatCellEnd()
    ostr += pif.render.FormatRowEnd()
    ostr += pif.render.FormatTableEnd()
    ostr += '</form>'
    return ostr


def CountLineupModel(pif, mdict):
    ostr = ''

    if mdict:
	mdict = pif.dbh.DePref('base_id', mdict)

	if mdict['casting.id']:
	    mdict['product'] = ''
	    if mdict['lineup_model.picture_id']:
		mdict['product'] = mdict['lineup_model.picture_id']
	    elif mdict.get('image_format'):
		mdict['product'] = mdict['image_format'] % mdict['lineup_model.number']
	    #pif.render.verbose = 0
	    if pif.render.FindImageFile([mdict['product']], suffix='jpg', pdir=mdict['pdir']):
		#pif.render.verbose = 0
		return 1
	    #pif.render.verbose = 0
    return 0


def CountSection(pif, lsec, lran, mods, region, year):
    im_count = pr_count = 0
    for mdict in mods:
	mdict['image_format'] = lran['img_format']
	pdir = pif.render.pic_dir
	if lran.get('pic_dir'):
	    pdir = lran['pic_dir']
	mdict['pdir'] = pdir
	pr_count += 1
	im_count += CountLineupModel(pif, mdict)
    return pr_count, im_count


def PictureCount(pif, region, year):
    pr_count = im_count = 0
    region, year = CorrectRegion(region, year)
    llineup = {'id' : region, 'section' : [], 'name' : '', 'tail' : []}

    region, lsec, secs = GetManSections(pif, year, region)
    if not region:
	return 0

    modlist = list(GenerateManLineup(pif, year, region))

    endv = len(modlist)
    for sec in reversed(secs):
	sec['end'] = endv
	endv = sec['start']

    lsec['id'] = region
    lsec['range'] = []

    if secs:
	for lran in secs:
	    lran.update({
		'id' : region + '_' + str(lran['display_order']),
		'entry' : [],
		'graphics' : [lran['img_format'][:2] + region + 's%02d' % lran['display_order']]
	    })
	    count = CountSection(pif, lsec, lran, modlist[lran['start']:lran['end']], region, year)
	    pr_count += count[0]
	    im_count += count[1]
    else:
	lran = copy.deepcopy(lsec)
	lran.update({'id' : region + '_1', 'name' : '', 'entry' : [], 'note' : '', 'graphics' : []})
	count = CountSection(pif, lsec, lran, modlist, region, year)
	pr_count += count[0]
	im_count += count[1]

    #==================================

    secs = GetExtraSections(pif, year)
    CreateExtraLineup(pif, year, secs, verbose=pif.render.verbose)

    for lran in secs:
	lran.update({
	    'id' : 'X_' + str(lran['display_order']),
	    'entry' : [],
	    'graphics' : [lran['img_format'][:2] + region + 's%02d' % lran['display_order']]
	})
	count = CountSection(pif, lsec, lran, lran['mods'], 'X', year)
	pr_count += count[0]
	im_count += count[1]
    return pr_count, im_count


def ProductPicLineupMain(pif):
    pif.render.title = str(pif.form.get('region', 'Matchbox')) + ' Lineup'
    print pif.render.FormatHead()
    llineup = RunProductPictures(pif, pif.form['region'].upper())
    print pif.render.FormatLineup(llineup)


def RankLineupMain(pif):
    pif.render.hierarchy.append(('/', 'Home'))
    pif.render.hierarchy.append(('/database.php', 'Database'))
    pif.render.hierarchy.append(('/cgi-bin/lineup.cgi', 'Annual Lineup'))
    pif.render.hierarchy.append(('/cgi-bin/lineup.cgi?n=1&num=%s&region=%s&syear=%s&eyear=%s' % (pif.form.get('num'), pif.form.get('region'), pif.form.get('syear'), pif.form.get('eyear')),
	"%s #%d" % (mbdata.regions.get(pif.form.get('region'), ''), pif.FormInt('num'))))
    pif.render.title = str(pif.form.get('year', 'Matchbox')) + ' Lineup'
    print pif.render.FormatHead()
    llineup = RunRanks(pif, pif.form.get('num'), pif.form.get('region', 'U').upper(), pif.form.get('syear', '1953'), pif.form.get('eyear', '2014'))
    print pif.render.FormatLineup(llineup)


def MultiYearsMain(pif):
    pif.render.hierarchy.append(('/', 'Home'))
    pif.render.hierarchy.append(('/database.php', 'Database'))
    pif.render.hierarchy.append(('/cgi-bin/lineup.cgi', 'Annual Lineup'))
    pif.render.hierarchy.append(('/cgi-bin/lineup.cgi?year=%s&region=%s' % (pif.form.get('year'), pif.form.get('region')),
	pif.form.get('year', '') + ' ' + mbdata.regions.get(pif.form.get('region'), '')))
    pif.render.title = str(pif.form.get('year', 'Matchbox')) + ' Lineup'
    print pif.render.FormatHead()
    llineup = RunMultiFile(pif, pif.form['year'], pif.form['region'].upper(), int(pif.form['nyears']))
    print pif.render.FormatLineup(llineup)


def LineupMain(pif):
    pif.render.hierarchy.append(('/', 'Home'))
    pif.render.hierarchy.append(('/database.php', 'Database'))
    pif.render.hierarchy.append(('/cgi-bin/lineup.cgi', 'Annual Lineup'))
    pif.render.hierarchy.append(('/cgi-bin/lineup.cgi?year=%s&region=%s' % (pif.form.get('year'), pif.form.get('region')),
	pif.form.get('year', '') + ' ' + mbdata.regions.get(pif.form.get('region'), '')))
    pif.render.title = str(pif.form.get('year', 'Matchbox')) + ' Lineup'
    print pif.render.FormatHead()
    llineup = RunFile(pif, pif.form['region'].upper(), pif.form['year'])
    print pif.render.FormatLineup(llineup)


def Main(pif):
    pif.render.PrintHtml()

    if 'prodpic' in pif.form:
	ProductPicLineupMain(pif)
    elif pif.FormInt('n'):
	RankLineupMain(pif)
    elif pif.FormInt('nyears', 1) > 1:
	MultiYearsMain(pif)
    elif pif.form.get('region') and pif.form.get('year'):
	LineupMain(pif)
    else:
	print SelectLineup(pif, pif.form.get('region', 'W').upper(), pif.form.get('year', '0'))
	pif.render.title = str(pif.form.get('year', 'Matchbox')) + ' Lineup'
	print pif.render.FormatHead()
    print pif.render.FormatTail()

#--------- text lineup -----------------------------

def TextMain(pif, year, region):
    return RunTextFile(pif, region.upper(), year)


def ShowTextLineupModel(pif, mdict, verbose=0):
    ostr = ''

    if mdict:
	mdict = pif.dbh.DePref('base_id', mdict)
	mdict.setdefault('make', '')

	mdict['name'] = str(mdict.get('rawname', '')).replace(';', ' ')
	mdict['iconname'] = pif.dbh.IconName(mdict['rawname'])
	mdict['unlicensed'] = {'unl': '-', '': '?'}.get(mdict.get('casting.make', ''), ' ')
	mdict.setdefault('description', '')
	mdict['descs'] = filter(lambda x:x, str(mdict['description']).split(';'))
	if not mdict['flags']:
	    mdict['flags'] = 0
	mdict['made'] = not (mdict['flags'] & pif.dbh.FLAG_MODEL_NOT_MADE)
	mdict['notmade'] = {True: '', False: '*'}[mdict['made']]
	#mdict['link'] = linkurl[linky]
	#mdict['linkid'] = mdict.get('mod_id', mdict.get('id'))
	mdict['casting_type'] = mbdata.casting_types.get(mdict.get('model_type', 'SF'), 'Casting')

	imglist = []
	mdict['varlist'] = []
	if mdict.get('lineup_model.mod_id'):
	    imglist.append(mdict['lineup_model.mod_id'])
	    for var in mdict.get('vars', []):
		if var[2]:
		    mdict['varlist'].append(var[2])
		elif var[0]:
		    mdict['varlist'].append(var[0])
	pif.render.Comment('varlist', mdict['varlist'])
	mdict['imgstr'] = pif.render.FormatImageRequired(imglist, prefix='s_', vars=mdict['varlist'], pdir=config.imgdir175)
	mdict['product'] = ''

	mdict['name'] = mdict['lineup_model.name']
	mdict['mod_id'] = mdict['lineup_model.mod_id']
	mdict['ref_id'] = mdict['vs.ref_id']
	mdict['sub_id'] = mdict['vs.sub_id']
	mdict['descriptions'] = map(lambda x: x[1], mdict['vars'])
	mdict['href'] = ""
	if mdict['casting.id']:
	    if mdict['lineup_model.picture_id']:
		mdict['product'] = mdict['lineup_model.picture_id']
	    elif mdict.get('image_format'):
		mdict['product'] = mdict['image_format'] % mdict['lineup_model.number']
	    if pif.render.FindImageFile([mdict['product']], suffix='jpg', pdir=mdict['pdir']):
		mdict['is_product_picture'] = 1
	    mdict['href'] = "single.cgi?dir=%(pdir)s&pic=%(product)s&ref=%(ref_id)s&sub=%(sub_id)s&id=%(mod_id)s" % mdict
	    if mdict['imgstr'].find('-') < 0:
		mdict['no_specific_image'] = 1
	    if len(mdict['varlist']) < 1:
		mdict['no_variation'] = 1
	elif mdict['pack.id']:
	    if mdict['lineup_model.picture_id']:
		mdict['product'] = mdict['lineup_model.picture_id']
	    elif mdict.get('image_format'):
		mdict['product'] = mdict['image_format'] % mdict['pack.id']
	    if pif.render.FormatImageSized([mdict['product']], pdir=mdict['pdir'], largest='g'):
		mdict['is_product_picture'] = 1
	    mdict['href'] = "packs.cgi?page=%(pack.page_id)s&id=%(pack.id)s" % mdict
	elif mdict['publication.id']:
	    mdict['product'] = mdict['publication.id'] + '_01'
	    if pif.render.FormatImageSized([mdict['product']], pdir=mdict['pdir'], largest='g'):
		mdict['is_product_picture'] = 1
	    mdict['href'] = "pub.cgi?id=%(publication.id)s" % mdict
	#mdict: imgstr name number pdir product vars
	ostr = models.AddModelTextLine(pif, mdict)
    return ostr


def ShowTextSection(pif, lsec, lran, mods, lup_region, year):
    ostr = ''
    for mdict in mods:
	mdict['disp_format'] = lran.get('disp_format', '')
	if lran['flags'] & pif.dbh.FLAG_SECTION_DEFAULT_IDS:
	    mdict['shown_id'] = pif.dbh.DefaultID(mdict['lineup_model.mod_id'])
	    mdict['disp_format'] = '%s.'
	else:
	    mdict['shown_id'] = mdict['lineup_model.number']
	mdict['image_format'] = lran['img_format']
	pdir = pif.render.pic_dir
	if lran.get('pic_dir'):
	    pdir = lran['pic_dir']
	mdict['pdir'] = pdir
	if lup_region == 'X':
	    mdict['anchor'] = 'X%d' % mdict['number']
	else:
	    mdict['anchor'] = '%d' % mdict['number']
	ent = {
	    'text' : ShowTextLineupModel(pif, mdict), 
	    'display_id' : mdict.get('lineup_model.style_id', 0),
	    'st_suff' : '', 'style' : ''
	}
	ostr += ent['text']
	if not (lran['flags'] & pif.dbh.FLAG_SECTION_NO_FIRSTS) and year == mdict['first_year']:
	    ent['class'] = 'newcasting'
	lran['entry'].append(ent)
    lsec['range'].append(lran)
    return ostr


def RunTextFile(pif, region, year):
    ostr = ''
    lup_region, year = CorrectRegion(region, year)
    llineup = {'id' : lup_region, 'section' : [], 'name' : '', 'tail' : []}

    lup_region, lsec, secs = GetManSections(pif, year, region)
    if not lup_region:
	return ostr

    modlist = list(GenerateManLineup(pif, year, lup_region))

    endv = len(modlist)
    for sec in reversed(secs):
	sec['end'] = endv
	endv = sec['start']

    lsec['id'] = lup_region
    lsec['range'] = []
    hdr = lsec['name']

    if secs:
	for lran in secs:
	    lran.update({
		'id' : lup_region + '_' + str(lran['display_order']),
		'entry' : [],
		'graphics' : [lran['img_format'][:2] + lup_region + 's%02d' % lran['display_order']]
	    })
	    ostr += ShowTextSection(pif, lsec, lran, modlist[lran['start']:lran['end']], lup_region, year)
    else:
	lran = copy.deepcopy(lsec)
	lran.update({'id' : lup_region + '_1', 'name' : '', 'entry' : [], 'note' : '', 'graphics' : []})
	ostr += ShowTextSection(pif, lsec, lran, modlist, lup_region, year)

    #==================================

    secs = GetExtraSections(pif, year)
    CreateExtraLineup(pif, year, secs, verbose=pif.render.verbose)

    for lran in secs:
	lran['anchor'] = 'S' + lran['id'].replace('.', '')
	lran.update({
	    'id' : 'X_' + str(lran['display_order']),
	    'entry' : [],
	    'graphics' : [lran['img_format'][:2] + lup_region + 's%02d' % lran['display_order']]
	})
	ostr += ShowTextSection(pif, lsec, lran, lran['mods'], 'X', year)

    llineup['section'].append(lsec)
    llineup['tail'] = [pif.render.FormatImageArt('bamca_sm'), '']
    llineup['tail'][1] += pif.render.FormatButtonComment(pif, 'yr=%s&rg=%s' % (pif.form.get('year'), pif.form.get('region')))
#    if int(year) > config.yearstart:
#	llineup['tail'][1] += pif.render.FormatButton("previous_year", link='http://www.bamca.org/cgi-bin/lineup.cgi?year=%s&region=%s' % (int(year) - 1, region))
#    if int(year) > config.yearend:
#	llineup['tail'][1] += pif.render.FormatButton("following_year", link='http://www.bamca.org/cgi-bin/lineup.cgi?year=%s&region=%s' % (int(year) + 1, region))
    return ostr


#--------- ranks -----------------------------------

def GenerateRankLineup(pif, rank, region, syear, eyear):
    verbose = pif.render.verbose
    lmodlist = pif.dbh.FetchLineupModelsByRank(rank, syear, eyear)
    lmodlist.sort(key=lambda x: x['lineup_model.year'])
    regionlist = mbdata.GetRegionTree(region)
    if verbose: # pragma: no cover
	print regionlist, '<br>'
    years = dict()
    for mod in lmodlist:
	if verbose: # pragma: no cover
	    print '<hr>', mod
	mod['number'] = int(mod['lineup_model.year'])
	if mod['lineup_model.region'] and mod['lineup_model.region'] not in regionlist:
	    if verbose: # pragma: no cover
		print 'dropreg<br>'
	elif not mod['vs.sub_id'] or mod['lineup_model.region'] == mod['vs.sub_id']:
	    years.setdefault(mod['number'], dict())
	    years[mod['number']].setdefault(mod['lineup_model.region'], [])
	    years[mod['number']][mod['lineup_model.region']].append(mod)
	    if verbose: # pragma: no cover
		print 'keep', mod['number'], mod['lineup_model.region'], '<br>'
	elif verbose: # pragma: no cover
	    print 'drop<br>'
    if verbose: # pragma: no cover
	print '<hr>'

    lmoddict = dict()
    keys = years.keys()
    keys.sort()
    for year in keys:
	if verbose: # pragma: no cover
	    print year, '<br>'
	#reg, year = CorrectRegion(region, year)
	reg = region

	for line_reg in regionlist:
	    if verbose: # pragma: no cover
		print '<b>', year, line_reg, '</b><br>'
	    mod_list = years[year].get(line_reg, [])
	    for reg in regionlist:
#		if year in lmoddict:
#		    if verbose: # pragma: no cover
#			print "completed %s/%s<br>" % (year, reg)
#		    break
		for mod in mod_list:
		    SetVar(mod, lmoddict, reg, 'year.%s' % year, verbose)
	if year in lmoddict:
	    if verbose: # pragma: no cover
		print 'yield', lmoddict[year], '<br>'
	    yield lmoddict[year]
	    if verbose: # pragma: no cover
		print '<br>'


def GatherRankPages(pif, pages, region):
    region_list = mbdata.GetRegionTree(region)
    sections = pif.dbh.FetchSections(where="page_id like 'year.%'")
    sections = map(lambda x: pif.dbh.DePref('section', x), sections)
    sections = filter(lambda x: x['id'][0] in region_list, sections)
    sections.sort(key=lambda x: x['start'], reverse=True)
    for rg in region_list:
	for page in pages:
	    pages[page].setdefault('section', list())
	    for section in sections:
		if section['id'][0] == rg and section['page_id'] == page:
		    pages[page]['section'].append(section)
    # now each page should have the right sections and in the right order
    # the first section found where start < num is the right one


def GetProductImage(page, mnum):
    if page:
	for section in page['section']:
	    if section['start'] < mnum:
		return section['img_format'], page['page_info.pic_dir']
    return 'xxx%02d', 'unknown'


def RunRanks(pif, mnum, region, syear, eyear):
    if not mnum or not mnum.isdigit():
	print 'Lineup number must be a number from 1 to 120.  Please back up and try again.'
	print '<meta http-equiv="refresh" content="10;url=/database.php">'
	return dict()
    mnum = int(mnum)
    pif.render.Comment('lineup.RunRanks', mnum, region, syear, eyear)

    pages = dict(map(lambda x: (x['page_info.id'], x), pif.dbh.FetchPageYears()))
    GatherRankPages(pif, pages, region)

    lmodlist = GenerateRankLineup(pif, mnum, region, syear, eyear)

    llineup = {'id' : pif.page_id, 'section' : [], 'name' : '', 'tail':''}
    lsec = {'columns' : 5, 'id' : 'lineup', 'range' : []}
    hdr = "Number %s" % mnum
    comments = set()

    lran = {'id' : 'range', 'name' : '', 'entry' : [], 'note' : '', 'graphics' : []}
    pif.render.Comment("RunRanks: range", lran)
    for mdict in lmodlist:
	if mdict:
	    ifmt, pdir = GetProductImage(pages.get(mdict.get('lineup_model.page_id', ''), {}), mnum)
	    #mdict['number'] = mnum
	    mdict['disp_format'] = '%s.'
	    mdict['shown_id'] = mdict['lineup_model.year']
	    mdict['image_format'] = ifmt
	    mdict['pdir'] = pdir
	    mdict['anchor'] = '%d' % mdict['number']
	    ent = {
		'text' : ShowLineupModel(pif, mdict, comments, 1), 
		'display_id' : '0', 'style' : ''
	    }
	    if mdict['lineup_model.year'] == mdict['first_year']:
		ent['class'] = 'newcasting'
	    lran['entry'].append(ent)
	else:
	    lran['entry'].append({'text' : '', 'display_id' : ''})
    lsec['range'].append(lran)

    llineup['section'].append(lsec)
    llineup['tail'] = [pif.render.FormatImageArt('bamca_sm'), '']
    #llineup['tail'][1] += pif.render.FormatButton("comment_on_this_page", link='../pages/comment.php?page=%s&yr=%s&rg=%s' % (pif.page_id, pif.form.get('year'), pif.form.get('region')), also={'class' : 'comment'}, lalso=dict())
    llineup['tail'][1] += pif.render.FormatButtonComment(pif, 'yr=%s&rg=%s' % (pif.form.get('year'), pif.form.get('region')))
    for comment in comments:
	llineup['tail'][1] += mbdata.comment_designation[comment] + '<br>'
    return llineup


#--------- prodpics --------------------------------

def RunProductPictures(pif, region):
    halfstars = dict()
    if os.path.exists('pic/multivars.dat'):
	for ln in open('pic/multivars.dat').readlines():
	    ln = ln.strip().split()
	    if len(ln) > 1 and ln[1] == region:
		halfstars[ln[0]] = map(int, ln[2:])
    pages = pif.dbh.FetchPageYears()
    if pif.form.get('syear'):
	pages = filter(lambda x: x['page_info.id'] >= 'year.' + pif.form['syear'], pages)
    if pif.form.get('eyear'):
	pages = filter(lambda x: x['page_info.id'] <= 'year.' + pif.form['eyear'], pages)
    pages = dict(map(lambda x: (x['page_info.id'], x), pages))
    GatherRankPages(pif, pages, region)
    region_list = mbdata.GetRegionTree(region)

    llineup = {'id' : pif.page_id, 'section' : [], 'name' : '', 'tail':''}
    lsec = {'columns' : 1, 'id' : 'lineup', 'range' : []}
    hdr = ""
    comments = set()

    keys = pages.keys()
    keys.sort()
    for page in keys:
	lmodlist = pif.dbh.FetchSimpleLineupModels(page[5:], region)
	lmodlist = filter(lambda x: x['lineup_model.region'][0] in region_list, lmodlist)
	lmoddict = dict(map(lambda x: (x['lineup_model.number'], x), lmodlist))
	min_num = 1
	max_num = pages[page]['max(lineup_model.number)']
	if pif.form.get('num'):
	    min_num = int(pif.form['num'])
	if pif.form.get('enum'):
	    max_num = int(pif.form['enum'])
	lsec['columns'] = max(lsec['columns'], max_num + 1)
	lran = {'id' : pages[page]['page_info.id'], 'name' : '', 'entry' : [], 'note' : '', 'graphics' : []}
	ent = {
	    'text' : page[5:],
	    'display_id' : '1', 'style' : ''
	}
	lran['entry'].append(ent)
	for mnum in range(min_num, max_num + 1):
	    ifmt, pdir = GetProductImage(pages[page], mnum)
	    lmod = lmoddict.get(mnum, {})
	    lpic_id = pic_id = lmod.get('lineup_model.picture_id')
	    if pic_id:
		lpic_id = pic_id = pic_id.replace('W', region)
		product_image = pif.render.FindImageFile(pic_id, suffix='jpg', pdir=pdir)
	    else:
		lpic_id = ifmt % mnum
		product_image = pif.render.FindImageFile([ifmt % mnum], suffix='jpg', pdir=pdir)
	    #http://www.bamca.org/cgi-bin/single.cgi?dir=pic/univ&pic=1982u05&ref=year.1982&sub=&id=MB005
	    lnk = "single.cgi?dir=%s&pic=%s&ref=%s&sub=%s&id=%s" % (pdir, lpic_id, page, '', lmod.get('lineup_model.mod_id', ''))
	    #def FormatLink(self, url, txt, args={}, nstyle=None, also={}):
	    ent = {
		'text' : pif.render.FormatLink(lnk, images.ImageStar(pif, product_image, pic_id, mnum in halfstars.get(page[5:], []))),
		'display_id' : str(int(mnum % 10 == 0 or page[-1] == '0'))
	    }
	    lran['entry'].append(ent)
	lsec['range'].append(lran)

    llineup['section'].append(lsec)
    return llineup

#--------- mack ------------------------------------

def ShowMackModel(pif, mod):
    # id, man_id, imgstr, name
    mdict = {'id' : mod['mack_id'], 'man_id' : mod['mod_id'], 'name' : mod['name'].strip(),
	'imgstr' : pif.render.FormatImageRequired('s_' + mod['mod_id'])
    }
    return models.AddModelLink(pif, mdict)


# missing 51s 
#id_re = re.compile('(?P<p>\D*)(?P<n>\d*)(?P<l>\D*)')
def LineupToMack(pif, start, end, series):
    # mack_id, mod_id, name
    if 'RW' in series:
	if 'SF' in series:
	    series = None
	else:
	    series = ''
    else:
	series = 'MB'
    rwmods = pif.dbh.FetchCastingList('rw')
    sfmods = pif.dbh.FetchCastingList('sf')
    aliases = pif.dbh.FetchAliases()
    mack = dict()
    for alias in aliases:
	ModToMack(mack, alias, 'alias.id', start, end, series)
    for sfmod in sfmods:
	ModToMack(mack, sfmod, 'base_id.id', start, end, series)
    for rwmod in rwmods:
	ModToMack(mack, rwmod, 'base_id.id', start, end, series)
    return mack


def ModToMack(mack, rec, key, start, end, series):
    mack_id = mbdata.GetMackNumber(rec[key])
    if not mack_id:
	return
    if int(mack_id[1]) < start:
	return
    if int(mack_id[1]) > end:
	return
    if series != None and series != mack_id[0]:
	return
    mack_id_fmt = '%s%02s-%s' % mack_id
    mack[mack_id] = {
	'mack_id' : mack_id_fmt.upper(),
	'mack_id_unf' : mack_id,
	'mod_id' : rec['base_id.id'],
	'name' : rec['base_id.rawname'].replace(';', ' ')
    }
	    


def MackLineup(pif):
    pif.render.hierarchy.append(('/', 'Home'))
    pif.render.hierarchy.append(('/database.php', 'Database'))
    pif.render.hierarchy.append((pif.request_uri, 'Mack Numbers'))
    pif.render.PrintHtml()
    region = pif.form.get('region', 'U')
    series = pif.form.get('sect', 'all')
    if series == 'all':
	series = ['RW', 'SF']
    else:
	series = [series.upper()]
    range = pif.form.get('range', 'all')
    import useful
    start = pif.FormInt('start', 1)
    end = pif.FormInt('end', 100)
    if range == 'all':
	start = 1
	end = 100

    print pif.render.FormatHead()

    lsec = pif.dbh.DePref('section', pif.dbh.FetchSections({'page_id' : pif.page_id})[0])
    mods = LineupToMack(pif, start, end, series)

    modids = mods.keys()
    modids.sort(key=lambda x: (mods[x]['mack_id_unf'][1], mods[x]['mack_id_unf'][0], mods[x]['mack_id_unf'][2]))

    llineup = {'section' : [], 'note' : ''}
    lsec['range'] = []
    ran = {'entry' : []}
    if modids:
	for mod in modids:
	    ran['entry'].append({'text' : ShowMackModel(pif, mods[mod])})
    else:
	llineup['note'] = 'Your request produced no models.'
	if start > 100:
	    llineup['note'] += '  Be sure to use numbers from 1 to 100.'
	if start > end:
	    llineup['note'] += "  Use a start number that isn't higher than the end number."
    lsec['range'].append(ran)
    llineup['section'].append(lsec)

    print pif.render.FormatLineup(llineup)
    #print pif.render.FormatButton("comment_on_this_page", link='../pages/comment.php?page=%s&rg=%s&sec=%s&start=%s&end=%s' % (pif.page_id, pif.form.get('region', ''), pif.form.get('sect', ''), pif.form.get('start', ''), pif.form.get('end', '')), also={'class' : 'comment'}, lalso=dict())
    print pif.render.FormatButtonComment(pif, 'rg=%s&sec=%s&start=%s&end=%s' % (pif.form.get('region', ''), pif.form.get('sect', ''), pif.form.get('start', ''), pif.form.get('end', '')))
    print pif.render.FormatTail()

#--------- makes -----------------------------------

def MakesMain(pif):
    makelist = map(lambda x: (x['vehicle_make.make'], x['vehicle_make.make_name']), pif.dbh.FetchVehicleMakes())
    makedict = dict(makelist + [('unl', 'Unlicensed'), ('', 'Unknown')])
    make = pif.form.get('make', '')
    makes = [make]

    pif.render.hierarchy.append(('/', 'Home'))
    pif.render.hierarchy.append(('/database.php', 'Database'))
    pif.render.hierarchy.append(('/cgi-bin/makes.cgi', 'Models by Make'))
    if make == 'text':
	pif.render.hierarchy.append((pif.request_uri, 'Search'))
    elif make:
	pif.render.hierarchy.append((pif.request_uri, makedict.get(make, make)))
    pif.render.PrintHtml()
    print pif.render.FormatHead()

    if make == 'text':
	makename = pif.form.get('text')
	if makename:
	    makes = []
	    for m in makelist:
		if m[1].lower().startswith(makename.lower()):
		    makes.append(m[0])
	    if not makes:
		makes = ['unk']
	else:
	    make = ''

    if make:
	llineup = ShowMakes(pif, makedict, makes)
	print pif.render.FormatLineup(llineup)
    else:
	print MakesForm(pif, makelist)
    print pif.render.FormatButtonComment(pif, 'make=%s&text=%s' % (pif.form.get('make', ''), pif.form.get('text', '')))
    print pif.render.FormatTail()


def MakesForm(pif, makelist):
    cols = 5
    makelist.sort(key=lambda x: x[1])
    rows = ((len(makelist) + 1) / cols) + 1
    ostr = '<center><h2>Matchbox 1-75 Models By Make</h2></center><hr>'
    ostr += 'Choose a make:<br><form>'
    ostr += '<table width="100%%"><tr><td width="%d%%" valign="top">' % (100/cols)
    ostr += '<input type="radio" name="make" value="unk" checked>unknown<br>'
    i = rows - 1
    for ent in [['unl', 'unlicensed']] + makelist:
	ostr += ' <input type="radio" name="make" value="%s">%s' % tuple(ent)
	if pif.IsAllowed('a'): # pragma: no cover
	    ostr += ' - ' + ent[0]
	ostr += '<br>'
	i = i - 1
	if i == 0:
	    ostr += '</td><td width="%d%%" valign="top">' % (100/cols)
	    i = rows
    ostr += '</td></tr></table><hr>'
    ostr += pif.render.FormatButtonInput('see the models')
    ostr += '</form>'
    return ostr


def ShowMakeSection(pif, make_id, make_dict):
    casting_make = make_id
    if make_id == 'unk':
	casting_make = ''
    lsec = dict()#pif.dbh.FetchSections({'page_id' : pif.page_id})[0]
    lsec['anchor'] = make_id
    lsec['range'] = []
    lsec['note'] = ''
    lsec['id'] = ''
    lsec['name'] = make_dict.get(make_id, make_id)
    lran = {'id' : '', 'name' : '', 'anchor' : '', 'note' : '', 'entry' : []}
    castings = pif.dbh.FetchCastingList(where=["casting.make='%s'" % casting_make, "section.page_id='manno'"])
    aliases = []#pif.dbh.FetchAliases(where="casting.make='%s'" % casting_make)
    mlist = []

    for mdict in castings:
	mlist.append(pif.dbh.ModifyManItem(mdict))

    for mdict in aliases:
	mdict = pif.dbh.ModifyManItem(mdict)
	if mdict.get('alias.ref_id'):
	    mdict['picture_id'] = mdict['id']
	    mdict['id'] = mdict['alias.id']
	    #mdict['descs'] = mdict['descs']
	    #mdict['descs'].append('same as ' + mdict['ref_id'])
	mlist.append(mdict)

    mlist.sort(key=lambda x: x['name'])
    for mdict in mlist:
	# input mdict:  id, (picture_id), made, country, link, linkid, name, descs, made, unlicensed, scale, (type)
	lran['entry'].append({'text' : models.AddModelTablePicLink(pif, mdict, flago=models.flago)})

    lsec['range'].append(lran)
    return lsec


def ShowMakes(pif, makedict, makes):
    llineup = {'id' : '', 'name' : '', 'section' : []}
    models.flago = flags.FlagList(pif)

    for make_id in makes:
	lsec = ShowMakeSection(pif, make_id, makedict)
	llineup['section'].append(lsec)
    return llineup


#--------- mline -----------------------------------

# Kill it with a stick!
def FullLineup(pif):
    pif.render.PrintHtml()
    #pif.ReadForm({ 'year' : '1966' })
    import useful
    year = pif.FormInt('year')

    import files
    dblist = files.SimpleFile('src/mbx.dat')

    print pif.render.FormatHead()

    shown = 0
    dirs = dict()

    llineup = {'id' : pif.page_id, 'name' : "Matchbox Lineup for %d" % year, 'graphics' : [], 'section' : []}
    ostr = ''

    for llist in dblist:
	cmd = llist.GetArg('', 0)
	if cmd == 'dir':
	    dirs[llist.GetArg(start=1)] = llist.GetArg(start=2)
	    continue

	startyear = int(llist.GetArg('0', 1))
	endyear = int(llist.GetArg('0', 2))
	modno = llist.GetArg('0', 3)
	rank = int(llist.GetArg('0', 4))
	title = llist.GetArg('', 5)
	desc = llist.GetArg('', 6)

	if year < startyear or year > endyear:
	    continue

	if cmd == 'H':
	    if rank and pif.FormInt(modno):
		if shown:
		    ostr += "</tr></table></center>"
		ostr += "<h3><center>" + title + "</center></h3>"
		shown = 0
		cols = int(rank)
	elif pif.form.get(cmd, '0') != '1':
	    pass
	elif cmd == 'CAT':
	    llineup['graphics'].append({'file' : cmd + modno})
	    ostr += "<center><table>"
	    ostr += " <tr align=top><td><center>%s</td></tr>" % pif.render.FormatImageRequired([cmd + modno], pdir=dirs.get(cmd))
	    ostr += "</table></center>"
	    shown = 0
	else:
	    if shown == 0:
		ostr += "<center><table><tr align=top>"
	    shown += 1

	    modelid = ''
	    if cmd == 'MB' or cmd == 'RW':
		modelid = "%d" % int(modno)
	    elif not (cmd == 'E' or cmd == 'PZL'):
		modelid = "%s-%d" % (cmd, int(modno))

	    # id, man_id, imgstr, is_new, name
	    mdict = {'id' : '', 'man_id' : modelid, 'imgstr' : '', 'is_new' : 0, 'name' : ''}
	    ostr += " <td valign=top width=%d><center><b>%s</b><br>" % (width[cols], modelid)
	    if cmd == 'RW':
		ostr += '<a href="single.cgi?dir=%s&pic=%sw%s&id=%s">%s</a><br>' %\
		    (pif.render.pic_dir, str(year)[2:], modno, cmd + modno + VerNo(int(rank)), pif.render.FormatImageRequired(['s_' + cmd + modno + VerNo(int(rank))], pdir=dirs.get(cmd)))
	    else:
		ostr += '%s<br>' %\
		    (pif.render.FormatImageRequired([cmd + modno + VerNo(int(rank)) ,'s_' + cmd + modno + VerNo(int(rank))], pdir=dirs.get(cmd)))
	    if year == startyear:
		ostr += pif.render.FormatImageArt('new') + ' '
	    ostr += title + "</center></td>"
	    if (shown == cols):
		ostr += "</tr></table></center>"
		shown = 0

    if shown:
	ostr += "</tr></table></center>"

    ostr += '<hr>'#'<a href=".">BACK to query</a>'
    ostr += '<p>'

    print ostr
    print pif.render.FormatTail()

#---- -------------------------------------------------------------------


if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
