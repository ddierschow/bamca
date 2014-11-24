#!/usr/local/bin/python

import glob, os, re, sys, urllib2

def Main():
    src = 'http://www.mbxforum.com/11-Catalogs/02-MB75/MB75-Documents/'
    ln_re = re.compile('''<img src=".*?".*?> <a href="(?P<f>[^"]*)">''')

    flist = urllib2.urlopen(src).readlines()
    olist = glob.glob('orig/*.doc')

    for ln in flist:
        mat = ln_re.match(ln)
        if not mat:
            continue
        if not mat.group('f').endswith('.doc'):
            continue
        if not os.path.exists('orig/' + mat.group('f')):
            print mat.group('f'), 'not on dest'
        else:
            olist.remove('orig/' + mat.group('f'))
    for fn in olist:
        print fn, 'not on source'

if __name__ == '__main__':  # pragma: no cover
    Main()
