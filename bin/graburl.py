#!/usr/local/bin/python

import os, sys

def ImportPSDC(pif):
    pref = 'http://www.publicsafetydiecast.com/'
    import re, urllib2
    u = urllib2.urlopen('http://www.publicsafetydiecast.com/Matchbox_MAN.htm').read()
    u_re = re.compile('<a href="(?P<u>[^"]*)".*?<font.*?>(?P<i>.*?)<\/font>')
    q = pif.dbh.FetchLinkLines(where='associated_link=365')
    ul = list(set([x['link_line.url'] for x in q]))
    pl = list(set(u_re.findall(u)))
    for l in pl:
	if not pref + l[0] in ul:
	    print l[1], pref + l[0]

if __name__ == '__main__':
    import basics
    pif = basics.GetPageInfo('editor')
