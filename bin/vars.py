#!/usr/local/bin/python

import copy, glob, os, re

import basics
import config
import mbdata
import models
import useful


note_attributes = ['manufacture', 'area', 'category', 'date', 'note', 'from_CY_number']
desc_attributes = ['text_description', 'text_base', 'text_body', 'text_interior', 'text_wheels', 'text_windows']
hidden_attributes = ['mod_id', 'var', 'picture_id', 'other', 'references', 'imported', 'imported_from', 'imported_var', 'flags']
detail_attributes = ['base', 'body', 'interior', 'windows']

list_columns = ['ID', 'Description', 'Details', 'Picture', 'Notes']

DISPLAY_TYPE_GRID = 1
DISPLAY_TYPE_LIST = 2

fieldwidth_re = re.compile(r'\w+\((?P<w>\d+)\)')

# ----- display single variation --------------------------

def single_variation(pif, man, var_id):
    mod_id = id = man['id']
    vsform = VarSearchForm(pif, mod_id)
    #pif.render.title = mod_id + ': ' + man['name']
    print pif.render.format_head(extra=pif.render.reset_button_js + pif.render.increment_select_js)
    print '<table width="100%"><tr>'

    content = pif.render.format_link('vars.cgi?mod=%s' % mod_id, "See All") + '<br>'
    if pif.is_allowed('a'):  # pragma: no cover
        content += ' - ' + pif.render.format_link('vars.cgi?mod=%s&var=%s&delete=1' % (mod_id, var_id), "Delete") + '<br>'
        content += pif.render.format_link('vars.cgi?mod=%s&var=%s&edit=1' % (mod_id, var_id), "Edit") + '<br>'
        content += pif.render.format_link('upload.cgi?d=%s&m=%s&v=%s&l=1' % (os.path.join(config.LIB_MAN_DIR, mod_id.lower()), mod_id, var_id), "Pictures") + '<br>'
        content += pif.render.format_link('?mod=%s&var=%s&rmpic=1' % (mod_id, var_id), "Remove Pictures") + '<br>'
        content += pif.render.format_link(pif.dbh.get_editor_link('casting', {'id': mod_id}), "Casting") + '<br>'
        content += pif.render.format_link('?recalc=1&mod=%s' % mod_id, "Recalc") + '<br>'
    if pif.is_allowed('u'):  # pragma: no cover
        content += ' - ' + pif.render.format_link('upload.cgi?d=' + os.path.join(config.LIB_MAN_DIR, mod_id.lower()), "Upload") + '<br>'
    #content += pif.render.format_link(pif, 'man=%s&var=%s' % (id, var_id))
    print models.add_left_bar(pif, '', man['id'], man['vehicle_type'], 4, content)
    print models.add_banner(pif, pif.render.title)
    print '<tr><td>'
    print '<center>'

    variation = pif.dbh.depref('variation', pif.dbh.fetch_variation(mod_id, var_id))
    if not variation:  # pragma: no cover
        return
    variation = variation[0]
    print '<center>'

    pic_var = variation['picture_id'] if variation['picture_id'] else variation['var']
    img = pif.render.format_image_required(variation['mod_id'], vars=pic_var, pdir=pif.render.pic_dir, largest=mbdata.IMG_SIZ_HUGE)
    if pif.is_allowed('u'):  # pragma: no cover
        print '<a href="upload.cgi?d=%s&m=%s&v=%s">' % (os.path.join(config.LIB_MAN_DIR, id.lower()), id, pic_var) + img + '</a>'
    else:
        print '<a href="upload.cgi?m=%s&v=%s">%s</a>' % (id, var_id, img)
    print '<p>'
    print '<table class="vartable" style="width: auto;">'
    print '<tr><td class="varentry"><i>%s</i></td></tr>' % variation['text_description']
    print "</table>"
    print '<p></center>'

    variation['area'] = ', '.join([mbdata.regions.get(x, x) for x in variation.get('area', '').split(';')])
    data = variation.keys() + filter(lambda d: d not in variation, vsform.attributes)
    hdrs = {x: x for x in variation}
    data.sort()

    print '<center>'

    llistix = dict(id='single')
    lsec = {'columns': ['title', 'value'],
	'headers': {'title': 'Title', 'value': 'Value'},
	'range': list(),
    }
    ranges = [
	{'name': 'Description Texts', 'id': 'det', '_attrs': desc_attributes[1:]},
	{'name': 'Individual Attributes', 'id': 'det', '_attrs': [d for d in data if not (d in desc_attributes or d in note_attributes or d in hidden_attributes)]},
	{'name': 'Notes', 'id': 'det', '_attrs': note_attributes},
    ]

    for lran in ranges:
	lran['entry'] = show_details(pif, lran['_attrs'], vsform.attributes, variation, id=lran['id'])
	lsec['range'].append(lran)

    llistix['section'] = [lsec]
    print pif.render.format_listix(llistix)

    print '<p><center><b><a href="upload.cgi?m=%s&v=%s">Upload a Picture</a></b></center>' % (mod_id, var_id)

    print '<p>'
    print appearances(pif, mod_id, var_id, pics=True)

    print '<p>'
    print models.show_adds(pif, mod_id, var_id)

    print '<tr><td class="bottombar">'
    print pif.render.format_button_comment(pif, 'man=%s&var_id=%s' % (mod_id, var_id))
    print '</td></tr></table>'


def appearances(pif, mod_id, var_id, pics=False):
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

def show_detail(pif, field, attributes, variation, edit=False, id=''):
    return {
	'field': field,
	'title': attributes[field]['title'],
	'value': variation.get(field, ''),
	'new': pif.render.format_text_input(field + "." + variation['var'], 
	    int(fieldwidth_re.search(attributes[field]['definition']).group('w')) \
		if '(' in attributes[field]['definition'] else 20,
	    64, value=variation.get(field, ''))
    }


def show_details(pif, data, attributes, variation, id=''):
    return [show_detail(pif, d, attributes, variation, id=id) for d in data if d in variation]


def show_variation_editor(pif, id, var_id):
    vsform = VarSearchForm(pif, id)
    man = pif.dbh.fetch_casting(id)
    if not man:
        raise useful.SimpleError("That casting was not found.")
    pif.render.title = man['id'] + ': ' + man['name']
    mod_id = man['id']

    variation = pif.dbh.depref('variation', pif.dbh.fetch_variation(mod_id, var_id))
    if not variation:
        raise useful.SimpleError("That variation was not found.")
    print pif.render.format_head(extra=pif.render.reset_button_js + pif.render.increment_select_js)
    variation = variation[0]
    print '<center>Variation %s<p>' % variation['var'].upper()

    pic_var = variation['picture_id'] if variation['picture_id'] else variation['var']
    img = ''
    if pif.is_allowed('a'):  # pragma: no cover
        img += pif.render.format_image_required(variation['mod_id'], pdir=pif.render.pic_dir, vars=pic_var, nobase=True, prefix=mbdata.IMG_SIZ_TINY)
        img += pif.render.format_image_required(variation['mod_id'], pdir=pif.render.pic_dir, vars=pic_var, nobase=True, prefix=mbdata.IMG_SIZ_SMALL)
        img += pif.render.format_image_required(variation['mod_id'], pdir=pif.render.pic_dir, vars=pic_var, nobase=True, prefix=mbdata.IMG_SIZ_MEDIUM)
        img += pif.render.format_image_required(variation['mod_id'], pdir=pif.render.pic_dir, vars=pic_var, nobase=True, prefix=mbdata.IMG_SIZ_LARGE)
    else:
        img += pif.render.format_image_required(variation['mod_id'], pdir=pif.render.pic_dir, vars=pic_var, nobase=True, largest=mbdata.IMG_SIZ_HUGE)
    if pif.is_allowed('u'):  # pragma: no cover
        print '<a href="upload.cgi?d=%s&m=%s&v=%s">' % (os.path.join(config.LIB_MAN_DIR, id.lower()), id, var_id) + img + '</a>'
    else:
        print '<a href="upload.cgi?m=%s&v=%s">%s</a>' % (id, var_id, img)
    print '<p></center>'

    print '<form action="vars.cgi" name="vars" method="post">'

    variation['references'] = ' '.join(list(set(vsform.selects.get(var_id, []))))
    variation['area'] = ', '.join([mbdata.regions.get(x, x) for x in variation.get('area', '').split(';')])
    data = variation.keys()
    for key in vsform.attributes:
	variation.setdefault(key, '')
        if key not in data:
            data.append(key)
    hdrs = {x: x for x in variation.keys()}
    data.sort()

    llistix = dict()
    lsec = {'columns': ['title', 'value'],
	'headers': {'title': 'Title', 'value': 'Value', 'field': 'Field', 'new': 'New'},
	'range': list(),
    }
    id_attributes = ['mod_id', 'var']
    if pif.is_allowed('a'):  # pragma: no cover
	lsec['columns'] = ['field', 'title', 'value', 'new']
        id_attributes.extend(['picture_id', 'imported_var', 'imported_from', 'references'])
    ranges = [
	{'name': 'Identification Attributes', 'id': 'det', '_attrs': id_attributes},
	{'name': 'Individual Attributes', 'id': 'det', '_attrs': [d for d in data if not (d in desc_attributes or d in note_attributes or d in hidden_attributes)]},
	{'name': 'Notes', 'id': 'det', '_attrs': note_attributes},
    ]

    for lran in ranges:
	lran['entry'] = show_details(pif, lran['_attrs'], vsform.attributes, variation, id=lran['id'])
	lsec['range'].append(lran)
    lsec['range'][0]['entry'].append({'field': '', 'title': 'Move pictures to', 'value': '',
	    'new': pif.render.format_text_input("repic." + variation['var'], 16, 16)})

    llistix['section'] = [lsec]
    print pif.render.format_listix(llistix)

    print appearances(pif, mod_id, var_id)

    print '<p>'
    print '<input type="hidden" name="page" value="%s">' % pif.page_id
    print '<input type="hidden" name="mod" value="%s">' % mod_id
    print '<input type="hidden" name="ovar" value="%s">' % var_id
    if pif.is_allowed('a'):  # pragma: no cover
        print pif.render.format_button_input('save')
        print pif.render.format_button_reset('vars')
        print pif.render.format_button("delete", 'vars.cgi?mod=%s&var=%s&delete=1' % (mod_id, var_id))
        print pif.render.format_button("remove_picture", 'vars.cgi?mod=%s&var=%s&rmpic=1' % (mod_id, var_id))
        print pif.render.format_button("promote", '?mod=%s&var=%s&promote=1' % (mod_id, var_id))
        print pif.render.format_button("casting", pif.dbh.get_editor_link('casting', {'id': mod_id}))
        print pif.render.format_button("recalc", '?recalc=1&mod=%s' % mod_id)
    if pif.is_allowed('u'):  # pragma: no cover
        print pif.render.format_button("upload", 'upload.cgi?d=' + os.path.join(config.LIB_MAN_DIR, mod_id.lower()))
        #print pif.render.format_button("pictures", 'traverse.cgi?d=./lib/%s' % mod_id.lower())
        print pif.render.format_button("pictures", 'upload.cgi?d=%s&m=%s&v=%s&l=1&c=%s+variation+%s' % (os.path.join(config.LIB_MAN_DIR, mod_id.lower()), mod_id, var_id, mod_id, var_id))
    #print pif.render.format_button("comment_on_this_page", link='../pages/comment.php?page=%s&man=%s&var=%s' % (pif.page_id, id, var_id), also={'class': 'comment'}, lalso={})
    print pif.render.format_button_comment(pif, 'man=%s&var=%s' % (id, var_id))
    print '</form>'
    print '<hr>'


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
                print 'repic', repic, '<br>'
            elif attr == 'picture_id':
                if pif.form.get_str(key) != var_id:
                    var_dict[attr] = pif.form.get_str(key)
            elif 'id' in attributes.get(attr, {}):
                det_dict[attr] = pif.form.get_str(key)
            else:
                var_dict[attr] = pif.form.get_str(key)
        if 'from_CY_number' in var_dict and 'from_CY_number' not in attributes:
            del var_dict['from_CY_number']
        print '<p>', det_dict, '<p>', var_dict
        if var_id != var_dict['var']:
            rename_variation(pif, var_dict['mod_id'], var_id, var_dict['var'])
        pif.dbh.write('variation', var_dict)
        for attr in det_dict:
            pif.dbh.write('detail', {'mod_id': var_dict['mod_id'], 'var_id': var_dict['var'], 'attr_id': str(attributes[attr]['id']), 'description': det_dict[attr]})
        if var_sel:
            print 'varsel', var_sel, '<br>'
            pif.dbh.update_variation_selects(mod_id, var_dict['var'], var_sel.split())
        if repic:
            rename_variation_pictures(pif, mod_id, var_dict['var'], mod_id, repic)
    else:
        save_model(pif, mod_id)
    pif.dbh.recalc_description(mod_id)
    man = pif.dbh.fetch_casting(mod_id)
    show_model(pif, man)


def add_variation(pif, mod_id, var_id='unset', attributes={}):  # pragma: no cover
    pif.dbh.insert_variation(mod_id, var_id, attributes)


def move_variation(pif, old_mod_id, old_var_id, new_mod_id, new_var_id, *args, **kwargs):  # pragma: no cover
    verbose = False
    if pif.argv:
        print 'move_variation', old_mod_id, old_var_id, new_mod_id, new_var_id
        pif.dbh.dbi.verbose = verbose = True
    if old_mod_id == new_mod_id and old_var_id == new_var_id:
	print 'no change'
        return
    pif.dbh.update_variation({'mod_id': new_mod_id, 'var': new_var_id, 'imported_var': new_var_id}, {'mod_id': old_mod_id, 'var': old_var_id}, verbose=verbose)
    pif.dbh.update_variation({'picture_id': ''}, {'mod_id': old_mod_id, 'picture_id': old_var_id}, verbose=verbose)

    # This will take some work.
    old_attrs = pif.dbh.depref('attribute', pif.dbh.fetch_attributes(old_mod_id))
    old_attrs = {x['attribute_name']: x for x in old_attrs}
    new_attrs = pif.dbh.depref('attribute', pif.dbh.fetch_attributes(new_mod_id))
    new_attrs = {x['attribute_name']: x for x in new_attrs}
    print old_attrs
    print new_attrs
    details = pif.dbh.fetch_details(old_mod_id, old_var_id, nodefaults=True).get(old_var_id, {})
    for detail in details:
	if detail in new_attrs:
	    new_att_id = new_attrs[detail]['id']
	    old_att_id = old_attrs[detail]['id']
	    pif.dbh.update_detail({'attr_id': new_att_id, 'mod_id': new_mod_id, 'var_id': new_var_id},
		{'attr_id': old_att_id, 'mod_id': old_mod_id, 'var_id': old_var_id})
	else:
	    print 'cannot transfer %s="%s"' % (detail, details[detail])

    pif.dbh.write('variation_select', {'mod_id': new_mod_id, 'var_id': new_var_id}, where="var_id='%s' and mod_id='%s'" % (old_var_id, old_mod_id), modonly=True, verbose=verbose)
    rename_variation_pictures(pif, old_mod_id, old_var_id, new_mod_id, new_var_id)


def copy_variation(pif, mod_id, old_var_id, new_var_id, *args, **kwargs):  # pragma: no cover
    verbose = False
    if pif.argv:
        print 'copy_variation', mod_id, old_var_id, new_var_id
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
        print 'rename_variation', mod_id, old_var_id, new_var_id
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
        print "rename", old_pic, new_pic, "<br>"
        os.rename(old_pic, new_pic)


def promote_picture(pif, mod_id, var_id):  # pragma: no cover
    print 'promoting picture for var', var_id, '<br>'
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
        print "delete", pic, "<br>"
        os.unlink(pic)


def delete_variation(pif, mod_id=None, var_id=None, *args, **kwargs):  # pragma: no cover
    if mod_id and var_id:
	pif.dbh.delete_variation({'mod_id': mod_id, 'var': var_id})
	pif.dbh.delete_detail({'mod_id': mod_id, 'var_id': var_id})
	pif.dbh.delete_variation_select({'mod_id': mod_id, 'var_id': var_id})

# ----- multiple variation page ---------------------------

def do_var(pif, model, attributes, prev):
    keys = model.keys()
    keys.sort()
    pic_id = model['picture_id']

    descs = list()
    dets = list()
    notes = list()
    for d in keys:
	if d.startswith('_') or d == 'text_description' or not model[d]:
	    pass
	elif d in desc_attributes:
	    descs.append(d)
	elif d in note_attributes:
	    notes.append(d)
	elif d not in hidden_attributes:
	    dets.append(d)

    row = dict()

    ostr = '<center>'
    ostr += pif.render.format_link('?edit=1&mod=%s&var=%s' % (model['mod_id'], model['var']), model['var'].upper())
    if pif.is_allowed('a'):  # pragma: no cover
        ostr += '<br><input type="checkbox" name="v" value="%s"><br>' % model['var']
    #count_descs = reduce(lambda y, x: y + (1 if model[x] != '' else 0), desc_attributes, 0)
    count_descs = sum([int(bool(x)) for x in desc_attributes])
    ostr += pif.render.format_image_art(
	    'stargreen.gif' if count_descs == len(desc_attributes) else ('starred.gif' if not count_descs else 'starorange.gif'))
    ostr += '</center>'
    row['ID'] = ostr
    row['Description'] = '<div class="varentry">' + model['text_description'] + '</div>\n' + '<br>'.join([
	    '<span class="%s">%s: %s</span>\n' % (
	    ("diff" if pif.is_allowed('a') and model[d] != prev.get(d, model[d]) else "same"),
	    attributes[d]['title'], model[d]) for d in descs])
    row['Details'] = '<br>'.join([
	    '<span class="%s">%s: %s</span>\n' % (
	    ("diff" if pif.is_allowed('a') and model[d] != prev.get(d, model[d]) else "same"),
	    attributes[d]['title'], model[d]) for d in dets])
    row['Picture'] = '<a href="%(_lnk)s">%(_picture)s</a>' % model

    cats = [mbdata.categories.get(x, x) for x in model['_catlist']]
    ostr = ''
    for d in keys:
        if d not in note_attributes or not model[d]:
            pass
        elif d == 'category':
            ostr += attributes[d]['title'] + ': ' + ', '.join(cats) + '<br>'
        else:
            ostr += attributes[d]['title'] + ': ' + model[d] + '<br>'
    if pif.is_allowed('a'):  # pragma: no cover
        ostr += 'Import: %s, %s-%s<br>' % (model['imported'], model['imported_from'], model['imported_var'])
        ostr += 'Show: ' + pif.render.format_text_input("picture_id." + model['var'], 8, value=pic_id)
	if pic_id:
	    print '<span class="warn">'
        for sz in mbdata.image_size_types:
            if os.path.exists(os.path.join(config.IMG_DIR_VAR, sz + '_' + model['mod_id'] + '-' + model['var'] + '.jpg').lower()):
                ostr += sz.upper() + ' '
	if pic_id:
	    print '</span>'
        ostr += "<br>References:<br>" + pif.render.format_text_input("var_sel." + model['var'], 256, 24, value=model['references'])
    row['Notes'] = ostr
    return row


def do_var_grid(pif, model):
    ostr = pif.render.format_link('?mod=%s&var=%s' % (model['mod_id'], model['var']),
        model['var'].upper() + '<br>' +
        '<center><table><tr><td class="spicture">' + model['_picture'] + '</td></tr></table></center>')
    ostr += '<table class="vartable">'
    ostr += '<tr><td class="varentry"><i>%s</i></td></tr>' % model['text_description']
    ostr += "</table>"
    ostr += ', '.join([mbdata.categories.get(x, x) for x in model['_catlist']])
    return {'text': ostr}


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
	self.attrs = {key: form.get_str(key) for key in self.attributes.keys()}
	self.attrq = dict()
	for attr in self.attributes:
	    if form.has(attr):
		self.attrq[attr] = form.search(attr)
	self.nots = {key: form.get_bool('not_' + key) for key in self.attributes.keys()}
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
	keys = self.attributes.keys()
	keys.sort()
	ostr = pif.render.format_table_start()
	for key in keys:
	    if key not in desc_attributes:
		continue
	    ostr += pif.render.format_row_start()
	    ostr += pif.render.format_cell(0, self.attributes[key]['title'])
	    ostr += pif.render.format_cell(1, pif.render.format_text_input(key, 64, 64))
	    ostr += pif.render.format_row_end()
	ostr += pif.render.format_row_start()
	ostr += pif.render.format_cell(0)
	ostr += pif.render.format_cell(1, pif.render.format_checkbox('ci', [(1, 'Case insensitive')]))
	ostr += pif.render.format_row_end()
	ostr += pif.render.format_table_end()
	ostr += '<br>'
	ostr += pif.render.format_table_start()
	for key in keys:
	    if key in hidden_attributes or key in desc_attributes:
		continue
	    #pif.render.comment(key)
	    ostr += pif.render.format_row_start()
	    ostr += pif.render.format_cell(0, self.attributes[key]['title'])
	    if key == 'category':
		cates = [('', '')] + [(x, mbdata.categories.get(x, x)) for x in values[key]]
		cates.sort(key=lambda x: x[1])
		pulldown = pif.render.format_button_up_down_select(key, -1) + pif.render.format_select(key, cates, id=key)
		pulldown += '&nbsp;' + pif.render.format_checkbox('c1', [(1, 'Code 1 only')])
		ostr += pif.render.format_cell(1, pulldown)
	    elif values.get(key):
		values[key].sort()
		ostr += pif.render.format_cell(1, pif.render.format_button_up_down_select(key, -1) +
			pif.render.format_select(key, [('', '')] + values[key], id=key))
	    else:
		ostr += pif.render.format_cell(1, pif.render.format_text_input(key, 64, 64))
	    ostr += pif.render.format_cell(1, pif.render.format_checkbox('not_' + key, [(1, 'not')]))
	    ostr += pif.render.format_row_end()

	if pif.is_allowed('a') and isinstance(values.get('imported_from'), list):  # pragma: no cover
	    ostr += pif.render.format_row_start()
	    ostr += pif.render.format_cell(0, self.attributes['imported_from']['title'])
	    values['imported_from'].sort()
	    ostr += pif.render.format_cell(1, pif.render.format_button_up_down_select('imported_from', -1) +
			pif.render.format_select('imported_from', [('', '')] + values['imported_from'], id='imported_from') +
			pif.render.format_checkbox('pic', [(1, 'with pictures'), (0, 'without pictures')]))
	    ostr += pif.render.format_cell(1, pif.render.format_checkbox('not_imported_from', [(1, 'not')]))
	    ostr += pif.render.format_row_end()

	ostr += pif.render.format_row_start()
	ostr += pif.render.format_cell(0, '&nbsp;')
	ostr += pif.render.format_cell_start(1)
	ostr += pif.render.format_button_input("filter", "submit")
	if pif.is_allowed('a'):  # pragma: no cover
	    ostr += pif.render.format_button_input("list")
	ostr += pif.render.format_button_reset('vars')
	ostr += pif.render.format_cell_end()
	ostr += pif.render.format_cell(1, '&nbsp;')
	ostr += pif.render.format_row_end()
	ostr += pif.render.format_table_end()
	return ostr

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
	if self.varl:
	    print 'Selected models'
	else:
	    print 'All models'
	if self.cateq:
	    print 'in', mbdata.categories.get(self.cateq, self.cateq)
	if self.wheelq:
	    print 'with', self.wheelq, "wheels"
	if self.attrq:
	    print 'matching search'

    def make_values(self, mvars):
	values = dict()
	wheels = list()

	cates = set()
	codes = [1]
	if not self.c1:
	    codes.append(2)
	for code in codes:
	    for key in mvars.keys():
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

    var_ids = mvars.keys()
    var_ids.sort()
    prev = dict()
    for code in vsform.codes:
	lsec = {'id': 'code_%d' % code, 'name': 'Code %d Models' % code, 'range': list(), 'switch': code != 1}
	lran = {'id': 'ran', 'entry': []}
        if display_type == DISPLAY_TYPE_GRID:
            lsec.update({'columns': 4})
        elif display_type == DISPLAY_TYPE_LIST:
            lsec.update({'columns': list_columns, 'headers': dict(zip(list_columns, list_columns))})
        for var_id in var_ids:
            model = mvars[var_id]
            pif.render.comment(model)
            #model['references'] = ' '.join(list(set(vsform.selects.get(var_id, []))))
            if vsform.model_match(model, code):
                #model['area'] = ', '.join([mbdata.regions.get(x, x) for x in model.get('area', '').split(';')])
                if display_type == DISPLAY_TYPE_GRID:
                    ent = do_var_grid(pif, model)
                elif display_type == DISPLAY_TYPE_LIST:
                    ent = do_var(pif, model, vsform.attributes, prev)
		    prev = model
		if ent:
		    lran['entry'].append(ent)

	if len(lran['entry']):
	    if display_type == DISPLAY_TYPE_GRID:
		if len(lran['entry']) > 1:
		    lsec['count'] = '%d entries' % len(lran['entry'])
		else:
		    lsec['count'] = '1 entry'
		while len(lran['entry']) < 4:
		    lran['entry'].append({'text': '', 'class': 'blank'})
	    lsec['range'].append(lran)
	    llineup['section'].append(lsec)

    if display_type == DISPLAY_TYPE_GRID:
        print pif.render.format_matrix(llineup)
    elif display_type == DISPLAY_TYPE_LIST:
        print pif.render.format_listix(llineup)


def update_values(var, values):
    for key in var:
        if key in desc_attributes:
            continue
        values.setdefault(key, [])
        newvalue = var[key]
        if not newvalue:
            newvalue = ''
        if newvalue not in values[key]:
            values[key].append(newvalue)
    return values


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
    id = model['id']
    vsform = VarSearchForm(pif, id).read(pif.form)
    if vsform.recalc:
        pif.dbh.recalc_description(id)
    #pif.render.title = id + ': ' + model['name']
    print pif.render.format_head(extra=pif.render.reset_button_js + pif.render.increment_select_js + pif.render.toggle_display_js)
    #print model, '<br>'

    cates = {'MB'}
    mvars = dict()
    for variation in pif.dbh.depref('variation', pif.dbh.fetch_variations(id)):
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

    vsform = VarSearchForm(pif, id).read(pif.form)
    values = vsform.make_values(mvars)

    print '<table width=100%><tr><td class="title">' + pif.render.title + '</td></tr></table><p>'
    #print '<h2>' + model['name'] + '</h2>'
    #print '<h3>%s</h3>' % '-'.join(parse_model(id)).upper()
    print '<center>'
    print pif.render.format_image_required(id, largest=mbdata.IMG_SIZ_MEDIUM, pdir=config.IMG_DIR_MAN)
    print '</center><br>'
    vsform.show_search_object()

    print '<form action="vars.cgi" name="vars" method="post">'
    if vsform.verbose:
        print '<input type="hidden" name="verbose" value="1">'

    do_model(pif, vsform, mvars, DISPLAY_TYPE_LIST if vsform.is_list else DISPLAY_TYPE_GRID)

    print '<p style="font-weight: bold; font-size: large;">'
    print pif.render.format_button_input_visibility("varsearch", True)
    print 'Search Variations</p>'
    print '<div id="varsearch"><input type="hidden" name="page" value="%s">' % pif.page_id
    print '<input type="hidden" name="mod" value="%s">' % id

    values['category'] = list(cates)

    print vsform.write(pif, values)
    print '</div><hr>'
    print pif.render.format_button_input('list')
    if pif.is_allowed('a'):  # pragma: no cover
        print pif.render.format_button_input('save')
        print pif.render.format_button("add", 'vars.cgi?edit=1&mod=%s&add=1' % id)
        print pif.render.format_button("casting", pif.dbh.get_editor_link('casting', {'id': id}))
        print pif.render.format_button("recalc", '?recalc=1&mod=%s' % id)
    if pif.is_allowed('u'):  # pragma: no cover
        print pif.render.format_button("upload", 'upload.cgi?d=' + os.path.join(config.LIB_MAN_DIR, id.lower()) + '&m=' + id)
        print pif.render.format_button("pictures", 'traverse.cgi?d=%s' % os.path.join(config.LIB_MAN_DIR, id.lower()))
    #print pif.render.format_button("comment_on_this_page", link='../pages/comment.php?page=%s&man=%s&var=%s' % (pif.page_id, id, varl), also={'class': 'comment'}, lalso={})
    print pif.render.format_button_comment(pif, 'man=%s&var=%s' % (id, vsform.varl))
    print '</form>'
    print '<hr>'


@basics.web_page
def main(pif):
    id = pif.form.get_str('mod')
    var = pif.form.get_str('var')

    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/single.cgi', 'By ID')
    pif.render.hierarchy_append('/cgi-bin/single.cgi?id=%s' % id, id)
    pif.render.hierarchy_append('/cgi-bin/vars.cgi?mod=%s' % id, 'Variations')
    if var:
	pif.render.hierarchy_append('/cgi-bin/vars.cgi?mod=%s&var=%s' % (id, var), var)
    pif.render.print_html()

    regs = mbdata.get_countries()
    regs.update(mbdata.regions)
    man = dict()
    if id:
        man = pif.dbh.fetch_casting(id)
        if not man:
            man = pif.dbh.fetch_casting_by_alias(id)
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

    if pif.form.has("add"):
        add_variation(pif, id, 'unset', {'imported_from': 'web'})
        show_variation_editor(pif, id, 'unset')
    elif pif.form.has('edit'):
        show_variation_editor(pif, id, pif.form.get_str('var'))
    elif pif.form.has("rmpic"):
        remove_picture(pif, id, var)
        single_variation(pif, man, var)
    elif pif.form.has("promote"):
        promote_picture(pif, id, var)
        single_variation(pif, man, var)
    elif pif.form.has("delete"):
        delete_variation(pif, id, var)
        show_model(pif, man)
    elif pif.form.has("save"):
	var = pif.form.get_str('ovar')
        save(pif, id, var)
    elif var:
        single_variation(pif, man, var)
    elif id:
        show_model(pif, man)
    else:
        raise useful.SimpleError("Can't find requested information.  Please try something else.")
    print pif.render.format_tail()

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
    else:
        return var_search(pif)


def var_search_ask(pif):
    id = pif.form.get_str('id')
    model = pif.dbh.fetch_casting(id)

    #pif.render.title = model['id'] + ': ' + model['name']
    if not model:
        raise useful.SimpleError("That is not a recognized model ID.")

    ostr = pif.render.format_head(extra=pif.render.reset_button_js + pif.render.increment_select_js + pif.render.toggle_display_js)
    vsform = VarSearchForm(pif, id).read(pif.form)
    ostr += '<form action="vars.cgi" name="vars" method="post">'
    if vsform.verbose:
        ostr += '<input type="hidden" name="verbose" value="1">'
    ostr += '<input type="hidden" name="page" value="vars">'
    ostr += '<input type="hidden" name="mod" value="%s">' % id

    mvars = {var['var']: var for var in pif.dbh.depref('variation', pif.dbh.fetch_variations(id))}
    ostr += vsform.write(pif, vsform.make_values(mvars))

    ostr += '<hr>'
    if pif.is_allowed('a'):  # pragma: no cover
        ostr += pif.render.format_button_input("list")
    ostr += pif.render.format_button_comment(pif, 'man=%s' % id)
    ostr += '</form>'
    ostr += '<hr>'
    return ostr


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

    pif.render.format_button_comment(pif, 'casting=%s&base=%s&body=%s&interior=%s&wheels=%s&windows=%s' % (pif.form.get_str('casting'), pif.form.get_str('base'), pif.form.get_str('body'), pif.form.get_str('interior'), pif.form.get_str('wheels'), pif.form.get_str('windows')))
    return pif.render.format_template('simplematrix.html', llineup=llineup)


#       'columns': ['mod_id', 'var', 'flags',
#           'text_description', 'text_base', 'text_body', 'text_interior', 'text_wheels', 'text_windows',
#           'base', 'body', 'interior', 'windows',
#           'manufacture', 'category', 'area', 'date', 'note', 'other', 'picture_id', 'imported', 'imported_from', 'imported_var'],
def run_search_command(pif, args):
    mods = pif.dbh.fetch_variations(args[0])
    mods.sort(key=lambda x: x['variation.var'])
    for mod in mods:
        print '%(mod_id)-8s|%(var)-5s|%(imported_from)-8s|%(text_description)-s' % pif.dbh.depref('variation', mod)


def info(pif, fields=None, mod_id=None, var_id=None, *args, **kwargs):
    if not mod_id:
	return
    fields = fields.split(',') if (fields and fields != '.') else []
    if var_id:
	for variation in pif.dbh.depref('variation', pif.dbh.fetch_variation(mod_id, var_id)):
	    if fields:
		print '|'.join([str(variation[f]) for f in fields])
	    else:
		print '|'.join([str(variation[f]) for f in sorted(variation.keys())])
    else:
	for variation in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
	    if fields:
		print '|'.join([str(variation[f]) for f in fields])
	    else:
		print '|'.join([str(variation[f]) for f in sorted(variation.keys())])


def command_help(pif, *args):
    print "./vars.py [d|r|c|s|m|i] ..."
    print "  d for delete: mod_id var_id"
    print "  r for rename: mod_id old_var_id new_var_id"
    print "  c for copy: mod_id old_var_id new_var_id"
    print "  s for swap: mod_id var_id_1 var_id_2"
    print "  m for move: old_mod_id old_var_id new_mod_id [new_var_id]"
    print "  i for info: fields mod_id var_id"


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
