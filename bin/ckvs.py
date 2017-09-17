#!/usr/local/bin/python

import basics

@basics.command_line
def main(pif):
    print 'missing models'
    res = pif.dbh.raw_execute('''select mod_id, id from variation_select where mod_id not in (select mod_id from casting);''')
    for r in res[0]:
	print r

    print 'missing variations'
    res = pif.dbh.raw_execute('''select mod_id, var_id, id from variation_select where (mod_id, var_id) not in (select mod_id, var from variation);''')
    for r in res[0]:
	print r

    print 'missing pages'
    res = pif.dbh.raw_execute('''select ref_id, id from variation_select where ref_id != '' and ref_id not in (select id var from page_info);''')
    for r in res[0]:
	print r


if __name__ == '__main__':  # pragma: no cover
    main(page_id='editor', switches='l')
