#!/usr/local/bin/python

import os, sys, urllib2
import basics
import config
import mbdata
import useful


# -- links

# main entry point for toylinks
@basics.web_page
def links(pif):
    pif.render.print_html()
    ostr = ''
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/cgi-bin/links.cgi', 'Toy Links')
    if pif.form.get_int('id'):
        link = pif.dbh.fetch_link_line(pif.form.get_int('id'))
	if link:
	    return single_link(pif, link[0])
    pif.render.set_page_extra(pif.render.reset_button_js)
    if pif.page_id != 'links.toylinks':
	pif.render.hierarchy_append('/cgi-bin/links.cgi?page=%s' % pif.page_id[6:], pif.render.title)
    return link_page(pif)


def single_link(pif, link):
    if link['page_id'] != 'links.toylinks':
	pif.render.hierarchy_append('/cgi-bin/links.cgi?page=%s' % pif.page_id[6:], pif.render.title)
    pif.render.hierarchy_append('', 'Specific Link')
    extra = ''
    if pif.is_allowed('m'):  # pragma: no cover
	extra = '- ' + pif.render.format_button("edit", "edlinks.cgi?id=%s" % link['id'])
    return pif.render.format_template('tlink.html', link=link, extra=extra)


def link_page(pif):
    section_id = useful.clean_id(pif.form.get_str('section'))
    if section_id:
        sections = pif.dbh.fetch_sections({'page_id': pif.page_id, 'id': section_id})
    else:
        sections = pif.dbh.fetch_sections({'page_id': pif.page_id})
    linklines = pif.dbh.fetch_link_lines(pif.page_id, not_flags=pif.dbh.FLAG_ITEM_HIDDEN)
    linklines = pif.dbh.depref('link_line', linklines)
    linklines.sort(key=lambda x: int(x['display_order']))
    sect_links = dict()
    for link in linklines:
        sect_links.setdefault(link['section_id'], list())
        sect_links[link['section_id']].append(link)

    llineup = {'id': pif.page_id, 'name': '', 'section': []}
    for lsec in sections:
        lsec['anchor'] = lsec['id']
        lsec['columns'] = 1
        lran = {'id': 'range', 'name': '', 'entry': list(generate_links(pif, sect_links.get(lsec['id'], [])))}
        lsec['range'] = [lran]
        llineup['section'].append(lsec)

    return pif.render.format_template('tlinks.html', llineup=llineup, sections=sections,
				      flags=pif.render.format_shown_flags())


def generate_links(pif, links):
    for ent in links:
        if ent['link_type'] != 'x' and not (ent['flags'] & pif.dbh.FLAG_LINK_LINE_NEW):
	    yield make_link(pif, ent)


def make_link(pif, ent):
    lnk = dict()
    lnk['text'], lnk['desc'] = format_entry(pif, ent)
    lnk['indent'] = (ent['flags'] & pif.dbh.FLAG_LINK_LINE_INDENTED) != 0
    lnk['id'] = ent['id']
    cmd = ent['link_type']
    lnk['comment'] = True
    if pif.is_allowed('m'):  # pragma: no cover
	if ent.get('last_status') == 'exc':
	    cmd = 'b'
    lnk['linktype'] = cmd # linktypes.get(cmd)
    lnk['large'] = ent['flags'] & pif.dbh.FLAG_LINK_LINE_FORMAT_LARGE
    return lnk


def format_entry(pif, ent):
    dictFlag = {
            '': ('o', pif.render.format_image_art('wheel.gif', also={'class': 'dlm'})),
            'Reciprocal': ('Reciprocal', '<i class="fas fa-refresh dlm"></i>'),
            'PayPal': ('Accepts PayPal', '<i class="fab fa-paypal dlm"></i>'),
    }
    is_large = ent['flags'] & pif.dbh.FLAG_LINK_LINE_FORMAT_LARGE
    url = ent['url']
    tag = ent['name']
    dlms = []
    if ent['country']:
        dlms.append(ent['country'])
    cmt = ent['description']
    if ent['flags'] & pif.dbh.FLAG_LINK_LINE_RECIPROCAL:
        dlms.append('Reciprocal')
    if ent['flags'] & pif.dbh.FLAG_LINK_LINE_PAYPAL:
        dlms.append('PayPal')

    ostr = pif.render.format_link(url, tag) + ' '

    if not dlms and not cmt:
        pass
    elif not dlms:
        # add name
        if not is_large:
            ostr += format_delimiter(pif, dictFlag[''])
    else:
        also = {'class': 'dlm'}
        for dlm in dlms:
            flag = pif.render.show_flag(dlm)
            if flag:
                ostr += useful.img_src(flag[1], also={'class': 'dlm'})
            else:
                ostr += format_delimiter(pif, dictFlag[dlm])
#    if cmt and is_large:
#       ostr += '<br>' + '<br>'.join(cmt.split('|'))
#    else:
#       ostr += cmt
    return ostr, cmt.split('|')


def format_delimiter(pif, dlm):
    return dlm[1] + ' '
    also = {'class': 'dlm', 'alt': '[' + dlm[0] + ']'}
    pif.render.comment('format_delimiter', dlm)
    return useful.img_src(dlm[1], also=also) + ' '


# -- addlink


def read_config(pif, showall=False):
    listCats = []
    listIndices = []
    listRejectCats = []
    dictCats = {}
    allpages = pif.dbh.fetch_pages("id like 'links.%'")
    if pif.is_allowed('a'):  # and pif.render.is_beta:  # pragma: no cover
        showpage = {x['page_info.id']: 1 for x in allpages}
    else:
        showpage = {x['page_info.id']: not (x['page_info.flags'] & pif.dbh.FLAG_PAGE_INFO_HIDDEN) for x in allpages}
    sections = pif.dbh.fetch_sections(where="page_id like 'links.%'")
    for section in sections:
        page_name = section['section.page_id'].split('.', 1)[1]
        if page_name not in listIndices:
            listIndices.append(page_name)
        if showpage[section['section.page_id']]:
            listCats.append((section['section.id'], section['section.name']))
        if section['section.page_id'] in ['links.rejects', 'links.trash']:
            listRejectCats.append((section['section.id'], section['section.name']))
        dictCats[section['section.id']] = page_name
    return listCats, listIndices, dictCats, listRejectCats


def read_blacklist(pif):
    blacklist = pif.dbh.fetch_blacklist()
    reject = [x['blacklist.target'] for x in filter(lambda x: x['blacklist.reason'] == 'site', blacklist)]
    banned = [x['blacklist.target'] for x in filter(lambda x: x['blacklist.reason'] == 'ip', blacklist)]
    return reject, banned


def is_blacklisted(url, rejects):
    for reject in rejects:
        if url.find(reject) >= 0:
            return reject
    return ''


def fix_url(url):
    url = url.lower()
    if url[-1] == '/':
        url = url[:-1]
    return url


def read_all_links(pif):
    highest_disp_order = {}
    all_links = []
    for section in pif.dbh.fetch_sections(where="page_id like 'links%'"):
        highest_disp_order.setdefault((section['section.page_id'], section['section.id']), 0)
    for link in pif.dbh.fetch_link_lines():
        link = pif.dbh.depref('link_line', link)
        highest_disp_order.setdefault((link['page_id'], link['section_id']), 0)
        if link['display_order'] > highest_disp_order[(link['page_id'], link['section_id'])]:
            highest_disp_order[(link['page_id'], link['section_id'])] = link['display_order']
        if link['url'] and link['link_type'] in 'lsx':
            all_links.append(fix_url(link['url']))
    return all_links, highest_disp_order



def add_new_link(pif, dictCats, listRejects):
    reasons = []
    ostr = "<hr>"
    #'columns': ['id', 'page_id', 'section_id', 'display_order', 'flags', 'link_type', 'country', 'url', 'name', 'description', 'note'],
    all_links, highest_disp_order = read_all_links(pif)
    link = {}
    try:
        link['url'] = url = pif.form.get_str('url', '')
        link['section_id'] = pif.form.get_str('cat', '')
        link['page_id'] = 'links.' + dictCats[link['section_id']]
        link['display_order'] = highest_disp_order[(link.get('page_id', 'unknown'), link.get('section_id', 'unknown'))] + 1
    except:
        reasons.extend([
            "Some information was missing.",
            "The request was badly formed.",
            "The request was not made by the supplied web form."])

    link['flags'] = pif.dbh.FLAG_LINK_LINE_NEW
    if pif.is_allowed('a'):  # pragma: no cover
        link['flags'] = 0
    link['link_type'] = 'l'
    link['name'] = pif.form.get_str('name', '')
    link['country'] = pif.form.get_str('country', '')
    link['description'] = pif.form.get_str('desc', '')
    link['note'] = pif.remote_addr + '/' + pif.remote_host + '. ' + pif.form.get_str('note', '')

    url = fix_url(url)
    for reject in listRejects:
        if url.find(reject) >= 0:
            reasons.append("The URL is on a banned list.")
    if url in all_links and not pif.form.get('dup'):
        reasons.append("The site has already been submitted.")
    if url.find('://') < 0:
        reasons.append("The URL is not properly formed.")
    if (link['description'].find('<') >= 0) or (link['name'].find('<') >= 0):
        reasons.extend("The description text or the notes text contains HTML.")
    if (link['description'].find('\n') >= 0) or (link['name'].find('\n') >= 0):
        reasons.extend([
            "The request was badly formed.",
            "The request was not made by the supplied web form."])

    if link['country'] == 'US':
        link['country'] = ''
    #str = 'l|' + url + '|' + tag + '|' + dlm + '|' + cmt

    if reasons:
        ostr += "<b>The site submitted is being rejected.  Sorry.</b><br>\n"
        ostr += "Possible reason%s:<ul>\n" % useful.plural(reasons)
        for reason in reasons:
            ostr += "<li>" + reason + '\n'
        ostr += "</ul>If your submission has to do with sex, drugs, hotel reservations or ringtones, please go away and never come back.  Seriously.<p>\n"
        ostr += "Feel free to use your browser's BACK button to fix your entry, then resubmit; or,\n"
        ostr += "if you think this rejection was in error, you can send email.  Just don't hope for too much.\n"
        open(os.path.join(config.LOG_ROOT, 'trash.log'), 'a+').write(str(link) + '\n')
    else:
        link['id'] =  pif.dbh.insert_link_line(link)
        ostr += "The following has been added to the list:<br><ul>\n"
        ent = format_entry(pif, link)
        ostr += ent[0] + ' '
        ostr += '<br>' .join(ent[1])
        ostr += '\n</ul>\n'
	check_link(pif, link)
    return ostr


# main routine for addlink
@basics.web_page
def add_page(pif):
    pif.render.print_html()
    pif.render.set_page_extra(pif.render.reset_button_js)

    rejected, blacklist = read_blacklist(pif)
    for l in blacklist:
        if os.environ.get('REMOTE_ADDR') == l:
            raise useful.SimpleError("You have been banned from using this service because of previous abuses.  If you have a problem with this, contact us via email, but don't hope for much.")

    listCats, listIndices, dictCats, listRejectCats = read_config(pif)

    lnk = add_new_link(pif, dictCats, rejected) if pif.form.get_str('url') else ''

    context = {
	'categories': listCats,
        'countries': mbdata.countries,
	'link': lnk,
    }
    return pif.render.format_template('tlinkadd.html', **context)


# -- edlinks


link_type_names = [
    ('b', 'bad'),
    ('f', 'folder'),
    ('g', 'graphic'),
    ('l', 'normal'),
    ('n', 'none'),
    ('p', 'button'),
    ('s', 'star'),
    ('t', 'text'),
    ('x', 'trash'),
]

flag_check_names = [
    ('01', 'New'),
    ('02', 'Recip'),
    ('04', 'Paypal'),
    ('08', 'Indent'),
    ('10', 'Large'),
    ('20', 'NoVer'),
    ('40', 'Assoc'),
]

def edit_single(pif):
    listCats, listIndices, dictCats, listRejectCats = read_config(pif, True)
    #listCats.append(('single', 'single'))
    table_info = pif.dbh.table_info['link_line']
    link_id = pif.form.get_str('id')
    if pif.form.get_bool('save'):
        all_links, highest_disp_order = read_all_links(pif)
        nlink = {x: pif.form.get_str(x) for x in table_info['columns']}
        nlink['flags'] = 0
        if pif.form.get_str('section_id') == 'single':
            pass
        else:
            nlink['page_id'] = 'links.' + dictCats.get(pif.form.get_str('section_id', ''), pif.form.get_str('section_id', ''))
        nlink['display_order'] = highest_disp_order.get((nlink['page_id'], nlink['section_id']), 0) + 1
        for flag in pif.form.get_list('flags'):
            nlink['flags'] += int(flag, 16)
        if nlink['flags'] & pif.dbh.FLAG_LINK_LINE_NOT_VERIFIABLE:
            nlink['last_status'] = 'NoVer'
        pif.dbh.update_link_line(nlink)
        pif.render.message('<br>record saved<br>')
    elif pif.form.get_bool('test'):
        link = pif.dbh.fetch_link_line(link_id)[0]
        check_link(pif, link)  # don't care about blacklist here, just actual check
    elif pif.form.get_bool('delete'):
        pif.dbh.delete_link_line(link_id)
        return "<br>deleted<br>"
    elif pif.form.get_bool('reject'):
        nlink = {x: pif.form.get_str(x, '') for x in table_info['columns']}
        nlink['page_id'] = 'links.rejects'
        nlink['display_order'] = 1
        nlink['section_id'] = pif.form.get_str('rejects_sec')
        nlink['flags'] = 0
        pif.dbh.update_link_line(nlink)
        pif.render.message('<br>record rejected<br>')
    elif pif.form.get_bool('add'):
        link_id = (#pif.dbh.insert_link_line({'page_id': pif.form.get_str('page_id', ''), 'section_id': pif.form.get_str('sec')})
#        pif.form.set_val('id',
	    pif.dbh.insert_link_line({'page_id': pif.form.get_str('page_id'), 'country': '', 'flags': 1, 'link_type': 'l'}))

    links = pif.dbh.fetch_link_lines(where="id='%s'" % link_id)
    if not links:
	raise useful.SimpleError("That ID wasn't found.")
    link = links[0]
    asslinks = [(0, '')] + [(x['link_line.id'], x['link_line.name']) for x in pif.dbh.fetch_link_lines(flags=pif.dbh.FLAG_LINK_LINE_ASSOCIABLE)]
    descs = pif.dbh.describe_dict('link_line')

    header = '<form>' + pif.create_token()
    header += '<input type="hidden" name="o_id" value="%s">\n' % link['link_line.id']

    entries = []
    for col in table_info['columns']:
	col_long = 'link_line.' + col
	coltype = descs.get(col).get('type', 'unknown')
	value = useful.printablize(link.get(col_long, ''))
	entries.append({'text': col})
#	entries.append({'text': '<a href="%s">%s</a>' % (link.get(col_long, ''), link.get(col_long, ''))
#			if col == 'url' else link[col_long]})
	entries.append({'text': '<a href="%s">%s</a>' % (value, value) if col == 'url' else value})
	if col in table_info.get('readonly', []):
	    cell = '&nbsp;<input type="hidden" name="%s" value="%s">' % (col, value)
#       elif col == 'page_id':
#           cell = '&nbsp;<input type="hidden" name="%s" value="%s">' % (col, value)
	elif col == 'section_id':
	    cell = pif.render.format_select('section_id', listCats, selected=value, blank='Please choose one from the list')
	elif col == 'flags':
	    cell = pif.render.format_checkbox("flags", flag_check_names, useful.bit_list(link[col_long]))
	elif col == 'country':
	    cell = pif.render.format_select_country('country', value)
	elif col == 'link_type':
	    cell = pif.render.format_select(col, link_type_names, selected=value)
	elif col == 'associated_link':
	    cell = pif.render.format_select(col, asslinks, selected=value)
	elif coltype.startswith('varchar('):
	    colwidth = int(coltype[8:-1])
	    cell = pif.render.format_text_input(col, colwidth, 64, value=value)
	elif coltype.startswith('int('):
	    if link[col_long] is None:
		value = 0
	    colwidth = int(coltype[4:-1])
	    cell = pif.render.format_text_input(col, colwidth, value=value)
	else:
	    cell = coltype
	entries.append({'text': cell})

    footer = ''.join([
	pif.render.format_button_input("save"),
	pif.render.format_button_input("delete"),
	pif.render.format_button_input("test"),
	pif.render.format_button_input("reject"),
	pif.render.format_select('rejects_sec', listRejectCats, blank='Please choose one from the list'),
	'</form>',
	pif.render.format_button("edit", link=pif.dbh.get_editor_link('link_line', {'id': link_id})),
    ])

    llineup = {'id': 'tl', 'name': 'Edit Link', 'columns': 3, 'widthauto': True,
	'section': [{'id': 's', 'name': '',
	    'range': [{'entry': entries}]}],
	'header': header, 'footer': footer,
    }
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('simplematrix.html', llineup=llineup)


def edit_multiple(pif):
    table_info = pif.dbh.table_info['link_line']
    page_id = ''
    sec_id = pif.form.get_str('sec', '')
    if pif.form.get_bool('as'):
        linklines = pif.dbh.fetch_link_lines(flags=pif.dbh.FLAG_LINK_LINE_ASSOCIABLE, order="display_order")
    elif sec_id == 'new':
        linklines = pif.dbh.fetch_link_lines(flags=pif.dbh.FLAG_LINK_LINE_NEW)
    elif sec_id == 'nonf':
        linklines = pif.dbh.fetch_link_lines(where="last_status is not Null and last_status != 'H200' and link_type in ('l','s') and page_id != 'links.rejects' and page_id != 'links.trash' and (flags & 32)=0")
    elif pif.form.get_str('stat'):
	if pif.form.get_str('stat') == 'None':
	    linklines = pif.dbh.fetch_link_lines(where="last_status is NULL", order='id')
	else:
	    linklines = pif.dbh.fetch_link_lines(where="last_status='%s'" % pif.form.get_str('stat'), order='id')
    elif sec_id:
        linklines = pif.dbh.fetch_link_lines(where="section_id='%s'" % sec_id, order="display_order")
        section = pif.dbh.fetch_section(sec_id)
        page_id = section['page_id']
    else:
        linklines = pif.dbh.fetch_link_lines(where="page_id='%s'" % pif.form.get_str('page'), order="display_order")
    pif.render.message(len(linklines), 'lines')

    entries = [{'text': col} for col in table_info['columns']]
    for link in linklines:
	pif.dbh.depref('link_line', link)
	for col in table_info['columns']:
	    val = link.get(col, '')
	    if col == 'id':
		entries.append({'text': '<a href="?id=' + str(val) + '">' + str(val) + '</a>'})
	    elif col == 'url':
		entries.append({'text': '<a href="%s">%s</a>' % (val, val)})
	    else:
		entries.append({'text': useful.printablize(val)})
    footer = pif.render.format_button("add", "edlinks.cgi?page_id=%s&sec=%s&add=1" % (page_id, sec_id))

    llineup = {'id': 'tl', 'name': 'Edit Link', 'columns': len(table_info['columns']),
	'section': [{'id': 's', 'name': '',
	    'range': [{'entry': entries}]}],
	'footer': footer,
    }
    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('simplematrix.html', llineup=llineup)


def edit_choose(pif):
    reasons = {
	'None': '(Untested)',
	'H200': '(Good)',
	'H302': '(Moved)',
	'H400': '(Bad Request)',
	'H403': '(Forbidden)',
	'H404': '(Not Found)',
	'H410': '(Gone)',
	'H418': '(Teapot)',
	'H429': '(Too Many Reqs)',
	'H500': '(Internal Error)',
	'H502': '(Bad Gateway)',
	'H503': '(Unavailable)',
	'NoVer': '(Ignored)',
	'U1': '(Bad Cert)',
	'U60': '(Timeout)',
	'U61': '(Conn Refused)',
	'U65': '(No Route)',
	'U8': '(No DNS)',
	'exc': '(Exception)',
    }
    link_statuses = pif.dbh.fetch_link_statuses()
    link_statuses = {str(x['last_status']): x['count(*)'] for x in link_statuses}
    #'link_statuses': ["%s (%s)" % (x, reasons.get(x, 'Unknown')) for x in sorted(pif.dbh.fetch_link_statuses())],
    context = {
	'sections': sorted(pif.dbh.fetch_sections(where="page_id like 'links%'"),
			key=lambda x: x['section.page_id']),
	'blacklist': pif.dbh.get_editor_link('blacklist', {}),
	'link_statuses': link_statuses,
	'reasons': reasons,
    }
    return pif.render.format_template('tlinkcats.html', **context)


# main entry point for links editor
@basics.web_page
def edit_links(pif):
    pif.render.print_html()
    if pif.form.get_str('id') or pif.form.get_bool('add'):
	return edit_single(pif)
    elif pif.form.has_any(['as', 'sec', 'stat', 'page']):
	return edit_multiple(pif)
    else:
	return edit_choose(pif)

# -- link checker

def check_links(pif, sections=None, reject=[], retest=False, visible=False):
    pif.dbh.set_verbose(True)
    for sec in sections if sections else [None]:
        pif.dbh.clear_link_line_statuses(section=sec, where='last_status != "H200"' if retest else '')
        links = pif.dbh.fetch_link_lines(section=sec, where='last_status is NULL' if retest else '', order='id')
        for link in links:
	    if not retest or link['link_line.page_id'] != 'links.rejects':
		check_link(pif, link, reject, visible=visible)


def check_link(pif, link, rejects=[], visible=False):
    if link:
	print link, visible
        link = pif.dbh.depref('link_line', link)
        lstatus = 'unset'
	if visible and (link['flags'] & pif.dbh.FLAG_LINK_LINE_HIDDEN or link['page_id'] == 'links.rejects'):
	    return
        print link['id'], link['url'],
        if link['flags'] & pif.dbh.FLAG_LINK_LINE_NOT_VERIFIABLE or link['link_type'] in 'tfpn':
            lstatus = 'NoVer'
        elif link['link_type'] in 'bglsx':
#            ret = is_blacklisted(link['url'], rejects)
#            if ret:
#                print link['id'], link['section_id'], link['url'], "BLACKLISTED", ret
                #pif.dbh.dbi.remove('link_line', 'id=%s' % link['id'])
	    lurl = link['url']
	    if lurl.startswith('/'):
		lurl = 'https://www.bamca.org' + lurl
            try:
		url = urllib2.urlopen(urllib2.Request(lurl, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0'}))
                lstatus = 'H' + str(url.code)
            except urllib2.HTTPError as (c):
                print 'http error:', c.code
                lstatus = 'H' + str(c.code)
            except urllib2.URLError as (c):
                print 'url error:', c.reason
                lstatus = 'U' + str(c.reason[0])
            except:
                lstatus = 'exc'
        print lstatus
	if link.get('last_status') != lstatus:
	    pif.dbh.update_link_line({'id': str(link['id']), 'last_status': lstatus})

# ---- ----------------------------------------------------

def check_blacklisted_links(pif, sections=None):
    reject, banned = links.read_blacklist(pif)
    pif.dbh.set_verbose(True)
    for sec in sections if sections else [None]:
        for link in pif.dbh.fetch_link_lines(section=sec):
            link = pif.dbh.depref('link_line', link)
            if link['link_type'] in 'blsxg':
                ret = is_blacklisted(link['url'], reject)
                if ret:
                    print link['id'], link['section_id'], link['url'], "BLACKLISTED", ret
                    #pif.dbh.dbi.remove('link_line', 'id=%s' % link['id'])


def update_links(pif):
    links = pif.dbh.fetch_link_lines()
    good_ids = [x for x in range(100, 3000)]
    bad_ids = []
    for lnk in links:
	id = lnk['link_line.id']
	if id in good_ids:
	    good_ids.remove(id)
	elif id < 100 and not lnk['link_line.flags'] & 64:
	    bad_ids.append(id)
    bad_ids.sort()
    for ids in zip(good_ids, bad_ids):
	print "update link_line set id=%d where id=%d;" % ids


def cl_check_links(pif, *filelist):
    retest = visible = False
    if 'retest' in filelist:
	retest = True
	filelist.remove('retest')
    if 'visible' in filelist:
	visible = True
	filelist.remove('visible')
    check_links(pif, filelist, retest=retest, visible=visible)


cmds = [
    ('u', update_links, "update"),
    ('c', cl_check_links, "check"),
    ('b', check_blacklisted_links, 'check blacklist'),
]

@basics.command_line
def commands(pif):
    useful.cmd_proc(pif, './tlinks.py', cmds)

# ---- ----------------------------------------------------

if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='')
