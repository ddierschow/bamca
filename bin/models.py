#!/usr/local/bin/python

import config
import mbdata
import mflags
import useful


arts = {
        'Rolamatics': 'rola-matics-sm.gif',
        'Choppers': 'choppers-sm.gif',
        'Real Talkin': 'realtalkin-sm.gif',
        'D.A.R.E.': 'dare-sm.gif',
        'Caterpillar': 'caterpillar-sm.gif',
        'Auto Steer': 'autosteer-sm.gif',
}
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
    mdict['img'] = pif.render.format_image_required(img, None, made=mdict['made'], prefix=mdict.get('prefix', mbdata.IMG_SIZ_SMALL))
    mdict['flag'] = ''
    if mdict.get('country') in flago:
        mdict['flag'] = pif.render.format_image_flag(mdict['country'], flago[mdict['country']], also={'align': 'right'})
    elif mdict['unlicensed'] == '-':
        mdict['flag'] = pif.render.format_image_art('mbx.gif')
    pif.render.comment('FLAG?', mdict['id'], mdict['country'], mdict['flag'])
    if mdict.get('link'):
        mdict['lname'] = '<a href="%(link)s=%(linkid)s">%(img)s<br><b>%(name)s</b></a>' % mdict
    else:
        mdict['lname'] = '%(img)s<br><b>%(name)s</b>' % mdict
    mdict['desclist'] = ''
    if not mdict.get('nodesc'):
        for s in mdict['descs']:
            if s in arts:
                mdict['desclist'] += "   <br>\n" + pif.render.format_image_art(arts[s])
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
        ostr += pif.render.format_image_art('stargreen.gif')
    elif not mdict.get('picture_only'):
        if mdict.get('no_specific_image'):
            ostr += pif.render.format_image_art('star.gif')
        if mdict.get('no_variation'):
            ostr += pif.render.format_image_art('starred.gif')
    ostr += '</td><td class="modelnumber">'
    ostr += mdict['displayed_id']
    ostr += '</td><td class="modelicons">'
    if mdict.get('not_made'):
        ostr += pif.render.format_image_art('no.gif')
    if mdict.get('is_reused_product_picture'):  # pragma: no cover
        ostr += pif.render.format_image_art('staryellow.gif')
    if mdict.get('is_product_picture'):
        ostr += pif.render.format_image_art('camera.gif')
    ostr += '</td></tr></table>\n'

    if mdict.get('show_vars'):
	# imgstr descriptions
	for vdict in mdict['show_vars']:
	    if mdict.get('href'):
		ostr += '<a href="%(href)s">\n' % mdict
	    ostr += '<table><tr><td class="spicture"><center>%s</center></td></tr></table>\n' % (vdict['imgstr'])
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
	ostr += '<table><tr><td class="spicture"><center>%s</center></td></tr></table>\n' % (mdict['imgstr'])
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


# id, man_id, imgstr, is_new, name
def add_model_link(pif, mdict):
    ostr = '   <center>%(id)s<br><a href="single.cgi?id=%(man_id)s">%(imgstr)s</a><br>' % mdict
    if mdict.get('is_new', 0):
        ostr += pif.render.format_image_art('new') + ' '
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
	mdict['box_sm'] = pif.render.format_image_art('box-sm.gif')
    return mdict


def add_model_table_list_entry(pif, mdict):
    mdict = add_model_table_list_entry_dict(pif, mdict)
    return mod_tab_lst_ent_pat % mdict


def add_model_pic_link_short(pif, id):
    ostr = '<center><b>%s</b><br>' % id
    ostr += '<a href="single.cgi?id=%s">' % id
    ostr += pif.render.format_image_required([id], prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_MAN) + '</a></center>'
    return ostr


def add_icons(pif, type_id, base_id, vehicle_type):
    icon_list = []
    if type_id:
        icon = pif.render.format_image_art(type_id, also={'class': 'centered'})
        if icon != '&nbsp;':
            icon_list.append(icon)
    if base_id:
        icon = pif.render.format_image_optional(base_id, None, prefix='i_', suffix='gif', pdir=config.IMG_DIR_ICON, also={'class': 'centered'})
        if icon != '&nbsp;':
            icon_list.append(icon)
    for vtype in vehicle_type:
        if vtype in mbdata.model_icons:
            icon_list.append(pif.render.format_image_art(mbdata.model_icons[vtype]))
    ostr = '<p>' + '<p><p>'.join(icon_list)
    return ostr


def add_left_bar(pif, type_id=None, base_id=None, vehicle_type='', rowspan=4, content=''):
    # left bar
    ostr = '<td rowspan="%d" class="leftbar bamcamark"><div class="leftbarcontent">\n<p>\n' % rowspan
    if base_id:
        ostr += add_icons(pif, type_id, base_id, vehicle_type) + '\n<p>'
    ostr += content
    ostr += '\n</div></td>\n'
    return ostr


def add_banner(pif, title, note=''):
    # title banner
    ostr = '<td class="titlebar">\n'
    ostr += '%s\n' % title
    if note:
        ostr += '<br><span style="font-size: smaller;">%s</span>' % note
    ostr += '</td></tr>\n'
    return ostr


def show_adds(pif, mod_id, var_id=''):
    mod_adds = [
        ["b_", "Sample Baseplate%(s)s", "<p>"],
        ["d_", "Detail%(s)s", " "],
        ["i_", "Interior%(s)s", "<p>"],
        ["p_", "Prototype%(s)s or Preproduction Model%(s)s", "<p>"],
        ["r_", "Real Vehicle Example%(s)s", "<p>"],
        ["a_", "Customization%(s)s", "<p>"],
        ["f_", "Advertisement%(s)s", "<p>"],
        ["e_", "Error Model%(s)s", "<p>"],
    ]
    var_adds = [
        ["b_", "Baseplate%(s)s", "<p>"],
        ["d_", "Detail%(s)s", " "],
        ["i_", "Interior%(s)s", "<p>"],
    ]

    attribute_pictures = pif.dbh.fetch_attribute_pictures(mod_id)
    attribute_pictures = dict([
        (x['attribute_picture.attr_type'].lower() + '_' + x['attribute_picture.mod_id'].lower() + '-' + x['attribute_picture.picture_id'] + '.', x) for x in attribute_pictures if x['attribute_picture.picture_id']])

    img_id = (mod_id + ('-' + var_id if var_id else '')).lower()
    pdir = config.IMG_DIR_VAR if var_id else config.IMG_DIR_ADD
    adds = var_adds if var_id else mod_adds
    ostr = ''
    for add in adds:
        imgs = pif.render.format_image_list(img_id, wc='-*', prefix=add[0], pdir=pdir)
        if imgs:
            ostr += '<h3>%s</h3>\n' % add[1] % {'s': useful.plural(imgs)}
            for img in imgs:
                ostr += img + '<br>'
                for apic in attribute_pictures:
		    # This is terrible and I'm a terrible person but I don't want to think too much right now.
                    if apic in img and attribute_pictures[apic]['attribute_picture.description']:
			if attribute_pictures[apic]['attribute.title']:
			    ostr += "%(attribute.title)s: %(attribute_picture.description)s" % attribute_pictures[apic]
			else:
			    ostr += "%(attribute_picture.description)s" % attribute_pictures[apic]
                ostr += '<p>\n'
    return ostr


def add_model_thumb_pic_link(pif, mdict):
    ostr = '<table><tr><td class="image">'
    ostr += pif.render.format_image_required([mdict['id']], prefix=mbdata.IMG_SIZ_TINY, pdir=config.IMG_DIR_MAN)
    ostr += '</td>\n<td class="text">'
    if mdict['id']:
	ostr += '<span class="modelname">'
	ostr += pif.render.format_link('single.cgi?id=%s' % mdict['id'], mdict['id'] + ': ' + mdict['name'])
	ostr += '</span><br>\n'
    ostr += '<span class="info">See: %s</span>' % mdict['img']
    ostr += '</td></tr></table>\n'
    return ostr


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pic/gfx/tested.gif"></body></html>'''
