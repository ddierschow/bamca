#!/usr/local/bin/python

import sys
import basics
import vars

fields = [
        'text_body',
        'text_interior',
        'text_windows',
        'text_base',
        'text_wheels',
        'text_description',
        'body',
        'base',
        'windows',
        'interior',
        'category',
        'area',
        'date',
        'note',
        'other',
        'picture_id',
        'manufacture',
]


@basics.CommandLine
def Main(pif):
    for field in fields:
        pif.dbh.dbi.execute("update variation set %s='' where %s is NULL" % (field, field))
    count = 0
    verbose = False
    #verbose = True
    if not pif.filelist:
        castings = [x['id'] for x in pif.dbh.dbi.select('casting', verbose=False)]
    elif pif.filelist[0][0] >= 'a':
        castings = [x['id'] for x in pif.dbh.dbi.select('casting', where="section_id='%s'" % pif.filelist[0], verbose=False)]
    else:
        castings = pif.filelist
        verbose = True
    for casting in castings:
        sys.stdout.write(casting + ' ')
        sys.stdout.flush()
        if vars.CheckFormatting(pif, casting, verbose=verbose):
            print '*'
            count += 1
        else:
            print
        vars.RecalcDescription(pif, casting, verbose)
    print
    print count, "to go *"


if __name__ == '__main__':  # pragma: no cover
    Main('vars')
