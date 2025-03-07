#!/usr/local/bin/python

import glob
from io import open
import os
import urllib
import urllib.error
import urllib.request

import basics
import config
import mbdata
import render
import useful


# -- links


# main entry point for toylinks
@basics.web_page
def links(pif):
    pif.ren.print_html()
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/cgi-bin/links.cgi', 'Toy Links')
    if pif.form.get_int('id'):
        if link := pif.dbh.fetch_link_line(pif.form.get_int('id')):
            return single_link(pif, pif.dbh.make_link_line_item(link))
    pif.ren.set_page_extra(pif.ren.reset_button_js)
    if pif.page_id != 'links.toylinks':
        pif.ren.hierarchy_append(f'/cgi-bin/links.cgi?page={pif.page_id[6:]}', pif.ren.title)
    return link_page(pif)


def single_link(pif, link):
    if link.page_id != 'links.toylinks':
        pif.ren.hierarchy_append(f'/cgi-bin/links.cgi?page={pif.page_id[6:]}', pif.ren.title)
    pif.ren.hierarchy_append('', 'Specific Link')
    extra = ''
    if pif.is_allowed('m'):  # pragma: no cover
        extra = '- ' + pif.ren.format_button_link("edit", f"edlinks.cgi?id={link.id}")
    return pif.ren.format_template('tlink.html', link=link, extra=extra)


def link_page(pif):
    page_id = 'makes' if pif.page_id == 'links.makes' else pif.page_id
    section_id = useful.clean_id(pif.form.get_str('section'))
    sections = pif.dbh.make_sec_items(pif.dbh.fetch_sections(
        {'page_id': page_id, 'id': section_id} if section_id else
        {'page_id': page_id})) if page_id != 'makes' else pif.dbh.make_sec_items([{'page_id': 'makes', 'id': 'all'}])
    linklines = pif.dbh.make_link_line_items(pif.dbh.fetch_link_lines(page_id, order='display_order'))
    sect_links = {}
    for link in linklines:
        if link.link_type != 'x' and not link.new and not link.hidden:
            link.link_type = 'b' if pif.is_allowed('m') and link.last_status == 'exc' else link.link_type
            link.comment = True
            link.text = format_entry(pif, link)
            sec_id = 'all' if page_id == 'makes' else link.section_id
            sect_links.setdefault(sec_id, list())
            sect_links[sec_id].append(link)

    llineup = render.Listix(id=pif.page_id, section=[render.Section(
        section=x, anchor=x.id,
        range=[render.Range(id='range', entry=sect_links.get(x.id, []))]) for x in sections])

    return pif.ren.format_template('tlinks.html', llineup=llineup, flags=pif.ren.format_shown_flags())


def format_entry(pif, ent):
    dict_flag = {
        '': pif.ren.format_image_art('wheel.gif', also={'class': 'dlm'}),
        'Reciprocal': pif.ren.fmt_mini(icon='refresh', alsoc='dlm'),
        'PayPal': pif.ren.fmt_mini(family='brands', icon='paypal', alsoc='dlm'),
    }
    dlms = []
    if ent.country:
        dlms.append(ent.country)
    if ent.reciprocal:
        dlms.append('Reciprocal')
    if ent.paypal:
        dlms.append('PayPal')
    if not dlms and ent.description and not ent.format_large:
        dlms.append('')

    ostr = pif.ren.format_link('' if ent.disabled else ent.url,
                               (f'{ent.section_id} - ' if ent.page_id == 'makes' else '') + ent.name) + ' '
    # also = {'class': 'dlm'}
    for dlm in dlms:
        if flag := pif.ren.show_flag(dlm):
            ostr += useful.img_src(flag[1], also={'class': 'dlm'})
        elif dlm in dict_flag:
            ostr += dict_flag[dlm]
        else:
            useful.write_comment(f'tlinks.format_entry: dlm {dlm} not found {dict_flag}')
    return ostr


# -- addlink


def read_config(pif, showall=False):
    listCats = []
    listIndices = []
    listRejectCats = []
    dictCats = {}
    allpages = pif.dbh.make_page_items(pif.dbh.fetch_pages("id like 'links.%'"))
    if pif.is_allowed('a'):  # and pif.ren.is_beta:  # pragma: no cover
        showpage = {x.id: True for x in allpages}
    else:
        showpage = {x.id: not x.is_hidden for x in allpages}
    sections = pif.dbh.make_sec_items(pif.dbh.fetch_sections(where="page_id like 'links.%'"))
    for section in sections:
        page_name = section.page_id.split('.', 1)[1]
        if page_name not in listIndices:
            listIndices.append(page_name)
        if showpage.get(section.page_id):
            listCats.append((section.id, section.name))
        if section.page_id in ['links.rejects', 'links.trash']:
            listRejectCats.append((section.id, section.name))
        dictCats[section.id] = page_name
    return listCats, listIndices, dictCats, listRejectCats


def read_blacklist(pif):
    blacklist = pif.dbh.fetch_blacklist()
    reject = [x['blacklist.target'] for x in blacklist if x['blacklist.reason'] == 'site']
    banned = [x['blacklist.target'] for x in blacklist if x['blacklist.reason'] == 'ip']
    return reject, banned


def is_blacklisted(url, rejects):
    for reject in rejects:
        if reject in url:
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
    for section in pif.dbh.make_sec_items(pif.dbh.fetch_sections(where="page_id like 'links%'")):
        highest_disp_order.setdefault((section.page_id, section.id), 0)
    for link in pif.dbh.fetch_link_lines():
        link = pif.dbh.make_link_line_item(link)
        highest_disp_order.setdefault((link.page_id, link.section_id), 0)
        if link.display_order > highest_disp_order[(link.page_id, link.section_id)]:
            highest_disp_order[(link.page_id, link.section_id)] = link.display_order
        if link.url and link.link_type in 'lsx':
            all_links.append(fix_url(link.url))
    return all_links, highest_disp_order


def add_new_link(pif, dictCats, listRejects):
    reasons = []
    ostr = "<hr>"
    # columns: [id page_id section_id display_order flags link_type country url name description note]
    all_links, highest_disp_order = read_all_links(pif)
    link = {}
    try:
        link['url'] = url = pif.form.get_str('url', '')
        link['section_id'] = pif.form.get_str('cat', '')
        link['page_id'] = 'links.' + dictCats[link['section_id']]
        link['display_order'] = highest_disp_order[
            (link.get('page_id', 'unknown'), link.get('section_id', 'unknown'))] + 1
    except Exception:
        reasons.extend([
            "Some information was missing.",
            "The request was badly formed.",
            "The request was not made by the supplied web form."])

    link['flags'] = config.FLAG_LINK_LINE_NEW
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
    # str = 'l|' + url + '|' + tag + '|' + dlm + '|' + cmt

    if reasons:
        ostr += "<b>The site submitted is being rejected.  Sorry.</b><br>\n"
        ostr += f"Possible reason{useful.plural(reasons)}:<ul>\n"
        for reason in reasons:
            ostr += "<li>" + reason + '\n'
        ostr += (
            "</ul>If your submission has to do with sex, drugs, hotel reservations or ringtones, "
            "please go away and never come back.  Seriously.<p>\n"
            "Feel free to use your browser's BACK button to fix your entry, then resubmit; or,\n"
            "if you think this rejection was in error, you can send email.  Just don't hope for too much.\n")
        open(os.path.join(config.LOG_ROOT, 'trash.log'), 'a+').write(str(link) + '\n')
    else:
        link['id'] = pif.dbh.insert_link_line(link)
        ostr += "Your suggestion has been sent to the site administrators.  Thank you.<br>"
        check_link(pif, pif.dbh.make_link_line_item(link))
    return ostr


# main routine for addlink
@basics.web_page
def add_page(pif):
    pif.ren.print_html()
    pif.ren.set_page_extra(pif.ren.reset_button_js)

    rejected, blacklist = read_blacklist(pif)
    for ent in blacklist:
        if pif.remote_addr == ent:
            raise useful.SimpleError(
                "You have been banned from using this service because of previous abuses.  "
                "If you have a problem with this, contact us via email, but don't hope for much.")

    listCats, listIndices, dictCats, listRejectCats = read_config(pif)

    lnk = add_new_link(pif, dictCats, rejected) if pif.form.get_str('url') else ''

    context = {
        'categories': listCats,
        'countries': mbdata.countries,
        'link': lnk,
    }
    return pif.ren.format_template('tlinkadd.html', **context)


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
    listCats.append(('single', 'single'))
    listMakes = [(x['vehicle_make.id'], x['vehicle_make.name']) for x in pif.dbh.fetch_vehicle_makes()]
    table_data = pif.dbh.get_table_data('link_line')
    link_id = pif.form.get_str('id')
    nlink = {x: pif.form.get_str(x) for x in table_data.columns}
    if pif.form.get_str('save'):
        _, highest_disp_order = read_all_links(pif)
        if not nlink['id']:
            nlink['flags'] = 0
            if nlink['section_id'] == 'single' or nlink['page_id'] == 'makes':
                pass
            else:
                nlink['page_id'] = 'links.' + dictCats.get(
                    pif.form.get_str('section_id', ''), pif.form.get_str('section_id', ''))
            nlink['display_order'] = highest_disp_order.get((nlink['page_id'], nlink['section_id']), 0) + 1
            for flag in pif.form.get_list('flags'):
                nlink['flags'] += int(flag, 16)
            if nlink['flags'] & config.FLAG_LINK_LINE_NOT_VERIFIABLE:
                nlink['last_status'] = 'NoVer'
            del nlink['id']
            pif.ren.message(nlink)
            pif.dbh.insert_link_line(nlink)
            pif.ren.message('<br>record added<br>')
        else:
            nlink['flags'] = 0
            if pif.form.get_str('section_id') == 'single':
                pass
            elif pif.form.get_str('page_id') == 'makes':
                pass
            else:
                nlink['page_id'] = 'links.' + dictCats.get(
                    pif.form.get_str('section_id', ''), pif.form.get_str('section_id', ''))
            nlink['display_order'] = highest_disp_order.get((nlink['page_id'], nlink['section_id']), 0) + 1
            for flag in pif.form.get_list('flags'):
                nlink['flags'] += int(flag, 16)
            if nlink['flags'] & config.FLAG_LINK_LINE_NOT_VERIFIABLE:
                nlink['last_status'] = 'NoVer'
            pif.dbh.update_link_line(nlink)
            pif.ren.message('<br>record saved<br>')
    elif pif.form.get_str('test'):
        link = pif.dbh.make_link_line_item(pif.dbh.fetch_link_line(link_id))
        check_link(pif, link)  # don't care about blacklist here, just actual check
    elif pif.form.get_str('delete'):
        pif.dbh.delete_link_line(link_id)
        return "<br>deleted<br>"
    elif pif.form.get_str('reject'):
        nlink = {x: pif.form.get_str(x, '') for x in table_data.columns}
        nlink['page_id'] = 'links.rejects'
        nlink['display_order'] = 1
        nlink['section_id'] = pif.form.get_str('rejects_sec')
        nlink['flags'] = 0
        pif.dbh.update_link_line(nlink)
        pif.ren.message('<br>record rejected<br>')

    if pif.form.get_str('add'):
        link = {
            'link_line.id': '',
            'link_line.page_id': pif.form.get('page_id', ''),
            'link_line.section_id': pif.form.get('sec', ''),
            'link_line.display_order': 0,
            'link_line.flags': 1,
            'link_line.associated_link': '',
            'link_line.last_status': '-',
            'link_line.link_type': 'l',
            'link_line.country': '',
            'link_line.url': '',
            'link_line.name': '',
            'link_line.description': '',
            'link_line.note': '',
        }
    else:
        link = pif.dbh.fetch_link_line(link_id)
        if not link:
            raise useful.SimpleError("That ID wasn't found.")
    asslinks = [(0, '')] + [(x['link_line.id'], x['link_line.name'])
                            for x in pif.dbh.fetch_link_lines(flags=config.FLAG_LINK_LINE_ASSOCIABLE)]
    descs = pif.dbh.describe_dict('link_line')

    header = '<form>' + pif.create_token()
    header += f'<input type="hidden" name="o_id" value="{link["link_line.id"]}">\n'

    entries = []
    for col in table_data.columns:
        col_long = 'link_line.' + col
        coltype = descs.get(col).get('type', 'unknown')
        val = useful.printablize(link.get(col_long, ''))
        # entries.append({'text': '<a href="%s">%s</a>' % (link.get(col_long, ''), link.get(col_long, ''))
        #                if col == 'url' else link[col_long]})
        if col in table_data.readonly:
            cell = '&nbsp;' + pif.form.put_hidden_input({col: val})
        # elif col == 'page_id':
        #     cell = '&nbsp;<input type="hidden" name="%s" value="%s">' % (col, val)
        elif col == 'section_id':
            if link['link_line.page_id'] == 'makes':
                cell = pif.form.put_select(
                    'section_id', listMakes, selected=val, blank='Please choose one from the list')
            else:
                cell = pif.form.put_select(
                    'section_id', listCats, selected=val, blank='Please choose one from the list')
        elif col == 'flags':
            cell = pif.form.put_checkbox("flags", table_data.bits['flags'],
                                         useful.bit_list(link[col_long], format='{:04x}'))
        elif col == 'country':
            cell = pif.form.put_select_country('country', val)
        elif col == 'link_type':
            cell = pif.form.put_select(col, link_type_names, selected=val)
        elif col == 'associated_link':
            cell = pif.form.put_select(col, asslinks, selected=val)
        elif coltype.startswith('varchar('):
            colwidth = int(coltype[8:-1])
            cell = pif.form.put_text_input(col, colwidth, 64, value=val)
        elif coltype.startswith('int('):
            if link[col_long] is None:
                val = 0
            colwidth = int(coltype[4:-1])
            cell = pif.form.put_text_input(col, colwidth, value=val)
        else:
            cell = coltype
        entries.append({'col': col, 'old': f'<a href="{val}">{val}</a>' if col == 'url' else val, 'edit': cell})

    footer = ''.join([
        pif.form.put_button_input("save"),
        pif.form.put_button_input("delete"),
        pif.form.put_button_input("test"),
        pif.form.put_button_input("reject"),
        pif.form.put_select('rejects_sec', listRejectCats, blank='Please choose one from the list'),
        '</form>',
        pif.ren.format_button_link("edit", link=pif.dbh.get_editor_link('link_line', {'id': link_id})),
    ])

    llineup = render.Listix(
        id='tl', name='Edit Link',
        section=[render.Section(id='s', range=[render.Range(entry=entries)],
                 colist=['col', 'old', 'edit'], header=header, footer=footer)]
    )
    return pif.ren.format_template('simplelistix.html', llineup=llineup.prep())


def edit_multiple(pif, good=None):
    stat = pif.form.get_str('stat')
    table_data = pif.dbh.get_table_data('link_line')
    page_id = ''
    sec_id = pif.form.get_str('sec', '')

    where = flags = order = None
    if pif.form.get_str('as'):
        flags = config.FLAG_LINK_LINE_ASSOCIABLE
        order = "display_order"
    elif sec_id == 'new':
        flags = config.FLAG_LINK_LINE_NEW
    elif sec_id == 'nonf':
        where = ["last_status is not Null", "last_status != 'H200'", "link_type in ('l','s')"
                 "page_id != 'links.rejects'", "page_id != 'links.trash'", "(flags & 32)=0"]
    elif stat:
        where = ["page_id != 'links.rejects' and page_id != 'links.trash'" if good else
                 "(page_id='links.rejects' or page_id='links.trash')",
                 "last_status is NULL" if stat == 'None' else f"last_status='{stat}'"]
        order = 'id'
    elif pif.form.get_str('page_id') == 'makes':
        where = f"page_id='{pif.form.get_str('page_id')}'"
        order = "section_id"
        page_id = 'makes'
    elif sec_id:
        where = f"section_id='{sec_id}'"
        order = "display_order"
        section = pif.dbh.fetch_section(sec_id)
        page_id = section['page_id']
    else:
        where = f"page_id='{pif.form.get_str('page_id')}'"
        order = "display_order"

    linklines = pif.dbh.fetch_link_lines(where=where, flags=flags, order=order)
    pif.ren.message(len(linklines), 'lines')
    pif.dbh.depref('link_line', linklines)

    def mangle_item(col, val):
        return (f'<a href="?id={val}">{val}</a>' if col == 'id' else
                f'<a href="{val}">{val}</a>' if col == 'url' else useful.printablize(val))

    entries = [{col: mangle_item(col, link.get(col, '')) for col in table_data.columns}
               for link in linklines]
    footer = pif.ren.format_button_link("add", f"edlinks.cgi?page_id={page_id}&sec={sec_id}&add=1")

    llineup = render.Listix(
        id='tl', name='Edit Link',
        section=[render.Section(id='s', colist=table_data.columns, range=[render.Range(entry=entries)],
                                footer=footer)]
    )
    return pif.ren.format_template('simplelistix.html', llineup=llineup.prep())


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
        'H451': '(Legal)',
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
    ok_link_statuses = {
        str(x['last_status']): x['count(*)']
        for x in pif.dbh.fetch_link_statuses("page_id != 'links.rejects' and page_id != 'links.trash'")}
    rej_link_statuses = {
        str(x['last_status']): x['count(*)']
        for x in pif.dbh.fetch_link_statuses("page_id='links.rejects' or page_id='links.trash'")}
    # 'link_statuses': ["%s (%s)" % (x, reasons.get(x, 'Unknown')) for x in sorted(pif.dbh.fetch_link_statuses())],
    context = {
        'sections': sorted(pif.dbh.fetch_sections(where="page_id like 'links%'"), key=lambda x: x['page_id']),
        'blacklist': pif.dbh.get_editor_link('blacklist', {}),
        'link_statuses': sorted(ok_link_statuses.items()),
        'link_rejects': sorted(rej_link_statuses.items()),
        'reasons': reasons,
    }
    return pif.ren.format_template('tlinkcats.html', **context)


# main entry point for links editor
@basics.web_page
def edit_links(pif):
    pif.ren.print_html()
    if pif.form.get_str('id') or pif.form.get_str('add') or pif.form.get_str('save'):
        return edit_single(pif)
    elif pif.form.has_any(['as', 'sec', 'stat', 'page_id']):
        return edit_multiple(pif, good=pif.form.get_bool('good'))
    else:
        return edit_choose(pif)


# -- link checker


def check_links(pif, sections=None, reject=[], retest=False, visible=False):
    pif.dbh.set_verbose(True)
    for sec in sections if sections else [None]:
        pif.dbh.clear_link_line_statuses(section=sec, where='last_status != "H200"' if retest else '')
        links = pif.dbh.make_link_line_items(
            pif.dbh.fetch_link_lines(section=sec, where='last_status is NULL' if retest else '', order='id'))
        for link in links:
            if not retest or link.page_id != 'links.rejects':
                check_link(pif, link, reject, visible=visible)


def check_link(pif, link, rejects=[], visible=False):
    if link:
        print(link.__dict__, visible)
        lstatus = 'unset'
        if visible and (link.hidden or link.page_id == 'links.rejects'):
            return
        print(link.id, link.url,)
        if link.not_verifiable or link.link_type in 'tfpn':
            lstatus = 'NoVer'
        elif link.link_type in 'bglsx':
            # ret = is_blacklisted(link.url, rejects)
            # if ret:
            #     print(link.id, link.section_id, link.url, "BLACKLISTED", ret)
            # pif.dbh.dbi.remove('link_line', 'id=%s' % link.id)
            lurl = link.url
            if lurl.startswith('/'):
                lurl = 'https://www.bamca.org' + lurl
            try:
                url = urllib.request.urlopen(urllib.request.Request(
                    lurl, headers={
                        'User-Agent':
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0'}))
                pif.ren.message('http success:', url.code)
                lstatus = 'H' + str(url.code)
            except urllib.error.HTTPError as c:
                pif.ren.message('http error:', c)
                lstatus = 'H' + str(c.code)
            except urllib.error.URLError as c:
                pif.ren.message('url error:', c)
                lstatus = 'U' + str(c)
            except Exception as e:
                pif.ren.message('Exception:', str(e))
                lstatus = 'exc'
        if link.last_status != lstatus:
            pif.dbh.update_link_line({'id': str(link.id), 'last_status': lstatus})


# ---- ----------------------------------------------------


def check_spam(pif):
    reject, banned = read_blacklist(pif)
    found = {}
    for fn in glob.glob('../../comments/spam/comment.*'):
        for x in open(fn).readlines():
            if x.startswith('REMOTE_ADDR='):
                x = x[12:].strip()
                found.setdefault(x, 0)
                found[x] += 1
    for k, v in found.items():
        if v > 5 and k not in reject and k not in banned:
            print(v, k)
            # print(pif.dbh.insert_blacklist(k, 'ip'))


def check_blacklisted_links(pif, sections=None):
    reject, banned = read_blacklist(pif)
    pif.dbh.set_verbose(True)
    for sec in sections if sections else [None]:
        for link in pif.dbh.fetch_link_lines(section=sec):
            link = pif.dbh.depref('link_line', link)
            if link['link_type'] in 'blsxg':
                ret = is_blacklisted(link['url'], reject)
                if ret:
                    print(link['id'], link['section_id'], link['url'], "BLACKLISTED", ret)
                    # pif.dbh.dbi.remove('link_line', 'id=%s' % link['id'])


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
        print(f"update link_line set id={ids} where id=%d;")


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
    ('s', check_spam, 'check spam'),
]


# ---- ----------------------------------------------------


if __name__ == '__main__':  # pragma: no cover
    basics.process_command_list(cmds=cmds, dbedit='')
