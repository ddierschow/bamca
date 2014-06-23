#!/usr/local/bin/python

import glob, os, re, sys

import basics
import config

errors = []


#-----------------------------------------------------------------------------
# WebRead

WEB_RETURN_SUCCESS = 'success'
WEB_RETURN_CONTENTS = 'contents'
WEB_RETURN_CODE = 'code'
WEB_RETURN_EXCEPTION_TYPE = 'exctype'
WEB_RETURN_EXCEPTION_VALUE = 'excvalue'

def WebRead(url, noread=False, quiet=False, log=None):
    '''Read and return something from a url.  Package it up nicely.
    Take care of as much crap as possible.'''

    wp = lstatus = ''
    retval = {
	WEB_RETURN_CONTENTS : '',
	WEB_RETURN_CODE : None,
	WEB_RETURN_SUCCESS : False,
	WEB_RETURN_EXCEPTION_TYPE : None,
	WEB_RETURN_EXCEPTION_VALUE : None,
    }
#    if not quiet:
#	Info('WebRead: ' + url, log=log)
    try:
	wp = urllib2.urlopen(url)
	retval[WEB_RETURN_CODE] = str(wp.code)
    except urllib2.HTTPError as (e): # we expect these
	retval[WEB_RETURN_CODE] = 'H' + str(e.code)
#	Error("Reading %s failed with HTTPError:" % url, str(e), log=log)
	retval[WEB_RETURN_EXCEPTION_TYPE] = sys.exc_info()[0]
	retval[WEB_RETURN_EXCEPTION_VALUE] = sys.exc_info()[1]
	return retval
    except urllib2.URLError as (e): # we expect these
	retval[WEB_RETURN_CODE] = 'U' + str(e.reason[0])
#	Error("Reading %s failed with URLError:" % url, str(e), log=log)
	retval[WEB_RETURN_EXCEPTION_TYPE] = sys.exc_info()[0]
	retval[WEB_RETURN_EXCEPTION_VALUE] = sys.exc_info()[1]
	return retval
    except: # we don't expect these
#	Error("Reading %s encountered unexpected error:" % url, str(sys.exc_info()[0]), log=log)
	retval[WEB_RETURN_EXCEPTION_TYPE] = sys.exc_info()[0]
	retval[WEB_RETURN_EXCEPTION_VALUE] = sys.exc_info()[1]
	raise

#    if noread: # check only, don't actually read
#	return retval

    for hdr in wp.headers.headers:
	if hdr.lower().startswith('content-length:'):
	    Info(hdr.strip())
    retval[WEB_RETURN_CONTENTS] = ''
    while 1:
	try:
	    wread = wp.read()
	except httplib.IncompleteRead, e:
#	    Error("Reading encountered Incomplete Read error. Retrying.")
	    wp = urllib2.urlopen(url)
	    retval[WEB_RETURN_CONTENTS] = ''
	    continue
	except:
#	    Error("Reading %s encountered unexpected error:" % url, str(sys.exc_info()[0]), log=log)
	    retval[WEB_RETURN_EXCEPTION_TYPE] = sys.exc_info()[0]
	    retval[WEB_RETURN_EXCEPTION_VALUE] = sys.exc_info()[1]
	    raise
	if not wread:
	    break
	retval[WEB_RETURN_CONTENTS] += wread
    retval[WEB_RETURN_SUCCESS] = True
    return retval


def FixFiles(page_id):
    dir = os.path.join(config.libmandir, page_id[7:].lower())
    os.system('sudo chown bamca:www %s' % dir)
    os.system('sudo chmod 775 %s' % dir)
    os.system('sudo chown bamca:www %s/*.*' % dir)
    os.system('sudo chmod 664 %s/*.*' % dir)


def GrabPage(url):
    print 'read', url
    retval = WebRead(url)
    return retval[WEB_RETURN_CONTENTS]


def GrabList(ll, fl):
    for url in fl:
	fn = url[url.rfind('/') + 1:]
	libdir = os.path.join(config.libmandir, ll['link_line.page_id'][7:].lower())
	if not os.path.exists(libdir):
	    errors.append((ll, url))
	sfn = os.path.join(libdir, fn)
	dot = sfn.rfind('.')
	sfn = sfn[:dot] + sfn[dot:].lower()
	if os.path.exists(sfn):
	    print sfn, 'already exists'
	else:
	    img = GrabPage(ll['pth'] + '/' + url)
	    Save(ll, sfn, img)
	
def Save(ll, sfn, img):
    print 'save', sfn
    open(sfn, 'w').write(img)


mbxf_img_re = re.compile('''<IMG src='(?P<u>[^']*)' width='200'>''')
def MBXForum(ll):
    pag = GrabPage(ll['link_line.url'])
    GrabList(ll, mbxf_img_re.findall(pag))


def MCCH(ll):
    print ll['link_line.url'], "- ignored"


mbdb_sub_re = re.compile('''<a href="(?P<u>showmodel.php?[^"]*)"''')
mbdb_img_re = re.compile('''<img src="(?P<u>[^"]*)">''')
def MBDB(ll):
    pag = GrabPage(ll['link_line.url'])
    for subpg in mbdb_sub_re.findall(pag):
	imgpg = GrabPage(ll['pth'] + '/' + subpg)
	GrabList(ll, mbdb_img_re.findall(imgpg))


cf_img_re = re.compile('''<A HREF="(?P<u>[^"]*)" target="_blank">''')
def CF(ll):
    pag = GrabPage(ll['link_line.url'])
    GrabList(ll, cf_img_re.findall(pag))


mbdan_img_re = re.compile('''<IMG SRC="(?P<u>[^"]*)"''', re.M | re.I)
def MBDan(ll):
    pag = GrabPage(ll['link_line.url'])
    fl = mbdan_img_re.findall(pag)
    fl = filter(lambda x: x != '../hr.gif', fl)
    GrabList(ll, fl)


areh_sub_re = re.compile('''<a href="(?P<u>[^"]*)" title="[^"]*" target="DATA"> <img src="[^"]*"></a>&nbsp;&nbsp;''')
areh_img_re = re.compile('''<img src="(?P<u>[^"]*)">''')
def Areh(ll):
    pag = GrabPage(ll['link_line.url'])
    for subpg in areh_sub_re.findall(pag):
	imgpg = GrabPage(ll['pth'] + '/' + subpg)
	GrabList(ll, areh_img_re.findall(imgpg))

psdc_img_re = re.compile('''<a href="(?P<u>[^"]*)">''')
def PSDC(ll):
    pag = GrabPage(ll['link_line.url'])
    fl = psdc_img_re.findall(pag)
    fl = filter(lambda x: x != 'Notation.jpg' and not x.endswith('htm'), fl)
    GrabList(ll, fl)

def MBWiki(ll):
    print ll['link_line.url'], "- ignored"

def ToyVan(ll):
    print ll['link_line.url'], "- ignored"

def MCF(ll):
    print ll['link_line.url'], "- ignored"


def RunLine(ll):
    pth = ll['link_line.url']
    ll['pth'] = pth[:pth.rfind('/')]
    if ll['link_line.associated_link'] == 0:
	print "Huh?"
    elif ll['link_line.associated_link'] == 1:
	MCF(ll)
    elif ll['link_line.associated_link'] == 2:
	pass # mbxf docs
    elif ll['link_line.associated_link'] == 3:
	pass # comparisons
    elif ll['link_line.associated_link'] == 4:
	MBWiki(ll)
    elif ll['link_line.associated_link'] == 5:
	ToyVan(ll)
    elif ll['link_line.associated_link'] == 6:
	PSDC(ll)
    elif ll['link_line.associated_link'] == 7:
	Areh(ll)
    elif ll['link_line.associated_link'] == 8:
	MBDan(ll)
    elif ll['link_line.associated_link'] == 9:
	MBXForum(ll)
    elif ll['link_line.associated_link'] == 10:
	CF(ll)
    elif ll['link_line.associated_link'] == 13:
	MCCH(ll)
    elif ll['link_line.associated_link'] == 17:
	MBDB(ll)
    elif ll['link_line.associated_link'] == 27:
	pass # diecast plus
    else:
	print ll['link_line.url'], "- ignored"
    FixFiles(ll['link_line.page_id'])
    print

if __name__ == '__main__':
    pif = basics.GetPageInfo('vars')

    if len(sys.argv) > 1:
	for arg in sys.argv[1:]:
	    for ll in pif.dbh.FetchLinkLines(page_id='single.' + arg, section='single'):
		RunLine(ll)
    else:
	for ll in pif.dbh.FetchLinkLines(section='single'):
	    RunLine(ll)

    print
    print 'Errors found...'
    for err in errors:
	print err[0]['link_line.page_id'], err[1]
