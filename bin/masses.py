#!/usr/local/bin/python

import os, re, urllib2, urlparse
import basics
import config
import editor
import images
import mbdata
import useful



# ------- mass -----------------------------------------------------


@basics.web_page
def mass(pif):
    pif.render.print_html()
    pif.restrict('am')
    print pif.render.format_head(extra=pif.render.reset_button_js + pif.render.toggle_display_js)
    mass_type = pif.form.get_str('type')
    print mass_type, '<br>'
    #print pif.form, '<hr>'
    dict(mass_mains_list).get(mass_type, mass_mains_hidden.get(mass_type, mass_main))(pif)
    print pif.render.format_tail()


def mass_main(pif):
    if pif.form.has('save'):
	mass_save(pif)
    elif pif.form.has('select'):
	mass_select(pif)
    else:
	mass_ask(pif)


def mass_ask(pif):
    print '<form method="post">'
    print pif.render.format_table_start()

    print pif.render.format_row_start()
    print pif.render.format_cell(0, "select")
    print pif.render.format_cell(1, pif.render.format_text_input("select", 256, 80))
    print pif.render.format_row_end()

    print pif.render.format_row_start()
    print pif.render.format_cell(0, "from")
    print pif.render.format_cell(1, pif.render.format_text_input("from", 256, 80))
    print pif.render.format_row_end()

    print pif.render.format_row_start()
    print pif.render.format_cell(0, "where")
    print pif.render.format_cell(1, pif.render.format_text_input("where", 256, 80))
    print pif.render.format_row_end()

    print pif.render.format_row_start()
    print pif.render.format_cell(0, "order")
    print pif.render.format_cell(1, pif.render.format_text_input("order", 256, 80))
    print pif.render.format_row_end()

    print pif.render.format_table_end()
    print '<input type="hidden" name="verbose" value="1">'
    print pif.render.format_button_input()
    print "</form>"
    mass_sections(pif)


def mass_select(pif):
    # Get table descriptions and use widths.  Allow "*".
    columns = pif.form.get_str('select').split(',')
    table_info = pif.dbh.table_info[pif.form.get_str('from')]
    rows = pif.dbh.fetch(pif.form.get_str('from'), columns=columns + table_info['id'], where=pif.form.get_str('where'), order=pif.form.get_str('order'), tag='mass_select')
    print '<form method="post">'
    print '<input type="hidden" name="from" value="%s">' % pif.form.get_str('from')
    print '<input type="hidden" name="select" value="%s">' % pif.form.get_str('select')
    print '<input type="hidden" name="verbose" value="1">'
    print pif.render.format_table_start()

    print pif.render.format_row_start()
    for col in columns:
        print pif.render.format_cell(0, col)
    print pif.render.format_row_end()

    for row in rows:
        print pif.render.format_row_start()
        for col in columns:
            if col in table_info['id']:
                print pif.render.format_cell(1, row[col])
            else:
                print pif.render.format_cell(1,
                    pif.render.format_text_input(col + "." + '.'.join([str(row[x]) for x in table_info['id']]),
                    256, 40, row[col]))
        print pif.render.format_row_end()

    print pif.render.format_table_end()
    print pif.render.format_button_input("save")
    print "</form>"


def mass_save(pif):
    columns = pif.form.get_str('select').split(',')
    table_info = pif.dbh.table_info[pif.form.get_str('from')]

    for key in pif.form.keys(has='.'):
        col, ids = key.split('.', 1)
        if col in columns:
            wheres = pif.dbh.make_where(dict(zip(table_info['id'], ids.split('.'))))
            # where = " and ".join(["%s='%s'" % x for x in wheres])
            # update table set col=value where condition;
            # query = "update %s set %s='%s' where %s" % (pif.form.get_str('from'), col, pif.dbh.escape_string(pif.form.get_str(key)), where)
            # print query, '<br>'
            # pif.dbh.raw_execute(query, tag='mass_save')
            # note: untested
            # note: write might already escape values
            pif.dbh.write(pif.form.get_str('from'), values={col: pif.dbh.escape_string(pif.form.get_str(key))}, where=wheres, modonly=True, tag='mass_save')


paren_re = re.compile('''\((?P<n>\d*)\)''')
def table_entry_form(pif, tab, dat, div_id=None, note=''):
    if not div_id:
	div_id = tab
    print tab, pif.render.format_button('edit', link=pif.dbh.get_editor_link(tab, 
	pif.dbh.make_id(tab, dat, tab + '.')))
    print pif.render.format_button_input_visibility(div_id), note, '<br>'
    descs = pif.dbh.describe_dict(tab)
    print pif.render.format_table_start(id=div_id)
    for col in pif.dbh.table_info[tab]['columns']:
        print pif.render.format_row_start()
        print pif.render.format_cell(0, col)
        coltype = descs.get(col).get('type')
        print pif.render.format_cell(0, coltype)
        print pif.render.format_cell(1, str(dat.get(tab + '.' + col, '')))
        colwidth = int(paren_re.search(coltype).group('n'))
        print pif.render.format_cell(1, pif.render.format_text_input(tab + '.' + col, colwidth, min(colwidth, 80), value=dat.get(tab + '.' + col, '')))
        print pif.render.format_row_end()
        #sys.stdout.flush()
    print pif.render.format_table_end()

# ------- add lineup -----------------------------------------------

def lineup_desc_main(pif):
    for key in pif.form.keys(start='description.'):
	lid = key[key.find('.') + 1:]
	lm = pif.dbh.depref('lineup_model', pif.dbh.fetch_lineup_model({'id': lid})[0])
	if lm['name'] != pif.form.get_str(key):
	    print lid, pif.form.get_str(key), lm['name']
	    lm['name'] = pif.form.get_str(key)
	    print pif.dbh.update_lineup_model({'id': lid}, lm)
	    print '<br>'

# TODO add base_id/casting_id for new castings
def add_lineup_main(pif):
    if pif.form.has('save'):
        add_lineup_final(pif)
    elif pif.form.has('num'):
        add_lineup_list(pif)
    else:
        print "<form>"
        print "Number of models:"
        print pif.render.format_text_input("num", 8, 8, value='')
        print '<br>Year:'
        print pif.render.format_text_input("year", 4, 4, value='')
        print '<br>Region:'
        print pif.render.format_text_input("region", 4, 4, value='')
        print '<br>Model List:'
        print pif.render.format_text_input("models", 80, 80, value='')
        print pif.render.format_button_input()
        print pif.render.format_hidden_input({'type': 'lineup'})
        print "</form>"


def add_lineup_final(pif):
    pif.dbh.dbi.insert_or_update('page_info',
    {
        'id': pif.form.get_str('page_id'),
        'flags': 0,
        'health': '',
        'format_type': '',
        'title': '',
        'pic_dir': pif.form.get_str('picdir'),
        'tail': '',
        'description': '',
        'note': '',
    })
    pif.dbh.dbi.insert_or_update('section',
    {
        'id': pif.form.get_str('region'),
        'page_id': pif.form.get_str('page_id'),
        'display_order': 0,
        'category': 'man',
        'flags': 0,
        'name': pif.form.get_str('sec_title'),
        'columns': pif.form.get_int('cols', 4),
        'start': 0,
        'pic_dir': '',
        'disp_format': '%d.',
        'link_format': pif.form.get_str('link_fmt'),
        'img_format': '',
        'note': '',
    })

    for key in pif.form.keys(start='mod_id.'):
        num = key[7:]
        pif.dbh.dbi.insert_or_update('lineup_model',
        {
            'mod_id': pif.form.get_str(key),
            'number': num,
            'style_id': pif.form.get_str('style_id.' + num),
            'picture_id': '',
            'region': pif.form.get_str('region'),
            'year': pif.form.get_str('year'),
            'page_id': pif.form.get_str('page_id'),
            'name': pif.form.get_str('name.' + num),
        })


def add_lineup_list(pif):
    modlist = urllib2.urlopen(pif.form.get_str('models')).read().split('\n')
    castings = {x['base_id.rawname'].replace(';', ' '): x['base_id.id'] for x in pif.dbh.fetch_casting_list()}
    num_models = pif.form.get_int('num')
    year = pif.form.get_str('year')
    region = pif.form.get_str('region')
    print '<form method="post" action="mass.cgi">'

    print pif.render.format_table_start()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'Page and Section', hdr=True, also={'colspan': 2})
    print pif.render.format_row_end()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'Page ID')
    print pif.render.format_cell(0, pif.render.format_text_input("page_id", 20, 20, value='year.%s' % year))
    print pif.render.format_row_end()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'Picture Directory')
    print pif.render.format_cell(0, pif.render.format_text_input("picdir", 80, 80, value=''))
    print pif.render.format_row_end()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'Section Title')
    print pif.render.format_cell(0, pif.render.format_text_input("sec_title", 80, 80, value='Matchbox %s %s Lineup' % (year, mbdata.regions[region])))
    print pif.render.format_row_end()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'Link Format')
    print pif.render.format_cell(0, pif.render.format_text_input("link_fmt", 20, 20, value='%s%s%%03d' % (year[2:], region.lower())))
    print pif.render.format_row_end()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'Columns')
    print pif.render.format_cell(0, pif.render.format_text_input("cols", 1, 1, value=''))
    print pif.render.format_row_end()
    print pif.render.format_table_end()

    print pif.render.format_table_start()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'Models', hdr=True, also={'colspan': 4})
    print pif.render.format_row_end()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'Number')
    print pif.render.format_cell(0, 'Model ID')
    print pif.render.format_cell(0, 'Style ID')
    print pif.render.format_cell(0, 'Name')
    print pif.render.format_row_end()
    for cnt in range(0, num_models):
        print pif.render.format_row_start()
        print pif.render.format_cell(0, "%s" % (cnt + 1))
        name = modlist.pop(0)
        print pif.render.format_cell(0, pif.render.format_text_input("mod_id.%d" % (cnt + 1), 12, 12, value=castings.get(name, '')))
        print pif.render.format_cell(0, pif.render.format_text_input("style_id.%d" % (cnt + 1), 3, 3, value='0'))
        print pif.render.format_cell(0, pif.render.format_text_input("name.%d" % (cnt + 1), 64, 64, value=name))
        print pif.render.format_row_end()
    print pif.render.format_table_end()

    print pif.render.format_button_input('save')
    print pif.render.format_hidden_input({'type': 'lineup', 'num': num_models})
    print pif.render.format_hidden_input({"year": year})
    print pif.render.format_hidden_input({"region": region})
    print "</form>"


# ------- add casting ---------------------------------------------


def add_casting_main(pif):
    if pif.form.has('save'):
        add_casting_final(pif)
    print "<form>"
    print "ID:"
    print pif.render.format_text_input("id", 8, 8, value='')
    print '<br>Year:'
    print pif.render.format_text_input("year", 4, 4, value=pif.form.get_str('year'))
    print '<br>Model Type:'
    print pif.render.format_select('model_type', [x['model_type'] for x in pif.dbh.fetch_base_id_model_types()], selected='SF')
    print '<br>Name:'
    print pif.render.format_text_input("rawname", 80, 80, value='')
    print '<br>Description:'
    print pif.render.format_text_input("description", 80, 80, value='')
    print '<br>Made:' # flags = pif.dbh.FLAG_MODEL_NOT_MADE
    print pif.render.format_checkbox('notmade', [('not', 'not')])
    print '<br>Country:'
    print pif.render.format_select_country('country')
    print '<br>Make:'
    print pif.render.format_select('make', [('', ''), ('unl', 'MBX')] + [(x['vehicle_make.make'], x['vehicle_make.make_name']) for x in pif.dbh.fetch_vehicle_makes()])
    print '<br>Section:'
    print pif.render.format_select('section_id', [(x['section.id'], x['section.name']) for x in pif.dbh.fetch_sections(where="page_id like 'man%'")], selected=pif.form.get_str('section_id'))

    print pif.render.format_button_input('save')
    print pif.render.format_hidden_input({'type': 'casting'})
    print "</form>"


def add_casting_final(pif):
    print pif.form.get_form(), '<br>'
    if pif.dbh.fetch_base_id(pif.form.get_str('id')):
	raise useful.SimpleError("That ID is already in use.")
# base_id: id, first_year, model_type, rawname, description, flags
# casting: id, country, make, section_id
    print pif.dbh.add_new_base_id({
	'id': pif.form.get_str('id'),
	'first_year': pif.form.get_str('year'),
	'model_type': pif.form.get_str('model_type'),
	'rawname': pif.form.get_str('rawname'),
	'description': pif.form.get_str('description'),
	'flags': pif.dbh.FLAG_MODEL_NOT_MADE if pif.form.get_str('notmade') == 'not' else 0,
    })
    print pif.dbh.add_new_casting({
	'id': pif.form.get_str('id'),
	'country': pif.form.get_str('country'),
	'make': pif.form.get_str('make'),
	'section_id': pif.form.get_str('section_id'),
	'notes': '',
    })
    print '<br>'


# ------- add pub -------------------------------------------------


def add_pub_main(pif):
    if pif.form.has('save'):
        add_pub_final(pif)
    print "<form>"
    print "ID:"
    print pif.render.format_text_input("id", 8, 8, value='')
    print '<br>Year:'
    print pif.render.format_text_input("year", 4, 4, value=pif.form.get_str('year'))
    print '<br>Model Type:'
    #pif.dbh.fetch_base_id_model_types()
    print pif.render.format_select('model_type', sorted(mbdata.model_type_names.items()), selected='BK')
    print '<br>Name:'
    print pif.render.format_text_input("rawname", 80, 80, value='')
    print '<br>Description:'
    print pif.render.format_text_input("description", 80, 80, value='')
    print '<br>Made:' # flags = pif.dbh.FLAG_MODEL_NOT_MADE
    print pif.render.format_checkbox('notmade', [('not', 'not')])
    print '<br>Country:'
    print pif.render.format_select_country('country')
#    print '<br>Section:'
#    print pif.render.format_select('section_id', [(x['section.id'], x['section.name']) for x in pif.dbh.fetch_sections(where="page_id like 'man%'")], selected=pif.form.get_str('section_id'))

    print pif.render.format_button_input('save')
    print pif.render.format_hidden_input({'type': 'pub'})
    print "</form>"


def add_pub_final(pif):
    print pif.form.get_form(), '<br>'
    if pif.dbh.fetch_base_id(pif.form.get_str('id')):
	raise useful.SimpleError("That ID is already in use.")
# base_id: id, first_year, model_type, rawname, description, flags
# publication: id, country, section_id
    print pif.dbh.add_new_base_id({
	'id': pif.form.get_str('id'),
	'first_year': pif.form.get_str('year'),
	'model_type': pif.form.get_str('model_type'),
	'rawname': pif.form.get_str('rawname'),
	'description': pif.form.get_str('description'),
	'flags': pif.dbh.FLAG_MODEL_NOT_MADE if pif.form.get_str('notmade') == 'not' else 0,
    })
    print pif.dbh.add_new_publication({
	'id': pif.form.get_str('id'),
	'country': pif.form.get_str('country'),
	'section_id': pif.form.get_str('model_type').lower(),
    })
    print '<br>'


# ------- add var -------------------------------------------------


def add_var_main(pif):
    #print pif.form.get_form(), '<hr>'

    if pif.form.get_bool('save'):
	add_var_final(pif)
	#add_var_ask(pif)
    elif pif.form.get_str('mod_id'):
	add_var_info(pif)
    else:
	add_var_ask(pif)
	print pif.render.format_button('catalog', '/lib/mbusa/', lalso={'target': '_blank'})


def add_var_ask(pif):
    print "<form>"
    print "Man ID:", pif.render.format_text_input("mod_id", 8, 8, value=pif.form.get_str('mod_id')), '<br>'
    print 'Var ID:', pif.render.format_text_input("var", 8, 8, value=''), '<br>'
    print 'Date:', pif.render.format_text_input("date", 8, 8, value=''), '<br>'
    print 'Imported From:', pif.render.format_text_input("imported_from", 8, 8, value=''), '<br>'
    print pif.render.format_button_input('submit')
    print pif.render.format_hidden_input({'type': 'var'})
    print "</form>"


var_id_columns = ['mod_id', 'var']
var_attr_columns = ['body', 'base', 'windows', 'interior']
var_data_columns = ['category', 'area', 'date', 'note', 'manufacture', 'imported_from', 'imported_var']
var_record_columns = var_id_columns + var_attr_columns + var_data_columns
def add_var_info(pif):
    mod_id = pif.form.get_str('mod_id')
    mod = pif.dbh.fetch_casting(mod_id)
    var_id = mbdata.normalize_var_id(mod, pif.form.get_str('var'))
    attrs = pif.dbh.fetch_attributes(mod_id)
    attr_names = [x['attribute.attribute_name'] for x in attrs]
    var = pif.dbh.fetch_variation(mod_id, var_id)
    if not mod:
	raise useful.SimpleError("Model not found.")
    print '<h3>', mod['name'], '</h3>'
    print '<form>'
    if var:
	print pif.render.format_hidden_input({'store': 'update'})
	var = pif.dbh.depref('variation', var[0])
    else:
	print pif.render.format_hidden_input({'store': 'insert'})
	var = {}
    print '<table class="tb">'
    defs = {'mod_id': mod_id,
	    'var': var_id,
	    'flags': 0,
	    'manufacture': 'Thailand',
	    'imported_from': pif.form.get_str('imported_from'),
	    'imported_var': var_id,
	    'date': pif.form.get_str('date')
    }
    for col in var_id_columns + [None] + var_attr_columns + attr_names + [None] + var_data_columns:
	if col:
	    val = var.get(col) if var.get(col) else defs.get(col, '')
	    print '<tr><td class="eb">%s</td>' % col
	    if var:
		print '<td class="eb">%s</td>' % val
	    print '<td class="eb">%s</td></tr>' % (
		pif.render.format_select(col, [('', '')] + sorted(mbdata.categories.items()), val) if col == 'category' else
		pif.render.format_text_input(col, 64, 32, value=val))
	else:
	    print '<tr><td class="eb" colspan="%s"></td></tr>' % (3 if var else 2)
    print "</table>"
    print pif.render.format_button_input('save')
    print pif.render.format_hidden_input({'type': 'var'})
    print pif.render.format_link('/cgi-bin/single.cgi?id=' + mod_id, mod_id)
    print "</form>"

    for var in pif.dbh.fetch_variations(mod_id):
	lnk = '/cgi-bin/vars.cgi?edit=1&mod=%(variation.mod_id)s&var=%(variation.var)s' % var
	print var['variation.var'], ':', pif.render.format_link(lnk, var['variation.text_description']), '<br>'


def add_var_final(pif):
    mod_id = pif.form.get_str('mod_id')
    var_id = pif.form.get_str('var')
    attrs = pif.dbh.fetch_attributes(mod_id)
    attr_names = [x['attribute.attribute_name'] for x in attrs]
    upd = False
    if pif.form.get_str('store') == 'update':
	var = pif.dbh.depref('variation', pif.dbh.fetch_variation(mod_id, var_id))
	if var:
	    var = var[0]
	    upd = True
	else:
	    var = {}
    else:
	var = {}
    for col in var_record_columns + attr_names:
	var[col] = pif.form.get_str(col)
    print var, '<br>'
    if upd:
	pif.dbh.update_variation(var, {'mod_id': mod_id, 'var': var_id}, verbose=True)
    else:
	pif.dbh.insert_variation(mod_id, var_id, var, verbose=True)
    pif.dbh.recalc_description(mod_id, showtexts=False, verbose=False)
    raise useful.Redirect('/cgi-bin/vars.cgi?edit=1&mod=%s&var=%s' % (mod_id, var_id))


# ------- casting_related ------------------------------------------


def edit_casting_related(pif):
    mod_id = pif.form.get_str('mod_id')
    # 'columns': ['id', 'model_id', 'related_id', 'description'],
    if pif.form.has('add'):
	pif.dbh.add_casting_related({'model_id': mod_id, 'related_id': pif.form.get_str('r')})
	pif.dbh.add_casting_related({'model_id': pif.form.get_str('r'), 'related_id': mod_id})
    if pif.form.has('save'):
	crd = {}
	for key in pif.form.keys(start='m.'):
	    key = key[2:]
	    crd[key] = dict()
	    crd[key]['m'] = pif.form.get_str('m.' + key)
	    crd[key]['r'] = pif.form.get_str('r.' + key)
	    crd[key]['im'] = pif.form.get_str('im.' + key)
	    crd[key]['ir'] = pif.form.get_str('ir.' + key)
	    crd[key]['dm'] = pif.form.get_str('dm.' + key)
	    crd[key]['dr'] = pif.form.get_str('dr.' + key)
	for key in crd:
	    cr = crd[key]
	    print key, cr, '<br>'
	    #print '+', pif.dbh.fetch_casting_related(crd[key]['m'], crd[key]['r']), '<br>'
	    #print '+', pif.dbh.fetch_casting_related(crd[key]['r'], crd[key]['m']), '<br>'
	    if cr['dm']:
		print {'id': cr['im'], 'model_id': cr['m'], 'related_id': cr['r'], 'description': cr['dm']}, '<br>'
		pif.dbh.update_casting_related({'id': cr['im'], 'model_id': cr['m'], 'related_id': cr['r'], 'description': cr['dm']})
	    if cr['dr']:
		print {'id': cr['ir'], 'model_id': cr['r'], 'related_id': cr['m'], 'description': cr['dr']}, '<br>'
		pif.dbh.update_casting_related({'id': cr['ir'], 'model_id': cr['r'], 'related_id': cr['m'], 'description': cr['dr']})
    else:
	crl = pif.dbh.fetch_casting_relateds()
	crd_m = {}
	crd_r = {}
	for cr in crl:
	    if mod_id in (None, cr['casting_related.model_id'], cr['casting_related.related_id']):
		if mod_id or cr['m.model_type'] in ('SF', 'RW') or cr['r.model_type'] in ('SF', 'RW'):
		    m_id = cr['casting_related.model_id']
		    r_id = cr['casting_related.related_id']
		    if m_id < r_id:
			crd_m[(m_id, r_id)] = cr
			crd_r.setdefault((m_id, r_id), {})
		    else:
			crd_m.setdefault((r_id, m_id), {})
			crd_r[(r_id, m_id)] = cr
	#print crd_m, '<br>'
	#print crd_r, '<hr>'
#	for cr in crd_m:
#	    print cr, crd_m[cr], '<br>'
#	    print '...', crd_r[cr], '<br>'
	print '<form method="post"><table border=1>'
	cnt = 0
	for cr in crd_m:
	    cnt += 1
	    print '<tr>'
	    print '<td><a href="%s">%s</a></td>' % (pif.dbh.get_editor_link('casting_related', {'id': crd_m[cr].get('casting_related.id', '')}), crd_m[cr].get('casting_related.id', ''))
	    print '<td><a href="single.cgi?id=%s">%s</a><input type="hidden" name="m.%s" value="%s"></td>' % (cr[0], cr[0], cnt, cr[0])
	    print '<td>', crd_m[cr].get('m.rawname', ''), '</td>'
	    print '<input type="hidden" name="im.%s" value="%s">' % (cnt, crd_m[cr].get('casting_related.id', ''))
	    #print '<td>', crd_r[cr].get('casting_related.id', '') if cr in crd_r else '', '</td>'
	    if cr in crd_r:
		print '<td><a href="%s">%s</a></td>' % (pif.dbh.get_editor_link('casting_related', {'id': crd_r[cr].get('casting_related.id', '')}), crd_r[cr].get('casting_related.id', ''))
	    else:
		print '<td></td>'
	    print '<td><a href="single.cgi?id=%s">%s</a><input type="hidden" name="r.%s" value="%s"></td>' % (cr[1], cr[1], cnt, cr[1])
	    print '<td>', crd_m[cr].get('r.rawname', ''), '' if cr in crd_r else '(missing)', '</td>'
	    if cr in crd_r:
		print '<input type="hidden" name="ir.%s" value="%s">' % (cnt, crd_r[cr].get('casting_related.id', ''))
	    print '<td>', crd_m[cr].get('casting_related.section_id', ''), '</td>'
	    print '</tr><tr>'
	    print '<td colspan=3>%s</td>' % crd_m[cr].get('m.description', '')
	    print '<td colspan=3>%s</td>' % crd_m[cr].get('r.description', '')
	    print '<td></td>'
	    print '</tr><tr>'
	    rd = crd_r[cr].get('casting_related.description', '') if cr in crd_r else ''
	    print '<td colspan=3><input type="text" name="dr.%s" value="%s"></td>' % (cnt, rd)
	    print '<td colspan=3><input type="text" name="dm.%s" value="%s"></td>' % (cnt, crd_m[cr].get('casting_related.description', ''))
	    print '</tr>'
	print '</table>'
	print pif.render.format_button_input('save')
	print '</form>'
    uri = 'mass.cgi?type=related'
    if mod_id:
	uri += '&mod_id=' + mod_id
    if pif.form.has('mod_id'):
	print '<form>'
	print pif.render.format_hidden_input({'mod_id': pif.form.get_str('mod_id'), 'type': 'related'})
	print pif.render.format_text_input('r', 12)
	print pif.render.format_button_input('add')
	print '</form>'

# ------- packs ----------------------------------------------------

# should be able to either edit an existing or create a new pack here
def add_pack(pif):
    print '<hr>'
    print '<form>'
    print '<input type="hidden" name="verbose" value="1">'
    print '<input type="hidden" name="type" value="pack">'
    if pif.form.has('save'):
	add_pack_save(pif)
    elif pif.form.has('delete'):
	add_pack_delete(pif)
	add_pack_ask(pif)
    elif pif.form.get_str('pack'):
	add_pack_form(pif)
    else:
	add_pack_ask(pif)
    print '</form>'


def add_pack_ask(pif):
    # make into select
    pid = pif.form.get_str('id')
    if '.' in pid:
	pid = pid[pid.find('.') + 1:]
    print "Section ID:", pif.render.format_text_input("section_id", 12, 12, value=pid), '<br>'
    print "Pack ID:", pif.render.format_text_input("pack", 12, 12), '<br>'
    print 'Numer of Models:', pif.render.format_text_input("num", 8, 8, value=''), '<br>'
    print pif.render.format_button_input('submit')


pack_sec = {
    '5packs' : 'X.63',
    'lic5packs' : 'X.64',
    'launcher' : 'X.66',
    '10packs' : 'X.65',
    'rwgs' : 'X.62',
    'sfgs' : 'X.62',
    'rwps' : 'X.61',
}
def add_pack_form(pif):
    pack_id = pif.form.get_str('pack')

    section_id = pif.form.get_str('section_id')
    if section_id not in pack_sec:
	raise useful.SimpleError('Unrecognized section id.')
    year = pack_id[:4]
    if not year.isdigit():
	year = '0000'
    pack = pif.dbh.fetch_pack(id=pack_id)
    if pack:
	pack = pack[0]
	for f in pif.dbh.table_info['pack']['id']:
	    print '<input type="hidden" name="o_%s" value="%s">' % (f, pack.get('pack.' + f, ''))
    else:
	pack = {
	    'base_id.id': pack_id,
	    'base_id.first_year': year,
	    'base_id.model_type': 'MP',
	    'base_id.rawname': '',
	    'base_id.description': '',
	    'base_id.flags': 0,
	    'pack.id': pack_id,
	    'pack.page_id': 'packs.' + section_id,
	    'pack.section_id': section_id,
	    'pack.region': 'W',
	    'pack.layout': '5v',
	    'pack.product_code': '',
	    'pack.material': 'C',
	    'pack.country': 'TH',
	    'pack.note': '',
	}

    print pif.render.format_button("edit", "imawidget.cgi?d=%s&f=%s.jpg" % (config.IMG_DIR_PACK, pack_id))
    print pif.render.format_button("upload", "upload.cgi?d=%s&n=%s" % (config.IMG_DIR_PACK, pack_id))
    print '%(pack.page_id)s/%(pack.id)s<br>' % pack
    pack_img = pif.render.find_image_file(pack_id, pdir=config.IMG_DIR_PACK, largest='g')
    print pack_img, '<br>'
    print '<a href="imawidget.cgi?d=./%s&f=%s">%s</a>' % (pack_img + (pif.render.format_image_required(pack_id, pdir=config.IMG_DIR_PACK, largest='g'),))
    print '<a href="imawidget.cgi?d=./%s&f=%s.jpg">%s</a><br>' % (config.IMG_DIR_MAN, 's_' + pack_id, pif.render.format_image_required('s_' + pack_id, pdir=config.IMG_DIR_MAN))
    #print pif.render.format_image_required(pack_id, pdir=config.IMG_DIR_PACK), '<br>'

    pack_num = int(pack['pack.note'][2:-1]) if pack['pack.note'].startswith('(#') else 0
    linmod = pif.dbh.fetch_lineup_model(where="mod_id='%s'" % pack_id)
    linmod = linmod[0] if linmod else {
	'lineup_model.id': 0, # delete later
	'lineup_model.base_id': '%s%s%02d' % (year, pack_sec[section_id].replace('.', ''), pack_num),
	'lineup_model.mod_id': pack_id,
	'lineup_model.number': pack_num,
	'lineup_model.flags': 0,
	'lineup_model.style_id': '',
	'lineup_model.picture_id': '',
	'lineup_model.region': pack_sec[section_id],
	'lineup_model.year': year,
	'lineup_model.name': pack['base_id.rawname'],
	'lineup_model.page_id': 'year.' + year,
    }
    x_linmods = [x['lineup_model.base_id'][7:] for x in pif.dbh.fetch_lineup_models(year, pack_sec[section_id])
		    if x.get('lineup_model.region') == pack_sec[section_id]]
    x_linmods.sort()
    table_entry_form(pif, 'base_id', pack)
    table_entry_form(pif, 'pack', pack)
    print 'in use:', ', '.join(x_linmods), '<br>'
    table_entry_form(pif, 'lineup_model', linmod,
	note=pif.render.format_checkbox('nope', [('1', 'nope')], ['1'] if not linmod['lineup_model.id'] else []))

    # editor
    add_pack_model(pif, pack)

    # related
    relateds = pif.dbh.fetch_packs_related(pack_id)
    print 'related'
    print pif.render.format_button('edit', link='?type=related&mod_id=%s' % pack_id)
    print '<br>'
    for rel in relateds:
	print rel['pack.id'], '<br>'

    print pif.render.format_button_input("save")
    print pif.render.format_button_input("delete")


def add_pack_model(pif, pack):
    print 'pack_model<br>'
    print pif.render.format_table_start()
    pmodels = {x + 1: {'pack_model.display_order': x + 1} for x in range(pif.form.get_int('num'))}
    if pack.get('base_id.id'):
	model_list = pif.dbh.fetch_pack_models(pack_id=pack['pack.id'], page_id='packs.' + pif.form.get_str('section_id'))

	for mod in pif.dbh.modify_man_items([x for x in model_list if x['pack.id'] == pack['base_id.id']]):
	    sub_ids = [None, '', pack['base_id.id'], pack['base_id.id'] + '.' + str(mod['pack_model.display_order'])]
	    if mod['vs.sub_id'] in sub_ids:
		mod['vars'] = []
		if not pmodels.get(mod['pack_model.display_order'], {}).get('pack_model.mod_id'):
		    pmodels[mod['pack_model.display_order']] = mod
		if mod.get('vs.var_id'):
		    pmodels[mod['pack_model.display_order']]['vars'].append(mod['vs.var_id'])

    keys = pmodels.keys()
    keys.sort()
    for mod in keys:
	print pif.render.format_row_start()
	print '<input type="hidden" name="pm.id.%s" value="%s">\n' % (mod, pmodels[mod].get('pack_model.id', '0'))
	print '<input type="hidden" name="pm.pack_id.%s" value="%s">\n' % (mod, pmodels[mod].get('pack_model.pack_id', ''))
	print pif.render.format_cell(0, pif.render.format_link("single.cgi?id=%s" % pmodels[mod].get('pack_model.mod_id', ''), 'mod')
	    + ' ' + pif.render.format_text_input("pm.mod_id.%s" % mod, 8, 8, value=pmodels[mod].get('pack_model.mod_id', '')))
	print pif.render.format_cell(0, 'var ' + pif.render.format_text_input("pm.var_id.%s" % mod, 20, 20, value='/'.join(list(set(pmodels[mod].get('vars', ''))))) + ' (' + str(pmodels[mod].get('pack_model.var_id', '')) + ')')
	print pif.render.format_cell(0, 'disp ' + pif.render.format_text_input("pm.display_order.%s" % mod, 2, 2, value=pmodels[mod].get('pack_model.display_order', '')))
	print pif.render.format_cell(0, pif.render.format_button('edit', link=pif.dbh.get_editor_link('pack_model', 
	    pif.dbh.make_id('pack_model', pmodels[mod], 'pack_model' + '.'))))
	print pif.render.format_row_end()
    print pif.render.format_table_end()


def add_pack_delete(pif):
    print 'delete base_id', pif.form.get_str('base_id.id'), '<br>'
    pif.dbh.delete_base_id({'id': pif.form.get_str('base_id.id')})
    print 'delete pack', pif.form.get_str('pack.id'), '<br>'
    pif.dbh.delete_pack(pif.form.get_str('pack.id'))
    pif.dbh.delete_pack_models(pif.form.get_str('pack.page_id'), pif.form.get_str('pack.id'))
    print 'delete lineup_model', pif.form.get_str('lineup_model.id'), '<br>'
    pif.dbh.delete_lineup_model({'id': pif.form.get_int('lineup_model.id')})


def get_correct_model_id(pif, mod_id):
    alias = pif.dbh.fetch_alias(mod_id)
    return alias.get('base_id.id', mod_id)


def add_pack_save(pif):
    print pif.form.get_form(), '<br>'

    pm_table_info = pif.dbh.table_info['pack_model']
    mods = [x[6:] for x in pif.form.keys(start='pm.id.')]
    pms = [
	{
	    'id': pif.form.get_int('pm.id.' + mod),
	    'pack_id': pif.form.get_str('pack.id'),
	    'mod_id': get_correct_model_id(pif, pif.form.get_str('pm.mod_id.' + mod)),
	    'var_id': pif.form.get_str('pm.var_id.' + mod),
	    'display_order': pif.form.get_int('pm.display_order.' + mod),
	}
	for mod in mods]

    if pif.form.has('o_id'):  # update existing records
	pif.dbh.update_pack_models(pms)
	pif.dbh.update_variation_select_pack(pms, pif.form.get_str('pack.page_id'), pif.form.get_str('o_id'))

	p_table_info = pif.dbh.table_info['pack']
	if pif.form.get_str('o_id') != pif.form.get_str('pack.id'):  # change id of pack
	    pif.dbh.update_variation_select_subid(pif.form.get_str('pack.id'), pif.form.get_str('pack.page_id'), pif.form.get_str('o_id'))
	    if os.path.exists(pif.render.pic_dir + '/' + pif.form.get_str('o_id') + '.jpg'):
		os.rename(pif.render.pic_dir + '/' + pif.form.get_str('o_id') + '.jpg', pif.render.pic_dir + '/' + pif.form.get_str('pack.id') + '.jpg')
	pif.dbh.update_pack(pif.form.get_str('o_id'), {x: pif.form.get_str('pack.' + x) for x in p_table_info['columns']})

	p_table_info = pif.dbh.table_info['base_id']
	pif.dbh.update_base_id(pif.form.get_str('o_id'), {x: pif.form.get_str('base_id.' + x) for x in p_table_info['columns']})

    else:  # add new records
	pif.dbh.add_new_pack_models(pms)
	pif.dbh.update_variation_select_pack(pms, pif.form.get_str('pack.page_id'), pif.form.get_str('o_id'))
	pif.dbh.add_new_pack(pif.dbh.make_values('pack', pif.form, 'pack.'))
	pif.dbh.add_new_base_id(pif.dbh.make_values('base_id', pif.form, 'base_id.'))

    # now do lineup_model separately
    if not pif.form.get_int('nope'):
	values = pif.dbh.make_values('lineup_model', pif.form, 'lineup_model.')
	if pif.form.get_int('lineup_model.id'):
	    #print 'update line_model', values, '<br>'
	    pif.dbh.update_lineup_model({'id': pif.form.get_int('lineup_model.id')}, values)
	else:
	    #print 'new line_model', values, '<br>'
	    linmod = pif.dbh.fetch_lineup_model(where="mod_id='%s'" % values['mod_id'])
	    if not linmod:  # goddamn bounciness
		#print 'already<br>'
		del values['id']
		pif.dbh.insert_lineup_model(values)

    print pif.render.format_link("packs.cgi?page=%s&id=%s" % (pif.form.get_str('pack.section_id'), pif.form.get_str('pack.id')), "pack")


# ------- links ----------------------------------------------------

def add_links(pif):
    asslinks = pif.dbh.fetch_link_lines(flags=pif.dbh.FLAG_LINK_LINE_ASSOCIABLE)
    if pif.form.has('save'):
        add_links_final(pif)
    elif pif.form.has('url'):
        add_links_scrape(pif)
    else:
        print "<form>"
        print "URL to scrape:"
        print pif.render.format_text_input("url", 256, 80, value='')
        print '<br>'
        print "Section ID:"
        print pif.render.format_text_input("section_id", 256, 80, value='single')
        print '<br>'
        print "Associated Link:"
	print pif.render.format_select('associated_link', [(0, '')] + [(x['link_line.id'], x['link_line.name']) for x in asslinks])
        print '<br>'
        print pif.render.format_button_input()
        print pif.render.format_hidden_input({'type': 'links'})
        print "</form><p>"
	for lnk in asslinks:
	    print lnk['link_line.id'], pif.render.format_link(lnk['link_line.url'], lnk['link_line.name']), '<br>'
	    #print lnk, '<br>'

	print pif.render.format_link('http://www.mbx-u.com/Search_Models_Process.php?UMID_1=LR001&UMID_2=LR999'), '<br>'
	print pif.render.format_link('http://www.mbx-u.com/Search_Models_Process.php?UMID_1=SF0001&UMID_2=SF9999'), '<br>'

#-----------------+--------------+------+-----+---------+----------------+
# Field           | Type         | Null | Key | Default | Extra          |
#-----------------+--------------+------+-----+---------+----------------+
# id              | int(11)      | NO   | PRI | NULL    | auto_increment |
# page_id         | varchar(20)  | NO   |     |         |                |
# section_id      | varchar(20)  | YES  |     |         |                |
# display_order   | int(3)       | YES  |     | 0       |                |
# flags           | int(11)      | YES  |     | 0       |                |
# associated_link | int(11)      | YES  |     | 0       |                |
# last_status     | varchar(5)   | YES  |     | NULL    |                |
# link_type       | varchar(1)   | YES  |     |         |                |
# country         | varchar(2)   | YES  |     |         |                |
# url             | varchar(256) | YES  |     |         |                |
# name            | varchar(128) | YES  |     |         |                |
# description     | varchar(512) | YES  |     |         |                |
# note            | varchar(256) | YES  |     |         |                |
#-----------------+--------------+------+-----+---------+----------------+
# 8412 | single.MB897  | single     |             7 |     0 |               7 | 200         | l         |         | http://www.areh.de/HTML/Bas1142.html | Blaze Blaster(2013)                               |             |      |
# 8413 | single.MB899  | single     |             7 |     0 |               7 | 200         | l         |         | http://www.areh.de/HTML/Bas1144.html | Questor(2013)                                     |             |      |


def_re_str = '''<a\s+href=['"](?P<u>[^'"]*)['"].*?>(?P<t>.*?)</a>'''
site_re_str = {
    7: '''<option value="(?P<u>[^'"]*)">(?P<t>.*?)</option>'''
}
def add_links_parse(pif, site, url, data):
    return re.compile(site_re_str.get(site, def_re_str), re.I | re.M | re.S).findall(useful.url_fetch(url, data))

ml_re = re.compile('''<.*?>''', re.M|re.S)
def add_links_scrape_site(pif, url, site, lnk, txt):
    page_id = ''
    if ((site == 14 and 'list.php' in lnk or 'index.php' in lnk) or
	    lnk.startswith('mailto:') or
	    0):
	return '', {}

    txt = txt.strip()
    if site == 6:
	txt = ml_re.sub('', txt)
	if not txt:
	    return '', {}
    elif site == 8:
	txt = ml_re.sub('', txt)
    elif site == 10:
	txt = ml_re.sub('', txt)
	if not txt:
	    return '', {}
    elif site == 14:
	txt = lnk[lnk.rfind('=') + 1:]
    else:
	txt = txt.replace('<', '[').replace('>', ']')

    if site == 7:
	lnk = lnk[5:] if lnk.startswith('Data_') else lnk

    if site == 14 and 'showcar.php' in lnk:
	page_id = 'single.MB' + txt

    full_link = urlparse.urljoin(url, lnk)
    dat = {
	'page_id': page_id,
	'section_id': pif.form.get_str('section_id'),
	'flags': '0',
	'associated_link': site,
	'country': '',
	'name': txt,
	'description': '',
	'note': '',
    }
    return full_link, dat

link_fields = ['page_id', 'name']
link_field_widths = {
	    'page_id': 12,
	    #'section_id': 6,
	    #'flags': 2,
	    #'associated_link': 2,
	    #'country': 2,
	    'name': 40,
	    #'description': 20,
	    #'note': 20
}
def add_links_scrape(pif):
    print '<form method="post">'
    #print pif.render.format_hidden_input({'type': 'links'})
    url = pif.form.get_str('url')
    site = pif.form.get_int('associated_link')

    data = None
    if site == 15:
	urlp = urlparse.urlparse(url)
	url = urlparse.urlunparse(urlp[:3] + ('', '', ''))
	data = urlparse.parse_qs(urlp.query)
    print site, url, data, '<br>'
    print useful.url_fetch(url, data)
    return

    print pif.render.format_table_start()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'url')
    for field in link_fields:
	print pif.render.format_cell(0, field)
    print pif.render.format_row_end()
    #print pif.render.format_hidden_input({'associated_link': site})
    found = 0
    cnt = 1

    for lnk, txt in add_links_parse(pif, site, url, data):
	full_link, dat = add_links_scrape_site(pif, url, site, lnk, txt)
	if not full_link:
	    continue
	if pif.dbh.fetch_link_line_url(full_link):
	    found += 1
	    continue
	cnts = str(cnt)
	print pif.render.format_row_start()
	print pif.render.format_cell(1, pif.render.format_link(full_link))
	print pif.render.format_hidden_input({'url.' + cnts: full_link})
	for field in link_fields:
	    print pif.render.format_cell(0, pif.render.format_text_input(field + '.' + cnts, 256, link_field_widths[field], dat[field]))
	print pif.render.format_row_end()
	cnt += 1
    print pif.render.format_table_end()
    print pif.render.format_button_input('save')
    print found, "found and dropped"
    print "</form>"

def add_links_final(pif):
    #print pif.form, '<hr>'
    site = pif.form.get_int('associated_link')
    # cheating: leaving the dot off here removes it from the get_dict call.
    for key in pif.form.roots(start='page_id'):
	link_vals = pif.form.get_dict(end=key)
	link_vals.update({'display_order': site,
	    'section_id': 'single', 'flags': 0, 'country': '', 'description': '',
	    'associated_link': site, 'page_id': 'single.' + link_vals['page_id'],
	    'note': '', 'last_status': None, 'link_type': 'l'})
	print link_vals
	print pif.dbh.insert_link_line(link_vals)
        print '<br>'

# ------- book -----------------------------------------------------

def add_book(pif):
#-----------+-------------+------+-----+---------+----------------+
# Field     | Type        | Null | Key | Default | Extra          |
#-----------+-------------+------+-----+---------+----------------+
# id        | int(11)     | NO   | PRI | NULL    | auto_increment |
# author    | varchar(64) | YES  |     |         |                |
# title     | varchar(64) | YES  |     |         |                |
# publisher | varchar(32) | YES  |     |         |                |
# year      | varchar(4)  | YES  |     |         |                |
# isbn      | varchar(16) | YES  |     |         |                |
# flags     | int(11)     | YES  |     | 0       |                |
# pic_id    | varchar(16) | YES  |     |         |                |
#-----------+-------------+------+-----+---------+----------------+

    if pif.form.has('save'):
        add_book_final(pif)
    elif pif.form.has('clone'):
        add_book_ask(pif, pif.form.get_int('id'))
    else:
        add_book_ask(pif)

def add_book_ask(pif, book_id=None):
    book = {}
    if book_id:
	book = pif.dbh.fetch('book', where="id=%s" % book_id, tag='mass_book')
	book = book[0] if book else {}
    print '<form name="mass">'
    print "ID:"
    print pif.render.format_text_input("id", 64, 64, value='')
    print pif.render.format_button_input('clone')
    print '<hr>'
    print "Author:"
    print pif.render.format_text_input("author", 64, 64, value=book.get('book.author', ''))
    print '<br>'
    print "Title:"
    print pif.render.format_text_input("title", 64, 64, value=book.get('book.title', ''))
    print '<br>'
    print "Publisher:"
    print pif.render.format_text_input("publisher", 32, 32, value=book.get('book.publisher', ''))
    print '<br>'
    print "Year:"
    print pif.render.format_text_input("year", 4, 4, value=book.get('book.year', ''))
    print '<br>'
    print "ISBN:"
    print pif.render.format_text_input("isbn", 16, 16, value=book.get('book.isbn', ''))
    print '<br>'
    print "Hidden:"
    print pif.render.format_checkbox('hidden', [('1', 'yes')])
    print '<br>'
    print "Picture ID:"
    print pif.render.format_text_input("pic_id", 16, 16, value=book.get('book.pic_id', ''))
    print '<br>'
    print "Picture URL:"
    print pif.render.format_text_input("pic_url", 256, 80, value='')
    print '<br>'
    print pif.render.format_button_input('save')
    print pif.render.format_button_reset('mass')
    print pif.render.format_button('book', 'biblio.cgi?edit=1')
    print pif.render.format_button('edit', 'editor.cgi?table=book')
    print pif.render.format_hidden_input({'type': 'book'})
    print "</form><p>"

def add_book_final(pif):
    print pif.form, '<br>'
    if not pif.form.has('title'):
	print 'No title supplied.'
	return
    if pif.form.get_str('isbn'):
	if pif.dbh.fetch('book', where="isbn='%s'" % pif.form.get_str('isbn'), tag='mass_book'):
	    print 'That isbn is already in use.'
	    return
    if pif.form.get_str('pic_id') and pif.form.get_str('pic_url'):
	if pif.dbh.fetch('book', where="pic_id='%s'" % pif.form.get_str('pic_id'), tag='mass_book'):
	    print 'That pic_id is already in use.'
	    return
	images.grab_url_file(pif.form.get_str('pic_url'), config.IMG_DIR_BOOK, pif.form.get_str('pic_id'))
    vals = {
	'author': pif.form.get_str('author'),
	'title': pif.form.get_str('title'),
	'publisher': pif.form.get_str('publisher'),
	'year': pif.form.get_str('year'),
	'isbn': pif.form.get_str('isbn'),
	'flags': pif.dbh.FLAG_ITEM_HIDDEN if pif.form.get_int('flags') else 0,
	'pic_id': pif.form.get_str('pic_id'),
    }
    print vals
    print pif.dbh.write('book', vals, newonly=True, tag='mass_book', verbose=True), '<br>'
    if vals['pic_id']:
	print pif.render.format_image_required(vals['pic_id'], pdir=config.IMG_DIR_BOOK)

# ------- ----------------------------------------------------------

mass_mains_list = [
    ('lineup', add_lineup_main),
    ('casting', add_casting_main),
    ('pub', add_pub_main),
    ('var', add_var_main),
    ('related', edit_casting_related),
    ('pack', add_pack),
    ('links', add_links),
    ('book', add_book),
]

mass_mains_hidden = {
    'lineup_desc': lineup_desc_main,
}

def mass_sections(pif):
    for section in mass_mains_list:
	print pif.render.format_button(section[0], link='?type=' + section[0])


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
