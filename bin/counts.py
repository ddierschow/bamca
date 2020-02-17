#!/usr/local/bin/python

from sprint import sprint as print
import glob
from io import open
import os
import re

import basics
import config
import imglib
import lineup
import mbdata
import multip


# Start here

href_re = re.compile(r'''<a href=".*?">''')


def report(area, im_count, pr_count=0):
    print("%-23s %6d / %6d" % (area, im_count, pr_count))


def count_html(fpath):
    fim = open(fpath).read()
    count = 0
    for href in href_re.findall(fim):
        if '/' not in href:
            count += 1
    report(fpath, count, count)
    return count


def count_directory(pdir):
    count = len(glob.glob('.' + pdir + '/*.jpg'))
    report(pdir, count, count)
    return count


def count_combo_one_only(pdir, prefs, roots, suffs):
    count = 0
    for root in roots:
        found = False
        for pref in prefs:
            for suff in suffs:
                for ext in imglib.otypes:
                    fl = glob.glob('./{}/{}{}{}.{}'.format(pdir, pref, root, suff, ext))
                    for fn in fl:
                        if os.path.exists(fn):
                            count += 1
                            found = True
                            break
                    if found:
                        found = True
                        break
                if found:
                    found = True
                    break
            if found:
                found = True
                break
    report(pdir, count, len(roots))
    return count


def count_combo(pdir, prefs, roots, suffs):
    count = 0
    for root in roots:
        for pref in prefs:
            for suff in suffs:
                for ext in imglib.otypes:
                    fl = glob.glob('./{}/{}{}{}.{}'.format(pdir, pref + '_' if pref else '', root, suff, ext))
                    for fn in fl:
                        if os.path.exists(fn):
                            count += 1
    report(pdir, count, len(roots))
    return count


def get_year(pif, region, year):
    if year < 1970:
        pif.render.pic_dir = config.IMG_DIR_PROD_LRW
    elif year < 1982:
        pif.render.pic_dir = config.IMG_DIR_PROD_LSF
    elif year < 1993:
        pif.render.pic_dir = config.IMG_DIR_PROD_UNIV
    elif year < 1998:
        pif.render.pic_dir = config.IMG_DIR_PROD_TYCO
    elif year < 2005:
        pif.render.pic_dir = config.IMG_DIR_PROD_MT_LAUREL
    elif year < 2016:
        pif.render.pic_dir = config.IMG_DIR_PROD_EL_SEG
    else:
        pif.render.pic_dir = config.IMG_DIR_PROD_MWORLD
    return lineup.picture_count(pif, region, str(year))


def get_years(pif, region, ystart, yend, pr_count, im_count):
    for year in range(ystart, yend + 1):
        count = get_year(pif, region, year)
        pr_count += count[0]
        im_count += count[1]
        print("    %s  %s  %-4d / %-4d" % (year, region, count[1], count[0]))
    return pr_count, im_count


def count_lineups(pif):
    pr_count = im_count = 0
    answer = pif.dbh.dbi.rawquery("select min(year), max(year) from lineup_model")[0]
    ystart = int(answer['min(year)'])
    yend = int(answer['max(year)'])
    pr_count, im_count = get_years(pif, 'W', ystart, 1970, pr_count, im_count)
    pr_count, im_count = get_years(pif, 'U', 1971, yend, pr_count, im_count)
    pr_count, im_count = get_years(pif, 'R', 1971, yend, pr_count, im_count)
    pr_count, im_count = get_years(pif, 'L', 2008, 2011, pr_count, im_count)
    pr_count, im_count = get_years(pif, 'D', 1999, 2001, pr_count, im_count)
    pr_count, im_count = get_years(pif, 'B', 2000, 2001, pr_count, im_count)
    pr_count, im_count = get_years(pif, 'A', 2000, 2001, pr_count, im_count)
    report("lineups", im_count, pr_count)
    return 0  # count


def count_pub(pif):
    recs = pif.dbh.fetch_publications()
    count = 0
    count += count_combo(
        config.IMG_DIR_CAT, [mbdata.IMG_SIZ_SMALL, ''], [x['base_id.id'].lower() for x in recs], ['', '_*'])
    count += count_combo(config.IMG_DIR_MAN, [mbdata.IMG_SIZ_SMALL], [x['base_id.id'].lower() for x in recs], [''])
    return count


def count_pack(pif):
    recs = pif.dbh.fetch_packs()
    count = 0
    count += count_combo_one_only(
        config.IMG_DIR_PROD_PACK,
        [mbdata.IMG_SIZ_TINY, mbdata.IMG_SIZ_SMALL, mbdata.IMG_SIZ_PETITE, mbdata.IMG_SIZ_MEDIUM],
        [x['base_id.id'].lower() for x in recs], [''])
    count += count_combo(config.IMG_DIR_PROD_PACK, [mbdata.IMG_SIZ_LARGE, mbdata.IMG_SIZ_HUGE], [x['base_id.id'].lower()
                         for x in recs], [''])
    count += count_combo(config.IMG_DIR_MAN, [mbdata.IMG_SIZ_SMALL], [x['base_id.id'].lower() for x in recs], [''])
    return count


def count_man(pif):
    recs = pif.dbh.fetch_casting_list()
    count = 0
    count += count_combo(config.IMG_DIR_MAN, [mbdata.IMG_SIZ_SMALL, mbdata.IMG_SIZ_MEDIUM, mbdata.IMG_SIZ_LARGE, 'z'],
                         [x['base_id.id'].lower() for x in recs], [''])
    count += count_combo(
        config.IMG_DIR_ADD, ['a', 'b', 'e', 'i', 'p', 'r'], [x['base_id.id'].lower() for x in recs], [''])
    count += count_combo(config.IMG_DIR_MAN_ICON, ['i'], [x['base_id.id'].lower() for x in recs], [''])
    return count


def count_var(pif):
    varrecs = pif.dbh.fetch_variations_bare()
    recs = []
    for var in varrecs:
        var_id = var['variation.var']
        if var['variation.picture_id']:
            var_id = var['variation.picture_id']
        recs.append('{}-{}'.format(var['variation.mod_id'].lower(), var_id.lower()))
    count = 0
    count += count_combo(config.IMG_DIR_MAN + '/var', [mbdata.IMG_SIZ_SMALL, mbdata.IMG_SIZ_MEDIUM], recs, [''])
    return count


def count_box(pif):
    pr_count, im_count = multip.count_boxes(pif)
    report("box", im_count, pr_count)
    return im_count


def count_from_file(fpath, tag, fld, pdir):
    pr_count = im_count = 0
    for ln in open(fpath).readlines():
        lns = ln.strip().split('|')
        if lns and lns[0] == tag:
            pr_count += 1
            if os.path.exists('{}/{}.jpg'.format(pdir, lns[fld])):
                im_count += 1
    report(fpath, im_count, pr_count)
    return im_count


@basics.command_line
def main(pif):
    pif = basics.get_page_info('editor')

    count = 0
    count += count_from_file('src/coll43.dat', 'm', 2, config.IMG_DIR_COLL_43)
    count += count_from_file('src/coll72.dat', 'm', 2, config.IMG_DIR_COLL_43)
    count += count_from_file('src/coll18.dat', 'm', 2, config.IMG_DIR_COLL_43)
    count += count_box(pif)
    count += count_directory(config.IMG_DIR_PROD_SERIES)
    count += count_directory(config.IMG_DIR_ACC)
    count += count_directory(config.IMG_DIR_BLISTER)
    count += count_directory(config.IMG_DIR_PROD_CODE_2)
    count += count_directory(config.IMG_DIR_PROD_COLL_64)
    count += count_html(config.IMG_DIR_ADS + '/index.php')
    count += count_html(config.IMG_DIR_ERRORS + '/index.html')
    count += count_lineups(pif)
    count += count_man(pif)
    count += count_var(pif)
    count += count_pack(pif)
    count += count_pub(pif)

    print()
    report('total', count)


if __name__ == '__main__':  # pragma: no cover
    main()
