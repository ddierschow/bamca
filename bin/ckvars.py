#!/usr/local/bin/python

import os
import basics
import vars

@basics.command_line
def main(pif):
    check_var_data(pif)


def check_var_data(pif):
    mods = pif.dbh.fetch_casting_list()
    mods.sort(key=lambda x: x['casting.id'])
    for mod in mods:
	mod_id = mod['casting.id']
	varlist = pif.dbh.fetch_variations(mod_id)
	id_nums = set()
	for var in varlist:
	    vid = var['variation.var']
	    nid = vars.normalize_var_id(mod, vid)
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
