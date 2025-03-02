#!/usr/local/bin/python

import glob
import os

import basics
import config
import mbdata
import mbmods
import render
import useful

# ---------------------------------------------------------------------

# columns, colspan, rowspan, picsize
# columns MUST NOT exceed 4!
# picsize MUST NOT exceed h!
# colspan must be <= columns!
pack_layout_keys = ['columns', 'colspan', 'rowspan', 'picsize']
pack_layouts = {
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
    '1xh': [1, 1, 1, 'h'],
    '2xh': [2, 2, 1, 'h'],
    '3xh': [3, 3, 1, 'h'],
    '4xh': [4, 4, 1, 'h'],
}


# ---- pack list ------------------------------------------------------


def make_pack_list(pif, format_type, sec='', year='', region='', lid='', material='', verbose=False):
    # need to adapt this for id-var
    pif.ren.set_button_comment(pif)
    years = set()
    regions = set()
    materials = set()
    title = pif.form.search('title')
    sections = pif.dbh.make_sec_items(pif.dbh.fetch_sections({'page_id': pif.page_id}))

    pack_ids_found = []
    llineup = render.Listix()
    sec_id = sec if sec else sections[0].id if sections else '5packs'
    num_mods = 2 if sec_id == '2packs' else 10 if sec_id == '10packs' else 5
    page_id = pif.form.get_str('page')
    packs = pif.dbh.make_pack_items(pif.dbh.fetch_packs(page_id=pif.page_id))
    sizes = make_imgsizes(pif, pif.ren.pic_dir)

    for lsection in sections:
        if sec and lsection.id != sec:
            continue

        cols = ['pic', 'name', 'year', 'product_code', 'material']
        heads = ['', 'Name', 'Year', 'Product Code', 'Material']
        if verbose:
            cols = ['edlink'] + cols + ['region', 'country', 'layout', 'thumb', 'stars', 'rel']
            heads = ['Pack ID'] + heads + ['Rg', 'Cy', 'Ly', 'Th', 'Models', 'Related']
        elif lsection.flags & config.FLAG_SECTION_SHOW_IDS:
            cols = ['id'] + cols + ['regionname']
            heads = ['ID'] + heads + ['Region']
        else:
            cols += ['regionname']
            heads += ['Region']
        cols += ['note']
        heads += ['Note']

        entries = list()
        for pack in packs:
            if pack.section_id == lsection.id:
                if not verbose and pack.id in pack_ids_found:
                    continue
                pack_ids_found.append(pack.id)
                years.add(pack.first_year)
                regions.add(pack.region)
                materials.add(pack.material)
                if ((year and (year < pack.first_year or year > pack.end_year)) or
                        (region and region != pack.region) or
                        (lid and not pack.id.startswith(lid)) or
                        (material and material != pack.material) or
                        not useful.search_match(title, pack.name)):
                    continue

                pack.year = (f"{pack.first_year}-{pack.end_year}"
                             if (pack.end_year and pack.end_year != pack.first_year) else pack.first_year)
                pack.layout = (pack.layout if pack.layout in pack_layouts else f'<font color="red">{pack.layout}</font>')
                pack.page = page_id
                pack.regionname = mbdata.regions[pack.region]
                pack.pic = mbdata.comment_icon.get('c') if imgsizes(
                    pif, pif.ren.pic_dir, pack.id.lower(), sizes) else ''
                pack.material = mbdata.materials.get(pack.material, '')
                if pack.flags & config.FLAG_MODEL_NOT_MADE:
                    pack.product_code = mbdata.comment_icon.get('n')
                else:
                    pack.name = f'<a href="?page={pack.page}&id={pack.id}">{pack.name}</a>'
                if verbose:
                    modify_pack_admin(pif, pack)
                entries.append(pack)
        if not entries and not pif.is_allowed('a'):
            continue
        entries.sort(key=lambda x: (getattr(x, pif.form.get_str('order', 'first_year')), x.rawname, x.first_year))
        lsec = render.Section(section=lsection, colist=cols, headers=dict(zip(cols, heads)), note='',
                              range=[render.Range(entry=entries, note='', styles=dict(zip(cols, cols)))])
        if pif.is_allowed('a'):  # pragma: no cover
            if format_type == 'packs':
                lsec.name += ' ' + pif.ren.format_button_link('see', f"packs.cgi?page={page_id}&sec={lsec.id}")
            lsec.name += ' ' + pif.ren.format_button_link(
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
    return pif.ren.format_template('packlist.html', **context)


def modify_pack_admin(pif, pack):
    pmodels = distill_models(pif, pack, pif.page_id)
    stars = ''
    for mod in sorted(pmodels.keys()):
        if not pmodels[mod].get('id'):
            stars += pif.ren.fmt_star('green')
        elif not pmodels[mod].get('vs.var_id'):
            stars += pif.ren.fmt_star('red')
        elif pmodels[mod]['imgstr'].find('-') < 0:
            stars += pif.ren.fmt_star('yellow')
        else:
            stars += pif.ren.fmt_star('black')
    pack.stars = stars
    pack.edlink = (
        '<a href="mass.cgi?verbose=1&tymass=pack&'
        f'section_id={pack.section_id}&pack={pack.id}&var={pack.var}&num=">{pack.longid}</a>')
    relateds = pif.dbh.fetch_packs_related(pack.id)
    pack.rel = ' '.join(sorted([x['pack.id'] for x in relateds]))


# ---- single pack ----------------------------------------------------


def do_single_pack(pif, format_type, pid):
    packs = pif.dbh.make_pack_items(pif.dbh.fetch_pack(pid))
    if not packs:
        raise useful.SimpleError("That %s doesn't seem to exist." % ('pack' if format_type == 'packs' else 'playset'))
    pif.ren.hierarchy_append('', packs[0].rawname.replace(';', ' '))
    pif.ren.print_html()

    llineup = render.Matrix(tail=[''])
    for pack in packs:
        pack_id = pack.id
        page_id = pack.page_id
        db_relateds = pif.dbh.fetch_packs_related(pack_id)
        relateds = [
            {
                'link': pif.ren.format_link("?page=" + pif.form.get_str('page') + "&id=" + r['pack.id'],
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

        pmodels = distill_models(pif, pack, pack.page_id)
        if pack.layout.isdigit() and len(pack.layout) == 4:
            layout = [int(x) for x in pack.layout[:3]] + pack['layout'][3:]
        elif not pmodels:
            layout = pack_layouts['1xh']
        else:
            layout = pack_layouts.get(pack.layout, pack_layouts['4xh'])
        if len(layout) == 2:
            layout[3] = 1
        if len(layout) == 3:
            layout[4] = 4 - (layout[0] - layout[1])

        entries = [render.Entry(
            text=show_pack(pif, pack, layout[3]), class_name='bg_lg width_' + layout[3],
            display_id='0', colspan=layout[1], rowspan=layout[2])]
        modvars = []
        for mod in sorted(pmodels.keys()):
            pmod = pmodels[mod]
            pif.ren.comment("do_single_pack mod", pmod)
            modvars.append((f'vars.cgi?edt=1&mod={pmod.id}', pmodels[mod].mod_id, pmod.id))

            if not pmod.mod_id or pmod.mod_id == 'unknown':
                pmod.no_casting = 1
                tcomments.add('m')
            else:
                if pmod.imgstr.find('-') < 0:
                    tcomments.add('i')
                if not pmod.vs.var_id:
                    pmod.no_variation = 1
                    tcomments.add('v')

            entries.append(
                render.Entry(text=show_pack_model(pif, pmod), class_name=pmod.style_id or 'wh', display_id=1))

        llineup.comments = tcomments
        llineup.tail = ['', mbdata.text_comments(tcomments)]
        llineup.section.append(render.Section(id='', columns=layout[0], anchor=pack.id,
                                              range=[render.Range(entry=entries)]))

    left_bar_content = make_left_bar_content(pif, page_id, pack, modvars) if pif.is_allowed('a') else ''

    llineup.comments = tcomments
    llineup.tail = ['', '<br>'.join([mbdata.comment_designation[comment] for comment in sorted(tcomments)])]
    pif.ren.set_button_comment(pif, keys={'d': 'id'})
    context = {
        'title': packs[0].name,
        'note': packs[0].note,
        'type_id': 'p_' + packs[0].section_id,
        'icon_id': '',  # pack_id,
        'vehicle_type': '',
        'rowspan': 4,
        'left_bar_content': left_bar_content,
        'llineup': llineup.prep(),
        'relateds': relateds,
    }
    return pif.ren.format_template('pack.html', **context)


def make_left_bar_content(pif, page_id, pack, modvars):
    cat = (':5P' if page_id in ('packs.5packs', 'packs.lic5packs') else
           ':10P' if page_id == 'packs.10packs' else
           ':3P' if page_id == 'packs.3packs' else '')
    lib_set_dir = pif.ren.lib_dir.replace('prod', 'set')
    lib_man_dir = config.IMG_DIR_MAN.replace('pic', 'lib')
    lines = [
        '',
        f'<span style="font-size: x-small;">{page_id}/{pack.id}{cat}</span>',
        '',
        f'<b><a href="{pif.dbh.get_editor_link("pack", {"id": pack.id})}">Pack</a></b>',
        f'<b><a href="traverse.cgi?d={pif.ren.lib_dir}">Library</a></b>',
        f'<b><a href="mass.cgi?verbose=1&tymass=pack&section_id={pack.section_id}&pack={pack.id}&num=">Edit</a></b>',
        '',
        # would like to pass in picsize (layout[3])
        f'<b><a href="upload.cgi?d=./{pif.ren.lib_dir}&n={pack.id}">Package</a></b>',
        f'<b><a href="upload.cgi?d=./{lib_set_dir}&n={pack.id}">Contents</a></b>',
        f'<b><a href="upload.cgi?d=./{lib_man_dir}&n={pack.id}&m={pack.id}&c={pack.id}">Man</a></b>',
        '',
    ]
    for lnk, mod, pmid in modvars:
        lines.append(
            f'<a href="{lnk}">{mod}</a> '
            f'<a href="/cgi-bin/editor.cgi?table=pack_model&id={pmid}"> {pif.ren.fmt_edit("gray")}</a>')
    joiner = "\n<br>"  # because f-strings
    return f'<center>{joiner.join(lines)}</center>\n'


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
    pack_id = pack.longid
    pml = pif.dbh.fetch_pack_models(pack_id=pack.id, pack_var=pack.var, page_id=page_id)
    model_list = pif.dbh.make_pack_model_items(pml)
    pack.pic += imgsizes(pif, pif.ren.pic_dir, pack_id.lower())
    linmod = pif.dbh.fetch_lineup_model(where=f"mod_id='{pack_id}'")
    pack.thumb = pif.ren.fmt_square(hollow=True, checked=linmod)
    if ''.join(pif.ren.find_image_file(pack_id, pdir=config.IMG_DIR_MAN, prefix=mbdata.IMG_SIZ_SMALL)):
        pack.thumb += pif.ren.fmt_star('black')
    pmodels = {}

    for mod in model_list:
        mod.not_made = mod.picture_only = mod.no_specific_image = mod.no_casting = mod.no_variation = 0
        mod.show_vars = mod.is_product_picture = mod.is_reused_product_picture = 0
        mod.href = ''
        mod.style_id = 'bg_' + mod.style_id
        mod.pdir = pif.ren.pic_dir
        mod.spdir = mbdata.dirs_r.get(mod.pdir, mod.pdir)
        sec_ids = ['.', '', f"{pack_id}.", f"{pack_id}.{mod.display_order}"]
        if f"{mod.vs.sec_id}.{mod.vs.ran_id}" in sec_ids:
            mod.imgl = [mbdata.IMG_SIZ_SMALL + '_' + mod.mod_id, mod.mod_id]
            for s in mod.man.descs:
                if s.startswith('same as '):
                    mod.imgl.extend([mbdata.IMG_SIZ_SMALL + '_' + s[8:], s[8:]])
            if not mod.vs.ref_id:
                mod.vs.ref_id = ''
            if not mod.vs.sec_id:
                mod.vs.sec_id = ''
            mod.pic_id = mod.vs.sec_id or mod.pack_id
            if mod.mod_id != 'unknown':
                mod.href = (
                    f"single.cgi?id={mod.mod_id}&dir={mod.spdir}&pic={mod.pic_id}&ref={mod.vs.ref_id}&"
                    f"sec={mod.vs.sec_id}&ran={mod.vs.ran_id}")
            mod.vars = []
            mod.pics = []
            if mod.display_order not in pmodels:
                pmodels[mod.display_order] = mod
            if mod.v.picture_id:
                pmodels[mod.display_order].pics.append(mod.v.picture_id)
            else:
                pmodels[mod.display_order].pics.append(mod.vs.var_id)
            if mod.vs.var_id:
                pmodels[mod.display_order].vars.append(mod.vs.var_id)
    for dispo in pmodels:
        pmodels[dispo].imgstr = pif.ren.format_image_required(
            pmodels[dispo].imgl, pdir=config.IMG_DIR_MAN, prefix=mbdata.IMG_SIZ_SMALL,
            vars=pmodels[dispo].pics)
    return pmodels


# columns (id, page_id, section_id, name, first_year, end_year, region, layout, product_code, material, country)
def show_pack(pif, pack, picsize):
    pack_id = pack.longid

    prod_credit = pif.dbh.fetch_photo_credit(pif.ren.pic_dir, pack_id, verbose=True)
    pack.credit = prod_credit['photographer.name'] if prod_credit else ''
    prod_pic = pif.ren.find_image_path(pack_id, largest=picsize)

    cont_dir = pif.ren.pic_dir.replace('prod', 'set')
    cont_pic = pif.ren.find_image_path(pack_id, largest=picsize, pdir=cont_dir)

    pics = []
    if prod_pic:
        ostr = prod_pic
        pics.append(prod_pic)
    if cont_pic:
        ostr = cont_pic
        pics.append(cont_pic)
    ostr = pif.ren.format_image_selector(pics, 'ps') + '<br>'
    ostr += pif.ren.format_image_selectable(pics, 'ps')
    if pack.credit:
        ostr += f'<div class="credit">Photo credit: {pack.credit}</div>'

    # Ideally this would come from section.flags but we don't have that here.
    # So this is a giant FAKE OUT
    if pack.var:
        ostr = '<b>' + pack.longid + '</b><br>' + ostr

    year = pack.first_year if pack.first_year else ''
    if pack.first_year and pack.end_year and pack.end_year != pack.first_year:
        year += '-' + pack.end_year
    prod_title = [pack.name]
    if year:
        prod_title.append(year)
    ostr += '<h4 class="prodtitle">{}</h4>'.format(' - '.join(prod_title))

    pack.country = mbdata.get_country(pack.country)
    pack.material = mbdata.materials.get(pack.material, '')
    if pack.product_code:
        ostr += pack.product_code + '<br>'
    if pack.region:
        ostr += mbdata.regions[pack.region] + '<br>'
    ostr += '<p>'
    if pack.first_year and pack.end_year and pack.end_year != pack.first_year:
        ostr += f'<b>{pack.first_year}-{pack.end_year}</b><br>'
    dets = [x for x in [pack.country, pack.material] if x]
    ostr += ' - '.join(dets)
    return '<center>' + ostr + '</center>'


def show_pack_model(pif, mdict):
    mdict.anchor = mdict.number = ''
    mdict.descriptions = []
    if mdict.v.text_description:
        # mdict['v.text_description'] += (' (' + mdict['v.date'] + ')' if mdict.get('v.date') else '')
        mdict.descriptions = [mdict.v.text_description]  # fix this
    mdict.product = ''
    if mdict.imgstr.find('-') < 0:
        mdict.no_specific_image = 1

    desclist = list()
    for var in mdict.descriptions:  # dedup
        if var and var not in desclist:
            desclist.append(var)

    mdict.descriptions = desclist

    if 1:  # not mdict.disp_format or not mdict.shown_id:
        mdict.displayed_id = '&nbsp;'
    else:
        mdict.displayed_id = mdict.disp_format % mdict.shown_id
    mdict.picture_id = ''

    return mbmods.add_man_item_table_product_link(pif, mdict)


# ---- main -----------------------------------------------------------


@basics.web_page
def packs_main(pif):

    def fmt_link(sec):
        return pif.ren.format_link(
            '?sec=' + sec['id'],
            mbmods.add_icons(pif, 'p_' + sec['id'], '', '') + '<center>' + sec['name'] + '</center>')

    pif.ren.set_page_extra(pif.ren.image_selector_js)
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append('packs.cgi', 'Multi-Model Packs')
    if pif.form.has('id'):
        pif.ren.hide_title = True
        pif.form.set_val('id', pif.form.get_list('id')[0])  # with no id this blows
        pid = useful.clean_id(pif.form.get_str('id'))
        return do_single_pack(pif, 'packs', pid)
    elif pif.form.has('page'):
        pif.ren.print_html()
        return make_pack_list(
            pif, 'packs',
            verbose=pif.is_allowed('m') and pif.form.get_int('verbose'),
            **pif.form.get_dict(['sec', 'year', 'region', 'lid', 'material']))
    elif pif.form.has('sec'):
        pif.ren.hide_title = True
        sections = pif.dbh.fetch_sections_by_page_type('packs', pif.form.get_str('sec'))
        if not sections:
            pif.ren.print_html()
            return mbmods.make_page_list(pif, 'packs', fmt_link)
        pif.page_id = sections[0]['page_info.id']
        pif.ren.print_html()
        return make_pack_list(
            pif, 'packs',
            verbose=pif.is_allowed('m') and pif.form.get_int('verbose'),
            **pif.form.get_dict(['sec', 'year', 'region', 'lid', 'material']))
    pif.ren.print_html()
    return mbmods.make_page_list(pif, 'packs', fmt_link)


# ---- play ----------------------------------


@basics.web_page
def play_main(pif):
    pif.ren.set_page_extra(pif.ren.image_selector_js)
    pif.page_id = 'playset.ps'
    pif.set_page_info(pif.page_id)
    pif.ren.print_html()
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append('play.cgi', 'Playsets')
    if pif.form.has('id'):
        pif.form.set_val('id', pif.form.get_list('id')[0])  # with no id this blows
        pid = useful.clean_id(pif.form.get_str('id'))
        return do_single_pack(pif, 'playset', pid)
    return make_pack_list(pif, 'playset',
                          verbose=pif.is_allowed('m') and pif.form.get_int('verbose'),
                          **pif.form.get_dict(['sec', 'year', 'region']))
