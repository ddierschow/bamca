#!/usr/local/bin/python

import os
import basics
import config
import mbdata


@basics.command_line
def main(pif):
    crs = pif.dbh.fetch_casting_relateds(section_id='single')
    mods = []
    for cr in crs:
	m = cr['casting_related.model_id']
	r = cr['casting_related.related_id']
	mods.append((m, r))

    cnt = 0
    for mod in mods:
	if (tuple(reversed(mod)) not in mods):
	    print mod
	    cnt += 1
    print cnt, 'of', len(mods)


if __name__ == '__main__':  # pragma: no cover
    main(page_id='editor')
