#!/usr/local/bin/python

import copy, glob, os, re

import basics
import config
import mbdata
import models
import single
import useful


id_attributes = ['mod_id', 'var', 'picture_id', 'imported_var', 'imported_from', 'references', '_repic', '_credit']
note_attributes = ['manufacture', 'area', 'category', 'date', 'note']
desc_attributes = ['text_description', 'text_base', 'text_body', 'text_interior', 'text_wheels', 'text_windows']
hidden_attributes = id_attributes + ['imported', 'flags']
detail_attributes = ['base', 'body', 'interior', 'windows']

list_columns = ['ID', 'Description', 'Details', 'Picture', 'Notes']
detail_columns = ['ID', 'Description', 'Ty', 'Cr', 'Pic', 'L', 'M', 'S', 'T', 'Ba', 'Bo', 'In', 'Wh', 'Wi']

DISPLAY_TYPE_GRID = 'g'
DISPLAY_TYPE_LIST = 'l'
DISPLAY_TYPE_DETAIL = 'd'

fieldwidth_re = re.compile(r'\w+\((?P<w>\d+)\)')

# ----- display single variation --------------------------

def show_variation_editor(pif, man, var_id, edit=False, addnew=False):
    edit = edit and pif.is_allowed('a')
    if not man:
        raise useful.SimpleError("That casting was not found.")
    mod_id = man['id']

    variation = pif.dbh.depref('variation', pif.dbh.fetch_variation(mod_id, var_id))
    if variation:
	variation = variation[0]
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
	footer += pif.render.format_button("promote", '?mod=%s&var=%s&promote=1' % (mod_id, var_id))

    photogs = [('', '')] + [(x['photographer.id'], x['photographer.name']) for x in pif.dbh.get_photographers()]
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
	ranges = [{'name': 'Description Texts', 'id': 'det', '_attrs': desc_attributes[1:]}]
    ranges.extend([
	    {'name': 'Individual Attributes', 'id': 'det',
	     '_attrs': [d for d in data if not (d in desc_attributes or d in note_attributes or d in hidden_attributes)]},
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
                ostr += '<li>' + pif.render.format_link("packs.cgi?page=%s&id=%s" % (vs['variation_select.ref_id'], vs['variation_select.sub_id']), "%(page_info.title)s: %(base_id.rawname)s (%(base_id.first_year)s)" % vs) + '\n'
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
    if field == '_repic':
	return {'field': '', 'title': 'Move pictures to', 'value': '',
		'new': pif.render.format_text_input("repic." + variation['var'], 16, 16)}
    if field == '_credit':
	return {'field': '', 'title': 'Credit', 'value': '',
		'new': pif.render.format_select("phcred." + variation['var'], photogs, selected=variation.get('_credit', ''))}
    title = attributes[field]['title']
    value = variation.get(field, '')
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
            if 'id' in attributes.get(attr, {}):
                det_dict[attr] = pif.form.get_str(attr + '.' + var_id)
            else:
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
            elif 'id' in attributes.get(attr, {}):
                det_dict[attr] = pif.form.get_str(key)
            else:
                var_dict[attr] = pif.form.get_str(key)
        pif.render.message('<p>', det_dict, '<p>', var_dict)
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
        pif.dbh.dbi.verbose = verbose = True
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
        #pif.dbh.dbi.verbose = verbose = True
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
        #pif.dbh.dbi.verbose = verbose = True
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


def promote_picture(pif, mod_id, var_id):  # pragma: no cover
    pif.render.message('promoting picture for var', var_id, '<br>')
    for pic in glob.glob('.' + config.IMG_DIR_VAR + '/?_%s-%s.*' % (mod_id.lower(), var_id.lower())):
        ofn = pic[pic.rfind('/') + 1:]
        nfn = ofn[:ofn.find('-')] + ofn[ofn.find('.'):]
        useful.file_copy(pic, '.' + config.IMG_DIR_MAN + '/' + nfn)


def remove_picture(pif, mod_id, var_id):  # pragma: no cover
    patt1 = '.' + config.IMG_DIR_VAR + '/?_%s-%s.*' % (mod_id, var_id)
    patt2 = '.' + config.IMG_DIR_VAR + '/%s-%s.*' % (mod_id, var_id)
    pics = glob.glob(patt1.lower()) + glob.glob(patt2.lower())
    for pic in pics:
        pif.render.comment("delete", pic)
        pif.render.message("delete", pic, "<br>")
        os.unlink(pic)


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

def do_var(pif, display_type, model, attributes, prev, credits, photogs):
    if display_type == DISPLAY_TYPE_GRID:
	return model
    elif display_type == DISPLAY_TYPE_DETAIL:
	return do_var_detail(pif, model, attributes, prev, credits, photogs)
    return do_var_for_list(pif, model, attributes, prev, credits, photogs)


var_types = {
	'c': 'Core',
	'1': 'C1',
	'2': 'C2',
	'f': 'F',
	'p': '2P',
}
def do_var_detail(pif, model, attributes, prev, credits, photogs):
    def mk_star(has_thing):
	return '<i class="fa fa-star %s"></i>' % ('green' if has_thing else 'white')

    phcred = credits.get(('%(mod_id)s-%(var)s' % model).lower(), '')
    ty_var, is_found, has_de, has_ba, has_bo, has_in, has_wh, has_wi = single.calc_var_pics(pif, model)
    row = {
	'ID': pif.render.format_link('?edit=1&mod=%s&var=%s' % (model['mod_id'], model['var']), model['var'].upper()),
	'Description': model['text_description'],
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
    for sz in mbdata.image_size_types:
	row[sz.upper()] = mk_star(
	    os.path.exists(useful.relpath('.', config.IMG_DIR_VAR, sz + '_' + model['mod_id'] + '-' + model['var'] + '.jpg').lower()))
    return row


def do_var_for_list(pif, model, attributes, prev, credits, photogs):
    pic_id = model['picture_id']
    cats = [mbdata.categories.get(x, x) for x in model['_catlist']]

    descs = list()
    dets = list()
    note_text = ''
    for d in sorted(model.keys()):
	if d.startswith('_') or d == 'text_description' or not model[d]:
	    pass
	elif d in desc_attributes:
	    descs.append(d)
	elif d in note_attributes:
	    if model[d]:
		if d == 'category':
		    note_text += attributes[d]['title'] + ': ' + ', '.join(cats) + '<br>'
		else:
		    note_text += attributes[d]['title'] + ': ' + model[d] + '<br>'
	elif d not in hidden_attributes:
	    dets.append(d)
    if pif.is_allowed('a'):  # pragma: no cover
        note_text += 'Import: %s, %s-%s<br>' % (model['imported'], model['imported_from'], model['imported_var'])
        note_text += 'Show: ' + pif.render.format_text_input("picture_id." + model['var'], 8, value=pic_id, also={'class': 'bggray' if pic_id else 'bgok'})
	if pic_id:
	    note_text += '<span class="warn">'
        for sz in mbdata.image_size_types:
            if os.path.exists(useful.relpath('.', config.IMG_DIR_VAR, sz + '_' + model['mod_id'] + '-' + model['var'] + '.jpg').lower()):
                note_text += sz.upper() + ' '
	if pic_id:
	    note_text += '</span>'
	else:
	    phcred = credits.get(('%(mod_id)s-%(var)s' % model).lower(), '')
	    note_text += '<div class="%s">Credit: ' % ('bgok' if phcred or pic_id else 'bgno')
	    note_text += pif.render.format_select("phcred." + model['var'], photogs, selected=phcred) + '</div>'
        note_text += "References:<br>" + pif.render.format_text_input("var_sel." + model['var'], 256, 24, value=model['references'], also={'class': 'bgok' if model['references'] else 'bgno'})

    ostr = '<center>'
    ostr += pif.render.format_link('?edit=1&mod=%s&var=%s' % (model['mod_id'], model['var']), model['var'].upper())
    if pif.is_allowed('a'):  # pragma: no cover
        ostr += '<br><input type="checkbox" name="v" value="%s"><br>' % model['var']
    #count_descs = reduce(lambda y, x: y + (1 if model[x] != '' else 0), desc_attributes, 0)
    count_descs = sum([int(len(model[x]) > 0) for x in desc_attributes])
    ostr += '<i class="fa fa-star %s"></i>' % (
	    'green' if count_descs == len(desc_attributes) else ('red' if not count_descs else 'orange'))
    ostr += '</center>'
    return {
        'ID': ostr,
        'Description': '<div class="varentry">' + model['text_description'] + '</div>\n' + '<br>'.join([
	    '<span class="%s">%s: %s</span>\n' % (
	    ("diff" if pif.is_allowed('a') and model[d] != prev.get(d, model[d]) else "same"),
	    attributes[d]['title'], model[d]) for d in descs]),
        'Details': '<br>'.join([
	    '<span class="%s">%s: %s</span>\n' % (
	    ("diff" if pif.is_allowed('a') and model[d] != prev.get(d, model[d]) else "same"),
	    attributes[d]['title'], model[d]) for d in dets if d in attributes]),
        'Picture': '<a href="%(_lnk)s">%(_picture)s</a>' % model,
        'Notes': note_text,
    }


class VarSearchForm(object):

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
	for attr in self.attributes:
	    if form.has(attr):
		self.attrq[attr] = form.search(attr)
	self.nots = {key: form.get_bool('not_' + key) for key in self.attributes}
	self.ci = form.get_bool('ci')
	self.c1 = form.get_bool('c1')
	self.cateq = form.get_str('category', '')
	self.with_pics = form.get_str('pic') != '0'
	self.without_pics = form.get_str('pic') != '1'
	self.varl = form.get_str("v")
	self.wheelq = form.get_str("var.wheels")
	self.sobj = form.search("var.s")
	self.is_list = form.has('list')
	self.is_detail = form.has('vdet')
	self.recalc = form.has('recalc')
	self.verbose = form.get_bool('verbose')
	self.codes = [1]
	if not self.c1:
	    self.codes.append(2)
	#useful.write_message(str(self.__dict__))
	return self

    def write(self, pif, values={}):
	pif.render.comment("attributes", self.attributes)

	entries = [{'title': self.attributes[x]['title'], 'value': pif.render.format_text_input(x, 64, 64)} for x in desc_attributes]
	entries.append({'title': '', 'value': pif.render.format_checkbox('ci', [(1, 'Case insensitive')])})
	lsections = [dict(columns=['title', 'value'], range=[{'entry': entries}], note='', noheaders=True, footer='<br>')]

	entries = []
	for key in sorted(set(self.attributes.keys()) - set(hidden_attributes) - set(desc_attributes)):
	    if key == 'category':
		cates = [('', '')] + [(x, mbdata.categories.get(x, x)) for x in values[key]]
		cates.sort(key=lambda x: x[1])
		value = pif.render.format_button_up_down_select(key, -1) + pif.render.format_select(key, cates, id=key) + \
			'&nbsp;' + pif.render.format_checkbox('c1', [(1, 'Code 1 only')])
	    elif not any(values.get(key, [])):
		continue
	    else:
		value = pif.render.format_button_up_down_select(key, -1) + \
			pif.render.format_select(key, [('', '')] + sorted(values[key]), id=key)
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
		     pif.render.format_button_reset('vars'),
	    'not': '&nbsp;'
	})

	lsections.append(dict(columns=['title', 'value', 'not'], range=[{'entry': entries}], note='', noheaders=True))
	return dict(section=lsections)

    def cate_match(self, model, code):
	category = model['_catlist'] = model.get('category', '').split()
	if not category:
	    category = ['MB']
	search_not = self.nots['category']
	modelcode = 2 if (set(mbdata.code2_categories) & set(category)) else 1
	retval = not code or (code == modelcode)
	if retval and self.cateq:
	    retval = (self.cateq in category) or (self.cateq == 'MB' and not category)
	    if search_not:
		retval = not retval
	return retval

    def wheel_match(self, var):
	return (not self.wheelq) or var['wheels'] == self.wheelq or var['text_wheels'] == self.wheelq

    def search_match(self, var):
	if not self.sobj:
	    return True
	for k in var:
	    if k in desc_attributes and useful.search_match(self.sobj, var[k]):
		return True
	return False

    def desc_match(self, var):
	if not self.attrq:
	    return True
	for attr in self.attrq:
	    var_val = var.get(attr, '')
	    query_val = ' '.join(self.attrq.get(attr, []))
	    if attr in desc_attributes:
		for obj in self.attrq[attr]:
		    if not self.ci and var[attr].find(obj) < 0:
			return False
		    if self.ci and var[attr].lower().find(obj.lower()) < 0:
			return False
	return True

    def field_match(self, var):
	if not self.attrq:
	    return True
	for attr in self.attrq:
	    search_not = self.nots[attr]
	    var_val = var.get(attr, '')
	    query_val = ' '.join(self.attrq.get(attr, []))
	    if attr == 'category':
		continue
	    elif attr in desc_attributes:
		continue
	    elif var_val == query_val and search_not:
		return False
	    elif var_val != query_val and not search_not:
		return False
	return True

    def model_match(self, model, code):
	    return ((not self.varl or (model['var'] in self.varl)) and
			(self.with_pics and model['_has_pic'] or self.without_pics and not model['_has_pic']) and
                        self.cate_match(model, code) and
                        self.search_match(model) and
                        self.wheel_match(model) and
			(not self.wheelq or var['wheels'] == self.wheelq or var['text_wheels'] == self.wheelq) and
                        self.desc_match(model) and
                        self.field_match(model))

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
	codes = [1]
	if not self.c1:
	    codes.append(2)
	for code in codes:
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
		    if key in desc_attributes:
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


def do_model(pif, vsform, mvars, display_type, photogs):
    llineup = {'id': 'vars', 'section': []}
    shown_columns = detail_columns if display_type == DISPLAY_TYPE_DETAIL else list_columns

    credits = {x['photo_credit.name'].lower(): x['photographer.id'] for x in pif.dbh.fetch_photo_credits_for_vars(path=config.IMG_DIR_VAR[1:], name=vsform.mod_id, verbose=False)}
    prev = {}
    for code in vsform.codes:
	lsec = {'id': 'code_%d dt_%s' % (code, display_type), 'name': 'Code %d Models' % code, 'range': list(), 'switch': code != 1,
            'headers': dict(zip(shown_columns, shown_columns)),
            'columns': 4 if display_type == DISPLAY_TYPE_GRID else shown_columns,
	}
	lran = {'id': 'ran', 'entry': []}
        for var_id in sorted(mvars.keys()):
            model = mvars[var_id]
            pif.render.comment(model)
            #model['references'] = ' '.join(list(set(vsform.selects.get(var_id, []))))
            if vsform.model_match(model, code):
                #model['area'] = ', '.join([mbdata.regions.get(x, x) for x in model.get('area', '').split(';')])
		model['link'] = '?mod=%s&var=%s' % (model['mod_id'], model['var'])
		model['categories'] =  ' - '.join([pif.render.format_image_art(mbdata.cat_arts.get(x), desc=mbdata.categories.get(x, x)) for x in model['_catlist']])
		lran['entry'].append(do_var(pif, display_type, model, vsform.attributes, prev, credits, photogs))
		prev = model

	lran['styles'] = {'Description': 'lefty'}
	if len(lran['entry']):
	    lsec['count'] = '%d entries' % len(lran['entry']) if len(lran['entry']) > 1 else '1 entry'
	    if display_type == DISPLAY_TYPE_GRID:
		while len(lran['entry']) < 4:
		    lran['entry'].append({'text': '', 'class': 'blank'})
	    lsec['range'].append(lran)
	    llineup['section'].append(lsec)

    if display_type == DISPLAY_TYPE_GRID:
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
    photogs = [('', '')] + [(x['photographer.id'], x['photographer.name']) for x in pif.dbh.get_photographers()]
    display_type = DISPLAY_TYPE_LIST if vsform.is_list else DISPLAY_TYPE_DETAIL if vsform.is_detail else DISPLAY_TYPE_GRID;
    llineup = do_model(pif, vsform, mvars, display_type, photogs)
    img = pif.render.format_image_required(mod_id, largest=mbdata.IMG_SIZ_MEDIUM, pdir=config.IMG_DIR_MAN)
    phcred = pif.dbh.fetch_photo_credit('.' + config.IMG_DIR_MAN, mod_id)
    phcred = phcred.get('photographer.id', '') if phcred else ''

    footer = pif.render.format_button_input('list')
    if pif.is_allowed('a'):  # pragma: no cover
	footer += pif.render.format_button_input('save')
	footer += pif.render.format_button("add", 'vars.cgi?edit=1&mod=%s&add=1' % mod_id)
	footer += pif.render.format_button("casting", pif.dbh.get_editor_link('casting', {'id': mod_id}))
	footer += pif.render.format_button("recalc", '?recalc=1&mod=%s' % mod_id)
	if display_type == DISPLAY_TYPE_LIST:
	    img += '<div class="%s">Credit: ' % ('bgok' if phcred or pic_id else 'bgno')
	    img += pif.render.format_select("phcred", photogs, selected=phcred) + '</div>'
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
        man = pif.dbh.fetch_casting(man_id)
        if not man:
            man = pif.dbh.fetch_casting_by_alias(man_id)
    if not man:
        man_id = var = ''
    elif var:
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
        promote_picture(pif, man_id, var)
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
    ostr += '   <a href="%(link)s">%(img)s<br><b>%(casting.name)s</b></a>\n' % mdict
    #ostr += "   <br><i>%(v.text_description)s</i>\n" % mdict
    ostr += '<table class="vartable">'
    ostr += '<tr><td class="varentry"><i>%s</i></td></tr>' % mdict['v.text_description']
    ostr += "</table>"
    ostr += "  </center></td></tr></table></center>\n"
    return ostr


vfields = {'base': 'text_base', 'body': 'text_body', 'interior': 'text_interior', 'wheels': 'text_wheels', 'windows': 'text_windows', 'cat': 'category', 'date': 'date', 'area': 'area'}
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
    lsec = pif.dbh.depref('section', pif.dbh.fetch_sections({'page_id': pif.page_id})[0])
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


#       'columns': ['mod_id', 'var', 'flags',
#           'text_description', 'text_base', 'text_body', 'text_interior', 'text_wheels', 'text_windows',
#           'base', 'body', 'interior', 'windows',
#           'manufacture', 'category', 'area', 'date', 'note', 'picture_id', 'imported', 'imported_from', 'imported_var'],
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

    
def list_variations(pif, mod_id=None, *args, **kwargs):
    if not mod_id:
	return
    for variation in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
	pif.render.message('%5s: %s' % (variation['var'], variation['text_description']))

    
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


def command_help(pif, *args):
    pif.render.message("./vars.py [d|r|c|s|m|i|v] ...")
    pif.render.message("  d for delete: mod_id var_id")
    pif.render.message("  a for add: mod_id var_id body")
    pif.render.message("  r for rename: mod_id old_var_id new_var_id")
    pif.render.message("  c for copy: mod_id old_var_id new_var_id")
    pif.render.message("  s for swap: mod_id var_id_1 var_id_2")
    pif.render.message("  m for move: old_mod_id old_var_id new_mod_id [new_var_id]")
    pif.render.message("  i for info: fields mod_id var_id")
    pif.render.message("  v for value: mod_id var_id-or-default-or-all attribute value")
    pif.render.message("  l for list: mod_id")


command_lookup = {
    'd': delete_variation,
    'a': add_variation,
    'r': rename_variation,
    'c': copy_variation,
    's': swap_variations,
    'm': move_variation,
    'f': run_search_command,
    'i': info,
    'v': add_value,
    'l': list_variations,
}


@basics.command_line
def commands(pif):
    if pif.filelist:
	command_lookup.get(pif.filelist[0], command_help)(pif, *pif.filelist[1:])
    else:
	command_help(pif)


if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='')
