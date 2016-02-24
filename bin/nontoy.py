#!/usr/local/bin/python

import glob, os
import basics
import bfiles
import config
import javasc

#pagename = 'biblio'

# -- biblio

def_map_link = javasc.def_map_link
fmt = '''http://maps.google.com/maps?f=q&source=s_q&hl=en&geocode=&q='''

def map_link(bits):
    if '' in bits:
        return ''
    return (fmt + ','.join(bits)).replace(' ', '+')

#def map_link(addr, city, state):
#    return (fmt + addr + ',' + city + ',' + state).replace(' ', '+')


# links (both site links and map links) aren't working.
@basics.web_page
def biblio(pif):
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append(pif.request_uri, pif.render.title)
    pif.render.print_html()

    dblist = bfiles.SimpleFile(os.path.join(config.SRC_DIR, pif.page_name + '.dat'))

    lrange = dict(entry=list(), note='')
    lsection = dict(columns=list(), headers=dict(), range=[lrange], note='')
    llistix = dict(section=[lsection])

    fields = list()
    table = list()  # two phase to allow sorting
    row_links = dict()
    sort_cols = [None]
    for llist in dblist:

        cmd = llist.get_arg()

        if cmd == 'h':
	    for iarg in range(1, llist.args()):
		hdr = arg = llist.get_arg('&nbsp;')
		key = arg.lower().replace(' ', '_')
		if arg[0] == '*':
		    hdr = hdr[1:]
		    key = key[1:]
		    lsection['columns'].append(key)
		    hdr = '<a href="biblio.cgi?page=%s&sort=%d">%s</a>' % (pif.page_name, iarg, hdr)
		elif arg[0] == '-':
		    pass
		else:
		    lsection['columns'].append(key)
		sort_cols.append(key)
		lsection['headers'][key] = hdr
		fields.append(key)

        elif cmd == 'l':
            row_links[llist[1].lower().replace(' ', '_')] = llist[2]

        elif cmd == 'n':
	    lsection['note'] += llist.get_arg('&nbsp;') + '<br>'

        elif cmd == 'b':
	    table.append(dict(zip(fields, llist.llist[1:])))

    if pif.form.has('sort'):
        print sort_cols,pif.form.get_int('sort')
        table.sort(key=lambda x: x[sort_cols[pif.form.get_int('sort')]].lower())

    for fdict in table:
	ent = dict()
	for field in lsection['columns']:
	    cont = fdict.get(field, '&nbsp')
	    url = ''
	    if field in row_links:
		if row_links[field] in fields:
		    url = fdict.get(row_links[field], '')
		elif row_links[field].find(',') >= 0:
		    url = map_link([fdict.get(x, '') for x in row_links[field].split(',')[1:]])
		elif cont.startswith('http://'):
		    url = cont
	    ent[field] = pif.render.format_link(url, cont)
	lrange['entry'].append(ent)

    return pif.render.format_template('simplelistix.html', llineup=llistix)

# -- calendar

def event_type(pif, event):
    return '<center><b>%s</b></center>' % pif.render.format_image_art(event, event.upper())


def event(pif, ty, llist):
    return [event_type(pif, ty),
		    llist.get_arg('&nbsp;').replace(';', '<br>'),
		    llist.get_arg('&nbsp;').replace(';', '<br>'),
		    llist.get_arg('&nbsp;').replace(';', '<br>')]

@basics.web_page
def calendar(pif):
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append(pif.request_uri, 'Calendar')
    pif.render.print_html()

    dblist = bfiles.SimpleFile(os.path.join(config.SRC_DIR, pif.page_name + '.dat'))

    lrange = None
    lsection = dict(columns=list(), headers=dict(), range=list(), note='')
    llistix = dict(section=[lsection])

    for llist in dblist:

        cmd = llist.get_arg()

        if (cmd == 'h'):
            for iarg in range(1, llist.args()):
                arg = llist.get_arg('&nbsp;')
		lsection['columns'].append(arg)
		lsection['headers'][arg] = arg

        elif (cmd == 'm'):
	    lrange['entry'].append(dict(zip(lsection['columns'],
		    event(pif, 'meet', llist))))

        elif (cmd == 's'):
	    lrange['entry'].append(dict(zip(lsection['columns'], 
		    event(pif, 'show', llist))))

        elif (cmd == 'n'):
	    if lrange:
		lsection['range'].append(lrange)
	    lrange = dict(entry=list(), name=llist.get_arg('&nbsp;', 1))

        elif (cmd == 'e'):
	    if lrange:
		lsection['range'].append(lrange)
	    lrange = None

    if lrange:
	lsection['range'].append(lrange)

    return pif.render.format_template('simplelistix.html', llineup=llistix)

# -- activity

@basics.web_page
def activity_main(pif):
    pif.render.print_html()
    pif.render.title = "Site Activity"

    print pif.render.format_head()
    if pif.form.has('d'):
        for id in pif.form.get_list('d'):
            pif.dbh.delete_activity(id)
    print '<hr>'
    acts = pif.dbh.fetch_activities()
    acts.sort(key=lambda x: x['site_activity.timestamp'])
    acts.reverse()
    for act in acts:
        if not act['site_activity.by_user_id']:
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
