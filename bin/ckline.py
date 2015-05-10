#!/usr/local/bin/python

import basics


def check(pif, reg, num, yr, man, d):
    num = int(num.replace(' ', ''))
    if not num:
        return
    man = man.replace(' ', '')
    if man.startswith('MW') and man[2] < '7':
        man = 'MB' + man[2:]
    if man.startswith('MI') and man[2] < '7':
        man = 'MB' + man[2:]
    rec = pif.dbh.dbi.select("lineup_model", where="region='%s' and number='%d' and year='%d'" % (reg, num, yr))
    if len(rec) > 1:
        for r in rec:
            print "dup", r
        id = rec[-1]['id']
        del rec[0]['id']
        del rec[-1]['id']
        if rec[0] == rec[-1]:
            print "rm", id
            pif.dbh.dbi.remove("lineup_model", where="id=%d" % id)
        print
    elif len(rec) < 1:
        print reg, num, yr, man, "no record!"
    elif man.lower() != rec[0]['mod_id'].lower():
        print reg, num, yr, man, "diff"
        print '  mine', rec[0]
        print '  mbxf', d
        print


@basics.command_line
def main(pif):

    for fn in pif.filelist:
        yr = int(fn)
        if yr < 53:
            yr += 2000
        else:
            yr += 1900

        od = {}
        fil = open('cf/lines/All' + fn + '.dat')
        for ln in fil.readlines():
            arr = [x.strip() for x in ln.split('|')]
            if arr[0] == 'h':
                hdr = [x.replace(' ', '') for x in arr]
            elif arr[0] == 'e':
                d = dict(zip(hdr, arr))

                if 'CAT#' in d and not d['CAT#']:
                    d['CAT#'] = od.get('CAT#', '')
                if 'MAN#' in d and not d['MAN#']:
                    d['MAN#'] = od.get('MAN#', '')
                if 'Name' in d and not d['Name']:
                    d['Name'] = od.get('Name', '')
                if 'Model name' in d and not d['Model name']:
                    d['Model name'] = od.get('Model name', '')
                if 'Description' in d and not d['Description']:
                    d['Description'] = od.get('Description', '')
                if 'MACK#' in d and not d['MACK#']:
                    d['MACK#'] = od.get('MACK#', '')
                if 'Area' in d:
                    if 'MAN#' in d:
                        if d.get('USA#', ''):
                            check(pif, 'U', d['USA#'], yr, d['MAN#'], d)
                        if d.get('D#', ''):
                            check(pif, 'R', d['ROW#'], yr, d['MAN#'], d)
                    else:
                        if d.get('USA#', ''):
                            check(pif, 'U', d['USA#'], yr, d['CAT#'], d)
                        if d.get('D#', ''):
                            check(pif, 'R', d['ROW#'], yr, d['CAT#'], d)
                else:
                    if d.get('USA#', ''):
                        check(pif, 'U', d['USA#'][1:], yr, d['MAN#'], d)
                    if d.get('D#', ''):
                        check(pif, 'D', d['D#'][1:], yr, d['MAN#'], d)
                    if d.get('GB#', ''):
                        check(pif, 'B', d['GB#'][1:], yr, d['MAN#'], d)
                    if d.get('AUS#', ''):
                        check(pif, 'A', d['AUS#'][1:], yr, d['MAN#'], d)
                    if d.get('LAAM#', ''):
                        check(pif, 'L', d['LAAM#'][1:], yr, d['MAN#'], d)
                    if d.get('ROW#', ''):
                        check(pif, 'R', d['ROW#'][1:], yr, d['MAN#'], d)
                    if d.get('MW#', ''):
                        check(pif, 'U', d['MW#'], yr, d['MAN#'], d)
                        check(pif, 'R', d['MW#'], yr, d['MAN#'], d)
                od = d

if __name__ == '__main__':  # pragma: no cover
    main()
