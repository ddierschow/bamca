#!/usr/local/bin/python

import copy, re
import basics
import config
import mbdata
import models
import tables
import useful

d_re = re.compile(r'%\d*d')

class MatrixFile:
    def __init__(self, pif):
	self.tables = []
	self.text = []

	mats = pif.dbh.FetchSections({'page_id' : pif.page_id})
	ents = pif.dbh.FetchMatrixModelsVariations(pif.page_id)
	for mat in mats:
	    mat = pif.dbh.DePref('section', mat)
	    ffmt = {'link' : mat['link_format'], 'disp' : mat['disp_format'], 'img' : mat['img_format']}
	    is_num_id = d_re.search(ffmt['disp']) or d_re.search(ffmt['link']) or d_re.search(ffmt['img'])
	    mat['text'] = ''
	    mat['ents'] = {}
	    pif.render.Comment('matrix section:', mat)
	    for ent in ents:
		if ent['matrix_model.section_id'] == mat['id']:
		    ent.setdefault('vs.ref_id', '')
		    ent.setdefault('vs.sub_id', '')
		    ent['id']              = ent['matrix_model.id']
		    ent['mod_id']          = ent['matrix_model.mod_id']
		    ent['section_id']      = ent['matrix_model.section_id']
		    ent['display_order']   = ent['matrix_model.display_order']
		    ent['page_id']         = ent['matrix_model.page_id']
		    ent['range_id']        = ent['matrix_model.range_id']
		    ent['flags']           = ent['matrix_model.flags']
		    ent['shown_id']        = ent['matrix_model.shown_id']
		    ent['name']            = ent['matrix_model.name']
		    ent['subname']         = ent['matrix_model.subname']
		    ent['sub_id']          = mbdata.reverse_regions.get(ent['matrix_model.subname'], '')
		    #ent['subname'] += ' (%s, %s)' % (ent['sub_id'], ent.get('vs.sub_id', ''))
		    ent['description']     = []
		    if ent.get('sub_id') and ent.get('vs.sub_id') and ent['sub_id'] != ent['vs.sub_id']:
			continue
		    if ent.get('v.text_description'):
			ent['description'].append(ent['v.text_description'])
		    if ent.get('matrix_model.description'):
			ent['description'].extend(ent['matrix_model.description'].split(';'))
#		    if pif.render.verbose:
#			ent['description'].append('(' + ent['matrix_model.description'] + ')')
		    ent['description'] = filter(None, ent['description'])
		    ent['disp_id'] = ''
		    ent['image'] = ''
		    ent['link'] = ''
		    ent['pdir']         = mat['pic_dir']
		    if not ent['pdir']:
			ent['pdir'] = pif.render.pic_dir
		    if is_num_id:
			if ent['range_id']:
			    ent['range_id'] = int(ent['range_id'])
			else:
			    ent['range_id'] = 0
		    if ent['range_id'] and ffmt['img']:
			ent['image'] = \
				pif.render.FormatImageRequired([useful.CleanName(ffmt['img'] % ent['range_id'], '/')])
		    elif ent.get('v.picture_id'):
			ent['image'] = \
				pif.render.FormatImageOptional(ent['mod_id'] + '-' + ent['v.picture_id'], prefix='s_', pdir=config.imgdirVar)
		    elif ent.get('v.var'):
			ent['image'] = \
				pif.render.FormatImageOptional(ent['mod_id'] + '-' + ent['v.var'], prefix='s_', pdir=config.imgdirVar)
		    if ent['range_id'] and ffmt['disp']:
			ent['disp_id'] = ent['range_id']
		    if ent['range_id'] and ffmt['link']:
			if '%' in ffmt['link']:
			    ent['link'] = useful.CleanName(ffmt['link'] % ent['range_id'], '/')
			else:
			    ent['link'] = useful.CleanName(ffmt['link'], '/')
#		    if ent['image']:
#			ent['image'] = '<center><table><tr><td class="spicture">%s</td></tr></table></center>' % ent['image']
		    mat['ents'].setdefault(ent['range_id'], list())
		    mat['ents'][ent['range_id']].append(ent)
		    ent['disp_format'] = mat['disp_format']
		    pif.render.Comment('        entry:', ent)
	    self.tables.append(mat)
	self.tables.sort(key=lambda x: x['display_order'])

    def Matrix(self, pif):
	if not pif.render.simple:
	    pif.render.tail['printable'] = 1
	llineup = {'id' : pif.page_name, 'section' : [], 'note' : '\n'.join(self.text), 'columns' : 4, 'tail' : ''}
	comments = set()

	for table in self.tables:
	    section_name = table['name']
	    if not (table['flags'] & pif.dbh.FLAG_MODEL_HIDE_IMAGE) and (table['id'] not in pif.page_id.split('.')):
		img = pif.render.FormatImageOptional(table['id'], pdir=table['pic_dir'])
		if img:
		    section_name += '<br>' + img
	    section = {'id' : table['id'], 'name' : section_name, 'range' : [], 'anchor' : table['id'], 'columns' : table['columns'], 'anchor' : table['id']}
	    if pif.IsAllowed('a'): # pragma: no cover
		section['name'] += " (%s/%s)" % (pif.page_id, section['id'])
		if pif.FormHas('large'):
		    section['columns'] = 1
	    ran = {'entry' : []}
	    range_ids = table['ents'].keys()
	    #range_ids.sort()
	    range_ids.sort(key=lambda x: table['ents'][x][0]['display_order'])
	    for range_id in range_ids:
		if pif.render.flags & pif.dbh.FLAG_PAGE_INFO_UNROLL_MODELS:
		    for ent in table['ents'][range_id]:
			if ent.get('sub_id'):
			    mods = self.FindMatrixVariations([ent], pif.page_id, [ent['sub_id']])
			else:
			    mods = self.FindMatrixVariations([ent], pif.page_id, [table['id'], str(range_id)])
			ostr = self.AddCell(pif, mods, table, comments)
			ran['entry'].append({'text' : ostr, 'display_id' : pif.page_name})
		else:
		    mods = self.FindMatrixVariations(table['ents'][range_id], pif.page_id, [table['id'], str(range_id)])
		    ostr = self.AddCell(pif, mods, table, comments)
		    ran['entry'].append({'text' : ostr, 'display_id' : pif.page_name})
	    section['range'].append(ran)
	    llineup['section'].append(section)
	pif.render.Comment('Calculating tail.')
	llineup['tail'] = [pif.render.FormatImageArt('bamca_sm'), '']
	#llineup['tail'][1] = pif.render.FormatButton("comment_on_this_page", link='../pages/comment.php?page=%s' % (pif.page_id), also={'class' : 'comment'}, lalso={})
	llineup['tail'][1] = pif.render.FormatButtonComment(pif, '')
	for comment in comments:
	    llineup['tail'][1] += mbdata.comment_designation[comment] + '<br>'
	return llineup

    def FindMatrixVariations(self, ents, page_id, vsids):
	for idsegs in range(len(vsids), 0, -1):
	    id = '.'.join(vsids[:idsegs])
	    mods = filter(lambda x: x['vs.sub_id'] == id, ents)
	    if mods:
		return mods
	mods = filter(lambda x: x['vs.sub_id'] == '', ents)
	if mods:
	    return mods
	mod = copy.deepcopy(ents[0])
	mod['description'] = mod['matrix_model.description'].split(';')
	mod['vs.ref_id'] = ''
	mod['vs.sub_id'] = ''
	mod['v.picture_id'] = None
	mod['v.text_description'] = None
	mod['v.var'] = None
	mod.setdefault('image', '')
	return [mod]

    def AddCell(self, pif, ents, table, comments):
	entd = {}
	for ent in ents:
	    entd.setdefault(ent['mod_id'], [])
	    entd[ent['mod_id']].append(ent)

	pif.render.Comment('AddCell', entd)

	varimage = ''
	for mod in entd:
	    ent = entd[mod][0]

	    for ent2 in entd[mod][1:]:
		if ent['flags'] & tables.FLAG_MODEL_SHOW_ALL_VARIATIONS:
		    ent['image'] += ent2['image']
		elif not ent['image']:
		    ent['image'] = ent2['image']
		for desc in ent2['description']:
		    if desc not in ent['description']:
			ent['description'].append(desc)
	    if ent['image']:
		varimage = ent['image']

	if ent['flags'] & tables.FLAG_MODEL_NO_VARIATION:
	    ent['picture_only'] = 1
	elif not ent['mod_id']:
	    comments.add('m')
	    ent['no_casting'] = 1
	    ent['picture_only'] = 1
	else:
	    if not ent.get('vs.ref_id'):
		comments.add('v')
		ent['no_variation'] = 1
	    if not varimage:
		comments.add('i')
		ent['no_specific_image'] = 1
	ent['imgstr'] = varimage

	ent['number'] = ent['disp_id']
	if not ent['shown_id'] and ent['disp_id']:
	    ent['shown_id'] = ent['disp_id']
	if ent['flags'] & pif.dbh.FLAG_MODEL_NO_ID:
	    ent['shown_id'] = ''

	ent['product'] = [ent['link']]
	if pif.render.FindImageFile(ent['product'], suffix='jpg'):
	    comments.add('c')
	    ent['is_product_picture'] = 1
	    if pif.IsAllowed('a') and pif.FormHas('large'): # pragma: no cover
		pass
	if ent['flags'] & tables.FLAG_MODEL_NOT_MADE:
	    comments.add('n')
	    ent['not_made'] = 1
	    ent['picture_only'] = 1

	ent['href'] = ''
	if ent['mod_id']:
	    ent['href'] = "single.cgi?dir=%(pdir)s&pic=%(link)s&ref=%(vs.ref_id)s&sub=%(vs.sub_id)s&id=%(mod_id)s" % ent
	else:
	    img = pif.render.FindImageFile(ent['link'])
	    if img:
		ent['href'] = '/' + img
	    #FormatImageOptional([ent['link']])
	vstr = ''
	ent['descriptions'] = filter(None, ent['description'])
	if ent['descriptions'] and (not ent['flags'] & tables.FLAG_MODEL_NO_VARIATION):
	    pass
	elif ent['matrix_model.description']:
	    ent['descriptions'] = ent['matrix_model.description'].split(';')

	ent['anchor'] = '%s' % ent['number']

	#mdict: descriptions imgstr name no_casting not_made number pdir product
	ostr = models.AddModelTableProductLink(pif, ent)
	if pif.IsAllowed('a'): # pragma: no cover
	    ostr += pif.render.FormatButton("edit", pif.dbh.GetEditorLink('matrix_model', {'id' : ent['id']}))
	    ostr += pif.render.FormatButton("upload", "upload.cgi?d=%s&r=%s" % (pif.render.pic_dir, ent['link'] + '.jpg'))
	return ostr


def scmp(a, b):
    r = cmp(a['page_info.description'], b['page_info.description'])
    if r == 0:
	r = cmp(a['page_info.title'], b['page_info.title'])
    return r

#'columns' : ['id', 'flags', 'format_type', 'title', 'pic_dir', 'tail', 'description', 'note'],
def SelectMatrix(pif):
    ostr = "A few of the special sets produced by Matchbox in recent years:\n<ul>\n"
    ser = pif.dbh.FetchPages("id like 'matrix.%'")
    ser.sort(scmp)
    for ent in ser:
	ent['page_info.id'] = ent['page_info.id'].split('.', 1)[-1]
	link = '<b><a href="?page=%(page_info.id)s">%(page_info.title)s</a></b> - %(page_info.description)s' % ent
	if not (ent['page_info.flags'] & 1):
	    ostr += '<li>' + link + '\n'
	elif pif.IsAllowed('a'): # pragma: no cover
	    ostr += '<li><i>' + link + '</i>\n'
    ostr += "</ul>\n"
    ostr = pif.render.FormatTableSingleCell(0, ostr) + '\n'
    ostr += pif.render.FormatButton("back", link="..")
    ostr += " to the main index.\n"
    return ostr


@basics.WebPage
def Main(pif):
    pif.render.PrintHtml()
    matf = None
    if pif.FormHas('page'):
	matf = MatrixFile(pif)
    pif.render.hierarchy.append(('/', 'Home'))
    pif.render.hierarchy.append(('/database.php', 'Database'))
    pif.render.hierarchy.append(('/cgi-bin/matrix.cgi', 'Series'))
    pif.render.hierarchy.append(('/cgi-bin/matrix.cgi?page=%s' % pif.FormStr('page'), pif.render.title))
    print pif.render.FormatHead()
    if matf:
	#print pif.render.FormatImageOptional(pif.FormStr('page', 'default').split('.'), also={'class':'centered'})
	llineup = matf.Matrix(pif)
	print pif.render.FormatLineup(llineup)
    else:
	print SelectMatrix(pif)
    print pif.render.FormatTail()

if __name__ == '__main__': # pragma: no cover
    pass
