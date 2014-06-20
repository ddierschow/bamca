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

def Main(pif):
    import tables
    tablelist = pif.dbh.dbi.execute('show tables')
    for table in tablelist[0]:
	table = table[0]
	print table, ':',
	if table in tables.table_info:
	    desc = pif.dbh.dbi.execute('desc ' + table)
	    cols = map(lambda x:x[0], desc[0])
	    if set(cols) != set(tables.table_info[table]['columns']):
		print "differ"
	    else:
		print "same"
	else:
	    print "missing from table_info"


if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('vars')
    Main(pif)
