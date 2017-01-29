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


@basics.command_line
def main(pif):
    for field in fields:
        pif.dbh.dbi.execute("update variation set %s='' where %s is NULL" % (field, field))
    count = 0
    showtexts = verbose = False
    #verbose = True
    #showtexts = True
    if not pif.filelist:
        castings = [x['id'] for x in pif.dbh.dbi.select('casting', verbose=False)]
    elif pif.filelist[0][0] >= 'a':
        castings = [x['id'] for x in pif.dbh.dbi.select('casting', where="section_id='%s'" % pif.filelist[0], verbose=False)]
    else:
        castings = pif.filelist
        verbose = True
    for casting in castings:
        #sys.stdout.write(casting + ' ')
        sys.stdout.flush()
	print casting,
        fmt_invalid, messages = pif.dbh.check_description_formatting(casting)
        if fmt_invalid:
            print '*'
	    if verbose:
		print messages
            count += 1
        else:
            print
        pif.dbh.recalc_description(casting, showtexts, verbose)
    print
    print count, "to go *"


if __name__ == '__main__':  # pragma: no cover
    main(dbedit='')
