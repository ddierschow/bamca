#!/usr/local/bin/python

import basics
import mbdata
import mflags
import models
import useful
import varias

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


def create_var_lineup(pif, mods, var_id):
    llineup = {'columns': 4}
    lsec = pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
    lran = {'entry': []}
    for mod in mods:
	for var in pif.dbh.fetch_variation_query_by_id(mod['id'], var_id):
	    lran['entry'].append({'text': varias.add_model_var_table_pic_link(pif, var)})
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
        firstyear = pif.form.get_int('syear', 1)
        lastyear = pif.form.get_int('eyear', 9999)
        pif.render.title = 'Models matching name: ' + targ
        mods = search_name(pif)
        mods = [pif.dbh.modify_man_item(x) for x in mods if x['section.page_id'] in ('manls', 'manno') and int(x['base_id.first_year']) >= firstyear and int(x['base_id.first_year']) <= lastyear]
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

    mods.sort(key=lambda x: x.get('rawname', ''))
    var_id = pif.form.get_str('var')
    if var_id:
	pif.render.set_button_comment(pif, 'query=%s' % (pif.form.get_str('query')))
	llineup = create_var_lineup(pif, mods, var_id)
    else:
	pif.render.set_button_comment(pif, 'query=%s' % (pif.form.get_str('query')))
	llineup = create_lineup(pif, mods)

    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('simplematrix.html', llineup=llineup)


def get_mack_numbers(pif, mod_id):
    def fmt_mack_id(m):
	ostr = ''
	if m[0]:
	    ostr += '%s-' % m[0]
	if m[2]:
	    ostr += '%03d-%s' % m[1:]
	else:
	    ostr += '%03d' % m[1]
	return ostr

    ret = []
    mack = mbdata.get_mack_number(mod_id)
    if mod_id.startswith('RW') or mod_id in ('MI740', 'MI816', 'MI861') or (mack and mack[0] and mack[2]):
	ret.append(fmt_mack_id(mack))
    aliases = sorted(pif.dbh.fetch_aliases(mod_id), key=lambda x: (-x['alias.flags'], x['alias.ref_id']))
    ret += [fmt_mack_id(mbdata.get_mack_number(x['alias.id'])) for x in aliases]
    if not mack or not mack[2]:
	ret.append(mod_id)
    return ret


descs = ['body', 'base', 'interior', 'windows', 'wheels']
def date_search(pif, dt=None, yr=None):
    llineup = {'columns': 4}
    lsec = {}
    lran = {}
    llineup['header'] = llineup['footer'] = ''
    if dt:
	pif.render.title = dt
	vars = pif.dbh.fetch_variations_by_date(dt)
	last = None
	ver_count = 0
	for var in vars:
	    verified = ['1'] if var['variation.flags'] & pif.dbh.FLAG_MODEL_VARIATION_VERIFIED else []
	    id_mismatch = ['1'] if var['variation.flags'] & pif.dbh.FLAG_MODEL_ID_INCORRECT else []
	    ver_count += 1 if verified else 0
	    macks = get_mack_numbers(pif, var['variation.mod_id'])
	    var['sort'] = macks[0] if macks else var['variation.mod_id']
	    mvid = "%s-%s" % (var['variation.mod_id'], var['variation.var'])

	    done = all([var['variation.text_' + x] != '' for x in ['description'] + descs]) # ignore text_with for now
	    done = ' <i class="fas fa-star %s"></i>\n' % ('green' if done else 'red')
	    cats = ('(%s)' % var['variation.category']) if var['variation.category'] else ''
	    desc = ''.join(['<li>' + x + ': ' + var['variation.text_' + x] for x in descs])
	    if var['variation.text_with']:
		desc += '<li>with: ' + var['variation.text_with']
	    var['shown'] = ''
	    if last != var['variation.mod_id']:
		var['shown'] += (
		    pif.render.format_link('/cgi-bin/single.cgi?id=%s' % (var['variation.mod_id']),
			'<b>%s ' % '/'.join(macks)) +
		    pif.render.format_link('/cgi-bin/vars.cgi?mod=%s' % (var['variation.mod_id']),
			'%s</b><br>' % var['base_id.rawname'].replace(';', ' '))
		)
		last = var['variation.mod_id']
	    var['shown'] += pif.render.format_image_optional(var['variation.mod_id'], vars=[var['variation.picture_id'] or 'unmatchable', var['variation.var']], also={'class': 'righty'}, nobase=True, largest='s')
	    var['shown'] += (pif.render.format_hidden_input({'v.' + mvid: '1'}) +
		pif.render.format_checkbox('c.' + mvid, [('1', '',)], checked=verified, sep='\n') +
		pif.render.format_checkbox('i.' + mvid, [('1', '',)], checked=id_mismatch, sep='\n') +
		pif.render.format_link(
		    '/cgi-bin/vars.cgi?mod=%s&var=%s&edit=1' % (var['variation.mod_id'], var['variation.var']),
		    '(%s) %s' % (var['variation.var'], var['variation.text_description'])) + done +
		    '<i>' + var['variation.note'] + '</i> ' + cats + '\n<ul>' + desc + '</ul>\n'
	    )
	vars.sort(key=lambda x: x['sort'])
	lran['entry'] = [{'text': x['shown']} for x in vars]
	lsec['columns'] = 1
	llineup['header'] += 'Verified: %d of %d<br><form action="/cgi-bin/mass.cgi?type=dates" method="post">' % (ver_count, len(vars))
	llineup['footer'] += pif.render.format_button_input() + '</form>'
    else:
	pif.render.title = 'Search Dates'
	dates = pif.dbh.fetch_variation_dates(yr=yr)
	lran['entry'] = [{'text': pif.render.format_link(
		    '/cgi-bin/msearch.cgi?date=1&dt=%s' % dt['date'],
		    '%s (%s)' % (dt['date'], dt['count(*)']))} for dt in dates if dt['date']]
	lsec['columns'] = 6
    lsec['range'] = [lran]
    llineup['section'] = [lsec]
    llineup['footer'] += '<hr>'
    llineup['footer'] += '<form action="/cgi-bin/msearch.cgi">Year = /<input type="hidden" name="date" value="1"><input type="text" name="yr"> <input type="submit" name="submit" value="GO" class="textbutton"></form>\n'
    llineup['footer'] += '''<form action="/cgi-bin/msearch.cgi">Mod ID: <input type="text" name="id" size="12"> Var ID: <input type="text" name="var" size="12"> <input type="submit" name="submit" value="GO" class="textbutton"></form>\n'''
    pif.render.format_matrix_for_template(llineup, flip=True)
    return pif.render.format_template('simplematrix.html', llineup=llineup)
