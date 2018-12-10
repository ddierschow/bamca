#!/usr/local/bin/python

import copy, os, re, urllib2
import basics
import config
import imglib
import masses
import mbdata
import useful


# ------- editor ---------------------------------------------------

# - presentation


def editor_start(pif):
    if pif.form.get_bool('clear'):
        pif.dbh.clear_health()

    errs = pif.dbh.fetch_counters("health!=0")
    if errs:
        useful.warn('<hr>', "<b>Errors found:<br><ul>",
	    '\n'.join(["<li>" + err['counter.id'] for err in errs]),
	    "</ul></b>", pif.render.format_button('clear', '?clear=1'))

    context = {
	'table_info': pif.dbh.table_info,
	'asks': sorted([t for t in pif.dbh.table_info if 'ask' in pif.dbh.table_info[t]]),
	'masses': [x[0] for x in masses.mass_mains_list],
    }
    return pif.render.format_template('editorask.html', **context)


# primary entry

@basics.web_page
def editor_main(pif):
    pif.render.print_html()
    pif.restrict('a')
    pif.render.set_page_extra(pif.render.reset_button_js)
    if pif.form.get_str('promote'):
	return imglib.promote_picture(pif, pif.form.get_str('mod'), pif.form.get_str('var'))
    if pif.form.get_str('table'):
	return show_table(pif)
    return editor_start(pif)


def show_table(pif):
    pif.render.message(str(pif.form.get_form()))
    table_info = pif.dbh.get_table_info(pif.form.get_str('table'))

    def save_val(key):
	if key in table_info.get('bits', {}):
	    return pif.form.get_bits(key)
	return pif.form.get_str(key)

    dats = []
    if pif.duplicate_form: #not pif.dbh.insert_token(pif.form.get_str('token')):
	print 'duplicate form submission detected'
    elif pif.form.has('save'):
		#rec['flags'] = sum(int(x, 16) for x in pif.form.get_list('base_id.flags'))
        pif.dbh.write(table_info['name'], {x: save_val(x) for x in table_info['columns'] + table_info.get('extra_columns', [])},
                      pif.form.where(table_info['id'], 'o_'), tag='ShowTableSave')
        pif.render.message('record saved')
    elif pif.form.has('delete'):
        pif.dbh.delete(table_info['name'], pif.form.where(table_info['id'], 'o_'))
        pif.form.delete('id')
        pif.render.message('record deleted')
    elif pif.form.has('clone'):
	# this should be done in memory without saving yet
        pif.dbh.write(table_info['name'], {x: save_val(x) for x in table_info['columns'] + table_info.get('extra_columns', [])}, pif.form.where(table_info['id'], 'o_'), newonly=True, tag='ShowTableClone')
        #del pif.form.delete('id')
        pif.render.message('record cloned')
	pif.form.delete('clone')
    elif pif.form.has('add'):
        pif.render.message('add' + table_info.get('name', 'unset'))
#        print table_info, '<br>'
        adds = table_info.get('add', {})
        creat = table_info.get('create', {})
        cond = {}
        for id in table_info['columns']:
            pif.form.default(id, creat.get(id, save_val(id)))
            cond[id] = save_val(id)
	dats = [cond]
        print 'new record'

    if not dats:
	where = pif.form.where(table_info['columns'] + table_info.get('extra_columns', []))
	dats = pif.dbh.fetch(table_info['name'], where=where, tag='ShowTable', extras=True)

    header = footer = ''
#    header = '<b>' + table_info['name'] + '</b>'
#    header += pif.render.format_button('show all', "?table=" + table_info['name'])
    lsections = []

    if len(dats) > 1:
	lsections.extend(show_multi(pif, table_info, dats))
    elif len(dats) == 1:
        lsections.extend(show_single(pif, table_info, dats))
    else:
        lsections.extend(show_none(pif, table_info, {x: save_val(x) for x in table_info['columns'] + table_info.get('extra_columns', [])}))
    if table_info['name'] in table_info.get('add', {}):
	cond = {'add': '1'}
	footer += pif.render.format_button('add', "?table=" + table_info['name'] + "&" + "&".join([x + '=' + cond[x] for x in cond]))
    lsections[0]['header'] = header + lsections[0].get('header', '')
    lsections[0]['footer'] = lsections[0].get('footer', '') + footer
    lsections.extend(show_sub_tables(pif, table_info, dats[0] if len(dats) == 1 else None))
    llistix = {'section': lsections}
    return pif.render.format_template('simplelistix.html', llineup=llistix)


def show_multi(pif, table_info, dats, cols=None):
    if pif.form.has('order') and dats:
	sort_ord = table_info['name'] + '.' + pif.form.get_str('order')
	if sort_ord in dats[0]:
	    dats.sort(key=lambda x: x[sort_ord])
    lsections = [show_multi_section(pif, table_info, dats, cols)]
    return lsections


def show_single(pif, table_info, dats):
    dat = pif.dbh.depref(table_info['name'], dats[0])
    dats = [dat]
    adds = table_info.get('add', {})
    descs = pif.dbh.describe_dict(table_info['name'])

    lsections = []
    for base_tab, base_rel in table_info.get('extends', {}).items():
	base_inf = pif.dbh.get_table_info(base_tab)
	base_rel = base_rel.split('/')
	base_where = '%s="%s"' % (base_rel[1], dat[base_rel[0]])
	base_dats = pif.dbh.fetch(base_inf['name'], where=base_where, tag='ShowBaseTable', extras=True)
	if len(base_dats) > 1:
	    pif.render.message('multiple instances of', base_tab, '!')
	elif not base_dats:
	    pif.render.message('no instances of', base_tab, '!')
	else:
	    lsections.extend(show_single(pif, base_inf, base_dats))

    header = '<b>' + table_info['name'] + '</b>'
    header += pif.render.format_button('show all', "?table=" + table_info['name'])
    header += '<form action="/cgi-bin/editor.cgi">\n'
    header += pif.create_token()
    header += '<input type="hidden" name="verbose" value="1">\n'
    header += '<input type="hidden" name="table" value="%s">\n' % table_info['name']
    for f in table_info['id']:
        header += '<input type="hidden" name="o_%s" value="%s">\n' % (f, dat.get(f, ''))

    columns = ['column', 'type', 'value', 'new value']
    entries = []

    for col in table_info['columns'] + table_info.get('extra_columns', []):
	coltype = descs.get(col).get('type', 'unknown')
	oldvalue = make_col_value(table_info, col, dat)
	newvalue = coltype
	# char(N)
	# datetime
	# int(N)
	# smallint(N)
	# text
	# time
	# timestamp
	# tinyint(N)
	# varchar(N)
	if col in table_info.get('readonly', []):
	    newvalue = '&nbsp;<input type=hidden name="%s" value="%s">' % (col, dat.get(col, ''))
	elif col in table_info.get('bits', {}):
	    newvalue = pif.render.format_checkbox(col, table_info['bits'][col], useful.bit_list(oldvalue, format='%04x'))
	elif coltype == 'text':
	    newvalue = pif.render.format_textarea_input(col, value=dat.get(col, ''))
	elif coltype.startswith('varchar('):
	    colwidth = int(coltype[8:-1])
	    newvalue = pif.render.format_text_input(col, colwidth, colwidth, value=dat.get(col, ''))
	elif coltype.startswith('char('):
	    colwidth = int(coltype[5:-1])
	    newvalue = pif.render.format_text_input(col, colwidth, colwidth, value=dat.get(col, ''))
	elif coltype.startswith('tinyint('):
	    if dat.get(col) is None:
		dat[col] = 0
	    colwidth = int(coltype[8:-1])
	    val = dat[col]
	    if isinstance(val, str) and val.isdigit():
		val = str(int(val))
	    elif not val:
		val = '0'
	    newvalue = pif.render.format_text_input(col, colwidth, colwidth, value=val)
	elif coltype.startswith('smallint('):
	    if dat.get(col) is None:
		dat[col] = 0
	    colwidth = int(coltype[9:-1])
	    val = dat[col]
	    if isinstance(val, str) and val.isdigit():
		val = str(int(val))
	    elif not val:
		val = '0'
	    newvalue = pif.render.format_text_input(col, colwidth, colwidth, value=val)
	elif coltype.startswith('int('):
	    if dat.get(col) is None:
		dat[col] = 0
	    colwidth = int(coltype[4:-1])
	    val = dat[col]
	    if isinstance(val, str) and val.isdigit():
		val = int(val)
	    elif not val:
		val = 0
	    newvalue = pif.render.format_text_input(col, colwidth, colwidth, value=str(val))
	entries.append({'column': col, 'type': coltype, 'value': oldvalue, 'new value': newvalue})

    footer = pif.render.format_button_input("save")
    footer += pif.render.format_button_input("delete")

    if table_info['name'] in adds:
        footer += pif.render.format_button('add', "?table=" + table_info['name'] + "&add=1&" + make_url_cond(adds[table_info['name']], dat))
        del adds[table_info['name']]
        footer += pif.render.format_button_input('clone')
    footer += '</form>\n'
    for elink in table_info.get('elinks', []):
        footer += pif.render.format_button(elink['name'], elink['url'] % dat) + '<br>\n'
    footer += '<hr>\n'

    lrange = {'entry': entries, 'styles': {'column': 0}}
    lsections.append({'columns': columns, 'range': [lrange], 'note': '',
	'headers': dict(zip(columns, columns)), 'header': header, 'footer': footer})
    return lsections


def show_sub_tables(pif, table_info, dat=None):
    columns = ['column', 'type', 'value', 'new value']
    adds = table_info.get('add', {})
    lsections = []
    lsections.append({'entry': [], 'header': '<h3>Subtables</h3>\n'})

    anchors = []
    for subtab in table_info.get('tlinks', []):
	if subtab['tab'] in table_info.get('extends', {}):
	    continue
	try:
	    if not eval(subtab.get('if', '1')):
		continue
	except:
	    continue
        #ostr += "<hr>"
        header = '<b>' + subtab['tab'] + '</b>'

        if dat and subtab['tab'] in adds:
            header += pif.render.format_button('add', "?table=" + subtab['tab'] + "&" + make_url_cond(adds[subtab['tab']], dat))
            del adds[subtab['tab']]

        cond = dict()
        if dat and 'id' in subtab:
	    cond = make_cond(subtab['id'], dat)
            lsection = show_sub_table_section(pif, pif.dbh.get_table_info(subtab['tab']), cond, ref=subtab.get('ref', {}))
            lsection['header'] = header + pif.render.format_button('show', "?table=" + subtab['tab'] + "&" + "&".join([x + '=' + str(cond[x]) for x in cond])) + '\n' + lsection['header']
        else:
            header += pif.render.format_button('show', "?table=" + subtab['tab'])
#       if subtab['tab'] in adds:
#           ostr += pif.render.format_button('add', "?table=" + subtab['tab'] + "&" + "&".join([x + '=' + str(cond[x]) forx in cond]))
	    lsection = {'columns': columns, 'range': [{'entry': [], 'styles': {'column': 0}}], 'note': '',
		'headers': dict(zip(columns, columns)), 'header': header}
	lsection['anchor'] = subtab['tab']
	anchors.append(subtab['tab'])
	lsections.append(lsection)

    return lsections


def show_none(pif, table_info, dat):
    pif.render.message("No records found.")
    adds = table_info.get('add', {})
    header = '<b>' + table_info['name'] + '</b>'
    header += pif.render.format_button('show all', "?table=" + table_info['name'])
    lsections = []
    lsections.append({'header': header})
    if table_info['name'] in adds:
	cond = make_url_cond(adds[table_info['name']], dat)
        lsections.append({'header': pif.render.format_button('add', "?table=" + table_info['name'] + "&add=1&" + cond)})
        del adds[table_info['name']]
    for subtab in table_info.get('tlinks', []):
        if not eval(subtab.get('if', '1')):
            continue
        header = "<hr>" + subtab['tab']
#        if subtab['tab'] in adds:
#            header += pif.render.format_button('add', "?table=" + subtab['tab'] + "&add=1&" + "&".join([x + '=' + str(cond[x]) for x in cond]))
        cond = {}
        if 'id' in subtab:
            for id in subtab['id']:
                fr, to = id.split('/')
                if to[0] == '*':
                    cond[fr] = eval(to[1:])
                else:
                    cond[fr] = dat.get(to, '')
	    lsection = show_sub_table_section(pif, pif.dbh.get_table_info(subtab['tab']), cond, ref=subtab.get('ref', {}))
            lsection['header'] = header + pif.render.format_button('show', "?table=" + subtab['tab'] + "&" +
                                           "&".join([x + '=' + str(cond[x]) for x in cond])) + '\n' + lsection['header']
	else:
	    lsection = {header + 'header': pif.render.format_button('show', "?table=" + subtab['tab'])}
	lsections.append(lsection)
        if subtab['tab'] in adds:  #  ummmm?
            cond = {'add': '1'}
            for id in adds[subtab['tab']]:
                fr, to = id.split('/')
                cond[fr] = dat.get(to, '')
            del adds[subtab['tab']]
    #llistix = {'section': lsections}
    return lsections


def make_cond(clinks, dat):
    cond = {}
    for cid in clinks:
	fr, to = cid.split('/') if '/' in cid else (cid, cid)
	to = eval(to[1:]) if to[0] == '*' else dat.get(to, '')
	cond[fr] = to
    return cond


def make_url_cond(clinks, dat):
    cond = make_cond(clinks, dat)
    return '&'.join(['%s=%s' % x for x in cond.items()])


def make_col_value(table_info, col, dat):
    val = dat.get(col, '')
    if col in table_info.get('id', []):
	return '<a href="?table=%s&%s">%s</a>' % (table_info['name'], make_url_cond(table_info['id'], dat), val)
    elif col in table_info.get('clinks', {}):
	return '<a href="?table=%s&%s">%s</a>' % (table_info['clinks'][col]['tab'], make_url_cond(table_info['clinks'][col]['id'], dat), val)
    return val


def show_multi_section(pif, table_info, dats, cols=None):
    columns = [col for col in
	(cols if cols else table_info['columns'] + table_info.get('extra_columns', []))
       	if col not in table_info.get('hidden', [])]
    entries = [
	{x: make_col_value(table_info, x, dat) for x in columns}
	    for dat in pif.dbh.depref(table_info['name'], dats)
    ]

    header = ''#'<b>' + table_info['name'] + '</b>\n'
    header += pif.render.format_button('show all', "?table=" + table_info['name'])
    header += '\n%s entries\n' % len(entries)

    lsection = {'columns': columns, 'note': '', 'header': header, 'footer': '<hr>\n',
	'range': [{'entry': entries, 'styles': dict.fromkeys(table_info.get('id', []), '2')}],
	'headers': dict(zip(columns, columns))}
    return lsection


def show_sub_table_section(pif, table_info, cond, ref={}):
    # need to make this handle subtab['ref']
    # {'tab': 'detail', 'id': ['mod_id/mod_id', 'var_id/var'], 'ref': {'attr_id': ['attribute', 'id', 'attribute_name']}},
    # so in this case: ref = {'attr_id': ['attribute', 'id', 'attribute_name']}
    tname = table_info['name']
    if ref:
        cols = [table_info['name'] + '.' + x for x in table_info['columns'] + table_info.get('extra_columns', [])]
        lcond = {}
        for key in ref:
            lcond[key] = ref[key][0] + '.' + ref[key][1]
            cols.append(ref[key][0] + '.' + ref[key][2])
            tname += ',' + ref[key][0]  # this will break if we do two columns
        where = " and ".join([table_info['name'] + '.' + x + "='" + cond[x] + "'" for x in cond])
        if lcond:
            where += " and " + " and ".join([table_info['name'] + '.' + x + "=" + lcond[x] for x in lcond])
    else:
        cols = table_info['columns'] + table_info.get('extra_columns', [])
        where = " and ".join([table_info['name'] + '.' + x + "='" + str(cond[x]) + "'" for x in cond])
    dats = pif.dbh.fetch(tname, columns=cols, where=where, tag='show_sub_table_section')
    return show_multi_section(pif, table_info, dats, cols)


# ------- counters -------------------------------------------------

@basics.web_page
def show_counters(pif):
    pif.render.print_html()
    pif.restrict('a')
    pif.render.set_page_extra(pif.render.reset_button_js)

    res = pif.dbh.depref('counter', pif.dbh.fetch_counters())
    sortorder = pif.form.get_str('s', 'id')
    revorder = pif.form.get_int('r')
    res.sort(key=lambda x: x[sortorder])
    if revorder:
        res.reverse()

    columns = ['id', 'value', 'timestamp', 'health']
    headers = dict(zip(columns, ['ID', 'Value', 'Timestamp', 'Health']))
    lsection = dict(columns=columns, range=[{'entry': useful.printablize(res)}], note='',
	headers={col: pif.render.format_link('?s=' + col +
	'&r=1' if col == sortorder and not revorder else '', headers[col]) for col in columns})
    return pif.render.format_template('simplelistix.html', llineup=dict(section=[lsection]))


# ------- ----------------------------------------------------------


desc_cols = ['Field', 'Type', 'Null', 'Key', 'Default', 'Extra']
def command_info(pif):
    tabs = pif.dbh.fetch_tables()
    for table in tabs[0]:
	print table[0]
	tinfo = pif.dbh.table_info.get(table[0])
	tab = pif.dbh.fetch_table(table[0])
	for col in tab[0]:
	    dcol = dict(zip(desc_cols, col))
	    dcol['listed'] = 'X' if col[0] in (tinfo['columns'] + tinfo.get('extra_columns', [])) else ''
	    dcol['ask'] = 'X' if col[0] in tinfo.get('ask', []) else ''
	    dcol['readonly'] = 'X' if col[0] in tinfo.get('readonly', []) else ''
	    print "  %(Field)-20s %(Type)-12s %(Null)-5s %(Key)-5s %(listed)1s %(ask)1s %(readonly)1s %(Default)-5s %(Extra)-5s" % dcol
	print


cmds = [
    ('i', command_info, "info"),
]

@basics.command_line
def commands(pif):
    useful.cmd_proc(pif, './editor.py', cmds)

# ------- ----------------------------------------------------------

if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='')
