#!/usr/local/bin/python

import basics
import config
import lineup
import single


def check_man_mappings(pif, sections):
    for section in sections:
	mans = pif.dbh.fetch_casting_list(section_id=section, page_id='manno')
	mans.sort(key=lambda x: x['casting.id'])
	for man in mans:
	    cid = man['casting.id']
	    aliases = [x['alias.id'] for x in pif.dbh.fetch_aliases(cid, 'mack')]
	    mack_nums = single.get_mack_numbers(pif, cid, man['base_id.model_type'], aliases)
	    if not mack_nums:
		print cid


def check_mack_ranges(pif):
    letters = list('abcdefghijklmnopqrstuvwyz') + ['aa']
    ranks = {}
    mods = lineup.mack_models(pif, 1, config.MAX_MACK_NUMBER, ['SF'])
    num = 0
    for mod in mods:
	if num != int(mod['mack_id_unf'][1]):
	    num = int(mod['mack_id_unf'][1])
	    ranks[num] = set()
	ranks[num].add(mod['mack_id_unf'][2])
    for num in range(1, config.MAX_MACK_NUMBER + 1):
	s = ranks.get(num)
	if s:
	    missing = ''
	    for li in range(letters.index(max(s))):
		if letters[li] not in s:
		    missing += letters[li]
	    if missing:
		missing = '^' + missing
	    s1 = min(s)
	    s2 = max(s)
	    if s1 != s2:
		print '| %3d : %s-%s%-3s' % (num, s1, s2, missing)
	    else:
		print '| %3d : %s  %-3s' % (num, s1, missing)
	else:
	    print '| %3d :       ' % num


@basics.command_line
def main(pif):
    check_mack_ranges(pif)
    #check_man_mappings(pif, ['man', 'man2'])


if __name__ == '__main__':  # pragma: no cover
    main()
