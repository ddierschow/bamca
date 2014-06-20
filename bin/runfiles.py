import glob, os, re, sys, time, urllib2

# This runs on Windows and uses Word to convert files.
# There is a macro that has to be installed in Word for this to work.

inloc = 'http://www.mbxforum.com/11-Catalogs/02-MB75/MB75-Documents'
tmploc = 'tmp'
wordloc = 'C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office'
startword = {
    'rtf' : 'word.lnk /mrtfconv',
    'html' : 'word.lnk /mhtmlconv',
}
startvcp = '"c:\\Program Files (x86)\\SecureCRT\\vcp"'
outloc = 'bamca@xocolatl.com:www/htdocs/src/mbxf'

error_list = []

def Fetch(url, with_continue=True):
    fn = os.path.basename(url)
    #url = urllib.quote(url, ':/')
    img = ''
    finished_len = 0
    img = ''
    tries = 32
    retry = 0
    content_len = None
    while retry < tries:
        retry += 1
        try:
            if with_continue:
                url_req = urllib2.Request(url, headers={'Range' : 'bytes=%d-' % finished_len})
                url_file = urllib2.urlopen(url_req, None, 90)
            else:
                url_file = urllib2.urlopen(url, None, 90)
                img = ''
            if content_len == None and 'content-length' in url_file.info():
                content_len = int(url_file.info()['content-length'])
            if with_continue:
                pass # print "fn %s len %s try %s range %s-" % (fn, content_len, retry, finished_len)
            img_add = ''
            while 1:
                buf = url_file.read()
                if not buf:
                    break
                img_add += buf
            #print "adding to %s current %s new %s" % (fn, len(img), len(img_add)),
            img += img_add
            finished_len = len(img)
            #print "=", finished_len
            if not content_len or (finished_len >= content_len):
                break
            else:
                #Log('read truncated (was %d not %d)' % (len(img), content_len))
                print '*** read truncated on %s (was %d not %d) try %d' % (fn, len(img), content_len, retry)
        except KeyboardInterrupt:
            #Log('read interrupted (%s)' % url)
            raise
        except urllib2.HTTPError:
            img = ''
            print '*** exception in GetImg open :', url, "error", str(sys.exc_info()[0])
            #Log('read failed (%s)' % url)
            break
        except:
            img = ''
            print '*** exception in GetImg open :', url, "error", str(sys.exc_info()[0])
            #Log('read failed (%s)' % url)
        time.sleep(2)
    if content_len and (len(img) != content_len):
        print '*** read incomplete on %s (was %s not %s)' % (fn, len(img), content_len)
	error_list.append(url)
    #print "  size expected %10s - actual %10s" % (content_len, len(img))
    return img


web_index_re    = re.compile('<a href="(?P<u>[^"]*)">', re.I)
def WebReadDirectory(dir_path):
    retval = urllib2.urlopen(dir_path).read()
    files = filter(lambda x: not x.startswith('?') and not x.find('/') >= 0, web_index_re.findall(retval))
    return files


def GetFiles(url, file_list):
    for fn in file_list:
	print fn
	open(tmploc + '/' + fn, 'wb').write(Fetch(url + '/' + fn))


def Process(filetype):
    if os.path.exists(tmploc + '/done.txt'):
	os.unlink(tmploc + '/done.txt')
    #map(os.unlink, glob.glob(tmploc + '/*.' + filetype))
    os.system(startword[filetype])
    while not os.path.exists(tmploc + '/done.txt'):
	time.sleep(3)


def Main(args):
    if not args:
	print "Commands are: get", ' '.join(startword.keys()), "clean put reset"
    else:
	for arg in args:
	    if arg == 'get':
		map(os.unlink, glob.glob(tmploc + '/*.doc'))
		fl = WebReadDirectory(inloc)
		GetFiles(inloc, filter(lambda x: x.endswith('.doc'), fl))
	    elif arg in startword:
		Process(arg)
	    elif arg == 'reset':
		map(lambda x: os.unlink(x), glob.glob(tmploc + '/*.doc'))
		map(lambda x: os.unlink(x), glob.glob(tmploc + '/*.rtf'))
		map(lambda x: os.unlink(x), glob.glob(tmploc + '/*.htm'))
	    elif arg == 'clean':
		docfiles = map(lambda x: x[:-4], glob.glob(tmploc + '/*.doc'))
		rtffiles = map(lambda x: x[:-4], glob.glob(tmploc + '/*.rtf'))
		htmfiles = map(lambda x: x[:-4], glob.glob(tmploc + '/*.htm'))
		for fn in docfiles:
		    if fn in htmfiles or fn in rtffiles:
			os.unlink(fn + '.doc')
		dirs = filter(lambda x: os.path.isdir(x), glob.glob(tmploc + '/*'))
		for dir in dirs:
		    for fn in glob.glob(dir + '/*'):
			print '   deleting', fn
			os.unlink(fn)
		    print ' removing', dir
		    os.rmdir(dir)
	    elif arg == 'put':
		os.system(startvcp + ' ' + tmploc + '\\*.rtf ' + tmploc + '\\*.htm ' + outloc)
    if error_list:
	print
	print 'errors:'
	print "\n".join(error_list)


if __name__ == '__main__': # pragma: no cover
    Main(sys.argv[1:])
