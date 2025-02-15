#!/usr/local/bin/python

import csv
import filecmp
import glob
from io import StringIO
import json
import os
import sys

import basics
import config
import imglib
import mbdata
import mbmods
import render
import useful


id_attributes = ['mod_id', 'var', 'picture_id', 'imported_var', 'imported_from', 'references', '_repic', '_credit']
note_attributes = ['area', 'date', 'note', 'category']
internal_desc_attributes = ['description', 'base', 'body', 'deco', 'interior', 'wheels', 'windows']
desc_attributes = ['description', 'base', 'body', 'interior', 'wheels', 'windows', 'with', 'text']
text_attributes = ['text_var'] + ['text_' + x for x in desc_attributes]
hidden_attributes = id_attributes + ['imported', 'flags', 'variation_type', 'logo_type', 'deco_type']
detail_attributes = ['base', 'body', 'deco', 'interior', 'wheels', 'windows']
base_attributes = ['additional_text', 'base_name', 'base_number', 'base_scale', 'tool_id', 'company_name', 'copyright',
                   'production_id', 'manufacture', 'base_reads']
system_attributes = ['_any', '_catdefs', '_categories', '_catlist', '_code', '_copy_base_from', '_credit',
                     '_dir', '_has_pic', '_lnk', '_picture', '_repic']
not_individual_attributes = (text_attributes + note_attributes + hidden_attributes + base_attributes +
                             system_attributes + ['vs', 'link', 'categories'])
internal_attributes = (['mod_id', 'var', 'picture_id', 'imported_var', 'imported_from'] + note_attributes +
                       internal_desc_attributes + hidden_attributes + detail_attributes + base_attributes)
form_attributes = note_attributes + detail_attributes + base_attributes + ['logo_type']

list_columns = ['ID', 'Description', 'Details', 'Picture']
detail_columns = ['ID', 'Description', 'Ty', 'Cat', 'Date', 'Ver', 'Im', 'Or', 'Cr', 'Pic', 'L', 'M', 'S', 'T', 'Lo',
                  'Ba', 'Bo', 'In', 'Wh', 'Wi', 'W/', 'BT']


# ----- display single variation --------------------------


def single_variation_left_bar(pif, variation, edit):
    mod_id = variation['mod_id']
    var_id = variation['var']
    libdir = useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower())
    left_bar_content = ''
    if pif.is_allowed('a'):  # pragma: no cover
        left_bar_content += (
            # pif.ren.format_link('vars.cgi?mod=%s&var=%s&delete=1' % (mod_id, var_id), "Delete") + '<br>' +
            (pif.ren.format_link(f'vars.cgi?mod={mod_id}&var={var_id}', "See") if edit else
             pif.ren.format_link(f'vars.cgi?mod={mod_id}&var={var_id}&edt=1', "Edit")) + '<br>' +
            pif.ren.format_link(f'upload.cgi?d={libdir}&m={mod_id}&v={var_id}&l=1&c={mod_id}+variation+{var_id}',
                                'Pictures') + '<br>' +
            # pif.ren.format_link('?mod=%s&var=%s&rmpic=1' % (mod_id, var_id), "Remove Pictures") + '<br>' +
            pif.ren.format_link(pif.dbh.get_editor_link('casting', {'id': mod_id}), "Casting") + '<br>' +
            pif.ren.format_link(f'?recalc=1&mod={mod_id}', "Recalc") + '<br>' +
            pif.ren.format_link(
                f'traverse.cgi?g=1&d={libdir}&man={mod_id}&var={var_id}', "Select") + '<br>')
    if pif.is_allowed('u'):  # pragma: no cover
        left_bar_content += pif.ren.format_link('upload.cgi?d=' + libdir, "Upload") + '<br>'

    if pif.is_allowed('a'):
        if variation['flags'] & config.FLAG_MODEL_VARIATION_VERIFIED:
            left_bar_content += '<br>' + pif.ren.fmt_check('white')
            if variation['flags'] & config.FLAG_MODEL_ID_INCORRECT:
                left_bar_content += '<br>' + pif.ren.fmt_x('red')
        if variation['date']:
            for fn in sorted(glob.glob(f'lib/docs/mbusa/{variation["date"]}-?.png')):
                left_bar_content += '<br>' + pif.ren.format_link('/' + fn, fn[fn.rfind('/') + 1:])
    return left_bar_content


def show_single_variation(pif, man, var_id, edit=False, addnew=False):
    pif.ren.print_html()
    edit = edit and pif.is_allowed('a')
    if not man:
        raise useful.SimpleError("That casting was not found.")
    categories = {x.id: x for x in pif.dbh.fetch_categories()}
    mod_id = man['id']
    man.setdefault('_catdefs', dict())
    libdir = useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower())

    varrecs, detrecs = pif.dbh.fetch_variation_deconstructed(mod_id, var_id, nodefaults=False)
    if varrecs:
        variation = pif.dbh.depref('variation', varrecs[0])
        variation = mangle_variation(pif, None, variation, categories)
        for attr, det in detrecs.get(var_id, {}).items():
            if not variation.get(attr):
                variation[attr] = det
    elif addnew:
        variation = {x: '' for x in pif.dbh.get_table_data('variation').columns}
        variation['var'] = var_id
        variation['mod_id'] = mod_id
    else:
        raise useful.SimpleError("That variation was not found.")
    attr_pics = {x['attribute.attribute_name']: x
                 for x in pif.dbh.depref('attribute_picture', pif.dbh.fetch_attribute_pictures(mod_id))}
    for attr in pif.dbh.fetch_attributes(mod_id):
        variation.setdefault(attr['attribute.attribute_name'], '')
    vsform = VarSearchForm(pif, mod_id)
    pdir = pif.ren.pic_dir

    left_bar_content = single_variation_left_bar(pif, variation, edit)

    footer = ''
    if edit:
        footer += pif.form.put_button_input('save')
        footer += pif.form.put_button_reset('vars')
        footer += pif.ren.format_button_link("delete", f'vars.cgi?mod={mod_id}&var={var_id}&delete=1')
        footer += pif.ren.format_button_link("remove_picture", f'vars.cgi?mod={mod_id}&var={var_id}&rmpic=1')
        footer += pif.ren.format_button_link("promote", f'editor.cgi?mod={mod_id}&var={var_id}&promote=1')

    # photogs = [('', '')] + [(x.photographer.id, x.photographer.name) for x in pif.dbh.fetch_photographers()]
    # hide private?
    photogs = [(x.photographer.id, x.photographer.name) for x in pif.dbh.fetch_photographers(config.FLAG_ITEM_HIDDEN)]
    pic_var = variation['picture_id'] if variation['picture_id'] else variation['var']
    picture_variation = None
    img = ''.join([
        pif.ren.format_image_required(mod_id, pdir=pdir, vars=pic_var, nobase=True, prefix=s)
        for s in [mbdata.IMG_SIZ_TINY, mbdata.IMG_SIZ_SMALL, mbdata.IMG_SIZ_MEDIUM, mbdata.IMG_SIZ_LARGE]
    ]) if edit else pif.ren.format_image_required(
        mod_id, pdir=pdir, vars=pic_var, nobase=True, largest=mbdata.IMG_SIZ_HUGE)
    var_img_credit = pif.dbh.fetch_photo_credit('.' + config.IMG_DIR_VAR, mod_id, pic_var, verbose=True)
    variation['_credit'] = var_img_credit['photographer.id'] if var_img_credit else ''
    var_img_credit = pif.ren.format_credit(var_img_credit)

    variation['references'] = ' '.join(list(set(vsform.selects.get(var_id, []))))
    variation['area'] = ', '.join([
        mbdata.get_countries().get(x, mbdata.areas.get(x, x)) for x in variation.get('area', '').split(';')])
    data = sorted(list(variation.keys()) + [d for d in vsform.attributes if d not in variation])

    lsec = render.Section(colist=['title', 'value'], id='single')
    shown_attributes = [d for d in data if d not in not_individual_attributes]
    if edit:
        lsec.headers = {'title': 'Title', 'value': 'Value', 'field': 'Field', 'new': 'New', 'pic': 'Picture Var'}
        lsec.colist = ['field', 'title', 'value', 'new']
        if variation['picture_id']:
            lsec.colist.append('pic')
            picture_variation = pif.dbh.depref('variation', pif.dbh.fetch_variation(mod_id, variation['picture_id']))
        ranges = [render.Range(name='Identification Attributes', id='det')]
        ranges[0]._attrs = id_attributes
        base_attributes.extend(['logo_type', '_copy_base_from'])
    else:
        lsec.headers = {'title': 'Title', 'value': 'Value'}
        lsec.colist = ['title', 'value']
        ranges = [render.Range(name='Description Texts', id='det')]
        ranges[0]._attrs = text_attributes[2:]
        variation['text_base'] += (' ' + ' '.join([
            pif.ren.format_image_icon('l_base-' + x, mbdata.base_logo_dict.get(x)) for x in variation['logo_type']]))
    ran1 = render.Range(name='Individual Attributes', id='det')
    ran1._attrs = shown_attributes
    ran2 = render.Range(name='Information on Base', id='det')
    ran2._attrs = base_attributes
    ran3 = render.Range(name='Notes', id='det')
    ran3._attrs = note_attributes
    ranges.extend([ran1, ran2, ran3])
    for lran in ranges:
        lran.entry = show_details(
            pif, lran._attrs, vsform.attributes, man, variation, attr_pics, ran_id=lran.id, photogs=photogs,
            picture_var=picture_variation)
    lsec.range = ranges
    llistix = render.Listix(id='single', section=[lsec])
    llistix.dump()

    appearances = show_appearances(pif, mod_id, var_id, pics=True)
    adds = mbmods.show_adds(pif, mod_id, var_id)
    upload = f'upload.cgi?m={mod_id}&v={var_id}' + (f'&d={libdir}' if pif.is_allowed('u') else '')

    # ------- render ------------------------------------

    pif.ren.set_page_extra(pif.ren.reset_button_js + pif.ren.increment_select_js + pif.ren.modal_js)
    pif.ren.set_button_comment(pif, f'man={mod_id}&var_id={var_id}')
    context = {
        'title': pif.ren.title,
        'note': '',
        'type_id': '',
        'base_id': man['id'],
        'icon_id': mod_id if os.path.exists(
            useful.relpath('.', config.IMG_DIR_MAN_ICON, 'i_' + mod_id.lower() + '.gif')) else '',
        'vehicle_type': [mbdata.model_icons.get(x) for x in man['vehicle_type']] + [
            categories[x].image for x in variation['_catlist'] if categories[x].image],
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
    return pif.ren.format_template('var.html', **context)


def show_appearances(pif, mod_id, var_id, pics=False):
    varsel = pif.dbh.fetch_variation_selects(mod_id, var_id)
    appears = []
    for vs in varsel:
        if vs.ref_id.startswith('matrix.'):
            if vs.sec_id:
                appears.append(pif.ren.format_link(
                    f"matrix.cgi?page={vs.ref_id}#{vs.sec_id}", vs.page_info.title))
            else:
                appears.append(pif.ren.format_link(f"matrix.cgi?page={vs.ref_id}", vs.page_info.title))
        elif vs.ref_id.startswith('packs.'):
            # bugly.  for 2packs, this doesn't work so we have to work around it.
            if not vs.pack.id:
                pack_id, pack_var = vs.sec_id.split('-') if '-' in vs.sec_id else (vs.sec_id, '')
                pack = pif.dbh.fetch_pack(pack_id, pack_var)
                if pack:
                    vs.receive(pack[0])
            appears.append(pif.ren.format_link(f"packs.cgi?page={vs.pack.page_id}&id={vs.pack.id}" + (
                                               '#' + vs.pack.var if vs.pack.var else ''),
                           "%(page_info.title)s: %(base_id.rawname)s (%(base_id.first_year)s)" % vs))
        elif vs.ref_id.startswith('playset.'):
            appears.append(pif.ren.format_link(
                f"play.cgi?page={vs.pack.page_id}&id={vs.pack.id}",
                "%(page_info.title)s: %(base_id.rawname)s (%(base_id.first_year)s)" % vs))
        elif vs.ref_id.startswith('year.') and vs.lineup_model.region:
            vs['region'] = mbdata.regions.get(vs.lineup_model.region, 'Worldwide')
            # if not vs.lineup_model.get('region'):
            #     vs.lineup_model['region'] = 'W'
            if vs.get('lineup_model.region', '').startswith('X'):
                vs['region'] = 'Worldwide'
                vs.lineup_model.number = 'S' + vs.lineup_model.region.replace('.', '')
                vs.lineup_model.region = 'U'
                appears.append(pif.ren.format_link(
                    "lineup.cgi?year=%(lineup_model.year)s&region=%(lineup_model.region)s#%(lineup_model.number)s" % vs,
                    "%(lineup_model.year)s %(region)s lineup" % vs))
            elif vs.lineup_model.region == 'W' and vs.lineup_model.year > '1970':
                appears.append(pif.ren.format_link(
                    "lineup.cgi?year=%(lineup_model.year)s&region=U#%(lineup_model.number)s" % vs,
                    "%(lineup_model.year)s United States lineup lineup number %(lineup_model.number)s" % vs))
                appears.append(pif.ren.format_link(
                    "lineup.cgi?year=%(lineup_model.year)s&region=R#%(lineup_model.number)s" % vs,
                    "%(lineup_model.year)s Rest of World lineup lineup number %(lineup_model.number)s" % vs))
            elif not vs.sec_id or vs.sec_id == vs.get('lineup_model.region'):
                appears.append(pif.ren.format_link(
                    "lineup.cgi?year=%(lineup_model.year)s&region=%(lineup_model.region)s#%(lineup_model.number)s" % vs,
                    "%(lineup_model.year)s %(region)s lineup number %(lineup_model.number)s" % vs))
        elif vs.ref_id.startswith('pub.'):
            appears.append(pif.ren.format_link(f'pub.cgi?id={vs.sec_id}', vs.pub.rawname))
        elif vs.ref_id == 'code2':
            appears.append(
                pif.ren.format_link('code2.cgi?section=' + vs.sec_id, vs.page_info.title + ' - ' + vs.section.name))
        elif not vs.get('ref_id', ''):
            if (vs.get('category.flags') or 0) & config.FLAG_CATEGORY_INDEXED:
                appears.append(pif.ren.format_link("cats.cgi?cat=%(category.id)s" % vs, vs['category.name']))
        elif pif.is_allowed('a'):  # pragma: no cover
            appears.append('<i>ref_id = ' + str(vs.ref_id) +
                           (' / sec_id = ' + str(vs.sec_id)) if vs.sec_id else '' + f"<br>(vs = {vs})</i>\n")
    if appears:
        return "<b>Appearances</b>\n<ul>\n" + ''.join(['<li>' + x + '\n' for x in appears]) + '</ul>\n'
    return ''


# ----- variation editor ----------------------------------


def show_detail(pif, field, attributes, model, variation, attr_pics={}, ran_id='', photogs=[], picture_var=None):
    if field.startswith('variation.'):  # not sure where this is coming from.
        field = field[10:]
    if field == '_copy_base_from':
        return {'field': '', 'title': 'Copy base info from', 'value': '',
                'new': pif.form.put_text_input("cpbas." + variation['var'], 16, 16)}
    if field == '_repic':
        return {'field': '', 'title': 'Move pictures to', 'value': '',
                'new': pif.form.put_text_input("repic." + variation['var'], 16, 16)}
    if field == '_credit':
        return {'field': '', 'title': 'Credit', 'value': '',
                'new': pif.form.put_select(
                    "phcred." + variation['var'], photogs, selected=variation.get('_credit', ''), blank='')}
    if field in ('vs', 'link', 'categories') or field.startswith('_'):
        useful.write_comment('show_detail not writing', field)
        return {}
    title = attributes.get(field, {}).get('title', '')
    value = variation.get(field, '')
    if field == 'category':
        # cates = sorted(list(set(value.split() + variation['_catlist'])))
        # value = '<br>'.join([model['_catdefs'].get(x, {}).get('name', x) for x in cates])
        value = variation['categories']
    # modals = ''
    title_modal = show_detail_modal(pif, attr_pics.get(field, {}), variation['mod_id'])
    if title_modal:
        title += ' ' + pif.ren.fmt_mini(icon="circle-question", family="regular",
                                        also=f"onclick=\"init_modal('m.{field}')\";", alsoc='modalbutton')
        title += pif.ren.format_modal('m.' + field, title_modal)
    value_modal = show_detail_modal(pif, attr_pics.get(field, {}), variation['mod_id'], variation['var'])
    if value_modal:
        value += ' ' + pif.ren.fmt_mini(icon="circle-question", family="regular",
                                        also=f"onclick=\"init_modal('v.{field}');\"", alsoc='modalbutton')
        value += pif.ren.format_modal('v.' + field, value_modal)
    pic_val = ''
    if picture_var:
        pic_val = picture_var.get(field, '')
    if field == 'logo_type':
        l1 = l2 = ''
        for ch in variation[field]:
            if ch in mbdata.base_logo_dict:
                l1 = ch
            elif ch in mbdata.base_logo_2_dict:
                l2 = ch
        value = (pif.ren.format_image_icon('l_base-' + l1, mbdata.base_logo_dict.get(l1, '(unknown)')) + ' ' +
                 pif.ren.format_image_icon('l_base-' + l2, mbdata.base_logo_2_dict.get(l2, '(none)')))
        new_value = (
            pif.form.put_select(field + "." + variation['var'], mbdata.base_logo, selected=l1) + ' ' +
            pif.form.put_select(field + "." + variation['var'], mbdata.base_logo_2, selected=l2))
    elif field == 'deco':
        dt = variation['deco_type']
        value = f'{value}<br>{mbdata.deco_types_dict.get(dt, "")}'
        new_value = (pif.form.put_text_input(
            field + "." + variation['var'], 64, 64, value=variation.get(field, '')) + '<br>' +
            pif.form.put_select('deco_type.' + variation['var'], mbdata.deco_types, selected=dt))
    else:
        new_value = pif.form.put_text_input(
            field + "." + variation['var'],
            int(mbdata.sql_fieldwidth_re.search(attributes[field]['definition']).group('w'))
            if '(' in attributes[field]['definition'] else 20,
            64, value=variation.get(field, ''))
    if field == 'var':
        flags = (variation.get('flags', variation.get('variation.flags', '0')) & (
                 config.FLAG_MODEL_VARIATION_VERIFIED | config.FLAG_MODEL_ID_INCORRECT))
        new_value += ' ' + pif.form.put_select(
            'flags.' + variation['var'],
            [('0', 'unverified'), (str(config.FLAG_MODEL_VARIATION_VERIFIED), 'verified'),
             (str(config.FLAG_MODEL_VARIATION_VERIFIED | config.FLAG_MODEL_ID_INCORRECT), 'incorrect')],
            str(flags))
    return {'field': field, 'title': title, 'value': value, 'new': new_value, 'pic': pic_val}


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
    img_id = (mod_id + ('-' + var_id if var_id else '')).lower() + (
        '-' + attr_pic['picture_id'] if attr_pic['picture_id'] else '')
    pdir = config.IMG_DIR_VAR if var_id else config.IMG_DIR_ADD
    var_img_credit = pif.dbh.fetch_photo_credit(pdir, img_id, verbose=True)
    var_img_credit = var_img_credit['photographer.name'] if var_img_credit else ''

    img = pif.ren.find_image_path(img_id, prefix=attr_pic['attr_type'], pdir=pdir)
    caption = ''
    if attr_pic['description']:
        caption = attr_pic['description']
        if attr_pic['attribute.title']:
            caption = attr_pic['attribute.title'] + ': ' + caption
    return show_var_image(pif, attr_pic, img, add % {'s': ''}, caption, var_img_credit)


def show_var_image(pif, attr_pic, img, title, caption='', var_img_credit=''):
    ostr = ''
    if img:
        ostr += f'<center><h3>{title}</h3>\n'
        ostr += f'<table><tr><td>{pif.ren.fmt_img_src(img)}<br>'
        if var_img_credit:
            ostr += f'<div class="credit">{pif.ren.format_credit(var_img_credit)}</div>'
        ostr += '</td></tr></table>'
        if attr_pic and attr_pic['description']:
            if attr_pic['attribute.title']:
                ostr += attr_pic['attribute.title'] + ': '
            ostr += attr_pic['description']
        ostr += '<p></center>\n'
    return ostr


def show_details(pif, data, attributes, model, variation, attr_pics={}, ran_id='', photogs=[], picture_var=None):
    return [show_detail(pif, d, attributes, model, variation, attr_pics, ran_id=ran_id, photogs=photogs,
                        picture_var=picture_var) for d in data if d in variation]
# or d.startswith('_')]


def save_variation(pif, mod_id, var_id):
    var_bare = pif.dbh.depref('variation', pif.dbh.fetch_variation_bare(mod_id, var_id))
    var_bare = var_bare[0] if var_bare else {}
    country_codes = mbdata.get_country_codes()
    phcred = var_sel = repic = cpbas = ''
    attributes = {x['attribute_name']: x for x in pif.dbh.depref('attribute', pif.dbh.fetch_attributes(mod_id))}
    pif.ren.comment("Save: ", attributes)
    var_dict = {'mod_id': pif.form.get_raw('mod'), 'picture_id': ''}
    det_dict = dict()
    for attr in form_attributes:
        # if 'id' in attributes.get(attr, {}):
        #     det_dict[attr] = pif.form.get_str(attr + '.' + var_id)
        # else:
        var_dict[attr] = pif.form.get_raw(attr + '.' + var_id)
    for key in pif.form.keys(end='.' + var_id):
        attr = key[:key.rfind('.')]
        if attr == 'references':
            var_sel = pif.form.get_raw(key)  # make it work!
        elif attr == 'phcred':
            phcred = pif.form.get_raw(key)
        elif attr == 'repic':
            repic = pif.form.get_raw(key)
        elif attr == 'cpbas':
            cpbas = pif.form.get_raw(key)
        elif attr == 'picture_id':
            if pif.form.get_raw(key) != var_id:
                var_dict[attr] = pif.form.get_raw(key)
        elif attr == 'area':
            var_dict[attr] = ';'.join([country_codes.get(x, x) for x in pif.form.get_raw(key).split(',')])
        elif attr == 'flags':
            var_dict[attr] = var_bare[attr]
            var_dict[attr] &= ~(config.FLAG_MODEL_VARIATION_VERIFIED | config.FLAG_MODEL_ID_INCORRECT)
            var_dict[attr] |= pif.form.get_int(key)
        elif attr == 'logo_type':
            var_dict[attr] = ''.join(pif.form.get_list(key))
        elif attr in internal_attributes:
            var_dict[attr] = pif.form.get_raw(key)
        else:
            det_dict[attr] = pif.form.get_raw(key)
    if cpbas:
        copy_base_info(pif, mod_id, var_dict, cpbas)
    useful.write_message('var_dict', var_dict)
    useful.write_message('det_dict', det_dict)
    if var_id != var_dict['var']:
        rename_variation(pif, var_dict['mod_id'], var_id, var_dict['var'])
    pif.dbh.write('variation', var_dict, tag='SaveVar')
    for attr in det_dict:
        pif.dbh.write('detail', {'mod_id': var_dict['mod_id'], 'var_id': var_dict['var'],
                      'attr_id': str(attributes[attr]['id']), 'description': det_dict[attr]}, tag='SaveVarDet')
    if var_sel:
        useful.write_message('varsel', var_sel, '<br>')
        pif.dbh.update_variation_selects_for_variation(mod_id, var_dict['var'], var_sel.split())
    useful.write_message('phcred', phcred, '<br>')
    pif.ren.message('Credit added: ',
                    pif.dbh.write_photo_credit(phcred, config.IMG_DIR_VAR[1:], mod_id, var_dict['var']))
#    ty_var = mbmods.calc_var_type(pif, var_bare)  # needs vs
#    if ty_var != var['variation_type']:
#        useful.write_message(var['mod_id'], var['var'], ty_var)
#        # pif.dbh.update_variation({'varation_type': ty_var}, {'mod_id': var['mod_id'], 'var': var['var']})
#        wheres = pif.dbh.make_where(var, cols=['mod_id', 'var'])
#        pif.dbh.write('variation', {'variation_type': ty_var}, wheres, modonly=True, tag='FixVarType')
    if repic:
        rename_variation_pictures(pif, mod_id, var_dict['var'], mod_id, repic)
    pif.dbh.recalc_description(mod_id)


def rename_variation(pif, mod_id=None, old_var_id=None, new_var_id=None, *args, **kwargs):  # pragma: no cover
    if not mod_id or not old_var_id or not new_var_id:
        return
    verbose = False
    if pif.argv:
        useful.write_message('rename_variation', mod_id, old_var_id, new_var_id)
    if old_var_id == new_var_id:
        return
    new_var = pif.dbh.fetch_variation_bare(mod_id, new_var_id)
    if new_var:
        raise useful.SimpleError('That variation already exists!')
    pif.dbh.update_variation({'var': new_var_id, 'imported_var': new_var_id},
                             {'mod_id': mod_id, 'var': old_var_id}, verbose=verbose)
    pif.dbh.update_variation({'picture_id': new_var_id}, {'mod_id': mod_id, 'picture_id': old_var_id}, verbose=verbose)
    pif.dbh.update_detail({'var_id': new_var_id}, {'var_id': old_var_id, 'mod_id': mod_id}, verbose=verbose)
    pif.dbh.write('variation_select', {'var_id': new_var_id}, where=f"var_id='{old_var_id}' and mod_id='{mod_id}'",
                  modonly=True, verbose=verbose, tag='RenameVar')
    # If we're renaming, I'd like to also rename the pictures.
    rename_variation_pictures(pif, mod_id, old_var_id, mod_id, new_var_id)


def rename_variation_pictures(pif, old_mod_id, old_var_id, new_mod_id, new_var_id):  # pragma: no cover
    old_mod_id = old_mod_id.lower()
    new_mod_id = new_mod_id.lower()
    old_var_id = old_var_id.lower()
    new_var_id = new_var_id.lower()
    if old_mod_id == new_mod_id and old_var_id == new_var_id:
        return
    patt1 = useful.relpath('.', config.IMG_DIR_VAR, f'?_{old_mod_id}-{old_var_id}.*')
    patt2 = useful.relpath('.', config.IMG_DIR_VAR, f'{old_mod_id}-{old_var_id}.*')
    pics = glob.glob(patt1) + glob.glob(patt2)
    new_name = f'{new_mod_id}-{new_var_id}'
    old_name = f'{old_mod_id}-{old_var_id}'
    for old_pic in pics:
        new_pic = old_pic.replace(f'-{old_var_id}.', f'-{new_var_id}.')
        new_pic = new_pic.replace(f'_{old_mod_id}-', f'_{new_mod_id}-')
        pif.ren.comment("rename", old_pic, new_pic)
        useful.write_message("rename", old_pic, new_pic, "<br>")
        os.rename(old_pic, new_pic)
    pif.dbh.rename_photo_credit(config.IMG_DIR_VAR[1:], old_name, new_name)


def remove_picture(pif, mod_id, var_id):  # pragma: no cover
    mv_id = f"{mod_id}={var_id}".lower()
    patt1 = f'.{config.IMG_DIR_VAR}/?_{mv_id}.*'
    patt2 = f'.{config.IMG_DIR_VAR}/{mv_id}.*'
    pics = glob.glob(patt1) + glob.glob(patt2)
    for pic in pics:
        pif.ren.comment("delete", pic)
        useful.write_message("delete", pic, "<br>")
        os.unlink(pic)
    cred = pif.dbh.fetch_photo_credit('.' + config.IMG_DIR_VAR, mv_id)
    if cred:
        pif.dbh.delete_photo_credit(cred['photo_credit.id'])


def delete_variation(pif, mod_id=None, var_id=None, *args, **kwargs):  # pragma: no cover
    if mod_id and var_id:
        pif.dbh.delete_variation({'mod_id': mod_id, 'var': var_id})
        pif.dbh.delete_detail({'mod_id': mod_id, 'var_id': var_id})
        pif.dbh.delete_variation_select({'mod_id': mod_id, 'var_id': var_id})


vars_formatter = [
    mbdata.ListType.NORMAL,
    mbdata.ListType.LARGE,
    mbdata.ListType.DETAIL,
    mbdata.ListType.DESCR,
    mbdata.ListType.EDITOR,
    mbdata.ListType.ADMIN,
    mbdata.ListType.CHECKLIST,
    mbdata.ListType.THUMBNAIL,
    # mbdata.ListType.TEXT,
    mbdata.ListType.CSV,
    mbdata.ListType.JSON,
]


# ----- variation search form -----------------------------


class VarSearchForm(object):

    # add output format to this
    output_types = [
        (mbdata.ListType.NORMAL, 'Normal'),
        (mbdata.ListType.CHECKLIST, 'Checklist'),
        (mbdata.ListType.THUMBNAIL, 'Thumbnail'),
        (mbdata.ListType.TEXT, 'Text'),
        (mbdata.ListType.CSV, 'CSV'),
        (mbdata.ListType.JSON, 'JSON'),
    ]

    def __init__(self, pif, mod_id):
        tinf = pif.dbh.get_table_data('variation')
        self.page_id = pif.page_id
        self.mod_id = mod_id
        self.mvars = {var['var']: var for var in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id))}
        self.attr_pics = {x['attribute.attribute_name']: x
                          for x in pif.dbh.depref('attribute_picture', pif.dbh.fetch_attribute_pictures(mod_id))}
        self.attr_recs = pif.dbh.depref('attribute', pif.dbh.fetch_attributes(mod_id, with_global=True))
        attributes = {x['attribute_name']: x for x in self.attr_recs}
        attributes.update({x: {'title': tinf.title.get(x, x.replace('_', ' ').title())} for x in tinf.columns})
        attributes['references'] = {'title': 'References', 'definition': 'varchar(256)'}
        attributes['category'] = {'title': 'Category', 'definition': 'varchar(256)'}
        attributes['text_var'] = {'title': 'Variation ID', 'definition': 'varchar(8)'}
        for vardesc in pif.dbh.describe('variation'):
            if vardesc['field'] in attributes:
                attributes[vardesc['field']]['definition'] = vardesc['type']
        self.attributes = attributes

        self.var_selects = pif.dbh.fetch_variation_selects(mod_id, bare=True)
        self.catdefs = {x['category.id']:
                        {'name': x['category.name'], 'image': x['category.image'], 'flags': x['category.flags']}
                        for x in self.var_selects}
        selects = {}
        varsels = {}
        for var_sel in self.var_selects:
            varsels.setdefault(var_sel['var_id'], [])
            varsels[var_sel['var_id']].append(var_sel)
            selects.setdefault(var_sel['var_id'], [])
            selects[var_sel['var_id']].append(
                var_sel['ref_id'] +
                (('/' + var_sel['sec_id']) if var_sel['sec_id'] else '/' if var_sel['ran_id'] else '') +
                (('.' + var_sel['ran_id']) if var_sel['ran_id'] else '') +
                ((':' + var_sel['category.id']) if var_sel['category.id'] else '')
            )
        self.selects = selects
        self.varsels = varsels

    def read(self, form):
        self.attrs = {x: form.get_raw(x) for x in self.attributes}
        self.attrq = {x: (
            '' if x == 'manufacture' and form.get_str(x) == 'unset' else form.search(x))
            for x in list(self.attributes.keys()) + ['text_note', 'var'] if form.has(x)}
        self.nots = {key: form.get_bool('not_' + key) for key in self.attributes}
        self.contains = {key: form.get_raw('con_' + key) for key in self.attributes}
        self.ci = form.get_bool('ci')
        self.c1 = form.get_bool('c1') or not form.get_bool('hc')
        self.c2 = form.get_bool('c2') or not form.get_bool('hc')
        self.cateq = form.get_str('category', '')
        self.with_pics = form.get_bool('pic1') or not form.get_bool('hc')
        self.without_pics = form.get_bool('pic0') or not form.get_bool('hc')
        self.own_pics_only = form.get_bool('picown')
        self.varl = form.get_str("v")
        self.wheelq = form.get_str("var.wheels")
        self.sobj = form.search("var.s")
        self.recalc = form.has('recalc')
        self.verbose = form.get_bool('verbose')
        self.codes = []
        if self.c1:
            self.codes.append(1)
        if self.c2:
            self.codes.append(2)
        # useful.write_message(str(self.__dict__))
        self.all = (
            not self.attrq and
            # self.ci = form.get_bool('ci')
            # self.c1 = form.get_bool('c1')
            not self.cateq and
            self.with_pics and
            self.without_pics and
            not self.varl and
            not self.wheelq and
            not self.sobj and
            self.codes == [1, 2]
        )
        ltypes = list(set(vars_formatter) & set(form.keys()))
        # useful.write_comment('ltypes', ltypes)
        self.display_type = ltypes[0] if ltypes else mbdata.ListType.NORMAL
        return self

    def write(self, pif, values={}):
        pif.ren.comment("attributes", self.attributes)
        useful.write_comment(pif.form)

        entries = [{'title': self.attributes[x]['title'],
                    'value': pif.form.put_text_input(x, 64, 128)} for x in text_attributes]
        entries.append({'title': 'Note', 'value': pif.form.put_text_input('text_note', 64, 64)})
        entries.append({
            'title': '', 'value':
            pif.form.put_checkbox('ci', [(1, 'Case insensitive')], checked=[1])  # + ' - ' +
            # pif.form.put_select('listtype', self.output_types, selected=mbdata.ListType.NORMAL)
        })
        lsections = [render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)],
                     noheaders=True, footer='<br>')]

        entries = []
        for key in sorted(set(self.attributes.keys()) - set(hidden_attributes) - set(text_attributes)):
            if key == 'category':
                cates = [('', '')] + [(x, self.catdefs.get(x, {'name': x})['name']) for x in values.get(key, [])]
                cates.sort(key=lambda x: x[1])
                value = (pif.form.put_button_up_down_select(key, -1) +
                         pif.form.put_select(key, cates, id=key) +
                         '&nbsp;' + pif.form.put_checkbox('c1', [(1, 'Show Code 1')], checked=[1]) +
                         '&nbsp;' + pif.form.put_checkbox('c2', [(2, 'Show Code 2')], checked=[2]))
            # elif key == 'deco_type':
            #     value = (pif.form.put_button_up_down_select(key, -1) +
            #              pif.form.put_select(key, sorted([
            #                  x for x in mbdata.deco_types if x[0] and x[0] in values.get(key, [])]),
            #                  id=key, blank='') + '&nbsp;')
            elif key == 'manufacture':
                value = (pif.form.put_button_up_down_select(key, -1) +
                         pif.form.put_select(key, sorted(values.get(key, [])), id=key, blank='') +
                         '&nbsp;')
                # + pif.form.put_checkbox('mo', [(1, 'include ' + ', '.join(mbdata.other_plants))])
            elif not any(values.get(key, [])):
                continue
            else:
                value = (pif.form.put_button_up_down_select(key, -1) +
                         pif.form.put_select(key, sorted([x for x in values[key] if x]), id=key, blank=''))
            title = self.attributes[key]['title']
            title_modal = show_detail_modal(pif, self.attr_pics.get(key, {}), self.mod_id)
            if title_modal:
                title += ' ' + pif.ren.fmt_mini(icon="circle-question", family="regular",
                                                also=f"onclick=\"init_modal('m.{key}');\"", alsoc='modalbutton')
                title += pif.ren.format_modal('m.' + key, title_modal)
            entries.append({
                'title': title,
                'value': value,
                'contains': '' if key in ['category', 'deco_type'] else
                            'or contains ' + pif.form.put_text_input('con_' + key, 12),
                'not': pif.form.put_checkbox('not_' + key, [(1, 'not')])
            })

        submit = pif.form.put_button_input("filter", "submit") + '\n'
        submit += pif.form.put_button_input("list", mbdata.ListType.LARGE) + '\n'
        submit += pif.form.put_button_reset('vars') + pif.form.put_hidden_input(hc=1) + '\n'
        if pif.is_allowed('a'):
            submit += (pif.form.put_button_input("edit", mbdata.ListType.EDITOR) + '\n' +
                       '&nbsp;' + pif.form.put_checkbox('pic1', [(1, 'With Pictures')], checked=[1]) +
                       '&nbsp;' + pif.form.put_checkbox('pic0', [(1, 'Without Pictures')], checked=[1]) +
                       '&nbsp;' + pif.form.put_checkbox('picown', [(0, 'Own Pictures Only')]))
        entries.append({
            'title': '&nbsp;',
            'value': submit,
            'not': '&nbsp;'
        })

        lsections.append(render.Section(colist=['title', 'value', 'contains', 'not'],
                         range=[render.Range(entry=entries)], noheaders=True))
        return render.Listix(section=lsections)

    def cate_match(self, var):
        category = var['_catlist']
        search_not = self.nots['category']
        # modelcode = var['_code']
        retval = True
        if self.cateq:
            retval = self.cateq in category
            if search_not:
                retval = not retval
        # useful.write_message('cate_match', var['var'], retval, self.cateq, code)
        return retval

    def wheel_match(self, var):
        retval = (not self.wheelq) or var['wheels'] == self.wheelq or var['text_wheels'] == self.wheelq
        # useful.write_message('wheel_match', var['var'], retval)
        return retval

    def search_match(self, var):
        if not self.sobj:
            # useful.write_message('search_match', var['var'], True, self.sobj)
            return True
        for k in var:
            if k in text_attributes + ['text_note'] and useful.search_match(self.sobj, var[k]):
                # useful.write_message('search_match', var['var'], True, self.sobj, k)
                return True
        # useful.write_message('search_match', var['var'], False, 'final')
        return False

    def desc_match(self, var):
        if not self.attrq:
            # useful.write_message('desc_match', var['var'], True, self.attrq, 'no attrq')
            return True
        for attr in self.attrq:
            # var_val = var.get('note', '') if attr == 'text_note' else var.get(attr, '')
            # query_val = ' '.join(self.attrq.get(attr, []))
            if attr in text_attributes + ['text_note']:
                attrval = var['note' if attr == 'text_note' else 'var' if attr == 'text_var' else attr]
                for obj in self.attrq[attr]:
                    if not self.ci and attrval.find(obj) < 0:
                        # useful.write_message('desc_match', var['var'], False, self.attrq, self.ci, attrval, '-', obj)
                        return False
                    if self.ci and attrval.lower().find(obj.lower()) < 0:
                        # useful.write_message('desc_match', var['var'], False, self.attrq, self.ci, attrval, '-', obj)
                        return False
        # useful.write_message('desc_match', var['var'], True, self.attrq, 'final')
        return True

    def field_match(self, var):
        # if not self.attrq:
        #     #useful.write_message('field_match', var['var'], True, 'no attrq')
        #     return True
        for attr in self.attributes:
            contains = self.contains.get(attr)
            query_val = ' '.join(self.attrq.get(attr, []))
            if contains or query_val:
                search_not = self.nots.get(attr)
                var_val = var.get(attr, '')
                line_match = (query_val and query_val == var_val) or (contains and contains in var_val)
                if attr in text_attributes + ['text_note', 'category']:
                    continue
                elif line_match and search_not:
                    # useful.write_message('field_match', var['var'], False, var_val, query_val, 'neg')
                    return False
                elif not line_match and not search_not:
                    # useful.write_message('field_match', var['var'], False, var_val, query_val, 'pos')
                    return False
        # useful.write_message('field_match', var['var'], True, self.attrq, 'final')
        return True

    def id_match(self, var):
        retval = (not self.varl or (var['var'] in self.varl))
        # useful.write_message('id_match', var['var'], retval, self.varl)
        return retval

    def pic_match(self, var):
        retval = ((self.with_pics and var['_has_pic'] or self.without_pics and not var['_has_pic']) and
                  (not self.own_pics_only or not var['picture_id']))
        return retval

    def model_match(self, var):
        # useful.write_message('model_match', 'attrq', self.attrq)
        return (self.id_match(var) and
                self.pic_match(var) and
                self.cate_match(var) and
                self.search_match(var) and
                self.wheel_match(var) and
                self.desc_match(var) and
                self.field_match(var))

    def show_search_object(self):
        ostr = 'Selected models' if self.varl else 'All models'
        if self.cateq:
            if self.cateq in self.catdefs:
                ostr += ' in ' + self.catdefs[self.cateq]['name']
            else:
                ostr += ' in ' + self.cateq
        if self.wheelq:
            ostr += ' with ' + self.wheelq + " wheels"
        if self.attrq:
            ostr += ' matching search'
        return ostr

    def make_values(self, mvars):
        values = dict()
        wheels = list()

        cates = set()
        for var_id, variation in mvars.items():
            variation['references'] = ' '.join(list(set(self.selects.get(var_id, []))))
            # category = variation['_catlist'] = variation.get('category', '').split()
            # if not category:
            #     category = ['MB']
            # for c in category:
            #     cates.add(c)
            if variation.get('wheels') not in wheels:
                wheels.append(variation.get('wheels'))
            if variation.get('text_wheels') not in wheels:
                wheels.append(variation.get('text_wheels'))
            for key, newvalue in variation.items():
                if key in text_attributes:
                    continue
                values.setdefault(key, [])
                newvalue = newvalue or ''
                if newvalue not in values[key]:
                    values[key].append(newvalue)

        self.form_values = values
        self.form_wheels = wheels
        self.form_cates = cates
        return values


# ----- multiple variation page ---------------------------


def do_var_detail(pif, model, var, credits, varsels):
    def mk_star(has_thing, no_thing):
        return pif.ren.fmt_star('green' if has_thing else 'gray' if no_thing else 'white')

    varsel = varsels.get(var['var'], [])  # pif.dbh.fetch_variation_selects(var['mod_id'], var['var'])
    phcred = credits.get(('%(mod_id)s-%(var)s' % var).lower(), '')
    ty_var, is_found, has = mbmods.calc_var_pics(pif, var)
    cat_v = set(var['category'].split())
    cat_vs = set([x['variation_select.category'] for x in varsel])
    cat = ' '.join(cat_v)
    if cat_v != cat_vs:
        cat += '/' + ' '.join(cat_vs)
    if var.get('manufacture', '') == '':
        flag = ('unset', '')
    elif var['manufacture'] == 'no origin':
        flag = ('none', pif.ren.find_image_path('no', art=True),)
    else:
        flag = pif.ren.show_flag(mbdata.plant_d[var['manufacture']])
    flag = useful.img_src(flag[1], also={'title': flag[0]}) if flag[1] else flag[0]
    row = {
        'ID': pif.ren.format_link('?mod=%s&var=%s&edt=1' % (var['mod_id'], var['var']), var['var'].upper()),
        'Description': var['text_description'],
        'Cat': cat,
        'Ty': mbdata.var_types.get(ty_var, ty_var),
        'Cr': phcred,
        'Pic': var['picture_id'],
        'Date': var['date'],
        'Ver': ((pif.ren.fmt_x('red') + ' ' + var['imported_var'])
                if var['flags'] & config.FLAG_MODEL_ID_INCORRECT else
                pif.ren.fmt_check('black') if var['flags'] & config.FLAG_MODEL_VARIATION_VERIFIED else
                pif.ren.fmt_circle('gray', hollow=True)),
        'Im': var['imported_from'],
        'Or': flag,
        'Lo': var['logo_type'],
        'style': 'c2' if var['_code'] == 2 else ''
    }
    row.update({mbmods.text_short_titles[k]: mk_star(has[k], not model[v]) for k, v in mbmods.text_fmts})
    for sz in mbdata.image_size_types:
        row[sz.upper()] = mk_star(
            os.path.exists(useful.relpath(
                '.', config.IMG_DIR_VAR, sz + '_' + var['mod_id'] + '-' + var['var'] + '.jpg').lower()),
            False)
    return row


def do_var_descriptions(pif, var):
    def mk_star(has_thing, no_thing=False):
        return pif.ren.fmt_star('green' if has_thing else 'white' if no_thing else 'red')

    row = {x: mk_star(y) for x, y in var.items()}
    row['additional_text'] = mk_star(var['additional_text'], True)
    row['note'] = mk_star(var['note'], True)
    row['var'] = pif.ren.format_link('?mod=%s&var=%s&edt=1' % (var['mod_id'], var['var']), var['var'].upper())
    row['flags'] = f'{var["flags"]:02x}' if var['flags'] else '-'
    row['variation_type'] = mbdata.var_types.get(var["variation_type"], var["variation_type"])
    row['manufacture'] = mbdata.plant_d.get(var["manufacture"], var["manufacture"])
    return row


def do_var_for_list(pif, edit, model, var, attributes, varsels, prev, credits, photogs):
    pic_id = var['picture_id']
    # cats = [model['_catdefs'][x]['name'] for x in sorted(set(var['_catlist'])) if x in model['_catdefs']]

    edit = edit and pif.is_allowed('a')
    infs = {'desc1': [], 'desc2': [], 'dets1': [], 'dets2': []}
    for d in sorted(var.keys()):
        if d.startswith('_') or d == 'text_description' or d == 'category' or not var[d] or d in hidden_attributes:
            continue
        elif d in text_attributes:
            pass  # infs['desc1'].append(d)
        elif d in note_attributes:
            if d in attributes:
                infs['desc2'].append(d)
        elif d in base_attributes:
            infs['dets2'].append(d)
        elif d in attributes:
            if d == 'deco' and var['deco_type']:
                var['deco'] += ' - ' + mbdata.deco_types_dict.get(var['deco_type'], var['deco_type'])
            infs['dets1'].append(d)
    infs['desc1'] = [x for x in text_attributes if var.get(x)]

    def attr_star(model, var):
        return sum([int(bool(var['text_' + x]) or not model['format_' + x]) for x in desc_attributes])

    id_text = '<center>'
    if edit:  # pragma: no cover
        id_text += pif.ren.format_link('?edt=1&mod=%s&var=%s' % (var['mod_id'], var['var']), var['var'].upper())
        id_text += '<br>' + pif.form.put_checkbox('v', [(var['var'], '')])

        count_descs = attr_star(model, var)
        id_text += pif.ren.fmt_star(
            'green' if count_descs == len(text_attributes) else 'red' if not count_descs else 'orange')
        if var['flags'] & config.FLAG_MODEL_VARIATION_VERIFIED:
            id_text += '<br>' + pif.ren.fmt_check('black')
            if var['flags'] & config.FLAG_MODEL_ID_INCORRECT:
                id_text += '<br>' + pif.ren.fmt_x('red')
    else:
        id_text += pif.ren.format_link('?mod=%s&var=%s' % (var['mod_id'], var['var']), var['var'].upper())
    id_text += '</center>'

    def show_list(descs):
        def show_det(x):
            return '; '.join([y.replace('~', ':') for y in x.split('|')])

        return '<br>'.join(['<span class="%s">%s: %s</span>\n' % (
            ("diff" if var[d] != prev.get(d, var[d]) else "same"), attributes[d]['title'], show_det(var[d]))
            for d in descs])
        # return ('<table class="long_tab">' +
        #     '\n'.join([
        #         '<tr><td><span class="%s">%s:</td><td>%s</span></td></tr>\n' % (
        #         ("diff" if var[d] != prev.get(d, var[d]) else "same"), attributes[d]['title'], var[d])
        #     for d in descs]) +
        #     '</table>\n')

    desc_text = '<div class="varentry">' + var['text_description'] + '</div>\n'
    desc_text += show_list(infs['desc1'])
    if infs['desc2']:
        desc_text += '<hr>'
        desc_text += show_list(infs['desc2'])

    det_text = show_list(infs['dets1'])
    if infs['dets2']:
        det_text += '<hr>'
        det_text += show_list(infs['dets2'])

    pic_text = '<center><a href="%(_lnk)s">%(_picture)s</a>' % var
    note_text = ''
    if edit:  # pragma: no cover
        cat_v = set(var['category'].split())
        cat_vs = set([x['variation_select.category'] for x in varsels.get(var['var'], [])])
        cat = ' '.join(cat_v)
        if cat_v != cat_vs:
            cat += '/' + ' '.join(cat_vs)
        note_text += "%s: %s<br>" % (attributes['category']['title'], cat)
        if var['date']:
            note_text += "%s: %s<br>" % (
                attributes['date']['title'],
                pif.ren.format_link('msearch.cgi?date=1&dt=%s' % var['date'], var['date']))
        note_text += 'Import: %s, %s-%s<br>' % (var['imported'], var['imported_from'], var['imported_var'])
        note_text += 'Show: ' + pif.form.put_text_input(
            "picture_id." + var['var'], 8, value=pic_id, also={'class': 'bggray' if pic_id else 'bgok'})
        if pic_id:
            note_text += '<span class="warning">'
        for sz in mbdata.image_size_types:
            if os.path.exists(useful.relpath(
                    '.', config.IMG_DIR_VAR, sz + '_' + var['mod_id'] + '-' + var['var'] + '.jpg').lower()):
                note_text += sz.upper() + ' '
        if pic_id:
            note_text += '</span>'
            phcred = credits.get(('%(mod_id)s-%(picture_id)s' % var).lower(), '')
            if phcred:
                pic_text += '<span class="credit">%s</span><br>' % dict(photogs).get(phcred, phcred)
        else:
            phcred = credits.get(('%(mod_id)s-%(var)s' % var).lower(), '')
            pic_text += '<div class="%s">' % ('bgok' if phcred or pic_id else 'bgno')
            pic_text += pif.form.put_select("phcred." + var['var'], photogs, selected=phcred, blank='') + '</div>'
        note_text += "<br>References:<br>" + pif.form.put_text_input(
            "var_sel." + var['var'], 512, 28, value=var['references'],
            also={'class': 'bgok' if var['references'] else 'bgno'})
        note_text += quickie_modal(pif, model['id'], var['var'], 'base')
        note_text += quickie_modal(pif, model['id'], var['var'], 'detail')
    else:
        phcred = credits.get(
            ('%s-%s' % (var['mod_id'], var['picture_id'] if var['picture_id'] else var['var'])).lower(), '')
        if phcred:
            pic_text += '<span class="credit">%s</span><br>' % dict(photogs).get(phcred, phcred)

    if var['logo_type']:
        for logo in var['logo_type']:
            pic_text += pif.ren.format_image_icon('l_base-' + logo, mbdata.base_logo_dict.get(logo, '')) + ' '
    else:
        pic_text += ' '
    if var['categories']:
        pic_text += '<hr>' + var['categories']
    pic_text += '</center>'

    return {
        'ID': id_text,
        'Description': desc_text,
        'Details': det_text,
        'Picture': pic_text,
        'Notes': note_text,
    }


def quickie_modal(pif, mod_id, var_id, field):
    img_id = mod_id + '-' + var_id
    pdir = config.IMG_DIR_VAR
    img = pif.ren.find_image_path(img_id, prefix=field[0], pdir=pdir)
    modal = show_var_image(pif, None, img, '', '', '')
    if modal:
        value = '''<br><span onclick="init_modal('v.%s');" class="modalbutton">%s</span>\n''' % (
            field, pif.form.put_text_button(field))
        value += pif.ren.format_modal('v.' + field, modal) + '\n'
        return value
    return ''


# mbdata.ListType.LARGE mbdata.LISTTYPE_EDITOR listix
def do_model_list(pif, model, vsform, dvars, photogs):
    llistix = render.Listix(id='vars', section=[])

    edit = vsform.display_type == mbdata.ListType.EDITOR and pif.is_allowed('a')
    credits = {x['photo_credit.name'].lower(): x['photographer.id']
               for x in pif.dbh.fetch_photo_credits_for_vars(
        path=config.IMG_DIR_VAR[1:], name=model['id'], verbose=False)}
    prev = {}
    if edit:  # pragma: no cover
        list_columns.append('Notes')
    for code in vsform.codes:
        lsec = render.Section(
            id='code_%d dt_%s' % (code, 'e'), name='Code %d Models' % code, range=list(), switch=code != 1,
            colist=list_columns,
        )
        lran = render.Range(id='ran', entry=[])
        for var_id in sorted(dvars.keys()):
            var = dvars[var_id]
            pif.ren.comment(var)
            if var['_code'] == code:
                lran.entry.append(do_var_for_list(
                    pif, edit, model, var, vsform.attributes, vsform.varsels, prev, credits, photogs))
                prev = var

        lran.styles = {'Description': 'lefty'}
        if len(lran.entry):
            lsec.count = '%d entries' % len(lran.entry) if len(lran.entry) > 1 else '1 entry'
            lsec.range.append(lran)
            llistix.section.append(lsec)

    llistix.footer = (related_casting_links(
        pif, model['id'],
        url="vars.cgi?%s=1&mod=" % (mbdata.ListType.EDITOR if edit else mbdata.LISTTYPE_LARGE)) + '<br>' +
        pif.ren.format_button_link("show as grid", 'vars.cgi?mod=%s' % model['id']))
    return llistix


# mbdata.ListType.DETAIL listix
def do_model_detail(pif, model, vsform, dvars, photogs):
    mod_id = model['id']
    llistix = render.Listix(id='vars')

    credits = {x['photo_credit.name'].lower(): x['photographer.id']
               for x in pif.dbh.fetch_photo_credits_for_vars(path=config.IMG_DIR_VAR[1:], name=mod_id, verbose=False)}
    mack = sorted(pif.dbh.fetch_aliases(mod_id, type_id='mack'), key=lambda x: -x['alias.flags'])
    mack = mack[0]['alias.id'] if mack else 'All Models'

    if 1:  # mixed
        lsec = render.Section(
            id='dt_d', name=str(mack), range=list(),
            colist=detail_columns,
        )
        lran = render.Range(id='ran', styles={'Description': 'lefty'})
        lran.entry = [do_var_detail(pif, model, var, credits, vsform.varsels)
                      for var_id, var in sorted(dvars.items())]
        lsec.count = '%d entries' % len(lran.entry) if len(lran.entry) > 1 else '1 entry'
        lsec.range.append(lran)
        llistix.section.append(lsec)

    else:
        for code in vsform.codes:
            lsec = render.Section(
                id='code_%d dt_%s' % (code, 'd'), name='Code %d Models' % code, range=list(),
                switch=code != 1,
                colist=detail_columns,
            )
            lran = render.Range(id='ran', entry=[])
            lran.entry = [do_var_detail(pif, model, var, credits, vsform.varsels)
                          for var_id, var in sorted(dvars.items()) if var['_code'] == code]
            lran.styles = {'Description': 'lefty'}
            if len(lran.entry):
                lsec.count = '%d entries' % len(lran.entry) if len(lran.entry) > 1 else '1 entry'
                lsec.range.append(lran)
                llistix.section.append(lsec)
    llistix.footer = related_casting_links(pif, mod_id, url="vars.cgi?vdt=1&mod=")
    return llistix


# mbdata.ListType.DESCR listix
def do_model_descriptions(pif, model, vsform, dvars, photogs):
    mod_id = model['id']

    mack = sorted(pif.dbh.fetch_aliases(mod_id, type_id='mack'), key=lambda x: -x['alias.flags'])
    mack = mack[0]['alias.id'] if mack else 'All Models'
    attrs = [x['attribute.attribute_name'] for x in pif.dbh.fetch_attributes(model['id'])]

    def mk_hdr(x):
        if '_' in x:
            return (x[0] + x[x.find('_') + 1]).upper()
        return x[0].upper() + x[1]

    columns = ['var', 'flags', 'base', 'body', 'deco', 'interior', 'wheels', 'windows', 'manufacture',
               'additional_text', 'base_name', 'base_number', 'base_scale', 'tool_id', 'production_id',
               'copyright', 'company_name', 'logo_type', 'base_reads', 'note', 'variation_type'] + attrs
    headers = ['var', 'Fl', 'Ba', 'Bo', 'De', 'In', 'Wh', 'Wi', 'Ma', 'AT', 'BN', 'B#', 'BS', 'TI', 'PI', 'CR', 'CN',
               'LT', 'BR', 'No', 'VT'] + [mk_hdr(x) for x in attrs]

    return render.Listix(id='vars', section=[render.Section(
        id='dt_d', name=str(mack), colist=columns, headers=headers, header='<br>' + ', '.join(columns),
        count='%d entries' % len(dvars) if len(dvars) > 1 else '1 entry',
        footer=related_casting_links(pif, mod_id, url="vars.cgi?vdt=1&mod="),
        range=[render.Range(id='ran', entry=[do_var_descriptions(pif, x) for _, x in sorted(dvars.items())])]
    )])


# mbdata.ListType.ADMIN listix
def do_model_editor(pif, model, vsform, dvars, photogs):
    mod_id = model['id']
    llistix = render.Listix(id='vars', section=[])
    attrs = ['var'] + [x['attribute_name'] for x in vsform.attr_recs]

    mack = sorted(pif.dbh.fetch_aliases(mod_id, type_id='mack'), key=lambda x: -x['alias.flags'])
    mack = mack[0]['alias.id'] if mack else 'All Models'

    lsec = render.Section(id='ed', name='All Models', colist=attrs, header='<form action="vars.cgi">')
    lran = render.Range(id='ran')

    def attr_edit(v, x):
        return v.get(x, '') + '<br>' + pif.form.put_text_input(v['var'] + '.' + x, 80, 16, v.get(x, ''))

    lran.entry = [{x: attr_edit(v, x) for x in attrs} for var_id, v in sorted(dvars.items())]
    lsec.count = '%d entries' % len(lran.entry) if len(lran.entry) > 1 else '1 entry'
    lsec.range.append(lran)
    llistix.section.append(lsec)

    llistix.footer = related_casting_links(pif, mod_id, url="vars.cgi?vdt=1&mod=")
    llistix.footer += pif.form.put_button_input('save')
    llistix.footer += pif.form.put_hidden_input(mod=mod_id)
    llistix.footer += '</form>'
    return llistix


def related_casting_links(pif, mod_id, url):
    var_id_set = set()
    related = set()
    for cr in pif.dbh.fetch_casting_relateds(section_id='single', mod_id=mod_id):
        if cr['casting_related.flags'] & config.FLAG_CASTING_RELATED_SHARED:
            var_id_set.add(cr['casting_related.related_id'])
        else:
            related.add(cr['casting_related.related_id'])

    ostr = ''
    if var_id_set:
        ostr += 'Shares variation IDs with: ' + ', '.join(
            [pif.ren.format_link(url + x, x) for x in sorted(var_id_set)])
        if related:
            ostr += '<br>'
    if related:
        ostr += 'Related castings: ' + ', '.join([pif.ren.format_link(url + x, x) for x in sorted(related)])
    return ostr


# mbdata.ListType.CHECKLIST
def do_model_checklist(pif, model, vsform, dvars, photogs):
    pass


# mbdata.ListType.THUMBNAIL
def do_model_thumbnail(pif, model, vsform, dvars, photogs):
    llineup = render.Matrix(id='vars', section=[])

    for code in vsform.codes:
        lsec = render.Section(
            id='code_%d dt_%s' % (code, 'g'), name=f'Code {code} Models', switch=code != 1, columns=4)
        lran = render.Range(
            id='ran',
            entry=[render.Entry(data=var) for var_id, var in sorted(dvars.items()) if var['_code'] == code],
            styles={'Description': 'lefty'},
        )
        if lran.entry:
            lsec.count = '%d entries' % len(lran.entry) if len(lran.entry) > 1 else '1 entry'
            while len(lran['entry']) < 4:
                lran.entry.append(render.Entry(text='', class_name='blank'))
            lsec.range.append(lran)
            llineup.section.append(lsec)

    return llineup.prep()


# mbdata.ListType.NORMAL
def do_model_grid(pif, model, vsform, dvars, photogs):
    llineup = render.Matrix(
        id='vars', footer='<br>' +
        pif.ren.format_button_link("show as list", 'vars.cgi?lrg=1&mod=%s' % model['id'])
    )

    for code in vsform.codes:
        lsec = render.Section(
            id='code_%d dt_%s' % (code, 'g'), name='Code %d Models' % code, switch=code != 1, columns=4,
        )
        lran = render.Range(
            id='ran',
            entry=[render.Entry(data=var) for var_id, var in sorted(dvars.items()) if var['_code'] == code],
            styles={'Description': 'lefty'},
        )
        if lran.entry:
            lsec.count = '%d entries' % len(lran.entry) if len(lran.entry) > 1 else '1 entry'
            while len(lran.entry) < 4:
                lran.entry.append(render.Entry(text='', class_name='blank'))
            lsec.range.append(lran)
            llineup.section.append(lsec)

    return llineup.prep()


def reduce_vs(vs):
    varsel = []
    for x in sorted(vs.split(), reverse=True):
        if x in varsel:
            continue
        if (':' in x and x[:x.find(':')] in varsel):
            continue
        varsel.append(x)
    return varsel


def save_model(pif, mod_id):
    for key in pif.form.keys(start='picture_id.'):
        if key[11:] == pif.form.get_str(key):
            useful.write_message('pic', key[11:], 'clear')
            pif.dbh.update_variation({'picture_id': pif.form.get_str(key)}, {'mod_id': mod_id, 'var': ''})
        else:
            useful.write_message('pic', key[11:], pif.form.get_str(key))
            pif.dbh.update_variation({'picture_id': pif.form.get_str(key)}, {'mod_id': mod_id, 'var': key[11:]})
    for key in pif.form.keys(start='var_sel.'):
        varsel = reduce_vs(pif.form.get_str(key))
        useful.write_message('vs', key, pif.form.get_str(key), '/', varsel)
        pif.dbh.update_variation_selects_for_variation(mod_id, key[8:], varsel)
    for var in pif.form.roots(start='phcred.'):
        phcred = pif.form.get_str('phcred.' + var)
        if phcred:
            useful.write_message('phcred', mod_id, var, "'%s'" % phcred, '<br>')
            pif.ren.message(
                'Credit added: ', pif.dbh.write_photo_credit(phcred, config.IMG_DIR_VAR[1:], mod_id, var))
    phcred = pif.form.get_str('phcred')
    if phcred:
        useful.write_message('phcred', mod_id, "'%s'" % phcred, '<br>')
        pif.ren.message('Credit added: ', pif.dbh.write_photo_credit(phcred, config.IMG_DIR_MAN[1:], mod_id))
    attrs = {x['attribute_name']: x['id'] for x in pif.dbh.depref('attribute', pif.dbh.fetch_attributes(mod_id))}
    for key in pif.form.roots(end='.var'):
        pass  # save_variation(pif, mod_id, key) - keys are backwards!  argh
        attr_dict = pif.form.get_dict(start=key + '.')
        var_dict = {x: attr_dict.get(x, '') for x in detail_attributes + ['var']}
        det_dict = {attrs[x]: attr_dict[x] for x in attr_dict if x not in var_dict}
        # key of det_dict has to be attr.id, not attr.name
        var_dict['mod_id'] = mod_id

        useful.write_message(
            'var_dict', var_dict,
            pif.dbh.write('variation', var_dict, {'mod_id': mod_id, 'var': key}, tag="UpdateVarEdit"))
        useful.write_message('det_dict', det_dict, pif.dbh.update_details(mod_id, key, det_dict))
        # pif.dbh.write('variation', var_dict)
        # for attr in det_dict:
        #     pif.dbh.write('detail', {'mod_id': var_dict['mod_id'], 'var_id': var_dict['var'],
        #                   'attr_id': str(attributes[attr]['id']), 'description': det_dict[attr]})
        pif.dbh.recalc_description(mod_id)


def mangle_variation(pif, model, variation, cats):
    vcats = variation['_catlist'] = sorted(set([x['variation_select.category']
                                                for x in variation['vs']] + variation['category'].split()))
    # variation['area'] = ', '.join([mbdata.regions.get(x, x) for x in variation.get('area', '').split(';')])
    # variation['_code'] = 2 if any([x['category.flags'] & config.FLAG_MODEL_CODE_2 for x in variation['vs']]) else 1
    variation['_code'] = 2 if any([x in cats and (cats[x].flags & config.FLAG_MODEL_CODE_2) for x in vcats]) else 1
    variation['link'] = '?mod=%s&var=%s' % (variation['mod_id'], variation['var'])
    pic_id = variation['picture_id']

    img = pif.ren.find_image_path([variation['mod_id']], nobase=True,
                                  vars=pic_id if pic_id else variation['var'], prefix=mbdata.IMG_SIZ_SMALL)
    variation['_has_pic'] = bool(img)
    variation['_picture'] = (pif.ren.fmt_img_src(img, also={'title': variation['var']}) if img else
                             pif.ren.fmt_no_pic(True, mbdata.IMG_SIZ_SMALL))

    variation['area'] = ', '.join([
        mbdata.get_countries().get(x, mbdata.areas.get(x, x)) for x in variation.get('area', '').split(';')])
    variation['_categories'] = [cats[x]['name'] for x in vcats if x in cats]
    variation['categories'] = '<br>'.join([
        pif.ren.format_image_icon('c_' + cats[x]['image'], desc=cats[x]['name']) for x in vcats if x in cats])
    return variation


def do_var_for_dict(pif, model, var, attributes, varsels):
    # pic_id = var['picture_id']

    # infs = {'desc1': [], 'desc2': [], 'dets1': [], 'dets2': []}
    ent = {d: var[d] for d in var if var.get(d) and d in attributes and
           not (d.startswith('_') or d == 'category' or
           d in hidden_attributes or (d in note_attributes and d not in attributes))}
    ent['id'] = var['var']
    ent['categories'] = ', '.join(var['_categories'])
    return ent


def do_model_json(pif, model, vsform, dvars, photogs):
    llineup = {'id': 'vars', 'section': []}

    for code in vsform.codes:
        lsec = {'id': 'code_%d' % code, 'name': 'Code %d Models' % code, 'entry': list()}
        for var_id in sorted(dvars.keys()):
            var = dvars[var_id]
            if var['_code'] == code:
                lsec['entry'].append(do_var_for_dict(pif, model, var, vsform.attributes, vsform.varsels))

        if len(lsec['entry']):
            lsec['count'] = '%d entries' % len(lsec['entry']) if len(lsec['entry']) > 1 else '1 entry'
            llineup['section'].append(lsec)

    return json.dumps(llineup)


def do_model_csv(pif, model, vsform, dvars, photogs):
    out_file = StringIO()
    field_names = (['id'] + text_attributes + detail_attributes + [x['attribute_name'] for x in vsform.attr_recs] +
                   base_attributes + note_attributes + ['categories'])
    writer = csv.DictWriter(out_file, fieldnames=field_names)
    writer.writeheader()

    for code in vsform.codes:
        for var_id in sorted(dvars.keys()):
            var = dvars[var_id]
            if var['_code'] == code:
                rec = do_var_for_dict(pif, model, var, vsform.attributes, vsform.varsels)
                writer.writerow(dict(zip(field_names, [rec.get(x, '') for x in field_names])))
    out_str = out_file.getvalue()
    out_file.close()
    return out_str


# def do_model_text(pif, model, vsform, fvars, photogs):
#     secs = self.run_thing(pif, self.show_section_text_list)
#     fmt = '[_] %(man)-8s  %(name)-48s  %(year)s\n'
#     return ''.join([''.join([fmt % y for y in x]) for x in secs])


def show_casting(pif, model):
    mod_id = model['id']
    vsform = VarSearchForm(pif, mod_id).read(pif.form)
    pif.ren.print_html(mbdata.get_mime_type(vsform.display_type))  # (mbdata.get_mime_type(listtype))
    model['_catdefs'] = categories = {x.id: x for x in pif.dbh.fetch_categories()}
    cates = set()
    mvars = dict()
    fvars = dict()
    libdir = useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower()) if pif.is_allowed('u') else ('.' + config.INC_DIR)
    uplink = ('upload.cgi?d=%(_dir)s&m=%(mod_id)s&v=%(var)s' if pif.is_allowed('u') else
              'upload.cgi?m=%(mod_id)s&v=%(var)s')
    for variation in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
        variation = mangle_variation(pif, model, variation, categories)
        variation['_dir'] = libdir
        variation['_lnk'] = uplink % variation
        cates.update(variation['_catlist'])
        mvars[variation['var']] = variation
        if vsform.model_match(variation):
            fvars[variation['var']] = variation
    # vsform.catdefs = model['_catdefs']

    form_values = vsform.make_values(mvars)
    form_values['category'] = list(cates)
    # hide private?
    photogs = [(x.photographer.id, x.photographer.name) for x in pif.dbh.fetch_photographers()]
    phcred = pif.dbh.fetch_photo_credit('.' + config.IMG_DIR_MAN, mod_id)

    formatter = {
        mbdata.ListType.NORMAL: do_model_grid,
        mbdata.ListType.LARGE: do_model_list,
        mbdata.ListType.DETAIL: do_model_detail,
        mbdata.ListType.DESCR: do_model_descriptions,
        mbdata.ListType.EDITOR: do_model_list,
        mbdata.ListType.ADMIN: do_model_editor,
        mbdata.ListType.CHECKLIST: do_model_checklist,
        mbdata.ListType.THUMBNAIL: do_model_thumbnail,
        # mbdata.ListType.TEXT:
        mbdata.ListType.CSV: do_model_csv,
        mbdata.ListType.JSON: do_model_json,
    }

    llineup = formatter.get(vsform.display_type, do_model_grid)(pif, model, vsform, fvars, photogs)
    if vsform.display_type in mbdata.mime_types:
        return llineup

    img = pif.ren.format_image_required(mod_id, largest=mbdata.IMG_SIZ_MEDIUM, pdir=config.IMG_DIR_MAN)
    phcred = phcred.get('photographer.id', '') if phcred else ''

    footer = ''
    if pif.is_allowed('a'):  # pragma: no cover
        footer += pif.form.put_button_input('list', mbdata.ListType.LARGE)
        if vsform.display_type in (mbdata.ListType.LARGE, mbdata.LISTTYPE_EDITOR,):
            img += '<div class="%s">Credit: ' % ('bgok' if phcred else 'bgno')
            img += pif.form.put_select("phcred", photogs, selected=phcred, blank='') + '</div>'
            footer += pif.form.put_button_input('save')
        # footer += pif.ren.format_button_link("add", 'vars.cgi?edt=1&mod=%s&add=1' % mod_id)
        footer += pif.ren.format_button_link("add", 'mass.cgi?tymass=var&mod_id=%s' % mod_id)
        footer += pif.ren.format_button_link("casting", pif.dbh.get_editor_link('casting', {'id': mod_id}))
        footer += pif.ren.format_button_link("recalc", '?recalc=1&mod=%s' % mod_id)
    if pif.is_allowed('u'):  # pragma: no cover
        footer += pif.ren.format_button_link("upload", 'upload.cgi?d=' + libdir + '&m=' + mod_id)
        footer += pif.ren.format_button_link("pictures", 'traverse.cgi?d=%s' % libdir)

    # ------- render ------------------------------------

    pif.ren.set_page_extra(pif.ren.reset_button_js + pif.ren.increment_select_js +
                           pif.ren.toggle_display_js + pif.ren.modal_js)
    pif.ren.set_button_comment(pif, 'man=%s&var=%s' % (mod_id, vsform.varl))
    context = {
        'image': img,
        'notes': model['notes'],
        'llineup': llineup,
        'footer': footer,
        'search_object': vsform.show_search_object(),
        'verbose': vsform.verbose,
        'show_as_list': vsform.display_type in (
            mbdata.ListType.LARGE, mbdata.LISTTYPE_EDITOR, mbdata.LISTTYPE_DETAIL, mbdata.LISTTYPE_DESCR,
            mbdata.ListType.ADMIN),
        'mod_id': mod_id,
        'var_search_form': vsform.write(pif, form_values),
        'var_search_visible': pif.form.put_button_input_visibility("varsearch", True),
    }
    return pif.ren.format_template('vars.html', **context)


def get_man_id(pif):
    return ''


@basics.web_page
def main(pif):
    man_id = get_man_id(pif) if pif.form.get_bool('mbusa') else pif.form.get_id('mod')
    var_id = pif.form.get_id('var')

    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append('/cgi-bin/single.cgi', 'By ID')
    pif.ren.hierarchy_append('/cgi-bin/single.cgi?id=%s' % man_id, man_id)
    pif.ren.hierarchy_append('/cgi-bin/vars.cgi?mod=%s' % man_id, 'Variations')

    man = dict()
    if man_id:
        man = pif.dbh.fetch_casting(man_id, extras=True)
        if not man:
            man = pif.dbh.fetch_casting_by_alias(man_id, extras=True)

    if man and var_id:
        return single_variation(pif, man, var_id)
    elif man:
        return variation_list(pif, man)
    raise useful.SimpleError("Can't find requested information.  Please try something else.")


def variation_list(pif, man):
    pif.ren.title = '%(casting_type)s %(id)s: %(name)s - Variations' % man
    # pif.ren.print_html()
    if pif.form.has("save"):
        save_model(pif, man['id'])
    elif pif.form.has('recalc'):
        pif.dbh.recalc_description(man['id'])
    # mbdata.ListType.TEXT
    # mbdata.ListType.CSV
    # mbdata.ListType.JSON
    return show_casting(pif, man)


def action(pif, man, var_id):
    edit = addnew = False
    if pif.form.has("delete"):
        delete_variation(pif, man['id'], None)
        var_id = ''
    elif pif.form.has("save"):
        var_id = pif.form.get_str('ovar')
        save_variation(pif, man['id'], var_id)
        var_id = ''
    elif pif.form.has("add"):
        var_id = var_id or 'unset'
        edit = addnew = True
    elif pif.form.has(mbdata.ListType.EDITOR):
        edit = True
    elif pif.form.has("rmpic"):
        remove_picture(pif, man['id'], var_id)
    elif pif.form.has("promote"):
        imglib.promote_picture(pif, man['id'], var_id)
    return var_id, edit, addnew


def single_variation(pif, man, var_id):
    pif.ren.hierarchy_append('/cgi-bin/vars.cgi?mod=%s&var=%s' % (man['id'], var_id), var_id)
    # pif.ren.print_html()

    var_id = mbdata.normalize_var_id(man, var_id)
    pif.ren.title = '%(casting_type)s %(id)s: %(name)s' % man
    pif.ren.title += ' - Variation ' + var_id

    var_id, edit, addnew = action(pif, man, var_id)

    if var_id:
        return show_single_variation(pif, man, var_id, edit=edit, addnew=addnew)
    return show_casting(pif, man)


# ----- msearch -------------------------------------------


vfields = {'base': 'text_base', 'body': 'text_body', 'interior': 'text_interior', 'wheels': 'text_wheels',
           'windows': 'text_windows', 'with': 'text_with', 'text': 'text_text',
           'cat': 'category', 'date': 'date', 'area': 'area', 'note': 'note'}
cfields = {'casting': 'rawname'}


@basics.web_page
def run_search(pif):
    pif.ren.print_html()
    if pif.form.has('ask'):
        return var_search_ask(pif)
    return var_search(pif)


def var_search_ask(pif):
    mod_id = pif.form.get_str('id')
    model = pif.dbh.fetch_casting(mod_id)
    if not model:
        raise useful.SimpleError("That is not a recognized model ID.")
    vsform = VarSearchForm(pif, mod_id).read(pif.form)
    pif.ren.title = 'Search ' + model['id'] + ' Variations'

    pif.ren.set_page_extra(pif.ren.reset_button_js + pif.ren.increment_select_js + pif.ren.modal_js)
    pif.ren.set_button_comment(pif, keys={'man': 'id'})
    context = {
        'verbose': vsform.verbose,
        'vsform': vsform.write(pif, vsform.make_values(vsform.mvars)),
        'id': mod_id,
    }
    return pif.ren.format_template('vsearchask.html', **context)


def get_codes(pif):
    codes = 0
    for code in pif.form.get_list('codes'):
        if code not in "123":
            return None
        codes += int(code)
    return codes


# http://beta.bamca.org/cgi-bin/vsearch.cgi?body=&windows=&cat=&base=wheelstrip&interior=&wheels=&casting=&codes=3&start=100
def var_search(pif):
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append(pif.request_uri, 'Variation Search')
    pif.ren.title = 'Models matching: ' + ' '.join(pif.form.search('query'))
    varsq = {vfields[x]: pif.form.search(x) for x in vfields}
    castq = {cfields[x]: pif.form.search(x) for x in cfields}
    codes = get_codes(pif)
    if codes is None:
        raise useful.SimpleError("This submission was not created by the form provided.")

    pif.ren.comment('varsq', varsq, 'castq', castq, 'codes', codes)
    mods = pif.dbh.fetch_variation_query(varsq, castingq=castq, codes=codes)
    mods.sort(key=lambda x: x['v.mod_id'] + '-' + x['v.var'])
    nmods = len(mods)

    llineup = render.Matrix(note='%d variations found matching search' % nmods, columns=4, tail=['', ''])
    start = pif.form.get_int('start')
    mods = mods[start:start + mbdata.modsperpage]
    sect = pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
    lran = render.Range()
    for mod in mods:
        mod['name'] = mod['base_id.rawname'].replace(';', ' ')
        lran.entry.append(render.Entry(text=mbmods.add_model_var_table_pic_link(pif, mod)))
    lsec = render.Section(section=sect, range=[lran], columns=4)
    llineup.section = [lsec]
    qf = pif.form.reformat(vfields) + '&' + pif.form.reformat(cfields)
    if pif.ren.verbose:
        qf += '&verbose=1'
    qf += f'&codes={codes}'
    if start > 0:
        llineup.tail[1] += pif.ren.format_button_link(
            "previous", f'vsearch.cgi?{qf}&start={max(start - mbdata.modsperpage, 0)}') + ' '
    if start + mbdata.modsperpage < nmods:
        llineup.tail[1] += pif.ren.format_button_link(
            "next", f'vsearch.cgi?{qf}&start={min(start + mbdata.modsperpage, nmods)}')

    pif.ren.set_button_comment(pif, keys={'casting': 'casting', 'base': 'base', 'body': 'body',
                                          'interior': 'interior', 'wheels': 'wheels', 'windows': 'windows'})
    return pif.ren.format_template('simplematrix.html', llineup=llineup.prep())


# ----- commands ------------------------------------------


def move_variation(pif, old_mod_id, old_var_id, new_mod_id, new_var_id, *args, **kwargs):  # pragma: no cover
    verbose = False
    if pif.argv:
        useful.write_message('move_variation', old_mod_id, old_var_id, new_mod_id, new_var_id)
        verbose = True
        pif.dbh.set_verbose(True)
    if old_mod_id == new_mod_id and old_var_id == new_var_id:
        useful.write_message('no change')
        return
    pif.dbh.update_variation({'mod_id': new_mod_id, 'var': new_var_id, 'imported_var': new_var_id},
                             {'mod_id': old_mod_id, 'var': old_var_id}, verbose=verbose)
    pif.dbh.update_variation({'picture_id': ''}, {'mod_id': old_mod_id, 'picture_id': old_var_id}, verbose=verbose)

    # This will take some work.
    old_attrs = pif.dbh.depref('attribute', pif.dbh.fetch_attributes(old_mod_id))
    old_attrs = {x['attribute_name']: x for x in old_attrs}
    new_attrs = pif.dbh.depref('attribute', pif.dbh.fetch_attributes(new_mod_id))
    new_attrs = {x['attribute_name']: x for x in new_attrs}
    useful.write_message(old_attrs)
    useful.write_message(new_attrs)
    details = pif.dbh.fetch_details(old_mod_id, old_var_id, nodefaults=True).get(old_var_id, {})
    for detail in details:
        if detail in new_attrs:
            new_att_id = new_attrs[detail]['id']
            old_att_id = old_attrs[detail]['id']
            pif.dbh.update_detail({'attr_id': new_att_id, 'mod_id': new_mod_id, 'var_id': new_var_id},
                                  {'attr_id': old_att_id, 'mod_id': old_mod_id, 'var_id': old_var_id})
        else:
            useful.write_message(f'cannot transfer {detail}="{details[detail]}"')

    pif.dbh.write('variation_select', {'mod_id': new_mod_id, 'var_id': new_var_id},
                  where=f"var_id='{old_var_id}' and mod_id='{old_mod_id}'",
                  modonly=True, verbose=verbose, tag='MoveVar')
    rename_variation_pictures(pif, old_mod_id, old_var_id, new_mod_id, new_var_id)


def swap_variations(pif, mod_id=None, var1=None, var2=None, *args, **kwargs):
    if not mod_id or not var1 or not var2:
        return
    rename_variation(pif, mod_id, var1, var1 + 'x')
    rename_variation(pif, mod_id, var2, var1)
    rename_variation(pif, mod_id, var1 + 'x', var2)


def copy_variation(pif, mod_id, old_var_id, new_var_id, *args, **kwargs):  # pragma: no cover
    # verbose = False
    if pif.argv:
        useful.write_message('copy_variation', mod_id, old_var_id, new_var_id)
    if old_var_id == new_var_id:
        return

    var = pif.dbh.fetch_variation(mod_id, old_var_id)
    if var:
        var = pif.dbh.depref('variation', var)
        var['imported_var'] = new_var_id
        pif.dbh.insert_variation(mod_id, new_var_id, var)


def run_search_command(pif, args):
    mods = pif.dbh.fetch_variations(args[0])
    mods.sort(key=lambda x: x['variation.var'])
    for mod in mods:
        useful.write_message('%(mod_id)-8s|%(var)-5s|%(imported_from)-8s|%(text_description)-s' %
                             pif.dbh.depref('variation', mod))


def verify(pif, flag, mod_id, *var_ids):
    # need to read the old flags and modify
    flag = (config.FLAG_MODEL_VARIATION_VERIFIED if flag == 'v' else
            config.FLAG_MODEL_VARIATION_VERIFIED | config.FLAG_MODEL_ID_INCORRECT if flag == 'i' else 0)
    var = {'variation.mod_id': mod_id, 'flags': flag}
    for var_id in var_ids:
        print('verify', mod_id, var_id)
        var['variation.var'] = var_id
        pif.dbh.update_variation_bare(var)


def add_value(pif, mod_id=None, var_id=None, attribute=None, *args):
    value = ' '.join(args)
    mod = pif.dbh.fetch_casting(mod_id)
    if not mod:
        print(mod_id, 'not found')
        return
    attrs = {x['attribute_name']: x for x in pif.dbh.depref('attribute', pif.dbh.fetch_attributes(mod_id))}
    if attribute not in (detail_attributes + list(attrs.keys())):
        print(attribute, 'not found')
        return
    attr = attrs.get(attribute)
    vars = {x['var']: x for x in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id))}
    # var = {}
    if var_id == 'default':
        var_id = ''
        var_id_list = []
    elif var_id == 'all':
        var_id = '*'
        var_id_list = [x for x, y in vars.items() if not y.get(attribute)]
    elif var_id == 'force':
        var_id = '*'
        var_id_list = list(vars.keys())
    elif var_id not in vars:
        print(var_id, 'not found')
        return
    else:
        # var = [vars[var_id]]
        var_id_list = [var_id]

    print(mod_id, var_id_list, attribute, attr['id'] if attr else None, '=>', value)
    if var_id:
        for var_id in var_id_list:
            new_value = vars[var_id][value[1:]] if value.startswith('&') else value
            if attribute in detail_attributes and var_id:
                pif.dbh.update_variation({attribute: new_value}, {'mod_id': mod_id, 'var': var_id})
            else:
                print(pif.dbh.add_or_update_detail(
                    {'description': new_value, 'mod_id': mod_id, 'var_id': var_id, 'attr_id': attr['id']},
                    {'mod_id': mod_id, 'var_id': var_id, 'attr_id': attr['id']}, verbose=True))
    else:
        print(pif.dbh.add_or_update_detail(
            {'description': value, 'mod_id': mod_id, 'var_id': var_id, 'attr_id': attr['id']},
            {'mod_id': mod_id, 'var_id': var_id, 'attr_id': attr['id']}, verbose=True))
    pif.dbh.recalc_description(mod_id)


def list_variations(pif, mod_id=None, var_id=None, *args, **kwargs):
    if not mod_id:
        return
    if var_id:
        var = pif.dbh.depref('variation', pif.dbh.fetch_variation(mod_id, var_id))
        if var:
            fmt = pif.dbh.preformat_results(var.items())
            for item in sorted(var[0].items()):
                print(fmt % item)
    else:
        for variation in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
            useful.write_message('%5s: %s' % (variation['var'], variation['text_description']))


def list_variation_pictures(pif, start=None, end=None, *args, **kwargs):
    # very similar to do_var_detail(pif, model, attributes, credits)

    def mk_star(has_thing):
        return 'X' if has_thing else '-'

    fmt_str = (
        '%(ID)-12s %(Cat)-8s %(Ty)-5s %(Cr)-4s %(Pic)-5s|%(De)s %(Ba)s %(Bo)s %(In)s %(Wh)s %(Wi)s|%(T)s %(S)s %(M)s '
        '%(L)s|%(Description)s')
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
    useful.write_message(fmt_str % row)
    for mod_id in mod_ids[mod_ids.index(start):mod_ids.index(end) + 1]:
        useful.write_message(
            '--------------------------------------+-----------+-------+-------------------------------------------')
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
        useful.write_message(fmt_str % row)
        credits = {x['photo_credit.name'].lower(): x['photographer.id']
                   for x in pif.dbh.fetch_photo_credits_for_vars(
            path=config.IMG_DIR_VAR[1:], name=mod_id, verbose=False)}
        for model in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
            pic_id = model['picture_id'] if model['picture_id'] else model['var']
            varsel = pif.dbh.fetch_variation_selects(model['mod_id'], model['var'])
            phcred = credits.get(('%s-%s' % (model['mod_id'], pic_id)).lower(), '')
            ty_var, is_found, has = mbmods.calc_var_pics(pif, model)
            cat_v = set(model['category'].split())
            cat_vs = set([x['variation_select.category'] for x in varsel])
            cat = ' '.join(cat_v) + ('/' + ' '.join(cat_vs)) if cat_v != cat_vs else ''
            row = {
                'ID': model['mod_id'] + '-' + model['var'],
                'Description': model['text_description'],
                'Cat': cat,
                'Ty': mbdata.var_types.get(ty_var, ty_var),
                'Cr': phcred,
                'Pic': model['picture_id'],
            }
            row.update({mbmods.text_short_titles[k]: mk_star(has[k]) for k in has})
            row.update(check_picture_sizes(config.IMG_DIR_VAR, model['mod_id'] + '-' + pic_id + '.jpg', mk_star))
            # for sz in mbdata.image_size_types:
            #     row[sz.upper()] = mk_star(
            #         os.path.exists(useful.relpath('.', config.IMG_DIR_VAR, sz + '_' + model['mod_id'] +
            #                           '-' + pic_id + '.jpg').lower()))
            useful.write_message(fmt_str % row)


def check_picture_sizes(pdir, root, mk_star):
    exists = [os.path.exists(useful.relpath('.', pdir, sz + '_' + root).lower()) for sz in mbdata.image_size_types]
    ret = {'_any': any(exists)}
    ret.update(dict(zip([x.upper() for x in mbdata.image_size_types], [mk_star(x) for x in exists])))
    return ret


def fix_variation_type(pif, start=None, end=None, *args, **kwargs):
    # very similar to do_var_detail(pif, model, attributes, credits)

    mod_ids = sorted(pif.dbh.fetch_casting_ids())
    if not start:
        start = mod_ids[0]
        end = mod_ids[-1]
    elif not end:
        end = start
    for mod_id in mod_ids[mod_ids.index(start):mod_ids.index(end) + 1]:
        # mod = pif.dbh.fetch_casting(mod_id)
        for var in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
            ty_var = mbmods.calc_var_type(pif, var)
            if ty_var != var['variation_type']:
                useful.write_message(var['mod_id'], var['var'], ty_var)
                # pif.dbh.update_variation({'varation_type': ty_var}, {'mod_id': var['mod_id'], 'var': var['var']})
                wheres = pif.dbh.make_where(var, cols=['mod_id', 'var'])
                pif.dbh.write('variation', {'variation_type': ty_var}, wheres, modonly=True, tag='FixVarType')


def list_photo_credits(pif, photog_id=None):
    start = end = None
    # hide private?
    photogs = [photog_id] if photog_id else sorted([x.photographer.id for x in pif.dbh.fetch_photographers()])
    # photogs = [photog_id] if photog_id else sorted([x.photographer.id
    #                   for x in pif.dbh.fetch_photographers(config.FLAG_ITEM_HIDDEN)])
    totals = {x: 0 for x in photogs}
    totals['mod_id'] = totals['main'] = totals['count'] = totals['model_type'] = ''
    fmt_str = '%(mod_id)-6s %(model_type)2s %(main)-4s %(count)7s | ' + ' '.join(['%%(%s)7s' % x for x in photogs])
    headers = {'mod_id': '', 'main': 'Main', 'count': 'Total', 'model_type': 'MT'}
    headers.update({x: x for x in photogs})
    useful.write_message(fmt_str % headers)
    mod_ids = sorted(pif.dbh.fetch_casting_ids())
    if not start:
        start = mod_ids[0]
        end = mod_ids[-1]
    elif not end:
        end = start
    for mod_id in mod_ids[mod_ids.index(start):mod_ids.index(end) + 1]:
        mod = pif.dbh.fetch_casting(mod_id)
        main_phcred = pif.dbh.fetch_photo_credit(path=config.IMG_DIR_MAN[1:], name=mod_id, verbose=False)
        credits = {x['photo_credit.name'].lower(): x['photographer.id']
                   for x in pif.dbh.fetch_photo_credits_for_vars(
            path=config.IMG_DIR_VAR[1:], name=mod_id, verbose=False)}
        row = {x: 0 for x in photogs}
        row['mod_id'] = mod_id
        row['model_type'] = mod['model_type']
        row['main'] = main_phcred['photographer.id'] if main_phcred else ''
        row['count'] = 0
        for model in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
            if model['picture_id']:
                continue
            ty_var, is_found, has = mbmods.calc_var_pics(pif, model)
            if mbdata.var_types.get(ty_var, ty_var) == 'C2':
                continue
            phcred = credits.get(f"{model['mod_id']}-{model['var']}".lower(), '')
            row['count'] += 1
            if phcred in photogs:
                row[phcred] += 1
                totals[phcred] += 1
        for ph in photogs:
            if row[ph] == row['count']:
                row[ph] = 'all'
        useful.write_message(fmt_str % row)
    useful.write_message(fmt_str % totals)


def count_photo_credits(pif):
    pass
    # pc = pif.dbh.fetch('photographer', left_joins=[('photo_credit', 'casting.make=vehicle_make.id')]
    # def fetch(self, table_name, args=None, left_joins=None, columns=None, extras=False, where=None, group=None,
    #           order=None, one=False, distinct=False, limit=None, tag='Fetch', verbose=False):
    # )


def info(pif, fields=None, mod_id=None, var_id=None, *args, **kwargs):
    if not mod_id:
        return
    fields = fields.split(',') if (fields and fields != '.') else []
    if var_id:
        variation = pif.dbh.depref('variation', pif.dbh.fetch_variation(mod_id, var_id))
        if variation:
            if fields:
                useful.write_message('|'.join([str(variation[f]) for f in fields]))
            else:
                useful.write_message('|'.join([str(variation[f]) for f in sorted(variation.keys())]))
    else:
        for variation in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
            if fields:
                useful.write_message('|'.join([str(variation[f]) for f in fields]))
            else:
                useful.write_message('|'.join([str(variation[f]) for f in sorted(variation.keys())]))


def add_variation(pif, mod_id=None, var_id=None, *args, **kwargs):  # pragma: no cover
    if mod_id and var_id:
        new_var = {'body': ' '.join(args), 'imported_from': 'cl', 'imported_var': var_id}
        new_var.update(kwargs)
        var = pif.dbh.fetch_variation(mod_id, var_id)
        if var:
            print('That variation already exists!', mod_id, var_id)
        else:
            pif.dbh.insert_variation(mod_id, var_id, new_var)
            pif.dbh.recalc_description(mod_id)


def count_vars(pif, filelist=None):
    # count = 0
    # verbose = True
    # showtexts = True
    if not filelist:
        castings = [x['id'] for x in pif.dbh.dbi.select('casting', verbose=False)]
    elif filelist[0][0] >= 'a':
        castings = [x['id'] for x in pif.dbh.dbi.select(
            'casting', where=f"section_id='{filelist[0]}'", verbose=False)]
    else:
        castings = filelist
        # verbose = True
    t_founds = [0, 0, 0, 0, 0, 0]
    t_needs = [0, 0, 0, 0, 0, 0]
    t_cnts = [0, 0, 0, 0, 0, 0, 0]

    def adder(into_arr, from_tup):
        return [sum(x) for x in zip(into_arr, from_tup)]

    print('(f_a, f_c, f_1, f_2, f_f, f_p), (n_a, n_c, n_1, n_2, n_f, n_p), '
          '(c_vars, c_de, c_ba, c_bo, c_in, c_wh, c_wi)')
    for mod_id in castings:
        # sys.stdout.write(casting + ' ')
        sys.stdout.flush()
        founds, needs, cnts, id_set = mbmods.count_list_var_pics(pif, mod_id)
        print(mod_id, founds, needs, cnts)
        t_founds = adder(t_founds, founds)
        t_needs = adder(t_needs, needs)
        t_cnts = adder(t_cnts, cnts)
    print('total', t_founds, t_needs, t_cnts)


def fix_var(pif):
    for mod_id in pif.dbh.fetch_casting_ids():
        for var in pif.dbh.fetch_variations_bare(mod_id):
            print(var['variation.mod_id'], var['variation.var'])
            rec = {
                'base': var['variation.base'].strip(),
                'body': var['variation.body'].strip(),
                'deco': var['variation.deco'].strip(),
                'interior': var['variation.interior'].strip(),
                'windows': var['variation.windows'].strip(),
            }
            where = {
                'mod_id': var['variation.mod_id'],
                'var': var['variation.var'],
            }
            pif.dbh.update_variation(rec, where)


def check_variation_select(pif):
    print('missing models')
    res = pif.dbh.raw_execute(
        '''select mod_id, id from variation_select where mod_id not in (select mod_id from casting);''')
    for r in res[0]:
        print(r)

    print('missing variations')
    res = pif.dbh.raw_execute(
        '''select * from variation_select where (mod_id, var_id) not in (select mod_id, var from variation);''')
    for r in res[0]:
        print(r)

    print('missing categories')
    res = pif.dbh.raw_execute(
        '''select * from variation_select where cateogory not in (select id from category);''')
    for r in res[0]:
        print(r)

    print('missing pages')
    res = pif.dbh.raw_execute(
        "select ref_id, id from variation_select where ref_id != '' and ref_id not in (select id var from page_info);")
    pages = {}
    for r, id in res[0]:
        pages.setdefault(r, [])
        pages[r].append(id)
    for k, v in pages.items():
        print(k, v)

    print('duplicates')
    res = pif.dbh.fetch_variation_selects(bare=True)
    resd = {}
    for r in res:
        if r.ref_id:
            k = f'{r.ref_id}/{r.sec_id}/{r.ran_id}/{r.mod_id}/{r.var_id}'
            resd.setdefault(k, set())
            resd[k].add(str(r.category.id))
    for k, v in resd.items():
        if len(v) > 1:
            print(k, sorted(v))


# not in use right now
def check_table_data(pif):
    for table in pif.dbh.table_data:
        print(table)
        dats = pif.dbh.dbi.execute('select * from ' + table)[0]
        cols = pif.dbh.describe(table)
        # types = list()
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
                except Exception:
                    print(table, col, dat)
            for c in s:
                if ord(c) > 127:
                    print(table, dat)


def check_mod_data(pif):
    variation_id_sets = create_var_id_sets(pif)
    mods = pif.dbh.fetch_casting_list()
    modd = {x['casting.id']: x for x in mods}
    ret = False
    for modset in variation_id_sets:
        for mod in modset[1:]:
            if modd[mod]['casting.variation_digits'] != modd[modset[0]]['casting.variation_digits']:
                print('vardig mismatch:', mod, modd[mod]['casting.variation_digits'], modset[0],
                      modd[modset[0]]['casting.variation_digits'])
                ret = True
    return ret


def create_var_id_sets(pif, mod_id=None):
    crs = pif.dbh.fetch_casting_relateds(section_id='single', mod_id=mod_id)
    crs = [sorted([x['casting_related.model_id'], x['casting_related.related_id']])
           for x in crs if x['casting_related.flags'] & 2]
    cr_d = {}
    seen = []
    for cr in crs:
        if cr[0] not in seen or cr[1] not in seen:
            cr_d.setdefault(cr[0], set())
            cr_d[cr[0]].add(cr[0])
            cr_d[cr[0]].add(cr[1])
            seen.extend(cr)
    return sorted([sorted(x) for x in cr_d.values()])


def get_vars(pif, mod_ids):
    varlist = []
    for mod_id in mod_ids:
        varlist.extend(pif.dbh.fetch_variations(mod_id))
    return varlist


def check_var_cats(pif, *mod_id_list):
    db_cats = set([x.id for x in pif.dbh.fetch_categories()])
    variation_id_sets = create_var_id_sets(pif)
    mods = pif.dbh.fetch_casting_list()
    mods.sort(key=lambda x: x['casting.id'])
    for mod in mods:
        mod_id = mod['casting.id']
        if mod_id_list and mod_id not in mod_id_list:
            continue
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
            varsels = pif.dbh.fetch_variation_selects(mod_id, vid)
            vs_cats = set([x['variation_select.category'] for x in varsels])
            cats = set(var['variation.category'].split())
            if cats - db_cats:
                print('unknown cat', mod_id, vid, var['variation.category'], '-', cats - db_cats)
            if cats - vs_cats:
                print('orphan cat', mod_id, vid, var['variation.category'], '-', cats - vs_cats)
        missing = []
        if id_nums:
            for vid in range(1, max(id_nums)):
                if vid not in id_nums:
                    missing.append(str(vid))
        if missing:
            print(mod_id, ':', ', '.join(missing))


def check_var_data(pif, *mod_id_list):
    db_cats = set([x['category.id'] for x in pif.dbh.fetch_category_counts()])
    mods = pif.dbh.fetch_casting_list()
    mods.sort(key=lambda x: x['casting.id'])
    for mod in mods:
        mod_id = mod['casting.id']
        if mod_id_list and mod_id not in mod_id_list:
            continue
        mod_ids = [mod_id]
        varlist = get_vars(pif, mod_ids)
        var_id_list = [var['variation.var'].lower() for var in varlist if not var['variation.picture_id']]
        id_nums = set()
        for var in varlist:
            vid = var['variation.var']
            if var['variation.picture_id'] and var['variation.picture_id'].lower() not in var_id_list:
                print('*** picture_id', mod_id, vid, var['variation.picture_id'])
            nid = mbdata.normalize_var_id(mod, vid)
            cats = set(var['variation.category'].split())
            if nid != vid:
                print('*** id mismatch', mod_id, vid, nid)
            if cats - db_cats:
                print('cat', mod_id, vid, var['variation.category'])
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
            print(mod_id, ':', ', '.join(missing))


def show_cats(pif, *mod_ids):
    fmt = '%-12s %-8s %-12s %-12s'
    print(fmt % ('Mod ID', 'Var', 'From Var', 'From VS'))
    for mod_id in mod_ids:
        vars = pif.dbh.fetch_variations(mod_id)
        for var in vars:
            print(fmt % (var['variation.mod_id'], var['variation.var'],
                         ' '.join(sorted(var['variation.category'].split(' '))),
                         ' '.join(sorted(set([x['variation_select.category'] for x in var['vs']])))))


def check_tilley_credits(pif):
    mans = imglib.get_tilley_file()
    dn = 'lib/man/'
    for man in sorted(mans):
        # print(man, ':')
        targs = [(x, os.stat(x).st_size, ) for x in glob.glob('.' + config.IMG_DIR_VAR + '/l_' + man + '-*.*')]
        credits = {'.' + config.IMG_DIR_VAR + '/l_' + x['photo_credit.name'] + '.jpg': x['photographer.id']
                   for x in pif.dbh.fetch_photo_credits_for_vars(config.IMG_DIR_VAR, man)}
        for pref in mans[man]:
            fl = glob.glob(dn + man + '/' + pref + '*.jpg')
            if not fl:
                print('!', man, pref)
                continue
            for fn in fl:
                ssize = os.stat(fn).st_size
                for tf in targs:
                    if tf[1] == ssize and filecmp.cmp(tf[0], fn) and credits.get(tf[0] != 'DT'):
                        print('x', man, tf[0], credits.get(tf[0], ''))


def copy_base(pif, mod_id, old_var_id, *new_var_ids):
    for new_var_id in new_var_ids:  # yes, i'm lazy, why do you ask?
        var_dict = pif.dbh.depref('variation', pif.dbh.fetch_variation_bare(mod_id, new_var_id))
        if var_dict:
            var_dict = copy_base_info(pif, mod_id, var_dict[0], old_var_id)
            del var_dict['imported']
            print(pif.dbh.write('variation', var_dict, tag='CopyBase'))
            pif.dbh.recalc_description(mod_id)


def copy_base_info(pif, mod_id, var_dict, old_var_id):
    other_var = pif.dbh.depref('variation', pif.dbh.fetch_variation_bare(mod_id, old_var_id))
    if other_var:
        other_var = other_var[0]
        useful.write_message('copying base info', mod_id, var_dict['var'], old_var_id)
        for attr in base_attributes + ['logo_type']:
            if not var_dict.get(attr):
                var_dict[attr] = other_var[attr] or ''
    return var_dict


def check_attributes(pif, *attr_names):
    if not attr_names:
        attr_names = sorted(set([x['attribute.attribute_name'] for x in pif.dbh.fetch_attributes_by_name()]))
    for attr_name in attr_names:
        mod_ids = [x['attribute.mod_id'] for x in pif.dbh.fetch_attributes_by_name(attr_name)]
        print(f"{len(mod_ids)} {attr_name} ({', '.join(sorted(mod_ids))})")


cmds = [
    ('d', delete_variation, "delete: mod_id var_id"),
    ('a', add_variation, "add: mod_id var_id body"),
    ('r', rename_variation, "rename: mod_id old_var_id new_var_id"),
    ('c', copy_variation, "copy: mod_id old_var_id new_var_id"),
    ('s', swap_variations, "swap: mod_id var_id_1 var_id_2"),
    ('m', move_variation, "move: old_mod_id old_var_id new_mod_id [new_var_id]"),
    ('f', run_search_command, "search: obj ..."),
    ('i', info, "info: fields mod_id var_id"),
    ('v', add_value, "value: mod_id var_id-or-default-or-all-or-force attribute value"),
    ('mp', rename_variation_pictures, "move picture: old_mod_id, old_var_id, new_mod_id, new_var_id"),
    ('cb', copy_base, "copy base: mod_id var_id var_id"),
    ('l', list_variations, "list: mod_id"),
    ('p', list_variation_pictures, "pictures: mod_id"),
    ('pc', list_photo_credits, "photo credits"),
    ('cpc', count_photo_credits, "count photo credits"),
    ('ver', verify, "verify: [v|i|u] mod_id var_id ..."),
    ('cv', count_vars, "count vars"),   # broken
    ('x', fix_var, "fix var"),
    ('ckvs', check_variation_select, "check variation select"),
    ('ckmd', check_mod_data, "check model data"),
    ('ckvd', check_var_data, "check variation data"),
    ('ckc', check_var_cats, "check variation categories"),
    ('cat', show_cats, "cats: mod_id ..."),
    ('fvt', fix_variation_type, "mod_id [mod_id]"),
    ('tilley', check_tilley_credits, "do the tilley thing"),
    ('ckat', check_attributes, "check attributes: [attr_name]..."),
]


if __name__ == '__main__':  # pragma: no cover
    basics.process_command_list(cmds=cmds, dbedit='')
