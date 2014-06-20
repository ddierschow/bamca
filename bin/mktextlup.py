#!/usr/local/bin/python

import os, sys
import cmdline
#os.environ['DOCUMENT_ROOT'] = '/usr/local/www/bamca/beta/htdocs'
#os.environ['SERVER_NAME'] = 'beta.bamca.org'
#sys.path.append('../../cgi-bin')
import basics
import lineup

# Start here
#verbose = False




if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('editor')

    switch, files = cmdline.CommandLine('', 'ry')
    for y in switch['y']:
	for r in switch['r']:
	    print lineup.TextMain(pif, y, r)
