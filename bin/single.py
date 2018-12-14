#!/usr/local/bin/python

import copy, os, re, urllib
import basics
import config
import imglib
import mbdata
import mflags
import models
import useful

#http://beta.bamca.org/cgi-bin/single.cgi?dir=pic/prod/mworld&pic=2017u079&ref=year.2017&sub=67&id=MB895

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
	thismods['picture_id'] = thatmods['picture_id'].lower() if thatmods['picture_id'] else thatmods['base_id'].lower()
    elif cmd == 2:  # clear
	thismods['picture_id'] = ''
    pif.dbh.update_lineup_model(where={'id': thismods['id']}, values=thismods)
    return thismods['picture_id'].replace('w', region)


var_types = ['c', '1', '2', 'f', 'p']
def calc_var_pics(pif, var):
    has_de = 1 if len(var['text_description']) > 0 else 0
    has_ba = 1 if len(var['text_base']) > 0 else 0
    has_bo = 1 if len(var['text_body']) > 0 else 0
    has_in = 1 if len(var['text_interior']) > 0 else 0
    has_wh = 1 if len(var['text_wheels']) > 0 else 0
    has_wi = 1 if len(var['text_windows']) > 0 else 0
    has_wt = 1 if len(var['text_with']) > 0 else 0
    is_found = False
    if not var['picture_id']:
	is_found = int(bool(pif.render.find_image_path(pdir=config.IMG_DIR_MAN, nobase=True,
	    prefix=mbdata.IMG_SIZ_SMALL, suffix='jpg', fnames=var['mod_id'], vars=var['var'])))

    return (calc_var_type(pif, var),) + (is_found, has_de, has_ba, has_bo, has_in, has_wh, has_wi, has_wt)

# hardcoding this because i don't want to do a query at this point
code2cats = set(['ASAP', 'C2', 'CCI', 'CQ', 'NC', 'WR', 'YF'])
def calc_var_type(pif, var):
    ty_var = ''
    if not var['picture_id']:
	if any([var['manufacture'].startswith(x) for x in mbdata.other_plants]):
	    ty_var = 'p'
	elif any([x['category.flags'] & pif.dbh.FLAG_MODEL_CODE_2 for x in var['vs']]) or code2cats & set(var['category'].split()):
	    ty_var = '2'
	elif var['var'].startswith('f'):
	    ty_var = 'f'
	elif any([x['variation_select.category'] == 'MB' for x in var['vs']]):
	    ty_var = 'c'
	else:
	    ty_var = '1'
    return ty_var


def count_list_var_pics(pif, mod_id):  # called from elsewhere
    vars = pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id))
    needs_c = needs_f = needs_a = needs_1 = needs_2 = needs_p = 0
    found_c = found_f = found_a = found_1 = found_2 = found_p = 0
    count_de = count_ba = count_bo = count_in = count_wh = count_wi = count_wt = 0
#    nf = []
    for var in vars:
	ty_var, is_found, has_de, has_ba, has_bo, has_in, has_wh, has_wi, has_wt = calc_var_pics(pif, var)
	count_de += has_de
	count_ba += has_ba
	count_bo += has_bo
	count_in += has_in
	count_wh += has_wh
	count_wi += has_wi
	count_wt += has_wt
	if not var['picture_id']:
    #        if not is_found:
    #            nf.append(var['var'])

	    needs_a += 1
	    found_a += is_found
	    if ty_var == 'p':
		needs_p += 1
		found_p += is_found
	    elif ty_var == 'f':
		needs_f += 1
		found_f += is_found
	    elif ty_var == 'c':
		needs_c += 1
		found_c += is_found
	    elif ty_var == '2':
		needs_2 += 1
		found_2 += is_found
	    else:
		needs_1 += 1
		found_1 += is_found
    return (found_a, found_c, found_1, found_2, found_f, found_p), \
	   (needs_a, needs_c, needs_1, needs_2, needs_f, needs_p), \
	   (len(vars), count_de, count_ba, count_bo, count_in, count_wh, count_wi, count_wt)


def show_list_var_pics(pif, mod_id):
    founds, needs, cnts = count_list_var_pics(pif, mod_id)
    return fmt_var_pics(founds, needs), cnts


def fmt_var_pic(f, n):  # called from elsewhere
    return ('<span class="%s">%d/%d</span>' % ('ok' if f == n else 'no', f, n)) if n else '-'


def fmt_var_pics(found, needs):  # called from elsewhere
    if isinstance(found, list) or isinstance(found, tuple):
	return [fmt_var_pic(*x) for x in zip(found, needs)]
    return fmt_var_pic(found, needs)


def make_compares(pif, mod_id, relateds):
    return [
	pif.render.format_link('/cgi-bin/compare.cgi#' + x['casting_related.model_id'], 'Comparisons for this model')
	    for x in relateds
    ]


def make_relateds(pif, mod_id, relateds):
    #relateds = pif.dbh.fetch_casting_relateds(mod_id, section_id='single')
    for related in relateds:
	related['id'] = related['casting_related.related_id']
	related = pif.dbh.modify_man_item(related)
	related['descs'] = related.get('casting_related.description', '').split(';')
	related['imgid'] = [related['id']]
	for s in related['descs']:
	    if s.startswith('same as '):
		related['imgid'].append(s[8:])
	related['img'] = pif.render.format_image_required(related['imgid'], made=related['made'], pdir=config.IMG_DIR_MAN, largest=mbdata.IMG_SIZ_SMALL)
	if related['link']:
	    related['img'] = '<a href="%(link)s=%(linkid)s">%(img)s</a>' % related
    return relateds


angle_re = re.compile(r'<.*?>')
def show_link(href, names):
    return '<a href="%s">%s</a>' % (href, ' - '.join(filter(None, [angle_re.sub('', x) for x in names])))


def reduce_variations(pif, mod_id, vars):
    '''Reduce all relevant vars to a list.
    Each entry has 0) list of var ids; 1) a picture; 2) a description.'''
    vard = {}
    for var in vars:
        if var['v.var']:
	    vtd = var['v.text_description']
            vard.setdefault(vtd, [list(), list()])  #eek
            #vard[vtd][0].append(pif.render.format_link('vars.cgi?mod=%s&var=%s' % (mod_id, var['v.var']), var['v.var']))
	    vard[vtd][0].append(var['v.var'])
	    vard[vtd][1].append(var['v.picture_id'] if var['v.picture_id'] else var['v.var'])
    #useful.write_comment('single.reduce_variations', vars, vard)
    return sorted([[
	sorted(vard[vtd][0]),
	pif.render.find_alt_image_path(
	    pif.render.find_image_path(mod_id, nobase=True, vars=vard[vtd][1], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_MAN),
	    largest=mbdata.IMG_SIZ_SMALL, required=True),
	vtd] for vtd in vard])


def show_external_links(pif, external_links):
    return [
	('<a href="%(l1.url)s">%(l1.name)s</a> at <a href="%(l2.url)s">%(l2.name)s</a>' % e) if e['l1.associated_link']
        else ('<a href="%(l1.url)s">%(l1.name)s</a>' % e) for e in external_links
    ]


def show_series_appearances(pif, matrixes, relateds):
    # order by year?
    # group series where necessary

    matrixes.sort(key=lambda x: x['page_info.description'] + x['section.name'])
    dedup_mat = {}
    appears = []

    for appear in matrixes:
	appear['title'] = [appear['section.name'], appear['page_info.description']] if appear['page_info.flags'] & pif.dbh.FLAG_PAGE_INFO_HIDE_TITLE \
	    else [appear['page_info.title'], appear['page_info.description'], appear['section.name']]
	if appear['section.flags'] & pif.dbh.FLAG_SECTION_GROUP_SINGLES:
	    dedup_mat[(appear['page_info.id'], appear['section.id'])] = appear
	else:
	    appears.append(appear)
    appears.extend(dedup_mat.values())

    relateds = [x for x in relateds if x['casting_related.section_id'] == 'pub']
    pubs = [show_link('pub.cgi?id=%s' % appear['base_id.id'],
	                    (appear['base_id.rawname'].replace(';', ' '), appear['base_id.first_year'])) for appear in relateds]
    appears = [show_link('matrix.cgi?page=%s#%s' % (appear['page_info.id'][7:], appear['matrix_model.section_id']),
	                    appear['title']) for appear in appears]
    return appears + pubs


def show_code2_appearances(pif, mod_id, vscounts):
    return [show_link('code2.cgi?mod_id=%s&cat=%s' % (mod_id, x['variation_select.category']),
			['%s (%d variation%s)' % (x['category.name'], x['count(*)'], 's' if x['count(*)'] != 1 else '')])
		for x in vscounts if x['count(*)'] and x['category.flags'] & pif.dbh.FLAG_MODEL_CODE_2]


def show_pack_appearances(pif, packs):
    # doesn't do pagename properly
    pack_d = {x['pack.id']: x for x in packs}
    return [show_link("packs.cgi?page=%s&id=%s" % (pack['pack.page_id'], pack['pack.id']),
            [pack['base_id.rawname'], pack['section.name'], mbdata.regions.get(pack['pack.region'], 'Worldwide'), pack['base_id.first_year']])
	    for pack_id, pack in sorted(pack_d.items())]


id_re = re.compile('(?P<p>\D*)(?P<n>\d*)(?P<l>\D*)')
def get_mack_numbers(pif, cid, mod_type, aliases):  # called from elsewhere
    aliases = [(x['alias.flags'], x['alias.id']) for x in aliases if x['alias.type'] == 'mack']
    if mod_type == cid[0:2] and mod_type in ('RW', 'SF'):
        aliases.append((pif.dbh.FLAG_ALIAS_PRIMARY, cid,))
    mack_nums = []
    for alias in aliases:
	mack_id = mbdata.get_mack_number(alias[1])
	if mack_id:
	    mack_nums.append(((alias[0] & pif.dbh.FLAG_ALIAS_PRIMARY) != 0,) + mack_id)
    mack_nums.sort(key=lambda x: x[2])
    # if aliases.flags == 2, put it first or bold it or something
    return [('<b>' if x[0] else '') +
	    '-'.join([str(y) for y in x[1:]]).upper() +
	    ('</b>' if x[0] else '')
	for x in mack_nums]


def show_left_bar_content(pif, model, ref, pic, pdir, lm_pic_id, raw_variations):
    mod_id = model['id']
    links = []
    if pif.is_allowed('a'):  # pragma: no cover
        links.append('<a href="vars.cgi?recalc=1&mod=%s">Recalculate</a>' % mod_id)
        links.append('<a href="%s">Casting</a>' % pif.dbh.get_editor_link('casting', {'id': mod_id}))
        links.append('<a href="%s">AttrPics</a>' % pif.dbh.get_editor_link('attribute_picture', {'mod_id': mod_id}))
        links.append('<a href="mass.cgi?type=related&mod_id=%s">Relateds</a>' % mod_id)
        links.append('<a href="mass.cgi?type=alias&mod_id=%s">Aliases</a>' % mod_id)
        links.append('<a href="vars.cgi?edit=1&mod=%s">Variations</a>' % mod_id)
        links.append('<a href="vars.cgi?vdet=1&mod=%s">Details</a>' % mod_id)
        links.append('<a href="vsearch.cgi?ask=1&id=%s">Search</a>' % mod_id)
        links.append('<a href="pics.cgi?m=%s">Pics</a> <a href="vars.cgi?list=LIST&mod=%s&pic1=1&hc=1&picown=1&ci=1&c1=1&c2=1">Creds</a>' % (mod_id.lower(), mod_id))
        links.append('<a href="edlinks.cgi?page=single.%s">Links</a>' % mod_id)
    if os.path.exists(useful.relpath('.', config.LIB_MAN_DIR, mod_id.replace('/', '_').lower())):
	if pif.is_allowed('v'):  # pragma: no cover
	    links.append('<a href="traverse.cgi?d=%s">Library</a>' % useful.relpath('.', config.LIB_MAN_DIR, mod_id.replace('/', '_').lower()))
	if pif.is_allowed('a'):  # pragma: no cover
	    links.append('<a href="upload.cgi?d=%s&m=%s">Library Upload</a>' % (useful.relpath('.', config.LIB_MAN_DIR, mod_id.replace('/', '_').lower()), mod_id.replace('/', '_').lower()))
	    links.append('<a href="/cgi-bin/traverse.cgi?p=%s&d=%s&mr=1&lty=mss&til=1&credit=DT" target="_blank">Tilley List</a>' %
			 (imglib.get_tilley_file().get(mod_id.lower(), [''])[0] + '*',
			 useful.relpath('.', config.LIB_MAN_DIR, mod_id.replace('/', '_').lower())))

    ref_link = ostr = ''
    if pif.is_allowed('a'):  # pragma: no cover
        prodstar = 'far fa-star black'
        if ref.startswith('year.'):
            ref_link = pif.dbh.get_editor_link('lineup_model', {'year': ref[5:], 'mod_id': mod_id})
        elif ref.startswith('matrix.'):
            ref_link = pif.dbh.get_editor_link('matrix_model', {'page_id': ref, 'mod_id': id})
        elif ref.startswith('packs.'):
            ref_link = pif.dbh.get_editor_link('pack_model', {'pack_id': pif.form.get_str('sec'), 'mod_id': mod_id})
        if pic:
	    links.append('')
            prodstar = 'fas fa-star white'
	    prod = pic
            prod += ' <a href="upload.cgi?d=%s&n=%s&c=%s&link=%s"><i class="fas fa-upload"></i></a>' % (pdir.replace('pic', 'lib'), pic, pic, urllib.quote(pif.request_uri))
            prodpic = pif.render.find_image_path(pic, pdir=pdir, largest="m")
            if lm_pic_id:
		prod = '<i class="%s"></i>\n' % prodstar + prod
                prod += ' <a href="%s&useprev=2"><i class="fas fa-step-backward red"></i></a>' % pif.request_uri
            elif prodpic:
                x, y = imglib.get_size(prodpic)
                if x > 400:
                    prodstar = 'fas fa-star yellow'
                elif x == 400:
                    prodstar = 'fas fa-star black'
                else:
                    prodstar = 'fas fa-star red'
		prod = '<i class="%s"></i>\n' % prodstar + prod
                prod += ' <a href="imawidget.cgi?act=1&d=./%s&f=%s&trash=1"><i class="fas fa-times"></i></a>' % (pdir, prodpic[prodpic.rfind('/') + 1:])
		if ref_link:
		    prod += pif.render.format_link(ref_link, ' <i class="fas fa-edit"></i>')
            else:
		prod = '<i class="%s"></i>\n' % prodstar + prod
		if ref_link:
		    prod += pif.render.format_link(ref_link, ' <i class="fas fa-edit"></i>')
                prod += ' <a href="%s&useprev=1"><i class="fas fa-step-backward"></i></a>' % pif.request_uri
	    links.append(prod)
        links.append('')
        vfl = pif.dbh.fetch_variation_files(mod_id)
        for vf in vfl if vfl else [{'mod_id': mod_id, 'imported_from': 'importer'}]:
            links.append('<a href="vedit.cgi?d=src/mbxf&m=%(mod_id)s&f=%(imported_from)s">%(imported_from)s</a>' % vf)
	var_pics, var_texts = show_list_var_pics(pif, mod_id)
        ostr += '<br>\n'.join(var_pics) + '<p>\n'
	fmt_bad, _, _ = pif.dbh.check_description_formatting(mod_id)
	ostr += '<i class="fas fa-times red"></i>' if fmt_bad else '<i class="fas fa-check green"></i>'
	ostr += '<br>'
	for i_vt in range(1, len(var_texts)):
	    vt = var_texts[i_vt]
	    ostr += '<i title="%s" class="%s"></i>\n' % (mbdata.model_texts[i_vt - 1],
		    'far fa-star gray' if not model['format_' + mbdata.desc_attributes[i_vt - 1]] else
                    ('fas fa-star green' if vt == var_texts[0] else ('fas fa-star red' if not vt else 'fas fa-star yellow')))
        ostr += '<p>\n'
        var_ids = [x['v.var'] for x in raw_variations]
        var_ids.sort()
        for var in var_ids:
            ostr += '<a href="vars.cgi?mod=%s&var=%s&edit=1">%s</a>\n' % (mod_id, var, var)
	    if var:
		for sz in mbdata.image_size_types:
		    if os.path.exists(useful.relpath('.', config.IMG_DIR_VAR, sz + '_' + mod_id + '-' + var + '.jpg').lower()):
			ostr += sz.upper() + ' '
		ostr += '<a href="vars.cgi?mod=%s&var=%s&edit=1"><i class="fas fa-edit"></i></a>\n' % (mod_id, var)
		ostr += pif.render.format_link('upload.cgi?d=%s&m=%s&v=%s&l=1&c=%s+variation+%s' % (useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower()), mod_id, var, mod_id, var), '<i class="fas fa-upload"></i>') + '\n'
		ostr += pif.render.format_link('traverse.cgi?g=1&d=%s&man=%s&var=%s' % (useful.relpath('.', config.LIB_MAN_DIR, mod_id.lower()), mod_id, var), '<i class="fas fa-bars"></i>') + '\n'
            ostr += '<br>\n'
	for attr in pif.dbh.fetch_attributes(mod_id):
	    ostr += attr['attribute.attribute_name'] + '<br>\n'
    ostr = '<br>\n'.join(links) + '<p>\n' + ostr
    return ostr


def make_boxes(pif, mod_id, box_types, mack_nums):
    mod_id = box_types[0]['box_type.mod_id']
    base_box_types = [box['box_type.box_type'][0] for box in box_types]
    box_fmt = "<b>%s style box</b><br>%s" #<br>%s entries"
    # rewrite this.  glob for alternate boxes.  well, maybe.
    entries = [
	{'desc':
	    pif.render.format_link('boxart.cgi', txt='%s style box' % box_type,
		args={'mod': mod_id, 'ty': box_type}),
	 'img':
	    pif.render.format_link('boxart.cgi',
		txt=pif.render.format_image_sized([mod_id + '-' + box_type], pdir=config.IMG_DIR_BOX, required=True),
		args={'mod': mod_id, 'ty': box_type}),
	} for box_type in sorted(list(set(base_box_types)))]
    elem = {'title': 'Box Style%(s)s' % {'s': useful.plural(entries)}, 'entry': entries,
	    'columns': 2}
    return elem


def show_lineup_appearances(pif, appearances):
    if not appearances:
	return {}

    #useful.write_comment(str(appearances))
    # lineup appearances
    yd = {}
    rs = set()
    for appear in appearances:
        yd.setdefault(appear['year'], dict())
        yd[appear['year']].setdefault(appear['region'][0], list())
        yd[appear['year']][appear['region'][0]].append(appear)
        rs.add(appear['region'][0])
    rl = filter(lambda x: x in rs, mbdata.regionlist)
    entries = []

    if not yd:
	return {}

    def show_lineup(appear):
	return 'lineup.cgi?year=%(year)s&region=%(region)s&lty=all#%(number)s' % appear

    if 'X' in rs:  # not implemented yet  # pragma: no cover
	#return {}

	columns = ['', 'W']
	for yr in sorted(yd.keys()):
	    if yd[yr].get('X'):
		appear = yd[yr]['X'][0]
		entry = {'': '<b>%s</b>' % str(yr),
			'W': '<a href="lineup.cgi?year=%s&region=U&lty=all#X%s">%s</a>' % (appear['year'], appear['number'], 'X')}
	    entries.append(entry)
    else:
	columns = [''] + rl
	for yr in sorted(yd.keys()):
	    entry = {'': '<b>%s</b>' % str(yr)}
	    for reg in rl:
		entry[reg] = ', '.join([pif.render.format_link(show_lineup(appear), str(appear['number']))
					for appear in yd[yr][reg]]) if yd[yr].get(reg) else '&nbsp;'
	    entries.append(entry)

    llineup = {'id': 'lappear', 'name': '',
	'section': [{'id': 'la', 'name': '', 'columns': columns, 'headers': mbdata.regions,
	    'range': [{'entry': entries}],
	}],
    }
    return llineup


def make_plants(pif, mod_id, plants):
    columns = []
    headers = {}
    entry = {}

    for plant in plants:
	if plant['manufacture'] == 'no origin':
	    flag = ('none', pif.render.find_image_path('no', art=True),)
	elif plant['manufacture'] == '':
	    flag = ('unset', '')
	else:
	    flag = pif.render.show_flag(mbdata.plant_d[plant['manufacture']])
	url = "/cgi-bin/vars.cgi?manufacture=%s&mod=%s" % (plant['manufacture'] if plant['manufacture'] else 'unset', mod_id)
	columns.append(plant['manufacture'])
	headers[plant['manufacture']] = pif.render.format_link(url, useful.img_src(flag[1], also={'title': plant['manufacture']}) if flag[1] else flag[0])
	entry[plant['manufacture']] = pif.render.format_link(url, str(plant['count']))

    llineup = {'id': 'lplants', 'name': '', 'shown': len(plants) > 0,
	'section': [{'id': 'la', 'name': '', 'columns': columns, 'headers': headers,
	    'range': [{'entry': [entry]}],
	}],
    }
    return llineup


img_re = re.compile('src="(?P<u>[^"]*)"')
@basics.web_page
def show_single(pif):
    model = pif.dbh.fetch_casting(pif.form.get_id('id'), extras=True, verbose=True)
    if not model:
	raise useful.SimpleError("That ID wasn't found.")
    pif.render.print_html(status=404 if not model else 200)
    #useful.write_comment('model', model)
    pic = pif.form.get_str('pic')
    pdir = pif.form.get_str('dir')
    if pdir.startswith('./'):
	pdir = pdir[2:]
    if not pdir.startswith('pic/') or '/' in pic:
	pdir = pic = ''
    ref = pif.form.get_id('ref')
    sec = pif.form.get_str('sec')
    ran = pif.form.get_str('ran')
    reg = sec if sec else pic[4] if (ref.startswith('year') and pic and len(pic) > 4 and pic[:4].isdigit()) else ''
    reg_list = mbdata.get_region_tree(reg) + ['']
    mod_id = model['id']
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/single.cgi', 'By ID')
    pif.render.hierarchy_append('/cgi-bin/single.cgi?id=%s' % mod_id, mod_id)

    pif.render.comment('id=', mod_id, 'man=', model)
    raw_variations = variations = []
    if ref:
        raw_variations = pif.dbh.fetch_variation_by_select(mod_id, ref, sec_id=reg_list, ran_id=ran)
        variations = reduce_variations(pif, mod_id, raw_variations)
    base_names = pif.dbh.fetch_variation_base_names(mod_id)
    # years 1971 to 1981 needs to cleave W to U and R
    appearances = list()
    for appear in pif.dbh.depref('lineup_model', pif.dbh.fetch_casting_lineups(mod_id)):
	if (appear.get('region', '') == 'W' and
		int(appear.get('year', 0)) >= 1971 and int(appear.get('year', 0)) <= 1981):
	    nappear = copy.deepcopy(appear)
	    nappear['region'] = 'U'
	    appear['region'] = 'R'
	    appearances.append(nappear)
	appearances.append(appear)
    lm_pic_id = ''
    prod_title = ''
    if ref.startswith('year.'):
	for appear in appearances:
	    if appear.get('page_id', '-') == ref and (appear.get('region', '-') in reg_list or reg_list == ['']):
		prod_title = appear['name']
		lm_pic_id = appear['picture_id']
		break
	if pif.form.has('useprev'):  # pragma: no cover
	    pic = use_previous_product_pic(pif, pif.form.get_int('useprev'), appear)

    appearances.sort(key=lambda x: x['year'])
    aliases = pif.dbh.fetch_aliases(mod_id, 'mack')

    sections_recs = pif.dbh.fetch_sections(where="page_id like 'year.%'")
    sections = {}
    for section in sections_recs:
        if section['columns'] and not section['display_order']:
            sections.setdefault(section['page_id'][5:], [])
            sections[section['page_id'][5:]].append(section)

    boxstyles = pif.dbh.fetch_box_type_by_mod(model['id'])

    pif.render.title = '%(casting_type)s %(id)s: %(name)s' % model
    product_img = pif.render.format_image_sized(pic, pdir=pdir, largest=mbdata.IMG_SIZ_MEDIUM)
    product_img_credit = pif.dbh.fetch_photo_credit(pdir, pic, verbose=True)
    product_img_credit = product_img_credit['photographer.name'] if product_img_credit else ''
    if product_img and pif.is_allowed('a'):  # pragma: no cover
	img = img_re.search(product_img).group('u')
	url = 'imawidget.cgi?d=%s&f=%s' % tuple(img[3:].rsplit('/', 1))
	product_img = pif.render.format_link(url, product_img)

    vscounts = pif.dbh.fetch_variation_select_counts(mod_id)

    model['imgid'] = [model['id']]
    descs = []
    for s in model['descs']:
        if s.startswith('same as '):
            model['imgid'].append(s[8:])
	if s in mbdata.arts:
	    descs.append(pif.render.format_image_icon('c_' + mbdata.arts[s]))
	elif s:
	    descs.append("<i>%s</i>" % s)
    model['descs'] = descs
    model['img'] = pif.render.format_image_required(model['imgid'], made=model['made'], pdir=config.IMG_DIR_MAN, largest=mbdata.IMG_SIZ_MEDIUM if product_img else mbdata.IMG_SIZ_LARGE)
    model_img_credit = pif.dbh.fetch_photo_credit('.' + config.IMG_DIR_MAN, model['imgid'][0], verbose=True)
    model['credit'] = model_img_credit['photographer.name'] if model_img_credit else ''
    if model['country']:
	model['country_flag'] = pif.render.format_image_flag(model['country'])
	model['country_name'] = mflags.FlagList()[model['country']]

    def make_make_link(make, name):
	if not make:
	    return ''
	if not name:
	    name = 'unlicensed'
	pic = pif.render.fmt_img(make, prefix='u', pdir=config.IMG_DIR_MAKE)
	if pic:
	    name = pic + '<br>' + name
	return pif.render.format_link("makes.cgi?make=" + make, name)

    model['make_name'] = make_make_link(model.get('make', ''), model.get('vehicle_make.name', ''))
    def make_make(make):
	return {
	    'image': pif.render.fmt_img(make['vehicle_make.id'], prefix='u', pdir=config.IMG_DIR_MAKE),
	    'id': make['vehicle_make.id'],
	    'name': make['vehicle_make.name'],
	    'company_name': make['vehicle_make.company_name'],
	    'flags': make['vehicle_make.flags'] | make['casting_make.flags'],
	    'link': 'makes.cgi?make=%s' % make['vehicle_make.id'],
	}

    model['makes'] = [make_make(x) for x in pif.dbh.fetch_casting_makes(mod_id)]
    adds = [make_boxes(pif, mod_id, boxstyles, [x['alias.id'] for x in pif.dbh.fetch_aliases(mod_id, 'mack')])] if boxstyles else []
    adds += models.make_adds(pif, mod_id)

    plants = make_plants(pif, mod_id, pif.dbh.fetch_variation_plant_counts(mod_id))
    relateds = pif.dbh.fetch_casting_relateds(mod_id)
    mack_nums = get_mack_numbers(pif, mod_id, model['model_type'], aliases)

    # ------- render ------------------------------------

    pif.render.set_button_comment(pif, 'id=%s&pic=%s&dir=%s&ref=%s' % (mod_id, pic, pdir, ref))
    context = {
	'title': '%s %s: %s' % (mbdata.model_types[model['model_type']], mod_id, model['name']),
	'note': '',
	'type_id': '',
	'icon_id': mod_id if os.path.exists(useful.relpath('.', config.IMG_DIR_MAN_ICON, 'i_' + mod_id.lower() + '.gif')) else '',
	'vehicle_type': [mbdata.model_icons.get(x) for x in model['vehicle_type']],
	'rowspan': '4',
	'left_bar_content': show_left_bar_content(pif, model, ref, pic, pdir, lm_pic_id, raw_variations),
	'model': model,
	'variations': variations,
	'prod_title': prod_title,
	'product_image': product_img,
	'product_img_credit': product_img_credit,
	'mack_nums': mack_nums,
	'product_pic': pic,
	'appearances': show_lineup_appearances(pif, appearances),
	'matrixes': show_series_appearances(pif, pif.dbh.fetch_matrix_appearances(mod_id), relateds),
	'code2s': show_code2_appearances(pif, mod_id, vscounts),
	'packs': show_pack_appearances(pif,
		 sorted(pif.dbh.fetch_pack_model_appearances(mod_id), key=lambda x: x['base_id.first_year'])),
	'show_comparison_link': pif.dbh.fetch_casting_related_exists(mod_id, model['model_type'].lower()),
	'external_links': show_external_links(pif, pif.dbh.fetch_links_single('single.' + mod_id)),
	'relateds': make_relateds(pif, mod_id, [x for x in relateds if x['casting_related.section_id'] == 'single']),
	'compares': make_compares(pif, mod_id, [x for x in relateds if x['casting_related.section_id'] in ['sf', 'rw', 'tr']]),
	'adds_box': models.show_adds(pif, mod_id),
	'adds': adds,
	'plants': plants,
	'base_names': base_names,
	'info_cols': int(bool(model.get('makes'))) + int(bool(mack_nums)) +
	    int(bool(model['scale'])) + int(bool(model['country'])) + int(bool(model['first_year'])),
#	'group': pif.render.find_image_path(mod_id, prefix='g', pdir=config.IMG_DIR_ADD)
    }
    return pif.render.format_template('single.html', **context)
