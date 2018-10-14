#!/usr/local/bin/python

import datetime, glob, os, pprint, re
import basics
import bfiles
import config
import images
import javasc
import mbdata
import useful

#pagename = 'biblio'

# -- biblio

map_url = '''https://www.google.com/maps/place/'''
squish_re = re.compile(r'\s\s*')

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
    lsection = sections[0].todict() if sections else dict(note='')
    tab_name = page_info.get('tab', pif.page_name)
    row_links = page_info.get('links', {})
    table = pif.dbh.depref(tab_name, pif.dbh.fetch(tab_name, where='flags&1=0', tag='biblio', verbose=True))

    lrange = dict(entry=list(), note='')
    lsection.update(dict(columns=list(), headers=dict(), range=[lrange]))

    editable = pif.form.get_bool('edit') and pif.is_allowed('a')
    if editable:
	lsection['columns'].append('edit')
	lsection['headers']['edit'] = '&nbsp;'
	row_link_formatters['edit'] = lambda x: ('https://beta.bamca.org/cgi-bin/editor.cgi?table=%s&id=' % tab_name) + str(x[0])
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
	    this_sort = int(this_sort)
	    this_sort = lsection['columns'][this_sort]
	sortkey.append(this_sort)
    if page_info.get('lastsort'):
	sortkey.append(page_info.get('lastsort'))
    if sortkey:
        table.sort(key=lambda x: [x[y] for y in sortkey if y in lsection['columns']])

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
		edlink += ' ' + pif.render.format_link('/cgi-bin/imawidget.cgi?d=.%s&f=%s' % (config.IMG_DIR_BOOK, fdict['pic_id'] + '.jpg'), '<i class="fas fa-paint-brush"></i>')
	    edlink += ' ' + pif.render.format_link('/cgi-bin/upload.cgi?d=.%s&n=%s' % (config.IMG_DIR_BOOK, fdict['pic_id'] + '.jpg'), '<i class="fas fa-upload"></i>')

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


@basics.web_page
def submit_comment(pif):
    pif.render.print_html()
    print pif.render.format_head()
    useful.write_message(pif.form)
    ostr = "I am sending this comment for you. "

    fname = pif.form.get_str('pic.name')
    fimage = pif.form.get_str('pic')
    pif.form.delete('pic')
    pif.form.change_key('page', 'page_id')
    fn = "../../comments/comment." + datetime.datetime.now().strftime('%Y%m%d.%H%M%S')

    mysubject = pif.form.get_str('mysubject')
    mycomment = pif.form.get_str('mycomment')
    if ('http://' in mysubject or 'http://' in mycomment or
	'https://' in mysubject or 'https://' in mycomment):
	ostr += "<dl><dt>ERROR</dt><dd>Whoa there.  This isn't for submitting links.  Please use the SUGGEST A LINK feature from the link list.</dd></dl>"
	return ostr

    ostr += "<dl><dt>My Subject</dt><dd>" + mysubject + "</dd>\n"
    ostr += "<dl><dt>My Comment</dt><dd>" + mycomment + "</dd>\n"
    ostr += "<dt>My Name</dt><dd>" + pif.form.get_str('myname') + "</dd>\n"
    ostr += "<dt>My Email</dt><dd>" + pif.form.get_str('myemail') + "</dd></dl>\n"

    if fimage:
	ostr += "<dt>Relevant File</dt><dd>" + fname + "<br>\n"
	direc = config.INC_DIR
	descriptions_file = config.LOG_ROOT + '/descr.log'
	dest_filename = images.get_next_upload_filename()
	dest_filename = useful.file_save(direc, dest_filename, fimage)
	images.file_log(direc + '/' + dest_filename, direc)

        cred = who = comment = '-'
	if pif.form.get_str('mycomment'):
            comment = squish_re.sub(' ', pif.form.get_str('mycomment'))
        if pif.form.get_str('credit'):
            cred = squish_re.sub(' ', pif.form.get_str('credit'))
	if pif.form.get_str('myname'):
            who = squish_re.sub(' ', pif.form.get_str('myname'))
        open(descriptions_file, 'a+').write('\t'.join([dest_filename,
                '-',
                '-',
                '-',
                comment, cred, who]) + '\n')
        ostr = '<div class="warning">Thank you for submitting that file.</div><br>\n'

	ostr += "</dd></dl>\n";

    fh = open(fn, "wt")
    fh.write("_POST\n\n" + pprint.pformat(pif.form, indent=2, width=132) + "\n\n");
    fh.write("REMOTE_ADDR=" + os.getenv('REMOTE_ADDR') + "\n");
    ostr += "Thanks for sending that.  Now please use the BACK button on your browser to return to where you were.";
    return ostr

@basics.web_page
def counts_main(pif):
    pif.render.title = 'Site Counts'
    pif.render.print_html()
    counts = pif.dbh.fetch_counts()
    v = {c['model_type']: c['count'] for c in counts[1]}
    for c in counts[0]:
	c['name'] = mbdata.model_type_names[c['model_type']]
	c['type'] = mbdata.model_types[c['model_type']]
	c['vars'] = v.get(c['model_type'], 0)

    things = []
    for mt in sorted(set(mbdata.model_types.values())):
	section = {'name': mt,
	    'columns': ['name', 'count', 'vars'],
	    'headers': {'name': 'Model Type', 'count': 'Count', 'vars': 'Variations'},
	    'range': [{
		'entry': [x for x in counts[0] if x['type'] == mt],
	    }],
	}
	tot = sum([x['count'] for x in section['range'][0]['entry']])
	vc = sum([x['vars'] for x in section['range'][0]['entry']])
	section['range'][0]['entry'].append({'name': 'total', 'count': tot, 'vars': vc})
	if tot:
	    things.append(section)
    llineup = {
	'section': things,
    }
    return pif.render.format_template('simplelistix.html', llineup=llineup)
