#!/usr/local/bin/python

import csv
from io import open
import json
import os
import re
import sys

import basics
import config
import imglib
import mbdata
import mbmods
import render
import useful


# 1953-1969  pic/prod/lrw
# 1970-1982  pic/prod/lsf
# 1983-1992  pic/prod/univ
# 1993-1997  pic/prod/tyco
# 1998-2004  pic/prod/mtlaurel
# 2005-2015  pic/prod/elseg
# 2016-      pic/prod/mworld

# A 1981 1987 1991-1993 1997 2000-2001
# B 2000-2001
# D 1999-2001
# J 1977-1992
# L 2008-2011
# R 1982-2018
# U 1982-2018
# W 1953-1981

# X.01 | Packaging                              | pub      |
# X.02 | Catalogs                               | pub      |
# X.03 | Advertisements                         | pub      |
# X.11 | Series                                 | series   |
# X.14 | Collectors                             | series   |
# X.15 | Moving Parts                           | series   |
# X.17 | Promotional                            | promo    |
# X.19 | Convoy                                 | series   |
# X.21 | Early Lesney Toys                      | ks       |
# X.22 | Major Packs                            | ks       |
# X.23 | King Size                              | ks       |
# X.24 | Real Working Rigs                      | ks       |
# X.25 | Super Rigs                             | ks       |
# X.31 | Models of Yesteryear                   | yy       |
# X.32 | Dinky                                  | yy       |
# X.41 | Accessory Packs                        | acc      |
# X.42 | Skybusters                             | sb       |
# X.51 | Buildings                              | bld      |
# X.52 | Playsets                               | bld      |
# X.60 | Presentation Sets                      | pack     |
# X.61 | Gift Sets / Battle Kings               | pack     |
# X.62 | 2-Packs / Hitch n Haul                 | pack     |
# X.63 | 3-Packs                                | pack     |
# X.65 | 5-Packs                                | pack     |
# X.66 | Licensed 5-Packs                       | pack     |
# X.67 | Themed 5-Packs / Action Launchers      | pack     |
# X.68 | Larger Packs                           | pack     |
# X.71 | Roadways                               | pub      |
# X.72 | Games and Puzzles                      | pub      |
# X.73 | Books                                  | pub      |

# Australia also had the MB76-79 in 1981.
# The Australian amalgamated range of the mid-1980s (where they mixed the ROW and USA ranges for their 1-75),
# and the 1997 Aussie exclusive 1-75 models? They often get forgotten.

# Germany had a few exclusive 1-75 versions for their market in 1977.


def calc_lineup_model(pif, lsec, year, region, mdict):
    id_re = re.compile(r'(?P<a>[a-zA-Z]+)(?P<n>\d+)')
    mdict.update({
        'image_format': lsec.get('link_format', ''),
        'anchor': '{}{}'.format('X' if region.startswith('X') else '', mdict['number']),
        'class_name': '', 'product': '', 'prod_id': '', 'href': '',
        'is_reused_product_picture': 0, 'is_product_picture': 0, 'halfstar': 0,
        'displayed_id': '',  # '&nbsp;'
    })
    if not mdict.get('pdir'):
        pdir = lsec.get('pic_dir')
        mdict['pdir'] = pdir = pdir if pdir else pif.ren.pic_dir
    mdict['spdir'] = mbdata.dirs_r.get(mdict['pdir'], mdict['pdir'])

    if not (lsec['flags'] & config.FLAG_SECTION_NO_FIRSTS) and str(year) == mdict['base_id.first_year']:
        mdict['class_name'] = ('revcasting' if mdict['base_id.flags'] & config.FLAG_MODEL_CASTING_REVISED else
                               'newcasting')

    # useful.write_comment(mdict)

    if mdict['casting.id']:
        # modify this if rank_id exists
        mdict['prod_id'] = mdict['casting.id']
        if mdict['picture_id']:
            mdict['product'] = mdict['picture_id'].replace('w', pif.form.get_strl('region'))
            mdict['is_reused_product_picture'] = pif.is_allowed('a')
        elif mdict.get('image_format'):
            imgfmt = (mdict['image_format'].replace('w', pif.form.get_strl('region'))
                      if not region.startswith('X') and int(mdict['year']) > 1970 else mdict['image_format'])
            mdict['product'] = imgfmt % mdict['number']
        if pif.ren.find_image_path([mdict['product']], suffix='jpg', pdir=mdict['pdir'], largest='m'):
            mdict['is_product_picture'] = 1
        # seems to do the wrong thing with xsecs, see 2023 X.17 #11
        mdict['href'] = (
            "single.cgi?dir=%(spdir)s&pic=%(product)s&ref=%(ref_id)s&sec=%(sec_id)s&ran=%(ran_id)s&id=%(mod_id)s" %
            mdict)
        mdict['halfstar'] = int(bool(mdict.get('flags', 0) & config.FLAG_LINEUP_MODEL_MULTI_VARS))
    elif mdict['pack.id']:
        mdict['prod_id'] = mdict['pack.id']
        if mdict['picture_id']:
            mdict['product'] = mdict['picture_id']
            mdict['is_reused_product_picture'] = pif.is_allowed('a')
        elif mdict.get('image_format'):
            mdict['product'] = mdict['image_format'] % mdict['pack.id']
        if pif.ren.find_image_path([mdict['product']], pdir=mdict['pdir'], largest=mbdata.IMG_SIZ_GIGANTIC):
            mdict['is_product_picture'] = 1
        if mdict['pack.section_id'] == 'playset':
            mdict['href'] = "play.cgi?page=%(pack.page_id)s&id=%(pack.id)s" % mdict
        else:
            mdict['href'] = "packs.cgi?page=%(pack.page_id)s&id=%(pack.id)s" % mdict
    elif mdict['publication.id']:
        mdict['prod_id'] = mdict['publication.id']
        mdict['product'] = mdict['publication.id'] + '_01'
        if pif.ren.find_image_path([mdict['product']], pdir=mdict['pdir'], largest=mbdata.IMG_SIZ_GIGANTIC):
            mdict['is_product_picture'] = 1
        mdict['href'] = "pub.cgi?id=%(publication.id)s" % mdict
    elif mdict['page_info.id']:  # series
        mdict['prod_id'] = mdict['product'] = mdict['page_info.id']
        mdict['href'] = "matrix.cgi?page=" + mdict['mod_id'][7:]
        if mdict['picture_id']:
            mdict['href'] += "#" + mdict['picture_id']
            # mdict['product'] += "-" + mdict['picture_id']

    mdict['product'] = mdict['product'].replace('.', '_')
    mdict['large_img'] = pif.ren.format_image_required(
        mdict['product'], suffix='jpg', pdir=mdict['pdir'], largest='m', also={'class': 'largepic'})

    if lsec['flags'] & config.FLAG_SECTION_DEFAULT_IDS:
        mdict['shown_id'] = pif.dbh.default_id(mdict['mod_id'])
        disp_format = '%s'
    else:
        mdict['shown_id'] = '' if (mdict.get('flags', 0) & config.FLAG_MODEL_NO_ID) else mdict['number']
        disp_format = lsec.get('disp_format', '%s')
    if 'ID' in disp_format:
        id_m = id_re.match(mdict['prod_id'])
        if id_m:
            mdict['displayed_id'] = disp_format.replace('ID', '%s-%d' % (id_m.group('a'), int(id_m.group('n'))))
    elif disp_format and mdict.get('shown_id'):
        mdict['displayed_id'] = disp_format % (mdict['shown_id'])
    mdict['upload_link'] = pif.ren.format_link('upload.cgi?d=%s&n=%s' % (mdict['pdir'].replace('pic', 'lib'),
                                                                         mdict['product']), mdict['large_img'])
    return mdict


def create_lineup(pif, mods, year, lsec, fdebug=False):
    # useful.write_comment('CLS', year, lsec)
    region = lsec['id']
    vssec = region.replace('.', '')
    is_extra = region.startswith('X')
    regions = [vssec] if is_extra else mbdata.get_region_tree(region) + ['']
    if is_extra:
        mods = [x for x in mods
                if x['lineup_model.region'] == region and (not x['vs.ref_id'] or x['vs.sec_id'] == vssec)]
    else:
        mods = [x for x in mods if not x['lineup_model.region'].startswith('x')]

    # 1. lay down model list from current region only.
    mods.sort(key=lambda x: (x['lineup_model.number'], x['lineup_model.display_order'],))
    ref_id = 'year.%s' % year

    modlist = []
    foundlist = []
    for mod in mods:
        if (mod['lineup_model.number'], mod['lineup_model.display_order'],) not in foundlist:
            if ((not mod['vs.ran_id'] or not mod['vs.ran_id'].isdigit() or
                    int(mod['vs.ran_id']) == mod['lineup_model.number']) and
                    ((is_extra and region == mod['lineup_model.region'] and
                      mod['vs.sec_id'] == vssec or not mod['vs.sec_id']) or
                     not is_extra)):
                pass  # we're good, now add it below
            elif mod['lineup_model.flags'] & config.FLAG_MODEL_NOT_MADE:
                # see 2019:3 vs :99.  if #3 has vs and #99 doesn't, that ^ can't show #99.
                mod = {k: v for k, v in mod.items() if not (k.startswith('v.') or k.startswith('vs.'))}
            else:
                continue
            lm = pif.dbh.make_lineup_item(mod)
            # useful.write_comment('CL', lsec, year, region, lm)
            modlist.append(calc_lineup_model(pif, lsec, year, region, lm))
            foundlist.append((mod['lineup_model.number'], mod['lineup_model.display_order'],))

    # 2. edit model list for only entries we're interested in
    mods = [mod for mod in mods if mod['vs.sec_id'] is None or (
        (not mod['vs.ran_id'].isdigit() or int(mod['vs.ran_id']) == mod['lineup_model.number']) and
        (mod['vs.ran_id'].isdigit() or mod['vs.sec_id'] in regions))
    ]

    # 3. put it in a usable order
    def mod_sort_key(x):
        return (x['lineup_model.number'], x['lineup_model.display_order'],
                0 if (is_extra or x['vs.sec_id'] is None or x['vs.sec_id'].isdigit()) else
                regions.index(x['vs.sec_id']),)

    mods.sort(key=mod_sort_key)

    # 4. traverse region tree to figure out variation(s)
    for curmod in modlist:
        set_vars(mods, curmod, regions, ref_id, fdebug)

    # 5. declare victory and grab a beer
    return modlist


def set_vars(rmods, curmod, regions, ref_id, fdebug=False):
    '''Given a model and a lineup, try to figure out where to
    insert that model into the lineup.  This is not easy.'''
    if fdebug:
        print('--------------------------------------------------------')
        print('SETVAR', regions, ref_id)
        print('CURMOD:', useful.defang(curmod))
        for rmod in rmods:
            if (rmod['lineup_model.number'] == curmod['number'] and
                    rmod['lineup_model.display_order'] == curmod['display_order']):
                print('RMOD:', rmod['lineup_model.number'], 'ord', rmod['lineup_model.display_order'],
                      'vs.ref_id', rmod['vs.ref_id'], 'vs.sec_id', rmod['vs.sec_id'], 'var', rmod['v.var'],
                      rmod['v.text_description'], 'pic', rmod['v.picture_id'])

    quittable = False
    for region in regions:
        if fdebug:
            print('CHECK', region)
        for rmod in rmods:
            if ((region.startswith('X') and not rmod['vs.sec_id']) or
                    (rmod['lineup_model.number'] == curmod['number'] and
                     rmod['lineup_model.display_order'] == curmod['display_order'] and
                     rmod['vs.sec_id'] == region)):
                # add to cvarlist
                for var in curmod['cvarlist']:
                    if rmod['v.var'] in var['var_ids']:
                        if fdebug:
                            print('NO UPDATE')
                        break  # "I seen the airport." -- Stephens
                    elif rmod['v.text_description'] == var['desc']:
                        if fdebug:
                            print('UPDATE', rmod['v.var'], rmod['v.text_description'])
                        var['var_ids'].append(rmod['v.var'])
                        pic_id = rmod['v.picture_id'] if rmod['v.picture_id'] else rmod['v.var']
                        if pic_id not in var['picture_ids']:
                            var['picture_ids'].append(pic_id)
                        var['vars'] = ','.join(var['var_ids'])
                        break
                else:
                    pic_id = rmod['v.picture_id'] if rmod['v.picture_id'] else rmod['v.var']
                    curmod['cvarlist'].append({'var_ids': [rmod['v.var']], 'desc': rmod.get('v.text_description', ''),
                                               'picture_ids': [pic_id], 'vars': rmod['v.var']})
                    curmod['sec_id'] = rmod['vs.sec_id']
                    if fdebug:
                        print('ADD', rmod['v.var'], rmod['v.text_description'])

                    if rmod['vs.sec_id'] == region:
                        quittable = True
            elif fdebug:
                print('NO ADD')
        if quittable:
            break
    if fdebug:
        print('<br>')
    return curmod


def get_man_sections(pif, year, region, section_types):
    wheres = ["page_id='year.%s'" % year]
    if pif.ren.is_alpha or not pif.ren.is_beta:
        wheres.append("not flags & %d" % config.FLAG_SECTION_HIDDEN)
    secs = pif.dbh.fetch_sections(wheres)
    if not secs:
        raise useful.SimpleError(
            """I'm sorry, that lineup was not found.  Please use your "BACK" button or try something else.""")

    xsecs = [x for x in secs if x['id'].startswith('X') and x['category'] in section_types]
    secs = [x for x in secs if not x['id'].startswith('X')]

    for region in mbdata.get_region_tree(region):
        lsecs = [x for x in secs if x['id'].startswith(region)]
        if lsecs:
            break
    else:
        region = ''
        lsecs = [{}]
    return region, lsecs[0], lsecs[1:] if 'man' in section_types else [], xsecs


def create_lineup_sections(pif, year, region, section_types, fdebug=False):
    year = mbdata.correct_year(year)
    region = mbdata.correct_region(region, year)
    if not region:
        raise useful.SimpleError(
            """I'm sorry, that lineup was not found.  Please use your "BACK" button or try something else.""")

    region, mainsec, secs, xsecs = get_man_sections(pif, year, region, section_types)
    limits = pif.dbh.fetch_lineup_limits()

    # generate main section
    mainsec.update({
        'year': year,
        'region': region,
        'mods': [],
        'first_year': int(limits['min(year)']),
        'last_year': int(limits['max(year)']),
    })

    if 'man' in section_types:
        modlist = create_lineup(pif, pif.dbh.fetch_lineup_models(year, region), year, mainsec, fdebug)

        # carve up modlist by section
        if secs:
            endv = modlist[-1]['number']
            for sec in reversed(secs):
                sec.update({
                    'id': region + '_' + str(sec['display_order']),
                    'graphics': pif.ren.fmt_opt_img([
                        (sec['img_format'][:4] + region + 's%02d' % sec['display_order']).lower()]),
                    'end': endv,
                    'mods': [x for x in modlist if x['number'] > sec['start'] and x['number'] <= endv],
                })
                endv = sec['start']
        else:
            mainsec.update({
                'id': region + '_1',
                'graphics': pif.ren.fmt_opt_img([mainsec['img_format'][:4] + region + 's']),
                'mods': modlist
            })

    # generate extra sections
    lmods = pif.dbh.fetch_lineup_models(year, [x['id'] for x in xsecs])
    for sec in xsecs:
        # lmods = pif.dbh.fetch_lineup_models(year, sec['id'])
        sec['mods'] = create_lineup(pif, lmods, year, sec, fdebug)

    return mainsec, secs, xsecs


def render_lineup_model(pif, mdict, comments, unroll=False, large=False):
    ostr = ''
    if mdict['is_product_picture']:
        comments.add('c')
    if large:
        ostr += '<table><tr><td width=400>%s</td><td><center>' % mdict['upload_link']
    if unroll and mdict.get('casting.id') and mdict['cvarlist']:
        for cvar in mdict['cvarlist']:
            ostr += render_lineup_model_var(pif, mdict, comments, show_var=cvar['var_ids'][0])
    else:
        ostr += render_lineup_model_var(pif, mdict, comments)
    style_id = mdict.get('style_id')
    class_name = mdict.get('class_name' '') + (' bg_' + style_id if style_id else '')
    if large:
        # ostr += '<br>' + pif.ren.format_button_link("edit", pif.dbh.get_editor_link(
        #     'lineup_model', {'id': mdict['lineup_model.id']}))
        ostr += '<br>'.join([
            'name' + pif.form.put_text_input('description.%s' % mdict['id'], 64, value=mdict['name']),
            'style' + pif.form.put_text_input('style_id.%s' % mdict['id'], 4, value=mdict['style_id']),
            pif.form.put_checkbox('halfstar.%s' % mdict['id'], [(1, 'multi')], checked=[mdict.get('halfstar', 0)]),
            '</center></td></tr></table>'])
    return render.Entry(
        text=ostr,
        # display_id=mdict.get('style_id', 0),
        # style=mdict.get('style'),
        class_name=class_name,
        also=mdict.get('also'),
        data=mdict,
    )


def render_lineup_model_var(pif, mdict, comments, show_var=None):
    imglist = []
    varlist = []
    if mdict.get('flags', 0) & config.FLAG_MODEL_NOT_MADE:
        mdict['not_made'] = True
        imgname = mdict['mod_id'].replace('.', '_')
        imglist.append(imgname)
        comments.add('n')
    elif mdict.get('page_info.id'):
        imgname = mdict['mod_id'].replace('.', '_')
        imglist.append(imgname)
        if mdict['picture_id']:
            imgname += "-" + mdict['picture_id']
        imglist.insert(0, imgname)
    elif mdict.get('mod_id'):
        imgname = mdict['mod_id'].replace('.', '_')
        imglist.append(imgname)
        for var in mdict['cvarlist']:
            if not show_var or show_var in var['var_ids']:
                varlist.extend(var['picture_ids'])
    imgstr = pif.ren.format_image_required(imglist, prefix=mbdata.IMG_SIZ_SMALL, vars=[x for x in varlist if x],
                                           pdir=config.IMG_DIR_MAN)
    mdict['imgstr'] = imgstr
    mdict['descriptions'] = [x['desc'] for x in mdict['cvarlist'] if not show_var or show_var in x['var_ids']]
    mdict['no_specific_image'] = 0
    if mdict['casting.id'] and not mdict.get('not_made'):
        if imgstr.find('-') < 0:
            comments.add('i')
            mdict['no_specific_image'] = 1
        if len(varlist) < 1:  # pragma: no cover
            comments.add('v')
            mdict['no_variation'] = 1
        # also if there is no description string

    desclist = list()
    for var in mdict.get('descriptions', []):
        if var and var not in desclist:
            desclist.append(var)
    mdict['descriptions'] = desclist

    # mdict: imgstr name number pdir product vars
    ostr = mbmods.add_model_table_product_link(pif, mdict)
    return ostr


def render_lineup_year_sections(pif, mainsec, secs, xsecs, large=False, multi=False):
    lsec = render.Section(section=mainsec)
    unroll = pif.form.get_bool('unroll')
    year = mainsec['year']
    # region = mainsec['region']
    comments = set()
    lsec.range = []
    img = pif.ren.fmt_img(['%ss' % year])
    if img:
        lsec.name += '<br>' + img
    if large:
        lsec.columns = 1
    if secs:
        for sec in secs:
            # copy more stuff here
            lran = render.Range(entry=[
                render_lineup_model(pif, x, comments, unroll=unroll, large=large)
                for x in sec['mods'] if not multi or len(x['cvarlist']) > 1],
                name=sec['name'],
                id=sec['id'],
                note=sec['note'],
                graphics=pif.ren.fmt_opt_img([(sec['img_format'][:5] + 's%02d' % sec['display_order']).lower()]))
            lsec.range.append(lran)
    else:
        lsec.range = [render.Range(entry=[
            render_lineup_model(pif, x, comments, unroll=unroll, large=large)
            for x in mainsec['mods'] if not multi or len(x['cvarlist']) > 1],
            id=mainsec['id'],
            note=mainsec['note'])]
    sections = [lsec]
    for sec in xsecs:
        sections.append(render.Section(range=[render.Range(
            entry=[render_lineup_model(pif, x, comments, unroll=unroll, large=large) for x in sec['mods']],
            name='<i>' + sec['name'] + '</i>' if sec['flags'] & config.FLAG_SECTION_HIDDEN else sec['name'],
            id='X',
            note=sec['note'],
        )]))
    llineup = render.Matrix(id='year', section=sections)

    llineup.comments = comments
    llineup.tail = ['', '<br>'.join([mbdata.comment_designation[comment] for comment in comments])]
    if large:
        llineup.header = (
            '<form action="mass.cgi" method="post">\n<input type="hidden" name="tymass" value="lineup_desc">\n' +
            pif.create_token())
        llineup.footer = pif.form.put_button_input() + '</form>\n'
#    if pif.is_allowed('a'):  # pragma: no cover
#        llineup['tail'][1] += '<br>multivars %s %s ' % (year, region) + ' '.join(multivars) + '<br>'
    return llineup


def render_lineup_year(pif, mainsec, secs, xsecs, large=False):
    # unroll = pif.form.get_bool('unroll')
    footer = ''
    year = mainsec['year']
    # region = mainsec['region']
    llineup = render_lineup_year_sections(pif, mainsec, secs, xsecs, large=large, multi=pif.form.get_bool('multi'))
#    if year > mainsec['first_year']:
#       footer += pif.ren.format_button_link("previous_year", '?year=%s&region=%s' %
#                                          (year - 1, pif.form.get_stru('region')))
#    if year < mainsec['last_year']:
#       footer += pif.ren.format_button_link("following_year", '?year=%s&region=%s' %
#                                          (year + 1, pif.form.get_stru('region')))
    pif.ren.set_footer(footer)
    pif.ren.bamcamark = mbdata.bamcamark(year)
    return pif.ren.format_template('simplematrix.html', llineup=llineup.prep(),
                                   large=large, unroll=pif.form.get_bool('unroll'))


def render_lineup_text(pif, mainsec, secs, xsecs):
    output = []
    for sec in [mainsec] + secs + xsecs:
        output.append(sec['name'])
        for mod in sec.get('mods', []):
            for cvar in mod['cvarlist'] or [{'desc': ''}]:
                output.append('%4s %-8s  %-40s  %s' % (mod['displayed_id'], mod['mod_id'], mod['name'], cvar['desc']))
        output.append('')
    return '\n'.join(output) + '\n'


def render_lineup_checklist(pif, mainsec, secs, xsecs):
    entries = []
    for sec in [mainsec] + secs + xsecs:
        entries.append(dict(name=sec['name']))
        for mod in sec.get('mods', []):
            for cvar in mod['cvarlist'] or [{'desc': ''}]:
                entries.append(dict(number=mod['displayed_id'], mod_id=mod['mod_id'], name=mod['name'],
                                    desc=cvar['desc'], x=pif.ren.fmt_square(hollow=True)))

    cols = ['x', 'number', 'mod_id', 'name', 'desc']
    titles = ['', '#', 'Model ID', 'Name', 'Description']
    lsection = render.Section(
        colist=cols, headers=dict(zip(cols, titles)),
        range=[render.Range(entry=entries)])
    llistix = render.Listix(section=[lsection])
    return pif.ren.format_template('simplelistix.html', llineup=llistix)


def render_lineup_csv(pif, mainsec, secs, xsecs):
    out_file = sys.stdout
    field_names = ["Number", "Model ID", "Name", "Description"]
    writer = csv.DictWriter(out_file, fieldnames=field_names)
    writer.writeheader()
    for sec in [mainsec] + secs + xsecs:
        writer.writerow(dict(zip(field_names, ['section', sec['name'], '', ''])))
        for mod in sec.get('mods', []):
            for cvar in mod['cvarlist'] or [{'desc': ''}]:
                writer.writerow(dict(zip(field_names, [mod['number'], mod['mod_id'], mod['name'], cvar['desc']])))
    return ''


def render_lineup_json(pif, mainsec, secs, xsecs):
    sec_keys = ['year', 'id', 'category', 'name', 'note', 'range']
    ran_keys = ['id', 'category', 'name', 'note']
    mod_keys = ['displayed_id', 'made', 'mod_id', 'name']
    var_keys = ['desc', 'vars']

    mainsec['range'] = []
    if secs:
        mainsec['range'] = secs
    mainsec['range'] += xsecs
    sec = {x: mainsec[x] for x in sec_keys}
    sec['range'] = []
    for mran in mainsec['range']:
        ran = {x: mran[x] for x in ran_keys}
        ran['model'] = []
        for mmod in mran['mods']:
            mod = {x: mmod[x] for x in mod_keys}
            if mmod['cvarlist']:
                for mvar in mmod['cvarlist']:
                    mod['var'] = {x: mvar[x] for x in var_keys}
            ran['model'].append(mod)
        sec['range'].append(ran)
    llineup = {'section': [sec]}
    return json.dumps(llineup)


def year_lineup_main(pif, listtype):
    region = pif.form.get_stru('region')
    year = pif.form.get_str('year')
    section_types = pif.form.get_list('lty')

    if not section_types or section_types == ['all']:
        section_types = dict(mbdata.lineup_types).keys()

    pif.ren.hierarchy_append(
        '/cgi-bin/lineup.cgi?year=%s&region=%s&lty=all' % (year, region),
        str(year) + ' ' + mbdata.regions.get(region, ''))
    pif.ren.set_button_comment(pif, keys={'yr': 'year', 'rg': 'region'})

    mainsec, secs, xsecs = create_lineup_sections(pif, year, region, section_types, fdebug=pif.form.get_bool('verbose'))

    # now that we have our sections calculated, format them.
    if listtype == mbdata.LISTTYPE_CSV:
        return render_lineup_csv(pif, mainsec, secs, xsecs)
    elif listtype == mbdata.LISTTYPE_JSON:
        return render_lineup_json(pif, mainsec, secs, xsecs)
    elif listtype == mbdata.LISTTYPE_TEXT:
        return render_lineup_text(pif, mainsec, secs, xsecs)
    elif listtype == mbdata.LISTTYPE_CHECKLIST:
        return render_lineup_checklist(pif, mainsec, secs, xsecs)
    # normal and/or large
    return render_lineup_year(pif, mainsec, secs, xsecs,
                              large=(listtype == mbdata.LISTTYPE_LARGE))


# --------- prodpics --------------------------------


def run_product_pics(pif, region):
    syear = 'year.' + pif.form.get_str('syear', '0000')
    eyear = 'year.' + pif.form.get_str('eyear', '9999')
    pages = [x for x in pif.dbh.fetch_page_years() if x['page_info.id'] >= syear and x['page_info.id'] <= eyear]
    pages = {x['id']: x for x in pages}
    gather_rank_pages(pif, pages, region)
    region_list = mbdata.get_region_tree(region)

    llineup = render.Matrix(id=pif.page_id)
    lsec = render.Section(columns=1, id='lineup')
    # hdr = ""

    for page in sorted(pages.keys()):
        lmodlist = pif.dbh.fetch_simple_lineup_models(page[5:], region)
        lmodlist = [x for x in lmodlist if x['lineup_model.region'][0] in region_list]
        lmoddict = {x['lineup_model.number']: x for x in lmodlist}
        min_num = 1
        max_num = pages[page]['max_lineup_number']
        if pif.form.get_str('num'):
            min_num = pif.form.get_int('num')
        if pif.form.get_str('enum'):
            max_num = pif.form.get_int('enum')
        lsec.columns = max(lsec.columns, max_num + 1)
        lran = render.Range(id=pages[page]['id'])
        ent = render.Entry(
            text='<a href="?year=%s&region=%s&lty=all&submit=1">%s</a>' % (page[5:], region, page[5:]),
            display_id='1'
        )
        lran.entry.append(ent)
        for mnum in range(min_num, max_num + 1):
            ifmt, pdir = get_product_image(pages[page], mnum)  # this isnt working - no section
            spdir = mbdata.dirs_r.get(pdir, pdir)
            lmod = lmoddict.get(mnum, {})
            lmod_id = lmod.get('lineup_model.mod_id', '')
            lpic_id = pic_id = lmod.get('lineup_model.picture_id', '').replace('w', pif.form.get_strl('region'))
            lreg = pif.form.get_stru('region')
            if pic_id:
                lpic_id = pic_id = pic_id.replace('W', lreg).replace('w', lreg.lower())
                product_image_path, product_image_file = pif.ren.find_image_file(
                    pic_id, suffix='jpg', pdir=pdir, largest='l')
            elif ifmt:
                lpic_id = ifmt.replace('w', lreg.lower()) % mnum
                product_image_path, product_image_file = pif.ren.find_image_file(
                    [lpic_id], suffix='jpg', pdir=pdir, largest='l')
            else:
                lpic_id = ''
                product_image_path, product_image_file = '', ''
                pic_id = None
            if not lmod or lmod.get('lineup_model.flags', 0) & config.FLAG_MODEL_NOT_MADE:
                pic_id = None
            halfstar = lmod and lmod.get('lineup_model.flags', 0) & config.FLAG_LINEUP_MODEL_MULTI_VARS
            lnk = f"single.cgi?dir={spdir}&pic={lpic_id}&ref={page}&sub=&id={lmod_id}"
            istar = '&nbsp;' if not lmod else imglib.format_image_star(
                pif, product_image_path, product_image_file, pic_id, halfstar)
            title = f"{mnum}: {lmod.get('lineup_model.name', '')}"
            ent = render.Entry(
                text=pif.ren.format_link(lnk, istar, also={'title': title}),
                display_id=str(int(mnum % 10 == 0 or page[-1] == '0'))
                # style='bl' if not mnum % 10 or page[-1] == '0' else 'yl' if mnum % 10 == 5 or page[-1] == '5' el 'wt'
            )
            lran.entry.append(ent)
        lsec.range.append(lran)

    llineup.section.append(lsec)
    return llineup


def gather_rank_pages(pif, pages, region):
    # all this is to grab pic_dir and img_format from section.  that's it.
    region_list = mbdata.get_region_tree(region)
    sections = [x for x in pif.dbh.fetch_sections(where="page_id like 'year.%'")
                if x['id'][0] in region_list]
    sections.sort(key=lambda x: x['start'], reverse=True)
    for rg in region_list:
        for page in pages:
            pages[page].setdefault('section', list())
            for section in sections:
                if section['id'].startswith(rg) and section['page_id'] == page:
                    pages[page]['section'].append(section)
    # now each page should have the right sections and in the right order
    # the first section found where start < num is the right one
    # though really we only care about the first one


def get_product_image(page, mnum):
    if page:
        if page.section:
            section = page.section[0]
            # useful.write_comment('get_product_image section', section['page_id'], section['id'])
            return section['link_format'], page['pic_dir']
        # useful.write_comment('get_product_image no section')
    # else:
        # useful.write_comment('get_product_image no page')
    return 'xxx%02d', 'unknown'


def product_pic_lineup_main(pif):
    pif.ren.styles.append('prodpic')
    pif.ren.title = mbdata.regions.get(pif.form.get_str('region'), 'Matchbox') + ' Lineup'
    llineup = run_product_pics(pif, pif.form.get_str('region').upper())
    return pif.ren.format_template('simplematrix.html', llineup=llineup.prep())


# --------- by ranks --------------------------------


def generate_rank_lineup(pif, rank, region, syear, eyear):
    # verbose = pif.ren.verbose
    regionlist = mbdata.get_region_tree(region) + ['']
    lmodlist = pif.dbh.fetch_lineup_models_by_rank(rank, syear, eyear)
    lmodlist.sort(key=lambda x: x['lineup_model.year'])
    years = dict()
    for mod in lmodlist:
        year = int(mod['lineup_model.year'])
        if mod['lineup_model.region'] in regionlist:
            years.setdefault(year, list())
            years[year].append(mod)

    for year in sorted(years.keys()):
        yield set_vars(years[year], pif.dbh.make_lineup_item(years[year][0]), regionlist, 'year.%s' % year)


def run_ranks(pif, mnum, region, syear, eyear):
    if not mnum:
        raise useful.SimpleError('Lineup number must be a number from 1 to 120.  Please back up and try again.')
    pif.ren.comment('lineup.run_ranks', mnum, region, syear, eyear)

    pages = {x['id']: x for x in pif.dbh.fetch_page_years()}
    gather_rank_pages(pif, pages, region)

    lmodlist = generate_rank_lineup(pif, mnum, region, syear, eyear)

    llineup = render.Matrix(id=pif.page_id)
    sect = dict(columns=5, flags=0, id='lineup')
    lsec = render.Section(columns=5, id='lineup')
    # hdr = "Number %s" % mnum
    comments = set()

    lran = render.Range(id='range')
    for mdict in lmodlist:
        if mdict:
            ifmt, pdir = get_product_image(pages.get(mdict.get('page_id', ''), {}), mnum)
            mdict['image_format'] = sect['img_format'] = ifmt
            mdict['disp_format'] = '%s.'
            mdict['pdir'] = pdir
            mdict['anchor'] = '%d' % mdict['number']
            mdict = calc_lineup_model(pif, sect, mdict['year'], region, mdict)
            mdict['displayed_id'] = str(mdict['year'])
            ent = render_lineup_model(pif, mdict, comments)
            if mdict['year'] == mdict['base_id.first_year']:
                ent.class_name = 'newcasting'
            lran.entry.append(ent)
        else:
            lran.entry.append(render.Entry())
    lsec.range.append(lran)

    llineup.section.append(lsec)
    pif.ren.set_button_comment(pif, keys={'yr': 'year', 'rg': 'region'})
    llineup.tail = ['', '<br>'.join([mbdata.comment_designation[comment] for comment in comments])]
    return llineup


def rank_lineup_main(pif):
    pif.ren.hierarchy_append(
        '/cgi-bin/lineup.cgi?n=1&num=%s&region=%s&syear=%s&eyear=%s&lty=all' % (
            pif.form.get_str('num'), pif.form.get_str('region'), pif.form.get_str('syear'), pif.form.get_str('eyear')),
        "%s #%d" % (mbdata.regions.get(pif.form.get_str('region'), ''), pif.form.get_int('num')))
    pif.ren.title = 'Matchbox Number %d' % pif.form.get_int('num')
    llineup = run_ranks(pif, pif.form.get_int('num'), pif.form.get_str('region', 'U').upper(),
                        pif.form.get_str('syear', '1953'), pif.form.get_str('eyear', '2014'))
    return pif.ren.format_template('simplematrix.html', llineup=llineup.prep(),
                                   large=False, unroll=pif.form.get_bool('unroll'))


# --------- select lineup ---------------------------


def select_lineup(pif, region, year):
    ypp = 15
    lran = render.Range()
    lsec = render.Section(range=[lran])
    llineup = render.Matrix(section=[lsec], header='<form>\n', footer='</form>')
    years = pif.dbh.fetch_lineup_years()
    while years:
        lines = pif.form.put_radio('year', [(x['year'], x['year']) for x in years[:ypp]], checked=year, sep='<br>\n')
        lran.entry.append(render.Entry(text=lines))
        years = years[ypp:]
    lran.entry.append(
        render.Entry(text=pif.form.put_radio('region', [(x, mbdata.regions[x]) for x in mbdata.regionlist[1:]],
                                             checked=region, sep='<br>\n')))
    lran.entry.append(render.Entry(
        text=pif.form.put_checkbox(
            'lty', mbdata.lineup_types, checked=[x[0] for x in mbdata.lineup_types], sep='<br>\n') +
        '<p>' + pif.form.put_button_input()))
    lsec.columns = len(lran.entry)
    return pif.ren.format_template('simplematrix.html', llineup=llineup.prep())


def show_all_lineups(pif):
    grid = {'': {
        'X.01': 'pkg', 'X.02': 'cat', 'X.03': 'ads', 'X.11': 'series', 'X.15': 'mvp', 'X.17': 'promo',
        'X.21': 'early', 'X.22': 'major', 'X.23': 'ks', 'X.24': 'rwr', 'X.25': 'srigs', 'X.31': 'moy',
        'X.41': 'acc', 'X.51': 'bui', 'X.61': 'ps', 'X.62': 'gs', 'X.63': '5p', 'X.64': 'l5p', 'X.65': 't5p',
        'X.66': '9/10', 'X.67': '2p', 'X.71': 'rwy', 'X.72': 'gm/pz', 'X.73': 'books',
    }}
    cols = set([' year'])
    for sec in pif.dbh.fetch_sections_by_page_type('lineup'):
        year = sec['section.page_id'][5:]
        sec_id = sec['section.id']
        if not sec_id.startswith('X'):
            sec_id = sec_id[0]
        grid.setdefault(year, {' year': year})
        grid[year][sec_id] = '<i>X</i>' if sec['section.flags'] & config.FLAG_SECTION_HIDDEN else 'X'
        cols.add(sec_id)

    llineup = render.Listix(section=[
        render.Section(range=[render.Range(entry=[y for x, y in sorted(grid.items())])], colist=sorted(cols))])
    return pif.ren.format_template('simplelistix.html', llineup=llineup.prep())


# --------- multiyear lineup ------------------------


def run_multi_file(pif, year, region, nyears):
    year = mbdata.correct_year(year)
    nyears = 5
    # as yet not rewritten
    pages = pif.dbh.fetch_pages('id in (' + ','.join(["'year.%d'" % x for x in range(year, year + nyears)]) + ')')

    # modlistlist = []
    max_mods = 0
    y = year
    nyears = len(pages)
    for page in pages:
        yregion = mbdata.correct_region(region, y)
        page['year'] = str(y)
        reg, mainsec, _, _ = get_man_sections(pif, y, yregion, ['man'])
        page['region'] = reg
        page['sec'] = mainsec
        page['img_format'] = mainsec['img_format']
        mods = pif.dbh.fetch_lineup_models(y, reg)
        page['mods'] = create_lineup(pif, mods, y, mainsec)
        max_mods = max(max_mods, len(page['mods']))
        y += 1

    llineup = render.Matrix(id=pif.page_id)
    mainsec = pages.first['sec']
    lsec = render.Section(columns=nyears, id='lineup')
    # hdr = lsec['name']
    comments = set()

    lran = render.Range(id='range')
    pif.ren.comment("run_file: range", lran)
    for inum in range(max_mods):
        for iyr in range(nyears):
            pdir = pages[iyr]['page_info.pic_dir']
            if pages[iyr]['mods']:
                mdict = pages[iyr]['mods'].pop(0)
                # mdict['disp_format'] = lsec.get('disp_format', '')
                mdict['shown_id'] = mdict['number']
                mdict['image_format'] = pages[iyr]['img_format']
                mdict['pdir'] = pdir
                mdict['anchor'] = '%d' % mdict['number']
                # mdict['region'] = region
                mdict = calc_lineup_model(pif, pages[iyr]['sec'], year + iyr, region, mdict)
                mdict['display_id'] = mdict.get('style_id', 0)
                if mdict['base_id.id'] and year + iyr == int(mdict['base_id.first_year']):
                    mdict['class_name'] = 'newcasting'
                mdict['displayed_id'] += ' (%s)' % (year + iyr)
                lran.entry.append(render_lineup_model(pif, mdict, comments))
            else:
                lran.entry.append(render.Entry())
    lsec.range.append(lran)

    llineup.section.append(lsec)
    pif.ren.set_button_comment(pif, keys={'yr': 'year', 'rg': 'region'})
    llineup.tail = ['', '<br>'.join([mbdata.comment_designation[comment] for comment in comments])]
    return llineup


def render_multiyear(pif, nyears=5):
    region = pif.form.get_stru('region')
    year = pif.form.get_str('year')
    pif.ren.hierarchy_append(
        '/cgi-bin/lineup.cgi?year=%s&region=%s&lty=all' % (year, region),
        "%s %s" % (year, mbdata.regions.get(region)))
    pif.ren.title = 'Matchbox %s-%s' % (year, int(year) + nyears - 1)
    llineup = run_multi_file(pif, year, region, nyears)
    return pif.ren.format_template('simplematrix.html', llineup=llineup.prep(), large=False,
                                   unroll=pif.form.get_bool('unroll'))


# --------- remember the main -----------------------


@basics.web_page
def main(pif):
    listtype = pif.form.get_str('listtype')
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append('/cgi-bin/lineup.cgi', 'Annual Lineup')

    if pif.form.get_str('year') and not pif.form.get_str('year').isdigit():
        raise useful.SimpleError('Year is incorrect.  It must be a number.')
    if pif.form.get_str('region') and pif.form.get_str('region') not in mbdata.regions:
        raise useful.SimpleError('Region not recognized.')

    if pif.form.has('prodpic'):
        pif.ren.print_html()
        return product_pic_lineup_main(pif)
    elif pif.form.get_int('byrank'):
        pif.ren.print_html(mbdata.get_mime_type(listtype))
        return rank_lineup_main(pif)
    elif pif.form.get_str('region') and pif.form.get_str('year'):
        if listtype == mbdata.LISTTYPE_CSV:
            pif.ren.filename = 'mb%s.csv' % pif.form.get_str('year')
        pif.ren.print_html(mbdata.get_mime_type(listtype))
        if listtype == mbdata.LISTTYPE_MULTIYEAR:
            return render_multiyear(pif)
        return year_lineup_main(pif, listtype)
    pif.ren.print_html()
    pif.ren.title = str(pif.form.get_str('year', 'Matchbox')) + ' Lineup'
    if pif.form.get_bool('large'):
        return show_all_lineups(pif)
    return select_lineup(pif, pif.form.get_str('region', 'W').upper(), pif.form.get_str('year', '0'))


# --------- command line stuff ----------------------


# def picture_count(pif, region, year):
#     # nonfunctional as yet
#     pr_count = im_count = 0
#     return 0, 0
#     year = mbdata.correct_year(year)
#     region = mbdata.correct_region(region, year)
#     # llineup = {'id': region, 'section': [], 'name': '', 'tail': []}
#
#     region, lsec, secs, xsecs = get_man_sections(pif, year, region, dict(mbdata.lineup_types).keys())
#     if not region:
#         return 0, 0
#
#     modlist = list(generate_man_lineup(pif, year, region))
#
#     endv = len(modlist)
#     for sec in reversed(secs):
#         sec['end'] = endv
#         endv = sec['start']
#
#     lsec['id'] = region
#     lsec['range'] = []
#
#     if secs:
#         for lran in secs:
#             lran.update({
#                 'id': region + '_' + str(lran['display_order']),
#                 'entry': [],
#                 'graphics': pif.ren.fmt_opt_img(
#                     [(lran['img_format'][:2] + region + 's%02d' % lran['display_order']).lower()])
#             })
#             count = count_section(pif, lsec, lran, modlist[lran['start']:lran['end']], region, year)
#             pr_count += count[0]
#             im_count += count[1]
#     else:
#         lran = copy.deepcopy(lsec)
#         lran.update({'id': region + '_1', 'name': '', 'entry': [], 'note': '', 'graphics': '&nbsp;'})
#         count = count_section(pif, lsec, lran, modlist, region, year)
#         pr_count += count[0]
#         im_count += count[1]
#
#     # ==================================
#
#     # xsecs = get_extra_sections(pif, year)
#     create_extra_lineup(pif, year, xsecs, verbose=pif.ren.verbose)
#
#     for lran in xsecs:
#         lran.update({
#             'id': 'X_' + str(lran['display_order']),
#             'entry': [],
#             'graphics': pif.ren.fmt_opt_img([(lran['img_format'][:2] + region +
#                 's%02d' % lran['display_order']).lower()])
#         })
#         count = count_section(pif, lsec, lran, lran['mods'], 'X', year)
#         pr_count += count[0]
#         im_count += count[1]
#     return pr_count, im_count
#
#
# def count_section(pif, lsec, lran, mods, region, year):
#     im_count = pr_count = 0
#     for mdict in mods:
#         mdict['image_format'] = lran['img_format']
#         pdir = pif.ren.pic_dir
#         if lran.get('pic_dir'):
#             pdir = lran['pic_dir']
#         mdict['pdir'] = pdir
#         pr_count += 1
#         im_count += count_lineup_model(pif, mdict)
#     return pr_count, im_count


def yearlist(pif):
    for year in range(1953, 2018):
        rl = set()
        for reg in mbdata.regionlist[1:]:
            rl.add(mbdata.correct_region(reg, year))
        print(year, rl)


def cklup(pif):
    mainsec, secs, xsecs = create_lineup_sections(
        pif, pif.form.get_str('year', '1966'), pif.form.get_str('region', 'W'), dict(mbdata.lineup_types).keys())

    for sec in [mainsec] + secs:
        print(sec['id'])
        for mod in sec.get('mods', []):
            print(' ', mod['number'], mod['display_order'], mod['name'])
            for vard in mod['cvarlist']:
                print('    ', vard['desc'])

    for sec in xsecs:
        print(sec['id'])
        for mod in sec['mods']:
            print('   ', mod['number'], mod['display_order'], mod['name'])


def year_lineup(pif, year, region):
    section_types = dict(mbdata.lineup_types).keys()
    mainsec, secs, xsecs = create_lineup_sections(pif, year, region, section_types, fdebug=False)
    # llineup = {'id': 'year', 'section': [], 'name': '', 'tail': []}
    print(render_lineup_text(pif, mainsec, secs, xsecs))


def clone_lineup(pif, year, old_region, new_region=''):
    old_region = old_region.upper()
    new_region = new_region.upper()
    for mod in pif.dbh.depref('lineup_model', pif.dbh.fetch_lineup_models_bare(year, old_region)):
        if old_region != new_region and new_region:
            del mod['id']
            mod['base_id'] = mod['base_id'].replace(old_region, new_region)
            mod['picture_id'] = mod['picture_id'].replace(old_region.lower(), new_region.lower())
            mod['region'] = new_region
            pif.dbh.insert_lineup_model(mod)
        print(mod)


# def count_lineup(pif, year, region):
    # print(picture_count(pif, region, year))


def rank_lineup(pif, number, region, syear, eyear):
    llineup = run_ranks(pif, number, region.upper(), syear, eyear)
    print(render_lineup_text(pif, llineup['section'][0], llineup['section'][1:], []))


def list_lineups(pif):
    section_types = ['man']  # dict(mbdata.lineup_types).keys()
    ctypes = sorted(mbdata.comment_name.keys())
    regionlist = [x for x in mbdata.regionlist if x != 'W']
    limits = pif.dbh.fetch_lineup_limits()
    first_year = int(limits['min(year)'])
    last_year = int(limits['max(year)'])
    comments = set()
    for year in range(first_year, last_year + 1):
        regions = sorted(set([mbdata.correct_region(x, year) for x in regionlist]))
        if not regions:
            regions = ['R', 'U']
        for region in regions:
            mainsec, secs, xsecs = create_lineup_sections(pif, year, region, section_types)
            llineup = render_lineup_year_sections(pif, mainsec, secs, xsecs)
            comments |= llineup['comments']
            print(year, region, ':', ' '.join([x if x in llineup['comments'] else ' ' for x in ctypes]))
    print()
    for comment in sorted(comments):
        print(comment, mbdata.comment_name[comment])


# input file has new models in form:
# 1|MB1002|Heavy Railer|red/yellow
# lineup_number | mod_id | mod_name | var_description

# currently can't handle multiple variations of a particular number

# hardcoded values:
regions = ['U', 'R']
picdir = 'pic/prod/mworld'


def raw_insert(pif, table, data):
    pif.dbh.dbi.insert_or_update(table, data)


def add_page(pif, year):
    raw_insert(pif, 'page_info', {
        'id': 'year.' + year,
        'flags': 0,
        'format_type': 'lineup',
        'title': 'Matchbox %s Lineup' % year,
        'pic_dir': picdir,
        'tail': '',
        'description': '',
        'note': '',
    })


def add_section(pif, year, region):
    raw_insert(pif, 'section', {
        'id': region,
        'page_id': 'year.' + year,
        'display_order': 0,
        'category': 'man',
        'flags': 0,
        'name': mbdata.regions[region],
        'columns': 4,
        'start': 0,
        'pic_dir': '',
        'disp_format': '%d.',
        'link_format': pif.form.get_str('link_fmt'),  # clearly wrong
        'img_format': '%s%s%%03d' % (year, region.lower()),
        'note': '',
    })


def add_casting(pif, mod, year):
    # base_id: id, first_year, model_type, rawname, description, flags
    # casting: id, country, make, section_id
    print('add casting', mod, year)
    pif.dbh.add_new_base_id({
        'id': mod[1],
        'first_year': year,
        'model_type': 'SF',
        'rawname': mod[2],
        'description': '',
        'flags': 0,
    })
    pif.dbh.add_new_casting({
        'id': mod[1],
        'country': '',
        'make': '',
        'section_id': 'man3',
        'notes': '',
    })


def add_variation(pif, mod, year):
    var_id = 'Y' + year[2:]
    var = {
        'mod_id': mod[1],
        'var': var_id,
        'flags': 0,
        'text_description': '',
        'text_base': '',
        'text_body': '',
        'text_interior': '',
        'text_wheels': '',
        'text_windows': '',
        'text_with': '',
        'base': '',
        'body': mod[3],
        'interior': '',
        'windows': '',
        'manufacture': '',
        # 'category': '',
        'area': '',
        'date': '',
        'note': '',
        'other': '',
        'picture_id': '',
        'imported': '',
        'imported_from': 'file',
        'imported_var': var_id,
    }
    # print(('variation', mod[1], var_id, var))
    pif.dbh.insert_variation(mod[1], var_id, var, verbose=True)
    pif.dbh.recalc_description(mod[1], showtexts=False, verbose=False)


def add_lineup_model(pif, mod, year, region):
    lin_id = '%s%s%03d' % (year, region, int(mod[0]))
    # lineup_model
    raw_insert(pif, 'lineup_model', {
        'base_id': lin_id,
        'mod_id': mod[1],
        'number': mod[0],
        'flags': 0,
        'style_id': mod[2],
        'picture_id': '',
        'region': region,
        'year': year,
        'name': mod[3],
        'page_id': 'year.' + year,
    })


def add_variation_select(pif, mod, year, region):
    raw_insert(pif, 'variation_select', {
        'ref_id': 'year.' + year,
        'mod_id': mod[1],
        'var_id': 'Y' + year[2:],
        'sec_id': '',
        'ran_id': '',
    })


def make_lineup(pif, year, fn):
    inmods = [x.split('|') for x in open(fn).readlines() if not x.startswith('#')]
    add_page(pif, year)
    for region in regions:
        add_section(pif, year, region)
        for mod in inmods:
            # casting = pif.dbh.fetch_casting(mod[1])
            # if not casting:
            #     add_casting(pif, mod, year)
            # add_variation(pif, mod, year)
            add_lineup_model(pif, mod, year, region)
            # add_variation_select(pif, mod, year, '')


def generate_promos(pif, year):
    lineup_page_id = 'year.' + year
    vars = pif.dbh.fetch_variations_by_date(year, wildcard=True)
    for var in vars:
        if set(['TF', 'PR']) & set(var['variation.category'].split(' ')):
            nvs = {
                'mod_id': var['variation.mod_id'],
                'var_id': var['variation.var'],
                'ref_id': lineup_page_id,
                'sec_id': 'X17',
                'ran_id': '',
                'category': 'PR',
            }
            print(nvs)
            print(pif.dbh.write('variation_select', values=nvs, newonly=True, tag='WriteVarSel'))
    print()
    vslist = sorted(pif.dbh.fetch_variation_selects_by_ref(ref_id=lineup_page_id, sec_id='X17'),
                    key=lambda x: x['variation.date'])
    for number, vs in enumerate(vslist, start=1):
        lm = {
            'base_id': f'{year}X17{number:02}',
            'mod_id': vs['base_id.id'],
            'number': number,
            'display_order': number,
            'flags': 0,
            'style_id': 'lg',
            'picture_id': '',
            'region': 'X.17',
            'year': year,
            'page_id': lineup_page_id,
            'name': vs['base_id.rawname'].replace(';', ' '),
        }
        nvs = {
            'id': vs.get('variation_select.id'),
            'mod_id': vs['base_id.id'],
            'var_id': vs['variation.var'],
            'ref_id': lineup_page_id,
            'sec_id': 'X17',
            'ran_id': number,
            'category': 'PR',
        }
        print(vs['variation.date'])
        print(lm)
        print(pif.dbh.insert_lineup_model(lm))
        print(nvs)
        print(pif.dbh.update_variation_select(nvs))


def generate_lineup(pif, ref_id):
    vslist = sorted(pif.dbh.fetch_variation_selects_by_ref(ref_id=ref_id), key=lambda x: x['variation.date'])
    if ref_id.startswith('year.'):
        print('#number|mod_id|style|name')
        for vs in vslist:
            # print(vs.mod_id, 'gy'), vs.base_id.rawname
            print(f"{vs['variation.note']}|{vs['variation_select.mod_id']}|gy|{vs['base_id.rawname']}")
    elif ref_id.startswith('matrix.'):
        print('#section_id|display_order|page_id|range_id|mod_id|name')
        for ind, vs in enumerate(vslist, start=1):
            print(f"{vs['variation_select.sec_id']}|{ind}|{ref_id}|{ind}|"
                  f"{vs['variation_select.mod_id']}|{vs['base_id.rawname']}")
    else:
        print("don't understand", ref_id, "yet")


# def check_lineup(pif, *args):
#     def do_lup(pif, year, region):
#         lup = run_file(pif, region, str(year))
#         totals['i'] += lup['var_info']['i']
#         totals['p'] += lup['var_info']['p']
#         print('%d  %s  %3d  %3d' % (year, region, lup['var_info']['i'], lup['var_info']['p']))
#
#     totals = {'i': 0, 'p': 0}
#
#     st = 1953
#     en = 2018
#     if args:
#         st = int(args[0])
#         if len(args) > 1:
#             en = int(args[1])
#         else:
#             en = st
#     for year in range(st, en + 1):
#         pif.page_id = 'year.%d' % year
#         lup = do_lup(pif, year, 'U')
#         if year >= 1982:
#             lup = do_lup(pif, year, 'R')
#         if year in (1999, 2000, 2001):
#             lup = do_lup(pif, year, 'D')
#         if year in (2000, 2001):
#             lup = do_lup(pif, year, 'B')
#             lup = do_lup(pif, year, 'A')
#         if year >= 2008 and year <= 2011:
#             lup = do_lup(pif, year, 'L')
#     print('        %4d %4d' % (totals['i'], totals['p']))


def show_sections(pif):
    secs = pif.dbh.depref('section', pif.dbh.fetch('section', where='page_id like "year.%" and id like "X.%"'))
    sec_ids = set()
    pages = {}
    for sec in secs:
        sec['showflag'] = '-' if sec['flags'] & 1 else 'X'
        sec_ids.add(sec['id'][2:])
        pages.setdefault(sec['page_id'][5:], dict())
        pages[sec['page_id'][5:]][sec['id'][2:]] = sec
    sec_ids = sorted(sec_ids)

    def hdr():
        print('page |', ' | '.join(sec_ids), '|')

    hdr()
    print('-----+' + len(sec_ids) * '----+')
    for page_id in sorted(pages):
        if not (int(page_id) % 40):
            hdr()
        print(page_id, '|', ' | '.join(
            [pages[page_id].get(sec_id, {}).get('showflag', ' ') + ' ' for sec_id in sec_ids]) + ' |')


def lineup_pics(pif, *args):
    missing = 'm' in args
    years = useful.expand_number_list([x for x in args if x.replace('-', '').isdigit()])
    regions = [x for x in args if not x.isdigit() and x.isupper()]
    if not years:
        lim = pif.dbh.fetch_lineup_limits()
        years = range(int(lim['min(year)']), int(lim['max(year)']) + 1)
    if not regions:
        regions = mbdata.regionlist
    for yr in years:
        page = pif.dbh.fetch_page('year.%d' % int(yr))
        pdir = page.pic_dir
        found = {}
        lml = pif.dbh.fetch_simple_lineup_models(year=yr)
        for lm in lml:
            reg = lm['lineup_model.region']
            if reg in regions:
                found.setdefault(reg, list())
                fn = pdir + '/m_' + (lm['lineup_model.picture_id'] if lm['lineup_model.picture_id'] else
                                     lm['lineup_model.base_id']).replace('W', reg).lower() + '.jpg'
                if (lm['lineup_model.flags'] & config.FLAG_MODEL_NOT_MADE or os.path.exists(fn)) and not missing:
                    found[reg].append(lm['lineup_model.number'])
                elif not (lm['lineup_model.flags'] & config.FLAG_MODEL_NOT_MADE or os.path.exists(fn)) and missing:
                    found[reg].append(lm['lineup_model.number'])
        for reg in sorted(found):
            print(yr, reg, ' '.join(useful.collapse_number_list(found[reg])))


def detect_lineup(pif, year):
    for vs in pif.dbh.fetch_variation_selects(ref_id='year.' + year):
        # 1|MB1227  |1|2020 Honda E
        casting = pif.dbh.fetch_casting(vs.mod_id)
        var = pif.dbh.fetch_variation_bare(vs.mod_id, vs.var_id)[0]
        print('{}|{}|{}|{}'.format(var['variation.note'], vs.mod_id, '1', casting['rawname']))


def import_series(pif, matrix_page, matrix_section, year, lineup_section):
    pass
    for mm in pif.dbh.fetch_matrix_models(page_id=matrix_page, section=matrix_section):
        values = {
            'base_id': f'{year}{lineup_section.replace(".", "")}{mm.range_id}',
            'mod_id': mm.mod_id,
            'number': mm.range_id,
            'display_order': mm.display_order,
            'flags': 0,
            'style_id': 'lg',
            'picture_id': '',
            'region': lineup_section,
            'year': year,
            'page_id': f'year.{year}',
            'name': mm.name,
            'subname': '',
        }
        print(pif.dbh.insert_lineup_model(values))
    for vs in pif.dbh.fetch_variation_selects_for_ref(matrix_page, matrix_section):
        del vs['variation_select.id']
        vs['variation_select.ref_id'] = f'year.{year}'
        vs['variation_select.sec_id'] = lineup_section.replace('.', '')
        print(pif.dbh.update_variation_select(vs))


cmds = [
    ('s', year_lineup, "show: year region [number]"),
    ('c', clone_lineup, "clone: year old_region new_region"),
    # ('p', count_lineup, "count: year region"),
    ('r', rank_lineup, "ranks: number region syear eyear"),
    ('l', list_lineups, "list lineups"),
    ('m', make_lineup, "make lineup"),
    ('g', generate_lineup, "generate lineup"),
    ('gp', generate_promos, "generate promos: year"),
    ('dl', detect_lineup, "detect lineup: year"),
    # ('x', check_lineup, "check lineup"),
    ('s', show_sections, "show sections"),
    ('pic', lineup_pics, "pics"),
    ('is', import_series, "import series: matrix_page matrix_section year lineup_section"),
]


# ---- ---------------------------------------


if __name__ == '__main__':  # pragma: no cover
    basics.process_command_list(cmds=cmds, page_id='editor', dbedit='')
