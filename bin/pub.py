#!/usr/local/bin/python

import glob, os
import basics
import config
import models


# -- pub

@basics.WebPage
def Publication(pif):
    pif.render.PrintHtml()
    ostr = pif.render.FormatHead()
    pub_id = pif.FormStr('id')

    man = pif.dbh.FetchPublication(pub_id)
    if not man:
	ostr += '<meta http-equiv="refresh" content="0;url=/database.php">\n'
	return
    man = man[0]
    man['casting_type'] = 'Publication'
    man['name'] = man['base_id.rawname'].replace(';', ' ')
    imgs = PubImages(pif, pub_id)

    # top

    ostr += '<table width="100%"><tr>'
    # left bar
    content = ''
    if pif.IsAllowed('a'): # pragma: no cover
	content += '<p><b><a href="%s">Base ID</a><br>\n' % pif.dbh.GetEditorLink('base_id', {'id' : pub_id})
	content += '<a href="%s">Publication ID</a><br>\n' % pif.dbh.GetEditorLink('publication', {'id' : pub_id})
	content += '<a href="traverse.cgi?d=%s">Library</a><br>\n' % config.imgdirCat
	content += '<a href="upload.cgi?d=%s">Library Upload</a><br>\n' % config.imgdirCat

    ostr += models.AddLeftBar(pif, '', pub_id, '', 4, content)

    # title banner
    ostr += models.AddBanner(pif, man.get('name', ''))

    # top box
    ostr += '<tr><td valign=top>\n'
    if len(imgs) > 1:
	ostr += pif.render.FormatImageSized([pub_id, pub_id + '_01'], largest='l')
    if not imgs:
	img = pub_id + '.jpg'
	txt = pif.render.FormatImageSized(img, largest='s')
	txt = pif.render.FormatLink(os.path.join('..', pif.render.pic_dir, img), txt)
	ostr += txt
    if man['base_id.description']:
	ostr += '<br>' + man['base_id.description']
    ostr += '</td>\n'
    ostr += '</tr>\n'

    # lower box
    ostr += '<tr><td>\n'
    ostr += '<center>'
    if imgs:
	lran = {'id' : 'ran', 'entry' : []}
	imgs.sort()
	for img in imgs:
	    img = img[img.rfind('/') + 1:]
	    txt = pif.render.FormatImageSized(img, largest='s')
	    lnk = pif.render.FindImageFile(img, largest='g')
	    lran['entry'].append({'text' : pif.render.FormatLink('../' + lnk, txt)})
	llineup = {'id' : pub_id, 'name' : '', 'section' : [{'id' : 'sec', 'range' : [lran]}], 'columns' : 4}
	ostr += pif.render.FormatLineup(llineup)
    else:
	img = pub_id + '.jpg'
	txt = pif.render.FormatImageSized(img, largest='s')
	txt = pif.render.FormatLink(os.path.join('..', pif.render.pic_dir, img), txt)
	ostr += txt
    ostr += '</center>\n'
    ostr += '</td></tr>\n'

    ostr += '<tr><td class="bottombar">\n'
    ostr += pif.render.FormatButtonComment(pif, 'id=%s' % pub_id)
    ostr += '</td></tr></table>\n'
    ostr += pif.render.FormatTail()
    return ostr


def PubImages(pif, id):
    imgs = glob.glob(os.path.join(pif.render.pic_dir, '?_' + id.lower() + '_*.jpg'))
    imgs = list(set([os.path.split(fn)[1][2:-4] for fn in imgs]))
    imgs.sort()
    return imgs


if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
