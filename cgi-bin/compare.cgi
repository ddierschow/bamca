#!/usr/local/bin/python

import sys
sys.path.append("../bin")

if __name__ == '__main__':
    import basics
    import manno
    basics.StartPage(manno.CompareMain, 'compare')
