import datetime, fnmatch, glob, os, re, sys, time, urllib2

# todo:
#   add a start date

inloc = 'http://www.mbxforum.com/11-Catalogs/02-MB75/MB75-Documents'
tmploc = 'tmp'
startword = {
    'rtf': 'word.lnk /mrtfconv',
    'html': 'word.lnk /mhtmlconv',
}
startscp = '"c:\\Program Files\\pscp"'
outloc = 'bamca@xocolatl.com:www/htdocs/src/mbxf'

error_list = []

def fetch(url, with_continue=True):
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
                url_req = urllib2.Request(url, headers={'Range': 'bytes=%d-' % finished_len})
                url_file = urllib2.urlopen(url_req, None, 90)
            else:
                url_file = urllib2.urlopen(url, None, 90)
                img = ''
            if content_len is None and 'content-length' in url_file.info():
                content_len = int(url_file.info()['content-length'])
            if with_continue:
                pass  # print "fn %s len %s try %s range %s-" % (fn, content_len, retry, finished_len)
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


web_index_re    = re.compile('<a href="(?P<u>[^"]*)">.*?<\/a>\s*(?P<d>....-..-..)', re.I)
def web_read_directory(dir_path, start_date=None, fn_patt=None):
    page_text = urllib2.urlopen(dir_path).read()
    bfiles = web_index_re.findall(page_text)
    if start_date:
        bfiles = filter(lambda x: datetime.datetime.strptime(x[1], '%Y-%m-%d') > start_date, bfiles)
    bfiles = filter(lambda x: not x.startswith('?') and not x.find('/') >= 0, [y[0] for y in bfiles])
    if fn_patt:
        print fn_patt
        bfiles = filter(lambda x: fnmatch.fnmatch(x, fn_patt), bfiles)
    return bfiles


def get_files(url, file_list):
    for fn in file_list:
        print fn
        open(tmploc + '/' + fn, 'wb').write(fetch(url + '/' + fn))


def process(filetype):
    if os.path.exists(tmploc + '/done.txt'):
        os.unlink(tmploc + '/done.txt')
    #map(os.unlink, glob.glob(tmploc + '/*.' + filetype))
    os.system(startword[filetype])
    while not os.path.exists(tmploc + '/done.txt'):
        time.sleep(3)


def main(args):
    start_date = None
    fn_patt = None
    if not args:
        print "Commands are: get list date= file=", ' '.join(startword.keys()), "clean put reset"
    else:
        for arg in args:
            if arg == 'get':
                if not os.path.exists(tmploc):
                    os.mkdir(tmp)
                map(os.unlink, glob.glob(tmploc + '/*.doc'))
                fl = web_read_directory(inloc, start_date, fn_patt)
                get_files(inloc, filter(lambda x: x.endswith('.doc'), fl))
            elif arg == 'list':
                fl = web_read_directory(inloc, start_date, fn_patt)
                print '\n'.join(fl)
            elif arg.startswith('date='):
                start_date = datetime.datetime.strptime(arg, 'date=%d-%b-%Y')
                print start_date
            elif arg.startswith('file='):
                fn_patt = arg[5:]
            elif arg in startword:
                process(arg)
            elif arg == 'reset':
                map(os.unlink, glob.glob(tmploc + '/*.doc'))
                map(os.unlink, glob.glob(tmploc + '/*.rtf'))
                map(os.unlink, glob.glob(tmploc + '/*.htm'))
            elif arg == 'clean':
                docfiles = [x[:-4] for x in glob.glob(tmploc + '/*.doc')]
                rtffiles = [x[:-4] for x in glob.glob(tmploc + '/*.rtf')]
                htmfiles = [x[:-4] for x in glob.glob(tmploc + '/*.htm')]
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
                os.system(startscp + ' ' + tmploc + '\\*.rtf ' + tmploc + '\\*.htm ' + outloc)
    if error_list:
        print
        print 'errors:'
        print "\n".join(error_list)


if __name__ == '__main__':  # pragma: no cover
    main(sys.argv[1:])
