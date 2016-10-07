#!/usr/local/bin/python

import copy, os, re, urllib2
import basics
import config
import masses
import mbdata
import useful


# ------- editor ---------------------------------------------------

# - presentation


def editor_start(pif):
    if pif.form.get_bool('clear'):
        pif.dbh.clear_health()

    errs = pif.dbh.fetch_pages("health!=0")
    if errs:
        useful.warn('<hr>', "<b>Errors found:<br><ul>",
	    '\n'.join(["<li>" + err['page_info.id'] for err in errs]),
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
    if pif.form.get_str('table'):
	return show_table(pif)
    return editor_start(pif)


def show_table(pif):
    pif.render.message(str(pif.form.get_form()))

    table_info = pif.dbh.get_table_info(pif.form.get_str('table'))
    loaded = False
    if pif.form.has('save'):
        pif.dbh.write(table_info['name'], {x: pif.form.get_str(x) for x in table_info['columns'] + table_info.get('extra_columns', [])},
                      pif.form.where(table_info['id'], 'o_'), tag='ShowTableSave')
#modonly=True,
        #del pif.form.delete('id')
        pif.render.message('record saved')
    elif pif.form.has('delete'):
        pif.dbh.delete(table_info['name'], pif.form.where(table_info['id'], 'o_'))
        pif.form.delete('id')
        pif.render.message('record deleted')
    elif pif.form.has('add'):
        pif.render.message('add' + table_info.get('name', 'unset'))
#        print table_info, '<br>'
        adds = table_info.get('add', {})
        creat = table_info.get('create', {})
        cond = {}
        for id in creat:
            pif.form.default(id, creat[id])
            cond[id] = pif.form.get_str(id)
#        print 'cond', cond, '<br>'
#        print 'write', table_info['name'], cond
	dats = [cond]
	loaded = True
#        lid = pif.dbh.write(table_info['name'], cond, newonly=True, tag='ShowTableAdd', verbose=1)
#        if lid > 0:
#            pif.form.set_val('id', lid)
#        print 'lid', lid, '<br>'
#        print 'record added'
    elif pif.form.has('clone'):
        pif.dbh.write(table_info['name'], {x: pif.form.get_str(x) for x in table_info['columns'] + table_info.get('extra_columns', [])}, pif.form.where(table_info['id'], 'o_'), newonly=True, tag='ShowTableClone')
        #del pif.form.delete('id')
        pif.render.message('record cloned')
	pif.form.delete('clone')
    if not loaded:
	where = pif.form.where(table_info['columns'] + table_info.get('extra_columns', []))
	dats = pif.dbh.fetch(table_info['name'], where=where, tag='ShowTable', extras=True)

    footer = ''
    header = '<b>' + table_info['name'] + '</b>'
    header += pif.render.format_button('show all', "?table=" + table_info['name'])
    lsections = []

    if pif.form.has('order'):
        dats.sort(key=lambda x: x[pif.form.get_str('order')])
    if len(dats) > 1:
	lsections.append(show_multi_section(pif, table_info, dats, showsubs=True))
        if table_info['name'] in table_info.get('add', {}):
            cond = {'add': '1'}
            footer += pif.render.format_button('add', "?table=" + table_info['name'] + "&" + "&".join([x + '=' + cond[x] for x in cond]))
    elif len(dats) == 1:
        lsections.extend(show_single(pif, table_info, dats[0]))
    else:
        lsections.extend(show_none(pif, table_info, {x: pif.form.get_str(x) for x in table_info['columns'] + table_info.get('extra_columns', [])}))
    lsections[0]['header'] = header + lsections[0].get('header', '')
    lsections[0]['footer'] = lsections[0].get('footer', '') + footer
    llistix = {'section': lsections}
    return pif.render.format_template('simplelistix.html', llineup=llistix)
#    args = ''
#    for col in table_info['columns'] + table_info.get('extra_columns', []):
#        if pif.form.has(col):
#            args += '&' + pif.form.reformat([col])
#    print '<a href="?table=' + table_info['name'] + '&add=1' + args + '">' + pif.render.format_button('add') + '</a>'


def show_multi_section(pif, table_info, dats, cols=None, showsubs=False):
    if not cols:
        cols = table_info['columns'] + table_info.get('extra_columns', [])
    if pif.form.has('order'):
        sort_ord = pif.form.get_str('order')
        dats.sort(key=lambda x: x[sort_ord])

    columns = [col for col in cols if col not in table_info.get('hidden', [])]
    entries = []
    for dat in pif.dbh.depref(table_info['name'], dats):
	entry = {}
	for col in columns:
	    entry[col] = dat[col]
	    if col in table_info.get('clinks', {}):
		cond = []
		for id in table_info['clinks'][col]['id']:
		    fr, to = id.split('/')
		    cond.append(fr + "=" + str(dat[to]))
		entry[col] = '<a href="?table=%s&%s">%s</a>' % (table_info['clinks'][col]['tab'], '&'.join(cond), str(dat[col]))
	entries.append(entry)

    footer = ''
    if showsubs:
        for subtab in table_info.get('tlinks', []):
            if eval(subtab.get('if', '1')):
		footer += "<hr>" + subtab['tab'] + '\n' + pif.render.format_button('show', "?table=" + subtab['tab'])
    footer += '<hr>\n'

    lrange = {'entry': entries, 'styles': dict.fromkeys(table_info.get('id', []), '2')}
    lsection = {'columns': columns, 'range': [lrange], 'note': '',
	'headers': dict(zip(columns, columns)), 'header': '%s entries\n' % len(entries), 'footer': footer}
    return lsection


def show_single(pif, table_info, dat):
    dat = pif.dbh.depref(table_info['name'], dat)
    dats = [dat]
    adds = table_info.get('add', {})
    descs = pif.dbh.describe_dict(table_info['name'])

    header = '<form>\n'
    header += '<input type="hidden" name="verbose" value="1">\n'
    header += '<input type="hidden" name="table" value="%s">\n' % table_info['name']
    for f in table_info['id']:
        header += '<input type="hidden" name="o_%s" value="%s">\n' % (f, dat.get(f, ''))

    columns = ['column', 'type', 'value', 'new value']
    entries = []
#	    if col in table_info['id']:
#		also = {'class': 'id'}

    for col in table_info['columns'] + table_info.get('extra_columns', []):
	coltype = descs.get(col).get('type', 'unknown')

	oldvalue = str(dat.get(col, ''))
	if col in table_info.get('clinks', {}):
	    cond = {'table': table_info['clinks'][col]['tab']}
	    for id in table_info['clinks'][col]['id']:
		fr, to = id.split('/')
		cond[fr] = str(dat.get(to, ''))
	    oldvalue = pif.render.format_link('', oldvalue, cond)

	newvalue = coltype
	if col in table_info.get('readonly', []):
	    newvalue = '&nbsp;<input type=hidden name="%s" value="%s">' % (col, dat.get(col, ''))
	elif coltype.startswith('varchar('):
	    colwidth = int(coltype[8:-1])
	    newvalue = pif.render.format_text_input(col, colwidth, colwidth, value=dat.get(col))
	elif coltype.startswith('char('):
	    colwidth = 1
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
        cond = dict()
        cond['add'] = '1'
        for id in adds[table_info['name']]:
            fr, to = id.split('/')
            cond[fr] = dat.get(to, '')
        footer += pif.render.format_button('add', "?table=" + table_info['name'] + "&" + "&".join([x + '=' + cond[x] for x in cond]))
        del adds[table_info['name']]
        footer += pif.render.format_button_input('clone')
    footer += '</form>\n'
    for elink in table_info.get('elinks', []):
        footer += pif.render.format_link((elink['url'] % dat).lower(), elink['name']) + '<br>\n'
    footer += '<h3>Subtables</h3>\n'

    lrange = {'entry': entries, 'styles': {'column': 0}}
    lsections = [{'columns': columns, 'range': [lrange], 'note': '',
	'headers': dict(zip(columns, columns)), 'header': header, 'footer': footer}]

    anchors = []
    for subtab in table_info.get('tlinks', []):
	try:
	    if not eval(subtab.get('if', '1')):
		continue
	except:
	    continue
        #ostr += "<hr>"
        header = subtab['tab']

        if subtab['tab'] in adds:
            cond = dict()
            cond['add'] = '1'
            for id in adds[subtab['tab']]:
                fr, to = id.split('/')
                cond[fr] = dat.get(to, '')
            header += pif.render.format_button('add', "?table=" + subtab['tab'] + "&" + "&".join([x + '=' + str(cond[x]) for x in cond]))
            del adds[subtab['tab']]

        cond = dict()
        if 'id' in subtab:
            for id in subtab['id']:
                fr, to = id.split('/')
                if to[0] == '*':
                    cond[fr] = eval(to[1:])
                else:
                    cond[fr] = dat.get(to, '')
            lsection = show_sub_table_section(pif, pif.dbh.get_table_info(subtab['tab']), cond, ref=subtab.get('ref', {}))
            lsection['header'] = '<b>' + subtab['tab'] + '</b> ' + pif.render.format_button('show', "?table=" + subtab['tab'] + "&" + "&".join([x + '=' + str(cond[x]) for x in cond])) + '\n' + lsection['header']
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
    dats = []
    pif.render.message("No records found.")
    adds = table_info.get('add', {})
    cond = {'add': '1'}
    lsections = []
    if table_info['name'] in adds:
        for id in adds[table_info['name']]:
            fr, to = id.split('/')
            cond[fr] = dat.get(to, '')
        lsections.append({'header': pif.render.format_button('add', "?table=" + table_info['name'] + "&" + "&".join([x + '=' + cond[x] for x in cond]))})
        del adds[table_info['name']]
    for subtab in table_info.get('tlinks', []):
        if not eval(subtab.get('if', '1')):
            continue
        header = "<hr>" + subtab['tab']
        if subtab['tab'] in adds:
            header += pif.render.format_button('add', "?table=" + subtab['tab'] + "&" + "&".join([x + '=' + str(cond[x]) for x in cond]))
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
	lsection.append(lsection)
        if subtab['tab'] in adds:  #  ummmm?
            cond = {'add': '1'}
            for id in adds[subtab['tab']]:
                fr, to = id.split('/')
                cond[fr] = dat.get(to, '')
            del adds[subtab['tab']]
    #llistix = {'section': lsections}
    return lsections


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

# fixed = unicodedata.normalize('NFKD', unicode(crazy_town)).encode('ascii','ignore')
def printablize(lord):
    if isinstance(lord, dict):
	lord = [lord]
    for ent in lord:
	for key, val in ent.items():
	    if isinstance(val, str):
		val = unicode(val, errors='ignore')
	    else:
		val = str(val)
	    ent[key] = val
    return lord

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

    columns = ['id', 'value', 'timestamp']
    headers = dict(zip(columns, ['ID', 'Value', 'Timestamp']))
    lsection = dict(columns=columns, range=[{'entry': printablize(res)}], note='',
	headers={col: pif.render.format_link('?s=' + col +
	'&r=1' if col == sortorder and not revorder else '', headers[col]) for col in columns})
    return pif.render.format_template('simplelistix.html', llineup=dict(section=[lsection]))


# ------- ----------------------------------------------------------

def command_help(pif, *args):
    pif.render.message("./editor.py [i] ...")


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


command_lookup = {
    'i': command_info,
}

@basics.command_line
def commands(pif):
    if pif.filelist:
	command_lookup.get(pif.filelist[0], command_help)(pif, *pif.filelist[1:])
    else:
	command_help()

# ------- ----------------------------------------------------------

if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='')
