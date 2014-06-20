#!/usr/local/bin/python

import os, sys
#os.environ['DOCUMENT_ROOT'] = '/usr/local/www/bamca/beta/htdocs'
#os.environ['SERVER_NAME'] = 'beta.bamca.org'
#sys.path.append('../../cgi-bin')
import basics
import links

# Start here


def CheckLinks(sec=None):
    if sec:
	linklist = pif.dbh.dbi.select('link_line', where="section_id='%s'" % sec)
    else:
	linklist = pif.dbh.dbi.select('link_line')
    pif.dbh.dbi.verbose = True
    for link in linklist:
	link = pif.dbh.DePref('link_line', link)
	if link['link_type'] in 'blsxg':
	    ret = links.IsBlacklisted(link['url'])
	    if ret:
		print link['id'], link['section_id'], link['url'], "BLACKLISTED", ret
		#pif.dbh.dbi.remove('link_line', 'id=%s' % link['id'])


def Main(pif):
    links.listCats, links.listIndices, links.dictCats, links.listRejs = links.ReadConfig(pif)
    links.listRejects, links.blacklist = links.ReadBlacklist(pif)

    if len(sys.argv) > 1:
	for sec in sys.argv[1:]:
	    CheckLinks(sec)
    else:
	CheckLinks()


if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('editor')
    Main(pif)
