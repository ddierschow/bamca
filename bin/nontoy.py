#!/usr/local/bin/python

import datetime
from io import open
import os
import pprint

import basics
import bfiles
import config
import images
import mbdata
import render
import useful

# pagename = 'biblio'

# -- biblio

map_url = '''https://www.google.com/maps/place/'''

biblios = {
    'biblio': {
        'mags': 0,
        'tab': 'book',
        'headers': ['*Author', '*Title', '*Publisher', '*Year', 'ISBN'],
        'show': ['author', 'title', 'publisher', 'year', 'isbn'],
        'sort': 'author',
        'lastsort': 'title',  # last sorting key
        'links': {
            'title': 'pic:pic_id',
            'edit': 'edit:id',
        },
    },
    'bayarea': {
        'tab': 'bayarea',
        'headers': ['*Name', 'Address', '*City', 'State', 'Phone'],
        'show': ['name', 'address', 'city', 'state', 'phone'],
        'sort': 'name',
        'lastsort': 'name',
        'links': {
            'name': 'url:url',
            'address': 'map:address,city,state',
            'edit': 'edit:id',
        },
    },
    'mag': {
        'mags': config.FLAG_BOOK_MAGAZINE,
        'tab': 'book',
        'headers': ['*Editor', '*Title', '*Publisher', '*First Year'],
        'show': ['editor', 'title', 'publisher', 'year'],
        'sort': 'title',
        'lastsort': 'title',
        'links': {
            'title': 'issues:id',
            'edit': 'edit:id',
        },
    },
    'issues': {
        'tab': 'periodical',
        'headers': ['*Volume', 'Issue', '*Date', 'Pages'],
        'show': ['volume', 'issue', 'date', 'pages'],
        'sort': 'date',
        'lastsort': 'date',
        'links': {
        },
    },
}


# links (both site links and map links) aren't working.
@basics.web_page
def biblio(pif):
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append(pif.request_uri, pif.ren.title)

    def pic_formatter(x):
        img = pif.ren.find_image_file([str(y) for y in x])
        return ('/' + '/'.join(pif.ren.find_image_file([str(y) for y in x]))) if ''.join(img) else ''

    row_link_formatters = {
        'map': lambda x: '' if '' in x else (map_url + ','.join(x)).replace(' ', '+'),
        'url': lambda x: x[0],
        'pic': pic_formatter,
        'issues': lambda x: f'biblio.cgi?page=issues&id={x[0]}',
    }

    period_id = pif.form.get_str('id') if pif.page_id == 'mag' else None
    if period_id:
        # crumb
        pass

    pif.ren.print_html()

    page_info = biblios.get(pif.page_name, {})
    sections = pif.dbh.fetch_sections({'page_id': pif.page_id})
    lsection = render.Section(section=sections[0] if sections else None)
    tab_name = page_info.get('tab', pif.page_name)
    row_links = page_info.get('links', {})
    print(pif.page_id, tab_name)

    wheres = [f'flags&{config.FLAG_ITEM_HIDDEN}=0']
    if page_info.get('mags') is not None:
        wheres.append(f'flags&{config.FLAG_BOOK_MAGAZINE}={page_info["mags"]}')
    if period_id:
        wheres.append(f'pub_id={period_id}')
    # period
    table = pif.dbh.depref(tab_name, pif.dbh.fetch(tab_name, where=wheres, tag='Biblio', verbose=True))

    lrange = render.Range(entry=list())
    lsection.range = [lrange]

    editable = pif.form.get_bool('edit') and pif.is_allowed('a')
    if editable:
        lsection.colist.append('edit')
        lsection.headers['edit'] = '&nbsp;'
        row_link_formatters['edit'] = lambda x: (
            '%s/cgi-bin/editor.cgi?table=%s&id=%s' % (pif.secure_host, tab_name, x[0]))
    for key, hdr in zip(page_info['show'], page_info['headers']):
        if hdr.startswith('*'):
            hdr = hdr[1:]
            hdr = f'<a href="biblio.cgi?page={pif.page_name}&sort={key}">{hdr}</a>'
        lsection.colist.append(key)
        lsection.headers[key] = hdr

    sortkey = []
    this_sort = pif.form.get_str('sort', page_info.get('sort'))
    if this_sort:
        if this_sort.isdigit():
            this_sort = max(0, min(len(lsection.colist) - 1, int(this_sort)))
            this_sort = lsection.colist[this_sort]
        sortkey.append(this_sort)
    if page_info.get('lastsort') and page_info['lastsort'] not in sortkey:
        sortkey.append(page_info['lastsort'])
    if sortkey:
        table.sort(key=lambda x: [x[y] for y in sortkey if y in lsection.colist])

    def bib_field(fdict, field):
        cont = str(fdict.get(field, '&nbsp'))
        url = ''
        if field in row_links:
            if field == 'edit':
                cont = str(fdict['id'])
            cmd, arg = row_links[field].split(':')
            arg = [str(fdict.get(x, getattr(lsection, x, ''))) for x in arg.split(',')]
            if ''.join(arg):
                url = row_link_formatters[cmd](arg)

        edlink = ''
        if field == 'title' and editable:
            if os.path.exists('.' + config.IMG_DIR_BOOK + '/' + fdict['pic_id'] + '.jpg'):
                edlink += (' ' + pif.ren.format_link('/cgi-bin/imawidget.cgi?d=.%s&f=%s' % (
                    config.IMG_DIR_BOOK, fdict['pic_id'] + '.jpg'), pif.ren.fmt_mini(icon='paintbrush')))
            edlink += (' ' + pif.ren.format_link('/cgi-bin/upload.cgi?d=.%s&n=%s' % (
                config.IMG_DIR_BOOK, fdict['pic_id'] + '.jpg'), pif.ren.fmt_mini(icon='upload')))

        return pif.ren.format_link(url, cont) + edlink

    lrange.entry = [{field: bib_field(fdict, field) for field in lsection.colist} for fdict in table]
    pif.ren.set_button_comment(pif)
    return pif.ren.format_template('simplelistix.html', llineup=render.Listix(section=[lsection]))


# -- calendar


def event_type(pif, event):
    return '<center><b>%s</b></center>' % pif.ren.format_image_icon('i_' + event, event.upper())


def event(pif, ty, llist):
    return [event_type(pif, ty),
            llist.get_arg('&nbsp;').replace(';', '<br>'),
            llist.get_arg('&nbsp;').replace(';', '<br>'),
            llist.get_arg('&nbsp;').replace(';', '<br>')]


@basics.web_page
def calendar(pif):
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append(pif.request_uri, 'Calendar')
    pif.ren.print_html()

    dblist = bfiles.SimpleFile(os.path.join(config.SRC_DIR, pif.page_name + '.dat'))

    lrange = None
    lsection = render.Section()
    llistix = render.Listix(section=[lsection])

    for llist in dblist:

        cmd = llist.get_arg()

        if (cmd == 'h'):
            for iarg in range(1, llist.args()):
                arg = llist.get_arg('&nbsp;')
                lsection.colist.append(arg)
                lsection.headers[arg] = arg

        elif (cmd == 'm'):
            lrange.entry.append(dict(zip(lsection.colist, event(pif, 'meet', llist))))

        elif (cmd == 's'):
            lrange.entry.append(dict(zip(lsection.colist, event(pif, 'show', llist))))

        elif (cmd == 'n'):
            if lrange:
                lsection.range.append(lrange)
            lrange = render.Range(entry=list(), name=llist.get_arg('&nbsp;', 1))

        elif (cmd == 'e'):
            if lrange:
                lsection.range.append(lrange)
            lrange = None

    if lrange:
        lsection.range.append(lrange)

    return pif.ren.format_template('simplelistix.html', llineup=llistix)


@basics.web_page
def submit_comment(pif):
    if pif.method == 'GET':
        raise useful.Redirect('../pages/comment.php')
    pif.ren.print_html()
    print(pif.ren.format_head())
    # useful.write_message(pif.form)
    ostr = "I am sending this comment for you. "

    mysubject = pif.form.get_str('mysubject')
    mycomment = pif.form.get_str('mycomment')
    myname = pif.form.get_str('myname')
    myemail = pif.form.get_str('myemail')
    credit = pif.form.get_str('credit')
    fname = pif.form.get_str('pic.name')
    fimage = pif.form.get('pic')
    if isinstance(fimage, list):
        fimage = b''.join([x for x in fimage if x])
    pif.form.delete('pic')

    def comment_error(msg):
        return "<dl><dt>ERROR</dt><dd>%s</dd></dl>" % msg

    if myemail and '@' not in myemail:
        return comment_error('Badly formatted email address.  Try again.')

    pif.form.change_key('page', 'page_id')
    fn = "../../comments/comment." + datetime.datetime.now().strftime('%Y%m%d.%H%M%S')

    if any([x in y for x in ('http://', 'https://') for y in (mysubject, mycomment, myemail)]):
        return comment_error(
            "Whoa there.  This isn't for submitting links.  Please use the SUGGEST A LINK feature from the link list.")

    ostr += "<dl><dt>My Subject</dt><dd>" + mysubject + "</dd>\n"
    ostr += "<dl><dt>My Comment</dt><dd>" + mycomment + "</dd>\n"
    ostr += "<dt>My Name</dt><dd>" + myname + "</dd>\n"
    ostr += "<dt>My Email</dt><dd>" + myemail + "</dd></dl>\n"

    if fimage:
        ostr += "<dt>Relevant File</dt><dd>" + fname + "<br>\n"
        direc = config.INC_DIR
        descriptions_file = config.LOG_ROOT + '/descr.log'
        dest_filename = images.get_next_upload_filename()
        dest_filename = useful.file_save(direc, dest_filename, fimage)
        images.file_log(direc + '/' + dest_filename, direc)

        cred = who = comment = '-'
        if mycomment:
            comment = mbdata.multi_spaces_re.sub(' ', mycomment)
        if credit:
            cred = mbdata.multi_spaces_re.sub(' ', credit)
        if myname:
            who = mbdata.multi_spaces_re.sub(' ', myname)
        open(descriptions_file, 'a+').write('\t'.join([dest_filename, '-', '-', '-', comment, cred, who]) + '\n')
        ostr = '<div class="warning">Thank you for submitting that file.</div><br>\n'

        ostr += "</dd></dl>\n"

    fh = open(fn, "wt")
    fh.write("_POST\n\n" + pprint.pformat(pif.form, indent=2, width=132) + "\n\n")
    fh.write("REMOTE_ADDR=" + os.getenv('REMOTE_ADDR') + "\n")
    ostr += "Thanks for sending that.  Now please use the BACK button on your browser to return to where you were."
    return ostr


@basics.web_page
def counts_main(pif):
    pif.ren.title = 'Site Counts'
    pif.ren.print_html()
    counts = pif.dbh.fetch_counts()
    v = {c['model_type']: c['count'] for c in counts[1]}
    for c in counts[0]:
        c['name'] = mbdata.model_type_names[c['model_type']]
        c['type'] = mbdata.model_types[c['model_type']]
        c['vars'] = v.get(c['model_type'], 0)

    things = []
    for mt in sorted(set(mbdata.model_types.values())):
        section = render.Section(
            name=mt,
            colist=['name', 'count', 'vars'],
            headers={'name': 'Model Type', 'count': 'Count', 'vars': 'Variations'},
            range=[render.Range(entry=[x for x in counts[0] if x['type'] == mt])],
        )
        tot = sum([x['count'] for x in section.range[0].entry])
        vc = sum([x['vars'] for x in section.range[0].entry])
        section.range[0].entry.append({'name': 'total', 'count': tot, 'vars': vc})
        if tot:
            things.append(section)
    return pif.ren.format_template('simplelistix.html', llineup=render.Listix(section=things))
