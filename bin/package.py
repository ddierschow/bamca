#!/usr/local/bin/python

import copy, glob, os
import basics
import bfiles
import config
import imglib
import mbdata
import useful


# -- package

def print_tree_row(tree, text):
    print tree + text
    print '<br>\n'


def render_tree(pif, ch):
    ostr = ''
    for c in ch:
        if c.isdigit():
            for i in range(0, int(c)):
                ostr += pif.render.format_image_art("treeb"+".gif", also={'align': 'absmiddle', 'height': 24, 'width': 24}) + '\n'
        else:
            ostr += pif.render.format_image_art("tree"+c+".gif", also={'align': 'absmiddle', 'height': 24, 'width': 24}) + '\n'
    return ostr


def show_pic(pif, flist):
    ostr = ''
    for f in flist:
        f = f[f.rfind('/') + 1:-4]
        ostr += pif.render.format_image_as_link([f], f.upper(), also={'target': '_showpic'}) + '\n'
    return ostr


def do_tree_page(pif, dblist):
    for llist in dblist:
        cmd = llist.get_arg()
        if cmd == 'dir':
            pif.render.pic_dir = llist.get_arg()
        elif cmd == 'render':
            useful.render(pif.render.pic_dir + '/' + llist.get_arg())
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
            #print render_tree(pif, llist[1]) + desc
            #print '<br>\n'
            print_tree_row(render_tree(pif, llist[1]), desc)
        elif cmd == 'n':
            print_tree_row(render_tree(pif, llist[1]), '<font color="#666600"><i>%s</i></font>' % llist[2])
        elif cmd == 'a':
            print_tree_row(render_tree(pif, llist[1]), pif.render.format_image_as_link([llist[2]], llist[3], also={'target': '_showpic'}))
        elif cmd == 'e':
            flist = glob.glob(pif.render.pic_dir + '/' + llist[2] + "*.jpg")
            flist.sort()
            if flist:
                print '<font color="blue">'
                print_tree_row(render_tree(pif, llist[1]), ('<i>Example%s:</i>\n' % useful.plural(flist)) + show_pic(pif, flist))
                print '</font>'


@basics.web_page
def blister(pif):
    pif.render.print_html()
    #global pagename
    #pagename = pif.form.get_str('page', 'blister')

    dblist = bfiles.SimpleFile(os.path.join(config.SRC_DIR, pif.page_name + '.dat'))

    print pif.render.format_head()
    do_tree_page(pif, dblist)
    print pif.render.format_tail()

# -- boxart

# need to add va, middle to eb_1 style

def get_box_image(pif, picroot, picsize=None, compact=False):
    if compact:
	product_image = pif.render.find_image_path(picroot, prefix=picsize + '_')
	pic = pif.render.format_image_art(imglib.image_star(product_image, target_x=mbdata.imagesizes[picsize][0]))
    elif picsize:
	pic = pif.render.format_image_required(picroot, prefix=picsize + '_')
    else:
	pic = pif.render.format_image_required(picroot, largest='c')
    return pic


def show_model(pif, mod, compact=False):
    img = '' if compact else pif.render.format_image_required(mod['casting.id'], pdir=config.IMG_DIR_MAN, largest='s')
    url = "single.cgi?id=" + mod['casting.id']
    ostr  = '<center><a href="%s">%s<br>%s<br>' % (url, mod['id'], img)
    ostr += '<b>%s</b></a></center>' % mod['base_id.rawname'].replace(';', ' ')
    return ostr


def show_boxes(pif):
    pif.render.print_html()
    series = pif.form.get_str('series')
    style = pif.form.get_str('style')
    verbose = pif.form.get_bool('verbose')
    compact = pif.form.get_bool('c')
    start = pif.form.get_int('start', 1)
    end = pif.form.get_int('end', 99)
    headers = {'mod': 'Model', 'm': 'M', 'c': 'C', 's': 'S', 'box': 'Box'}
    if verbose:
	columns = ['mod', 'm', 'c', 's']
    else:
	columns = ['mod', 'box']
    boxes = list()
    for box in pif.dbh.fetch_castings_by_box(series, style):
        box['id'] = box['alias.id'] if box.get('alias.id') else box['casting.id']
        if (series and box['base_id.model_type'] != series) or \
		(style and (style not in box['box_style.styles'])) or \
		(int(box['id'][2:4]) < start) or \
		((end and int(box['id'][2:4]) > end) or (not end and int(box['id'][2:4]) != start)):
	    continue
	boxes.append(box)
    boxes.sort(key=lambda x: x['id'][2:])

    lrange = dict(note='', entry=list())
    for mod in boxes:
	box_styles = style if style else mod['box_style.styles']
	ent = {'mod': {'txt': show_model(pif, mod, compact=compact), 'rows': len(box_styles)}}
	for box_style in box_styles:
	    picroots = list(set([(mod['id'] + '-' + box_style).lower()] +
		[x[x.rfind('/') + 3:-4] for x in glob.glob(os.path.join(config.IMG_DIR_BOX, ('?_' + mod['id'] + '-' + box_style + '?.jpg').lower()))]))
	    picroots.sort()
	    hdr = "<b>%s style</b>" % box_style
	    if verbose:
		for picsize in 'mcs':
		    imgs = [get_box_image(pif, picroot, picsize, compact=compact) for picroot in picroots]
		    if compact:
			ostr = hdr + ''.join(imgs)
		    else:
			ostr = "<center>%s</center>" % hdr + '<br>'.join(imgs)
		    if pif.is_allowed('ma'):
			ostr = '<a href="upload.cgi?d=%s&n=%s">%s</a>' % (config.IMG_DIR_BOX, mod['id'].lower() + '-' + box_style.lower() + '.jpg', ostr)
		    ent[picsize] = {'txt': ostr}
	    else:
		pic = ''.join([get_box_image(pif, picroot) for picroot in picroots])
		ent['box'] = {'txt': "<center>%s<br>%s</center>" % (hdr, pic)}
	    lrange['entry'].append(copy.deepcopy(ent))
	    ent['mod'] = None
    lsection = dict(columns=columns, headers=headers, range=[lrange], note='')
    llistix = dict(section=[lsection])
    return pif.render.format_template('boxes.html', llistix=llistix)


def box_ask(pif):
    pif.render.print_html()
    pif.render.set_page_extra(pif.render.reset_button_js)
    pif.render.set_page_extra(pif.render.increment_js)
    return pif.render.format_template('boxes.html')


@basics.web_page
def box_main(pif):
    if pif.form.form:
	return show_boxes(pif)
    else:
	return box_ask(pif)


def count_boxes(pif):
    series = ""
    style = ""
    boxes = pif.dbh.fetch_castings_by_box(series, style)
    for box in boxes:
        if 'alias.id' in box:
            box['id'] = box['alias.id']
        else:
            box['id'] = box['casting.id']

    pr_count = im_count = 0
    for box in boxes:
        if box['id'].startswith('M'):
            continue
        if series and box['base_id.model_type'] != series:
            continue
        if style and style not in box['box_style.styles']:
            continue

        for c in box['box_style.styles'].replace('-', ''):
            if pif.render.find_image_path(['s_' + box['id'] + '-' + c], pdir=config.IMG_DIR_BOX):
                im_count += 1
            if pif.render.find_image_path(['c_' + box['id'] + '-' + c], pdir=config.IMG_DIR_BOX):
                im_count += 1
            if pif.render.find_image_path(['m_' + box['id'] + '-' + c], pdir=config.IMG_DIR_BOX):
                im_count += 1
            pr_count += 1

    return pr_count, im_count


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
