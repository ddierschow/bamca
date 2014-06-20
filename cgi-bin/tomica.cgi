#!/usr/local/bin/python

import sys
sys.path.append("../bin")

if __name__ == '__main__':
    import basics
    import tomica
    basics.StartPage(tomica.Main, 'tomica')
