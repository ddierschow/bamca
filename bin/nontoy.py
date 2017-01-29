#!/usr/local/bin/python

import glob, os
import basics
import bfiles
import config
import javasc
import useful

#pagename = 'biblio'

# -- biblio

map_url = '''https://www.google.com/maps/place/'''

biblios = {
    'biblio': {
	'tab': 'book',
	'show': ['*Author', '*Title', '*Publisher', '*Year', 'ISBN'],
	'sort': 'author',
	'lastsort': 'title',
	'links': {
	    'title': 'pic:pic_id',
	    'edit': 'edit:id',
	},
    },
    'bayarea': {
	'tab': 'bayarea',
	'show': ['*Name', 'Address', '*City', 'State', 'Phone'],
	'sort': 'name',
	'lastsort': 'name',
	'links': {
	    'name': 'url:url',
	    'address': 'map:address,city,state',
	    'edit': 'edit:id',
	},
    },
}

# links (both site links and map links) aren't working.
@basics.web_page
def biblio(pif):
    def pic_formatter(x):
	img = pif.render.find_image_file([str(y) for y in x])
	return ('/' + '/'.join(pif.render.find_image_file([str(y) for y in x]))) if ''.join(img) else ''

    row_link_formatters = {
	'map': lambda x: '' if '' in x else (map_url + ','.join(x)).replace(' ', '+'),
	'url': lambda x: x[0],
	'pic': pic_formatter,
    }

    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append(pif.request_uri, pif.render.title)
    pif.render.print_html()

    page_info = biblios.get(pif.page_name, {})
    sections = pif.dbh.fetch_sections({'page_id': pif.page_id})
    lsection = pif.dbh.depref('section', sections[0]) if sections else dict(note='')
    tab_name = page_info.get('tab', pif.page_name)
    row_links = page_info.get('links', {})
    table = pif.dbh.depref(tab_name, pif.dbh.fetch(tab_name, where='flags&1=0', tag='biblio', verbose=True))

    lrange = dict(entry=list(), note='')
    lsection.update(dict(columns=list(), headers=dict(), range=[lrange]))

    editable = pif.form.get_bool('edit') and pif.is_allowed('a')
    if editable:
	lsection['columns'].append('edit')
	lsection['headers']['edit'] = '&nbsp;'
	row_link_formatters['edit'] = lambda x: ('http://beta.bamca.org/cgi-bin/editor.cgi?table=%s&id=' % tab_name) + str(x[0])
    for arg in page_info['show']:
	hdr = arg
	key = arg.lower().replace(' ', '_')
	if arg.startswith('*'):
	    key = key[1:]
	    hdr = '<a href="biblio.cgi?page=%s&sort=%s">%s</a>' % (pif.page_name, key, hdr[1:])
	lsection['columns'].append(key)
	lsection['headers'][key] = hdr

    sortkey = []
    this_sort = pif.form.get_str('sort', page_info.get('sort'))
    if this_sort:
	if this_sort.isdigit():
	    this_sort = lsection['columns'][int(this_sort)]
	sortkey.append(this_sort)
    if page_info.get('lastsort'):
	sortkey.append(page_info.get('lastsort'))
    if sortkey:
        table.sort(key=lambda x: [x[y] for y in sortkey])

    def bib_field(fdict, field):
	cont = str(fdict.get(field, '&nbsp'))
	url = ''
	if field in row_links:
	    if field == 'edit':
		cont = str(fdict['id'])
	    cmd, arg = row_links[field].split(':')
	    arg = [str(fdict.get(x, lsection.get(x, ''))) for x in arg.split(',')]
	    if ''.join(arg):
		url = row_link_formatters[cmd](arg)

	edlink = ''
	if field == 'title' and editable:
	    if os.path.exists('.' + config.IMG_DIR_BOOK + '/' + fdict['pic_id'] + '.jpg'):
		edlink += ' ' + pif.render.format_link('/cgi-bin/imawidget.cgi?d=.%s&f=%s' % (config.IMG_DIR_BOOK, fdict['pic_id'] + '.jpg'), '<i class="fa fa-paint-brush"></i>')
	    edlink += ' ' + pif.render.format_link('/cgi-bin/upload.cgi?d=.%s&n=%s' % (config.IMG_DIR_BOOK, fdict['pic_id'] + '.jpg'), '<i class="fa fa-upload"></i>')

	return pif.render.format_link(url, cont) + edlink

    lrange['entry'] = [{field: bib_field(fdict, field) for field in lsection['columns']}
		       for fdict in table]
    pif.render.set_button_comment(pif)
    return pif.render.format_template('simplelistix.html', llineup=dict(section=[lsection]))

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


if __name__ == '__main__':  # pragma: no cover
    basics.goaway()
