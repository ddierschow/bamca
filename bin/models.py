#!/usr/local/bin/python

import config
import mbdata
import useful


arts = {
	'Rolamatics' : 'rola-matics-sm.gif',
	'Choppers' : 'choppers-sm.gif',
	'Real Talkin' : 'realtalkin-sm.gif',
	'D.A.R.E.' : 'dare-sm.gif',
	'Caterpillar' : 'caterpillar-sm.gif',
}
flago = None



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
def AddModelTablePicLink(pif, mdict, flago=flago):
    # input mdict:  id, (picture_id), made, country, link, linkid, name, descs, made, unlicensed, first_year, (type)
    pif.render.Comment('AddModelTablePicLink', mdict)
    if not flago:
	flago = {}
    #img = ['s_' + mdict['id']]
    img = [mdict['id']]
    if mdict.get('picture_id'):
	#img = ['s_' + mdict['picture_id']]
	img = [mdict['picture_id']]
    for s in mdict['descs']:
	if s.startswith('same as '):
	    #img.append('s_' + s[8:].lower())
	    img.append(s[8:].lower())
    mdict['img'] = pif.render.FormatImageRequired(img, None, made=mdict['made'], prefix=mdict.get('prefix', 's'))
    mdict['flag'] = ''
    if mdict.get('country') in flago:
	mdict['flag'] = pif.render.FormatImageFlag(mdict['country'], flago[mdict['country']], also={'align':'right'})
    elif mdict['unlicensed'] == '-':
	mdict['flag'] = pif.render.FormatImageArt('mbx.gif')
    if mdict.get('link'):
	mdict['lname'] = '<a href="%(link)s=%(linkid)s">%(img)s<br><b>%(name)s</b></a>' % mdict
    else:
	mdict['lname'] = '%(img)s<br><b>%(name)s</b>' % mdict
    mdict['desclist'] = ''
    if not mdict.get('nodesc'):
	for s in mdict['descs']:
	    if s in arts:
		mdict['desclist'] += "   <br>\n" + pif.render.FormatImageArt(arts[s])
	    elif s:
		mdict['desclist'] += "   <br><i>"+s+"</i>\n"
    if mdict.get('prefix') == 't':
	return mod_tab_thumb_pat % mdict
    return mod_tab_pic_lnk_pat % mdict


def GenerateModelTablePicLink(pif, mdict, mlist):
    for mod_id in mlist:
	yield {'text' : AddModelTablePicLink(pif, mdict[mod_id])}


#mdict: descriptions href imgstr name no_casting not_made number pdir picture_only product subname
def AddModelTableProductLink(pif, mdict):
    pif.render.Comment('AddModelTableProductLink', mdict)

    ostr = ''
    if mdict.get('anchor'):
	ostr += '<a name="%s"></a>' % mdict['anchor']

#    if pif.form.get('large'):
#	ostr += pif.render.FormatImageOptional(mdict['product'], suffix='jpg', pdir=mdict['pdir'], also={'class':'largepic'})
    ostr += '<center><table width=100%><tr><td width=40%>'
    if mdict.get('no_casting'):
	ostr += pif.render.FormatImageArt('stargreen.gif', also={'align':'left'})
    elif not mdict.get('picture_only'):
	if mdict.get('no_specific_image'):
	    ostr += pif.render.FormatImageArt('star.gif', also={'align':'left'})
	#if len(mdict['descriptions']) < 1:
	if mdict.get('no_variation'):
	    ostr += pif.render.FormatImageArt('starred.gif', also={'align':'left'})
    ostr += '</td><td width=20% style="text-align: center;">'
    if not mdict.get('disp_format') or not mdict.get('shown_id'):
	ostr += '&nbsp;'
    else:
	ostr += mdict['disp_format'] % (mdict['shown_id'])
    ostr += '</td><td width=40%>'
    if mdict.get('not_made'):
	ostr += pif.render.FormatImageArt('no.gif', also={'align':'right'})
    if pif.IsAllowed('a') and mdict.get('is_reused_product_picture'): # pragma: no cover
	ostr += pif.render.FormatImageArt('staryellow.gif', also={'align':'right'})
    if mdict.get('is_product_picture'):
	ostr += pif.render.FormatImageArt('camera.gif', also={'align':'right'})
    ostr += '</td></tr></table>\n'

    mstr = '<table><tr><td class="spicture"><center>%s</center></td></tr></table>\n' % (mdict['imgstr'])
    mstr += '<span class="modelname">' + mdict['name'] + '</span>'
    if mdict.get('href'):
	mstr = '<a href="%(href)s">\n' % mdict + mstr + '</a>'
    ostr += mstr
    if mdict.get('subname'):
	ostr += "<br>" + "<br>".join(mdict['subname'].split(';'))
    desclist = []
    for var in mdict.get('descriptions', []):
	if var and var not in desclist:
	    desclist.append(var)
    if desclist:
	ostr += '<table class="vartable">'
	for var in desclist:
	    ostr += '<tr><td class="varentry">%s</td></tr>' % var
	ostr += "</table>"
    ostr += "</center>"
    return ostr


# lineup, mannum
# shows scale, flag, pic, model name, description, with link to single.
mod_txt_lin_pat = '''%(long_id)s|%(name)s|%(desc)s    
'''
def AddModelTextLine(pif, mdict):
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
def AddModelLink(pif, mdict):
    ostr = '   <center>%(id)s<br><a href="single.cgi?id=%(man_id)s">%(imgstr)s</a><br>' % mdict
    if mdict.get('is_new', 0):
	ostr += pif.render.FormatImageArt('new') + ' '
    ostr += '<b>%(name)s</b></center>' % mdict
    return ostr


# lineup, mannum
# shows scale, flag, pic, model name, description, with link to single.
mod_tab_lst_ent_pat = '''  <td>%(box_sm)s</td>
  <td><center>%(id)s</center></td>
  <td>%(first_year)s</td>
  <td>%(lname)s</td>
'''
def AddModelTableListEntry(pif, mdict):
    # input mdict:  id, (picture_id), made, country, link, linkid, name, descs, made, unlicensed, scale, (type)
    mdict['lname'] = mdict['shortname']
    if mdict.get('link'):
	mdict['lname'] = '<a href="%(link)s=%(linkid)s">%(lname)s</a>' % mdict
    mdict['box_sm'] = pif.render.FormatImageArt('box-sm.gif')

    return mod_tab_lst_ent_pat % mdict


def AddModelPicLinkShort(pif, id):
    ostr = '<b>%s</b><br>' % id
    ostr += '<a href="single.cgi?id=%s">' % id
    ostr += pif.render.FormatImageRequired([id], prefix='s_', pdir=config.imgdir175) + '</a>'
    return ostr


def AddIcons(pif, type_id, base_id, vehicle_type):
    icon_list = []
    if type_id:
	icon = pif.render.FormatImageArt(type_id, also={'class':'centered'})
	if icon != '&nbsp;':
	    icon_list.append(icon)
    if base_id:
	icon = pif.render.FormatImageOptional(base_id, None, prefix='i_', suffix='gif', pdir=config.imgdir175 + '/icon', also={'class':'centered'})
	if icon != '&nbsp;':
	    icon_list.append(icon)
    for vtype in vehicle_type:
	if vtype in mbdata.model_icons:
	    icon_list.append(pif.render.FormatImageArt(mbdata.model_icons[vtype]))
    ostr = '<p>' + '<p><p>'.join(icon_list)
    return ostr


def AddLeftBar(pif, type_id=None, base_id=None, vehicle_type='', rowspan=4, content=''):
    # left bar
    ostr = '<td rowspan=%d class="leftbar bamcamark"><div class="leftbarcontent">' % rowspan
    if base_id:
	ostr += AddIcons(pif, type_id, base_id, vehicle_type)
    ostr += '<center>\n'
    ostr += content
    ostr += '</center>\n'
    ostr += '</div></td>\n'
    return ostr


if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
