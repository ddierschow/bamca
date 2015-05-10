#!/usr/local/bin/python

import glob, os
import basics
import bfiles
import config
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

def show_box(pif, mod, style):
    largest = 'c'
    if style:
        box_styles = [style]
        largest = 'm'
    else:
        box_styles = mod['casting.box_styles'].replace('-', '')
    ostr = ''
    for style in box_styles:
        pic = pif.render.format_image_sized([mod['id'] + '-' + style], largest=largest, pdir=config.IMG_DIR_BOX, required=True)
        if pif.is_allowed('ma'):
            pic = '<a href="http://www.bamca.org/cgi-bin/upload.cgi?d=%s&r=%s">%s</a>' % (config.IMG_DIR_BOX, mod['id'].lower() + '-' + style.lower() + '.jpg', pic)
        ostr += pif.render.format_table_single_cell(1, "<center><b>%s style</b></center>%s" % (style, pic))
    return ostr


def show_model(pif, mod):
    #img = pif.render.format_image_required(['s_' + x for x in mod['modpic'][1]], pdir=config.IMG_DIR_MAN)
    img = pif.render.format_image_required('s_' + mod['casting.id'], pdir=config.IMG_DIR_MAN)
    url = "single.cgi?id=" + mod['casting.id']
    ostr  = "<center>%s<br>" % mod['id']
    ostr += '<a href="%s">%s</a><br>' % (url, img)
    ostr += '<b>%s</b>' % mod['base_id.rawname'].replace(';', ' ')
    ostr += "</center>"
    return ostr


@basics.web_page
def show_boxes(pif):
    pif.render.print_html()
    print pif.render.format_head()
    series = pif.form.get_str('series')
    style = pif.form.get_str('style')
    boxes = pif.dbh.fetch_castings_by_box(series, style)
    for box in boxes:
        if box.get('alias.id'):
            box['id'] = box['alias.id']
        else:
            box['id'] = box['casting.id']
    boxes.sort(key=lambda x: x['id'])

    ostr = pif.render.format_table_start()
    for box in boxes:
#       if box['id'].startswith('M'):
#           continue
        if series and box['base_id.model_type'] != series:
            continue
        if style and style not in box['casting.box_styles']:
            continue
        ostr += pif.render.format_row_start()
        ostr += pif.render.format_cell(0, show_model(pif, box))
        ostr += pif.render.format_cell(1, show_box(pif, box, style))
        ostr += pif.render.format_row_end()
    ostr += pif.render.format_table_end()
    print ostr
    print pif.render.format_tail()


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
        if style and style not in box['casting.box_styles']:
            continue

        for c in box['casting.box_styles'].replace('-', ''):
            if pif.render.find_image_file(['s_' + box['id'] + '-' + c], pdir=config.IMG_DIR_BOX):
                im_count += 1
            if pif.render.find_image_file(['c_' + box['id'] + '-' + c], pdir=config.IMG_DIR_BOX):
                im_count += 1
            if pif.render.find_image_file(['m_' + box['id'] + '-' + c], pdir=config.IMG_DIR_BOX):
                im_count += 1
            pr_count += 1

    return pr_count, im_count


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
