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
        if link['page_id'] != 'links.toylinks':
            pif.render.hierarchy_append('/cgi-bin/links.cgi?page=%s' % pif.page_id[6:], pif.render.title)
        pif.render.hierarchy_append('', 'Specific Link')
        ostr += pif.render.format_head()
        ostr += single_link(pif, link)
        ostr += pif.render.format_tail()
    else:
        if pif.page_id != 'links.toylinks':
            pif.render.hierarchy_append('/cgi-bin/links.cgi?page=%s' % pif.page_id[6:], pif.render.title)
        ostr += pif.render.format_head()
        ostr += link_page(pif)
        ostr += pif.render.format_tail()
    return ostr


def single_link(pif, link):
    ostr  = 'Do you have a comment about this link?  Please send it to us.\n'
    ostr += '<form action="../pages/comment.php" method="post" name="comment">\n'
    ostr += '''
<table>
<tr><td>My Subject</td><td><input type="text" name="mysubject" size=80 maxlength=80></td></tr>
<tr><td>My Comment</td><td><textarea name="mycomment" cols=80 rows=6></textarea></td></tr>
<tr><td>My Name</td><td><input type="text" name="myname" size=80 maxlength=80> (optional)</td></tr>
<tr><td>My E-mail Address</td><td><input type="text" name="myemail" size=80 maxlength=80> (optional)</td></tr>
</table>
'''
    ostr += pif.render.format_button_input() + ' - '
    ostr += pif.render.format_button_reset('comment') + '\n'
    ostr += '</form>\n'
    if pif.is_allowed('a'):  # pragma: no cover
        ostr += pif.render.format_button("edit_this_page", link=pif.dbh.get_editor_link('link_line', {'id': pif.form.get_str('id', '')}), also={'class': 'comment'}, lalso={})
    ostr += '<br>' + str(link) + '<br>'
    return ostr


def link_page(pif):
    section_id = pif.form.get_str('section')
    if section_id:
        sections = pif.dbh.fetch_sections({'page_id': pif.page_id, 'id': section_id})
    else:
        sections = pif.dbh.fetch_sections({'page_id': pif.page_id})
    sections = pif.dbh.depref('section', sections)
    linklines = pif.dbh.fetch_link_lines(pif.page_id)
    linklines = pif.dbh.depref('link_line', linklines)
    linklines.sort(key=lambda x: int(x['display_order']))
    sect_links = dict()
    for link in linklines:
        sect_links.setdefault(link['section_id'], list())
        sect_links[link['section_id']].append(link)

    llineup = {'id': pif.page_id, 'name': '', 'section': []}
    for lsec in sections:
        lsec.update({'anchor': lsec['id'], 'columns': 1})
        lran = {'id': 'range', 'name': '', 'entry': generate_links(pif, sect_links.get(lsec['id'], []))}
        lsec['range'] = [lran]
        llineup['section'].append(lsec)

    return pif.render.format_links(llineup) + '\n' + end_of_page(pif)


def generate_links(pif, links):
    for ent in links:
        if ent['link_type'] != 'x' and not (ent['flags'] & pif.dbh.FLAG_LINK_LINE_NEW):
            lnk = dict()
            lnk['text'], lnk['desc'] = format_entry(pif, ent)
            lnk['indent'] = (ent['flags'] & pif.dbh.FLAG_LINK_LINE_INDENTED) != 0
            lnk['id'] = ent['id']
            cmd = ent['link_type']
            if pif.is_allowed('m'):  # pragma: no cover
                lnk['comment'] = True
                if ent.get('last_status') == 'exc':
                    cmd = 'b'
            lnk['linktype'] = linktypes.get(cmd)
            lnk['large'] = ent['flags'] & pif.dbh.FLAG_LINK_LINE_FORMAT_LARGE
            yield lnk


# the grafic for each of these, if any
linktypes = {
    'b': 'bad',
    'f': 'folder',
    'g': '',  #graphic
    'l': 'ball',
    'p': '',  #button
    's': 'star',
    't': '',  #text
    'x': 'trash',  #trash
}

def format_entry(pif, ent):
    dictFlag = {
            '': ('o', pif.render.find_art('wheel.gif')),
            'Reciprocal': ('Reciprocal', pif.render.find_art('recip.gif')),
            'PayPal': ('Accepts PayPal', pif.render.find_art('paypal.gif')),
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
                ostr += format_delimiter(pif, flag)
            else:
                ostr += format_delimiter(pif, dictFlag[dlm])
#    if cmt and is_large:
#       ostr += '<br>' + '<br>'.join(cmt.split('|'))
#    else:
#       ostr += cmt
    return ostr, cmt.split('|')


def format_delimiter(pif, dlm):
    also = {'class': 'dlm', 'alt': '[' + dlm[0] + ']'}
    pif.render.comment('format_delimiter', dlm)
    return useful.img_src(dlm[1], also=also) + ' '


def end_of_page(pif):
    ball = '%s\n' % pif.render.fmt_art('ball.gif', desc='o')
    ostr = '<hr>\n'
    ostr += '<center>This page is maintained by <em>Dean Dierschow</em>.<br>\n'
    ostr += '<nobr>%s Dean\'s Recommendations</nobr>\n' % pif.render.fmt_art('star.gif', desc='*')
    ostr += ball
    ostr += '<nobr>%s Reciprocal Link</nobr>\n' % pif.render.fmt_art('recip.gif')
    if pif.is_allowed('m'):  # pragma: no cover
        ostr += ball
        ostr += '<nobr>%s Comment on this link</nobr>\n' % pif.render.fmt_art('comment.gif')
    ostr += '</center>\n'
    return ostr


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
        showpage = {x['page_info.id']: not (x['page_info.flags'] & pif.dbh.FLAG_PAGE_INFO_NOT_RELEASED) for x in allpages}
    sections = pif.dbh.fetch_sections(where="page_id like 'links.%'")
    for section in sections:
        page_name = section['section.page_id'].split('.', 1)[1]
        if page_name not in listIndices:
            listIndices.append(page_name)
        if showpage[section['section.page_id']]:
            listCats.append((section['section.id'], section['section.name']))
        if section['section.page_id'] == 'links.rejects':
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


def format_form(pif, listCats):
    ostr = '<form action="addlink.cgi" method="post" name="addlink">\n'
    ostr += pif.render.format_table_start()
    ostr += pif.render.format_row_start()
    ostr += pif.render.format_cell(0)
    ostr += pif.render.format_cell(1, 'Please enter the <b>full</b> URL (including the "http" part).')
    ostr += pif.render.format_row_end()
    ostr += pif.render.format_row_start()
    ostr += pif.render.format_cell(0, 'URL:')
    ostr += pif.render.format_cell(1, pif.render.format_text_input("url", 256, 64))
    ostr += pif.render.format_row_end()
    ostr += pif.render.format_row_start()
    ostr += pif.render.format_cell(0, 'Name:')
    ostr += pif.render.format_cell(1, pif.render.format_text_input("name", 256, 64))
    ostr += pif.render.format_row_end()
    ostr += pif.render.format_row_start()
    ostr += pif.render.format_cell(0, 'Description:')
    ostr += pif.render.format_cell(1, pif.render.format_text_input("desc", 256, 64) + ' (optional)')
    ostr += pif.render.format_row_end()
    ostr += pif.render.format_row_start()
    ostr += pif.render.format_cell(0, 'Country:')
    ostr += pif.render.format_cell(1, pif.render.format_select_country('country', ''))
    ostr += pif.render.format_row_end()
    ostr += pif.render.format_row_start()
    ostr += pif.render.format_cell(0, 'Category:')
    ostr += pif.render.format_cell(1, pif.render.format_select('cat', [('', 'Please choose one from the list')] + listCats, selected=''))
    ostr += pif.render.format_row_end()
    ostr += pif.render.format_row_start()
    ostr += pif.render.format_cell(0, 'Note to the webmaster (optional):', also={'colspan': 2})
    ostr += pif.render.format_row_end()
    ostr += pif.render.format_row_start()
    ostr += pif.render.format_cell(0)
    ostr += pif.render.format_cell(1, pif.render.format_text_input("note", 80, 80))
    ostr += pif.render.format_row_end()
    ostr += pif.render.format_row_start()
    ostr += pif.render.format_cell(0, '&nbsp;')
    ostr += pif.render.format_cell(1, pif.render.format_button_input("submit link") + pif.render.format_button_reset("addlink"))
    ostr += pif.render.format_row_end()
    ostr += pif.render.format_table_end()
    ostr += '</form>\n'
    return ostr


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
        if link['url'] and link['link_type'] in 'lnsx':
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
    if url in all_links:
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
        pif.dbh.insert_link_line(link)
        ostr += "The following has been added to the list:<br><ul>\n"
        ent = format_entry(pif, link)
        ostr += ent[0] + ' '
        ostr += '<br>' .join(ent[1])
        ostr += '\n</ul>\n'
	check_link(link)
	# TODO: Add auto-verification
    return ostr


# main routine for addlink
@basics.web_page
def add_page(pif):
    pif.render.print_html()

    rejected, blacklist = read_blacklist(pif)
    for l in blacklist:
        if os.environ.get('REMOTE_ADDR') == l:
            raise useful.SimpleError("You have been banned from using this service because of previous abuses.  If you have a problem with this, contact us via email, but don't hope for much.")

    print pif.render.format_head(extra=pif.render.reset_button_js)
    listCats, listIndices, dictCats, listRejectCats = read_config(pif)
    ostr = '''
You can now suggest links to be added to the ToyLinks page.  I will review them and move them to the approprate place.
Thanks for helping out!
<p><hr><p>
''' + format_form(pif, listCats) + '''
<p><hr><p>
Please submit only links that have something to do with toys or toy collecting.  Die-cast toys are of particular interest.
If you submit a site that has nothing to do with the subject material of this website, it will be summarily deleted.
Note that if your submission includes just gibberish in the name or description, it will be rejected without being checked.
'''
    if pif.form.get_str('url'):
        ostr += add_new_link(pif, dictCats, rejected)
    print ostr
    print pif.render.format_tail()



# -- edlinks


link_type_names = [
    ('b', 'bad'),
    ('f', 'folder'),
    ('g', 'graphic'),
    ('l', 'normal'),
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
        formflags = pif.form.get_list('flags')
        for flag in formflags:
            nlink['flags'] += int(flag, 16)
        if nlink['flags'] & pif.dbh.FLAG_LINK_LINE_NOT_VERIFIABLE:
            nlink['last_status'] = 'NoVer'
        pif.dbh.update_link_line(nlink)
        print '<br>record saved<br>'
    elif pif.form.get_bool('test'):
        link = pif.dbh.fetch_link_line(link_id)
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
        print '<br>record rejected<br>'
    elif pif.form.get_bool('add'):
        link_id = (#pif.dbh.insert_link_line({'page_id': pif.form.get_str('page_id', ''), 'section_id': pif.form.get_str('sec')})
#        pif.form.set_val('id',
	    pif.dbh.insert_link_line({'page_id': pif.form.get_str('page_id'), 'country': '', 'flags': 1, 'link_type': 'l'}))

    links = pif.dbh.fetch_link_lines(where="id='%s'" % link_id)
    if not links:
	raise useful.SimpleError("That ID wasn't found.")
    link = links[0]
    asslinks = [(0, '')] + [(x['link_line.id'], x['link_line.name']) for x in pif.dbh.fetch_link_lines(flags=pif.dbh.FLAG_LINK_LINE_ASSOCIABLE)]
    ostr = pif.render.format_table_start()
    ostr += '<form>\n<input type="hidden" name="o_id" value="%s">\n' % link['link_line.id']
    descs = pif.dbh.describe_dict('link_line')
    ostr += pif.render.format_table_start()
    for col in table_info['columns']:
        col_long = 'link_line.' + col
        coltype = descs.get(col).get('type', 'unknown')
        ostr += pif.render.format_row_start()
        ostr += pif.render.format_cell(0, col)
        if col == 'url':
            ostr += pif.render.format_cell(1, '<a href="%s">%s</a>' % (link.get(col_long, ''), link.get(col_long, '')))
        else:
            ostr += pif.render.format_cell(1, link[col_long])
        if col in table_info.get('readonly', []):
            ostr += pif.render.format_cell(1, '&nbsp;<input type="hidden" name="%s" value="%s">' % (col, link[col_long]))
#       elif col == 'page_id':
#           ostr += pif.render.format_cell(1, '&nbsp;<input type="hidden" name="%s" value="%s">' % (col, link[col_long]))
        elif col == 'section_id':
            ostr += pif.render.format_cell(1, pif.render.format_select('section_id', [('', 'Please choose one from the list')] + listCats, selected=link[col_long]))
        elif col == 'flags':
            ostr += pif.render.format_cell(1, pif.render.format_checkbox("flags", flag_check_names, useful.bit_list(link[col_long])))
        elif col == 'country':
            ostr += pif.render.format_cell(1, pif.render.format_select_country('country', link[col_long]))
        elif col == 'link_type':
            ostr += pif.render.format_cell(1, pif.render.format_select(col, link_type_names, selected=link[col_long]))
        elif col == 'associated_link':
            ostr += pif.render.format_cell(1, pif.render.format_select(col, asslinks, selected=link[col_long]))
        elif coltype.startswith('varchar('):
            colwidth = int(coltype[8:-1])
            ostr += pif.render.format_cell(1, pif.render.format_text_input(col, colwidth, 64, value=link[col_long]))
        elif coltype.startswith('int('):
            if link[col_long] is None:
                link[col_long] = 0
            colwidth = int(coltype[4:-1])
            val = link[col_long]
            if isinstance(val, str) and val.isdigit():
                val = str(int(val))
            elif not val:
                val = ''
            ostr += pif.render.format_cell(1, pif.render.format_text_input(col, colwidth, value=val))
        else:
            ostr += pif.render.format_cell(1, coltype)
        ostr += pif.render.format_row_end()
    ostr += pif.render.format_table_end()
    ostr += pif.render.format_button_input("save")
    ostr += pif.render.format_button_input("delete")
    ostr += pif.render.format_button_input("test")
    ostr += pif.render.format_button_input("reject")
    ostr += pif.render.format_select('rejects_sec', [('', 'Please choose one from the list')] + listRejectCats)
    ostr += '</form>'
    ostr += pif.render.format_button("edit", link=pif.dbh.get_editor_link('link_line', {'id': link_id}))
    #ostr += pif.render.format_table_end()
    return ostr


def edit_multiple(pif):
    table_info = pif.dbh.table_info['link_line']
    page_id = ''
    sec_id = pif.form.get_str('sec', '')
    if pif.form.get_bool('as'):
        linklines = pif.dbh.fetch_link_lines(flags=pif.dbh.FLAG_LINK_LINE_ASSOCIABLE, order="display_order")
    elif sec_id == 'new':
        linklines = pif.dbh.fetch_link_lines(flags=pif.dbh.FLAG_LINK_LINE_NEW)
    elif sec_id == 'nonf':
        linklines = pif.dbh.fetch_link_lines(where="last_status != 'H200' and link_type in ('l','s') and page_id != 'links.rejects' and (flags & 32)=0")
    elif pif.form.get_str('stat'):
        linklines = pif.dbh.fetch_link_lines(where="last_status='%s'" % pif.form.get_str('stat'))
    elif sec_id:
        linklines = pif.dbh.fetch_link_lines(where="section_id='%s'" % sec_id, order="display_order")
        page_id = pif.dbh.fetch_section(sec_id)['section.page_id']
    else:
        linklines = pif.dbh.fetch_link_lines(where="page_id='%s'" % pif.form.get_str('page'), order="display_order")
    print len(linklines), '<br>'
    ostr = pif.render.format_table_start()
    ostr += pif.render.format_row_start()
    for col in table_info['columns']:
        ostr += pif.render.format_cell(0, col)
    ostr += pif.render.format_row_end()
    for link in linklines:
        pif.dbh.depref('link_line', link)
        ostr += pif.render.format_row_start()
        for col in table_info['columns']:
            val = link.get(col, '')
            if col == 'id':
                ostr += pif.render.format_cell(1, '<a href="?id=' + str(val) + '">' + str(val) + '</a>')
            elif col == 'url':
                ostr += pif.render.format_cell(1, '<a href="%s">%s</a>' % (val, val))
            else:
                ostr += pif.render.format_cell(1, str(val))
        ostr += pif.render.format_row_end()
    ostr += pif.render.format_table_end()
    ostr += pif.render.format_button("add", "edlinks.cgi?page_id=%s&sec=%s&add=1" %
        (page_id, sec_id))
    return ostr


def edit_choose(pif):
    sections = pif.dbh.fetch_sections(where="page_id like 'links%'")
    sections.sort(key=lambda x: x['section.page_id'])
    ostr = '<table width="100%"><tr><td width="65%" valign="top">\n'
    ostr += '<ul>\n'
    for sec in sections:
        ostr += '<li><a href="edlinks.cgi?sec=%(section.id)s">%(section.page_id)s: %(section.name)s</a>\n' % sec
    ostr += '</ul>\n'
    ostr += '</td>\n'
    ostr += '<td width="35%" valign="top">\n'
    ostr += '<ul>\n'
    ostr += '<li><a href="edlinks.cgi?sec=new">New</a>\n'
    ostr += '<li><a href="edlinks.cgi?sec=nonf">Nonfunctional</a>\n'
    ostr += '<li><a href="edlinks.cgi?sec=single">Single</a>\n'
    ostr += '<li><a href="edlinks.cgi?as=1">Associables</a><p>\n'
    ostr += '<li><a href="%s">Blacklist</a><p>' % pif.dbh.get_editor_link('blacklist', {})
    for stat in sorted(pif.dbh.fetch_link_statuses()):
        ostr += '<li><a href="edlinks.cgi?stat=%(last_status)s">%(last_status)s</a>\n' % stat
    ostr += '</ul>\n'
    ostr += '</td></tr></table>\n'
    return ostr


# main entry point for links editor
@basics.web_page
def edit_links(pif):
    pif.render.print_html()
    print pif.render.format_head()
#    if pif.form.get_bool('add'):
#        pif.form.set_val('id', pif.dbh.insert_link_line({'page_id': pif.form.get_str('page_id'), 'country': '', 'flags': 1, 'link_type': 'l'}))
#	pif.form.delete('add')
    ostr = ''
    if pif.form.get_str('id'):
        ostr += edit_single(pif)
    elif pif.form.get_bool('as'):
        ostr += edit_multiple(pif)
    elif pif.form.get_str('sec'):
        ostr += edit_multiple(pif)
    elif pif.form.get_str('stat'):
        ostr += edit_multiple(pif)
    elif pif.form.get_str('page'):
        ostr += edit_multiple(pif)
    else:
        ostr += edit_choose(pif)
    print ostr
    print pif.render.format_tail()


def check_links(pif, sections=None, reject=[], retest=False, visible=False):
    pif.dbh.dbi.verbose = True
    for sec in sections if sections else [None]:
        links = pif.dbh.fetch_link_lines(section=sec, where='last_status != "200"' if retest else '')
        for link in links:
            check_link(pif, link, reject, visible=visible)


def check_link(pif, link, rejects=[], visible=False):
    if link:
	print link, visible
        link = pif.dbh.depref('link_line', link)
        lstatus = 'unset'
	if visible and (link['flags'] & pif.dbh.FLAG_LINK_LINE_HIDDEN or link['page_id'] == 'links.rejects'):
	    return
        print link['id'], link['url'],
        if link['flags'] & pif.dbh.FLAG_LINK_LINE_NOT_VERIFIABLE or link['link_type'] in 'tfp':
            lstatus = 'NoVer'
        elif link['link_type'] in 'bglsx':
#            ret = is_blacklisted(link['url'], rejects)
#            if ret:
#                print link['id'], link['section_id'], link['url'], "BLACKLISTED", ret
                #pif.dbh.dbi.remove('link_line', 'id=%s' % link['id'])
            try:
		url = urllib2.urlopen(urllib2.Request(link['url'], headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0'}))
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
	if link['last_status'] != lstatus:
	    pif.dbh.update_link_line({'id': str(link['id']), 'last_status': lstatus})


def check_blacklisted_links(pif, sections=None):
    reject, banned = links.read_blacklist(pif)
    pif.dbh.dbi.verbose = True
    for sec in sections if sections else [None]:
        for link in pif.dbh.fetch_link_lines(section=sec):
            link = pif.dbh.depref('link_line', link)
            if link['link_type'] in 'blsxg':
                ret = is_blacklisted(link['url'], reject)
                if ret:
                    print link['id'], link['section_id'], link['url'], "BLACKLISTED", ret
                    #pif.dbh.dbi.remove('link_line', 'id=%s' % link['id'])


@basics.command_line
def commands(pif):
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


if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='')
