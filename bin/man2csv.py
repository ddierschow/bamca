#!/usr/local/bin/python

import basics
import mannum

if __name__ == '__main__':  # pragma: no cover
    pif = basics.get_page_info('manno')
    manf = mannum.MannoFile(pif)

    manf.run_man2csv(pif)
