#!/usr/local/bin/python

import basics
import tables


@basics.command_line
def main(pif):
    tablelist = pif.dbh.dbi.execute('show tables')
    for table in tablelist[0]:
        table = table[0]
        print table, ':',
        if table in tables.table_info:
            desc = pif.dbh.dbi.execute('desc ' + table)
            dbcols = set([x[0] for x in desc[0]])
            ticols = set(tables.table_info[table]['columns'] + tables.table_info[table].get('extra_columns', []))
            if dbcols != ticols:
                print "differ"
		print "  db:", sorted(dbcols - ticols)
		print "  ti:", sorted(ticols - dbcols)
            else:
                print "same"
        else:
            print "missing from table_info"


if __name__ == '__main__':  # pragma: no cover
    main()
