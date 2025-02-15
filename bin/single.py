#!/usr/local/bin/python

import copy
import os
import re

import basics
import config
import imglib
import mbdata
import mflags
import models
import render
import useful

# http://beta.bamca.org/cgi-bin/single.cgi?dir=pic/prod/mworld&pic=2017u079&ref=year.2017&sub=67&id=MB895
# fun fact: MB128 has the most different values for "manufacture" (6).


def use_previous_product_pic(pif, cmd, thismods):  # pragma: no cover
    if not thismods:
        return ''
    thismods = pif.dbh.depref('lineup_model', copy.deepcopy(thismods))
    thispic = thismods['base_id'].lower()
    region = thismods['region']
    if cmd == 1:  # set
        thatpic = str(int(thispic[:4]) - 1) + thispic[4:]
        thatmods = pif.dbh.fetch_simple_lineup_models(base_id=thatpic)
        if not thatmods:
            thatmods = pif.dbh.fetch_simple_lineup_models(base_id=thatpic[:4] + 'W' + thatpic[5:])
        thatmods = pif.dbh.depref('lineup_model', thatmods[0])
        thismods['picture_id'] = (
            thatmods['picture_id'].lower() if thatmods['picture_id'] else thatmods['base_id'].lower())
    elif cmd == 2:  # clear
        thismods['picture_id'] = ''
    pif.dbh.update_lineup_model(where={'id': thismods['id']}, values=thismods)
    return thismods['picture_id'].replace('w', region)


def show_list_var_pics(pif, mod_id):
    founds, needs, cnts, id_set = models.count_list_var_pics(pif, mod_id)
    missing_ids = (
        ', '.join([str(x) for x in sorted(set(range(min(id_set), max(id_set) + 1)) - id_set)])) if id_set else ''
    return models.fmt_var_pics(founds, needs), cnts, missing_ids


def make_compares(pif, mod_id, relateds):
    return [
        pif.ren.format_link('/cgi-bin/compare.cgi#' + x['casting_related.model_id'], 'Comparisons for this model')
        for x in relateds
    ]


def make_relateds(pif, mod_id, relateds):
    # relateds = pif.dbh.fetch_casting_relateds(mod_id, section_id='single')
    for related in relateds:
        related['id'] = related['casting_related.related_id']
        related = pif.dbh.modify_man_item(related)
        related['descs'] = related.get('casting_related.description', '').split(';')
        related['imgid'] = [related['id']]
        for s in related['descs']:
            if s.startswith('same as '):
                related['imgid'].append(s[8:])
        related['img'] = pif.ren.format_image_required(
            related['imgid'], made=related['made'], pdir=config.IMG_DIR_MAN, largest=mbdata.IMG_SIZ_SMALL)
        if related['link']:
            related['img'] = '<a href="%(link)s=%(linkid)s">%(img)s</a>' % related
    return relateds


def show_link(pif, href, names):
    angle_re = re.compile(r'<.*?>')
    return pif.ren.format_link(href, ' - '.join([angle_re.sub('', x) for x in names if x]))


def reduce_variations(pif, mod_id, vars):
    '''Reduce all relevant vars to a list.
    Each entry has 0) list of var ids; 1) a picture; 2) a description.'''
    vard = {}
    for var in vars:
        if var['v.var']:
            vtd = var['v.text_description']
            vard.setdefault(vtd, [list(), list()])  # eek
            # vard[vtd][0].append(pif.ren.format_link('vars.cgi?mod=%s&var=%s' % (
            # mod_id, var['v.var']), var['v.var']))
            vard[vtd][0].append(var['v.var'])
            vard[vtd][1].append(var['v.picture_id'] if var['v.picture_id'] else var['v.var'])
    # useful.write_comment('single.reduce_variations', vars, vard)
    return sorted([[
        sorted(vard[vtd][0]),
        pif.ren.find_alt_image_path(
            pif.ren.find_image_path(
                mod_id, nobase=True, vars=vard[vtd][1], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_MAN),
            largest=mbdata.IMG_SIZ_SMALL, required=True),
        vtd] for vtd in vard])


def show_external_links(pif, external_links):
    return [
        f"{pif.ren.format_link(x.l1.url, x.l1.name)} at {pif.ren.format_link(x.l2.url, x.l2.name)}"
        if x.l1.associated_link else f"{pif.ren.format_link(x.l1.url, x.l1.name)}" for x in external_links
    ]


def show_series_appearances(pif, matrixes, relateds):
    # order by year?
    # group series where necessary

    matrixes.sort(key=lambda x: x['page_info.description'] + x['section.name'])
    dedup_mat = {}
    appears = []

    for appear in matrixes:
        appear['title'] = ([appear['section.name'], appear['page_info.description']]
                           if appear['page_info.flags'] & config.FLAG_PAGE_INFO_HIDE_TITLE
                           else [appear['page_info.title'], appear['page_info.description'], appear['section.name']])
        if appear['section.flags'] & config.FLAG_SECTION_GROUP_SINGLES:
            dedup_mat[(appear['page_info.id'], appear['section.id'])] = appear
        else:
            appears.append(appear)
    appears.extend(dedup_mat.values())

    relateds = [x for x in relateds if x['casting_related.section_id'] == 'pub']
    pubs = [show_link(pif, 'pub.cgi?id=' + appear['base_id.id'],
                      (appear['base_id.rawname'].replace(';', ' '), appear['base_id.first_year']))
            for appear in relateds]
    appears = [show_link(pif, 'matrix.cgi?page=%s#%s' % (appear['page_info.id'][7:], appear['section_id']),
                         appear['title']) for appear in appears]
    return appears + pubs


def show_code2_appearances(pif, mod_id, vscounts):
    return [show_link(pif, 'code2.cgi?mod_id=%s&cat=%s' % (mod_id, x['variation_select.category']),
                      ['%s (%d variation%s)' % (x['category.name'], x['count(*)'], 's' if x['count(*)'] != 1 else '')])
            for x in vscounts if x['count(*)'] and x['category.flags'] & config.FLAG_MODEL_CODE_2]


def show_pack_appearances(pif, packs):
    # doesn't do pagename properly
    pack_d = {x['pack.id']: x for x in packs}
    return [show_link(pif, "packs.cgi?page=%s&id=%s" % (pack['pack.page_id'], pack['pack.id']),
            [pack['base_id.rawname'], pack['section.name'], mbdata.regions.get(pack['pack.region'], 'Worldwide'),
             pack['base_id.first_year']])
            for pack_id, pack in sorted(pack_d.items())]


id_re = re.compile(r'(?P<p>\D*)(?P<n>\d*)(?P<l>\D*)')


def show_left_bar_content(pif, model, ref, pic, pdir, lm_pic_id, raw_variations):
    mod_id = model['id']
    links = []
    if pif.is_allowed('a'):  # pragma: no cover
        links.append(f'<a href="vars.cgi?recalc=1&mod={mod_id}">Recalculate</a>')
        links.append('<a href="%s">Casting</a>' % pif.dbh.get_editor_link('casting', {'id': mod_id}))
        links.append('<a href="%s">AttrPics</a>' % pif.dbh.get_editor_link('attribute_picture', {'mod_id': mod_id}))
        links.append(f'<a href="mass.cgi?tymass=related&mod_id={mod_id}">Relateds</a>')
        links.append(f'<a href="mass.cgi?tymass=alias&mod_id={mod_id}">Aliases</a>')
        links.append(f'<a href="vars.cgi?edt=1&mod={mod_id}">Variations</a>')
        links.append(f'<a href="vars.cgi?adl=1&mod={mod_id}">Attr Edit</a>')
        links.append(f'<a href="vars.cgi?vdt=1&mod={mod_id}">Details</a>')
        links.append(f'<a href="vars.cgi?vds=1&mod={mod_id}">Descriptions</a>')
        links.append(f'<a href="vsearch.cgi?ask=1&id={mod_id}">Search</a>')
        links.append(
            f'<a href="pics.cgi?m={mod_id.lower()}">Pics</a> ' +
            f'<a href="vars.cgi?lrg=1&mod={mod_id}&pic1=1&hc=1&picown=1&ci=1&c1=1&c2=1">Creds</a>')
        links.append(f'<a href="edlinks.cgi?page_id=single.{mod_id}">Links</a>')
    if os.path.exists(useful.relpath('.', config.LIB_MAN_DIR, mod_id.replace('/', '_').lower())):
        if pif.is_allowed('v'):  # pragma: no cover
            links.append('<a href="traverse.cgi?d=%s">Library</a>' % useful.relpath(
                '.', config.LIB_MAN_DIR, mod_id.replace('/', '_').lower()))
        if pif.is_allowed('a'):  # pragma: no cover
            links.append('<a href="upload.cgi?d=%s&m=%s">Library Upload</a>' % (
                useful.relpath('.', config.LIB_MAN_DIR,
                               mod_id.replace('/', '_').lower()), mod_id.replace('/', '_').lower()))
            url = "/cgi-bin/traverse.cgi?mr=1&lty=mss&til=1&credit=DT&p={}&d={}".format(
                imglib.get_tilley_file().get(mod_id.lower(), [''])[0] + '*',
                useful.relpath('.', config.LIB_MAN_DIR, mod_id.replace('/', '_').lower()))
            links.append(
                f'<a href="{url}" target="_blank">Tilley List</a> '
                f'<a href="/cgi-bin/pics.cgi?m={mod_id}&t=1">Im</a>')

    ref_link = ostr = ''
    if pif.is_allowed('a'):  # pragma: no cover
        prodstar = pif.ren.fmt_star('black', hollow=True)
        if ref.startswith('year.'):
            ref_link = pif.dbh.get_editor_link('lineup_model', {'year': ref[5:], 'mod_id': mod_id})
        elif ref.startswith('matrix.'):
            ref_link = pif.dbh.get_editor_link('matrix_model', {'page_id': ref, 'mod_id': mod_id})
        elif ref.startswith('packs.'):
            ref_link = pif.dbh.get_editor_link('pack_model', {'pack_id': pif.form.get_str('sec'), 'mod_id': mod_id})
        if pic:
            links.append('')
            prodstar = pif.ren.fmt_star('white')
            prod = '<a href="upload.cgi?d=%s&n=%s&c=%s&link=%s">%s</a>' % (
                pdir.replace('pic', 'lib'), pic, pic, useful.url_quote(pif.request_uri),
                pif.ren.fmt_mini(icon='upload'))
            prodpic = pif.ren.find_image_path(pic, pdir=pdir, largest="m")
            if lm_pic_id:
                prod = prodstar + '\n' + prod
                prod += f' <a href="{pif.request_uri}&useprev=2">{pif.ren.fmt_mini("red", icon="backward-step")}</a>'
            elif prodpic:
                x, y = imglib.get_size(prodpic)
                prod = pif.ren.fmt_star('yellow' if x > 400 else 'black' if x == 400 else 'red') + '\n' + prod
                prod += ' <a href="imawidget.cgi?act=1&d=./%s&f=%s&trash=1">' % (
                    pdir, prodpic[prodpic.rfind('/') + 1:]) + pif.ren.fmt_x() + '</i></a>'
                if ref_link:
                    prod += pif.ren.format_link(ref_link, pif.ren.fmt_edit())
            else:
                prod = prodstar + '\n' + prod
                if ref_link:
                    prod += pif.ren.format_link(ref_link, ' ' + pif.ren.fmt_edit())
                prod += f' <a href="{pif.request_uri}&useprev=1">{pif.ren.fmt_mini(icon="backward-step")}</a>'
            prod = pic + '<br>' + prod
            links.append(prod)
        links.append('')
        date_re = re.compile(r'^\d\d\d\d-\d\d-\d$')
        vfl = [x['imported_from'] for x in pif.dbh.fetch_variation_files(mod_id)]
        vfl = sorted(set(['mbusa' if date_re.match(x) else x for x in vfl])) or ['importer']
        for vf in vfl:
            links.append(f'<a href="vedit.cgi?d=src/mbxf&m={mod_id}&f={vf}">{vf}</a>')
        var_pics, var_texts, missing_ids = show_list_var_pics(pif, mod_id)
        if missing_ids:
            ostr += f'\n<span class="red">{missing_ids}</span><br>\n'
        ostr += '<br>\n'.join(var_pics) + '<p>\n'
        fmt_bad, _, _ = pif.dbh.check_description_formatting(mod_id)
        ostr += pif.ren.fmt_x('red') if fmt_bad else pif.ren.fmt_check('green')
        ostr += '<br>'
        for i_vt in range(1, len(var_texts)):
            mt = 'title="' + mbdata.model_texts[i_vt - 1] + '"'
            vt = var_texts[i_vt]
            ostr += (
                pif.ren.fmt_star('gray', also=mt, alsoc='smallish', hollow=True)
                if not model['format_' + mbdata.desc_attributes[i_vt - 1]] else
                pif.ren.fmt_star('green', also=mt, alsoc='smallish') if vt == var_texts[0] else
                pif.ren.fmt_star('red', also=mt, alsoc='smallish') if not vt else
                pif.ren.fmt_star('yellow', also=mt, alsoc='smallish'))
        ostr += '<p>\n'
        var_ids = [x['v.var'] for x in raw_variations]
        var_ids.sort()
        for var in var_ids:
            ostr += f'<a href="vars.cgi?mod={mod_id}&var={var}&edt=1">{var}</a>\n'
            if var:
                for sz in mbdata.image_size_types:
                    if os.path.exists(
                            useful.relpath('.', config.IMG_DIR_VAR, sz + '_' + mod_id + '-' + var + '.jpg').lower()):
                        ostr += sz.upper() + ' '
                ostr += f'<a href="vars.cgi?mod={mod_id}&var={var}&edt=1">{pif.ren.fmt_edit()}</a>\n'
                ostr += pif.ren.format_link('upload.cgi?d=%s&m=%s&v=%s&l=1&c=%s+variation+%s' % (
                    useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower()), mod_id, var, mod_id, var),
                    pif.ren.fmt_mini(icon='upload')) + '\n'
                ostr += pif.ren.format_link('traverse.cgi?g=1&d=%s&man=%s&var=%s' % (
                    useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower()), mod_id, var),
                    pif.ren.fmt_mini(icon='bars')) + '\n'
            ostr += '<br>\n'
        for attr in pif.dbh.fetch_attributes(mod_id):
            ostr += attr['attribute.attribute_name'] + '<br>\n'
    ostr = '<br>\n'.join(links) + '<p>\n' + ostr
    return ostr


def make_boxes(pif, mod_id, box_types, mack_nums):
    mod_id = box_types[0]['box_type.mod_id']
    base_box_types = [box['box_type.box_type'][0] for box in box_types]
    # box_fmt = "<b>%s style box</b><br>%s"  # <br>%s entries"
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

    # useful.write_comment(str(appearances))
    # lineup appearances
    yd = {}
    rs = set()
    for appear in appearances:
        reg = appear['region'][0]
        yd.setdefault(appear['year'], dict())
        yd[appear['year']].setdefault(reg, set())
        yd[appear['year']][reg].add(appear['number'])
        rs.add(reg)
    rl = [x for x in mbdata.regionlist if x in rs]
    entries = []

    if not yd:
        return {}

    def show_lineup(yr, rg, num):
        return f'lineup.cgi?year={yr}&region={rg}&lty=all#{num}'

    if 'X' in rs:
        columns = ['', 'W']
        show_as = pif.ren.fmt_check('black')
        for yr in sorted(yd.keys()):
            if yd[yr].get('X'):
                appear = sorted(yd[yr]['X'])[0]
                entry = {'': f'<b>{yr}</b>',
                         'W': f'<a href="lineup.cgi?year={yr}&region=U&lty=all#X{appear}">{show_as}</a>'}
                entries.append(entry)
    else:
        columns = [''] + rl
        for yr in sorted(yd.keys()):
            entry = {'': f'<b>{yr}</b>'}
            for reg in rl:
                entry[reg] = ', '.join([pif.ren.format_link(show_lineup(yr, reg, appear), str(appear))
                                        for appear in sorted(yd[yr][reg])]) if yd[yr].get(reg) else '&nbsp;'
            entries.append(entry)

    llistix = render.Listix(
        id='lappear', name='',
        section=[render.Section(
            id='la', name='', colist=columns, headers=mbdata.regions,
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
    img_re = re.compile(r'src="(?P<u>[^"]*)"')
    model = pif.dbh.fetch_casting(pif.form.get_id('id'), extras=True, verbose=True)
    if not model:
        raise useful.SimpleError("That ID wasn't found.", status=404)
    pif.ren.print_html()
    # useful.write_comment('model', model)
    pic = pif.form.get_str('pic')
    pdir = pif.form.get_dir('dir')
    if pdir.startswith('./'):
        pdir = pdir[2:]
    if not pdir.startswith('pic/') or '/' in pic:
        pdir = pic = ''
    ref = pif.form.get_id('ref')
    sec = pif.form.get_str('sec')
    ran = pif.form.get_str('ran')
    reg = sec if sec else pic[4] if (ref.startswith('year') and len(pic) > 4 and pic[:4].isdigit()) else ''
    if reg.startswith('X'):
        reg = 'X.' + reg[1:]
    reg_list = mbdata.get_region_tree(reg) + ['']
    sec_list = mbdata.get_region_tree(sec) + ['']
    mod_id = model['id']
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append('/cgi-bin/single.cgi', 'By ID')
    pif.ren.hierarchy_append(f'/cgi-bin/single.cgi?id={mod_id}', mod_id)

    useful.write_comment('ARGS', mod_id, 'P', pdir, pic, 'Ref', ref, '/', sec, sec_list, '.', ran, 'Rg', reg, reg_list)

    pif.ren.comment('id=', mod_id, 'man=', model)
    raw_variations = variations = []
    if ref:
        raw_variations = pif.dbh.fetch_variation_by_select(mod_id, ref, sec_id=sec_list, ran_id=ran)
        variations = reduce_variations(pif, mod_id, raw_variations)
        useful.write_comment('RVARS', raw_variations)
        useful.write_comment('VARS', variations)
    base_names = pif.dbh.fetch_variation_base_names(mod_id)
    # years 1971 to 1981 needs to cleave W to U and R
    lineup_appearances = list()
    for appear in pif.dbh.depref('lineup_model', pif.dbh.fetch_casting_lineups(mod_id)):
        if (appear.get('region', '') == 'W' and
                int(appear.get('year', 0)) >= 1971 and int(appear.get('year', 0)) <= 1981):
            nappear = copy.deepcopy(appear)
            nappear['region'] = 'U'
            appear['region'] = 'R'
            lineup_appearances.append(nappear)
        lineup_appearances.append(appear)
    lm_pic_id = ''
    lineup_appearances.sort(key=lambda x: x['year'])
    matrix_appearances = pif.dbh.depref('matrix_model', pif.dbh.fetch_matrix_appearances(mod_id))
    pack_appearances = sorted(pif.dbh.fetch_pack_model_appearances(mod_id), key=lambda x: x['base_id.first_year'])

    prod_title = []
    if ref.startswith('year.'):
        for appear in lineup_appearances:
            if appear.get('page_id', '-') == ref and (appear.get('region', '-') in reg_list or reg_list == ['']):
                prod_title = [appear['year'], mbdata.regions.get(appear['region'], ''),
                              f"#{appear['number']}", appear['name']]
                lm_pic_id = appear['picture_id']
                break
        if pif.form.has('useprev'):  # pragma: no cover
            pic = use_previous_product_pic(pif, pif.form.get_int('useprev'), appear)
    elif ref.startswith('matrix.'):
        for appear in matrix_appearances:
            if appear.get('page_id', '') == ref:
                prod_title = [appear['page_info.title'], appear['section.name'], appear['name']]
                break
    elif ref.startswith('packs.'):
        for appear in pack_appearances:
            if appear.get('pack.page_id', '') == ref and appear.get('pack.id', '') == sec:
                prod_title = [appear['section.name'], appear['base_id.first_year'], appear['base_id.rawname']]
                break

    sections_recs = pif.dbh.fetch_sections(where="page_id like 'year.%'")
    sections = {}
    for section in sections_recs:
        if section['columns'] and not section['display_order']:
            sections.setdefault(section['page_id'][5:], [])
            sections[section['page_id'][5:]].append(section)

    boxstyles = pif.dbh.fetch_box_type_by_mod(model['id'])

    pif.ren.title = '%(casting_type)s %(id)s: %(name)s' % model
    product_img = pif.ren.format_image_sized(pic, pdir=pdir, largest=mbdata.IMG_SIZ_MEDIUM)
    product_img_credit = pif.dbh.fetch_photo_credit(pdir, pic, verbose=True)
    # product_img_credit = product_img_credit['photographer.name'] if product_img_credit else ''
    product_img_credit = pif.ren.format_credit(product_img_credit)
    if product_img and pif.is_allowed('a'):  # pragma: no cover
        img = img_re.search(product_img).group('u')
        url = 'imawidget.cgi?d=%s&f=%s' % tuple(img[3:].rsplit('/', 1))
        product_img = pif.ren.format_link(url, product_img)

    vscounts = pif.dbh.fetch_variation_select_counts(mod_id)

    prodnames = sorted(set([x['name'] for x in matrix_appearances + lineup_appearances
                       if x['name'] != model['name']]))
    for x in matrix_appearances:
        useful.write_comment('M', x['id'], x['name'])
    for x in lineup_appearances:
        useful.write_comment('L', x['id'], x['year'], x['region'], x['number'], x['name'])
    model['imgid'] = [model['id']]
    vehicle_types = [mbdata.model_icons.get(x) for x in model['vehicle_type']]
    descs = []
    for s in model['descs']:
        if s.startswith('same as '):
            model['imgid'].append(s[8:])
        if s in mbdata.arts:
            vehicle_types.append('c_' + mbdata.arts[s])
        elif s:
            descs.append(f"<i>{s}</i>")
    model['descs'] = descs
    model['img'] = pif.ren.format_image_required(
        model['imgid'], made=model['made'], pdir=config.IMG_DIR_MAN,
        largest=mbdata.IMG_SIZ_MEDIUM if product_img else mbdata.IMG_SIZ_LARGE)
    model_img_credit = pif.dbh.fetch_photo_credit('.' + config.IMG_DIR_MAN, model['imgid'][0], verbose=True)
    model['credit'] = pif.ren.format_credit(model_img_credit)
    if model['country']:
        model['country_flag'] = pif.ren.format_image_flag(model['country'])
        model['country_name'] = mflags.FlagList()[model['country']]

#    def make_make_link(make, name):
#        if not make:
#            return ''
#        pic = (pif.ren.fmt_img(make, prefix='u', pdir=config.IMG_DIR_MAKE) if name else
#               pif.ren.format_image_art('mbx.gif'))
#        name = name or 'unlicensed'
#        if pic:
#            name = pic + '<br>' + name
#        return pif.ren.format_link("makes.cgi?make=" + make, name)
#
#    model['make_name'] = make_make_link(model.get('make', ''), model.get('vehicle_make.name', ''))

    def make_make(make):
        return {
            'image': (pif.ren.fmt_img(make['casting_make.make_id'], prefix='u', pdir=config.IMG_DIR_MAKE)
                      if make['casting_make.make_id'] else ''),
            'id': make['casting_make.make_id'],
            'name': 'Unlicensed' if make['casting_make.make_id'] == 'unl' else make.get('vehicle_make.name', ''),
            'company_name': make.get('vehicle_make.company_name', ''),
            'flags': (make.get('vehicle_make.flags') or 0) | (make.get('casting_make.flags') or 0),
            'link': 'makes.cgi?make=' + make['casting_make.make_id'],
        }

    model['makes'] = [make_make(x) for x in pif.dbh.fetch_casting_makes(mod_id)]
    # move these to left pane
    boxes = [make_boxes(pif, mod_id, boxstyles, [x['alias.id']
             for x in pif.dbh.fetch_aliases(mod_id, 'mack')])] if boxstyles else []
    adds = boxes + models.make_adds(pif, mod_id)

    plants = make_plants(pif, mod_id, pif.dbh.fetch_variation_plant_counts(mod_id))
    relateds = pif.dbh.fetch_casting_relateds(mod_id)
    aliases = pif.dbh.fetch_aliases(mod_id, 'mack')
    mack_nums = models.get_mack_numbers(pif, mod_id, model['model_type'], aliases)
    if model:
        model['notes'] = '<br>'.join((model.get('notes', '') or '').split(';'))

    # ------- render ------------------------------------

    pif.ren.set_button_comment(pif, keys={'id': 'id', 'pic': 'pic', 'dir': 'dir', 'ref': 'ref'})
    context = {
        'title': '%s %s: %s' % (mbdata.model_types[model['model_type']], mod_id, model['name']),
        'note': '',
        'type_id': '',
        'icon_id':
            mod_id if os.path.exists(useful.relpath('.', config.IMG_DIR_MAN_ICON, 'i_' + mod_id.lower() + '.gif'))
            else '',
        'vehicle_type': vehicle_types,
        'rowspan': '4',
        'left_bar_content': show_left_bar_content(pif, model, ref, pic, pdir, lm_pic_id, raw_variations),
        'model': model,
        'variations': variations,
        'prod_title': ' - '.join([x for x in prod_title if x]),
        'product_image': product_img,
        'product_img_credit': product_img_credit,
        'mack_nums': mack_nums,
        'product_pic': pic,
        'appearances': show_lineup_appearances(pif, lineup_appearances),
        'matrixes': show_series_appearances(pif, matrix_appearances, relateds),
        'code2s': show_code2_appearances(pif, mod_id, vscounts),
        'packs': show_pack_appearances(pif, pack_appearances),
        'prodnames': prodnames,
        'show_comparison_link': pif.dbh.fetch_casting_related_exists(mod_id, model['model_type'].lower()),
        'external_links': show_external_links(pif, pif.dbh.fetch_links_single('single.' + mod_id)),
        'relateds': make_relateds(pif, mod_id, [x for x in relateds if x['casting_related.section_id'] == 'single']),
        'compares':
            make_compares(pif, mod_id, [x for x in relateds if x['casting_related.section_id'] in ['sf', 'rw', 'tr']]),
        'adds_box': models.show_adds(pif, mod_id),
        'adds': adds,
        'plants': plants,
        'base_names': base_names,
        'info_cols': (int(bool(model.get('makes'))) + int(bool(mack_nums)) +
                      int(bool(model['scale'])) + int(bool(model['country'])) + int(bool(model['first_year']))),
        'man_cat': pif.ren.format_link('/cgi-bin/manno.cgi?section={}#{}'.format(model['section_id'], mod_id),
                                       model['section.name']),
        'revised': model['flags'] & config.FLAG_MODEL_CASTING_REVISED,
        # 'group': pif.ren.find_image_path(mod_id, prefix='g', pdir=config.IMG_DIR_ADD)
    }
    return pif.ren.format_template('single.html', **context)
