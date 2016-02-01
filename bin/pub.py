#!/usr/local/bin/python

import glob, os
import basics
import config
import models
import useful


# -- pub

@basics.web_page
def publication(pif):
    pif.render.print_html()
    ostr = pif.render.format_head()
    pub_id = pif.form.get_str('id')

    man = pif.dbh.fetch_publication(pub_id)
    if not man:
	raise useful.SimpleError("That publication was not found.")
    man = man[0]
    man['casting_type'] = 'Publication'
    man['name'] = man['base_id.rawname'].replace(';', ' ')
    imgs = pub_images(pif, pub_id)

    # top

    ostr += '<table width="100%"><tr>'
    # left bar
    content = ''
    if pif.is_allowed('a'):  # pragma: no cover
        content += '<p><b><a href="%s">Base ID</a><br>\n' % pif.dbh.get_editor_link('base_id', {'id': pub_id})
        content += '<a href="%s">Publication</a><br>\n' % pif.dbh.get_editor_link('publication', {'id': pub_id})
        content += '<a href="traverse.cgi?d=%s">Library</a><br>\n' % config.IMG_DIR_CAT
	content += '<a href="upload.cgi?d=./%s&n=%s&c=%s">Product Upload</a><br>\n' % (config.IMG_DIR_CAT, pub_id, pub_id)

    ostr += models.add_left_bar(pif, '', pub_id, '', 4, content)

    # title banner
    ostr += models.add_banner(pif, man.get('name', ''))

    # top box
    ostr += '<tr><td valign=top>\n'
#    if len(imgs) > 1:
#        ostr += pif.render.format_image_sized([pub_id, pub_id + '_01'], largest='l')
    if not imgs:
        img = pub_id + '.jpg'
        txt = pif.render.format_image_sized(img, largest='s')
        txt = pif.render.format_link(os.path.join('..', pif.render.pic_dir, img), txt)
        ostr += txt
    if man['base_id.description']:
        ostr += '<br>' + man['base_id.description']
    ostr += '</td>\n'
    ostr += '</tr>\n'

    # lower box
    ostr += '<tr><td>\n'
    ostr += '<center>'
    if imgs:
        lran = {'id': 'ran', 'entry': []}
        imgs.sort()
        for img in imgs:
            img = img[img.rfind('/') + 1:]
            txt = pif.render.format_image_sized(img, largest='s')
            lnk = pif.render.find_image_path(img, largest='g')
            lran['entry'].append({'text': pif.render.format_link('../' + lnk, txt)})
        llineup = {'id': pub_id, 'name': '', 'section': [{'id': 'sec', 'range': [lran]}], 'columns': 4}
        ostr += pif.render.format_matrix(llineup)
    else:
        img = pub_id + '.jpg'
        txt = pif.render.format_image_sized(img, largest='s')
        txt = pif.render.format_link(os.path.join('..', pif.render.pic_dir, img), txt)
        ostr += txt
    ostr += '</center>\n'
    ostr += '</td></tr>\n'

    ostr += '<tr><td class="bottombar">\n'
    ostr += pif.render.format_button_comment(pif, 'id=%s' % pub_id)
    ostr += '</td></tr></table>\n'
    ostr += pif.render.format_tail()
    return ostr


def pub_images(pif, id):
    imgs = glob.glob(os.path.join(pif.render.pic_dir, '?_' + id.lower() + '_*.jpg'))
    imgs = list(set([os.path.split(fn)[1][2:-4] for fn in imgs]))
    imgs.sort()
    return imgs


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
