#!/usr/local/bin/python

import copy, os, urllib2
import basics
import mbdata
import useful


# ------- editor ---------------------------------------------------

# - presentation


def start(pif):
    if pif.form_bool('clear'):
        pif.dbh.clear_health()

    errs = pif.dbh.fetch_pages("health!=0")
    if errs:
        print '<hr>'
        print "<b>Errors found:<br><ul>"
        for err in errs:
            print "<li>", err['page_info.id']
        print "</ul>"
        print pif.render.format_button('clear', '?clear=1')

    table_list = []
    for table in pif.dbh.table_info:
        if 'ask' in pif.dbh.table_info[table]:
            table_list.append(table)
    table_list.sort()
    for table in table_list:
        print '<hr>'
        print '<b>' + table + '</b>'
        ask(pif, pif.dbh.get_table_info(table))


def ask(pif, table_info):
    print "<form>"
    print '<input type="hidden" name="table" value="%s">' % table_info['name']
    print pif.render.format_table_start()
    for ent in table_info['ask']:
        print pif.render.format_row_start()
        print pif.render.format_cell(0, ent)
        print pif.render.format_cell(1, '<input type="text" name="%s">' % ent)
        print pif.render.format_row_end()
    print pif.render.format_table_end()
    print pif.render.format_button_input("submit")
    print pif.render.format_button_input('add')
    print "</form>"


# primary entry

@basics.web_page
def editor_main(pif):
    pif.render.print_html()
    print pif.form, '<br>'
    pif.restrict('a')
    print pif.render.format_head(extra=pif.render.reset_button_js)
    show_table(pif)
    print pif.render.format_tail()


def show_table(pif):
    if not pif.form_str('table'):
        start(pif)
        return
    table_info = pif.dbh.get_table_info(pif.form_str('table'))
    print '<b>', table_info['name'], '</b>'
    print pif.render.format_button('show all', "?table=" + table_info['name'])
    print pif.form, '<br>'
    # DOES ANYBODY KNOW WHAT THE HELL I WAS THINKING HERE?
#    if len(pif.form) == 1 and table_info.get('ask'):
#       ask(pif, table_info)
#       return

    if pif.form_has('save'):
        pif.dbh.write(table_info['name'], {x: pif.form_str(x) for x in table_info['columns']},
                      pif.form_where(table_info['id'], 'o_'), modonly=True, tag='ShowTableSave')
        #del pif.form_del('id')
        print '<br>record saved<br>'
    elif pif.form_has('delete'):
        pif.dbh.delete(table_info['name'], pif.form_where(table_info['id'], 'o_'))
        pif.form_del('id')
        print '<br>record deleted<br>'
    elif pif.form_has('add'):
        print '<br>add', table_info.get('name', 'unset'), '<br>'
        print table_info, '<br>'
        adds = table_info.get('add', {})
        creat = table_info.get('create', {})
        cond = {}
        for id in creat:
            pif.form_def(id, creat[id])
            cond[id] = pif.form_str(id)
        print 'cond', cond, '<br>'
        print 'write', table_info['name'], cond
        lid = pif.dbh.write(table_info['name'], cond, newonly=True, tag='ShowTableAdd', verbose=1)
        if lid > 0:
            pif.form_set('id', lid)
        print 'lid', lid, '<br>'
        print '<br>record added<br>'
    elif pif.form_has('clone'):
        pif.dbh.write(table_info['name'], {x: pif.form_str(x) for x in table_info['columns']}, pif.form_where(table_info['id'], 'o_'), newonly=True, tag='ShowTableClone')
        #del pif.form_del('id')
        print '<br>record cloned<br>'
    where = pif.form_where(table_info['columns'])
    dats = pif.dbh.fetch(table_info['name'], where=where, tag='ShowTable')
    if pif.form_has('order'):
        dats.sort(key=lambda x: x[pif.form_str('order')])
    if len(dats) > 1:
        print len(dats), 'records'
        show_multi(pif, table_info, dats, showsubs=True)
        if table_info['name'] in table_info.get('add', {}):
            cond = {'add': '1'}
            print pif.render.format_button('add', "?table=" + table_info['name'] + "&" + "&".join([x + '=' + cond[x] for x in cond]))
    elif len(dats) == 1:
        show_single(pif, table_info, dats[0])
    else:
        show_none(pif, table_info, {x: pif.form_str(x) for x in table_info['columns']})
    return
    args = ''
    for col in table_info['columns']:
        if pif.form_has(col):
            args += '&' + pif.form_reformat([col])
    print '<a href="?table=' + table_info['name'] + '&add=1' + args + '">' + pif.render.format_button('add') + '</a>'


def show_multi(pif, table_info, dats, cols=None, showsubs=False):
    print '%s entries' % len(dats)
    if not cols:
        cols = table_info['columns']
    if pif.form_has('order'):
        sort_ord = pif.form_str('order')
        dats.sort(key=lambda x: x[sort_ord])
    print pif.render.format_table_start()
    print pif.render.format_row_start()
    for col in cols:
        if col not in table_info.get('hidden', []):
            print pif.render.format_cell(0, col)
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
        print '<input type="hidden" name="o_%s" value="%s">' % (f, dat[f])
    descs = pif.dbh.describe_dict(table_info['name'])
    print pif.render.format_table_start()
    for col in table_info['columns']:
        print pif.render.format_row_start()
        also = {}
        if col in table_info['id']:
            also = {'class': 'id'}
        print pif.render.format_cell(0, col, also=also)
        coltype = descs.get(col).get('type')
        print pif.render.format_cell(0, coltype, also=also)
        if col in table_info.get('clinks', {}):
            cond = {'table': table_info['clinks'][col]['tab']}
            for id in table_info['clinks'][col]['id']:
                fr, to = id.split('/')
                cond[fr] = str(dat[to])
            #print pif.render.format_cell(1, '<a href="?table=%s&%s">%s</a><br>' % (table_info['clinks'][col]['tab'], '&'.join(cond), dat[col]), also=also)
            print pif.render.format_cell(1, pif.render.format_link('', str(dat[col]), cond, also=also))
        else:
            print pif.render.format_cell(1, str(dat[col]), also=also)
        if col in table_info.get('readonly', []):
            print pif.render.format_cell(1, '&nbsp;<input type=hidden name="%s" value="%s">' % (col, dat[col]), also=also)
        elif coltype.startswith('varchar('):
            colwidth = int(coltype[8:-1])
            print pif.render.format_cell(1, pif.render.format_text_input(col, colwidth, colwidth, value=dat[col]), also=also)
        elif coltype.startswith('char('):
            colwidth = 1
            print pif.render.format_cell(1, pif.render.format_text_input(col, colwidth, colwidth, value=dat[col]), also=also)
        elif coltype.startswith('tinyint('):
            if dat[col] is None:
                dat[col] = 0
            colwidth = int(coltype[8:-1])
            val = dat[col]
            if isinstance(val, str) and val.isdigit():
                val = str(int(val))
            elif not val:
                val = '0'
            print pif.render.format_cell(1, pif.render.format_text_input(col, colwidth, colwidth, value=val), also=also)
        elif coltype.startswith('int('):
            if dat[col] is None:
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
            cond[fr] = dat[to]
        print pif.render.format_button('add', "?table=" + table_info['name'] + "&" + "&".join([x + '=' + cond[x] for x in cond]))
        del adds[table_info['name']]
        print pif.render.format_button_input('clone')
    print '</form>'
    for elink in table_info.get('elinks', []):
        print pif.render.format_link((elink['url'] % dat).lower(), elink['name']) + '<br>'

    print '<h3>Subtables</h3>'
    for subtab in table_info.get('tlinks', []):
        if not eval(subtab.get('if', '1')):
            continue
        #print "<hr>"
        print subtab['tab']

        if subtab['tab'] in adds:
            cond = dict()
            cond['add'] = '1'
            for id in adds[subtab['tab']]:
                fr, to = id.split('/')
                cond[fr] = dat[to]
            print pif.render.format_button('add', "?table=" + subtab['tab'] + "&" + "&".join([x + '=' + str(cond[x]) for x in cond]))
            del adds[subtab['tab']]

        cond = dict()
        if 'id' in subtab:
            for id in subtab['id']:
                fr, to = id.split('/')
                if to[0] == '*':
                    cond[fr] = eval(to[1:])
                else:
                    cond[fr] = dat[to]
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
    if table_info['name'] in adds:
        cond = {'add': '1'}
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
        cols = [table_info['name'] + '.' + x for x in table_info['columns']]
        lcond = {}
        for key in ref:
            lcond[key] = ref[key][0] + '.' + ref[key][1]
            cols.append(ref[key][0] + '.' + ref[key][2])
            tname += ',' + ref[key][0]  # this will break if we do two columns
        where = " and ".join([table_info['name'] + '.' + x + "='" + cond[x] + "'" for x in cond])
        if lcond:
            where += " and " + " and ".join([table_info['name'] + '.' + x + "=" + lcond[x] for x in lcond])
    else:
        cols = table_info['columns']
        where = " and ".join([table_info['name'] + '.' + x + "='" + str(cond[x]) + "'" for x in cond])
    dats = pif.dbh.fetch(tname, columns=cols, where=where, tag='show_sub_table')
    show_multi(pif, table_info, dats, cols)


# ------- mass -----------------------------------------------------


@basics.web_page
def mass_main(pif):
    if pif.form_str('type') == 'lineup':
        add_lineup_main(pif)
    else:
        pif.render.print_html()
        pif.restrict('a')
        print pif.render.format_head(extra=pif.render.reset_button_js)
        if pif.form_has('save'):
            mass_save(pif)
        elif pif.form_has('select'):
            mass_select(pif)
        else:
            mass_ask(pif)
        print pif.render.format_tail()


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


def mass_select(pif):
    columns = pif.form_str('select').split(',')
    table_info = pif.dbh.table_info[pif.form_str('from')]
    rows = pif.dbh.fetch(pif.form_str('from'), columns=columns + table_info['id'], where=pif.form_str('where'), order=pif.form_str('order'), tag='mass_select')
    print '<form method="post">'
    print '<input type="hidden" name="from" value="%s">' % pif.form_str('from')
    print '<input type="hidden" name="select" value="%s">' % pif.form_str('select')
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
                    256, 80, row[col]))
        print pif.render.format_row_end()

    print pif.render.format_table_end()
    print pif.render.format_button_input("save")
    print "</form>"


def mass_save(pif):
    columns = pif.form_str('select').split(',')
    table_info = pif.dbh.table_info[pif.form_str('from')]

    for key in pif.form_keys(has='.'):
        col, ids = key.split('.', 1)
        if col in columns:
            wheres = pif.dbh.make_where(dict(zip(table_info['id'], ids.split('.'))))
            # where = " and ".join(["%s='%s'" % x for x in wheres])
            # update table set col=value where condition;
            # query = "update %s set %s='%s' where %s" % (pif.form_str('from'), col, pif.dbh.escape_string(pif.form_str(key)), where)
            # print query, '<br>'
            # pif.dbh.raw_execute(query, tag='mass_save')
            # note: untested
            # note: write might already escape values
            pif.dbh.write(pif.form_str('from'), values={col: pif.dbh.escape_string(pif.form_str(key))}, where=wheres, modonly=True, tag='mass_save')


# ------- add lineup -----------------------------------------------


# TODO add base_id/casting_id for new castings
def add_lineup_main(pif):
    pif.render.print_html()
    pif.restrict('a')
    print pif.render.format_head(extra=pif.render.reset_button_js)
    if pif.form_has('save'):
        add_lineup_final(pif)
    elif pif.form_has('num'):
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
    print pif.render.format_tail()


def add_lineup_final(pif):
    pif.dbh.dbi.insert_or_update('page_info',
    {
        'id': pif.form_str('page_id'),
        'flags': 0,
        'health': '',
        'format_type': '',
        'title': '',
        'pic_dir': pif.form_str('picdir'),
        'tail': '',
        'description': '',
        'note': '',
    })
    pif.dbh.dbi.insert_or_update('section',
    {
        'id': pif.form_str('region'),
        'page_id': pif.form_str('page_id'),
        'display_order': 0,
        'category': 'man',
        'flags': 0,
        'name': pif.form_str('sec_title'),
        'columns': pif.form_int('cols', 4),
        'start': 0,
        'pic_dir': '',
        'disp_format': '%d.',
        'link_format': pif.form_str('link_fmt'),
        'img_format': '',
        'note': '',
    })

    for key in pif.form_keys(start='mod_id.'):
        num = key[7:]
        pif.dbh.dbi.insert_or_update('lineup_model',
        {
            'mod_id': pif.form_str(key),
            'number': num,
            'style_id': pif.form_str('style_id.' + num),
            'picture_id': '',
            'region': pif.form_str('region'),
            'year': pif.form_str('year'),
            'page_id': pif.form_str('page_id'),
            'name': pif.form_str('name.' + num),
        })


def add_lineup_list(pif):
    modlist = urllib2.urlopen(pif.form_str('models')).read().split('\n')
    castings = {x['base_id.rawname'].replace(';', ' '): x['base_id.id'] for x in pif.dbh.fetch_casting_list()}
    num_models = pif.form_int('num')
    year = pif.form_str('year')
    region = pif.form_str('region')
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
    cols = pif.dbh.table_info[table]['columns']
    wheres = []
    for col in cols:
        if pif.form_has(col):
            wheres.append(pif.form_reformat(col))
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
                    cond.append(fr + "=" + str(dat[to]))
                print pif.render.format_cell(1, '<a href="roam.cgi?table=%s&%s">%s</a><br>' % (clinks[col]['tab'], '&'.join(cond), dat[col]))
            else:
                print pif.render.format_cell(1, dat[col])
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
    table = pif.form_str('table', 'tables')
    pif.render.title = table

    print pif.render.format_head()
    if pif.form_has('table'):
        editor.roam_show_table(pif, table)
    else:
        editor.roam_select_table(pif)
    print pif.render.format_tail()


# ------- counters -------------------------------------------------


@basics.web_page
def show_counters(pif):
    pif.render.print_html()
    pif.restrict('a')
    print pif.render.format_head(extra=pif.render.reset_button_js)
    columns = ['ID', 'Value', 'Timestamp']
    res = pif.dbh.fetch_counters()
    sortorder = pif.form_str('s', 'id')
    revorder = pif.form_int('r')
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
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
