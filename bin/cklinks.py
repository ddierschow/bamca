#!/usr/local/bin/python

import basics
import tlinks


@basics.command_line
def main(pif):
    retest = visible = False
    if 'retest' in pif.filelist:
	retest = True
	pif.filelist.remove('retest')
    if 'visible' in pif.filelist:
	visible = True
	pif.filelist.remove('visible')
    tlinks.check_links(pif, pif.filelist, retest=retest, visible=visible)

if __name__ == '__main__':  # pragma: no cover
    main(dbedit='')
