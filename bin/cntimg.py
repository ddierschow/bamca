#!/usr/local/bin/python

import os, re
import basics


# Start here


def blisters(fl):
    fn_re = re.compile('[0-9][0-9][a-z][0-9][0-9]*\.')
    cnt = 0
    for fn in fl:
        m = fn_re.match(fn)
        if m:
            pass  # print fn, 'yes'
            cnt += 1
        else:
            pass  # print fn, '-'
    return cnt


def count_castings(fl):
    global castings
    fn_re = re.compile('[a-z]_(?P<c>[a-z0-9]*)(-[a-z0-9]*)?\.')
    cnt = 0
    for fn in fl:
        m = fn_re.match(fn)
        if m:
            pass  # print fn, m.group('c')
            if m.group('c') in castings:
                cnt += 1
        else:
            pass  # print fn, '-'
    return cnt


def count_all(fl):
    return len(fl)


def zero(fl):
    return 0


@basics.command_line
def count(pif):
    global castings
    castings = [x['id'].lower() for x in pif.dbh.dbi.select('casting', ['id'])]

    dirs = [
        ('set/acc',     count_all),
        ('man/add',     count_castings),
        ('pub/ads',     count_all),
        ('pub/blister', count_all),
        ('pub/box',     count_all),
        ('set/error',   count_all),
        ('flags',       count_all),
        ('gfx',         zero),  # not considered part of the collection
        ('set/king',    count_all),
        ('set/lesney',  count_all),
        ('man',         count_castings),
        ('man/var',     count_castings),
        ('prod/mattel', blisters),
        ('set/mcoll',   count_all),
        ('prod/pack',   count_all),
        ('pages',       zero),
        ('prod/prem',   count_all),
        ('prod/series', count_all),
        ('set/sky',     count_all),
        ('prod/tyco',   blisters),
        ('prod/univ',   blisters),
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
    print "This has not been rewritten to match the moved directories."
    count()
