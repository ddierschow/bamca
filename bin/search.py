#!/usr/local/bin/python

import basics
import config
import imglib
import mbdata
import mflags
import models
import render
import single
import useful
import varias


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
    sect = pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
    lran = render.Range()
    for mod in mods:
        for var in pif.dbh.fetch_variation_query_by_id(mod['id'], var_id):
            var['name'] = var['base_id.rawname'].replace(';', ' ')
            lran.entry.append(render.Entry(text=varias.add_model_var_table_pic_link(pif, var)))
    lsec = render.Section(section=sect, range=[lran], columns=4)
    return render.Matrix(columns=4, section=[lsec])


def create_lineup(pif, mods):
    flago = mflags.FlagList()
    sect = pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
    lran = render.Range()
    for mod in mods:
        mod = pif.dbh.modify_man_item(mod)
        lran.entry.append(render.Entry(text=models.add_model_table_pic_link(pif, mod, flago=flago)))
    lsec = render.Section(section=sect, range=[lran], columns=4)
    return render.Matrix(columns=4, section=[lsec])


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
        mods = [pif.dbh.modify_man_item(x) for x in mods if x['section.page_id'] in ('manls', 'manno') and
                int(x['base_id.first_year']) >= firstyear and int(x['base_id.first_year']) <= lastyear]
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

    return pif.render.format_template('simplematrix.html', llineup=llineup.prep())


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
    if dt:
        lsec = render.Section()
        lran = render.Range()
        pif.render.title = dt
        vars = pif.dbh.fetch_variations_by_date(dt)
        prefixes = imglib.get_tilley_file()
        last = None
        ver_count = 0
        for var in vars:
            mod_id = var['variation.mod_id']
            var_id = var['variation.var']
            ldir = 'man/' + mod_id.lower()
            vss = pif.dbh.fetch_variation_selects(mod_id=mod_id, var_id=var_id)
            vs = ', '.join(['-'.join([y[x] for x in ['ref_id', 'sec_id', 'ran_id']]) for y in vss])
            categories = [x['variation_select.category'] for x in vss if x['variation_select.category']]
            verified = ['1'] if var['variation.flags'] & config.FLAG_MODEL_VARIATION_VERIFIED else []
            id_mismatch = ['1'] if var['variation.flags'] & config.FLAG_MODEL_ID_INCORRECT else []
            ver_count += 1 if verified else 0
            aliases = [x['alias.id'] for x in pif.dbh.fetch_aliases(
                mod_id, 'mack') if x['alias.flags'] & config.FLAG_ALIAS_PRIMARY]
            mack_id = aliases[0] if aliases else mod_id
            macks = get_mack_numbers(pif, mack_id)
            var['sort'] = macks[0] if macks else mod_id
            mvid = "%s-%s" % (mod_id, var_id)

            done = all([var['variation.text_' + x] != '' for x in ['description'] + descs])  # ignore text_with for now
            done = ' <i class="fas fa-star %s"></i>\n' % ('green' if done else 'red')
            cats = '(%s/%s)' % (var['variation.category'], ' '.join(categories))
            desc = ''.join(['<li>' + x + ': ' + var['variation.text_' + x] for x in descs])
            if var['variation.text_with']:
                desc += '<li>with: ' + var['variation.text_with']
            var['shown'] = ''
            vt = '2' if var['variation.category'] in single.code2cats else '1' if categories else '0'
            var['class_name'] = 'ln' + vt
            if last != mod_id:
                var['shown'] += (
                    pif.render.format_link(f'/cgi-bin/single.cgi?id={mod_id}', f'<b>{mack_id} ({mod_id}) ') +
                    pif.render.format_link(
                        f'/cgi-bin/vars.cgi?edt=1&mod={mod_id}',
                        '%s</b>' % var['base_id.rawname'].replace(';', ' ')) + (
                        '' if ''.join(pif.render.find_image_file(
                            mod_id.lower(), prefix='s_', pdir='.' + config.IMG_DIR_MAN))
                        else ' <i class="fas fa-star red"></i> ') +
                    pif.render.format_link(
                        f'/cgi-bin/pics.cgi?m={mod_id}&t=1', ' - DT<br>')
                )
                last = mod_id
            prefix = f"&has={prefixes[mod_id.lower()][0]}" if mod_id.lower() in prefixes else ""
            var['shown'] += pif.render.format_link(
                f'traverse.cgi?g=1&d=lib/{ldir}&man={mod_id}&var={var_id}&suff={prefix}&lty=mss',
                # &mr=1&credit=DT&til=1',
                pif.render.format_image_required(
                    mod_id, vars=[var['variation.picture_id'] or 'unmatchable', var_id],
                    also={'class': 'righty'}, nobase=True, largest='s'))
            var['shown'] += (
                pif.form.put_hidden_input(**{'v.' + mvid: '1'}) +
                pif.form.put_checkbox('c.' + mvid, [('1', '',)], checked=verified, sep='\n') +
                pif.form.put_checkbox('i.' + mvid, [('1', '',)], checked=id_mismatch, sep='\n') +
                pif.render.format_link(
                    '/cgi-bin/vars.cgi?mod=%s&var=%s&edt=1' % (mod_id, var_id),
                    '(%s) %s' % (var_id, var['variation.text_description'])) + done +
                '<i>' + var['variation.note'] + '</i> ' + '-' + vs + '-&nbsp;' +
                pif.form.put_text_input('s.' + mvid, 12, showlength=10, value=var['variation.imported_from']) + '\n' +
                cats + '\n<ul>' + desc +
                '</ul>\n'
            )
        vars.sort(key=lambda x: x['sort'])
        lran.entry = [render.Entry(text=x['shown'], class_name=x['class_name']) for x in vars]
        lsec.columns = 1
        llineup.header += (
            'Verified: %d of %d<br><form action="/cgi-bin/mass.cgi?tymass=dates" method="post">' %
            (ver_count, len(vars)))
        llineup.footer += pif.form.put_button_input() + '</form>'
        lsec.range = [lran]
        llineup.section = [lsec]
    else:
        pif.render.title = 'Search Dates'
        date_d = {}
        first_year = last_year = 1984
        for dt in pif.dbh.fetch_variation_dates(yr=yr):
            if dt['date']:
                y = first_year - 1 if dt['date'] < str(first_year) else int(dt['date'][:4])
                date_d.setdefault(y, [])
                date_d[y].append((dt['date'], dt['count(*)']))
                last_year = y if y > last_year else last_year

        lsec = render.Section()
        for year in range(first_year - 1, last_year + 1):
            lran = render.Range()
            lran.entry = [render.Entry(
                text=pif.render.format_link(f'/cgi-bin/msearch.cgi?date=1&dt={d}',
                                            f'{d} ({c})')) for d, c in date_d[year]]
            lsec.range.append(lran)
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
    return pif.render.format_template('simplematrix.html', llineup=llineup.prep())
