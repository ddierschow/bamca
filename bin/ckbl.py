#!/usr/local/bin/python

import basics
import tlinks

@basics.CommandLine
def Main(pif):
    tlinks.CheckBlacklistedLinks(pif, pif.filelist)

if __name__ == '__main__': # pragma: no cover
    Main('editor')
