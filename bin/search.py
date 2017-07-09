#!/usr/local/bin/python

import basics
import mflags
import models
import useful
import vars

def search_name(pif):
    return pif.dbh.fetch_casting_list(where=["base_id.rawname like '%%%s%%'" % x for x in pif.form.search('query')], verbose=True)


# specific id request goes through here
# would like to accept K43a like things
def search_id(pif):
    cid = get_casting_id(pif.form.get_str('id'))
    mod = pif.dbh.fetch_casting(cid)
    var_id = pif.form.get_str('var')
    if mod:
	if var_id:
	    raise useful.Redirect('/cgi-bin/vars.cgi?mod=%s&var=%s' % (mod['id'], var_id))
	else:
	    raise useful.Redirect('/cgi-bin/single.cgi?id=%s' % mod['id'])

    mod = pif.dbh.fetch_castings_by_alias(cid)
    if len(mod) == 1:
	mod = mod[0]
        if mod.get('alias.id'):
	    if var_id:
		raise useful.Redirect('/cgi-bin/vars.cgi?mod=%s&var=%s' % (mod['casting.id'], var_id))
	    else:
		raise useful.Redirect('/cgi-bin/single.cgi?id=%s' % mod['casting.id'])

    if not mod:
        mod1 = pif.dbh.fetch_casting_list(where="casting.id like '%%%s%%'" % pif.form.get_str('id'))
        mod2 = pif.dbh.fetch_aliases(where="alias.id like '%%%s%%'" % pif.form.get_str('id'))
        mod = filter(lambda x: x.get('section.page_id', 'manno') in ['manls', 'manno'], mod1 + mod2)
    return [pif.dbh.modify_man_item(x) for x in mod]


def get_casting_id(id):
    if not id:
        return ''
    ok = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-/'
    id = ''.join(filter(lambda x: x in ok, list(id)))
    if not id:  # pragma: no cover
        return {}
    if id.upper().startswith('MW'):
        id = 'MB' + id[2:]
    if id.upper().startswith('MI') and id[2:].isdigit():
        if int(id[2:]) < 700:
            id = 'MB' + id[2:]
    if id.upper().startswith('LR'):
        id = 'RW' + id[2:]
    if id.upper().startswith('LS'):
        id = 'SF' + id[2:]
    return id


def create_var_lineup(mods, var_id):
    llineup = {'columns': 4}
    lsec = pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
    lran = {'entry': []}
    for mod in mods:
	var = pif.dbh.fetch_variation_query_by_id(mod['base_id.id'], var_id)
	lran['entry'].append({'text': vars.add_model_var_table_pic_link(pif, var)})
    lsec['range'] = [lran]
    lsec['columns'] = 4
    llineup['section'] = [lsec]
    return llineup


def create_lineup(pif, mods):
    flago = mflags.FlagList()
    llineup = {'columns': 4}
    lsec = pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
    lran = {'entry': []}
    for mod in mods:
        mod = pif.dbh.modify_man_item(mod)
        lran['entry'].append({'text': models.add_model_table_pic_link(pif, mod, flago=flago)})
    lsec['range'] = [lran]
    lsec['columns'] = 4
    llineup['section'] = [lsec]
    return llineup


@basics.web_page
def run_search(pif):
    # form['var'] is now a possibility
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append(pif.request_uri, 'Model Search')
    mods = None
    pif.render.print_html()
    if pif.form.has('date'):
	return date_search(pif, pif.form.get_str('dt'), pif.form.get_str('yr'))
    if pif.form.has('query'):
        targ = pif.form.get_str('query')
        pif.render.title = 'Models matching name: ' + targ
        mods = search_name(pif)
        mods = filter(lambda x: x['section.page_id'] in ('manls', 'manno'), [pif.dbh.modify_man_item(x) for x in mods])
    elif pif.form.has('id'):
        targ = pif.form.get_str('id')
        mods = search_id(pif)
        if mods is None:
	    raise useful.SimpleError("Your query parameters do not make sense.  Please try something different.")
        pif.render.title = 'Models matching ID: ' + targ
    else:
        raise useful.SimpleError("Your query parameters do not make sense.  Please try something different.")
    if not mods:
	raise useful.SimpleError("Your query did not produce any models.  Sorry 'bout that.")

    mods.sort(key=lambda x: x['rawname'])
    var_id = pif.form.get_str('var')
    if var_id:
	pif.render.set_button_comment(pif, 'query=%s' % (pif.form.get_str('query')))
	llineup = create_var_lineup(pif, mods, var_id)
    else:
	pif.render.set_button_comment(pif, 'query=%s' % (pif.form.get_str('query')))
	llineup = create_lineup(pif, mods)

    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('simplematrix.html', llineup=llineup)


def date_search(pif, dt=None, yr=None):
    llineup = {'columns': 4}
    lsec = {}
    lran = {'entry': []}
    if dt:
	vars = pif.dbh.fetch_variations_by_date(dt)
	for var in vars:
	    lran['entry'].append({'text': '<input type="checkbox"> ' +
		pif.render.format_link(
		'/cgi-bin/vars.cgi?mod=%s&var=%s' % (var['variation.mod_id'], var['variation.var']),
		'%s-%s %s<br>%s' % (var['variation.mod_id'], var['variation.var'], var['base_id.rawname'], var['variation.text_description']))
	    })
	lsec['columns'] = 3
    else:
	dates = pif.dbh.fetch_variation_dates(yr=yr)
	for dt in dates:
	    if dt['date']:
		lran['entry'].append({'text': pif.render.format_link(
		    '/cgi-bin/msearch.cgi?date=1&dt=%s' % dt['date'],
		    '%s (%s)' % (dt['date'], dt['count(*)']))})
	lsec['columns'] = 6
    lsec['range'] = [lran]
    llineup['section'] = [lsec]
    llineup['footer'] = '<hr><form action="/cgi-bin/msearch.cgi">Year = /<input type="hidden" name="date" value="1"><input type="text" name="yr"> <input type="submit" name="submit" value="GO" class="textbutton"></form>\n'
    llineup['footer'] += '''<form action="/cgi-bin/msearch.cgi">Mod ID: <input type="text" name="id" size="12"> Var ID: <input type="text" name="var" size="12"> <input type="submit" name="submit" value="GO" class="textbutton"></form>\n'''
    pif.render.format_matrix_for_template(llineup, flip=True)
    return pif.render.format_template('simplematrix.html', llineup=llineup)


if __name__ == '__main__':  # pragma: no cover
    basics.goaway()
