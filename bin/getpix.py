#!/usr/local/bin/python

from sprint import sprint as print
import binascii
import copy
import filecmp
from io import open
import os
import re
import requests
import stat

import basics
import config
import useful

errors = []


# ----------------------------------------------------------------------------


def fix_files(page_id):
    dn = useful.relpath('.', config.LIB_MAN_DIR, page_id[7:].lower())
    os.system('sudo chown bamca:www %s' % dn)
    os.system('sudo chmod 775 %s' % dn)
    os.system('sudo chown bamca:www %s/*.*' % dn)
    os.system('sudo chmod 664 %s/*.*' % dn)


def grab_page(url):
    print('read', url)
    retval = requests.get(url)
    return retval.text


def grab_list(ll, fl):
    for url in fl:
        fn = url[url.rfind('/') + 1:]
        libdir = useful.relpath('.', config.LIB_MAN_DIR, ll['link_line.page_id'][7:].lower())
        if not os.path.exists(libdir):
            errors.append((ll, url))
        sfn = os.path.join(libdir, fn)
        dot = sfn.rfind('.')
        sfn = sfn[:dot] + sfn[dot:].lower()
        if os.path.exists(sfn):
            print(sfn, 'already exists')
        else:
            img = grab_page(ll['pth'] + '/' + url)
            save(ll, sfn, img)


def save(ll, sfn, img):
    print('save', sfn)
    open(sfn, 'w').write(img)


def mbx_forum(ll):
    mbxf_img_re = re.compile(r'''<IMG src='(?P<u>[^']*)' width='200'>''')
    pag = grab_page(ll['link_line.url'])
    grab_list(ll, mbxf_img_re.findall(pag))


def mcch(ll):
    print(ll['link_line.url'], "- ignored")


def mbdb(ll):
    mbdb_sub_re = re.compile(r'''<a href="(?P<u>showmodel.php?[^"]*)"''')
    mbdb_img_re = re.compile(r'''<img src="(?P<u>[^"]*)">''')
    pag = grab_page(ll['link_line.url'])
    for subpg in mbdb_sub_re.findall(pag):
        imgpg = grab_page(ll['pth'] + '/' + subpg)
        grab_list(ll, mbdb_img_re.findall(imgpg))


def cf(ll):
    cf_img_re = re.compile(r'''<A HREF="(?P<u>[^"]*)" target="_blank">''')
    pag = grab_page(ll['link_line.url'])
    grab_list(ll, cf_img_re.findall(pag))


def mbdan(ll):
    mbdan_img_re = re.compile(r'''<IMG SRC="(?P<u>[^"]*)"''', re.M | re.I)
    pag = grab_page(ll['link_line.url'])
    fl = mbdan_img_re.findall(pag)
    fl = filter(lambda x: x != '../hr.gif', fl)
    grab_list(ll, fl)


def mbxu(ll):
    mbxu_sub_re = re.compile(r'''<a href="(?P<u>Ver_Detail_and_Var_Listing.php\?model=[^"]*)">''')
    mbxu_img_re = re.compile(r'''<img src=(?P<u>[^ "]*) />''')
    pag = grab_page(ll['link_line.url'])
    for subpg in mbxu_sub_re.findall(pag):
        imgpg = grab_page(ll['pth'] + '/' + subpg)
        grab_list(ll, mbxu_img_re.findall(imgpg))


def areh(ll):
    areh_sub_re = re.compile(
        r'''<a href="(?P<u>[^"]*)" title="[^"]*" target="DATA"> <img src="[^"]*"></a>&nbsp;&nbsp;''')
    areh_img_re = re.compile(r'''<img src="(?P<u>[^"]*)">''')
    pag = grab_page(ll['link_line.url'])
    for subpg in areh_sub_re.findall(pag):
        imgpg = grab_page(ll['pth'] + '/' + subpg)
        grab_list(ll, areh_img_re.findall(imgpg))


def psdc(ll):
    psdc_img_re = re.compile(r'''<a href="(?P<u>[^"]*)">''')
    pag = grab_page(ll['link_line.url'])
    fl = psdc_img_re.findall(pag)
    fl = filter(lambda x: x != 'Notation.jpg' and not x.endswith('htm'), fl)
    grab_list(ll, fl)


def mbwiki(ll):
    print(ll['link_line.url'], "- ignored")


def toyvan(ll):
    print(ll['link_line.url'], "- ignored")


def mcf(ll):
    print(ll['link_line.url'], "- ignored")


def run_line(ll):
    pth = ll['link_line.url']
    ll['pth'] = pth[:pth.rfind('/')]
    if ll['link_line.associated_link'] == 0:
        print("Huh?")
    elif ll['link_line.associated_link'] == 1:
        mcf(ll)
    elif ll['link_line.associated_link'] == 2:
        pass  # mbxf docs
    elif ll['link_line.associated_link'] == 3:
        pass  # comparisons
    elif ll['link_line.associated_link'] == 4:
        mbwiki(ll)
    elif ll['link_line.associated_link'] == 5:
        toyvan(ll)
    elif ll['link_line.associated_link'] == 6:
        psdc(ll)
    elif ll['link_line.associated_link'] == 7:
        areh(ll)
    elif ll['link_line.associated_link'] == 8:
        mbdan(ll)
    elif ll['link_line.associated_link'] == 9:
        mbx_forum(ll)
    elif ll['link_line.associated_link'] == 10:
        cf(ll)
    elif ll['link_line.associated_link'] == 11:
        pass  # toy brokers
    elif ll['link_line.associated_link'] == 12:
        pass  # diecast plus
    elif ll['link_line.associated_link'] == 13:
        mcch(ll)
    elif ll['link_line.associated_link'] == 14:
        mbdb(ll)
    elif ll['link_line.associated_link'] == 15:
        mbxu(ll)
    else:
        print(ll['link_line.url'], "- ignored")
    fix_files(ll['link_line.page_id'])
    print()


def clean_dir(page_id):
    ln = useful.relpath('.', config.LIB_DIR, '0files')
    dn = useful.relpath('.', config.LIB_MAN_DIR, page_id.lower())
    print("attempting to clean", page_id)
    do_top_dir(ln, dn)
    # Given this directory, clean it of things we know we don't want.


@basics.command_line
def main(pif):
    where = ' and '.join(['associated_link=%s' % x for x in pif.switch['a']])
    if pif.filelist:
        for arg in pif.filelist:
            for ll in pif.dbh.fetch_link_lines(page_id='single.' + arg, section='single', where=where):
                run_line(ll)
            clean_dir(arg)
    else:
        for ll in pif.dbh.fetch_link_lines(section='single', where=where):
            run_line(ll)

    if errors:
        print()
        print('Errors found...')
        for err in errors:
            print(err[0]['link_line.page_id'], err[1])


# from dirjoin

# num_rm = 0


def list_dirs(thisdir):
    fl = os.listdir(thisdir)
    subdirs = []
    for f in fl:
        full = thisdir + '/' + f
        if os.path.isdir(full):
            subdirs.append(f)
    subdirs.sort()
    return subdirs


def do_dir(thisdir, destdir, destdict):
    subdirs = []
    saved = crc_dir(thisdir, subdirs=subdirs)

    thisdict = {}
    for f in sorted(saved.keys()):
        thisinfo = saved[f]
        # thisdict[f.lower()] = thisinfo
        thisdict[f] = thisinfo
        # destinfo = destdict.get(f.lower(), None)
        destinfo = destdict.get(f, None)
        if not destinfo:
            pass
        elif not os.path.exists(destdir + '/' + f):
            pass
        elif not os.path.exists(thisdir + '/' + f):
            pass
        elif thisinfo[1:] == destinfo[1:]:
            if os.path.realpath(thisdir + '/' + f) == os.path.realpath(destdir + '/' + f):
                print('*** same file')  # not gunna do it!  wouldn't be prudent!
            else:
                try:
                    if filecmp.cmp(thisdir + '/' + f, destdir + '/' + f):
                        # num_rm = num_rm + 1
                        os.remove(thisdir + '/' + f)
                        print(' ', thisdir + '/' + f)
                        # del thisdict[f.lower()]
                        del thisdict[f]
                    else:
                        print('~', thisdir + '/' + f)
                except Exception:
                    print('*** filecmp died')
        else:
            print("   diff:", f)
            print("      ", thisinfo)
            print("      ", destinfo)

    fl = os.listdir(thisdir)
    if not fl:
        try:
            os.rmdir(thisdir)
        except Exception:  # shrug
            pass
    return thisdict


def do_top_dir(destdir, srcdir):
    print("joining", destdir, srcdir)
    if os.path.exists(destdir) and os.path.exists(srcdir):
        destdict = copy.deepcopy({})
        destdict = do_dir(destdir, None, destdict)
        do_dir(srcdir, destdir, destdict)


def crc_dir(destdir, subdirs=None):
    # recurse is cheap
    # same = diff = add = gone = unkn = 0
    add = 0

    print("+", destdir, end='')
    fl = os.listdir(destdir)
    print("(%d)" % len(fl))
    files = dict()
    fullfiles = dict()
    for f in fl:
        full = os.path.join(destdir, f)
        try:
            st = os.lstat(full)
        except Exception:
            continue
        sig = (st.st_mtime, st.st_size)
        if stat.S_ISLNK(st.st_mode):
            continue
        elif stat.S_ISDIR(st.st_mode):
            if subdirs is not None:
                subdirs.append(f)
            continue
        elif f[0] == '.':
            continue
        print(" ", f, end='')
        try:
            info = sig + file_crc(full)
        except KeyboardInterrupt:
            raise
        except Exception:
            print("*** Can't CRC", full)
            continue
        add += 1
        print("+")
        print(os.path.join(destdir, f), "added")
        files[f] = info
        fullfiles[os.path.join(destdir, f)] = info
    return files


def file_crc(fn):
    # print(".", fn,)
    f = open(fn, 'rb')
    crc = 0
    while 1:
        contents = f.read(16777216)
        # print(".",)
        if contents:
            crc = binascii.crc32(contents, crc)
        else:
            break
    # print()
    return (crc,)


if __name__ == '__main__':
    main(options='a')
