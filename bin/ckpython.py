#!/usr/local/bin/python

import copy
import basics

imports = dict()

def import_anal(imports, lev_list, fn):
    if fn in lev_list:
	print '***', lev_list, fn
    my_levs = copy.deepcopy(lev_list)
    my_levs.append(fn)
    for im in imports[fn]:
	if im in imports:
	    import_anal(imports, my_levs, im)


@basics.standalone
def main(switch, files):  # pragma: no cover
    for fn in files:
	imports[fn[:-3]] = list()
	for ln in open(fn).readlines():
	    if ln.startswith('import '):
		imports[fn[:-3]].extend([x.strip() for x in ln[6:].split(',')])
	    elif ln.startswith('from '):
		ln = ln[5:]
		ln = ln[:ln.find(' ')]
		imports[fn[:-3]].append(ln)

    lev_list = list()
    for fn in imports:
	import_anal(imports, lev_list, fn)

if __name__ == '__main__':
    main()
