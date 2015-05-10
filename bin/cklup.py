#!/usr/local/bin/python

import basics
import lineup


def do_lup(pif, year, region):
    lup = lineup.run_file(pif, region, str(year))
    totals['i'] += lup['var_info']['i']
    totals['p'] += lup['var_info']['p']
    print '%d  %s  %3d  %3d' % (year, region, lup['var_info']['i'], lup['var_info']['p'])


@basics.command_line
def main(pif):
    totals = {'i': 0, 'p': 0}

    st = 1953
    en = 2014
    if pif.filelist:
        st = int(pif.filelist[0])
        if len(pif.filelist) > 1:
            en = int(pif.filelist[1])
        else:
            en = st
    for year in range(st, en + 1):
        pif.page_id = 'year.%d' % year
        lup = do_lup(pif, year, 'U')
        if year >= 1982:
            lup = do_lup(pif, year, 'R')
        if year in (1999, 2000, 2001):
            lup = do_lup(pif, year, 'D')
        if year in (2000, 2001):
            lup = do_lup(pif, year, 'B')
            lup = do_lup(pif, year, 'A')
        if year >= 2008 and year <= 2011:
            lup = do_lup(pif, year, 'L')
    print '        %4d %4d' % (totals['i'], totals['p'])


if __name__ == '__main__':  # pragma: no cover
    main()
