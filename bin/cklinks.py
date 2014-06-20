#!/usr/local/bin/python

import os, sys
#os.environ['DOCUMENT_ROOT'] = '/usr/local/www/bamca/beta/htdocs'
#os.environ['SERVER_NAME'] = 'beta.bamca.org'
#sys.path.append('../../cgi-bin')
import basics

# Start here

import urllib2

def CheckLinks(sec=None):
    if sec:
	links = pif.dbh.dbi.select('link_line', where="section_id='%s'" % sec)
    else:
	links = pif.dbh.dbi.select('link_line')
    pif.dbh.dbi.verbose = True
    for link in links:
	link = pif.dbh.DePref('link_line', link)
	lstatus = ''
	print link['url'],
	if link['flags'] & pif.dbh.FLAG_LINK_LINE_NOT_VERIFIABLE:
	    lstatus = 'NoVer'
	elif link['link_type'] in 'blsxg':
	    try:
		url = urllib2.urlopen(link['url'])
		lstatus = str(url.code)
	    except urllib2.HTTPError as (c):
		print 'http error:', c.code
		lstatus = 'H' + str(c.code)
	    except urllib2.URLError as (c):
		print 'url error:', c.reason
		lstatus = 'U' + str(c.reason[0])
	    except:
		lstatus = 'exc'
	print lstatus
	pif.dbh.dbi.update('link_line', {'last_status' : lstatus}, "id='" + str(link['id']) + "'")


if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('editor')

    if len(sys.argv) > 1:
	for sec in sys.argv[1:]:
	    CheckLinks(sec)
    else:
	CheckLinks()
