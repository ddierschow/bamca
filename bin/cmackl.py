#!/usr/local/bin/python

import basics
import config
import lineup
import mbdata
import single
import useful

# ----- mack -----------------------------------------------------------

def mack_models(pif, start, end, series):
    mseries = 'MB' if 'RW' not in series else None if 'SF' in series else ''
    amods = {mbdata.get_mack_number(rec['alias.id']): rec for rec in pif.dbh.fetch_aliases(type_id='mack')}
    mmods = {mbdata.get_mack_number(rec['base_id.id']): rec for rec in
	pif.dbh.fetch_casting_list('sf') + pif.dbh.fetch_casting_list('rw')}
    amods.update(mmods)
    return mod_to_mack(pif, amods, start, end, mseries)


def mod_to_mack(pif, recs, start, end, series):
    keys = recs.keys()
    keys.sort(key=lambda x: (x[1], x[0], x[2]))
    for mack_id in keys:
	rec = recs[mack_id]
	if mack_id and int(mack_id[1]) >= start and int(mack_id[1]) <= end and \
		not (series is not None and series != mack_id[0]):
	    yield {
		'id': '%s%02s-%s' % mack_id,
		'name': rec['base_id.rawname'].replace(';', ' '),
		'href': 'single.cgi?id=' + rec['base_id.id'],
		'imgstr': pif.render.format_image_required(rec['base_id.id'], prefix=mbdata.IMG_SIZ_SMALL),
		'mack_id_unf': mack_id,  # for sorting
	    }


@basics.web_page
def mack_lineup(pif):
    pif.render.set_button_comment(pif, 'rg=%s&sec=%s&start=%s&end=%s' % (pif.form.get_str('region', ''), pif.form.get_str('sect', ''), pif.form.get_str('start', ''), pif.form.get_str('end', '')))
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append(pif.request_uri, 'Mack Numbers')
    pif.render.print_html()

    series = ['RW', 'SF'] if pif.form.get_str('sect', 'all') == 'all' else [pif.form.get_str('sect').upper()]
    range = pif.form.get_str('range', 'all')
    start = 1 if range == 'all' else pif.form.get_int('start', 1)
    end = config.MAX_MACK_NUMBER if range == 'all' else pif.form.get_int('end', config.MAX_MACK_NUMBER)

    mods = mack_models(pif, start, end, series)

    if not mods:
        note = 'Your request produced no models.'
        if start > config.MAX_MACK_NUMBER:
            note += '  Be sure to use numbers from 1 to %d.' % config.MAX_MACK_NUMBER
        if start > end:
            note += "  Use a start number that isn't higher than the end number."
	raise useful.SimpleError(note)

    #mods.sort(key=lambda x: (x['mack_id_unf'][1], x['mack_id_unf'][0], x['mack_id_unf'][2]))

    lsec = pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
    lsec['range'] = [{'entry': mods}]
    llineup = {'section': [lsec]}
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('mack.html', llineup=llineup)

# ----- ----------------------------------------------------------------

def check_man_mappings(pif, sections):
    for section in sections:
	mans = pif.dbh.fetch_casting_list(section_id=section, page_id='manno')
	mans.sort(key=lambda x: x['casting.id'])
	for man in mans:
	    cid = man['casting.id']
	    aliases = [x['alias.id'] for x in pif.dbh.fetch_aliases(cid, 'mack')]
	    mack_nums = single.get_mack_numbers(pif, cid, man['base_id.model_type'], aliases)
	    if not mack_nums:
		print cid


def check_mack_ranges(pif):
    letters = list('abcdefghijklmnopqrstuvwyz') + ['aa']
    ranks = {}
    mods = lineup.mack_models(pif, 1, config.MAX_MACK_NUMBER, ['SF'])
    num = 0
    for mod in mods:
	if num != int(mod['mack_id_unf'][1]):
	    num = int(mod['mack_id_unf'][1])
	    ranks[num] = set()
	ranks[num].add(mod['mack_id_unf'][2])
    for num in range(1, config.MAX_MACK_NUMBER + 1):
	s = ranks.get(num)
	if s:
	    missing = ''
	    for li in range(letters.index(max(s))):
		if letters[li] not in s:
		    missing += letters[li]
	    if missing:
		missing = '^' + missing
	    s1 = min(s)
	    s2 = max(s)
	    if s1 != s2:
		print '| %3d : %s-%s%-3s' % (num, s1, s2, missing)
	    else:
		print '| %3d : %s  %-3s' % (num, s1, missing)
	else:
	    print '| %3d :       ' % num

# ----- ----------------------------------------------------------------

cmds = [
    ('c', check_mack_ranges, "check mack ranges"),
]

@basics.command_line
def commands(pif):
    useful.cmd_proc(pif, './cmackl.py', cmds)

# ----- ----------------------------------------------------------------

if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='')
