#!/usr/local/bin/python

import os
import basics
import config
import mbdata

verbose = False


def run_models(pif, mods):
    upics = spics = spfnd = cpics = cpfnd = mpics = mpfnd = apics = apfnd = 0
    mods = [x[0] for x in mods]
    mods.sort()

    for mod in mods:
        uf, af, mf, cf, sf = show_list_var_pics(pif, mod)
        if (not pif.switch['q']) and \
           (not pif.switch['s'] or sf[2] < 100) and \
           (not pif.switch['c'] or cf[2] < 100) and \
           (not pif.switch['m'] or mf[2] < 100) and \
           (not pif.switch['a'] or af[2] < 100):
            print '%-8s%5d | %3d/%3d |%3d%% | %3d/%3d |%3d%% | %3d/%3d |%3d%% | %3d/%3d |%3d%%' % ((mod, uf) + af + mf + cf + sf)

        upics += uf
        spics += sf[1]
        spfnd += sf[0]
        cpics += cf[1]
        cpfnd += cf[0]
        mpics += mf[1]
        mpfnd += mf[0]
        apics += af[1]
        apfnd += af[0]

    return upics, spics, spfnd, cpics, cpfnd, mpics, mpfnd, apics, apfnd


def show_list_var_pics(pif, mod_id):
    upics = spics = spfnd = cpics = cpfnd = mpics = mpfnd = apics = apfnd = 0
    varsels = pif.dbh.fetch_variation_selects(mod_id)
    varsel = {}
    for vs in varsels:
        varsel.setdefault(vs['variation_select.ref_id'], [])
        varsel[vs['variation_select.ref_id']].append(vs['variation_select.var_id'])
    spics = len(varsel.keys())

    vars = pif.dbh.fetch_variations(mod_id)
    for var in vars:
        isorig = 1
        fn = mod_id + '-' + var['variation.var']
        if var['variation.picture_id']:
            fn = mod_id + '-' + var['variation.picture_id']
            isorig = 0
        fn = config.IMG_DIR_MAN + '/var/s_' + fn.lower() + '.jpg'
        apics += 1
        if not var['variation.var'].startswith('f'):
            if not mbdata.categories.get(var['variation.category'], '').startswith('['):
                mpics += 1
            if not var['variation.category']:
                cpics += 1
#        print '<!--', config.IMG_DIR_MAN + '/var/' + fn + '.jpg', '-->'
        if os.path.exists(fn):
            apfnd += 1
            upics += isorig
            if not var['variation.var'].startswith('f'):
                if not mbdata.categories.get(var['variation.category'], '').startswith('['):
                    mpfnd += 1
                if not var['variation.category']:
                    cpfnd += 1
            for vs in varsel:
                if var['variation.var'] in varsel[vs]:
                    spfnd += 1
                    varsel[vs] = []
    if verbose:
        print ' '.join(filter(lambda x: varsel[x], varsel))
    return upics, format_calc(apfnd, apics), format_calc(mpfnd, mpics), format_calc(cpfnd, cpics), format_calc(spfnd, spics)


def format_calc(found, pics):
    if 0:  # found == pics:
        return (found, pics, '--')
    if pics:
        return (found, pics, 100 * found / pics)
    return (0, 0, 100)


@basics.command_line
def main(pif):

    upics = nmods = spics = spfnd = cpics = cpfnd = mpics = mpfnd = apics = apfnd = 0

    if pif.switch['v']:
        verbose = True
    if pif.filelist:
        for spec in pif.filelist:
            mods = pif.dbh.dbi.execute("select distinct id from casting where id like '%s%%'" % spec)[0]
            nmods += len(mods)
            uf, sp, sf, cp, cf, mp, mf, ap, af = run_models(pif, mods)

            upics += uf
            spics += sp
            spfnd += sf
            cpics += cp
            cpfnd += cf
            mpics += mp
            mpfnd += mf
            apics += ap
            apfnd += af

    else:
        mods = pif.dbh.dbi.execute("select distinct id from casting")[0]
        nmods += len(mods)
        uf, sp, sf, cp, cf, mp, mf, ap, af = run_models(pif, mods)

        upics += uf
        spics += sp
        spfnd += sf
        cpics += cp
        cpfnd += cf
        mpics += mp
        mpfnd += mf
        apics += ap
        apfnd += af

    print
    print '%7d %5d  %3d/%3d %3d%%  %3d/%3d %3d%%  %3d/%3d %3d%%  %3d/%3d %3d%%' % \
          ((nmods, upics) +
           format_calc(apfnd, apics) + format_calc(mpfnd, mpics) + format_calc(cpfnd, cpics) + format_calc(spfnd, spics))

if __name__ == '__main__':  # pragma: no cover
    main('vars', switches='qvscma')
