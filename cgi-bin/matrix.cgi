#!/usr/local/bin/python

import sys
sys.path.append("../bin")

if __name__ == '__main__':
    import basics
    import matrix
    basics.StartPage(matrix.Main, 'matrix', 'page')
