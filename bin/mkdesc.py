#!/usr/local/bin/python

import os, sys
#os.environ['DOCUMENT_ROOT'] = '/usr/local/www/bamca/beta/htdocs'
#os.environ['SERVER_NAME'] = 'beta.bamca.org'
#sys.path.append('../../cgi-bin')
import basics
import vars

fields = [
	'text_body',
	'text_interior',
	'text_windows',
	'text_base',
	'text_wheels',
	'text_description',
	'body',
	'base',
	'windows',
	'interior',
	'category',
	'area',
	'date',
	'note',
	'other',
	'picture_id',
	'manufacture',
]

if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('vars')
    for field in fields:
	pif.dbh.dbi.execute("update variation set %s='' where %s is NULL" % (field, field))
    count = 0
    verbose = False
    #verbose = True
    if len(sys.argv) == 1:
	castings = [x['id'] for x in pif.dbh.dbi.select('casting', verbose=False)]
    elif sys.argv[1][0] >= 'a':
	castings = [x['id'] for x in pif.dbh.dbi.select('casting', where="section_id='%s'" % sys.argv[1], verbose=False)]
    else:
	castings = sys.argv[1:]
	verbose = True
    for casting in castings:
	sys.stdout.write(casting + ' ')
	sys.stdout.flush()
	if vars.CheckFormatting(pif, casting, verbose=verbose):
	    print '*'
	    count += 1
	else:
	    print
	vars.RecalcDescription(pif, casting, verbose)
    print
    print count, "to go *"
