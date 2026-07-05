#!/usr/local/bin/python

import os
import re

import basics
import config
import imglib
import mbdata
import mbmods
import mflags
import render
import useful

# http://beta.bamca.org/cgi-bin/single.cgi?dir=pic/prod/mworld&pic=2017u079&ref=year.2017&sub=67&id=MB895
# fun fact: MB128 has the most different values for "manufacture" (6).

# A single page does the following queries.
# GetCookie
# User
# Page
# Casting
# VarBySelect
# VarBaseNames
# CastingLineups
# MatrixAppearances
# PackModelAppearances
# Sections
# BoxTypeByMod
# BoxTypeByModAl
# PhotoCredit - twice
# VariationSelectCounts
# PhotoCredit - twice
# CastingMakes
# Aliases
# PhotoCredits
# AttributePictures
# VarPlantCounts
# CastingRelated
# VariationFiles
# VarVS
# Variations
# Details1
# Details3
# Attributes
# CastingRelatedExists
# LinksSingle


def make_compares(pif, mod_id, relateds):
    return [
        pif.ren.format_link(f"/cgi-bin/compare.cgi#{x['casting_related.model_id']}", 'Comparisons for this model')
        for x in relateds if x['casting_related.section_id'] in ['sf', 'rw', 'tr']
    ]


def make_relateds(pif, mod_id, relateds):

    def prep_related(related):
        mod_id = related['casting_related.related_id']
        name = related['base_id.rawname'].replace(';', ' ')
        descs = [x for x in related.get('casting_related.description', '').split(';') if x]
        img = pif.ren.format_image_required(
            [mod_id] + [x[8:] for x in descs if x.startswith('same as ')],
            made=not (related['base_id.flags'] & config.FLAG_MODEL_NOT_MADE),
            pdir=config.IMG_DIR_MAN, largest=mbdata.IMG_SIZ_SMALL)
        img = f'<a href="single.cgi?id={mod_id}">{img}</a>'
        return {'id': mod_id, 'img': img, 'name': name, 'descs': descs}

    return [prep_related(x) for x in relateds if x['casting_related.section_id'] == 'single']


def show_single_link(pif, href, names):
    title = names if isinstance(names, str) else ' - '.join([x for x in names if x])
    return pif.ren.format_link(href, mbdata.angle_re.sub('', title))


def reduce_variations(pif, mod_id, vars):
    '''Reduce all relevant vars to a list.
    Each entry has 0) list of var ids; 1) a picture; 2) a description.'''
    vard = {}
    for var in vars:
        if var['v.var']:
            vtd = var['v.text_description']
            vard.setdefault(vtd, [list(), list()])  # eek
            vard[vtd][0].append(var['v.var'])
            vard[vtd][1].append(var['v.picture_id'] if var['v.picture_id'] else var['v.var'])
    return sorted([[
        sorted(vard[vtd][0]),
        pif.ren.find_alt_image_path(
            pif.ren.find_image_path(
                mod_id, nobase=True, vars=vard[vtd][1], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_MAN),
            largest=mbdata.IMG_SIZ_SMALL, required=True),
        vtd] for vtd in vard])


def show_external_links(pif, x_links):

    def ll_link(x, pfx):
        if x[f'{pfx}.flags'] & config.FLAG_LINK_LINE_RAW_HTML:
            return x[f'{pfx}.url'].format(x[f'{pfx}.name'])
        return pif.ren.format_link(x[f'{pfx}.url'], x[f'{pfx}.name'])

    return [f"{ll_link(x, 'l1')} at {ll_link(x, 'l2')}" if x['l1.associated_link'] else ll_link(x, 'l1') for x in x_links]


def show_series_appearances(pif, matrixes, relateds):
    # order by year?
    # group series where necessary

    matrixes.sort(key=lambda x: x.page_info.description + x.section.name)
    dedup_mat = {}
    appears = []

    for appear in matrixes:
        appear.title = ([appear.section.name, appear.page_info.description]
                        if appear.page_info.flags & config.FLAG_PAGE_INFO_HIDE_TITLE
                        else [appear.page_info.title, appear.page_info.description, appear.section.name])
        if appear.section.group_singles:
            dedup_mat[(appear.page_info.id, appear.section.id)] = appear
        else:
            appears.append(appear)
    appears.extend(dedup_mat.values())
    appears = [show_single_link(pif, f"matrix.cgi?page={appear.page_info.id[7:]}#{appear.section_id}",
                                appear.title) for appear in appears]

    relateds = [x for x in relateds if x['casting_related.section_id'] == 'pub']
    pubs = [show_single_link(pif, f"pub.cgi?id={appear['base_id.id']}",
                             [appear['base_id.rawname'].replace(';', ' '), appear['base_id.first_year']])
            for appear in relateds]
    return appears + pubs


def show_code2_appearances(pif, mod_id, vscounts):
    return [show_single_link(pif, f"code2.cgi?mod_id={mod_id}&cat={x['variation_select.category']}",
                             f"{x['category.name']} ({x['count(*)']} variation{useful.plural(x['count(*)'])})")
            for x in vscounts if x['count(*)'] and x['category.flags'] & config.FLAG_MODEL_CODE_2]


def show_pack_appearances(pif, packs):
    # doesn't do pagename properly
    pack_d = {x.id: x for x in packs}
    return [show_single_link(pif, f"packs.cgi?page={pack.page_id}&id={pack.id}",
            [pack.rawname, pack.section.name, mbdata.regions.get(pack.region, 'Worldwide'), pack.first_year])
            for pack_id, pack in sorted(pack_d.items())]


id_re = re.compile(r'(?P<p>\D*)(?P<n>\d*)(?P<l>\D*)')


def show_left_bar_content(pif, model, ref, pic, pdir, raw_variations):
    # This function holds ALL admin capability for this page.
    mod_id = model.id
    lines = []
    if pif.is_allowed('a'):  # pragma: no cover
        lines.extend([
            f'<a href="vars.cgi?recalc=1&mod={mod_id}">Recalculate</a>',
            '<a href="%s">Casting</a>' % pif.dbh.get_editor_link('casting', id=mod_id),
            '<a href="%s">AttrPics</a>' % pif.dbh.get_editor_link('attribute_picture', mod_id=mod_id),
            f'<a href="mass.cgi?tymass=related&mod_id={mod_id}">Relateds</a>',
            f'<a href="mass.cgi?tymass=alias&mod_id={mod_id}">Aliases</a>',
            f'<a href="vars.cgi?edt=1&mod={mod_id}">Variations</a>',
            f'<a href="vars.cgi?adl=1&mod={mod_id}">Attr Edit</a>',
            f'<a href="vars.cgi?vdt=1&mod={mod_id}">Details</a>',
            f'<a href="vars.cgi?vds=1&mod={mod_id}">Descriptions</a>',
            f'<a href="mass.cgi?tymass=var&mbusa=MBUSA&mod={mod_id}">MBUSA</a>',
            f'<a href="vsearch.cgi?ask=1&id={mod_id}">Search</a>',
            f'<a href="pics.cgi?m={mod_id.lower()}">Pics</a> ' +
            f'<a href="vars.cgi?lrg=1&mod={mod_id}&pic1=1&hc=1&picown=1&ci=1&c1=1&c2=1">Creds</a>',
            f'<a href="edlinks.cgi?page_id=single.{mod_id}">Links</a>',
        ])
    if os.path.exists(useful.relpath('.', config.LIB_MAN_DIR, mod_id.replace('/', '_').lower())):
        if pif.is_allowed('v'):  # pragma: no cover
            lines.append('<a href="traverse.cgi?d=%s">Library</a>' % useful.relpath(
                '.', config.LIB_MAN_DIR, mod_id.replace('/', '_').lower()))
            lines[-1] += f' <a href="https://www.google.com/search?q={model.name.replace(" ", "+")}">G</a>'
        if pif.is_allowed('a'):  # pragma: no cover
            lines.append('<a href="upload.cgi?d=%s&m=%s">Library Upload</a>' % (
                useful.relpath('.', config.LIB_MAN_DIR, mod_id.replace('/', '_').lower()),
                mod_id.replace('/', '_').lower()))
            lines.append(
                f'<a href="/cgi-bin/library.cgi?m={mod_id}&til=1" target="_blank">Tilley List</a> '
                f'<a href="/cgi-bin/pics.cgi?m={mod_id}&t=1">Im</a>')

    ref_link = ''
    if pif.is_allowed('a'):  # pragma: no cover
        prodstar = pif.ren.fmt_star('black', hollow=True)
        if ref.startswith('year.'):
            ref_link = pif.dbh.get_editor_link('lineup_model', year=ref[5:], mod_id=mod_id)
        elif ref.startswith('matrix.'):
            ref_link = pif.dbh.get_editor_link('matrix_model', page_id=ref, mod_id=mod_id)
        elif ref.startswith('packs.'):
            ref_link = pif.dbh.get_editor_link('pack_model', pack_id=pif.form.get_str('sec'), mod_id=mod_id)
        if pic:
            lines.append('')
            prodstar = pif.ren.fmt_star('white')
            ldir = pdir.replace('pic', 'lib')
            prod = pif.ren.format_link(f"upload.cgi?d={ldir}&n={pic}&c={pic}", pif.ren.fmt_mini(icon="upload"))
            if prodpic := pif.ren.find_image_path(pic, pdir=pdir, largest="m"):
                x, y = imglib.get_size(prodpic)
                prodpicname = prodpic[prodpic.rfind('/') + 1:]
                prod = (
                    f'{pif.ren.fmt_star("yellow" if x > 400 else "black" if x == 400 else "red")}\n{prod}'
                    f' <a href="imawidget.cgi?act=1&d=./{pdir}&f={prodpicname}&trash=1">{pif.ren.fmt_x()}</i></a>')
            else:
                prod = f'{prodstar}\n{prod}'
            if ref_link:
                prod += pif.ren.format_link(ref_link, ' ' + pif.ren.fmt_edit())
            prod = (
                f'{pic}<br>{prod}'
                f' <a href="imawidget.cgi?d={pdir}&f=m_{pic}.jpg">{pif.ren.fmt_mini(icon="paintbrush")}</a>')
            lines.append(prod)
        lines.append('')

        date_re = re.compile(r'^\d\d\d\d-\d\d-\d$')
        vfl = [x['imported_from'] for x in pif.dbh.fetch_variation_files(mod_id)]
        vfl = sorted(set(['mbusa' if date_re.match(x) else x for x in vfl])) or ['importer']
        for vf in vfl:
            lines.append(f'<a href="vedit.cgi?d=src/mbxf&m={mod_id}&f={vf}">{vf}</a>')
        lines.append('')

        var_pics, var_texts, missing_ids = mbmods.show_list_var_pics(pif, mod_id)
        if missing_ids:
            lines.append(f'\n<span class="red">{missing_ids}</span>')
        lines.extend(var_pics)
        lines.append('')

        attrs = pif.dbh.fetch_attributes(mod_id)
        fmt_bad, messages, missing = pif.dbh.check_description_formatting_casting(model, attrs)
        lines.append(f'<!-- {str(messages)} {str(missing)} -->')
        lines.append(pif.ren.fmt_x('red') if fmt_bad else pif.ren.fmt_check('green'))
        var_cnt, var_counts = var_texts
        lines.append(''.join([
            pif.ren.fmt_star(
                'gray' if not model.get_attr(mbmods.text_fmts[k]) else 'red' if not v else
                'green' if v == var_cnt else 'yellow', also=f'title="{mbmods.text_titles[k]}"', alsoc='smallish')
            for k, v in var_counts.items()]))
        lines.append('')

        for var in sorted([x['v.var'] for x in raw_variations]):
            ln = f'<a href="vars.cgi?mod={mod_id}&var={var}&edt=1">{var}</a> '
            if var:
                ln += ''.join([x.upper() for x in mbdata.image_size_types if os.path.exists(
                    useful.relpath('.', config.IMG_DIR_VAR, f'{x}_{mod_id}-{var}.jpg').lower())]) + ' '
                ln += f'<a href="vars.cgi?mod={mod_id}&var={var}&edt=1">{pif.ren.fmt_edit()}</a>\n'
                ln += pif.ren.format_link(
                    f'upload.cgi?d={useful.relpath(".", config.LIB_MAN_DIR, mod_id.lower())}&'
                    f'm={mod_id}&v={var}&l=1&c={mod_id}+variation+{var}', pif.ren.fmt_mini(icon='upload')) + '\n'
                ln += pif.ren.format_link('traverse.cgi?g=1&d=%s&man=%s&var=%s' % (
                    useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower()), mod_id, var),
                    pif.ren.fmt_mini(icon='bars')) + '\n'
            lines.append(ln)
        lines.append('')
        for attr in attrs:
            lines.append(attr['attribute.attribute_name'])
    return lines


def make_boxes(pif, mod_id, box_types, mack_nums):
    mod_id = box_types[0]['box_type.mod_id']
    base_box_types = [box['box_type.box_type'][0] for box in box_types]
    # rewrite this.  glob for alternate boxes.  well, maybe.
    entries = [{
        'desc':
            pif.ren.format_link(
                'boxart.cgi', txt=f'{box_type} style box',
                args={'mod': mod_id, 'ty': box_type}),
        'img':
            pif.ren.format_link(
                'boxart.cgi',
                txt=pif.ren.format_image_sized([mod_id + '-' + box_type], pdir=config.IMG_DIR_BOX, required=True),
                args={'mod': mod_id, 'ty': box_type}),
    } for box_type in sorted(list(set(base_box_types)))]
    return {'title': f'Box Style{useful.plural(entries)}', 'entry': entries, 'columns': 2}


def show_lineup_appearances(pif, appearances):
    if not appearances:
        return {}

    yd = {}
    rs = set()
    for appear in appearances:
        reg = appear.region
        yd.setdefault(appear.year, dict())
        yd[appear.year].setdefault(reg, set())
        yd[appear.year][reg].add(appear.number)
        rs.add(reg[0])
    rl = [x for x in mbdata.regionlist + ['X'] if x in rs]
    entries = []

    if not yd:
        return {}

    for yr in sorted(yd.keys()):
        entry = {'': f'<b>{yr}</b>'}
        for reg in rl:
            if reg == 'X':
                for yreg in yd[yr]:
                    if yreg.startswith('X'):
                        show_as = pif.ren.fmt_check('black')
                        appear = yreg.replace('.', '') + f'.{sorted(yd[yr][yreg])[0]}'
                        entry[reg] = f'<a href="lineup.cgi?year={yr}&region=U&lty=all#{appear}">{show_as}</a>'
                        break
            else:
                entry[reg] = ', '.join([
                    pif.ren.format_link(f'lineup.cgi?year={yr}&region={reg}&lty=all#{reg}.{appear}', str(appear))
                    for appear in sorted(yd[yr][reg])]) if yd[yr].get(reg) else '&nbsp;'
        entries.append(entry)

    llistix = render.Listix(
        id='lappear', name='', section=[render.Section(
            id='la', name='', colist=[''] + [x for x in mbdata.regionlist + ['X'] if x in rs], headers=mbdata.regions,
            range=[render.Range(entry=entries)],
        )],
    )
    return llistix


def make_plants(pif, mod_id, plants):
    columns = []
    headers = {}
    entry = {}

    for plant in plants:
        if plant['manufacture'] == 'no origin':
            flag = ('none', pif.ren.find_image_path('no', art=True),)
        elif plant['manufacture'] == '':
            flag = ('unset', '')
        else:
            flag = pif.ren.show_flag(mbdata.plant_d[plant['manufacture']])
        url = "/cgi-bin/vars.cgi?manufacture=%s&mod=%s" % (plant['manufacture'].replace(' ', '+')
                                                           if plant['manufacture'] else 'unset', mod_id)
        columns.append(plant['manufacture'])
        headers[plant['manufacture']] = pif.ren.format_link(
            url, useful.img_src(flag[1], also={'title': plant['manufacture']}) if flag[1] else flag[0])
        entry[plant['manufacture']] = pif.ren.format_link(url, str(plant['count']))

    llistix = render.Listix(
        id='lplants', name='',
        section=[render.Section(
            id='la', name='', colist=columns, headers=headers,
            range=[render.Range(entry=[entry])],
        )],
    )
    llistix.shown = len(plants) > 0
    return llistix


@basics.web_page
def show_single(pif):
    model = pif.dbh.fetch_casting(pif.form.get_id('id'), extras=True)
    if not model:
        raise useful.SimpleError("That ID wasn't found.", status=404)
    pif.ren.print_html()
    model = pif.dbh.make_man_item(model)
    mod_id = model.id

    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append('/cgi-bin/single.cgi', 'By ID')
    pif.ren.hierarchy_append(f'/cgi-bin/single.cgi?id={mod_id}', mod_id)
    pif.ren.title = f'{model.casting_type} {model.id}: {model.name}'

    prod = mbmods.get_product_info(pif)
    raw_variations = variations = []
    if prod.ref:
        raw_variations = pif.dbh.fetch_variation_by_select(mod_id, prod.ref, sec_id=prod.sec_list, ran_id=prod.ran)
        variations = reduce_variations(pif, mod_id, raw_variations)
    lineup_appearances = sorted(pif.dbh.make_line_items(pif.dbh.fetch_casting_lineups(mod_id)), key=lambda x: x.year)
    matrix_appearances = pif.dbh.make_mat_items(pif.dbh.fetch_matrix_appearances(mod_id))
    pack_appearances = sorted(pif.dbh.make_pack_items(pif.dbh.fetch_pack_model_appearances(mod_id)),
                              key=lambda x: x.first_year)

    prod_title = []
    for appear in (
            lineup_appearances if prod.ref_type == 'LI' else
            matrix_appearances if prod.ref_type == 'SE' else
            pack_appearances if prod.ref_type == 'MP' else []):
        if prod_title := prod.get_prod_title(appear):
            break
    product_img = pif.ren.format_image_sized(prod.pic, pdir=prod.pdir, largest=mbdata.IMG_SIZ_MEDIUM)
    product_img_credit = pif.ren.format_credit(pif.dbh.fetch_photo_credit(prod.pdir, prod.pic))

    sections_recs = pif.dbh.fetch_sections(where="page_id like 'year.%'")
    sections = {}
    for section in sections_recs:
        if section['columns'] and not section['display_order']:
            sections.setdefault(section['page_id'][5:], [])
            sections[section['page_id'][5:]].append(section)

    prodnames = sorted(set([x.name for x in matrix_appearances + lineup_appearances]))
    model.imgid = [model.id]
    vehicle_types = [mbdata.model_icons.get(x) for x in model.vehicle_type]
    descs = []
    for s in model.descs:
        if s.startswith('same as '):
            model.imgid.append(s[8:])
        if s in mbdata.casting_arts:
            vehicle_types.append(mbdata.casting_arts[s])
        elif s:
            descs.append(f"<i>{s}</i>")
    model.descs = descs
    model.img = pif.ren.format_image_required(
        model.imgid, made=model.made, pdir=config.IMG_DIR_MAN,
        largest=mbdata.IMG_SIZ_MEDIUM if product_img else mbdata.IMG_SIZ_LARGE)
    model_img_credit = pif.dbh.fetch_photo_credit('.' + config.IMG_DIR_MAN, model.imgid[0])
    model.credit = pif.ren.format_credit(model_img_credit)
    if model.country:
        model.country_flag = pif.ren.format_image_flag(model.country)
        model.country_name = mflags.FlagList()[model.country]

    aliases = pif.dbh.fetch_aliases(mod_id, 'mack')
    model.makes = [mbmods.make_make(pif, x) for x in pif.dbh.fetch_casting_makes(mod_id)]
    # move these to left pane
    boxstyles = pif.dbh.fetch_box_type_by_mod(model.id)
    boxes = [make_boxes(pif, mod_id, boxstyles, [x['alias.id'] for x in aliases])] if boxstyles else []
    adds = boxes + mbmods.make_adds(pif, mod_id)
    plants = make_plants(pif, mod_id, pif.dbh.fetch_variation_plant_counts(mod_id))
    relateds = pif.dbh.fetch_casting_relateds(mod_id)
    mack_nums = mbmods.get_mack_numbers(pif, mod_id, model.model_type, aliases)
    model.notes = '<br>'.join(model.notes.split(';'))
    base_names = sorted(set([x['base_name'] for x in pif.dbh.fetch_variation_base_names(mod_id) if x['base_name']]))
    vscounts = pif.dbh.fetch_variation_select_counts(mod_id)

    icon_add = {'suffix': 'gif', 'also': {'class': 'centered'}, 'tail': '<p>', 'nopad': True}
    left_bar_icons = [
        pif.ren.format_image_icon(''),  # type_id
        pif.ren.format_image_optional(mod_id, pdir=config.IMG_DIR_MAN_ICON, prefix='i_', **icon_add)] + [
        pif.ren.format_image_optional(vtype, pdir=config.IMG_DIR_ICON, **icon_add) for vtype in vehicle_types] + [
        pif.ren.format_image_optional(mod_id, pdir=config.IMG_DIR_MAN_ICON, prefix='b_', **icon_add) +
        pif.ren.format_image_optional(mod_id, pdir=config.IMG_DIR_MAN_ICON, prefix='f_', **icon_add)
    ]

    # ------- render ------------------------------------

    pif.ren.set_button_comment(pif, keys={'id': 'id', 'pic': 'pic', 'dir': 'dir', 'ref': 'ref'})
    context = {
        'title': f'{mbdata.model_types[model.model_type]} {mod_id}: {model.name}',
        'note': '',
        'type_id': '',
        'icon_id': mod_id,
        'vehicle_type': vehicle_types,
        'rowspan': '4',
        'left_bar_icons': left_bar_icons,
        'left_bar_content': '<br>\n'.join(
            show_left_bar_content(pif, model, prod.ref, prod.pic, prod.pdir, raw_variations)),
        'right_side_image':
            pif.ren.format_image_optional(mod_id, pdir=config.IMG_DIR_ADD, prefix='v_', also={'class': 'righty'}),
        'model': model,
        'variations': variations,
        'prod_title': ' - '.join([x for x in prod_title if x]),
        'product_image': product_img,
        'product_img_credit': product_img_credit,
        'product_pic': prod.pic,
        'mack_nums': mack_nums,
        'appearances': show_lineup_appearances(pif, lineup_appearances),
        'matrixes': show_series_appearances(pif, matrix_appearances, relateds),
        'code2s': show_code2_appearances(pif, mod_id, vscounts),
        'packs': show_pack_appearances(pif, pack_appearances),
        'prodnames': prodnames,
        'show_comparison_link': pif.dbh.fetch_casting_related_exists(mod_id, model.model_type.lower()),
        'external_links': show_external_links(pif, pif.dbh.fetch_links_single('single.' + mod_id)),
        'relateds': make_relateds(pif, mod_id, [x for x in relateds if x['casting_related.section_id'] == 'single']),
        'compares':
            make_compares(pif, mod_id, [x for x in relateds if x['casting_related.section_id'] in ['sf', 'rw', 'tr']]),
        'adds': adds,
        'plants': plants,
        'base_names': base_names,
        'info_cols': useful.count_exist([model.makes, mack_nums, model.scale, model.country, model.first_year]),
        'man_cat': pif.ren.format_link(f'/cgi-bin/manno.cgi?section={model.section_id}#{mod_id}', model.section.name),
        'revised': model.casting_revised,
        # 'group': pif.ren.find_image_path(mod_id, prefix='g', pdir=config.IMG_DIR_ADD)
    }
    return pif.ren.format_template('single.html', **context)
