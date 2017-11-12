#!/usr/local/bin/python

import glob, os
import basics
import mbdata

@basics.command_line
def main(pif):
    regions = ''.join(mbdata.regionlist).lower()
    files = {}
    dirs = {}
    direct_files(pif, regions, files, dirs)
    indirect_files(pif, regions, files, dirs)
    show_files(regions, files)


def show_files(regions, files):
    for reg in regions:
	if reg in files:
	    for year in sorted(files[reg]):
		print year, reg, ' '.join(collapse(files[reg][year]))
	    print


def direct_files(pif, regions, files, dirs):
    for pg in pif.dbh.fetch_pages(where={'format_type': 'lineup'}, order='id'):
	year = pg.id[5:]
	dirs[year] = pg.pic_dir
	imgs = glob.glob('%s/%s[%s][0-9][0-9].*' % (pg.pic_dir, year, regions))
	imgs += glob.glob('%s/%s[%s][0-9][0-9][0-9].*' % (pg.pic_dir, year, regions))
	for im in imgs:
	    im = im[len(pg.pic_dir) + 1:]
	    files.setdefault(im[4], dict())
	    files[im[4]].setdefault(im[:4], list())
	    files[im[4]][im[:4]].append(im[5:-4])


def indirect_files(pif, regions, files, dirs):
    for lm in pif.dbh.fetch_simple_lineup_models(region=mbdata.regionlist):
	if lm['lineup_model.picture_id']:
	    year = str(lm['lineup_model.year'])
	    region = lm['lineup_model.region'].lower()
	    num = '%%0%dd' % len(files.get(region, {}).get(year, ['00'])[0]) % lm['lineup_model.number']
	    if num in files.get(region, {}).get(year, ['00']):
		print 'hidden image', year, lm['lineup_model.region'], lm['lineup_model.number'], lm['lineup_model.picture_id']
	    else:
		imgs = glob.glob('%s/%s.*' % (dirs[year], lm['lineup_model.picture_id']))
		if imgs:
		    files[region][year].append(str(num))


def collapse(lst):
    intlist = []
    strlist = []
    maxlen = 0
    for ent in sorted(lst):
	try:
	    val = int(ent)
	except:
	    pass
	else:
	    maxlen = max(maxlen, len(ent))
	    intlist.append(val)
	    continue

	try:
	    ents = ent.split('-', 1)
	    val1 = int(ents[0])
	    val2 = int(ents[1])
	except:
	    pass
	else:
	    maxlen = max(maxlen, len(ent[0]))
	    maxlen = max(maxlen, len(ent[1]))
	    intlist.extend(range(val1, val2 + 1))
	    continue

	strlist.append(ent)

    str1 = "%%0%dd" % maxlen
    str2 = str1 + '-' + str1
    intlist.sort()
    start = None
    prev = None
    for val in intlist:
	if start == None:
	    start = prev = val
	elif val == prev + 1:
	    prev = val
	elif start == prev:
	    strlist.append(str1 % start)
	    start = prev = val
	else:
	    strlist.append(str2 % (start, prev))
	    start = prev = val
    if start != None:
	if start == prev:
	    strlist.append(str1 % start)
	    start = None
	else:
	    strlist.append(str2 % (start, prev))
	    start = None

    return strlist


#---- ---------------------------------------

if __name__ == '__main__':  # pragma: no cover
    main()
