#!/usr/local/bin/python

import os, sys
import cmdline
#os.environ['DOCUMENT_ROOT'] = '/usr/local/www/bamca/beta/htdocs'
#os.environ['SERVER_NAME'] = 'beta.bamca.org'
#sys.path.append('../../cgi-bin')
import basics
import mbdata
import config

# Start here
verbose = False


def RunModels(mods):
    upics = spics = sfound = cpics = cfound = mpics = mfound = apics = afound = 0
    mods = map(lambda x: x[0], mods)
    mods.sort()

    for mod in mods:
	uf, af, mf, cf, sf = ShowListVarPics(pif, mod)
	if (not switch['q']) and \
	   (not switch['s'] or sf[2] < 100) and \
	   (not switch['c'] or cf[2] < 100) and \
	   (not switch['m'] or mf[2] < 100) and \
	   (not switch['a'] or af[2] < 100):
	    print '%-8s%5d | %3d/%3d |%3d%% | %3d/%3d |%3d%% | %3d/%3d |%3d%% | %3d/%3d |%3d%%' % ((mod, uf) + af + mf + cf + sf)

	upics  += uf
	spics  += sf[1]
	sfound += sf[0]
	cpics  += cf[1]
	cfound += cf[0]
	mpics  += mf[1]
	mfound += mf[0]
	apics  += af[1]
	afound += af[0]

    return upics, spics, sfound, cpics, cfound, mpics, mfound, apics, afound 


def ShowListVarPics(pif, mod_id):
    upics = spics = sfound = cpics = cfound = mpics = mfound = apics = afound = 0
    varsels = pif.dbh.FetchVariationSelects(mod_id)
    varsel = {}
    for vs in varsels:
	varsel.setdefault(vs['variation_select.ref_id'], [])
	varsel[vs['variation_select.ref_id']].append(vs['variation_select.var_id'])
    spics = len(varsel.keys())

    vars = pif.dbh.FetchVariations(mod_id)
    for var in vars:
	isorig = 1
	fn = mod_id + '-' + var['variation.var']
	if var['variation.picture_id']:
	    fn = mod_id + '-' + var['variation.picture_id']
	    isorig = 0
	fn = config.imgdir175 + '/var/s_' + fn.lower() + '.jpg'
	apics += 1
	if not var['variation.var'].startswith('f'):
	    if not mbdata.categories.get(var['variation.category'], '').startswith('['):
		mpics += 1
	    if not var['variation.category']:
		cpics += 1
	#print '<!--', config.imgdir175 + '/var/' + fn + '.jpg', '-->'
	if os.path.exists(fn):
	    afound += 1
	    upics += isorig
	    if not var['variation.var'].startswith('f'):
		if not mbdata.categories.get(var['variation.category'], '').startswith('['):
		    mfound += 1
		if not var['variation.category']:
		    cfound += 1
	    for vs in varsel:
		if var['variation.var'] in varsel[vs]:
		    sfound += 1
		    varsel[vs] = []
    if verbose:
	print ' '.join(filter(lambda x: varsel[x], varsel))
    return upics, FormatCalc(afound, apics), FormatCalc(mfound, mpics), FormatCalc(cfound, cpics), FormatCalc(sfound, spics)


def FormatCalc(found, pics):
#    if found == pics:
#	return (found, pics, '--')
    if pics:
	return (found, pics, 100 * found/pics)
    return (0, 0, 100)


def Main(pif):

    switch, files = cmdline.CommandLine('qvscma', '')
    upics = nmods = spics = sfound = cpics = cfound = mpics = mfound = apics = afound = 0

    if switch['v']:
	verbose = True
    if files:
	for spec in files:
	    mods = pif.dbh.dbi.execute("select distinct id from casting where id like '%s%%'" % spec)[0]
	    nmods += len(mods)
	    uf, sp, sf, cp, cf, mp, mf, ap, af = RunModels(mods)

	    upics  += uf
	    spics  += sp
	    sfound += sf
	    cpics  += cp
	    cfound += cf
	    mpics  += mp
	    mfound += mf
	    apics  += ap
	    afound += af

    else:
	mods = pif.dbh.dbi.execute("select distinct id from casting")[0]
	nmods += len(mods)
	uf, sp, sf, cp, cf, mp, mf, ap, af = RunModels(mods)

	upics  += uf
	spics  += sp
	sfound += sf
	cpics  += cp
	cfound += cf
	mpics  += mp
	mfound += mf
	apics  += ap
	afound += af

    print
    print '%7d %5d  %3d/%3d %3d%%  %3d/%3d %3d%%  %3d/%3d %3d%%  %3d/%3d %3d%%' % ((nmods, upics) + \
	FormatCalc(afound, apics) + FormatCalc(mfound, mpics) + FormatCalc(cfound, cpics) + FormatCalc(sfound, spics))

if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('vars')
    Main(pif)
