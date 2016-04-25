#!/usr/local/bin/python

import copy, os, re, urllib2
import basics
import config
import mbdata
import useful


# ------- editor ---------------------------------------------------

# - presentation


def editor_start(pif):
    if pif.form.get_bool('clear'):
        pif.dbh.clear_health()

    errs = pif.dbh.fetch_pages("health!=0")
    if errs:
        print '<hr>'
        print "<b>Errors found:<br><ul>"
        for err in errs:
            print "<li>", err['page_info.id']
        print "</ul></b>"
        print pif.render.format_button('clear', '?clear=1')

    print pif.render.format_button('mass', link='mass.cgi')
    print pif.render.format_button('lineup', link='mass.cgi?type=lineup')
    print pif.render.format_button('casting', link='mass.cgi?type=casting')
    print pif.render.format_button('var', link='mass.cgi?type=var')
    print pif.render.format_button('related', link='mass.cgi?type=related')
    print pif.render.format_button('pack', link='mass.cgi?type=pack')
    table_list = [t for t in pif.dbh.table_info if 'ask' in pif.dbh.table_info[t]]
    table_list.sort()
#    tabs = [table_list[:len(table_list) / 2], table_list[len(table_list) / 2:]]
    entries = list()
#    print '<table><tr>'
#    for col in (0, 1):
#	print '<td style="vertical-align: top; width: 50%;">'
#	for table in tabs[col]:
    for table in table_list:
	    entries.append({'text': '<b>' + table + '</b>' + editor_ask(pif, pif.dbh.get_table_info(table))})
#	print '</td>'
#    print '</tr></table>'
    lran = {'entry': entries}
    lsec = {'range': [lran], 'columns': 4}
    llineup = {'section': [lsec]}
    print pif.render.format_matrix(llineup)


def editor_ask(pif, table_info):
    ostr = "<form>"
    ostr += '<input type="hidden" name="table" value="%s">' % table_info['name']
    ostr += pif.render.format_table_start()
    for ent in table_info['ask']:
        ostr += pif.render.format_row_start()
        ostr += pif.render.format_cell(0, ent)
        ostr += pif.render.format_cell(1, '<input type="text" name="%s">' % ent)
        ostr += pif.render.format_row_end()
    ostr += pif.render.format_table_end()
    ostr += pif.render.format_button_input("submit")
    ostr += pif.render.format_button_input('add')
    ostr += "</form>"
    return ostr


# primary entry

@basics.web_page
def editor_main(pif):
    pif.render.print_html()
    print pif.form.get_form(), '<br>'
    pif.restrict('a')
    pif.render.set_page_extra(pif.render.reset_button_js)
    print pif.render.format_head()
    useful.header_done()
    show_table(pif)
    print pif.render.format_tail()


def show_table(pif):
    if not pif.form.get_str('table'):
        editor_start(pif)
        return
    table_info = pif.dbh.get_table_info(pif.form.get_str('table'))
    print '<b>', table_info['name'], '</b>'
    print pif.render.format_button('show all', "?table=" + table_info['name'])
    print pif.form.get_form(), '<br>'
    # DOES ANYBODY KNOW WHAT THE HELL I WAS THINKING HERE?
#    if len(pif.form.get_form()) == 1 and table_info.get('ask'):
#       editor_ask(pif, table_info)
#       return

    loaded = False
    if pif.form.has('save'):
        pif.dbh.write(table_info['name'], {x: pif.form.get_str(x) for x in table_info['columns'] + table_info.get('extra_columns', [])},
                      pif.form.where(table_info['id'], 'o_'), tag='ShowTableSave')
#modonly=True,
        #del pif.form.delete('id')
        print '<br>record saved<br>'
    elif pif.form.has('delete'):
        pif.dbh.delete(table_info['name'], pif.form.where(table_info['id'], 'o_'))
        pif.form.delete('id')
        print '<br>record deleted<br>'
    elif pif.form.has('add'):
        print '<br>add', table_info.get('name', 'unset'), '<br>'
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
#        print '<br>record added<br>'
    elif pif.form.has('clone'):
        pif.dbh.write(table_info['name'], {x: pif.form.get_str(x) for x in table_info['columns'] + table_info.get('extra_columns', [])}, pif.form.where(table_info['id'], 'o_'), newonly=True, tag='ShowTableClone')
        #del pif.form.delete('id')
        print '<br>record cloned<br>'
	pif.form.delete('clone')
    if not loaded:
	where = pif.form.where(table_info['columns'] + table_info.get('extra_columns', []))
	dats = pif.dbh.fetch(table_info['name'], where=where, tag='ShowTable')
    if pif.form.has('order'):
        dats.sort(key=lambda x: x[pif.form.get_str('order')])
    if len(dats) > 1:
        print len(dats), 'records'
        show_multi(pif, table_info, dats, showsubs=True)
        if table_info['name'] in table_info.get('add', {}):
            cond = {'add': '1'}
            print pif.render.format_button('add', "?table=" + table_info['name'] + "&" + "&".join([x + '=' + cond[x] for x in cond]))
    elif len(dats) == 1:
        show_single(pif, table_info, dats[0])
    else:
        show_none(pif, table_info, {x: pif.form.get_str(x) for x in table_info['columns'] + table_info.get('extra_columns', [])})
    return
    args = ''
    for col in table_info['columns'] + table_info.get('extra_columns', []):
        if pif.form.has(col):
            args += '&' + pif.form.reformat([col])
    print '<a href="?table=' + table_info['name'] + '&add=1' + args + '">' + pif.render.format_button('add') + '</a>'


def show_multi(pif, table_info, dats, cols=None, showsubs=False):
    print '%s entries' % len(dats)
    if not cols:
        cols = table_info['columns'] + table_info.get('extra_columns', [])
    if pif.form.has('order'):
        sort_ord = pif.form.get_str('order')
        dats.sort(key=lambda x: x[sort_ord])
    print pif.render.format_table_start()
    print pif.render.format_row_start()
    for col in cols:
        if col not in table_info.get('hidden', []):
            print pif.render.format_cell(0, col, hdr=True, also={'class': 'hd'})
    print pif.render.format_row_end()
    for dat in dats:
        dat = pif.dbh.depref(table_info['name'], dat)
        print pif.render.format_row_start()
        for col in cols:
            if col in table_info.get('hidden', []):
                pass
            if col in table_info.get('clinks', {}):
                cond = []
                for id in table_info['clinks'][col]['id']:
                    fr, to = id.split('/')
                    cond.append(fr + "=" + str(dat[to]))
                print pif.render.format_cell(1, '<a href="?table=%s&%s">%s</a><br>' % (table_info['clinks'][col]['tab'], '&'.join(cond), str(dat[col])))
            else:
                print pif.render.format_cell(1, str(dat.get(col, '')))
        print pif.render.format_row_end()
    print pif.render.format_table_end()

    if showsubs:
        for subtab in table_info.get('tlinks', []):
            if not eval(subtab.get('if', '1')):
                continue
            print "<hr>", subtab['tab']
            print pif.render.format_button('show', "?table=" + subtab['tab'])

    print '<hr>'


def show_single(pif, table_info, dat):
    dat = pif.dbh.depref(table_info['name'], dat)
    dats = [dat]
    adds = table_info.get('add', {})
    print '<form>'
    print '<input type="hidden" name="verbose" value="1">'
    print '<input type="hidden" name="table" value="%s">' % table_info['name']
    for f in table_info['id']:
        print '<input type="hidden" name="o_%s" value="%s">' % (f, dat.get(f, ''))
    descs = pif.dbh.describe_dict(table_info['name'])
    print pif.render.format_table_start()
    for col in table_info['columns'] + table_info.get('extra_columns', []):
        print pif.render.format_row_start()
        also = {}
        if col in table_info['id']:
            also = {'class': 'id'}
        print pif.render.format_cell(0, col, also={'class': 'hd'})
        coltype = descs.get(col).get('type')
        print pif.render.format_cell(0, coltype, also=also)
        if col in table_info.get('clinks', {}):
            cond = {'table': table_info['clinks'][col]['tab']}
            for id in table_info['clinks'][col]['id']:
                fr, to = id.split('/')
                cond[fr] = str(dat.get(to, ''))
            #print pif.render.format_cell(1, '<a href="?table=%s&%s">%s</a><br>' % (table_info['clinks'][col]['tab'], '&'.join(cond), dat.get(col, '')), also=also)
            print pif.render.format_cell(1, pif.render.format_link('', str(dat.get(col, '')), cond, also=also))
        else:
            print pif.render.format_cell(1, str(dat.get(col, '')), also=also)
        if col in table_info.get('readonly', []):
            print pif.render.format_cell(1, '&nbsp;<input type=hidden name="%s" value="%s">' % (col, dat.get(col, '')), also=also)
        elif coltype.startswith('varchar('):
            colwidth = int(coltype[8:-1])
            print pif.render.format_cell(1, pif.render.format_text_input(col, colwidth, colwidth, value=dat.get(col)), also=also)
        elif coltype.startswith('char('):
            colwidth = 1
            print pif.render.format_cell(1, pif.render.format_text_input(col, colwidth, colwidth, value=dat.get(col, '')), also=also)
        elif coltype.startswith('tinyint('):
            if dat.get(col) is None:
                dat[col] = 0
            colwidth = int(coltype[8:-1])
            val = dat[col]
            if isinstance(val, str) and val.isdigit():
                val = str(int(val))
            elif not val:
                val = '0'
            print pif.render.format_cell(1, pif.render.format_text_input(col, colwidth, colwidth, value=val), also=also)
        elif coltype.startswith('smallint('):
            if dat.get(col) is None:
                dat[col] = 0
            colwidth = int(coltype[9:-1])
            val = dat[col]
            if isinstance(val, str) and val.isdigit():
                val = str(int(val))
            elif not val:
                val = '0'
            print pif.render.format_cell(1, pif.render.format_text_input(col, colwidth, colwidth, value=val), also=also)
        elif coltype.startswith('int('):
            if dat.get(col) is None:
                dat[col] = 0
            colwidth = int(coltype[4:-1])
            val = dat[col]
            if isinstance(val, str) and val.isdigit():
                val = int(val)
            elif not val:
                val = 0
            print pif.render.format_cell(1, pif.render.format_text_input(col, colwidth, colwidth, value=str(val)), also=also)
        else:
            print pif.render.format_cell(1, coltype, also=also)
        print pif.render.format_row_end()
    print pif.render.format_table_end()
    print pif.render.format_button_input("save")
    print pif.render.format_button_input("delete")
    if table_info['name'] in adds:
        cond = dict()
        cond['add'] = '1'
        for id in adds[table_info['name']]:
            fr, to = id.split('/')
            cond[fr] = dat.get(to, '')
        print pif.render.format_button('add', "?table=" + table_info['name'] + "&" + "&".join([x + '=' + cond[x] for x in cond]))
        del adds[table_info['name']]
        print pif.render.format_button_input('clone')
    print '</form>'
    for elink in table_info.get('elinks', []):
        print pif.render.format_link((elink['url'] % dat).lower(), elink['name']) + '<br>'

    print '<h3>Subtables</h3>'
    for subtab in table_info.get('tlinks', []):
	try:
	    if not eval(subtab.get('if', '1')):
		continue
	except:
	    continue
        #print "<hr>"
        print subtab['tab']

        if subtab['tab'] in adds:
            cond = dict()
            cond['add'] = '1'
            for id in adds[subtab['tab']]:
                fr, to = id.split('/')
                cond[fr] = dat.get(to, '')
            print pif.render.format_button('add', "?table=" + subtab['tab'] + "&" + "&".join([x + '=' + str(cond[x]) for x in cond]))
            del adds[subtab['tab']]

        cond = dict()
        if 'id' in subtab:
            for id in subtab['id']:
                fr, to = id.split('/')
                if to[0] == '*':
                    cond[fr] = eval(to[1:])
                else:
                    cond[fr] = dat.get(to, '')
            print pif.render.format_button('show', "?table=" + subtab['tab'] + "&" + "&".join([x + '=' + str(cond[x]) for x in cond]))
            show_sub_table(pif, pif.dbh.get_table_info(subtab['tab']), cond, ref=subtab.get('ref', {}))
        else:
            print pif.render.format_button('show', "?table=" + subtab['tab'])
#       if subtab['tab'] in adds:
#           print pif.render.format_button('add', "?table=" + subtab['tab'] + "&" + "&".join([x + '=' + str(cond[x]) forx in cond]))

    print '<hr>'


def show_none(pif, table_info, dat):
    dats = []
    print "No records found.<br>"
    adds = table_info.get('add', {})
    cond = {'add': '1'}
    if table_info['name'] in adds:
        for id in adds[table_info['name']]:
            fr, to = id.split('/')
            cond[fr] = dat.get(to, '')
        print pif.render.format_button('add', "?table=" + table_info['name'] + "&" + "&".join([x + '=' + cond[x] for x in cond]))
        del adds[table_info['name']]
    for subtab in table_info.get('tlinks', []):
        if not eval(subtab.get('if', '1')):
            continue
        print "<hr>", subtab['tab']
        if subtab['tab'] in adds:
            print pif.render.format_button('add', "?table=" + subtab['tab'] + "&" + "&".join([x + '=' + str(cond[x]) for x in cond]))
        cond = {}
        if 'id' in subtab:
            for id in subtab['id']:
                fr, to = id.split('/')
                if to[0] == '*':
                    cond[fr] = eval(to[1:])
                else:
                    cond[fr] = dat.get(to, '')
            print pif.render.format_button('show', "?table=" + subtab['tab'] + "&" +
                                           "&".join([x + '=' + str(cond[x]) for x in cond]))
            show_sub_table(pif, pif.dbh.get_table_info(subtab['tab']), cond, ref=subtab.get('ref', {}))
        else:
            print pif.render.format_button('show', "?table=" + subtab['tab'])
        if subtab['tab'] in adds:
            cond = {'add': '1'}
            for id in adds[subtab['tab']]:
                fr, to = id.split('/')
                cond[fr] = dat.get(to, '')
            del adds[subtab['tab']]


def show_sub_table(pif, table_info, cond, ref={}):
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
    dats = pif.dbh.fetch(tname, columns=cols, where=where, tag='show_sub_table')
    show_multi(pif, table_info, dats, cols)


# ------- roam -----------------------------------------------------


def roam_select_table(pif):
    tnames = [''] + pif.dbh.table_info.keys()
    tnames.sort()
    print "<form>"
    print "Table:"
    print pif.render.format_select("table", zip(tnames, tnames))
    print pif.render.format_button_input()
    print "</form>"


def roam_show_table(pif, table):
    clinks = pif.dbh.table_info[table].get('clinks', {})
    tlinks = pif.dbh.table_info[table].get('tlinks', [])
    where = ''
    cols = pif.dbh.table_info[table]['columns'] + table_info.get('extra_columns', [])
    wheres = []
    for col in cols:
        if pif.form.has(col):
            wheres.append(pif.form.reformat(col))
    dats = pif.dbh.fetch(table, where=" and ".join(wheres), tag='Roam')

    if len(dats) > 1:
        roam_show_multi(pif, cols, dats, clinks, tlinks)
    elif len(dats) == 1:
        roam_show_single(pif, cols, dats[0], clinks, tlinks)
    else:
        print "No records found."


def roam_show_multi(pif, cols, dats, clinks, tlinks):
    print pif.render.format_table_start()
    print pif.render.format_row_start()
    for col in cols:
        print pif.render.format_cell(0, col)
    for tlink in tlinks:
        print pif.render.format_cell(0, tlink['tab'])
    print pif.render.format_row_end()
    for dat in dats:
        print pif.render.format_row_start()
        for col in cols:
            if col in clinks:
                cond = []
                for id in clinks[col]['id']:
                    fr, to = id.split('/')
                    cond.append(fr + "=" + str(dat.get(to, '')))
                print pif.render.format_cell(1, '<a href="roam.cgi?table=%s&%s">%s</a><br>' % (clinks[col]['tab'], '&'.join(cond), dat.get(col, '')))
            else:
                print pif.render.format_cell(1, dat.get(col, ''))
        for tlink in tlinks:
            cond = []
            for id in tlink['id']:
                fr, to = id.split('/')
                cond.append(fr + "=" + dat[to])
            print pif.render.format_cell(1, '<a href="roam.cgi?table=%s&%s">%s</a><br>' % (tlink['tab'], '&'.join(cond), tlink['tab']))
        print pif.render.format_row_end()
    print pif.render.format_table_end()


def roam_show_single(pif, cols, dat, clinks, tlinks):
    print pif.render.format_table_start()
    for col in cols:
        print pif.render.format_row_start()
        print pif.render.format_cell(0, col)
        if col in clinks:
            cond = []
            for id in clinks[col]['id']:
                fr, to = id.split('/')
                cond.append(fr + "=" + dat[to])
            print pif.render.format_cell(1, '<a href="roam.cgi?table=%s&%s">%s</a><br>' % (clinks[col]['tab'], '&'.join(cond), dat[col]))
        else:
            print pif.render.format_cell(1, dat[col])
        print pif.render.format_row_end()
    print pif.render.format_table_end()

    print '<p>'
    for tlink in tlinks:
        cond = []
        for id in tlink['id']:
            fr, to = id.split('/')
            cond.append(fr + "=" + dat[to])
        print '<a href="roam.cgi?table=%s&%s">%s</a><br>' % (tlink['tab'], '&'.join(cond), tlink['tab'])


# not the tip of an iceberg
@basics.web_page
def roam_main(pif):
    os.environ['PATH'] += ':/usr/local/bin'
    pif.render.print_html()
    pif.restrict('a')
    table = pif.form.get_str('table', 'tables')
    pif.render.title = table

    print pif.render.format_head()
    useful.header_done()
    if pif.form.has('table'):
        editor.roam_show_table(pif, table)
    else:
        editor.roam_select_table(pif)
    print pif.render.format_tail()


# ------- counters -------------------------------------------------


@basics.web_page
def show_counters(pif):
    pif.render.print_html()
    pif.restrict('a')
    pif.render.set_page_extra(pif.render.reset_button_js)
    print pif.render.format_head()
    useful.header_done()
    columns = ['ID', 'Value', 'Timestamp']
    res = pif.dbh.fetch_counters()
    sortorder = pif.form.get_str('s', 'id')
    revorder = pif.form.get_int('r')
    res.sort(key=lambda x: x['counter.' + sortorder.lower()])
    if revorder:
        res.reverse()
    print pif.render.format_table_start()
    print pif.render.format_row_start()
    for col in columns:
        if col == sortorder and not revorder:
            print pif.render.format_cell(0, pif.render.format_link('?s=' + col + '&r=1', col), hdr=True)
        else:
            print pif.render.format_cell(0, pif.render.format_link('?s=' + col, col), hdr=True)
    print pif.render.format_row_end()
    for row in res:
        print pif.render.format_row_start()
        for col in columns:
            print pif.render.format_cell(0, row['counter.' + col.lower()])
        print pif.render.format_row_end()
    print pif.render.format_table_end()
    print pif.render.format_tail()


# ------- ----------------------------------------------------------


if __name__ == '__main__':  # pragma: no cover
    basics.goaway()
