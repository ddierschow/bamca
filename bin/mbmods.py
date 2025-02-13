#!/usr/local/bin/python

import config
import mbdata
import mflags
import render
import useful


flago = mflags.FlagList()


text_attrs = {'de': 'text_description', 'ba': 'text_base', 'bo': 'text_body', 'in': 'text_interior',
              'wh': 'text_wheels', 'wi': 'text_windows', 'wt': 'text_with', 'bt': 'text_text'}
text_fmts = {'de': 'format_description', 'ba': 'format_base', 'bo': 'format_body', 'in': 'format_interior',
             'wh': 'format_wheels', 'wi': 'format_windows', 'wt': 'format_with', 'bt': 'format_text'}
text_titles = {'de': 'Description', 'ba': 'Base', 'bo': 'Body', 'in': 'Interior',
               'wh': 'Wheels', 'wi': 'Windows', 'wt': 'With', 'bt': 'Base Text'}
text_short_titles = {'de': 'De', 'ba': 'Ba', 'bo': 'Bo', 'in': 'In', 'wh': 'Wh', 'wi': 'Wi', 'wt': 'W/', 'bt': 'BT'}
var_types = ['c', '1', '2', 'p', 'f']

# lineup, mannum
# shows first_year, flag, pic, model name, description, with link to single.
mod_tab_pic_lnk_pat = '''
  <center>
   <table class="entry">
    <tr>
     <td></td>
     <td width="32"><i><font size=-1>%(first_year)s</font></i></td>
     <td width="136"><center><font face="Courier">%(id)s</font></center></td>
     <td width="32">%(flag)s</td>
     <td></td></tr>
    <tr>
     <td colspan="5"><center>%(lname)s %(desclist)s</center></td>
    </tr>
   </table>
  </center>
'''
mod_tab_thumb_pat = '''
  <center>
   <table class="entry">
    <tr>
     <td><center><font face="Courier">%(id)s</font></center></td>
    </tr>
    <tr>
     <td><center>%(lname)s</center></td>
    </tr>
   </table>
  </center>
'''


def add_model_table_pic_link(pif, mdict, flago=flago):
    mdict = add_model_table_pic_link_dict(pif, mdict, flago)
    if mdict.get('prefix') == mbdata.IMG_SIZ_TINY:
        return mod_tab_thumb_pat % mdict
    return mod_tab_pic_lnk_pat % mdict


def generate_model_table_pic_link(pif, mdict, mlist):
    for mod_id in mlist:
        yield {'text': add_model_table_pic_link(pif, mdict[mod_id])}


# for templates


def add_model_table_pic_link_dict(pif, mdict, flago=flago):
    # input mdict:  id, (picture_id), made, country, link, linkid, name, descs, made, unlicensed, first_year, (type)
    # pif.ren.comment('add_model_table_pic_link', mdict)
    if not flago:
        flago = {}
    img = [mdict['id']]
    if mdict.get('picture_id'):
        img = [mdict['picture_id']]
    for s in mdict['descs']:
        if s.startswith('same as '):
            img.append(s[8:].lower())
    img_size = mdict.get('prefix', mbdata.IMG_SIZ_LARGE if pif.form.get_bool('large') else mbdata.IMG_SIZ_SMALL)
    mdict['img'] = pif.ren.format_image_required(img, made=mdict['made'], prefix=img_size)
    mdict['flag'] = ''
    if mdict.get('country') in flago:
        mdict['flag'] = pif.ren.format_image_flag(mdict['country'], flago[mdict['country']], also={'align': 'right'})
    elif mdict['unlicensed'] == '-':
        mdict['flag'] = pif.ren.format_image_art('mbx.gif')
    # pif.ren.comment('FLAG?', mdict['id'], mdict['country'], mdict['flag'])
    if mdict.get('link'):
        mdict['lname'] = '<a href="%(link)s=%(linkid)s">%(img)s<br><b>%(name)s</b></a>' % mdict
    else:
        mdict['lname'] = '%(img)s<br><b>%(name)s</b>' % mdict
    if mdict.get('subname'):
        mdict['lname'] += '<br>' + mdict['subname']
    mdict['desclist'] = ''
    # useful.write_comment(mdict['id'], mdict['descs'])
    if not mdict.get('nodesc'):
        for s in mdict['descs']:
            if s in mbdata.casting_arts:
                mdict['desclist'] += f"<br>{pif.ren.format_image_icon(mbdata.casting_arts[s] + '.gif')}"
            elif s:
                mdict['desclist'] += f"<br><i>{s}</i>\n"
    mdict['shown_id'] = mdict.get('alias.id') or mdict['id']
    return mdict


def generate_model_table_pic_link_dict(pif, mdict, mlist):
    for mod_id in mlist:
        yield add_model_table_pic_link_dict(pif, mdict[mod_id])


# mdict: descriptions href imgstr name no_casting not_made number pdir picture_only product subname additional
def add_model_table_product_link(pif, mdict):
    # pif.ren.comment('add_model_table_product_link', mdict)

    ostr = pif.ren.fmt_anchor(mdict.get('anchor'))
    ostr += '<center><table class="modeltop"><tr><td class="modelstars">'
    if mdict.get('no_casting'):
        ostr += mbdata.comment_icon.get('m', '')
    elif not mdict.get('picture_only'):
        if mdict.get('no_specific_image'):
            ostr += mbdata.comment_icon.get('i', '')
        if mdict.get('no_variation'):
            ostr += mbdata.comment_icon.get('v', '')
    ostr += f'</td><td class="modelnumber">{mdict["displayed_id"]}</td><td class="modelicons">'
    if pif.is_allowed('a'):
        # breaks packs
        ref_link = pif.dbh.get_editor_link('lineup_model', {'year': mdict.get('year'), 'mod_id': mdict.get('mod_id')})
        ostr += pif.ren.format_link(ref_link, pif.ren.fmt_edit('gray'))
        if 'mod_id' in mdict:
            fn = mdict.get('mod_id', '').replace('.', '_') + (
                '-' + mdict.get('picture_id', '') if mdict.get('picture_id', '') else '')
            ostr += pif.ren.format_link(f'upload.cgi?d=lib/man&n={fn}&m={fn}&c={fn}',
                                        pif.ren.fmt_mini('gray', icon='upload'))
    if mdict.get('not_made'):
        ostr += mbdata.comment_icon.get('n', '')
    if mdict.get('is_reused_product_picture'):  # pragma: no cover
        ostr += mbdata.comment_icon.get('r', '')
    if mdict.get('is_product_picture'):
        ostr += mbdata.comment_icon.get('c', '')
    ostr += '</td></tr></table>\n'

    if mdict.get('show_vars'):
        # imgstr descriptions
        for vdict in mdict['show_vars']:
            if mdict.get('href'):
                ostr += '<a href="%(href)s">\n' % mdict
            # ostr += ('<table class="spicture"><tr><td class="spicture"><center>%s</center></td></tr></table>\n' %
            #          vdict['imgstr'])
            ostr += f'<center>{vdict["imgstr"]}</center>\n<span class="modelname">{mdict["name"]}</span>'
            if mdict.get('href'):
                ostr += '</a>'
            if mdict.get('subname'):
                mdict['lname'] += '<br>' + mdict['subname']
            if mdict.get('subnames'):
                ostr += "<br>" + "<br>".join(mdict['subnames'])
            if vdict.get('description'):
                ostr += '<table class="vartable">'
                ostr += f'<tr><td class="varentry">{vdict["description"]}</td></tr>'
                ostr += "</table>"
            ostr += "</center>"
    else:
        if mdict.get('href'):
            ostr += '<a href="%(href)s">\n' % mdict
        # ostr += ('<table class="spicture"><tr><td class="spicture"><center>%s</center></td></tr></table>\n' %
        #          mdict['imgstr'])
        ostr += '<center>%s</center>\n' % (mdict['imgstr'])
        ostr += '<span class="modelname">' + mdict['name'] + '</span>'
        if mdict.get('href'):
            ostr += '</a>'
        if mdict.get('subname'):
            ostr += '<br>' + mdict['subname']
        if mdict.get('subnames'):
            ostr += "<br>" + "<br>".join(mdict['subnames'])
        if mdict.get('descriptions'):
            ostr += '<table class="vartable">'
            for var in mdict['descriptions']:
                ostr += '<tr><td class="varentry">%s</td></tr>' % var
            ostr += "</table>"
        ostr += "</center>"

    ostr += mdict.get('additional', '')
    return ostr


# lineup, mannum
# shows scale, flag, pic, model name, description, with link to single.
mod_txt_lin_pat = '''%(long_id)s|%(name)s|%(desc)s
'''


def add_model_text_line(pif, mdict):
    # input mdict:  id, (picture_id), made, country, link, linkid, name, descs, made, unlicensed, scale, (type)
    sub_id = 'a'
    ostr = ''
    desclist = []
    for var in mdict.get('descriptions', []):
        if var and var not in desclist:
            desclist.append(var)
    if desclist:
        for s in desclist:
            if not mdict.get('disp_format') or not mdict.get('shown_id'):
                mdict['long_id'] = mdict['id'] + sub_id
            else:
                mdict['long_id'] = mdict['disp_format'] % (mdict['shown_id']) + sub_id
            sub_id = chr(ord(sub_id) + 1)
            mdict['desc'] = s
            ostr += mod_txt_lin_pat % mdict
    else:
        if not mdict.get('disp_format') or not mdict.get('shown_id'):
            mdict['long_id'] = mdict['id']
        else:
            mdict['long_id'] = mdict['disp_format'] % (mdict['shown_id'])
        mdict['desc'] = ''
        ostr += mod_txt_lin_pat % mdict
    return ostr


# id, man_id, imgstr, name
def add_model_link(pif, mdict):
    ostr = '   <center>%(id)s<br><a href="single.cgi?id=%(man_id)s">%(imgstr)s</a><br>' % mdict
    ostr += '<b>%(name)s</b></center>' % mdict
    return ostr


# lineup, mannum
# shows scale, flag, pic, model name, description, with link to single.
mod_tab_lst_ent_pat = '''  <td>%(box_sm)s</td>
  <td><center>%(id)s</center></td>
  <td>%(first_year)s</td>
  <td>%(lname)s</td>
'''


def add_model_table_list_entry_dict(pif, mdict):
    if mdict:
        # input mdict:  id, (picture_id), made, country, link, linkid, name, descs, made, unlicensed, scale, (type)
        mdict['lname'] = mdict['shortname']
        if mdict.get('link'):
            mdict['lname'] = '<a href="%(link)s=%(linkid)s">%(lname)s</a>' % mdict
        mdict['box_sm'] = pif.ren.fmt_square(hollow=True)
    return mdict


def add_model_table_list_entry(pif, mdict):
    mdict = add_model_table_list_entry_dict(pif, mdict)
    return mod_tab_lst_ent_pat % mdict


def add_model_pic_link_short(pif, id):
    ostr = f'<center><b id="{id}">{id}</b><br><a href="single.cgi?id={id}">' + pif.ren.format_image_required(
        [id], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_MAN) + '</a></center>'
    return ostr


def add_icons(pif, type_id, base_id, vehicle_type):
    icon_list = []
    if type_id:
        icon = pif.ren.format_image_icon(type_id, also={'class': 'centered'})
        if icon != '&nbsp;':
            icon_list.append(icon)
    if base_id:
        icon = pif.ren.format_image_optional(
            base_id, None, prefix='i_', suffix='gif', pdir=config.IMG_DIR_MAN_ICON, also={'class': 'centered'})
        if icon != '&nbsp;':
            icon_list.append(icon)
    for vtype in vehicle_type:
        if vtype in mbdata.model_icons:
            icon_list.append(pif.ren.format_image_icon(mbdata.model_icons[vtype]))
    ostr = '<p>' + '<p><p>'.join(icon_list)
    return ostr


def show_adds(pif, mod_id, var_id=''):
    photo_credits = {x['photo_credit.name']: x['photographer.name']
                     for x in pif.dbh.fetch_photo_credits(path='.' + config.IMG_DIR_ADD)}
    attribute_pictures = pif.dbh.fetch_attribute_pictures(mod_id)
    attribute_pictures = dict([
        (x['attribute_picture.attr_type'].lower() + '_' + x['attribute_picture.mod_id'].lower() + '-' +
         x['attribute_picture.picture_id'] + '.', x) for x in attribute_pictures if x['attribute_picture.picture_id']])

    img_id = (mod_id + ('-' + var_id if var_id else '')).lower()
    pdir = '.' + (config.IMG_DIR_VAR if var_id else config.IMG_DIR_ADD)
    adds = mbdata.var_adds if var_id else mbdata.model_adds
    ostr = ''
    for add in adds:
        imgs = pif.ren.find_image_list(img_id, wc='-*', suffix='*', prefix=add[0], pdir=pdir)
        if imgs:
            ostr += '<h3>%s</h3>\n' % add[1] % {'s': useful.plural(imgs)}
            for img in imgs:
                ostr += '<table><tr><td class="center">'
                ostr += pif.ren.fmt_img_src(pdir + '/' + img) + '<br>'
                fn = img[:img.find('.')]
                if fn in photo_credits:
                    ostr += '<div class="credit">Photo credit: %s</div>' % photo_credits[fn]
                for apic in attribute_pictures:
                    # This is terrible and I'm a terrible person but I don't want to think too much right now.
                    if apic in img and attribute_pictures[apic]['attribute_picture.description']:
                        if attribute_pictures[apic]['attribute.title']:
                            ostr += "%(attribute.title)s: %(attribute_picture.description)s" % attribute_pictures[apic]
                        else:
                            ostr += "%(attribute_picture.description)s" % attribute_pictures[apic]
                ostr += '</td></tr></table>'
                ostr += '<p>\n'
    return ostr


def make_adds(pif, mod_id, var_id=''):
    photo_credits = {x['photo_credit.name']: x['photographer.name']
                     for x in pif.dbh.fetch_photo_credits(path='.' + config.IMG_DIR_ADD)}
    attribute_pictures = pif.dbh.fetch_attribute_pictures(mod_id)
    attribute_pictures = dict([
        (x['attribute_picture.attr_type'].lower() + '_' + x['attribute_picture.mod_id'].lower() + '-' +
         x['attribute_picture.picture_id'] + '.', x) for x in attribute_pictures if x['attribute_picture.picture_id']])

    img_id = (mod_id + ('-' + var_id if var_id else '')).lower()
    pdir = '.' + (config.IMG_DIR_VAR if var_id else config.IMG_DIR_ADD)
    adds = mbdata.var_adds if var_id else mbdata.model_adds
    outd = []
    for add in adds:
        imgs = pif.ren.find_image_list(img_id, wc='-*', suffix='*', prefix=add[0], pdir=pdir)
        if imgs:
            elem = {'title': add[1] % {'s': useful.plural(imgs)}, 'entry': [],
                    'columns': add[3]}
            for img in imgs:
                fn = img[:img.find('.')]
                ent = {'img': pif.ren.fmt_img_src(pdir + '/' + img),
                       'credit': photo_credits.get(fn, '')}
                for apic in attribute_pictures:
                    # This is terrible and I'm a terrible person but I don't want to think too much right now.
                    if apic in img and attribute_pictures[apic]['attribute_picture.description']:
                        if attribute_pictures[apic]['attribute.title']:
                            ent['desc'] = ("%(attribute.title)s: %(attribute_picture.description)s" %
                                           attribute_pictures[apic])
                        else:
                            ent['desc'] = "%(attribute_picture.description)s" % attribute_pictures[apic]
                elem['entry'].append(ent)
            outd.append(elem)
    return outd


def add_model_thumb_pic_link(pif, mdict):
    ostr = '<table><tr><td class="image">'
    ostr += pif.ren.format_image_required([mdict['id']], prefix=mbdata.IMG_SIZ_TINY, pdir=config.IMG_DIR_MAN)
    ostr += '</td>\n<td class="text">'
    if mdict['id']:
        ostr += '<span class="modelname">'
        ostr += pif.ren.format_link('single.cgi?id=%s' % mdict['id'], mdict['id'] + ': ' + mdict['name'])
        ostr += '</span><br>\n'
    img = mdict['img']
    if isinstance(img, list):
        img = '<ul>%s</ul>' % ('\n'.join(['<li>' + x for x in img]))
    ostr += '<span class="info">See: %s</span>' % img
    ostr += '</td></tr></table>\n'
    return ostr


def add_model_var_pic_link(pif, vdict):
    vdict['link'] = 'vars.cgi?mod=%s&var=%s' % (vdict['mod_id'], vdict['var'].upper())
    vdict['categories'] = ''
    pic_id = vdict['picture_id'] if vdict['picture_id'] else vdict['var']
    img = pif.ren.find_image_path([vdict['mod_id']], nobase=True, vars=pic_id, prefix=mbdata.IMG_SIZ_SMALL,
                                  pdir=config.IMG_DIR_MAN)
    vdict['img'] = pif.ren.fmt_img_src(img) if img else pif.ren.fmt_no_pic(True, mbdata.IMG_SIZ_SMALL)

    return '''
<a href="%(link)s">%(var)s<br>
<center><table class="spicture"><tr><td class="spicture">%(img)s</td></tr></table></center></a>
<table class="vartable">
<tr><td class="varentry"><i>%(text_description)s</i></td></tr>
</table>
''' % vdict


def make_page_list(pif, format_type, fmt_link):
    pif.ren.set_button_comment(pif)
    secs = pif.dbh.fetch_sections_by_page_type(format_type)
    entries = list()
    for sec in secs:
        hidden = sec.flags & config.FLAG_PAGE_INFO_HIDDEN or sec.page_info.flags & config.FLAG_PAGE_INFO_HIDDEN
        if '.' in sec.page_id and (pif.ren.is_alpha or pif.ren.is_beta or not hidden):
            entries.append(render.Entry(text=('<i>%s</i>' if hidden else '%s') % fmt_link(sec)))
    lsec = render.Section(
        section=[x for x in secs if x.page_id == format_type][0],
        range=[render.Range(entry=entries)], columns=5
    )
    llineup = render.Matrix(id='main', section=[lsec])
    return pif.ren.format_template('packpages.html', llineup=llineup.prep())


def add_model_var_table_pic_link(pif, mdict):
    if mdict.get('v.picture_id'):
        mdict['img'] = pif.ren.format_image_required(
            mdict['v.mod_id'], prefix=mbdata.IMG_SIZ_SMALL, nobase=True, vars=mdict['v.picture_id'])
    else:
        mdict['img'] = pif.ren.format_image_required(
            mdict['v.mod_id'], prefix=mbdata.IMG_SIZ_SMALL, nobase=True, vars=mdict['v.var'])
    # mdict['link'] = 'single.cgi?id=%(v.mod_id)s' % mdict
    mdict['link'] = 'vars.cgi?mod=%(v.mod_id)s&var=%(v.var)s' % mdict
    ostr = (
        '  <center><table class="entry"><tr><td><center><font face="Courier">%(v.mod_id)s-%(v.var)s</font></br>\n'
        '   <a href="%(link)s">%(img)s<br><b>%(name)s</b></a>\n') % mdict
    # ostr += "   <br><i>%(v.text_description)s</i>\n" % mdict
    ostr += '<table class="vartable">'
    ostr += '<tr><td class="varentry"><i>%s</i></td></tr>' % mdict['v.text_description']
    ostr += "</table>"
    ostr += "  </center></td></tr></table></center>\n"
    return ostr


def get_mack_numbers(pif, cid, mod_type, aliases):
    aliases = [(x['alias.flags'], x['alias.id']) for x in aliases if x['alias.type'] == 'mack']
    if mod_type == cid[0:2] and mod_type in ('RW', 'SF'):
        aliases.append((config.FLAG_ALIAS_PRIMARY, cid,))
    mack_nums = []
    for alias in aliases:
        mack_id = mbdata.get_mack_number(alias[1])
        if mack_id:
            mack_nums.append(((alias[0] & config.FLAG_ALIAS_PRIMARY) != 0,) + mack_id)
    mack_nums.sort(key=lambda x: x[2])
    # if aliases.flags == 2, put it first or bold it or something
    return [('<b>' if x[0] else '') + '-'.join([str(y) for y in x[1:] if y]).upper() + ('</b>' if x[0] else '')
            for x in mack_nums]


def fmt_var_pic(f, n):
    return (f'<span class="{"ok" if f == n else "no"}">{f}/{n}</span>') if n else '-'


def fmt_var_pics(found, needs):
    if isinstance(found, list) or isinstance(found, tuple):
        return [fmt_var_pic(*x) for x in zip(found, needs)]
    return fmt_var_pic(found, needs)


def calc_var_type(pif, var):
    return (
        'p' if any([var['manufacture'].startswith(x) for x in mbdata.other_plants]) else
        '2' if (any([x['category.flags'] & config.FLAG_MODEL_CODE_2 for x in var['vs']]) or
                mbdata.code2_cats & set(var['category'].split())) else
        'f' if var['var'].startswith('f') else
        'c' if any([x['variation_select.category'] == 'MB' for x in var['vs']]) else
        '1')


def calc_var_pics(pif, var):
    has = {k: int(len(var[v]) > 0) for k, v in text_attrs.items()}
    is_found = False
    if not var['picture_id']:
        is_found = int(bool(pif.ren.find_image_path(
            pdir=config.IMG_DIR_MAN, nobase=True,
            prefix=mbdata.IMG_SIZ_SMALL, suffix='jpg', fnames=var['mod_id'], vars=var['var'])))

    return (calc_var_type(pif, var), is_found, has)


def count_list_var_pics(pif, mod_id):
    vars = pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id))
    needs_c = needs_f = needs_a = needs_1 = needs_2 = needs_p = 0
    found_c = found_f = found_a = found_1 = found_2 = found_p = 0
    count = {k: 0 for k, v in text_attrs.items()}
    id_set = set()
    # nf = []
    for var in vars:
        ty_var, is_found, has = calc_var_pics(pif, var)

        for k in text_attrs:
            count[k] += has[k]
        if not var['picture_id']:
            # if not is_found:
            #     nf.append(var['var'])

            needs_a += 1
            found_a += is_found
            if ty_var == 'p':
                needs_p += 1
                found_p += is_found
            elif ty_var == 'f':
                needs_f += 1
                found_f += is_found
            elif ty_var == 'c':
                needs_c += 1
                found_c += is_found
            elif ty_var == '2':
                needs_2 += 1
                found_2 += is_found
            else:
                needs_1 += 1
                found_1 += is_found

        var_id = var['var']
        if var_id[0].isdigit():
            while not var_id[-1].isdigit():
                var_id = var_id[:-1]
            id_set.add(int(var_id))

    return ((found_a, found_c, found_1, found_2, found_f, found_p),
            (needs_a, needs_c, needs_1, needs_2, needs_f, needs_p),
            (len(vars), count),
            id_set)


def show_list_var_pics(pif, mod_id):
    founds, needs, cnts, id_set = count_list_var_pics(pif, mod_id)
    missing_ids = (
        ', '.join([str(x) for x in sorted(set(range(min(id_set), max(id_set) + 1)) - id_set)])) if id_set else ''
    return fmt_var_pics(founds, needs), cnts, missing_ids
