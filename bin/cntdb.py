#!/usr/local/bin/python

import os
import basics
import mbdata

@basics.command_line
def main(pif):
    count_tables(pif)


def count_tables(pif):
    for tab in pif.dbh.dbi.execute('show tables')[0]:
	cnts = pif.dbh.dbi.execute('select count(*) from ' + tab[0])
	print "%7d %s" % (cnts[0][0][0], tab[0])
	if pif.switch['v']:
	    cols = pif.dbh.dbi.execute('desc ' + tab[0])
	    for col in cols[0]:
		print ' ', col


if __name__ == '__main__':  # pragma: no cover
    main(switches='v')
