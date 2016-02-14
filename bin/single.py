#!/usr/local/bin/python

import copy, os, re
import basics
import config
import imglib
import mbdata
import mflags
import models
import useful


def use_previous_product_pic(pif, cmd, thismods):  # pragma: no cover
    if not thismods:
	return ''
    #thismods = pif.dbh.fetch_simple_lineup_models(base_id=thispic)
#    if not thismods:
#	thismods = pif.dbh.fetch_simple_lineup_models(base_id=thispic[:4] + 'W' + thispic[5:])
    thismods = pif.dbh.depref('lineup_model', copy.deepcopy(thismods))
    thispic = thismods['base_id'].lower()
    #print thispic, thismods, '<br>'
#    region = thispic[4] # hack
    region = thismods['region']
    if cmd == 1:  # set
	thatpic = str(int(thispic[:4]) - 1) + thispic[4:]
	thatmods = pif.dbh.fetch_simple_lineup_models(base_id=thatpic)
	if not thatmods:
	    thatmods = pif.dbh.fetch_simple_lineup_models(base_id=thatpic[:4] + 'W' + thatpic[5:])
	thatmods = pif.dbh.depref('lineup_model', thatmods[0])
	#print thatpic, thatmods, '<br>'
	if thatmods['picture_id']:
	    thismods['picture_id'] = thatmods['picture_id']
	else:
	    thismods['picture_id'] = thatmods['base_id'].lower()
    elif cmd == 2:  # clear
	thismods['picture_id'] = ''
    #print thismods['id'], thismods
    pif.dbh.update_lineup_model(where={'id': thismods['id']}, values=thismods)
    return thismods['picture_id'].replace('w', region)


def show_model_table(pif, mdict, link=True, largest=mbdata.IMG_SIZ_SMALL):
    mdict['imgid'] = [mdict['id']]
    for s in mdict['descs']:
        if s.startswith('same as '):
            mdict['imgid'].append(s[8:])
#    mdict['imgid'] = []
#    for pf in prefix:
#        mdict['imgid'].extend([pf + x for x in imgid])
    mdict['img'] = pif.render.format_image_required(mdict['imgid'], made=mdict['made'], pdir=config.IMG_DIR_MAN, largest=largest)
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


def show_model_notes(pif, mdict):
    if not mdict.get('notes'):
	return '<!-- no notes -->'
    return '<center>' + pif.render.format_table_single_cell(0, content=mdict['notes'], talso={'class': 'notes'}) + '</center>'


def show_boxes(pif, mod_id, box_types, mack_nums):
    mod_id = box_types[0]['box_type.mod_id']
    base_box_types = [box['box_type.box_type'][0] for box in box_types]
    box_fmt = "<b>%s style box</b><br>%s<br>%s entries"
    # rewrite this.  glob for alternate boxes.  well, maybe.
    entries = [
	{'text':
	    pif.render.format_link('boxart.cgi',
		txt=box_fmt % (box_type,
		    pif.render.format_image_sized([mod_id + '-' + box_type], pdir=config.IMG_DIR_BOX, required=True),
		    base_box_types.count(box_type)),
		args={'mod': mod_id, 'ty': box_type})
	} for box_type in sorted(list(set(base_box_types)))]
    llineup = {'id': 'boxes', 'name': 'Boxes', 'columns': min(2, len(entries)),
	'section': [{'id': 'box', 'name': 'Box Styles',
	    'range': [{'entry': entries}],
	}],
    }
    ostr = pif.render.format_matrix(llineup)
    return ostr


def show_model_info(pif, man, mack):
    flago = mflags.FlagList()
    ostr = '<center><table cellspacing="8"><tr>'
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
        ostr += '<td valign="top"><center>%(scale)s</center></td>\n' % man
    if man['country']:
        ostr += '<td valign="top"><center>' + pif.render.format_image_flag(man['country'])
        ostr += '<br>' + flago[man['country']]
        ostr += '</center></td>\n'
    if man['first_year']:
        ostr += '<td valign="top"><center>%(first_year)s</center></td>\n' % man
    if mack:
        ostr += '<td valign="top"><center>' + '<br>'.join(mack) + '</center></td>\n'
    ostr += '</tr></table></center>\n'
    return ostr


other_plants = ['Brazil', 'Bulgaria', 'Hungary', 'Japan']
def count_list_var_pics(pif, mod_id):
    vars = pif.dbh.fetch_variations(mod_id)
    needs_c = needs_f = needs_a = needs_1 = needs_2 = needs_p = 0
    found_c = found_f = found_a = found_1 = found_2 = found_p = 0
    count_de = count_ba = count_bo = count_in = count_wh = count_wi = 0
#    nf = []
    for var in vars:
	count_de += int(bool(var['variation.text_description']))
	count_ba += int(bool(var['variation.text_base']))
	count_bo += int(bool(var['variation.text_body']))
	count_in += int(bool(var['variation.text_interior']))
	count_wh += int(bool(var['variation.text_wheels']))
	count_wi += int(bool(var['variation.text_windows']))
        if var['variation.picture_id'] or not var['variation.text_description']:
            continue
	is_found = int(bool(os.path.join(*pif.render.find_image_file(pdir=config.IMG_DIR_MAN, nobase=True,
	    prefix=mbdata.IMG_SIZ_SMALL, suffix='jpg', fnames=mod_id, vars=var['variation.var']))))
#        if not is_found:
#            nf.append(var['variation.var'])
        is_code2 = set(mbdata.code2_categories) & set(var['variation.category'].split())

        needs_a += 1
        found_a += is_found
	if any([var['variation.manufacture'].startswith(x) for x in other_plants]):
            needs_p += 1
            found_p += is_found
        elif var['variation.var'].startswith('f'):
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
    return (found_a, found_c, found_1, found_2, found_f, found_p), \
	   (needs_a, needs_c, needs_1, needs_2, needs_f, needs_p), \
	   (len(vars), count_de, count_ba, count_bo, count_in, count_wh, count_wi)


def show_list_var_pics(pif, mod_id):
    founds, needs, cnts = count_list_var_pics(pif, mod_id)
    return fmt_var_pics(founds, needs), cnts


okno = {True: 'ok', False: 'no'}
def fmt_var_pic(f, n):
    return ('<span class="%s">%d/%d</span>' % ('ok' if f == n else 'no', f, n)) if n else '-'


def fmt_var_pics(found, needs):
    if isinstance(found, list) or isinstance(found, tuple):
	return [fmt_var_pic(*x) for x in zip(found, needs)]
    return fmt_var_pic(found, needs)


def show_variations(pif, variations, prod_title):
    ostr = ''
    if prod_title:
	ostr += '<center>' + prod_title + '</center>'
    if variations:
        ostr += '<center><h3>Variations for This Product</h3>\n'
#'<br>' + prod_title +
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
            ostr += show_model_table(pif, related, largest=mbdata.IMG_SIZ_SMALL)
            ostr += '<br>\n'
        ostr += '</center>\n'
    return ostr


def show_lineup(appear):
    return 'lineup.cgi?year=%(lineup_model.year)s&region=%(lineup_model.region)s&lty=all#%(lineup_model.number)s' % appear


angle_re = re.compile(r'<.*?>')
def show_link(href, names):
    return '<a href="%s">%s</a>' % (href, ' - '.join(filter(None, [angle_re.sub('', x) for x in names])))


def show_model_links(pif, mod_id, pic, appearances, matrixes, packs, man, show_comparison, external_links, baseplates=[]):
    ostr = '<div class="inset">'
    ostr += '<center><h3>Model-Related Links</h3></center>'

    ostr += '<center><b><a href="vars.cgi?mod=%s">Variations</a></b></center>' % mod_id
    ostr += '<center><b><a href="upload.cgi?m=%s&y=%s">Upload a Picture</a></b></center>' % (mod_id, pic)
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
        ostr += '<center><a href="compare.cgi#%s">See <b>casting comparison</b> page</a></center><p>' % mod_id

    if external_links:
        ostr += '<center><b>External Pages</b></center><p><ul>'
        ostr += '\n'.join(format_external_links(pif, external_links))
        ostr += '</ul><p>'
    ostr += '</div>'
    return ostr


def reduce_variations(pif, mod_id, vars):
    vard = {}
    for var in vars:
        if var['v.var']:
            vard.setdefault(var['v.text_description'], [[], []])  #eek
            vard[var['v.text_description']][0].append(pif.render.format_link('vars.cgi?mod=%s&var=%s' % (mod_id, var['v.var']), var['v.var']))
            if var['v.picture_id']:
                vard[var['v.text_description']][1].append(var['v.picture_id'])
            else:
                vard[var['v.text_description']][1].append(var['v.var'])
    for var in vard:
        vard[var][1] = pif.render.format_image_required(mod_id, nobase=True, vars=vard[var][1], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_MAN)
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
    # need to cover case of multiple appearances by one casting (2013 #36, 72)
    for appear in appearances:
        yd.setdefault(appear['lineup_model.year'], dict())
        yd[appear['lineup_model.year']].setdefault(appear['lineup_model.region'][0], list())
        yd[appear['lineup_model.year']][appear['lineup_model.region'][0]].append(appear)
        rs.add(appear['lineup_model.region'][0])
    rl = filter(lambda x: x in rs, mbdata.regionlist)
    astr = ''
    if yd:
        ykeys = yd.keys()
        ykeys.sort()
        astr += pif.render.format_table_start(id='')
        if 'X' in rs:  # not implemented yet  # pragma: no cover
	    if 0:
		astr += pif.render.format_row_start()
		astr += pif.render.format_cell(0, '')
		astr += pif.render.format_cell(0, 'Worldwide')
		astr += pif.render.format_row_end()
		for yr in ykeys:
		    astr += pif.render.format_row_start()
		    astr += pif.render.format_cell(0, yr)
		    if 'X' in yd[yr]:
			appear = yd[yr]['X']
			astr += pif.render.format_cell(0, '<a href="lineup.cgi?year=%s&region=U&lty=all#X%s">%s</a>' % (appear['lineup_model.year'], appear['lineup_model.number'], 'X'))
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
		    aplink = ', '.join([pif.render.format_link(show_lineup(appear), str(appear['lineup_model.number']))
					    for appear in yd[yr].get(reg, [])])
		    astr += pif.render.format_cell(0, aplink) + '\n'
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
    return ['-'.join([str(y) for y in x]).upper() for x in mack_nums]


img_re = re.compile('src="(?P<u>[^"]*)"')
@basics.web_page
def show_single(pif):
    pif.render.print_html()
    pic = pif.form.get_str('pic')
    man = pif.dbh.fetch_casting(pif.form.get_str('id'), extras=True)
    pdir = pif.form.get_str('dir')
    ref = pif.form.get_str('ref')
    sub = pif.form.get_str('sub')
    reg = sub if sub else pic[4] if pic and pic[:4].isdigit() else ''
    cid = man.get('id', '')
    prod_title = ''
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/single.cgi', 'By ID')
    pif.render.hierarchy_append('/cgi-bin/single.cgi?id=%s' % cid, cid)

    if not man:
	raise useful.SimpleError("That ID wasn't found.")
    mod_id = man['id']
    pif.render.comment('id=', mod_id, 'man=', man)
    relateds = pif.dbh.fetch_casting_related(mod_id, section_id='single')
    raw_variations = variations = []
    if ref:
        sub = mbdata.get_region_tree(reg) + ['']
        raw_variations = pif.dbh.fetch_variation_by_select(mod_id, ref, sub)
        variations = reduce_variations(pif, mod_id, raw_variations)
    related_box = show_relateds(pif, relateds)
    # years 1971 to 1981 needs to cleave W to U and R
    appearances = list()
    for appear in pif.dbh.fetch_casting_lineups(mod_id):
	if (appear.get('lineup_model.region', '') == 'W' and
		int(appear.get('lineup_model.year', 0)) >= 1971 and int(appear.get('lineup_model.year', 0)) <= 1981):
	    nappear = copy.deepcopy(appear)
	    nappear['lineup_model.region'] = 'U'
	    appear['lineup_model.region'] = 'R'
	    appearances.append(nappear)
	appearances.append(appear)
    lm_pic_id = ''
    if ref.startswith('year.'):
	for appear in appearances:
	    if appear.get('lineup_model.page_id', '-') == ref and (appear.get('lineup_model.region', '-') in sub or sub == ['']):
		prod_title = appear['lineup_model.name']
		lm_pic_id = appear['lineup_model.picture_id']
		break
	if pif.form.has('useprev'):  # pragma: no cover
	    pic = use_previous_product_pic(pif, pif.form.get_int('useprev'), appear)
#	print appear, '<br>'
#	print pif.form, '<br>'
#	print 'pic', pic, 'pdir', pdir, 'ref', ref, 'sub', sub, 'reg', reg, 'cid', cid, '<br>'

    variations_box = show_variations(pif, variations, prod_title)

    appearances.sort(key=lambda x: x['lineup_model.year'])
    aliases = [x['alias.id'] for x in pif.dbh.fetch_aliases(cid, 'mack')]
    mack_nums = get_mack_numbers(pif, cid, man['model_type'], aliases)

    matrixes = filter(lambda x: not x['page_info.flags'] & pif.dbh.FLAG_PAGE_INFO_NOT_RELEASED, pif.dbh.fetch_matrix_appearances(mod_id))
    matrixes.sort(key=lambda x: x['page_info.description'])

    packs = pif.dbh.fetch_pack_model_appearances(mod_id)
    packs.sort(key=lambda x: x['base_id.first_year'])

    sections_recs = pif.dbh.fetch_sections(where="page_id like 'year.%'")
    sections = {}
    for section in sections_recs:
        section = pif.dbh.depref('section', section)
        if section['columns'] and not section['display_order']:
            sections.setdefault(section['page_id'][5:], [])
            sections[section['page_id'][5:]].append(section)

    external_links = filter(lambda x: not (x['l1.flags'] & pif.dbh.FLAG_LINK_LINE_HIDDEN), pif.dbh.fetch_links_single('single.' + mod_id))
    show_comparison_link = pif.dbh.fetch_casting_related_exists(mod_id, man['model_type'].lower())

    baseplates = []
    product_box = ''
    boxstyles = pif.dbh.fetch_box_type_by_mod(man['id'])

    pif.render.title = '%(casting_type)s %(id)s: %(name)s' % man
    largest = mbdata.IMG_SIZ_MEDIUM
    #mainimg = pif.render.format_image_optional(pic, pdir=pdir, nopad=True)
    mainimg = pif.render.format_image_sized(pic, pdir=pdir, largest=mbdata.IMG_SIZ_MEDIUM)
    if not mainimg:
        largest = mbdata.IMG_SIZ_LARGE
    elif pif.is_allowed('a'):  # pragma: no cover
        img = img_re.search(mainimg).group('u')
        url = 'imawidget.cgi?d=%s&f=%s' % tuple(img[3:].rsplit('/', 1))
        product_box = '<center>' + pif.render.format_link(url, mainimg) + '</center>'
    else:
        product_box = '<center>' + mainimg + '</center>'

    model_box = show_model_table(pif, man, False, largest=largest) + '\n' + show_model_info(pif, man, mack_nums) + '\n'
    notes_box = show_model_notes(pif, man)
    links_box = show_model_links(pif, mod_id, pic, appearances, matrixes, packs, man, show_comparison_link, external_links)
    var_pics, var_texts = show_list_var_pics(pif, mod_id)

    # ------- render ------------------------------------

    # top
    print pif.render.format_head()

    print '<table width="100%"><tr>'

    # left bar

    content = ''
    if pif.is_allowed('a'):  # pragma: no cover
        content += '<a href="vars.cgi?recalc=1&mod=%s">Recalculate</a><br>\n' % mod_id
        content += '<a href="%s">Base ID</a><br>\n' % pif.dbh.get_editor_link('base_id', {'id': mod_id})
        content += '<a href="%s">Casting</a><br>\n' % pif.dbh.get_editor_link('casting', {'id': mod_id})
        content += '<a href="%s">AttrPics</a><br>\n' % pif.dbh.get_editor_link('attribute_picture', {'mod_id': mod_id})
        content += '<a href="mass.cgi?type=related&mod_id=%s">Relateds</a><br>\n' % mod_id
        if ref.startswith('year.'):
            content += '<a href="%s">Lineup Model</a><br>\n' % pif.dbh.get_editor_link('lineup_model', {'year': ref[5:], 'mod_id': mod_id})
        elif ref.startswith('matrix.'):
            content += '<a href="%s">Matrix Model</a><br>\n' % pif.dbh.get_editor_link('matrix_model', {'page_id': ref, 'mod_id': id})
        elif ref.startswith('packs.'):
            content += '<a href="%s">Pack Model</a><br>\n' % pif.dbh.get_editor_link('pack_model', {'pack_id': sub, 'mod_id': mod_id})
        content += '<a href="vars.cgi?list=1&mod=%s">Variations</a><br>\n' % mod_id
        content += '<a href="vsearch.cgi?ask=1&id=%s">Search</a><br>\n' % mod_id
        content += '<a href="pics.cgi?m=%s">Pictures</a><br>\n' % mod_id.lower()
        content += '<a href="edlinks.cgi?page=single.%s">Links</a><br>\n' % mod_id
    if os.path.exists(os.path.join(config.LIB_MAN_DIR, mod_id.lower())):
	if pif.is_allowed('v'):  # pragma: no cover
	    content += '<a href="traverse.cgi?d=%s">Library</a><br>\n' % os.path.join(config.LIB_MAN_DIR, mod_id.lower())
	if pif.is_allowed('a'):  # pragma: no cover
	    content += '<a href="upload.cgi?d=%s&m=%s">Library Upload</a><br>\n' % (os.path.join(config.LIB_MAN_DIR, mod_id.lower()), mod_id.lower())
    if pif.is_allowed('a'):  # pragma: no cover
        prodstar = 'stargreen.gif'
        if pic:
            prodstar = 'starwhite.gif'
            content += '<a href="upload.cgi?d=./%s&n=%s&c=%s">Product Upload</a><br>\n' % (pdir, pic, pic)
            prodpic = pif.render.find_image_path(pic, pdir=pdir)
            if lm_pic_id:
                content += '<a href="%s&useprev=2">Clr Prev</a><br>\n' % pif.request_uri
            elif prodpic:
                x, y = imglib.get_size(prodpic)
                if x > 400:
                    prodstar = 'staryellow.gif'
                elif x == 400:
                    prodstar = 'starblack.gif'
                else:
                    prodstar = 'starred.gif'
                content += '<a href="imawidget.cgi?act=1&d=./%s&f=%s&delete=1">Remove Prod Pic</a><br>\n' % (pdir, prodpic[prodpic.rfind('/') + 1:])
            else:
                #content += '<a href="single.cgi?pic=%s&useprev=1">Use Prev</a><br>\n' % str(pic)
                content += '<a href="%s&useprev=1">Use Prev</a><br>\n' % pif.request_uri
        content += '<br>\n'
        for vf in pif.dbh.fetch_variation_files(mod_id):
            content += '<a href="vedit.cgi?d=src/mbxf&m=%(mod_id)s&f=%(imported_from)s">%(imported_from)s</a><br>\n' % vf
        content += '<br>\n'
        content += '<br>\n'.join(var_pics) + '<p>'
	for vt in var_texts[1:]:
	    content += pif.render.format_image_art(
                    'stargreen.gif' if vt == var_texts[0] else ('starred.gif' if not vt else 'staryellow.gif'))
        content += '<p>'
        content += pif.render.format_image_art(prodstar) + '<p>'
        var_ids = [x['v.var'] for x in raw_variations]
        var_ids.sort()
        for var in var_ids:
            content += '<a href="vars.cgi?mod=%s&var=%s&edit=1">%s</a><br>\n' % (mod_id, var, var)
    #content += '</center>\n'

    print models.add_left_bar(pif, '', man['id'], man['vehicle_type'], 4, content)

    # title banner
    print models.add_banner(pif, '%s %s: %s' % (mbdata.casting_types[man['model_type']], mod_id, man['name']))

    print '<tr><td>'
    print '<center>'
    print '<table cellspacing="8"><tr>'

    if (variations_box or related_box) and product_box:

	# top left box
	print '<td valign="top">'
	print '<table class="inset inset_m"><tr><td>'
	print product_box
	if variations_box:
	    print '<p>'
	    print variations_box
	print '</td></tr></table>'

	# lower left box
	if related_box:
	    print '<p>'
	    print related_box

	print '</td>'

	# top right box
	print '<td valign="top">'
	print model_box
	print notes_box

	# lower right box

	print '<p>'
	print links_box
	print '</td>'

    elif variations_box or related_box:

	# top left box (missing)

	# top right box
	if related_box or variations_box:
	    print '<td valign="top" colspan="2">'
	else:
	    print '<td valign="top">'
	print model_box
	print notes_box
	print '</td>'

	print '</tr>'

	# lower left box
	print '<tr>'
	if related_box or variations_box:
	    print '<td width="400" valign="top">'
	    if variations_box:
		print '<table class="inset inset_m"><tr><td>'
		print variations_box
		print '</td></tr></table>'
	    if related_box:
		print '<p>'
		print related_box
	    print '</td>'

	# lower right box

	print '<td valign="top">'
	print links_box
	print '</td>'

    elif product_box:

	# top left box
	print '<td valign="top">'
	print '<table class="inset inset_m"><tr><td>'
	print product_box
	print '</td></tr></table>'
	print '</td>'

	# top right box
	print '<td valign="top">'
	print model_box
	print notes_box
	print '</td></tr>'

	# lower right box

	print '<tr><td colspan="2">'
	print links_box
	print '</td>'

    else:

	# top left box (missing)

	# top right box
	print '<td valign="top">'
	print model_box
	print notes_box
	print '</td>'

	print '</tr>'

	# lower left box
	print '<tr>'

	# lower right box

	print '<td valign="top">'
	print links_box
	print '</td>'

    print '</tr></table>'
    print '</center>'
    print '</td></tr>'

    # bottom
    print '<tr><td>'
    print '<center>'
    if boxstyles:
        print show_boxes(pif, mod_id, boxstyles, aliases)

    print models.show_adds(pif, mod_id)

    print '<p></center>'
    print '</td></tr>'

    print '<tr><td class="bottombar">'
    print pif.render.format_button_comment(pif, 'id=%s&pic=%s&dir=%s&ref=%s' % (cid, pic, pdir, ref))
    print '</td></tr></table>'

    print pif.render.format_tail()


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
