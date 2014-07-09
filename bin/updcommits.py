#!/usr/local/bin/python

'''
This script takes commits from the git log and puts them
into the site activity table in the database.

It also does some other housekeeping: man2csv, and writing
the config file for php's use.
'''

import datetime, os, re, subprocess, sys
import basics
import mannum

# Start here


def Main(pif):
    act = GetLastActivity(pif)
    dat = ReadCommits(act['site_activity.timestamp'])
    WriteCommits(pif, dat)
    WriteConfigFile()
    WriteManCSV(pif)


def GetLastActivity(pif):
    acts = filter(lambda x: x['site_activity.name'] == 'commit', pif.dbh.FetchActivities())
    acts.sort(key=lambda x: x['site_activity.id'])
    return acts[-1]


def ReadCommits(endtime):
    p = subprocess.Popen(["/usr/local/bin/git", "log"], stdout=subprocess.PIPE, stderr=None, close_fds=True)
    l = p.stdout.read()
    commits = list()
    #Date:   Fri Jun 13 19:26:34 2014 +0200
    date_re = re.compile('Date:\s*(?P<d>... ... \d+ \d+:\d+:\d+ \d+)')
    for log_msg in re.compile('\ncommit ', re.M).split(l):
	if log_msg.find('Merge: ') >= 0:
	    continue
	m = date_re.search(log_msg)
	if not m:
	    continue
	s = m.group('d')
	commit = dict()
	commit['user_id'] = 1
	commit['name'] = 'commit'
	commit['description'] = log_msg.split('\n', 4)[4].strip()
	commit['timestamp'] = datetime.datetime.strptime(s, '%a %b %d %X %Y')
	if commit['timestamp'] <= endtime:
	    continue
	commits.append(commit)
    commits.sort(key=lambda x:x['timestamp'])
    return commits


def WriteCommits(pif, commits):
    print "Writing to activity table."
    for commit in commits:
	print commit
	pif.dbh.InsertActivity(**commit)
    print
    

def WriteConfigFile():
    print "Writing config file."
    cfg = open('../bin/config.py').readlines()
    cfg[0] = '<?php\n// Generated file.  Do not modify.\n'
    for idx in range(1, len(cfg)):
	if cfg[idx][0] == '#':
	    cfg[idx] = '//' + cg[idx][1:]
	elif cfg[idx].find('=') >= 0:
	    cfg[idx] = '$' + cfg[idx].replace('\n', ';\n')
    cfg.append('?>\n')
    open('config.php', 'w').writelines(cfg)
    print


def WriteManCSV(pif):
    print "Writing Man CSV file."
    manf = mannum.MannoFile(pif)
    manf.RunMan2CSV(pif)
    print


if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('editor', dbedit='')
    Main(pif)
