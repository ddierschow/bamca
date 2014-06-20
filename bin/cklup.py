#!/usr/local/bin/python

import os, sys
#os.environ['DOCUMENT_ROOT'] = '/usr/local/www/bamca/beta/htdocs'
#os.environ['SERVER_NAME'] = 'beta.bamca.org'
#sys.path.append('../../cgi-bin')
import basics
import lineup

# Start here

def DoLup(year, region):
    lup = lineup.RunFile(pif, region, str(year)) 
    totals['i'] += lup['var_info']['i']
    totals['p'] += lup['var_info']['p']
    print '%d  %s  %3d  %3d' % (year, region, lup['var_info']['i'], lup['var_info']['p'])

def Main(pif):
    totals = {'i':0, 'p':0}

    st = 1953
    en = 2010
    if len(sys.argv) > 1:
	st = int(sys.argv[1])
	if len(sys.argv) > 2:
	    en = int(sys.argv[2])
	else:
	    en = st
    for year in range(st, en + 1):
	pif.page_id = 'year.%d' % year
	lup = DoLup(year, 'U') 
	if year >= 1982:
	    lup = DoLup(year, 'R') 
	if year in (1999,2000,2001):
	    lup = DoLup(year, 'D') 
	if year in (2000,2001):
	    lup = DoLup(year, 'B') 
	    lup = DoLup(year, 'A') 
	if year >= 2008:
	    lup = DoLup(year, 'L') 
    print '        %4d %4d' % (totals['i'], totals['p'])

if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('vars')
    Main(pif)
