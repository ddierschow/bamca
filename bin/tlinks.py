#!/usr/local/bin/python

import os, sys, urllib2
import basics
import config
import mbdata
import useful


# -- links

# main entry point for toylinks
@basics.WebPage
def Links(pif):
    pif.render.PrintHtml()
    ostr = ''
    pif.render.hierarchy.append(('/', 'Home'))
    pif.render.hierarchy.append(('/cgi-bin/links.cgi', 'Toy Links'))
    if pif.FormInt('id'):
        link = pif.dbh.FetchLinkLine(pif.FormInt('id'))
        if link['page_id'] != 'links.toylinks':
            pif.render.hierarchy.append(('/cgi-bin/links.cgi?page=%s' % pif.page_id[6:], pif.render.title))
        pif.render.hierarchy.append(('', 'Specific Link'))
        ostr += pif.render.FormatHead()
        ostr += SingleLink(pif, link)
        ostr += pif.render.FormatTail()
    else:
        if pif.page_id != 'links.toylinks':
            pif.render.hierarchy.append(('/cgi-bin/links.cgi?page=%s' % pif.page_id[6:], pif.render.title))
        ostr += pif.render.FormatHead()
        ostr += LinkPage(pif)
        ostr += pif.render.FormatTail()
    return ostr


def SingleLink(pif, link):
    ostr  = 'Do you have a comment about this link?  Please send it to us.\n'
    ostr += '<form action="comment.php" method="post" name="comment">\n'
    ostr += '''
<table>
<tr><td>My Subject</td><td><input type="text" name="mysubject" size=80 maxlength=80></td></tr>
<tr><td>My Comment</td><td><textarea name="mycomment" cols=80 rows=6></textarea></td></tr>
<tr><td>My Name</td><td><input type="text" name="myname" size=80 maxlength=80> (optional)</td></tr>
<tr><td>My E-mail Address</td><td><input type="text" name="myemail" size=80 maxlength=80> (optional)</td></tr>
</table>
'''
    ostr += pif.render.FormatButtonInput() + ' - '
    ostr += pif.render.FormatButtonReset('comment') + '\n'
    ostr += '</form>\n'
    if pif.IsAllowed('a'):  # pragma: no cover
        ostr += pif.render.FormatButton("edit_this_page", link=pif.dbh.GetEditorLink('link_line', {'id': pif.FormStr('id', '')}), also={'class': 'comment'}, lalso={})
    ostr += '<br>' + str(link) + '<br>'
    return ostr


def LinkPage(pif):
    section_id = pif.FormStr('section')
    if section_id:
        sections = pif.dbh.FetchSections({'page_id': pif.page_id, 'id': section_id})
    else:
        sections = pif.dbh.FetchSections({'page_id': pif.page_id})
    sections = pif.dbh.DePref('section', sections)
    linklines = pif.dbh.FetchLinkLines(pif.page_id)
    linklines = pif.dbh.DePref('link_line', linklines)
    linklines.sort(key=lambda x: int(x['display_order']))
    sect_links = dict()
    for link in linklines:
        sect_links.setdefault(link['section_id'], list())
        sect_links[link['section_id']].append(link)

    llineup = {'id': pif.page_id, 'name': '', 'section': []}
    for lsec in sections:
        lsec.update({'anchor': lsec['id'], 'columns': 1})
        lran = {'id': 'range', 'name': '', 'entry': GenerateLinks(pif, sect_links.get(lsec['id'], []))}
        lsec['range'] = [lran]
        llineup['section'].append(lsec)

    return pif.render.FormatLinks(llineup) + '\n' + EndOfPage(pif)


def GenerateLinks(pif, links):
    for ent in links:
        if ent['link_type'] != 'x' and not (ent['flags'] & pif.dbh.FLAG_LINK_LINE_NEW):
            lnk = dict()
            lnk['text'], lnk['desc'] = FormatEntry(pif, ent)
            lnk['indent'] = (ent['flags'] & pif.dbh.FLAG_LINK_LINE_INDENTED) != 0
            lnk['id'] = ent['id']
            cmd = ent['link_type']
            if pif.IsAllowed('m'):  # pragma: no cover
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

def FormatEntry(pif, ent):
    dictFlag = {
            '': ('o', pif.render.FindArt('wheel.gif')),
            'Reciprocal': ('Reciprocal', pif.render.FindArt('recip.gif')),
            'PayPal': ('Accepts PayPal', pif.render.FindArt('paypal.gif')),
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

    ostr = pif.render.FormatLink(url, tag, nstyle={'class': 'link'}) + ' '

    if not dlms and not cmt:
        pass
    elif not dlms:
        # add name
        if not is_large:
            ostr += FormatDelimiter(pif, dictFlag[''])
    else:
        also = {'class': 'dlm'}
        for dlm in dlms:
            flag = pif.render.ShowFlag(dlm)
            if flag:
                ostr += FormatDelimiter(pif, flag)
            else:
                ostr += FormatDelimiter(pif, dictFlag[dlm])
#    if cmt and is_large:
#       ostr += '<br>' + '<br>'.join(cmt.split('|'))
#    else:
#       ostr += cmt
    return ostr, cmt.split('|')


def FormatDelimiter(pif, dlm):
    also = {'class': 'dlm', 'alt': '[' + dlm[0] + ']'}
    pif.render.Comment('FormatDelimiter', dlm)
    return useful.ImgSrc(dlm[1], also=also) + ' '


def EndOfPage(pif):
    ball = '%s\n' % pif.render.FmtArt('ball.gif', desc='o')
    ostr = '<hr>\n'
    ostr += '<center>This page is maintained by <em>Dean Dierschow</em>.<br>\n'
    ostr += '<nobr>%s Dean\'s Recommendations</nobr>\n' % pif.render.FmtArt('star.gif', desc='*')
    ostr += ball
    ostr += '<nobr>%s Reciprocal Link</nobr>\n' % pif.render.FmtArt('recip.gif')
    if pif.IsAllowed('m'):  # pragma: no cover
        ostr += ball
        ostr += '<nobr>%s Comment on this link</nobr>\n' % pif.render.FmtArt('comment.gif')
    ostr += '</center>\n'
    return ostr


# -- addlink


def ReadConfig(pif, showall=False):
    listCats = []
    listIndices = []
    listRejectCats = []
    dictCats = {}
    allpages = pif.dbh.FetchPages("id like 'links.%'")
    if pif.IsAllowed('a'):  # and pif.render.isbeta:  # pragma: no cover
        showpage = {x['page_info.id']: 1 for x in allpages}
    else:
        showpage = {x['page_info.id']: not (x['page_info.flags'] & pif.dbh.FLAG_PAGE_INFO_NOT_RELEASED) for x in allpages}
    sections = pif.dbh.FetchSections(where="page_id like 'links.%'")
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


def ReadBlacklist(pif):
    blacklist = pif.dbh.FetchBlacklist()
    reject = [x['blacklist.target'] for x in filter(lambda x: x['blacklist.reason'] == 'site', blacklist)]
    banned = [x['blacklist.target'] for x in filter(lambda x: x['blacklist.reason'] == 'ip', blacklist)]
    return reject, banned


def IsBlacklisted(url, rejects):
    for reject in rejects:
        if url.find(reject) >= 0:
            return reject
    return ''


def FormatForm(pif, listCats):
    ostr = '<form action="addlink.cgi" method="post" name="addlink">\n'
    ostr += pif.render.FormatTableStart()
    ostr += pif.render.FormatRowStart()
    ostr += pif.render.FormatCell(0)
    ostr += pif.render.FormatCell(1, 'Please enter the <b>full</b> URL (including the "http" part).')
    ostr += pif.render.FormatRowEnd()
    ostr += pif.render.FormatRowStart()
    ostr += pif.render.FormatCell(0, 'URL:')
    ostr += pif.render.FormatCell(1, pif.render.FormatTextInput("url", 256, 64))
    ostr += pif.render.FormatRowEnd()
    ostr += pif.render.FormatRowStart()
    ostr += pif.render.FormatCell(0, 'Name:')
    ostr += pif.render.FormatCell(1, pif.render.FormatTextInput("name", 256, 64))
    ostr += pif.render.FormatRowEnd()
    ostr += pif.render.FormatRowStart()
    ostr += pif.render.FormatCell(0, 'Description:')
    ostr += pif.render.FormatCell(1, pif.render.FormatTextInput("desc", 256, 64) + ' (optional)')
    ostr += pif.render.FormatRowEnd()
    ostr += pif.render.FormatRowStart()
    ostr += pif.render.FormatCell(0, 'Country:')
    ostr += pif.render.FormatCell(1, pif.render.FormatSelectCountry('country', ''))
    ostr += pif.render.FormatRowEnd()
    ostr += pif.render.FormatRowStart()
    ostr += pif.render.FormatCell(0, 'Category:')
    ostr += pif.render.FormatCell(1, pif.render.FormatSelect('cat', [('', 'Please choose one from the list')] + listCats, selected=''))
    ostr += pif.render.FormatRowEnd()
    ostr += pif.render.FormatRowStart()
    ostr += pif.render.FormatCell(0, 'Note to the webmaster (optional):', also={'colspan': 2})
    ostr += pif.render.FormatRowEnd()
    ostr += pif.render.FormatRowStart()
    ostr += pif.render.FormatCell(0)
    ostr += pif.render.FormatCell(1, pif.render.FormatTextInput("note", 80))
    ostr += pif.render.FormatRowEnd()
    ostr += pif.render.FormatRowStart()
    ostr += pif.render.FormatCell(0, '&nbsp;')
    ostr += pif.render.FormatCell(1, pif.render.FormatButtonInput("submit link") + pif.render.FormatButtonReset("addlink"))
    ostr += pif.render.FormatRowEnd()
    ostr += pif.render.FormatTableEnd()
    ostr += '</form>\n'
    return ostr


def FixURL(url):
    url = url.lower()
    if url[-1] == '/':
        url = url[:-1]
    return url


def ReadAllLinks(pif):
    highest_disp_order = {}
    all_links = []
    for section in pif.dbh.FetchSections(where="page_id like 'links%'"):
        highest_disp_order.setdefault((section['section.page_id'], section['section.id']), 0)
    for link in pif.dbh.FetchLinkLines():
        link = pif.dbh.DePref('link_line', link)
        highest_disp_order.setdefault((link['page_id'], link['section_id']), 0)
        if link['display_order'] > highest_disp_order[(link['page_id'], link['section_id'])]:
            highest_disp_order[(link['page_id'], link['section_id'])] = link['display_order']
        if link['url'] and link['link_type'] in 'lnsx':
            all_links.append(FixURL(link['url']))
    return all_links, highest_disp_order



def AddNewLink(pif, dictCats, listRejects):
    reasons = []
    ostr = "<hr>"
    #'columns': ['id', 'page_id', 'section_id', 'display_order', 'flags', 'link_type', 'country', 'url', 'name', 'description', 'note'],
    all_links, highest_disp_order = ReadAllLinks(pif)
    link = {}
    try:
        link['url'] = url = pif.FormStr('url', '')
        link['section_id'] = pif.FormStr('cat', '')
        link['page_id'] = 'links.' + dictCats[link['section_id']]
        link['display_order'] = highest_disp_order[(link.get('page_id', 'unknown'), link.get('section_id', 'unknown'))] + 1
    except:
        reasons.extend([
            "Some information was missing.",
            "The request was badly formed.",
            "The request was not made by the supplied web form."])

    link['flags'] = pif.dbh.FLAG_LINK_LINE_NEW
    if pif.IsAllowed('a'):  # pragma: no cover
        link['flags'] = 0
    link['link_type'] = 'l'
    link['name'] = pif.FormStr('name', '')
    link['country'] = pif.FormStr('country', '')
    link['description'] = pif.FormStr('desc', '')
    link['note'] = pif.remote_addr + '/' + pif.remote_host + '. ' + pif.FormStr('note', '')

    url = FixURL(url)
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
        ostr += "Possible reason%s:<ul>\n" % useful.Plural(reasons)
        for reason in reasons:
            ostr += "<li>" + reason + '\n'
        ostr += "</ul>If your submission has to do with sex, drugs, hotel reservations or ringtones, please go away and never come back.  Seriously.<p>\n"
        ostr += "Feel free to use your browser's BACK button to fix your entry, then resubmit; or,\n"
        ostr += "if you think this rejection was in error, you can send email.  Just don't hope for too much.\n"
        open(os.path.join(config.logroot, 'trash.dat'), 'a+').write(str(link) + '\n')
    else:
        pif.dbh.InsertLinkLine(link)
        ostr += "The following has been added to the list:<br><ul>\n"
        ent = FormatEntry(pif, link)
        ostr += ent[0] + ' '
        ostr += '<br>' .join(ent[1])
        ostr += '\n</ul>\n'
    return ostr


# main routine for addlink
@basics.WebPage
def AddPage(pif):
    pif.render.PrintHtml()
    print pif.render.FormatHead(extra=pif.render.reset_button_js)

    rejected, blacklist = ReadBlacklist(pif)
    for l in blacklist:
        if os.environ.get('REMOTE_ADDR') == l:
            print "You have been banned from using this service because of previous abuses.  If you have a problem with this, contact us via email, but don't hope for much."
            print pif.render.FormatTail()
            sys.exit(0)
    listCats, listIndices, dictCats, listRejectCats = ReadConfig(pif)
    ostr = '''
You can now suggest links to be added to the ToyLinks page.  I will review them and move them to the approprate place.
Thanks for helping out!
<p><hr><p>
''' + FormatForm(pif, listCats) + '''
<p><hr><p>
Please submit only links that have something to do with toys or toy collecting.  Die-cast toys are of particular interest.
If you submit a site that has nothing to do with the subject material of this website, it will be summarily deleted.
Note that if your submission includes just gibberish in the name or description, it will be rejected without being checked.
'''
    if pif.FormStr('url'):
        ostr += AddNewLink(pif, dictCats, rejected)
    print ostr
    print pif.render.FormatTail()



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

def EditSingle(pif):
    listCats, listIndices, dictCats, listRejectCats = ReadConfig(pif, True)
    listCats.append(('single', 'single'))
    table_info = pif.dbh.table_info['link_line']
    id = pif.FormStr('id')
    if pif.FormBool('save'):
        all_links, highest_disp_order = ReadAllLinks(pif)
        nlink = {x: pif.FormStr(x) for x in table_info['columns']}
        nlink['flags'] = 0
        if pif.FormStr('section_id') == 'single':
            pass
        else:
            nlink['page_id'] = 'links.' + dictCats.get(pif.FormStr('section_id', ''), pif.FormStr('section_id', ''))
        nlink['display_order'] = highest_disp_order.get((nlink['page_id'], nlink['section_id']), 0) + 1
        formflags = pif.FormList('flags')
        for flag in formflags:
            nlink['flags'] += int(flag, 16)
        if nlink['flags'] & pif.dbh.FLAG_LINK_LINE_NOT_VERIFIABLE:
            nlink['last_status'] = 'NoVer'
        pif.dbh.UpdateLinkLine(nlink)
        print '<br>record saved<br>'
    elif pif.FormBool('test'):
        link = pif.dbh.FetchLinkLine(id)
        CheckLink(pif, link)  # don't care about blacklist here, just actual check
    elif pif.FormBool('delete'):
        pif.dbh.DeleteLinkLine(id)
        return "<br>deleted<br>"
    elif pif.FormBool('reject'):
        nlink = {x: pif.FormStr(x, '') for x in table_info['columns']}
        nlink['page_id'] = 'links.rejects'
        nlink['display_order'] = 1
        nlink['section_id'] = pif.FormStr('rejects_sec')
        nlink['flags'] = 0
        pif.dbh.UpdateLinkLine(nlink)
        print '<br>record rejected<br>'
    elif pif.FormBool('add'):
        id = pif.dbh.InsertLinkLine({'page_id': pif.FormStr('page_id', ''), 'section_id': pif.FormStr('sec')})

    links = pif.dbh.FetchLinkLines(where="id='%s'" % id)
    link = links[0]
    asslinks = [(0, '')] + [(x['link_line.id'], x['link_line.name']) for x in pif.dbh.FetchLinkLines(where="flags & %s" % pif.dbh.FLAG_LINK_LINE_ASSOCIABLE)]
    ostr = pif.render.FormatTableStart()
    ostr += '<form>\n<input type="hidden" name="o_id" value="%s">\n' % link['link_line.id']
    descs = pif.dbh.DescribeDict('link_line')
    ostr += pif.render.FormatTableStart()
    for col in table_info['columns']:
        col_long = 'link_line.' + col
        coltype = descs.get(col).get('type', 'unknown')
        ostr += pif.render.FormatRowStart()
        ostr += pif.render.FormatCell(0, col)
        if col == 'url':
            ostr += pif.render.FormatCell(1, '<a href="%s">%s</a>' % (link.get(col_long, ''), link.get(col_long, '')))
        else:
            ostr += pif.render.FormatCell(1, link[col_long])
        if col in table_info.get('readonly', []):
            ostr += pif.render.FormatCell(1, '&nbsp;<input type="hidden" name="%s" value="%s">' % (col, link[col_long]))
#       elif col == 'page_id':
#           ostr += pif.render.FormatCell(1, '&nbsp;<input type="hidden" name="%s" value="%s">' % (col, link[col_long]))
        elif col == 'section_id':
            ostr += pif.render.FormatCell(1, pif.render.FormatSelect('section_id', [('', 'Please choose one from the list')] + listCats, selected=link[col_long]))
        elif col == 'flags':
            ostr += pif.render.FormatCell(1, pif.render.FormatCheckbox("flags", flag_check_names, useful.BitList(link[col_long])))
        elif col == 'country':
            ostr += pif.render.FormatCell(1, pif.render.FormatSelectCountry('country', link[col_long]))
        elif col == 'link_type':
            ostr += pif.render.FormatCell(1, pif.render.FormatSelect(col, link_type_names, selected=link[col_long]))
        elif col == 'associated_link':
            ostr += pif.render.FormatCell(1, pif.render.FormatSelect(col, asslinks, selected=link[col_long]))
        elif coltype.startswith('varchar('):
            colwidth = int(coltype[8:-1])
            ostr += pif.render.FormatCell(1, pif.render.FormatTextInput(col, colwidth, 64, value=link[col_long]))
        elif coltype.startswith('int('):
            if link[col_long] is None:
                link[col_long] = 0
            colwidth = int(coltype[4:-1])
            val = link[col_long]
            if isinstance(val, str) and val.isdigit():
                val = str(int(val))
            elif not val:
                val = ''
            ostr += pif.render.FormatCell(1, pif.render.FormatTextInput(col, colwidth, value=val))
        else:
            ostr += pif.render.FormatCell(1, coltype)
        ostr += pif.render.FormatRowEnd()
    ostr += pif.render.FormatTableEnd()
    ostr += pif.render.FormatButtonInput("save")
    ostr += pif.render.FormatButtonInput("delete")
    ostr += pif.render.FormatButtonInput("test")
    ostr += pif.render.FormatButtonInput("reject")
    ostr += pif.render.FormatSelect('rejects_sec', [('', 'Please choose one from the list')] + listRejectCats)
    ostr += '</form>'
    ostr += pif.render.FormatTableEnd()
    return ostr


def EditMultiple(pif):
    table_info = pif.dbh.table_info['link_line']
    page_id = ''
    sec_id = pif.FormStr('sec', '')
    if pif.FormBool('as'):
        linklines = pif.dbh.FetchLinkLines(where="flags&%d" % pif.dbh.FLAG_LINK_LINE_ASSOCIABLE, order="display_order")
    elif sec_id == 'new':
        linklines = pif.dbh.FetchLinkLines(where="flags&%d" % pif.dbh.FLAG_LINK_LINE_NEW)
    elif sec_id == 'nonf':
        linklines = pif.dbh.FetchLinkLines(where="last_status != '200' and link_type in ('l','s') and page_id != 'links.rejects' and (flags & 32)=0")
    elif sec_id:
        linklines = pif.dbh.FetchLinkLines(where="section_id='%s'" % sec_id, order="display_order")
        page_id = pif.dbh.FetchSection(sec_id)['section.page_id']
    else:
        linklines = pif.dbh.FetchLinkLines(where="page_id='%s'" % pif.FormStr('page'), order="display_order")
    ostr = pif.render.FormatTableStart()
    ostr += pif.render.FormatRowStart()
    for col in table_info['columns']:
        ostr += pif.render.FormatCell(0, col)
    ostr += pif.render.FormatRowEnd()
    for link in linklines:
        pif.dbh.DePref('link_line', link)
        ostr += pif.render.FormatRowStart()
        for col in table_info['columns']:
            val = link.get(col, '')
            if col == 'id':
                ostr += pif.render.FormatCell(1, '<a href="?id=' + str(val) + '">' + str(val) + '</a>')
            elif col == 'url':
                ostr += pif.render.FormatCell(1, '<a href="%s">%s</a>' % (val, val))
            else:
                ostr += pif.render.FormatCell(1, str(val))
        ostr += pif.render.FormatRowEnd()
    ostr += pif.render.FormatTableEnd()
    ostr += pif.render.FormatButton("add", "edlinks.cgi?page_id=%s&sec=%s&add=1" %
        (page_id, sec_id))
    return ostr


def EditChoose(pif):
    sections = pif.dbh.FetchSections(where="page_id like 'links%'")
    ostr = '<ul>\n'
    ostr += '<li><a href="edlinks.cgi?sec=new">New</a>\n'
    ostr += '<li><a href="edlinks.cgi?sec=nonf">Nonfunctional</a>\n'
    ostr += '<li><a href="edlinks.cgi?sec=single">Single</a>\n'
    ostr += '<li><a href="edlinks.cgi?as=1">Associables</a>\n'
    sections.sort(key=lambda x: x['section.page_id'])
    for sec in sections:
        ostr += '<li><a href="edlinks.cgi?sec=%(section.id)s">%(section.page_id)s: %(section.name)s</a>\n' % sec
    ostr += '<li><a href="%s">Blacklist</a>' % pif.dbh.GetEditorLink('blacklist', {})
    ostr += '</ul>\n'
    return ostr


# main entry point for links editor
@basics.WebPage
def EditLinks(pif):
    pif.render.PrintHtml()
    print pif.render.FormatHead()
    if pif.FormBool('add'):
        pif.FormSet('id', pif.dbh.InsertLinkLine({'page_id': pif.FormStr('page_id'), 'country': '', 'flags': 1, 'link_type': 'l'}))
    ostr = ''
    if pif.FormStr('id'):
        ostr += EditSingle(pif)
    elif pif.FormBool('as'):
        ostr += EditMultiple(pif)
    elif pif.FormStr('sec'):
        ostr += EditMultiple(pif)
    elif pif.FormStr('page'):
        ostr += EditMultiple(pif)
    else:
        ostr += EditChoose(pif)
    print ostr
    print pif.render.FormatTail()


def CheckLinks(pif, sections=None, reject=[]):
    pif.dbh.dbi.verbose = True
    for sec in sections if sections else [None]:
        links = pif.dbh.FetchLinkLines(section=sec)
        for link in links:
            CheckLink(pif, link, reject)


def CheckLink(pif, link, rejects=[]):
    if link:
        link = pif.dbh.DePref('link_line', link)
        lstatus = 'unset'
        print link['url'],
        if link['flags'] & pif.dbh.FLAG_LINK_LINE_NOT_VERIFIABLE:
            lstatus = 'NoVer'
        elif link['link_type'] in 'bglsx':
#            ret = IsBlacklisted(link['url'], rejects)
#            if ret:
#                print link['id'], link['section_id'], link['url'], "BLACKLISTED", ret
                #pif.dbh.dbi.remove('link_line', 'id=%s' % link['id'])
            try:
                url = urllib2.urlopen(link['url'])
                lstatus = str(url.code)
            except urllib2.HTTPError as (c):
                print 'http error:', c.code
                lstatus = 'H' + str(c.code)
            except urllib2.URLError as (c):
                print 'url error:', c.reason
                lstatus = 'U' + str(c.reason[0])
            except:
                lstatus = 'exc'
        print lstatus
        pif.dbh.UpdateLinkLine({'id': str(link['id']), 'last_status': lstatus})


def CheckBlacklistedLinks(pif, sections=None):
    reject, banned = links.ReadBlacklist(pif)
    pif.dbh.dbi.verbose = True
    for sec in sections if sections else [None]:
        for link in pif.dbh.FetchLinkLines(section=sec):
            link = pif.dbh.DePref('link_line', link)
            if link['link_type'] in 'blsxg':
                ret = IsBlacklisted(link['url'], reject)
                if ret:
                    print link['id'], link['section_id'], link['url'], "BLACKLISTED", ret
                    #pif.dbh.dbi.remove('link_line', 'id=%s' % link['id'])


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
