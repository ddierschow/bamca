#!/usr/local/bin/python

import os, sys
#os.environ['DOCUMENT_ROOT'] = '/usr/local/www/bamca/beta/htdocs'
#os.environ['SERVER_NAME'] = 'beta.bamca.org'
#sys.path.append('../../cgi-bin')
import basics
import manno

# Start here




def NumFormat(t):
    return '"=""%s"""' % t

def TextFormat(t):
    if '"' in t or ',' in t:
	t = '"' + t.replace('"', '""') + '"'
    return t


if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('manno')

    manf = manno.MannoFile(pif)
    manf.SetArguments(pif)
    of = open('pages/man.csv', 'w')

    of.write("MAN #,Year,Scale,Name,Notes\r\n")

    for sect in manf.slist:

	sect['models'].sort(key=lambda x: x['id'])
        for mod in sect['models']:

            mod = manf.DereferenceAlias(mod)

	    of.write(",".join([mod['id'], NumFormat(mod['first_year']), NumFormat(mod['scale']), TextFormat(mod['name']), TextFormat(', '.join(mod['descs']))]) + '\r\n')
