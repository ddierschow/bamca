#!/usr/local/bin/python

import os, re
import basics

# Start here

def Blisters(fl):
    fn_re = re.compile('[0-9][0-9][a-z][0-9][0-9]*\.')
    cnt = 0
    for fn in fl:
        m = fn_re.match(fn)
        if m:
            pass  #print fn, 'yes'
            cnt += 1
        else:
            pass  #print fn, '-'
    return cnt


def Castings(fl):
    fn_re = re.compile('[a-z]_(?P<c>[a-z0-9]*)(-[a-z0-9]*)?\.')
    cnt = 0
    for fn in fl:
        m = fn_re.match(fn)
        if m:
            pass  #print fn, m.group('c')
            if m.group('c') in castings:
                cnt += 1
        else:
            pass  #print fn, '-'
    return cnt


def All(fl):
    return len(fl)


def Zero(fl):
    return 0


@basics.CommandLine
def Count(pif):
    castings = [x['id'].lower() for x in pif.dbh.dbi.select('casting', ['id'])]

    dirs = [
            ('acc',     All),
            ('add',     Castings),
            ('ads',     All),
            ('blister', All),
            ('box',     All),
            ('errors',  All),
            ('flags',   All),
            ('gfx',     Zero),  # not considered part of the collection
            ('king',    All),
            ('lesney',  All),
            ('man',     Castings),
            ('man/var', Castings),
            ('mattel',  Blisters),
            ('mcoll',   All),
            ('packs',   All),
            ('pages',   Zero),
            ('prem',    All),
            ('series',  All),
            ('sky',     All),
            ('tyco',    Blisters),
            ('univ',    Blisters),
    ]

    t = 0
    for d in dirs:
        fl = os.listdir('pic/' + d[0])
        dt = d[1](filter(lambda x: x.endswith('.jpg'), fl))
        dt += d[1](filter(lambda x: x.endswith('.gif'), fl))
        print d[0], dt
        t += dt
    print t


if __name__ == '__main__':  # pragma: no cover
    Count('vars')
