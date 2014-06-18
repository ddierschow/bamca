#!/usr/local/bin/python

import os, sys
import cmdline
os.environ['DOCUMENT_ROOT'] = '/usr/local/www/bamca/www/htdocs'
os.environ['SERVER_NAME'] = 'www.bamca.org'
sys.path.append('../../cgi-bin')
import basics
import mbdata
import config
import manno
pif = basics.GetPageInfo('manno')

# Start here




def NumFormat(t):
    return '"=""%s"""' % t

def TextFormat(t):
    if '"' in t or ',' in t:
	t = '"' + t.replace('"', '""') + '"'
    return t


if __name__ == '__main__':
    sys.path.append('../../cgi-bin')

    manf = manno.MannoFile(pif)
    manf.SetArguments(pif)
    print os.getcwd(), 'pages/man.csv'
    outf = open('pages/man.csv', 'w')

    outf.write("MAN #,Year,Scale,Name,Notes\r\n")

    for sect in manf.slist:

        for mod in sect['models']:

            mod = manf.DereferenceAlias(mod)

	    print mod['id']
	    outf.write(",".join([mod['id'], NumFormat(mod['first_year']), NumFormat(mod['scale']), TextFormat(mod['name']), TextFormat(', '.join(mod['descs']))]) + '\r\n')

    outf.close()
