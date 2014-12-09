#!/usr/local/bin/python

import datetime, glob, os, re, stat, subprocess, sys, time, traceback, urllib, urllib2
import Image
import basics
import bfiles
import config
import imicon
import javascript
import mbdata
import useful

#os.environ['PATH'] += ':/usr/local/bin'


'''  API
images.action
images.export_file
images.get_dir
images.get_size
images.imawidget
images.import_file
images.pipe_chain
images.show_picture
images.upload_main
images.cycle
images.def_edit_app
images.def_edit_js
images.image_inputter
'''

# -- form markups

def_edit_js = javascript.def_edit_js
def_edit_app = javascript.def_edit_app

editformstart = '''
<form action="imawidget.cgi" name="myForm" onSubmit="return getValueFromApplet()">
'''

editformend = '''
  <input type="hidden" value="%(f)s" name="f">
  <input type="hidden" value="%(d)s" name="d">
  <input type="hidden" value="" name="q">
</form>
'''

# Globals 'cause I'm too friggin' lazy sometimes.
xts = 180
yts = 125

cycle = 0

image_content_type = {
    'bmp': 'Content-Type: image/bmp',
    'gif': 'Content-Type: image/gif',
    'ico': 'Content-Type: image/x-icon',
    'jpg': 'Content-Type: image/jpeg',
    'jpeg': 'Content-Type: image/jpeg',
    'png': 'Content-Type: image/png',
    'tif': 'Content-Type: image/tiff',
    'xbm': 'Content-Type: image/x-xbitmap',
    '': 'Content-Type: image/jpeg',
}

image_inputter = {
    'bmp': [['/usr/local/bin/bmptopnm']],
    'gif': [['/usr/local/bin/giftopnm']],
    'ico': [['/usr/local/bin/winicontoppm']],
    'jpg': [['/usr/local/bin/jpegtopnm']],
    'jpeg': [['/usr/local/bin/jpegtopnm']],
    'png': [['/usr/local/bin/pngtopnm']],
    'tif': [['/usr/local/bin/tifftopnm']],
    'xbm': [['/usr/local/bin/xbmtopbm']],
#    '': [['/usr/local/bin/jpegtopnm']],
}
itypes = ['bmp', 'gif', 'ico', 'jpg', 'jpeg', 'png', 'tif', 'xbm']

image_outputter = {
    'bmp': [['/usr/local/bin/ppmtobmp']],
    'gif': [['/usr/local/bin/pnmquant', '256'], ['/usr/local/bin/ppmtogif']],
    'ico': [['/usr/local/bin/ppmtowinicon']],
    'jpg': [['/usr/local/bin/pnmtojpeg']],
    'jpeg': [['/usr/local/bin/pnmtojpeg']],
    'png': [['/usr/local/bin/pnmtopng']],
    '': [['/usr/local/bin/pnmtojpeg']],
}
otypes = ['', 'bmp', 'gif', 'ico', 'jpg', 'png']


def import_file(fn):
    fn = fn[fn.rfind('/') + 1:]
    fex = fn[fn.rfind('.') + 1:]
    if '?' in fex:
        fex = fex[:fex.find('?')]
    return image_inputter[fex]


def export_file(nfn, ofn=''):
    nfn = nfn[nfn.rfind('/') + 1:]
    if '.' in nfn:
        fex = nfn[nfn.rfind('.') + 1:]
    else:
        ofn = ofn[ofn.rfind('/') + 1:]
        fex = ofn[ofn.rfind('.') + 1:]
    return image_outputter[fex]


# -- upload


def get_dir(tdir):
    fl = os.listdir(tdir)
    fl.sort()
    dl = list()  # directories
    gl = list()  # graphics
    ol = list()  # other files
    sl = list()  # dat files
    xl = list()  # executables

    for f in fl:
        root, ext = useful.root_ext(f)
        if os.path.exists(tdir + '/' + f):
            if f[-1] == '~' or f == '.crcs' or f[-4:] == '.pyc':
                continue
            perms = os.stat(tdir + '/' + f)[stat.ST_MODE]
            if stat.S_ISDIR(perms):
                dl.append(f)
            elif ext == 'dat':
                sl.append(f)
            elif ext in image_inputter:
                gl.append(f)
            elif stat.S_IMODE(perms) & stat.S_IXUSR:
                xl.append(f)
            else:
                ol.append(f)
    return dl, gl, ol, sl, xl


def filename(man, var='', ext='.jpg'):
    pth = os.path.join(config.LIB_MAN_DIR, man.lower())
    if var:
        fn = (man + '-' + var).lower()
    else:
        fn = man.lower()
    if os.path.exists(os.path.join(pth, fn + ext)):
        i = 1
        while os.path.exists(pth + '/' + fn + '-' + str(i) + ext):
            i = i + 1
        fn = fn + '-' + str(i)
    return pth, fn + ext


def upload_pic(pif, infile, pdir, fn, overwrite=False, desc=''):
    upload_file(pif, infile, pdir, fn, overwrite)
    show(pif, pdir, fn)


def upload_file(pif, infile, pdir, fn, overwrite=False, desc=''):
    fn = safe_save(pif, pdir, fn, infile, overwrite)
    if fn.endswith('.') or '.' not in fn:
        fn = fix_file_type(pif, pdir, fn)


def scrape_url_mod(pif, url, man, var, overwrite=False, desc=''):
    pdir = pif.form_str('d', os.path.join(config.LIB_MAN_DIR, man))
    fn = url[url.rfind('/') + 1:].lower()
    scrape_url_pic(pif, url, pdir, fn, overwrite, desc=desc)


scrape_re = re.compile(r'''<img src="(?P<img>[^"]*)"''', re.I)
def scrape_url_pic(pif, url, pdir, fn, overwrite=False, desc=''):
    print '<br>', url, ':', pdir, ':', fn, '<br>'
    try:
        up = urllib2.urlopen(url).read()
    except:
        pif.show_error()
        return
    url = url[:url.rfind('/') + 1]
    imgs = scrape_re.findall(up)
    sfn = ''
    for img in imgs:
        fn = img[img.rfind('/') + 1:]
        print img, pdir, fn, '<br>'
        if not img.startswith('http://'):
            img = url + '/' + img
        sfn = grab_url_file(pif, img, pdir, fn, overwrite)

        pif.render.pic_dir = pdir
        print '<center><h3>Added: ' + sfn + '</h3><p>'
        print '<img src="../%s/%s"></center>' % (pdir, sfn)
    #picker(pif, sfn)


def fix_file_type(pif, pdir, fn):
    types = [
        ('JPEG', 'jpg'),
        ('GIF', 'gif'),
        ('PC bitmap', 'bmp'),
        ('PNG', 'png'),
    ]
    if '.' in fn:
        root, ext = fn.rsplit('.', 1)
    else:
        root = fn
        ext = ''

    c = ["/usr/bin/file", "-b", pdir + '/' + fn]
    p = subprocess.Popen(c, stdout=subprocess.PIPE, stderr=None, close_fds=True)
    l = p.stdout.readlines()
    if not l:
        return fn
    l = l[0].strip()

    for typ in types:
        if l.startswith(typ[0]):
            ext = typ[1]

    nfn = root + '.' + ext
    if nfn == fn:
        return fn
    if os.path.exists(pdir + '/' + nfn):
        addon = 1
        while os.path.exists(pdir + '/' + root + '_' + str(addon) + '.' + ext):
            addon += 1
        root += '_' + str(addon)
    nfn = root + '.' + ext
    os.rename(pdir + '/' + fn, pdir + '/' + nfn)
    return nfn


def safe_save(pif, pdir, fn, contents, overwrite=False):
    if not os.path.exists(pdir):
        os.mkdir(pdir, 0775)
    if '.' in fn:
        root, ext = fn.rsplit('.', 1)
    else:
        root = fn
        ext = ''
    ext = ext.lower()
    root = useful.clean_name(root, '!@$%^&*()[]{}~`<>"+')
    fn = root + '.' + ext
    if os.path.exists(pdir + '/' + fn):
        if overwrite:
            #os.unlink(pdir + '/' + fn)
            useful.file_mover(pdir + '/' + fn, os.path.join(config.LIB_DIR, 'trash', fn), mv=True, inc=True, trash=True)
        else:
            addon = 1
            while os.path.exists(pdir + '/' + root + '_' + str(addon) + '.' + ext):
                addon += 1
            root += '_' + str(addon)
    fn = root + '.' + ext
    open(pdir + '/' + fn, 'w').write(contents)
    log(pif, pdir + '/' + fn, pdir)
    return fn


def grab_url_mod(pif, url, man, var, overwrite=False, desc=''):
    pdir = pif.form_str('d', os.path.join(config.LIB_MAN_DIR, man))
    fn = url[url.rfind('/') + 1:].lower()
    grab_url_pic(pif, url, pdir, fn, var, overwrite, desc=desc)


def grab_url_pic(pif, url, pdir, fn, var=None, overwrite=False, track=False, desc=''):
    fn = grab_url_file(pif, url, pdir, fn, var, overwrite)
    #if var:
        #print '''<meta http-equiv="REFRESH" content="0;url=/cgi-bin/imawidget.cgi?d=%s&f=%s&cy=%d&v=%s">''' % (pdir, fn, 0, var)
    #else:
        #print '''<meta http-equiv="REFRESH" content="0;url=/cgi-bin/imawidget.cgi?d=%s&f=%s&cy=%d">''' % (pdir, fn, 0)
    pif.render.pic_dir = pdir
    picker(pif, fn)
    if track:
        pif.dbh.insert_activity(fn, pif.id, description=desc, image=pdir + '/' + fn)
    print '<hr>'
    show_editor(pif, pif.render.pic_dir, fn)


def grab_url_file(pif, url, pdir, fn, var=None, overwrite=False, desc=''):
    open(os.path.join(config.LOG_ROOT, 'upload.log'), 'a').write(datetime.datetime.now().strftime('%Y%m%d.%H%M%S') + ' %s %s\n' % (url, pdir))
    try:
        up = urllib2.urlopen(url).read()
    except:
        pif.show_error()
        return "Error encountered!  File not uploaded."
    if not fn:
        fn = url[url.rfind('/') + 1:].lower()
    elif '.' not in fn:
        fn += url[url.rfind('.'):].lower()
    fn = safe_save(pif, pdir, fn, up, overwrite)
    return fn


def upload_mod(pif, infile, man, var, overwrite=False, desc=''):
    pdir, fn = filename(man, var)
    fn = safe_save(pif, pdir, fn, infile, overwrite)
    show(pif, pdir, fn)


def select_from_library(pif, man, var, desc=''):
    nfn = man.lower()
    if var:
        nfn = nfn + '-' + var
    tdir = os.path.join(config.LIB_MAN_DIR, man.lower())
    grafs = True
    os.chdir(tdir)

    gl = filter(lambda f: not stat.S_ISDIR(os.stat(f)[stat.ST_MODE]) and useful.root_ext(f)[1] in image_inputter, os.listdir('.'))
    gl.sort()

    if gl:
        for f in gl:
            r, e = useful.root_ext(f)
            perms = os.stat(f)[stat.ST_MODE]
            if (perms & 4) == 0:
                print '%s<br>' % f
            else:
                #print '<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s&newname=%s.%s&v=%s">' % (tdir, f, nfn, e, var)
                print '<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s&v=%s&c=%s">' % (tdir, f, var, urllib.quote_plus(desc))
                print '<img src="../%s" border=0>%s</a><br>' % (tdir + '/' + f, f)
        print '<br><hr>'


def show(pif, pdir, fn):
    pif.render.pic_dir = pdir
    show_picture(pif, fn)
    #print '<center><h3>' + fn + '</h3><p>'
    #print '<img src="../%s/%s"></center>' % (pdir, fn)
    #picker(pif, fn)

# for things out of http space:
#print '<img src="/cgi-bin/image.cgi?d=%s&f=%s">' % (pif.render.pic_dir, fn)
def show_picture(pif, fn):
    picker(pif, fn)
    root, ext = useful.root_ext(fn.strip())
    pif.render.comment(root, ext)
    print '<table><tr><td></td><td>' + pif.render.format_image_art('hruler.gif') + '</td></tr>'
    print '<tr><td valign="top">' + pif.render.format_image_art('vruler.gif') + '</td><td valign="top">'
    #print '<a href="../' + pif.render.pic_dir + '/' + fn + '">' + pif.render.format_image_required([root], suffix=ext, also={"border":"0"}) + '</a>'
    print '<a href="/cgi-bin/image.cgi?d=%s&f=%s"><img src="/cgi-bin/image.cgi?d=%s&f=%s"></a>' % (pif.render.pic_dir, fn, pif.render.pic_dir, fn)
    print '</td></tr></table>'


def log(pif, fn, tdir):
    open(os.path.join(config.LOG_ROOT, "file.log"), "a").write('|'.join([fn, tdir, str(pif.id)]) + '\n')


def get_man(pif):
    #print 'get_man man', pif.form_str('man'), 'pic_dir', pif.render.pic_dir, '<br>'
    man = pif.form_str("man")
    if man:
        #print 'form', man, '<br>'
        return man
    pdir = pif.render.pic_dir
    if pdir.startswith('./'):
        pdir = pdir[2:]
    if pdir.endswith('/'):
        pdir = pdir[:-1]
    if pdir.startswith(config.LIB_DIR):
        #print 'lib', pdir[pdir.rfind('/') + 1:], '<br>'
        return pdir[pdir.rfind('/') + 1:]
    if pdir.startswith("pic/packs"):
        if pif.form_str('f'):
            if len(pif.form_str('f')) > 2 and pif.form_str('f')[1] == '_':
                #print 'pack1', pif.form_str('f')[2:-4], '<br>'
                return pif.form_str('f')[2:-4]
            else:
                #print 'pack2', pif.form_str('f')[:-4], '<br>'
                return pif.form_str('f')[:-4]
    if pdir.startswith("pic/cat"):
        if pif.form_str('f'):
            if len(pif.form_str('f')) > 2 and pif.form_str('f')[1] == '_':
                man = pif.form_str('f')[2:-4]
            else:
                man = pif.form_str('f')[:-4]
            if '_' in man:
                man = man[:man.find('_')]
            #print 'cat', man, '<br>'
            return man
    #print 'nope', '<br>'
    return ""

sel_cat = [
    ['unsorted', 'unsorted'],
    ['a',       'Accessories'],
    ['bigmx',   'BigMX'],
    ['blister', 'Blister'],
    ['cc',      'Carrying Case'],
    ['cat',     'Catalogs'],
    ['coll',    'Collectibles'],
    ['commando', 'Commando'],
    ['cy',      'Convoys'],
    ['copies',  'Copies'],
    ['disp',    'Displays'],
    ['e',       'Early'],
    ['game',    'Games'],
    ['g',       'Giftsets'],
    ['gw',      'Giftware'],
    ['gf',      'Graffic'],
    ['k',       'Kings'],
    ['moko',    'Moko'],
    ['mw',      'Motorways'],
    ['mult',    'Multiples'],
    ['o',       'Other'],
    ['packs',   'Packs'],
    ['ps',      'Play Sets'],
    ['prem',    'Premieres'],
    ['rt',      'Real Talkin'],
    ['rb',      'Roadblasters'],
    ['r',       'Roadway'],
    ['robotech', 'RoboTech'],
    ['sb',      'Sky Busters'],
    ['supergt', 'SuperGT'],
    ['tp',      'TwinPacks'],
    ['wr',      'White Rose'],
    ['zing',    'Zings'],
]

adds = 'abdeipr'
sel_pref = [
    ['', ''],
    ['t', 'thumbnail'],
    ['s', 'small'],
    ['c', 'compact'],
    ['m', 'medium'],
    ['l', 'large'],
    ['h', 'huge'],
    ['g', 'gigantic'],
    ['b', 'baseplate'],
    ['a', 'custom'],
    ['d', 'detail'],
    ['e', 'error'],
    ['i', 'interior'],
    ['p', 'prototype'],
    ['r', 'real'],
    ['z', 'comparison'],
]

sel_moveto = [
    ['',        ''],
    [config.IMG_DIR_MATTEL,     'mattel'],
    [config.IMG_DIR_MT_LAUREL,  'mtlaurel'],
    [config.IMG_DIR_TYCO,       'tyco'],
    [config.IMG_DIR_UNIV,       'univ'],
    [config.IMG_DIR_LSF,        'lsf'],
    [config.IMG_DIR_LRW,        'lrw'],
    [config.IMG_DIR_LESNEY,     'lesney'],
    [config.IMG_DIR_ACC,        'acc'],
    [config.IMG_DIR_ADS,        'ads'],
    [config.IMG_DIR_BLISTER,    'blister'],
    [config.IMG_DIR_BOX,        'box'],
    [config.IMG_DIR_COLL_43,    'mcoll'],
    [config.IMG_DIR_ERRORS,     'errors'],
    [config.IMG_DIR_KING,       'king'],
    [config.IMG_DIR_PACK,       'packs'],
    [config.IMG_DIR_COLL_64,    'prem'],
    [config.IMG_DIR_SERIES,     'series'],
    [config.IMG_DIR_SKY,        'sky'],
]

def picker(pif, fn):
    global cycle
    cycle = pif.form_int('cy')
    root, ext = useful.root_ext(fn.strip())
    print '<a href="?d=%s">%s</a> / ' % (pif.render.pic_dir, pif.render.pic_dir)
    print '<a href="/%s/%s">%s</a>' % (pif.render.pic_dir, fn, fn)
    szname = ''
    if os.path.exists(pif.render.pic_dir + '/' + fn):
        x, y = get_size(pif.render.pic_dir + '/' + fn)
        print (x, y)
        for (szname, szxy) in zip(mbdata.image_size_names, mbdata.image_size_sizes):
            if x <= szxy[0]:
                break
    print '<hr>'
    print '<form action="upload.cgi">'
    print '<input type=hidden name="act" value="1">'
    print '<input type=hidden name="d" value="%s">' % pif.render.pic_dir
    print '<input type=hidden name="f" value="%s">' % fn
    print '<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s&v=%s&cy=%d">%s</a>' % (pif.render.pic_dir, fn, pif.form_str('v', ''), cycle, pif.render.format_button('edit'))
    print pif.render.format_button_input('delete')
    print pif.render.format_button('stitch', 'stitch.cgi?fn_0=%s&submit=1&q=&fc=1' % (pif.render.pic_dir + '/' + fn))
    print 'New name: <input type="text" size="32" name="newname" value="%s">' % fn
    print pif.render.format_button_input('rename')
    print pif.render.format_radio('cpmv', [('c', 'copy'), ('m', 'move')], pif.form_str('cpmv', 'c'))
    if pif.is_allowed('m'):  # pragma: no cover
        if pif.form_bool('ov'):
            print '<input type=checkbox name="ov" value="1" checked>'
        else:
            print '<input type=checkbox name="ov" value="1">'
        print 'overwrite<br>'
        print 'Man: <input type="text" size="12" name="man" value="%s">' % get_man(pif)
        #print '''<a onclick="incrfield('man',1);"><img src="../pic/gfx/but_inc.gif" alt="UP" onmouseover="this.src='../pic/gfx/hov_inc.gif';" onmouseout="this.src='../pic/gfx/but_inc.gif';" ></a>'''
        #print '''<a onclick="incrfield('man',-1);"><img src="../pic/gfx/but_dec.gif" alt="UP" onmouseover="this.src='../pic/gfx/hov_dec.gif';" onmouseout="this.src='../pic/gfx/but_dec.gif';" ></a>'''
        print pif.render.format_button_up_down('man')
        print pif.render.format_button_input('move to library', 'lib')
        print 'Category:', pif.render.format_select('cat', sel_cat, pif.form_str('cat', ''))
        print pif.render.format_button_input('move to bin', 'mvbin')
        if cycle:
            print '<input type=checkbox name="cy" value="1" checked>'
        else:
            print '<input type=checkbox name="cy" value="1">'
        print 'cycle '
        print '<input type=checkbox name="inc" value="1"> increment name'
        print '<br>Variation: <input type="text" size="5" name="newvar" value="%s">' % pif.form_str('v', '')
        print 'Prefix:', pif.render.format_select('pref', sel_pref, pif.form_str('pref', pif.form_str('tysz', szname)))
        print pif.render.format_button_input('select to casting', 'select')
        print 'Move to:', pif.render.format_select('moveto', sel_moveto, pif.form_str('moveto', ''))
        print pif.render.format_button_input('select to category', 'selcat')
    print '</form>'


def action(pif, tdir, fn, act=1):
    global cycle
    nname = pif.form_str('newname', '')
    man = pif.form_str('man', '')
    cat = pif.form_str('cat', '')
    ov = pif.form_bool('ov', False)
    mv = pif.form_str('cpmv', 'c') == 'm'
    if pif.form_bool('delete'):
        useful.file_delete(tdir + '/' + fn)
    elif pif.form_bool('selcat'):
        dest = pif.form_str('moveto', '')
        if not nname or not dest:
            pif.render.format_warning('What?')
        else:
            useful.file_mover(tdir + '/' + fn, dest + '/' + nname, mv=mv, ov=ov)
    elif pif.form_bool('rename'):
        if not nname:
            pif.render.format_warning('What?')
        else:
            useful.file_mover(tdir + '/' + fn, tdir + '/' + nname, mv=mv, ov=ov)
    elif pif.form_bool('lib'):
        if not man:
            pif.render.format_warning('What?')
        elif not os.path.exists(os.path.join(config.LIB_MAN_DIR, man)):
            man2 = pif.dbh.fetch_alias(man)
            if not man2:
                pif.render.format_warning('bad destination')
            else:
                useful.file_mover(tdir + '/' + fn, os.path.join(config.LIB_MAN_DIR, man2['ref_id'].lower(), fn), mv=mv, ov=ov)
        else:
            useful.file_mover(tdir + '/' + fn, os.path.join(config.LIB_MAN_DIR, man, fn), mv=mv, ov=ov)
    elif pif.form_bool('mvbin'):
        if not os.path.exists(os.path.join('lib/new', cat)):
            print 'bad destination'
        else:
            useful.file_mover(tdir + '/' + fn, './new/' + cat + '/' + fn, mv=mv, ov=ov)
    elif pif.form_bool('select'):
        var = pif.form_str('newvar', '')
        pref = pif.form_str('pref', '')
        man = pif.form_str('man', '')
        inc = pif.form_str('inc', '')
        if not man:
            #man = tdir[tdir.rfind('/') + 1:]
            print 'Huh? (select, no man)'
        else:
            ddir = './' + config.IMG_DIR_MAN
            dnam = man
            if pref and adds.find(pref) >= 0:
                ddir = './' + config.IMG_DIR_ADD
                dnam = pref + '_' + dnam
                if var:
                    dnam += '-' + var
                inc = True
            elif var:
                ddir = './' + config.IMG_DIR_VAR
                dnam = dnam + '-' + var
                if pref:
                    dnam = pref + '_' + dnam
            elif pref:
                dnam = pref + '_' + dnam
            else:
                print "What?"
                return fn
            dnam = dnam.lower() + '.jpg'
            useful.file_mover(tdir + '/' + fn, ddir + '/' + dnam, mv=mv, ov=ov, inc=inc)

    if os.path.exists(fn):
        return fn
    elif cycle:
        dl, gl, ol, sl, xl = get_dir(tdir)
        while gl:
            if gl[0] == fn:
                gl.pop()
            else:
                return gl[0]
    return None

# -- imawidget

checked = {True: ' checked', False: ''}
def show_editor(pif, pdir, fn):
    full_path = os.path.join(pdir, fn)
    if not os.path.exists(full_path):
        print pif.render.format_warning('%s not found.' % full_path)
        return
    print editformstart
    print pif.render.format_hidden_input({'c': urllib.quote_plus(pif.form_str('c', ''))})
    x, y = show_edit_form(pif, pdir, fn)
    full_path = os.path.join(pdir, fn)
    root, ext = useful.root_ext(fn.strip())
    print '<table><tr><td></td><td>' + pif.render.format_image_art('hruler.gif') + '</td></tr>'
    print '<tr><td valign="top">' + pif.render.format_image_art('vruler.gif') + '</td><td valign="top">'
    #print '<a href="../' + full_path + '">' + pif.render.format_image_required([root], suffix=ext, also={"border": "0"}) + '</a>'
    dic = {'file': 'http://' + os.environ['SERVER_NAME'] + '/' + full_path, 'width': x, 'height': y}
    print def_edit_app % dic
    print '</td></tr></table>'
    print editformend % {'f': fn, 'd': pdir}


def pipe_chain(inp, pipes, stderr=None, verbose=True):
    #pth = '/usr/local/bin/'
    ch = '%'
    for pipe in pipes:
        if verbose:
            print ch, ' '.join(pipe)
        ch = '|'
        proc = subprocess.Popen(pipe, stdin=inp, stdout=subprocess.PIPE, stderr=stderr, close_fds=True)
        inp = proc.stdout
    if verbose:
        print '<br>'
    return inp.read()


def get_size(fn):
    l = pipe_chain(open(fn), import_file(fn) + [["/usr/local/bin/pamfile"]], subprocess.PIPE, verbose=False)
    f = l.split()
    try:
        x = int(f[3])
        y = int(f[5])
    except:
        x = y = 0
    return (x, y)


def save(pif, fn, of, tdir, nfn=None):
    if not tdir.endswith('/'):
        tdir = tdir + '/'
    if nfn:
        if '.' not in nfn:
            nfn = nfn + fn[fn.rfind('.'):]
    else:
        if '.' in fn:
            nfn = fn[:fn.rfind('.')] + '_s' + fn[fn.rfind('.'):]
        else:
            nfn = fn + '_s'
    open(tdir + nfn, "w").write(of)
    log(pif, nfn, tdir)
    return nfn


def rot_flip(pif):
    transforms = list()
    if pif.form_int('rr'):
        transforms.append(['/usr/local/bin/pamflip', '-r270'])
    elif pif.form_int('rh'):
        transforms.append(['/usr/local/bin/pamflip', '-r180'])
    elif pif.form_int('rl'):
        transforms.append(['/usr/local/bin/pamflip', '-r90'])
    elif pif.form_int('fh'):
        transforms.append(['/usr/local/bin/pamflip', '-lr'])
    elif pif.form_int('fv'):
        transforms.append(['/usr/local/bin/pamflip', '-tb'])
    return transforms


def resize(x=None, y=None):
    if not x and not y:
        return []
    if not y:
        return [["/usr/local/bin/pamscale", "-xsize", str(x)]]
    if not x:
        return [["/usr/local/bin/pamscale", "-ysize", str(y)]]
    return [["pamscale", "-xsize", str(x), "-ysize", str(y)]]


def cut(x1, y1, x2, y2):
    return [["/usr/local/bin/pamcut", "-top", str(y1), "-height", str(y2 - y1), "-left", str(x1), "-width", str(x2 - x1)]]


def mass_resize(pif, pic_dir, fn, nname, q, original_size, desc=''):
    var = pif.form_str('v', '')
    man = get_man(pif)
    if not man:
        print 'Huh? (mass, no man)'
        return

    xos, yos = original_size
    for pref in ['t', 's', 'm', 'l']:
        if xos < mbdata.imagesizes[pref][0]:
            break
        nname = fn
        if '.' in nname:
            nname = nname[:nname.rfind('.')]
        nname = nname + '_' + pref
        if pif.form_str('ot'):
            nname += '.' + pif.form_str('ot')
        shape(pif, pic_dir, fn, nname, q, mbdata.imagesizes[pref], original_size, False)

        ddir = './' + config.IMG_DIR_MAN
        dnam = man
        if var:
            ddir = './' + config.IMG_DIR_VAR
            dnam = dnam + '-' + var
            if pref:
                dnam = pref + '_' + dnam
        else:
            dnam = pref + '_' + dnam
        dnam = dnam.lower() + '.jpg'
        useful.file_mover(pic_dir + '/' + nname, ddir + '/' + dnam, mv=True, ov=True, inc=False)
        print '<br>', pif.render.format_image_required([dnam], pdir=ddir, also={"border": "0"}), '<br>'
        print '<hr>'

    name = man
    if var:
        name += '-' + var
    pif.dbh.insert_activity(name, pif.id, description=desc, image=ddir + '/' + dnam)


def shape(pif, tdir, fil, nname, bound, target_size, original_size, show_final=True):
    global xts, yts
    xts, yts = target_size
    x1, y1, x2, y2 = [int(x) for x in bound.split(',')]
    pth = tdir + '/' + fil
    root, ext = useful.root_ext(fil.strip())
    xcs = x2 - x1
    ycs = y2 - y1
    xos, yos = original_size

    print 'Shape :', pth, ': bounds', x1, y1, x2, y2, 'bound size', xcs, ycs, 'target size', xts, yts, '<br>'
    if xts and yts:
        x1, x2, y1, y2 = set_s200_sizes(tdir, fil, x1, x2, y1, y2, xts, yts, xos, yos)
        xcs = x2 - x1
        ycs = y2 - y1

        if xcs > xts:
            print "shrinking"
            of = pipe_chain(open(pth),
                    import_file(pth) +
                    cut(x1, y1, x2, y2) +
                    rot_flip(pif) +
                    resize(x=xts) +
                    export_file(nname, fil))
        elif xcs < xts:
            dx = xts - xcs
            dy = yts - ycs
            #x1, x2, y1, y2 = normalize(x1 - dx / 2, x2 + dx - (dx / 2), y1 - dy / 2, y2 + dy - (dy / 2), xts, yts)
            x1, x2, y1, y2 = normalize(x1, x2, y1, y2, xts, yts)
            print "expanding", x1, x2, y1, y2
            of = pipe_chain(open(pth),
                    import_file(pth) +
                    cut(x1, y1, x2, y2) +
                    rot_flip(pif) +
                    export_file(nname, fil))
        elif xos == xts and yos == yts and xos == xcs and yos == ycs:
            print "copying"
            of = open(pth).read()
        else:
            print "cutting"
            of = pipe_chain(open(pth),
                    import_file(pth) +
                    cut(x1, y1, x2, y2) +
                    rot_flip(pif) +
                    export_file(nname, fil))

    else:

        if xts < x2 - x1:
            print "trim shrinking x"
            of = pipe_chain(open(pth),
                    import_file(pth) +
                    cut(x1, y1, x2, y2) +
                    rot_flip(pif) +
                    resize(x=xts) +
                    export_file(nname, fil))
        elif yts < y2 - y1:
            print "trim shrinking y"
            of = pipe_chain(open(pth),
                    import_file(pth) +
                    cut(x1, y1, x2, y2) +
                    rot_flip(pif) +
                    resize(y=yts) +
                    export_file(nname, fil))
        else:
            print "trim cutting"
            of = pipe_chain(open(pth),
                    import_file(pth) +
                    cut(x1, y1, x2, y2) +
                    rot_flip(pif) +
                    export_file(nname, fil))

    print '<br>'
    nfn = save(pif, fil, of, tdir, nname)

    print nfn, tdir, pth, '%s (%d, %d)<br>' % ((nfn,) + get_size(tdir + '/' + nfn))
    if show_final:
        print pif.render.format_image_required([nfn], suffix=ext, also={"border": "0"}), '<br>'


def show_redoer(pif, pdir, fn):
    print editformstart
    show_edit_form(pif, pdir, fn)
    print 'Bounds:', pif.render.format_text_input('q', 20, value=pif.form_str('q'))
    print editformend % {'f': fn, 'd': pdir}
    print '<hr>'


def show_edit_form(pif, pdir, fn):
    if os.path.exists(os.path.join(pdir, '.ima')):
        presets = eval(open(os.path.join(pdir, '.ima')).read())
    else:
        presets = dict()
    full_path = os.path.join(pdir, fn)
    if not os.path.exists(full_path):
        print pif.render.format_warning('%s not found.<br>' % full_path)
        return 0, 0

    x, y = get_size(full_path)
    print '<div class="lefty">'
    print '(%d, %d)' % (x, y)
    print '<input type="radio" name="tysz" value="q"%s>' % checked[presets.get('tysz') == 'q']  #checked[not pif.form_str('v')]
    print 'x: <input name="x" type="text" size="4" value="%s"> y: <input name="y" type="text" size="4" value="%s">' % (xts, yts)
    print pif.render.format_radio('tysz', [(siz, siz.upper()) for siz in mbdata.image_size_names], presets.get('tysz', 's'))
    print '-', pif.render.format_checkbox("unlv", [("1", "V")], presets.get("unlv", []))
    print pif.render.format_checkbox("unlh", [("1", "H")], presets.get("unlh", []))
    print pif.render.format_button_input('keep')
    print pif.render.format_checkbox("rl", [("1", "RL")], presets.get("rl", []))
    print pif.render.format_checkbox("rh", [("1", "RH")], presets.get("rh", []))
    print pif.render.format_checkbox("rr", [("1", "RR")], presets.get("rr", []))
    print pif.render.format_checkbox("fh", [("1", "FH")], presets.get("fh", []))
    print pif.render.format_checkbox("fv", [("1", "FV")], presets.get("fv", []))
    print '<br>Name:', pif.render.format_text_input('newname', 20, value=pif.form_str('newname', ''))
    print pif.render.format_select('ot', otypes, 'jpg')
    print pif.render.format_button_input('resize')
    print pif.render.format_button_input('crop')
    print pif.render.format_button_input('crop and shrink', 'shrink')
    print pif.render.format_button_input('wipe')
    print pif.render.format_button_input('rename')
    if pif.is_allowed('m'):  # pragma: no cover
        print 'Var: ' + pif.render.format_text_input('v', 8, value=pif.form_str('v', ''))
    print pif.render.format_checkbox("repl", [("1", "Replace")], presets.get("repl", []))
    print pif.render.format_button_input('mass')
    return x, y


def set_s200_sizes(tdir, fil, x1, x2, y1, y2, xts, yts, xos, yos):
    #xos, yos = get_size(tdir + '/' + fil)
    xcs = x2 - x1
    ycs = y2 - y1
    ratio = float(xts) / float(yts)
    print "set_s200_sizes", tdir + '/' + fil, x1, y1, "/", x2, y2, ';', xts, yts, ';', xcs, ycs, ';', xos, yos, ';', ratio, "<br>"
    if xcs < xts:
        if xos < xts:
            print "fix x to orig /"
            x1 = 0
            x2 = xos - 1
        else:
            print "fix x to target /"
            x1 = max(0, x1 - (xts - xcs) / 2)
            x2 = x1 + xts
    if ycs < yts:
        if yos < yts:
            print "fix y to orig /"
            y1 = 0
            y2 = yos - 1
        else:
            print "fix y to target /"
            y1 = max(0, y1 - (yts - ycs) / 2)
            y2 = y1 + yts
    print "(", x1, y1, "/", x2, y2, ")"
    xcs = x2 - x1
    ycs = y2 - y1
    # might revisit this, for images that are off center this might not be right
    if xts <= xos and yts <= yos and xcs <= xts and ycs <= yts:
        print "shape expanding x and y<br>"
        x1 = x1 - (xts - xcs) / 2
        x2 = x1 + xts
        y1 = y1 - (yts - ycs) / 2
        y2 = y1 + yts
        print "(", x1, y1, ") (", x2, y2, ")"
        x1, x2, y1, y2 = normalize(x1, x2, y1, y2, xos, yos)
    elif xcs < int(float(ycs) * ratio):
        # too tall - expand x
        print "shape expanding x"
        nxs = int(float(ycs) * ratio)
        nx1 = x1 - (nxs - xcs) / 2
        nx2 = nx1 + nxs
        if nxs > xos:
            print "off both edges<br>"
            nx1 = 0
            nx2 = xos
        elif nx1 < 0:
            print "off the left<br>"
            nx2 = nx2 - nx1
            nx1 = 0
        elif nx2 > xos:
            print "off the right<br>"
            nx1 = nx1 - (nx2 - xos)
            nx2 = xos
        else:
            pass
            print "on<br>"
        x1 = nx1
        x2 = nx2
    elif xcs > int(float(ycs) * ratio):
        # too wide - expand y
        print "shape expanding y"
        nys = int(float(xcs) / ratio)
        ny1 = y1 - (nys - ycs) / 2
        ny2 = ny1 + nys
        if nys > yos:
            print "off both edges<br>"
            ny1 = 0
            ny2 = yos
        elif ny1 < 0:
            print "off the top<br>"
            ny2 = nys
            ny1 = 0
        elif ny2 > yos:
            print "off the bottom<br>"
            #ny1 = ny1 - (ny2 - yos)
            ny1 = yos - nys
            ny2 = yos
        else:
            pass
            print "on<br>"
        y1 = ny1
        y2 = ny2
    else:
        print "shape as is<br>"
        # hit the jackpot, Mel!
        pass
    print 'set_s200_sizes returned', x1, y1, '/', x2, y2, '->', x2 - x1, y2 - y1, '<br>'
    return x1, x2, y1, y2


def normalize(x1, x2, y1, y2, xm, ym):
    print 'normalize', x1, y1, "/", x2, y2, "orig", xm, ym
    if x1 < 0:
        x2 = x2 - x1
        x1 = 0
        print "x1"
    if y1 < 0:
        y2 = y2 - y1
        y1 = 0
        print "y1"
    if x2 >= xm:
        x1 = x1 - (x2 - xm)
        x2 = xm
        print "x2"
    if y2 >= ym:
        y1 = y1 - (y2 - ym)
        y2 = ym
        print "y2"
    print 'returns', x1, y1, "/", x2, y2, '<br>'
    return x1, x2, y1, y2


def shrink(pif, tdir, fil, nname, bound, maxsize):
    print 'In shrink', tdir, fil, nname, bound, maxsize, '<br>'
    global xts, yts
    x1, y1, x2, y2 = [int(x) for x in bound.split(',')]
    xts, yts = maxsize
    xcs = x2 - x1
    ycs = y2 - y1
    if not xts:
        xts = xcs
    if not yts:
        yts = ycs
    pth = tdir + '/' + fil
    print 'shrink', x1, y1, x2, y2, ':', xcs, ycs, ':', xts, yts, '<br>', pth, '<br>'
    if xcs == xts and ycs == yts:
        print "cutting", '<br>'
        of = pipe_chain(open(pth),
                import_file(pth) +
                cut(x1, y1, x1 + xcs, y1 + ycs) +
                rot_flip(pif) +
                export_file(nname, fil))
    elif xts/xcs < yts/ycs:
        print "shrinking x", '<br>'
        of = pipe_chain(open(pth),
                import_file(pth) +
                cut(x1, y1, x1 + xcs, y1 + ycs) +
                rot_flip(pif) +
                resize(x=xts) +
                export_file(nname, fil))
    else:
        print "shrinking y", '<br>'
        of = pipe_chain(open(pth),
                import_file(pth) +
                cut(x1, y1, x1 + xcs, y1 + ycs) +
                rot_flip(pif) +
                resize(y=yts) +
                export_file(nname, fil))
    nfn = save(pif, fil, of, tdir, nname)

    print nfn, tdir, pth, '<br>'
    print pif.render.format_image_required([nfn], suffix='jpg', also={"border": "0"}), '<br>'
    print '%s (%d, %d)' % ((nfn,) + get_size(tdir + '/' + nfn))


def crop(pif, tdir, fil, nname, bound):
    global xts, yts
    x1, y1, x2, y2 = [int(x) for x in bound.split(',')]
    pth = tdir + '/' + fil
    print 'crop', x1, y1, x2, y2, ':', x2-x1, y2-y1, '<br>', pth, '<br>'
    print "cutting", '<br>'
    of = pipe_chain(open(pth),
            import_file(pth) +
            cut(x1, y1, x2, y2) +
            rot_flip(pif) +
            export_file(nname, fil))
    nfn = save(pif, fil, of, tdir, nname)

    print nfn, tdir, pth, '<br>'
    print pif.render.format_image_required([nfn], suffix='jpg', also={"border": "0"}), '<br>'
    print '%s (%d, %d)' % ((nfn,) + get_size(tdir + '/' + nfn))


def rename(tdir, fil, nname):
    if not os.path.exists(tdir + '/' + nname):
        os.system('mv %s/%s %s/%s' % (tdir, fil, tdir, nname))
    else:
        print "Target exists"


@basics.web_page
def imawidget(pif):
    pif.render.print_html()
    pif.restrict('v')

    #print pif.form, '<br>'
    fn   = pif.form_str("f", '')
    root, ext = useful.root_ext(fn.strip())
    if pif.form_str('ot'):
        ext = pif.form_str('ot')
#    if pif.form_str('tysz'):
#       root += '_' + pif.form_str('tysz')
    nname = root + '.' + ext
    tdir = pif.form_str("d", '.')
    if not pif.is_allowed('m'):
        tdir = '../inc'

    global xts, yts
    nvar = pif.form_str("newvar", '')
    pif.form_def("v", '')
    var  = pif.form_str('v')
    pif.render.pic_dir = tdir

    pif.render.title = pif.render.pagetitle = pif.render.pic_dir + '/' + fn
    print pif.render.format_head(extra=def_edit_js + pif.render.increment_js)
    print pif.form, '<br>'

    if pif.form_str('f') and os.path.exists(os.path.join(pif.form_str('d', ''), 'descr.txt')):
        descs = open(os.path.join(pif.form_str('d', ''), 'descr.txt')).readlines()
        descs = dict([x.strip().split('\t', 1) for x in descs])
        # mod_id, var_id, year, comment
        print descs.get(os.path.splitext(pif.form_str('f'))[0], '').replace('\t', '<br>')
        print '<hr>'

    if pif.form_bool('keep'):
        picker(pif, fn)
        print '<hr>'
        print pif.render.format_image_required([fn[:fn.rfind('.')]], suffix=fn[fn.rfind('.') + 1:], also={"border": "0"}), '<br>'
        print pif.render.format_tail()
        return

    pif.form_def("q", '')
    q = pif.form_str('q')
    pif.form_def("newname", root)
    nname = pif.form_str("newname")

    tysz  = pif.form_str("tysz", "")
    xts = yts = 0
    if tysz == 'q':
        xts   = pif.form_int('x')
        yts   = pif.form_int('y')
    elif tysz:
        xts, yts = mbdata.imagesizes[tysz]
    if pif.form_bool('wipe'):
        tysz = 'w'
    if pif.form_int('unlv'):
        yts   = 0
    if pif.form_int('unlh'):
        xts   = 0
    if not nname:
        nname = fn
    if '.' in nname:
        nname = nname[:nname.rfind('.')]
    if not pif.form_int('repl') and tysz:
        nname = nname + '_' + tysz
    if pif.form_str('ot'):
        nname += '.' + pif.form_str('ot')
    else:
        nname += '.jpg'

    xos, yos = get_size(pif.render.pic_dir + '/' + fn)
    if not q:
        q = '0,0,%d,%d' % (xos, yos)

    picker(pif, nname)
    print '<hr>'
    is_edited = nname != fn
    try:
        if pif.form_bool('mass'):
            mass_resize(pif, pif.render.pic_dir, fn, nname, q, (xos, yos))
            man = get_man(pif)
            if man and pif.form_str('v'):
                print pif.render.format_button("promote", 'vars.cgi?mod=%s&var=%s&promote=1' % (man, pif.form_str('v')))
        elif pif.form_bool('wipe'):
            save_presets(pif, pif.render.pic_dir)
            wiper(pif, pif.render.pic_dir, fn, nname, q, xos, yos, pif.form_int('unlv'), pif.form_int('unlh'))
        elif pif.form_bool('resize'):
            save_presets(pif, pif.render.pic_dir)
            if not pif.form_bool('repl'):
                show_redoer(pif, pif.render.pic_dir, fn)
            shape(pif, pif.render.pic_dir, fn, nname, q, (xts, yts), (xos, yos))
        elif pif.form_bool('crop'):
            save_presets(pif, pif.render.pic_dir)
            if not pif.form_bool('repl'):
                show_redoer(pif, pif.render.pic_dir, fn)
            crop(pif, pif.render.pic_dir, fn, nname, q)
        elif pif.form_bool('shrink'):
            save_presets(pif, pif.render.pic_dir)
            if not pif.form_bool('repl'):
                show_redoer(pif, pif.render.pic_dir, fn)
            shrink(pif, pif.render.pic_dir, fn, nname, q, (xts, yts))
        elif pif.form_bool('rename'):
            rename(pif.render.pic_dir, fn, nname)
        else:
            show_editor(pif, pif.render.pic_dir, fn)
            is_edited = False
    except:
        pif.show_error()

    if is_edited:
        print pif.render.format_button('replace', 'upload.cgi?act=1&d=%s&f=%s&newname=%s&rename=1&cpmv=m&ov=1' % (tdir, nname, fn))

    print pif.render.format_tail()


def save_presets(pif, pdir):
    if os.path.exists(os.path.join(pdir, '.ima')):
        presets = {
            "unlv": [pif.form_str("unlv", '')],
            "unlh": [pif.form_str("unlh", '')],
            "rl": [pif.form_str("rl", '')],
            "rh": [pif.form_str("rh", '')],
            "rr": [pif.form_str("rr", '')],
            "fh": [pif.form_str("fh", '')],
            "fv": [pif.form_str("fv", '')],
            "repl": [pif.form_str("repl", '')],
            "tysz": pif.form_str("tysz", ''),
        }
        open(os.path.join(pdir, '.ima'), 'w').write(str(presets))


def wiper(pif, pdir, fin, fout, q, xs, ys, wipev, wipeh):
    print 'wiper', pdir, fin, fout, q, wipev, wipeh, '<br>'
    xl, yt, xr, yb = q.split(',')
    xl, yt, xr, yb = int(xl), int(yt), int(xr), int(yb)
    if xl > xr:
        x = xl
        xl = xr
        xr = x
    if yt > yb:
        y = yt
        yt = yb
        yb = y
    xr -= 1
    yb -= 1
    x1, y1, x2, y2 = xl, yt, xr, yb

    img = Image.open(pdir + '/' + fin)
    img = img.convert('RGB')

    while 1:
        if x1 > x2 or y1 > y2:
            break
        if wipev:
            if y1 != 0:
                wiper_copy(img, x1, yt, x2, yt, x1, y1, x2, y1)
                y1 += 1
            if x1 > x2 or y1 > y2:
                break
            if y2 != ys - 1:
                wiper_copy(img, x1, yb, x2, yb, x1, y2, x2, y2)
                y2 -= 1
        elif wipeh:
            if x1 != 0:
                wiper_copy(img, xl, y1, xl, y2, x1, y1, x1, y2)
                x1 += 1
            if x1 > x2 or y1 > y2:
                break
            if x2 != xs - 1:
                wiper_copy(img, xr, y1, xr, y2, x2, y1, x2, y2)
                x2 -= 1
        else:
            if y1 != 0:
                wiper_copy(img, x1, yt, x2, yt, x1, y1, x2, y1)
                y1 += 1
            if x1 != 0:
                wiper_copy(img, xl, y1, xl, y2, x1, y1, x1, y2)
                x1 += 1
            if x1 > x2 or y1 > y2:
                break
            if y2 != ys - 1:
                wiper_copy(img, x1, yb, x2, yb, x1, y2, x2, y2)
                y2 -= 1
            if x2 != xs - 1:
                wiper_copy(img, xr, y1, xr, y2, x2, y1, x2, y2)
                x2 -= 1
    img.save(pdir + '/' + fout)

    root, ext = useful.root_ext(fout.strip())
    #print pif.render.format_image_required([fout], suffix=ext, also={"border": "0"}), '<br>'
    print '%s (%d, %d)<br>' % ((fout,) + get_size(pdir + '/' + fout))
    show_editor(pif, pif.render.pic_dir, fout)


def wiper_copy(img, xf1, yf1, xf2, yf2, xt1, yt1, xt2, yt2):
    #print ('%3d ' * 8) % (xf1, yf1, xf2 + 1, yf2 + 1, xt1, yt1, xt2 + 1, yt2 + 1)
    cp = img.crop((xf1, yf1, xf2 + 1, yf2 + 1))
    img.paste(cp, (xt1, yt1, xt2 + 1, yt2 + 1))


# ----- upload


def pic_form(pif, restrict=False, desc=''):
    mod = pif.form_str('m', '')
    var = pif.form_str('v', '')
    print '<form action="upload.cgi" enctype="multipart/form-data" method="post" name="upload">'
    if pif.form_has('y'):
        print '<input type="hidden" name="y" value="%s">' % pif.form_str('y')
    #format_table({'also': {}, 'id': '', 'style_id': '', 'rows': []})
    #rows=[{'ids': [], 'also': {}, 'cells': []}, ...]
    #cells=[{'col': None, 'content': "&nbsp;", 'hdr': False, 'also': {}, 'large': False, 'id': ''}, ...]

    '''
    table = pif.render.create_table()
    table.row()
    if mod:
        rows.append({'cells': [{'col': 0, 'content': 'Model'}, {'col': 1, 'content': mod}]})
        print '<input type="hidden" name="m" value="%s">' % mod
        rows.append({'cells': [{'col': 0, 'content': 'Variation'}, {'col': 1, 'content': pif.render.format_text_input('v', 8, value=var)}]})
    if not restrict:
        rows.append({'cells': [{'col': 0, 'content': 'Directory'},
                    {'col': 1, 'content': pif.render.format_text_input('d', 64, value=pif.form_str('d', '../inc'))}]})
        rows.append({'cells': [{'col': 0, 'content': 'Rename file to'},
                    {'col': 1, 'content': pif.render.format_text_input('n', 64, value=pif.form_str('r', '')) + " (optional)"}]})
        rows.append({'cells': [{'col': 0},
                    {'col': 0, 'content': "Choose one of the following:"}]})
    rows.append({'cells': [{'col': 0, 'content': 'File to Upload'},
                {'col': 1, 'content': '<input type="file" name="f" size="40">'}]})
    if not restrict:
        rows.append({'cells': [{'col': 0, 'content': 'URL to grab'},
                    {'col': 1, 'content': pif.render.format_text_input('u', 80, 80)}]})
        rows.append({'cells': [{'col': 0, 'content': 'URL to scrape'},
                    {'col': 1, 'content': pif.render.format_text_input('s', 80, 80)}]})
    rows.append({'cells': [{'col': 0, 'content': 'Comment'},
                {'col': 1, 'content': pif.render.format_text_input('c', 80, 80, desc)}]})
    if not restrict and mod:  # var:
        rows.append({'cells': [{'col': 0, 'content': 'Choose from library'},
                    {'col': 1, 'content': pif.render.format_button_input("select", name="l", also={})}]})
    rows.append({'cells': [{'col': 0, 'content': '&nbsp;'},
                {'col': 0, 'content': pif.render.format_button_input() +
                    (pif.render.format_button_input("replace") if not restrict else '') +
                    pif.render.format_button_reset("upload") +
                    pif.render.format_button_input("mass")}]})
    print pif.render.format_table({'rows': rows})
    '''

    rows = list()
    if mod:
        rows.append({'cells': [{'col': 0, 'content': 'Model'}, {'col': 1, 'content': mod}]})
        print '<input type="hidden" name="m" value="%s">' % mod
        rows.append({'cells': [{'col': 0, 'content': 'Variation'}, {'col': 1, 'content': pif.render.format_text_input('v', 8, value=var)}]})
    if not restrict:
        rows.append({'cells': [{'col': 0, 'content': 'Directory'},
                    {'col': 1, 'content': pif.render.format_text_input('d', 64, value=pif.form_str('d', '../inc'))}]})
        rows.append({'cells': [{'col': 0, 'content': 'Rename file to'},
                    {'col': 1, 'content': pif.render.format_text_input('n', 64, value=pif.form_str('r', '')) + " (optional)"}]})
        rows.append({'cells': [{'col': 0},
                    {'col': 0, 'content': "Choose one of the following:"}]})
    rows.append({'cells': [{'col': 0, 'content': 'File to Upload'},
                {'col': 1, 'content': '<input type="file" name="f" size="40">'}]})
    if not restrict:
        rows.append({'cells': [{'col': 0, 'content': 'URL to grab'},
                    {'col': 1, 'content': pif.render.format_text_input('u', 80, 80)}]})
        rows.append({'cells': [{'col': 0, 'content': 'URL to scrape'},
                    {'col': 1, 'content': pif.render.format_text_input('s', 80, 80)}]})
    rows.append({'cells': [{'col': 0, 'content': 'Comment'},
                {'col': 1, 'content': pif.render.format_text_input('c', 80, 80, desc)}]})
    if not restrict and mod:  # var:
        rows.append({'cells': [{'col': 0, 'content': 'Choose from library'},
                    {'col': 1, 'content': pif.render.format_button_input("select", name="l", also={})}]})
    rows.append({'cells': [{'col': 0, 'content': '&nbsp;'},
                {'col': 0, 'content': pif.render.format_button_input() +
                    (pif.render.format_button_input("replace") if not restrict else '') +
                    pif.render.format_button_reset("upload") +
                    pif.render.format_button_input("mass")}]})
    print pif.render.format_table({'rows': rows})

    '''
    print pif.render.format_table_start()
    if mod:
        print pif.render.format_row_start()
        print pif.render.format_cell(0, 'Model')
        print pif.render.format_cell(1, mod)
        print '<input type="hidden" name="m" value="%s">' % mod
        print pif.render.format_row_end()
        print pif.render.format_row_start()
        print pif.render.format_cell(0, 'Variation')
        print pif.render.format_cell(1, pif.render.format_text_input('v', 8, value=var))
        print pif.render.format_row_end()
    if not restrict:
        print pif.render.format_row_start()
        print pif.render.format_cell(0, 'Directory')
        print pif.render.format_cell(1, pif.render.format_text_input('d', 64, value=pif.form_str('d', '../inc')))
        print pif.render.format_row_end()
        print pif.render.format_row_start()
        print pif.render.format_cell(0, 'Rename file to')
        print pif.render.format_cell(1, pif.render.format_text_input('n', 64, value=pif.form_str('r', '')) + " (optional)")
        print pif.render.format_row_end()
        print pif.render.format_row_start()
        print pif.render.format_cell(0)
        print pif.render.format_cell(0, "Choose one of the following:")
        print pif.render.format_row_end()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'File to Upload')
    print pif.render.format_cell(1, '<input type="file" name="f" size="40">')
    print pif.render.format_row_end()
    if not restrict:
        print pif.render.format_row_start()
        print pif.render.format_cell(0, 'URL to grab')
        print pif.render.format_cell(1, '<input type="text" name="u" size="80">')
        print pif.render.format_row_end()
        print pif.render.format_row_start()
        print pif.render.format_cell(0, 'URL to scrape')
        print pif.render.format_cell(1, '<input type="text" name="s" size="80">')
        print pif.render.format_row_end()
#       print pif.render.format_row_start()
#       print pif.render.format_cell(0, 'Replace existing')
#       print pif.render.format_cell(1, '<input type="checkbox" name="o">')
#       print pif.render.format_row_end()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, 'Comment')
    print pif.render.format_cell(1, '<input type="text" name="c" size="80" value="%s">' % desc)
    print pif.render.format_row_end()
    if not restrict and mod:  # var:
        print pif.render.format_row_start()
        print pif.render.format_cell(0, 'Choose from library')
        print pif.render.format_cell(1, pif.render.format_button_input("select", name="l", also={}))
        print pif.render.format_row_end()
    print pif.render.format_row_start()
    print pif.render.format_cell(0, '&nbsp;')
    print pif.render.format_cell(0, pif.render.format_button_input() +
        (pif.render.format_button_input("replace") if not restrict else '') +
        pif.render.format_button_reset("upload") +
        pif.render.format_button_input("mass"))
    print pif.render.format_row_end()
    print pif.render.format_table_end()
    '''
    print '</form>'


def pic_show(pif, tdir, fn, desc=''):
    show(pif, tdir, fn)


cols = 6
def show_list(pif, title, tdir, fl):
    if not fl:
        return
    clen = (len(fl) - 1) / cols + 1
    ffl = [fl[(x*clen):((x+1)*clen)] for x in range(0, cols)]
    print '<h4>%s (%d)</h4>' % (title, len(fl))
    print "<table width=100%><tr valign=top>"
    for cl in ffl:
        print "<td width=%d%%>" % (100/cols)
        for f in cl:
            root, ext = useful.root_ext(f.strip())
            fst = os.stat(tdir + '/' + f)
            perms = fst[stat.ST_MODE]
            if (perms & 5) == 0:
                print '%s<br>' % f
            elif ext in image_inputter:
                print '<a href="?d=%s&n=%s">%s</a><br>' % (tdir, f, f)
            else:
                print f
        print "</td>"
    print "</tr></table>"
    print '<br><hr>'


def show_dir(pif, tdir, desc=''):
    print '<hr>'

    dl, gl, ol, sl, xl = get_dir(tdir)

    #show_list(pif, "Directories", tdir, dl)

    if gl:
        show_list(pif, "Graphics", tdir, gl)

    #show_list(pif, "Data Files", tdir, sl)
    #show_list(pif, "Other Files", tdir, ol)


def restricted_upload(pif):
    direc = '../inc'
    descrips = open(direc + '/descr.txt').readlines()
    fn = 1
    if descrips:
        ln = descrips[-1].split()[0]
        for iln in range(0, len(ln)):
            if not ln[iln].isdigit():
                ln = ln[:iln]
                break
        fn = int(ln) + 1
    fn = '%09d' % fn
    if pif.form_str('u'):
        fn = grab_url_file(pif, pif.form_str('u'), direc, fn)
        thanks(pif, fn)
    elif pif.form_str('f'):
        upload_file(pif, pif.form_str('f'), direc, fn)
        thanks(pif, fn)
    else:
        pic_form(pif, restrict=True)


def thanks(pif, fn):
    comment = '-'
    if pif.form_str('c'):
        comment = re.compile(r'\s\s*').sub(' ', pif.form_str('c'))
    open('../inc/descr.txt', 'a+').write('\t'.join([fn, pif.form_str('m', '-'), pif.form_str('v', '-'), pif.form_str('y', '-'), comment]) + '\n')
    print pif.render.format_warning('Thank you for submitting that file.')
    print "Unfortunately, you will now have to use your browser's BACK button to get back to where you were, as I have no idea where that was."


def mass_upload_main(pif):
    # dnfus = bad
    # mvdfus = good
    #print '<hr>'
    #print pif.form
    print '<hr>'
    direc = pif.form_str('d', '')
    if not pif.is_allowed('u'):
        restricted_upload(pif)
        return

    if pif.form_str('ul'):
        for url in pif.form_str('ul').split('\n'):
            url = url.strip()
            if url:
                print url, '<br>'
                grab_url_file(pif, url, direc, '')
                sys.stdout.flush()
        print '<hr>'
    else:
        print '<form action="upload.cgi" enctype="multipart/form-data" method="post" name="upload">'
        print '<input type="hidden" value="1" name="mass">'
        print pif.render.format_table_start()
        print pif.render.format_row_start()
        print pif.render.format_cell(0, 'Directory')
        print pif.render.format_cell(1, pif.render.format_text_input('d', 64, value=pif.form_str('d', '../inc')))
        print pif.render.format_row_end()
        print pif.render.format_row_start()
        print pif.render.format_cell(0, 'URLs to grab')
        print pif.render.format_cell(1, '<textarea name="ul" cols="80" rows="20" wrap="off"></textarea>')
        print pif.render.format_row_end()
        print pif.render.format_row_start()
        print pif.render.format_cell(0, '&nbsp;')
        print pif.render.format_cell(0, pif.render.format_button_input() + pif.render.format_button_reset("upload"))
        print pif.render.format_row_end()
        print pif.render.format_table_end()
        print '</form>'


@basics.web_page
def upload_main(pif):
    # dnfus = bad
    # mvdfus = good
    os.environ['PATH'] += ':/usr/local/bin'
    pif.render.print_html()
    pif.render.title = 'upload - ' + pif.form_str('m', '')
    print pif.render.format_head(extra=def_edit_js + pif.render.reset_button_js + pif.render.increment_js)
    if pif.form_bool('mass'):
        mass_upload_main(pif)
        print pif.render.format_tail()
        return
    #print pif.form
    print '<hr>'
    desc = pif.form_str('c')
    if pif.form_str('m') and pif.form_str('v'):
        var = pif.dbh.fetch_variation(pif.form_str('m'), pif.form_str('v'))
        if var:
            var = var[0]
            var = pif.dbh.depref('variation', var)
            print '<br>%s:<ul>' % pif.form_str('v')
            print '<li>description:', var['text_description']
            print '<li>base:', var['text_base']
            print '<li>body:', var['text_body']
            print '<li>interior:', var['text_interior']
            print '<li>wheels:', var['text_wheels']
            print '<li>windows:', var['text_windows'], '</ul>'
            print '<hr>'
    overwrite = False
    direc = pif.form_str('d', '')
    if not pif.is_allowed('u'):
        restricted_upload(pif)
        print pif.render.format_tail()
        return
    elif not pif.is_allowed('m'):
        direc = '../inc'
    elif pif.form_bool('replace'):
        overwrite = True
    try:
        if pif.form_int('act'):
            do_action(pif, direc, pif.form_str('f'), cy=pif.form_int('cy'))
        elif pif.form_str('m'):
            if not pif.form_str('d'):
                direc = os.path.join(config.LIB_MAN_DIR, pif.form_str('m').lower())
            if pif.form_str('u'):
                grab_url_mod(pif, pif.form_str('u'), pif.form_str('m'), pif.form_str('v'), overwrite=overwrite, desc=desc)
            elif pif.form_str('s'):
                scrape_url_mod(pif, pif.form_str('s'), pif.form_str('m'), pif.form_str('v'), overwrite=overwrite, desc=desc)
            elif pif.form_str('f'):
                upload_mod(pif, pif.form_str('f'), pif.form_str('m'), pif.form_str('v'), overwrite=overwrite, desc=desc)
            elif pif.form_str('l'):
                select_from_library(pif, pif.form_str('m'), pif.form_str('v'), desc=desc)
            else:
                pic_form(pif, desc=desc)
        else:
            if pif.form_str('u'):
                grab_url_pic(pif, pif.form_str('u'), direc, pif.form_str('n'), overwrite=overwrite, track=True, desc=desc)
            elif pif.form_str('s'):
                scrape_url_pic(pif, pif.form_str('s'), direc, pif.form_str('n'), overwrite=overwrite, desc=desc)
            elif pif.form_str('r'):
                pic_form(pif, desc=desc)
            elif pif.form_str('f'):
                fn = pif.form_str('n')
                if not fn:
                    fn = pif.form_str('f.name')
                if not fn:
                    fn = 'unknown'
                upload_pic(pif, pif.form_str('f'), direc, fn, overwrite=overwrite, desc=desc)
            elif pif.form_str('n'):
                pic_show(pif, direc, pif.form_str('n'), desc=desc)
            elif pif.form_str('d'):
                show_dir(pif, direc, desc=desc)
            else:
                pic_form(pif, desc=desc)
    except OSError:
        print pif.render.format_warning('fail:', traceback.format_exc(0))
    print pif.render.format_tail()


def do_action(pif, tdir, fn, act=1, cy=0):
    nfn = action(pif, tdir, fn, act)
    if nfn:
        show_picture(pif, nfn)
    elif cy:
        pif.render.pic_dir = tdir
        dl, gl, ol, sl, xl = get_dir(tdir)
        if gl:
            show_picture(pif, gl[0])
        else:
            show_dir(pif, tdir)
    else:
        show_dir(pif, tdir)

# -- stitch

def stitch_h(ofn, fa, miny, limit_x, limit_y, verbose=False):
    if limit_y:
        miny = min(miny, limit_y)
    cat = ['pnmcat', '-lr']
    for f in fa:
        pipes = import_file(f[0]) + \
                cut(f[3], f[4], f[5], f[6]) + \
                resize(x=limit_x, y=miny)
        outf = pipe_chain(open(f[0]), pipes, verbose=verbose)
        if verbose:
            print '>', f[0] + '.pnm', '<br>'
        open(f[0] + '.pnm', 'w').write(outf)
        cat.append(f[0] + '.pnm')
    outf = pipe_chain(open('/dev/null'), [cat] + export_file(ofn), verbose=verbose)
    if verbose:
        print '>', ofn, '<br>'
    open(ofn, 'w').write(outf)

    if not verbose:
        for f in fa:
            os.unlink(f[0] + '.pnm')


def stitch_v(ofn, fa, minx, limit_x, limit_y, verbose=False):
    limit_y = 0
    if limit_x:
        minx = min(minx, limit_x)
    cat = ['pnmcat', '-tb']
    for f in fa:
        pipes = import_file(f[0]) + \
                cut(f[3], f[4], f[5], f[6]) + \
                resize(x=minx, y=limit_y)
        outf = pipe_chain(open(f[0]), pipes, verbose=verbose)
        if verbose:
            print '>', f[0] + '.pnm', '<br>'
        open(f[0] + '.pnm', 'w').write(outf)
        cat.append(f[0] + '.pnm')
    outf = pipe_chain(open('/dev/null'), [cat] + export_file(ofn), verbose=verbose)
    if verbose:
        print '>', ofn, '<br>'
    open(ofn, 'w').write(outf)

    if not verbose:
        for f in fa:
            os.unlink(f[0] + '.pnm')


def show_widget(pif, filepath):
    x, y = get_size(filepath)
    dic = {'file': 'http://' + os.environ['SERVER_NAME'] + '/' + filepath, 'width': x, 'height': y}
    return def_edit_app % dic


def stitch_read_form(pif, verbose=False):
    file_count = pif.form_int('fc')
    fsl = list()
    for file_num in range(0, file_count + 1):
        fs = dict()
        if pif.form_has('fn_%d' % file_num):
            fs['fn'] = pif.form_str('fn_%d' % file_num)
        fs['n'] = '%d' % file_num
        if file_num < file_count - 2:
            fs['x1'] = pif.form_int('x1_%d' % file_num)
            fs['y1'] = pif.form_int('y1_%d' % file_num)
            fs['x2'] = pif.form_int('x2_%d' % file_num)
            fs['y2'] = pif.form_int('y2_%d' % file_num)
        elif file_num == file_count - 2:
            fs['x1'], fs['y1'], fs['x2'], fs['y2'] = [int(x) for x in pif.form_str('q').split(',')]
        elif file_num == file_count - 1:
            if fs.get('fn', '').startswith('http://'):
                fs['fn'] = fs['fn'][fs['fn'].find('/', 7) + 1:]
        if verbose:
            print file_num, fs, '<br>'
        fsl.append(fs)
    return fsl


def stitch_finalize(pif, verbose=False):
    fsl = stitch_read_form(pif, verbose)
    final = fsl[-2].get('fn', '').strip()
    if not final:
        final = fsl[0]['fn'].rsplit('.', 1)
        final = final[0] + '_st.' + final[1]
    fsl = fsl[:-2]

    fa = list()
    minx = miny = None
    print pif.render.format_table_start()
    input_files = list()
    for fs in fsl:
        print pif.render.format_row_start()
        img = fs['fn']
        input_files.append(img)
        crop_l = int(fs['x1'])
        crop_r = int(fs['x2'])
        crop_t = int(fs['y1'])
        crop_b = int(fs['y2'])
        x, y = get_size(img)
        fa.append((img, x, y, crop_l, crop_t, crop_r, crop_b))
        cx = crop_r - crop_l
        cy = crop_b - crop_t
        if not minx or cx < minx:
            minx = cx
        if not miny or cy < miny:
            miny = cy
        #print fa[-1], '<br>'
        print pif.render.format_cell(1, str(fs['fn']))
        print pif.render.format_cell(1, str(fs['x1']), also={'width': 40})
        print pif.render.format_cell(1, str(fs['y1']), also={'width': 40})
        print pif.render.format_cell(1, str(fs['x2']), also={'width': 40})
        print pif.render.format_cell(1, str(fs['y2']), also={'width': 40})
        print pif.render.format_row_end()

    print pif.render.format_table_end()
    print 'Stitching...', final
    limit_x = int(pif.form_int('limit_x', 0))
    limit_y = int(pif.form_int('limit_y', 0))
    if pif.form_str('or') == 'h':
        print 'horizontal'
        stitch_h(final, fa, miny, limit_x, limit_y, verbose)
    else:
        print 'vertical'
        stitch_v(final, fa, minx, limit_x, limit_y, verbose)
    time.sleep(2)
    print '... Finished.<br>'
    sys.stdout.flush()
    #print '<a href="../' + final + '">' + final + '<br>'
    #print '<img src="../' + final + '"></a>'
    d, f = os.path.split(final)
    show(pif, d, f)
    orig = input_files[0][input_files[0].rfind('/') + 1:]
    print '<br><form>Final resting place:'
    print pif.render.format_text_input('o', 80, value='%s' % input_files[0])
    print pif.render.format_hidden_input({'f': '%s/%s' % (d, f)})
    for fn in input_files:
        print pif.render.format_hidden_input({'in': fn})
    print pif.render.format_button_input('finish')
    print '</form>'


def stitch_finish(pif, verbose=False):
    print pif.form, '<hr>'

    for fn in pif.form_list('in'):
        useful.file_mover(fn, os.path.join(config.LIB_DIR, 'trash', fn[fn.rfind('/') + 1:]), mv=True, inc=True, trash=False)
    useful.file_mover(pif.form_str('f'), pif.form_str('o'), mv=True, ov=True)


@basics.web_page
def stitch_main(pif, verbose=False):
    pif.render.print_html()

    pif.render.title = 'stitch'
    print pif.render.format_head(extra=def_edit_js)

    if pif.form_has('finish'):
        stitch_finish(pif, verbose)
    elif pif.form_has('finalize'):
        stitch_finalize(pif, verbose)
    else:
        stitch_input(pif, verbose)

    print pif.render.format_tail()


def stitch_input(pif, verbose=False):
    file_count = pif.form_int('fc')
    fsl = stitch_read_form(pif, verbose)
    print fsl, '<br>'

    print '''<form action="stitch.cgi" name="myForm" onSubmit="return getValueFromApplet()">'''
    print pif.render.format_hidden_input({'fc': file_count + 1})
    print pif.render.format_table_start()
    min_x = pif.form_int('limit_x', 999999)
    min_y = pif.form_int('limit_y', 999999)
    for fs in fsl:
        print pif.render.format_row_start()
        num = fs['n']
        fn = fs.get('fn', '').strip()
        fn_size = ''
        if fn:
            if 'x1' not in fs and os.path.exists(fn):
                x, y = get_size(fn)
                min_x = min(x, min_x)
                min_y = min(y, min_y)
                fn_size = '<br>' + str((x, y))
            print pif.render.format_cell(1, fn + fn_size)
            print pif.render.format_hidden_input({'fn_' + num: fn})
        else:
            print pif.render.format_cell(1, pif.render.format_text_input('fn_%d' % file_count, 80) + '<br>' + fsl[0]['fn'].strip())
            print pif.render.format_cell(1, pif.render.format_button_input() + ' ' +
                pif.render.format_button_input('finalize') + '<br>' +
                pif.render.format_checkbox('or', [('h', 'horizontal')]),
                    also={'colspan': 2})
            print pif.render.format_cell(1, 'x ' + pif.render.format_text_input('limit_x', 5, value=min_x))
            print pif.render.format_cell(1, 'y ' + pif.render.format_text_input('limit_y', 5, value=min_y))
        if 'x1' in fs:
            print pif.render.format_cell(1, str(fs['x1']), also={'width': 40})
            print pif.render.format_hidden_input({'x1_' + num: fs['x1']})
            print pif.render.format_cell(1, str(fs['y1']), also={'width': 40})
            print pif.render.format_hidden_input({'y1_' + num: fs['y1']})
            print pif.render.format_cell(1, str(fs['x2']), also={'width': 40})
            print pif.render.format_hidden_input({'x2_' + num: fs['x2']})
            print pif.render.format_cell(1, str(fs['y2']), also={'width': 40})
            print pif.render.format_hidden_input({'y2_' + num: fs['y2']})
        elif fn:
            if not os.path.exists(fn):
                print pif.render.format_cell(1, 'Nonexistant: ' + os.getcwd() + '/' + fn, also={'colspan': 4})
            else:
                print pif.render.format_cell(1, show_widget(pif, fn), also={'colspan': 4})
        print pif.render.format_row_end()
    print pif.render.format_table_end()
    print '<input type="hidden" value="" name="q">'  # for imawidget
    print '</form>'


def casting_pictures(pif, mod_id, direc):
    fl = glob.glob('%s/%s*.*' % (direc, mod_id)) + glob.glob('%s/?_%s*.*' % (direc, mod_id))
    fl.sort()
    if fl:
        print '<h3>%s</h3>' % direc
        if direc == config.IMG_DIR_ADD:
            print pif.render.format_button('describe', pif.dbh.get_editor_link('attribute_picture', {'mod_id': mod_id})) + '<br>'
        for fn in fl:
            print '<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s&man=%s"><img src="../%s">%s</a> ' % (direc, fn[fn.rfind('/') + 1:], mod_id, fn, fn)
            print '<br>'
        print '<hr>'



def lineup_pictures(pif, lup_models):
    print '<h3>Lineup Models</h3>'
    lup_models.sort(key=lambda x: x['lineup_model.year'])
    for mod in lup_models:
        if mod['section.img_format']:
            mod['filename'] = mod['section.img_format'] % mod['lineup_model.number'] + '.jpg'
            mod['filepath'] = mod['page_info.pic_dir'] + '/' + mod['filename']
            if os.path.exists(mod['filepath']):
                print '<a href="/cgi-bin/imawidget.cgi?d=%(page_info.pic_dir)s&f=%(filename)s&man=%(lineup_model.mod_id)s"><img src="../%(filepath)s">%(filepath)s</a><br>' % mod
    print '<hr>'


@basics.web_page
def pictures_main(pif):
    pif.render.print_html()
    pif.render.title = 'pictures - ' + pif.form_str('m', '')
    print pif.render.format_head()
    mod_id = pif.form_str('m', '')
    if mod_id:
        [casting_pictures(pif, mod_id.lower(), x) for x in [config.IMG_DIR_MAN, config.IMG_DIR_VAR, 'pic/man/icon', config.IMG_DIR_ADD]]
        lineup_pictures(pif, pif.dbh.fetch_casting_lineups(mod_id))
    else:
        print 'Huh?'
    print pif.render.format_tail()


# -- icon

# & ' + - .  /

def create_icon(fn, name, logo, isizex=100, isizey=100):
    print ' ', fn, '|'.join(name)

    fil = 'pic/man/s_' + fn + '.jpg'
    if not os.path.exists(fil):
        print 'no original file'
        return

    thumb = Image.open(fil)
    if thumb.size[1] != 120:
        print 'bad original size', thumb.size
        return
    thumb = thumb.resize((isizex, isizex * thumb.size[1] / thumb.size[0]), Image.NEAREST)
    banner = Image.open(logo)

    text = imicon.Icon(isizex, isizey)
    top = banner.size[1] + thumb.size[1]
    texttop = top + (isizey - top - 6 * len(name) + 1) / 2
    for n in name:
        if len(n) > isizex / 6:
            text.charset("3x5.font")
            left = 50 - len(n) * 2
        else:
            text.charset("5x5.font")
            left = 50 - len(n) * 3
        text.string(left, texttop, n.upper())
        texttop = texttop + 6
    iconimage = text.getimage()

    iconimage.paste(banner, ((isizex - banner.size[0]) / 2, 0))
    iconimage.paste(thumb, ((isizex - thumb.size[0]) / 2, banner.size[1]))

    # write out as png and job off the final conversion to netpbm.
    # doing this because I don't like how PIL disses GIFs.
    iconimage.save('pic/man/icon/' + fn + '.png')
    print "pngtopnm " + 'pic/man/icon/' + fn + ".png | pnmquant 256 | ppmtogif > " + 'pic/man/icon/i_' + fn + ".gif"
    os.system("pngtopnm " + 'pic/man/icon/' + fn + ".png | pnmquant 256 | ppmtogif > " + 'pic/man/icon/i_' + fn + ".gif")
    os.unlink('pic/man/icon/' + fn + '.png')
    print "Written to", 'pic/man/icon/i_' + fn + ".gif"


def mangle_name(name):
    if name[0] == '(':
        name = name[name.find(')') + 2:]
    if '(' in name:
        name = name[:name.find('(') - 1] + name[name.find(')') + 1:]
    if name[0] == '-':
        name = name[1:]
    names = list()
    for n in name.split(';'):
        if n[-1] == '/':
            n = n[:-1]
        names.append(n.strip().replace('*', ''))
    return names


def get_man_list(pif):
    manlist = pif.dbh.fetch_casting_list()
    mans = dict()
    for llist in manlist:
        llist = pif.dbh.modify_man_item(llist)
        mans[llist['id'].lower()] = llist
    return mans


@basics.command_line
def icon_main(pif):

    title = 'mb2'
    if pif.switch['b']:
        title = pif.switch['b'][-1]

    logo = pif.render.find_art(title)

    #manlist = filter(lambda x: x[0] == 'm', [x.strip().split('|') for x in open('../../src/man.dat').readlines()])
    #mandict = {x[1].strip().lower(): mangle_name(x[6])) for x in manlist}

    mandict = get_man_list(pif)

    if pif.switch['a']:
        for man in mandict:
            name = mangle_name(mandict[man]['rawname'])
            if pif.switch['n']:
                name = pif.switch['n'][-1].split(';')
            create_icon(man, name, logo)
    elif pif.filelist:
        for man in pif.filelist:
            if man in mandict:
                name = mangle_name(mandict[man]['rawname'])
                if pif.switch['n']:
                    name = pif.switch['n'][-1].split(';')
                create_icon(man, name, logo)
    else:
        print 'huh?'  # print mandict


def image_star(pif, image_path, pic_id='', halfstar=False):
    if pic_id is None:
        return pif.render.format_image_art('stargray.gif')
    if not os.path.exists(image_path):
        if pic_id:
            return pif.render.format_image_art('staryellow.gif')
        return pif.render.format_image_art('starwhite.gif')
        return '&nbsp;'  # pif.render.format_image_art('stargray.gif')
    try:
        img = Image.open(image_path)
    except:
        return pif.render.format_image_art('staryellow.gif')
        return ''
    ix, iy = img.size

    if ix < 200:
        return pif.render.format_image_art('starred.gif')
    if ix < 400:
        return pif.render.format_image_art('stargreen.gif')
    if ix > 400:
        return pif.render.format_image_art('starblue.gif')
    if halfstar:
        return pif.render.format_image_art('starhalf.gif')
    return pif.render.format_image_art('star.gif')

# -- bits

@basics.web_page
def bits_main(pif):
    years = {
        '1998': {'d': config.IMG_DIR_MT_LAUREL, 'p': '1998', 'r': 'ur'},
        '1999': {'d': config.IMG_DIR_MT_LAUREL, 'p': '1999', 'r': 'urd'},
        '2000': {'d': config.IMG_DIR_MT_LAUREL, 'p': '2000', 'r': 'urdab'},
        '2002': {'d': config.IMG_DIR_MT_LAUREL, 'p': '2002', 'r': 'ur'},
        '2003': {'d': config.IMG_DIR_MT_LAUREL, 'p': '2003', 'r': 'ur'},
        '2004': {'d': config.IMG_DIR_MT_LAUREL, 'p': '2004', 'r': 'ur'},
        '2008': {'d': config.IMG_DIR_MATTEL, 'p': '2008', 'r': 'u'},
        '2009': {'d': config.IMG_DIR_MATTEL, 'p': '2009', 'r': 'u'},
    }

    colors = {True: "#CCCCCC", False: "#FFFFFF"}

    pif.render.print_html()

    print "<table>"

    yearlist = years.keys()
    yearlist.sort()

    c = False
    print "<tr>"
    print "<th></th>"
    for y in yearlist:
        print '<th bgcolor="%s" colspan=%d>%s</th>' % (colors[c], len(years[y]['r']), y)
        c = not c
    print "</tr>"

    c = False
    print "<tr>"
    print "<th></th>"
    for y in yearlist:
        for r in years[y]['r']:
            print '<th bgcolor="%s">%s</th>' % (colors[c], r.upper())
        c = not c
    print "</tr>"

    for a in range(1, 21):

        c = False
        print "<tr>"
        print '<th bgcolor="%s">%d</th>' % (colors[True], a)

        for y in yearlist:
            for r in years[y]['r']:

                fmt = "%s/%s%ss%02d.gif"
                f = fmt % (years[y]['d'], years[y]['p'], r, a)

                cstr = '<th bgcolor="%s">' % (colors[c])
                if os.path.exists("../htdocs/"+f):
                    cstr += '<img src="%s">' % ("../" + f)
                else:
                    cstr += "&nbsp;"
                print cstr + '</th>'
            c = not c
        print "</tr>"
    print "</table>"


# -- library

def show_library_list(pif, title, tdir, fl):
    cols = pif.form_int("c", 5)
    if not fl:
        return
    clen = (len(fl) - 1) / cols + 1
    ffl = [fl[(x*clen):((x+1)*clen)] for x in range(0, cols)]
    print '<h4>%s (%d)</h4>' % (title, len(fl))
    print "<table width=100%><tr valign=top>"
    for cl in ffl:
        print "<td width=%d%%>" % (100/cols)
        for f in cl:
            root, ext = useful.root_ext(f.strip())
            fst = os.stat(tdir + '/' + f)
            perms = fst[stat.ST_MODE]
            if f[0] == '.':
                print '<i>%s</i><br>' % f
            elif stat.S_ISDIR(perms):
                print '<a href="/cgi-bin/traverse.cgi?d=%s">%s</a><br>' % (tdir + '/' + f, f)
            elif f[-4:] == '.dat':
                #print '<a href="/cgi-bin/table.cgi?page=%s">%s</a><br>' % (tdir + '/' + f, f)
                print '<a href="/cgi-bin/traverse.cgi?d=%s&f=%s">%s</a><br>' % (tdir, f, f)
            elif (perms & 5) == 0:
                print '%s<br>' % f
            elif ext in itypes:
                #print '<a href="/cgi-bin/traverse.cgi?d=%s&f=%s">%s</a><br>' % (tdir, f, f)
                print '<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s">%s</a><br>' % (tdir, f, f)
            else:
                print '<a href="../%s">%s</a><br>' % (tdir + '/' + f, f)
        print "</td>"
    print "</tr></table>"
    print '<br><hr>'


def show_library_graf(title, tdir, fl):
    if not fl:
        return

    print '<h4>%s (%d)</h4>' % (title, len(fl))
    fd = {}
    for f in fl:
        root, ext = useful.root_ext(f)
        if root[-2] == '_' and root[-1] in mbdata.image_size_names:
            root = root[:-2]
        fd.setdefault(root, [])
        fd[root].append(f)

    keys = fd.keys()
    keys.sort()
    print '<table>'
    for root in keys:
        fd[root].sort()
        print '<tr><td>%s</td><td><img src="thumber.cgi?d=%s&f=%s"></td><td>' % (root, tdir, fd[root][0])
        for f in fd[root]:
            perms = os.stat(tdir + '/' + f)[stat.ST_MODE]
            if (perms & 4) == 0:
                print '%s<br>' % f
            else:
                #print '<a href="/cgi-bin/traverse.cgi?d=%s&f=%s"><img src="../%s" border=0>%s</a><br>' % (tdir, f, tdir + '/' + f, f)
                print '<a href="imawidget.cgi?d=%s&f=%s&cy=0">%s' % (tdir, f, f)
        print '</td></tr>'
        sys.stdout.flush()
    print '</table>'
    print '<br><hr>'


def show_library_dir(pif, tdir, grafs=0):
    print '<hr>'

    dl, gl, ol, sl, xl = get_dir(tdir)

    show_library_list(pif, "Directories", tdir, dl)
    if grafs:
        show_library_graf("Graphics", tdir, gl)
    else:
        show_library_list(pif, "Graphics", tdir, gl)
    show_library_list(pif, "Data Files", tdir, sl)
    show_library_list(pif, "Executable Files", tdir, xl)
    show_library_list(pif, "Other Files", tdir, ol)

    if gl:
        print '<form action="traverse.cgi">'
        print '<a href="traverse.cgi?g=1&d=%s">%s</a> or ' % (tdir, pif.render.format_button('show all pictures'))
        print 'Pattern <input type="text" name="p">'
        print '<input type="hidden" name="d" value="%s">' % tdir
        print pif.render.format_button_input()
        print '</form>'

    print '<a href="upload.cgi?d=%s&m=%s">%s</a>' % (tdir, tdir[7:], pif.render.format_button('upload'))



imginputs = '''<input type="checkbox" name="rm" value="%(f)s"> rm<input type="checkbox" name="mv" value="%(f)s %(b)s"> mv'''
imginput = '''<input type="checkbox" name="rm" value="%(f)s"> rm
<input type="text" name="ren.%(f)s"> rename
'''
def library_img(args, base=''):
    print '<tr>'
    args.sort()
    for arg in args:
        root, ext = useful.root_ext(arg.strip())
        inp = ''
        if arg == base:
            inp = imginputs % {'f': arg, 'b': root + 'z.' + ext}
        elif base:
            inp = imginputs % {'f': arg, 'b': base}
        else:
            inp = imginput % {'f': arg}
        #inp += ' <a href="imawidget.cgi?d=%s&f=%s&cy=0">' % (pif.render.pic_dir, arg) + pif.render.format_button('edit') + '</a>'
        inp += ' ' + pif.render.format_button('edit', 'imawidget.cgi?d=%s&f=%s&cy=0' % (pif.render.pic_dir, arg))
        inp += ' ' + pif.render.format_button('stitch', 'stitch.cgi?fn_0=%s&submit=1&q=&fc=1' % (pif.render.pic_dir + '/' + arg))
        print pif.render.format_cell(0, '<a href="../%s/%s">%s</a><br>%s%s' % (pif.render.pic_dir, arg, pif.render.format_image_required([root], suffix=ext, also={"border": 0}), arg, inp))
    print '</tr>'


def show_library_imgs(pif, patt):
    print '<hr>'
    print '<form action="traverse.cgi" method="post">'
    plist = patt.split(',')
    for pent in plist:
        flist = useful.read_dir(pent, pif.render.pic_dir)
        flist.sort()
        print '<table>'
        for f in flist:
            library_img([f])
        print '</table>'
        print '<hr>'
    print '<input type="hidden" name="d" value="%s">' % pif.render.pic_dir
    print '<input type="hidden" name="sc" value="1">'
    print pif.render.format_button_input()
    print '<a href="upload.cgi?d=%s&r=1">%s</a>' % (pif.form_str('d', '.'), pif.render.format_button('upload'))
    print '</form>'


def show_library_file(pif, fn):
    if fn.endswith('.dat'):
        show_library_table(pif, fn)
    else:
        show_picture(pif, fn)



colors = ["#FFFFFF", "#CCCCCC"]


class LibraryTableFile(bfiles.ArgFile):
    def __init__(self, fname):
        self.dblist = []
        bfiles.ArgFile.__init__(self, fname)

    def parse_else(self, llist):
        self.dblist.append(llist)



#print '<a href="/cgi-bin/table.cgi?page=%s">%s</a><br>' % (tdir + '/' + f, f)
def show_library_table(pif, pagename):
    tablefile = LibraryTableFile(pif.render.pic_dir + '/' + pagename)
    cols = ''  # pif.form_str('cols', '')
    h = 0  # pif.form_int('h')
    sorty = pif.form_str('sort')

    print pif.render.format_table_start()
    hdr = ''
    if h:
        hdr = tablefile.dblist[0]
        table = tablefile.dblist[1:]
    else:
        table = tablefile.dblist

    if sorty:
        global sortfield
        sortfield = int(sorty)
        table.sort(key=lambda x: x[sortfield].lower())

    row = 0
    icol = irow = 0
    if 'y' in cols:
        icol = cols.find('y')
    id = ''
    for line in table:
        if line[icol] != id:
            id = line[icol]
            irow = (irow + 1) % 2
        if not row:
            row = h
            iarg = 0
            print '<tr>'
            for ent in range(0, len(hdr)):
                if ent >= len(cols) or cols[ent].lower() != 'n':
                    #print "<th>"+hdr[ent]+"</th>"
                    print '<th bgcolor="#FFFFCC"><a href="table.cgi?page=%s&sort=%d&h=%d&cols=%s">%s</th>' % (pagename, iarg, h, cols, hdr[ent])
                iarg = iarg + 1
            print "</tr>\n<tr>"
        print '<tr bgcolor="%s">' % colors[irow]
        row = row - 1
        for ent in range(0, len(line)):
            if ent >= len(cols) or cols[ent].lower() != 'n':
                print "<td>" + line[ent] + "</td>"
        print "</tr>"
    print pif.render.format_table_end()


def do_library_action(pif, tdir, fn, act):
    print '<div class="warning">'
    nfn = action(pif, tdir, fn, act)
    print '</div><br>'
    if nfn:
        ShowLibraryPicture(pif, nfn)
    else:
        ShowLibraryLibraryDir(pif, tdir, 0)


@basics.web_page
def library_main(pif):
    os.environ['PATH'] += ':/usr/local/bin'
    pif.render.print_html()
    pif.restrict('a')
    #pif.render.title = '<a href="traverse.cgi?d=%s">%s</a>' % (pif.form_str("d", '.'), pif.form_str("d", '.'))
    pif.render.title = pif.render.pic_dir = pif.form_str("d", '.')
    pif.render.title += '/' + pif.form_str("f", "")
    graf = pif.form_int("g")
    fnam = pif.form_str("f", '')
    patt = pif.form_str("p", '')
    cols = pif.form_int("c", 5)
    act = pif.form_int('act')
    cycle = pif.form_int("cy")

    print pif.render.format_head(extra=pif.render.increment_js)
    print pif.form
    if patt:
        show_library_imgs(pif, patt)
    elif act:
        do_library_action(pif, pif.render.pic_dir, fnam, act)
    elif fnam:
        show_library_file(pif, fnam)
    else:
        show_library_dir(pif, pif.render.pic_dir, graf)
    print pif.render.format_tail()


# -- image

@basics.web_page
def show_image(pif):
    print 'Content-Type: image/jpeg\n'
    print open(os.path.join(pif.form_str('d', '.'), pif.form_str('f', '')), "rb").read()


# -- thumber

@basics.web_page
def thumber(pif):
    os.environ['PATH'] += ':/usr/local/bin'

    #pif.restrict('a')

    print 'Content-Type: image/gif'
    print

    dir = pif.form_str('d', '.')
    fil = pif.form_str('f', '')
    pth = os.path.join(dir, fil)

    x = 100
    outf = pipe_chain(open(pth),
            import_file(pth) +
            [["/usr/local/bin/pamscale", "-xsize", str(x)]] +
            export_file('tmp.gif'), stderr=open('/dev/null', 'w'), verbose=False)

    print outf


if __name__ == '__main__':  # pragma: no cover
    icon_main('editor', switches='av', options='bn')
