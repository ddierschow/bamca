#!/usr/local/bin/python

import glob, os, sys
import basics
import config


def ren(cas, ov, nv):
    fl = glob.glob(os.path.join(pth, '?_' + cas + '-' + ov + '.jpg'))
    for fn in fl:
        nn = fn[:fn.rfind('-')] + '-' + nv + '.jpg'
        print 'ren', fn, nn
        if not os.path.exists(nn):
            os.rename(fn, nn)


def main(pif):
    pth = 'pic/man/var'
    piclist = []
    casvar = {}

    for pic in glob.glob(os.path.join(pth, '*.jpg')):
        pic = pic[len(pth) + 1:-4]
        if pic[1] != '_' and pic.find('-') < 0:
            print 'bad:', pic
            continue
        pic = pic[2:]
        cas, var = pic.split('-', 1)
        casvar.setdefault(cas, [])
        casvar[cas].append(var)

    for cas in casvar:
        dbvars = pif.dbh.fetch_variations(cas)
        #print cas, [x['variation.var'].lower() for x in dbvars]
        for var in casvar[cas]:
            #print ' ', var
            found = False
            for dbvar in dbvars:
                if dbvar['variation.var'] == var:
                    found = True
                    #print '    Ok', cas, var
                    break  # ok!
                if ('0' + dbvar['variation.var']) == var:
                    ren(cas, var, var[1:])
                    found = True
                    break
                if ('00' + dbvar['variation.var']) == var:
                    ren(cas, var, var[2:])
                    found = True
                    break
            if not found:
                if os.path.exists(os.path.join(config.LIB_MAN_DIR, cas)):
                    for src in glob.glob(os.path.join(pth, '?_' + cas + '-' + var + '.jpg')):
                        if not os.path.exists(os.path.join(config.LIB_MAN_DIR, cas + src[src.rfind('/'):])):
                            os.rename(src, os.path.join(config.LIB_MAN_DIR, cas + src[src.rfind('/'):]))
                else:
                    print '    Bad var:', cas, var, [x['variation.var'] for x in dbvars]


if __name__ == '__main__':
    pif = basics.get_page_info('vars')
    main(pif)
