#!/usr/local/bin/python

import basics
import config
import mbdata
import useful

# -------- mack ------------------------------------

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

    lsec = pif.dbh.depref('section', pif.dbh.fetch_sections({'page_id': pif.page_id})[0])
    lsec['range'] = [{'entry': mods}]
    llineup = {'section': [lsec]}
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('mack.html', llineup=llineup)


if __name__ == '__main__':  # pragma: no cover
    basics.goaway()
