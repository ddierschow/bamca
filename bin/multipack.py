#!/usr/local/bin/python

import glob, os, re, sys
import basics
import config
import imglib
import mbdata
import models

# ---------------------------------------------------------------------

# columns, colspan, rowspan, picsize
# columns and picsize MUST NOT exceed 4!
pack_layouts = {
    '2h': [2, 2, 1, 4],
    '2v': [2, 1, 2, 2],
    '3h': [3, 3, 1, 4],
    '3v': [2, 1, 3, 2],
    '4h': [4, 4, 1, 4],
    '4v': [2, 1, 4, 2],
    '5h': [4, 3, 1, 3],
    '5l': [2, 1, 3, 3],
    '5s': [3, 2, 2, 3],
    '5v': [2, 1, 5, 2],
    '6h': [3, 3, 1, 4],
    '6s': [3, 2, 3, 3],
    '6v': [2, 1, 4, 2],
    '7s': [4, 3, 3, 3],
    '8h': [4, 4, 1, 4],
    '8s': [3, 2, 2, 3],
    '8v': [4, 3, 4, 2],
    '9h': [3, 3, 1, 4],
    'th': [4, 3, 2, 3],
    'tv': [3, 2, 4, 2],
    'wh': [4, 4, 1, 4],
}
pack_pic_size = 'tcmlh'

# ---- page list ------------------------------------------------------

def make_page_list(pif):
    pages = pif.dbh.fetch_pages("format_type='packs'")
    pages.sort(key=lambda x: x['page_info.title'])
    lsec = [pif.dbh.depref('section', x) for x in pif.dbh.fetch_sections({'page_id': 'packs'})]
    entries = list()
    lsec[0]['range'] = [{'entry': entries}]
    llineup = {'id': 'main', 'name': '', 'section': lsec}
    for page in pages:
        page = pif.dbh.depref('page_info', page)
        if not (page['flags'] & pif.dbh.FLAG_PAGE_INFO_NOT_RELEASED):
            txt = models.add_icons(pif, page['id'][6:], '', '') + '<br>' + page['title']
            entries.append({'text': pif.render.format_link('?page=' + page['id'][page['id'].find('.') + 1:], txt)})
    ostr = '<center>\n' + pif.render.format_matrix(llineup) + '<center>\n'
    ostr += pif.render.format_button_comment(pif)
    print ostr

# ---- pack list ------------------------------------------------------

def make_pack_list(pif, year=None, reg=None, lid=None):
    packs = pif.dbh.fetch_packs(page_id=pif.page_id)
    for pack in packs:
        pif.dbh.depref('base_id', pack)
        pif.dbh.depref('pack', pack)
        pack['name'] = pack['rawname'].replace(';', ' ')
    # order: product_code, id, rawname, layout, first_year, note, page_id, description, material, section_id, name, country, region, flags, model_type
    packs.sort(key=lambda x: (x[pif.form.get_str('order', 'name')], x['name'], x['first_year']))
    years = []
    regions = []

    print '<table class="packs fullpage"><tr>'
    if pif.is_allowed('m'):  # pragma: no cover
        print '<td valign="top">\n'
    else:
        print '<td width="70%" valign="top">\n'
    print '<table>\n'
    if pif.is_allowed('m'):  # pragma: no cover
        print '<tr><th>Pack ID</th><th>Name</th><th>Year</th><th>Product</th><th>Rg</th><th>Cy</th><th>Ly</th><th>Th</th><th>Pic</th><th>Mat</th><th>Models</th><th>Note</th><th>Related</th></tr>\n'
    else:
        print '<tr><th>Name</th><th>Year</th><th>Product Code</th><th>Region</th><th>Note</th><th></th></tr>\n'
    for pack in packs:
        if pack['first_year'] not in years:
            years.append(pack['first_year'])
        if pack['region'] and pack['region'] not in regions:
            regions.append(pack['region'])
        if year and year != pack['first_year']:
            continue
        if reg and reg != pack['region']:
            continue
        if lid and not pack['id'].startswith(lid):
            continue
        pack['thumb'] = pack['pic'] = pack['stars'] = ''
        if pif.is_allowed('m'):  # pragma: no cover
            pmodels = distill_models(pif, pack, pif.page_id)

            stars = ''
            keys = pmodels.keys()
            keys.sort()
            for mod in keys:
                if not pmodels[mod].get('id'):
                    stars += pif.render.format_image_art('stargreen.gif') + ' '
                elif not pmodels[mod].get('vs.var_id'):
                    stars += pif.render.format_image_art('starred.gif') + ' '
                elif pmodels[mod]['imgstr'].find('-') < 0:
                    stars += pif.render.format_image_art('stargray.gif') + ' '
                else:
                    stars += pif.render.format_image_art('star.gif') + ' '

            pack['stars'] = stars
	    pack['edlink'] = 'mass.cgi?verbose=1&type=pack&section_id=%s&pack=%s&num=' % (pack['section_id'], pack['id'])

        relateds = []  #pif.dbh.fetch_packs_related(pack['id'])
        pack['rel'] = [x['pack.id'] for x in relateds]
        pack['rel'].sort()
        pack['rel'] = ' '.join(pack['rel'])

	if pack['layout'] not in pack_layouts:
	    pack['layout'] = '<font color="red">%s</font>' % pack['layout']
        pack['page'] = pif.form.get_str('page')
        pack['regionname'] = mbdata.regions[pack['region']]
        if pif.is_allowed('m'):  # pragma: no cover
            print '<tr><td><a href="%(edlink)s">%(id)s</a></td><td><a href="?page=%(page)s&id=%(id)s">%(name)s</a></td><td>%(first_year)s</td><td>%(product_code)s</td><td>%(region)s</td><td>%(country)s</td><td>%(layout)s</td><td>%(thumb)s</td><td>%(pic)s</td><td>%(material)s</td><td>%(stars)s</td><td>%(note)s</td><td>%(rel)s</td></tr>\n' % pack
        else:
            print '<tr><td><a href="?page=%(page)s&id=%(id)s">%(name)s</a></td><td>%(first_year)s</td><td>%(product_code)s</td><td>%(regionname)s</td><td>%(note)s</td><td>%(rel)s</td></tr>\n' % pack
        sys.stdout.flush()
    print '</table></td>'
    if pif.is_allowed('m'):  # pragma: no cover
        print '<td valign="top">'
    else:
        print '<td width="30%" valign="top">'
    print '<form>'

    years.sort()
    regions.sort()
    print 'Filter by Year<br>'
    print ''.join(pif.render.format_radio('year', zip([''] + years, ['all'] + years), checked='', sep='<br>'))
    print '<p>'
    print 'Filter by Region<br>'
    print ''.join(pif.render.format_radio('region', zip([''] + regions, ['all'] + [mbdata.regions[x] for x in regions]), checked='', sep='<br>'))
    print '<p>'
#    print pif.render.format_select('lid', calc_pack_select(pif, packs))
    print '<p>'
    print pif.render.format_button_input()
    print pif.render.format_button("add", 'mass.cgi?type=pack&id=%s' % pif.form.get_str('page', '5packs'))
    print '<input type="hidden" name="page" value="%s">' % pif.form.get_str('page')
    print '</form>'
    print '</td></tr></table>\n'
    print pif.render.format_button_comment(pif)

# ---- single pack ----------------------------------------------------

def do_single_pack(pif, pack):
    if not pack:
        return "That pack doesn't seem to exist.", ""
    id = pack['pack.id']
    relateds = pif.dbh.fetch_packs_related(id)

    tcomments = set()
    for key in pack.keys():
        pack[key[key.find('.') + 1:]] = pack[key]
    pack['name'] = pack['rawname'].replace(';', ' ')

    if pack['layout'].isdigit():
	layout = [int(x) for x in pack['layout']]
    else:
	layout = pack_layouts.get(pack['layout'], [4, 4, 1, 4])
    if len(layout) == 2:
	layout[3] = 1
    if len(layout) == 3:
	layout[4] = 4 - (layout[0] - layout[1])
    lsec = {}
    lsec['columns'] = layout[0]
    lsec['anchor'] = pack['id']
    pif.render.comment('pack:', pack)
    entries = [{'text': show_pack(pif, pack, pack_pic_size[layout[3]]), 'display_id': '0', 'colspan': layout[1], 'rowspan': layout[2]}]

    pmodels = distill_models(pif, pack, pif.page_id)
    keys = pmodels.keys()
    keys.sort()
    for mod in keys:
        pif.render.comment("do_single_pack mod", pmodels[mod])

        if not pmodels[mod].get('id'):
            pmodels[mod]['no_casting'] = 1
            tcomments.add('m')
        else:
            if pmodels[mod]['imgstr'].find('-') < 0:
                tcomments.add('i')
            if not pmodels[mod].get('vs.var_id'):
                pmodels[mod]['no_variation'] = 1
                tcomments.add('v')

        entries.append({'text': show_pack_model(pif, pmodels[mod]), 'display_id': 1})
        #pstr += edit_model(pif, pmodels[mod])
    lsec['range'] = [{'entry': entries}]

    lsec['id'] = ''

    llineup = {}
    llineup['section'] = []
    llineup['tail'] = ['']
    llineup['section'].append(lsec)
    llineup['id'] = ''

    # displayer

    # left bar
    content = ''
    if pif.is_allowed('a'):  # pragma: no cover
        #content += str(pack['page_id']) + '/' + str(pack['id'])
	content += '<br><center>'
        content += '<p><b><a href="%s">Base ID</a></b><br>\n' % pif.dbh.get_editor_link('base_id', {'id': id})
        content += '<b><a href="%s">Pack</a></b><br>\n' % pif.dbh.get_editor_link('pack', {'id': id})
        content += '<b><a href="traverse.cgi?d=%s">Library</a></b><br>\n' % config.IMG_DIR_PACK
        content += '<b><a href="mass.cgi?verbose=1&type=pack&section_id=%s&pack=%s&num=">Edit</a></b><br>\n' % (pack['section_id'], pack['id'])
        content += '<b><a href="imawidget.cgi?d=./%s&f=%s.jpg">Edit Pic</a></b>\n' % (pif.render.pic_dir, pack['id'])
        content += '</center>\n'

    ostr = '<table class="fullpage"><tr>\n'
    ostr += models.add_left_bar(pif, pif.page_name, id, '', 4, content)

    # top bar
    ostr += models.add_banner(pif, pack['name'], pack['note'])

    # our feature presentation
    ostr += '<tr><td>\n'
    ostr += pif.render.format_matrix(llineup)
    ostr += '</td></tr>\n'

    # oh, just one more thing
    ostr += '<tr><td>\n'
    if relateds:
        ostr += '<h3>Related Packs</h3>\n<ul>\n'
        for related in relateds:
            ostr += '<li>'
            ostr += pif.render.format_link("?page=" + pif.form.get_str('page') + "&id=" + related['pack.id'], related['base_id.rawname'])
            if related['pack.product_code']:
                ostr += ' - (' + related['pack.product_code'] + ')'
            if related['pack.region']:
                ostr += ' - ' + mbdata.regions[related['pack.region']]
            if related['pack.country']:
                ostr += ' - Made in ' + mbdata.get_country(related['pack.country'])
            if related['pack.material']:
                ostr += ' - ' + mbdata.materials.get(related['pack.material'], '')
            if related['base_id.description']:
                ostr += ' - ' + related['base_id.description']
        ostr += '</ul>\n'
    ostr += '</td></tr>\n'

    # bottom bar
    ostr += '<tr><td class="bottombar">\n'
    ostr += pif.render.format_button_comment(pif, 'd=%s' % pif.form.get_str('id'))
    for comment in tcomments:
        ostr += mbdata.comment_designation[comment] + '<br>'
    ostr += '</td></tr></table>\n'
    #pstr += pif.render.format_table_end()
    return ostr#, pstr


def distill_models(pif, pack, page_id):
    model_list = pif.dbh.fetch_pack_models(pack_id=pack['id'], page_id=page_id)
    pack['pic'] = ''
    #for pic in glob.glob(os.path.join(config.IMG_DIR_PACK, '?_' + pack['id'] + '.jpg')):
    pic = pif.render.find_image_path(pack['id'], pdir=config.IMG_DIR_PACK, largest=mbdata.IMG_SIZ_HUGE)
    pack['pic'] += pif.render.format_image_art(imglib.image_star(pic))
    linmod = pif.dbh.fetch_lineup_model(where="mod_id='%s'" % pack['id'])
    pack['thumb'] = pif.render.format_image_art('box-sm-x.gif' if linmod else 'box-sm.gif')
    if pif.render.find_image_file(pack['id'], pdir=config.IMG_DIR_MAN, prefix=mbdata.IMG_SIZ_SMALL):
        pack['thumb'] += pif.render.format_image_art('starblack.gif')
    pmodels = {}

    for mod in [x for x in model_list if x['pack.id'] == pack['id']]:
        #print mod, '<br>'
        mod = pif.dbh.modify_man_item(mod)
        sub_ids = [None, '', pack['id'], pack['id'] + '.' + str(mod['pack_model.display_order'])]
        if mod['vs.sub_id'] in sub_ids:
            mod['imgl'] = [mbdata.IMG_SIZ_SMALL + '_' + mod['id'], mod['id'], mod['pack_model.mod_id']]
            for s in mod['descs']:
                if s.startswith('same as '):
                    mod['imgl'].extend([mbdata.IMG_SIZ_SMALL + '_' + s[8:], s[8:]])
            if not mod.get('vs.ref_id'):
                mod['vs.ref_id'] = ''
            if not mod.get('vs.sub_id'):
                mod['vs.sub_id'] = ''
            mod['pdir'] = pif.render.pic_dir
	    if mod['pack_model.mod_id'] != 'unknown':
		mod['href'] = "single.cgi?id=%(pack_model.mod_id)s&dir=%(pdir)s&pic=%(pack_model.pack_id)s&ref=%(vs.ref_id)s&sub=%(vs.sub_id)s" % mod
            #'<a href="single.cgi?dir=%(dir)s&pic=%(link)s&ref=%(vs.ref_id)s&id=%(mod_id)s">' % ent
            #'pack_model.pack_id': 'car02',
        #    if mod['pack_model.var'] and mod['imgl']:  # still not perfect
        #       mod['href'] = mod['href'] + '&pic=' + mod['imgl'][mod['imgl'].rfind('/') + 1:-2]
            mod['vars'] = []
            mod['pics'] = []
            if not mod['pack_model.display_order'] in pmodels:
                pmodels[mod['pack_model.display_order']] = mod
            if mod['v.picture_id']:
                pmodels[mod['pack_model.display_order']]['pics'].append(mod['v.picture_id'])
            else:
                pmodels[mod['pack_model.display_order']]['pics'].append(mod['vs.var_id'])
            if mod.get('vs.var_id'):
                pmodels[mod['pack_model.display_order']]['vars'].append(mod['vs.var_id'])
    for dispo in pmodels:
        pmodels[dispo]['imgstr'] = pif.render.format_image_required(pmodels[dispo]['imgl'], pdir=config.IMG_DIR_MAN, prefix=mbdata.IMG_SIZ_SMALL, vars=pmodels[dispo].get('pics'))
    return pmodels


#'columns': ['id', 'page_id', 'section_id', 'name', 'first_year', 'region', 'layout', 'product_code', 'material', 'country'],
def show_pack(pif, pack, picsize):
    ostr = pif.render.format_image_required(pack['id'], largest=picsize)
    if pif.is_allowed('a'):  # pragma: no cover
        ostr = '<a href="upload.cgi?d=./%s&n=%s">%s</a>' % (pif.render.pic_dir, pack['id'], ostr)
    else:
        ostr = '<a href="upload.cgi">%s</a>' % (ostr)
    pack['country'] = mbdata.get_country(pack['country'])
    pack['material'] = mbdata.materials.get(pack['material'], '')
    if pack['product_code']:
        ostr += '<br>' + pack['product_code']
    if pack['region']:
        ostr += '<br>' + mbdata.regions[pack['region']]
    ostr += '<p>'
    if pack['first_year']:
        ostr += '<b>%(first_year)s</b><br>' % pack
    dets = filter(None, [pack['country'], pack['material']])
    ostr += ' - '.join(dets)
    return ostr


#mdict: descriptions href imgstr name no_casting not_made number pdir picture_only product subname
#def add_model_table_product_link(pif, mdict):

def show_pack_model(pif, mdict):
    pif.render.comment("show_pack_model", mdict)

    mdict['number'] = ''
    mdict['descriptions'] = []
    if mdict['v.text_description']:
        mdict['descriptions'] = [mdict['v.text_description']]  # fix this
    mdict['product'] = ''
    if mdict['imgstr'].find('-') < 0:
        mdict['no_specific_image'] = 1

    desclist = list()
    for var in mdict.get('descriptions', []):
	if var and var not in desclist:
	    desclist.append(var)
    mdict['descriptions'] = desclist

    if not mdict.get('disp_format') or not mdict.get('shown_id'):
        mdict['displayed_id'] = '&nbsp;'
    else:
        mdict['displayed_id'] = mdict['disp_format'] % (mdict['shown_id'])

    return models.add_model_table_product_link(pif, mdict)


def edit_model(pif, mdict):
    ostr = pif.render.format_row_start()
    ostr += '<input type="hidden" name="pm.id.%s" value="%s">\n' % (mdict['pack_model.id'], mdict['pack_model.id'])
    ostr += '<input type="hidden" name="pm.pack_id.%s" value="%s">\n' % (mdict['pack_model.id'], mdict['pack_model.pack_id'])
    ostr += pif.render.format_cell(0, 'mod ' + pif.render.format_text_input("pm.mod_id.%s" % mdict['pack_model.id'], 8, 8, value=mdict['pack_model.mod_id']))
    ostr += pif.render.format_cell(0, 'var ' + pif.render.format_text_input("pm.var_id.%s" % mdict['pack_model.id'], 20, 20, value='/'.join(mdict['vars'])) + ' (' + str(mdict['pack_model.var_id']) + ')')
    ostr += pif.render.format_cell(0, 'disp ' + pif.render.format_text_input("pm.display_order.%s" % mdict['pack_model.id'], 2, 2, value=mdict['pack_model.display_order']))
    ostr += pif.render.format_row_end()
    return ostr

# ---- main -----------------------------------------------------------

@basics.web_page
def do_page(pif):
    pif.render.print_html()
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('packs.cgi', 'Multi-Model Packs')
    #pif.form.set_val('id', pif.form.get_list('id')[0])  # with no id this blows
#    if isinstance(pif.form.get('id'), list):
#       pif.form['id'] = pif.form.get_str('id')[0]
    if pif.form.has('id'):
        pif.form.set_val('id', pif.form.get_list('id')[0])  # with no id this blows
    year = pif.form.get_str('year')
    reg = pif.form.get_str('region')
    pid = pif.form.get_str('id')
    lid = pif.form.get_str('lid')
    pack = dict()
    if pid:
        packs = pif.dbh.fetch_pack(pid)
        if packs:
            pack = packs[0]
            pif.render.hierarchy_append('', pack['base_id.rawname'])
    print pif.render.format_head()
    if pid:
        print do_single_pack(pif, pack)
    elif pif.form.has('page'):
        make_pack_list(pif, year, reg, lid)
    else:
        make_page_list(pif)
    print pif.render.format_tail()

# ---------------------------------------------------------------------

if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
