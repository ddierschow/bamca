#!/usr/local/bin/python

from __future__ import print_function
import string  # don't judge me

import basics
import config
import mbdata
import single
import useful


# ----- mack -----------------------------------------------------------


def mack_models(pif, start, end, series):
    mseries = 'MB' if 'RW' not in series else None if 'SF' in series else ''
    amods = [(mbdata.get_mack_number(rec['alias.id']), rec,) for rec in pif.dbh.fetch_aliases(type_id='mack')]
    mmods = [(mbdata.get_mack_number(rec['base_id.id']), rec,) for rec in
             pif.dbh.fetch_casting_list('sf') + pif.dbh.fetch_casting_list('rw')]
    amods = sorted([x for x in mmods + amods
                    if (x and x[0] and int(x[0][1]) >= start and int(x[0][1]) <= end and
                        not (mseries is not None and mseries != x[0][0]))],
                   key=lambda x: (x[0][1], x[0][0], x[0][2]))
    return amods


ranks = list(range(1, config.MAX_MACK_NUMBER + 1))
files = list(string.ascii_lowercase) + [x + x for x in string.ascii_lowercase]


def format_mack_text(pif, amods):
    sharedsets = []
    for pair in [[x['casting_related.model_id'], x['casting_related.related_id']]
                 for x in pif.dbh.fetch_casting_relateds(flags=config.FLAG_CASTING_RELATED_SHARED)]:
        for shared in sharedsets:
            if pair[0] in shared or pair[1] in shared:
                shared.update(pair)
                break
        else:
            sharedsets.append(set(pair))
    res = []
    bmods = {}
    for mack_id, mod in amods:
        bmods.setdefault(mack_id[0], {})
        bmods[mack_id[0]].setdefault(mack_id[1], {})
        bmods[mack_id[0]][mack_id[1]].setdefault(mack_id[2], [])
        bmods[mack_id[0]][mack_id[1]][mack_id[2]].append(mod)

    for mtype, mranks in sorted(bmods.items()):
        for mrank, mfiles in sorted(mranks.items()):
            res.append({'id': '<b>%s<b>' % mrank})
            mmods = bmods[mtype][mrank]
            for mfile in files[files.index(min(mmods)):files.index(max(mmods)) + 1]:
                ent = {
                    'id': '%s%02s-%s' % (mtype, mrank, mfile),
                    'name': '',
                    'man': '',
                    'year': '',
                    'error': '',
                    'mack_id_unf': (mtype, mrank, mfile),  # for internal use
                    'class': 'rw' if not mtype else 'sf' if mtype == 'MB' else 'mb',
                }
                if mfile not in mfiles:
                    ent['error'] = '<span class="warning">missing</span>'
                    res.append(ent)
                    continue
                for mod in mfiles[mfile]:
                    modlink = pif.render.format_link('single.cgi?id=' + mod['base_id.id'], mod['base_id.id'])
                    if ent['man']:
                        ent['man'] = '<br>'.join([ent['man'], modlink])
                        ent['name'] = '<br>'.join([ent['name'], mod['base_id.rawname'].replace(';', ' ')])
                        ent['year'] = '<br>'.join([ent['year'], mod['alias.first_year']])
                    else:
                        ent['man'] = modlink
                        ent['name'] = mod['base_id.rawname'].replace(';', ' ')
                        ent['year'] = mod.get('alias.first_year', mod.get('base_id.first_year', ''))
                if len(mfiles[mfile]) > 1:
                    for shared in sharedsets:
                        if not (set([x['base_id.id'] for x in mfiles[mfile]]) - shared):
                            break
                    else:
                        ent['error'] = ' <span class="warning">not shared</span>'
                res.append(ent)
    return [{'entry': res}] if res else []


def format_mack_html(pif, amods):
    res = [{
        'id': '%s%02s-%s' % x[0],
        'name': x[1]['base_id.rawname'].replace(';', ' '),
        'href': 'single.cgi?id=' + x[1]['base_id.id'],
        'imgstr': pif.render.format_image_required(x[1]['base_id.id'], prefix=mbdata.IMG_SIZ_SMALL),
        'mack_id_unf': x[0],  # for internal use
        'class': 'rw' if not x[0][0] else 'sf' if x[0][0] == 'MB' else 'mb',
    } for x in amods]
    return [{'entry': res}] if res else []


@basics.web_page
def mack_lineup(pif):
    pif.render.set_button_comment(pif, 'rg=%s&sec=%s&start=%s&end=%s' % (
        pif.form.get_str('region', ''), pif.form.get_str('sect', ''),
        pif.form.get_str('start', ''), pif.form.get_str('end', '')))
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append(pif.request_uri, 'Mack Numbers')
    pif.render.print_html()

    series = ['RW', 'SF'] if pif.form.get_str('sect', 'all') == 'all' else [pif.form.get_str('sect').upper()]
    range = pif.form.get_str('range', 'all')
    start = 1 if range == 'all' else pif.form.get_int('start', 1)
    end = config.MAX_MACK_NUMBER if range == 'all' else pif.form.get_int('end', config.MAX_MACK_NUMBER)
    text_list = pif.form.get_str('text', 'pic') == 'txt'

    amods = mack_models(pif, start, end, series)
    ranges = format_mack_text(pif, amods) if text_list else format_mack_html(pif, amods)

    if not ranges:
        note = 'Your request produced no models.'
        if start > config.MAX_MACK_NUMBER:
            note += '  Be sure to use numbers from 1 to %d.' % config.MAX_MACK_NUMBER
        if start > end:
            note += "  Use a start number that isn't higher than the end number."
        raise useful.SimpleError(note)

    lsec = pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
    lsec['range'] = ranges
    llineup = {'section': [lsec]}
    if text_list:
        lsec['headers'] = {'id': 'Mack ID', 'man': 'MAN ID', 'name': 'Name', 'year': 'Year', 'error': ''}
        lsec['columns'] = ['id', 'man', 'name', 'year', 'error']
        return pif.render.format_template('simplelistix.html', llineup=llineup)
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('mack.html', llineup=llineup)


# ----- ----------------------------------------------------------------


def check_man_mappings(pif, sections):
    for section in sections:
        mans = pif.dbh.fetch_casting_list(section_id=section, page_id='manno')
        mans.sort(key=lambda x: x['casting.id'])
        for man in mans:
            cid = man['casting.id']
            aliases = pif.dbh.fetch_aliases(cid, 'mack')
            mack_nums = single.get_mack_numbers(pif, cid, man['base_id.model_type'], aliases)
            if not mack_nums:
                print(cid)


def check_mack_ranges(pif):
    letters = list('abcdefghijklmnopqrstuvwyz') + ['aa']
    ranks = {}
    amods = mack_models(pif, 1, config.MAX_MACK_NUMBER, ['SF'])
    ranges = format_mack_html(pif, amods)
    num = 0
    for ran in ranges:
        for mod in ran['entry']:
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
                print('| %3d : %s-%s%-3s' % (num, s1, s2, missing))
            else:
                print('| %3d : %s  %-3s' % (num, s1, missing))
        else:
            print('| %3d :       ' % num)


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
