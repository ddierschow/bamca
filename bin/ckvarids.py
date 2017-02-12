#!/usr/local/bin/python

import os, re
import basics

@basics.command_line
def main(pif):
    check_var_data(pif)


starting_digits_re = re.compile('\d*')
def normalize_var_id(mod, var_id):
    if var_id[0].isdigit():
	while var_id and var_id[0] == '0':
	    var_id = var_id[1:]
	digs = starting_digits_re.match(var_id).end()
	var_id = '0' * (mod.get('casting.variation_digits', mod.get('variation_digits', 2)) - digs) + var_id
    return var_id


def check_var_data(pif):
    mods = pif.dbh.fetch_casting_list()
    mods.sort(key=lambda x: x['casting.id'])
    for mod in mods:
	mod_id = mod['casting.id']
	varlist = pif.dbh.fetch_variations(mod_id)
	id_nums = set()
	for var in varlist:
	    vid = var['variation.var']
	    nid = normalize_var_id(mod, vid)
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
