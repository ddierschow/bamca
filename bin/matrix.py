#!/usr/local/bin/python

import copy, re, urllib
import basics
import config
import mbdata
import tables
import useful

d_re = re.compile(r'%\d*d')

class MatrixFile(object):
    def __init__(self, pif):
        self.tables = []
        self.text = []
	self.dates = set()
	if pif.form.has('page'):
	    self.from_file(pif)
	elif pif.form.has('cat'):
	    self.from_cat(pif)

    def create_ent(self, pif, ent, mat):
	if ent['matrix_model.section_id'] != mat['id']:
	    return None
	# these should be outer level
	ffmt = {'link': mat['link_format'], 'disp': mat['disp_format'], 'img': mat['img_format']}
	is_num_id = d_re.search(ffmt['disp']) or d_re.search(ffmt['link']) or d_re.search(ffmt['img'])
	ent['vs.ref_id'] = ent['vs.ref_id'] or ''
	ent['vs.sec_id'] = ent['vs.sec_id'] or ''
	ent['vs.ran_id'] = ent['vs.ran_id'] or ''
	ent['id']              = ent['matrix_model.id']
	ent['mod_id']          = ent['matrix_model.mod_id']
	ent['section_id']      = ent['matrix_model.section_id']
	ent['display_order']   = ent['matrix_model.display_order']
	ent['page_id']         = ent['matrix_model.page_id']
	ent['range_id']        = ent['matrix_model.range_id']
	ent['flags']           = ent['matrix_model.flags']
	ent['shown_id']        = ent['matrix_model.shown_id']
	ent['name']            = ent['matrix_model.name']
	ent['subname']         = ent['matrix_model.subname']
	ent['subnames']        = ent['matrix_model.subname'].split(';')
	ent['sub_id']          = mbdata.reverse_regions.get(ent['matrix_model.subname'], '')
	ent['model_type']      = ent['base_id.model_type']
	ent.setdefault('pack.page_id', '')
	ent['description']     = []
	if ent.get('sub_id') and ent.get('vs.sec_id') and ent['sub_id'] != ent['vs.sec_id']:
	    return None
	if ent.get('v.text_description'):
	    ent['description'].append(ent['v.text_description'])
	if ent.get('matrix_model.description'):
	    ent['description'].extend(ent['matrix_model.description'].split(';'))
	ent['description'] = filter(None, ent['description'])
	ent['disp_id'] = ent['image'] = ent['link'] = ''
	ent['pdir'] = mat['pic_dir'] if mat['pic_dir'] else pif.render.pic_dir
	ent['disp_format'] = mat['disp_format']
	# currently this formats all the variations then just uses one.  needs to collate the variations then
	# call format_image_* with that.
	if is_num_id:
	    ent['range_id'] = int(ent['range_id']) if ent['range_id'] else 0
	if ent['model_type'] == 'MP':
	    ent['image'] = \
		    pif.render.format_image_required(ent['mod_id'], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_MAN, nopad=True, blank=True)
	elif ent['range_id'] and ffmt['img']:
	    ent['image'] = \
		    pif.render.format_image_required([useful.clean_name(ffmt['img'] % ent['range_id'], '/')], pdir=ent['pdir'])
	elif ent.get('v.picture_id'):
	    ent['image'] = \
		    pif.render.format_image_optional(ent['mod_id'] + '-' + ent['v.picture_id'], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_VAR, nopad=True)
	elif ent.get('v.var'):
	    ent['image'] = \
		    pif.render.format_image_optional(ent['mod_id'] + '-' + ent['v.var'], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_VAR, nopad=True)
	elif '%' in ffmt['link']:
	    ent['image'] = \
		    pif.render.format_image_required([useful.clean_name(ffmt['link'] % ent['range_id'], '/')], prefix=mbdata.IMG_SIZ_SMALL, pdir=ent['pdir'], blank=True)
	else:
	    ent['image'] = \
		    pif.render.format_image_required([useful.clean_name(ffmt['link'], '/')], prefix=mbdata.IMG_SIZ_SMALL, pdir=ent['pdir'], blank=True)
	if ent['range_id'] and ffmt['disp']:
	    ent['disp_id'] = ent['range_id']
	if ent['range_id'] and ffmt['link']:
	    ent['link'] = useful.clean_name(ffmt['link'] % ent['range_id'], '/') if '%' in ffmt['link'] else useful.clean_name(ffmt['link'], '/')
	pif.render.comment('        entry:', ent)
	return ent

    def from_file(self, pif):
	pif.render.hierarchy_append('/cgi-bin/matrix.cgi', 'Series')
	pif.render.hierarchy_append('/cgi-bin/matrix.cgi?page=%s' % pif.form.get_str('page'), pif.render.title)
        mats = pif.dbh.fetch_sections({'page_id': pif.page_id})
        ents = pif.dbh.fetch_matrix_models_variations(pif.page_id)
        for mat in mats:
            mat['text'] = ''
            mat['ents'] = {}
            pif.render.comment('matrix section:', mat)
            for ent in ents:
		ent = self.create_ent(pif, ent, mat)
		if ent:
                    mat['ents'].setdefault(ent['range_id'], list())
                    mat['ents'][ent['range_id']].append(ent)
                    pif.render.comment('        entry:', ent)
            self.tables.append(mat)
        self.tables.sort(key=lambda x: x['display_order'])

    def from_cat(self, pif):
	cat_id = pif.form.get_str('cat')
	if not cat_id:
	    return
	cat = pif.dbh.fetch_category(cat_id)
	if not cat:
	    raise useful.SimpleError('Category not found. %s' % cat_id)
	pif.render.title = cat.name
	pif.render.hierarchy_append('/database.php#cats', 'By Categories')
	pif.render.hierarchy_append('/cgi-bin/matrix.cgi?cat=%s' % cat_id, cat.name)
        mat = { # maybe make this the section for page_id='matrix'?
	    'id': 'cat',
	    'page_id': 'matrix',
	    'display_order': 0,
	    'category': cat['category.name'],
	    'flags': 0,
	    'name': '',
	    'columns': 4,
	    'start': 0,
	    'pic_dir': '',
	    'disp_format': '',
	    'link_format': '',
	    'img_format': '',
	    'note': '',
	}
	mat['text'] = ''
	mat['ents'] = {}
	pif.render.comment('matrix section:', mat)
	date_re = re.compile("^(?P<d>\d{4})")
	vsvars = pif.dbh.fetch_variations_by_vs_category(cat_id)
	vsvars = [x for x in vsvars if x.get('vs.ref_id')] + [x for x in vsvars if not x.get('vs.ref_id')]
	for ent in vsvars:
	    date_m = date_re.search(ent['v.date'])
	    if date_m:
		self.dates.add(date_m.group('d'))
	    ent['id']              = ent['vs.id']
	    ent['mod_id']          = ent['v.mod_id']
	    ent['var_id']          = ent['v.var']
	    range_id = ent['mod_id'] + '-' + ent['var_id']
	    ent['displayed_id']    = range_id
	    ent['section_id']      = mat['id']
	    ent['display_order']   = 0
	    ent['page_id']         = 'matrix'
	    ent['flags']           = 0
	    ent['shown_id']        = ''
	    ent['name']            = ent['base_id.rawname'].replace(';', ' ')
	    ent['subname']         = ''
	    ent['subnames']        = []
	    ent['sub_id']          = ''
	    ent['model_type']      = ent['base_id.model_type']
	    ent.setdefault('pack.page_id', '')
	    ent['description']     = []
	    if ent.get('sub_id') and ent.get('vs.sec_id') and ent['sub_id'] != ent['vs.sec_id']:
		continue
	    if ent.get('v.text_description'):
		ent['description'].append(ent['v.text_description'])
	    ent['description'] = filter(None, ent['description'])
	    ent['disp_id'] = ''
	    ent['image'] = ''
	    ent['link'] = ''
	    ent['pdir']         = mat['pic_dir']
	    ent['disp_format'] = mat['disp_format']
	    if not ent['pdir']:
		ent['pdir'] = pif.render.pic_dir
	    if ent['model_type'] == 'MP':
		ent['image'] = \
			pif.render.format_image_required(ent['mod_id'], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_MAN, nopad=True)
	    elif ent.get('v.picture_id'):
		ent['image'] = \
			pif.render.format_image_required(ent['mod_id'] + '-' + ent['v.picture_id'], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_VAR, nopad=True)
	    elif ent.get('v.var'):
		ent['image'] = \
			pif.render.format_image_required(ent['mod_id'] + '-' + ent['v.var'], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_VAR, nopad=True)
	    ent['range_id']        = range_id
	    mat['ents'].setdefault(ent['range_id'], list())
	    mat['ents'][ent['range_id']].append(ent)
	    pif.render.comment('        entry:', ent)

	for ent in pif.dbh.fetch_variations_by_category(cat_id):
	    ent['var_id']          = ent['var']
	    range_id = ent['mod_id'] + '-' + ent['var_id']
	    if range_id in mat['ents'] or cat_id not in ent['category'].split(' '):
		continue
	    ent.setdefault('vs.ref_id', '')
	    ent.setdefault('vs.sec_id', '')
	    ent.setdefault('vs.ran_id', '')
	    date_m = date_re.search(ent['date'])
	    if date_m:
		self.dates.add(date_m.group('d'))
	    ent['displayed_id']    = range_id
	    ent['id']              = ''
	    ent['section_id']      = mat['id']
	    ent['display_order']   = 0
	    ent['page_id']         = 'matrix'
	    ent['flags']           = 0
	    ent['shown_id']        = ''
	    ent['name']            = ent['base_id.rawname'].replace(';', ' ')
	    ent['subname']         = ''
	    ent['subnames']        = []
	    ent['sub_id']          = ''
	    ent['model_type']      = ent['base_id.model_type']
	    ent.setdefault('pack.page_id', '')
	    ent['description']     = []
	    if ent.get('sub_id') and ent.get('vs.sec_id') and ent['sub_id'] != ent['vs.sec_id']:
		continue
	    if ent.get('text_description'):
		ent['description'].append(ent['text_description'])
	    ent['description'] = filter(None, ent['description'])
	    ent['disp_id'] = ''
	    ent['image'] = ''
	    ent['link'] = ''
	    ent['pdir']         = mat['pic_dir']
	    ent['disp_format'] = mat['disp_format']
	    if not ent['pdir']:
		ent['pdir'] = pif.render.pic_dir
	    if ent['model_type'] == 'MP':
		ent['image'] = \
			pif.render.format_image_required(ent['mod_id'], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_MAN, nopad=True)
	    elif ent.get('picture_id'):
		ent['image'] = \
			pif.render.format_image_required(ent['mod_id'] + '-' + ent['picture_id'], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_VAR, nopad=True)
	    elif ent.get('var'):
		ent['image'] = \
			pif.render.format_image_required(ent['mod_id'] + '-' + ent['var'], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_VAR, nopad=True)
	    ent['range_id']        = range_id
	    mat['ents'].setdefault(ent['range_id'], list())
	    mat['ents'][ent['range_id']].append(ent)
	    pif.render.comment('        entry:', ent)
	disp_order = 1
	for range_id in sorted(mat['ents']):
	    mat['ents'][range_id][0]['display_order'] = disp_order
	    disp_order += 1
	self.tables.append(mat)

    def matrix(self, pif):
        llineup = {'id': pif.page_name, 'section': [], 'note': '\n'.join(self.text), 'columns': 4, 'tail': ''}
        comments = set()

        for table in self.tables:
            section_name = table['name']
            if not (table['flags'] & pif.dbh.FLAG_SECTION_HIDE_IMAGE) and (table['id'] not in pif.page_id.split('.')):
                img = pif.render.format_image_optional(table['id'], pdir=table['pic_dir'], nopad=True)
                if img:
                    section_name += '<br>' + img
            section = {'id': table['id'], 'name': section_name, 'range': [], 'anchor': table['id'], 'columns': table['columns'], 'anchor': table['id']}
            if pif.is_allowed('a'):  # pragma: no cover
		if section['id'] == 'cat':
		    dates = sorted(self.dates)
		    if len(self.dates) == 1:
			section['name'] += " %s" % dates[0]
		    elif len(self.dates) > 1:
			section['name'] += " %s-%s" % (dates[0], dates[-1])
		else:
		    section['name'] += " (%s/%s)" % (pif.page_id, section['id'])
		    section['name'] += ' ' + pif.render.format_button("add", "editor.cgi?table=matrix_model&page_id=%s&section_id=%s&add=1" % (pif.page_id, section['id']))

                if pif.form.has('large'):
                    section['columns'] = 1
            ran = {'entry': []}
            range_ids = table['ents'].keys()
            range_ids.sort(key=lambda x: table['ents'][x][0]['display_order'])
            for range_id in range_ids:
		if section['id'] == 'cat':
		    ran['entry'].append(self.add_cell(pif, table['ents'][range_id], table, comments))
                else:
                    mods = self.find_matrix_variations(table['ents'][range_id], pif.page_id, table['id'], str(range_id))
		    if mods:
			ran['entry'].append(self.add_cell(pif, mods, table, comments))
            section['range'].append(ran)
            llineup['section'].append(section)
        #llineup['tail'] = [pif.render.format_image_art('bamca_sm'), '']
	pif.render.set_button_comment(pif, '')
	llineup['tail'] = ['', '<br>'.join([mbdata.comment_designation[comment] for comment in comments])]
        return llineup

    def find_matrix_variations(self, ents, page_id, sec_id, ran_id):
	if sec_id and ran_id:
            mods = [x for x in ents if x['vs.sec_id'] == sec_id and x['vs.ran_id'] == ran_id]
            if mods:
                return mods
	if sec_id:
            mods = [x for x in ents if x['vs.sec_id'] == sec_id]
            if mods:
                return mods
	mods = [x for x in ents if x['vs.sec_id'] == '']
	return mods

    def add_cell(self, pif, ents, table, comments):
        entd = {}
        for ent in ents:
            entd.setdefault(ent['mod_id'], [])
            entd[ent['mod_id']].append(ent)

        pif.render.comment('add_cell', entd)

        varimage = ''
        for mod in entd:
            ent = entd[mod][0]

            for ent2 in entd[mod][1:]:
                if ent['flags'] & tables.FLAG_MODEL_SHOW_ALL_VARIATIONS:
                    ent['image'] += ent2['image']
                elif not ent['image']:
                    ent['image'] = ent2['image']
                for desc in ent2['description']:
                    if desc not in ent['description']:
                        ent['description'].append(desc)
            if ent['image']:
                varimage = ent['image']

        if ent['flags'] & tables.FLAG_MODEL_NO_VARIATION:
            ent['picture_only'] = 1
        elif not ent['mod_id']:
            comments.add('m')
            ent['no_casting'] = 1
            ent['picture_only'] = 1
        else:
            if not ent.get('vs.var_id') and not ent.get('var_id'):
                comments.add('v')
                ent['no_variation'] = 1
            if not varimage:
                comments.add('i')
                ent['no_specific_image'] = 1
	if pif.is_allowed('a') and not ent.get('vs.ref_id'):
	    ent['no_vs'] = 1
        ent['imgstr'] = varimage

        ent['number'] = ent['disp_id']
        if not ent['shown_id'] and ent['disp_id']:
            ent['shown_id'] = ent['disp_id']
        if ent['flags'] & pif.dbh.FLAG_MODEL_NO_ID:
            ent['shown_id'] = ''

        ent['product'] = [ent['link']]
        prodpic = pif.render.find_image_path(ent['product'], suffix='jpg', pdir=ent['pdir']) or \
		pif.render.find_image_path(ent['product'], suffix='jpg', largest='l', pdir=ent['pdir'])
        if prodpic:
            comments.add('c')
            ent['is_product_picture'] = 1
            if pif.is_allowed('a') and pif.form.has('large'):  # pragma: no cover
		ent['prodpic'] = prodpic
        if ent['flags'] & tables.FLAG_MODEL_NOT_MADE:
            comments.add('n')
            ent['not_made'] = 1
            ent['picture_only'] = 1

        ent['href'] = ''
	if ent['model_type'] == 'MP':
            ent['href'] = "packs.cgi?page=%(pack.page_id)s&id=%(mod_id)s" % ent
        elif not ent['mod_id']:
            img = pif.render.find_image_path(ent['link'], largest='h')
            if img:
                ent['href'] = '/' + img
        elif ent['vs.ref_id']:
            ent['href'] = "single.cgi?dir=%(pdir)s&pic=%(link)s&ref=%(vs.ref_id)s&sec=%(vs.sec_id)s&ran=%(vs.ran_id)s&id=%(mod_id)s" % ent
        elif ent.get('var_id'):
            ent['href'] = "vars.cgi?mod=%(mod_id)s&var=%(var_id)s" % ent
	else:
            ent['href'] = "single.cgi?dir=%(pdir)s&pic=%(link)s&id=%(mod_id)s" % ent
        vstr = ''
        ent['descriptions'] = filter(None, ent['description'])
        if ent['descriptions'] and (not ent['flags'] & tables.FLAG_MODEL_NO_VARIATION):
            pass
        elif ent.get('matrix_model.description', ''):
            ent['descriptions'] = ent['matrix_model.description'].split(';')

        ent['anchor'] = '%s' % ent['number']

	desclist = list()
	for var in ent.get('descriptions', []):
	    if var and var not in desclist:
		desclist.append(var)
	ent['descriptions'] = desclist

	ent['additional'] = ''
        if pif.is_allowed('a'):  # pragma: no cover
            ent['additional'] += pif.render.format_button("edit", pif.dbh.get_editor_link('matrix_model', {'id': ent['id']}))
	    pic = ent['link']
            ent['additional'] += pif.render.format_button("upload",
		    "upload.cgi?d=%s&n=%s&c=%s&link=%s" % (pif.render.pic_dir.replace('pic', 'lib'), pic, pic, urllib.quote('https://www.bamca.org/cgi-bin/matrix.cgi?page=' + pif.page_id)))

	ent.setdefault('displayed_id', '&nbsp;')
	if ent.get('disp_format'):
	    if ent.get('shown_id'):
		ent['displayed_id'] = ent['disp_format'] % (ent['shown_id'])
	elif ent.get('shown_id'):
	    ent['displayed_id'] = ent['shown_id']

	ent['display_id'] = pif.page_name

        return ent


def select_matrix(pif):
    lran = dict(id='ml', entry=list())
    lran['name'] = "A few of the special sets produced by Matchbox in recent years:"
    ser = pif.dbh.fetch_pages("id like 'matrix.%'", order='description, title')
    for ent in ser:
	ent['page_info.id'] = ent['page_info.id'].split('.', 1)[-1]
	link = '<b><a href="?page=%(page_info.id)s">%(page_info.title)s</a></b> - %(page_info.description)s' % ent
	if not (ent['page_info.flags'] & 1):
	    lran['entry'].append(link)
	elif pif.is_allowed('a'):  # pragma: no cover
	    lran['entry'].append('<i>' + link + '</i>')
    return dict(section=[{'id': 'ml', 'range': [lran]}])


@basics.web_page
def main(pif):
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.print_html()
    matf = MatrixFile(pif)
    if matf.tables:
        llineup = matf.matrix(pif)
	pif.render.format_matrix_for_template(llineup)
	return pif.render.format_template('matrix.html', llineup=llineup)
    return pif.render.format_template('matrixsel.html', llineup=select_matrix(pif))


def select_cats(pif):
    lran = dict(id='ml', entry=list())
    lran['name'] = "Model categories:"
    cats = pif.dbh.fetch_categories()
    for ent in cats:
	link = '<b><a href="?cat=%(id)s">%(name)s</a> (%(id)s)</b>' % ent
	if ent['flags'] & pif.dbh.FLAG_CATEGORY_INDEXED:
	    lran['entry'].append(link)
	elif pif.is_allowed('a'):  # pragma: no cover
	    lran['entry'].append('<i>' + link + '</i>')
    return dict(section=[{'id': 'ml', 'range': [lran]}])


@basics.web_page
def cats_main(pif):
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.print_html()
    matf = MatrixFile(pif)
    if matf.tables:
        llineup = matf.matrix(pif)
	pif.render.format_matrix_for_template(llineup)
	return pif.render.format_template('matrix.html', llineup=llineup)
    return pif.render.format_template('matrixsel.html', llineup=select_cats(pif))
