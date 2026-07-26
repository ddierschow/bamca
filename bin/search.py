#!/usr/local/bin/python

import glob

import basics
import config
import cvfind
import imglib
import mbdata
import mbmods
import mflags
import render
import useful


def search_name(pif):
    return pif.dbh.fetch_casting_list(
        where=[f"base_id.rawname like '%{x}%'" for x in pif.form.search('query')], verbose=True)


# specific id request goes through here
# would like to accept K43a like things
def search_id(pif):
    cid = get_casting_id(pif.form.get_str('id'))
    mod = pif.dbh.fetch_casting(cid)
    var_id = pif.form.get_str('var')
    if mod:
        mod = pif.dbh.make_man_item(mod)
        if var_id:
            raise useful.Redirect(f'/cgi-bin/vars.cgi?mod={mod.id}&var={var_id}')
        else:
            raise useful.Redirect(f'/cgi-bin/single.cgi?id={mod.id}')

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
        mod = [x for x in mod1 + mod2 if x.get('section.page_id', 'manno') in ['manls', 'manno']]
    return mod


def get_casting_id(id):
    if not id:
        return ''
    ok = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-/'
    id = ''.join([x for x in list(id) if x in ok])
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
    sect = pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
    lran = render.Range()
    for mod in mods:
        manitem = pif.dbh.make_man_item(mod)
        for var in pif.dbh.fetch_variation_query_by_id(manitem.id, var_id):
            var['name'] = var['base_id.rawname'].replace(';', ' ')
            lran.entry.append(render.Entry(text=mbmods.add_model_var_table_pic_link(pif, var)))
    lsec = render.Section(section=sect, range=[lran], columns=4)
    return render.Matrix(columns=4, section=[lsec])


def create_lineup(pif, mods):
    flago = mflags.FlagList()
    sect = pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
    lran = render.Range()
    for mod in mods:
        manitem = pif.dbh.make_man_item(mod)
        lran.entry.append(render.Entry(text=mbmods.add_man_item_table_pic_link(pif, manitem, flago=flago)))
    lsec = render.Section(section=sect, range=[lran], columns=4)
    return render.Matrix(columns=4, section=[lsec])


@basics.web_page
def run_search(pif):
    # form['var'] is now a possibility
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append(pif.request_uri, 'Model Search')
    mods = None
    pif.ren.print_html()
    if pif.form.has('arg'):
        return bamca_id_search(pif, pif.form.get_id('arg').replace('/', '-'))
    if pif.form.has('bid'):
        return bamca_id_search(pif, pif.form.get_id('bid'))
    if pif.form.has('date'):
        return date_search(pif, pif.form.get_str('dt'), pif.form.get_str('yr'))
    if pif.form.has('query'):
        targ = pif.form.get_str('query')
        firstyear = pif.form.get_int('syear', 1)
        lastyear = pif.form.get_int('eyear', 9999)
        pif.ren.title = 'Models matching name: ' + targ
        mods = [x for x in search_name(pif) if x['section.page_id'] in ('manls', 'manno') and
                int(x['base_id.first_year']) >= firstyear and int(x['base_id.first_year']) <= lastyear]
    elif pif.form.has('id'):
        targ = pif.form.get_str('id')
        mods = search_id(pif)
        if mods is None:
            raise useful.SimpleError("Your query parameters do not make sense.  Please try something different.", status=404)
        pif.ren.title = 'Models matching ID: ' + targ
    else:
        raise useful.SimpleError("Your query parameters do not make sense.  Please try something different.", status=404)
    if not mods:
        raise useful.SimpleError("Your query did not produce any models.  Sorry 'bout that.", status=404)

    mods.sort(key=lambda x: x.get('base_id.rawname', ''))
    var_id = pif.form.get_str('var')
    pif.ren.set_button_comment(pif, keys={'query': 'query'})
    if var_id:
        llineup = create_var_lineup(pif, mods, var_id)
    else:
        llineup = create_lineup(pif, mods)

    return pif.ren.format_template('simplematrix.html', llineup=llineup.prep())


def get_mack_numbers(pif, mod_id):
    def fmt_mack_id(m):
        ostr = ''
        if m[0]:
            ostr += '%s-' % m[0]
        if m[2]:
            ostr += '%03d-%2s' % m[1:]
        else:
            ostr += '%03d' % m[1]
        return ostr

    ret = []
    mack = mbdata.get_mack_number(mod_id)
    if mack[0] is not None and mod_id.startswith('RW') or mod_id in (
            'MI740', 'MI816', 'MI861') or (mack and mack[0] and mack[2]):
        ret.append(fmt_mack_id(mack))
    return ret


descs = ['body', 'base', 'interior', 'windows', 'wheels']


def date_search(pif, dt=None, yr=None):
    llineup = render.Matrix(columns=4)
    if dt:  # specific month page
        mbusa = {(x['mbusa.mod_id'], x['mbusa.var_id']): x for x in pif.dbh.fetch_mbusa_entries(date=dt)}
        lsec = render.Section()
        lran = render.Range()
        pif.ren.title = dt
        vars = pif.dbh.fetch_variations_by_date(dt, imported_from=dt if '-' in dt else None)
        prefixes = imglib.get_tilley_file(pif)
        last = None
        ver_count = ver_poss = 0
        for var in vars:
            mod_id = var['variation.mod_id']
            var_id = var['variation.var']
            mbusa_ent = mbusa.get((mod_id, var_id), {})
            ldir = 'man/' + mod_id.lower()
            vss = pif.dbh.fetch_variation_selects(mod_id=mod_id, var_id=var_id)
            vs = ', '.join(['-'.join([y[x] for x in ['ref_id', 'sec_id', 'ran_id']]) for y in vss])
            categories = [x['category'] for x in vss if x['category']]
            verified = ['1'] if var['variation.flags'] & config.FLAG_MODEL_VARIATION_VERIFIED else []
            id_mismatch = ['1'] if var['variation.flags'] & config.FLAG_MODEL_ID_INCORRECT else []
            if not var_id.startswith('f') and var['variation.manufacture'] not in mbdata.other_plants:
                ver_poss += 1
                ver_count += 1 if verified else 0
            aliases = [x['alias.id'] for x in pif.dbh.fetch_aliases(
                mod_id, 'mack') if x['alias.flags'] & config.FLAG_ALIAS_PRIMARY]
            mack_id = aliases[0] if aliases else mod_id
            macks = get_mack_numbers(pif, mack_id)
            var['sort'] = macks[0] if macks else mod_id
            mvid = "%s-%s" % (mod_id, var_id)

            done = all([var['variation.text_' + x] != '' for x in ['description'] + descs])  # ignore text_with for now
            done = pif.ren.fmt_star('green' if done else 'red')
            cats = '(%s/%s)' % (var['variation.category'], ' '.join(categories))

            def desct(x):
                if x == 'base':
                    return var['variation.text_base'] + ', ' + var['variation.text_text']
                return var['variation.text_' + x]

            desc = ''.join([f"<li>{x}: {desct(x)}" for x in descs])
            if var['variation.text_with']:
                desc += '<li>with: ' + var['variation.text_with']
            var['shown'] = ''
            vt = '2' if var['variation.category'] in mbdata.code2_cats else '1' if categories else '0'
            var['class_name'] = f'ln{vt} {"yay" if verified else "meh" if not mbusa_ent else "noo"}'
            if last != mod_id:
                var['shown'] += (
                    pif.ren.format_link(f'/cgi-bin/single.cgi?id={mod_id}', f'<b>{mack_id} ({mod_id}) ') +
                    pif.ren.format_link(
                        f'/cgi-bin/vars.cgi?edt=1&mod={mod_id}', var['base_id.rawname'].replace(';', ' ')) + '</b>' + (
                        '' if ''.join(pif.ren.find_image_file(
                            mod_id.lower(), prefix='s_', pdir='.' + config.IMG_DIR_MAN)) else pif.ren.fmt_star('red')) +
                    pif.ren.format_link(
                        f'/cgi-bin/pics.cgi?m={mod_id}&t=1', ' - DT<br>')
                )
                last = mod_id
            prefix = f"&has={prefixes[mod_id.lower()][0]}" if mod_id.lower() in prefixes else ""
            var['shown'] += (
                pif.ren.format_link(
                    f'traverse.cgi?g=1&d=lib/{ldir}&man={mod_id}&var={var_id}&suff={prefix}&lty=mss&r=1',
                    # &mr=1&credit=DT&til=1',
                    pif.ren.format_image_required(
                        mod_id, vars=[var['variation.picture_id'] or 'unmatchable', var_id],
                        also={'class': 'righty'}, nobase=True, largest='s')) +
                pif.form.put_hidden_input(**{'v.' + mvid: '1'}) +
                pif.form.put_checkbox('c.' + mvid, [('1', '',)], checked=verified, sep='\n') +
                pif.form.put_checkbox('i.' + mvid, [('1', '',)], checked=id_mismatch, sep='\n') +
                pif.ren.format_link(
                    '/cgi-bin/vars.cgi?mod=%s&var=%s&edt=1' % (mod_id, var_id),
                    '(%s) %s' % (var_id, var['variation.text_description'])) + done +
                '<i>' + var['variation.note'] + '</i> ' + '-' + vs + '-&nbsp;' +
                pif.form.put_text_input(
                    's.' + mvid, 12, showlength=10, value=(
                        mbusa_ent['mbusa.file'] if mbusa_ent else '') or var['variation.imported_from']) + '\n' + (
                    'file mismatch\n' if (
                        mbusa_ent and mbusa_ent['mbusa.file'] and var['variation.imported_from'] != 'mbusa' and
                        mbusa_ent['mbusa.file'] != var['variation.imported_from']) else '') +
                cats + ' ' + (pif.ren.fmt_check('green') if (mod_id, var_id) in mbusa else '') +
                '\n<ul>' + desc + '</ul>\n' + ((
                    pif.ren.format_link(pif.dbh.get_editor_link('mbusa', id=mbusa_ent['mbusa.id']),
                                        pif.ren.fmt_mini(color='green', icon="caret-right", family="solid")) +
                    ' ' + mbusa_ent['mbusa.variation'] + ' ' + mbusa_ent['mbusa.description']) if mbusa_ent else '') + '\n'
            )
        vars.sort(key=lambda x: x['sort'])
        lran.entry = [render.Entry(text=x['shown'], class_name=x['class_name']) for x in vars]
        lsec.columns = 1
        mbusa_files = sorted(glob.glob(f'lib/docs/mbusa/{dt}-*.png'))
        llineup.header += (
            f'Verified: {ver_count} of {ver_poss} -\n' + f'{len(mbusa)} in magazine -\n' +
            pif.ren.format_link(f'/cgi-bin/mass.cgi?tymass=var&mbusa=MBUSA&date={dt}', 'MBUSA') + '\n' +
            '\n'.join([pif.ren.format_link(f'/{x}', x[x.rfind('/') + 1:x.rfind('.')]) for x in mbusa_files]) + '\n' +
            '<form action="/cgi-bin/mass.cgi?tymass=dates" method="post">')
        llineup.footer += pif.form.put_button_input() + '</form>'
        lsec.range = [lran]
        llineup.section = [lsec]
    else:  # list of months page
        pif.ren.title = 'Search Dates'
        date_d = {}
        first_year = last_year = 1984
        for dt in pif.dbh.fetch_variation_dates(yr=yr):
            y = first_year - 1 if dt['date'] < str(first_year) else int(dt['date'][:4])
            date_d.setdefault(y, [])
            date_d[y].append((dt['date'], dt['count(*)']))
            last_year = max(y, last_year)

        for dt in pif.dbh.fetch_mbusa_dates(yr=yr):
            y = first_year - 1 if dt['date'] < str(first_year) else int(dt['date'][:4])
            date_d.setdefault(y, [])
            for x in date_d[y]:
                if x[0] == dt['date']:
                    break
            else:
                date_d[y].append((dt['date'], 0))
            last_year = max(y, last_year)

        def fmt_datelink(year, month):
            ym = f'{year}-{month:02}' if month else f'{year}'
            for d, c in date_d[year]:
                if d == ym:
                    return pif.ren.format_link(f'/cgi-bin/msearch.cgi?date=1&dt={d}', f'{d} ({c})' if c else f'{d}')
            return '' if month else ym

        lsec = render.Section(range=[render.Range(
            entry=[render.Entry(
                class_name='ln0',
                text=pif.ren.format_link(f'/cgi-bin/msearch.cgi?date=1&dt={d}',
                                         f'{d or "unset"} ({c})')) for d, c in date_d[first_year - 1]])
        ])
        classbool = True

        for year in range(first_year, last_year + 1):
            lran = render.Range(
                class_name='ln' + str(int(classbool)),
                entry=[render.Entry(text=fmt_datelink(year, x)) for x in range(13)])
            lran.entry.insert(7, render.Entry())
            lsec.range.append(lran)
            classbool = not classbool

        lsec.columns = 7
        llineup.section.append(lsec)
    llineup.footer += '<hr>'
    llineup.footer += (
        '<form action="/cgi-bin/msearch.cgi">Year = /<input type="hidden" name="date" value="1">'
        '<input type="text" name="yr"> <input type="submit" name="submit" value="GO" class="textbutton"></form>\n')
    llineup.footer += (
        '<form action="/cgi-bin/msearch.cgi">Mod ID: <input type="text" name="id" size="12"> '
        'Var ID: <input type="text" name="var" size="12"> '
        '<input type="submit" name="submit" value="GO" class="textbutton"></form>\n')
    return pif.ren.format_template('simplematrix.html', llineup=llineup.prep())


@basics.web_page
def run_super_search(pif):
    pif.ren.title = 'Super Search'
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append('/search.php', 'Search')
    pif.ren.print_html()
    # useful.write_message(pif.form)

    searcher = cvfind.Searcher(pif.form, withaliases=True)
    sections = searcher.run_query(pif)

    llineup = render.Matrix(columns=searcher.columns, tail=['', '', ''])
    pif.ren.set_button_comment(pif, keys={'sel': 'selection', 'ran': 'range', 'start': 'start', 'end': 'end'})
    lsec = render.Section(columns=searcher.columns)
    for sect in sections:
        mods = sect['models'] if not any(searcher.varsq.values()) else [x for x in sect['models'] if x.variations]
        if mods:
            if searcher.list_type == 'v':
                entries = [render.Entry(text=mbmods.add_man_item_sized_var_table_pic_link(pif, searcher.pic_type, y, x))
                           for y in mods for x in y.variations]
            else:
                entries = [render.Entry(text=mbmods.add_man_item_sized_table_pic_link(pif, searcher.pic_type, x))
                           for x in mods]

            lsec.range.append(render.Range(name=sect['name'], anchor=sect['id'], entry=entries))
    llineup.section = [lsec]
    if searcher.more or searcher.start:
        qf = searcher.make_search_criteria(pif)
        if searcher.start > 0:
            llineup.tail[1] += pif.ren.format_button_link(
                "previous", 'search.cgi?%s&start=%d' % (qf, max(searcher.start - mbdata.modsperpage, 0))) + ' '
        if searcher.more:
            llineup.tail[1] += pif.ren.format_button_link(
                "next", 'search.cgi?%s&start=%d' % (qf, searcher.start + mbdata.modsperpage))
    llineup.tail[2] = (
        f'{searcher.cascount} casting{useful.plural(searcher.cascount)} found.' if searcher.list_type == 'c' else
        f'{searcher.varcount} variation{useful.plural(searcher.varcount)} in '
        f'{searcher.cascount} casting{useful.plural(searcher.cascount)} found.')

    return pif.ren.format_template('simplematrix.html', llineup=llineup.prep())


def bamca_id_search(pif, bid):
    bid, var = bid.split('-', 1) if '-' in bid else (bid, '')
    base_id = pif.dbh.fetch_base_id(bid)
    if base_id:  # eventually these will all become just this easy
        match base_id['model_type']:
            case 'AC' | 'BR' | 'CH' | 'ET' | 'KS' | 'RW' | 'SB' | 'SF' | 'YY':
                if var:
                    raise useful.Redirect(f'/cgi-bin/vars.cgi?mod={bid}&var={var}')
                raise useful.Redirect(f'/cgi-bin/single.cgi?id={bid}')
            case 'PS':
                raise useful.Redirect(f'/cgi-bin/playset.cgi?id={bid}')
            case 'CC':
                pass  # not sure what to do with these
            case 'AD' | 'BK' | 'DC' | 'GM' | 'PC' | 'PD' | 'PK' | 'PZ' | 'RY':
                raise useful.Redirect(f'/cgi-bin/pub.cgi?id={bid}')
            case 'MP':
                raise useful.Redirect(f'/cgi-bin/packs.cgi?page=&id={bid}')
            case 'SE':
                mm = pif.dbh.depref('matrix_model', pif.dbh.fetch_matrix_model_by_base_id(bid))
                raise useful.Redirect(f'/cgi-bin/matrix.cgi?page={mm["page_id"]}#{mm["section_id"]}')
            case 'LI':
                lm = pif.dbh.depref('lineup_model', pif.dbh.fetch_lineup_model({'base_id': bid}))
                lm = lm[0]
                region = lm['region'] if lm['region'] != 'W' or not lm['region'].startswith('X') else 'U'
                num = f"{lm['region'].replace('.', '')}.{lm['number']}"
                raise useful.Redirect(f'/cgi-bin/lineup.cgi?year={lm["year"]}&region={region}#{num}')

    # oh.  hrm.  maybe base_id hasn't been populated yet.
    mm = pif.dbh.depref('matrix_model', pif.dbh.fetch_matrix_model_by_base_id(bid))
    if mm:
        raise useful.Redirect(f'/cgi-bin/matrix.cgi?page={mm["page_id"]}#{mm["section_id"]}')

    lm = pif.dbh.depref('lineup_model', pif.dbh.fetch_lineup_model({'base_id': bid}))
    if lm:
        lm = lm[0]
        region = lm['region'] if (lm['region'] != 'W' or not lm['region'].startswith('X')) else 'U'
        num = f"{lm['region'].replace('.', '')}.{lm['number']}"
        raise useful.Redirect(f'/cgi-bin/lineup.cgi?year={lm["year"]}&region={region}#{num}')

    raise useful.SimpleError("Your query did not produce any models.  Sorry 'bout that.", status=404)
