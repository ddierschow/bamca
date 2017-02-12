#!/usr/local/bin/python

import glob, os, re, sys, urllib2
import binascii, os, stat, sys

import basics
import config
import useful

errors = []


# ----------------------------------------------------------------------------
# web_read

WEB_RETURN_SUCCESS = 'success'
WEB_RETURN_CONTENTS = 'contents'
WEB_RETURN_CODE = 'code'
WEB_RETURN_EXCEPTION_TYPE = 'exctype'
WEB_RETURN_EXCEPTION_VALUE = 'excvalue'


def web_read(url, noread=False, quiet=False, log=None):
    '''Read and return something from a url.  Package it up nicely.
    Take care of as much crap as possible.'''

    wp = lstatus = ''
    retval = {
        WEB_RETURN_CONTENTS: '',
        WEB_RETURN_CODE: None,
        WEB_RETURN_SUCCESS: False,
        WEB_RETURN_EXCEPTION_TYPE: None,
        WEB_RETURN_EXCEPTION_VALUE: None,
    }

    #if not quiet:
        #Info('web_read: ' + url, log=log)

    try:
        wp = urllib2.urlopen(url)
        retval[WEB_RETURN_CODE] = str(wp.code)
    except urllib2.HTTPError as (e):  # we expect these
        retval[WEB_RETURN_CODE] = 'H' + str(e.code)
        #Error("Reading %s failed with HTTPError:" % url, str(e), log=log)
        retval[WEB_RETURN_EXCEPTION_TYPE] = sys.exc_info()[0]
        retval[WEB_RETURN_EXCEPTION_VALUE] = sys.exc_info()[1]
        return retval
    except urllib2.URLError as (e):  # we expect these
        retval[WEB_RETURN_CODE] = 'U' + str(e.reason[0])
        #Error("Reading %s failed with URLError:" % url, str(e), log=log)
        retval[WEB_RETURN_EXCEPTION_TYPE] = sys.exc_info()[0]
        retval[WEB_RETURN_EXCEPTION_VALUE] = sys.exc_info()[1]
        return retval
    except:  # we don't expect these
        #Error("Reading %s encountered unexpected error:" % url, str(sys.exc_info()[0]), log=log)
        retval[WEB_RETURN_EXCEPTION_TYPE] = sys.exc_info()[0]
        retval[WEB_RETURN_EXCEPTION_VALUE] = sys.exc_info()[1]
        raise

    #if noread:  # check only, don't actually read
        #return retval

#    for hdr in wp.headers.headers:
#        if hdr.lower().startswith('content-length:'):
#            Info(hdr.strip())
    retval[WEB_RETURN_CONTENTS] = ''
    while 1:
        try:
            wread = wp.read()
        except httplib.IncompleteRead, e:
            #Error("Reading encountered Incomplete Read error. Retrying.")
            wp = urllib2.urlopen(url)
            retval[WEB_RETURN_CONTENTS] = ''
            continue
        except:
            #Error("Reading %s encountered unexpected error:" % url, str(sys.exc_info()[0]), log=log)
            retval[WEB_RETURN_EXCEPTION_TYPE] = sys.exc_info()[0]
            retval[WEB_RETURN_EXCEPTION_VALUE] = sys.exc_info()[1]
            raise
        if not wread:
            break
        retval[WEB_RETURN_CONTENTS] += wread
    retval[WEB_RETURN_SUCCESS] = True
    return retval


def fix_files(page_id):
    dn = useful.relpath('.', config.LIB_MAN_DIR, page_id[7:].lower())
    os.system('sudo chown bamca:www %s' % dn)
    os.system('sudo chmod 775 %s' % dn)
    os.system('sudo chown bamca:www %s/*.*' % dn)
    os.system('sudo chmod 664 %s/*.*' % dn)


def grab_page(url):
    print 'read', url
    retval = web_read(url)
    return retval[WEB_RETURN_CONTENTS]


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
            print sfn, 'already exists'
        else:
            img = grab_page(ll['pth'] + '/' + url)
            save(ll, sfn, img)


def save(ll, sfn, img):
    print 'save', sfn
    open(sfn, 'w').write(img)


mbxf_img_re = re.compile('''<IMG src='(?P<u>[^']*)' width='200'>''')
def mbx_forum(ll):
    pag = grab_page(ll['link_line.url'])
    grab_list(ll, mbxf_img_re.findall(pag))


def mcch(ll):
    print ll['link_line.url'], "- ignored"


mbdb_sub_re = re.compile('''<a href="(?P<u>showmodel.php?[^"]*)"''')
mbdb_img_re = re.compile('''<img src="(?P<u>[^"]*)">''')
def mbdb(ll):
    pag = grab_page(ll['link_line.url'])
    for subpg in mbdb_sub_re.findall(pag):
        imgpg = grab_page(ll['pth'] + '/' + subpg)
        grab_list(ll, mbdb_img_re.findall(imgpg))


cf_img_re = re.compile('''<A HREF="(?P<u>[^"]*)" target="_blank">''')
def cf(ll):
    pag = grab_page(ll['link_line.url'])
    grab_list(ll, cf_img_re.findall(pag))


mbdan_img_re = re.compile('''<IMG SRC="(?P<u>[^"]*)"''', re.M | re.I)
def mbdan(ll):
    pag = grab_page(ll['link_line.url'])
    fl = mbdan_img_re.findall(pag)
    fl = filter(lambda x: x != '../hr.gif', fl)
    grab_list(ll, fl)


mbxu_sub_re = re.compile('''<a href="(?P<u>Ver_Detail_and_Var_Listing.php\?model=[^"]*)">''')
mbxu_img_re = re.compile('''<img src=(?P<u>[^ "]*) />''')
def mbxu(ll):
    pag = grab_page(ll['link_line.url'])
    for subpg in mbxu_sub_re.findall(pag):
        imgpg = grab_page(ll['pth'] + '/' + subpg)
        grab_list(ll, mbxu_img_re.findall(imgpg))


areh_sub_re = re.compile('''<a href="(?P<u>[^"]*)" title="[^"]*" target="DATA"> <img src="[^"]*"></a>&nbsp;&nbsp;''')
areh_img_re = re.compile('''<img src="(?P<u>[^"]*)">''')
def areh(ll):
    pag = grab_page(ll['link_line.url'])
    for subpg in areh_sub_re.findall(pag):
        imgpg = grab_page(ll['pth'] + '/' + subpg)
        grab_list(ll, areh_img_re.findall(imgpg))

psdc_img_re = re.compile('''<a href="(?P<u>[^"]*)">''')
def psdc(ll):
    pag = grab_page(ll['link_line.url'])
    fl = psdc_img_re.findall(pag)
    fl = filter(lambda x: x != 'Notation.jpg' and not x.endswith('htm'), fl)
    grab_list(ll, fl)

def mbwiki(ll):
    print ll['link_line.url'], "- ignored"

def toyvan(ll):
    print ll['link_line.url'], "- ignored"

def mcf(ll):
    print ll['link_line.url'], "- ignored"


def run_line(ll):
    pth = ll['link_line.url']
    ll['pth'] = pth[:pth.rfind('/')]
    if ll['link_line.associated_link'] == 0:
        print "Huh?"
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
        print ll['link_line.url'], "- ignored"
    fix_files(ll['link_line.page_id'])
    print


def clean_dir(page_id):
    ln = useful.relpath('.', config.LIB_DIR, '0files')
    dn = useful.relpath('.', config.LIB_MAN_DIR, page_id.lower())
    print "attempting to clean", page_id
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
	print
	print 'Errors found...'
	for err in errors:
	    print err[0]['link_line.page_id'], err[1]


# from dirjoin

#!/usr/local/bin/python

import copy, filecmp, glob, os, sys


#num_rm = 0


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
	#thisdict[f.lower()] = thisinfo
	thisdict[f] = thisinfo
	#destinfo = destdict.get(f.lower(), None)
	destinfo = destdict.get(f, None)
	if not destinfo:
	    pass
	elif not os.path.exists(destdir + '/' + f):
	    pass
	elif not os.path.exists(thisdir + '/' + f):
	    pass
	elif thisinfo[1:] == destinfo[1:]:
	    if os.path.realpath(thisdir + '/' + f) == os.path.realpath(destdir + '/' + f):
		print '*** same file' # not gunna do it!  wouldn't be prudent!
	    else:
		try:
		    if filecmp.cmp(thisdir + '/' + f, destdir + '/' + f):
			#num_rm = num_rm + 1
			os.remove(thisdir + '/' + f)
			print ' ', thisdir + '/' + f
			#del thisdict[f.lower()]
			del thisdict[f]
		    else:
			print '~', thisdir + '/' + f
		except:
		    print '*** filecmp died'
	else:
	    print "   diff:", f
	    print "      ", thisinfo
	    print "      ", destinfo

    fl = os.listdir(thisdir)
    if not fl:
	try:
	    os.rmdir(thisdir)
	except: # shrug
	    pass
    return thisdict


def do_top_dir(destdir, srcdir):
    print "joining", destdir, srcdir
    if os.path.exists(destdir) and os.path.exists(srcdir):
	destdict = copy.deepcopy({})
	destdict = do_dir(destdir, None, destdict)
	do_dir(srcdir, destdir, destdict)


def crc_dir(destdir, subdirs=None):
    # recurse is cheap
    same = diff = add = gone = unkn = 0

    print "+",destdir,
    fl = os.listdir(destdir)
    print "(%d)" % len(fl)
    files = dict()
    fullfiles = dict()
    for f in fl:
	full = os.path.join(destdir, f)
	try:
	    st = os.lstat(full)
	except:
	    continue
	sig = (st.st_mtime, st.st_size)
	if stat.S_ISLNK(st.st_mode):
	    continue
	elif stat.S_ISDIR(st.st_mode):
	    if subdirs != None:
		subdirs.append(f)
	    continue
	elif f[0] == '.':
	    continue
	print " ",f,
	try:
	    info = sig + file_crc(full)
	except KeyboardInterrupt:
	    raise
	except:
	    print "*** Can't CRC", full
	    continue
	add += 1
	print "+"
	print os.path.join(destdir, f),"added"
	files[f] = info
	fullfiles[os.path.join(destdir, f)] = info
    return files


def file_crc(fn):
    #print ".",fn,
    f = open(fn, 'rb')
    crc = 0
    while 1:
	contents = f.read(16777216)
	#print ".",
	if contents:
	    crc = binascii.crc32(contents, crc)
	else:
	    break
    #print
    return (crc,)


if __name__ == '__main__':
    main(options='a')
