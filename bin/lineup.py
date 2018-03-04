#!/usr/local/bin/python

import csv, json, os, re, sys
import basics
import config
import imglib
import mbdata
import models
import useful


# A B D J L R U W | man

# X.01 | Packaging                              | pub      |
# X.02 | Catalogs                               | pub      |
# X.03 | Advertisements                         | pub      |
# X.11 | Series                                 | series   |
# X.17 | Promotional                            | promo    |
# X.21 | Early Lesney Toys                      | ks       |
# X.22 | Major Packs                            | ks       |
# X.23 | King Size                              | ks       |
# X.24 | Real Working Rigs                      | ks       |
# X.25 | Super Rigs                             | ks       |
# X.31 | Models of Yesteryear                   | yy       |
# X.41 | Accessory Packs                        | acc      |
# X.51 | Buildings                              | bld      |
# X.61 | Presentation Sets                      | pack     |
# X.62 | Gift Sets                              | pack     |
# X.63 | 5-Packs                                | pack     |
# X.64 | Themed and Licensed 5-Packs            | pack     |
# X.65 | 9- and 10-Packs                        | pack     |
# X.71 | Roadways                               | pub      |
# X.72 | Games and Puzzles                      | pub      |
# X.73 | Books                                  | pub      |

# Australia also had the MB76-79 in 1981.
# The Australian amalgamated range of the mid-1980s (where they mixed the ROW and USA ranges for their 1-75),
# and the 1997 Aussie exclusive 1-75 models? They often get forgotten.

# Germany had a few exclusive 1-75 versions for their market in 1977. 


id_re = re.compile('(?P<a>[a-zA-Z]+)(?P<n>\d+)')
def calc_lineup_model(pif, lsec, year, region, mdict):
    mdict.update({
	'image_format': lsec['img_format'],
	'anchor': '%s%d' % ('X' if region.startswith('X') else '', mdict['number']),
	'class': '', 'product': '', 'prod_id': '', 'href': '',
	'is_reused_product_picture': 0, 'is_product_picture': 0,
	'displayed_id': '',  #'&nbsp;'
    })
    pdir = lsec.get('pic_dir')
    mdict['pdir'] = pdir = pdir if pdir else pif.render.pic_dir

    if not (lsec['flags'] & pif.dbh.FLAG_SECTION_NO_FIRSTS) and str(year) == mdict['base_id.first_year']:
	mdict['class'] = 'revcasting' if mdict['base_id.flags'] & pif.dbh.FLAG_MODEL_CASTING_REVISED else 'newcasting'

    if mdict['casting.id']:
        # modify this if rank_id exists
	mdict['prod_id'] = mdict['casting.id']
        if mdict['picture_id']:
            mdict['product'] = mdict['picture_id'].replace('w', pif.form.get_strl('region'))
            mdict['is_reused_product_picture'] = pif.is_allowed('a')
        elif mdict.get('image_format'):
            mdict['product'] = mdict['image_format'].replace('w', pif.form.get_strl('region')) % mdict['number']
        if pif.render.find_image_path([mdict['product']], suffix='jpg', pdir=mdict['pdir'], largest='m'):
            mdict['is_product_picture'] = 1
        mdict['href'] = "single.cgi?dir=%(pdir)s&pic=%(product)s&ref=%(ref_id)s&sub=%(sub_id)s&id=%(mod_id)s" % mdict
    elif mdict['pack.id']:
	mdict['prod_id'] = mdict['pack.id']
        if mdict['picture_id']:
            mdict['product'] = mdict['picture_id']
            mdict['is_reused_product_picture'] = pif.is_allowed('a')
        elif mdict.get('image_format'):
            mdict['product'] = mdict['image_format'] % mdict['pack.id']
        if pif.render.find_image_path([mdict['product']], pdir=mdict['pdir'], largest=mbdata.IMG_SIZ_GIGANTIC):
            mdict['is_product_picture'] = 1
        mdict['href'] = "packs.cgi?page=%(pack.page_id)s&id=%(pack.id)s" % mdict
    elif mdict['publication.id']:
	mdict['prod_id'] = mdict['publication.id']
        mdict['product'] = mdict['publication.id'] + '_01'
        if pif.render.find_image_path([mdict['product']], pdir=mdict['pdir'], largest=mbdata.IMG_SIZ_GIGANTIC):
            mdict['is_product_picture'] = 1
        mdict['href'] = "pub.cgi?id=%(publication.id)s" % mdict
    elif mdict['page_info.id']: # series
	mdict['prod_id'] = mdict['product'] = mdict['page_info.id']
        mdict['href'] = "matrix.cgi?page=" + mdict['mod_id'][7:]
	if mdict['picture_id']:
	    mdict['href'] += "#" + mdict['picture_id']
	    #mdict['product'] += "-" + mdict['picture_id']

    mdict['product'] = mdict['product'].replace('.', '_')
    mdict['large_img'] = pif.render.format_image_required(
	mdict['product'], suffix='jpg', pdir=mdict['pdir'], largest='m', also={'class': 'largepic'})

    if lsec['flags'] & pif.dbh.FLAG_SECTION_DEFAULT_IDS:
	mdict['shown_id'] = pif.dbh.default_id(mdict['mod_id'])
	disp_format = '%s'
    else:
	mdict['shown_id'] = mdict['number']
	disp_format = lsec.get('disp_format', '')
    if 'ID' in disp_format:
	id_m = id_re.match(mdict['prod_id'])
	if id_m:
	    mdict['displayed_id'] = disp_format.replace('ID', '%s-%d' % (id_m.group('a'), int(id_m.group('n'))))
    elif disp_format and mdict.get('shown_id'):
        mdict['displayed_id'] = disp_format % (mdict['shown_id'])
    mdict['upload_link'] =  pif.render.format_link('upload.cgi?d=%s&n=%s' % (mdict['pdir'], mdict['product']), mdict['large_img'])
    return mdict


def create_lineup(pif, mods, year, lsec, fdebug=False):
    region = lsec['id']
    is_extra = region.startswith('X')
    regions = [region] if is_extra else mbdata.get_region_tree(region) + ['']

    # 1. lay down model list from current region only.
    mods.sort(key=lambda x: (x['lineup_model.number'], x['lineup_model.display_order'],))
    ref_id = 'year.%s' % year

    modlist = []
    foundlist = []
    for mod in mods:
	if ((mod['lineup_model.number'], mod['lineup_model.display_order'],) not in foundlist and
		(not mod['vs.sub_id'] or not mod['vs.sub_id'].isdigit() or int(mod['vs.sub_id']) == mod['lineup_model.number']) and
		((is_extra and region == mod['lineup_model.region']) or not is_extra)):
	     modlist.append(calc_lineup_model(pif, lsec, year, region, pif.dbh.make_lineup_item(mod)))
	     foundlist.append((mod['lineup_model.number'], mod['lineup_model.display_order'],))

    # 2. edit model list for only entries we're interested in
    mods = [mod for mod in mods if
	mod['vs.sub_id'] is None or (
	(not mod['vs.sub_id'].isdigit() or int(mod['vs.sub_id']) == mod['lineup_model.number']) and
	(mod['vs.sub_id'].isdigit() or mod['vs.sub_id'] in regions))
    ]

    # 3. put it in a usable order
    def mod_sort_key(x):
	return (x['lineup_model.number'], x['lineup_model.display_order'],
	    0 if (is_extra or x['vs.sub_id'] is None or x['vs.sub_id'].isdigit()) else regions.index(x['vs.sub_id']),)

    mods.sort(key=mod_sort_key)

    # 4. traverse region tree to figure out variation(s)
    for curmod in modlist:
        set_vars(mods, curmod, regions, ref_id, fdebug)

    # 5. declare victory and grab a beer
    return modlist


def set_vars(rmods, curmod, regions, ref_id, fdebug=False):
    '''Given a model and a lineup, try to figure out where to
    insert that model into the lineup.  This is not easy.'''
    if fdebug:
	print '--------------------------------------------------------'
	print 'SETVAR', regions, ref_id
	print 'CURMOD:', useful.defang(curmod)
	for rmod in rmods:
	    if rmod['lineup_model.number'] == curmod['number'] and rmod['lineup_model.display_order'] == curmod['display_order']:
		print 'RMOD:', rmod['lineup_model.number'], 'ord', rmod['lineup_model.display_order'], 'vs.ref_id', rmod['vs.ref_id'], 'vs.sub_id', rmod['vs.sub_id'], 'var', rmod['v.var'], rmod['v.text_description'], 'pic', rmod['v.picture_id']

    quittable = False
    for region in regions:
	if fdebug:
	    print 'CHECK', region
	for rmod in rmods:
	    if (region.startswith('X') or
		    (rmod['lineup_model.number'] == curmod['number'] and
		     rmod['lineup_model.display_order'] == curmod['display_order'] and
		     (rmod['vs.sub_id'] == region or rmod['vs.sub_id'] == str(curmod['number'])))):
		# add to cvarlist
		for var in curmod['cvarlist']:
		    if rmod['v.var'] in var['var_ids']:
			if fdebug:
			    print 'NO UPDATE'
			break  # "I seen the airport." -- Stephens
		    elif rmod['v.text_description'] == var['desc']:
			if fdebug:
			    print 'UPDATE', rmod['v.var'], rmod['v.text_description']
			var['var_ids'].append(rmod['v.var'])
			pic_id = rmod['v.picture_id'] if rmod['v.picture_id'] else rmod['v.var']
			if pic_id not in var['picture_ids']:
			    var['picture_ids'].append(pic_id)
			var['vars'] = ','.join(var['var_ids'])
			break
		else:
		    pic_id = rmod['v.picture_id'] if rmod['v.picture_id'] else rmod['v.var']
		    curmod['cvarlist'].append({'var_ids': [rmod['v.var']], 'desc': rmod.get('v.text_description', ''),
					       'picture_ids': [pic_id], 'vars': rmod['v.var']})
		    curmod['sub_id'] = rmod['vs.sub_id']
		    if fdebug:
			print 'ADD', rmod['v.var'], rmod['v.text_description']

		    if rmod['vs.sub_id'] == region:
			quittable = True
	    elif fdebug:
		print 'NO ADD'
	if quittable:
	    break
    if fdebug:
	print '<br>'
    return curmod


def get_man_sections(pif, year, region, section_types):
    wheres = ["page_id='year.%s'" % year]
    if not pif.render.is_beta:
        wheres.append("not flags & %d" % pif.dbh.FLAG_SECTION_HIDDEN)
    secs = pif.dbh.fetch_sections(wheres).tolist()
    if not secs:
	raise useful.SimpleError("""I'm sorry, that lineup was not found.  Please use your "BACK" button or try something else.""")

    xsecs = [x for x in secs if x['id'].startswith('X') and x['category'] in section_types]
    secs = [x for x in secs if not x['id'].startswith('X')]

    for region in mbdata.get_region_tree(region):
        lsecs = [x for x in secs if x['id'].startswith(region)]
        if lsecs:
            break
    else:
	region = ''
	lsecs = [{}]
    return region, lsecs[0], lsecs[1:] if 'man' in section_types else [], xsecs


def create_lineup_sections(pif, year, region, section_types, fdebug=False):
    year = mbdata.correct_year(year)
    region = mbdata.correct_region(region, year)
    if not region:
	raise useful.SimpleError("""I'm sorry, that lineup was not found.  Please use your "BACK" button or try something else.""")

    region, mainsec, secs, xsecs = get_man_sections(pif, year, region, section_types)

    # generate main section
    mainsec.update({
	'year': year,
	'region': region,
	'mods': []
    })

    if 'man' in section_types:
	modlist = create_lineup(pif, pif.dbh.fetch_lineup_models(year, region), year, mainsec, fdebug)

	# carve up modlist by section
	if secs:
	    endv = modlist[-1]['number']
	    for sec in reversed(secs):
		sec.update({
		    'id': region + '_' + str(sec['display_order']),
		    'graphics': pif.render.fmt_opt_img([(sec['img_format'][:4] + region + 's%02d' % sec['display_order']).lower()]),
		    'end': endv,
		    'mods': [x for x in modlist if x['number'] > sec['start'] and x['number'] <= endv],
		})
		endv = sec['start']
	else:
	    mainsec.update({
		'id': region + '_1',
		'graphics': pif.render.fmt_opt_img([mainsec['img_format'][:4] + region + 's']),
		'mods': modlist
	    })

    # generate extra sections
    lmods = pif.dbh.fetch_lineup_models(year, [x['id'] for x in xsecs])
    for sec in xsecs:
	sec['mods'] = create_lineup(pif, lmods, year, sec, fdebug)

    # just one more thing, ma'am
    limits = pif.dbh.fetch_lineup_limits()
    mainsec['first_year'] = int(limits['min(year)'])
    mainsec['last_year'] = int(limits['max(year)'])
    return mainsec, secs, xsecs


def render_lineup_model(pif, mdict, comments, unroll=False, large=False):
    ostr = ''
    if mdict['is_product_picture']:
	comments.add('c')
    if large:
        ostr += '<table><tr><td width=400>%s</td><td><center>' % mdict['upload_link']
    if unroll and mdict.get('casting.id') and mdict['cvarlist']:
        for cvar in mdict['cvarlist']:
            ostr += render_lineup_model_var(pif, mdict, comments, show_var=cvar['var_ids'][0])
    else:
        ostr += render_lineup_model_var(pif, mdict, comments)
    if large:
	#ostr += '<br>' + pif.render.format_button("edit", pif.dbh.get_editor_link('lineup_model', {'id': mdict['lineup_model.id']}))
	ostr += pif.render.format_text_input('description.%s' % mdict['id'], 64, value=mdict['name'])
	ostr += pif.render.format_text_input('style_id.%s' % mdict['id'], 4, value=mdict['style_id'])
        ostr += '</center></td></tr></table>'
    mdict.update({
	'mod_text': ostr,
	'display_id': mdict.get('style_id', 0),
	'st_suff': '',
	'style': '',
    })
    return mdict


def render_lineup_model_var(pif, mdict, comments, show_var=None):
    imglist = []
    varlist = []
    if mdict.get('flags', 0) & pif.dbh.FLAG_MODEL_NOT_MADE:
        mdict['not_made'] = True
        imgname = mdict['mod_id'].replace('.', '_')
        imglist.append(imgname)
        comments.add('n')
    elif mdict.get('page_info.id'):
        imgname = mdict['mod_id'].replace('.', '_')
        imglist.append(imgname)
	if mdict['picture_id']:
	    imgname += "-" + mdict['picture_id']
        imglist.insert(0, imgname)
    elif mdict.get('mod_id'):
        imgname = mdict['mod_id'].replace('.', '_')
        imglist.append(imgname)
	for var in mdict['cvarlist']:
	    if not show_var or show_var in var['var_ids']:
		varlist.extend(var['picture_ids'])
    imgstr = pif.render.format_image_required(imglist, prefix=mbdata.IMG_SIZ_SMALL, vars=varlist, pdir=config.IMG_DIR_MAN)
    mdict['imgstr'] = imgstr
    mdict['descriptions'] = [x['desc'] for x in mdict['cvarlist'] if not show_var or show_var in x['var_ids']]
    mdict['no_specific_image'] = 0
    if mdict['casting.id'] and not mdict.get('not_made'):
        if imgstr.find('-') < 0:
            comments.add('i')
            mdict['no_specific_image'] = 1
        if len(varlist) < 1:  # pragma: no cover
            comments.add('v')
            mdict['no_variation'] = 1
        # also if there is no description string

    desclist = list()
    for var in mdict.get('descriptions', []):
	if var and var not in desclist:
	    desclist.append(var)
    mdict['descriptions'] = desclist

    # mdict: imgstr name number pdir product vars
    ostr = models.add_model_table_product_link(pif, mdict)
    return ostr


def render_lineup_year_sections(pif, mainsec, secs, xsecs, large=False):
    unroll = pif.form.get_bool('unroll')
    year = mainsec['year']
    region = mainsec['region']
    comments = set()
    mainsec['range'] = []
    img = pif.render.fmt_img(['%ss' % year])
    if img:
        mainsec['name'] += '<br>' + img
    if large:
	mainsec['columns'] = 1
    if secs:
	for sec in secs:
	    sec['entry'] = [render_lineup_model(pif, x, comments, unroll=unroll, large=large) for x in sec['mods']]
	mainsec['range'] = secs
    else:
	mainsec['range'] = [{'entry': [render_lineup_model(pif, x, comments, unroll=unroll, large=large) for x in mainsec['mods']]}]
    for sec in xsecs:
	if sec['flags'] & pif.dbh.FLAG_SECTION_HIDDEN:
	    sec['name'] = '<i>' + sec['name'] + '</i>'
	sec['entry'] = [render_lineup_model(pif, x, comments, unroll=unroll, large=large) for x in sec['mods']]
    mainsec['range'] += xsecs
    llineup = {'id': 'year', 'section': [mainsec], 'name': '', 'tail': []}

    llineup['comments'] = comments
    llineup['tail'] = ['', '<br>'.join([mbdata.comment_designation[comment] for comment in comments])]
    if large:
	llineup['header'] = '<form action="mass.cgi" method="post">\n<input type="hidden" name="type" value="lineup_desc">\n' + pif.create_token()
	llineup['footer'] = pif.render.format_button_input() + '</form>\n'
#    if pif.is_allowed('a'):  # pragma: no cover
#        llineup['tail'][1] += '<br>multivars %s %s ' % (year, region) + ' '.join(multivars) + '<br>'
    return llineup


def render_lineup_year(pif, mainsec, secs, xsecs, large=False):
    unroll = pif.form.get_bool('unroll')
    footer = ''
    year = mainsec['year']
    region = mainsec['region']
    llineup = render_lineup_year_sections(pif, mainsec, secs, xsecs, large=large)
#    if year > mainsec['first_year']:
#       footer += pif.render.format_button("previous_year", link='?year=%s&region=%s' % (year - 1, pif.form.get_stru('region')))
#    if year < mainsec['last_year']:
#       footer += pif.render.format_button("following_year", link='?year=%s&region=%s' % (year + 1, pif.form.get_stru('region')))
    pif.render.set_footer(footer)
    pif.render.format_matrix_for_template(llineup)
    if year >= 2001 and year <= 2005:
	pif.render.bamcamark = 'bamca_sm2.gif'
    elif year <= 1969:
	pif.render.bamcamark = 'bamca_sm3.gif'
    elif year <= 1974:
	pif.render.bamcamark = 'bamca_sm4.gif'
    return pif.render.format_template('lineup.html', llineup=llineup, large=large, unroll=pif.form.get_bool('unroll'))


def render_lineup_text(pif, mainsec, secs, xsecs):
    output = []
    for sec in [mainsec] + secs + xsecs:
	output.append(sec['name'])
	for mod in sec.get('mods', []):
	    for cvar in mod['cvarlist']:
		output.append('%4s %-8s  %-32s  %s' % (mod['displayed_id'], mod['mod_id'], mod['name'], cvar['desc']))
	output.append('')
    return '\n'.join(output) + '\n'


def render_lineup_checklist(pif, mainsec, secs, xsecs):
    entries = []
    for sec in [mainsec] + secs + xsecs:
	entries.append({'name': sec['name']})
	for mod in sec.get('mods', []):
	    for cvar in mod['cvarlist']:
		entries.append({'number': mod['displayed_id'], 'mod_id': mod['mod_id'], 'name': mod['name'],
				'desc': cvar['desc'], 'x': '<i class="fa fa-square-o"></i>'})

    cols = ['x', 'number', 'mod_id', 'name', 'desc']
    titles = ['', '#', 'Model ID', 'Name', 'Description']
    lsection = {'columns': cols, 'headers': dict(zip(cols, titles)),
	'range': [{'entry': entries, 'note': ''}], 'note': ''}
    llistix = dict(section=[lsection])
    return pif.render.format_template('simplelistix.html', llineup=llistix)


def render_lineup_csv(pif, mainsec, secs, xsecs):
    out_file = sys.stdout
    field_names = ["Number", "Model ID", "Name", "Description"]
    writer = csv.DictWriter(out_file, fieldnames=field_names)
    writer.writeheader()
    for sec in [mainsec] + secs + xsecs:
	writer.writerow(dict(zip(field_names, ln)), ('section', sec['name'], '', ''))
	for mod in sec.get('mods', []):
	    for cvar in mod['cvarlist']:
		writer.writerow(dict(zip(field_names, ln)), (mod['number'], mod['mod_id'], mod['name'], cvar['desc'],))
    return ''


def render_lineup_json(pif, mainsec, secs, xsecs):
    sec_keys = ['year', 'id', 'category', 'name', 'note', 'range']
    ran_keys = ['id', 'category', 'name', 'note']
    mod_keys = ['displayed_id', 'made', 'mod_id', 'name']
    var_keys = ['desc', 'vars']

    mainsec['range'] = []
    if secs:
	mainsec['range'] = secs
    mainsec['range'] += xsecs
    sec = {x: mainsec[x] for x in sec_keys}
    sec['range'] = []
    for mran in mainsec['range']:
	ran = {x: mran[x] for x in ran_keys}
	ran['model'] = []
	for mmod in mran['mods']:
	    mod = {x: mmod[x] for x in mod_keys}
	    if mmod['cvarlist']:
		for mvar in mmod['cvarlist']:
		    mod['var'] = {x: mvar[x] for x in var_keys}
	    ran['model'].append(mod)
	sec['range'].append(ran)
    llineup = {'section': [sec]}
    return json.dumps(llineup)


def year_lineup_main(pif, listtype):
    region = pif.form.get_stru('region')
    year = pif.form.get_str('year')
    section_types = pif.form.get_list('lty')

    if section_types == ['all']:
	section_types = dict(mbdata.lineup_types).keys()

    pif.render.hierarchy_append('/cgi-bin/lineup.cgi?year=%s&region=%s&lty=all' % (year, region),
        str(year) + ' ' + mbdata.regions.get(region, ''))
    pif.render.set_button_comment(pif, 'yr=%s&rg=%s' % (year, region))

    mainsec, secs, xsecs = create_lineup_sections(pif, year, region, section_types, fdebug=pif.form.get_bool('verbose'))

    # now that we have our sections calculated, format them.
    if listtype == mbdata.LISTTYPE_CSV:
	return render_lineup_csv(pif, mainsec, secs, xsecs)
    elif listtype == mbdata.LISTTYPE_JSON:
	return render_lineup_json(pif, mainsec, secs, xsecs)
    elif listtype == mbdata.LISTTYPE_TEXT:
	return render_lineup_text(pif, mainsec, secs, xsecs)
    elif listtype == mbdata.LISTTYPE_CHECKLIST:
	return render_lineup_checklist(pif, mainsec, secs, xsecs)
    # normal and/or large
    return render_lineup_year(pif, mainsec, secs, xsecs,
			      large=(listtype == mbdata.LISTTYPE_LARGE))

#--------- prodpics --------------------------------

def run_product_pics(pif, region):
    halfstars = dict()
    if os.path.exists('pic/multivars.dat'):
        for ln in open('pic/multivars.dat').readlines():
            ln = ln.strip().split()
            if len(ln) > 1 and ln[1] == region:
                halfstars[ln[0]] = [int(x) for x in ln[2:]]
    syear = 'year.' + pif.form.get_str('syear', '0000')
    eyear = 'year.' + pif.form.get_str('eyear', '9999')
    pages = [x for x in pif.dbh.fetch_page_years() if x['page_info.id'] >= syear and x['page_info.id'] <= eyear]
    pages = {x['id']: x for x in pages}
    gather_rank_pages(pif, pages, region)
    region_list = mbdata.get_region_tree(region)

    llineup = {'id': pif.page_id, 'section': [], 'name': '', 'tail': ''}
    lsec = {'columns': 1, 'id': 'lineup', 'range': []}
    hdr = ""

    for page in sorted(pages.keys()):
        lmodlist = pif.dbh.fetch_simple_lineup_models(page[5:], region)
        lmodlist = filter(lambda x: x['lineup_model.region'][0] in region_list, lmodlist)
        lmoddict = {x['lineup_model.number']: x for x in lmodlist}
        min_num = 1
        max_num = pages[page]['max_lineup_number']
        if pif.form.get_str('num'):
            min_num = pif.form.get_int('num')
        if pif.form.get_str('enum'):
            max_num = pif.form.get_int('enum')
        lsec['columns'] = max(lsec['columns'], max_num + 1)
        lran = {'id': pages[page]['id'], 'name': '', 'entry': [], 'note': '', 'graphics': []}
        ent = {
            'text': '<a href="?year=%s&region=%s&lty=all&submit=1">%s</a>' % (page[5:], region, page[5:]),
            'display_id': '1', 'style': ''
        }
        lran['entry'].append(ent)
        for mnum in range(min_num, max_num + 1):
            ifmt, pdir = get_product_image(pages[page], mnum)
            lmod = lmoddict.get(mnum, {})
            lpic_id = pic_id = lmod.get('lineup_model.picture_id', '').replace('w', pif.form.get_strl('region'))
            if pic_id:
                lpic_id = pic_id = pic_id.replace('W', pif.form.get_stru('region'))
                product_image_path, product_image_file = pif.render.find_image_file(pic_id, suffix='jpg', pdir=pdir, largest='l')
            else:
                lpic_id = ifmt % mnum
                product_image_path, product_image_file = pif.render.find_image_file([ifmt % mnum], suffix='jpg', pdir=pdir, largest='l')
	    if not lmod or lmod.get('lineup_model.flags', 0) & pif.dbh.FLAG_MODEL_NOT_MADE:
		pic_id = None
            lnk = "single.cgi?dir=%s&pic=%s&ref=%s&sub=%s&id=%s" % (pdir, lpic_id, page, '', lmod.get('lineup_model.mod_id', ''))
	    istar = imglib.format_image_star(pif, product_image_path, product_image_file, pic_id, mnum in halfstars.get(page[5:], []))
            ent = {
                'text': pif.render.format_link(lnk, istar),
                'display_id': str(int(mnum % 10 == 0 or page[-1] == '0'))
            }
            lran['entry'].append(ent)
        lsec['range'].append(lran)

    llineup['section'].append(lsec)
    return llineup


def gather_rank_pages(pif, pages, region):
    # all this is to grab pic_dir and img_format from section.  that's it.
    region_list = mbdata.get_region_tree(region)
    sections = [x for x in pif.dbh.fetch_sections(where="page_id like 'year.%'")
		if x['id'][0] in region_list]
    sections.sort(key=lambda x: x['start'], reverse=True)
    for rg in region_list:
        for page in pages:
            pages[page].setdefault('section', list())
            for section in sections:
                if section['id'].startswith(rg) and section['page_id'] == page:
                    pages[page]['section'].append(section)
    # now each page should have the right sections and in the right order
    # the first section found where start < num is the right one
    # though really we only care about the first one


def get_product_image(page, mnum):
    if page:
        if page.get('section'):
	    section = page['section'][0]
	    #useful.write_comment('get_product_image section', section['page_id'], section['id'])
	    return section['img_format'], page['pic_dir']
	#useful.write_comment('get_product_image no section')
    #else:
	#useful.write_comment('get_product_image no page')
    return 'xxx%02d', 'unknown'


def product_pic_lineup_main(pif):
    pif.render.styles.append('prodpic')
    pif.render.title = mbdata.regions.get(pif.form.get_str('region'), 'Matchbox') + ' Lineup'
    llineup = run_product_pics(pif, pif.form.get_str('region').upper())
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('simplematrix.html', llineup=llineup)

#--------- by ranks --------------------------------

def generate_rank_lineup(pif, rank, region, syear, eyear):
    verbose = pif.render.verbose
    regionlist = mbdata.get_region_tree(region) + ['']
    lmodlist = pif.dbh.fetch_lineup_models_by_rank(rank, syear, eyear)
    lmodlist.sort(key=lambda x: x['lineup_model.year'])
    years = dict()
    for mod in lmodlist:
        year = int(mod['lineup_model.year'])
        if mod['lineup_model.region'] in regionlist:
            years.setdefault(year, list())
            years[year].append(mod)

    for year in sorted(years.keys()):
	yield set_vars(years[year], pif.dbh.make_lineup_item(years[year][0]), regionlist, 'year.%s' % year)


def run_ranks(pif, mnum, region, syear, eyear):
    if not mnum:
        raise useful.SimpleError('Lineup number must be a number from 1 to 120.  Please back up and try again.')
    pif.render.comment('lineup.run_ranks', mnum, region, syear, eyear)

    pages = {x['id']: x for x in pif.dbh.fetch_page_years()}
    gather_rank_pages(pif, pages, region)

    lmodlist = generate_rank_lineup(pif, mnum, region, syear, eyear)

    llineup = {'id': pif.page_id, 'section': [], 'name': '', 'tail': ''}
    lsec = {'columns': 5, 'id': 'lineup', 'range': [], 'flags': 0, 'name': ''}
    hdr = "Number %s" % mnum
    comments = set()

    lran = {'id': 'range', 'name': '', 'entry': [], 'note': '', 'graphics': []}
    pif.render.comment("run_ranks: range", lran)
    for mdict in lmodlist:
        if mdict:
            ifmt, pdir = get_product_image(pages.get(mdict.get('page_id', ''), {}), mnum)
            mdict['image_format'] = lsec['img_format'] = ifmt
            mdict['disp_format'] = '%s.'
            lsec['pic_dir'] = pdir
            mdict['anchor'] = '%d' % mdict['number']
	    mdict = calc_lineup_model(pif, lsec, mdict['year'], region, mdict)
            mdict['displayed_id'] = str(mdict['year'])
	    ent = render_lineup_model(pif, mdict, comments)
            if mdict['year'] == mdict['base_id.first_year']:
                ent['class'] = 'newcasting'
            lran['entry'].append(ent)
        else:
            lran['entry'].append({'text': '', 'display_id': ''})
    lsec['range'].append(lran)

    llineup['section'].append(lsec)
    pif.render.set_button_comment(pif, 'yr=%s&rg=%s' % (pif.form.get_str('year'), pif.form.get_str('region')))
    llineup['tail'] = ['', '<br>'.join([mbdata.comment_designation[comment] for comment in comments])]
    return llineup


def rank_lineup_main(pif):
    pif.render.hierarchy_append('/cgi-bin/lineup.cgi?n=1&num=%s&region=%s&syear=%s&eyear=%s&lty=all' % (pif.form.get_str('num'), pif.form.get_str('region'), pif.form.get_str('syear'), pif.form.get_str('eyear')),
        "%s #%d" % (mbdata.regions.get(pif.form.get_str('region'), ''), pif.form.get_int('num')))
    pif.render.title = 'Matchbox Number %d' % pif.form.get_int('num')
    llineup = run_ranks(pif, pif.form.get_int('num'), pif.form.get_str('region', 'U').upper(), pif.form.get_str('syear', '1953'), pif.form.get_str('eyear', '2014'))
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('lineup.html', llineup=llineup, large=False, unroll=pif.form.get_bool('unroll'))

#--------- select lineup ---------------------------

def select_lineup(pif, region, year):
    lran = {'entry': []}
    lsec = {'range': [lran]}
    llineup = {'section': [lsec], 'header': '<form>\n', 'footer': '</form>'}
    lines = pif.render.format_radio('year', [(x['year'], x['year']) for x in pif.dbh.fetch_lineup_years()],
		checked=year, sep='<br>\n')
    while lines:
	lran['entry'].append({'text': ''.join(lines[:15])})
	lines = lines[15:]
    lran['entry'].append({'text': ''.join(
	pif.render.format_radio('region', [(x, mbdata.regions[x]) for x in mbdata.regionlist[1:]], checked=region, sep='<br>\n'))})
    lran['entry'].append({'text': ''.join(
	pif.render.format_checkbox('lty', mbdata.lineup_types, checked=[x[0] for x in mbdata.lineup_types], sep='<br>\n')) +
	'<p>' + pif.render.format_button_input()})
    lsec['columns'] = len(lran['entry'])
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('simplematrix.html', llineup=llineup)

#--------- multiyear lineup ------------------------

def run_multi_file(pif, year, region, nyears):
    # as yet not rewritten
    pages = pif.dbh.fetch_pages('id in (' + ','.join(["'year.%d'" % x for x in range(int(year), int(year) + nyears)]) + ')')

    modlistlist = []
    max_mods = 0
    y = int(year)
    nyears = len(pages)
    for page in pages:
        page['year'] = str(y)
        reg, mainsec, secs, xsecs = get_man_sections(pif, str(y), region, ['man'])
        page['region'] = reg
        page['sec'] = mainsec
        page['img_format'] = mainsec['img_format']
        page['mods'] = create_lineup(pif, pif.dbh.fetch_lineup_models(y, region), y, mainsec)
        max_mods = max(max_mods, len(page['mods']))
        y += 1

    llineup = {'id': pif.page_id, 'section': [], 'name': ''}
    lsec = pages.first['sec']
    lsec['columns'] = nyears
    lsec['id'] = 'lineup'
    lsec['range'] = []
    hdr = lsec['name']
    comments = set()

    lran = {'id': 'range', 'name': '', 'entry': [], 'note': '', 'graphics': ''}
    pif.render.comment("run_file: range", lran)
    for inum in range(max_mods):
        for iyr in range(nyears):
            pdir = pages[iyr]['page_info.pic_dir']
            if pages[iyr]['mods']:
                mdict = pages[iyr]['mods'].pop(0)
                #mdict['disp_format'] = lsec.get('disp_format', '')
                mdict['shown_id'] = mdict['number']
                mdict['image_format'] = pages[iyr]['img_format']
                mdict['pdir'] = pdir
                mdict['anchor'] = '%d' % mdict['number']
		#mdict['region'] = region
		mdict = calc_lineup_model(pif, pages[iyr]['sec'], year + iyr, region, mdict)
                mdict['display_id'] = mdict.get('style_id', 0)
                if int(year) + iyr == int(mdict['base_id.first_year']):
                    mdict['class'] = 'newcasting'
		mdict['displayed_id'] += ' (%s)' % (year + iyr)
		lran['entry'].append(render_lineup_model(pif, mdict, comments))
	    else:
		lran['entry'].append({'mod_text': ''})
    lsec['range'].append(lran)

    llineup['section'].append(lsec)
    pif.render.set_button_comment(pif, 'yr=%s&rg=%s' % (pif.form.get_str('year'), pif.form.get_str('region')))
    llineup['tail'] = ['', '<br>'.join([mbdata.comment_designation[comment] for comment in comments])]
    return llineup


def render_multiyear(pif, nyears=5):
    region = pif.form.get_stru('region')
    year = mbdata.correct_year(pif.form.get_str('year'))
    region = mbdata.correct_region(region, year)
    pif.render.hierarchy_append('/cgi-bin/lineup.cgi?year=%s&region=%s&lty=all' % (year, region),
        "%s %s" % (year, mbdata.regions.get(region)))
    pif.render.title = 'Matchbox %d-%d' % (year, year + nyears - 1)
    llineup = run_multi_file(pif, year, region.upper(), nyears)
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('lineup.html', llineup=llineup, large=False, unroll=pif.form.get_bool('unroll'))

#--------- remember the main -----------------------

@basics.web_page
def main(pif):
    listtype = pif.form.get_str('listtype')
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/lineup.cgi', 'Annual Lineup')

    if pif.form.has('prodpic'):
	pif.render.print_html()
        return product_pic_lineup_main(pif)
    elif pif.form.get_int('byrank'):
	pif.render.print_html(mbdata.get_mime_type(listtype))
        return rank_lineup_main(pif)
    elif pif.form.get_str('region') and pif.form.get_str('year'):
	pif.render.print_html(mbdata.get_mime_type(listtype))
	if listtype == mbdata.LISTTYPE_MULTIYEAR:
	    return render_multiyear(pif)
        return year_lineup_main(pif, listtype)
    pif.render.print_html()
    pif.render.title = str(pif.form.get_str('year', 'Matchbox')) + ' Lineup'
    return select_lineup(pif, pif.form.get_str('region', 'W').upper(), pif.form.get_str('year', '0'))

#--------- command line stuff ----------------------

def picture_count(pif, region, year):
    # nonfunctional as yet
    pr_count = im_count = 0
    return 0,0
    year = mbdata.correct_year(year)
    region = mbdata.correct_region(region, year)
    llineup = {'id': region, 'section': [], 'name': '', 'tail': []}

    region, lsec, secs, xsecs = get_man_sections(pif, year, region, dict(mbdata.lineup_types).keys())
    if not region:
        return 0, 0

    modlist = list(generate_man_lineup(pif, year, region))

    endv = len(modlist)
    for sec in reversed(secs):
        sec['end'] = endv
        endv = sec['start']

    lsec['id'] = region
    lsec['range'] = []

    if secs:
        for lran in secs:
            lran.update({
                'id': region + '_' + str(lran['display_order']),
                'entry': [],
                'graphics': pif.render.fmt_opt_img([(lran['img_format'][:2] + region + 's%02d' % lran['display_order']).lower()])
            })
            count = count_section(pif, lsec, lran, modlist[lran['start']:lran['end']], region, year)
            pr_count += count[0]
            im_count += count[1]
    else:
        lran = copy.deepcopy(lsec)
        lran.update({'id': region + '_1', 'name': '', 'entry': [], 'note': '', 'graphics': '&nbsp;'})
        count = count_section(pif, lsec, lran, modlist, region, year)
        pr_count += count[0]
        im_count += count[1]

    #==================================

    #xsecs = get_extra_sections(pif, year)
    create_extra_lineup(pif, year, xsecs, verbose=pif.render.verbose)

    for lran in xsecs:
        lran.update({
            'id': 'X_' + str(lran['display_order']),
            'entry': [],
            'graphics': pif.render.fmt_opt_img([(lran['img_format'][:2] + region + 's%02d' % lran['display_order']).lower()])
        })
        count = count_section(pif, lsec, lran, lran['mods'], 'X', year)
        pr_count += count[0]
        im_count += count[1]
    return pr_count, im_count


def count_section(pif, lsec, lran, mods, region, year):
    im_count = pr_count = 0
    for mdict in mods:
        mdict['image_format'] = lran['img_format']
        pdir = pif.render.pic_dir
        if lran.get('pic_dir'):
            pdir = lran['pic_dir']
        mdict['pdir'] = pdir
        pr_count += 1
        im_count += count_lineup_model(pif, mdict)
    return pr_count, im_count


def yearlist(pif):
    for year in range(1953, 2018):
	rl = set()
	for reg in mbdata.regionlist[1:]:
	    rl.add(mbdata.correct_region(reg, year))
	print year, rl


def cklup(pif):
    mainsec, secs, xsecs = create_lineup_sections(pif, pif.form.get_str('year', '1966'), pif.form.get_str('region', 'W'), dict(mbdata.lineup_types).keys())

    for sec in [mainsec] + secs:
	print sec['id']
	for mod in sec.get('mods', []):
	    print ' ', mod['number'], mod['display_order'], mod['name']
	    for vard in mod['cvarlist']:
		print '    ', vard['desc']

    for sec in xsecs:
	print sec['id']
	for mod in sec['mods']:
	    print '   ', mod['number'], mod['display_order'], mod['name']


def year_lineup(pif, year, region):
    section_types = dict(mbdata.lineup_types).keys()
    mainsec, secs, xsecs = create_lineup_sections(pif, year, region, section_types, fdebug=False)
    llineup = {'id': 'year', 'section': [], 'name': '', 'tail': []}
    print render_lineup_text(pif, mainsec, secs, xsecs)


def clone_lineup(pif, year, old_region, new_region=''):
    old_region = old_region.upper()
    new_region = new_region.upper()
    for mod in pif.dbh.depref('lineup_model', pif.dbh.fetch_lineup_models_bare(year, old_region)):
	if old_region != new_region and new_region:
	    del mod['id']
	    mod['base_id'] = mod['base_id'].replace(old_region, new_region)
	    mod['picture_id'] = mod['picture_id'].replace(old_region.lower(), new_region.lower())
	    mod['region'] = new_region
	    pif.dbh.insert_lineup_model(mod)
	print mod


def count_lineup(pif, year, region):
    print picture_count(pif, region, year)


def rank_lineup(pif, number, region, syear, eyear):
    llineup = run_ranks(pif, number, region.upper(), syear, eyear)
    print render_lineup_text(pif, llineup['section'][0], llineup['section'][1:], [])


def list_lineups(pif):
    section_types = ['man']#dict(mbdata.lineup_types).keys()
    ctypes = sorted(mbdata.comment_name.keys())
    regionlist = [x for x in mbdata.regionlist if x != 'W']
    limits = pif.dbh.fetch_lineup_limits()
    first_year = int(limits['min(year)'])
    last_year = int(limits['max(year)'])
    comments = set()
    for year in range(first_year, last_year + 1):
	regions = sorted(set([mbdata.correct_region(x, year) for x in regionlist]))
	if not regions:
	    regions = ['R', 'U']
	for region in regions:
	    mainsec, secs, xsecs = create_lineup_sections(pif, year, region, section_types)
	    llineup = render_lineup_year_sections(pif, mainsec, secs, xsecs)
	    comments |= llineup['comments']
	    print year, region, ':', ' '.join([x if x in llineup['comments'] else ' ' for x in ctypes])
    print
    for comment in sorted(comments):
	print comment, mbdata.comment_name[comment]


# input file has new models in form:
#1|MB1002|Heavy Railer|red/yellow
# lineup_number | mod_id | mod_name | var_description

# currently can't handle multiple variations of a particular number

# hardcoded values:
regions = ['U', 'R']
picdir = 'pic/prod/mworld'


def raw_insert(pif, table, data):
    pif.dbh.dbi.insert_or_update(
    #print (
	table, data
    )


def add_page(pif, year):
    raw_insert(pif, 'page_info', {
        'id': 'year.' + year,
        'flags': 0,
        'format_type': 'lineup',
        'title': 'Matchbox %s Lineup' % year,
        'pic_dir': picdir,
        'tail': '',
        'description': '',
        'note': '',
    })


def add_section(pif, year, region):
    raw_insert(pif, 'section', {
        'id': region,
        'page_id': 'year.' + year,
        'display_order': 0,
        'category': 'man',
        'flags': 0,
        'name': mbdata.regions[region],
        'columns': 4,
        'start': 0,
        'pic_dir': '',
        'disp_format': '%d.',
        'link_format': pif.form.get_str('link_fmt'),
        'img_format': '%s%s%%03d' % (year, region.lower()),
        'note': '',
    })


def add_casting(pif, mod, year):
    # base_id: id, first_year, model_type, rawname, description, flags
    # casting: id, country, make, section_id
    pif.dbh.add_new_base_id(
    {
	'id': mod[1],
	'first_year': year,
	'model_type': 'SF',
	'rawname': mod[2],
	'description': '',
	'flags': 0,
    })
    pif.dbh.add_new_casting(
    {
	'id': mod[1],
	'country': '',
	'make': '',
	'section_id': 'man3',
	'notes': '',
    })


def add_variation(pif, mod, year):
    var_id = 'Y' + year[2:]
    var = {
	'mod_id': mod[1],
	'var': var_id,
	'flags': 0,
	'text_description': '',
	'text_base': '',
	'text_body': '',
	'text_interior': '',
	'text_wheels': '',
	'text_windows': '',
	'text_with': '',
	'base': '',
	'body': mod[3],
	'interior': '',
	'windows': '',
	'manufacture': '',
#	'category': '',
	'area': '',
	'date': '',
	'note': '',
	'other': '',
	'picture_id': '',
	'imported': '',
	'imported_from': 'file',
	'imported_var': var_id,
    }
    #print ('variation', mod[1], var_id, var)
    pif.dbh.insert_variation(mod[1], var_id, var, verbose=True)
    pif.dbh.recalc_description(mod[1], showtexts=False, verbose=False)


def add_lineup_model(pif, mod, year, region):
    lin_id = '%s%s%03d' % (year, region, int(mod[0]))
    # lineup_model
    raw_insert(pif, 'lineup_model', {
	'base_id': lin_id,
	'mod_id': mod[1],
	'number': mod[0],
	'flags': 0,
	'style_id': '',
	'picture_id': '',
	'region': region,
	'year': year,
	'name': mod[2],
	'page_id': 'year.' + year,
    })


def add_variation_select(pif, mod, year, region):
    raw_insert(pif, 'variation_select', {
	'ref_id': 'year.' + year,
	'mod_id': mod[1],
	'var_id': 'Y' + year[2:],
	'sub_id': '',
    })


def make_lineup(pif, year, fn):
    inmods = [x.split('|') for x in open(fn).readlines()]
    add_page(pif, year)
    for region in regions:
	add_section(pif, year, region)
    for mod in inmods:
	casting = pif.dbh.fetch_casting(mod[1])
	if not casting:
	    add_casting(pif, mod, year)
	add_variation(pif, mod, year)
	for region in regions:
	    add_lineup_model(pif, mod, year, region)
	add_variation_select(pif, mod, year, '')


def check_lineup(pif, *args):
    def do_lup(pif, year, region):
	lup = lineup.run_file(pif, region, str(year))
	totals['i'] += lup['var_info']['i']
	totals['p'] += lup['var_info']['p']
	print '%d  %s  %3d  %3d' % (year, region, lup['var_info']['i'], lup['var_info']['p'])

    totals = {'i': 0, 'p': 0}

    st = 1953
    en = 2014
    if args:
        st = int(args[0])
        if len(args) > 1:
            en = int(args[1])
        else:
            en = st
    for year in range(st, en + 1):
        pif.page_id = 'year.%d' % year
        lup = do_lup(pif, year, 'U')
        if year >= 1982:
            lup = do_lup(pif, year, 'R')
        if year in (1999, 2000, 2001):
            lup = do_lup(pif, year, 'D')
        if year in (2000, 2001):
            lup = do_lup(pif, year, 'B')
            lup = do_lup(pif, year, 'A')
        if year >= 2008 and year <= 2011:
            lup = do_lup(pif, year, 'L')
    print '        %4d %4d' % (totals['i'], totals['p'])


def show_sections(pif):
    import tables
    secs = pif.dbh.depref('section', pif.dbh.fetch('section', where='page_id like "year.%" and id like "X.%"'))
    sec_ids = set()
    pages = {}
    for sec in secs:
	sec['showflag'] = '-' if sec['flags'] & 1 else 'X'
	sec_ids.add(sec['id'][2:])
	pages.setdefault(sec['page_id'][5:], dict())
	pages[sec['page_id'][5:]][sec['id'][2:]] = sec
    sec_ids = sorted(sec_ids)
    print 'page |', ' | '.join(sec_ids), '|'
    print '-----+' + len(sec_ids) * '----+'
    for page_id in sorted(pages):
	print page_id, '|', ' | '.join([pages[page_id].get(sec_id, {}).get('showflag', ' ') + ' ' for sec_id in sec_ids]) + ' |'


cmds = [
    ('s', year_lineup, "show: year region [number]"),
    ('c', clone_lineup, "clone: year old_region new_region"),
    ('p', count_lineup, "count: year region"),
    ('r', rank_lineup, "ranks: number region syear eyear"),
    ('l', list_lineups, "list lineups"),
    ('m', make_lineup, "make lineup"),
    ('x', check_lineup, "check lineup"),
    ('s', show_sections, "show sections"),
]


@basics.command_line
def commands(pif):
    useful.cmd_proc(pif, './lineup.py', cmds)

#---- ---------------------------------------

if __name__ == '__main__':  # pragma: no cover
    commands(page_id='editor', dbedit='')
