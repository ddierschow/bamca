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
            cols = [x[0] for x in desc[0]]
            if set(cols) != set(tables.table_info[table]['columns']):
                print "differ"
            else:
                print "same"
        else:
            print "missing from table_info"


if __name__ == '__main__':  # pragma: no cover
    main()
