#!/usr/local/bin/python

import os
import basics
import mbdata

@basics.command_line
def main(pif):
    #check_table_data(pif)
    check_mod_data(pif)
    check_var_data(pif)

modsets = [['MB213', 'MB293'], ['MB304', 'MB459', 'MB466'], ['MB254B', 'MB458', 'MB483'], ['MB103', 'MB310'],
    ['MB029', 'MB312'], ['MB168', 'MB574'], ['MB045', 'MB309', ''], ['MB106', 'MB307'], ['MB125', 'MB331'],
    ['MB134', 'MB313'], ['MB140', 'MB314'], ['MB150', 'MB316'], ['MB153', 'MB330', 'MB880'], ['MB431', 'MB472', 'MB554'],
    ['MB183', 'MB340'], ['MB202', 'MB311'], ['MB203', 'MB228', 'MB247'], ['MB214', 'MB308'], ['MB222', 'MB652'],
    ['MB256', 'MB329'], ['MB300', 'MB437'], ['MB319', 'MB337'], ['MB464', 'MB473'], ['MB477', 'MB615'],
    ['MB540', 'MB602'], ['MB510', 'MB606'], ['MB180', 'MB721'], ['MB215', 'MB746'], ['MB592', 'MB775'],
    ['MB787', 'MB813'], ['MB518', 'MB826'], ['MB718', 'MB747', 'MB868'], ['MB368', 'SW002'],
]

def check_table_data(pif):
    for table in pif.dbh.table_info:
	print table
	dats = pif.dbh.dbi.execute('select * from ' + table)[0]
	cols = pif.dbh.dbi.describe(table)
	types = list()
	for dat in dats:
	    ldat = list(dat)
	    for col in cols:
		s = ''
		n = 0
		d = ldat.pop(0)
		try:
		    if col['type'].startswith('varchar'):
			s += d
		    elif col['type'].startswith('char'):
			s += d
		    elif col['type'].startswith('text'):
			s += d
		    elif col['type'].startswith('int'):
			n += d
		    elif col['type'].startswith('tinyint'):
			n += d
		except:
		    print table, col, dat
	    for c in s:
		if ord(c) > 127:
		    print table, dat


def get_vars(pif, mod_ids):
    varlist = []
    for mod_id in mod_ids:
	varlist.extend(pif.dbh.fetch_variations(mod_id))
    return varlist


def check_mod_data(pif):
    mods = pif.dbh.fetch_casting_list()
    modd = {x['casting_id']: x for x in mods}
    for modset in modsets:
	for mod in modset[1:]:
	    if modd[mod]['casting.variation_digits'] != modd[modset[0]]['casting.variation_digits']:
		print 'vardig mismatch:', mod, modd[mod]['casting.variation_digits'], modset[0], modd[modset[0]]['casting.variation_digits']


def check_var_data(pif):
    mods = pif.dbh.fetch_casting_list()
    mods.sort(key=lambda x: x['casting.id'])
    for mod in mods:
	mod_id = mod['casting.id']
	mod_ids = [mod_id]
	for modset in modsets:
	    if modset[0] == mod_id:
		mod_ids = modset
		break
	    if mod_id in modset:
		mod_ids = []
		break
	if not mod_ids:
	    continue
	varlist = get_vars(pif, mod_ids)
	id_nums = set()
	for var in varlist:
	    vid = var['variation.var']
	    nid = mbdata.normalize_var_id(mod, vid)
	    if nid != vid:
		print '*** id mismatch', mod_id, vid, nid
	    if not vid[0].isdigit():
		continue
	    while not vid[-1].isdigit():
		vid = vid[:-1]
	    id_nums.add(int(vid))
	missing = []
	if id_nums:
	    for vid in range(1, max(id_nums)):
		if vid not in id_nums:
		    missing.append(str(vid))
	if missing:
	    print mod_id, ':', ', '.join(missing)


if __name__ == '__main__':  # pragma: no cover
    main()
'''
K004d : 4
K066a : 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37
MB010 : 33
MB034 : 22
MB038 : 644, 651, 714, 729, 733, 739, 766, 769, 770, 774, 776, 777, 782
MB053 : 33
MB068 : 82, 88
MB073 : 49, 50
MB101 : 9
MB103 : 108
MB153 : 68, 69
MB154 : 57
MB157 : 97, 100, 104
MB165 : 63
MB168 : 57, 58, 59, 60, 61
MB172 : 35
MB187 : 31, 34
MB188 : 64, 65
MB221 : 111, 112, 113
MB222 : 32, 39, 40, 41, 42
MB232 : 36
MB244 : 1, 2, 3, 4, 5, 6, 7
MB246 : 17, 18, 45, 46, 47
MB268 : 2
MB273 : 14, 15
MB280 : 80
MB282 : 48
MB291 : 29, 32, 42
MB295 : 91
MB304 : 117
MB318 : 3, 4, 5, 6, 9, 11
MB322 : 21
MB360 : 37, 38
MB372 : 26, 27
MB380 : 8
MB406 : 9, 17
MB486 : 19, 20
MB544 : 20
MB560 : 7
MB581 : 8, 9, 10, 11, 12, 13, 14, 15, 16
MB594 : 13
MB614 : 13
MB630 : 27, 28
MB667 : 32
MB677 : 19
MB688 : 47, 48
MB695 : 33, 36, 37, 38
MB705 : 17
MB712 : 43, 44, 45, 46
MB713 : 35
MB715 : 12, 13, 14, 15
MB716 : 25, 26
MB734 : 8, 20, 21, 22, 23, 24, 25
MB736 : 14, 15, 17
MB748 : 19
MB760 : 12
MB763 : 12
MB776 : 8
MB784 : 11, 12, 13, 14
MB787 : 7, 8, 9
MB797 : 11, 12
MB807 : 7
MB812 : 8
MB829 : 1
MB832 : 3, 4
MB841 : 1, 2, 3, 4, 5
MB855 : 2, 3, 4, 5
MB856 : 1, 2, 3
MB860 : 1, 2, 3, 4, 5
MB913 : 1, 2
MB946 : 1
MB971 : 1
MB973 : 1
WRP02 : 14
'''
