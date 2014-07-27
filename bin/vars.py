#!/usr/local/bin/python

import copy, glob, os, re

import basics
import config
import mbdata
import useful


note_attributes = ['manufacture', 'area', 'category', 'date', 'note', 'from_CY_number']
desc_attributes = ['text_description', 'text_base', 'text_body', 'text_interior', 'text_wheels', 'text_windows']
hidden_attributes = ['mod_id', 'var', 'picture_id', 'other', 'references', 'imported', 'imported_from', 'imported_var', 'flags', 'catlist']
detail_attributes = ['base', 'body', 'interior', 'windows']

DISPLAY_TYPE_NONE = 0
DISPLAY_TYPE_GRID = 1
DISPLAY_TYPE_FULL = 2

fieldwidth_re = re.compile(r'\w+\((?P<w>\d+)\)')
def ShowDetail(pif, field, attributes, variation, edit=False, id=''):
    ostr = pif.render.FormatRowStart()
    if edit and pif.IsAllowed('a'): # pragma: no cover
	ostr += pif.render.FormatCell(1, field)
    ostr += pif.render.FormatCell(0, attributes[field]['title'], id=id)
    ostr += pif.render.FormatCell(1, variation.get(field, ''), id=id)
    if edit and pif.IsAllowed('a'): # pragma: no cover
	width = 20
	if '(' in attributes[field]['definition']:
	    width = int(fieldwidth_re.search(attributes[field]['definition']).group('w'))
	ostr += pif.render.FormatCell(1, pif.render.FormatTextInput(field + "." + variation['var'], width, 64, value=variation.get(field, '')))
    ostr += pif.render.FormatRowEnd()
    return ostr


def ShowDetails(pif, data, attributes, variation, edit=False, id=''):
    ostr = ''
    for d in data:
	ostr += ShowDetail(pif, d, attributes, variation, edit, id=id)
    return ostr


def ShowVariation(pif, man, var_id):
    #man = pif.dbh.FetchCasting(id)
    mod_id = id = man['id']
    #pif.render.title = mod_id + ': ' + man['name']
    print pif.render.FormatHead(extra=pif.render.reset_button_js + pif.render.increment_select_js)
    print '<table width=100%><tr><td class="title">' + pif.render.title + '</td></tr></table>'
    #print pif.render.FormatButton("back_to_main_casting_page", "single.cgi?id=%s" % mod_id)
    values = dict()
    attributes = {x['attribute_name']: x for x in pif.dbh.DePref('attribute', pif.dbh.FetchAttributes(mod_id))}
    attributes.update({pif.dbh.table_info['variation']['columns'][x]: {'title' : pif.dbh.table_info['variation']['titles'][x]} for x in range(0, len(pif.dbh.table_info['variation']['columns']))})
    attributes['references'] = {'title' : 'References', 'definition' : 'varchar(256)'}

    variation = pif.dbh.DePref('variation', pif.dbh.FetchVariation(mod_id, var_id))
    #variation = pif.dbh.FetchVariation(mod_id, var_id)
    if not variation: # pragma: no cover
	return
    variation = variation[0]
    vardescs = pif.dbh.Describe('variation')
    for vardesc in vardescs:
	if vardesc['field'] in attributes:
	    attributes[vardesc['field']]['definition'] = vardesc['type']
    print '<center>'

    if variation['picture_id']:
	pic_var = variation['picture_id']
    else:
	pic_var = variation['var']
    fname = useful.CleanName(variation['mod_id'] + '-' + pic_var)
    img = pif.render.FormatImageRequired([fname], pdir=pif.render.pic_dir + '/var', prefix=['h_', 'l_', 'm_', 's_'])
    if pif.IsAllowed('u'): # pragma: no cover
	print '<a href="upload.cgi?d=%s&m=%s&v=%s">' % (os.path.join(config.libmandir, id.lower()), id, pic_var) + img + '</a>'
    else:
	print '<a href="upload.cgi?m=%s&v=%s">%s</a>' % (id, var_id, img)
    print '<p></center>'

    selects = GetVarSelects(pif, mod_id)

    values = UpdateValues(variation, values)
    variation['area'] = ', '.join([mbdata.regions.get(x, x) for x in variation.get('area', '').split(';')])
    data = variation.keys() + filter(lambda d: d not in variation, attributes)
    hdrs = {x:x for x in variation}
    data.sort()

    print '<form action="vars.cgi" name="vars" method="post">'
    print '<center>'

    print pif.render.FormatTableStart(id='det')

    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, 'Title', hdr=True, id='det')
    print pif.render.FormatCell(0, 'Value', hdr=True, id='det')
    print pif.render.FormatRowEnd()

    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, 'Description Attributes', hdr=True, also={'colspan':2}, id='det')
    print pif.render.FormatRowEnd()

    print ShowDetails(pif, filter(lambda d: not (d in desc_attributes or d in note_attributes or d in hidden_attributes), data),
		attributes, variation, id='det')

    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, 'Notes', hdr=True, also={'colspan':2}, id='det')
    print pif.render.FormatRowEnd()

    print ShowDetails(pif, filter(lambda d: d in note_attributes, data), attributes, variation, id='det')

    print pif.render.FormatTableEnd()

    print '<p>'
    #print '<input type="hidden" name="verbose" value="1">'
    print '<input type="hidden" name="page" value="%s">' % pif.page_id
    print '<input type="hidden" name="mod" value="%s">' % mod_id
    print '<input type="hidden" name="var" value="%s">' % var_id
    print '</center>'
    print Appearances(pif, mod_id, var_id)

    print pif.render.FormatButton("see all", 'vars.cgi?mod=%s' % mod_id)
    if pif.IsAllowed('a'): # pragma: no cover
	print '-', pif.render.FormatButton("delete", 'vars.cgi?mod=%s&var=%s&delete=1' % (mod_id, var_id))
	print pif.render.FormatButton("edit", 'vars.cgi?mod=%s&var=%s&edit=1' % (mod_id, var_id))
	print pif.render.FormatButton("pictures", 'upload.cgi?d=%s&m=%s&v=%s&l=1' % (os.path.join(config.libmandir, mod_id.lower()), mod_id, var_id))
	print pif.render.FormatButton("remove_picture", '?mod=%s&var=%s&rmpic=1' % (mod_id, var_id))
	print pif.render.FormatButton("casting", pif.dbh.GetEditorLink('casting', {'id' : mod_id}))
	print pif.render.FormatButton("recalc", '?recalc=1&mod=%s' % mod_id)
    if pif.IsAllowed('u'): # pragma: no cover
	print '-', pif.render.FormatButton("upload", 'upload.cgi?d=' + os.path.join(config.libmandir, mod_id.lower()))
    #print pif.render.FormatButton("comment_on_this_page", link='../pages/comment.php?page=%s&man=%s&var=%s' % (pif.page_id, id, var_id), also={'class' : 'comment'}, lalso={})
    print pif.render.FormatButtonComment(pif, 'man=%s&var=%s' % (id, var_id))
    print '</form>'
    print '<hr>'


def Appearances(pif, mod_id, var_id):
    varsel = pif.dbh.FetchVariationSelects(mod_id, var_id)
    ostr = ''
    if varsel:
	ostr += "Appearances:\n<ul>\n"
	for vs in varsel:
	    if vs['variation_select.ref_id'].startswith('matrix.'):
		if vs['variation_select.sub_id']:
		    ostr += '<li>' + pif.render.FormatLink("matrix.cgi?page=%s#%s" % (vs['variation_select.ref_id'], vs['variation_select.sub_id']), vs['page_info.title']) + '\n'
		else:
		    ostr += '<li>' + pif.render.FormatLink("matrix.cgi?page=%s" % vs['variation_select.ref_id'], vs['page_info.title']) + '\n'
	    elif vs['variation_select.ref_id'].startswith('packs.'):
		ostr += '<li>' + pif.render.FormatLink("packs.cgi?page=%s&id=%s" % (vs['variation_select.ref_id'], vs['variation_select.sub_id']), "%(page_info.title)s: %(base_id.rawname)s (%(base_id.first_year)s)" % vs) + '\n'
	    elif vs['variation_select.ref_id'].startswith('year.') and vs['lineup_model.region']:
		#lineup.cgi?year=2001&region=U#71
		vs['region'] = mbdata.regions.get(vs['lineup_model.region'], 'Worldwide')
		if not vs.get('lineup_model.region'):
		    vs['lineup_model.region'] = 'W'
		if vs.get('lineup_model.region', '').startswith('X'):
		    vs['region'] = 'Worldwide'
		    vs['lineup_model.number'] = 'S' + vs['lineup_model.region'].replace('.', '')
		    vs['lineup_model.region'] = 'U'
		    ostr += '<li>' + pif.render.FormatLink("lineup.cgi?year=%(lineup_model.year)s&region=%(lineup_model.region)s#%(lineup_model.number)s" % vs, "%(lineup_model.year)s %(region)s lineup" % vs) + '\n'
		elif vs.get('lineup_model.region') in ['M', 'S']:
		    pass
		elif not vs['variation_select.sub_id'] or vs['variation_select.sub_id'] == vs.get('lineup_model.region'):
		    ostr += '<li>' + pif.render.FormatLink("lineup.cgi?year=%(lineup_model.year)s&region=%(lineup_model.region)s#%(lineup_model.number)s" % vs, "%(lineup_model.year)s %(region)s lineup number %(lineup_model.number)s" % vs) + '\n'
	    elif pif.IsAllowed('a'): # pragma: no cover
		ostr += '<li><i>ref_id = ' + str(vs['variation_select.ref_id'])
		if vs['variation_select.sub_id']:
		    ostr += ' / sub_id = ' + str(vs['variation_select.sub_id'])
		ostr += " (vs = %s)</i>\n" % str(vs)
	ostr += "</ul><hr>\n"
    return ostr


def ShowVariationEditor(pif, id, var_id):
    man = pif.dbh.FetchCasting(id)
    pif.render.title = man['id'] + ': ' + man['name']
    print pif.render.FormatHead(extra=pif.render.reset_button_js + pif.render.increment_select_js)
    values = dict()
    mod_id = man['id']
    attributes = {x['attribute_name']: x for x in pif.dbh.DePref('attribute', pif.dbh.FetchAttributes(mod_id))}
    attributes.update({pif.dbh.table_info['variation']['columns'][x]: {'title' : pif.dbh.table_info['variation']['titles'][x]} for x in range(0, len(pif.dbh.table_info['variation']['columns']))})
    attributes['references'] = {'title' : 'References', 'definition' : 'varchar(256)'}

    variation = pif.dbh.DePref('variation', pif.dbh.FetchVariation(mod_id, var_id))
    if not variation:
	return
    variation = variation[0]
    for vardesc in pif.dbh.Describe('variation'):
	if vardesc['field'] in attributes:
	    attributes[vardesc['field']]['definition'] = vardesc['type']
    print '<center>Variation %s<p>' % variation['var'].upper()

    fname = useful.CleanName(variation['mod_id'])
    if variation['picture_id']:
	fname += '-' + useful.CleanName(variation['picture_id'])
    else:
	fname += '-' + useful.CleanName(variation['var'])
    if pif.IsAllowed('a'): # pragma: no cover
	img = pif.render.FormatImageRequired([fname], pdir=pif.render.pic_dir + '/var', prefix=['t_'])
	img += pif.render.FormatImageRequired([fname], pdir=pif.render.pic_dir + '/var', prefix=['s_'])
	img += pif.render.FormatImageRequired([fname], pdir=pif.render.pic_dir + '/var', prefix=['m_'])
	img += pif.render.FormatImageRequired([fname], pdir=pif.render.pic_dir + '/var', prefix=['l_'])
    else:
	img = pif.render.FormatImageRequired([fname], pdir=pif.render.pic_dir + '/var', prefix=['h_', 'l_', 'm_', 's_'])
    if pif.IsAllowed('u'): # pragma: no cover
	print '<a href="upload.cgi?d=%s&m=%s&v=%s">' % (os.path.join(config.libmandir, id.lower()), id, var_id) + img + '</a>'
    else:
	print '<a href="upload.cgi?m=%s&v=%s">%s</a>' % (id, var_id, img)
    print '<p></center>'
    selects = GetVarSelects(pif, mod_id)

    print '<form action="vars.cgi" name="vars" method="post">'

    print pif.render.FormatTableStart()

    print pif.render.FormatRowStart()
    if pif.IsAllowed('a'): # pragma: no cover
	print pif.render.FormatCell(0, 'Field', hdr=True)
    print pif.render.FormatCell(0, 'Title', hdr=True)
    print pif.render.FormatCell(0, 'Value', hdr=True)
    if pif.IsAllowed('a'): # pragma: no cover
	print pif.render.FormatCell(0, 'New', hdr=True)
    print pif.render.FormatRowEnd()

    variation['references'] = ' '.join(list(set(selects.get(var_id, []))))
    values = UpdateValues(variation, values)
    variation['area'] = ', '.join([mbdata.regions.get(x, x) for x in variation.get('area', '').split(';')])
    data = variation.keys()
    for key in attributes:
	if not key in data:
	    data.append(key)
    hdrs = {x: x for x in variation.keys()}
    data.sort()

    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, 'Identification Attributes', hdr=True, also={'colspan':4})
    print pif.render.FormatRowEnd()

    print ShowDetail(pif, 'mod_id', attributes, variation, True)
    print ShowDetail(pif, 'var', attributes, variation, True)

    if pif.IsAllowed('a'): # pragma: no cover
	print ShowDetail(pif, 'picture_id', attributes, variation, True)
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(1, '')
	print pif.render.FormatCell(0, "Move pictures to")
	print pif.render.FormatCell(1, '')
	print pif.render.FormatCell(1, pif.render.FormatTextInput("repic." + variation['var'], 16, 16))
	print pif.render.FormatRowEnd()

    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, 'Description Attributes', hdr=True, also={'colspan':4})
    print pif.render.FormatRowEnd()

    for d in data:
	if d in desc_attributes or d in note_attributes or d in hidden_attributes:
	    pass
	else:
	    print ShowDetail(pif, d, attributes, variation, True)

    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, 'Notes', hdr=True, also={'colspan':4})
    print pif.render.FormatRowEnd()

    for d in data:
	if d not in note_attributes:
	    pass
	else:
	    print ShowDetail(pif, d, attributes, variation, True)
    if pif.IsAllowed('a'): # pragma: no cover
	print ShowDetail(pif, 'references', attributes, variation, True)
	print ShowDetail(pif, 'imported_from', attributes, variation, True)
	print ShowDetail(pif, 'imported_var', attributes, variation, True)

    print pif.render.FormatTableEnd()
    print Appearances(pif, mod_id, var_id)

    print '<p>'
    #print '<input type="hidden" name="verbose" value="1">'
    print '<input type="hidden" name="page" value="%s">' % pif.page_id
    print '<input type="hidden" name="mod" value="%s">' % mod_id
    print '<input type="hidden" name="var" value="%s">' % var_id
    if pif.IsAllowed('a'): # pragma: no cover
	print pif.render.FormatButtonInput('save')
	print pif.render.FormatButtonReset('vars')
	print pif.render.FormatButton("delete", 'vars.cgi?mod=%s&var=%s&delete=1' % (mod_id, var_id))
	print pif.render.FormatButton("remove_picture", 'vars.cgi?mod=%s&var=%s&rmpic=1' % (mod_id, var_id))
	print pif.render.FormatButton("promote", '?mod=%s&var=%s&promote=1' % (mod_id, var_id))
	print pif.render.FormatButton("casting", pif.dbh.GetEditorLink('casting', {'id' : mod_id}))
	print pif.render.FormatButton("recalc", '?recalc=1&mod=%s' % mod_id)
    if pif.IsAllowed('u'): # pragma: no cover
	print pif.render.FormatButton("upload", 'upload.cgi?d=' + os.path.join(config.libmandir, mod_id.lower()))
	#print pif.render.FormatButton("pictures", 'traverse.cgi?d=./lib/%s' % mod_id.lower())
	print pif.render.FormatButton("pictures", 'upload.cgi?d=%s&m=%s&v=%s&l=1&c=%s+variation+%s' % (os.path.join(config.libmandir, mod_id.lower()), mod_id, var_id, mod_id, var_id))
    #print pif.render.FormatButton("comment_on_this_page", link='../pages/comment.php?page=%s&man=%s&var=%s' % (pif.page_id, id, var_id), also={'class' : 'comment'}, lalso={})
    print pif.render.FormatButtonComment(pif, 'man=%s&var=%s' % (id, var_id))
    print '</form>'
    print '<hr>'


def Save(pif, mod_id, var_id):
    if var_id:
	var_sel = repic = ''
	attributes = {x['attribute_name']: x for x in pif.dbh.DePref('attribute', pif.dbh.FetchAttributes(mod_id))}
	#attributes.update({pif.dbh.table_info['variation']['columns'][x]: {'title' : pif.dbh.table_info['variation']['titles'][x]} for x in range(0, len(pif.dbh.table_info['variation']['columns']))})
	pif.render.Comment("Save: ", attributes)
	var_dict = {'mod_id' : pif.FormStr('mod'), 'picture_id' : ''}
	det_dict = dict()
	for attr in note_attributes + detail_attributes:
	    if 'id' in attributes.get(attr, {}):
		det_dict[attr] = pif.FormStr(attr + '.' + var_id)
	    else:
		var_dict[attr] = pif.FormStr(attr + '.' + var_id)
	for key in pif.FormKeys(end='.' + var_id):
	    attr = key[:key.rfind('.')]
	    if attr == 'references':
		var_sel = pif.FormStr(key) # make it work!
	    elif attr == 'repic':
		repic = pif.FormStr(key)
		print 'repic', repic, '<br>'
	    elif attr == 'picture_id':
		if pif.FormStr(key) != var_id:
		    var_dict[attr] = pif.FormStr(key)
	    elif 'id' in attributes.get(attr, {}):
		det_dict[attr] = pif.FormStr(key)
	    else:
		var_dict[attr] = pif.FormStr(key)
	if 'from_CY_number' in var_dict and 'from_CY_number' not in attributes:
	    del var_dict['from_CY_number']
	print '<p>', det_dict, '<p>', var_dict
	if var_id != var_dict['var']:
	    RenameVariation(pif, var_dict['mod_id'], var_id, var_dict['var'])
	pif.dbh.Write('variation', var_dict)
	for attr in det_dict:
	    pif.dbh.Write('detail', {'mod_id' : var_dict['mod_id'], 'var_id' : var_dict['var'], 'attr_id' : str(attributes[attr]['id']), 'description' : det_dict[attr]})
	if var_sel:
	    print 'varsel', var_sel,'<br>'
	    pif.dbh.UpdateVariationSelects(mod_id, var_dict['var'], var_sel.split())
	if repic:
	    RenameVariationPictures(pif, mod_id, var_dict['var'], repic)
    else:
	SaveModel(pif, mod_id)
    RecalcDescription(pif, mod_id)
    man = pif.dbh.FetchCasting(mod_id)
    ShowModel(pif, man)


def AddVariation(pif, mod_id, var_id='unset', attributes={}): # pragma: no cover
    pif.dbh.InsertVariation(mod_id, var_id, attributes)


def RenameVariation(pif, mod_id, old_var_id, new_var_id): # pragma: no cover
    verbose = False
    if pif.argv:
	print 'RenameVariation', mod_id, old_var_id, new_var_id
	pif.dbh.dbi.verbose = verbose = True
    if old_var_id == new_var_id:
	return
    pif.dbh.UpdateVariation({'var' : new_var_id, 'imported_var' : new_var_id}, {'mod_id' : mod_id, 'var' : old_var_id}, verbose=verbose)
    pif.dbh.UpdateVariation({'picture_id' : new_var_id}, {'mod_id' : mod_id, 'picture_id' : old_var_id}, verbose=verbose)
    pif.dbh.UpdateDetail({'var_id' : new_var_id}, {'var_id' : old_var_id, 'mod_id' : mod_id}, verbose=verbose)
    pif.dbh.Write('variation_select', {'var_id' : new_var_id}, where="var_id='%s' and mod_id='%s'" % (old_var_id, mod_id), modonly=True, verbose=verbose)
    # If we're renaming, I'd like to also rename the pictures.
    RenameVariationPictures(pif, mod_id, old_var_id, new_var_id)


def RenameVariationPictures(pif, mod_id, old_var_id, new_var_id): # pragma: no cover
    patt1 = os.path.join(config.imgdirVar, '?_%s-%s.*' % (mod_id.lower(), old_var_id.lower()))
    patt2 = os.path.join(config.imgdirVar, '%s-%s.*' % (mod_id.lower(), old_var_id.lower()))
    pics = glob.glob(patt1.lower()) + glob.glob(patt2.lower())
    for pic in pics:
	pif.render.Comment("rename", pic, pic.replace('-%s.' % old_var_id.lower(), '-%s.' % new_var_id.lower()))
	print "rename", pic, pic.replace('-%s.' % old_var_id.lower(), '-%s.' % new_var_id.lower()), "<br>"
	os.rename(pic, pic.replace('-%s.' % old_var_id.lower(), '-%s.' % new_var_id.lower()))


def PromotePicture(pif, mod_id, var_id): # pragma: no cover
    print 'promoting picture for var', var_id, '<br>'
    for pic in glob.glob(config.imgdirVar + '/?_%s-%s.*' % (mod_id.lower(), var_id.lower())):
	ofn = pic[pic.rfind('/') + 1:]
	nfn = ofn[:ofn.find('-')] + ofn[ofn.find('.'):]
	useful.FileCopy(pic, config.imgdir175 + '/' + nfn)


def RemovePicture(pif, mod_id, var_id): # pragma: no cover
    patt1 = config.imgdirVar + '/?_%s-%s.*' % (mod_id, var_id)
    patt2 = config.imgdirVar + '/%s-%s.*' % (mod_id, var_id)
    pics = glob.glob(patt1.lower()) + glob.glob(patt2.lower())
    for pic in pics:
	pif.render.Comment("delete", pic)
	print "delete", pic, "<br>"
	os.unlink(pic)


def DeleteVariation(pif, mod_id, var_id): # pragma: no cover
    pif.dbh.DeleteVariation({'mod_id' : mod_id, 'var' : var_id})
    pif.dbh.DeleteDetail({'mod_id' : mod_id, 'var_id' : var_id})
    pif.dbh.DeleteVariationSelect({'mod_id' : mod_id, 'var_id' : var_id})


def SearchForm(pif, attributes, values={}):
    pif.render.Comment("attributes", attributes)
    keys = attributes.keys()
    keys.sort()
    print pif.render.FormatTableStart()
    for key in keys:
	if key not in desc_attributes:
	    continue
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, attributes[key]['title'])
	print pif.render.FormatCell(0, pif.render.FormatTextInput(key, 64, 64))
	print pif.render.FormatRowEnd()
    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0)
    print pif.render.FormatCell(0, pif.render.FormatCheckbox('ci', [(1, 'Case insensitive')]))
    print pif.render.FormatRowEnd()
    print pif.render.FormatTableEnd()
    print '<br>'
    print pif.render.FormatTableStart()
    for key in keys:
	if key in hidden_attributes or key in desc_attributes:
	    continue
	#pif.render.Comment(key)
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, attributes[key]['title'])
	if key == 'category':
	    cates = [('', '')] + [(x, mbdata.categories.get(x,x)) for x in values[key]]
	    cates.sort(key=lambda x: x[1])
	    pulldown = pif.render.FormatButtonUpDownSelect(key, -1) + pif.render.FormatSelect(key, cates, id=key)
	    pulldown += '&nbsp;' + pif.render.FormatCheckbox('c1', [(1, 'Code 1 only')])
	    print pif.render.FormatCell(0, pulldown)
	elif values.get(key):
	    values[key].sort()
	    print pif.render.FormatCell(0, pif.render.FormatButtonUpDownSelect(key, -1) + pif.render.FormatSelect(key, [('','')] + values[key], id=key))
	else:
	    print pif.render.FormatCell(0, pif.render.FormatTextInput(key, 64, 64))
	print pif.render.FormatCell(0, pif.render.FormatCheckbox('not_' + key, [(1, 'not')]))
	print pif.render.FormatRowEnd()

    if pif.IsAllowed('a') and isinstance(values.get('imported_from'), list): # pragma: no cover
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, attributes['imported_from']['title'])
	values['imported_from'].sort()
	print pif.render.FormatCell(0, pif.render.FormatButtonUpDownSelect('imported_from', -1) + pif.render.FormatSelect('imported_from', [('','')] + values['imported_from'], id='imported_from'))
	print pif.render.FormatCell(0, pif.render.FormatCheckbox('not_' + 'imported_from', [(1, 'not')]))
	print pif.render.FormatRowEnd()

    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, '&nbsp;')
    print pif.render.FormatCellStart(1)
    print pif.render.FormatButtonInput("filter", "submit")
    if pif.IsAllowed('a'): # pragma: no cover
	print pif.render.FormatButtonInput("list")
    print pif.render.FormatButtonReset('vars')
    print pif.render.FormatCellEnd()
    print pif.render.FormatCell(0, '&nbsp;')
    print pif.render.FormatRowEnd()
    print pif.render.FormatTableEnd()


'''
def ParseModel(model):
    result = []
    next = ''
    alpha = model[0].isalpha()
    for c in model:
	if alpha != c.isalpha():
	    if not alpha:
		next = str(int(next))
	    else:
		next = next.lower()
	    result.append(next)
	    alpha = not alpha
	    next = ''
	next = next + c
    result.append(next)
    return result
'''


def DoVar(pif, model, wheels, data, hdrs, attributes, prev):
    data.sort()
    cats = [mbdata.categories.get(x, x) for x in model['catlist']]

    ostr = pif.render.FormatRowStart()
    ostr += pif.render.FormatCellStart(0)

    ostr += '<center>'
    ostr += pif.render.FormatLink('?edit=1&mod=%s&var=%s' % (model['mod_id'], model['var']), model['var'].upper())
    if pif.IsAllowed('a'): # pragma: no cover
	ostr += '<br><input type="checkbox" name="v" value="%s"><br>' % model['var']
    ostr += '</center>'
    ostr += pif.render.FormatCellEnd()
    ostr += pif.render.FormatCellStart(1)
    dstr = ''
    for d in data:
	if d not in desc_attributes or d not in hdrs or not model[d]:
	    continue
	if d == 'text_description':
	    dstr = '<div class="varentry">' + model[d] + '</div>' + dstr
	else:
	    ln = attributes[d]['title'] + ' : ' + model[d]
	    if pif.IsAllowed('a') and model[d] != prev.get(d, model[d]): # pragma: no cover
		ln = '<b>' + ln + '</b>'
	    dstr += ln + '<br>'
    #ostr += ', '.join([model['body'], wheel])
    ostr += dstr + pif.render.FormatCellEnd()
    ostr += pif.render.FormatCellStart(1)
    for d in data:
	if d in desc_attributes or d in note_attributes or d in hidden_attributes or d not in hdrs or not model[d]:
	    pass
	elif pif.IsAllowed('a') and model[d] != prev.get(d, model[d]): # pragma: no cover
	    ostr += '<b>' + attributes[d]['title'] + ' : ' + model[d] + '</b><br>'
	else:
	    ostr += attributes[d]['title'] + ' : ' + model[d] + '<br>'
    #ostr += ', '.join([model['body'], wheel])
    ostr += pif.render.FormatCellEnd()
    if model['picture_id']:
	fname = useful.CleanName("%s-%s" % (model['mod_id'], model['picture_id'])).lower()
    else:
	fname = useful.CleanName("%s-%s" % (model['mod_id'], model['var'])).lower()
#    fnl = []
#    for i in range(2,len(model['var'])):
#	fnl.append(fname + model['var'][3:i+1])
#    fnl.reverse()
    cell = pif.render.FormatImageRequired([fname], pdir=pif.render.pic_dir + '/var', prefix=['s_'])
    if pif.IsAllowed('u'): # pragma: no cover
	cell = '<a href="upload.cgi?d=%s&m=%s&v=%s">' % (os.path.join(config.libmandir, model['mod_id'].lower()), model['mod_id'], model['var']) + cell + '</a>'
    else:
	cell = '<a href="upload.cgi?m=%s&v=%s">' % (model['mod_id'], model['var']) + cell + '</a>'
    ostr += pif.render.FormatCell(2, cell)
    ostr += pif.render.FormatCellStart(3)
    for d in data:
	if d not in note_attributes or not model[d]:
	    pass
	elif d == 'category':
	    ostr += attributes[d]['title'] + ' : ' + ', '.join(cats) + '<br>'
	else:
	    ostr += attributes[d]['title'] + ' : ' + model[d] + '<br>'
    if pif.IsAllowed('a'): # pragma: no cover
	ostr += 'Import : %s, %s-%s<br>' % (model['imported'], model['imported_from'], model['imported_var'])
	ostr += 'Show : ' + pif.render.FormatTextInput("picture_id." + model['var'], 8, value=model['picture_id'])
	for sz in mbdata.image_size_names:
	    if os.path.exists(os.path.join(config.imgdirVar, sz + '_' + model['mod_id'] + '-' + model['var'] + '.jpg').lower()):
		ostr += sz.upper() + ' '
	ostr += "<br>References:<br>" + pif.render.FormatTextInput("var_sel." + model['var'], 256, 24, value=model['references'])
    #ostr += ', '.join([model['body'], wheel])
    ostr += pif.render.FormatCellEnd()
    ostr += pif.render.FormatRowEnd()
    return ostr


def DoVarGrid(pif, model):
    if model['picture_id']:
	pic_var = model['picture_id']
    else:
	pic_var = model['var']
    data = model.keys()
    hdrs = {x: x for x in model}
    data.sort()
    cats = [mbdata.categories.get(x, x) for x in model['catlist']]

    fname = useful.CleanName("%s-%s" % (model['mod_id'], pic_var)).lower()
    imgstr = pif.render.FormatImageRequired([fname], pdir=pif.render.pic_dir + '/var', prefix=['s_'])
    ostr = pif.render.FormatLink('?mod=%s&var=%s' % (model['mod_id'], model['var']),
	model['var'].upper() + '<br>' + 
	'<center><table><tr><td class="spicture">' + imgstr + '</td></tr></table></center>')

    ostr += '<table class="vartable">'
    ostr += '<tr><td class="varentry"><i>%s</i></td></tr>' % model['text_description']
    ostr += "</table>"
    ostr += ', '.join([mbdata.categories.get(x, x) for x in model['catlist']])
    return ostr



def VarMatch(varq, key):
    return (not varq) or (key in varq) 


def CateMatch(catquery, catlist, code, search_not=False):
    modelcode = 1
    for cat in catlist:
	if cat in mbdata.code2_categories:
	    modelcode = 2
    retval = not code or (code == modelcode)
    if retval and catquery:
	retval = (catquery in catlist) or (catquery == 'MB' and not catlist)
	if search_not:
	    retval = not retval
    #print catquery, catlist, code, retval, '<br>'
    return retval


def WheelMatch(wheels, var):
    return (not wheels) or var['wheels'] == wheels or var['text_wheels'] == wheels


def SearchMatch(sobj, var):
    if not sobj:
	return True
    for k in var:
	if k in desc_attributes and useful.SearchMatch(sobj, var[k]):
	    return True
    return False


def DescMatch(attrq, var, ci=False):
    if not attrq:
	return True
    for attr in attrq:
	var_val = var.get(attr, '')
	query_val = ' '.join(attrq.get(attr, []))
	if attr in desc_attributes:
	    for obj in attrq[attr]:
		if not ci and var[attr].find(obj) < 0:
		    return False
		if ci and var[attr].lower().find(obj.lower()) < 0:
		    return False
    return True


def FieldMatch(pif, attrq, var):
    if not attrq:
	return True
    for attr in attrq:
	search_not = pif.FormBool('not_' + attr)
	var_val = var.get(attr, '')
	query_val = ' '.join(attrq.get(attr, []))
	if attr == 'category':
	    continue
#	elif attr in hidden_attributes:
#	    continue
	elif attr in desc_attributes:
#	    for obj in attrq[attr]:
#		if var[attr].find(obj) < 0:
#		    return False
	    continue
#	elif not var.get(attr, ''):
#	    return False
#	elif attrq.get(attr) and (' '.join(attrq[attr]) != var[attr]):
#	    return False
	elif var_val == query_val and search_not:
	    return False
	elif var_val != query_val and not search_not:
	    return False
    return True

# ----- from vars.cgi -------------------------------------

def DoModel(pif, man, variations, display_type):
    #print '<input type="hidden" name="list" value="1">'
    varl = pif.FormStr("v")
    wheelq = pif.FormStr("var.wheels")
    sobj = pif.FormSearch("var.s")
    cateq = pif.FormStr('category', '')
    values = dict()

    mod_id = man['id']
    attributes = {x['attribute_name']: x for x in pif.dbh.DePref('attribute', pif.dbh.FetchAttributes(mod_id))}
    attributes.update({pif.dbh.table_info['variation']['columns'][x]: {'title' : pif.dbh.table_info['variation']['titles'][x]} for x in range(0, len(pif.dbh.table_info['variation']['columns']))})
    attributes['references'] = {'title' : 'References'}
    selects = GetVarSelects(pif, mod_id)

    attrq = dict()
    for attr in attributes:
	if pif.FormStr(attr):
	#if not attr in hidden_attributes and pif.FormHas(attr):
	    attrq[attr] = pif.FormSearch(attr)

    mvars = dict()
    for var in variations:
	mvars[var['var']] = var

    wheels = list()

    if display_type == DISPLAY_TYPE_GRID:
	# a lineup consists of a header (outside of the table) plus a set of sections, each in its own table.
	#     id, name, section, graphics
	# a section consists of a header (inside the table) plus a set of ranges.
	#     id, name, anchor, columns, note, range
	# a range consists of a header plus a set of entries.
	#     id, name, anchor, note, graphics, entry

	llineup = {'id' : 'vars', 'section' : []}
    elif display_type == DISPLAY_TYPE_FULL:
	print pif.render.FormatTableStart()
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, 'ID', hdr=True)
	print pif.render.FormatCell(1, 'Description', hdr=True)
	print pif.render.FormatCell(1, 'Details', hdr=True)
	print pif.render.FormatCell(2, 'Picture', hdr=True)
	print pif.render.FormatCell(3, 'Notes', hdr=True)
	print pif.render.FormatRowEnd()

    keys = mvars.keys()
    keys.sort()
    prev = dict()
    cates = list()
    codes = [1]
    if not pif.FormBool('c1'):
	codes.append(2)
    for code in codes:
	if display_type == DISPLAY_TYPE_GRID:
	    lsec = {'id' : 'code_%d' % code, 'name' : 'Code %d Models' % code, 'columns' : 4, 'range' : [], 'switch' : code != 1}
	    lran = {'id' : 'ran', 'entry' : []}
	elif display_type == DISPLAY_TYPE_FULL:
	    print pif.render.FormatRowStart()
	    print pif.render.FormatCell(0, 'Code %d Models' % code, hdr=True, also={'colspan' : 5})
	    print pif.render.FormatRowEnd()
	count = 0
	for key in keys:
	    model = mvars[key]
	    pif.render.Comment(model)
	    model['references'] = ' '.join(list(set(selects.get(key, []))))
	    category = model['catlist'] = model.get('category', '').split()
	    if not category:
		category = ['MB']
	    for c in category:
		if c not in cates:
		    cates.append(c)
	    if model.get('wheels') not in wheels:
		wheels.append(model.get('wheels'))
	    if model.get('text_wheels') not in wheels:
		wheels.append(model.get('text_wheels'))
	    values = UpdateValues(model, values)
	    if VarMatch(varl, key) and \
			CateMatch(cateq, category, code, pif.FormBool('not_category')) and \
			SearchMatch(sobj, model) and \
			WheelMatch(wheelq, model) and \
			DescMatch(attrq, model, pif.FormBool('ci')) and \
			FieldMatch(pif, attrq, model):
		count += 1
		model['area'] = ', '.join([mbdata.regions.get(x, x) for x in model.get('area', '').split(';')])
		if display_type == DISPLAY_TYPE_GRID:
		    ostr = DoVarGrid(pif, model)
		    lran['entry'].append({'text' : ostr})
		elif display_type == DISPLAY_TYPE_FULL:
		    print DoVar(pif, model, None, model.keys(), {x: x for x in model}, attributes, prev)
		prev = model

	if display_type == DISPLAY_TYPE_GRID and count:
	    while len(lran['entry']) < 4:
		lran['entry'].append({'text' : '', 'class' : 'blank'})
	    lsec['range'].append(lran)
	    if count > 1:
		lsec['count'] = '%d entries' % count
	    else:
		lsec['count'] = '1 entry'
	    llineup['section'].append(lsec)

    if display_type == DISPLAY_TYPE_GRID:
	print pif.render.FormatLineup(llineup)
    elif display_type == DISPLAY_TYPE_FULL:
	print pif.render.FormatTableEnd()
    return values


def GetVarSelects(pif, mod_id):
    var_selects = pif.dbh.DePref('variation_select', pif.dbh.FetchVariationSelects(mod_id))
    selects = dict()
    for var_sel in var_selects:
	selects.setdefault(var_sel['var_id'], [])
	if var_sel['sub_id']:
	    selects[var_sel['var_id']].append(var_sel['ref_id'] + '/' + var_sel['sub_id'])
	else:
	    selects[var_sel['var_id']].append(var_sel['ref_id'])
    return selects


def UpdateValues(var, values):
    for key in var:
	if key in desc_attributes:
	#if key in hidden_attributes or key in desc_attributes:
	    continue
	values.setdefault(key, [])
	newvalue = var[key]
	if not newvalue:
	    newvalue = ''
	if not newvalue in values[key]:
	    values[key].append(newvalue)
    return values


def SaveModel(pif, id):
    for key in pif.FormKeys(start='picture_id.'):
	if key[11:] == pif.FormStr(key):
	    pif.dbh.UpdateVariation({'picture_id': pif.FormStr(key)}, {'mod_id' : id, 'var' : ''})
	else:
	    pif.dbh.UpdateVariation({'picture_id': pif.FormStr(key)}, {'mod_id' : id, 'var' : key[11:]})
    for key in pif.FormKeys(start='var_sel.'):
	varsel = list(set(pif.FormStr(key).split()))
	#pif.dbh.Delete('variation_select', where="mod_id='%s'" % id)
	#print 'varsel', varsel, '<br>'
	pif.dbh.UpdateVariationSelects(id, key[8:], varsel)


def ShowModel(pif, model):
    id = model['id']
    if pif.FormHas('recalc'):
	RecalcDescription(pif, id)
    model = pif.dbh.FetchCasting(id)
    #pif.render.title = model['id'] + ': ' + model['name']
    print pif.render.FormatHead(extra=pif.render.reset_button_js + pif.render.increment_select_js + pif.render.toggle_display_js)
    #print model, '<br>'
    if not model:
	print "<h2>That is not a recognized model ID.</h2>"
	return

    varl = pif.FormStr("v", '')
    cateq = pif.FormStr("var.cate")
    wheelq = pif.FormStr("var.wheels")
    attributes = {x['attribute_name']: x for x in pif.dbh.DePref('attribute', pif.dbh.FetchAttributes(model['id']))}
    attributes.update({pif.dbh.table_info['variation']['columns'][x]: {'title' : pif.dbh.table_info['variation']['titles'][x]} for x in range(0, len(pif.dbh.table_info['variation']['columns']))})
    attributes['references'] = {'title' : 'References'}
    attrq = dict()
    for attr in attributes:
	if pif.FormHas(attr):
	#if not attr in hidden_attributes and pif.FormHas(attr):
	    attrq[attr] = pif.FormSearch(attr)
    cates = ['MB']
    variations = pif.dbh.DePref('variation', pif.dbh.FetchVariations(model['id']))
    for variation in variations:
	for c in variation.get('category', '').split():
	    if c not in cates:
		cates.append(c)

    print '<table width=100%><tr><td class="title">' + pif.render.title + '</td></tr></table><p>'
    #print '<h2>' + model['name'] + '</h2>'
    #print '<h3>%s</h3>' % '-'.join(ParseModel(model['id'])).upper()
    print '<center>'
    print pif.render.FormatImageRequired([x + model['id'].lower() for x in ['m_', 's_']], pdir=config.imgdir175)
    print '</center><br>'
    if varl:
	print 'Selected models'
    else:
	print 'All models'
    if cateq:
	print 'in', mbdata.categories.get(cateq, cateq)
    if wheelq:
	print 'with', wheelq, "wheels"
    if attrq:
	print 'matching search'

    print '<form action="vars.cgi" name="vars" method="post">'
    if pif.FormBool('verbose'):
	print '<input type="hidden" name="verbose" value="1">'

    values = DoModel(pif, model, variations, {True:DISPLAY_TYPE_FULL, False:DISPLAY_TYPE_GRID}[pif.FormHas('list')])

    print '<p style="font-weight: bold; font-size: large;">'
    print pif.render.FormatButtonInputVisibility("varsearch", True)
    print 'Search Variations</p>'
    print '<div id="varsearch"><input type="hidden" name="page" value="%s">' % pif.page_id
    print '<input type="hidden" name="mod" value="%s">' % model['id']

    values['category'] = cates

    SearchForm(pif, attributes, values)
    print '</div><hr>'
    if pif.IsAllowed('a'): # pragma: no cover
	print pif.render.FormatButtonInput('save')
	print pif.render.FormatButton("add", 'vars.cgi?edit=1&mod=%s&add=1' % model['id'])
	print pif.render.FormatButton("casting", pif.dbh.GetEditorLink('casting', {'id' : model['id']}))
	print pif.render.FormatButton("recalc", '?recalc=1&mod=%s' % model['id'])
    if pif.IsAllowed('u'): # pragma: no cover
	print pif.render.FormatButton("upload", 'upload.cgi?d=' + os.path.join(config.libmandir, model['id'].lower()) + '&m=' + model['id'])
	print pif.render.FormatButton("pictures", 'traverse.cgi?d=%s' % os.path.join(config.libmandir, model['id'].lower()))
    #print pif.render.FormatButton("comment_on_this_page", link='../pages/comment.php?page=%s&man=%s&var=%s' % (pif.page_id, model['id'], varl), also={'class' : 'comment'}, lalso={})
    print pif.render.FormatButtonComment(pif, 'man=%s&var=%s' % (model['id'], varl))
    print '</form>'
    print '<hr>'

#{'body': 'dark green', 'submit': ('11', '16'), 'submit.x': '11', 'submit.y': '16', 'page': 'search', 'mod': 'SF34b'} 
#{'body': 'dark green', 'list': ('16', '10'), 'page': 'vars', 'list.x': '16', 'list.y': '10', 'mod': 'SF34b'}


@basics.WebPage
def Main(pif):
    id = pif.FormStr('mod')
    var = pif.FormStr('var')

    pif.render.hierarchy.append(('/', 'Home'))
    pif.render.hierarchy.append(('/database.php', 'Database'))
    pif.render.hierarchy.append(('/cgi-bin/single.cgi', 'By ID'))
    pif.render.hierarchy.append(('/cgi-bin/single.cgi?id=%s' % id, id))
    pif.render.hierarchy.append(('/cgi-bin/vars.cgi?mod=%s' % id, 'Variations'))
    pif.render.PrintHtml()

    regs = mbdata.GetCountries()
    regs.update(mbdata.regions)
    man = dict()
    if id:
	man = pif.dbh.FetchCasting(id)
	if not man:
	    man = pif.dbh.FetchCastingByAlias(id)
    if not man:
	id = var = ''
    elif var:
	pif.render.title = '%(casting_type)s %(id)s: %(name)s' % man
	pif.render.title += ' - Variation ' + var
    elif id:
	pif.render.title = '%(casting_type)s %(id)s: %(name)s' % man
	pif.render.title += ' - Variations'
    else:
	pass

    #print pif.render.FormatHead(extra=pif.render.reset_button_js + pif.render.increment_select_js)
    if pif.FormHas("add"):
	AddVariation(pif, id, 'unset', {'imported_from': 'web'})
	ShowVariationEditor(pif, id, 'unset')
    elif pif.FormHas('edit'):
	ShowVariationEditor(pif, id, pif.FormStr('var'))
    elif pif.FormHas("rmpic"):
	RemovePicture(pif, id, var)
	ShowVariation(pif, man, var)
    elif pif.FormHas("promote"):
	PromotePicture(pif, id, var)
	ShowVariation(pif, man, var)
    elif pif.FormHas("delete"):
	DeleteVariation(pif, id, var)
	ShowModel(pif, man)
    elif pif.FormHas("save"):
	Save(pif, id, var)
    elif var:
	ShowVariation(pif, man, var)
    elif id:
	ShowModel(pif, man)
    else:
	print "What?"
    print pif.render.FormatTail( )

# ----- from mkdesc.py ------------------------------------

# *attr = value attr
# &attr = value
# @attr = value -or- no attr
# +append = postpended append
# ^append = prepended append
# #default
attr_re = re.compile(r'%\((?P<a>[^)]*)\)s')
def FmtDetail(var, fmt, verbose):
    is_opt = False
    attr_name = fmt_append = alt = ''
    default = ''
    if fmt.startswith('?'):
	is_opt = True
	fmt = fmt[1:]
    if fmt.find('#') >= 0:
	default = fmt[fmt.find('#') + 1:]
	fmt = fmt[:fmt.find('#')]
    if fmt.find('+') >= 0:
	# YES I'M FORCING THE SPACE.
	fmt_append = ' ' + fmt[fmt.find('+') + 1:]
	fmt = fmt[:fmt.find('+')]
    if fmt.startswith('*'):
	attr_name = fmt[1:]
	fmt = '%%(%s)s %s%s' % (attr_name, attr_name.replace('_', ' '), fmt_append)
    elif fmt.startswith('@'): # & unless the detail is "no", then *.
	attr_name = fmt[1:]
	alt = 'no ' + attr_name.replace('_', ' ')
	is_opt = True
	fmt = '%%(%s)s%s' % (attr_name, fmt_append)
    elif fmt.startswith('&'):
	attr_name = fmt[1:]
	fmt = '%%(%s)s%s' % (attr_name, fmt_append)
    elif fmt.startswith('^'):
	attr_name = fmt[1:]
	fmt = '%s %%(%s)s' % (fmt_append, attr_name)
    else:
	# MI818 still needs this, at the least.
	attr_m = attr_re.search(fmt)
	if attr_m:
	    attr_name = attr_m.group('a')
    if not attr_name in var:
	if verbose:
	    print '!', attr_name
	return ''
    attr = var.get(attr_name)
    if not attr:
	return default
    if is_opt and (attr == 'no' or attr == '-'):
	return alt

    return fmt.strip()


# Sometimes this causes duplicate output.  It would be nice to merge those.
'''
def Fmt(var, casting, ovar, field, verbose):
    ovar['text_' + field] = ''
    fmt = ', '.join(filter(None, [FmtDetail(var, x, verbose) for x in casting['format_' + field].split('|')]))
    try:
	ovar['text_' + field] = fmt % var
    except:
	if verbose:
	    print '!', field
'''

def FmtDesc(var, casting, field, verbose):
    fmt = ', '.join(filter(None, [FmtDetail(var, x, verbose) for x in casting[field].split('|')]))
    desc = ''
    try:
	desc = fmt % var
    except:
	if verbose:
	    print '!', field
    return desc


cols = ['description', 'body', 'base', 'wheels', 'interior', 'windows']
def RecalcDescription(pif, mod_id, verbose=False):
    textcols = ['text_' + x for x in cols]
    casting = pif.dbh.FetchCasting(mod_id)
    vars = pif.dbh.DePref('variation', pif.dbh.FetchVariations(mod_id))
    for var in vars:
	if verbose:
	    print var['var']
	ovar = {x: '' for x in textcols}
	ovar.update({'text_' + x: FmtDesc(var, casting, 'format_' + x, verbose) for x in cols})
	pif.dbh.UpdateVariation(ovar, {'mod_id' : var['mod_id'], 'var' : var['var']})


cas_cols = ['format_' + x for x in cols]
var_cols = ['base', 'body', 'interior', 'windows', 'manufacture']
def CheckFormatting(pif, mod_id, verbose=False, linesep=''):
    casting = pif.dbh.FetchCasting(mod_id)
    attributes = var_cols + [x['attribute.attribute_name'] for x in pif.dbh.FetchAttributes(mod_id)]
    for attr in attributes:
	if attr == 'from_CY_number':
	    continue
	found = False
	attr_re = re.compile(r'\b%s\b' % attr)
	for col in cas_cols:
	    attr_m = attr_re.search(casting[col])
	    if attr_m:
		found = True
		if verbose:
		    print mod_id, '+', attr, linesep
		break
	if not found:
	    if verbose:
		print mod_id, '-', attr, linesep
	    else:
		return True
    return False


# ----- msearch -------------------------------------------

# {'v.text_base': 'unpainted, front to rear, E', 'v.text_wheels': 'dot dash 9x3.5mm silver', 'v.mod_id': 'MI803', 'v.picture_id': '', 'casting.rawname': 'Mercedes-Benz;"Binz" Ambulance', 'v.var': '08a', 'v.text_interior': 'light yellow, no stretcher', 'v.text_windows': 'dark blue', 'v.text_description': 'olive green, shut tailgate, wide wheel wells, unpainted bumpers and grille', 'casting.id': 'MI803', 'v.text_body': 'olive green, shut tailgate, wide wheel wells, unpainted bumpers and grille'}

def AddModelVarTablePicLink(pif, mdict):
    if mdict.get('v.picture_id'):
	mdict['img'] = pif.render.FormatImageRequired(mdict['v.mod_id'], prefix='s_', nobase=True, vars=mdict['v.picture_id'])
    else:
	mdict['img'] = pif.render.FormatImageRequired(mdict['v.mod_id'], prefix='s_', nobase=True, vars=mdict['v.var'])
    #mdict['link'] = 'single.cgi?id=%(v.mod_id)s' % mdict
    mdict['link'] = 'vars.cgi?mod=%(v.mod_id)s&var=%(v.var)s' % mdict
    ostr = '  <table class="entry"><tr><td><center><font face="Courier">%(v.mod_id)s-%(v.var)s</font></br>\n' % mdict
    ostr += '   <a href="%(link)s">%(img)s<br><b>%(casting.name)s</b></a>\n' % mdict
    #ostr += "   <br><i>%(v.text_description)s</i>\n" % mdict
    ostr += '<table class="vartable">'
    ostr += '<tr><td class="varentry"><i>%s</i></td></tr>' % mdict['v.text_description']
    ostr += "</table>"
    ostr += "  </center></td></tr></table>\n"
    return ostr


vfields = {'base' : 'text_base', 'body' : 'text_body', 'interior': 'text_interior', 'wheels' : 'text_wheels', 'windows' : 'text_windows', 'cat' : 'category'}
cfields = {'casting' : 'rawname'}


@basics.WebPage
def RunSearch(pif):
    if pif.FormHas('ask'):
	VarSearchAsk(pif)
    else:
	VarSearch(pif)


def VarSearchAsk(pif):
    pif.render.Comment('VarSearchAsk')
    pif.render.PrintHtml()
    id = pif.FormStr('id')
    model = pif.dbh.FetchCasting(id)

    #pif.render.title = model['id'] + ': ' + model['name']
    print pif.render.FormatHead(extra=pif.render.reset_button_js + pif.render.increment_select_js + pif.render.toggle_display_js)
    #print model, '<br>'
    if not model:
	print "<h2>That is not a recognized model ID.</h2>"
	return

    varl = pif.FormStr("v")
    cateq = pif.FormStr("var.cate")
    wheelq = pif.FormStr("var.wheels")
    attributes = {x['attribute_name']: x for x in pif.dbh.DePref('attribute', pif.dbh.FetchAttributes(model['id']))}
    attributes.update({pif.dbh.table_info['variation']['columns'][x]: {'title' : pif.dbh.table_info['variation']['titles'][x]} for x in range(0, len(pif.dbh.table_info['variation']['columns']))})
    attributes['references'] = {'title' : 'References'}
    attrq = dict()
    for attr in attributes:
	if pif.FormHas(attr):
	#if not attr in hidden_attributes and pif.FormHas(attr):
	    attrq[attr] = pif.FormSearch(attr)
    cates = ['MB']
    variations = pif.dbh.DePref('variation', pif.dbh.FetchVariations(model['id']))
    for variation in variations:
	for c in variation.get('category', '').split():
	    if c not in cates:
		cates.append(c)

    print '<form action="vars.cgi" name="vars" method="post">'
    if pif.FormBool('verbose'):
	print '<input type="hidden" name="verbose" value="1">'

    values = DoModel(pif, model, variations, DISPLAY_TYPE_NONE)

    #print '<input type="hidden" name="list" value="1">'
    print '<input type="hidden" name="page" value="vars">'
    print '<input type="hidden" name="mod" value="%s">' % model['id']

    values['category'] = cates

    SearchForm(pif, attributes, values)
    print '<hr>'
    if pif.IsAllowed('a'): # pragma: no cover
	print pif.render.FormatButtonInput("list")
    print pif.render.FormatButtonComment(pif, 'man=%s&var=%s' % (model['id'], varl))
    print '</form>'
    print '<hr>'


def GetCodes(pif):
    codes = 0
    for code in pif.FormList('codes'):
	if code not in "12":
	    return None
	codes += int(code)
    return codes


def VarSearch(pif):
    pif.render.hierarchy.append(('/', 'Home'))
    pif.render.hierarchy.append(('/database.php', 'Database'))
    pif.render.hierarchy.append((pif.request_uri, 'Variation Search'))
    pif.render.PrintHtml()
    pif.render.title = 'Models matching: ' + ' '.join(pif.FormSearch('query'))
    print pif.render.FormatHead()
    modsperpage = 100
    varsq = {vfields[x]: pif.FormSearch(x) for x in vfields}
    castq = {cfields[x]: pif.FormSearch(x) for x in cfields}
    codes = GetCodes(pif)
    if codes == None:
	print "This submission was not created by the form provided.<p>"
	print "Please stop being a dick."
	print pif.render.FormatTail()
	return
    pif.render.Comment('varsq', varsq, 'castq', castq, 'codes', codes)
    mods = pif.dbh.FetchVariationQuery(varsq, castq, codes)
    mods.sort(key=lambda x: x['v.mod_id'] + '-' + x['v.var'])
    nmods = len(mods)

    llineup = {'name' : '%d variations found matching search' % nmods, 'columns' : 4, 'tail' : ''}
    start = pif.FormInt('start')
    mods = mods[start:start + modsperpage]
    lsec = pif.dbh.FetchSections({'page_id' : pif.page_id})[0]
    lran = {'entry' : []}
    for mod in mods:
	mod['casting.name'] = mod['base_id.rawname'].replace(';', ' ')
	lran['entry'].append({'text' : AddModelVarTablePicLink(pif, mod)})
    lsec['range'] = [lran]
    llineup['section'] = [lsec]
    qf = pif.FormReformat(vfields) + '&' + pif.FormReformat(cfields)
    if pif.render.verbose:
	qf += '&verbose=1'
    qf += '&codes=%s' % codes
    if start > 0:
	llineup['tail'] += pif.render.FormatButton("previous", 'vsearch.cgi?%s&start=%d' % (qf, max(start - modsperpage, 0))) + ' '
    if start + modsperpage < nmods:
	llineup['tail'] += pif.render.FormatButton("next", 'vsearch.cgi?%s&start=%d' % (qf, min(start + modsperpage, nmods)))
    
    print pif.render.FormatLineup(llineup)
    print pif.render.FormatButtonComment(pif, 'casting=%s&base=%s&body=%s&interior=%s&wheels=%s&windows=%s' % (pif.FormStr('casting'), pif.FormStr('base'), pif.FormStr('body'), pif.FormStr('interior'), pif.FormStr('wheels'), pif.FormStr('windows')))
    print pif.render.FormatTail()


@basics.CommandLine
def Commands(pif):
    if pif.filelist and pif.filelist[0] == 'd':
	DeleteVariation(pif, pif.filelist[1], pif.filelist[2])
    elif pif.filelist and pif.filelist[0] == 'r':
	RenameVariation(pif, pif.filelist[1], pif.filelist[2], pif.filelist[3])
    elif pif.filelist and pif.filelist[0] == 's':
	RenameVariation(pif, pif.filelist[1], pif.filelist[2], pif.filelist[2] + 'x')
	RenameVariation(pif, pif.filelist[1], pif.filelist[3], pif.filelist[2])
	RenameVariation(pif, pif.filelist[1], pif.filelist[2] + 'x', pif.filelist[3])
    elif pif.filelist and pif.filelist[0] == 'm':
	print "move not yet implemented"
    else:
	print "./vars.py [d|r|s|m] ..."
	print "  d for delete: mod_id var_id"
	print "  r for rename: mod_id old_var_id new_var_id"
	print "  s for swap: mod_id var_id_1 var_id_2"
	print "  m for move: old_mod_id old_var_id new_mod_id [new_var_id]"


if __name__ == '__main__': # pragma: no cover
    Commands('vars', dbedit='')
