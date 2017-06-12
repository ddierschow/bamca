#!/usr/local/bin/python

import sys
import basics
import single


# Start here


@basics.command_line
def main(pif):
    count = 0
    showtexts = verbose = False
    #verbose = True
    #showtexts = True
    if not pif.filelist:
        castings = [x['id'] for x in pif.dbh.dbi.select('casting', verbose=False)]
    elif pif.filelist[0][0] >= 'a':
        castings = [x['id'] for x in pif.dbh.dbi.select('casting', where="section_id='%s'" % pif.filelist[0], verbose=False)]
    else:
        castings = pif.filelist
        verbose = True
    t_founds = [0, 0, 0, 0, 0, 0]
    t_needs = [0, 0, 0, 0, 0, 0]
    t_cnts = [0, 0, 0, 0, 0, 0, 0]
    def adder(into_arr, from_tup):
	return [sum(x) for x in zip(into_arr, from_tup)]

    print '(f_a, f_c, f_1, f_2, f_f, f_p), (n_a, n_c, n_1, n_2, n_f, n_p), (c_vars, c_de, c_ba, c_bo, c_in, c_wh, c_wi)'
    for mod_id in castings:
        #sys.stdout.write(casting + ' ')
        sys.stdout.flush()
	founds, needs, cnts = single.count_list_var_pics(pif, mod_id)
	print mod_id, founds, needs, cnts
	t_founds = adder(t_founds, founds)
	t_needs = adder(t_needs, needs)
	t_cnts = adder(t_cnts, cnts)
    print 'total', t_founds, t_needs, t_cnts

#    return (found_a, found_c, found_1, found_2, found_f, found_p), \
#	   (needs_a, needs_c, needs_1, needs_2, needs_f, needs_p), \
#	   (len(vars), count_de, count_ba, count_bo, count_in, count_wh, count_wi)


if __name__ == '__main__':  # pragma: no cover
    main()
