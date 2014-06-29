#!/usr/local/bin/python

import os, sys
import cmdline
#os.environ['DOCUMENT_ROOT'] = '/usr/local/www/bamca/beta/htdocs'
#os.environ['SERVER_NAME'] = 'beta.bamca.org'
#sys.path.append('../../cgi-bin')
import basics
import mbdata
import config

# Start here



if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('vars')

    aliases = pif.dbh.FetchAliases()
    lmodels = pif.dbh.FetchLineupModels()

    a_dict = {x['alias.id']: x for x in aliases}
    for lmodel in lmodels:
	if lmodel['lineup_model.letter']:
	    id = '%(base_id.model_type)s%(lineup_model.number)02d%(lineup_model.letter)s' % lmodel
	    if id == lmodel['base_id.id']:
		pass
	    elif id not in a_dict:
		print 'new', id, lmodel['base_id.id']
	    elif lmodel['base_id.id'] != a_dict[id]['alias.ref_id']:
		print 'bad', id, lmodel['base_id.id'], a_dict[id]['alias.ref_id']

