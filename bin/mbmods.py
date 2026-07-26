#!/usr/local/bin/python

import config
import mbdata
import mflags
import models
import render
import useful


flago = mflags.FlagList()


format_attributes = ['format_description', 'format_body', 'format_interior', 'format_windows', 'format_base',
                     'format_wheels', 'format_with']
text_attrs = {'de': 'text_description', 'ba': 'text_base', 'bo': 'text_body', 'in': 'text_interior',
              'wh': 'text_wheels', 'wi': 'text_windows', 'wt': 'text_with', 'bt': 'text_text'}
text_fmts = {'de': 'format_description', 'ba': 'format_base', 'bo': 'format_body', 'in': 'format_interior',
             'wh': 'format_wheels', 'wi': 'format_windows', 'wt': 'format_with', 'bt': 'format_text'}
text_titles = {'de': 'Description', 'ba': 'Base', 'bo': 'Body', 'in': 'Interior',
               'wh': 'Wheels', 'wi': 'Windows', 'wt': 'With', 'bt': 'Base Text'}
text_short_titles = {'de': 'De', 'ba': 'Ba', 'bo': 'Bo', 'in': 'In', 'wh': 'Wh', 'wi': 'Wi', 'wt': 'W/', 'bt': 'BT'}
var_types = ['c', '1', '2', 'f', 'p']


def add_man_item_table_pic_link(pif, manitem, flago=flago):
    manitem = add_model_table_pic_link_man_item(pif, manitem, flago)
    if manitem.prefix == mbdata.IMG_SIZ_TINY:
        return (
            '\n  <center>\n   <table class="entry">\n    <tr>\n'
            f'     <td class="centerize modelname monospace">{manitem.id}</td>\n    </tr>\n'
            f'    <tr>\n     <td><center>{manitem.lname}</center></td>\n    </tr>\n   </table>\n  </center>\n')
    return (
        '\n  <center>\n   <table class="entry">\n    <tr>\n     <td></td>\n'
        f'     <td width="32px" class="smallish"><i>{manitem.first_year}</i></td>\n'
        f'     <td width="136px" class="centerize modelname monospace">{manitem.id}</td>\n'
        f'     <td width="32px">{manitem.flag}</td>\n     <td></td></tr>\n    <tr>\n'
        f'     <td colspan="5"><center>{manitem.lname} {manitem.desclist}</center></td>\n    </tr>\n'
        '   </table>\n  </center>\n')


# for templates


def add_model_table_pic_link_man_item(pif, manitem, flago=flago):
    # input manitem:  id, (picture_id), made, country, link, linkid, name, descs, made, unlicensed, first_year, (type)
    if not flago:
        flago = {}
    img = [manitem.id]
    if manitem.picture_id:
        img = [manitem.picture_id]
    for s in manitem.descs:
        if s.startswith('same as '):
            img.append(s[8:].lower())
    img_size = mbdata.IMG_SIZ_LARGE if pif.form.get_bool('large') else manitem.prefix
    manitem.img = pif.ren.format_image_required(img, made=manitem.made, largest=img_size)
    manitem.flag = ''
    if manitem.country in flago:
        manitem.flag = pif.ren.format_image_flag(manitem.country, flago[manitem.country], also={'align': 'right'})
    elif manitem.unlicensed == '-':
        manitem.flag = pif.ren.format_image_art('mbx.gif')
    # pif.ren.comment('FLAG?', manitem.id, manitem.country, manitem.flag)
    if manitem.link:
        manitem.lname = f'<a href="{manitem.link}={manitem.linkid}">{manitem.img}<br><b>{manitem.name}</b></a>'
    else:
        manitem.lname = f'{manitem.img}<br><b>{manitem.name}</b>'
    if manitem.subname:
        manitem.lname += '<br>' + manitem.subname
    manitem.desclist = ''
    # useful.write_comment(manitem.id, manitem.descs)
    if not manitem.nodesc:
        for s in manitem.descs:
            if s in mbdata.casting_arts:
                manitem.desclist += f"<br>{pif.ren.format_image_icon(mbdata.casting_arts[s] + '.gif')}"
            elif s:
                manitem.desclist += f"<br><i>{s}</i>\n"
    # manitem.shown_id = manitem.get('alias.id') or manitem.id']
    manitem.shown_id = manitem.id
    if pif.is_allowed('a'):
        manitem.modelicons = pif.ren.format_link(f'vars.cgi?edt=1&mod={manitem.id}', pif.ren.fmt_mini('gray', 'link'))
    return manitem


def generate_model_table_pic_link_man_item(pif, mdict, mlist):
    for mod_id in mlist:
        yield add_model_table_pic_link_man_item(pif, mdict[mod_id])


# mdict: descriptions href imgstr name no_casting not_made number pdir picture_only product subname additional
def add_man_item_table_product_link(pif, item):
    item.ldir = item.pdir.replace('pic', 'lib')
    ostr = pif.ren.fmt_anchor(item.anchor)
    ostr += '<center><table class="modeltop"><tr><td class="modelstars">'
    if item.no_casting:
        ostr += mbdata.comment_icon.get('m', '')
    elif not item.picture_only:
        if item.no_specific_image:
            ostr += mbdata.comment_icon.get('i', '')
        if item.no_variation:
            ostr += mbdata.comment_icon.get('v', '')
    ostr += f'</td><td class="modelnumber">{item.displayed_id}</td><td class="modelicons">'
    if pif.is_allowed('a'):
        # breaks packs
        if isinstance(item, models.LineItem):
            ref_link = pif.dbh.get_editor_link('lineup_model', year=item.year, mod_id=item.mod_id)
        elif isinstance(item, models.PackModelItem):
            ref_link = pif.dbh.get_editor_link('pack_model', id=item.id)
            ostr += pif.ren.format_link(f'vars.cgi?edt=1&mod={item.mod_id}', pif.ren.fmt_mini('gray', 'link'))
        else:
            ref_link = ''
        ostr += pif.ren.format_link(ref_link, pif.ren.fmt_edit('gray'))
        if hasattr(item, 'mod_id'):
            # fn = item.mod_id.replace('.', '_') + ('-' + item.sub_id if item.sub_id else '')
            # d={ldir}&n={pic}&c={pic}
            ostr += pif.ren.format_link(f'upload.cgi?d={item.ldir}&n={item.product}&c={item.product}',
                                        pif.ren.fmt_mini('gray', icon='upload'))
    if item.not_made:
        ostr += mbdata.comment_icon.get('n', '')
    if item.is_reused_product_picture:  # pragma: no cover
        ostr += mbdata.comment_icon.get('r', '')
    if item.is_product_picture:
        ostr += mbdata.comment_icon.get('c', '')
    ostr += '</td></tr></table>\n'

    if item.show_vars:
        # imgstr descriptions
        for vdict in item.show_vars:
            vstr = f'<center>{vdict["imgstr"]}</center>\n<span class="modelname">{item.name or item.subname}</span>'
            if item.href:
                vstr = f'<a href="{item.href}">\n{vstr}</a>\n'
            if item.subname and item.name:
                item.lname += f'<br>{item.subname}'
            if item.subnames:
                vstr += "<br>" + "<br>".join(item.subnames)
            if vdict.get('description'):
                vstr += f'<table class="vartable"><tr><td class="varentry">{vdict["description"]}</td></tr></table>\n'
            vstr += "</center>"
            ostr += vstr
    else:
        vstr = f'<center>{item.imgstr}</center>\n<span class="modelname">{item.name or item.subname}</span>'
        if item.href:
            vstr = f'<a href="{item.href}">\n{vstr}</a>\n'
        if item.subname and item.name:
            vstr += f'<br>{item.subname}'
        if item.subnames:
            vstr += "<br>" + "<br>".join(item.subnames)
        if item.descriptions:
            vstr += '<table class="vartable">'
            for var in item.descriptions:
                vstr += f'<tr><td class="varentry">{var}</td></tr>'
            vstr += "</table>"
        vstr += "</center>"
        ostr += vstr

    ostr += item.additional
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


def add_model_table_list_entry_dict(pif, mdict):
    if mdict:
        # input mdict:  id, (picture_id), made, country, link, linkid, name, descs, made, unlicensed, scale, (type)
        mdict['lname'] = mdict['shortname']
        if mdict.get('link'):
            mdict['lname'] = '<a href="%(link)s=%(linkid)s">%(lname)s</a>' % mdict
        mdict['box_sm'] = pif.ren.fmt_square(hollow=True)
    return mdict


def add_model_table_list_entry_man_item(pif, manitem):
    if manitem:
        # input manitem:  id, (picture_id), made, country, link, linkid, name, descs, made, unlicensed, scale, (type)
        manitem.lname = manitem.shortname
        if manitem.link:
            manitem.lname = f'<a href="{manitem.link}={manitem.linkid}">{manitem.lname}</a>'
        manitem.box_sm = pif.ren.fmt_square(hollow=True)
    return manitem


# lineup, mannum
# shows scale, flag, pic, model name, description, with link to single.
mod_tab_lst_ent_pat = '''  <td>%(box_sm)s</td>
  <td><center>%(id)s</center></td>
  <td>%(first_year)s</td>
  <td>%(lname)s</td>
'''


def add_model_table_list_entry(pif, mdict):
    mdict = add_model_table_list_entry_dict(pif, mdict)
    return mod_tab_lst_ent_pat % mdict


def add_man_item_table_list_entry(pif, manitem):
    manitem = add_model_table_list_entry_man_item(pif, manitem)
    # lineup, mannum
    # shows scale, flag, pic, model name, description, with link to single.
    return (
        f'  <td>{manitem.box_sm}</td>\n'
        f'  <td><center>{manitem.id}</center></td>\n'
        f'  <td>{manitem.first_year}</td>\n'
        f'  <td>{manitem.lname}</td>')


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
    # pdir = '.' + (config.IMG_DIR_VAR if var_id else config.IMG_DIR_ADD)
    pdir = '.' + config.IMG_DIR_ADD
    adds = mbdata.var_adds if var_id else mbdata.model_adds
    ostr = ''
    for add in adds:
        imgs = pif.ren.find_image_list(img_id, wc='-*', suffix='*', prefix=add[0], pdir=pdir)
        if imgs:
            ostr += f'<h3>{add[1]}{useful.plural(imgs)}</h3>\n'
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
            elem = {'title': add[1] + useful.plural(imgs), 'entry': [], 'columns': add[3]}
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


def add_man_item_thumb_pic_link(pif, manitem):
    img = manitem.img
    if isinstance(img, list):
        img = '<ul>%s</ul>' % ('\n'.join(['<li>' + x for x in img]))

    ostr = '<table><tr><td class="image">'
    ostr += pif.ren.format_image_required([manitem.id], prefix=mbdata.IMG_SIZ_TINY, pdir=config.IMG_DIR_MAN)
    ostr += '</td>\n<td class="text">'
    if manitem.id:
        ostr += '<span class="modelname">'
        ostr += pif.ren.format_link(f'single.cgi?id={manitem.id}', f'{manitem.id}: {manitem.name}')
        ostr += '</span><br>\n'
    ostr += f'<span class="info">See: {img}</span></td></tr></table>\n'
    return ostr


def add_var_item_pic_link(pif, varitem):
    varitem.link = f'vars.cgi?mod={varitem.mod_id}&var={varitem.var.upper()}'
    varitem.categories = ''
    img = pif.ren.find_image_path([varitem.mod_id], nobase=True, vars=varitem.picture_id, prefix=mbdata.IMG_SIZ_SMALL,
                                  pdir=config.IMG_DIR_MAN)
    varitem.img = pif.ren.fmt_img_src(img) if img else pif.ren.fmt_no_pic(True, mbdata.IMG_SIZ_SMALL)

    return f'''
<a href="{varitem.link}">{varitem.var}<br>
<center><table class="spicture"><tr><td class="spicture">{varitem.img}</td></tr></table></center></a>
<table class="vartable">
<tr><td class="varentry"><i>{varitem.text_description}</i></td></tr>
</table>
'''


def make_page_list(pif, format_type, fmt_link):
    pif.ren.set_button_comment(pif)
    secs = pif.dbh.fetch_sections_by_page_type(format_type)
    entries = list()
    for sec in secs:
        hidden = sec['flags'] & config.FLAG_PAGE_INFO_HIDDEN or sec['page_info.flags'] & config.FLAG_PAGE_INFO_HIDDEN
        dropped = hidden and (not (pif.ren.is_alpha or pif.ren.is_beta) or pif.ren.diff_run)
        if '.' in sec['page_id'] and not dropped:
            entries.append(render.Entry(text=('<i>%s</i>' if hidden else '%s') % fmt_link(sec)))
    lsec = render.Section(
        section=[x for x in secs if x['page_id'] == format_type][0],
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
        '  <center><table class="entry"><tr><td width="20%"></td><td width="60%">'
        f'<center><span class="monospace modelname">{mdict["v.mod_id"]}-{mdict["v.var"]}</span></td>'
        '<td width="20%"></td></tr>\n'
        f'   <tr><td colspan="3"><a href="{mdict["link"]}">{mdict["img"]}<br><b>{mdict["name"]}</b></a>\n')
    # ostr += "   <br><i>%(v.text_description)s</i>\n" % mdict
    ostr += '<table class="vartable">'
    ostr += '<tr><td class="varentry"><i>%s</i></td></tr>' % mdict['v.text_description']
    ostr += "</table>"
    ostr += "  </center></td></tr></table></center>\n"
    return ostr


def make_base_logos(pif, logo_type):
    l1 = l2 = ''
    for ch in logo_type:
        if ch in mbdata.base_logo_dict:
            l1 = ch
        elif ch in mbdata.base_logo_2_dict:
            l2 = ch
    return [
        pif.ren.format_image_icon(f'l_base-{l1}', mbdata.base_logo_dict.get(l1)) if l1 else '',
        pif.ren.format_image_icon(f'l_base-{l2}', mbdata.base_logo_2_dict.get(l2)) if l2 else '']


def add_man_item_sized_var_table_pic_link(pif, size, manitem, varitem):
    manitem.img = pif.ren.format_image_required(varitem.mod_id, largest=size, nobase=True, vars=varitem.picture_id)
    manitem.link = f'vars.cgi?mod={varitem.mod_id}&var={varitem.var}'
    c2 = pif.ren.format_image_icon("l_code2", also={'class': 'lefty'}) if varitem.variation_type == "2" else ""
    if size == mbdata.IMG_SIZ_SMALL or size == mbdata.IMG_SIZ_MEDIUM:
        ostr = (
            f'  <center><table class="entry"><tr><td width="20%">{c2}</td><td width="60%">'
            f'<center><span class="modelname monospace">{varitem.mod_id}-{varitem.var}</span></center></td>'
            '<td width="20%"></td></tr><tr><td colspan="3">\n'
            f'   <center><a href="{manitem.link}" class="modelname">{manitem.img}<br>{manitem.name}</a>\n'
            f'<table class="vartable"><tr><td class="varentry"><i>{varitem.text_description}</i></td></tr></table>'
            "  </center></td></tr></table></center>\n")
    elif size == mbdata.IMG_SIZ_LARGE:
        # render details
        def show_details():
            return [(t, varitem.get_attr(f'text_{d}')) for d, t in
                    [('base', 'Base'), ('body', 'Body'), ('interior', 'Interior'), ('wheels', 'Wheels'),
                     ('windows', 'Windows'), ('text', 'Base Text'), ('with', 'With')]] + [
                ('First Release', pif.ren.format_date(varitem.get_attr('date')))]

        base_logos = ' '.join(make_base_logos(pif, varitem.iattrs['logo_type']))

        ostr = (
            '  <table class="entry centered">'
            f' <tr><td class="width_l center"><a href="{manitem.link}">{manitem.img}</a></td>\n'
            '   <td class="width_m center toppy"><table width="100%"><tr>'
            f'  <td width="10%">{c2}</td><td class="modelname monospace centerize">'
            f'{varitem.mod_id}-{varitem.var}</td><td width="10%"></td></tr></table><p>\n'
            f'  <div class="width_m toppy center"><a href="{manitem.link}"><b>{manitem.name}</b></a></div><p>\n'
            f'<table class="vartable width_m"><tr><td class="varentry"><i>{varitem.text_description}</i></td></tr></table>'
            '<table class="inset width_m">\n' +
            ''.join([f'<tr><td class="textleft">{title}</td><td class="textleft">{value}</td></tr>\n'
                     for title, value in show_details() if value]) +
            f'</table>\n{base_logos}\n  </td></tr></table>\n')

    return ostr


def add_man_item_sized_table_pic_link(pif, size, manitem, flago=flago):
    manitem.prefix = size
    manitem = add_model_table_pic_link_man_item(pif, manitem, flago)
    idsize = mbdata.imagesizes[size][0] - 64
    if size == mbdata.IMG_SIZ_TINY:
        return (
            '\n  <center>\n   <table class="entry">\n    <tr>\n'
            f'     <td class="modelname monospace centerize">{manitem.id}</td>\n    </tr>\n'
            f'    <tr>\n     <td><center>{manitem.lname}</center></td>\n    </tr>\n   </table>\n  </center>\n')
    return (
        '\n  <center>\n   <table class="entry">\n    <tr>\n     <td></td>\n'
        f'     <td width="32px" class="smallish"><i>{manitem.first_year}</i></td>\n'
        f'     <td width="{idsize}px" class="modelname monospace centerize">{manitem.id}</td>\n'
        f'     <td width="32px">{manitem.flag}</td>\n     <td></td></tr>\n    <tr>\n'
        f'     <td colspan="5"><center>{manitem.lname} {manitem.desclist}</center></td>\n    </tr>\n'
        '   </table>\n  </center>\n')


def get_mack_numbers(pif, cid, mod_type, aliases):
    aliases = [(x['alias.flags'], x['alias.id']) for x in aliases if x['alias.type'] == 'mack']
    if mod_type == cid[0:2] and mod_type in ('RW', 'SF'):
        aliases.append((config.FLAG_ALIAS_PRIMARY, cid,))
    mack_nums = []
    for alias in aliases:
        mack_id = mbdata.get_mack_number(alias[1])
        if mack_id and mack_id[1]:
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
    if isinstance(found, dict):
        return [fmt_var_pic(found[x], needs[x]) for x in ['a'] + var_types]
    return fmt_var_pic(found, needs)


def calc_var_type(pif, varitem):
    if isinstance(varitem, dict):
        ty_var = ''
        if not varitem['picture_id']:
            if any([varitem['manufacture'].startswith(x) for x in mbdata.other_plants]):
                ty_var = 'p'
            elif (any([x['category.flags'] & config.FLAG_MODEL_CODE_2 for x in varitem['vs']]) or
                  mbdata.code2_cats & set(varitem['category'].split())):
                ty_var = '2'
            elif varitem['var'].startswith('f'):
                ty_var = 'f'
            elif any([x['category'] == 'MB' for x in varitem['vs']]):
                ty_var = 'c'
            else:
                ty_var = '1'
        return ty_var

    return (
        'p' if any([varitem.manufacture.startswith(x) for x in mbdata.other_plants]) else
        '2' if (any([x.vs_cat_flags & config.FLAG_MODEL_CODE_2 for x in varitem.vs]) or
                mbdata.code2_cats & set(varitem.category)) else
        'f' if varitem.var.startswith('f') else
        'c' if any([x.vs_cat == 'MB' for x in varitem.vs]) else
        '1')


def calc_var_pics(pif, var):
    has = {k: int(len(var.get_attr(v)) > 0) for k, v in text_attrs.items()}
    is_found = False
    if var.var == var.picture_id:
        is_found = int(bool(pif.ren.find_image_path(
            pdir=config.IMG_DIR_MAN, nobase=True,
            prefix=mbdata.IMG_SIZ_SMALL, suffix='jpg', fnames=var.mod_id, vars=var.var)))
    return (calc_var_type(pif, var), is_found, has)


def count_list_var_pics(pif, mod_id):
    vars = pif.dbh.make_var_items(pif.dbh.fetch_variations(mod_id))
#    for cr in pif.dbh.fetch_casting_relateds(mod_id=mod_id, section_id='single', flags=config.FLAG_CASTING_RELATED_SHARED):
#        vars.extend(pif.dbh.make_var_items(pif.dbh.fetch_variations(cr['casting_related.related_id'])))
    needs = {x: 0 for x in ['a'] + var_types}
    found = {x: 0 for x in ['a'] + var_types}
    count = {k: 0 for k, v in text_attrs.items()}
    id_set = set()
    for var in vars:
        ty_var, is_found, has = calc_var_pics(pif, var)

        for k in text_attrs:
            count[k] += has[k]
        if var.var == var.picture_id:
            needs['a'] += 1
            found['a'] += is_found
            needs[ty_var] += 1
            found[ty_var] += is_found

        var_id = var.var
        if var_id[0].isdigit():
            while not var_id[-1].isdigit():
                var_id = var_id[:-1]
            id_set.add(int(var_id))

    return (found, needs, (len(vars), count), id_set)


def show_list_var_pics(pif, mod_id):
    founds, needs, cnts, id_set = count_list_var_pics(pif, mod_id)
    missing_ids = (
        ', '.join([str(x) for x in sorted(set(range(min(id_set), max(id_set) + 1)) - id_set)])) if id_set else ''
    return fmt_var_pics(founds, needs), cnts, missing_ids


def make_make(pif, make):
    return {
        'image': (pif.ren.fmt_img(make['casting_make.make_id'], prefix='u', pdir=config.IMG_DIR_MAKE)
                  if make['casting_make.make_id'] else ''),
        'id': make['casting_make.make_id'],
        'name': 'Unlicensed' if make['casting_make.make_id'] == 'unl' else make.get('vehicle_make.name', ''),
        'company_name': make.get('vehicle_make.company_name', ''),
        'flags': (make.get('vehicle_make.flags') or 0) | (make.get('casting_make.flags') or 0),
        'link': 'makes.cgi?make=' + make['casting_make.make_id'],
    }


class ProductInfo(object):
    def __init__(self, pif):
        self.pic = pif.form.get_str('pic')
        self.pdir = pif.form.get_dir('dir')
        if not self.pdir.startswith('pic/') or '/' in self.pic:
            self.pdir = self.pic = ''
        self.ref = pif.form.get_id('ref')
        self.sec = pif.form.get_str('sec')
        self.ran = pif.form.get_str('ran')
        self.reg = (
            self.sec if self.sec else
            self.pic[4] if (self.ref.startswith('year') and len(self.pic) > 4 and self.pic[:4].isdigit()) else
            '')
        if self.reg.startswith('X'):
            self.reg = 'X.' + self.reg[1:]
        self.reg_list = mbdata.get_region_tree(self.reg) + ['']
        self.sec_list = mbdata.get_region_tree(self.sec) + ['']
        self.ref_type = (
            'LI' if self.ref.startswith('year.') else
            'SE' if self.ref.startswith('matrix.') else
            'MP' if self.ref.startswith('packs.') else
            '')

    def is_lineup_appearance(self, appear):
        return appear.page_id == self.ref and (appear.region in self.reg_list or self.reg_list == [''])

    def is_matrix_appearance(self, appear):
        return appear.page_id == self.ref

    def is_pack_appearance(self, appear):
        return appear.page_id == self.ref and appear.id == self.sec

    def get_prod_title(self, appear):
        prod_title = []
        if self.ref_type == 'LI':
            if self.is_lineup_appearance(appear):
                prod_title = [appear.year, mbdata.regions.get(appear.region, ''), f"#{appear.number}", appear.name]
        elif self.ref_type == 'SE':
            if self.is_matrix_appearance(appear):
                prod_title = [appear.page_info.title, appear.section.name, appear.name]
        elif self.ref_type == 'MP':
            if self.is_pack_appearance(appear):
                prod_title = [appear.section.name, appear.first_year, appear.rawname]
        return prod_title


def get_product_info(pif):
    return ProductInfo(pif)
