#!/usr/local/bin/python

import os, re
import basics
import config
import images
import mbdata
import mflags
import models
import useful


def use_previous_product_pic(pif):  # pragma: no cover
    thispic = pif.form_str('pic')
    if not thispic:
        return
    thismods = pif.dbh.fetch_simple_lineup_models(base_id=thispic)
    if not thismods:
        thismods = pif.dbh.fetch_simple_lineup_models(base_id=thispic[:4] + 'W' + thispic[5:])
    thismods = pif.dbh.depref('lineup_model', thismods[0])
    print thispic, thismods, '<br>'
    thatpic = str(int(thispic[:4]) - 1) + thispic[4:]
    thatmods = pif.dbh.FetchSimpleLineupModels(base_id=thatpic)
    if not thatmods:
        thatmods = pif.dbh.FetchSimpleLineupModels(base_id=thatpic[:4] + 'W' + thatpic[5:])
    thatmods = pif.dbh.depref('lineup_model', thatmods[0])
    print thatpic, thatmods, '<br>'
    if thatmods['picture_id']:
        thismods['picture_id'] = thatmods['picture_id']
    else:
        thismods['picture_id'] = thatmods['base_id']
    print thismods['id'], thismods
    pif.dbh.update_lineup_model(where={'id': thismods['id']}, values=thismods)


def show_model_table(pif, mdict, link=True, prefix=['']):
    imgid = [mdict['id']]
    for s in mdict['descs']:
        if s.startswith('same as '):
            imgid.append(s[8:])
    mdict['imgid'] = []
    for pf in prefix:
        mdict['imgid'].extend([pf + x for x in imgid])
    mdict['img'] = pif.render.format_image_required(mdict['imgid'], None, made=mdict['made'], pdir=config.IMG_DIR_MAN)
    ostr = '<center><font face="Courier">%(id)s</font><br>\n' % mdict
    if link and mdict['link']:
        ostr += '   <a href="%(link)s=%(linkid)s">%(img)s</a><br>\n' % mdict
    else:
        ostr += "   %(img)s<br>\n" % mdict
    ostr += '   <b>%(name)s</b>\n' % mdict
    for s in mdict['descs']:
        ostr += "   <br><i>"+s+"</i>\n"
    ostr += "  </center>\n"
    return ostr


def show_boxes(pif, box_styles, mack_nums):
    box_fmt = "<b>%s style box</b>%s\n"
    entries = list()
    for c in box_styles:
        fnames = [id.replace('-', '').lower() + '-' + c.lower() for id in mack_nums]
        box = pif.render.format_image_sized(fnames, pdir=config.IMG_DIR_BOX, required=True)
        entries.append({'text': box_fmt % (c, box)})
    llineup = {'id': 'boxes', 'name': 'Boxes', 'columns': min(2, len(entries)),
        'section': [{'id': 'box', 'name': 'Box Styles',
            'range': [{'entry': entries}],
        }],
    }
    ostr = pif.render.format_lineup(llineup)
    return ostr


def show_model_info(pif, man, mack):
    flago = mflags.FlagList(pif)
    ostr = '<center><table cellspacing=8><tr>'
    if man['scale']:
        ostr += '<th>Scale</th>\n'
    if man['country']:
        ostr += '<th>Country</th>\n'
    if man['first_year']:
        ostr += '<th>Introduced</th>\n'
    if mack:
        ostr += '<th>Mack Number</th>\n'
    ostr += '</tr><tr>\n'
    if man['scale']:
        ostr += '<td valign=top><center>%(scale)s</center></td>\n' % man
    if man['country']:
        ostr += '<td valign=top><center>' + pif.render.format_image_flag(man['country'])
        ostr += '<br>' + flago[man['country']]
        ostr += '</center></td>\n'
    if man['first_year']:
        ostr += '<td valign=top><center>%(first_year)s</center></td>\n' % man
    if mack:
        ostr += '<td valign=top><center>' + '<br>'.join(mack) + '</center></td>\n'
    ostr += '</tr></table></center>\n'
    return ostr


okno = {True: 'ok', False: 'no'}
def show_list_var_pics(pif, mod_id):
    vars = pif.dbh.fetch_variations(mod_id)
    needs_c = found_c = needs_f = found_f = needs_a = found_a = needs_1 = found_1 = needs_2 = found_2 = 0
    nf = []
    for var in vars:
        if var['variation.picture_id'] or not var['variation.text_description']:
            continue
        fn = mod_id + '-' + var['variation.var']
        is_found = int(os.path.exists(config.IMG_DIR_VAR + '/s_' + fn.lower() + '.jpg'))
        if not is_found:
            nf.append(var['variation.var'])
        is_code2 = filter(lambda x: x in mbdata.code2_categories, var['variation.category'].split())

        needs_a += 1
        found_a += is_found
        if var['variation.var'].startswith('f'):
            needs_f += 1
            found_f += is_found
        elif not var['variation.category']:
            needs_c += 1
            found_c += is_found
        elif is_code2:
            needs_2 += 1
            found_2 += is_found
        else:
            needs_1 += 1
            found_1 += is_found
    percent_a = '<span class="%s">%d/%d</span>' % (okno[found_a == needs_a], found_a, needs_a)
    percent_c = '<span class="%s">%d/%d</span>' % (okno[found_c == needs_c], found_c, needs_c)
    percent_1 = '<span class="%s">%d/%d</span>' % (okno[found_1 == needs_1], found_1, needs_1)
    percent_2 = '<span class="%s">%d/%d</span>' % (okno[found_2 == needs_2], found_2, needs_2)
    percent_f = '<span class="%s">%d/%d</span>' % (okno[found_f == needs_f], found_f, needs_f)
    return [percent_a, percent_c, percent_1, percent_2, percent_f]


def show_variations(pif, variations):
    ostr = ''
    if variations:
        ostr += '<center><h3>Variations for This Product</h3>\n'
        pif.render.comment("variations", variations)
        ostr += '<table class="vartable">'
        keys = variations.keys()
        keys.sort(key=lambda x: variations[x][0])
        for key in keys:
            ostr += '<tr><td>'
            ostr += ', '.join(variations[key][0])
            ostr += '</td></tr>'
            ostr += '<tr><td>'
            ostr += variations[key][1]
            ostr += '</td></tr>'
            ostr += '<tr><td class="varentry">'
            ostr += '%s' % key
            ostr += '</td></tr>'
        ostr += '</table></center>\n'
    return ostr


def show_relateds(pif, relateds):
    ostr = ''
    if relateds:
        ostr += '<center><h3>Related Models</h3>\n'
        pif.render.comment("relateds", relateds)
        for related in relateds:
            related['id'] = related['casting_related.related_id']
            related = pif.dbh.modify_man_item(related)
            related['descs'] = related.get('casting_related.description', '').split(';')
            ostr += show_model_table(pif, related, prefix=['s_'])
            ostr += '<br>\n'
        ostr += '</center>\n'
    return ostr


def show_lineup(appear):
    return 'lineup.cgi?year=%(lineup_model.year)s&region=%(lineup_model.region)s#%(lineup_model.number)s' % appear


def show_adds(pif, id, attribute_pictures):
    adds = [
        ["b_", "Sample Baseplate%(s)s", "<p>"],
        ["d_", "Detail%(s)s", " "],
        ["i_", "Interior%(s)s", "<p>"],
        ["p_", "Prototype%(s)s or Preproduction Model%(s)s", "<p>"],
        ["r_", "Real Vehicle Example%(s)s", "<p>"],
        ["a_", "Customization%(s)s", "<p>"],
        ["e_", "Error Model%(s)s", "<p>"],
    ]

    ostr = ''
    for add in adds:
        imgs = pif.render.format_image_list(id.lower(), wc='-*', prefix=add[0], pdir=config.IMG_DIR_ADD)
        if imgs:
            ostr += '<h3>%s</h3>\n' % add[1] % {'s': useful.plural(imgs)}
            for img in imgs:
                ostr += img + '<br>'
                for apic in attribute_pictures:
                    if img.find(apic) >= 0:
                        ostr += attribute_pictures[apic]['attribute_picture.description']
                ostr += '<p>\n'
    return ostr


angle_re = re.compile(r'<.*?>')
def show_link(href, names):
    return '<a href="%s">%s</a>' % (href, ' - '.join(filter(None, [angle_re.sub('', x) for x in names])))


def show_model_links(pif, id, pic, appearances, matrixes, packs, man, show_comparison, external_links, baseplates=[]):
    ostr = '<div style="border-width: 1px; border-style: ridge; padding: 4px;">'
    ostr += '<center><h3>Model-Related Links</h3></center>'

    ostr += '<center><b><a href="vars.cgi?mod=%s">Variations</a></b></center>' % id
    ostr += '<center><b><a href="upload.cgi?m=%s&y=%s">Upload a Picture</a></b></center>' % (id, pic)
    ostr += '<p>'

    if baseplates:  # not currently implemented  # pragma: no cover
        ostr += '<center><h3>Base Plate Name%s</h3>' % useful.plural(baseplates)
        ostr += '<br>'.join(baseplates)
        ostr += '</center><p>'

    lapp = format_lineup_appearances(pif, appearances)
    if lapp:
        ostr += '<center><b>Lineup Appearances</b><p>' + lapp + '</center><p>'

    sapp = format_series_appearances(pif, matrixes, [])
    if sapp:
        ostr += '<center><b>Series Appearances</b></center><p><ul>' + sapp + '</ul><p>'

    sapp = format_series_appearances(pif, [], packs)
    if sapp:
        ostr += '<center><b>Multi-Pack Appearances</b></center><p><ul>' + sapp + '</ul><p>'

    if man['make'] and man['make'] != 'unl':
        ostr += '<center><a href="makes.cgi?make=%s">See more <b>%s</b> vehicles</a></center><p>' % (man['make'], man['vehicle_make.make_name'])

    if show_comparison:
        ostr += '<center><a href="compare.cgi#%s">See <b>casting comparison</b> page</a></center><p>' % id

    if external_links:
        ostr += '<center><b>External Pages</b></center><p><ul>'
        ostr += '\n'.join(format_external_links(pif, external_links))
        ostr += '</ul><p>'
    ostr += '</div>'
    return ostr


def reduce_variations(pif, id, vars):
    vard = {}
    for var in vars:
        if var['v.var']:
            vard.setdefault(var['v.text_description'], [[], []])  #eek
            vard[var['v.text_description']][0].append(pif.render.format_link('vars.cgi?mod=%s&var=%s' % (id, var['v.var']), var['v.var']))
            if var['v.picture_id']:
                vard[var['v.text_description']][1].append(var['v.picture_id'])
            else:
                vard[var['v.text_description']][1].append(var['v.var'])
    for var in vard:
        vard[var][1] = pif.render.format_image_required(id, nobase=True, vars=vard[var][1], prefix='s_', pdir=config.IMG_DIR_MAN)
    return vard


def format_external_links(pif, external_links):
    elst = []
    for e in external_links:
        if e['l1.associated_link']:
            elst.append('<li><a href="%(l1.url)s">%(l1.name)s</a> at <a href="%(l2.url)s">%(l2.name)s</a>' % e)
        else:  # pragma: no cover
            elst.append('<li><a href="%(l1.url)s">%(l1.name)s</a>' % e)
    return elst


def format_series_appearances(pif, matrixes, packs):
    # series appearances
    sstr = ''
    for appear in matrixes:
        if appear['page_info.flags'] & 2:
            sstr += '<li>' + show_link('matrix.cgi?page=%s#%s' % (appear['page_info.id'][7:], appear['matrix_model.section_id']),
                [appear['section.name'], appear['page_info.description']])
        else:
            sstr += '<li>' + show_link('matrix.cgi?page=%s#%s' % (appear['page_info.id'][7:], appear['matrix_model.section_id']),
                [appear['page_info.title'], appear['page_info.description'], appear['section.name']])
    # doesn't do pagename properly
    pif.render.comment('show pack', packs)
    for pack in packs:
        sstr += '<li>' + show_link("packs.cgi?page=%s&id=%s" % (pack['pack.section_id'], pack['base_id.id']),
            [pack['base_id.rawname'], pack['page_info.title'], mbdata.regions.get(pack['pack.region'], 'Worldwide'), pack['base_id.first_year']])
    return sstr


def format_lineup_appearances(pif, appearances):
    # lineup appearances
    yd = {}
    rs = set()
    for appear in appearances:
        yd.setdefault(appear['lineup_model.year'], {})
        yd[appear['lineup_model.year']][appear['lineup_model.region'][0]] = appear
        rs.add(appear['lineup_model.region'][0])
    rl = filter(lambda x: x in rs, mbdata.regionlist)
    astr = ''
    if yd:
        ykeys = yd.keys()
        ykeys.sort()
        astr += pif.render.format_table_start(id='')
        if 'X' in rs:  # not implemented yet  # pragma: no cover
            astr += pif.render.format_row_start()
            astr += pif.render.format_cell(0, '')
            astr += pif.render.format_cell(0, 'Worldwide')
            astr += pif.render.format_row_end()
            for yr in ykeys:
                astr += pif.render.format_row_start()
                astr += pif.render.format_cell(0, yr)
                if 'X' in yd[yr]:
                    appear = yd[yr]['X']
                    astr += pif.render.format_cell(0, '<a href="lineup.cgi?year=%s&region=U#X%s">%s</a>' % (appear['lineup_model.year'], appear['lineup_model.number'], 'X'))
                astr += '\n'
                astr += pif.render.format_row_end()
        else:
            astr += pif.render.format_row_start()
            astr += pif.render.format_cell(0, '')
            for reg in rl:
                astr += pif.render.format_cell(0, mbdata.regions[reg])
            astr += pif.render.format_row_end()
            for yr in ykeys:
                astr += pif.render.format_row_start()
                astr += pif.render.format_cell(0, yr)
                for reg in rl:
                    if reg in yd[yr]:
                        appear = yd[yr][reg]
                        astr += pif.render.format_cell(0, '<a href="%s">%s</a>' % (show_lineup(appear), appear['lineup_model.number']))
                    else:
                        astr += pif.render.format_cell(0)
                    astr += '\n'
                astr += pif.render.format_row_end()
        astr += pif.render.format_table_end()
    return astr


id_re = re.compile('(?P<p>\D*)(?P<n>\d*)(?P<l>\D*)')
def get_mack_numbers(pif, cid, mod_type, aliases):
    mack_nums = []
    if mod_type == cid[0:2] and mod_type in ('RW', 'SF'):
        aliases.append(cid)
    for alias in aliases:
        mack_id = mbdata.get_mack_number(alias)
        if mack_id:
            mack_nums.append(mack_id)
    mack_nums.sort(key=lambda x: x[1])
    return ['-'.join(x).upper() for x in mack_nums]


img_re = re.compile('src="(?P<u>[^"]*)"')
@basics.web_page
def show_single(pif):
    pif.render.print_html()
    if pif.form_has('useprev'):  # pragma: no cover
        use_previous_product_pic(pif)
    man = pif.dbh.fetch_casting(pif.form_str('id'))
    pic = pif.form_str('pic')
    dir = pif.form_str('dir')
    ref = pif.form_str('ref')
    sub = pif.form_str('sub')
    cid = man.get('id', '')
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/single.cgi', 'By ID')
    pif.render.hierarchy_append('/cgi-bin/single.cgi?id=%s' % cid, cid)

    if not man:
        print '<meta http-equiv="refresh" content="0;url=/database.php">'
        return
    id = man['id']
    pif.render.comment('id=', id, 'man=', man)
    relateds = pif.dbh.fetch_casting_related(id)
    raw_variations = variations = []
    if ref:
        sub = mbdata.get_region_tree(sub) + ['']
        raw_variations = pif.dbh.fetch_variation_by_select(id, ref, sub)
        variations = reduce_variations(pif, id, raw_variations)
    variations_box = show_variations(pif, variations)
    related_box = show_relateds(pif, relateds)
    appearances = pif.dbh.fetch_casting_lineups(id)

    appearances.sort(key=lambda x: x['lineup_model.year'])
    aliases = [x['alias.id'] for x in pif.dbh.fetch_aliases(cid, 'mack')]
    mack_nums = get_mack_numbers(pif, cid, man['model_type'], aliases)

    matrixes = filter(lambda x: not x['page_info.flags'] & pif.dbh.FLAG_PAGE_INFO_NOT_RELEASED, pif.dbh.fetch_matrix_appearances(id))
    matrixes.sort(key=lambda x: x['page_info.description'])

    packs = pif.dbh.fetch_pack_model_appearances(id)
    packs.sort(key=lambda x: x['base_id.first_year'])

    attribute_pictures = pif.dbh.fetch_attribute_pictures(id)
    attribute_pictures = dict([
        (x['attribute_picture.attr_type'].lower() + '_' + x['attribute_picture.mod_id'].lower() + '-' + x['attribute_picture.picture_id'] + '.', x) for x in attribute_pictures])

    sections_recs = pif.dbh.fetch_sections(where="page_id like 'year.%'")
    sections = {}
    for section in sections_recs:
        section = pif.dbh.depref('section', section)
        if section['columns'] and not section['display_order']:
            sections.setdefault(section['page_id'][5:], [])
            sections[section['page_id'][5:]].append(section)

    external_links = filter(lambda x: not (x['l1.flags'] & pif.dbh.FLAG_LINK_LINE_HIDDEN), pif.dbh.fetch_links_single('single.' + id))
    show_comparison_link = pif.dbh.fetch_casting_compare(id)

    baseplates = []
    product_box = boxstyles = ''
    boxstyles = man.get('box_styles', '')
    boxid = man['id']

    pif.render.title = '%(casting_type)s %(id)s: %(name)s' % man
    model_image_pfx = ['m_', 'c_', 's_']
    #mainimg = pif.render.format_image_optional(pic, pdir=dir, nopad=True)
    mainimg = pif.render.format_image_sized(pic, pdir=dir, largest='m')
    if not mainimg:
        model_image_pfx = ['l_'] + model_image_pfx
    elif pif.is_allowed('a'):  # pragma: no cover
        img = img_re.search(mainimg).group('u')
        url = 'imawidget.cgi?d=%s&f=%s' % tuple(img[3:].rsplit('/', 1))
        product_box = '<center>' + pif.render.format_link(url, mainimg) + '</center>'
    else:
        product_box = '<center>' + mainimg + '</center>'

    model_box = show_model_table(pif, man, False, model_image_pfx) + '\n' + show_model_info(pif, man, mack_nums) + '\n'
    links_box = show_model_links(pif, id, pic, appearances, matrixes, packs, man, show_comparison_link, external_links)
    var_pics = show_list_var_pics(pif, id)

    # ------- render ------------------------------------

    # top
    print pif.render.format_head()

    print '<table width="100%"><tr>'

    # left bar

    content = '<center>'
    if pif.is_allowed('a'):  # pragma: no cover
        content += '<b><a href="vars.cgi?recalc=1&mod=%s">Recalculate</a><br>\n' % id
        content += '<a href="%s">Base ID</a><br>\n' % pif.dbh.get_editor_link('base_id', {'id': id})
        content += '<a href="%s">Casting</a><br>\n' % pif.dbh.get_editor_link('casting', {'id': id})
        content += '<a href="%s">AttrPics</a><br>\n' % pif.dbh.get_editor_link('attribute_picture', {'mod_id': id})
        if ref.startswith('year.'):
            content += '<a href="%s">Lineup Model</a><br>\n' % pif.dbh.get_editor_link('lineup_model', {'year': ref[5:], 'mod_id': id})
        elif ref.startswith('matrix.'):
            content += '<a href="%s">Matrix Model</a><br>\n' % pif.dbh.get_editor_link('matrix_model', {'page_id': ref, 'mod_id': id})
        elif ref.startswith('packs.'):
            content += '<a href="%s">Pack Model</a><br>\n' % pif.dbh.get_editor_link('pack_model', {'pack_id': sub, 'mod_id': id})
        content += '<a href="vars.cgi?list=1&mod=%s">Variations</a><br>\n' % id
        content += '<a href="vsearch.cgi?ask=1&id=%s">Search</a><br>\n' % id
        content += '<a href="pics.cgi?m=%s">Pictures</a><br>\n' % id.lower()
        content += '<a href="edlinks.cgi?page=single.%s">Links</a><br>\n' % id
        if os.path.exists(os.path.join(config.LIB_MAN_DIR, id.lower())):
            content += '<a href="traverse.cgi?g=1&d=%s">Library</a><br>\n' % os.path.join(config.LIB_MAN_DIR, id.lower())
            content += '<a href="upload.cgi?d=%s&m=%s">Library Upload</a><br>\n' % (os.path.join(config.LIB_MAN_DIR, id.lower()), id.lower())
        prodstar = 'stargreen.gif'
        if pic:
            prodstar = 'starwhite.gif'
            content += '<a href="upload.cgi?d=./%s&r=%s&c=%s">Product Upload</a><br>\n' % (dir, pic, pic)
            prodpic = pif.render.find_image_file(pic, pdir=dir)
            if prodpic:
                x, y = images.get_size(prodpic)
                if x > 400:
                    prodstar = 'staryellow.gif'
                elif x == 400:
                    prodstar = 'starblack.gif'
                else:
                    prodstar = 'starred.gif'
                content += '<a href="upload.cgi?d=./%s&f=%s&act=1&delete=1">Remove Prod Pic</a><br>\n' % (dir, prodpic[prodpic.rfind('/') + 1:])
            else:
                #content += '<a href="single.cgi?pic=%s&useprev=1">Use Prev</a><br>\n' % str(pic)
                content += '<a href="%s&useprev=1">Use Prev</a><br>\n' % pif.request_uri
        content += '<br>\n'
        for vf in pif.dbh.fetch_variation_files(id):
            content += '<a href="vedit.cgi?d=src/mbxf&f=%(imported_from)s">%(imported_from)s</a><br>\n' % vf
        content += '<br>\n'
        content += '<br>\n'.join(var_pics)
        content += '</b><p>'
        content += pif.render.format_image_art(prodstar) + '<p>'
        var_ids = [x['v.var'] for x in raw_variations]
        var_ids.sort()
        for var in var_ids:
            content += '<a href="vars.cgi?mod=%s&var=%s&edit=1">%s</a><br>\n' % (id, var, var)
    content += '</center>\n'

    print models.add_left_bar(pif, '', man['id'], man['vehicle_type'], 4, content)

    # title banner
    print models.add_banner(pif, '%s %s: %s' % (mbdata.casting_types[man['model_type']], id, man['name']))

    print '<tr><td>'
    print '<center>'
    print '<table cellspacing=8><tr>'
    if product_box:

        # top left box
        print '<td valign=top>'
        print product_box

        # lower left box
        if variations_box:
            print '<p>'
            print variations_box
        if related_box:
            print '<p>'
            print related_box

        print '</td>'

        # top right box
        print '<td valign=top>'
        print model_box

        # lower right box

        print '<p>'
        print links_box
        print '</td>'

    else:

        # top left box (missing)

        # top right box
        if related_box or variations_box:
            print '<td valign=top colspan=2>'
        else:
            print '<td valign=top>'
        print model_box
        print '</td>'

        print '</tr>'

        # lower left box
        print '<tr>'
        if related_box or variations_box:
            print '<td width=300 valign=top>'
            if variations_box:
                print '<p>'
                print variations_box
            if related_box:
                print '<p>'
                print related_box
            print '</td>'

        # lower right box

        print '<td valign=top>'
        print links_box
        print '</td>'

    print '</tr></table>'
    print '</center>'
    print '</td></tr>'

    # bottom
    print '<tr><td>'
    print '<center>'
    if boxstyles:
        print show_boxes(pif, boxstyles, aliases)

    print show_adds(pif, id, attribute_pictures)

    print '<p></center>'
    print '</td></tr>'

    print '<tr><td class="bottombar">'
    print pif.render.format_button_comment(pif, 'id=%s&pic=%s&dir=%s&ref=%s' % (cid, pic, dir, ref))
    print '</td></tr></table>'

    print pif.render.format_tail()


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
