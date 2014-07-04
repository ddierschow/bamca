#!/usr/local/bin/python

import copy, glob, os, re, sys, urllib2
import basics
import mbdata
import images
import lineup
import package
import config

# Start here

def Report(area, im_count, pr_count=0):
    print "%-23s %6d / %6d" % (area, im_count, pr_count)

href_re = re.compile('''<a href=".*?">''')
def CountHtml(fpath):
    fim = open(fpath).read()
    count = 0
    for href in href_re.findall(fim):
	if not '/' in href:
	    count += 1
    Report(fpath, count, count)
    return count
    
def CountDirectory(pdir):
    count = len(glob.glob(pdir + '/*.jpg'))
    Report(pdir, count, count)
    return count

def CountComboOneOnly(pdir, prefs, roots, suffs):
    count = 0
    for root in roots:
	found = False
	for pref in prefs:
	    for suff in suffs:
		for ext in images.otypes:
		    fl = glob.glob('%s/%s%s%s.%s' % (pdir, pref, root, suff, ext))
		    for fn in fl:
			if os.path.exists(fn):
			    count += 1
			    found = True
			    break
		    if found:
			found = True
			break
		if found:
		    found = True
		    break
	    if found:
		found = True
		break
    Report(pdir, count, len(roots))
    return count

def CountCombo(pdir, prefs, roots, suffs):
    count = 0
    for root in roots:
	for pref in prefs:
	    for suff in suffs:
		for ext in images.otypes:
		    fl = glob.glob('%s/%s%s%s.%s' % (pdir, pref, root, suff, ext))
		    for fn in fl:
			if os.path.exists(fn):
			    count += 1
    Report(pdir, count, len(roots))
    return count

def GetYear(pif, region, year):
    if year < 1982:
	pif.render.pic_dir = config.imgdirLesney
    elif year < 1993:
	pif.render.pic_dir = config.imgdirUniv
    elif year < 1998:
	pif.render.pic_dir = config.imgdirTyco
    else:
	pif.render.pic_dir = config.imgdirMattel
    return lineup.PictureCount(pif, region, str(year))

def GetYears(pif, region, ystart, yend, pr_count, im_count):
    for year in range(ystart, yend + 1):
	count = GetYear(pif, region, year)
	pr_count += count[0]
	im_count += count[1]
	print "    %s  %s  %-4d / %-4d" % (year, region, count[1], count[0])
    return pr_count, im_count

def CountLineups(pif):
    pr_count = im_count = 0
    answer = pif.dbh.dbi.rawquery("select min(year), max(year) from lineup_model")[0]
    ystart = int(answer['min(year)'])
    yend = int(answer['max(year)'])
    dircheck = {}
    pr_count, im_count = GetYears(pif, 'U', ystart, yend, pr_count, im_count)
    pr_count, im_count = GetYears(pif, 'R', 1982, yend, pr_count, im_count)
    pr_count, im_count = GetYears(pif, 'L', 2008, yend, pr_count, im_count)
    pr_count, im_count = GetYears(pif, 'D', 1999, 2001, pr_count, im_count)
    pr_count, im_count = GetYears(pif, 'B', 2000, 2001, pr_count, im_count)
    pr_count, im_count = GetYears(pif, 'A', 2000, 2001, pr_count, im_count)
    Report("lineups", im_count, pr_count)
    return count

def CountPub(pif):
    recs = pif.dbh.FetchPublications()
    count = 0
    count += CountCombo(config.imgdirCat, ['s_', ''], [x['base_id.id'].lower() for x in recs], ['', '_*'])
    count += CountCombo(config.imgdir175, ['s_'], [x['base_id.id'].lower() for x in recs], [''])
    return count

def CountPack(pif):
    recs = pif.dbh.FetchPacks()
    count = 0
    count += CountComboOneOnly(config.imgdirPack, ['t_', 's_', 'c_', 'm_'], [x['base_id.id'].lower() for x in recs], [''])
    count += CountCombo(config.imgdirPack, ['l_', 'h_'], [x['base_id.id'].lower() for x in recs], [''])
    count += CountCombo(config.imgdir175, ['s_'], [x['base_id.id'].lower() for x in recs], [''])
    return count

def CountMan(pif):
    recs = pif.dbh.FetchCastingList()
    count = 0
    count += CountCombo(config.imgdir175, ['s_', 'm_', 'l_', 'z_'], [x['base_id.id'].lower() for x in recs], [''])
    count += CountCombo(config.imgdirAdd, ['a_', 'b_', 'e_', 'i_', 'p_', 'r_'], [x['base_id.id'].lower() for x in recs], [''])
    count += CountCombo(config.imgdir175 + '/icon', ['i_'], [x['base_id.id'].lower() for x in recs], [''])
    return count

def CountVar(pif):
    varrecs = pif.dbh.FetchVariationsBare()
    recs = []
    for var in varrecs:
	var_id = var['variation.var']
	if var['variation.picture_id']:
	    var_id = var['variation.picture_id']
	recs.append('%s-%s' % (var['variation.mod_id'].lower(), var_id.lower()))
    count = 0
    count += CountCombo(config.imgdir175 + '/var', ['s_', 'm_'], recs, [''])
    return count

def CountBox(pif):
    pr_count, im_count = package.CountBoxes(pif)
    Report("box", im_count, pr_count)
    return im_count

def CountFromFile(fpath, tag, fld, pdir):
    pr_count = im_count = 0
    for ln in open(fpath).readlines():
	lns = ln.strip().split('|')
	if lns and lns[0] == tag:
	    pr_count += 1
	    if os.path.exists('%s/%s.jpg' % (pdir, lns[fld])):
		im_count +=1
    Report(fpath, im_count, pr_count)
    return im_count

if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('editor')

    count = 0
    count += CountFromFile('src/coll43.dat', 'm', 2, config.imgdirColl43)
    count += CountFromFile('src/coll72.dat', 'm', 2, config.imgdirColl43)
    count += CountFromFile('src/coll18.dat', 'm', 2, config.imgdirColl43)
    count += CountBox(pif)
    count += CountDirectory(config.imgdirSeries)
    count += CountDirectory(config.imgdirAcc)
    count += CountDirectory(config.imgdirBlister)
    count += CountDirectory(config.imgdirCode2)
    count += CountDirectory(config.imgdirColl64)
    count += CountHtml(config.imgdirAds + '/index.php')
    count += CountHtml(config.imgdirErrors + '/index.html')
    count += CountLineups(pif)
    count += CountMan(pif)
    count += CountVar(pif)
    count += CountPack(pif)
    count += CountPub(pif)

    print
    Report('total', count)
