#!/usr/local/bin/python

import basics
import mbdata

# check for duplicate entries in tables
# existing code silently smushes these so we need to look for them to clean them up

@basics.command_line
def main(pif):
    check_matrix_model(pif)
    check_lineup_model(pif)
    check_detail(pif)


def check_q(rows):
    problems = set()
    for row in rows:
	if row[-1] > 1:
	    problems.add(row[:-1])
    print problems if problems else 'all ok'


def check_matrix_model(pif):
    print 'matrix_model'
    res = pif.dbh.raw_execute('''select page_id, section_id, range_id, count(*) from matrix_model group by page_id, section_id, range_id''')
    check_q(res[0])


def check_lineup_model(pif):
    print 'lineup_model'
    res = pif.dbh.raw_execute('''select page_id, region, number, count(*) from lineup_model group by page_id, region, number''')
    check_q(res[0])
    return
    problems = set()
    for row in res[0]:
	if row[3] > 1:
	    problems.add(row[:2])
    print problems if problems else 'all ok'


def check_detail(pif):
    print 'detail'
    res = pif.dbh.raw_execute('''select mod_id, var_id, attr_id, count(*) from detail group by mod_id, var_id, attr_id''')
    check_q(res[0])
    return
    problems = set()
    for row in res[0]:
	if row[3] > 1:
	    problems.add(row[:2])
    print problems


if __name__ == '__main__':  # pragma: no cover
    main(page_id='editor', switches='l')
