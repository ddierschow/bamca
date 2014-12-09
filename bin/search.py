#!/usr/local/bin/python

import basics
import mflags
import models

def search_name(pif):
    return pif.dbh.fetch_casting_list(where=["base_id.rawname like '%%%s%%'" % x for x in pif.form_search('query')], verbose=True)


# specific id request goes through here
# would like to accept K43a like things
def search_id(pif):
    cid = get_casting_id(pif.form_str('id'))
    mod = pif.dbh.fetch_casting(cid)
    if mod:
        print '<meta http-equiv="refresh" content="0;url=/cgi-bin/single.cgi?id=%s">' % mod['id']
        return None

    mod = pif.dbh.fetch_castings_by_alias(cid)
    if len(mod) == 1:
        if mod[0].get('alias.id'):
            print '<meta http-equiv="refresh" content="0;url=/cgi-bin/single.cgi?id=%s">' % mod[0]['casting.id']
        return None

    if not mod:
        mod1 = pif.dbh.fetch_casting_list(where="casting.id like '%%%s%%'" % pif.form_str('id'))
        mod2 = pif.dbh.fetch_aliases(where="alias.id like '%%%s%%'" % pif.form_str('id'))
        mod = filter(lambda x: x.get('section.page_id', 'manno') in ['manls', 'manno'], mod1 + mod2)
    return [pif.dbh.modify_man_item(x) for x in mod]


def get_casting_id(id):
    if not id:
        return ''
    ok = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-/'
    id = ''.join(filter(lambda x: x in ok, list(id)))
    if not id:  # pragma: no cover
        return {}
    if id.upper().startswith('MW'):
        id = 'MB' + id[2:]
    if id.upper().startswith('MI') and id[2:].isdigit():
        if int(id[2:]) < 700:
            id = 'MB' + id[2:]
    if id.upper().startswith('LR'):
        id = 'RW' + id[2:]
    if id.upper().startswith('LS'):
        id = 'SF' + id[2:]
    return id


def create_lineup(pif, mods):
    flago = mflags.FlagList(pif)
    llineup = {'columns': 4}
    lsec = pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
    lran = {'entry': []}
    for mod in mods:
        mod = pif.dbh.modify_man_item(mod)
        lran['entry'].append({'text': models.add_model_table_pic_link(pif, mod, flago=flago)})
    lsec['range'] = [lran]
    llineup['section'] = [lsec]
    return llineup


@basics.web_page
def run_search(pif):
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append(pif.request_uri, 'Model Search')
    mods = None
    pif.render.print_html()
    if pif.form_has('query'):
        targ = pif.form_str('query')
        pif.render.title = 'Models matching name: ' + targ
        mods = search_name(pif)
        mods = filter(lambda x: x['section.page_id'] in ('manls', 'manno'), [pif.dbh.modify_man_item(x) for x in mods])
        print pif.render.format_head()
    elif pif.form_has('id'):
        targ = pif.form_str('id')
        mods = search_id(pif)
        if mods is None:
            return
        pif.render.title = 'Models matching ID: ' + targ
        print pif.render.format_head()
    else:
        print pif.render.format_head()
        print "Huh?"
    if mods:
        mods.sort(key=lambda x: x['rawname'])
        llineup = create_lineup(pif, mods)
        #llineup['name'] ='Models matching: ' + targ
        print pif.render.format_lineup(llineup)
    print pif.render.format_button_comment(pif, 'query=%s' % (pif.form_str('query')))
    print pif.render.format_tail()



if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
