#!/usr/local/bin/python

import copy, glob, os, re, sys

import basics
import config
import imglib
import mbdata
import models
import single
import useful


id_attributes = ['mod_id', 'var', 'picture_id', 'imported_var', 'imported_from', 'references', '_repic', '_credit']
note_attributes = ['manufacture', 'area', 'category', 'date', 'note']
internal_desc_attributes = ['description', 'base', 'body', 'interior', 'windows']
desc_attributes = ['description', 'base', 'body', 'interior', 'wheels', 'windows', 'with']
text_attributes = ['text_' + x for x in desc_attributes]
format_attributes = ['format_' + x for x in desc_attributes]
hidden_attributes = id_attributes + ['imported', 'flags']
detail_attributes = ['base', 'base_text', 'body', 'interior', 'windows']

list_columns = ['ID', 'Description', 'Details', 'Picture', 'Notes']
detail_columns = ['ID', 'Description', 'Ty', 'Cat', 'Cr', 'Pic', 'L', 'M', 'S', 'T', 'Ba', 'Bo', 'In', 'Wh', 'Wi', 'W/']

fieldwidth_re = re.compile(r'\w+\((?P<w>\d+)\)')

# ----- display single variation --------------------------

def show_variation_editor(pif, man, var_id, edit=False, addnew=False):
    edit = edit and pif.is_allowed('a')
    if not man:
        raise useful.SimpleError("That casting was not found.")
    mod_id = man['id']

    varrecs, detrecs = pif.dbh.fetch_variation_deconstructed(mod_id, var_id, nodefaults=False)
    if varrecs:
	variation = pif.dbh.depref('variation', varrecs[0])
	for attr, det in detrecs.get(var_id, {}).items():
	    if not variation.get(attr):
		variation[attr] = det
    elif addnew:
	variation = {x: '' for x in pif.dbh.table_info['variation']['columns']}
	variation['var'] = var_id
	variation['mod_id'] = mod_id
    else:
        raise useful.SimpleError("That variation was not found.")
    attr_pics = {x['attribute.attribute_name']: x for x in pif.dbh.depref('attribute_picture', pif.dbh.fetch_attribute_pictures(mod_id))}
    for attr in pif.dbh.fetch_attributes(mod_id):
	variation.setdefault(attr['attribute.attribute_name'], '')
    vsform = VarSearchForm(pif, mod_id)
    pdir = pif.render.pic_dir

    left_bar_content = ''
    if pif.is_allowed('a'):  # pragma: no cover
        #left_bar_content += pif.render.format_link('vars.cgi?mod=%s&var=%s&delete=1' % (mod_id, var_id), "Delete") + '<br>'
	if edit:
	    left_bar_content += pif.render.format_link('vars.cgi?mod=%s&var=%s' % (mod_id, var_id), "See") + '<br>'
	else:
	    left_bar_content += pif.render.format_link('vars.cgi?mod=%s&var=%s&edit=1' % (mod_id, var_id), "Edit") + '<br>'
	left_bar_content += pif.render.format_link('upload.cgi?d=%s&m=%s&v=%s&l=1&c=%s+variation+%s' % (useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower()), mod_id, var_id, mod_id, var_id), 'Pictures') + '<br>'
        #left_bar_content += pif.render.format_link('?mod=%s&var=%s&rmpic=1' % (mod_id, var_id), "Remove Pictures") + '<br>'
        left_bar_content += pif.render.format_link(pif.dbh.get_editor_link('casting', {'id': mod_id}), "Casting") + '<br>'
        left_bar_content += pif.render.format_link('?recalc=1&mod=%s' % mod_id, "Recalc") + '<br>'
        left_bar_content += pif.render.format_link('traverse.cgi?g=1&d=%s&man=%s&var=%s' % (useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower()), mod_id, var_id), "Select") + '<br>'
    if pif.is_allowed('u'):  # pragma: no cover
        left_bar_content += pif.render.format_link('upload.cgi?d=' + useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower()), "Upload") + '<br>'

    footer = ''
    if edit:
	footer += pif.render.format_button_input('save')
	footer += pif.render.format_button_reset('vars')
	footer += pif.render.format_button("delete", 'vars.cgi?mod=%s&var=%s&delete=1' % (mod_id, var_id))
	footer += pif.render.format_button("remove_picture", 'vars.cgi?mod=%s&var=%s&rmpic=1' % (mod_id, var_id))
	footer += pif.render.format_button("promote", 'editor.cgi?mod=%s&var=%s&promote=1' % (mod_id, var_id))

    #photogs = [('', '')] + [(x.photographer.id, x.photographer.name) for x in pif.dbh.fetch_photographers()]
    photogs = [(x.photographer.id, x.photographer.name) for x in pif.dbh.fetch_photographers(pif.dbh.FLAG_ITEM_HIDDEN)]
    pic_var = variation['picture_id'] if variation['picture_id'] else variation['var']
    img = ''.join([
        pif.render.format_image_required(mod_id, pdir=pdir, vars=pic_var, nobase=True, prefix=s)
	for s in [mbdata.IMG_SIZ_TINY, mbdata.IMG_SIZ_SMALL, mbdata.IMG_SIZ_MEDIUM, mbdata.IMG_SIZ_LARGE]
    ]) if edit else pif.render.format_image_required(mod_id, pdir=pdir, vars=pic_var, nobase=True, largest=mbdata.IMG_SIZ_HUGE)
    var_img_credit = pif.dbh.fetch_photo_credit('.' + config.IMG_DIR_VAR, mod_id, pic_var, verbose=True)
    variation['_credit'] = var_img_credit['photographer.id'] if var_img_credit else ''
    var_img_credit = var_img_credit['photographer.name'] if var_img_credit else ''

    variation['references'] = ' '.join(list(set(vsform.selects.get(var_id, []))))
    variation['area'] = ', '.join([mbdata.get_countries().get(x, mbdata.areas.get(x, x)) for x in variation.get('area', '').split(';')])
    data = sorted(variation.keys() + [d for d in vsform.attributes if d not in variation])

    lsec = {'columns': ['title', 'value'], 'id': 'single'}
    if edit:
	lsec['headers'] = {'title': 'Title', 'value': 'Value', 'field': 'Field', 'new': 'New'}
	lsec['columns'] = ['field', 'title', 'value', 'new']
	ranges = [{'name': 'Identification Attributes', 'id': 'det', '_attrs': id_attributes}]
    else:
	lsec['headers'] = {'title': 'Title', 'value': 'Value'}
	lsec['columns'] = ['title', 'value']
	ranges = [{'name': 'Description Texts', 'id': 'det', '_attrs': text_attributes[1:]}]
    ranges.extend([
	    {'name': 'Individual Attributes', 'id': 'det',
	     '_attrs': [d for d in data if not (d in text_attributes or d in note_attributes or d in hidden_attributes)]},
	    {'name': 'Notes', 'id': 'det', '_attrs': note_attributes},
	])
    for lran in ranges:
	lran['entry'] = show_details(pif, lran['_attrs'], vsform.attributes, variation, attr_pics, ran_id=lran['id'], photogs=photogs)
    lsec['range'] = ranges
    llistix = {'id': 'single', 'section': [lsec]}

    appearances = show_appearances(pif, mod_id, var_id, pics=True)
    adds = models.show_adds(pif, mod_id, var_id)
    upload = 'upload.cgi?m=%s&v=%s' % (mod_id, var_id) + (
	'&d=%s' % useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower())
	if pif.is_allowed('u') else '')

    # ------- render ------------------------------------

    pif.render.set_page_extra(pif.render.reset_button_js + pif.render.increment_select_js + pif.render.modal_js)
    pif.render.set_button_comment(pif, 'man=%s&var_id=%s' % (mod_id, var_id))
    context = {
	'title': pif.render.title,
	'note': '',
	'type_id': '',
	'base_id': man['id'],
	'icon_id': mod_id if os.path.exists(useful.relpath('.', config.IMG_DIR_ICON, 'i_' + mod_id.lower() + '.gif')) else '',
	'vehicle_type': [mbdata.model_icons.get(x) for x in man['vehicle_type']],
	'rowspan': '4',
	'left_bar_content': left_bar_content,
	'description': variation['text_description'],
	'image': img,
	'credit': var_img_credit,
	'llistix': llistix,
	'appearances': appearances,
	'adds': adds,
	'upload': upload,
	'edit': edit,
	'addnew': addnew,
	'variation': variation,
	'footer': footer,
    }
    return pif.render.format_template('var.html', **context)


def show_appearances(pif, mod_id, var_id, pics=False):
    varsel = pif.dbh.fetch_variation_selects(mod_id, var_id)
    ostr = ''
    if varsel:
        ostr += "<b>Appearances</b>\n<ul>\n"
        for vs in varsel:
            if vs['variation_select.ref_id'].startswith('matrix.'):
                if vs['variation_select.sub_id']:
                    ostr += '<li>' + pif.render.format_link("matrix.cgi?page=%s#%s" % (vs['variation_select.ref_id'], vs['variation_select.sub_id']), vs['page_info.title']) + '\n'
                else:
                    ostr += '<li>' + pif.render.format_link("matrix.cgi?page=%s" % vs['variation_select.ref_id'], vs['page_info.title']) + '\n'
            elif vs['variation_select.ref_id'].startswith('packs.'):
		# bugly.  for 2packs, this doesn't work so we have to work around it.
		if not vs['pack.id']:
		    pack_id, pack_var = vs['variation_select.sub_id'].split('-') if '-' in vs['variation_select.sub_id'] else (vs['variation_select.sub_id'], '')
		    pack = pif.dbh.fetch_pack(pack_id, pack_var)
		    if pack:
			vs.update(pack[0])
		ostr += '<li>' + pif.render.format_link("packs.cgi?page=%s&id=%s" % (vs['pack.page_id'], vs['pack.id']),
		    "%(page_info.title)s: %(base_id.rawname)s (%(base_id.first_year)s)" % vs) + '\n'
            elif vs['variation_select.ref_id'].startswith('year.') and vs['lineup_model.region']:
                #lineup.cgi?year=2001&region=U#71
                vs['region'] = mbdata.regions.get(vs['lineup_model.region'], 'Worldwide')
                if not vs.get('lineup_model.region'):
                    vs['lineup_model.region'] = 'W'
                if vs.get('lineup_model.region', '').startswith('X'):
                    vs['region'] = 'Worldwide'
                    vs['lineup_model.number'] = 'S' + vs['lineup_model.region'].replace('.', '')
                    vs['lineup_model.region'] = 'U'
                    ostr += '<li>' + pif.render.format_link("lineup.cgi?year=%(lineup_model.year)s&region=%(lineup_model.region)s&lty=all#%(lineup_model.number)s" % vs, "%(lineup_model.year)s %(region)s lineup" % vs) + '\n'
                elif vs.get('lineup_model.region') in ['M', 'S']:
                    pass
                elif not vs['variation_select.sub_id'] or vs['variation_select.sub_id'] == vs.get('lineup_model.region'):
                    ostr += '<li>' + pif.render.format_link("lineup.cgi?year=%(lineup_model.year)s&region=%(lineup_model.region)s&lty=all#%(lineup_model.number)s" % vs, "%(lineup_model.year)s %(region)s lineup number %(lineup_model.number)s" % vs) + '\n'
            elif pif.is_allowed('a'):  # pragma: no cover
                ostr += '<li><i>ref_id = ' + str(vs['variation_select.ref_id'])
                if vs['variation_select.sub_id']:
                    ostr += ' / sub_id = ' + str(vs['variation_select.sub_id'])
                ostr += " (vs = %s)</i>\n" % str(vs)
        ostr += "</ul>\n"
    return ostr

# ----- variation editor ----------------------------------

def show_detail(pif, field, attributes, variation, attr_pics={}, ran_id='', photogs=[]):
    if field.startswith('variation.'):  # not sure where this is coming from.
	field = field[10:]
    if field == '_repic':
	return {'field': '', 'title': 'Move pictures to', 'value': '',
		'new': pif.render.format_text_input("repic." + variation['var'], 16, 16)}
    if field == '_credit':
	return {'field': '', 'title': 'Credit', 'value': '',
		'new': pif.render.format_select("phcred." + variation['var'], photogs, selected=variation.get('_credit', ''), blank='')}
    title = attributes[field]['title']
    value = variation.get(field, '')
    if field == 'category':
	value = ', '.join([mbdata.categories.get(x, x) for x in value.split()])
    modals = ''
    title_modal = show_detail_modal(pif, attr_pics.get(field, {}), variation['mod_id'])
    if title_modal:
	title += ''' <i onclick="init_modal('m.%s');" class="modalbutton fa fa-question-circle-o"></i>\n''' % field
	title += pif.render.format_modal('m.' + field, title_modal)
    value_modal = show_detail_modal(pif, attr_pics.get(field, {}), variation['mod_id'], variation['var'])
    if value_modal:
	value += ''' <i onclick="init_modal('v.%s');" class="modalbutton fa fa-question-circle-o"></i>\n''' % field
	value += pif.render.format_modal('v.' + field, value_modal)
    return {
	'field': field,
	'title': title,
	'value': value,
	'new': pif.render.format_text_input(field + "." + variation['var'],
	    int(fieldwidth_re.search(attributes[field]['definition']).group('w')) \
		if '(' in attributes[field]['definition'] else 20,
	    64, value=variation.get(field, '')),
    }


def show_detail_modal(pif, attr_pic, mod_id, var_id=''):
    adds = {
        "b_": "Baseplate%(s)s",
        "d_": "Detail%(s)s",
        "i_": "Interior%(s)s",
    }

    if not attr_pic:
	return ''
    add = adds.get(attr_pic['attr_type'] + '_')
    if not add:
	return ''
    img_id = (mod_id + ('-' + var_id if var_id else '')).lower() + ('-' + attr_pic['picture_id'] if attr_pic['picture_id'] else '')
    pdir = config.IMG_DIR_VAR if var_id else config.IMG_DIR_ADD
    var_img_credit = pif.dbh.fetch_photo_credit(pdir, img_id, verbose=True)
    var_img_credit = var_img_credit['photographer.name'] if var_img_credit else ''

    img = pif.render.find_image_path(img_id, prefix=attr_pic['attr_type'], pdir=pdir)
    caption = ''
    if attr_pic['description']:
	caption = attr_pic['description']
	if attr_pic['attribute.title']:
	    caption = attr_pic['attribute.title'] + ': ' + caption
    return show_var_image(pif, attr_pic, img, add % {'s': ''}, caption, var_img_credit)


def show_var_image(pif, attr_pic, img, title, caption='', var_img_credit=''):
    ostr = ''
    if img:
	ostr += '<center><h3>%s</h3>\n' % title
	ostr += '<table><tr><td>' + pif.render.fmt_img_src(img) + '<br>'
	if var_img_credit:
	    ostr += '<div class="credit">Photo credit: %s</div>' % var_img_credit
	ostr += '</td></tr></table>'
	if attr_pic['description']:
	    if attr_pic['attribute.title']:
		ostr += attr_pic['attribute.title'] + ': '
	    ostr += attr_pic['description']
	ostr += '<p></center>\n'
    return ostr



def show_details(pif, data, attributes, variation, attr_pics={}, ran_id='', photogs=[]):
    return [show_detail(pif, d, attributes, variation, attr_pics, ran_id=ran_id, photogs=photogs) for d in data if d in variation or d.startswith('_')]


def save(pif, mod_id, var_id):
    # pif.form.get_bool('addnew')
    if var_id:
	country_codes = mbdata.get_country_codes()
        phcred = var_sel = repic = ''
        attributes = {x['attribute_name']: x for x in pif.dbh.depref('attribute', pif.dbh.fetch_attributes(mod_id))}
        #attributes.update({pif.dbh.table_info['variation']['columns'][x]: {'title': pif.dbh.table_info['variation']['titles'][x]} for x in range(0, len(pif.dbh.table_info['variation']['columns']))})
        pif.render.comment("Save: ", attributes)
        var_dict = {'mod_id': pif.form.get_str('mod'), 'picture_id': ''}
        det_dict = dict()
        for attr in note_attributes + detail_attributes:
        #    if 'id' in attributes.get(attr, {}):
        #        det_dict[attr] = pif.form.get_str(attr + '.' + var_id)
        #    else:
                var_dict[attr] = pif.form.get_str(attr + '.' + var_id)
        for key in pif.form.keys(end='.' + var_id):
            attr = key[:key.rfind('.')]
            if attr == 'references':
                var_sel = pif.form.get_str(key)  # make it work!
	    elif attr == 'phcred':
		phcred = pif.form.get_str(key)
		pif.render.message('read phcred', key, phcred, '<br>')
            elif attr == 'repic':
                repic = pif.form.get_str(key)
                pif.render.message('repic', repic, '<br>')
            elif attr == 'picture_id':
                if pif.form.get_str(key) != var_id:
                    var_dict[attr] = pif.form.get_str(key)
	    elif attr == 'area':
		var_dict[attr] = ';'.join([country_codes.get(x, x) for x in pif.form.get_str(key).split(',')])
            elif attr in note_attributes + internal_desc_attributes + hidden_attributes + detail_attributes:
                var_dict[attr] = pif.form.get_str(key)
            else:
                det_dict[attr] = pif.form.get_str(key)
        pif.render.message('var_dict', var_dict)
        pif.render.message('det_dict', det_dict)
        if var_id != var_dict['var']:
            rename_variation(pif, var_dict['mod_id'], var_id, var_dict['var'])
        pif.dbh.write('variation', var_dict)
        for attr in det_dict:
            pif.dbh.write('detail', {'mod_id': var_dict['mod_id'], 'var_id': var_dict['var'], 'attr_id': str(attributes[attr]['id']), 'description': det_dict[attr]})
        if var_sel:
            pif.render.message('varsel', var_sel, '<br>')
            pif.dbh.update_variation_selects_for_variation(mod_id, var_dict['var'], var_sel.split())
	pif.render.message('phcred', phcred, '<br>')
	pif.dbh.write_photo_credit(phcred, config.IMG_DIR_VAR[1:], mod_id, var_dict['var'])
        if repic:
            rename_variation_pictures(pif, mod_id, var_dict['var'], mod_id, repic)
    else:
        save_model(pif, mod_id)
    pif.dbh.recalc_description(mod_id)


def move_variation(pif, old_mod_id, old_var_id, new_mod_id, new_var_id, *args, **kwargs):  # pragma: no cover
    verbose = False
    if pif.argv:
        pif.render.message('move_variation', old_mod_id, old_var_id, new_mod_id, new_var_id)
        verbose = True
	pif.dbh.set_verbose(True)
    if old_mod_id == new_mod_id and old_var_id == new_var_id:
	pif.render.message('no change')
        return
    pif.dbh.update_variation({'mod_id': new_mod_id, 'var': new_var_id, 'imported_var': new_var_id}, {'mod_id': old_mod_id, 'var': old_var_id}, verbose=verbose)
    pif.dbh.update_variation({'picture_id': ''}, {'mod_id': old_mod_id, 'picture_id': old_var_id}, verbose=verbose)

    # This will take some work.
    old_attrs = pif.dbh.depref('attribute', pif.dbh.fetch_attributes(old_mod_id))
    old_attrs = {x['attribute_name']: x for x in old_attrs}
    new_attrs = pif.dbh.depref('attribute', pif.dbh.fetch_attributes(new_mod_id))
    new_attrs = {x['attribute_name']: x for x in new_attrs}
    pif.render.message(old_attrs)
    pif.render.message(new_attrs)
    details = pif.dbh.fetch_details(old_mod_id, old_var_id, nodefaults=True).get(old_var_id, {})
    for detail in details:
	if detail in new_attrs:
	    new_att_id = new_attrs[detail]['id']
	    old_att_id = old_attrs[detail]['id']
	    pif.dbh.update_detail({'attr_id': new_att_id, 'mod_id': new_mod_id, 'var_id': new_var_id},
		{'attr_id': old_att_id, 'mod_id': old_mod_id, 'var_id': old_var_id})
	else:
	    pif.render.message('cannot transfer %s="%s"' % (detail, details[detail]))

    pif.dbh.write('variation_select', {'mod_id': new_mod_id, 'var_id': new_var_id}, where="var_id='%s' and mod_id='%s'" % (old_var_id, old_mod_id), modonly=True, verbose=verbose)
    rename_variation_pictures(pif, old_mod_id, old_var_id, new_mod_id, new_var_id)


def copy_variation(pif, mod_id, old_var_id, new_var_id, *args, **kwargs):  # pragma: no cover
    verbose = False
    if pif.argv:
        pif.render.message('copy_variation', mod_id, old_var_id, new_var_id)
    if old_var_id == new_var_id:
        return

    var = pif.dbh.fetch_variation(mod_id, old_var_id)
    if var:
	var = pif.dbh.depref('variation', var[0])
	var['imported_var'] = new_var_id
	pif.dbh.insert_variation(mod_id, new_var_id, var)


def rename_variation(pif, mod_id=None, old_var_id=None, new_var_id=None, *args, **kwargs):  # pragma: no cover
    if not mod_id or not old_var_id or not new_var_id:
	return
    verbose = False
    if pif.argv:
        pif.render.message('rename_variation', mod_id, old_var_id, new_var_id)
    if old_var_id == new_var_id:
        return
    pif.dbh.update_variation({'var': new_var_id, 'imported_var': new_var_id}, {'mod_id': mod_id, 'var': old_var_id}, verbose=verbose)
    pif.dbh.update_variation({'picture_id': new_var_id}, {'mod_id': mod_id, 'picture_id': old_var_id}, verbose=verbose)
    pif.dbh.update_detail({'var_id': new_var_id}, {'var_id': old_var_id, 'mod_id': mod_id}, verbose=verbose)
    pif.dbh.write('variation_select', {'var_id': new_var_id}, where="var_id='%s' and mod_id='%s'" % (old_var_id, mod_id), modonly=True, verbose=verbose)
    # If we're renaming, I'd like to also rename the pictures.
    rename_variation_pictures(pif, mod_id, old_var_id, mod_id, new_var_id)


def swap_variations(pif, mod_id=None, var1=None, var2=None, *args, **kwargs):
    if not mod_id or not var1 or not var2:
	return
    rename_variation(pif, mod_id, var1, var1 + 'x')
    rename_variation(pif, mod_id, var2, var1)
    rename_variation(pif, mod_id, var1 + 'x', var2)


def rename_variation_pictures(pif, old_mod_id, old_var_id, new_mod_id, new_var_id):  # pragma: no cover
    if old_mod_id.lower() == new_mod_id.lower() and old_var_id.lower() == new_var_id.lower():
	return
    patt1 = useful.relpath('.', config.IMG_DIR_VAR, '?_%s-%s.*' % (old_mod_id.lower(), old_var_id.lower()))
    patt2 = useful.relpath('.', config.IMG_DIR_VAR, '%s-%s.*' % (old_mod_id.lower(), old_var_id.lower()))
    pics = glob.glob(patt1.lower()) + glob.glob(patt2.lower())
    for old_pic in pics:
        new_pic = old_pic.replace('-%s.' % old_var_id.lower(), '-%s.' % new_var_id.lower())
        new_pic = new_pic.replace('_%s-' % old_mod_id.lower(), '_%s-' % new_mod_id.lower())
        pif.render.comment("rename", old_pic, new_pic)
        pif.render.message("rename", old_pic, new_pic, "<br>")
        os.rename(old_pic, new_pic)
    pif.dbh.write('photo_credit',
	{'name': '%s-%s' % (new_mod_id.lower(), new_var_id.lower())},
	pif.dbh.make_where({'name': '%s-%s' % (old_mod_id.lower(), old_var_id.lower()), 'path': config.IMG_DIR_VAR[1:]}),
	modonly=True, tag='RenamePictures')


def remove_picture(pif, mod_id, var_id):  # pragma: no cover
    patt1 = '.' + config.IMG_DIR_VAR + '/?_%s-%s.*' % (mod_id, var_id)
    patt2 = '.' + config.IMG_DIR_VAR + '/%s-%s.*' % (mod_id, var_id)
    pics = glob.glob(patt1.lower()) + glob.glob(patt2.lower())
    for pic in pics:
        pif.render.comment("delete", pic)
        pif.render.message("delete", pic, "<br>")
        os.unlink(pic)
    cred = pif.dbh.fetch_photo_credit('.' + config.IMG_DIR_VAR, '%s-%s' % (mod_id, var_id))
    if cred:
	pif.dbh.delete_photo_credit(cred['photo_credit.id'])


def add_variation(pif, mod_id=None, var_id=None, *args, **kwargs):  # pragma: no cover
    if mod_id and var_id:
	new_var = {'body': ' '.join(args), 'imported_from': 'cl', 'imported_var': var_id}
	new_var.update(kwargs)
	var = pif.dbh.fetch_variation(mod_id, var_id)
	if var:
	    print 'That variation already exists!', mod_id, var_id
	else:
	    pif.dbh.insert_variation(mod_id, var_id, new_var)
	    pif.dbh.recalc_description(mod_id)


def delete_variation(pif, mod_id=None, var_id=None, *args, **kwargs):  # pragma: no cover
    if mod_id and var_id:
	pif.dbh.delete_variation({'mod_id': mod_id, 'var': var_id})
	pif.dbh.delete_detail({'mod_id': mod_id, 'var_id': var_id})
	pif.dbh.delete_variation_select({'mod_id': mod_id, 'var_id': var_id})

# ----- multiple variation page ---------------------------

def do_var(pif, display_type, model, var, attributes, prev, credits, photogs):
    if display_type == mbdata.LISTTYPE_NORMAL:
	return var
    elif display_type == mbdata.LISTTYPE_PICTURE:
	return do_var_detail(pif, model, var, attributes, prev, credits, photogs)
    return do_var_for_list(pif, model, var, attributes, prev, credits, photogs)


var_types = {
	'c': 'Core',
	'1': 'C1',
	'2': 'C2',
	'f': 'F',
	'p': '2P',
}
def do_var_detail(pif, model, var, attributes, prev, credits, photogs):
    def mk_star(has_thing, no_thing):
	return '<i class="fa fa-star %s"></i>' % ('green' if has_thing else 'gray' if no_thing else 'white')

    varsel = pif.dbh.fetch_variation_selects(var['mod_id'], var['var'])
    phcred = credits.get(('%(mod_id)s-%(var)s' % var).lower(), '')
    ty_var, is_found, has_de, has_ba, has_bo, has_in, has_wh, has_wi, has_wt = single.calc_var_pics(pif, var)
    cat_v = set(var['category'].split())
    cat_vs = set([x['variation_select.category'] for x in varsel])
    cat = ' '.join(cat_v)
    if cat_v != cat_vs:
	cat += '/' + ' '.join(cat_vs)
    row = {
	'ID': pif.render.format_link('?edit=1&mod=%s&var=%s' % (var['mod_id'], var['var']), var['var'].upper()),
	'Description': var['text_description'],
	'Cat': cat,
	'Ty': var_types.get(ty_var, ty_var),
	'Cr': phcred,
	'Pic': var['picture_id'],
	'De': mk_star(has_de, not model['format_description']),
	'Ba': mk_star(has_ba, not model['format_base']),
	'Bo': mk_star(has_bo, not model['format_body']),
	'In': mk_star(has_in, not model['format_interior']),
	'Wh': mk_star(has_wh, not model['format_wheels']),
	'Wi': mk_star(has_wi, not model['format_windows']),
	'W/': mk_star(has_wt, not model['format_with']),
    }
    for sz in mbdata.image_size_types:
	row[sz.upper()] = mk_star(
	    os.path.exists(useful.relpath('.', config.IMG_DIR_VAR, sz + '_' + var['mod_id'] + '-' + var['var'] + '.jpg').lower()),
	    False)
    return row


def do_var_for_list(pif, model, var, attributes, prev, credits, photogs):
    pic_id = var['picture_id']
    cats = [mbdata.categories.get(x, x) for x in var['_catlist']]

    descs = list()
    dets = list()
    note_text = ''
    for d in sorted(var.keys()):
	if d.startswith('_') or d == 'text_description' or not var[d]:
	    pass
	elif d in text_attributes:
	    descs.append(d)
	elif d in note_attributes:
	    if var[d]:
		if d == 'category':
		    note_text += attributes[d]['title'] + ': ' + ', '.join(cats) + '<br>'
		else:
		    note_text += attributes[d]['title'] + ': ' + var[d] + '<br>'
	elif d not in hidden_attributes:
	    dets.append(d)
    if pif.is_allowed('a'):  # pragma: no cover
        note_text += 'Import: %s, %s-%s<br>' % (var['imported'], var['imported_from'], var['imported_var'])
        note_text += 'Show: ' + pif.render.format_text_input("picture_id." + var['var'], 8, value=pic_id, also={'class': 'bggray' if pic_id else 'bgok'})
	if pic_id:
	    note_text += '<span class="warn">'
        for sz in mbdata.image_size_types:
            if os.path.exists(useful.relpath('.', config.IMG_DIR_VAR, sz + '_' + var['mod_id'] + '-' + var['var'] + '.jpg').lower()):
                note_text += sz.upper() + ' '
	if pic_id:
	    note_text += '</span>'
	else:
	    phcred = credits.get(('%(mod_id)s-%(var)s' % var).lower(), '')
	    note_text += '<div class="%s">Credit: ' % ('bgok' if phcred or pic_id else 'bgno')
	    note_text += pif.render.format_select("phcred." + var['var'], photogs, selected=phcred, blank='') + '</div>'
        note_text += "References:<br>" + pif.render.format_text_input("var_sel." + var['var'], 256, 24, value=var['references'], also={'class': 'bgok' if var['references'] else 'bgno'})

    ostr = '<center>'
    ostr += pif.render.format_link('?edit=1&mod=%s&var=%s' % (var['mod_id'], var['var']), var['var'].upper())
    if pif.is_allowed('a'):  # pragma: no cover
        ostr += '<br><input type="checkbox" name="v" value="%s"><br>' % var['var']
    #count_descs = reduce(lambda y, x: y + (1 if var[x] != '' else 0), text_attributes, 0)
    # take into account if format_* is blank
    def attr_star(model, var):
	return sum([int(bool(var['text_' + x]) or not model['format_' + x]) for x in desc_attributes])

    count_descs = attr_star(model, var)
    ostr += '<i class="fa fa-star %s"></i>' % (
	    'green' if count_descs == len(text_attributes) else ('red' if not count_descs else 'orange'))
    ostr += '</center>'
    return {
        'ID': ostr,
        'Description': '<div class="varentry">' + var['text_description'] + '</div>\n' + '<br>'.join([
	    '<span class="%s">%s: %s</span>\n' % (
	    ("diff" if pif.is_allowed('a') and var[d] != prev.get(d, var[d]) else "same"),
	    attributes[d]['title'], var[d]) for d in descs]),
        'Details': '<br>'.join([
	    '<span class="%s">%s: %s</span>\n' % (
	    ("diff" if pif.is_allowed('a') and var[d] != prev.get(d, var[d]) else "same"),
	    attributes[d]['title'], var[d]) for d in dets if d in attributes]),
        'Picture': '<a href="%(_lnk)s">%(_picture)s</a>' % var,
        'Notes': note_text,
    }


class VarSearchForm(object):

    # add output format to this
    output_types = [
	(mbdata.LISTTYPE_NORMAL, 'Normal'),
	(mbdata.LISTTYPE_CHECKLIST, 'Checklist'),
	(mbdata.LISTTYPE_THUMBNAIL, 'Thumbnail'),
	(mbdata.LISTTYPE_TEXT, 'Text'),
	(mbdata.LISTTYPE_CSV, 'CSV'),
	(mbdata.LISTTYPE_JSON, 'JSON'),
    ]
    def __init__(self, pif, mod_id):
	self.page_id = pif.page_id
	self.mod_id = mod_id
	self.attr_pics = {x['attribute.attribute_name']: x for x in pif.dbh.depref('attribute_picture', pif.dbh.fetch_attribute_pictures(mod_id))}
	attributes = {x['attribute_name']: x for x in pif.dbh.depref('attribute', pif.dbh.fetch_attributes(mod_id, with_global=True))}
	attributes.update({pif.dbh.table_info['variation']['columns'][x]:
	    {'title': pif.dbh.table_info['variation']['titles'][x]}
		for x in range(0, len(pif.dbh.table_info['variation']['columns']))})
	attributes['references'] = {'title': 'References', 'definition': 'varchar(256)'}
	for vardesc in pif.dbh.describe('variation'):
	    if vardesc['field'] in attributes:
		attributes[vardesc['field']]['definition'] = vardesc['type']
	self.attributes = attributes

	var_selects = pif.dbh.depref('variation_select', pif.dbh.fetch_variation_selects(mod_id))
	selects = dict()
	for var_sel in var_selects:
	    selects.setdefault(var_sel['var_id'], [])
	    selects[var_sel['var_id']].append(var_sel['ref_id'] +
		(('/' + var_sel['sub_id']) if var_sel['sub_id'] else '') +
		((':' + var_sel['category']) if var_sel['category'] else '')
	    )
	self.selects = selects

    def read(self, form):
	self.attrs = {key: form.get_str(key) for key in self.attributes}
	self.attrq = dict()
	for attr in self.attributes.keys() + ['text_note']:
	    if form.has(attr):
		if attr == 'manufacture' and form.get_str(attr) == 'unset':
		    self.attrq[attr] = ''
		else:
		    self.attrq[attr] = form.search(attr)
	self.nots = {key: form.get_bool('not_' + key) for key in self.attributes}
	self.ci = form.get_bool('ci')
	self.c1 = form.get_bool('c1') or not form.get_bool('hc')
	self.c2 = form.get_bool('c2') or not form.get_bool('hc')
	self.cateq = form.get_str('category', '')
	self.with_pics = form.get_bool('pic1') or not form.get_bool('hc')
	self.without_pics = form.get_bool('pic0') or not form.get_bool('hc')
	self.varl = form.get_str("v")
	self.wheelq = form.get_str("var.wheels")
	self.sobj = form.search("var.s")
	self.is_list = form.has('list')
	self.is_detail = form.has('vdet')
	self.recalc = form.has('recalc')
	self.verbose = form.get_bool('verbose')
	self.codes = []
	if self.c1:
	    self.codes.append(1)
	if self.c2:
	    self.codes.append(2)
	#useful.write_message(str(self.__dict__))
	self.all = (
	    not self.attrq and
	    #self.ci = form.get_bool('ci')
	    #self.c1 = form.get_bool('c1')
	    not self.cateq and
	    self.with_pics and
	    self.without_pics and
	    not self.varl and
	    not self.wheelq and
	    not self.sobj and
	    self.codes == [1, 2]
	)
	return self

    def write(self, pif, values={}):
	pif.render.comment("attributes", self.attributes)

	entries = [{'title': self.attributes[x]['title'], 'value': pif.render.format_text_input(x, 64, 64)} for x in text_attributes]
	entries.append({'title': 'Note', 'value': pif.render.format_text_input('text_note', 64, 64)})
	entries.append({'title': '', 'value':
	    pif.render.format_checkbox('ci', [(1, 'Case insensitive')], checked=[1]) #+ ' - ' +
	    #pif.render.format_select('listtype', self.output_types, selected=mbdata.LISTTYPE_NORMAL)
	})
	lsections = [dict(columns=['title', 'value'], range=[{'entry': entries}], note='', noheaders=True, footer='<br>')]

	entries = []
	for key in sorted(set(self.attributes.keys()) - set(hidden_attributes) - set(text_attributes)):
	    if key == 'category':
		cates = [('', '')] + [(x, mbdata.categories.get(x, x)) for x in values.get(key, [])]
		cates.sort(key=lambda x: x[1])
		value = pif.render.format_button_up_down_select(key, -1) + pif.render.format_select(key, cates, id=key) + \
			'&nbsp;' + pif.render.format_checkbox('c1', [(1, 'Show Code 1')], checked=[1]) + \
			'&nbsp;' + pif.render.format_checkbox('c2', [(2, 'Show Code 2')], checked=[2])
	    elif not any(values.get(key, [])):
		continue
	    else:
		value = pif.render.format_button_up_down_select(key, -1) + \
			pif.render.format_select(key, sorted(values[key]), id=key, blank='')
	    title = self.attributes[key]['title']
	    title_modal = show_detail_modal(pif, self.attr_pics.get(key, {}), self.mod_id)
	    if title_modal:
		title += ''' <i onclick="init_modal('m.%s');" class="modalbutton fa fa-question-circle-o"></i>\n''' % key
		title += pif.render.format_modal('m.' + key, title_modal)
	    entries.append({
		'title': title,
		'value': value,
		'not': pif.render.format_checkbox('not_' + key, [(1, 'not')])
	    })

	entries.append({
	    'title': '&nbsp;',
	    'value': pif.render.format_button_input("filter", "submit") + '\n' +
		     ((pif.render.format_button_input("list") + '\n') if pif.is_allowed('a') else '') +
		     pif.render.format_button_reset('vars') + pif.render.format_hidden_input({'hc': 1}) +
		    '&nbsp;' + pif.render.format_checkbox('pic1', [(1, 'With Pictures')], checked=[1]) +
		    '&nbsp;' + pif.render.format_checkbox('pic0', [(1, 'Without Pictures')], checked=[1]),
	    'not': '&nbsp;'
	})

	lsections.append(dict(columns=['title', 'value', 'not'], range=[{'entry': entries}], note='', noheaders=True))
	return dict(section=lsections)

    def cate_match(self, var, code):
	category = var['_catlist'] = var.get('category', '').split()
	if not category:
	    category = ['MB']
	search_not = self.nots['category']
	modelcode = 2 if (set(mbdata.code2_categories) & set(category)) else 1
	retval = not code or (code == modelcode)
	if retval and self.cateq:
	    retval = (self.cateq in category) or (self.cateq == 'MB' and not category)
	    if search_not:
		retval = not retval
	#useful.write_message('cate_match', var['var'], retval, self.cateq, code)
	return retval

    def wheel_match(self, var):
	retval = (not self.wheelq) or var['wheels'] == self.wheelq or var['text_wheels'] == self.wheelq
	#useful.write_message('wheel_match', var['var'], retval)
	return retval

    def search_match(self, var):
	if not self.sobj:
	    #useful.write_message('search_match', var['var'], True, self.sobj)
	    return True
	for k in var:
	    if k in text_attributes + ['text_note'] and useful.search_match(self.sobj, var[k]):
		#useful.write_message('search_match', var['var'], True, self.sobj, k)
		return True
	#useful.write_message('search_match', var['var'], False, 'final')
	return False

    def desc_match(self, var):
	if not self.attrq:
	    #useful.write_message('desc_match', var['var'], True, self.attrq, 'no attrq')
	    return True
	for attr in self.attrq:
	    var_val = var.get('note', '') if attr == 'text_note' else var.get(attr, '')
	    query_val = ' '.join(self.attrq.get(attr, []))
	    if attr in text_attributes + ['text_note']:
		attrval = var['note' if attr == 'text_note' else attr]
		for obj in self.attrq[attr]:
		    if not self.ci and attrval.find(obj) < 0:
			#useful.write_message('desc_match', var['var'], False, self.attrq, self.ci, attrval, '-', obj)
			return False
		    if self.ci and attrval.lower().find(obj.lower()) < 0:
			#useful.write_message('desc_match', var['var'], False, self.attrq, self.ci, attrval, '-', obj)
			return False
	#useful.write_message('desc_match', var['var'], True, self.attrq, 'final')
	return True

    def field_match(self, var):
	if not self.attrq:
	    #useful.write_message('field_match', var['var'], True, 'no attrq')
	    return True
	for attr in self.attrq:
	    search_not = self.nots.get(attr)
	    var_val = var.get(attr, '')
	    query_val = ' '.join(self.attrq.get(attr, []))
	    if attr in text_attributes + ['text_note', 'category']:
		continue
	    elif var_val == query_val and search_not:
		#useful.write_message('field_match', var['var'], False, var_val, query_val, 'neg')
		return False
	    elif var_val != query_val and not search_not:
		#useful.write_message('field_match', var['var'], False, var_val, query_val, 'pos')
		return False
	#useful.write_message('field_match', var['var'], True, self.attrq, 'final')
	return True

    def id_match(self, var):
	retval = (not self.varl or (var['var'] in self.varl))
	#useful.write_message('id_match', var['var'], retval, self.varl)
	return retval

    def pic_match(self, var):
	retval = (self.with_pics and var['_has_pic'] or self.without_pics and not var['_has_pic'])
	return retval

    def model_match(self, var, code):
	#useful.write_message('model_match', 'attrq', self.attrq)
	return (self.id_match(var) and
		self.pic_match(var) and
		self.cate_match(var, code) and
		self.search_match(var) and
		self.wheel_match(var) and
		self.desc_match(var) and
		self.field_match(var))

    def show_search_object(self):
	ostr = 'Selected models' if self.varl else 'All models'
	if self.cateq:
	    ostr +=  ' in ' +  mbdata.categories.get(self.cateq, self.cateq)
	if self.wheelq:
	    ostr += ' with ' + self.wheelq + " wheels"
	if self.attrq:
	    ostr += ' matching search'
	return ostr

    def make_values(self, mvars):
	values = dict()
	wheels = list()

	cates = set()
	for key in mvars:
	    variation = mvars[key]
	    variation['references'] = ' '.join(list(set(self.selects.get(key, []))))
	    category = variation['_catlist'] = variation.get('category', '').split()
	    if not category:
		category = ['MB']
	    for c in category:
		cates.add(c)
	    if variation.get('wheels') not in wheels:
		wheels.append(variation.get('wheels'))
	    if variation.get('text_wheels') not in wheels:
		wheels.append(variation.get('text_wheels'))
	    for key in variation:
		if key in text_attributes:
		    continue
		values.setdefault(key, [])
		newvalue = variation[key]
		if not newvalue:
		    newvalue = ''
		if newvalue not in values[key]:
		    values[key].append(newvalue)

	self.form_values = values
	self.form_wheels = wheels
	self.form_cates = cates
	return values


def do_model(pif, model, vsform, mvars, display_type, photogs):
    llineup = {'id': 'vars', 'section': []}
    shown_columns = detail_columns if display_type == mbdata.LISTTYPE_PICTURE else list_columns

    credits = {x['photo_credit.name'].lower(): x['photographer.id'] for x in pif.dbh.fetch_photo_credits_for_vars(path=config.IMG_DIR_VAR[1:], name=vsform.mod_id, verbose=False)}
    prev = {}
    for code in vsform.codes:
	lsec = {'id': 'code_%d dt_%s' % (code, display_type), 'name': 'Code %d Models' % code, 'range': list(), 'switch': code != 1,
            'headers': dict(zip(shown_columns, shown_columns)),
            'columns': 4 if display_type == mbdata.LISTTYPE_NORMAL else shown_columns,
	}
	lran = {'id': 'ran', 'entry': []}
        for var_id in sorted(mvars.keys()):
            var = mvars[var_id]
            pif.render.comment(var)
            #var['references'] = ' '.join(list(set(vsform.selects.get(var_id, []))))
            if vsform.model_match(var, code):
                #var['area'] = ', '.join([mbdata.regions.get(x, x) for x in var.get('area', '').split(';')])
		var['link'] = '?mod=%s&var=%s' % (var['mod_id'], var['var'])
		var['categories'] =  ' - '.join([pif.render.format_image_art(mbdata.cat_arts.get(x), desc=mbdata.categories.get(x, x)) for x in var['_catlist']])
		lran['entry'].append(do_var(pif, display_type, model, var, vsform.attributes, prev, credits, photogs))
		prev = var

	lran['styles'] = {'Description': 'lefty'}
	if len(lran['entry']):
	    lsec['count'] = '%d entries' % len(lran['entry']) if len(lran['entry']) > 1 else '1 entry'
	    if display_type == mbdata.LISTTYPE_NORMAL:
		while len(lran['entry']) < 4:
		    lran['entry'].append({'text': '', 'class': 'blank'})
	    lsec['range'].append(lran)
	    llineup['section'].append(lsec)

    if display_type == mbdata.LISTTYPE_NORMAL:
	pif.render.format_matrix_for_template(llineup)
    return llineup


def save_model(pif, mod_id):
    for key in pif.form.keys(start='picture_id.'):
        if key[11:] == pif.form.get_str(key):
            pif.dbh.update_variation({'picture_id': pif.form.get_str(key)}, {'mod_id': mod_id, 'var': ''})
        else:
            pif.dbh.update_variation({'picture_id': pif.form.get_str(key)}, {'mod_id': mod_id, 'var': key[11:]})
    for key in pif.form.keys(start='var_sel.'):
        varsel = list(set(pif.form.get_str(key).split()))
        pif.dbh.update_variation_selects_for_variation(mod_id, key[8:], varsel)
    for var in pif.form.roots(start='phcred.'):
	phcred = pif.form.get_str('phcred.' + var)
	if phcred:
	    pif.render.message('phcred', mod_id, var, "'%s'" % phcred, '<br>')
            pif.dbh.write_photo_credit(phcred, config.IMG_DIR_VAR[1:], mod_id, var)
    phcred = pif.form.get_str('phcred')
    if phcred:
	pif.render.message('phcred', mod_id, "'%s'" % phcred, '<br>')
	pif.dbh.write_photo_credit(phcred, config.IMG_DIR_MAN[1:], mod_id)


def show_model(pif, model):
    if not model:
        raise useful.SimpleError("That is not a recognized model ID.")
    mod_id = model['id']
    vsform = VarSearchForm(pif, mod_id).read(pif.form)
    if vsform.recalc:
        pif.dbh.recalc_description(mod_id)

    pic_id = None
    cates = {'MB'}
    mvars = dict()
    for variation in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
	variation['_catlist'] = variation.get('category', '').split()
	cates.update(variation['_catlist'])
	pic_id = variation['picture_id']

        img = pif.render.find_image_path([variation['mod_id']], nobase=True, vars=pic_id if pic_id else variation['var'], prefix=mbdata.IMG_SIZ_SMALL)
	variation['_has_pic'] = bool(img)
        variation['_picture'] = pif.render.fmt_img_src(img, also={'title': variation['var']}) if img else pif.render.fmt_no_pic(True, mbdata.IMG_SIZ_SMALL)

	if pif.is_allowed('u'):  # pragma: no cover
	    variation['_dir'] = useful.relpath('.', config.LIB_MAN_DIR, variation['mod_id'].lower())
	    variation['_lnk'] = 'upload.cgi?d=%(_dir)s&m=%(mod_id)s&v=%(var)s' % variation
	else:
	    variation['_dir'] = '.' + config.INC_DIR
	    variation['_lnk'] = 'upload.cgi?m=%(mod_id)s&v=%(var)s' % variation
	variation['area'] = ', '.join([mbdata.get_countries().get(x, mbdata.areas.get(x, x)) for x in variation.get('area', '').split(';')])
	mvars[variation['var']] = variation

    vsform = VarSearchForm(pif, mod_id).read(pif.form)
    values = vsform.make_values(mvars)
    values['category'] = list(cates)
    #photogs = [(x.photographer.id, x.photographer.name) for x in pif.dbh.fetch_photographers()]
    photogs = [(x.photographer.id, x.photographer.name) for x in pif.dbh.fetch_photographers(pif.dbh.FLAG_ITEM_HIDDEN)]
    display_type = mbdata.LISTTYPE_ADMIN if vsform.is_list else mbdata.LISTTYPE_PICTURE if vsform.is_detail else mbdata.LISTTYPE_NORMAL;
    llineup = do_model(pif, model, vsform, mvars, display_type, photogs)
    img = pif.render.format_image_required(mod_id, largest=mbdata.IMG_SIZ_MEDIUM, pdir=config.IMG_DIR_MAN)
    phcred = pif.dbh.fetch_photo_credit('.' + config.IMG_DIR_MAN, mod_id)
    phcred = phcred.get('photographer.id', '') if phcred else ''

    footer = pif.render.format_button_input('list')
    if pif.is_allowed('a'):  # pragma: no cover
	footer += pif.render.format_button_input('save')
	footer += pif.render.format_button("add", 'vars.cgi?edit=1&mod=%s&add=1' % mod_id)
	footer += pif.render.format_button("casting", pif.dbh.get_editor_link('casting', {'id': mod_id}))
	footer += pif.render.format_button("recalc", '?recalc=1&mod=%s' % mod_id)
	if display_type == mbdata.LISTTYPE_ADMIN:
	    img += '<div class="%s">Credit: ' % ('bgok' if phcred or pic_id else 'bgno')
	    img += pif.render.format_select("phcred", photogs, selected=phcred, blank='') + '</div>'
    if pif.is_allowed('u'):  # pragma: no cover
	footer += pif.render.format_button("upload", 'upload.cgi?d=' + useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower()) + '&m=' + mod_id)
	footer += pif.render.format_button("pictures", 'traverse.cgi?d=%s' % useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower()))

    # ------- render ------------------------------------

    pif.render.set_page_extra(pif.render.reset_button_js + pif.render.increment_select_js + pif.render.toggle_display_js)
    pif.render.set_button_comment(pif, 'man=%s&var=%s' % (mod_id, vsform.varl))
    context = {
	'image': img,
	'llineup': llineup,
	'footer': footer,
	'search_object': vsform.show_search_object(),
	'verbose': vsform.verbose,
	'show_as_list': vsform.is_list or vsform.is_detail,
	'mod_id': mod_id,
	'var_search_form': vsform.write(pif, values),
	'var_search_visible': pif.render.format_button_input_visibility("varsearch", True),
    }
    return pif.render.format_template('vars.html', **context)


@basics.web_page
def main(pif):
    man_id = pif.form.get_id('mod')
    var = pif.form.get_id('var')

    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/single.cgi', 'By ID')
    pif.render.hierarchy_append('/cgi-bin/single.cgi?id=%s' % man_id, man_id)
    pif.render.hierarchy_append('/cgi-bin/vars.cgi?mod=%s' % man_id, 'Variations')
    if var:
	pif.render.hierarchy_append('/cgi-bin/vars.cgi?mod=%s&var=%s' % (man_id, var), var)
    pif.render.print_html()

    regs = mbdata.get_countries()
    regs.update(mbdata.regions)
    man = dict()
    if man_id:
        man = pif.dbh.fetch_casting(man_id, extras=True)
        if not man:
            man = pif.dbh.fetch_casting_by_alias(man_id, extras=True)
    if not man:
        man_id = var = ''
    elif var:
	var = mbdata.normalize_var_id(man, var)
        pif.render.title = '%(casting_type)s %(id)s: %(name)s' % man
        pif.render.title += ' - Variation ' + var
    elif man_id:
        pif.render.title = '%(casting_type)s %(id)s: %(name)s' % man
        pif.render.title += ' - Variations'
    else:
        pass

    edit = False
    if pif.form.has("delete"):
        delete_variation(pif, man_id, var)
        var = ''
    elif pif.form.has("save"):
	var = pif.form.get_str('ovar')
        save(pif, man_id, var)
	var = ''
    elif pif.form.has("add"):
        var = var or 'unset'
        #add_variation(pif, man_id, var, kwargs={'imported_from': 'web'})
	return show_variation_editor(pif, man, var, True, True)
    elif pif.form.has('edit'):
	edit = True
    elif pif.form.has("rmpic"):
        remove_picture(pif, man_id, var)
    elif pif.form.has("promote"):
        imglib.promote_picture(pif, man_id, var)
    elif not man:
	raise useful.SimpleError("Can't find requested information.  Please try something else.")

    if var:
	return show_variation_editor(pif, man, var, edit)
    return show_model(pif, man)

# ----- msearch -------------------------------------------

def add_model_var_table_pic_link(pif, mdict):
    if mdict.get('v.picture_id'):
        mdict['img'] = pif.render.format_image_required(mdict['v.mod_id'], prefix=mbdata.IMG_SIZ_SMALL, nobase=True, vars=mdict['v.picture_id'])
    else:
        mdict['img'] = pif.render.format_image_required(mdict['v.mod_id'], prefix=mbdata.IMG_SIZ_SMALL, nobase=True, vars=mdict['v.var'])
    #mdict['link'] = 'single.cgi?id=%(v.mod_id)s' % mdict
    mdict['link'] = 'vars.cgi?mod=%(v.mod_id)s&var=%(v.var)s' % mdict
    ostr = '  <center><table class="entry"><tr><td><center><font face="Courier">%(v.mod_id)s-%(v.var)s</font></br>\n' % mdict
    ostr += '   <a href="%(link)s">%(img)s<br><b>%(base_id.rawname)s</b></a>\n' % mdict
    #ostr += "   <br><i>%(v.text_description)s</i>\n" % mdict
    ostr += '<table class="vartable">'
    ostr += '<tr><td class="varentry"><i>%s</i></td></tr>' % mdict['v.text_description']
    ostr += "</table>"
    ostr += "  </center></td></tr></table></center>\n"
    return ostr


vfields = {'base': 'text_base', 'body': 'text_body', 'interior': 'text_interior', 'wheels': 'text_wheels',
	   'windows': 'text_windows', 'with': 'text_with',
	   'cat': 'category', 'date': 'date', 'area': 'area'}
cfields = {'casting': 'rawname'}


@basics.web_page
def run_search(pif):
    pif.render.print_html()
    if pif.form.has('ask'):
        return var_search_ask(pif)
    return var_search(pif)


def var_search_ask(pif):
    mod_id = pif.form.get_str('id')
    model = pif.dbh.fetch_casting(mod_id)
    if not model:
        raise useful.SimpleError("That is not a recognized model ID.")
    vsform = VarSearchForm(pif, mod_id).read(pif.form)
    pif.render.title = 'Search ' + model['id'] + ' Variations'
    mvars = {var['var']: var for var in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id))}

    pif.render.set_page_extra(pif.render.reset_button_js + pif.render.increment_select_js + pif.render.modal_js)
    pif.render.set_button_comment(pif, 'man=%s' % mod_id)
    context = {
	'verbose': vsform.verbose,
	'vsform': vsform.write(pif, vsform.make_values(mvars)),
	'id': mod_id,
    }
    return pif.render.format_template('vsearchask.html', **context)


def get_codes(pif):
    codes = 0
    for code in pif.form.get_list('codes'):
        if code not in "123":
            return None
        codes += int(code)
    return codes


#http://beta.bamca.org/cgi-bin/vsearch.cgi?body=&windows=&cat=&base=wheelstrip&interior=&wheels=&casting=&codes=3&start=100
def var_search(pif):
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append(pif.request_uri, 'Variation Search')
    pif.render.title = 'Models matching: ' + ' '.join(pif.form.search('query'))
    modsperpage = 100
    varsq = {vfields[x]: pif.form.search(x) for x in vfields}
    castq = {cfields[x]: pif.form.search(x) for x in cfields}
    codes = get_codes(pif)
    if codes is None:
        raise useful.SimpleError("This submission was not created by the form provided.")

    pif.render.comment('varsq', varsq, 'castq', castq, 'codes', codes)
    mods = pif.dbh.fetch_variation_query(varsq, castq, codes)
    mods.sort(key=lambda x: x['v.mod_id'] + '-' + x['v.var'])
    nmods = len(mods)

    llineup = {'note': '%d variations found matching search' % nmods, 'columns': 4, 'tail': ['', '']}
    start = pif.form.get_int('start')
    mods = mods[start:start + modsperpage]
    lsec = pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
    lran = {'entry': []}
    for mod in mods:
        mod['casting.name'] = mod['base_id.rawname'].replace(';', ' ')
        lran['entry'].append({'text': add_model_var_table_pic_link(pif, mod)})
    lsec['range'] = [lran]
    lsec['columns'] = 4
    llineup['section'] = [lsec]
    qf = pif.form.reformat(vfields) + '&' + pif.form.reformat(cfields)
    if pif.render.verbose:
        qf += '&verbose=1'
    qf += '&codes=%s' % codes
    if start > 0:
        llineup['tail'][1] += pif.render.format_button("previous", 'vsearch.cgi?%s&start=%d' % (qf, max(start - modsperpage, 0))) + ' '
    if start + modsperpage < nmods:
        llineup['tail'][1] += pif.render.format_button("next", 'vsearch.cgi?%s&start=%d' % (qf, min(start + modsperpage, nmods)))

    pif.render.set_button_comment(pif, 'casting=%s&base=%s&body=%s&interior=%s&wheels=%s&windows=%s' % (pif.form.get_str('casting'), pif.form.get_str('base'), pif.form.get_str('body'), pif.form.get_str('interior'), pif.form.get_str('wheels'), pif.form.get_str('windows')))
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('simplematrix.html', llineup=llineup)


def run_search_command(pif, args):
    mods = pif.dbh.fetch_variations(args[0])
    mods.sort(key=lambda x: x['variation.var'])
    for mod in mods:
        pif.render.message('%(mod_id)-8s|%(var)-5s|%(imported_from)-8s|%(text_description)-s' % pif.dbh.depref('variation', mod))


def add_value(pif, mod_id=None, var_id=None, attribute=None, *args):
    value = ' '.join(args)
    mod = pif.dbh.fetch_casting(mod_id)
    if not mod:
	print mod_id, 'not found'
	return
    attrs = pif.dbh.depref('attribute', pif.dbh.fetch_attributes(mod_id, with_global=True))

    for attr in attrs:
	if attr['attribute_name'] == attribute:
	    break
    else:
	print attribute, 'not found'
	return

    var = {}
    if var_id == 'default':
	var_id = ''
	var_id_list = []
    elif var_id == 'all':
	var_id = '*'
	var_id_list = [x['variation.var'] for x in pif.dbh.fetch_variations(mod_id)]
    else:
	var = pif.dbh.depref('variation', pif.dbh.fetch_variation(mod_id, var_id))
	var_id_list = [var_id]
	if not var:
	    print var_id, 'not found'
	    return

    print mod_id, var_id_list, attribute, attr['id'], '=>', value
    if var_id:
	for var_id in var_id_list:
	    if attribute in detail_attributes and var_id:
		pif.dbh.update_variation({attribute: value}, {'mod_id': mod_id, 'var': var_id})
	    else:
		print pif.dbh.add_or_update_detail({'description': value, 'mod_id': mod_id, 'var_id': var_id, 'attr_id': attr['id']}, {'mod_id': mod_id, 'var_id': var_id, 'attr_id': attr['id']}, verbose=True)
    else:
	print pif.dbh.add_or_update_detail({'description': value, 'mod_id': mod_id, 'var_id': var_id, 'attr_id': attr['id']}, {'mod_id': mod_id, 'var_id': var_id, 'attr_id': attr['id']}, verbose=True)
    pif.dbh.recalc_description(mod_id)


def list_variations(pif, mod_id=None, var_id=None, *args, **kwargs):
    if not mod_id:
	return
    if var_id:
	var = pif.dbh.depref('variation', pif.dbh.fetch_variation(mod_id, var_id))
	if var:
	    fmt = pif.dbh.preformat_results(var[0].items())
	    for item in sorted(var[0].items()):
		print fmt % item
    else:
	for variation in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
	    pif.render.message('%5s: %s' % (variation['var'], variation['text_description']))


def list_variation_pictures(pif, start=None, end=None, *args, **kwargs):
    # very similar to do_var_detail(pif, model, attributes, prev, credits, photogs)

    def mk_star(has_thing):
	return 'X' if has_thing else '-'

    fmt_str = '%(ID)-12s %(Cat)-8s %(Ty)-5s %(Cr)-4s %(Pic)-5s|%(De)s %(Ba)s %(Bo)s %(In)s %(Wh)s %(Wi)s|%(T)s %(S)s %(M)s %(L)s|%(Description)s'
    mod_ids = sorted(pif.dbh.fetch_casting_ids())
    if not start:
	start = mod_ids[0]
	end = mod_ids[-1]
    elif not end:
	end = start
    row = {
	'ID': 'ID',
	'Description': 'Description',
	'Cat': 'Cat',
	'Ty': 'Type',
	'Cr': 'Cred',
	'Pic': 'Pic',
	'De': 'D',
	'Ba': 'B',
	'Bo': 'B',
	'In': 'I',
	'Wh': 'W',
	'Wi': 'W',
	'T': 'T',
	'S': 'S',
	'M': 'M',
	'L': 'L',
    }
    pif.render.message(fmt_str % row)
    for mod_id in mod_ids[mod_ids.index(start):mod_ids.index(end) + 1]:
	pif.render.message('--------------------------------------+-----------+-------+-------------------------------------------')
	mod = pif.dbh.fetch_casting(mod_id)
	phcred = pif.dbh.fetch_photo_credit(path=config.IMG_DIR_MAN[1:], name=mod_id, verbose=False)
	row = {
	    'ID': mod['id'],
	    'Description': mod['name'],
	    'Cat': 'not made' if not mod['made'] else '',
	    'Ty': mod['model_type'],
	    'Cr': phcred['photographer.id'] if phcred else '',
	    'Pic': '',
	    'De': ' ',
	    'Ba': ' ',
	    'Bo': ' ',
	    'In': ' ',
	    'Wh': ' ',
	    'Wi': ' ',
	}
	row.update(check_picture_sizes(config.IMG_DIR_MAN, mod_id + '.jpg', mk_star))
	pif.render.message(fmt_str % row)
	credits = {x['photo_credit.name'].lower(): x['photographer.id'] for x in pif.dbh.fetch_photo_credits_for_vars(path=config.IMG_DIR_VAR[1:], name=mod_id, verbose=False)}
	for model in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
	    pic_id = model['picture_id'] if model['picture_id'] else model['var']
	    varsel = pif.dbh.fetch_variation_selects(model['mod_id'], model['var'])
	    phcred = credits.get(('%s-%s' % (model['mod_id'], pic_id)).lower(), '')
	    ty_var, is_found, has_de, has_ba, has_bo, has_in, has_wh, has_wi = single.calc_var_pics(pif, model)
	    cat_v = set(model['category'].split())
	    cat_vs = set([x['variation_select.category'] for x in varsel])
	    cat = ' '.join(cat_v)
	    if cat_v != cat_vs:
		cat += '/' + ' '.join(cat_vs)
	    row = {
		'ID': model['mod_id'] + '-' + model['var'],
		'Description': model['text_description'],
		'Cat': cat,
		'Ty': var_types.get(ty_var, ty_var),
		'Cr': phcred,
		'Pic': model['picture_id'],
		'De': mk_star(has_de),
		'Ba': mk_star(has_ba),
		'Bo': mk_star(has_bo),
		'In': mk_star(has_in),
		'Wh': mk_star(has_wh),
		'Wi': mk_star(has_wi),
	    }
	    row.update(check_picture_sizes(config.IMG_DIR_VAR, model['mod_id'] + '-' + pic_id + '.jpg', mk_star))
#	    for sz in mbdata.image_size_types:
#		row[sz.upper()] = mk_star(
#		    os.path.exists(useful.relpath('.', config.IMG_DIR_VAR, sz + '_' + model['mod_id'] + '-' + pic_id + '.jpg').lower()))
	    pif.render.message(fmt_str % row)


def check_picture_sizes(pdir, root, mk_star):
    return {sz.upper(): mk_star(os.path.exists(useful.relpath('.', pdir, sz + '_' + root).lower())) for sz in mbdata.image_size_types}


def list_photo_credits(pif, photog_id=None):
    start = end = None
    photogs = [photog_id] if photog_id else sorted([x.photographer.id for x in pif.dbh.fetch_photographers()])
    #photogs = [photog_id] if photog_id else sorted([x.photographer.id for x in pif.dbh.fetch_photographers(pif.dbh.FLAG_ITEM_HIDDEN)])
    totals = {x: 0 for x in photogs}
    totals['mod_id'] = totals['main'] = totals['count'] = totals['model_type'] = ''
    fmt_str = '%(mod_id)-6s %(model_type)2s %(main)-4s %(count)7s | ' + ' '.join(['%%(%s)7s' % x for x in photogs])
    headers = {'mod_id': '', 'main': 'Main', 'count': 'Total', 'model_type': 'MT'}
    headers.update({x: x for x in photogs})
    pif.render.message(fmt_str % headers)
    mod_ids = sorted(pif.dbh.fetch_casting_ids())
    if not start:
	start = mod_ids[0]
	end = mod_ids[-1]
    elif not end:
	end = start
    for mod_id in mod_ids[mod_ids.index(start):mod_ids.index(end) + 1]:
	mod = pif.dbh.fetch_casting(mod_id)
	main_phcred = pif.dbh.fetch_photo_credit(path=config.IMG_DIR_MAN[1:], name=mod_id, verbose=False)
	credits = {x['photo_credit.name'].lower(): x['photographer.id'] for x in pif.dbh.fetch_photo_credits_for_vars(path=config.IMG_DIR_VAR[1:], name=mod_id, verbose=False)}
	row = {x: 0 for x in photogs}
	row['mod_id'] = mod_id
	row['model_type'] = mod['model_type']
	row['main'] = main_phcred['photographer.id'] if main_phcred else ''
	row['count'] = 0
	for model in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
	    if model['picture_id']:
		continue
	    ty_var, is_found, has_de, has_ba, has_bo, has_in, has_wh, has_wi = single.calc_var_pics(pif, model)
	    if var_types.get(ty_var, ty_var) == 'C2':
		continue
	    phcred = credits.get(('%s-%s' % (model['mod_id'], model['var'])).lower(), '')
	    row['count'] += 1
	    if phcred in photogs:
		row[phcred] += 1
		totals[phcred] += 1
	for ph in photogs:
	    if row[ph] == row['count']:
		row[ph] = 'all'
	pif.render.message(fmt_str % row)
    pif.render.message(fmt_str % totals)


def info(pif, fields=None, mod_id=None, var_id=None, *args, **kwargs):
    if not mod_id:
	return
    fields = fields.split(',') if (fields and fields != '.') else []
    if var_id:
	for variation in pif.dbh.depref('variation', pif.dbh.fetch_variation(mod_id, var_id)):
	    if fields:
		pif.render.message('|'.join([str(variation[f]) for f in fields]))
	    else:
		pif.render.message('|'.join([str(variation[f]) for f in sorted(variation.keys())]))
    else:
	for variation in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
	    if fields:
		pif.render.message('|'.join([str(variation[f]) for f in fields]))
	    else:
		pif.render.message('|'.join([str(variation[f]) for f in sorted(variation.keys())]))



def count_vars(pif, filelist):
    count = 0
    showtexts = verbose = False
    #verbose = True
    #showtexts = True
    if not filelist:
        castings = [x['id'] for x in pif.dbh.dbi.select('casting', verbose=False)]
    elif filelist[0][0] >= 'a':
        castings = [x['id'] for x in pif.dbh.dbi.select('casting', where="section_id='%s'" % filelist[0], verbose=False)]
    else:
        castings = filelist
        verbose = True
    t_founds = [0, 0, 0, 0, 0, 0]
    t_needs = [0, 0, 0, 0, 0, 0]
    t_cnts = [0, 0, 0, 0, 0, 0, 0]
    def adder(into_arr, from_tup):
	return [sum(x) for x in zip(into_arr, from_tup)]

    print '(f_a, f_c, f_1, f_2, f_f, f_p), (n_a, n_c, n_1, n_2, n_f, n_p), (c_vars, c_de, c_ba, c_bo, c_in, c_wh, c_wi)'
    for mod_id in castings:
        #sys.stdout.write(casting + ' ')
        sys.stdout.flush()
	founds, needs, cnts = single.count_list_var_pics(pif, mod_id)
	print mod_id, founds, needs, cnts
	t_founds = adder(t_founds, founds)
	t_needs = adder(t_needs, needs)
	t_cnts = adder(t_cnts, cnts)
    print 'total', t_founds, t_needs, t_cnts

#    return (found_a, found_c, found_1, found_2, found_f, found_p), \
#	   (needs_a, needs_c, needs_1, needs_2, needs_f, needs_p), \
#	   (len(vars), count_de, count_ba, count_bo, count_in, count_wh, count_wi)



def fix_var(pif):
    for mod_id in pif.dbh.fetch_casting_ids():
	for var in pif.dbh.fetch_variations_bare(mod_id):
	    print var['variation.mod_id'], var['variation.var']
	    rec = {
		'base': var['variation.base'].strip(),
		'body': var['variation.body'].strip(),
		'interior': var['variation.interior'].strip(),
		'windows': var['variation.windows'].strip(),
	    }
	    where = {
		'mod_id': var['variation.mod_id'],
		'var': var['variation.var'],
	    }
	    pif.dbh.update_variation(rec, where)


def check_variation_select(pif):
    print 'missing models'
    res = pif.dbh.raw_execute('''select mod_id, id from variation_select where mod_id not in (select mod_id from casting);''')
    for r in res[0]:
	print r

    print 'missing variations'
    res = pif.dbh.raw_execute('''select mod_id, var_id, id from variation_select where (mod_id, var_id) not in (select mod_id, var from variation);''')
    for r in res[0]:
	print r

    print 'missing pages'
    res = pif.dbh.raw_execute('''select ref_id, id from variation_select where ref_id != '' and ref_id not in (select id var from page_info);''')
    for r in res[0]:
	print r


def check_table_data(pif):
    for table in pif.dbh.table_info:
	print table
	dats = pif.dbh.dbi.execute('select * from ' + table)[0]
	cols = pif.dbh.dbi.describe(table)
	types = list()
	for dat in dats:
	    ldat = list(dat)
	    for col in cols:
		s = ''
		n = 0
		d = ldat.pop(0)
		try:
		    if col['type'].startswith('varchar'):
			s += d
		    elif col['type'].startswith('char'):
			s += d
		    elif col['type'].startswith('text'):
			s += d
		    elif col['type'].startswith('int'):
			n += d
		    elif col['type'].startswith('tinyint'):
			n += d
		except:
		    print table, col, dat
	    for c in s:
		if ord(c) > 127:
		    print table, dat


def get_vars(pif, mod_ids):
    varlist = []
    for mod_id in mod_ids:
	varlist.extend(pif.dbh.fetch_variations(mod_id))
    return varlist


def check_mod_data(pif):
    variation_id_sets = create_var_id_sets(pif)
    mods = pif.dbh.fetch_casting_list()
    modd = {x['casting.id']: x for x in mods}
    ret = False
    for modset in variation_id_sets:
	for mod in modset[1:]:
	    if modd[mod]['casting.variation_digits'] != modd[modset[0]]['casting.variation_digits']:
		print 'vardig mismatch:', mod, modd[mod]['casting.variation_digits'], modset[0], modd[modset[0]]['casting.variation_digits']
		ret = True
    return ret


def create_var_id_sets(pif):
    crs = pif.dbh.fetch_casting_relateds(section_id='single')
    crs = [sorted([x['casting_related.model_id'], x['casting_related.related_id']]) for x in crs if x['casting_related.flags'] & 2]
    cr_d = {}
    seen = []
    for cr in crs:
	if cr[0] not in seen or cr[1] not in seen:
	    cr_d.setdefault(cr[0], set())
	    cr_d[cr[0]].add(cr[0])
	    cr_d[cr[0]].add(cr[1])
	    seen.extend(cr)
    return sorted([sorted(x) for x in cr_d.values()])


def check_var_data(pif):
    variation_id_sets = create_var_id_sets(pif)
    mods = pif.dbh.fetch_casting_list()
    mods.sort(key=lambda x: x['casting.id'])
    for mod in mods:
	mod_id = mod['casting.id']
	mod_ids = [mod_id]
	for modset in variation_id_sets:
	    if modset[0] == mod_id:
		mod_ids = modset
		break
	    if mod_id in modset:
		mod_ids = []
		break
	if not mod_ids:
	    continue
	varlist = get_vars(pif, mod_ids)
	id_nums = set()
	for var in varlist:
	    vid = var['variation.var']
	    nid = mbdata.normalize_var_id(mod, vid)
	    if nid != vid:
		print '*** id mismatch', mod_id, vid, nid
	    if not vid[0].isdigit():
		continue
	    while not vid[-1].isdigit():
		vid = vid[:-1]
	    id_nums.add(int(vid))
	missing = []
	if id_nums:
	    for vid in range(1, max(id_nums)):
		if vid not in id_nums:
		    missing.append(str(vid))
	if missing:
	    print mod_id, ':', ', '.join(missing)


cmds = [
    ('d', delete_variation, "delete: mod_id var_id"),
    ('a', add_variation, "add: mod_id var_id body"),
    ('r', rename_variation, "rename: mod_id old_var_id new_var_id"),
    ('c', copy_variation, "copy: mod_id old_var_id new_var_id"),
    ('s', swap_variations, "swap: mod_id var_id_1 var_id_2"),
    ('m', move_variation, "move: old_mod_id old_var_id new_mod_id [new_var_id]"),
    ('f', run_search_command, "search: obj ..."),
    ('i', info, "info: fields mod_id var_id"),
    ('v', add_value, "value: mod_id var_id-or-default-or-all attribute value"),
    ('l', list_variations, "list: mod_id"),
    ('p', list_variation_pictures, "pictures: mod_id"),
    ('pc', list_photo_credits, "photo credits"),
    ('cv', count_vars, "count vars"),
    ('x', fix_var, "fix var"),
    ('ckvs', check_variation_select, "check variation select"),
    ('ckmd', check_mod_data, "check model data"),
    ('ckvd', check_var_data, "check variation data"),
]


@basics.command_line
def commands(pif):
    useful.cmd_proc(pif, './varias.py', cmds)


if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='')
