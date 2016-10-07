#!/usr/local/bin/python

import copy, glob, os, re

import basics
import config
import mbdata
import models
import useful


id_attributes = ['mod_id', 'var', 'picture_id', 'imported_var', 'imported_from', 'references', '_repic']
note_attributes = ['manufacture', 'area', 'category', 'date', 'note', 'from_CY_number']
desc_attributes = ['text_description', 'text_base', 'text_body', 'text_interior', 'text_wheels', 'text_windows']
hidden_attributes = ['mod_id', 'var', 'picture_id', 'other', 'references', 'imported', 'imported_from', 'imported_var', 'flags']
detail_attributes = ['base', 'body', 'interior', 'windows']

list_columns = ['ID', 'Description', 'Details', 'Picture', 'Notes']

DISPLAY_TYPE_GRID = 1
DISPLAY_TYPE_LIST = 2

fieldwidth_re = re.compile(r'\w+\((?P<w>\d+)\)')

# ----- display single variation --------------------------

def show_variation_editor(pif, man, var_id, edit=False):
    edit = edit and pif.is_allowed('a')
    if not man:
        raise useful.SimpleError("That casting was not found.")
    mod_id = man['id']

    variation = pif.dbh.depref('variation', pif.dbh.fetch_variation(mod_id, var_id))
    if not variation:
        raise useful.SimpleError("That variation was not found.")
    variation = variation[0]
    vsform = VarSearchForm(pif, mod_id)
    pdir = pif.render.pic_dir

    left_bar_content = ''
    if pif.is_allowed('a'):  # pragma: no cover
	left_bar_content += pif.render.format_link('vars.cgi?mod=%s' % mod_id, "See All") + '<br>'
        #left_bar_content += pif.render.format_link('vars.cgi?mod=%s&var=%s&delete=1' % (mod_id, var_id), "Delete") + '<br>'
	if edit:
	    left_bar_content += pif.render.format_link('vars.cgi?mod=%s&var=%s' % (mod_id, var_id), "See") + '<br>'
	else:
	    left_bar_content += pif.render.format_link('vars.cgi?mod=%s&var=%s&edit=1' % (mod_id, var_id), "Edit") + '<br>'
	left_bar_content += pif.render.format_link('upload.cgi?d=%s&m=%s&v=%s&l=1&c=%s+variation+%s' % (os.path.join(config.LIB_MAN_DIR, mod_id.lower()), mod_id, var_id, mod_id, var_id), 'Pictures') + '<br>'
        #left_bar_content += pif.render.format_link('?mod=%s&var=%s&rmpic=1' % (mod_id, var_id), "Remove Pictures") + '<br>'
        left_bar_content += pif.render.format_link(pif.dbh.get_editor_link('casting', {'id': mod_id}), "Casting") + '<br>'
        left_bar_content += pif.render.format_link('?recalc=1&mod=%s' % mod_id, "Recalc") + '<br>'
    if pif.is_allowed('u'):  # pragma: no cover
        left_bar_content += pif.render.format_link('upload.cgi?d=' + os.path.join(config.LIB_MAN_DIR, mod_id.lower()), "Upload") + '<br>'

    footer = ''
    if edit:
	footer += pif.render.format_button_input('save')
	footer += pif.render.format_button_reset('vars')
	footer += pif.render.format_button("delete", 'vars.cgi?mod=%s&var=%s&delete=1' % (mod_id, var_id))
	footer += pif.render.format_button("remove_picture", 'vars.cgi?mod=%s&var=%s&rmpic=1' % (mod_id, var_id))
	footer += pif.render.format_button("promote", '?mod=%s&var=%s&promote=1' % (mod_id, var_id))

    pic_var = variation['picture_id'] if variation['picture_id'] else variation['var']
    img = ''.join([
        pif.render.format_image_required(mod_id, pdir=pdir, vars=pic_var, nobase=True, prefix=s)
	for s in [mbdata.IMG_SIZ_TINY, mbdata.IMG_SIZ_SMALL, mbdata.IMG_SIZ_MEDIUM, mbdata.IMG_SIZ_LARGE]
    ]) if edit else pif.render.format_image_required(mod_id, pdir=pdir, vars=pic_var, nobase=True, largest=mbdata.IMG_SIZ_HUGE)

    variation['references'] = ' '.join(list(set(vsform.selects.get(var_id, []))))
    variation['area'] = ', '.join([mbdata.regions.get(x, x) for x in variation.get('area', '').split(';')])
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
	    {'name': 'Individual Attributes', 'id': 'det', '_attrs': [d for d in data if not (d in desc_attributes or d in note_attributes or d in hidden_attributes)]},
	    {'name': 'Notes', 'id': 'det', '_attrs': note_attributes},
	])
    for lran in ranges:
	lran['entry'] = show_details(pif, lran['_attrs'], vsform.attributes, variation, ran_id=lran['id'])
    lsec['range'] = ranges
    llistix = {'id': 'single', 'section': [lsec]}

    appearances = show_appearances(pif, mod_id, var_id, pics=True)
    adds = models.show_adds(pif, mod_id, var_id)
    upload = 'upload.cgi?m=%s&v=%s' % (mod_id, var_id) + (
	'd=%s' % os.path.join(config.LIB_MAN_DIR, mod_id.lower())
	if pif.is_allowed('u') else '')

    # ------- render ------------------------------------

    pif.render.set_page_extra(pif.render.reset_button_js + pif.render.increment_select_js)
    pif.render.set_button_comment(pif, 'man=%s&var_id=%s' % (mod_id, var_id))
    context = {
	'title': pif.render.title,
	'note': '',
	'type_id': '',
	'base_id': man['id'],
	'vehicle_type': man['vehicle_type'],
	'rowspan': '4',
	'left_bar_content': left_bar_content,
	'description': variation['text_description'],
	'image': img,
	'llistix': llistix,
	'appearances': appearances,
	'adds': adds,
	'upload': upload,
	'edit': edit,
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

def show_detail(pif, field, attributes, variation, edit=False, ran_id=''):
    if field == '_repic':
	return {'field': '', 'title': 'Move pictures to', 'value': '',
		'new': pif.render.format_text_input("repic." + variation['var'], 16, 16)}
    return {
	'field': field,
	'title': attributes[field]['title'],
	'value': variation.get(field, ''),
	'new': pif.render.format_text_input(field + "." + variation['var'], 
	    int(fieldwidth_re.search(attributes[field]['definition']).group('w')) \
		if '(' in attributes[field]['definition'] else 20,
	    64, value=variation.get(field, ''))
    }


def show_details(pif, data, attributes, variation, ran_id=''):
    return [show_detail(pif, d, attributes, variation, ran_id=ran_id) for d in data if d in variation]


def save(pif, mod_id, var_id):
    if var_id:
        var_sel = repic = ''
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
            elif attr == 'repic':
                repic = pif.form.get_str(key)
                pif.render.message('repic', repic, '<br>')
            elif attr == 'picture_id':
                if pif.form.get_str(key) != var_id:
                    var_dict[attr] = pif.form.get_str(key)
            elif 'id' in attributes.get(attr, {}):
                det_dict[attr] = pif.form.get_str(key)
            else:
                var_dict[attr] = pif.form.get_str(key)
        if 'from_CY_number' in var_dict and 'from_CY_number' not in attributes:
            del var_dict['from_CY_number']
        pif.render.message('<p>', det_dict, '<p>', var_dict)
        if var_id != var_dict['var']:
            rename_variation(pif, var_dict['mod_id'], var_id, var_dict['var'])
        pif.dbh.write('variation', var_dict)
        for attr in det_dict:
            pif.dbh.write('detail', {'mod_id': var_dict['mod_id'], 'var_id': var_dict['var'], 'attr_id': str(attributes[attr]['id']), 'description': det_dict[attr]})
        if var_sel:
            pif.render.message('varsel', var_sel, '<br>')
            pif.dbh.update_variation_selects(mod_id, var_dict['var'], var_sel.split())
        if repic:
            rename_variation_pictures(pif, mod_id, var_dict['var'], mod_id, repic)
    else:
        save_model(pif, mod_id)
    pif.dbh.recalc_description(mod_id)


def add_variation(pif, mod_id, var_id='unset', attributes={}):  # pragma: no cover
    pif.dbh.insert_variation(mod_id, var_id, attributes)


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
    patt1 = os.path.join(config.IMG_DIR_VAR, '?_%s-%s.*' % (old_mod_id.lower(), old_var_id.lower()))
    patt2 = os.path.join(config.IMG_DIR_VAR, '%s-%s.*' % (old_mod_id.lower(), old_var_id.lower()))
    pics = glob.glob(patt1.lower()) + glob.glob(patt2.lower())
    for old_pic in pics:
        new_pic = old_pic.replace('-%s.' % old_var_id.lower(), '-%s.' % new_var_id.lower())
        new_pic = new_pic.replace('_%s-' % old_mod_id.lower(), '_%s-' % new_mod_id.lower())
        pif.render.comment("rename", old_pic, new_pic)
        pif.render.message("rename", old_pic, new_pic, "<br>")
        os.rename(old_pic, new_pic)


def promote_picture(pif, mod_id, var_id):  # pragma: no cover
    pif.render.message('promoting picture for var', var_id, '<br>')
    for pic in glob.glob(config.IMG_DIR_VAR + '/?_%s-%s.*' % (mod_id.lower(), var_id.lower())):
        ofn = pic[pic.rfind('/') + 1:]
        nfn = ofn[:ofn.find('-')] + ofn[ofn.find('.'):]
        useful.file_copy(pic, config.IMG_DIR_MAN + '/' + nfn)


def remove_picture(pif, mod_id, var_id):  # pragma: no cover
    patt1 = config.IMG_DIR_VAR + '/?_%s-%s.*' % (mod_id, var_id)
    patt2 = config.IMG_DIR_VAR + '/%s-%s.*' % (mod_id, var_id)
    pics = glob.glob(patt1.lower()) + glob.glob(patt2.lower())
    for pic in pics:
        pif.render.comment("delete", pic)
        pif.render.message("delete", pic, "<br>")
        os.unlink(pic)


def delete_variation(pif, mod_id=None, var_id=None, *args, **kwargs):  # pragma: no cover
    if mod_id and var_id:
	pif.dbh.delete_variation({'mod_id': mod_id, 'var': var_id})
	pif.dbh.delete_detail({'mod_id': mod_id, 'var_id': var_id})
	pif.dbh.delete_variation_select({'mod_id': mod_id, 'var_id': var_id})

# ----- multiple variation page ---------------------------

def do_var(pif, model, attributes, prev):
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
        note_text += 'Show: ' + pif.render.format_text_input("picture_id." + model['var'], 8, value=pic_id)
	if pic_id:
	    note_text += '<span class="warn">'
        for sz in mbdata.image_size_types:
            if os.path.exists(os.path.join(config.IMG_DIR_VAR, sz + '_' + model['mod_id'] + '-' + model['var'] + '.jpg').lower()):
                note_text += sz.upper() + ' '
	if pic_id:
	    note_text += '</span>'
        note_text += "<br>References:<br>" + pif.render.format_text_input("var_sel." + model['var'], 256, 24, value=model['references'])

    ostr = '<center>'
    ostr += pif.render.format_link('?edit=1&mod=%s&var=%s' % (model['mod_id'], model['var']), model['var'].upper())
    if pif.is_allowed('a'):  # pragma: no cover
        ostr += '<br><input type="checkbox" name="v" value="%s"><br>' % model['var']
    #count_descs = reduce(lambda y, x: y + (1 if model[x] != '' else 0), desc_attributes, 0)
    count_descs = sum([int(bool(x)) for x in desc_attributes])
    ostr += pif.render.format_image_art(
	    'stargreen.gif' if count_descs == len(desc_attributes) else ('starred.gif' if not count_descs else 'starorange.gif'))
    ostr += '</center>'
    row = {
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

    return row


class VarSearchForm(object):

    def __init__(self, pif, mod_id):
	self.page_id = pif.page_id
	self.mod_id = mod_id
	attributes = {x['attribute_name']: x for x in pif.dbh.depref('attribute', pif.dbh.fetch_attributes(mod_id))}
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
	    if var_sel['sub_id']:
		selects[var_sel['var_id']].append(var_sel['ref_id'] + '/' + var_sel['sub_id'])
	    else:
		selects[var_sel['var_id']].append(var_sel['ref_id'])
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
	self.recalc = form.has('recalc')
	self.verbose = form.get_bool('verbose')
	self.codes = [1]
	if not self.c1:
	    self.codes.append(2)
	return self

    def write(self, pif, values={}):
	pif.render.comment("attributes", self.attributes)

	entries = [{'title': self.attributes[x]['title'], 'value': pif.render.format_text_input(x, 64, 64)} for x in desc_attributes]
	entries.append({'title': '', 'value': pif.render.format_checkbox('ci', [(1, 'Case insensitive')])})
	lsections = [dict(columns=['title', 'value'], range=[{'entry': entries}], note='', noheaders=True, footer='<br>')]

	entries = []
	for key in sorted(set(self.attributes.keys()) - set(hidden_attributes) - set(desc_attributes)):
	    #pif.render.comment(key)
	    if key == 'category':
		cates = [('', '')] + [(x, mbdata.categories.get(x, x)) for x in values[key]]
		cates.sort(key=lambda x: x[1])
		value = pif.render.format_button_up_down_select(key, -1) + pif.render.format_select(key, cates, id=key) + \
			'&nbsp;' + pif.render.format_checkbox('c1', [(1, 'Code 1 only')])
	    elif values.get(key):
		value = pif.render.format_button_up_down_select(key, -1) + \
			pif.render.format_select(key, [('', '')] + sorted(values[key]), id=key)
	    else:
		value = pif.render.format_text_input(key, 64, 64)
	    entries.append({
		'title': self.attributes[key]['title'],
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


def do_model(pif, vsform, mvars, display_type):
    llineup = {'id': 'vars', 'section': []}

    prev = {}
    for code in vsform.codes:
	lsec = {'id': 'code_%d' % code, 'name': 'Code %d Models' % code, 'range': list(), 'switch': code != 1,
            'headers': dict(zip(list_columns, list_columns)),
            'columns': list_columns if display_type == DISPLAY_TYPE_LIST else 4,
	}
	lran = {'id': 'ran', 'entry': []}
        for var_id in sorted(mvars.keys()):
            model = mvars[var_id]
            pif.render.comment(model)
            #model['references'] = ' '.join(list(set(vsform.selects.get(var_id, []))))
            if vsform.model_match(model, code):
                #model['area'] = ', '.join([mbdata.regions.get(x, x) for x in model.get('area', '').split(';')])
		model['link'] = '?mod=%s&var=%s' % (model['mod_id'], model['var'])
		model['categories'] =  ', '.join([mbdata.categories.get(x, x) for x in model['_catlist']])
		lran['entry'].append(
                    do_var(pif, model, vsform.attributes, prev) if display_type == DISPLAY_TYPE_LIST else model
		)
		prev = model

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


def save_model(pif, id):
    for key in pif.form.keys(start='picture_id.'):
        if key[11:] == pif.form.get_str(key):
            pif.dbh.update_variation({'picture_id': pif.form.get_str(key)}, {'mod_id': id, 'var': ''})
        else:
            pif.dbh.update_variation({'picture_id': pif.form.get_str(key)}, {'mod_id': id, 'var': key[11:]})
    for key in pif.form.keys(start='var_sel.'):
        varsel = list(set(pif.form.get_str(key).split()))
        pif.dbh.update_variation_selects(id, key[8:], varsel)


def show_model(pif, model):
    if not model:
        raise useful.SimpleError("That is not a recognized model ID.")
    mod_id = model['id']
    vsform = VarSearchForm(pif, mod_id).read(pif.form)
    if vsform.recalc:
        pif.dbh.recalc_description(mod_id)

    cates = {'MB'}
    mvars = dict()
    for variation in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
	variation['_catlist'] = variation.get('category', '').split()
	cates.update(variation['_catlist'])
	pic_id = variation['picture_id']

        img = pif.render.find_image_path([variation['mod_id']], nobase=True, vars=pic_id if pic_id else variation['var'], prefix=mbdata.IMG_SIZ_SMALL)
	variation['_has_pic'] = bool(img)
        variation['_picture'] = pif.render.fmt_img_src(img) if img else pif.render.fmt_no_pic(True, mbdata.IMG_SIZ_SMALL)

	if pif.is_allowed('u'):  # pragma: no cover
	    variation['_dir'] = os.path.join(config.LIB_MAN_DIR, variation['mod_id'].lower())
	    variation['_lnk'] = 'upload.cgi?d=%(_dir)s&m=%(mod_id)s&v=%(var)s' % variation
	else:
	    variation['_dir'] = config.INC_DIR
	    variation['_lnk'] = 'upload.cgi?m=%(mod_id)s&v=%(var)s' % variation
	mvars[variation['var']] = variation

    vsform = VarSearchForm(pif, mod_id).read(pif.form)
    values = vsform.make_values(mvars)
    values['category'] = list(cates)
    llineup = do_model(pif, vsform, mvars, DISPLAY_TYPE_LIST if vsform.is_list else DISPLAY_TYPE_GRID)
    img = pif.render.format_image_required(mod_id, largest=mbdata.IMG_SIZ_MEDIUM, pdir=config.IMG_DIR_MAN)

    footer = pif.render.format_button_input('list')
    if pif.is_allowed('a'):  # pragma: no cover
	footer += pif.render.format_button_input('save')
	footer += pif.render.format_button("add", 'vars.cgi?edit=1&mod=%s&add=1' % mod_id)
	footer += pif.render.format_button("casting", pif.dbh.get_editor_link('casting', {'id': mod_id}))
	footer += pif.render.format_button("recalc", '?recalc=1&mod=%s' % mod_id)
    if pif.is_allowed('u'):  # pragma: no cover
	footer += pif.render.format_button("upload", 'upload.cgi?d=' + os.path.join(config.LIB_MAN_DIR, mod_id.lower()) + '&m=' + mod_id)
	footer += pif.render.format_button("pictures", 'traverse.cgi?d=%s' % os.path.join(config.LIB_MAN_DIR, mod_id.lower()))

    # ------- render ------------------------------------

    pif.render.set_page_extra(pif.render.reset_button_js + pif.render.increment_select_js + pif.render.toggle_display_js)
    pif.render.set_button_comment(pif, 'man=%s&var=%s' % (mod_id, vsform.varl))
    context = {
	'image': img,
	'llineup': llineup,
	'footer': footer,
	'search_object': vsform.show_search_object(),
	'verbose': vsform.verbose,
	'show_as_list': vsform.is_list,
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
        add_variation(pif, man_id, var, {'imported_from': 'web'})
	edit = True
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


vfields = {'base': 'text_base', 'body': 'text_body', 'interior': 'text_interior', 'wheels': 'text_wheels', 'windows': 'text_windows', 'cat': 'category', 'date': 'date'}
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

    pif.render.set_page_extra(pif.render.reset_button_js + pif.render.increment_select_js + pif.render.toggle_display_js)
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
#           'manufacture', 'category', 'area', 'date', 'note', 'other', 'picture_id', 'imported', 'imported_from', 'imported_var'],
def run_search_command(pif, args):
    mods = pif.dbh.fetch_variations(args[0])
    mods.sort(key=lambda x: x['variation.var'])
    for mod in mods:
        pif.render.message('%(mod_id)-8s|%(var)-5s|%(imported_from)-8s|%(text_description)-s' % pif.dbh.depref('variation', mod))


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
    pif.render.message("./vars.py [d|r|c|s|m|i] ...")
    pif.render.message("  d for delete: mod_id var_id")
    pif.render.message("  r for rename: mod_id old_var_id new_var_id")
    pif.render.message("  c for copy: mod_id old_var_id new_var_id")
    pif.render.message("  s for swap: mod_id var_id_1 var_id_2")
    pif.render.message("  m for move: old_mod_id old_var_id new_mod_id [new_var_id]")
    pif.render.message("  i for info: fields mod_id var_id")


command_lookup = {
    'd': delete_variation,
    'r': rename_variation,
    'c': copy_variation,
    's': swap_variations,
    'm': move_variation,
    'f': run_search_command,
    'i': info,
}


@basics.command_line
def commands(pif):
    if pif.filelist:
	command_lookup.get(pif.filelist[0], command_help)(pif, *pif.filelist[1:])
    else:
	command_help()


if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='')
