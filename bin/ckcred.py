#!/usr/local/bin/python

import glob, os
import basics

root = '/usr/local/www/bamca'

'''
Checks photo credits, deleting any that are dups or dangling, reporting
dups that are different.

Current creds only apply to
| pic/man     |
| pic/man/var |
| pic/man/add |
but this will change.

Would like to make sure that all pictures apply to database objects as well.
'''

@basics.command_line
def main(pif):
    pids = {}
    creds = {x['id']: x for x in pif.dbh.depref('photo_credit', pif.dbh.fetch_photo_credits_raw())}
    for cred in creds.values():
	pid = (cred['path'], cred['name'], )
	if pid in pids:
	    if cred['photographer_id'] == creds[pids[pid]]['photographer_id']:
		pif.dbh.delete_photo_credit(cred['id'])
		print 'del', pid, cred['id'], pids[pid]
		continue
	    print 'dup', pid, cred['id'], cred['photographer_id'], pids[pid], creds[pids[pid]]['photographer_id']
	if cred['name'][1] == '_':
	    path = cred['path'] + '/' + cred['name'] + '.*'
	else:
	    path = cred['path'] + '/[tsml]_' + cred['name'] + '.*'
	files = glob.glob(root + '/' + path)
	if not files:
	    print 'n/f', pid, cred['id']
	    pif.dbh.delete_photo_credit(cred['id'])
	    continue
	pids[pid] = cred['id']

if __name__ == '__main__':  # pragma: no cover
    main(page_id='editor', switches='', dbedit='')
