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


def castings(fl):
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
    castings = [x['id'].lower() for x in pif.dbh.dbi.select('casting', ['id'])]

    dirs = [
        ('acc',     count_all),
        ('add',     castings),
        ('ads',     count_all),
        ('blister', count_all),
        ('box',     count_all),
        ('errors',  count_all),
        ('flags',   count_all),
        ('gfx',     zero),  # not considered part of the collection
        ('king',    count_all),
        ('lesney',  count_all),
        ('man',     castings),
        ('man/var', castings),
        ('mattel',  blisters),
        ('mcoll',   count_all),
        ('packs',   count_all),
        ('pages',   zero),
        ('prem',    count_all),
        ('series',  count_all),
        ('sky',     count_all),
        ('tyco',    blisters),
        ('univ',    blisters),
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
    count('vars')
