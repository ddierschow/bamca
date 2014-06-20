#!/usr/local/bin/python

'''
This script takes commits from the git log and puts them
into the site activity table in the database.  It will only
do them back to the previously most recent entry in the table,
so it is best run after every commit so as not to lose any
information.
'''

import datetime, os, re, subprocess, sys
import cmdline
import basics

# Start here


def Main(pif):
    act = GetLastActivity(pif)
    dat = ReadCommits(act['site_activity.timestamp'])
    WriteCommits(pif, dat)


def GetLastActivity(pif):
    acts = pif.dbh.FetchActivities()
    acts.sort(key=lambda x: x['site_activity.id'])
    return acts[-1]


def ReadCommits(endtime):
    p = subprocess.Popen(["/usr/local/bin/git", "log"], stdout=subprocess.PIPE, stderr=None, close_fds=True)
    l = p.stdout.read()
    commits = list()
    date_re = re.compile('Date:\s*(?P<d>... ... .. ..:..:.. ....)')
    for log_msg in re.compile('\ncommit ', re.M).split(l):
	print
	#print log_msg
	if log_msg.find('Merge: ') >= 0:
	    print "merge"
	    continue
	m = date_re.search(log_msg)
	if not m:
	    print "no date"
	    continue
	s = m.group('d')
	commit = dict()
	commit['user_id'] = 1
	commit['name'] = 'commit'
	commit['description'] = log_msg.split('\n', 4)[4].strip()
	commit['timestamp'] = datetime.datetime.strptime(s, '%a %b %d %X %Y')
	if commit['timestamp'] <= endtime:
	    print "too old"
	    continue
	commits.append(commit)
	print commit
    commits.sort(key=lambda x:x['timestamp'])
    return commits


def WriteCommits(pif, commits):
    print
    print "Writing to activity table."
    for commit in commits:
	print commit
	pif.dbh.InsertActivity(**commit)
    


if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('editor', dbedit=True)
    Main(pif)
