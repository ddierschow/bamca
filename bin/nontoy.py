#!/usr/local/bin/python

import glob, os
import basics
import bfiles
import config
import javascript

pagename = 'biblio'

# -- biblio

def_map_link = javascript.def_map_link
fmt = '''http://maps.google.com/maps?f=q&source=s_q&hl=en&geocode=&q='''

def MapLink(bits):
    if '' in bits:
        return ''
    return (fmt + ','.join(bits)).replace(' ', '+')

#def MapLink(addr, city, state):
#    return (fmt + addr + ',' + city + ',' + state).replace(' ', '+')


@basics.WebPage
def Biblio(pif):
    pif.render.PrintHtml()
    global pagename
    pagename = pif.FormStr('page', 'biblio')

    dblist = bfiles.SimpleFile(os.path.join(config.srcdir, pagename + '.dat'))
    print pif.render.FormatHead()

    shown = False
    fields = []
    layout = []
    table = []
    row_links = {}
    for llist in dblist:

        if llist.GetArg() == 'b':
            table.append(llist)
        else:
            llist.Rewind()
            layout.append(llist)

    if pif.FormHas('sort'):
        global sortfield
        sortfield = pif.FormInt('sort')
        table.sort(key=lambda x: x[sortfield].lower())

    ostr = ''
    for llist in layout:

#       if not llist:
#           ostr += '\n'
#           continue

        cmd = llist.GetArg()

        if cmd == 'h':
            if pif.render.simple:
                for iarg in range(1, llist.Args()):
                    arg = llist.GetArg('&nbsp;')
                    if arg[0] == '*':
                        arg = arg[1:]
                        ostr += ' <ul><li>%s\n' % arg
                    else:
                        ostr += ' <ul><li>%s\n' % arg
                    fields.append(arg)
                for field in fields:
                    ostr += ' </ul>\n'
            else:
                ostr += pif.render.FormatTableStart()
                ostr += pif.render.FormatRowStart()
                for iarg in range(1, llist.Args()):
                    arg = llist.GetArg('&nbsp;')
                    if arg[0] == '*':
                        arg = arg[1:]
                        ostr += pif.render.FormatCell(0, '<a href="biblio.cgi?page=%s&sort=%d">%s' % (pagename, iarg, arg), hdr=True)
                    elif arg[0] == '-':
                        pass
                    else:
                        ostr += pif.render.FormatCell(0, arg, hdr=True)
                    fields.append(arg)
                ostr += pif.render.FormatRowEnd()
            ostr += '\n'
            shown = True

        elif cmd == 'l':
            row_links[llist[1]] = llist[2]

        elif cmd == 't':
            for tlist in table:
                if pif.render.simple:
                    for field in fields:
                        ostr += ' <ul><li>%s\n' % tlist.GetArg('&nbsp;')
                    for field in fields:
                        ostr += ' </ul>\n'
                    ostr += pif.render.FormatRowEnd()
                else:
                    ostr += pif.render.FormatRowStart()
                    fdict = dict(zip(fields, tlist.llist[1:]))
                    for field in fields:
                        if field[0] == '-':
                            continue
                        cont = tlist.GetArg('&nbsp;')
                        url = ''
                        if field in row_links:
                            if row_links[field] in fields:
                                url = fdict.get(row_links[field], '')
                            elif row_links[field].find(',') >= 0:
                                url = MapLink([fdict.get(x, '') for x in row_links[field].split(',')[1:]])
                            elif cont.startswith('http://'):
                                url = cont
                        if url:
                            ostr += pif.render.FormatCell(0, pif.render.FormatLink(url, cont))
                        else:
                            ostr += pif.render.FormatCell(0, cont)
                    ostr += pif.render.FormatRowEnd()
            ostr += '\n'

        elif cmd == 'n':
            if not pif.render.simple and shown:
                ostr += pif.render.FormatRowStart()
                ostr += pif.render.FormatCell(0, llist.GetArg('&nbsp;'), also={'colspan': len(fields)})
                ostr += pif.render.FormatRowEnd()
            else:
                ostr += '%s<p>\n' % llist.GetArg('&nbsp;')

        elif cmd == 'e':
            if pif.render.simple:
                pass
            else:
                ostr += pif.render.FormatTableEnd()
            shown = False

        else:
            ostr += '\n'

    if not pif.render.simple:
        if shown:
            ostr += pif.render.FormatTableEnd()
        ostr += 'There is also a <a href="biblio.cgi?page=%s&simple=1">cheezy, non-tables version of this page.</a><p>\n' % pagename

    print ostr
    print pif.render.FormatTail()

# -- calendar

def PrintType(pif, event):
    #return pif.render.FormatCell(0, '<center><b><img src="../pic/gfx/%s.gif" alt="[%s]"></b></center>' % (event, event.upper()))
    return pif.render.FormatCell(0, '<center><b>%s</b></center>' % pif.render.FormatImageArt(event, event.upper()))


@basics.WebPage
def Calendar(pif):
    pif.render.PrintHtml()
    global pagename
    pagename = pif.FormStr('page', 'calendar')
    dblist = bfiles.SimpleFile(os.path.join(config.srcdir, pagename + '.dat'))
    print pif.render.FormatHead()
    shown = False
    ostr = ''
    for llist in dblist:

        if not llist:
            ostr += '\n'
            continue

        cmd = llist.GetArg()

        if (cmd == 'h'):
            ostr += pif.render.FormatTableStart()
            ostr += pif.render.FormatRowStart()
            for iarg in range(1, llist.Args()):
                arg = llist.GetArg('&nbsp;')
                ostr += pif.render.FormatCell(1, arg, hdr=1)
            ostr += pif.render.FormatRowEnd()
            ostr += '\n'
            shown = True

        elif (cmd == 't'):
            ostr += '<center><h1>%s</h1></center>\n' % (llist.GetArg())

        elif (cmd == 'm'):
            ostr += pif.render.FormatRowStart()
            ostr += PrintType(pif, 'meet')
            ostr += pif.render.FormatCell(1, llist.GetArg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.FormatCell(1, llist.GetArg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.FormatCell(1, llist.GetArg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.FormatRowEnd()
            ostr += '\n'

        elif (cmd == 's'):
            ostr += pif.render.FormatRowStart()
            ostr += PrintType(pif, 'show')
            ostr += pif.render.FormatCell(1, llist.GetArg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.FormatCell(1, llist.GetArg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.FormatCell(1, llist.GetArg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.FormatRowEnd()
            ostr += '\n'

        elif (cmd == 'b'):
            ostr += pif.render.FormatRowStart()
            ostr += PrintType(pif, llist.GetArg())
            ostr += pif.render.FormatCell(1, llist.GetArg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.FormatCell(1, llist.GetArg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.FormatCell(1, llist.GetArg('&nbsp;').replace(';', '<br>'))
            ostr += pif.render.FormatRowEnd()
            ostr += '\n'

        elif (cmd == 'n'):
            #ostr += pif.render.FormatRowStart()
            #ostr += '<td colspan=4><center><font size=+2><b>%s</b></font></center></td>\n' % llist.GetArg('&nbsp;')
            #ostr += pif.render.FormatRowEnd()
            ostr += pif.render.FormatSection(llist.GetArg('&nbsp;'), also={'colspan': 4})

        elif (cmd == 'e'):
            ostr += pif.render.FormatTableEnd()
            shown = False

        else:
            ostr += '\n'

    if shown:
        ostr += pif.render.FormatTableEnd()

    print ostr
    print pif.render.FormatTail()

# -- activity

@basics.WebPage
def ActivityMain(pif):
    pif.render.PrintHtml()
    pif.render.title = "Site Activity"

    print pif.render.FormatHead()
    if pif.FormHas('d'):
        for id in pif.FormList('d'):
            pif.dbh.DeleteActivity(id)
    print '<hr>'
    acts = pif.dbh.FetchActivities()
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
        if pif.IsAllowed('am'):
            print pif.render.FormatButton('delete', link='?d=%s' % act['site_activity.id'])
        print '<hr>'
    print pif.render.FormatTail()


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
