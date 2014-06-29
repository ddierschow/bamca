#!/usr/local/bin/python

import basics
import flags
import models

def SearchName(pif):
    return pif.dbh.FetchCastingList(where=["base_id.rawname like '%%%s%%'" % x for x in pif.GetSearch('query')], verbose=True)


# specific id request goes through here
# would like to accept K43a like things
def SearchID(pif):
    cid = GetCastingId(pif.form.get('id'))
    mod = pif.dbh.FetchCasting(cid)
    if mod:
	print '<meta http-equiv="refresh" content="0;url=/cgi-bin/single.cgi?id=%s">' % mod['id']
	return None
    
    mod = pif.dbh.FetchCastingsByAlias(cid)
    if len(mod) == 1:
	if mod[0].get('alias.id'):
	    print '<meta http-equiv="refresh" content="0;url=/cgi-bin/single.cgi?id=%s">' % mod[0]['casting.id']
	return None

    if not mod:
	mod1 = pif.dbh.FetchCastingList(where="casting.id like '%%%s%%'" % pif.FormStr('id'))
	mod2 = pif.dbh.FetchAliases(where="alias.id like '%%%s%%'" % pif.FormStr('id'))
	mod = filter(lambda x: x.get('section.page_id', 'manno') in ['manls', 'manno'], mod1 + mod2)
    return [pif.dbh.ModifyManItem(x) for x in mod]


def GetCastingId(id):
    if not id:
	return ''
    ok = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-/'
    id = ''.join(filter(lambda x: x in ok, list(id)))
    if not id: # pragma: no cover
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


def CreateLineup(pif, mods):
    flago = flags.FlagList(pif)
    llineup = {'columns' : 4}
    lsec = pif.dbh.FetchSections({'page_id' : pif.page_id})[0]
    lran = {'entry' : []}
    for mod in mods:
	mod = pif.dbh.ModifyManItem(mod)
	lran['entry'].append({'text' : models.AddModelTablePicLink(pif, mod, flago=flago)})
    lsec['range'] = [lran]
    llineup['section'] = [lsec]
    return llineup


@basics.WebPage
def RunSearch(pif):
    pif.render.hierarchy.append(('/', 'Home'))
    pif.render.hierarchy.append(('/database.php', 'Database'))
    pif.render.hierarchy.append((pif.request_uri, 'Model Search'))
    mods = None
    pif.render.PrintHtml()
    if pif.form.has_key('query'):
	targ = pif.FormStr('query')
	pif.render.title = 'Models matching name: ' + targ
	mods = SearchName(pif)
	mods = filter(lambda x: x['section.page_id'] in ('manls', 'manno'), [pif.dbh.ModifyManItem(x) for x in mods])
	print pif.render.FormatHead()
    elif pif.form.has_key('id'):
	targ = pif.FormStr('id')
	mods = SearchID(pif)
	if mods == None:
	    return
	pif.render.title = 'Models matching ID: ' + targ
	print pif.render.FormatHead()
    else:
	print pif.render.FormatHead()
	print "Huh?"
    if mods:
	mods.sort(key=lambda x: x['rawname'])
	llineup = CreateLineup(pif, mods)
	#llineup['name'] ='Models matching: ' + targ
	print pif.render.FormatLineup(llineup)
    print pif.render.FormatButtonComment(pif, 'query=%s' % (pif.form.get('query', '')))
    print pif.render.FormatTail()



if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
