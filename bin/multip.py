#!/usr/local/bin/python

import glob
import os

import basics
import config
import mbdata
import models
import render
import useful

# ---------------------------------------------------------------------

# columns, colspan, rowspan, picsize
# columns MUST NOT exceed 4!
# picsize MUST NOT exceed h!
# colspan must be <= columns!
pack_layout_keys = ['columns', 'colspan', 'rowspan', 'picsize']
pack_layouts = {
    '01s': [1, 1, 1, 'h'],
    '02v': [2, 1, 2, 'l'],
    '03v': [2, 1, 3, 'm'],
    '04v': [2, 1, 4, 'm'],
    '05h': [4, 3, 1, 'l'],
    '05l': [2, 1, 3, 'l'],
    '05s': [3, 2, 2, 'l'],
    '05v': [2, 1, 5, 'm'],
    '06s': [3, 2, 3, 'l'],
    '06v': [2, 1, 4, 'm'],
    '07s': [4, 3, 3, 'l'],
    '08s': [3, 2, 2, 'l'],
    '08v': [4, 3, 4, 'm'],
    '10h': [4, 3, 2, 'l'],
    '10v': [3, 2, 4, 'm'],
    '2xh': [2, 2, 1, 'h'],
    '3xh': [3, 3, 1, 'h'],
    '4xh': [4, 4, 1, 'h'],
}


# ---- pack list ------------------------------------------------------


def make_pack_list(pif, format_type, sec='', year='', region='', lid='', material='', verbose=False):
    # need to adapt this for id-var
    pif.render.set_button_comment(pif)
    years = set()
    regions = set()
    materials = set()
    title = pif.form.search('title')
    sections = pif.dbh.fetch_sections({'page_id': pif.page_id})

    pack_ids_found = []
    llineup = render.Listix()
    sec_id = sec if sec else sections[0]['id'] if sections else '5packs'
    num_mods = 2 if sec_id == '2packs' else 10 if sec_id == '10packs' else 5
    page_id = pif.form.get_str('page')
    packs = pif.dbh.depref(['base_id', 'pack'], pif.dbh.fetch_packs(page_id=pif.page_id))
    sizes = make_imgsizes(pif, pif.render.pic_dir)

    for lsection in sections:
        if sec and lsection['id'] != sec:
            continue

        cols = ['pic', 'name', 'year', 'product_code', 'material']
        heads = ['', 'Name', 'Year', 'Product Code', 'Material']
        if verbose:
            cols = ['edlink'] + cols + ['region', 'country', 'layout', 'thumb', 'stars', 'rel']
            heads = ['Pack ID'] + heads + ['Rg', 'Cy', 'Ly', 'Th', 'Models', 'Related']
        elif lsection['flags'] & config.FLAG_SECTION_SHOW_IDS:
            cols = ['id'] + cols + ['regionname']
            heads = ['ID'] + heads + ['Region']
        else:
            cols += ['regionname']
            heads += ['Region']
        cols += ['note']
        heads += ['Note']

        entries = list()
        for pack in packs:
            if pack['section_id'] == lsection['id']:
                if not verbose and pack['id'] in pack_ids_found:
                    continue
                pack_ids_found.append(pack['id'])
                years.add(pack['first_year'])
                regions.add(pack['region'])
                materials.add(pack['material'])
                pack['name'] = pack['rawname'].replace(';', ' ')
                if ((year and (year < pack['first_year'] or year > pack['end_year'])) or
                        (region and region != pack['region']) or
                        (lid and not pack['id'].startswith(lid)) or
                        (material and material != pack['material']) or
                        not useful.search_match(title, pack['name'])):
                    continue

                pack['year'] = ((pack['first_year'] + '-' + pack['end_year'])
                                if (pack['end_year'] and pack['end_year'] != pack['first_year']) else
                                pack['first_year'])
                pack['layout'] = (pack['layout'] if pack['layout'] in pack_layouts else
                                  '<font color="red">%s</font>' % pack['layout'])
                pack['page'] = page_id
                pack['regionname'] = mbdata.regions[pack['region']]
                pack['pic'] = mbdata.comment_icon.get('c') if imgsizes(
                    pif, pif.render.pic_dir, pack['id'].lower(), sizes) else ''
                pack['material'] = mbdata.materials.get(pack['material'], '')
                if pack['flags'] & config.FLAG_MODEL_NOT_MADE:
                    pack['product_code'] = mbdata.comment_icon.get('n')
                else:
                    pack['name'] = '<a href="?page=%(page)s&id=%(id)s">%(name)s</a>' % pack
                pack['longid'] = pack['id'] + ('-' + pack['var'] if pack['var'] else '')
                if verbose:
                    modify_pack_admin(pif, pack)
                entries.append(pack)
        if not entries and not pif.is_allowed('a'):
            continue
        entries.sort(key=lambda x: (x[pif.form.get_str('order', 'first_year')], x['rawname'], x['first_year']))
        lsec = render.Section(section=lsection, colist=cols, headers=dict(zip(cols, heads)), note='',
                              range=[render.Range(entry=entries, note='', styles=dict(zip(cols, cols)))])
        if pif.is_allowed('a'):  # pragma: no cover
            if format_type == 'packs':
                lsec.name += ' ' + pif.render.format_button_link('see', f"packs.cgi?page={page_id}&sec={lsec.id}")
            lsec.name += ' ' + pif.render.format_button_link(
                'add', f"mass.cgi?tymass=pack&section_id={sec_id}&num={num_mods}")

        llineup.section.append(lsec)
    context = {
        'page_id': pif.page_id,
        'years': sorted(years),
        'regions': [(x, mbdata.regions[x]) for x in sorted(regions)],
        'materials': [(x, mbdata.materials.get(x, 'unknown')) for x in sorted(materials)],
        'llineup': llineup.prep(),
        'section_id': sec_id,
        'num': num_mods,
        # 'lid': calc_pack_select(pif, packs),
    }
    return pif.render.format_template('packlist.html', **context)


def modify_pack_admin(pif, pack):
    pmodels = distill_models(pif, pack, pif.page_id)
    stars = ''
    for mod in sorted(pmodels.keys()):
        if not pmodels[mod].get('id'):
            stars += '<i class="fas fa-star green"></i> '
        elif not pmodels[mod].get('vs.var_id'):
            stars += '<i class="fas fa-star red"></i> '
        elif pmodels[mod]['imgstr'].find('-') < 0:
            stars += '<i class="fas fa-star yellow"></i> '
        else:
            stars += '<i class="fas fa-star black"></i> '
    pack['stars'] = stars
    pack['edlink'] = (
        '<a href="mass.cgi?verbose=1&tymass=pack&section_id=%(section_id)s&pack=%(id)s&var=%(var)s&num=">%(longid)s</a>'
        % pack)
    relateds = pif.dbh.fetch_packs_related(pack['id'])
    pack['rel'] = ' '.join(sorted([x['pack.id'] for x in relateds]))


# ---- single pack ----------------------------------------------------


def do_single_pack(pif, format_type, pid):
    pack = dict()
    packs = pif.dbh.fetch_pack(pid)
    if not packs:
        raise useful.SimpleError("That %s doesn't seem to exist." % ('pack' if format_type == 'packs' else 'playset'))
    pif.render.hierarchy_append('', packs[0]['base_id.rawname'].replace(';', ' '))
    pif.render.print_html()

    llineup = render.Matrix(tail=[''])
    for pack in packs:
        pack_id = pack['pack.id']
        page_id = pack['pack.page_id']
        pack['longid'] = pack_id + ('-' + pack['pack.var'] if pack['pack.var'] else '')
        db_relateds = pif.dbh.fetch_packs_related(pack_id)
        relateds = [
            {
                'link': pif.render.format_link("?page=" + pif.form.get_str('page') + "&id=" + r['pack.id'],
                                               r['base_id.rawname'].replace(';', ' ')),
                'product_code': r['pack.product_code'],
                'region': mbdata.regions.get(r['pack.region'], ''),
                'country': mbdata.get_country(r['pack.country']),
                'material': mbdata.materials.get(r['pack.material'], ''),
                'description': r['base_id.description'],
            }
            for r in db_relateds
        ]

        tcomments = set()
        pack.update({key[key.find('.') + 1:]: pack[key] for key in pack})
        pack['name'] = pack['rawname'].replace(';', ' ')

        pmodels = distill_models(pif, pack, pack['page_id'])
        if pack['layout'].isdigit() and len(pack['layout']) == 4:
            layout = [int(x) for x in pack['layout'][:3]] + pack['layout'][3:]
        elif not pmodels:
            layout = pack_layouts['01s']
        else:
            layout = pack_layouts.get(pack['layout'], pack_layouts['4xh'])
        if len(layout) == 2:
            layout[3] = 1
        if len(layout) == 3:
            layout[4] = 4 - (layout[0] - layout[1])

        pif.render.comment('pack:', pack)
        entries = [render.Entry(
            text=show_pack(pif, pack, layout[3]), class_name='bg_lg width_' + layout[3],
            display_id='0', colspan=layout[1], rowspan=layout[2])]
        modvars = []
        for mod in sorted(pmodels.keys()):
            pmod = pmodels[mod]
            pif.render.comment("do_single_pack mod", pmod)
            modvars.append((f'vars.cgi?edt=1&mod={pmod["id"]}', pmodels[mod]["id"], pmod["pack_model.id"]))

            if not pmod.get('id'):
                pmod['no_casting'] = 1
                tcomments.add('m')
            else:
                if pmod['imgstr'].find('-') < 0:
                    tcomments.add('i')
                if not pmod.get('vs.var_id'):
                    pmod['no_variation'] = 1
                    tcomments.add('v')

            entries.append(
                render.Entry(text=show_pack_model(pif, pmod), class_name=pmod['style_id'] or 'wh', display_id=1))

        llineup.section.append(render.Section(id='', columns=layout[0], anchor=pack['id'],
                                              range=[render.Range(entry=entries)]))

    # left bar
    left_bar_content = ''
    if pif.is_allowed('a'):  # pragma: no cover
        cat = (':5P' if page_id in ('packs.5packs', 'packs.lic5packs') else
               ':10P' if page_id == 'packs.10packs' else
               ':3P' if page_id == 'packs.3packs' else '')
        left_bar_content += f'<br><center><span style="font-size: x-small;">{page_id}/{pack_id}{cat}</span><p>'
        left_bar_content += '<b><a href="%s">Pack</a></b><br>\n' % pif.dbh.get_editor_link('pack', {'id': pack_id})
        left_bar_content += ('<b><a href="traverse.cgi?d=%s">Library</a></b><br>\n' %
                             pif.render.pic_dir.replace('pic', 'lib'))
        left_bar_content += (
            '<b><a href="mass.cgi?verbose=1&tymass=pack&section_id=%s&pack=%s&num=">Edit</a></b><br>\n' %
            (packs[0]['section_id'], pack_id))
        # would like to pass in picsize (layout[3])
        left_bar_content += (
            '<p><a href="upload.cgi?d=./%s&n=%s">Package</a><br>\n' %
            (pif.render.pic_dir.replace('pic', 'lib'), pack_id) +
            '<b><a href="upload.cgi?d=./%s&n=%s">Contents</a><br>\n' %
            (pif.render.pic_dir.replace('prod', 'set').replace('pic', 'lib'), pack_id) +
            '<b><a href="upload.cgi?d=./%s&n=%s&m=%s&c=%s">Man</a><br>\n' %
            (config.IMG_DIR_MAN.replace('pic', 'lib'), pack_id, pack_id, pack_id) +
            '<p>\n')
        for lnk, mod, pmid in modvars:
            left_bar_content += (
                f'<a href="{lnk}">{mod}</a> '
                f'<a href="/cgi-bin/editor.cgi?table=pack_model&id={pmid}"> <i class="fas fa-edit gray"></i></a>'
                '<br>\n')
        left_bar_content += '</center>\n'

    pif.render.set_button_comment(pif, 'd=%s' % pif.form.get_str('id'))
    context = {
        'title': packs[0]['name'],
        'note': packs[0]['note'],
        'type_id': 'p_' + packs[0]['section_id'],
        'icon_id': '',  # pack_id,
        'vehicle_type': '',
        'rowspan': 4,
        'left_bar_content': left_bar_content,
        'llineup': llineup.prep(),
        'relateds': relateds,
    }
    return pif.render.format_template('pack.html', **context)


def make_imgsizes(pif, pdir):
    sizes = {}
    for fn in glob.glob(os.path.join(pdir, '?_*.jpg')):
        fn = fn[fn.rfind('/') + 1:-4]
        sizes.setdefault(fn[2:], [])
        sizes[fn[2:]].append(fn[0])
    return sizes


def imgsizes(pif, pdir, pic_id, sizes=None):
    sl = []
    if sizes:
        for k, v in sizes.items():
            if k == pic_id or k.startswith(pic_id + '-'):
                sl.extend(v)
    else:
        fl = [x[x.rfind('/') + 1:-4] for x in glob.glob(os.path.join(pdir, f'?_{pic_id}*.jpg'))]
        sl = [x[0] for x in fl if x[2:] == pic_id or x[2:].startswith(pic_id + '-')]
    return (' '.join(sorted(set(sl)))).upper()


def distill_models(pif, pack, page_id):
    pack_id = pack['id'] + ('-' + pack['var'] if pack['var'] else '')
    model_list = pif.dbh.fetch_pack_models(pack_id=pack['id'], pack_var=pack['var'], page_id=page_id)
    pack['pic'] = ''
    # for pic in glob.glob(os.path.join(config.IMG_DIR_PROD_PACK, '?_' + pack_id + '.jpg')):
    # path, pic = pif.render.find_image_file(pack_id, pdir=config.IMG_DIR_PROD_PACK, largest=mbdata.IMG_SIZ_HUGE)
    # pack['pic'] += imglib.format_image_star(pif, path, pic)
    pack['pic'] += imgsizes(pif, pif.render.pic_dir, pack_id.lower())
    linmod = pif.dbh.fetch_lineup_model(where="mod_id='%s'" % pack_id)
    pack['thumb'] = '<i class="far fa-%s"></i>' % ('check-square' if linmod else 'square')
    if ''.join(pif.render.find_image_file(pack_id, pdir=config.IMG_DIR_MAN, prefix=mbdata.IMG_SIZ_SMALL)):
        pack['thumb'] += '<i class="fas fa-star"></i>'
    pmodels = {}

    for mod in model_list:
        mod = pif.dbh.modify_man_item(mod)
        useful.write_comment('mod', mod)
        mod['style_id'] = 'bg_' + mod['pack_model.style_id']
        useful.write_comment(mod)
        mod['pdir'] = pif.render.pic_dir
        mod['spdir'] = mbdata.dirs.inverse.get(mod['pdir'], mod['pdir'])
        sec_ids = ['.', '', pack_id + '.', pack_id + '.' + str(mod['pack_model.display_order'])]
        if (mod['vs.sec_id'] or '') + '.' + (mod['vs.ran_id'] or '') in sec_ids:
            mod['imgl'] = [mbdata.IMG_SIZ_SMALL + '_' + mod['id'], mod['id'], mod['pack_model.mod_id']]
            for s in mod['descs']:
                if s.startswith('same as '):
                    mod['imgl'].extend([mbdata.IMG_SIZ_SMALL + '_' + s[8:], s[8:]])
            if not mod.get('vs.ref_id'):
                mod['vs.ref_id'] = ''
            if not mod.get('vs.sec_id'):
                mod['vs.sec_id'] = ''
            mod['pic_id'] = mod['vs.sec_id'] if mod['vs.sec_id'] else mod['pack_model.pack_id']
            if mod['pack_model.mod_id'] != 'unknown':
                mod['href'] = (
                    "single.cgi?id=%(pack_model.mod_id)s&dir=%(spdir)s&pic=%(pic_id)s&ref=%(vs.ref_id)s&"
                    "sec=%(vs.sec_id)s&ran=%(vs.ran_id)s" % mod)
            # '<a href="single.cgi?dir=%(dir)s&pic=%(link)s&ref=%(vs.ref_id)s&id=%(mod_id)s">' % ent
            # 'pack_model.pack_id': 'car02',
        #    if mod['pack_model.var'] and mod['imgl']:  # still not perfect
        #       mod['href'] = mod['href'] + '&pic=' + mod['imgl'][mod['imgl'].rfind('/') + 1:-2]
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
        pmodels[dispo]['imgstr'] = pif.render.format_image_required(
            pmodels[dispo]['imgl'], pdir=config.IMG_DIR_MAN, prefix=mbdata.IMG_SIZ_SMALL,
            vars=pmodels[dispo].get('pics'))
    return pmodels


# columns (id, page_id, section_id, name, first_year, end_year, region, layout, product_code, material, country)
def show_pack(pif, pack, picsize):
    pack_id = pack['id'] + ('-' + pack['var'] if pack['var'] else '')

    prod_credit = pif.dbh.fetch_photo_credit(pif.render.pic_dir, pack_id, verbose=True)
    pack['credit'] = prod_credit['photographer.name'] if prod_credit else ''
    prod_pic = pif.render.find_image_path(pack_id, largest=picsize)

    cont_dir = pif.render.pic_dir.replace('prod', 'set')
    # cont_credit = pif.dbh.fetch_photo_credit(cont_dir, pack_id, verbose=True)
    # pack['credit'] = cont_credit['photographer.name'] if cont_credit else ''
    cont_pic = pif.render.find_image_path(pack_id, largest=picsize, pdir=cont_dir)

    pics = []
    if prod_pic:
        ostr = prod_pic
        pics.append(prod_pic)
    if cont_pic:
        ostr = cont_pic
        pics.append(cont_pic)
    ostr = pif.render.format_image_selector(pics, 'ps') + '<br>'
    ostr += pif.render.format_image_selectable(pics, 'ps')
    if pack['credit']:
        ostr += '<div class="credit">Photo credit: %s</div>' % pack['credit']

    # Ideally this would come from section.flags but we don't have that here.
    # So this is a giant FAKE OUT
    if pack['var']:
        ostr = '<b>' + pack['id'] + '-' + pack['var'] + '</b><br>' + ostr

    year = pack['first_year'] if pack['first_year'] else ''
    if pack['first_year'] and pack['end_year'] and pack['end_year'] != pack['first_year']:
        year += '-' + pack['end_year']
    prod_title = [pack['base_id.rawname']]
    if year:
        prod_title.append(year)
    ostr += '<h4 class="prodtitle">{}</h4>'.format(' - '.join(prod_title))

    pack['country'] = mbdata.get_country(pack['country'])
    pack['material'] = mbdata.materials.get(pack['material'], '')
    if pack['product_code']:
        ostr += pack['product_code'] + '<br>'
    if pack['region']:
        ostr += mbdata.regions[pack['region']] + '<br>'
    ostr += '<p>'
    if pack['first_year'] and pack['end_year'] and pack['end_year'] != pack['first_year']:
        ostr += '<b>%(first_year)s-%(end_year)s</b><br>' % pack
    dets = filter(None, [pack['country'], pack['material']])
    ostr += ' - '.join(dets)
    return '<center>' + ostr + '</center>'


# mdict: descriptions href imgstr name no_casting not_made number pdir picture_only product subname
# def add_model_table_product_link(pif, mdict):

def show_pack_model(pif, mdict):
    pif.render.comment("show_pack_model", mdict)

    mdict['number'] = ''
    mdict['descriptions'] = []
    if mdict['v.text_description']:
        # mdict['v.text_description'] += (' (' + mdict['v.date'] + ')' if mdict.get('v.date') else '')
        mdict['descriptions'] = [mdict['v.text_description']]  # fix this
    mdict['product'] = ''
    if mdict['imgstr'].find('-') < 0:
        mdict['no_specific_image'] = 1

    desclist = list()
    for var in mdict.get('descriptions', []):
        if var and var not in desclist:
            desclist.append(var)

    mdict['descriptions'] = desclist

    if not mdict.get('disp_format') or not mdict.get('shown_id'):
        mdict['displayed_id'] = '&nbsp;'
    else:
        mdict['displayed_id'] = mdict['disp_format'] % (mdict['shown_id'])

    return models.add_model_table_product_link(pif, mdict)


# ---- main -----------------------------------------------------------


@basics.web_page
def packs_main(pif):

    def fmt_link(sec):
        return pif.render.format_link(
            '?sec=' + sec.id,
            models.add_icons(pif, 'p_' + sec.id, '', '') + '<center>' + sec.name + '</center>')

    pif.render.set_page_extra(pif.render.image_selector_js)
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('packs.cgi', 'Multi-Model Packs')
    if pif.form.has('id'):
        pif.render.hide_title = True
        pif.form.set_val('id', pif.form.get_list('id')[0])  # with no id this blows
        pid = useful.clean_id(pif.form.get_str('id'))
        return do_single_pack(pif, 'packs', pid)
    elif pif.form.has('page'):
        pif.render.print_html()
        return make_pack_list(
            pif, 'packs',
            verbose=pif.is_allowed('m') and pif.form.get_int('verbose'),
            **pif.form.get_dict(['sec', 'year', 'region', 'lid', 'material']))
    elif pif.form.has('sec'):
        pif.render.hide_title = True
        # useful.write_comment(pif.form)
        sections = pif.dbh.fetch_sections_by_page_type('packs', pif.form.get_str('sec'))
        if not sections:
            pif.render.print_html()
            return models.make_page_list(pif, 'packs', fmt_link)
        pif.page_id = sections[0].page_info.id
        pif.render.print_html()
        return make_pack_list(
            pif, 'packs',
            verbose=pif.is_allowed('m') and pif.form.get_int('verbose'),
            **pif.form.get_dict(['sec', 'year', 'region', 'lid', 'material']))
    pif.render.print_html()
    return models.make_page_list(pif, 'packs', fmt_link)


# ---- play ----------------------------------


@basics.web_page
def play_main(pif):
    pif.render.set_page_extra(pif.render.image_selector_js)
    # useful.write_comment(pif.form)
    pif.page_id = 'playset.ps'
    pif.set_page_info(pif.page_id)
    pif.render.print_html()
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('play.cgi', 'Playsets')
    if pif.form.has('id'):
        pif.form.set_val('id', pif.form.get_list('id')[0])  # with no id this blows
        pid = useful.clean_id(pif.form.get_str('id'))
        return do_single_pack(pif, 'playset', pid)
    return make_pack_list(pif, 'playset',
                          verbose=pif.is_allowed('m') and pif.form.get_int('verbose'),
                          **pif.form.get_dict(['sec', 'year', 'region']))
