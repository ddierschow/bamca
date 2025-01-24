#!/usr/local/bin/python

import os
import re
import urllib

import basics
import config
import images
import mannum
import mbdata
import render
import tables
import useful


# ------- mass -----------------------------------------------------


@basics.web_page
def mass(pif):
    pif.render.print_html()
    pif.restrict('am')
    pif.render.set_page_extra(pif.render.reset_button_js + pif.render.toggle_display_js)

    mass_type = pif.form.get_raw('tymass')
    return dict(mass_mains_list).get(mass_type, mass_mains_hidden.get(mass_type, mass_main))(pif)


def mass_main(pif):
    if pif.duplicate_form:
        print('duplicate form submission detected')
    elif pif.form.has('save'):
        return mass_save(pif)
    elif pif.form.has('select'):
        return mass_select(pif)
    return mass_ask(pif)


def mass_ask(pif):
    # header = '<form method="post">' + pif.create_token()
    header = pif.form.put_form_start(method='post', token=pif.dbh.create_token())

    rows = ['select', 'table', 'where', 'order']
    entries = [{'title': row, 'value': pif.form.put_text_input(row, 256, 80)} for row in rows]

    footer = pif.form.put_hidden_input(verbose=1)
    footer += pif.form.put_button_input()
    footer += "</form>"
    footer += mass_sections(pif)

    lsection = render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)], noheaders=True,
                              header=header, footer=footer)
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=[lsection]), nofooter=True)


def mass_select(pif):
    # Get table descriptions and use widths.  Allow "*".
    columns = pif.form.get_raw('select').split(',')
    table_data = pif.dbh.get_table_data(pif.form.get_raw('table'))
    rows = pif.dbh.fetch(pif.form.get_raw('table'), columns=columns + table_data.id, where=pif.form.get_raw('where'),
                         order=pif.form.get_raw('order'), tag='mass_select')
    header = pif.form.put_form_start(method='post', token=pif.dbh.create_token())
    header += pif.form.put_hidden_input(table=pif.form.get_raw('table'), select=pif.form.get_raw('select'), verbose=1)
    footer = pif.form.put_button_input("save") + "</form>"
    entries = []

    for row in rows:
        entries.append({
            col: (row[col] if col in table_data.id else
                  pif.form.put_text_input(col + "." + '.'.join([str(row[x]) for x in table_data.id]),
                  256, 40, row[col])) for col in columns})

    lsection = render.Section(colist=columns, range=[render.Range(entry=entries)],
                              header=header, footer=footer)
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=[lsection]), nofooter=True)


def mass_save(pif):
    columns = pif.form.get_raw('select').split(',')
    table_data = pif.dbh.get_table_data(pif.form.get_raw('table'))

    for key in pif.form.keys(has='.'):
        col, ids = key.split('.', 1)
        if col in columns:
            wheres = pif.dbh.make_where(dict(zip(table_data.id, ids.split('.'))))
            # where = " and ".join(["%s='%s'" % x for x in wheres])
            # update table set col=value where condition;
            # query = "update %s set %s='%s' where %s" %
            #   (pif.form.get_raw('table'), col, pif.dbh.escape_string(pif.form.get_raw(key)), where)
            # print(query, '<br>')
            # pif.dbh.raw_execute(query, tag='mass_save')
            # note: untested
            # note: write might already escape values
            pif.dbh.write(pif.form.get_raw('table'), values={col: pif.dbh.escape_string(pif.form.get_raw(key))},
                          where=wheres, modonly=True, tag='mass_save')
    return pif.render.format_template('blank.html', content='')


def mass_type_reinput(pif):
    return pif.form.put_hidden_input(tymass=pif.form.get_raw('tymass'))


# ------- variation dates ------------------------------------------


def dates_main(pif):
    for mvid in pif.form.roots(start='v.'):
        val = pif.form.get_bool('c.' + mvid)
        idm = pif.form.get_bool('i.' + mvid)
        imp = pif.form.get_str('s.' + mvid)
        useful.write_message(mvid, val, idm, imp)
        vars = pif.dbh.fetch_variation_bare(*mvid.split('-'))
        if vars:
            var = vars[0]
            var['variation.flags'] &= ~(config.FLAG_MODEL_VARIATION_VERIFIED | config.FLAG_MODEL_ID_INCORRECT)
            var['variation.flags'] |= (config.FLAG_MODEL_VARIATION_VERIFIED if val else 0)
            var['variation.flags'] |= (config.FLAG_MODEL_ID_INCORRECT if idm else 0)
            var['variation.imported_from'] = imp
            pif.dbh.update_variation_bare(var)
    return pif.render.format_template('blank.html', content='')


# ------- mack numbers ---------------------------------------------


def aliases_main(pif):
    if pif.duplicate_form:
        print('duplicate form submission detected')
    elif pif.form.has('save'):
        return aliases_final(pif)
    elif pif.form.has('add'):
        return aliases_add(pif)
    elif pif.form.has('copy'):
        return aliases_copy(pif)
    return aliases_ask(pif)


def aliases_ask(pif):
    '''Top level of phase 1.'''
    mod_id = pif.form.get_raw('mod_id')
    if not mod_id:
        raise useful.SimpleError("ID not found.")

    aliases = pif.dbh.depref('alias', pif.dbh.fetch_aliases(mod_id))
    cols = ['pk', 'id', 'type', 'ref_id', 'first_year', 'primary', 'section_id', 'del']
    entries = [
        {
            'pk': str(x['pk']) + pif.form.put_hidden_input(pk=x['pk']),
            'id': pif.form.put_text_input("id." + str(x['pk']), 12, value=x['id']),
            'type': pif.form.put_text_input("type." + str(x['pk']), 16, value=x['type']),
            'ref_id': pif.form.put_text_input("ref_id." + str(x['pk']), 12, value=x['ref_id']),
            'first_year': pif.form.put_text_input("first_year." + str(x['pk']), 4, value=x['first_year']),
            'primary': pif.form.put_checkbox(
                'primary.' + str(x['pk']), [('1', '')], checked=['1' if x['flags'] & 2 else '0']),
            'section_id': pif.form.put_text_input("section_id." + str(x['pk']), 20, value=x['section_id']),
            'del': pif.form.put_checkbox('del.' + str(x['pk']), [('1', '')]),
        } for x in aliases
    ]
    adds = [
        {
            'id': pif.form.put_text_input("id.0", 12),
            'first_year': pif.form.put_text_input("first_year.0", 4),
            'ref_id': pif.form.put_text_input("ref_id.0", 12, value=mod_id),
            'section_id': pif.form.put_text_input("section_id.0", 20),
            'type': pif.form.put_text_input("type.0", 16),
            'primary': pif.form.put_checkbox("primary.0", [('1', '')]),
        }
    ]
    copys = [
        {
            'mod id': pif.form.put_text_input("copy_id.0", 12),
        }
    ]

# {'title': "Section ID:", 'value': pif.form.put_text_input("section_id", 256, 80, value='single')},
# {'title': "Associated Link:", 'value': pif.form.put_select('associated_link', [(0, '')] + [(x['link_line.id'],
#  x['link_line.name']) for x in asslinks])},
# {'title': '', 'value': pif.form.put_button_input()},

    # header = '<form name="mass" action="mass.cgi">' + pif.create_token()
    header = pif.form.put_form_start(name='mass', action='mass.cgi', token=pif.dbh.create_token())
    header += 'Mod ID: ' + mod_id + pif.form.put_hidden_input(mod_id=mod_id)
    footer = mass_type_reinput(pif) + "</form><p>"

    lsections = [
        render.Section(colist=cols, range=[render.Range(entry=entries)], header=header,
                       footer=pif.form.put_button_input('save') + footer),
        render.Section(colist=cols, range=[render.Range(entry=adds)], header=header,
                       footer=pif.form.put_button_input('add') + footer),
        render.Section(colist=['mod id'], range=[render.Range(entry=copys)], header=header,
                       footer=pif.form.put_button_input('copy') + footer),
    ]
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=lsections), nofooter=True)


def aliases_add(pif):
    print('add', pif.form, '<br>')
    mod_id = pif.form.get_raw('mod_id')
    ent = {
        'id': pif.form.get_raw('id.0'),
        'first_year': pif.form.get_raw('first_year.0'),
        'ref_id': pif.form.get_raw('ref_id.0') or mod_id,
        'section_id': pif.form.get_raw('section_id.0'),
        'type': pif.form.get_raw('type.0'),
        'flags': 2 if pif.form.get_raw('primary.0') else 0,
    }
    print(ent, '<br>')
    print(pif.dbh.add_alias(ent))


def aliases_copy(pif):
    print('copy', pif.form, '<br>')
    mod_id = pif.form.get_raw('mod_id')
    aliases = pif.dbh.depref('alias', pif.dbh.fetch_aliases(pif.form.get_raw('copy_id.0')))
    adds = [
        {
            'id': x['id'],
            'first_year': x['first_year'],
            'ref_id': mod_id,
            'section_id': x['section_id'],
            'type': x['type'],
            'flags': x['flags'],
        } for x in aliases
    ]
    for ent in adds:
        print(ent, '<br>')
        print(pif.dbh.add_alias(ent))


def aliases_final(pif):
    for pk in pif.form.get_list('pk'):
        ent = pif.form.get_dict(end='.' + pk)
        if ent.get('del'):
            print('delete', pk)
            print(pif.dbh.delete_alias(pk), '<br>')
        else:
            ent = {
                'id': ent['id'],
                'first_year': ent.get('first_year', ''),
                'ref_id': ent['ref_id'],
                'section_id': ent.get('section_id', ''),
                'type': ent['type'],
                'flags': 2 if ent.get('primary') else 0,
            }
            print('update', pk, ent)
            print(pif.dbh.update_alias(int(pk), ent), '<br>')


# ------- add lineup -----------------------------------------------


def lineup_desc_main(pif):
    print(pif.render.format_head())
    useful.header_done()
    # for key in pif.form.keys(start='description.'):
    for root in pif.form.roots(start='description.'):
        # root = key[key.find('.') + 1:]
        lm = pif.dbh.depref('lineup_model', pif.dbh.fetch_lineup_model({'id': root})[0])
        halfstar = lm['flags'] & config.FLAG_LINEUP_MODEL_MULTI_VARS
        if (lm['name'] != pif.form.get_raw('description.' + root) or
                lm['style_id'] != pif.form.get_raw('style_id.' + root) or
                bool(halfstar) != pif.form.get_bool('halfstar.' + root)):
            print('name', root, pif.form.get_raw('description.' + root), lm['name'])
            print('style', pif.form.get_raw('style_id.' + root), lm['style_id'])
            print('halfstar', pif.form.get_bool('halfstar.' + root), bool(halfstar))
            lm['name'] = pif.form.get_raw('description.' + root)
            lm['style_id'] = pif.form.get_raw('style_id.' + root)
            # i am a terrible person
            lm['flags'] = ((lm['flags'] & ~config.FLAG_LINEUP_MODEL_MULTI_VARS) |
                           (config.FLAG_LINEUP_MODEL_MULTI_VARS * pif.form.get_int('halfstar.' + root)))
            print(pif.dbh.update_lineup_model({'id': root}, lm, verbose=True))
            print('<br>')
    print(pif.render.format_tail())


# TODO add base_id/casting_id for new castings
def add_lineup_main(pif):
    if pif.duplicate_form:
        print('duplicate form submission detected')
    elif pif.form.has('save'):
        print(pif.render.format_head())
        useful.header_done()
        add_lineup_final(pif)
        print(pif.render.format_tail())
        return
    elif pif.form.has('num'):
        return add_lineup_list(pif)
    return add_lineup_ask(pif)


def add_lineup_ask(pif):
    # header = '<form action="mass.cgi">' + pif.create_token()
    header = pif.form.put_form_start(action='mass.cgi', token=pif.dbh.create_token())
    entries = [
        {'title': 'Number of models:', 'value': pif.form.put_text_input("num", 8, 8)},
        {'title': 'Year:', 'value': pif.form.put_text_input("year", 4, 4)},
        {'title': 'Region:', 'value': pif.form.put_text_input("region", 4, 4)},
        {'title': 'Model List File:', 'value': pif.form.put_text_input("models", 80, 80)},
        {'title': '', 'value': 'bar file: num|man_id|style|name'},
        {'title': '', 'value': pif.form.put_button_input()},
    ]
    footer = mass_type_reinput(pif)
    footer += "</form>"
    lsection = render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)], note='', noheaders=True,
                              header=header, footer=footer)
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=[lsection]), nofooter=True)


def add_lineup_final(pif):
    # "I think we could all do better." -- Jim Jeffries
    pid = {
        'id': pif.form.get_raw('page_id'),
        'flags': 0,
        'format_type': '',
        'title': '',
        'pic_dir': pif.form.get_raw('picdir'),
        'tail': '',
        'description': '',
        'note': ''}
    print(pid)
    pif.dbh.dbi.insert_or_update('page_info', pid, verbose=True)
    sid = {
        'id': pif.form.get_raw('region'),
        'page_id': pif.form.get_raw('page_id'),
        'display_order': 0,
        'category': 'man',
        'flags': 0,
        'name': pif.form.get_raw('sec_title'),
        'columns': pif.form.get_int('cols', 4),
        'start': 0,
        'pic_dir': '',
        'disp_format': '%d.',
        'link_format': pif.form.get_raw('link_fmt'),
        'img_format': '',
        'note': ''}
    print(sid)
    pif.dbh.dbi.insert_or_update('section', sid, verbose=True)

    for key in pif.form.keys(start='mod_id.'):
        num = key[7:]
        mid = {
            'mod_id': pif.form.get_raw(key),
            'number': num,
            'style_id': pif.form.get_raw('style_id.' + num),
            'picture_id': '',
            'region': pif.form.get_raw('region'),
            'year': pif.form.get_raw('year'),
            'page_id': pif.form.get_raw('page_id'),
            'name': pif.form.get_raw('name.' + num)}
        print(mid)
        pif.dbh.dbi.insert_or_update('lineup_model', mid, verbose=True)


def add_lineup_list(pif):
    # Currently untested.  Used too rarely to worry about right now.
    # modlist = requests.get(pif.form.get_raw('models')).text.split('\n')
    modlist = [x.strip().split('|') for x in open(pif.form.get_raw('models')).readlines()]
    # castings = {x['base_id.rawname'].replace(';', ' '): x['base_id.id'] for x in pif.dbh.fetch_casting_list()}
    # num_models = pif.form.get_int('num')
    year = pif.form.get_raw('year')
    region = pif.form.get_raw('region')

    entries = [
        {'title': 'Page ID:', 'value': pif.form.put_text_input("page_id", 20, 20, value=f'year.{year}')},
        {'title': 'Year:', 'value': pif.form.put_text_input("year", 20, 20, value=year)},
        {'title': 'Region:', 'value': pif.form.put_text_input("region", 4, 4, value=region)},
        {'title': 'Picture Directory:', 'value': pif.form.put_text_input("picdir", 80, 80)},
        {'title': 'Section Title:', 'value': pif.form.put_text_input(
            "sec_title", 80, 80, value='Matchbox %s %s Lineup' % (year, mbdata.regions[region]))},
        {'title': 'Link Format:', 'value': pif.form.put_text_input(
            "link_fmt", 20, 20, value='%s%s%%03d' % (year[2:], region.lower()))},
        {'title': 'Columns:', 'value': pif.form.put_text_input("cols", 1, 1)},
        {'title': '', 'value': pif.form.put_button_input('save')},
    ]
    lsections = [render.Section(
        colist=['title', 'value'], range=[render.Range(entry=entries)], note='Page and Section', noheaders=True,
        header=pif.form.put_form_start(action='mass.cgi', token=pif.dbh.create_token()))]
    entries = []
    for cnt, mod, style_id, name in modlist:
        cnt = int(cnt)
        mod = mod.strip()
        entries.append({
            'number': str(cnt),
            'mod_id': pif.form.put_text_input(f"mod_id.{cnt}", 12, 12, value=mod),
            'style_id': pif.form.put_text_input(f"style_id.{cnt}", 3, 3, value=style_id),
            'name': pif.form.put_text_input(f"name.{cnt}", 64, 64, value=name),
        })
#    for cnt in range(0, num_models):
#        name = modlist.pop(0)
#        entries.append({
#            'number': "%s" % (cnt + 1),
#            'mod_id': pif.form.put_text_input("mod_id.%d" % (cnt + 1), 12, 12, value=castings.get(name, '')),
#            'style_id': pif.form.put_text_input("style_id.%d" % (cnt + 1), 3, 3, value='0'),
#            'name': pif.form.put_text_input("name.%d" % (cnt + 1), 64, 64, value=name),
#        })
    footer = mass_type_reinput(pif)
    footer += "</form>"
#    columns = ['number', 'mod_id', 'style_id', 'name']
#    headers = ['Number', 'Model ID', 'Style ID', 'Name']
    lsections.append(render.Section(
        colist=['number', 'mod_id', 'style_id', 'name'], range=[render.Range(entry=entries)],
        note='Models', footer=footer))
#    lsection = render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)], note='', noheaders=True,
#                              footer=footer)
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=lsections), nofooter=True)


# ------- add lineup_model -----------------------------------------


def add_lm_main(pif):
    if pif.duplicate_form:
        add_lm_save(pif)
        print('duplicate form submission detected')
    elif pif.form.has('save'):
        add_lm_save(pif)
        return
    elif pif.form.has('number'):
        return add_lm_enter(pif)
    return add_lm_ask(pif)


def add_lm_ask(pif):
    header = '<form action="mass.cgi">' + pif.create_token()
    colors = [('0', ''), ('1', 'blue'), ('2', 'red'), ('3', 'yellow'), ('4', 'green'), ('5', 'brown')]
    entries = [
        {'title': 'Year:', 'value': pif.form.put_text_input("year", 4, 4)},
        {'title': 'Number:', 'value': pif.form.put_text_input("number", 4, 4)},
        {'title': 'Mod ID:', 'value': pif.form.put_text_input("mod_id", 24, 4)},
        {'title': 'Style:', 'value': pif.form.put_select("style_id", colors)},
        {'title': '', 'value': pif.form.put_button_input()},
    ]
    footer = mass_type_reinput(pif)
    footer += "</form>"
    lsection = render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)], note='', noheaders=True,
                              header=header, footer=footer)
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=[lsection]), nofooter=True)


def add_lm_enter(pif):
    year = pif.form.get_raw('year')
    pg = pif.dbh.fetch_page('year.' + year)
    if not pg:
        raise useful.SimpleError("no page")
    secs = pif.dbh.fetch_sections({'page_id': pg.id})
    if not secs:
        raise useful.SimpleError("no secs")
    tab = pif.dbh.get_table_data('lineup_model')
    mod_id = pif.form.get_raw('mod_id')
    mod = pif.dbh.fetch_casting(mod_id)
    number = pif.form.get_int('number')

    colors = [('0', ''), ('1', 'blue'), ('2', 'red'), ('3', 'yellow'), ('4', 'green'), ('5', 'brown')]
    regions = [x.id for x in secs]
    entries = [
        {'title': 'Page ID:', 'value': pif.form.put_text_input("page_id", 32, 32, value=f'year.{year}')},
        {'title': 'Mod ID:', 'value': pif.form.put_text_input("mod_id", 24, 24, value=mod_id)},
        {'title': 'Number:', 'value': pif.form.put_text_input("number", 4, 4, value=number)},
        {'title': 'Display Order:', 'value': pif.form.put_text_input("display_order", 4, 4, value='0')},
        {'title': 'Flags:', 'value':
            pif.form.put_checkbox('flags', tab.bits['flags'], useful.bit_list(0, format='%04x'))},
        {'title': 'Style:', 'value':
            pif.form.put_select("style_id", colors, selected=pif.form.get_raw('style_id'))},
        {'title': 'Picture ID:', 'value': pif.form.put_text_input("picture_id", 12, 12, value='')},
        {'title': 'Region:', 'value': pif.form.put_checkbox('region', zip(regions, regions), checked=regions)},
        {'title': 'Year:', 'value': pif.form.put_text_input("year", 6, 6, value=year)},
        {'title': 'Name:', 'value': pif.form.put_text_input("name", 64, 64, value=mod['name'])},
        # {'title': 'Variation:', 'value': pif.form.put_text_input("var", 8, 8)},
        {'title': '', 'value': pif.form.put_button_input('save')},
    ]

    columns = ['title', 'value']
    header = '<form name="mass" action="mass.cgi">' + pif.create_token()
    footer = mass_type_reinput(pif) + "</form>"
    lsection = render.Section(colist=columns, range=[render.Range(entry=entries)],
                              noheaders=True, header=header, footer=footer)
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=[lsection]), nofooter=True)


def add_lm_save(pif):
    print(pif.render.format_head())
    useful.header_done()

#    var = pif.form.get_raw('var')
    lm = pif.form.get_dict(['mod_id', 'number', 'display_order', 'style_id', 'picture_id', 'year', 'page_id', 'name'])
    lm['flags'] = pif.form.get_bits('flags')
    regions = pif.form.get_list('region')

    for region in regions:
        lm['region'] = region
        lm['base_id'] = lm['year'] + region + '%03d' % int(lm['number'])
        print(lm, pif.dbh.dbi.insert_or_update('lineup_model', lm, verbose=1))
    print(pif.render.format_tail())


# ------- add lm_series -----------------------------------------


def add_lm_series_main(pif):
    region = 'X.11'
    page_id = pif.form.get_raw('page_id')
    section_id = pif.form.get_raw('section_id')
    useful.write_message(pif.form)
    if pif.form.get_raw('save'):
        print(pif.render.format_head())
        useful.header_done()
        add_lm_series_final(pif)
        print(pif.render.format_tail())
        return
    elif pif.form.get_raw('year'):
        return add_lm_series_form(pif, page_id, section_id, region)
    return add_lm_series_ask(pif, page_id, section_id)


def add_lm_series_ask(pif, page_id, section_id):
    rows = [
        ('Year:', "year", ''),
        ('Page ID:', "page_id", page_id),
        ('Section ID:', "section_id", section_id),
    ]
    entries = [{'title': x[0], 'value': pif.form.put_text_input(x[1], 16, 16, value=x[2])} for x in rows]

    lsection = render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)], note='', noheaders=True,
                              header=pif.form.put_form_start(token=pif.dbh.create_token()) +
                              '\n<input type="hidden" name="tymass" value="lm_series">\n',
                              footer=pif.form.put_button_input('submit') + "</form>")
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=[lsection]), nofooter=True)


def add_lm_series_form(pif, page_id, section_id, region):
    year = pif.form.get_raw('year')
    page = pif.dbh.fetch_page(id=page_id)
    section = pif.dbh.fetch_section(page_id=page_id, sec_id=section_id)
    useful.write_message('page', str(page))
    useful.write_message('section', str(section))
    lm_list = pif.dbh.fetch_lineup_models_bare(year=year, region=region)
    num = len(lm_list) + 1

    header = '<hr>\n'
    header += str(pif.form) + '<hr>\n'
    header += '<form action="mass.cgi" method="post">\n' + pif.create_token()
    header += '<input type="hidden" name="verbose" value="1">\n'
    header += '<input type="hidden" name="tymass" value="lm_series">\n'

    linmod = pif.dbh.depref('lineup_model', pif.dbh.fetch_lineup_model(
        where=f"mod_id='{page_id}' and picture_id='{section_id}'"))
    linmod = linmod[0] if linmod else {
        'id': 0,  # delete later
        'base_id': '%sX11%02d' % (year, num),
        'mod_id': page_id,
        'number': num,
        'display_order': num,
        'flags': '0',
        'style_id': 'lg',
        'picture_id': section_id,
        'region': region,
        'year': year,
        'name': page.get('title', '') + ' - ' + section.get('name'),
        'page_id': 'year.' + year,
    }
    linmod['flags'] = linmod['flags'] or 0

    llistix = render.Listix(note=header)
    llistix.section.append(entry_form(pif, 'lineup_model', linmod))

    footer = ''
    footer += pif.form.put_button_input("save")
    footer += '</form>\n'
    footer += pif.render.format_button_link('see',
                                            f"lineup.cgi?year={year}&region=U&listtype=&lty=series&submit=1") + ' '
    footer += pif.render.format_button_link('edit',
                                            f"editor.cgi?table=section&id={region}&page_id=year.{year}") + '<br>'
    for lm in sorted(lm_list, key=lambda x: x['lineup_model.number']):
        footer += f"{lm['lineup_model.number']}. {lm['lineup_model.name']} ({lm['lineup_model.display_order']})<br>\n"
    llistix.section[-1].footer = footer

    return pif.render.format_template('simplelistix.html', llineup=llistix)


def add_lm_series_final(pif):
    values = pif.dbh.make_values('lineup_model', pif.form, 'lineup_model.')
    values['flags'] = values['flags'] or 0
    if pif.form.get_int('lineup_model.id'):
        print('update line_model', values, '<br>')
        pif.dbh.update_lineup_model({'id': pif.form.get_int('lineup_model.id')}, values)
    else:
        print('new line_model', values, '<br>')
        linmod = pif.dbh.fetch_lineup_model(
            where="mod_id='%s' and picture_id='%s'" % (values['mod_id'], values['picture_id']))
        if not linmod:  # goddamn bounciness
            del values['id']
            print('already<br>')
            pif.dbh.insert_lineup_model(values)


# ------- add casting ---------------------------------------------


def add_casting_main(pif):
    if pif.form.has('save'):
        return add_casting_final(pif)

    entries = [
        {'title': "ID:", 'value': pif.form.put_text_input("id", 8, 8, value=f'{pif.form.get_raw("id")}')},
        {'title': 'Year:', 'value': pif.form.put_text_input("year", 4, 4, value=pif.form.get_raw('year'))},
        {'title': 'Model Type:', 'value': pif.form.put_select(
            'model_type', [x.model_type for x in pif.dbh.fetch_base_id_model_types()], selected='SF')},
        {'title': 'Name:', 'value': pif.form.put_text_input("rawname", 80, 80, value='')},
        {'title': 'Description:', 'value': pif.form.put_text_input("description", 80, 80, value='')},
        {'title': 'Flags:', 'value':
            pif.form.put_checkbox('notmade', [('not', 'Not Made')]) +
            pif.form.put_checkbox('revised', [('is', 'Revised')])},
        {'title': 'Country:', 'value': pif.form.put_select_country('country')},
        {'title': 'Make:', 'value': pif.form.put_select(
            'make', [('unl', 'MBX')] + [(x['vehicle_make.id'], x['vehicle_make.name'])
                                        for x in pif.dbh.fetch_vehicle_makes()], blank='')},
        {'title': 'Section:', 'value': pif.form.put_select(
            'section_id', [(x['section.id'], x['section.name'])
                           for x in pif.dbh.fetch_sections(where="page_id like 'man%'")],
            selected=pif.form.get_raw('section_id'))},
        {'title': 'Attributes:', 'value': pif.form.put_text_input('attributes', 80, 80)},
        {'title': 'Mack:', 'value': pif.form.put_text_input('mack', 8, 8)},
        {'title': 'Related:', 'value': pif.form.put_text_input('related', 80, 80)},
        {'title': 'Vehicle Type:', 'value':
            pif.form.put_checkbox(
                'vt', [[x, mbdata.vehicle_types[x]] for x in list(mbdata.model_type_chars[:14])]) + '<br>' +
            pif.form.put_checkbox(
                'vt', [[x, mbdata.vehicle_types[x]] for x in list(mbdata.model_type_chars[14:])])},
        {'title': '', 'value': pif.form.put_button_input('save')},
    ]

    header = '<form name="mass" action="mass.cgi">' + pif.create_token()
    footer = mass_type_reinput(pif) + "</form><p>"

    lsections = [render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)], noheaders=True,
                                header=header, footer=footer)]
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=lsections), nofooter=True)


def add_casting_final(pif):
    casting_id = pif.form.get_raw('id')
    ostr = str(pif.form.get_form()) + '<br>\n'
    if pif.duplicate_form:
        print('duplicate form submission detected')
    else:
        if pif.dbh.fetch_base_id(casting_id):
            raise useful.SimpleError("That ID is already in use.")
        # base_id: id, first_year, model_type, rawname, description, flags
        # casting: id, country, make, section_id
        ostr += str(pif.dbh.add_new_base_id({
            'id': casting_id,
            'first_year': pif.form.get_raw('year'),
            'model_type': pif.form.get_raw('model_type'),
            'rawname': pif.form.get_raw('rawname'),
            'description': pif.form.get_raw('description'),
            'flags': ((config.FLAG_MODEL_NOT_MADE if pif.form.get_raw('notmade') == 'not' else 0) |
                      (config.FLAG_MODEL_CASTING_REVISED if pif.form.get_raw('revised') == 'is' else 0)),
        })) + '<br>\n'
        ostr += str(pif.dbh.add_new_casting({
            'id': casting_id,
            'country': pif.form.get_raw('country'),
            'make': pif.form.get_raw('make'),
            'section_id': pif.form.get_raw('section_id'),
            'notes': '',
        })) + '<br>\n'
        mannum.add_attributes(pif, casting_id, *pif.form.get_raw('attributes').split(' '))
        if pif.form.get_raw('make'):
            ostr += str(pif.dbh.add_casting_make(
                mod_id=casting_id, make_id=pif.form.get_raw('make'), verbose=True)) + '<br>\n'
        if pif.form.get_raw('mack'):
            ostr += str(pif.dbh.add_alias(
                {'id': pif.form.get_raw('mack'), 'first_year': pif.form.get_raw('year'),
                 'ref_id': casting_id, 'type': 'mack', 'flags': 2})) + '<br>\n'
        if pif.form.get_raw('related'):
            for rel_id in pif.form.get_raw('related').split(' '):
                ostr += str(pif.dbh.add_casting_related({
                    'model_id': casting_id,
                    'related_id': rel_id,
                    'section_id': 'single',
                    'picture_id': '',
                    'description': '',
                    'flags': 0,
                })) + '<br>\n'
                ostr += str(pif.dbh.add_casting_related({
                    'model_id': rel_id,
                    'related_id': casting_id,
                    'section_id': 'single',
                    'picture_id': '',
                    'description': '',
                    'flags': 0,
                })) + '<br>\n'
        os.mkdir(os.path.join('lib', 'man', casting_id.lower()), mode=0o775)

        val = ''.join(pif.form.get_list('vt'))
        pif.dbh.write_casting(values={'vehicle_type': val}, id=casting_id)
    print(pif.render.format_template('blank.html', content=ostr))
    raise useful.Redirect(f'single.cgi?id={casting_id}')


# ------- add pub -------------------------------------------------


def add_pub_main(pif):
    if pif.form.has('save'):
        return add_pub_final(pif)
    entries = [
        {'title': "ID:", 'value': pif.form.put_text_input("id", 12, 12, value='')},
        {'title': 'Year:', 'value': pif.form.put_text_input("year", 4, 4, value=pif.form.get_raw('year'))},
        {'title': 'Model Type:', 'value': pif.form.put_select('model_type', sorted(
            mbdata.model_type_names.items()), selected='BK')},
        {'title': 'Name:', 'value': pif.form.put_text_input("rawname", 80, 80, value='')},
        {'title': 'Description:', 'value': pif.form.put_text_input("description", 80, 80, value='')},
        {'title': 'Made:', 'value': pif.form.put_checkbox('notmade', [('not', 'not')])},
        {'title': 'Country:', 'value': pif.form.put_select_country('country')},
        {'title': 'ISBN:', 'value': pif.form.put_text_input("isbn", 20, 20, value='')},
        # {'title': 'Section:', 'value': pif.form.put_select('section_id', [
        #     (x['section.id'], x['section.name']) for x in pif.dbh.fetch_sections(where="page_id like 'man%'")],
        #     selected=pif.form.get_raw('section_id'))},
        {'title': '', 'value': pif.form.put_button_input('save')},
    ]

    header = '<form name="mass" action="mass.cgi">' + pif.create_token()
    footer = mass_type_reinput(pif) + "</form><p>"

    lsections = [render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)], note='', noheaders=True,
                                header=header, footer=footer)]
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=lsections), nofooter=True)


def add_pub_final(pif):
    if pif.dbh.fetch_base_id(pif.form.get_raw('id')):
        raise useful.SimpleError("That ID is already in use.")
    # base_id: id, first_year, model_type, rawname, description, flags
    # publication: id, country, section_id
    ostr = str(pif.form.get_form()) + '<br>\n'
    if pif.duplicate_form:
        print('duplicate form submission detected')
    else:
        ostr += str(pif.dbh.add_new_base_id({
            'id': pif.form.get_raw('id'),
            'first_year': pif.form.get_raw('year'),
            'model_type': pif.form.get_raw('model_type'),
            'rawname': pif.form.get_raw('rawname'),
            'description': pif.form.get_raw('description'),
            'flags': config.FLAG_MODEL_NOT_MADE if pif.form.get_raw('notmade') == 'not' else 0,
        })) + '<br>\n'
        ostr += str(pif.dbh.add_new_publication({
            'id': pif.form.get_raw('id'),
            'country': pif.form.get_raw('country'),
            'section_id': pif.form.get_raw('model_type').lower(),
            'isbn': pif.form.get_raw('isbn'),
        })) + '<br>\n'
    return pif.render.format_template('blank.html', content=ostr)


# ------- add var -------------------------------------------------


def add_var_main(pif):
    useful.write_message(pif.form)
    if pif.form.get_raw('store'):
        print(pif.render.format_head())
        useful.header_done()
        add_var_final(pif)
        print(pif.render.format_tail())
        return
    elif pif.form.get_raw('var'):
        return add_var_info(pif)
    return add_var_ask(pif)


def add_var_ask(pif):
    header = pif.form.put_form_start(token=pif.dbh.create_token())

    rows = [
        ('Man ID:', "mod_id", pif.form.get_raw('mod_id')),
        ('Var ID:', "var", ''),
        ('Date:', "date", ''),
        ('Copy From:', "copy", ''),
        ('Imported From:', "imported_from", 'mbusa'),
    ]
    entries = [{'title': x[0], 'value': pif.form.put_text_input(x[1], 10, 8, value=x[2])} for x in rows]

    footer = pif.form.put_button_input('submit')
    footer += mass_type_reinput(pif)
    footer += "<form>"
    footer += pif.render.format_button_link('catalog', '/lib/docs/mbusa/', lalso={'target': '_blank'})
    footer += pif.render.format_button_link('casting', '/cgi-bin/mass.cgi?tymass=casting')

    lsection = render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)], note='', noheaders=True,
                              header=header, footer=footer)
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=[lsection]), nofooter=True)


var_id_columns = ['mod_id', 'var']
var_attr_columns = ['body', 'base', 'windows', 'interior', 'deco', 'wheels']
var_data_columns = ['category', 'note', 'additional_text', 'manufacture', 'area', 'date',
                    'imported_from', 'imported_var', 'references']
var_record_columns = var_id_columns + var_attr_columns + var_data_columns + ['deco_type']


def add_var_info(pif):
    mod_id = pif.form.get_raw('mod_id')
    date = pif.form.get_raw('date')
    mod = pif.dbh.fetch_casting(mod_id)
    var_id = pif.form.get_raw('var')
    if not mod:
        mod = pif.dbh.fetch_casting_by_id_or_alias(mod_id)
        if not mod:
            raise useful.Redirect(f'/cgi-bin/mass.cgi?tymass=casting&id={mod_id}&year={date[:4]}')
        elif len(mod) > 1:
            raise useful.SimpleError("Multiple models found.")
        mod = pif.dbh.modify_man_item(mod[0])
    mod_id = mod['id']
    img = pif.render.format_image_required(mod_id, pdir=config.IMG_DIR_MAN, largest=mbdata.IMG_SIZ_MEDIUM,
                                           also={'style': 'float: right;'})
    var_id = mbdata.normalize_var_id(mod, var_id)
    attrs = pif.dbh.fetch_attributes(mod_id)
    attr_names = [x['attribute.attribute_name'] for x in attrs]
    var = pif.dbh.fetch_variation(mod_id, var_id) or {}
    var = pif.dbh.depref('variation', var)
    aliases = pif.dbh.fetch_aliases(mod_id)
    old_var_id = pif.form.get_raw('copy')
    cats = sorted([(x['category.id'], x['category.name']) for x in pif.dbh.fetch_category_counts()],
                  key=lambda x: x[1])
    plants = sorted([(x[0], x[0]) for x in mbdata.plants])

    if var:
        selects = pif.dbh.fetch_variation_selects(mod_id, var_id, bare=True)
        var['references'] = ' '.join([
            x['ref_id'] +
            (('/' + x['sec_id']) if x['sec_id'] else '') +
            (('.' + x['ran_id']) if x['ran_id'] else '') +
            ((':' + x['category.id']) if x['category.id'] else '') for x in selects]
        )
    elif old_var_id and old_var_id != var_id:
        nvar = pif.dbh.fetch_variation(mod_id, old_var_id)
        if nvar:
            useful.write_message('copy_variation', mod_id, old_var_id, var_id)
            nvar = pif.dbh.depref('variation', nvar)
            nvar['var'] = var['imported_var'] = var_id
            nvar['imported_from'] = pif.form.get_raw('imported_from')
            nvar['date'] = pif.form.get_raw('date')
            for k, v in nvar.items():
                var[k] = var.get(k, '') or v

    header = f"<h3>{mod['name']}</h3>" + img
    header += ' '.join(x['alias.id'] for x in aliases) + '<br>'
    header += '<form onsubmit="save.disabled=true; return true;">' + pif.create_token()
    if var:
        header += 'revising' + pif.form.put_hidden_input(store='update')
    else:
        header += 'creating' + pif.form.put_hidden_input(store='insert')

    entries = []
    defs = {'mod_id': mod_id,
            'var': var_id,
            'flags': 0,
            'manufacture': 'Thailand',
            'imported_from': pif.form.get_raw('imported_from'),
            'imported_var': var_id,
            'date': pif.form.get_raw('date')}
    for col in var_id_columns:
        val = var.get(col) if var and var.get(col) else defs.get(col, '')
        entries.append({'title': col, 'value': val, 'input': val + pif.form.put_hidden_input(**{col: val})})
    entries.append({})
    for col in var_attr_columns + attr_names + [None] + var_data_columns:
        if col:
            val = var.get(col) if var and var.get(col) else defs.get(col, '')
            entries.append(
                {'title': col, 'value': val, 'input':
                 pif.form.put_text_input(col, 64, 32, value=val) +
                 pif.form.put_select('deco_type', mbdata.deco_types, var.get('deco_type')) if col == 'deco' else
                 pif.form.put_select(col, sorted(cats), val, blank='') if col == 'category' else
                 pif.form.put_select(col, sorted(plants), val, blank='') if col == 'manufacture' else
                 pif.form.put_text_input(col, 64, 32, value=val)})
        else:
            entries.append({})
    footer = pif.form.put_button_input('save')
    footer += mass_type_reinput(pif)
    footer += pif.render.format_button_link('casting', f'/cgi-bin/single.cgi?id={mod_id}')
    footer += pif.render.format_button_link('vars', f'/cgi-bin/vars.cgi?edt=1&mod={mod_id}')
    footer += pif.render.format_button_link('search', f'/cgi-bin/vsearch.cgi?ask=1&id={mod_id}')
    footer += "</form>"

    for var in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
        lnk = '/cgi-bin/vars.cgi?edit=1&mod=%(mod_id)s&var=%(var)s' % var
        footer += var['var'] + ' : ' + pif.render.format_link(lnk, var['text_description']) + '<br>'
    footer += pif.render.format_tail()

    lsection = render.Section(colist=['title', 'value', 'input'], range=[render.Range(entry=entries)], noheaders=True,
                              header=header, footer=footer)
    llistix = render.Listix(section=[lsection])
    return pif.render.format_template('simplelistix.html', llineup=llistix, nofooter=True)


def add_var_final(pif):
    mod_id = pif.form.get_raw('mod_id')
    var_id = pif.form.get_raw('var')
    attrs = pif.dbh.fetch_attributes(mod_id)
    attr_names = [x['attribute.attribute_name'] for x in attrs]
    upd = False
    if pif.form.get_raw('store') == 'update':
        var = pif.dbh.depref('variation', pif.dbh.fetch_variation(mod_id, var_id))
        if var:
            upd = True
        else:
            var = {}
    else:
        var = {}
    for col in var_record_columns + attr_names:
        if col == 'references':
            var_sel = pif.form.get_raw(col)
        elif pif.form.get_raw(col):
            var[col] = pif.form.get_raw(col)
    print(var, '<br>')
    if pif.duplicate_form:
        print('duplicate form submission detected')
    elif upd:
        pif.dbh.update_variation(var, {'mod_id': mod_id, 'var': var_id}, verbose=True)
    else:
        pif.dbh.insert_variation(mod_id, var_id, var, verbose=True)
    if var_sel:
        useful.write_message('varsel', var_sel, '<br>')
        pif.dbh.update_variation_selects_for_variation(mod_id, var_id, var_sel.split())
    pif.dbh.recalc_description(mod_id, showtexts=False, verbose=False)
    raise useful.Redirect(f'/cgi-bin/vars.cgi?edt=1&mod={mod_id}&var={var_id}')


# ------- casting_related ------------------------------------------


def show_all_casting_related(pif):
    useful.write_message('show_all_casting_related')
    print(pif.render.format_head())
    # 'columns': ['id', 'model_id', 'related_id', 'section_id', 'picture_id', 'description'],
    print('show_all_casting_related', pif.form, '<br>')

    mod_id = ''
    section_id = pif.form.get_raw('section_id', 'single')
    crl = pif.dbh.fetch_casting_related_models()
    crd_m = {}
    crd_r = {}
    for cr in crl:
        if mod_id in (None, cr['casting_related.model_id'], cr['casting_related.related_id']):
            if mod_id or cr['m.model_type'] in ('SF', 'RW') or cr['r.model_type'] in ('SF', 'RW'):
                m_id = cr['casting_related.model_id']
                r_id = cr['casting_related.related_id']
                if m_id < r_id:
                    crd_m[(m_id, r_id)] = cr
                    crd_r.setdefault((m_id, r_id), {})
                else:
                    crd_m.setdefault((r_id, m_id), {})
                    crd_r[(r_id, m_id)] = cr

    print('<form action="mass.cgi" onsubmit="save.disabled=true; return true;">' + pif.create_token())
    print('<table border=1>')
    print(mass_type_reinput(pif))
    print(pif.form.put_hidden_input(section_id=section_id))
    cnt = 0
    for cr in crd_m:
        cnt += 1
        print('<tr>')
        print('<td><a href="%s">%s</a></td>' % (pif.dbh.get_editor_link('casting_related', {
            'id': crd_m[cr].get('casting_related.id', '')}), crd_m[cr].get('casting_related.id', '')))
        print('<td><a href="single.cgi?id=%s">%s</a><input type="hidden" name="m.%s" value="%s"></td>' % (
            cr[0], cr[0], cnt, cr[0]))
        print('<td>', crd_m[cr].get('m.rawname', ''), '</td>')
        print('<input type="hidden" name="im.%s" value="%s">' % (cnt, crd_m[cr].get('casting_related.id', '')))
        # print('<td>', crd_r[cr].get('casting_related.id', '') if cr in crd_r else '', '</td>')
        if cr in crd_r:
            print('<td><a href="%s">%s</a></td>' % (pif.dbh.get_editor_link('casting_related', {
                'id': crd_r[cr].get('casting_related.id', '')}), crd_r[cr].get('casting_related.id', '')))
        else:
            print('<td></td>')
        print('<td><a href="single.cgi?id=%s">%s</a><input type="hidden" name="r.%s" value="%s"></td>' % (
            cr[1], cr[1], cnt, cr[1]))
        print('<td>', crd_m[cr].get('r.rawname', ''), '' if cr in crd_r else '(missing)', '</td>')
        if cr in crd_r:
            print('<input type="hidden" name="ir.%s" value="%s">' % (cnt, crd_r[cr].get('casting_related.id', '')))
        print('</tr><tr>')
        print('<td colspan=3>%s</td>' % crd_m[cr].get('m.description', ''))
        print('<td colspan=3>%s</td>' % crd_m[cr].get('r.description', ''))
        print('</tr><tr>')
        rd = crd_r[cr].get('casting_related.description', '') if cr in crd_r else ''
        print('<td colspan=3><input type="text" name="dr.%s" value="%s"></td>' % (cnt, rd))
        print('<td colspan=3><input type="text" name="dm.%s" value="%s"></td>' % (
            cnt, crd_m[cr].get('casting_related.description', '')))
        print('</tr><tr>')
        rd = crd_r[cr].get('casting_related.section_id', '') if cr in crd_r else ''
        print('<td colspan=3><input type="text" name="sr.%s" value="%s"></td>' % (cnt, rd))
        print('<td colspan=3><input type="text" name="sm.%s" value="%s"></td>' % (
            cnt, crd_m[cr].get('casting_related.section_id', '')))
        print('</tr>')
    print('</table>')
    print(pif.form.put_button_input('save'))
    print('</form><hr>')
    print(pif.render.format_tail())


def edit_casting_related_ask(pif):
    useful.write_message('edit_casting_related_ask')
    header = '<form action="mass.cgi">' + pif.create_token()
    entries = [
        {'title': 'Model:', 'value': pif.form.put_text_input("mod_id", 16, 16)},
        {'title': '', 'value': pif.form.put_button_input()},
        {'title': '', 'value': pif.render.format_button_link("show all", "mass.cgi?tymass=related&show_all=1")},
    ]
    footer = mass_type_reinput(pif)
    footer += "</form>"
    lsection = render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)], note='', noheaders=True,
                              header=header, footer=footer)
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=[lsection]), nofooter=True)


def edit_casting_related(pif):
    useful.write_message('edit_casting_related')
    if pif.form.has('show_all'):
        return show_all_casting_related(pif)
    if not pif.form.has('mod_id'):
        return edit_casting_related_ask(pif)

    print(pif.render.format_head())
    mod_id = pif.form.get_raw('mod_id')
    section_id = pif.form.get_raw('section_id', 'single')
    # 'columns': ['id', 'model_id', 'related_id', 'section_id', 'picture_id', 'description'],
    print('edit_casting_related', pif.form, '<br>')
    print('This currently only handles single.<br>')

    revlist = pif.form.get_list('rev')
    revdict = {}
    if pif.form.has('save'):
        for root in pif.form.roots(start='i'):
            rec = {'id': pif.form.get_raw('i' + root),
                   'model_id': pif.form.get_raw('m' + root),
                   'related_id': pif.form.get_raw('r' + root),
                   'description': pif.form.get_raw('d' + root),
                   'flags': pif.form.get_raw('f' + root, '0'),
                   'section_id': section_id,
                   'picture_id': ''}
            revdict[pif.form.get_raw('m' + root)] = root[1:] in revlist
            pif.dbh.update_casting_related(rec)
        print(revdict)
        for upd_id in revdict:
            if revdict[upd_id]:
                pif.dbh.update_flags('base_id', config.FLAG_MODEL_CASTING_REVISED, 0, where=f"id='{upd_id}'")
                print(upd_id, 'on<br>')
            else:
                pif.dbh.update_flags('base_id', 0, config.FLAG_MODEL_CASTING_REVISED, where=f"id='{upd_id}'")
                print(upd_id, 'off<br>')

    # id          | int(11)
    # model_id    | varchar(12)
    # related_id  | varchar(12)
    # section_id  | varchar(16)
    # picture_id  | varchar(12) - always blank for single
    # description | varchar(256)

    crl_m = pif.dbh.fetch_casting_relateds(mod_id=mod_id, section_id=section_id)
    crl_r = pif.dbh.fetch_casting_relateds(rel_id=mod_id, section_id=section_id)

    crd_m = {x['casting_related.related_id']: x for x in crl_m}
    crd_r = {x['casting_related.model_id']: x for x in crl_r}
    keys = set(list(crd_m.keys()) + list(crd_r.keys()))
    if pif.form.has('r'):
        keys.add(pif.form.get_raw('r'))
    print('<hr>')

    def show_rel(num, cr):
        print('<td>', cr.get('casting_related.id', ''))
        print(pif.form.put_hidden_input(**{f'i.{num}': cr.get('casting_related.id', 0)}), '</td>')
        for tag, key, wid in [
                ('m', 'casting_related.model_id', 12),
                ('r', 'casting_related.related_id', 12),
                ('d', 'casting_related.description', 256),
                ('f', 'casting_related.flags', 4)]:
            print('<td>', pif.form.put_text_input(
                f'{tag}.{num}', wid, min(wid, 48), value=str(cr.get(key, '0' if tag == 'f' else ''))), '</td>')

    print('<form name="edit" method="post" action="mass.cgi">' + pif.create_token())
    print('<table border=1>')

    print('<table border=1>')
    num = 1
    revised = []
    for rel_id in keys:
        print('<tr>')
        print(f'<td>{num} {section_id}</td>')
        if rel_id in crd_r:
            print('<td colspan=4>%s</td>' % pif.render.format_link(
                '/cgi-bin/single.cgi?id=' + crd_r[rel_id]['base_id.id'], crd_r[rel_id]['base_id.rawname']))
            if crd_r[rel_id]['base_id.flags'] & config.FLAG_MODEL_CASTING_REVISED:
                revised.append(str(num))
        else:
            print('<td colspan=4></td>')
        print(f'<td>{num + 1}</td>')
        if rel_id in crd_m:
            print('<td colspan=4>%s</td>' % pif.render.format_link(
                '/cgi-bin/single.cgi?id=' + crd_m[rel_id]['base_id.id'], crd_m[rel_id]['base_id.rawname']))
            if crd_m[rel_id]['base_id.flags'] & config.FLAG_MODEL_CASTING_REVISED:
                revised.append(str(num + 1))
        else:
            print('<td colspan=4></td>')
        print('</tr>')
        print('<tr>')
        print('<td>%s</td>' % pif.form.put_checkbox('rev', [(str(num), 'R')], checked=revised))
        if rel_id in crd_r:
            print('<td colspan=4>%s</td>' % pif.render.format_image_required(
                mod_id, pdir=config.IMG_DIR_MAN, largest=mbdata.IMG_SIZ_SMALL))
        else:
            print('<td colspan=4></td>')
        print('<td>%s</td>' % pif.form.put_checkbox('rev', [(str(num + 1), 'R')], checked=revised))
        if rel_id in crd_m:
            print('<td colspan=4>%s</td>' % pif.render.format_image_required(
                rel_id, pdir=config.IMG_DIR_MAN, largest=mbdata.IMG_SIZ_SMALL))
        else:
            print('<td colspan=4></td>')
        print('</tr>')
        print('<tr>')
        if rel_id in crd_m:
            show_rel(num, crd_m[rel_id])
        else:
            show_rel(num, {'casting_related.model_id': mod_id, 'casting_related.related_id': rel_id})
        num += 1
        if rel_id in crd_r:
            show_rel(num, crd_r[rel_id])
        else:
            show_rel(num, {'casting_related.model_id': rel_id, 'casting_related.related_id': mod_id})
        print('</tr>')
        num += 1
    print('</table>')

    print(pif.form.put_button_input('save'))
    print(pif.form.put_hidden_input(mod_id=pif.form.get_raw('mod_id')))
    print(mass_type_reinput(pif))
    print(pif.form.put_hidden_input(section_id=section_id))
    print('</form><hr>')
    if pif.form.has('mod_id'):
        print('<form name="add" action="mass.cgi" onsubmit="add.disabled=true; return true;">' + pif.create_token())
        print(pif.form.put_hidden_input(mod_id=pif.form.get_raw('mod_id'), tymass='related'))
        print(pif.form.put_text_input('r', 12))
        print(pif.form.put_button_input('add'))
        print(pif.form.put_hidden_input(section_id=section_id))
        print('</form>')
    print(pif.render.format_tail())


# ------- packs ----------------------------------------------------


# should be able to either edit an existing or create a new pack here
def add_pack(pif):
    if pif.form.has('save'):
        add_pack_save(pif)
    elif pif.form.has('delete'):
        add_pack_delete(pif)
    elif pif.form.get_raw('pack'):
        return add_pack_form(pif)
    return add_pack_ask(pif)


def add_pack_ask(pif):
    pid = pif.form.get_raw('id')
    if not pid:
        pid = pif.form.get_raw('section_id')
    if '.' in pid:
        pid = pid[pid.find('.') + 1:]
    header = '<form action="mass.cgi">' + pif.create_token()
    entries = [
        {'title': 'Section ID:', 'value': pif.form.put_text_input("section_id", 12, 12, value=pid)},
        {'title': 'Pack ID:', 'value': pif.form.put_text_input("pack", 12, 12)},
        {'title': 'Var ID:', 'value': pif.form.put_text_input("var", 12, 12)},
        {'title': 'Number of Models:',
         'value': pif.form.put_text_input("num", 4, 4, value=pif.form.get_raw('num'))},
        {'title': '', 'value': pif.form.put_button_input()},
    ]
    footer = mass_type_reinput(pif)
    footer += pif.form.put_hidden_input(verbose='1')
    footer += "</form>"
    lsection = render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)], noheaders=True,
                              header=header, footer=footer)
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=[lsection]), nofooter=True)


pack_sec = {
    'playset': 'X.52',
    'rwps': 'X.61',
    'rwgs': 'X.62',
    'sfgs': 'X.62',
    '2packs': 'X.62',
    'hnh': 'X.62',
    'bk': 'X.61',
    '5packs': 'X.65',
    'lic5packs': 'X.66',
    'launcher': 'X.67',
    '10packs': 'X.68',
}
pack_layout = {
    'playset': '1xh',
    'rwps': '08s',
    'rwgs': '05s',
    'sfgs': '4xh',
    'bk': '2xh',
    'hnh': '2xh',
    '2packs': '2xh',
    '3packs': '03v',
    '5packs': '05v',
    'lic5packs': '05s',
    'launcher': '05s',
    '10packs': '10h',
}


def add_pack_form(pif):
    pack_id = pif.form.get_raw('pack')
    long_pack_id = pif.form.get_raw('pack') + ('-' + pif.form.get_raw('var') if pif.form.get_raw('var') else '')

    section_id = pif.form.get_raw('section_id')
    section = pif.dbh.fetch_section(sec_id=section_id, category='MP')
    page_id = section.page_id if section else 'packs.5packs'
    lineup_sec = pack_sec.get(section_id, 'X.65')
    year = pack_id[:4]
    if not year.isdigit():
        year = '0000'
    base_id = pif.dbh.fetch_base_id(id=pack_id)
    useful.write_message('base_id', pack_id, base_id)
    pack = tables.Results('pack', pif.dbh.fetch_pack(id=pack_id, var=pif.form.get_raw('var')))
    useful.write_message('pack', pack_id, pif.form.get_raw('var'), pack)
    pack_img = pif.render.find_image_file(long_pack_id, pdir=config.IMG_DIR_PROD_PACK, largest='g')

    header = '<hr>\n'
    header += str(pif.form) + '<hr>\n'
    header += '<form action="mass.cgi">\n' + pif.create_token()
    header += '<input type="hidden" name="verbose" value="1">\n'
    header += '<input type="hidden" name="tymass" value="pack">\n'

    if base_id:
        header += id_attributes(pif, 'base_id', base_id)
    else:
        base_id = {
            'id': pack_id,
            'first_year': year,
            'model_type': 'MP',
            'rawname': '',
            'description': '',
            'flags': 0,
        }
    if pack:
        pack = pack[0]
        header += id_attributes(pif, 'pack', pack)
    else:
        pack = {
            'id': pack_id,
            'var': pif.form.get_raw('var'),
            'page_id': page_id,
            'section_id': section_id,
            'end_year': year,
            'region': 'W',
            'layout': pack_layout.get(section_id, '05v'),
            'product_code': '',
            'material': 'C',
            'country': 'TH',
            'note': '',
        }

    header += pif.render.format_button_link("edit", f"imawidget.cgi?d=.{config.IMG_DIR_PROD_PACK}&f={pack_id}.jpg")
    header += pif.render.format_button_link("upload", "upload.cgi?d=.%s&n=%s" % (
        config.IMG_DIR_PROD_PACK.replace('pic', 'lib'), pack_id))
    header += '%(page_id)s/%(id)s<br>' % pack
    header += '/'.join(pack_img) + '<br>'
    header += '<a href="imawidget.cgi?d=./%s&f=%s">%s</a>' % (
        pack_img + (pif.render.format_image_required(long_pack_id, pdir=config.IMG_DIR_PROD_PACK, largest='g'),))
    header += '<a href="imawidget.cgi?d=.%s&f=%s.jpg">%s</a><br>' % (
        config.IMG_DIR_MAN, 's_' + pack_id, pif.render.format_image_required('s_' + pack_id, pdir=config.IMG_DIR_MAN))
    header += pif.render.format_image_required(long_pack_id, pdir=config.IMG_DIR_PROD_PACK) + '<br>'

    pack_num = int(pack['note'][2:-1]) if pack['note'].startswith('(#') else 0
    linmod = pif.dbh.depref('lineup_model', pif.dbh.fetch_lineup_model(where=f"mod_id='{pack_id}'"))
    linmod = linmod[0] if linmod else {
        'id': 0,  # delete later
        'base_id': '%s%s%02d' % (year, lineup_sec.replace('.', ''), pack_num),
        'mod_id': pack_id,
        'number': pack_num,
        'display_order': pack_num,
        'flags': 0,
        'style_id': 'lg',
        'picture_id': '',
        'region': lineup_sec,
        'year': year,
        'name': base_id['rawname'],
        'page_id': 'year.' + year,
    }
    linmod['flags'] = linmod['flags'] or 0
    x_linmods = [x['base_id'][7:] for x in pif.dbh.fetch_lineup_models(year, lineup_sec)
                 if x.get('region') == lineup_sec]
    x_linmods.sort()
    llistix = render.Listix(note=header)
    llistix.section.append(entry_form(pif, 'base_id', base_id))
    llistix.section.append(entry_form(pif, 'pack', pack))
    llistix.section.append(entry_form(
        pif, 'lineup_model', linmod,
        note=pif.form.put_checkbox('nope', [('1', 'nope')], ['1'] if not linmod.get('id') else [])))
    llistix.section[-1].header = 'in use: %s<br>\n' % ', '.join(x_linmods) + llistix.section[-1].header

    # editor
    # useful.write_message('add_pack_model', pack, long_pack_id)
    llistix.section.append(add_pack_model(pif, pack, long_pack_id))

    # related
    relateds = pif.dbh.fetch_packs_related(pack_id)
    footer = 'related '
    footer += pif.render.format_button_link('edit', '?tymass=related&section_id=packs&mod_id=%s' % pack_id)
    footer += '<br>\n'
    for rel in relateds:
        footer += rel['pack.id'] + '<br>\n'

    footer += pif.form.put_button_input("save")
    footer += pif.form.put_button_input("delete")
    footer += '</form>'
    llistix.section[-1].footer = footer

    return pif.render.format_template('simplelistix.html', llineup=llistix)


def add_pack_model(pif, pack, long_pack_id):
    # there may be a better way to do this.
    cols = ['mod', 'disp', 'style_id']  # 'edit']
    pmodels = {x + 1: {'pack_model.display_order': x + 1} for x in range(pif.form.get_int('num'))}
    if pack.get('id'):
        model_list = pif.dbh.fetch_pack_models(
            pack_id=pack['id'], pack_var=pack['var'], page_id=pack.get('page_id'))

        # for mod in pif.dbh.modify_man_items([x for x in model_list if x['pack_model.pack_id'] == long_pack_id]):
        for mod in pif.dbh.modify_man_items(model_list):
            sec_ids = [None, '', long_pack_id, long_pack_id + '.' + str(mod['pack_model.display_order'])]
            if mod['vs.sec_id'] in sec_ids:
                mod['vars'] = []
                if not pmodels.get(mod['pack_model.display_order'], {}).get('pack_model.mod_id'):
                    pmodels[mod['pack_model.display_order']] = mod

    entries = [
        {
            'mod':
                pif.form.put_hidden_input(**{'pm.id.%s' % key: mod.get('pack_model.id', '0'),
                                             'pm.pack_id.%s' % key: long_pack_id}) +
                # pif.render.format_link("single.cgi?id=%s" % mod.get('pack_model.mod_id', ''),
                #                        mod.get('pack_model.mod_id', '')) + ' ' +
                pif.form.put_text_input("pm.mod_id.%s" % key, 8, 8, value=mod.get('pack_model.mod_id', '')),
            'disp': pif.form.put_text_input(
                "pm.display_order.%s" % key, 2, 2, value=mod.get('pack_model.display_order', '')),
            'style_id': pif.form.put_text_input(
                "pm.style_id.%s" % key, 3, 3, value=mod.get('pack_model.style_id', '')),
            # 'edit': pif.render.format_button_link(
            #     'edit', pif.dbh.get_editor_link('pack_model',
            #                                     pif.dbh.make_id('pack_model', mod, 'pack_model.'))),
        } for key, mod in sorted(pmodels.items())]
    return render.Section(colist=cols, range=[render.Range(entry=entries)], noheaders=False, header='pack_model<br>')


def add_pack_delete(pif):
    if not pif.duplicate_form:
        # print('delete base_id', pif.form.get_raw('base_id.id'), '<br>')
        pif.dbh.delete_base_id({'id': pif.form.get_raw('base_id.id')})
        # print('delete pack', pif.form.get_raw('pack.id'), '<br>')
        pif.dbh.delete_pack(pif.form.get_raw('pack.id'))
        pif.dbh.delete_pack_models(pif.form.get_raw('pack.page_id'), pif.form.get_raw('pack.id'))
        # print('delete lineup_model', pif.form.get_raw('lineup_model.id'), '<br>')
        pif.dbh.delete_lineup_model({'id': pif.form.get_int('lineup_model.id')})


def get_correct_model_id(pif, mod_id):
    casting = pif.dbh.fetch_casting_raw(mod_id)
    if casting:
        return casting.get('casting.id', mod_id)
    alias = pif.dbh.fetch_alias(mod_id)
    if alias:
        return alias.get('base_id.id', mod_id)
    return mod_id


def add_pack_save(pif):
    pack_id = pif.form.get_raw('pack.id') + ('-' + pif.form.get_raw('pack.var') if pif.form.get_raw('pack.var') else '')
    useful.write_message(pack_id)

    mods = [x[6:] for x in pif.form.keys(start='pm.id.')]
    pms = [
        {
            'id': pif.form.get_int('pm.id.' + mod),
            'pack_id': pack_id,
            'mod_id': get_correct_model_id(pif, pif.form.get_raw('pm.mod_id.' + mod)),
            'var_id': pif.form.get_raw('pm.var_id.' + mod),
            'display_order': pif.form.get_int('pm.display_order.' + mod),
            'style_id': pif.form.get_str('pm.style_id.' + mod),
        }
        for mod in mods]
    pack = pif.dbh.make_values('pack', pif.form, 'pack.')
    base_id = pif.dbh.make_values('base_id', pif.form, 'base_id.')
    base_id['flags'] = base_id['flags'] or 0
    o_pack_id = pif.form.get_raw('o_pack_id')
    o_base_id_id = pif.form.get_raw('o_base_id_id')
    useful.write_message('pms', pms)
    useful.write_message('pack', pack)
    useful.write_message('base_id', base_id)
    useful.write_message('o_pack_id', pif.form.has('o_pack_id'), o_pack_id)
    useful.write_message('o_base_id_id', pif.form.has('o_base_id_id'), o_base_id_id)

    if pif.duplicate_form:
        return

    if pif.form.has('o_base_id_id'):  # update existing records
        pif.dbh.update_base_id(pif.form.get_raw('o_base_id_id'), base_id)
    else:
        pif.dbh.add_new_base_id(base_id, verbose=True)

    if pif.form.has('o_pack_id'):  # update existing records
        pif.dbh.update_pack_models(pms)
        # pif.dbh.update_variation_select_pack(pms, pack['page_id'], o_pack_id)

        p_table_data = pif.dbh.get_table_data('pack')
        if o_pack_id != pack['id']:  # change id of pack
            # pif.dbh.update_variation_select_subid(pack['id'], pack['page_id'], o_pack_id)
            if os.path.exists(pif.render.pic_dir + '/' + o_pack_id + '.jpg'):
                os.rename(pif.render.pic_dir + '/' + o_pack_id + '.jpg',
                          pif.render.pic_dir + '/' + pack['id'] + '.jpg')
        pif.dbh.update_pack(o_pack_id, {x: pif.form.get_raw('pack.' + x) for x in p_table_data.columns})

        p_table_data = pif.dbh.get_table_data('base_id')

    else:  # add new records
        useful.write_message('add pm', pif.dbh.add_new_pack_models(pms, verbose=True))
        # useful.write_message('add vs', pif.dbh.update_variation_select_pack(
        #     pms, pack['page_id'], pack['id'], verbose=True))
        useful.write_message('add pack', pif.dbh.add_new_pack(pack, verbose=True))

    # now do lineup_model separately
    if not pif.form.get_int('nope'):
        values = pif.dbh.make_values('lineup_model', pif.form, 'lineup_model.')
        values['flags'] = values['flags'] or 0
        if pif.form.get_int('lineup_model.id'):
            # print('update line_model', values, '<br>')
            pif.dbh.update_lineup_model({'id': pif.form.get_int('lineup_model.id')}, values)
        else:
            # print('new line_model', values, '<br>')
            linmod = pif.dbh.fetch_lineup_model(where="mod_id='%s'" % values['mod_id'])
            if not linmod:  # goddamn bounciness
                # print('already<br>')
                del values['id']
                pif.dbh.insert_lineup_model(values)

    # print(pif.render.format_link("packs.cgi?page=%s&id=%s" %
    # (pif.form.get_raw('pack.section_id'), pif.form.get_raw('pack.id')), "pack"))


def id_attributes(pif, tab, dat):
    table_data = pif.dbh.get_table_data(tab)
    useful.write_message(dat)
    ids = []
    for x in table_data.id:
        long_x = f"{tab}.{x}"
        old_id = dat.id or ''
        old_id = old_id or (dat[long_x] if long_x in dat else '')
        ids.append(f'<input type="hidden" name="o_{tab}_{x}" value="{old_id}">\n')
    return '\n'.join(ids) + '\n'
    return '\n'.join(
        ['<input type="hidden" name="o_%s_%s" value="%s">\n' % (tab, f, dat.get(f, dat.get(tab + '.' + f, '')))
         for f in table_data.id]) + '\n'


def entry_form(pif, tab, dat, div_id=None, note=''):
    paren_re = re.compile(r'''\((?P<n>\d*)\)''')
    if not div_id:
        div_id = tab
    header = tab + ' ' + pif.render.format_button_link('edit', pif.dbh.get_editor_link(
        tab, pif.dbh.make_id(tab, dat, tab + '.')))
    header += pif.form.put_button_input_visibility(div_id) + ' ' + note + '<br>'
    descs = pif.dbh.describe_dict(tab)
    entries = []
    for col in pif.dbh.get_table_data(tab).columns:
        coltype = descs.get(col).get('type')
        colwidth = int(paren_re.search(coltype).group('n'))
        entries.append({'title': col, 'type': coltype, 'value': str(dat.get(col, '')),
                        'new_value': pif.form.put_text_input(
            tab + '.' + col, colwidth, min(colwidth, 80), value=dat.get(col, ''))})
    return render.Section(colist=['title', 'type', 'value', 'new_value'], range=[render.Range(entry=entries)],
                          noheaders=True, header=header)


# ------- links ----------------------------------------------------

COBRA = 1  # offline
MBXFDOC = 2
COMPARE = 3  # no scraper
WIKIA = 4
TOYVAN = 5
PSDC = 6
AREH = 7
DAN = 8
MBXF = 9
CF = 10
KULIT = 11
DCPLUS = 12
MCCH = 13  # offline
MBDB = 14
MBXU = 15
LW = 16
YT = 17

ml_re = re.compile(r'''<.*?>''', re.M | re.S)
def_re_str = r'''<a\s+href=['"](?P<u>[^'"]*)['"].*?>(?P<t>.*?)</a>'''


def url_fetch(url, data=None):
    pass


class LinkScraper(object):
    def_re = re.compile(def_re_str, re.I | re.M | re.S)

    def __init__(self, pif):
        self.pif = pif

    def url_fetch(self, url):
        return url_fetch(url, None)

    def links_parse(self, url):
        data = self.url_fetch(url)
        return [(x, useful.printablize(y)) for x, y in self.def_re.findall(data)]

    def is_valid_link(self, url, lnk):
        return not lnk.startswith('mailto:') and not lnk.startswith('javascript:')

    def clean_link(self, lnk):
        return lnk

    def clean_name(self, lnk, txt):
        return txt.replace('<', '[').replace('>', ']')

    def calc_page_id(self, lnk, txt):
        return ''

    def clean_page_id(self, page_id):
        if not page_id.startswith('single'):
            return ''
        page_id = page_id[7:]
        mod = self.pif.dbh.fetch_casting(page_id)
        if mod:
            return 'single.' + mod['id']
        mod = self.pif.dbh.fetch_casting_by_alias(page_id)
        if mod:
            return 'single.' + mod['id']
        return ''

    def scrape_link(self, url, lnk, txt):
        return {
            'page_id': self.calc_page_id(lnk, txt),
            'url': urllib.parse.urljoin(url, self.clean_link(lnk)),
            'name': self.clean_name(lnk, txt),
        }


class LinkScraperMBXFDOC(LinkScraper):
    lid = MBXFDOC


class LinkScraperWIKIA(LinkScraper):
    lid = WIKIA


class LinkScraperTOYVAN(LinkScraper):
    lid = TOYVAN


class LinkScraperPSDC(LinkScraper):
    lid = PSDC

    def is_valid_link(self, url, lnk):
        return super().is_valid_link(url, lnk) and ('index.htm' not in lnk)

    def links_parse(self, url):
        lnks = []
        for lnk in super().links_parse(url):
            for olnk in lnks:
                if olnk[0] == lnk[0]:
                    olnk[1] = olnk[1].strip() + ' ' + lnk[1].strip()
                    break
            else:
                lnks.append([lnk[0], lnk[1].strip()])
        return lnks

    def calc_page_id(self, lnk, txt):
        return 'single.' + txt[:txt.find(' ')]

    def clean_name(self, lnk, txt):
        return ml_re.sub('', txt).strip()


class LinkScraperAREH(LinkScraper):
    lid = AREH
    site_re_str = r'''<option value="(?P<u>[^'"]*)">(?P<t>.*?)</option>'''

    def links_parse(self, url):
        data = self.url_fetch(url)
        return re.compile(self.site_re_str, re.I | re.M | re.S).findall(data)

    def clean_link(self, lnk):
        return lnk[5:] if lnk.startswith('Data_') else lnk


class LinkScraperDAN(LinkScraper):
    lid = DAN

    def is_valid_link(self, url, lnk):
        return lnk.startswith('../mb') or (super().is_valid_link(url, lnk) and
                                           not lnk.startswith('man') and not lnk.startswith('../') and
                                           not lnk.startswith('http://'))

    def calc_page_id(self, lnk, txt):
        txt = self.clean_name(lnk, txt)
        return self.clean_page_id('single.' + txt[:txt.find(' ')]) if txt else ''

    def clean_name(self, lnk, txt):
        return ml_re.sub('', txt).strip()


class LinkScraperMBXF(LinkScraper):
    lid = MBXF


class LinkScraperCF(LinkScraper):
    lid = CF

    def clean_name(self, lnk, txt):
        return ml_re.sub('', txt)


class LinkScraperKULIT(LinkScraper):
    lid = KULIT


class LinkScraperDCPLUS(LinkScraper):
    lid = DCPLUS


class LinkScraperMBDB(LinkScraper):
    lid = MBDB

    def links_parse(self, url):
        if 'list.php' in url:
            return super().links_parse(url)
        topdata = self.url_fetch(url)
        top_re_str = r'''<a\s+href=['"](?P<u>list.php?[^'"]*)['"].*?>(?P<t>.*?)</a>'''
        toplinks = re.compile(top_re_str, re.I | re.M | re.S).findall(topdata)
        links = []
        for lnk in toplinks:
            links.extend(super().links_parse(urllib.parse.urljoin(url, lnk[0])))
        return links

    def is_valid_link(self, url, lnk):
        return super().is_valid_link(url, lnk) and not ('list.php' in lnk or 'index.php' in lnk)

    def calc_page_id(self, lnk, txt):
        return 'single.MB' + self.clean_name(lnk, txt) if 'showcar.php' in lnk else ''

    def clean_name(self, lnk, txt):
        return lnk[lnk.rfind('=') + 1:]


class LinkScraperMBXU(LinkScraper):
    lid = MBXU

    def url_fetch(self, url):
        urlp = urllib.parse.urlparse(url)
        url = urllib.parse.urlunparse(urlp[:3] + ('', '', ''))
        data = urllib.parse.parse_qs(urlp.query)
        return url_fetch(url, data)


class LinkScraperLW(LinkScraper):
    lid = LW


class LinkScraperYT(LinkScraper):
    lid = YT
    def_re = re.compile(r'''<a href="(?P<url>/watch\?[^"]*)"\s.*?\stitle="(?P<name>[^"]*)"''')

    def links_parse(self, url):
        links = super().links_parse(url)
        return [x for x in links if '/watch?' in x[0]]

    def calc_page_id(self, lnk, txt):
        return 'links.others'


link_scraper = {
    MBXFDOC: LinkScraperMBXFDOC,
    WIKIA: LinkScraperWIKIA,
    TOYVAN: LinkScraperTOYVAN,
    PSDC: LinkScraperPSDC,
    AREH: LinkScraperAREH,
    DAN: LinkScraperDAN,
    MBXF: LinkScraperMBXF,
    CF: LinkScraperCF,
    KULIT: LinkScraperKULIT,
    DCPLUS: LinkScraperDCPLUS,
    MBDB: LinkScraperMBDB,
    MBXU: LinkScraperMBXU,
    LW: LinkScraperLW,
    YT: LinkScraperYT,
}


def add_links(pif):
    if pif.form.has('save'):
        return add_links_final(pif)
    elif pif.form.has('url'):
        return add_links_scrape(pif)
    return add_links_ask(pif)


def add_links_ask(pif):
    '''Top level of phase 1.'''
    asslinks = pif.dbh.fetch_link_lines(flags=config.FLAG_LINK_LINE_ASSOCIABLE)

    entries = [
        {'title': "URL to scrape:", 'value': pif.form.put_text_input("url", 256, 80, value='')},
        {'title': "Section ID:", 'value': pif.form.put_text_input("section_id", 256, 80, value='single')},
        {'title': "Associated Link:", 'value': pif.form.put_select(
            'associated_link', [(0, '')] + [(x['link_line.id'], x['link_line.name']) for x in asslinks])},
        {'title': '', 'value': pif.form.put_button_input()},
    ]

    header = '<form name="mass" action="mass.cgi">' + pif.create_token()
    footer = pif.form.put_hidden_input(tymass='links') + "</form><p>"

    for lnk in asslinks:
        if lnk['link_line.id'] in link_scraper:
            footer += '{} {}<br>\n'.format(lnk['link_line.id'],
                                           pif.render.format_link(lnk['link_line.url'], lnk['link_line.name']))
    lsections = [render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)], note='', noheaders=True,
                                header=header, footer=footer)]
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=lsections), nofooter=True)


# +-----------------+--------------+------+-----+---------+----------------+
# | Field           | Type         | Null | Key | Default | Extra          |
# +-----------------+--------------+------+-----+---------+----------------+
# | id              | int(11)      | NO   | PRI | NULL    | auto_increment |
# | page_id         | varchar(20)  | NO   |     |         |                |
# | section_id      | varchar(20)  | YES  |     |         |                |
# | display_order   | int(3)       | YES  |     | 0       |                |
# | flags           | int(11)      | YES  |     | 0       |                |
# | associated_link | int(11)      | YES  |     | 0       |                |
# | last_status     | varchar(5)   | YES  |     | NULL    |                |
# | link_type       | varchar(1)   | YES  |     |         |                |
# | country         | varchar(2)   | YES  |     |         |                |
# | url             | varchar(256) | YES  |     |         |                |
# | name            | varchar(128) | YES  |     |         |                |
# | description     | varchar(512) | YES  |     |         |                |
# | note            | varchar(256) | YES  |     |         |                |
# +-----------------+--------------+------+-----+---------+----------------+
# 8412 | single.MB897 | single | 7 | 0 | 7 | 200 | l || http://www.areh.de/HTML/Bas1142.html | Blaze Blaster(2013) |||
# 8413 | single.MB899 | single | 7 | 0 | 7 | 200 | l || http://www.areh.de/HTML/Bas1144.html | Questor(2013)       |||


def add_links_scrape(pif):
    '''Top level of phase 2.'''
    url = pif.form.get_raw('url')
    site = pif.form.get_int('associated_link')
    scraper = link_scraper.get(site)
    if not scraper:
        raise useful.SimpleError("no scraper for", site)
    scraper = scraper(pif)

    header = '<form method="post" action="mass.cgi">' + pif.create_token()

    columns = ['ch', 'url', 'page_id', 'name', 'description', 'country']
    found = 0
    cnt = 1
    entries = []

    for lnk, txt in scraper.links_parse(url):
        if not scraper.is_valid_link(url, lnk):
            continue
        dat = scraper.scrape_link(url, lnk, txt.strip())
        if pif.dbh.fetch_link_line_url(dat['url']):
            found += 1
            continue
        entries.append({
            'ch': pif.form.put_checkbox('ch.' + str(cnt), [('1', '')], checked=['1']),
            'url':
                pif.render.format_link(dat['url']) +
                pif.form.put_hidden_input(**{'url.' + str(cnt): dat['url']}),
            'page_id': pif.form.put_text_input('page_id.' + str(cnt), 256, 20, dat['page_id']),
            'name': pif.form.put_text_input('name.' + str(cnt), 256, 40, dat['name']),
            'description': pif.form.put_text_input('description.' + str(cnt), 256, 20, ''),
            'country': pif.form.put_text_input('country.' + str(cnt), 2, 2, ''),
        })
        cnt += 1
    footer = pif.form.put_button_input('save')
    footer += pif.form.put_hidden_input(tymass='links')
    footer += "%d found and dropped" % found
    footer += "</form>"

    lsections = [render.Section(colist=columns, range=[render.Range(entry=entries)],
                                header=header, footer=footer)]
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=lsections), nofooter=True)


def add_links_final(pif):
    '''Top level of phase 3.'''
    # print(pif.form, '<hr>')
    site = pif.form.get_int('associated_link')
    # cheating: leaving the dot off here removes it from the get_dict call.
    ostr = ''
    for key in pif.form.roots(start='page_id'):
        link_vals = pif.form.get_dict(end=key)
        if link_vals.get('ch'):
            del link_vals['ch']
            link_vals.update({
                'display_order': site,
                'flags': 0, 'country': link_vals.get('country', ''),
                'description': link_vals.get('description', ''),
                'associated_link': site, 'page_id': link_vals.get('page_id', ''),
                'note': '', 'last_status': None, 'link_type': 'l'})
            ostr += str(link_vals)
            ostr += ' ' + str(pif.dbh.insert_link_line(link_vals, verbose=True))
            ostr += '<br>\n'
    return pif.render.format_template('blank.html', content=ostr)

# ------- book -----------------------------------------------------

# +-----------+-------------+------+-----+---------+----------------+
# | Field     | Type        | Null | Key | Default | Extra          |
# +-----------+-------------+------+-----+---------+----------------+
# | id        | int(11)     | NO   | PRI | NULL    | auto_increment |
# | author    | varchar(64) | YES  |     |         |                |
# | title     | varchar(64) | YES  |     |         |                |
# | publisher | varchar(32) | YES  |     |         |                |
# | year      | varchar(4)  | YES  |     |         |                |
# | isbn      | varchar(16) | YES  |     |         |                |
# | flags     | int(11)     | YES  |     | 0       |                |
# | pic_id    | varchar(16) | YES  |     |         |                |
# +-----------+-------------+------+-----+---------+----------------+


def add_book(pif):
    if pif.form.has('save'):
        return add_book_final(pif)
    elif pif.form.has('clone'):
        return add_book_ask(pif, pif.form.get_int('id'))
    return add_book_ask(pif)


def add_book_ask(pif, book_id=None):
    book = {}
    if book_id:
        book = pif.dbh.fetch('book', where="id=%s" % book_id, tag='mass_book')
        book = book[0] if book else {}

    header = '<form name="mass" action="mass.cgi">' + pif.create_token()
    entries = [
        {'title': "ID:",
         'value': pif.form.put_text_input("id", 64, 64, value='') + pif.form.put_button_input('clone')},
    ]
    lsections = [render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)], noheaders=True,
                                header=header, footer='<br>')]
    entries = [
        {'title': "Author:",
         'value': pif.form.put_text_input("author", 64, 64, value=book.get('book.author', ''))},
        {'title': "Title:", 'value': pif.form.put_text_input("title", 64, 64, value=book.get('book.title', ''))},
        {'title': "Publisher:",
         'value': pif.form.put_text_input("publisher", 32, 32, value=book.get('book.publisher', ''))},
        {'title': "Year:", 'value': pif.form.put_text_input("year", 4, 4, value=book.get('book.year', ''))},
        {'title': "ISBN:", 'value': pif.form.put_text_input("isbn", 16, 16, value=book.get('book.isbn', ''))},
        {'title': "Hidden:", 'value': pif.form.put_checkbox('hidden', [('1', 'yes')])},
        {'title': "Picture ID:",
         'value': pif.form.put_text_input("pic_id", 16, 16, value=book.get('book.pic_id', ''))},
        {'title': "Picture URL:", 'value': pif.form.put_text_input("pic_url", 256, 80, value='')},
        {'title': '', 'value': '{}{}{}{}'.format(
            pif.form.put_button_input('save'), pif.form.put_button_reset('mass'),
            pif.render.format_button_link('book', 'biblio.cgi?edit=1'),
            pif.render.format_button_link('edit', 'editor.cgi?table=book'))}
    ]
    footer = pif.form.put_hidden_input(tymass='book') + "</form><p>"
    lsections.append(render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)],
                                    noheaders=True, footer=footer))
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=lsections), nofooter=True)


def add_book_final(pif):
    ostr = str(pif.form) + '<br>'
    if not pif.form.has('title'):
        raise useful.SimpleError("No title supplied.")
    if pif.form.get_raw('isbn'):
        if pif.dbh.fetch('book', where="isbn='%s'" % pif.form.get_raw('isbn'), tag='mass_book'):
            raise useful.SimpleError("That isbn is already in use.")
    if pif.form.get_raw('pic_id') and pif.form.get_raw('pic_url'):
        if pif.dbh.fetch('book', where="pic_id='%s'" % pif.form.get_raw('pic_id'), tag='mass_book'):
            raise useful.SimpleError("That pic_id is already in use.")
        images.grab_url_file(pif.form.get_raw('pic_url'), '.' + config.IMG_DIR_BOOK, pif.form.get_raw('pic_id'))
    vals = {
        'author': pif.form.get_raw('author'),
        'title': pif.form.get_raw('title'),
        'publisher': pif.form.get_raw('publisher'),
        'year': pif.form.get_raw('year'),
        'isbn': pif.form.get_raw('isbn'),
        'flags': config.FLAG_ITEM_HIDDEN if pif.form.get_int('flags') else 0,
        'pic_id': pif.form.get_raw('pic_id'),
    }
    ostr += str(vals)
    ostr += str(pif.dbh.write('book', vals, newonly=True, tag='mass_book', verbose=True)) + '<br>'
    if vals['pic_id']:
        ostr += pif.render.format_image_required(vals['pic_id'], pdir='.' + config.IMG_DIR_BOOK)
    return pif.render.format_template('blank.html', content=ostr)


# ------- ads ------------------------------------------------------


def add_ads(pif):
    if pif.form.has('save'):
        return add_ads_final(pif)
    return add_ads_ask(pif)
    # 'base_id': ['id', 'first_year', 'model_type'='AD', 'rawname', 'description', 'flags'=0],
    # 'publication': ['id', 'country', 'section_id'='ca'],


def add_ads_ask(pif):
    ad_id = pif.form.get_raw('id')
    ad = pif.dbh.fetch_publication(ad_id)
    if ad:
        raise useful.SimpleError('Duplicate ID.')
    o_ad_id = pif.form.get_raw('id')
    yr = pif.form.get_raw('year')
    cy = pif.form.get_raw('country')
    desc = pif.form.get_raw("description")
    ad = {}
    if ad_id.startswith('ad'):
        ad = pif.dbh.fetch_publication(ad_id)
        ad = ad if ad else {}
    elif yr and cy:
        ad_id = 'ad' + cy.lower() + str(yr)
        ads = pif.dbh.fetch_publications(country=cy, year=yr, order='base_id.id', model_type='AD')
        ad_id += chr(ord(ads[-1]['base_id.id'][8]) + 1) if ads else 'a'

    header = '<form name="mass" action="mass.cgi">' + pif.create_token()
    if desc == ad_id and '_' in desc:
        desc = desc[desc.find('_') + 1:].replace('_', ' ').title()
    if not yr and not cy and ad_id.startswith('ad'):
        if ad_id[4:8].isdigit():
            yr = ad_id[4:8]
        cy = ad_id[2:4].upper()
    name = 'Advertisement'
    name += ' ;- ' + mbdata.get_countries().get(cy, 'International')
    if yr:
        name += ' - ' + yr
    entries = [
        {'title': "ID:", 'value': pif.form.put_text_input("id", 64, 64, value=ad_id)},
        {'title': "Raw Name:", 'value': pif.form.put_text_input("rawname", 64, 64, value=name)},
        {'title': "Description:", 'value': pif.form.put_text_input("description", 64, 64, desc)},
        {'title': "Year:", 'value': pif.form.put_text_input("first_year", 4, 4, value=yr)},
        {'title': "Country:", 'value': pif.form.put_text_input("country", 16, 16, value=cy)},
        {'title': '', 'value': pif.form.put_button_input('save') + pif.form.put_button_reset('mass')},
    ]
    footer = pif.form.put_hidden_input(tymass='ads')
    footer += pif.form.put_hidden_input(o_id=o_ad_id)
    footer += "</form><p>" + pif.render.format_image_required(o_ad_id, pdir=config.IMG_DIR_ADS, largest='e')
    lsections = []
    lsections.append(render.Section(colist=['title', 'value'],
                                    range=[render.Range(entry=entries)], noheaders=True, header=header, footer=footer))
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=lsections), nofooter=True)


def add_ads_final(pif):
    ostr = str(pif.form) + '<br>'
    if not pif.form.has('id'):
        raise useful.SimpleError("No id supplied.")
    ad_id = pif.form.get_raw('id')
    ad = pif.dbh.fetch_publication(ad_id)
    if ad:
        raise useful.SimpleError('Duplicate ID.')
    ostr += str(pif.dbh.add_new_base_id({
        'id': ad_id,
        'first_year': pif.form.get_raw('first_year'),
        'model_type': 'AD',
        'rawname': pif.form.get_raw('rawname'),
        'description': pif.form.get_raw('description'),
        'flags': 0,
    })) + '<br>'
    # 'publication': ['id', 'country', 'section_id'='ca'],
    ostr += str(pif.dbh.add_new_publication({
        'id': ad_id,
        'country': pif.form.get_raw('country'),
        'section_id': '',
    })) + '<br>'
    o_id = pif.form.get_raw('o_id')
    if o_id and o_id != ad_id and os.path.exists('.' + config.IMG_DIR_ADS + '/' + o_id + '.jpg'):
        useful.file_mover('.' + config.IMG_DIR_ADS + '/' + o_id + '.jpg',
                          '.' + config.IMG_DIR_ADS + '/' + ad_id + '.jpg', mv=True)
    return pif.render.format_template('blank.html', content=ostr)

# ------- matrix ---------------------------------------------------

# should be able to either edit an existing or create a new matrix here


def add_matrix(pif):
    if pif.form.has('save'):
        add_matrix_save(pif)
    elif pif.form.get_raw('section_id'):
        return add_matrix_form(pif)
    return add_matrix_ask(pif)


def add_matrix_ask(pif):
    llineup = render.Listix()
    pid = pif.form.get_raw('id')
    if '.' in pid:
        pid = pid[pid.find('.') + 1:]
    header = '<form action="mass.cgi">' + pif.create_token()
    entries = [
        {'title': 'Year:', 'value': pif.form.put_text_input("year", 4, 4)},
        {'title': 'Page ID:', 'value': pif.form.put_text_input("page_id", 24, 24)},
        {'title': 'Page Name (if new):', 'value': pif.form.put_text_input("page_name", 48, 48)},
        {'title': 'Section ID:', 'value': pif.form.put_text_input("section_id", 24, 24, value=pid)},
        {'title': 'Number of Models:', 'value': pif.form.put_text_input("num", 4, 4)},
        {'title': 'Model List File:', 'value': pif.form.put_text_input("models", 80, 80)},
        {'title': 'Ref ID:', 'value': pif.form.put_text_input("ref_id", 80, 80)},
        {'title': '', 'value': 'bar file: num|man_id|name -- only one of: number, file, ref_id'},
        {'title': '', 'value': pif.form.put_button_input()},
    ]
    footer = pif.form.put_hidden_input(tymass='matrix', verbose='1')
    footer += "</form>"
    llineup.section.append(
        render.Section(colist=['title', 'value'], range=[render.Range(entry=entries)], noheaders=True,
                       header=header, footer=footer))
    header = '<form action="vars.cgi" name="vars" method="post">' + pif.create_token()
    entries = [
        {'title': '', 'value': 'Model Search'},
        {'title': 'MAN:', 'value': pif.form.put_text_input("mod", 12, 12)},
        {'title': 'Body:', 'value': pif.form.put_text_input("text_body", 24, 24)},
        {'title': 'Note:', 'value': pif.form.put_text_input("text_note", 24, 24)},
        {'title': '', 'value': pif.form.put_button_input()},
    ]
    footer = pif.form.put_hidden_input(edt='1')
    footer += "</form>"
    llineup.section.append(render.Section(
        colist=['title', 'value'], range=[render.Range(entry=entries)], noheaders=True, header=header, footer=footer))
    return pif.render.format_template('simplelistix.html', llineup=llineup, nofooter=True)


'''
page_info_create = {
    'id': page_id,
    'flags': 0,
    'format_type': 'matrix',
    'title': page_name,
    'pic_dir': 'pic/prod/series',
}

section_create = {
    'id': section_id,
    'page_id': page_id,
    'display_order': 2,  # highest plus one
    'flags': 0,
    'name': year,
    'columns': 3,
    'start': 0,
}

matrix_model_create = {
    'section_id': section_id,
    'display_order': num,
    'page_id': page_id,
    'range_id': num,
    'mod_id': man_id,
    'flags': 0,
    'name': name,
}
'''


def add_matrix_form(pif):
    # add picture info.  add vs ref info.
    year = pif.form.get_raw('year')
    page_id = pif.form.get_raw('page_id')
    section_id = pif.form.get_raw('section_id')
    ref_id = pif.form.get_raw('ref_id')
    page = pif.dbh.fetch_page(id=page_id)
    section = pif.dbh.fetch_section(page_id=page_id, sec_id=section_id)
    category = ''
    useful.write_message('page', str(page))
    useful.write_message('section', str(section))

    header = '<hr>\n'
    header += str(pif.form) + '<hr>\n'
    header += '<form action="mass.cgi" method="post">\n' + pif.create_token()
    header += '<input type="hidden" name="verbose" value="1">\n'
    header += '<input type="hidden" name="tymass" value="matrix">\n'

    if page:
        header += id_attributes(pif, 'page_info', page)
    else:
        page = {
            'id': page_id,
            'flags': 1,
            'format_type': 'matrix',
            'pic_dir': 'pic/prod/series',
        }

    if section:
        header += id_attributes(pif, 'section', section)
    else:
        section = {
            'id': section_id,
            'page_id': page_id,
            'columns': 4,
        }

    linmod = pif.dbh.depref('lineup_model', pif.dbh.fetch_lineup_model(
        where=f"mod_id='{page_id}' and picture_id='{section_id}'"))
    linmod = linmod[0] if linmod else {
        'id': 0,  # delete later
        'base_id': '%sX1100' % year,
        'mod_id': page_id,
        'number': 0,
        'flags': 0,
        'style_id': 'lg',
        'picture_id': section_id,
        'region': 'X.11',
        'year': year,
        'name': page.get('name', ''),
        'page_id': 'year.' + year,
    }
    linmod['flags'] = linmod['flags'] or 0

    llistix = render.Listix(note=header)
    llistix.section.append(entry_form(pif, 'page_info', page if isinstance(page, dict) else page.todict()))
    llistix.section.append(entry_form(pif, 'section', section if isinstance(section, dict) else section.todict()))
    llistix.section.append(entry_form(
        pif, 'lineup_model', linmod,
        note=pif.form.put_checkbox('nope', [('1', 'nope')], ['1'] if not linmod['id'] else [])))

    mm, category = add_matrix_model(pif, section, ref_id)
    llistix.section.append(mm)
    llistix.section[0].range[-1].entry.append({
        'title': 'category', 'type': 'varchar(8)', 'value': category,
        'new_value': pif.form.put_text_input('category', 8, 8, value=category) + ' for variation_select'})

    footer = ''
    footer += pif.form.put_button_input("save")
    footer += '</form>'
    llistix.section[-1].footer = footer

    return pif.render.format_template('simplelistix.html', llineup=llistix)


def add_matrix_model(pif, section, ref_id=None):
    category = ''
    cols = ['display_order', 'mod_id', 'var_id', 'name', 'range_id', 'flags', 'edit']
    # rewrite this; could now come from a file, preloaded
    # also, with a ref_id, could be read via varsels

    def mod_name(mod):
        return mod.get('matrix_model.name', mod.get('base_id.rawname', ''))

    if ref_id:
        models = pif.dbh.fetch_variation_by_select(ref_id=ref_id, sec_id=section['id'])
        category = models[0]['vs.category'] if models else section['id'] if section else ''
        mmodels = {x['vs.ran_id']: {
            'matrix_model.section_id': section['id'],
            'matrix_model.display_order': x['vs.ran_id'],
            'matrix_model.page_id': section['page_id'],
            'matrix_model.range_id': x['vs.ran_id'],
            'matrix_model.mod_id': x['b.id'],
            'matrix_model.flags': 0,
            'matrix_model.name': x['b.rawname'],
        } for x in models}
    else:
        mmodels = {x + 1: {'matrix_model.display_order': x + 1, 'vars': []} for x in range(pif.form.get_int('num'))}
        mmodelsdb = pif.dbh.fetch_matrix_models_variations(section['page_id'], section=section['id'])
        for mmdb in mmodelsdb:
            if mmdb['vs.sec_id'] and mmdb['vs.sec_id'] != section['id']:
                continue
            if mmdb['vs.category']:
                category = mmdb['vs.category']
            dispo = mmdb['matrix_model.display_order']
            if dispo not in mmodels:
                mmodels[dispo] = {'matrix_model.display_order': dispo, 'vars': []}
            if mmodels[dispo].get('matrix_model.id'):
                useful.write_message(
                    'duplicate matrix_model entry found:', mmodels[dispo]['matrix_model.id'], mmdb['matrix_model.id'])
            mmodels[dispo].update(mmdb)
            if mmdb['v.var']:
                mmodels[dispo]['vars'].append(mmdb['v.var'])

    entries = [
        {
            'mod_id': pif.form.put_hidden_input({
                'mm.id.%s' % key: mod.get('matrix_model.id', ''),
                'mm.matrix_id.%s' % key:
                    mod.get('matrix_model.matrix_id', '')}) +
                pif.render.format_link("single.cgi?id=%s" % mod.get('matrix_model.mod_id', ''),
                                       mod.get('matrix_model.mod_id', '')) + ' ' +
                pif.form.put_text_input("mm.mod_id.%s" % key, 8, 8, value=mod.get('matrix_model.mod_id', '')),
            'var_id': pif.form.put_text_input(
                "mm.var_id.%s" % key, 20, 20, value='/'.join(sorted(set(mod.get('vars', []))))),
            'display_order': 'disp ' + pif.form.put_text_input(
                "mm.display_order.%s" % key, 3, 3, value=mod.get('matrix_model.display_order', '')),
            'edit': pif.render.format_button_link(
                'edit', pif.dbh.get_editor_link(
                    'matrix_model',
                    pif.dbh.make_id('matrix_model', mod, 'matrix_model' + '.'))) + str(mod.get('matrix_model.id', '')),
            'name': pif.form.put_text_input("mm.name.%s" % key, 80, 20, value=mod_name(mod)),
            'range_id': pif.form.put_text_input(
                "mm.range_id.%s" % key, 4,
                value=mod.get('matrix_model.range_id', mod.get('matrix_model.display_order', '0'))),
            'flags': pif.form.put_text_input("mm.flags.%s" % key, 4, value=str(mod.get('matrix_model.flags', 0))),
        }
        for key, mod in sorted(mmodels.items())]

    return render.Section(colist=cols, range=[render.Range(entry=entries)], header='matrix_model<br>',
                          note=pif.form.put_checkbox('mmclear', [('1', 'clear')], ['1'])), category


def add_matrix_save(pif):
    category = pif.form.get_raw('category', '')
    page_info = pif.form.get_dict(start='page_info.')
    section = pif.form.get_dict(start='section.')
    lineup_model = pif.form.get_dict(start='lineup_model.')
    # useful.write_message('page_info', page_info)
    pif.dbh.insert_or_update_page(page_info)
    # useful.write_message('section', section)
    pif.dbh.insert_or_update_section(section)
    if not pif.form.get_int('nope'):
        useful.write_message('lineup_model', lineup_model)
        if 'id' in lineup_model and not lineup_model['id']:
            del lineup_model['id']
        pif.dbh.insert_lineup_model(lineup_model, newonly=False)
    thisis = {'page_id': page_info['id'], 'section_id': section['id']}
    modvars = []
    # this really likes making duplicates.  stahp.
    if pif.form.get('mmclear') == '1':
        print('clearing', page_info['id'], section['id'])
        print(str(pif.dbh.delete_matrix_models(page_id=page_info['id'], sec_id=section['id'])) + '<br>')
    for root in pif.form.roots(start='mm.name'):
        mm = pif.form.get_dict(start='mm.', end=root)
        if not mm.get('mod_id'):
            continue
        if 'id' in mm and (not mm['id'] or not int(mm['id'])):
            del mm['id']
        if 'var_id' in mm:
            modvars.extend([(mm['mod_id'], x) for x in mm['var_id'].split('/')])
            del mm['var_id']
        if not mm.get('name'):
            mod = pif.dbh.fetch_base_id(mm['mod_id'])
            mm['name'] = mod.rawname.replace(';', ' ')
        mm.update(thisis)
        useful.write_message('matrix_model', mm)
        pif.dbh.insert_or_update_matrix_model(mm, verbose=True)
    useful.write_message('MODVARS', modvars)
    useful.write_message('ref_id', page_info['id'], 'sec_id', section['id'], 'category', category)
    # pif.dbh.update_variation_selects_for_ref(modvars, ref_id=page_info['id'], sec_id=section['id'], category=category)
    useful.write_message(modvars, page_info['id'], section['id'], category)
    return

    # if pif.form.has('o_id'):  # update existing records
    #     pif.dbh.update_matrix_models(mms)
    #     pif.dbh.update_variation_select_matrix(pms, pif.form.get_raw('matrix.page_id'), pif.form.get_raw('o_id'))

    #     p_table_data = pif.dbh.get_table_data('matrix')
    #     if pif.form.get_raw('o_id') != pif.form.get_raw('matrix.id'):  # change id of matrix
    #         pif.dbh.update_variation_select_subid(
    #             pif.form.get_raw('matrix.id'), pif.form.get_raw('matrix.page_id'), pif.form.get_raw('o_id'))
    #         # ok, this is pretty cool.  I should do this.
    #         if os.path.exists(pif.render.pic_dir + '/' + pif.form.get_raw('o_id') + '.jpg'):
    #             os.rename(pif.render.pic_dir + '/' + pif.form.get_raw('o_id') + '.jpg',
    #                       pif.render.pic_dir + '/' + pif.form.get_raw('matrix.id') + '.jpg')
    #     pif.dbh.update_matrix(pif.form.get_raw('o_id'),
    #                           {x: pif.form.get_raw('matrix.' + x) for x in p_table_data.columns})

    #     p_table_data = pif.dbh.get_table_data('base_id')
    #     pif.dbh.update_base_id(pif.form.get_raw('o_id'),
    #                            {x: pif.form.get_raw('base_id.' + x) for x in p_table_data.columns})

    # else:  # add new records
    #     pif.dbh.add_new_matrix_models(pms)
    #     pif.dbh.update_variation_select_matrix(pms, pif.form.get_raw('matrix.page_id'), pif.form.get_raw('o_id'))
    #     pif.dbh.add_new_matrix(pif.dbh.make_values('matrix', pif.form, 'matrix.'))
    #     pif.dbh.add_new_base_id(pif.dbh.make_values('base_id', pif.form, 'base_id.'))

    # # now do lineup_model separately
    # if not pif.form.get_int('nope'):
    #     values = pif.dbh.make_values('lineup_model', pif.form, 'lineup_model.')
    #     if pif.form.get_int('lineup_model.id'):
    #         # print('update line_model', values, '<br>')
    #         pif.dbh.update_lineup_model({'id': pif.form.get_int('lineup_model.id')}, values)
    #     else:
    #         # print('new line_model', values, '<br>')
    #         linmod = pif.dbh.fetch_lineup_model(where="mod_id='%s'" % values['mod_id'])
    #         if not linmod:  # goddamn bounciness
    #             # print('already<br>')
    #             del values['id']
    #             pif.dbh.insert_lineup_model(values)

    # print(pif.render.format_link("matrixs.cgi?page=%s&id=%s" % (pif.form.get_raw('matrix.section_id'),
    # pif.form.get_raw('matrix.id')), "matrix"))


# ------- attr_pics ------------------------------------------------


def add_attr_pics(pif):
    if pif.form.has('save'):
        add_attr_pics_save(pif)
    elif pif.form.get_raw('attr_type'):
        return add_attr_pics_form(pif)
    return add_attr_pics_ask(pif)


def add_attr_pics_ask(pif):
    header = '<form action="mass.cgi">' + pif.create_token()
    entries = [
        {'title': 'Type:', 'value': pif.form.put_select('attr_type', mbdata.image_adds_list, blank='')},
        {'title': '', 'value': '{} {} {} {}'.format(
            pif.form.put_button_input(),
            pif.render.format_button_link('customs', '/cgi-bin/custom.cgi'),
            pif.render.format_button_link('errors', '/cgi-bin/errors.cgi'),
            pif.render.format_button_link('prepros', '/cgi-bin/prepro.cgi'))}
    ]
    footer = pif.form.put_hidden_input(tymass='attrpics', verbose='1') + "</form>"
    lsection = render.Section(colist=['title', 'value'],
                              range=[render.Range(entry=entries)], noheaders=True, header=header, footer=footer)
    return pif.render.format_template('simplelistix.html', llineup=render.Listix(section=[lsection]), nofooter=True)


def add_attr_pics_form(pif):
    pref = pif.form.get_raw('attr_type')
    photogs = [(x.photographer.id, x.photographer.name) for x in pif.dbh.fetch_photographers(config.FLAG_ITEM_HIDDEN)]
    credits = {x['photo_credit.name']: x['photo_credit.photographer_id']
               for x in pif.dbh.fetch_photo_credits(path=config.IMG_DIR_ADD[1:])}
    fl, rl = get_attr_pics(pif, pref)

    def attr_pic_rec(rec, recid):
        img = pref + '_' + rec['mod_id'].lower()
        if rec['picture_id']:
            img += '-' + rec['picture_id']
        pic = pif.render.format_link('upload.cgi?m={}&suff={}&d={}'.format(
            rec['mod_id'], rec['picture_id'], '.' + config.IMG_DIR_ADD),
            pif.render.fmt_img(img, alt='', pdir=config.IMG_DIR_ADD, required=True))
        desc = '{} {}<br>{} {}<br>{}<br>{}{}'.format(
            pif.render.format_link('single.cgi?id=%s' % rec['mod_id'], rec['mod_id']),
            pif.render.format_button_link('edit', pif.dbh.get_editor_link('attribute_picture', {'id': recid})),
            pif.form.put_text_input('pic_id.%s' % recid, maxlength=4, showlength=4, value=rec['picture_id']),
            pif.form.put_checkbox('do.%s' % recid, [('1', 'save')], checked=rec['do']),
            pif.form.put_checkbox('rm.%s' % recid, [('1', 'del')]),
            pif.form.put_hidden_input(**{'mod_id.%s' % recid: rec['mod_id'], 'img.%s' % recid: img}),
            pif.form.put_text_input(
                'desc.%s' % recid, maxlength=128, showlength=40,
                value='{}<br>Credit: {}'.format(
                    rec['description'],
                    pif.form.put_select('crd.%s' % recid, photogs, selected=credits.get(img), blank=''))))
        return {
            'pic': pic,
            'desc': desc,
        }

    header = '<hr>\n'
    header += '<form action="mass.cgi" method="post">\n' + pif.create_token()
    header += pif.form.put_hidden_input(verbose=1, tymass='attrpics', attr_type=pref)

    llistix = render.Listix(note=header)
    entries = [attr_pic_rec(rec, rec['id']) for rec in rl]
    lsec = render.Section(colist=['pic', 'desc'], range=[render.Range(entry=entries)], noheaders=True)
    llistix.section.append(lsec)

    entries = [attr_pic_rec(rec, 'n%s' % num) for num, rec in fl]
    lsec = render.Section(colist=['pic', 'desc'], range=[render.Range(entry=entries)], noheaders=True)
    llistix.section.append(lsec)

    footer = ''
    footer += pif.form.put_button_input("save")
    footer += '</form>'
    llistix.section[-1].footer = footer

    return pif.render.format_template('simplelistix.html', llineup=llistix)


def get_attr_pics(pif, pref):
    filelist = os.listdir('.' + config.IMG_DIR_ADD)
    filelist = sorted(list(set([x for x in filelist if x.startswith(pref + '_') and x.endswith('.jpg')])))
    rl = []

    pics = pif.dbh.fetch_attribute_pictures_by_type(pref)
    for pic in pics:
        if not pic.get('base_id.id'):
            print(pic, '<br>')
            continue
        if pic['attribute_picture.picture_id']:
            pic_name = '%s_%s-%s.jpg' % (pic['attribute_picture.attr_type'], pic['base_id.id'].lower(),
                                         pic['attribute_picture.picture_id'])
        else:
            pic_name = '%s_%s.jpg' % (pic['attribute_picture.attr_type'], pic['base_id.id'].lower())
        rec = {'mod_id': pic['base_id.id'], 'attr_id': pic['attribute_picture.attr_id'], 'attr_type': pref,
               'picture_id': pic['attribute_picture.picture_id'], 'description': pic['attribute_picture.description'],
               'id': pic['attribute_picture.id'], 'do': ['1']}
        rl.append(rec)
        if pic_name in filelist:
            filelist.remove(pic_name)
        else:
            pass  # print('no pic for', pic_name)
    rl.sort(key=lambda x: (x['mod_id'].lower(), x['picture_id']))
    num = 1
    fl = []
    for fn in filelist:
        if fn.startswith(pref + '_') and fn.endswith('.jpg'):
            fn = fn[2:-4]
            mod_id, pic_id = fn.split('-', 1) if '-' in fn else [fn, '']
            base_id = pif.dbh.fetch_base_id(mod_id)
            if base_id:
                mod_id = base_id['base_id.id']
            # look mod_id up to get casing
            rec = {'mod_id': mod_id, 'attr_id': 0, 'attr_type': pref, 'picture_id': pic_id, 'description': '', 'do': []}
            fl.append((num, rec))
            num += 1
    return fl, rl


def add_attr_pics_save(pif):
    add_dir = '.' + config.IMG_DIR_ADD
    pref = pif.form.get_raw('attr_type')
    for apid in pif.form.roots(start='mod_id.'):
        inp = pif.form.get_dict(end='.' + apid)
        oimg = pif.form.get_raw('img.' + apid)
        nimg = pref + '_' + inp['mod_id'].lower()
        if inp['pic_id']:
            nimg += '-' + inp['pic_id']
        print(apid, inp, nimg)
        rec = {
            'mod_id': pif.form.get_raw('mod_id.' + apid), 'picture_id': pif.form.get_raw('pic_id.' + apid),
            'description': pif.form.get_raw('desc.' + apid), 'attr_id': 0, 'attr_type': pref,
        }

        if pif.form.get_bool('rm.' + apid):
            print('del', pif.dbh.delete_attribute_picture(apid))
        if pif.form.get_bool('do.' + apid):
            if apid.startswith('n'):
                print('add', pif.dbh.add_attribute_picture(rec))
            else:
                print('upd', pif.dbh.update_attribute_picture(rec, apid))

        if oimg != nimg and not os.path.exists(add_dir + '/' + nimg + '.jpg'):
            useful.file_mover(add_dir + '/' + oimg + '.jpg', add_dir + '/' + nimg + '.jpg', mv=True)
            if pif.form.get_raw('crd.' + apid, config.IMG_DIR_ADD[1:], oimg):
                print('crd', pif.dbh.delete_photo_credit(config.IMG_DIR_ADD[1:], oimg))

        if pif.form.get_raw('crd.' + apid):
            print('crd', pif.dbh.write_photo_credit(pif.form.get_raw('crd.' + apid), config.IMG_DIR_ADD[1:], oimg))

        print('<br>')


# ------- photogs --------------------------------------------------


def photogs_main(pif):
    if pif.form.has('save'):
        add_photogs_save(pif)
    return add_photogs_form(pif)


def add_photogs_form(pif):
    # pref = pif.form.get_raw('attr_type')
    photographers = sorted(pif.dbh.fetch_photographers(), key=lambda x: x['photographer.name'])

    def photog_rec(rec):
        recid = rec['id']
        return {
            'X': pif.form.put_checkbox('X.%s' % recid, [('1', '')],
                                       checked='1' if not rec['flags'] & config.FLAG_ITEM_HIDDEN else ''),
            'id': pif.form.put_text_input('id.%s' % recid, maxlength=4, showlength=4, value=rec['id']),
            'name': pif.form.put_text_input('name.%s' % recid, maxlength=32, showlength=32, value=rec['name']),
            'url': pif.form.put_text_input('url.%s' % recid, maxlength=128, showlength=64, value=rec['url']),
        }

    header = '<hr>\n<form action="mass.cgi" method="post">\n' + pif.create_token()
    header += pif.form.put_hidden_input(verbose=1, tymass='photogs')

    footer = pif.form.put_button_input("save")
    footer += pif.render.format_button_link('add', '/cgi-bin/editor.cgi?table=photographer&id=&add=1')
    footer += '</form>'

    entries = [photog_rec(rec) for rec in photographers]
    lsec = render.Section(colist=['X', 'id', 'name', 'url'], range=[render.Range(entry=entries)],
                          noheaders=True, footer=footer)
    llistix = render.Listix(section=[lsec], note=header)

    return pif.render.format_template('simplelistix.html', llineup=llistix)


def add_photogs_save(pif):
    for phid in pif.form.roots(start='id.'):
        inp = pif.form.get_dict(end='.' + phid)
        flags = config.FLAG_ITEM_HIDDEN if inp.get('X') else 0
        print(phid, inp, flags)
        # rec = {
        #     'id': inp['id'],
        #     'name': inp['name'],
        #     'url': inp['url'],
        #     'flags': flags,
        # }

        print('<br>')


# ------- period ---------------------------------------------------

# add/edit issue
# add/edit articles

def period_main(pif):
    if pif.form.has('save'):
        period_save(pif)

    period_id = pif.form.get_id('period')
    issue_id = pif.form.get_id('issue')
    if issue_id:
        return period_edit_issue(pif, issue_id)
    if period_id:
        return period_list(pif, period_id)
    return period_ask(pif)


def period_ask(pif, period_id=None):
    wheres = [f'flags&{config.FLAG_BOOK_MAGAZINE}={config.FLAG_BOOK_MAGAZINE}']
    if period_id:
        wheres.append(f'pub_id={period_id}')
    header = '<form>'
    footer = "</form>"
    llistix = render.Listix(section=[render.Section(colist=['q', 'a'], range=[render.Range(
        entry=[{'q': 'Periodical', 'a': pif.form.put_select('period', [
            (x['id'], x['title']) for x in pif.dbh.depref('book', pif.dbh.fetch(
                'book', where=wheres, tag='MassPeriod', verbose=True))])},
            {'q': '', 'a': pif.form.put_button_input('submit') + mass_type_reinput(pif)}])],
        noheaders=True, footer=footer)], note=header)

    return pif.render.format_template('simplelistix.html', llineup=llistix)

    # periodical ['id', 'pub_id', 'volume', 'issue', 'date', 'pages']
    # article ['id', 'per_id', 'title', 'author', 'page']


def period_list(pif, period_id):
    table = pif.dbh.get_table_data('periodical')
    wheres = [f'pub_id={period_id}']
    header = '<form>'
    footer = "</form>"

    def ent(x):
        x = pif.dbh.depref('periodical', x)
        x['id'] = pif.render.format_link(url=f'mass.cgi?issue={x["id"]}&tymass=period', txt=str(x['id']))
        return x

    entries = [ent(x) for x in pif.dbh.fetch('periodical', where=wheres, tag='MassPeriod', verbose=True)]
    llistix = render.Listix(section=[render.Section(colist=table.columns, range=[render.Range(
        entry=entries)],
        footer=footer)], note=header)

    return pif.render.format_template('simplelistix.html', llineup=llistix)


def period_edit_issue(pif, period_id):
    table = pif.dbh.get_table_data('article')
    wheres = [f'per_id={period_id}']
    header = '<form>'
    footer = "</form>"

    def ent(x):
        x = pif.dbh.depref('article', x)
        return x

    entries = [ent(x) for x in pif.dbh.fetch('article', where=wheres, tag='MassPeriod', verbose=True)]
    llistix = render.Listix(section=[render.Section(colist=table.columns, range=[render.Range(
        entry=entries)],
        footer=footer)], note=header)

    return pif.render.format_template('simplelistix.html', llineup=llistix)


def period_save(pif):
    pass


# ------- ----------------------------------------------------------


mass_mains_list = [
    ('lineup', add_lineup_main),
    ('casting', add_casting_main),
    ('pub', add_pub_main),
    ('var', add_var_main),
    ('related', edit_casting_related),
    ('pack', add_pack),
    ('links', add_links),
    ('book', add_book),
    ('ads', add_ads),
    ('matrix', add_matrix),
    ('attrpics', add_attr_pics),
    ('lineup_model', add_lm_main),
    ('period', period_main),
]

mass_mains_hidden = {
    'lineup_desc': lineup_desc_main,
    'dates': dates_main,
    'photogs': photogs_main,
    'alias': aliases_main,
    'lm_series': add_lm_series_main,
}


def mass_sections(pif):
    return '\n'.join([pif.render.format_button_link(x, f'?tymass={x}') for x, y in mass_mains_list])
