#!/usr/local/bin/python

import os
import basics
import config
import mbdata

# Start here


def model(pif, mod):
    # formerly regions S, M and J were excluded, but there are no longer any entries with these regions.
    yrs = pif.dbh.dbi.execute("select distinct year from lineup_model where mod_id='%s'" % mod)[0]
    yrs = [x[0] for x in yrs]
    yrs.sort()

    sel = pif.dbh.dbi.execute("select distinct ref_id from variation_select where mod_id='%s'" % mod)[0]
    sel = [x[0][:9] for x in sel]

    missing = []
    for yr in yrs:
        if not 'year.' + yr in sel:
            missing.append(yr)
    bad = []
    for pg in sel:
        if pg.startswith('year.') and not pg[5:9] in yrs:
            bad.append(pg)
    return missing, bad


def show_list_var_pics(pif, mod_id):
    vars = pif.dbh.fetch_variations(mod_id)
    cpics = cfound = pics = found = 0
    for var in vars:
        var = pif.dbh.depref('variation', var)
        if var['var'].startswith('f') or mbdata.categories.get(var['category'], '').startswith('['):
            continue
        elif not var['picture_id']:
            fn = mod_id + '-' + var['var']
            pid = var['var']
        elif var['picture_id'] == var['var']:
            fn = mod_id + '-' + var['picture_id']
            pid = var['picture_id']
        else:
            continue
	pic_path = pif.render.find_image_file(fnames=fn, vars=pid, prefix=mbdata.IMG_SIZ_SMALL)
        pics += 1
        if not var['category']:
            cpics += 1
#        print '<!--', config.IMG_DIR_MAN + '/var/' + fn + '.jpg', '-->'
        #if os.path.exists(config.IMG_DIR_MAN + '/var/s_' + fn.lower() + '.jpg'):
	if pic_path:
            found += 1
            if not var['category']:
                cfound += 1
    af = '%d/%d' % (found, pics)
    cf = '%d/%d' % (cfound, cpics)
    if found == pics:
        af = '--'
    if cfound == cpics:
        cf = '--'
    return af, cf


@basics.command_line
def main(pif):

    specs = pif.filelist

    sw = []
    if specs[0][0] == '0':
        sw = list(specs[0][1:])
        specs = specs[1:]

    for spec in specs:
        mods = pif.dbh.dbi.execute("select distinct id from casting where id like '%s%%'" % spec)[0]
        mods = [x[0] for x in mods]
        mods.sort()

        for mod in mods:
            missing, bad = model(pif, mod)
            af, cf = show_list_var_pics(pif, mod)

            if 'a' in sw or 'p' in sw or missing or bad or af != '--' or cf != '--':
                print mod,
            if 'p' in sw or af != '--' or cf != '--':
                print af, cf,
            if missing:
                print 'needs', ' '.join(missing),

            if bad:
                print 'has bad', ' '.join(bad),

            if 'a' in sw or 'p' in sw or missing or bad or af != '--' or cf != '--':
                print

if __name__ == '__main__':  # pragma: no cover
    main()
