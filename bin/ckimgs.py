#!/usr/local/bin/python

import glob, os
import basics
import config
import imglib

@basics.command_line
def main(pif):
    global casting_ids, variation_ids

    casting_ids = [x['base_id.id'].lower() for x in pif.dbh.fetch_base_ids()]
    variation_ids = [x['variation.mod_id'].lower() + '-' + x['variation.var'].lower() for x in pif.dbh.fetch_variations_bare()]

    for key in sorted(checks.keys()):
	if checks[key]:
	    print key
	    checks[key](pif, key)
	    print


def check_blister(pif, dn):
    pass

def check_box(pif, dn):
    pass

def check_man(pif, dn):
    files = glob.glob('.' + dn + '/*.*')
    files.sort()
    c = 0
    for fn in files:
	try:
	    root, ext = os.path.splitext(os.path.basename(fn))
	    if not ext or ext[1:] not in imglib.itypes:
		continue
	    root = root.lower()
	    var = ''
	    if '-' in root:
		root, var = root.rsplit('-', 1)
	    if len(root) > 1 and root[1] == '_':
		root = root[2:]
	    if root not in casting_ids:
		print fn, "missing base", root
	    elif var and (root + '-' + var) not in variation_ids:
		print fn, "missing var", root, var
	    else:
		c += 1
	except:
	    print fn, "fail"
	    raise
    print c, 'ok'

def check_package(pif, dn):
    pass

def check_set(pif, dn):
    pass


checks = {
    config.IMG_DIR_ACC:              check_set,
    config.IMG_DIR_ADD:              check_man,
    config.IMG_DIR_BLISTER:          check_blister,
    config.IMG_DIR_BOX:              check_box,
    config.IMG_DIR_CAT:              None,
    config.IMG_DIR_PROD_CODE_2:      None,
    config.IMG_DIR_COLL_43:          check_package,
    config.IMG_DIR_PROD_COLL_64:     check_package,
    config.IMG_DIR_ICON:             check_man,
    config.IMG_DIR_KING:             check_man,
    config.IMG_DIR_LESNEY:           check_set,
    config.IMG_DIR_PROD_LRW:         check_package,
    config.IMG_DIR_PROD_LSF:         check_package,
    config.IMG_DIR_MAN:              check_man,
    config.IMG_DIR_PROD_MWORLD:      check_package,
    config.IMG_DIR_PROD_EL_SEG:      check_package,
    config.IMG_DIR_PROD_MT_LAUREL:   check_package,
    config.IMG_DIR_PROD_PACK:        check_package,
    config.IMG_DIR_PROD_SERIES:      check_package,
    config.IMG_DIR_SKY:              None,
    config.IMG_DIR_PROD_TYCO:        check_package,
    config.IMG_DIR_PROD_UNIV:        check_package,
    config.IMG_DIR_VAR:              check_man,
}


#---- ---------------------------------------

if __name__ == '__main__':  # pragma: no cover
    main()
