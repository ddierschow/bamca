#!/usr/local/bin/python

import basics
import imglib
import masses
import render
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
                    "</ul></b>", pif.ren.format_button_link('clear', '?clear=1'))

    context = {
        'table_data': pif.dbh.table_data,
        'asks': sorted([t.name for t in pif.dbh.table_data.values() if t.ask]),
        'masses': [x[0] for x in masses.mass_mains_list],
    }
    return pif.ren.format_template('editorask.html', **context)


# primary entry

@basics.web_page
def editor_main(pif):
    pif.dbh.dbi.logger.info('form {}'.format(pif.form.get_form()))
    pif.ren.set_page_extra(pif.ren.reset_button_js)
    pif.ren.print_html()
    pif.restrict('a')
    if pif.form.get_raw('promote'):
        return imglib.promote_picture(pif, pif.form.get_raw('mod'), pif.form.get_raw('var'))
    if pif.form.get_raw('table'):
        return show_table(pif)
    return editor_start(pif)


def show_table(pif):
    pif.ren.message(str(pif.form.get_form()))
    table_data = pif.dbh.get_table_data(pif.form.get_raw('table'))

    def save_val(key):
        return pif.form.get_bits(key) if key in table_data.bits else pif.form.get_raw(key)

    dats = []
    if pif.duplicate_form:  # not pif.dbh.insert_token(pif.form.get_raw('token')):
        print('duplicate form submission detected')
    elif not table_data:
        print('table not found')
        return
    elif pif.form.has('save'):
        # rec['flags'] = sum(int(x, 16) for x in pif.form.get_list('base_id.flags'))
        values = {x: save_val(x) for x in table_data.columns + table_data.extra_columns
                  if save_val(x) or table_data.saveid or x not in table_data.id}
        pif.dbh.write(
            table_data.name, values, pif.form.where(table_data.id, 'o_'), tag='ShowTableSave', verbose=True)
        pif.ren.message('record saved')
    elif pif.form.has('delete'):
        pif.dbh.delete(table_data.name, pif.form.where(table_data.id, 'o_'))
        pif.form.delete('id')
        pif.ren.message('record deleted')
    elif pif.form.has('clone'):
        # this should be done in memory without saving yet
        values = {x: save_val(x) for x in table_data.columns + table_data.extra_columns
                  if save_val(x) or table_data.saveid or x not in table_data.id}
        pif.dbh.write(
            table_data.name, values, pif.form.where(table_data.id, 'o_'), newonly=True, tag='ShowTableClone')
        # del pif.form.delete('id')
        pif.ren.message('record cloned')
        pif.form.delete('clone')
    elif pif.form.has('add'):
        pif.ren.message('add' + (table_data.name or 'unset'))
#        print(table_data, '<br>')
        # adds = table_data.add
        creat = table_data.create
        cond = {}
        for id in table_data.columns:
            pif.form.default(id, creat.get(id, save_val(id)))
            cond[id] = save_val(id)
        dats = [cond]
        print('new record')

    if not dats:
        where = pif.form.where(table_data.columns + table_data.extra_columns)
        dats = pif.dbh.fetch(table_data.name, where=where, tag='ShowTable', extras=True)

    header = footer = ''
#    header = '<b>' + table_data.name + '</b>'
#    header += pif.ren.format_button_link('show all', "?table=" + table_data.name)
    lsections = []

    if len(dats) > 1:
        lsections.extend(show_multi(pif, table_data, dats))
    elif len(dats) == 1:
        lsections.extend(show_single(pif, table_data, dats))
    else:
        lsections.extend(show_none(
            pif, table_data, {x: save_val(x) for x in table_data.columns + table_data.extra_columns}))
    if table_data.name in table_data.add:
        cond = {'add': '1'}
        footer += pif.ren.format_button_link(
            'add', "?table=" + table_data.name + "&" + "&".join([x + '=' + cond[x] for x in cond]))
    lsections[0].header = header + lsections[0].header
    lsections[0].footer += footer
    lsections.extend(show_sub_tables(pif, table_data, dats[0] if len(dats) == 1 else None))
    llistix = render.Listix(section=lsections)
    return pif.ren.format_template('simplelistix.html', llineup=llistix)


def show_multi(pif, table_data, dats, cols=None):
    if pif.form.has('order') and dats:
        sort_ord = table_data.name + '.' + pif.form.get_raw('order')
        if sort_ord in dats[0]:
            dats.sort(key=lambda x: x[sort_ord])
    lsections = [show_multi_section(pif, table_data, dats, cols)]
    return lsections


def show_single(pif, table_data, dats):
    dat = pif.dbh.depref(table_data.name, dats[0])
    dats = [dat]
    adds = table_data.add
    descs = pif.dbh.describe_dict(table_data.name)

    lsections = []
    for base_tab, base_rel in table_data.extends.items():
        base_dat = pif.dbh.get_table_data(base_tab)
        base_rel = base_rel.split('/')
        base_where = '{}="{}"'.format(base_rel[1], dat[base_rel[0]])
        base_dats = pif.dbh.fetch(base_dat.name, where=base_where, tag='ShowBaseTable', extras=True)
        if len(base_dats) > 1:
            pif.ren.message('multiple instances of', base_tab, '!')
        elif not base_dats:
            pif.ren.message('no instances of', base_tab, '!')
        else:
            lsections.extend(show_single(pif, base_dat, base_dats))

    header = '<b>' + table_data.name + '</b>'
    header += pif.ren.format_button_link('show all', "?table=" + table_data.name)
    header += '<form action="/cgi-bin/editor.cgi">\n'
    header += pif.create_token()
    header += '<input type="hidden" name="verbose" value="1">\n'
    header += '<input type="hidden" name="table" value="{}">\n'.format(table_data.name)
    for f in table_data.id:
        header += '<input type="hidden" name="o_{}" value="{}">\n'.format(f, dat.get(f, ''))

    columns = ['column', 'type', 'value', 'new value']
    entries = []

    for col in table_data.columns + table_data.extra_columns:
        coltype = descs.get(col).get('type', 'unknown')
        oldvalue = make_col_value(table_data, col, dat)
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
        if col in table_data.readonly:
            newvalue = '&nbsp;<input type=hidden name="{}" value="{}">'.format(col, dat.get(col, ''))
        elif col in table_data.bits:
            newvalue = pif.form.put_checkbox(
                col, table_data.bits[col], useful.bit_list(oldvalue, format='%04x'))
        elif coltype == 'text':
            newvalue = pif.form.put_textarea_input(col, value=dat.get(col, ''))
        elif coltype.startswith('varchar('):
            colwidth = int(coltype[8:-1])
            newvalue = pif.form.put_text_input(col, colwidth, colwidth, value=dat.get(col, ''))
        elif coltype.startswith('char('):
            colwidth = int(coltype[5:-1])
            newvalue = pif.form.put_text_input(col, colwidth, colwidth, value=dat.get(col, ''))
        elif coltype.startswith('tinyint('):
            if dat.get(col) is None:
                dat[col] = 0
            colwidth = int(coltype[8:-1])
            val = dat[col]
            if isinstance(val, str) and val.isdigit():
                val = str(int(val))
            elif not val:
                val = '0'
            newvalue = pif.form.put_text_input(col, colwidth, colwidth, value=val)
        elif coltype.startswith('smallint('):
            if dat.get(col) is None:
                dat[col] = 0
            colwidth = int(coltype[9:-1])
            val = dat[col]
            if isinstance(val, str) and val.isdigit():
                val = str(int(val))
            elif not val:
                val = '0'
            newvalue = pif.form.put_text_input(col, colwidth, colwidth, value=val)
        elif coltype.startswith('int('):
            if dat.get(col) is None:
                dat[col] = 0
            colwidth = int(coltype[4:-1])
            val = dat[col]
            if isinstance(val, str) and val.isdigit():
                val = int(val)
            elif not val:
                val = 0
            newvalue = pif.form.put_text_input(col, colwidth, colwidth, value=str(val))
        entries.append({'column': col, 'type': coltype, 'value': oldvalue, 'new value': newvalue})

    footer = pif.form.put_button_input("save")
    footer += pif.form.put_button_input("delete")

    if table_data.name in adds:
        footer += pif.ren.format_button_link(
            'add', "?table=" + table_data.name + "&add=1&" + make_url_cond(adds[table_data.name], dat))
        del adds[table_data.name]
        footer += pif.form.put_button_input('clone')
    footer += '</form>\n'
    for elink in table_data.elinks:
        footer += pif.ren.format_button_link(elink['name'], elink['url'] % dat) + '<br>\n'
    footer += '<hr>\n'

    lrange = render.Range(entry=entries, styles={'column': 0})
    lsections.append(render.Section(colist=columns, range=[lrange], header=header, footer=footer))
    return lsections


def show_sub_tables(pif, table_data, dat=None):
    columns = ['column', 'type', 'value', 'new value']
    adds = table_data.add
    lsections = []
    lsections.append(render.Section(colist=[], header='<h3>Subtables</h3>\n'))

    anchors = []
    for subtab in table_data.tlinks:
        if subtab['tab'] in table_data.extends:
            continue
        try:
            if not eval(subtab.get('if', '1')):
                continue
        except Exception:
            continue
        # ostr += "<hr>"
        header = '<b>' + subtab['tab'] + '</b>'

        if dat and subtab['tab'] in adds:
            header += pif.ren.format_button_link('add', "?table=" + subtab['tab'] + "&" +
                                                 make_url_cond(adds[subtab['tab']], dat))
            del adds[subtab['tab']]

        cond = dict()
        if dat and 'id' in subtab:
            cond = make_cond(subtab['id'], dat)
            lsection = show_sub_table_section(
                pif, pif.dbh.get_table_data(subtab['tab']), cond, ref=subtab.get('ref', {}))
            lsection.header = header + pif.ren.format_button_link(
                'show', "?table=" + subtab['tab'] + "&" + "&".join([
                    x + '=' + str(cond[x]) for x in cond])) + '\n' + lsection.header
        else:
            header += pif.ren.format_button_link('show', "?table=" + subtab['tab'])
            # if subtab['tab'] in adds:
            #     ostr += pif.ren.format_button_link('add', "?table=" + subtab['tab'] + "&" + "&".join([
            #         x + '=' + str(cond[x]) forx in cond]))
            lsection = render.Section(colist=columns, range=[render.Range(entry=[], styles={'column': 0})],
                                      header=header)
        lsection.anchor = subtab['tab']
        anchors.append(subtab['tab'])
        lsections.append(lsection)

    return lsections


def show_none(pif, table_data, dat):
    pif.ren.message("No records found.")
    adds = table_data.add
    header = '<b>' + table_data.name + '</b>'
    header += pif.ren.format_button_link('show all', "?table=" + table_data.name)
    lsections = []
    lsections.append(render.Section(header=header))
    if table_data.name in adds:
        cond = make_url_cond(adds[table_data.name], dat)
        lsections.append(render.Section(
            header=pif.ren.format_button_link('add', "?table=" + table_data.name + "&add=1&" + cond)))
        del adds[table_data.name]
    for subtab in table_data.tlinks:
        if not eval(subtab.get('if', '1')):
            continue
        header = "<hr>" + subtab['tab']
        # if subtab['tab'] in adds:
        #     header += pif.ren.format_button_link('add', "?table=" + subtab['tab'] + "&add=1&" + "&".join([
        #         x + '=' + str(cond[x]) for x in cond]))
        cond = {}
        if 'id' in subtab:
            for id in subtab['id']:
                fr, to = id.split('/')
                if to[0] == '*':
                    cond[fr] = eval(to[1:])
                else:
                    cond[fr] = dat.get(to, '')
            lsection = show_sub_table_section(pif, pif.dbh.get_table_data(subtab['tab']), cond,
                                              ref=subtab.get('ref', {}))
            lsection.header = '{}{}\n{}'.format(
                header, pif.ren.format_button_link(
                    'show', "?table=" + subtab['tab'] + "&" + "&".join([x + '=' + str(cond[x]) for x in cond])),
                lsection.header)
        else:
            lsection = render.Section(header=header + pif.ren.format_button_link('show', "?table=" + subtab['tab']))
        lsections.append(lsection)
        if subtab['tab'] in adds:  # ummmm?
            cond = {'add': '1'}
            for id in adds[subtab['tab']]:
                fr, to = id.split('/')
                cond[fr] = dat.get(to, '')
            del adds[subtab['tab']]
    # llistix = {'section': lsections}
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
    return '&'.join(['{}={}'.format(*x) for x in cond.items()])


def make_col_value(table_data, col, dat):
    val = dat.get(col, '')
    if col in table_data.id:
        return '<a href="?table={}&{}">{}</a>'.format(table_data.name, make_url_cond(table_data.id, dat), val)
    elif col in table_data.clinks:
        return '<a href="?table={}&{}">{}</a>'.format(table_data.clinks[col]['tab'],
                                                      make_url_cond(table_data.clinks[col]['id'], dat), val)
    return val


def show_multi_section(pif, table_data, dats, cols=None):
    columns = [
        col for col in (cols if cols else table_data.columns + table_data.extra_columns)
        if col not in table_data.hidden]
    entries = [
        {x: make_col_value(table_data, x, dat) for x in columns}
        for dat in pif.dbh.depref(table_data.name, dats)
    ]

    header = ''  # '<b>' + table_data.name + '</b>\n'
    header += pif.ren.format_button_link('show all', "?table=" + table_data.name)
    header += '\n{} entries\n'.format(len(entries))

    lsection = render.Section(
        colist=columns, header=header, footer='<hr>\n',
        range=[{'entry': entries, 'styles': dict.fromkeys(table_data.id, '2')}])
    return lsection


def show_sub_table_section(pif, table_data, cond, ref={}):
    # need to make this handle subtab['ref']
    # {'tab': 'detail', 'id': ['mod_id/mod_id', 'var_id/var'],
    #  'ref': {'attr_id': ['attribute', 'id', 'attribute_name']}},
    # so in this case: ref = {'attr_id': ['attribute', 'id', 'attribute_name']}
    tname = table_data.name
    if ref:
        cols = [table_data.name + '.' + x for x in table_data.columns + table_data.extra_columns]
        lcond = {}
        for key in ref:
            lcond[key] = ref[key][0] + '.' + ref[key][1]
            cols.append(ref[key][0] + '.' + ref[key][2])
            tname += ',' + ref[key][0]  # this will break if we do two columns
        where = " and ".join([table_data.name + '.' + x + "='" + cond[x] + "'" for x in cond])
        if lcond:
            where += " and " + " and ".join([table_data.name + '.' + x + "=" + lcond[x] for x in lcond])
    else:
        cols = table_data.columns + table_data.extra_columns
        where = " and ".join([table_data.name + '.' + x + "='" + str(cond[x]) + "'" for x in cond])
    dats = pif.dbh.fetch(tname, columns=cols, where=where, tag='show_sub_table_section')
    return show_multi_section(pif, table_data, dats, cols)


# ------- counters -------------------------------------------------


@basics.web_page
def show_counters(pif):
    pif.ren.print_html()
    pif.restrict('a')
    pif.ren.set_page_extra(pif.ren.reset_button_js)

    res = pif.dbh.depref('counter', pif.dbh.fetch_counters())
    sortorder = pif.form.get_raw('s', 'id')
    revorder = pif.form.get_int('r')
    res.sort(key=lambda x: x[sortorder])
    if revorder:
        res.reverse()

    columns = ['id', 'value', 'timestamp', 'health']
    headers = dict(zip(columns, ['ID', 'Value', 'Timestamp', 'Health']))
    lsection = render.Section(
        colist=columns, range=[render.Range(entry=useful.printablize(res))], note='',
        headers={col: pif.ren.format_link('?s=' + col + '&r=1' if col == sortorder and not revorder else '',
                                          headers[col]) for col in columns})
    return pif.ren.format_template('simplelistix.html', llineup=render.Listix(section=[lsection]))


# ------- ----------------------------------------------------------


def command_info(pif):
    desc_cols = ['Field', 'Type', 'Null', 'Key', 'Default', 'Extra']
    cfmt = "  %(Field)-20s %(Type)-12s %(Null)-5s %(Key)-5s %(listed)1s %(ask)1s %(ro)1s %(Default)-5s %(Extra)-5s"
    tabs = pif.dbh.fetch_tables()
    for table in tabs[0]:
        print(table[0])
        tdata = pif.dbh.get_table_data(table[0])
        tab = pif.dbh.fetch_table(table[0])
        for col in tab[0]:
            dcol = dict(zip(desc_cols, col))
            dcol['listed'] = 'X' if col[0] in (tdata.columns + tdata.extra_columns) else ''
            dcol['ask'] = 'X' if col[0] in tdata.ask else ''
            dcol['ro'] = 'X' if col[0] in tdata.readonly else ''
            print(cfmt % dcol)
        print()


cmds = [
    ('i', command_info, "info"),
]


# ------- ----------------------------------------------------------


if __name__ == '__main__':  # pragma: no cover
    basics.process_command_list(cmds=cmds, dbedit='')
