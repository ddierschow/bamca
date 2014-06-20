#!/usr/local/bin/python

import glob, os, sys

def ren(cas, ov, nv):
    fl = glob.glob(os.path.join(pth, '?_' + cas + '-' + ov + '.jpg'))
    for fn in fl:
	nn = fn[:fn.rfind('-')] + '-' + nv + '.jpg'
	print 'ren', fn, nn
	if not os.path.exists(nn):
	    os.rename(fn, nn)


def Main(pif):
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
	dbvars = pif.dbh.FetchVariations(cas)
	#print cas, map(lambda x: x['variation.var'].lower(), dbvars)
	for var in casvar[cas]:
	    #print ' ', var
	    found = False
	    for dbvar in dbvars:
		if dbvar['variation.var'] == var:
		    found = True
		    #print '    Ok', cas, var
		    break # ok!
		if ('0' + dbvar['variation.var']) == var:
		    ren(cas, var, var[1:])
		    found = True
		    break
		if ('00' + dbvar['variation.var']) == var:
		    ren(cas, var, var[2:])
		    found = True
		    break
	    if not found:
		if os.path.exists('lib/' + cas):
		    for src in glob.glob(pth + '/' + '?_' + cas + '-' + var + '.jpg'):
			if not os.path.exists('lib/' + cas + src[src.rfind('/'):]):
			    os.rename(src, 'lib/' + cas + src[src.rfind('/'):])
		else:
		    print '    Bad var:', cas, var, map(lambda x: x['variation.var'], dbvars)


if __name__ == '__main__':
    import basics
    pif = basics.GetPageInfo('vars')
    Main(pif)
