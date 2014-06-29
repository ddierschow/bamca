#!/usr/local/bin/python

import glob, os, re, sys
import basics
import config
import images
import mbdata
import models

# ---------------------------------------------------------------------

# columns, colspan, rowspan
layouts = {
    '2h' : [2, 2, 1],
    '2v' : [2, 1, 2],
    '3h' : [3, 3, 1],
    '3v' : [2, 1, 3],
    '4h' : [4, 4, 1],
    '4v' : [2, 1, 4],
    '5h' : [4, 3, 1],
    '5l' : [2, 1, 3],
    '5s' : [3, 2, 2],
    '5v' : [2, 1, 5],
    '6s' : [3, 2, 3],
    '7s' : [4, 3, 3],
    '8h' : [4, 4, 1],
    '8s' : [3, 2, 2],
    '8v' : [4, 3, 4],
    '9h' : [3, 3, 1],
    'th' : [4, 3, 2],
    'tv' : [3, 2, 4],
    'wh' : [4, 4, 1],
}

# ---- actions --------------------------------------------------------

def AddModel(pif, id, num=1):
    print pif.form
    while num:
	pif.dbh.InsertPackModel(id)
	num -= 1


def DeletePack(pif, id):
    print "deleting", id
    pif.dbh.DeletePack(id)
    pif.dbh.DeletePackModels(pif.page_id, id)


def SaveForm(pif):
    print pif.form,'<br>'
    mods = [x[6:] for x in filter(lambda x: x.startswith('pm.id.'), pif.form.keys())]
    pm_table_info = pif.dbh.table_info['pack_model']
    pm_table_info['name'] = 'pack_model'
    pms = []
    for mod in mods:
	pms.append({
	    'id' : mod,
	    'pack_id' : pif.FormStr('id'),
	    'mod_id' : pif.form.get('pm.mod_id.' + mod, ''),
	    'var_id' : pif.form.get('pm.var_id.' + mod, ''),
	    'display_order' : pif.FormInt('pm.display_order.' + mod),
	})
    pif.dbh.UpdatePackModels(pms, pif.page_id, pif.FormStr('o_id'))
    p_table_info = pif.dbh.table_info['pack']
    p_table_info['name'] = 'pack'
    if pif.FormStr('o_id') != pif.FormStr('id'): # change id of pack
	pif.dbh.UpdateVariationSelectSub(pif.FormStr('id'), pif.FormStr('page_id'), pif.FormStr('o_id'))
	if os.path.exists(pif.render.pic_dir + '/' + pif.FormStr('o_id') + '.jpg'):
	    os.rename(pif.render.pic_dir + '/' + pif.FormStr('o_id') + '.jpg', pif.render.pic_dir + '/' + pif.FormStr('id') + '.jpg')
    pif.dbh.UpdatePack(pif.FormStr('o_id'), {x: pif.form.get(x, '') for x in p_table_info['columns']})
    p_table_info = pif.dbh.table_info['base_id']
    p_table_info['name'] = 'base_id'
    pif.dbh.UpdateBaseId(pif.FormStr('o_id'), {x: pif.form.get(x, '') for x in p_table_info['columns']})

# ---- page list ------------------------------------------------------

def MakePageList(pif):
    pages = pif.dbh.FetchPages("format_type='packs'")
    pages.sort(key=lambda x: x['page_info.title'])
    lsec = [pif.dbh.DePref('section', x) for x in pif.dbh.FetchSections({'page_id' : 'packs'})]
    entries = list()
    lsec[0]['range'] = [{'entry' : entries}]
    llineup = {'id': 'main', 'name': '', 'section': lsec}
    for page in pages:
	page = pif.dbh.DePref('page_info', page)
	if not (page['flags'] & pif.dbh.FLAG_PAGE_INFO_NOT_RELEASED):
	    txt = models.AddIcons(pif, page['id'][6:], '', '') + '<br>' + page['title']
	    entries.append({'text' : pif.render.FormatLink('?page=' + page['id'][page['id'].find('.') + 1:], txt)})
    ostr = '<center>\n' + pif.render.FormatLineup(llineup) + '<center>\n'
    ostr += pif.render.FormatButtonComment(pif)
    print ostr

# ---- pack list ------------------------------------------------------

def MakePackList(pif, year=None, reg=None, lid=None):
    packs = pif.dbh.FetchPacks(page_id=pif.page_id)
    for pack in packs:
	pif.dbh.DePref('base_id', pack)
	pif.dbh.DePref('pack', pack)
	pack['name'] = pack['rawname'].replace(';', ' ')
    packs.sort(key=lambda x: (x[pif.form.get('order', 'name')], x['name'], x['first_year']))
    years = []
    regions = []

    print '<table class="packs" width="100%"><tr>'
    if pif.IsAllowed('m'): # pragma: no cover
	print '<td valign="top">\n'
    else:
	print '<td width="70%" valign="top">\n'
    print '<table>\n'
    if pif.IsAllowed('m'): # pragma: no cover
	print '<tr><th>Pack ID</th><th>Name</th><th>Year</th><th>Product</th><th>Reg</th><th>Ctry</th><th>Th</th><th>Pic</th><th>Mat</th><th>Models</th><th>Note</th><th>Related</th></tr>\n'
    else:
	print '<tr><th>Name</th><th>Year</th><th>Product Code</th><th>Region</th><th>Note</th><th></th></tr>\n'
    for pack in packs:
	if pack['first_year'] not in years:
	    years.append(pack['first_year'])
	if pack['region'] and pack['region'] not in regions:
	    regions.append(pack['region'])
	if year and year != pack['first_year']:
	    continue
	if reg and reg != pack['region']:
	    continue
	if lid and not pack['id'].startswith(lid):
	    continue
	pack['thumb'] = pack['pic'] = pack['stars'] = ''
	if pif.IsAllowed('m'): # pragma: no cover
	    models = pif.dbh.FetchPackModels(pack_id=pack['id'], page_id=pif.page_id)
	    pmodels = DistillModels(pif, pack, models)

	    stars = ''
	    keys = pmodels.keys()
	    keys.sort()
	    for mod in keys:

		if not pmodels[mod].get('id'):
		    stars += pif.render.FormatImageArt('stargreen.gif') + ' '
		elif not pmodels[mod].get('vs.var_id'):
		    stars += pif.render.FormatImageArt('starred.gif') + ' '
		elif pmodels[mod]['imgstr'].find('-') < 0:
		    stars += pif.render.FormatImageArt('stargray.gif') + ' '
		else:
		    stars += pif.render.FormatImageArt('star.gif') + ' '

	    pack['stars'] = stars

	relateds = []#pif.dbh.FetchPacksRelated(pack['id'])
	pack['rel'] = [x['pack.id'] for x in relateds]
	pack['rel'].sort()
	pack['rel'] = ' '.join(pack['rel'])

	pack['page'] = pif.form.get('page', '')
	pack['regionname'] = mbdata.regions[pack['region']]
	if pif.IsAllowed('m'): # pragma: no cover
	    print '<tr><td>%(id)s</td><td><a href="?page=%(page)s&id=%(id)s">%(name)s</a></td><td>%(first_year)s</td><td>%(product_code)s</td><td>%(region)s</td><td>%(country)s</td><td>%(thumb)s</td><td>%(pic)s</td><td>%(material)s</td><td>%(stars)s</td><td>%(note)s</td><td>%(rel)s</td></tr>\n' % pack
	else:
	    print '<tr><td><a href="?page=%(page)s&id=%(id)s">%(name)s</a></td><td>%(first_year)s</td><td>%(product_code)s</td><td>%(regionname)s</td><td>%(note)s</td><td>%(rel)s</td></tr>\n' % pack
	sys.stdout.flush()
    print '</table></td>'
    if pif.IsAllowed('m'): # pragma: no cover
	print '<td valign="top">'
    else:
	print '<td width="30%" valign="top">'
    print '<form>'

    years.sort()
    regions.sort()
    print 'Filter by Year<br>'
    print pif.render.FormatRadio('year', zip([''] + years, ['all'] + years), checked='', sep='<br>')
    print '<p>'
    print 'Filter by Region<br>'
    print pif.render.FormatRadio('region', zip([''] + regions, ['all'] + [mbdata.regions[x] for x in regions]), checked='', sep='<br>')
    print '<p>'
#    print pif.render.FormatSelect('lid', CalcPackSelect(pif, packs))
    print '<p>'
    print pif.render.FormatButtonInput()
    print pif.render.FormatButton("add", '?add_pack=unset&page=%s' % pif.form.get('page', '5packs'))
    print '<input type="hidden" name="page" value="%s">' % pif.form.get('page')
    print '</form>'
    print '</td></tr></table>\n'
    print pif.render.FormatButtonComment(pif)


'''
def CalcPackSelect(pif, packs):
    cats = {}
    for pack in packs:
	cats.setdefault(pack['id'][0:3], [])
	if pack['name'] not in cats[pack['id'][0:3]]:
	    cats[pack['id'][0:3]].append(pack['name'])
    sels = [('','')]
    keys = cats.keys()
    keys.sort()
    for key in keys:
	if pif.IsAllowed('a'): # pragma: no cover
	    sels.append((key, key + ' ' + ' / '.join(cats[key])))
	else:
	    sels.append((key, ' / '.join(cats[key])))
    return sels
'''


'''
def Dump(name, recs):
    print '<h3>', name, '</h3>'
    for rec in recs:
	print rec, '<br>'
    print '<p>'
'''

# ---- single pack ----------------------------------------------------

def DoSinglePack(pif, pack):
    if not pack:
	return "That pack doesn't seem to exist.", ""
    id = pack['pack.id']
    packmodels = pif.dbh.FetchPackModels(pack_id=id, page_id=pif.page_id)
    relateds = pif.dbh.FetchPacksRelated(id)
    #Dump('relateds', relateds)
    #Dump('packs', packs)
    #Dump('packmodels', packmodels)

    # editor
    pstr = pif.render.FormatTableStart()
    tcomments = set()
    #pif.render.Comment('section:', section[0])
    for key in pack.keys():
	pack[key[key.find('.') + 1:]] = pack[key]
    pack['name'] = pack['rawname'].replace(';', ' ')

    layout = layouts.get(pack['layout'], [4,4,1])
    lsec = {}
    lsec['columns'] = layout[0]
    lsec['anchor'] = pack['id']
    pif.render.Comment('pack:', pack)
    entries = [{'text' : ShowPack(pif, pack), 'display_id' : '0', 'colspan' : layout[1], 'rowspan' : layout[2]}]

    pmodels = DistillModels(pif, pack, packmodels)
    keys = pmodels.keys()
    keys.sort()
    for mod in keys:
	pif.render.Comment("DoSinglePack mod", pmodels[mod])

	if not pmodels[mod].get('id'):
	    pmodels[mod]['no_casting'] = 1
	    tcomments.add('m')
	else:
	    if pmodels[mod]['imgstr'].find('-') < 0:
		tcomments.add('i')
	    if not pmodels[mod].get('vs.var_id'):
		pmodels[mod]['no_variation'] = 1
		tcomments.add('v')

	entries.append({'text' : ShowPackModel(pif, pmodels[mod]), 'display_id' : 1})
	pstr += EditModel(pif, pmodels[mod])
    lsec['range'] = [{'entry' : entries}]

    lsec['id'] = ''

    llineup = {}
    llineup['section'] = []
    llineup['tail'] = ''
    llineup['section'].append(lsec)
    llineup['id'] = ''

    # displayer

    # left bar
    content = ''
    if pif.IsAllowed('a'): # pragma: no cover
	content += str(pack['page_id']) + '/' + str(pack['id']) + '<br>'
	content += '<p><b><a href="%s">Base ID</a></b><br>\n' % pif.dbh.GetEditorLink(pif, 'base_id', {'id' : id})
	content += '<b><a href="%s">Pack</a></b><br>\n' % pif.dbh.GetEditorLink(pif, 'pack', {'id' : id})
	content += '<b><a href="traverse.cgi?d=./pic/packs">Library</a></b>\n'

    ostr = '<table width="100%"><tr>\n'
    ostr += models.AddLeftBar(pif, pif.page_name, id, '', 4, content)

    # top bar
    ostr += '<td class="titlebar">\n'
    ostr += pack['name']
    if pack['note']:
	ostr += '<br><span style="font-size: smaller;">' + pack['note'] + '</span>'
    ostr += '</td></tr>\n'

    # our feature presentation
    ostr += '<tr><td>\n'
    ostr += pif.render.FormatLineup(llineup)
    ostr += '</td></tr>\n'

    # oh, just one more thing
    ostr += '<tr><td>\n'
    if relateds:
	ostr += '<h3>Related Packs</h3>\n<ul>\n'
	for related in relateds:
	    ostr += '<li>'
	    ostr += pif.render.FormatLink("?page=" + pif.form.get('page', '') + "&id=" + related['pack.id'], related['base_id.rawname'])
	    if related['pack.product_code']:
		ostr += ' - (' + related['pack.product_code'] + ')'
	    if related['pack.region']:
		ostr += ' - ' + mbdata.regions[related['pack.region']]
	    if related['pack.country']:
		ostr += ' - Made in ' + mbdata.GetCountry(related['pack.country'])
	    if related['pack.material']:
		ostr += ' - ' + materials.get(related['pack.material'], '')
	    if related['base_id.description']:
		ostr += ' - ' + related['base_id.description']
	ostr += '</ul>\n'
    ostr += '</td></tr>\n'

    # bottom bar
    ostr += '<tr><td class="bottombar">\n'
    ostr += pif.render.FormatButtonComment(pif, 'd=%s' % pif.form.get('id'))
    for comment in tcomments:
	ostr += mbdata.comment_designation[comment] + '<br>'
    ostr += '</td></tr></table>\n'
    pstr += pif.render.FormatTableEnd()
    return ostr, pstr


def DistillModels(pif, pack, models):
    pack['pic'] = ''
    for pic in glob.glob('pic/packs/' + pack['id'] + '.jpg'):
	pack['pic'] += images.ImageStar(pif, pic)
    if glob.glob('pic/man/s_' + pack['id'] + '.jpg'):
	pack['thumb'] = pif.render.FormatImageArt('starblack.gif')
    pmodels = {}
    #['pack_model.pack_id', 'pack_model.mod_id', 'pack.layout', 'vs.ref_id', 'pack_model.id', 'casting.rawname', 'base_id.id', 'pack.year', 'v.text_description', 'casting.vehicle_type', 'casting.model_type', 'vs.sub_id', 'pack.name', 'pack.material', 'base_id.description', 'pack.country', 'casting.scale', 'pack_model.var_id', 'pack.id', 'pack.section_id', 'casting.country', 'casting.section_id', 'pack.product_code', 'vs.var_id', 'v.picture_id', 'base_id.model_type', 'pack_model.display_order', 'casting.make', 'pack.page_id', 'base_id.flags', 'vs.mod_id', 'casting.first_year', 'casting.description', 'base_id.rawname', 'base_id.first_year', 'casting.id', 'pack.region']

    for mod in filter(lambda x: x['pack.id'] == pack['id'], models):
	#print mod,'<br>'
	mod = pif.dbh.ModifyManItem(mod)
	sub_ids = [None, '', pack['id'], pack['id'] + '.' + str(mod['pack_model.display_order'])]
	if mod['vs.sub_id'] in sub_ids:
	    mod['imgl'] = ['s_' + mod['id'], mod['id']]
	    for s in mod['descs']:
		if s.startswith('same as '):
		    mod['imgl'].extend(['s_' + s[8:], s[8:]])
	    if not mod.get('vs.ref_id'):
		mod['vs.ref_id'] = ''
	    if not mod.get('vs.sub_id'):
		mod['vs.sub_id'] = ''
	    mod['pdir'] = pif.render.pic_dir
	    mod['href'] = "single.cgi?id=%(pack_model.mod_id)s&dir=%(pdir)s&pic=%(pack_model.pack_id)s&ref=%(vs.ref_id)s&sub=%(vs.sub_id)s" % mod
	    #'<a href="single.cgi?dir=%(dir)s&pic=%(link)s&ref=%(vs.ref_id)s&id=%(mod_id)s">' % ent
	    #'pack_model.pack_id': 'car02',
	#    if mod['pack_model.var'] and mod['imgl']: # still not perfect
	#	mod['href'] = mod['href'] + '&pic=' + mod['imgl'][mod['imgl'].rfind('/') + 1:-2]
	    mod['vars'] = []
	    mod['pics'] = []
	    if not mod['pack_model.display_order'] in pmodels:
		pmodels[mod['pack_model.display_order']] = mod
	    if mod['v.picture_id']:
		pmodels[mod['pack_model.display_order']]['pics'].append(mod['v.picture_id'])
	    else:
		pmodels[mod['pack_model.display_order']]['pics'].append(mod['vs.var_id'])
	    if mod.get('vs.var_id'):
		pmodels[mod['pack_model.display_order']]['vars'].append(mod['vs.var_id'])
    for dispo in pmodels:
	pmodels[dispo]['imgstr'] = pif.render.FormatImageRequired(pmodels[dispo]['imgl'], pdir=config.imgdir175, vars=pmodels[dispo].get('pics'))
    return pmodels


materials = {
    'C' : 'cardboard',
    'T' : 'plastic tube',
    'S' : 'square plastic tube',
    '' : 'unknown',
}
#'columns' : ['id', 'page_id', 'section_id', 'name', 'first_year', 'region', 'layout', 'product_code', 'material', 'country'],
def ShowPack(pif, pack):
    ostr = pif.render.FormatImageRequired(pack['id'])
    if pif.IsAllowed('a'): # pragma: no cover
	ostr = '<a href="upload.cgi?d=./%s&r=%s">%s</a>' % (pif.render.pic_dir, pack['id'], ostr)
    else:
	ostr = '<a href="upload.cgi">%s</a>' % (ostr)
    pack['country'] = mbdata.GetCountry(pack['country'])
    pack['material'] = materials.get(pack['material'], '')
    if pack['product_code']:
	ostr += '<br>' + pack['product_code']
    if pack['region']:
	ostr += '<br>' + mbdata.regions[pack['region']]
    if pack['first_year']:
	ostr += '<p><b>%(first_year)s</b><br>%(country)s - %(material)s' % pack
    return ostr


#mdict: descriptions href imgstr name no_casting not_made number pdir picture_only product subname
#def AddModelTableProductLink(pif, mdict):

def ShowPackModel(pif, mdict):
    pif.render.Comment("ShowPackModel", mdict)

    mdict['number'] = ''
    mdict['descriptions'] = []
    if mdict['v.text_description']:
	mdict['descriptions'] = [mdict['v.text_description']] # fix this
    mdict['product'] = ''
    if mdict['imgstr'].find('-') < 0:
	mdict['no_specific_image'] = 1
    return models.AddModelTableProductLink(pif, mdict)


def EditModel(pif, mdict):
    ostr = pif.render.FormatRowStart()
    ostr += '<input type="hidden" name="pm.id.%s" value="%s">\n' % (mdict['pack_model.id'], mdict['pack_model.id'])
    ostr += '<input type="hidden" name="pm.pack_id.%s" value="%s">\n' % (mdict['pack_model.id'], mdict['pack_model.pack_id'])
    ostr += pif.render.FormatCell(0, 'mod ' + pif.render.FormatTextInput("pm.mod_id.%s" % mdict['pack_model.id'], 8, 8, value=mdict['pack_model.mod_id']))
    ostr += pif.render.FormatCell(0, 'var ' + pif.render.FormatTextInput("pm.var_id.%s" % mdict['pack_model.id'], 20, 20, value='/'.join(mdict['vars'])) + ' (' + str(mdict['pack_model.var_id']) + ')')
    ostr += pif.render.FormatCell(0, 'disp ' + pif.render.FormatTextInput("pm.display_order.%s" % mdict['pack_model.id'], 2, 2, value=mdict['pack_model.display_order']))
    ostr += pif.render.FormatRowEnd()
    return ostr

# ---- main -----------------------------------------------------------

@basics.WebPage
def DoPage(pif):
    pif.render.PrintHtml()
    pif.render.hierarchy.append(('/', 'Home'))
    pif.render.hierarchy.append(('/database.php', 'Database'))
    pif.render.hierarchy.append(('packs.cgi', 'Multi-Model Packs'))
    if type(pif.form.get('id')) == list:
	pif.form['id'] = pif.FormStr('id')[0]
    year = pif.form.get('year')
    reg = pif.form.get('region')
    var = pif.form.get('ver')
    id = pif.form.get('id')
    lid = pif.form.get('lid')
    if pif.form.get('add_pack'):
	pif.dbh.InsertPack(pif.form.get('add_pack'), pif.page_id)
	id = pif.form.get('add_pack')
	if pif.form.get('page') == '5packs':
	    AddModel(pif, id, 5)
	elif pif.form.get('page') == '10packs':
	    AddModel(pif, id, 10)
    elif pif.form.get('delete'):
	DeletePack(pif, id)
	return
    pack = dict()
    if id:
	packs = pif.dbh.FetchPack(id)
	if packs:
	    pack = packs[0]
	    pif.render.hierarchy.append(('', pack['base_id.rawname']))
    print pif.render.FormatHead()
    if id:
	if pif.form.get('add'):
	    AddModel(pif, pif.form.get('o_id', 'unset'), pif.FormInt('n', 1))
	elif pif.form.get('save'):
	    SaveForm(pif)
	pack_l, mod_form = DoSinglePack(pif, pack)
	print pack_l
	if pif.IsAllowed('m'): # pragma: no cover
	    print '<form>'
	    PackForm(pif, id)
	    print mod_form
	    print pif.render.FormatButtonInput("save")
	    print pif.render.FormatButtonInput("delete")
	    print pif.render.FormatTextInput('n', 2, 2, '1')
	    print pif.render.FormatButtonInput("add")
	    print '</form>'
    elif pif.form.get('page'):
	MakePackList(pif, year, reg, lid)
    else:
	MakePageList(pif)
    print pif.render.FormatTail()


def PackForm(pif, id):
    ostr = ''
    tabinf = pif.dbh.table_info
    tabinf['pack']['name'] = 'pack'
    tabinf['base_id']['name'] = 'base_id'
    dat = pif.dbh.FetchPack(id=id)
    if dat:
	dat = dat[0]
	print '<input type="hidden" name="verbose" value="1">'
	print '<input type="hidden" name="page" value="%s">' % pif.page_name
	#print '<input type="hidden" name="save" value="1">'
	print '<input type="hidden" name="table" value="%s">' % tabinf['pack']['name']
	for f in tabinf['pack']['id']:
	    print '<input type="hidden" name="o_%s" value="%s">' % (f, dat['pack.' + f])
	print pif.render.FormatTableStart()
	TabForm(pif, tabinf, 'pack', dat)
	TabForm(pif, tabinf, 'base_id', dat)
    print pif.render.FormatTableEnd()


paren_re = re.compile('''\((?P<n>\d*)\)''')
def TabForm(pif, tabinf, tab, dat):
    descs = pif.dbh.DescribeDict(tabinf[tab]['name'])
    for col in tabinf[tab]['columns']:
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, col)
	coltype = descs.get(col).get('type')
	print pif.render.FormatCell(0, coltype)
	print pif.render.FormatCell(1, str(dat[tab + '.' + col]))
	colwidth = int(paren_re.search(coltype).group('n'))
	print pif.render.FormatCell(1, pif.render.FormatTextInput(col, colwidth, colwidth, value=dat[tab + '.' + col]))
	print pif.render.FormatRowEnd()
	sys.stdout.flush()

# ---------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
