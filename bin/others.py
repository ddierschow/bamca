#!/usr/local/bin/python

import basics
import config
import mbdata
import models
import useful


def create_section(pif, attribute_type):
    def prep_mod(mod):
	mod = pif.dbh.modify_man_item(mod)
	mod['img'] = '/'.join(pif.render.find_image_file(mod['attribute_picture.mod_id'] + '-' + mod['attribute_picture.picture_id'], prefix=attribute_type, pdir=config.IMG_DIR_ADD))
	mod['img'] = pif.render.format_link('/' + mod['img'], txt=mod['attribute_picture.description'])
	return mod

    lsec = pif.dbh.depref('section', pif.dbh.fetch_sections({'page_id': pif.page_id})[0])
    lsec['range'] = [{'entry':
	[{'text': models.add_model_thumb_pic_link(pif, prep_mod(mod))} for mod in pif.dbh.fetch_attribute_pictures_by_type(attribute_type)]}]
    return lsec


def errors(pif):
    pif.render.print_html()
    pif.render.hierarchy_append('/', 'Home')
    #pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/errors.cgi', 'Error Models')
    pif.render.set_button_comment(pif)

    lsec = create_section(pif, 'e')

    llineup = {'section': [lsec]}
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('simplematrix.html', llineup=llineup)


def prepro(pif):
    pif.render.print_html()
    pif.render.hierarchy_append('/', 'Home')
    #pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/prepro.cgi', 'Prototype and Preproduction Models')
    pif.render.set_button_comment(pif)

    lsec = create_section(pif, 'p')

    llineup = {'section': [lsec]}
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('simplematrix.html', llineup=llineup)


def code2(pif):
    def prep_mod(pif, mod, cat):
	mod = pif.dbh.modify_man_item(mod)
	mod['img'] = pif.render.format_link('?mod_id=%s&cat=%s' % (mod['id'], cat), txt='%d Variation%s' % (mod['count(*)'], 's' if mod['count(*)'] != 1 else ''))
	return models.add_model_thumb_pic_link(pif, mod)

    section_id = pif.form.get_str('section')
    pif.render.print_html()
    pif.render.hierarchy_append('/', 'Home')
    #pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/code2.cgi', 'Code 2 Models')
    pif.render.set_button_comment(pif)

    llineup = {'section': []}
    for lsec in pif.dbh.depref('section', pif.dbh.fetch_sections({'page_id': pif.page_id})):
	if not section_id or section_id == lsec['id']:
	    if section_id:
		pif.render.hierarchy_append('/cgi-bin/code2.cgi?section=%s' % section_id, lsec['name'])
	    mods = pif.dbh.fetch_castings_by_category(lsec['page_id'], lsec['category'])
	    lsec['range'] = [{'entry': [{'text': prep_mod(pif, mod, lsec['category'])} for mod in mods]}]
	    llineup['section'].append(lsec)

    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('simplematrix.html', llineup=llineup)


def code2_model(pif):
    mod_id = pif.form.get_str('mod_id')
    cat_id = pif.form.get_str('cat')
    pif.render.print_html()
    pif.render.hierarchy_append('/', 'Home')
    #pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/code2.cgi', 'Code 2 Models')
    pif.render.set_button_comment(pif)

    mod = pif.dbh.modify_man_item(pif.dbh.fetch_casting(mod_id))
    img = pif.render.format_image_required(mod_id, largest=mbdata.IMG_SIZ_MEDIUM, pdir=config.IMG_DIR_MAN)
    header = '<center>%s<br><b>%s: %s</b></center><p>' % (img, mod['id'], mod['name'])
    lsec = pif.dbh.depref('section', pif.dbh.fetch_section(page_id=pif.page_id, category=cat_id))
    pif.render.hierarchy_append('/cgi-bin/code2.cgi?section=%s' % lsec['id'], lsec['name'])
    pif.render.hierarchy_append('/cgi-bin/code2.cgi?mod_id=%s&cat=%s' % (mod['id'], cat_id), mod['id'])
    lsec['range'] = [{'entry': []}]
    mvars = pif.dbh.fetch_variation_by_select(mod_id, pif.page_id, '', category=cat_id, verbose=True)
    for var in mvars:
	useful.write_comment(var)
	entry = {'text': models.add_model_var_pic_link(pif, pif.dbh.depref('v', var))}
	lsec['range'][0]['entry'].append(entry)

    llineup = {
	'section': [lsec],
	'header': header,
    }
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('simplematrix.html', llineup=llineup)


@basics.web_page
def main(pif):
    if pif.page_id == 'errors':
	return errors(pif)
    if pif.page_id == 'prepro':
	return prepro(pif)
    if pif.page_id == 'code2':
	if pif.form.get_str('mod_id'):
	    return code2_model(pif)
	else:
	    return code2(pif)


if __name__ == '__main__':  # pragma: no cover
    basics.goaway()
