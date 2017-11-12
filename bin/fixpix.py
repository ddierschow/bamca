#!/usr/local/bin/python

import glob, os, sys
import basics
import config
import imglib
import useful


def ren(cas, ov, nv):
    fl = glob.glob(os.path.join(pth, '?_' + cas + '-' + ov + '.jpg'))
    for fn in fl:
        nn = fn[:fn.rfind('-')] + '-' + nv + '.jpg'
        print 'ren', fn, nn
        if not os.path.exists(nn):
            os.rename(fn, nn)


@basics.command_line
def main(pif):
    caslist = pif.filelist
    pth = '.' + config.IMG_DIR_VAR
    piclist = []
    casvars = {}

    for pic in glob.glob(os.path.join(pth, '*.jpg')):
        pic = pic[len(pth) + 1:-4]
        if pic[1] != '_' and pic.find('-') < 0:
            print 'bad:', pic
            continue
        pic = pic[2:]
        cas, var = pic.split('-', 1)
        casvars.setdefault(cas, [])
        casvars[cas].append(var)

    if not caslist:
	caslist = sorted(casvars.keys())

    for cas in caslist:
        dbvars = pif.dbh.fetch_variations(cas)
	casvar = casvars.get(cas, [])
        #print cas, [x['variation.var'].lower() for x in dbvars]
        for var in casvars[cas]:
            #print ' ', var
            found = False
            for dbvar in dbvars:
                if dbvar['variation.var'].lower() == var:
                    found = True
                    #print '    Ok', cas, var
                    break  # ok!
                if ('0' + dbvar['variation.var']).lower() == var:
                    ren(cas, var, var[1:])
                    found = True
                    break
                if ('00' + dbvar['variation.var']).lower() == var:
                    ren(cas, var, var[2:])
                    found = True
                    break
            if not found:
                if os.path.exists('.' + useful.relpath(config.LIB_MAN_DIR, cas)):
                    for src in glob.glob(os.path.join(pth, '?_' + cas + '-' + var + '.jpg')):
                        if not os.path.exists(useful.relpath('.', config.LIB_MAN_DIR, cas + src[src.rfind('/'):])):
                            print 'should rename', src, useful.relpath('.', config.LIB_MAN_DIR, cas + src[src.rfind('/'):])
                            #os.rename(src, useful.relpath('.', config.LIB_MAN_DIR, cas + src[src.rfind('/'):]))
                else:
                    print '    Bad var:', cas, var, [x['variation.var'] for x in dbvars]

	    for dbvar in dbvars:
		if not dbvar['variation.picture_id']:
		    fn = dbvar['variation.mod_id'] + '-' +  dbvar['variation.var'] + '.jpg'
		    ensmallen('.' + config.IMG_DIR_VAR, fn)


def ensmallen(pdir, fn):
    ipth = useful.relpath(pdir, 's_' + fn).lower()
    opth = useful.relpath(pdir, 't_' + fn).lower()
    if os.path.exists(ipth) and not os.path.exists(opth):
	print 'ensmallen', fn
	pipes = [['/usr/local/bin/jpegtopnm'], ["/usr/local/bin/pamscale", "-xsize", str(100)], ['/usr/local/bin/pnmtojpeg']]
	open(opth, 'w').write(imglib.pipe_chain(open(ipth), pipes))


if __name__ == '__main__':
    main()
