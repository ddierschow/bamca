#!/usr/local/bin/python

import glob, os
import basics
import config
import mbdata
import models
import useful


# -- pub

@basics.web_page
def publication(pif):
    pif.render.print_html()
    pub_id = pif.form.get_str('id')

    man = pif.dbh.fetch_publication(pub_id)
    if not man:
	raise useful.SimpleError("That publication was not found.")
    man = man[0]
    man['casting_type'] = 'Publication'
    man['name'] = man['base_id.rawname'].replace(';', ' ')
    imgs = pub_images(pif, pub_id)

    left_bar_content = ''
    if pif.is_allowed('a'):  # pragma: no cover
        left_bar_content += '<p><b><a href="%s">Base ID</a><br>\n' % pif.dbh.get_editor_link('base_id', {'id': pub_id})
        left_bar_content += '<a href="%s">Publication</a><br>\n' % pif.dbh.get_editor_link('publication', {'id': pub_id})
        left_bar_content += '<a href="traverse.cgi?d=.%s">Library</a><br>\n' % config.IMG_DIR_CAT
	left_bar_content += '<a href="upload.cgi?d=.%s&n=%s&c=%s">Product Upload</a><br>\n' % (config.IMG_DIR_CAT, pub_id, pub_id)

    upper_box = ''
    if imgs:
	upper_box += pif.render.format_image_link_image(imgs[0], link_largest=mbdata.IMG_SIZ_LARGE)
    else:
	upper_box += pif.render.format_image_link_image(img, link_largest=mbdata.IMG_SIZ_LARGE)
    if man['base_id.description']:
	upper_box += '<br>' if upper_box else ''
	upper_box += man['base_id.description']

    lran = {'id': 'ran', 'entry':
	[{'text': pif.render.format_image_link_image(img[img.rfind('/') + 1:])} for img in sorted(imgs)] if imgs else
	[{'text': pif.render.format_image_link_image(pub_id)}]
    }
    llineup = {'id': pub_id, 'name': '', 'section': [{'id': 'sec', 'range': [lran], 'columns': 4}], 'columns': 4}

    pif.render.set_button_comment(pif, 'id=%s' % pub_id)
    pif.render.format_matrix_for_template(llineup)
    context = {
	'title': man.get('name', ''),
	'note': '',
	'type_id': '',
	#'icon_id': pub_id,
	'vehicle_type': '',
	'rowspan': 5 if upper_box else 4,
	'left_bar_content': left_bar_content,
	'upper_box': upper_box,
	'llineup': llineup,
    }
    return pif.render.format_template('pub.html', **context)


def pub_images(pif, id):
    imgs = glob.glob(os.path.join(pif.render.pic_dir, '?_' + id.lower() + '_*.jpg'))
    imgs = list(set([os.path.split(fn)[1][2:-4] for fn in imgs]))
    imgs.sort()
    return imgs


if __name__ == '__main__':  # pragma: no cover
    basics.goaway()
