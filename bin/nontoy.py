#!/usr/local/bin/python

import glob, os
import basics
import bfiles
import config
import javascript

#pagename = 'biblio'

# -- biblio

def_map_link = javascript.def_map_link
fmt = '''http://maps.google.com/maps?f=q&source=s_q&hl=en&geocode=&q='''

def map_link(bits):
    if '' in bits:
        return ''
    return (fmt + ','.join(bits)).replace(' ', '+')

#def map_link(addr, city, state):
#    return (fmt + addr + ',' + city + ',' + state).replace(' ', '+')


@basics.web_page
def biblio(pif):
    pif.render.print_html()
    #global pagename
    #pagename = pif.form_str('page', 'biblio')

    dblist = bfiles.SimpleFile(os.path.join(config.SRC_DIR, pif.page_id + '.dat'))
    print pif.render.format_head()

    shown = False
    fields = []
    layout = []
    table = []
    row_links = {}
    for llist in dblist:

        if llist.get_arg() == 'b':
            table.append(llist)
        else:
            llist.rewind()
            layout.append(llist)

    if pif.form_has('sort'):
        table.sort(key=lambda x: x[pif.form_int('sort')].lower())

    ostr = ''
    for llist in layout:

#       if not llist:
#           ostr += '\n'
#           continue

        cmd = llist.get_arg()

        if cmd == 'h':
            if pif.render.simple:
                for iarg in range(1, llist.args()):
                    arg = llist.get_arg('&nbsp;')
                    if arg[0] == '*':
                        arg = arg[1:]
                        ostr += ' <ul><li>%s\n' % arg
                    else:
                        ostr += ' <ul><li>%s\n' % arg
                    fields.append(arg)
                for field in fields:
                    ostr += ' </ul>\n'
            else:
                ostr += pif.render.format_table_start()
                ostr += pif.render.format_row_start()
                for iarg in range(1, llist.args()):
                    arg = llist.get_arg('&nbsp;')
                    if arg[0] == '*':
                        arg = arg[1:]
                        ostr += pif.render.format_cell(0, '<a href="biblio.cgi?page=%s&sort=%d">%s' % (pif.page_id, iarg, arg), hdr=True)
                    elif arg[0] == '-':
                        pass
                    else:
                        ostr += pif.render.format_cell(0, arg, hdr=True)
                    fields.append(arg)
                ostr += pif.render.format_row_end()
            ostr += '\n'
            shown = True

        elif cmd == 'l':
            row_links[llist[1]] = llist[2]

        elif cmd == 't':
            for tlist in table:
                if pif.render.simple:
                    for field in fields:
                        ostr += ' <ul><li>%s\n' % tlist.get_arg('&nbsp;')
                    for field in fields:
                        ostr += ' </ul>\n'
                    ostr += pif.render.format_row_end()
                else:
                    ostr += pif.render.format_row_start()
                    fdict = dict(zip(fields, tlist.llist[1:]))
                    for field in fields:
                        if field[0] == '-':
                            continue
                        cont = tlist.get_arg('&nbsp;')
                        url = ''
                        if field in row_links:
                            if row_links[field] in fields:
                                url = fdict.get(row_links[field], '')
                            elif row_links[field].find(',') >= 0:
                                url = map_link([fdict.get(x, '') for x in row_links[field].split(',')[1:]])
                            elif cont.startswith('http://'):
                                url = cont
                        if url:
                            ostr += pif.render.format_cell(0, pif.render.format_link(url, cont))
                        else:
                            ostr += pif.render.format_cell(0, cont)
                    ostr += pif.render.format_row_end()
            ostr += '\n'

        elif cmd == 'n':
            if not pif.render.simple and shown:
                ostr += pif.render.format_row_start()
                ostr += pif.render.format_cell(0, llist.get_arg('&nbsp;'), also={'colspan': len(fields)})
                ostr += pif.render.format_row_end()
            else:
                ostr += '%s<p>\n' % llist.get_arg('&nbsp;')

        elif cmd == 'e':
            if pif.render.simple:
                pass
            else:
                ostr += pif.render.format_table_end()
            shown = False

        else:
            ostr += '\n'

    if not pif.render.simple:
        if shown:
            ostr += pif.render.format_table_end()
        ostr += 'There is also a <a href="biblio.cgi?page=%s&simple=1">cheezy, non-tables version of this page.</a><p>\n' % pif.page_id

    print ostr
    print pif.render.format_tail()

# -- calendar

def print_type(pif, event):
    #return pif.render.format_cell(0, '<center><b><img src="../pic/gfx/%s.gif" alt="[%s]"></b></center>' % (event, event.upper()))
    return pif.render.format_cell(0, '<center><b>%s</b></center>' % pif.render.format_image_art(event, event.upper()))


@basics.web_page
def calendar(pif):
    pif.render.print_html()
    #global pagename
    #pagename = pif.form_str('page', 'calendar')
    dblist = bfiles.SimpleFile(os.path.join(config.SRC_DIR, pif.page_id + '.dat'))
    print pif.render.format_head()
    shown = False
    ostr = ''
    for llist in dblist:

        if not llist:
            ostr += '\n'
            continue

        cmd = llist.get_arg()

        if (cmd == 'h'):
            ostr += pif.render.format_table_start()
            ostr += pif.render.format_row_start()
            for iarg in range(1, llist.args()):
                arg = llist.get_arg('&nbsp;')
                ostr += pif.render.format_cell(1, arg, hdr=1)
            ostr += pif.render.format_row_end()
            ostr += '\n'
            shown = True

        elif (cmd == 't'):
            ostr += '<center><h1>%s</h1></center>\n' % (llist.get_arg())

        elif (cmd == 'm'):
            ostr += pif.render.format_row_start()
            ostr += print_type(pif, 'meet')
            ostr += pif.render.format_cell(1, llist.get_arg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.format_cell(1, llist.get_arg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.format_cell(1, llist.get_arg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.format_row_end()
            ostr += '\n'

        elif (cmd == 's'):
            ostr += pif.render.format_row_start()
            ostr += print_type(pif, 'show')
            ostr += pif.render.format_cell(1, llist.get_arg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.format_cell(1, llist.get_arg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.format_cell(1, llist.get_arg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.format_row_end()
            ostr += '\n'

        elif (cmd == 'b'):
            ostr += pif.render.format_row_start()
            ostr += print_type(pif, llist.get_arg())
            ostr += pif.render.format_cell(1, llist.get_arg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.format_cell(1, llist.get_arg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.format_cell(1, llist.get_arg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.format_row_end()
            ostr += '\n'

        elif (cmd == 'n'):
            #ostr += pif.render.format_row_start()
            #ostr += '<td colspan=4><center><font size=+2><b>%s</b></font></center></td>\n' % llist.get_arg('&nbsp;')
            #ostr += pif.render.format_row_end()
            ostr += pif.render.format_section(llist.get_arg('&nbsp;'), also={'colspan': 4})

        elif (cmd == 'e'):
            ostr += pif.render.format_table_end()
            shown = False

        else:
            ostr += '\n'

    if shown:
        ostr += pif.render.format_table_end()

    print ostr
    print pif.render.format_tail()

# -- activity

@basics.web_page
def activity_main(pif):
    pif.render.print_html()
    pif.render.title = "Site Activity"

    print pif.render.format_head()
    if pif.form_has('d'):
        for id in pif.form_list('d'):
            pif.dbh.delete_activity(id)
    print '<hr>'
    acts = pif.dbh.fetch_activities()
    acts.sort(key=lambda x: x['site_activity.timestamp'])
    acts.reverse()
    for act in acts:
        if not act['site_activity.user_id']:
            continue
        if act['site_activity.url']:
            print '<a href="../%s">' % act['site_activity.url']
        print '<b>%s</b><br>' % act['site_activity.name']
        if act['site_activity.image']:
            print '<img src="../%s"><br>' % act['site_activity.image']
        print '%s<br>' % act['site_activity.description']
        print 'Change made by %s at %s<br>' % (act['user.name'], act['site_activity.timestamp'])
        if act['site_activity.url']:
            print '</a>'
        if pif.is_allowed('am'):
            print pif.render.format_button('delete', link='?d=%s' % act['site_activity.id'])
        print '<hr>'
    print pif.render.format_tail()


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
