#!/usr/local/bin/python

import os, sys
#os.environ['DOCUMENT_ROOT'] = '/usr/local/www/bamca/beta/htdocs'
#os.environ['SERVER_NAME'] = 'beta.bamca.org'
#sys.path.append('../../cgi-bin')
import basics
import mbdata
import config

# Start here

def Model(mod):
    yrs = pif.dbh.dbi.execute("select distinct year from lineup_model where mod_id='%s' and region!='S' and region!='M' and region!='J'" % mod)[0]
    yrs = map(lambda x: x[0], yrs)
    yrs.sort()

    sel = pif.dbh.dbi.execute("select distinct ref_id from variation_select where mod_id='%s'" % mod)[0]
    sel = map(lambda x: x[0][:9], sel)

    missing = []
    for yr in yrs:
	if not 'year.' + yr in sel:
	    missing.append(yr)
    bad = []
    for pg in sel:
	if pg.startswith('year.') and not pg[5:9] in yrs:
	    bad.append(pg)
    return missing, bad


def ShowListVarPics(pif, mod_id):
    vars = pif.dbh.FetchVariations(mod_id)
    cpics = cfound = pics = found = 0
    for var in vars:
	if var['var'].startswith('f') or mbdata.categories.get(var['category'], '').startswith('['):
	    continue
	elif not var['picture_id']:
	    fn = mod_id + '-' + var['var']
	elif var['picture_id'] == var['var']:
	    fn = mod_id + '-' + var['picture_id']
	else:
	    continue
	pics += 1
	if not var['category']:
	    cpics += 1
	#print '<!--', config.imgdir175 + '/var/' + fn + '.jpg', '-->'
	if os.path.exists(config.imgdir175 + '/var/s_' + fn.lower() + '.jpg'):
	    found += 1
	    if not var['category']:
		cfound += 1
    af = '%d/%d' % (found, pics)
    cf = '%d/%d' % (cfound, cpics)
    if found == pics:
	af = '--'
    if cfound == cpics:
	cf = '--'
    return af, cf


def Main(pif):

    specs = sys.argv[1:]

    sw = []
    if specs[0][0] == '0':
	sw = list(specs[0][1:])
	specs = specs[1:]

    for spec in specs:
	mods = pif.dbh.dbi.execute("select distinct id from casting where id like '%s%%'" % spec)[0]
	mods = map(lambda x: x[0], mods)
	mods.sort()

	for mod in mods:
	    missing, bad = Model(mod)
	    af, cf = ShowListVarPics(pif, mod)

	    if 'a' in sw or 'p' in sw or missing or bad or af != '--' or cf != '--':
		print mod,
	    if 'p' in sw or af != '--' or cf != '--':
		print af, cf,
	    if missing:
		print 'needs', ' '.join(missing),

	    if bad:
		print 'has bad', ' '.join(bad),

	    if 'a' in sw or 'p' in sw or missing or bad or af != '--' or cf != '--':
		print

if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('vars')
    Main(pif)
