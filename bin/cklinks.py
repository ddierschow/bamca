#!/usr/local/bin/python

import basics
import links

@basics.CommandLine
def Main(pif):
    links.CheckLinks(pif.filelist)

if __name__ == '__main__': # pragma: no cover
    Main('editor')
