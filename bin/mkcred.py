#!/usr/local/bin/python

import basics


def command_help(pif, *args):
    pif.render.message("./mkcred.py photographer_id file_path")


def set_credit(pif, photographer_id, fn):
    if not '/' in fn:
	print 'must have path:', fn
    else:
	pif.dbh.write_photo_credit(photographer_id, ddir, *fn.rsplit('/', 1))


@basics.command_line
def commands(pif):
    if pif.filelist:
	photographer_id = pif.filelist.pop(0)
	for fn in pif.filelist:
	    set_credit(pif, photographer_id, fn)
    else:
	command_help(pif)

#---- ---------------------------------------

if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='')
