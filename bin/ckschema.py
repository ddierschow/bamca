#!/usr/local/bin/python

import basics
import tables


@basics.command_line
def main(pif):
    tablelist = [x[0] for x in pif.dbh.dbi.execute('show tables')[0]] + ['buser.' + x[0] for x in pif.dbh.dbi.execute('show tables in buser')[0]]
    for table in tablelist:
        if table in tables.table_info:
            desc = pif.dbh.dbi.execute('desc ' + table)
            dbcols = set([x[0] for x in desc[0]])
            ticols = set(tables.table_info[table]['columns'] + tables.table_info[table].get('extra_columns', []))
            if dbcols != ticols:
		print table, ':', "differ"
		print "  db:", sorted(dbcols - ticols)
		print "  ti:", sorted(ticols - dbcols)
#            else:
#                print "same"
        else:
	    print table, ':', "missing from table_info"
    for table in set(tables.table_info.keys()) - set(tablelist):
	print table, ': missing from database'


if __name__ == '__main__':  # pragma: no cover
    main()
