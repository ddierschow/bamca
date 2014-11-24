#!/usr/local/bin/python

import basics
import mannum

if __name__ == '__main__':  # pragma: no cover
    pif = basics.GetPageInfo('manno')
    manf = mannum.MannoFile(pif)

    manf.RunMan2CSV(pif)
