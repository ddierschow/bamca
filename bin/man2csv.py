#!/usr/local/bin/python

import basics
import manno

if __name__ == '__main__': # pragma: no cover
    pif = basics.GetPageInfo('manno')
    manf = manno.MannoFile(pif)

    manf.RunMan2CSV(pif)
