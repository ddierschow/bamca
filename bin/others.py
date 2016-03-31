#!/usr/local/bin/python

import basics
import config
import models


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
    pif.render.format_button_comment(pif)

    lsec = create_section(pif, 'e')

    return pif.render.format_template('simplematrix.html', llineup={'section': [lsec]})


def prepro(pif):
    pif.render.print_html()
    pif.render.hierarchy_append('/', 'Home')
    #pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/prepro.cgi', 'Prototype and Preproduction Models')
    pif.render.format_button_comment(pif)

    lsec = create_section(pif, 'p')

    return pif.render.format_template('simplematrix.html', llineup={'section': [lsec]})


@basics.web_page
def main(pif):
    if pif.page_id == 'errors':
	return errors(pif)
    if pif.page_id == 'prepro':
	return prepro(pif)


if __name__ == '__main__':  # pragma: no cover
    basics.goaway()
