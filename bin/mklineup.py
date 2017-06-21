#!/usr/local/bin/python

import sys
import basics
import mbdata

# input file has new models in form:
#1|MB1002|Heavy Railer|red/yellow
# lineup_number | mod_id | mod_name | var_description

# currently can't handle multiple variations of a particular number

# hardcoded values:
regions = ['U', 'R']
picdir = 'pic/prod/mattel'


def raw_insert(pif, table, data):
    pif.dbh.dbi.insert_or_update(
    #print (
	table, data
    )


def add_page(pif, year):
    raw_insert(pif, 'page_info', {
        'id': 'year.' + year,
        'flags': 0,
        'health': 0,
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
	'base': '',
	'body': mod[3],
	'interior': '',
	'windows': '',
	'manufacture': '',
	'category': '',
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


@basics.command_line
def main(pif):
    year = pif.filelist[0]
    fn = pif.filelist[1]
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


if __name__ == '__main__':  # pragma: no cover
    #main(dbedit='')  # too dangerous to leave on all the time
    main()
