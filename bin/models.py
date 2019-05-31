#!/usr/local/bin/python

import config
import mbdata
import mflags
import useful


flago = mflags.FlagList()


# lineup, mannum
# shows first_year, flag, pic, model name, description, with link to single.
mod_tab_pic_lnk_pat = '''
  <center>
   <table class="entry">
    <tr><td></td><td width=32><i><font size=-1>%(first_year)s</font></i></td>
    <td width=136><center><font face="Courier">%(id)s</font></center></td>
    <td width=32>%(flag)s</td><td></td></tr>
    <tr><td colspan=5><center>
     %(lname)s
     %(desclist)s    </center></td></tr>
   </table>
  </center>
'''
mod_tab_thumb_pat = '''
  <center>
   <table class="entry">
    <tr><td></td>
    <td ><center><font face="Courier">%(id)s</font></center></td>
    </tr>
    <tr><td colspan=5><center>
     %(lname)s
     </center></td></tr>
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
    pif.render.comment('add_model_table_pic_link', mdict)
    if not flago:
        flago = {}
    img = [mdict['id']]
    if mdict.get('picture_id'):
        img = [mdict['picture_id']]
    for s in mdict['descs']:
        if s.startswith('same as '):
            img.append(s[8:].lower())
    img_size = mdict.get('prefix', mbdata.IMG_SIZ_LARGE if pif.form.get_bool('large') else mbdata.IMG_SIZ_SMALL)
    mdict['img'] = pif.render.format_image_required(img, made=mdict['made'], prefix=img_size)
    mdict['flag'] = ''
    if mdict.get('country') in flago:
        mdict['flag'] = pif.render.format_image_flag(mdict['country'], flago[mdict['country']], also={'align': 'right'})
    elif mdict['unlicensed'] == '-':
        mdict['flag'] = pif.render.format_image_art('mbx.gif')
    pif.render.comment('FLAG?', mdict.get('id'), mdict.get('country'), mdict.get('flag'))
    if mdict.get('link'):
        mdict['lname'] = '<a href="%(link)s=%(linkid)s">%(img)s<br><b>%(name)s</b></a>' % mdict
    else:
        mdict['lname'] = '%(img)s<br><b>%(name)s</b>' % mdict
    mdict['desclist'] = ''
    if not mdict.get('nodesc'):
        for s in mdict['descs']:
            if s in mbdata.arts:
                mdict['desclist'] += "   <br>\n" + pif.render.format_image_icon('c_' + mbdata.arts[s])
            elif s:
                mdict['desclist'] += "   <br><i>"+s+"</i>\n"
    return mdict


def generate_model_table_pic_link_dict(pif, mdict, mlist):
    for mod_id in mlist:
        yield add_model_table_pic_link_dict(pif, mdict[mod_id])


#mdict: descriptions href imgstr name no_casting not_made number pdir picture_only product subname additional
def add_model_table_product_link(pif, mdict):
    pif.render.comment('add_model_table_product_link', mdict)

    ostr = pif.render.fmt_anchor(mdict.get('anchor'))
    ostr += '<center><table class="modeltop"><tr><td class="modelstars">'
    if mdict.get('no_casting'):
        ostr += mbdata.comment_icon.get('m', '')
    elif not mdict.get('picture_only'):
        if mdict.get('no_specific_image'):
	    ostr += mbdata.comment_icon.get('i', '')
        if mdict.get('no_variation'):
	    ostr += mbdata.comment_icon.get('v', '')
    ostr += '</td><td class="modelnumber">'
    ostr += mdict['displayed_id']
    ostr += '</td><td class="modelicons">'
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
	    #ostr += '<table class="spicture"><tr><td class="spicture"><center>%s</center></td></tr></table>\n' % (vdict['imgstr'])
	    ostr += '<center>%s</center>\n' % (vdict['imgstr'])
	    ostr += '<span class="modelname">' + mdict['name'] + '</span>'
	    if mdict.get('href'):
		ostr += '</a>'
	    if mdict.get('subnames'):
		ostr += "<br>" + "<br>".join(mdict['subnames'])
	    if vdict.get('description'):
		ostr += '<table class="vartable">'
		ostr += '<tr><td class="varentry">%s</td></tr>' % vdict['description']
		ostr += "</table>"
	    ostr += "</center>"
    else:
	if mdict.get('href'):
	    ostr += '<a href="%(href)s">\n' % mdict
	#ostr += '<table class="spicture"><tr><td class="spicture"><center>%s</center></td></tr></table>\n' % (mdict['imgstr'])
	ostr += '<center>%s</center>\n' % (mdict['imgstr'])
	ostr += '<span class="modelname">' + mdict['name'] + '</span>'
	if mdict.get('href'):
	    ostr += '</a>'
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
	mdict['box_sm'] = '<i class="far fa-square"></i>'
    return mdict


def add_model_table_list_entry(pif, mdict):
    mdict = add_model_table_list_entry_dict(pif, mdict)
    return mod_tab_lst_ent_pat % mdict


def add_model_pic_link_short(pif, id):
    ostr = '<center><b id="%s">%s</b><br>' % (id, id)
    ostr += '<a href="single.cgi?id=%s">' % id
    ostr += pif.render.format_image_required([id], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_MAN) + '</a></center>'
    return ostr


def add_icons(pif, type_id, base_id, vehicle_type):
    icon_list = []
    if type_id:
        icon = pif.render.format_image_icon(type_id, also={'class': 'centered'})
        if icon != '&nbsp;':
            icon_list.append(icon)
    if base_id:
        icon = pif.render.format_image_optional(base_id, None, prefix='i_', suffix='gif', pdir=config.IMG_DIR_MAN_ICON, also={'class': 'centered'})
        if icon != '&nbsp;':
            icon_list.append(icon)
    for vtype in vehicle_type:
        if vtype in mbdata.model_icons:
            icon_list.append(pif.render.format_image_icon(mbdata.model_icons[vtype]))
    ostr = '<p>' + '<p><p>'.join(icon_list)
    return ostr


var_adds = [
    ["b_", "Base%(s)s", "<p>", 1],
    ["d_", "Detail%(s)s", " ", 1],
    ["i_", "Interior%(s)s", "<p>", 1],
]


def show_adds(pif, mod_id, var_id=''):
    photo_credits = {x['photo_credit.name']: x['photographer.name'] for x in pif.dbh.fetch_photo_credits(path='.' + config.IMG_DIR_ADD)}
    attribute_pictures = pif.dbh.fetch_attribute_pictures(mod_id)
    attribute_pictures = dict([
        (x['attribute_picture.attr_type'].lower() + '_' + x['attribute_picture.mod_id'].lower() + '-' + x['attribute_picture.picture_id'] + '.', x) for x in attribute_pictures if x['attribute_picture.picture_id']])

    img_id = (mod_id + ('-' + var_id if var_id else '')).lower()
    pdir = '.' + (config.IMG_DIR_VAR if var_id else config.IMG_DIR_ADD)
    adds = var_adds if var_id else mbdata.model_adds
    ostr = ''
    for add in adds:
        imgs = pif.render.find_image_list(img_id, wc='-*', prefix=add[0], pdir=pdir)
        if imgs:
            ostr += '<h3>%s</h3>\n' % add[1] % {'s': useful.plural(imgs)}
            for img in imgs:
		ostr += '<table><tr><td class="center">'
                ostr += pif.render.fmt_img_src(pdir + '/' + img) + '<br>'
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
    photo_credits = {x['photo_credit.name']: x['photographer.name'] for x in pif.dbh.fetch_photo_credits(path='.' + config.IMG_DIR_ADD)}
    attribute_pictures = pif.dbh.fetch_attribute_pictures(mod_id)
    attribute_pictures = dict([
        (x['attribute_picture.attr_type'].lower() + '_' + x['attribute_picture.mod_id'].lower() + '-' + x['attribute_picture.picture_id'] + '.', x) for x in attribute_pictures if x['attribute_picture.picture_id']])

    img_id = (mod_id + ('-' + var_id if var_id else '')).lower()
    pdir = '.' + (config.IMG_DIR_VAR if var_id else config.IMG_DIR_ADD)
    adds = var_adds if var_id else mbdata.model_adds
    outd = []
    for add in adds:
        imgs = pif.render.find_image_list(img_id, wc='-*', prefix=add[0], pdir=pdir)
        if imgs:
	    elem = {'title': add[1] % {'s': useful.plural(imgs)}, 'entry': [],
		    'columns': add[3]}
            for img in imgs:
		fn = img[:img.find('.')]
		ent = {'img': pif.render.fmt_img_src(pdir + '/' + img),
		       'credit': photo_credits.get(fn, '')}
                for apic in attribute_pictures:
		    # This is terrible and I'm a terrible person but I don't want to think too much right now.
                    if apic in img and attribute_pictures[apic]['attribute_picture.description']:
			if attribute_pictures[apic]['attribute.title']:
			    ent['desc'] = "%(attribute.title)s: %(attribute_picture.description)s" % attribute_pictures[apic]
			else:
			    ent['desc'] = "%(attribute_picture.description)s" % attribute_pictures[apic]
                elem['entry'].append(ent)
	    outd.append(elem)
    return outd


def add_model_thumb_pic_link(pif, mdict):
    ostr = '<table><tr><td class="image">'
    ostr += pif.render.format_image_required([mdict['id']], prefix=mbdata.IMG_SIZ_TINY, pdir=config.IMG_DIR_MAN)
    ostr += '</td>\n<td class="text">'
    if mdict['id']:
	ostr += '<span class="modelname">'
	ostr += pif.render.format_link('single.cgi?id=%s' % mdict['id'], mdict['id'] + ': ' + mdict['name'])
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
    img = pif.render.find_image_path([vdict['mod_id']], nobase=True, vars=pic_id, prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_MAN)
    vdict['img'] = pif.render.fmt_img_src(img) if img else pif.render.fmt_no_pic(True, mbdata.IMG_SIZ_SMALL)

    return '''
<a href="%(link)s">%(var)s<br>
<center><table class="spicture"><tr><td class="spicture">%(img)s</td></tr></table></center></a>
<table class="vartable">
<tr><td class="varentry"><i>%(text_description)s</i></td></tr>
</table>
''' % vdict


def make_page_list(pif, format_type, fmt_link):
    pif.render.set_button_comment(pif)
    secs = pif.dbh.fetch_sections_by_page_type(format_type)
    lsec = [x for x in secs if x.page_id == format_type][0]
    entries = list()
    lsec['range'] = [{'entry': entries}]
    llineup = {'id': 'main', 'name': '', 'section': [lsec]}
    for sec in secs:
	hidden = sec.flags & config.FLAG_PAGE_INFO_HIDDEN or sec.page_info.flags & config.FLAG_PAGE_INFO_HIDDEN
        if '.' in sec.page_id and (pif.render.is_beta or not hidden):
            entries.append({'text': ('<i>%s</i>' if hidden else '%s') % fmt_link(sec)})
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('packpages.html', llineup=llineup)
