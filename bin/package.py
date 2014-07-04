#!/usr/local/bin/python

import glob, os
import basics
import config
import useful


# -- package

def PrintTreeRow(tree, text):
    print tree + text
    print '<br>\n'


def RenderTree(pif, ch):
    ostr = ''
    for c in ch:
	if c.isdigit():
	    for i in range(0,int(c)):
		ostr += pif.render.FormatImageArt("treeb"+".gif", also={'align':'absmiddle', 'height':24, 'width':24}) + '\n'
	else:
	    ostr += pif.render.FormatImageArt("tree"+c+".gif", also={'align':'absmiddle', 'height':24, 'width':24}) + '\n'
    return ostr


def ShowPic(pif, flist):
    ostr = ''
    for f in flist:
	f = f[f.rfind('/') + 1:-4]
	ostr += pif.render.FormatImageAsLink( [f], f.upper(), also={'target':'_showpic'} ) + '\n'
    return ostr


def DoTreePage(pif, dblist):
    for llist in dblist:
	cmd = llist.GetArg()
	if cmd == 'dir':
	    pif.render.pic_dir = llist.GetArg()
	elif cmd == 'render':
	    useful.Render(pif.render.pic_dir + '/' + llist.GetArg())
	elif cmd == 'p':
	    print '<p>\n'
	elif cmd == 's':
	    print '<p>\n'
	    print '<a name="%s"></a>' % llist[1]
	    if llist[2]:
		print '<b><u>%s -' % llist[2],
	    else:
		print '<b><u>',
	    print '%s</u></b>' % llist[3]
	    print '<br>\n'
	elif cmd == 'm':
	    desc = ''
	    if llist[2]:
		desc += ('<b>%s</b> ' % llist[2])
		if llist[3] and not llist[3][0].isupper():
		    desc += "- "
	    desc += llist[3]
	    #print RenderTree(pif, llist[1]) + desc
	    #print '<br>\n'
	    PrintTreeRow(RenderTree(pif, llist[1]), desc)
	elif cmd == 'n':
	    PrintTreeRow(RenderTree(pif, llist[1]), '<font color="#666600"><i>%s</i></font>' % llist[2])
	elif cmd == 'a':
	    PrintTreeRow(RenderTree(pif, llist[1]), pif.render.FormatImageAsLink([llist[2]], llist[3], also={'target':'_showpic'}) )
	elif cmd == 'e':
	    flist = glob.glob(pif.render.pic_dir + '/' + llist[2] + "*.jpg")
	    flist.sort()
	    if flist:
		print '<font color="blue">'
		PrintTreeRow(RenderTree(pif, llist[1]), ('<i>Example%s:</i>\n' % useful.Plural(flist)) + ShowPic(pif, flist))
		print '</font>'


@basics.WebPage
def Blister(pif):
    pif.render.PrintHtml()
    global pagename
    pagename = pif.form.get('page', 'blister')

    import files
    dblist = files.SimpleFile(os.path.join(config.srcdir, pagename + '.dat'))

    print pif.render.FormatHead()
    DoTreePage(pif, dblist)
    print pif.render.FormatTail()

# -- boxart

# need to add va,middle to eb_1 style

def ShowBox(pif, mod, style):
    largest = 'c'
    if style:
	box_styles = [style]
	largest = 'm'
    else:
	box_styles = mod['casting.box_styles'].replace('-', '')
    ostr = ''
    for style in box_styles:
	pic = pif.render.FormatImageSized([mod['id'] + '-' + style], largest=largest, pdir=config.imgdirBox, required=True)
	if pif.IsAllowed('ma'):
	    pic = '<a href="http://www.bamca.org/cgi-bin/upload.cgi?d=%s&r=%s">%s</a>' % (config.imgdirBox, mod['id'].lower() + '-' + style.lower() + '.jpg', pic)
	ostr += pif.render.FormatTableSingleCell(1, "<center><b>%s style</b></center>%s" % (style, pic))
    return ostr


def ShowModel(pif, mod):
    #img = pif.render.FormatImageRequired(['s_' + x for x in mod['modpic'][1]], pdir=config.imgdir175)
    img = pif.render.FormatImageRequired('s_' + mod['casting.id'], pdir=config.imgdir175)
    url = "single.cgi?id=" + mod['casting.id']
    ostr  = "<center>%s<br>" % mod['id']
    ostr += '<a href="%s">%s</a><br>' % (url, img)
    ostr += '<b>%s</b>' % mod['base_id.rawname'].replace(';', ' ')
    ostr += "</center>"
    return ostr


@basics.WebPage
def ShowBoxes(pif):
    pif.render.PrintHtml()
    print pif.render.FormatHead()
    series = pif.form.get('series')
    style = pif.form.get('style')
    boxes = pif.dbh.FetchCastingsByBox(series, style)
    for box in boxes:
	if box.get('alias.id'):
	    box['id'] = box['alias.id']
	else:
	    box['id'] = box['casting.id']
    boxes.sort(key=lambda x:x['id'])

    ostr = pif.render.FormatTableStart()
    for box in boxes:
#	if box['id'].startswith('M'):
#	    continue
	if series and box['base_id.model_type'] != series:
	    continue
	if style and not style in box['casting.box_styles']:
	    continue
	ostr += pif.render.FormatRowStart()
	ostr += pif.render.FormatCell(0, ShowModel(pif, box))
	ostr += pif.render.FormatCell(1, ShowBox(pif, box, style))
	ostr += pif.render.FormatRowEnd()
    ostr += pif.render.FormatTableEnd()
    print ostr
    print pif.render.FormatTail()


def CountBoxes(pif):
    series = ""
    style = ""
    boxes = pif.dbh.FetchCastingsByBox(series, style)
    for box in boxes:
	if box.has_key('alias.id'):
	    box['id'] = box['alias.id']
	else:
	    box['id'] = box['casting.id']

    pr_count = im_count = 0
    for box in boxes:
	if box['id'].startswith('M'):
	    continue
	if series and box['base_id.model_type'] != series:
	    continue
	if style and not style in box['casting.box_styles']:
	    continue

	for c in box['casting.box_styles'].replace('-', ''):
	    if pif.render.FindImageFile(['s_' + box['id'] + '-' + c], pdir=config.imgdirBox):
		im_count += 1
	    if pif.render.FindImageFile(['c_' + box['id'] + '-' + c], pdir=config.imgdirBox):
		im_count += 1
	    if pif.render.FindImageFile(['m_' + box['id'] + '-' + c], pdir=config.imgdirBox):
		im_count += 1
	    pr_count += 1

    return pr_count, im_count


if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
