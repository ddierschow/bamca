#!/usr/local/bin/python

import basics
import datetime

ok_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,?!/\'_()#":-%&;*|@<>=$+[]`\\^~'
#0 9 13
#133 145 146 148 150 220 174 178 180 188 194 195 196 201 204 209 214 217 226 228 229 232 233 235 239 169

def check_tables(pif):
    if pif.filelist:
	for tab in pif.filelist:
	    check_table(pif, tab)
	    print
    else:
	#found_ch = set()
	tabs = pif.dbh.dbi.execute('show tables')
	for tab in tabs[0]:
	    tab = tab[0]
	    if tab == 'counter':
		continue
	    check_table(pif, tab)
	    print
	#print found_ch


def check_table(pif, tab):
    print tab
    rows = pif.dbh.dbi.execute('select * from ' + tab)[0]
    cols = [desc[0] for desc in pif.dbh.dbi.execute('desc ' + tab)[0]]
    #print cols
    #print rows[0][0]
    for row in rows:
	for icol in range(len(row)):
	    if isinstance(row[icol], long):
		continue
	    elif isinstance(row[icol], int):
		continue
	    elif row[icol] is None:
		continue
	    elif isinstance(row[icol], datetime.datetime):
		continue
	    elif isinstance(row[icol], datetime.timedelta):
		continue
	    elif isinstance(row[icol], str):
		for ch in row[icol]:
		    if not ch in ok_letters:
			print '  ', row
			#found_ch.add(ord(ch))
			break
	    else:
		print tab, cols[icol], row[icol], type(row[icol])


@basics.command_line
def main(pif):
    check_tables(pif)

if __name__ == '__main__':  # pragma: no cover
    main()
