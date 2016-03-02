#!/usr/local/bin/python

import os
import basics
import mbdata

@basics.command_line
def main(pif):
    for cas in pif.dbh.fetch_casting_list():
	print cas['casting.id']
	if cas['casting.format_description'] == '':
	    print '  desc'
	    pif.dbh.write_casting({'format_description': '&body|&tampo'}, cas['casting.id'])
	if cas['casting.format_body'] == '':
	    print '  body'
	    pif.dbh.write_casting({'format_body': '*body|*tampo'}, cas['casting.id'])
	if cas['casting.format_interior'] == '':
	    print '  int'
	    pif.dbh.write_casting({'format_interior': '&interior'}, cas['casting.id'])
	if cas['casting.format_windows'] == '':
	    print '  windows'
	    pif.dbh.write_casting({'format_windows': '&windows'}, cas['casting.id'])
	if cas['casting.format_base'] == '':
	    print '  base'
	    pif.dbh.write_casting({'format_base': '&base|&manufacture'}, cas['casting.id'])
	if cas['casting.format_wheels'] == '':
	    print '  wheels'
	    pif.dbh.write_casting({'format_wheels': '&wheels'}, cas['casting.id'])


if __name__ == '__main__':  # pragma: no cover
    main(dbedit='')
