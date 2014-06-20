#!/usr/local/bin/python

import sys
sys.path.append("../bin")

if __name__ == '__main__':
    import basics
    import links
    basics.StartPage(links.AddPage, 'addlink', dbedit=True)
