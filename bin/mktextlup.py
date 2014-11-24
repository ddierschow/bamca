#!/usr/local/bin/python

import basics
import lineup


@basics.CommandLine
def Main(pif):
    for y in pif.switch['y']:
        for r in pif.switch['r']:
            print lineup.TextMain(pif, y, r)

if __name__ == '__main__':  # pragma: no cover
    Main('editor', options='ry')
