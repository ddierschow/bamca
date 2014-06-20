#!/usr/local/bin/python

import datetime, filecmp, glob, os, re, stat, subprocess, sys, time, traceback, urllib, urllib2
import cmdline
import config
import icon
import javascript
import mbdata
import useful
import Image

#os.environ['PATH'] += ':/usr/local/bin'


'''  API
images.Action
images.ExportFile
images.GetDir
images.GetSize
images.ImaWidget
images.ImportFile
images.PipeChain
images.ShowPicture
images.UploadMain
images.cycle
images.def_edit_app
images.def_edit_js
images.image_inputters
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

xts = 180
yts = 125

cycle = 0

image_inputters = {
    'bmp' : [['/usr/local/bin/bmptopnm']],
    'gif' : [['/usr/local/bin/giftopnm']],
    'ico' : [['/usr/local/bin/winicontoppm']],
    'jpg' : [['/usr/local/bin/jpegtopnm']],
    'jpeg' : [['/usr/local/bin/jpegtopnm']],
    'png' : [['/usr/local/bin/pngtopnm']],
    'tif' : [['/usr/local/bin/tifftopnm']],
    'xbm' : [['/usr/local/bin/xbmtopbm']],
#    '' : [['/usr/local/bin/jpegtopnm']],
}

image_outputters = {
    'bmp' : [['/usr/local/bin/ppmtobmp']],
    'gif' : [['/usr/local/bin/pnmquant', '256'], ['/usr/local/bin/ppmtogif']],
    'ico' : [['/usr/local/bin/ppmtowinicon']],
    'jpg' : [['/usr/local/bin/pnmtojpeg']],
    'jpeg' : [['/usr/local/bin/pnmtojpeg']],
    'png' : [['/usr/local/bin/pnmtopng']],
    '' : [['/usr/local/bin/pnmtojpeg']],
}
otypes = ['', 'bmp', 'gif', 'ico', 'jpg', 'png']

def ImportFile(fn):
    fn = fn[fn.rfind('/') + 1:]
    fex = fn[fn.rfind('.') + 1:]
    if '?' in fex:
	fex = fex[:fex.find('?')]
    return image_inputters[fex]

def ExportFile(nfn, ofn=''):
    nfn = nfn[nfn.rfind('/') + 1:]
    if '.' in nfn:
	fex = nfn[nfn.rfind('.') + 1:]
    else:
	ofn = ofn[ofn.rfind('/') + 1:]
	fex = ofn[ofn.rfind('.') + 1:]
    return image_outputters[fex]

# -- upload

def GetDir(tdir):
    fl = os.listdir(tdir)
    fl.sort()
    dl = list() # directories
    gl = list() # graphics
    ol = list() # other files
    sl = list() # dat files
    xl = list() # executables

    for f in fl:
	root,ext = useful.RootExt(f)
	if os.path.exists(tdir + '/' + f):
	    if f[-1] == '~' or f == '.crcs' or f[-4:] == '.pyc':
		continue
	    perms = os.stat(tdir + '/' + f)[stat.ST_MODE]
	    if stat.S_ISDIR(perms):
		dl.append(f)
	    elif ext == 'dat':
		sl.append(f)
	    elif ext in image_inputters:
		gl.append(f)
	    elif stat.S_IMODE(perms) & stat.S_IXUSR:
		xl.append(f)
	    else:
		ol.append(f)
    return dl, gl, ol, sl, xl


def Filename(man, var='', ext='.jpg'):
    pth = 'lib/' + man.lower()
    if var:
	fn = (man + '-' + var).lower()
    else:
	fn = man.lower()
    if os.path.exists(pth + '/' + fn + ext):
	i = 1
	while os.path.exists(pth + '/' + fn + '-' + str(i) + ext):
	    i = i + 1
	fn = fn + '-' + str(i)
    return pth, fn + ext


def UploadPic(pif, infile, pdir, fn, overwrite=False, desc=''):
    UploadFile(pif, infile, pdir, fn, overwrite)
    Show(pif, pdir, fn)


def UploadFile(pif, infile, pdir, fn, overwrite=False, desc=''):
    fn = SafeSave(pif, pdir, fn, infile, overwrite)
    if fn.endswith('.') or not '.' in fn:
	fn = FixFileType(pif, pdir, fn)


def ScrapeURLMod(pif, url, man, var, overwrite=False, desc=''):
    pdir = pif.form.get('d', 'lib/' + man)
    fn = url[url.rfind('/') + 1:].lower()
    ScrapeURLPic(pif, url, pdir, fn, overwrite, desc=desc)


scrape_re = re.compile(r'''<img src="(?P<img>[^"]*)"''', re.I)
def ScrapeURLPic(pif, url, pdir, fn, overwrite=False, desc=''):
    print '<br>', url, ':', pdir, ':', fn, '<br>'
    try:
	up = urllib2.urlopen(url).read()
    except:
	pif.ShowError()
	return
    url = url[:url.rfind('/') + 1]
    imgs = scrape_re.findall(up)
    sfn = ''
    for img in imgs:
	fn = img[img.rfind('/') + 1:]
	print img, pdir, fn, '<br>'
	if not img.startswith('http://'):
	    img = url + '/' + img
	sfn = GrabURLFile(pif, img, pdir, fn, overwrite)

	pif.render.pic_dir = pdir
	print '<center><h3>Added: ' + sfn + '</h3><p>'
	print '<img src="../%s/%s"></center>' % (pdir, sfn)
    #Picker(pif, sfn)


def FixFileType(pif, pdir, fn):
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


def SafeSave(pif, pdir, fn, contents, overwrite=False):
    if not os.path.exists(pdir):
	os.mkdir(pdir, 0775)
    if '.' in fn:
	root, ext = fn.rsplit('.', 1)
    else:
	root = fn
	ext = ''
    ext = ext.lower()
    root = useful.CleanName(root, '!@$%^&*()[]{}~`<>"+')
    fn = root + '.' + ext
    if os.path.exists(pdir + '/' + fn):
	if overwrite:
	    #os.unlink(pdir + '/' + fn)
	    useful.FileMover(pdir + '/' + fn, 'lib/trash/' + fn, mv=True, inc=True, trash=True)
	else:
	    addon = 1
	    while os.path.exists(pdir + '/' + root + '_' + str(addon) + '.' + ext):
		addon += 1
	    root += '_' + str(addon)
    fn = root + '.' + ext
    open(pdir + '/' + fn, 'w').write(contents)
    Log(pif, pdir + '/' + fn, pdir)
    return fn


def GrabURLMod(pif, url, man, var, overwrite=False, desc=''):
    pdir = pif.form.get('d', 'lib/' + man)
    fn = url[url.rfind('/') + 1:].lower()
    GrabURLPic(pif, url, pdir, fn, var, overwrite, desc=desc)


def GrabURLPic(pif, url, pdir, fn, var=None, overwrite=False, track=False, desc=''):
    fn = GrabURLFile(pif, url, pdir, fn, var, overwrite)
#    if var:
#	print '''<meta http-equiv="REFRESH" content="0;url=/cgi-bin/imawidget.cgi?d=%s&f=%s&cy=%d&v=%s">''' % (pdir, fn, 0, var)
#    else:
#	print '''<meta http-equiv="REFRESH" content="0;url=/cgi-bin/imawidget.cgi?d=%s&f=%s&cy=%d">''' % (pdir, fn, 0)
    pif.render.pic_dir = pdir
    Picker(pif, fn)
    if track:
	pif.dbh.InsertActivity(fn, pif.id, description=desc, image=pdir + '/' + fn)
    print '<hr>'
    ShowEditor(pif, pif.render.pic_dir, fn)


def GrabURLFile(pif, url, pdir, fn, var=None, overwrite=False, desc=''):
    open('tb/upload.log', 'a').write(datetime.datetime.now().strftime('%Y%m%d.%H%M%S') + ' %s %s\n' % (url, pdir))
    try:
	up = urllib2.urlopen(url).read()
    except:
	pif.ShowError()
	return "Error encountered!  File not uploaded."
    if not fn:
	fn = url[url.rfind('/') + 1:].lower()
    elif not '.' in fn:
	fn += url[url.rfind('.'):].lower()
    fn = SafeSave(pif, pdir, fn, up, overwrite)
    return fn


def UploadMod(pif, infile, man, var, overwrite=False, desc=''):
    pdir, fn = Filename(man, var)
    fn = SafeSave(pif, pdir, fn, infile, overwrite)
    Show(pif, pdir, fn)


def SelectFromLibrary(pif, man, var, desc=''):
    nfn = man.lower()
    if var:
	nfn = nfn + '-' + var
    tdir = 'lib/' + man.lower()
    grafs = True
    os.chdir(tdir)

    gl = filter(lambda f: not stat.S_ISDIR(os.stat(f)[stat.ST_MODE]) and useful.RootExt(f)[1] in image_inputters, os.listdir('.'))
    gl.sort()

    if gl:
	for f in gl:
	    r,e = useful.RootExt(f)
	    perms = os.stat(f)[stat.ST_MODE]
	    if (perms & 4) == 0:
		print '%s<br>' % f
	    else:
		#print '<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s&newname=%s.%s&v=%s">' % (tdir, f, nfn, e, var)
		print '<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s&v=%s&c=%s">' % (tdir, f, var, urllib.quote_plus(desc))
		print '<img src="../%s" border=0>%s</a><br>' % (tdir + '/' + f, f)
	print '<br><hr>'


def Show(pif, pdir, fn):
    pif.render.pic_dir = pdir
    ShowPicture(pif, fn)
    #print '<center><h3>' + fn + '</h3><p>'
    #print '<img src="../%s/%s"></center>' % (pdir, fn)
    #Picker(pif, fn)

def ShowPicture(pif, fn):
    Picker(pif, fn)
    root,ext = useful.RootExt(fn.strip())
    pif.render.Comment(root, ext)
    print '<table><tr><td></td><td>' + pif.render.FormatImageArt('hruler.gif') + '</td></tr>'
    print '<tr><td valign="top">' + pif.render.FormatImageArt('vruler.gif') + '</td><td valign="top">'
    print '<a href="../' + pif.render.pic_dir + '/' + fn + '">' + pif.render.FormatImageRequired([root], suffix=ext, also={"border":"0"}) + '</a>'
    print '</td></tr></table>'


def Log(pif, fn, tdir):
    file("src/file.log", "a").write('|'.join([fn, tdir, str(pif.id)]) + '\n')


def GetMan(pif):
    #print 'GetMan man', pif.form.get('man'), 'pic_dir', pif.render.pic_dir, '<br>'
    man = pif.form.get("man")
    if man:
	#print 'form', man, '<br>'
	return man
    pdir = pif.render.pic_dir
    if pdir.startswith('./'):
	pdir = pdir[2:]
    if pdir.endswith('/'):
	pdir = pdir[:-1]
    if pdir.startswith("lib"):
	#print 'lib', pdir[pdir.rfind('/') + 1:], '<br>'
	return pdir[pdir.rfind('/') + 1:]
    if pdir.startswith("pic/packs"):
	if pif.form.get('f'):
	    if len(pif.form['f']) > 2 and pif.form['f'][1] == '_':
		#print 'pack1', pif.form.get('f')[2:-4], '<br>'
		return pif.form.get('f')[2:-4]
	    else:
		#print 'pack2', pif.form.get('f')[:-4], '<br>'
		return pif.form.get('f')[:-4]
    if pdir.startswith("pic/cat"):
	if pif.form.get('f'):
	    if len(pif.form['f']) > 2 and pif.form['f'][1] == '_':
		man = pif.form.get('f')[2:-4]
	    else:
		man = pif.form.get('f')[:-4]
	    if '_' in man:
		man = man[:man.find('_')]
	    #print 'cat', man, '<br>'
	    return man
    #print 'nope', '<br>'
    return ""

sel_cat = [
    ['unsorted',	'unsorted'],
    ['a',	'Accessories'],
    ['bigmx',	'BigMX'],
    ['blister',	'Blister'],
    ['cc',	'Carrying Case'],
    ['cat',	'Catalogs'],
    ['coll',	'Collectibles'],
    ['commando',	'Commando'],
    ['cy',	'Convoys'],
    ['copies',	'Copies'],
    ['disp',	'Displays'],
    ['e',	'Early'],
    ['game',	'Games'],
    ['g',	'Giftsets'],
    ['gw',	'Giftware'],
    ['gf',	'Graffic'],
    ['k',	'Kings'],
    ['moko',	'Moko'],
    ['mw',	'Motorways'],
    ['mult',	'Multiples'],
    ['o',	'Other'],
    ['packs',	'Packs'],
    ['ps',	'Play Sets'],
    ['prem',	'Premieres'],
    ['rt',	'Real Talkin'],
    ['rb',	'Roadblasters'],
    ['r',	'Roadway'],
    ['robotech',	'RoboTech'],
    ['sb',	'Sky Busters'],
    ['supergt',	'SuperGT'],
    ['tp',	'TwinPacks'],
    ['wr',	'White Rose'],
    ['zing',	'Zings'],
]

adds = 'abdeipr'
sel_pref = [
    ['',	''],
    ['t',	'thumbnail'],
    ['s',	'small'],
    ['c',	'compact'],
    ['m',	'medium'],
    ['l',	'large'],
    ['h',	'huge'],
    ['g',	'gigantic'],
    ['b',	'baseplate'],
    ['a',	'custom'],
    ['d',	'detail'],
    ['e',	'error'],
    ['i',	'interior'],
    ['p',	'prototype'],
    ['r',	'real'],
    ['z',	'comparison'],
]

sel_moveto = [
    ['',        ''],
    [config.imgdirMattel,       'mattel'],
    [config.imgdirMtLaurel,     'mtlaurel'],
    [config.imgdirTyco,         'tyco'],
    [config.imgdirUniv,         'univ'],
    [config.imgdirLSF,          'lsf'],
    [config.imgdirLRW,          'lrw'],
    [config.imgdirLesney,       'lesney'],
    [config.imgdirAcc,          'acc'],
    [config.imgdirAds,          'ads'],
    [config.imgdirBlister,      'blister'],
    [config.imgdirBox,          'box'],
    [config.imgdirColl43,       'mcoll'],
    [config.imgdirErrors,       'errors'],
    [config.imgdirKing,         'king'],
    [config.imgdirPack,         'packs'],
    [config.imgdirColl64,       'prem'],
    [config.imgdirSeries,       'series'],
    [config.imgdirSky,          'sky'],
]

def Picker(pif, fn):
    global cycle
    cycle = pif.FormInt('cy')
    root,ext = useful.RootExt(fn.strip())
    print '<a href="?d=%s">%s</a> / ' % (pif.render.pic_dir, pif.render.pic_dir)
    print '<a href="/%s/%s">%s</a>' % (pif.render.pic_dir, fn, fn)
    szname = ''
    if os.path.exists(pif.render.pic_dir + '/' + fn):
	x,y = GetSize(pif.render.pic_dir + '/' + fn)
	print (x,y)
	for (szname, szxy) in zip(mbdata.image_size_names, mbdata.image_size_sizes):
	    if x <= szxy[0]:
		break
    print '<hr>'
    print '<form action="upload.cgi">'
    print '<input type=hidden name="act" value="1">'
    print '<input type=hidden name="d" value="%s">' % pif.render.pic_dir
    print '<input type=hidden name="f" value="%s">' % fn
    print '<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s&v=%s&cy=%d">%s</a>' % (pif.render.pic_dir, fn, pif.form.get('v', ''), cycle, pif.render.FormatButton('edit'))
    print pif.render.FormatButtonInput('delete')
    print pif.render.FormatButton('stitch', 'stitch.cgi?fn_0=%s&submit=1&q=&fc=1' % (pif.render.pic_dir + '/' + fn))
    print 'New name: <input type="text" size="32" name="newname" value="%s">' % fn
    print pif.render.FormatButtonInput('rename')
    print pif.render.FormatRadio('cpmv', [('c', 'copy'), ('m', 'move')], pif.form.get('cpmv', 'c'))
    if pif.IsAllowed('m'): # pragma: no cover
	if pif.form.get('ov'):
	    print '<input type=checkbox name="ov" value="1" checked>'
	else:
	    print '<input type=checkbox name="ov" value="1">'
	print 'overwrite<br>'
	print 'Man: <input type="text" size="12" name="man" value="%s">' % GetMan(pif)
	#print '''<a onclick="incrfield('man',1);"><img src="../pic/gfx/but_inc.gif" alt="UP" onmouseover="this.src='../pic/gfx/hov_inc.gif';" onmouseout="this.src='../pic/gfx/but_inc.gif';" ></a>'''
	#print '''<a onclick="incrfield('man',-1);"><img src="../pic/gfx/but_dec.gif" alt="UP" onmouseover="this.src='../pic/gfx/hov_dec.gif';" onmouseout="this.src='../pic/gfx/but_dec.gif';" ></a>'''
	print pif.render.FormatButtonUpDown('man')
	print pif.render.FormatButtonInput('move to library', 'lib')
	print 'Category:', pif.render.FormatSelect('cat', sel_cat, pif.form.get('cat',''))
	print pif.render.FormatButtonInput('move to bin', 'mvbin')
	if cycle:
	    print '<input type=checkbox name="cy" value="1" checked>'
	else:
	    print '<input type=checkbox name="cy" value="1">'
	print 'cycle '
	print '<input type=checkbox name="inc" value="1"> increment name'
	print '<br>Variation: <input type="text" size="5" name="newvar" value="%s">' % pif.form.get('v', '')
	print 'Prefix:', pif.render.FormatSelect('pref', sel_pref, pif.form.get('pref',pif.form.get('tysz',szname)))
	print pif.render.FormatButtonInput('select to casting', 'select')
	print 'Move to:', pif.render.FormatSelect('moveto', sel_moveto, pif.form.get('moveto',''))
	print pif.render.FormatButtonInput('select to category', 'selcat')
    print '</form>'


def Action(pif, tdir, fn, act=1):
    global cycle
    nname = pif.form.get('newname', '')
    man = pif.form.get('man', '')
    cat = pif.form.get('cat', '')
    ov = pif.form.get('ov', False)
    mv = pif.form.get('cpmv', 'c') == 'm'
    if pif.form.get('delete'):
	useful.FileDelete(tdir + '/' + fn)
    elif pif.form.get('selcat'):
	dest = pif.form.get('moveto', '')
	if not nname or not dest:
	    print 'What?'
	else:
	    useful.FileMover(tdir + '/' + fn, dest + '/' + nname, mv=mv, ov=ov)
    elif pif.form.get('rename'):
	if not nname:
	    print 'What?'
	else:
	    useful.FileMover(tdir + '/' + fn, tdir + '/' + nname, mv=mv, ov=ov)
    elif pif.form.get('lib'):
	if not man:
	    print 'What?'
	elif not os.path.exists('./lib/' + man):
	    man2 = pif.dbh.FetchAlias(man)
	    if not man2:
		print 'bad destination'
	    else:
		useful.FileMover(tdir + '/' + fn, './lib/' + man2['ref_id'].lower() + '/' + fn, mv=mv, ov=ov)
	else:
	    useful.FileMover(tdir + '/' + fn, './lib/' + man + '/' + fn, mv=mv, ov=ov)
    elif pif.form.get('mvbin'):
	if not os.path.exists('./new/' + cat):
	    print 'bad destination'
	else:
	    useful.FileMover(tdir + '/' + fn, './new/' + cat + '/' + fn, mv=mv, ov=ov)
    elif pif.form.get('select'):
	var = pif.form.get('newvar', '')
	pref = pif.form.get('pref', '')
	man = pif.form.get('man', '')
	inc = pif.form.get('inc', '')
	if not man:
	    #man = tdir[tdir.rfind('/') + 1:]
	    print 'Huh? (select, no man)'
	else:
	    ddir = './' + config.imgdir175
	    dnam = man
	    if pref and adds.find(pref) >= 0:
		ddir = './' + config.imgdirAdd
		dnam = pref + '_' + dnam
		if var:
		    dnam += '-' + var
		inc = True
	    elif var:
		ddir = './' + config.imgdirVar
		dnam = dnam + '-' + var
		if pref:
		    dnam = pref + '_' + dnam
	    elif pref:
		dnam = pref + '_' + dnam
	    else:
		print "What?"
		return fn
	    dnam = dnam.lower() + '.jpg'
	    useful.FileMover(tdir + '/' + fn, ddir + '/' + dnam, mv=mv, ov=ov, inc=inc)

    if os.path.exists(fn):
	return fn
    elif cycle:
	dl, gl, ol, sl, xl = GetDir(tdir)
	while gl:
	    if gl[0] == fn:
		gl.pop()
	    else:
		return gl[0]
    return None

# -- imawidget

checked = {True : ' checked', False : ''}
def ShowEditor(pif, pdir, fn):
    full_path = os.path.join(pdir, fn)
    if not os.path.exists(full_path):
	print '<div class="warning">%s not found.</div><br>' % full_path
	return
    print editformstart
    print pif.render.FormatHiddenInput({'c' : urllib.quote_plus(pif.form.get('c', ''))})
    x,y = ShowEditForm(pif, pdir, fn)
    full_path = os.path.join(pdir, fn)
    root,ext = useful.RootExt(fn.strip())
    print '<table><tr><td></td><td>' + pif.render.FormatImageArt('hruler.gif') + '</td></tr>'
    print '<tr><td valign="top">' + pif.render.FormatImageArt('vruler.gif') + '</td><td valign="top">'
    #print '<a href="../' + full_path + '">' + pif.render.FormatImageRequired([root], suffix=ext, also={"border":"0"}) + '</a>'
    dic = {'file' : 'http://' + os.environ['SERVER_NAME'] + '/' + full_path, 'width' : x, 'height' : y}
    print def_edit_app % dic
    print '</td></tr></table>'
    print editformend % {'f' : fn, 'd' : pdir}


def PipeChain(inp, pipes, stderr=None, verbose=True):
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


def GetSize(fn):
    l = PipeChain(open(fn), ImportFile(fn) + [["/usr/local/bin/pamfile"]], subprocess.PIPE, verbose=False)
    f = l.split()
    try:
	x = int(f[3])
	y = int(f[5])
    except:
	x = y = 0
    return (x, y)


def Save(pif, fn, of, tdir, nfn=None):
    if not tdir.endswith('/'):
	tdir = tdir + '/'
    if nfn:
	if not '.' in nfn:
	    nfn = nfn + fn[fn.rfind('.'):]
    else:
	if '.' in fn:
	    nfn = fn[:fn.rfind('.')] + '_s' + fn[fn.rfind('.'):]
	else:
	    nfn = fn + '_s'
    open(tdir + nfn, "w").write(of)
    Log(pif, nfn, tdir)
    return nfn


def RotFlip(pif):
    transforms = list()
    if pif.FormInt('rr'):
	transforms.append(['/usr/local/bin/pamflip', '-r270'])
    elif pif.FormInt('rh'):
	transforms.append(['/usr/local/bin/pamflip', '-r180'])
    elif pif.FormInt('rl'):
	transforms.append(['/usr/local/bin/pamflip', '-r90'])
    elif pif.FormInt('fh'):
	transforms.append(['/usr/local/bin/pamflip', '-lr'])
    elif pif.FormInt('fv'):
	transforms.append(['/usr/local/bin/pamflip', '-tb'])
    return transforms


def Resize(x=None, y=None):
    if not x and not y:
	return []
    if not y:
	return [["/usr/local/bin/pamscale", "-xsize", str(x)]]
    if not x:
	return [["/usr/local/bin/pamscale", "-ysize", str(y)]]
    return [["pamscale", "-xsize", str(x), "-ysize", str(y)]]


def Cut(x1, y1, x2, y2):
    return [["/usr/local/bin/pamcut", "-top", str(y1), "-height", str(y2 - y1), "-left", str(x1), "-width", str(x2 - x1)]]


def MassResize(pif, pic_dir, fn, nname, q, original_size, desc=''):
    var = pif.form.get('v', '')
    man = GetMan(pif)
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
	if pif.form.get('ot'):
	    nname += '.' + pif.form['ot']
	Shape(pif, pic_dir, fn, nname, q, mbdata.imagesizes[pref], original_size, False)

	ddir = './' + config.imgdir175
	dnam = man
	if var:
	    ddir = './' + config.imgdirVar
	    dnam = dnam + '-' + var
	    if pref:
		dnam = pref + '_' + dnam
	else:
	    dnam = pref + '_' + dnam
	dnam = dnam.lower() + '.jpg'
	useful.FileMover(pic_dir + '/' + nname, ddir + '/' + dnam, mv=True, ov=True, inc=False)
	print '<br>', pif.render.FormatImageRequired([dnam], pdir=ddir, also={"border":"0"}),'<br>'
	print '<hr>'

    name = man
    if var:
	name += '-' + var
    pif.dbh.InsertActivity(name, pif.id, description=desc, image=ddir + '/' + dnam)


def Shape(pif, tdir, fil, nname, bound, target_size, original_size, show_final=True):
    global xts, yts
    xts,yts = target_size
    x1,y1,x2,y2 = map(lambda x: int(x), bound.split(','))
    pth = tdir + '/' + fil
    root,ext = useful.RootExt(fil.strip())
    xcs = x2 - x1
    ycs = y2 - y1
    xos, yos = original_size

    print 'Shape :', pth, ': bounds',x1,y1,x2,y2,'bound size',xcs,ycs,'target size', xts, yts, '<br>'
    if xts and yts:
	x1, x2, y1, y2 = SetS200Sizes(tdir, fil, x1, x2, y1, y2, xts, yts, xos, yos)
	xcs = x2 - x1
	ycs = y2 - y1

	if xcs > xts:
	    print "shrinking"
	    of = PipeChain(open(pth),
		    ImportFile(pth) + \
		    Cut(x1, y1, x2, y2) + \
		    RotFlip(pif) +  \
		    Resize(x=xts) + \
		    ExportFile(nname, fil))
	elif xcs < xts:
	    dx = xts - xcs
	    dy = yts - ycs
	    #x1, x2, y1, y2 = Normalize(x1 - dx / 2, x2 + dx - (dx / 2), y1 - dy / 2, y2 + dy - (dy / 2), xts, yts)
	    x1, x2, y1, y2 = Normalize(x1, x2, y1, y2, xts, yts)
	    print "expanding", x1, x2, y1, y2
	    of = PipeChain(open(pth),
		    ImportFile(pth) + \
		    Cut(x1, y1, x2, y2) + \
		    RotFlip(pif) + \
		    ExportFile(nname, fil))
	elif xos == xts and yos == yts and xos == xcs and yos == ycs:
	    print "copying"
	    of = open(pth).read()
	else:
	    print "cutting"
	    of = PipeChain(open(pth),
		    ImportFile(pth) + \
		    Cut(x1, y1, x2, y2) + \
		    RotFlip(pif) + \
		    ExportFile(nname, fil))

    else:

	if xts < x2 - x1:
	    print "trim shrinking x"
	    of = PipeChain(open(pth),
		    ImportFile(pth) + \
		    Cut(x1, y1, x2, y2) + \
		    RotFlip(pif) +  \
		    Resize(x=xts) + \
		    ExportFile(nname, fil))
	elif yts < y2 - y1:
	    print "trim shrinking y"
	    of = PipeChain(open(pth),
		    ImportFile(pth) + \
		    Cut(x1, y1, x2, y2) + \
		    RotFlip(pif) +  \
		    Resize(y=yts) + \
		    ExportFile(nname, fil))
	else:
	    print "trim cutting"
	    of = PipeChain(open(pth),
		    ImportFile(pth) + \
		    Cut(x1, y1, x2, y2) + \
		    RotFlip(pif) + \
		    ExportFile(nname, fil))

    print '<br>'
    nfn = Save(pif, fil, of, tdir, nname)

    print nfn, tdir, pth, '%s (%d, %d)<br>' % ((nfn,) + GetSize(tdir + '/' + nfn))
    if show_final:
	print pif.render.FormatImageRequired([nfn], suffix=ext, also={"border":"0"}),'<br>'


def ShowRedoer(pif, pdir, fn):
    print editformstart
    ShowEditForm(pif, pdir, fn)
    print 'Bounds:', pif.render.FormatTextInput('q', 20, value=pif.form['q'])
    print editformend % {'f' : fn, 'd' : pdir}
    print '<hr>'


def ShowEditForm(pif, pdir, fn):
    if os.path.exists(os.path.join(pdir, '.ima')):
	presets = eval(open(os.path.join(pdir, '.ima')).read())
    else:
	presets = dict()
    full_path = os.path.join(pdir, fn)
    if not os.path.exists(full_path):
	print '<div class="warning">%s not found.</div><br>' % full_path
	return 0,0

    x,y = GetSize(full_path)
    print '<div class="lefty">'
    print '(%d, %d)' % (x,y)
    print '<input type="radio" name="tysz" value="q"%s>' % checked[presets.get('tysz') == 'q']#checked[not pif.form.get('v')]
    print 'x: <input name="x" type="text" size="4" value="%s"> y: <input name="y" type="text" size="4" value="%s">' % (xts, yts)
    print pif.render.FormatRadio('tysz', map(lambda x: (x, x.upper()), mbdata.image_size_names), presets.get('tysz', 's'))
    print '-', pif.render.FormatCheckbox("unlv", [("1", "V")], presets.get("unlv", []))
    print pif.render.FormatCheckbox("unlh", [("1", "H")], presets.get("unlh", []))
    print pif.render.FormatButtonInput('keep')
    print pif.render.FormatCheckbox("rl", [("1", "RL")], presets.get("rl", []))
    print pif.render.FormatCheckbox("rh", [("1", "RH")], presets.get("rh", []))
    print pif.render.FormatCheckbox("rr", [("1", "RR")], presets.get("rr", []))
    print pif.render.FormatCheckbox("fh", [("1", "FH")], presets.get("fh", []))
    print pif.render.FormatCheckbox("fv", [("1", "FV")], presets.get("fv", []))
    print '<br>Name:', pif.render.FormatTextInput('newname', 20, value=pif.form.get('newname', ''))
    print pif.render.FormatSelect('ot', otypes, 'jpg')
    print pif.render.FormatButtonInput('resize')
    print pif.render.FormatButtonInput('crop')
    print pif.render.FormatButtonInput('crop and shrink', 'shrink')
    print pif.render.FormatButtonInput('wipe')
    print pif.render.FormatButtonInput('rename')
    if pif.IsAllowed('m'): # pragma: no cover
	print 'Var: ' + pif.render.FormatTextInput('v', 8, value=pif.form.get('v', ''))
    print pif.render.FormatCheckbox("repl", [("1", "Replace")], presets.get("repl", []))
    print pif.render.FormatButtonInput('mass')
    return x,y


def SetS200Sizes(tdir, fil, x1, x2, y1, y2, xts, yts, xos, yos):
    #xos, yos = GetSize(tdir + '/' + fil)
    xcs = x2 - x1
    ycs = y2 - y1
    ratio = float(xts) / float(yts)
    print "SetS200Sizes", tdir + '/' + fil, x1, y1, "/", x2, y2, ';', xts, yts, ';', xcs, ycs, ';', xos, yos, ';', ratio, "<br>"
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
	x1, x2, y1, y2 = Normalize(x1, x2, y1, y2, xos, yos)
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
    print 'SetS200Sizes returned', x1, y1, '/', x2, y2, '->', x2 - x1, y2 - y1, '<br>'
    return x1, x2, y1, y2


def Normalize(x1, x2, y1, y2, xm, ym):
    print 'Normalize', x1, y1, "/", x2, y2, "orig", xm, ym
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


def Shrink(pif, tdir, fil, nname, bound, maxsize):
    print 'In Shrink', tdir, fil, nname, bound, maxsize, '<br>'
    global xts, yts
    x1,y1,x2,y2 = map(lambda x: int(x), bound.split(','))
    xts, yts = maxsize
    xcs = x2 - x1
    ycs = y2 - y1
    if not xts:
	xts = xcs
    if not yts:
	yts = ycs
    pth = tdir + '/' + fil
    print 'Shrink',x1,y1,x2,y2,':',xcs,ycs,':',xts,yts,'<br>',pth,'<br>'
    if xcs == xts and ycs == yts:
	print "cutting",'<br>'
	of = PipeChain(open(pth),
		ImportFile(pth) + \
		Cut(x1, y1, x1 + xcs, y1 + ycs) + \
		RotFlip(pif) + \
		ExportFile(nname, fil))
    elif xts/xcs < yts/ycs:
	print "shrinking x",'<br>'
	of = PipeChain(open(pth),
		ImportFile(pth) + \
		Cut(x1, y1, x1 + xcs, y1 + ycs) + \
		RotFlip(pif) +  \
		Resize(x=xts) + \
		ExportFile(nname, fil))
    else:
	print "shrinking y",'<br>'
	of = PipeChain(open(pth),
		ImportFile(pth) + \
		Cut(x1, y1, x1 + xcs, y1 + ycs) + \
		RotFlip(pif) +  \
		Resize(y=yts) + \
		ExportFile(nname, fil))
    nfn = Save(pif, fil, of, tdir, nname)

    print nfn, tdir, pth, '<br>'
    print pif.render.FormatImageRequired([nfn], suffix='jpg', also={"border":"0"}),'<br>'
    print '%s (%d, %d)' % ((nfn,) + GetSize(tdir + '/' + nfn))


def Crop(pif, tdir, fil, nname, bound):
    global xts, yts
    x1,y1,x2,y2 = map(lambda x: int(x), bound.split(','))
    pth = tdir + '/' + fil
    print 'Crop',x1,y1,x2,y2,':',x2-x1,y2-y1,'<br>',pth,'<br>'
    print "cutting",'<br>'
    of = PipeChain(open(pth),
	    ImportFile(pth) + \
	    Cut(x1, y1, x2, y2) + \
	    RotFlip(pif) + \
	    ExportFile(nname, fil))
    nfn = Save(pif, fil, of, tdir, nname)

    print nfn, tdir, pth, '<br>'
    print pif.render.FormatImageRequired([nfn], suffix='jpg', also={"border":"0"}),'<br>'
    print '%s (%d, %d)' % ((nfn,) + GetSize(tdir + '/' + nfn))


def Rename(tdir, fil, nname):
    if not os.path.exists(tdir + '/' + nname):
	os.system('mv %s/%s %s/%s' % (tdir, fil, tdir, nname))
    else:
	print "Target exists"


def ImaWidget(pif):
    pif.render.PrintHtml()
    pif.Restrict('v')

    #print pif.form, '<br>'
    fn   = pif.form.get("f", '')
    root,ext = useful.RootExt(fn.strip())
    if pif.form.get('ot'):
	ext = pif.form['ot']
#    if pif.form.get('tysz'):
#	root += '_' + pif.form['tysz']
    nname = root + '.' + ext
    tdir = pif.form.get("d", '.')
    if not pif.IsAllowed('m'):
	tdir = './incoming'

    global xts, yts
    nvar = pif.form.get("newvar", '')
    pif.form.setdefault("v", '')
    var  = pif.form["v"]
    pif.render.pic_dir = tdir

    pif.render.title = pif.render.pagetitle = pif.render.pic_dir + '/' + fn
    print pif.render.FormatHead(extra=def_edit_js + pif.render.increment_js)
    if pif.form:
	print pif.form,'<br>'

    if pif.form.get('f') and os.path.exists(os.path.join(pif.form.get('d', ''), 'descr.txt')):
	descs = open(os.path.join(pif.form.get('d', ''), 'descr.txt')).readlines()
	descs = dict(map(lambda x: x.strip().split('\t', 1), descs))
	# mod_id, var_id, year, comment
	print descs.get(os.path.splitext(pif.form['f'])[0], '').replace('\t', '<br>')
	print '<hr>'

    if pif.form.get('keep'):
	Picker(pif, fn)
	print '<hr>'
	print pif.render.FormatImageRequired([fn[:fn.rfind('.')]], suffix=fn[fn.rfind('.') + 1:], also={"border":"0"}),'<br>'
	print pif.render.FormatTail()
	return

    pif.form.setdefault("q", '')
    q     = pif.form["q"]
    pif.form.setdefault("newname", root)
    nname = pif.form["newname"]

    tysz  = pif.form.get("tysz", "")
    xts = yts = 0
    if tysz == 'q':
	xts   = pif.FormInt('x')
	yts   = pif.FormInt('y')
    elif tysz:
	xts,yts = mbdata.imagesizes[tysz]
    if pif.form.get('wipe'):
	tysz = 'w'
    if pif.FormInt('unlv'):
	yts   = 0
    if pif.FormInt('unlh'):
	xts   = 0
    if not nname:
	nname = fn
    if '.' in nname:
	nname = nname[:nname.rfind('.')]
    if not pif.FormInt('repl') and tysz:
	nname = nname + '_' + tysz
    if pif.form.get('ot'):
	nname += '.' + pif.form['ot']
    else:
	nname += '.jpg'

    xos, yos = GetSize(pif.render.pic_dir + '/' + fn)
    if not q:
	q = '0,0,%d,%d' % (xos, yos)

    Picker(pif, nname)
    print '<hr>'
    is_edited = nname != fn
    try:
	if pif.form.get('mass'):
	    MassResize(pif, pif.render.pic_dir, fn, nname, q, (xos, yos))
	    man = GetMan(pif)
	    if man and pif.form.get('v'):
		print pif.render.FormatButton("promote", 'vars.cgi?mod=%s&var=%s&promote=1' % (man, pif.form['v']))
	elif pif.form.get('wipe'):
	    SavePresets(pif, pif.render.pic_dir)
	    Wiper(pif, pif.render.pic_dir, fn, nname, q, xos, yos, pif.FormInt('unlv'), pif.FormInt('unlh'))
	elif pif.form.get('resize'):
	    SavePresets(pif, pif.render.pic_dir)
	    if not pif.form.get('repl'):
		ShowRedoer(pif, pif.render.pic_dir, fn)
	    Shape(pif, pif.render.pic_dir, fn, nname, q, (xts, yts), (xos, yos))
	elif pif.form.get('crop'):
	    SavePresets(pif, pif.render.pic_dir)
	    if not pif.form.get('repl'):
		ShowRedoer(pif, pif.render.pic_dir, fn)
	    Crop(pif, pif.render.pic_dir, fn, nname, q)
	elif pif.form.get('shrink'):
	    SavePresets(pif, pif.render.pic_dir)
	    if not pif.form.get('repl'):
		ShowRedoer(pif, pif.render.pic_dir, fn)
	    Shrink(pif, pif.render.pic_dir, fn, nname, q, (xts, yts))
	elif pif.form.get('rename'):
	    Rename(pif.render.pic_dir, fn, nname)
	else:
	    ShowEditor(pif, pif.render.pic_dir, fn)
	    is_edited = False
    except:
	pif.ShowError()

    if is_edited:
	print pif.render.FormatButton('replace', 'upload.cgi?act=1&d=%s&f=%s&newname=%s&rename=1&cpmv=m&ov=1' % (tdir, nname, fn))

    print pif.render.FormatTail()


def SavePresets(pif, pdir):
    if os.path.exists(os.path.join(pdir, '.ima')):
	presets = {
	    "unlv" : [pif.form.get("unlv", '')],
	    "unlh" : [pif.form.get("unlh", '')],
	    "rl"   : [pif.form.get("rl", '')],
	    "rh"   : [pif.form.get("rh", '')],
	    "rr"   : [pif.form.get("rr", '')],
	    "fh"   : [pif.form.get("fh", '')],
	    "fv"   : [pif.form.get("fv", '')],
	    "repl" : [pif.form.get("repl", '')],
	    "tysz" : pif.form.get("tysz", ''),
	}
	open(os.path.join(pdir, '.ima'), 'w').write(str(presets))


def Wiper(pif, pdir, fin, fout, q, xs, ys, wipev, wipeh):
    print 'Wiper', pdir, fin, fout, q, wipev, wipeh, '<br>'
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
		WiperCopy(img, x1, yt, x2, yt, x1, y1, x2, y1)
		y1 += 1
	    if x1 > x2 or y1 > y2:
		break
	    if y2 != ys - 1:
		WiperCopy(img, x1, yb, x2, yb, x1, y2, x2, y2)
		y2 -= 1
	elif wipeh:
	    if x1 != 0:
		WiperCopy(img, xl, y1, xl, y2, x1, y1, x1, y2)
		x1 += 1
	    if x1 > x2 or y1 > y2:
		break
	    if x2 != xs - 1:
		WiperCopy(img, xr, y1, xr, y2, x2, y1, x2, y2)
		x2 -= 1
	else:
	    if y1 != 0:
		WiperCopy(img, x1, yt, x2, yt, x1, y1, x2, y1)
		y1 += 1
	    if x1 != 0:
		WiperCopy(img, xl, y1, xl, y2, x1, y1, x1, y2)
		x1 += 1
	    if x1 > x2 or y1 > y2:
		break
	    if y2 != ys - 1:
		WiperCopy(img, x1, yb, x2, yb, x1, y2, x2, y2)
		y2 -= 1
	    if x2 != xs - 1:
		WiperCopy(img, xr, y1, xr, y2, x2, y1, x2, y2)
		x2 -= 1
    img.save(pdir + '/' + fout)

    root,ext = useful.RootExt(fout.strip())
    #print pif.render.FormatImageRequired([fout], suffix=ext, also={"border":"0"}),'<br>'
    print '%s (%d, %d)<br>' % ((fout,) + GetSize(pdir + '/' + fout))
    ShowEditor(pif, pif.render.pic_dir, fout)


def WiperCopy(img, xf1, yf1, xf2, yf2, xt1, yt1, xt2, yt2):
    #print ('%3d ' * 8) % (xf1, yf1, xf2 + 1, yf2 + 1, xt1, yt1, xt2 + 1, yt2 + 1)
    cp = img.crop((xf1, yf1, xf2 + 1, yf2 + 1))
    img.paste(cp, (xt1, yt1, xt2 + 1, yt2 + 1))


# ----- upload


def PicForm(pif, restrict=False, desc=''):
    mod = pif.form.get('m', '')
    var = pif.form.get('v', '')
    print '<form action="upload.cgi" enctype="multipart/form-data" method="post" name="upload">'
    if 'y' in pif.form:
	print '<input type="hidden" name="y" value="%s">' % pif.form['y']
    #FormatTable({'also':{}, 'id':'', 'style_id':'', 'rows':[]})
    #rows=[{'ids':[], 'also':{}, 'cells':[]}, ...]
    #cells=[{'col':None, 'content':"&nbsp;", 'hdr':False, 'also':{}, 'large':False, 'id':''}, ...]

    '''
    table = pif.render.CreateTable()
    table.row()
    if mod:
	rows.append({'cells':[{'col':0, 'content':'Model'}, {'col':1, 'content':mod}]})
	print '<input type="hidden" name="m" value="%s">' % mod
	rows.append({'cells':[{'col':0, 'content':'Variation'}, {'col':1, 'content': pif.render.FormatTextInput('v', 8, value=var)}]})
    if not restrict:
	rows.append({'cells':[{'col':0, 'content':'Directory'},
		    {'col':1, 'content':pif.render.FormatTextInput('d', 64, value=pif.form.get('d', './incoming'))}]})
	rows.append({'cells':[{'col':0, 'content':'Rename file to'},
		    {'col':1, 'content':pif.render.FormatTextInput('n', 64, value=pif.form.get('r', '')) + " (optional)"}]})
	rows.append({'cells':[{'col':0},
		    {'col':0, 'content':"Choose one of the following:"}]})
    rows.append({'cells':[{'col':0, 'content':'File to Upload'},
		{'col':1, 'content':'<input type="file" name="f" size="40">'}]})
    if not restrict:
	rows.append({'cells':[{'col':0, 'content':'URL to grab'},
		    {'col':1, 'content':pif.render.FormatTextInput('u', 80, 80)}]})
	rows.append({'cells':[{'col':0, 'content':'URL to scrape'},
		    {'col':1, 'content':pif.render.FormatTextInput('s', 80, 80)}]})
    rows.append({'cells':[{'col':0, 'content':'Comment'},
		{'col':1, 'content':pif.render.FormatTextInput('c', 80, 80, desc)}]})
    if not restrict and mod: # var:
	rows.append({'cells':[{'col':0, 'content':'Choose from library'},
		    {'col':1, 'content':pif.render.FormatButtonInput("select", name="l", also={})}]})
    rows.append({'cells':[{'col':0, 'content':'&nbsp;'},
		{'col':0, 'content':pif.render.FormatButtonInput() +
		    (pif.render.FormatButtonInput("replace") if not restrict else '') +
		    pif.render.FormatButtonReset("upload") +
		    pif.render.FormatButtonInput("mass")}]})
    print pif.render.FormatTable({'rows':rows})
    '''

    rows = list()
    if mod:
	rows.append({'cells':[{'col':0, 'content':'Model'}, {'col':1, 'content':mod}]})
	print '<input type="hidden" name="m" value="%s">' % mod
	rows.append({'cells':[{'col':0, 'content':'Variation'}, {'col':1, 'content': pif.render.FormatTextInput('v', 8, value=var)}]})
    if not restrict:
	rows.append({'cells':[{'col':0, 'content':'Directory'},
		    {'col':1, 'content':pif.render.FormatTextInput('d', 64, value=pif.form.get('d', './incoming'))}]})
	rows.append({'cells':[{'col':0, 'content':'Rename file to'},
		    {'col':1, 'content':pif.render.FormatTextInput('n', 64, value=pif.form.get('r', '')) + " (optional)"}]})
	rows.append({'cells':[{'col':0},
		    {'col':0, 'content':"Choose one of the following:"}]})
    rows.append({'cells':[{'col':0, 'content':'File to Upload'},
		{'col':1, 'content':'<input type="file" name="f" size="40">'}]})
    if not restrict:
	rows.append({'cells':[{'col':0, 'content':'URL to grab'},
		    {'col':1, 'content':pif.render.FormatTextInput('u', 80, 80)}]})
	rows.append({'cells':[{'col':0, 'content':'URL to scrape'},
		    {'col':1, 'content':pif.render.FormatTextInput('s', 80, 80)}]})
    rows.append({'cells':[{'col':0, 'content':'Comment'},
		{'col':1, 'content':pif.render.FormatTextInput('c', 80, 80, desc)}]})
    if not restrict and mod: # var:
	rows.append({'cells':[{'col':0, 'content':'Choose from library'},
		    {'col':1, 'content':pif.render.FormatButtonInput("select", name="l", also={})}]})
    rows.append({'cells':[{'col':0, 'content':'&nbsp;'},
		{'col':0, 'content':pif.render.FormatButtonInput() +
		    (pif.render.FormatButtonInput("replace") if not restrict else '') +
		    pif.render.FormatButtonReset("upload") +
		    pif.render.FormatButtonInput("mass")}]})
    print pif.render.FormatTable({'rows':rows})

    '''
    print pif.render.FormatTableStart()
    if mod:
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, 'Model')
	print pif.render.FormatCell(1, mod)
	print '<input type="hidden" name="m" value="%s">' % mod
	print pif.render.FormatRowEnd()
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, 'Variation')
	print pif.render.FormatCell(1, pif.render.FormatTextInput('v', 8, value=var))
	print pif.render.FormatRowEnd()
    if not restrict:
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, 'Directory')
	print pif.render.FormatCell(1, pif.render.FormatTextInput('d', 64, value=pif.form.get('d', './incoming')))
	print pif.render.FormatRowEnd()
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, 'Rename file to')
	print pif.render.FormatCell(1, pif.render.FormatTextInput('n', 64, value=pif.form.get('r', '')) + " (optional)")
	print pif.render.FormatRowEnd()
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0)
	print pif.render.FormatCell(0, "Choose one of the following:")
	print pif.render.FormatRowEnd()
    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, 'File to Upload')
    print pif.render.FormatCell(1, '<input type="file" name="f" size="40">')
    print pif.render.FormatRowEnd()
    if not restrict:
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, 'URL to grab')
	print pif.render.FormatCell(1, '<input type="text" name="u" size="80">')
	print pif.render.FormatRowEnd()
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, 'URL to scrape')
	print pif.render.FormatCell(1, '<input type="text" name="s" size="80">')
	print pif.render.FormatRowEnd()
#	print pif.render.FormatRowStart()
#	print pif.render.FormatCell(0, 'Replace existing')
#	print pif.render.FormatCell(1, '<input type="checkbox" name="o">')
#	print pif.render.FormatRowEnd()
    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, 'Comment')
    print pif.render.FormatCell(1, '<input type="text" name="c" size="80" value="%s">' % desc)
    print pif.render.FormatRowEnd()
    if not restrict and mod: # var:
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, 'Choose from library')
	print pif.render.FormatCell(1, pif.render.FormatButtonInput("select", name="l", also={}))
	print pif.render.FormatRowEnd()
    print pif.render.FormatRowStart()
    print pif.render.FormatCell(0, '&nbsp;')
    print pif.render.FormatCell(0, pif.render.FormatButtonInput() +
	(pif.render.FormatButtonInput("replace") if not restrict else '') +
	pif.render.FormatButtonReset("upload") +
	pif.render.FormatButtonInput("mass"))
    print pif.render.FormatRowEnd()
    print pif.render.FormatTableEnd()
    '''
    print '</form>'


def PicShow(pif, tdir, fn, desc=''):
    Show(pif, tdir, fn)


cols = 6
def ShowList(pif, title, tdir, fl):
    if not fl:
	return
    clen = (len(fl) - 1) / cols + 1
    ffl = map(lambda x: fl[(x*clen):((x+1)*clen)], range(0, cols))
    print '<h4>%s (%d)</h4>' % (title, len(fl))
    print "<table width=100%><tr valign=top>"
    for cl in ffl:
	print "<td width=%d%%>" % (100/cols)
	for f in cl:
	    root,ext = useful.RootExt(f.strip())
	    fst = os.stat(tdir + '/' + f)
	    perms = fst[stat.ST_MODE]
	    if (perms & 5) == 0:
		print '%s<br>' % f
	    elif ext in image_inputters:
		print '<a href="?d=%s&n=%s">%s</a><br>' % (tdir, f, f)
	    else:
		print f
	print "</td>"
    print "</tr></table>"
    print '<br><hr>'


def ShowDir(pif, tdir):
    print '<hr>'

    dl, gl, ol, sl, xl = GetDir(tdir)

    #ShowList(pif, "Directories", tdir, dl)

    if gl:
	ShowList(pif, "Graphics", tdir, gl)

    #ShowList(pif, "Data Files", tdir, sl)
    #ShowList(pif, "Other Files", tdir, ol)


def RestrictedUpload(pif):
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
    pif.render.Comment("form", pif.form)
    if pif.form.get('u'):
	fn = GrabURLFile(pif, pif.form['u'], direc, fn)
	Thanks(pif, fn)
    elif pif.form.get('f'):
	UploadFile(pif, pif.form['f'], direc, fn)
	Thanks(pif, fn)
    else:
	PicForm(pif, restrict=True)


def Thanks(pif, fn):
    comment = '-'
    if pif.form.get('c'):
	comment = re.compile(r'\s\s*').sub(' ', pif.form['c'])
    open('./submitted/descr.txt', 'a+').write('\t'.join([fn, pif.form.get('m', '-'), pif.form.get('v', '-'), pif.form.get('y', '-'), comment]) + '\n')
    print '<div class="warning">Thank you for submitting that file.</div><br>'
    print "Unfortunately, you will now have to use your browser's BACK button to get back to where you were, as I have no idea where that was."


def MassUploadMain(pif):
    # dnfus = bad
    # mvdfus = good
    print '<hr>'
    #print pif.form
    print '<hr>'
    direc = pif.form.get('d', '')
    if not pif.IsAllowed('u'):
	RestrictedUpload(pif)
	return
    pif.render.Comment("form", pif.form)

    if pif.form.get('ul'):
	for url in pif.form['ul'].split('\n'):
	    url = url.strip()
	    if url:
		print url, '<br>'
		GrabURLFile(pif, url, direc, '')
		sys.stdout.flush()
	print '<hr>'
    else:
	print '<form action="upload.cgi" enctype="multipart/form-data" method="post" name="upload">'
	print '<input type="hidden" value="1" name="mass">'
	print pif.render.FormatTableStart()
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, 'Directory')
	print pif.render.FormatCell(1, pif.render.FormatTextInput('d', 64, value=pif.form.get('d', './incoming')))
	print pif.render.FormatRowEnd()
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, 'URLs to grab')
	print pif.render.FormatCell(1, '<textarea name="ul" cols="80" rows="20" wrap="off"></textarea>')
	print pif.render.FormatRowEnd()
	print pif.render.FormatRowStart()
	print pif.render.FormatCell(0, '&nbsp;')
	print pif.render.FormatCell(0, pif.render.FormatButtonInput() + pif.render.FormatButtonReset("upload"))
	print pif.render.FormatRowEnd()
	print pif.render.FormatTableEnd()
	print '</form>'


def UploadMain(pif):
    # dnfus = bad
    # mvdfus = good
    os.environ['PATH'] += ':/usr/local/bin'
    pif.render.PrintHtml()
    pif.render.title = 'upload - ' + pif.form.get('m', '')
    print pif.render.FormatHead(extra=def_edit_js + pif.render.reset_button_js + pif.render.increment_js)
    if pif.form.get('mass'):
	MassUploadMain(pif)
	print pif.render.FormatTail()
	return
    print pif.form
    print '<hr>'
    desc = pif.form.get('c')
    if pif.form.get('m') and pif.form.get('v'):
	var = pif.dbh.FetchVariation(pif.form['m'], pif.form['v'])
	if var:
	    var = var[0]
	    var = pif.dbh.DePref('variation', var)
	    print '<br>%s:<ul>' % pif.form['v']
	    print '<li>description:', var['text_description']
	    print '<li>base:', var['text_base']
	    print '<li>body:', var['text_body']
	    print '<li>interior:', var['text_interior']
	    print '<li>wheels:', var['text_wheels']
	    print '<li>windows:', var['text_windows'], '</ul>'
	    print '<hr>'
    overwrite = False
    direc = pif.form.get('d', '')
    if not pif.IsAllowed('u'):
	RestrictedUpload(pif)
	print pif.render.FormatTail()
	return
    elif not pif.IsAllowed('m'):
	direc = './incoming'
    elif pif.form.get('replace'):
	overwrite = True
    pif.render.Comment("form", pif.form)
    try:
	if pif.FormInt('act'):
	    DoAction(pif, direc, pif.form['f'], cy=pif.FormInt('cy'))
	elif pif.form.get('m'):
	    if not pif.form.get('d'):
		direc = './lib/' + pif.form['m'].lower()
	    if pif.form.get('u'):
		GrabURLMod(pif, pif.form['u'], pif.form['m'], pif.form.get('v'), overwrite=overwrite, desc=desc)
	    elif pif.form.get('s'):
		ScrapeURLMod(pif, pif.form['s'], pif.form['m'], pif.form.get('v'), overwrite=overwrite, desc=desc)
	    elif pif.form.get('f'):
		UploadMod(pif, pif.form['f'], pif.form['m'], pif.form.get('v'), overwrite=overwrite, desc=desc)
	    elif pif.form.get('l'):
		SelectFromLibrary(pif, pif.form['m'], pif.form.get('v'), desc=desc)
	    else:
		PicForm(pif, desc=desc)
	else:
	    if pif.form.get('u'):
		GrabURLPic(pif, pif.form['u'], direc, pif.form.get('n'), overwrite=overwrite, track=True, desc=desc)
	    elif pif.form.get('s'):
		ScrapeURLPic(pif, pif.form['s'], direc, pif.form.get('n'), overwrite=overwrite, desc=desc)
	    elif pif.form.get('r'):
		PicForm(pif, desc=desc)
	    elif pif.form.get('f'):
		fn = pif.form.get('n')
		if not fn:
		    fn = pif.form.get('f.name')
		if not fn:
		    fn = 'unknown'
		UploadPic(pif, pif.form['f'], direc, fn, overwrite=overwrite, desc=desc)
	    elif pif.form.get('n'):
		PicShow(pif, direc, pif.form['n'], desc=desc)
	    elif pif.form.get('d'):
		ShowDir(pif, direc, desc=desc)
	    else:
		PicForm(pif, desc=desc)
    except OSError:
	print '<div class="warning">'
	print 'fail:', traceback.format_exc(0)
	print '</div><br>'
    print pif.render.FormatTail()


def DoAction(pif, tdir, fn, act=1, cy=0):
    print '<div class="warning">'
    nfn = Action(pif, tdir, fn, act)
    print '</div><br>'
    if nfn:
	ShowPicture(pif, nfn)
    elif cy:
	pif.render.pic_dir = tdir
	dl, gl, ol, sl, xl = GetDir(tdir)
	if gl:
	    ShowPicture(pif, gl[0])
	else:
	    ShowDir(pif, tdir)
    else:
	ShowDir(pif, tdir)

# -- stitch

def StitchH(ofn, fa, miny, limit_x, limit_y, verbose=False):
    if limit_y:
	miny = min(miny, limit_y)
    cat = ['pnmcat', '-lr']
    for f in fa:
	pipes = ImportFile(f[0]) + \
		Cut(f[3], f[4], f[5], f[6]) + \
		Resize(x=limit_x, y=miny)
	outf = PipeChain(open(f[0]), pipes, verbose=verbose)
	if verbose:
	    print '>', f[0] + '.pnm', '<br>'
	open(f[0] + '.pnm', 'w').write(outf)
	cat.append(f[0] + '.pnm')
    outf = PipeChain(open('/dev/null'), [cat] + ExportFile(ofn), verbose=verbose)
    if verbose:
	print '>', ofn, '<br>'
    open(ofn, 'w').write(outf)

    if not verbose:
	for f in fa:
	    os.unlink(f[0] + '.pnm')


def StitchV(ofn, fa, minx, limit_x, limit_y, verbose=False):
    limit_y = 0
    if limit_x:
	minx = min(minx, limit_x)
    cat = ['pnmcat', '-tb']
    for f in fa:
	pipes = ImportFile(f[0]) + \
		Cut(f[3], f[4], f[5], f[6]) + \
		Resize(x=minx, y=limit_y)
	outf = PipeChain(open(f[0]), pipes, verbose=verbose)
	if verbose:
	    print '>', f[0] + '.pnm', '<br>'
	open(f[0] + '.pnm', 'w').write(outf)
	cat.append(f[0] + '.pnm')
    outf = PipeChain(open('/dev/null'), [cat] + ExportFile(ofn), verbose=verbose)
    if verbose:
	print '>', ofn, '<br>'
    open(ofn, 'w').write(outf)

    if not verbose:
	for f in fa:
	    os.unlink(f[0] + '.pnm')


def ShowWidget(pif, filepath):
    x,y = GetSize(filepath)
    dic = {'file' : 'http://' + os.environ['SERVER_NAME'] + '/' + filepath, 'width' : x, 'height' : y}
    return def_edit_app % dic


def StitchReadForm(pif, verbose=False):
    file_count = pif.FormInt('fc')
    fsl = list()
    for file_num in range(0, file_count + 1):
	fs = dict()
	if ('fn_%d' % file_num) in pif.form:
	    fs['fn'] = pif.form.get('fn_%d' % file_num)
	fs['n'] = '%d' % file_num
	if file_num < file_count - 2:
	    fs['x1'] = pif.FormInt('x1_%d' % file_num)
	    fs['y1'] = pif.FormInt('y1_%d' % file_num)
	    fs['x2'] = pif.FormInt('x2_%d' % file_num)
	    fs['y2'] = pif.FormInt('y2_%d' % file_num)
	elif file_num == file_count - 2:
	    fs['x1'], fs['y1'], fs['x2'], fs['y2'] = map(lambda x: int(x), pif.form['q'].split(','))
	elif file_num == file_count - 1:
	    if fs.get('fn', '').startswith('http://'):
		fs['fn'] = fs['fn'][fs['fn'].find('/', 7) + 1:]
	if verbose:
	    print file_num, fs,'<br>'
	fsl.append(fs)
    return fsl


def StitchFinalize(pif, verbose=False):
    fsl = StitchReadForm(pif, verbose)
    final = fsl[-2].get('fn', '').strip()
    if not final:
	final = fsl[0]['fn'].rsplit('.', 1)
	final = final[0] + '_st.' + final[1]
    fsl = fsl[:-2]

    fa = list()
    minx = miny = None
    print pif.render.FormatTableStart()
    input_files = list()
    for fs in fsl:
	print pif.render.FormatRowStart()
	img = fs['fn']
	input_files.append(img)
	crop_l = int(fs['x1'])
	crop_r = int(fs['x2'])
	crop_t = int(fs['y1'])
	crop_b = int(fs['y2'])
	x, y = GetSize(img)
	fa.append((img, x, y, crop_l, crop_t, crop_r, crop_b))
	cx = crop_r - crop_l
	cy = crop_b - crop_t
	if not minx or cx < minx:
	    minx = cx
	if not miny or cy < miny:
	    miny = cy
	#print fa[-1],'<br>'
	print pif.render.FormatCell(1, str(fs['fn']))
	print pif.render.FormatCell(1, str(fs['x1']), also={'width':40})
	print pif.render.FormatCell(1, str(fs['y1']), also={'width':40})
	print pif.render.FormatCell(1, str(fs['x2']), also={'width':40})
	print pif.render.FormatCell(1, str(fs['y2']), also={'width':40})
	print pif.render.FormatRowEnd()

    print pif.render.FormatTableEnd()
    print 'Stitching...', final
    limit_x = int(pif.form.get('limit_x', 0))
    limit_y = int(pif.form.get('limit_y', 0))
    if pif.form.get('or') == 'h':
	print 'horizontal'
	StitchH(final, fa, miny, limit_x, limit_y, verbose)
    else:
	print 'vertical'
	StitchV(final, fa, minx, limit_x, limit_y, verbose)
    time.sleep(2)
    print '... Finished.<br>'
    sys.stdout.flush()
    #print '<a href="../' + final + '">' + final + '<br>'
    #print '<img src="../' + final + '"></a>'
    d, f = os.path.split(final)
    Show(pif, d, f)
    orig = input_files[0][input_files[0].rfind('/') + 1:]
    print '<br><form>Final resting place:'
    print pif.render.FormatTextInput('o', 80, value='%s' % input_files[0])
    print pif.render.FormatHiddenInput({'f' : '%s/%s' % (d, f)})
    for fn in input_files:
	print pif.render.FormatHiddenInput({'in' : fn})
    print pif.render.FormatButtonInput('finish')
    print '</form>'


def StitchFinish(pif, verbose=False):
    print pif.form, '<hr>'

    for fn in pif.form.get('in', []):
	useful.FileMover(fn, 'lib/trash/' + fn[fn.rfind('/') + 1:], mv=True, inc=True, trash=False)
    useful.FileMover(pif.form.get('f'), pif.form.get('o'), mv=True, ov=True)


def StitchMain(pif, verbose=False):
    pif.render.PrintHtml()

    pif.render.title = 'stitch'
    print pif.render.FormatHead(extra=def_edit_js)

    if 'finish' in pif.form:
	StitchFinish(pif, verbose)
    elif 'finalize' in pif.form:
	StitchFinalize(pif, verbose)
    else:
	StitchInput(pif, verbose)

    print pif.render.FormatTail()


def StitchInput(pif, verbose=False):
    file_count = pif.FormInt('fc')
    fsl = StitchReadForm(pif, verbose)
    print fsl, '<br>'

    print '''<form action="stitch.cgi" name="myForm" onSubmit="return getValueFromApplet()">'''
    print pif.render.FormatHiddenInput({'fc':file_count + 1})
    print pif.render.FormatTableStart()
    min_x = pif.FormInt('limit_x', 999999)
    min_y = pif.FormInt('limit_y', 999999)
    for fs in fsl:
	print pif.render.FormatRowStart()
	num = fs['n']
	fn = fs.get('fn', '').strip()
	fn_size = ''
	if fn:
	    if not 'x1' in fs and os.path.exists(fn):
		x,y = GetSize(fn)
		min_x = min(x, min_x)
		min_y = min(y, min_y)
		fn_size = '<br>' + str((x,y))
	    print pif.render.FormatCell(1, fn + fn_size)
	    print pif.render.FormatHiddenInput({'fn_' + num : fn})
	else:
	    print pif.render.FormatCell(1, pif.render.FormatTextInput('fn_%d' % file_count, 80) + '<br>' + fsl[0]['fn'].strip())
	    print pif.render.FormatCell(1, pif.render.FormatButtonInput() + ' ' +
		pif.render.FormatButtonInput('finalize') + '<br>' +
		pif.render.FormatCheckbox('or', [('h','horizontal')]),
		    also={'colspan':2})
	    print pif.render.FormatCell(1, 'x ' + pif.render.FormatTextInput('limit_x', 5, value=min_x))
	    print pif.render.FormatCell(1, 'y ' + pif.render.FormatTextInput('limit_y', 5, value=min_y))
	if 'x1' in fs:
	    print pif.render.FormatCell(1, str(fs['x1']), also={'width':40})
	    print pif.render.FormatHiddenInput({'x1_' + num : fs['x1']})
	    print pif.render.FormatCell(1, str(fs['y1']), also={'width':40})
	    print pif.render.FormatHiddenInput({'y1_' + num : fs['y1']})
	    print pif.render.FormatCell(1, str(fs['x2']), also={'width':40})
	    print pif.render.FormatHiddenInput({'x2_' + num : fs['x2']})
	    print pif.render.FormatCell(1, str(fs['y2']), also={'width':40})
	    print pif.render.FormatHiddenInput({'y2_' + num : fs['y2']})
	elif fn:
	    if not os.path.exists(fn):
		print pif.render.FormatCell(1, 'Nonexistant: ' + os.getcwd() + '/' + fn, also={'colspan':4})
	    else:
		print pif.render.FormatCell(1, ShowWidget(pif, fn), also={'colspan':4})
	print pif.render.FormatRowEnd()
    print pif.render.FormatTableEnd()
    print '<input type="hidden" value="" name="q">' # for imawidget
    print '</form>'


def CastingPictures(pif, mod_id, direc):
    fl = glob.glob('%s/%s*.*' % (direc, mod_id)) + glob.glob('%s/?_%s*.*' % (direc, mod_id))
    fl.sort()
    if fl:
	print '<h3>%s</h3>' % direc
	if direc == config.imgdirAdd:
	    print pif.render.FormatButton('describe', pif.dbh.GetEditorLink(pif, 'attribute_picture', {'mod_id' : mod_id})) + '<br>'
	for fn in fl:
	    print '<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s&man=%s"><img src="../%s">%s</a> ' % (direc, fn[fn.rfind('/') + 1:], mod_id, fn, fn)
	    print '<br>'
	print '<hr>'



def LineupPictures(pif, lup_models):
    print '<h3>Lineup Models</h3>'
    lup_models.sort(key=lambda x: x['lineup_model.year'])
    for mod in lup_models:
	if mod['section.img_format']:
	    mod['filename'] = mod['section.img_format'] % mod['lineup_model.number'] + '.jpg'
	    mod['filepath'] = mod['page_info.pic_dir'] + '/' + mod['filename']
	    if os.path.exists(mod['filepath']):
		print '<a href="/cgi-bin/imawidget.cgi?d=%(page_info.pic_dir)s&f=%(filename)s&man=%(lineup_model.mod_id)s"><img src="../%(filepath)s">%(filepath)s</a><br>' % mod
    print '<hr>'


def PicturesMain(pif):
    pif.render.PrintHtml()
    pif.render.title = 'pictures - ' + pif.form.get('m', '')
    print pif.render.FormatHead()
    pif.render.Comment("form", pif.form)
    mod_id = pif.form.get('m', '')
    if mod_id:
	map(lambda x: CastingPictures(pif, mod_id.lower(), x), [config.imgdir175, config.imgdirVar, 'pic/man/icon', config.imgdirAdd])
	LineupPictures(pif, pif.dbh.FetchCastingLineups(mod_id))
    else:
	print 'Huh?'
    print pif.render.FormatTail()


# -- icon

# & ' + - .  /

def CreateIcon(fn, name, logo, isizex=100, isizey=100):
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

    text = icon.icon(isizex, isizey)
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


def MangleName(name):
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


def GetManList(pif):
    manlist = pif.dbh.FetchCastingList()
    mans = dict()
    for llist in manlist:
        llist = pif.dbh.ModifyManItem(llist)
        mans[llist['id'].lower()] = llist
    return mans


def IconMain(pif):

    SWITCHES = "av"
    OPTIONS = "bn"

    switch, files = cmdline.CommandLine(SWITCHES, OPTIONS)

    title = 'mb2'
    if switch['b']:
	title = switch['b'][-1]

    logo = pif.render.FindArt(title)

    #manlist = filter(lambda x: x[0] == 'm', map(lambda x: x.strip().split('|'), open('../../src/man.dat').readlines()))
    #mandict = dict(map(lambda x: (x[1].strip().lower(), MangleName(x[6])), manlist))

    mandict = GetManList(pif)

    if switch['a']:
	for man in mandict:
	    name = MangleName(mandict[man]['rawname'])
	    if switch['n']:
		name = switch['n'][-1].split(';')
	    CreateIcon(man, name, logo)
    elif files:
	for man in files:
	    if man in mandict:
		name = MangleName(mandict[man]['rawname'])
		if switch['n']:
		    name = switch['n'][-1].split(';')
		CreateIcon(man, name, logo)
    else:
	print 'huh?' # print mandict


def ImageStar(pif, image_path, pic_id='', halfstar=False):
    if pic_id == None:
	return pif.render.FormatImageArt('stargray.gif')
    if not os.path.exists(image_path):
	if pic_id:
	    return pif.render.FormatImageArt('staryellow.gif')
	return pif.render.FormatImageArt('starwhite.gif')
	return '&nbsp;' # pif.render.FormatImageArt('stargray.gif')
    try:
	img = Image.open(image_path)
    except:
	return pif.render.FormatImageArt('staryellow.gif')
	return ''
    ix, iy = img.size

    if ix < 200:
	return pif.render.FormatImageArt('starred.gif')
    if ix < 400:
	return pif.render.FormatImageArt('stargreen.gif')
    if ix > 400:
	return pif.render.FormatImageArt('starblue.gif')
    if halfstar:
	return pif.render.FormatImageArt('starhalf.gif')
    return pif.render.FormatImageArt('star.gif')

# -- bits

def BitsMain(pif):
    years = {
	'1998' : { 'd' : config.imgdirMtLaurel, 'p' : '1998', 'r' : 'ur' },
	'1999' : { 'd' : config.imgdirMtLaurel, 'p' : '1999', 'r' : 'urd' },
	'2000' : { 'd' : config.imgdirMtLaurel, 'p' : '2000', 'r' : 'urdab' },
	'2002' : { 'd' : config.imgdirMtLaurel, 'p' : '2002', 'r' : 'ur' },
	'2003' : { 'd' : config.imgdirMtLaurel, 'p' : '2003', 'r' : 'ur' },
	'2004' : { 'd' : config.imgdirMtLaurel, 'p' : '2004', 'r' : 'ur' },
	'2008' : { 'd' : config.imgdirMattel, 'p' : '2008', 'r' : 'u' },
	'2009' : { 'd' : config.imgdirMattel, 'p' : '2009', 'r' : 'u' },
    }

    colors = { True : "#CCCCCC", False : "#FFFFFF" }

    pif.render.PrintHtml()

    print "<table>"

    yearlist = years.keys()
    yearlist.sort()

    c = False
    print "<tr>"
    print "<th></th>"
    for y in yearlist:
	print '<th bgcolor="%s" colspan=%d>%s</th>' % ( colors[c], len(years[y]['r']), y )
	c = not c
    print "</tr>"

    c = False
    print "<tr>"
    print "<th></th>"
    for y in yearlist:
	for r in years[y]['r']:
	    print '<th bgcolor="%s">%s</th>' % ( colors[c], r.upper() )
	c = not c
    print "</tr>"

    for a in range(1,21):

	c = False
	print "<tr>"
	print '<th bgcolor="%s">%d</th>' % ( colors[True], a )

	for y in yearlist:
	    for r in years[y]['r']:

		fmt = "%s/%s%ss%02d.gif"
		f = fmt % ( years[y]['d'], years[y]['p'], r, a )

		cstr = '<th bgcolor="%s">' % ( colors[c] )
		if os.path.exists("../htdocs/"+f):
		    cstr += '<img src="%s">' % ( "../" + f )
		else:
		    cstr += "&nbsp;"
		print cstr + '</th>'
	    c = not c
	print "</tr>"
    print "</table>"


# -- library

def ShowLibraryList(pif, title, tdir, fl):
    cols = pif.FormInt("c", 5)
    if not fl:
	return
    clen = (len(fl) - 1) / cols + 1
    ffl = map(lambda x: fl[(x*clen):((x+1)*clen)], range(0, cols))
    print '<h4>%s (%d)</h4>' % (title, len(fl))
    print "<table width=100%><tr valign=top>"
    for cl in ffl:
	print "<td width=%d%%>" % (100/cols)
	for f in cl:
	    root,ext = useful.RootExt(f.strip())
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


def ShowLibraryGraf(title, tdir, fl):
    if not fl:
	return

    print '<h4>%s (%d)</h4>' % (title, len(fl))
    fd = {}
    for f in fl:
	root, ext = useful.RootExt(f)
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


def ShowLibraryDir(pif, tdir, grafs=0):
    print '<hr>'

    dl, gl, ol, sl, xl = GetDir(tdir)

    ShowLibraryList(pif, "Directories", tdir, dl)
    if grafs:
	ShowLibraryGraf("Graphics", tdir, gl)
    else:
	ShowLibraryList(pif, "Graphics", tdir, gl)
    ShowLibraryList(pif, "Data Files", tdir, sl)
    ShowLibraryList(pif, "Executable Files", tdir, xl)
    ShowLibraryList(pif, "Other Files", tdir, ol)

    if gl:
	print '<form action="traverse.cgi">'
	print '<a href="traverse.cgi?g=1&d=%s">%s</a> or ' % (tdir, pif.render.FormatButton('show all pictures'))
	print 'Pattern <input type="text" name="p">'
	print '<input type="hidden" name="d" value="%s">' % tdir
	print pif.render.FormatButtonInput()
	print '</form>'

    print '<a href="upload.cgi?d=%s&m=%s">%s</a>' % (tdir, tdir[7:], pif.render.FormatButton('upload'))



imginputs = '''<input type="checkbox" name="rm" value="%(f)s"> rm<input type="checkbox" name="mv" value="%(f)s %(b)s"> mv'''
imginput = '''<input type="checkbox" name="rm" value="%(f)s"> rm
<input type="text" name="ren.%(f)s"> rename
'''
def LibraryImg(args, base=''):
    print '<tr>'
    args.sort()
    for arg in args:
	root,ext = useful.RootExt(arg.strip())
	inp = ''
	if arg == base:
	    inp = imginputs % {'f':arg,'b':root + 'z.' + ext}
	elif base:
	    inp = imginputs % {'f':arg,'b':base}
	else:
	    inp = imginput % {'f':arg}
	#inp += ' <a href="imawidget.cgi?d=%s&f=%s&cy=0">' % (pif.render.pic_dir, arg) + pif.render.FormatButton('edit') + '</a>'
	inp += ' ' + pif.render.FormatButton('edit', 'imawidget.cgi?d=%s&f=%s&cy=0' % (pif.render.pic_dir, arg))
	inp += ' ' + pif.render.FormatButton('stitch', 'stitch.cgi?fn_0=%s&submit=1&q=&fc=1' % (pif.render.pic_dir + '/' + arg))
	print pif.render.FormatCell(0, '<a href="../%s/%s">%s</a><br>%s%s' % (pif.render.pic_dir, arg, pif.render.FormatImageRequired([root], suffix=ext, also={"border":0}), arg, inp))
    print '</tr>'


def ShowLibraryImgs(pif, patt):
    print '<hr>'
    print '<form action="traverse.cgi" method="post">'
    plist = patt.split(',')
    for pent in plist:
	flist = useful.ReadDir(pent, pif.render.pic_dir)
	flist.sort()
	print '<table>'
	for f in flist:
	    LibraryImg([f])
	print '</table>'
	print '<hr>'
    print '<input type="hidden" name="d" value="%s">' % pif.render.pic_dir
    print '<input type="hidden" name="sc" value="1">'
    print pif.render.FormatButtonInput()
    print '<a href="upload.cgi?d=%s">%s</a>' % (pif.form.get('d', '.'), pif.render.FormatButton('upload'))
    print '</form>'


def ShowLibraryFile(pif, fn):
    if fn.endswith('.dat'):
	ShowLibraryTable(pif, fn)
    else:
	ShowPicture(pif, fn)



colors = ["#FFFFFF", "#CCCCCC"]


import files
class LibraryTableFile(files.ArgFile):
    def __init__(self, fname):
	self.dblist = []
	files.ArgFile.__init__(self, fname)

    def ParseElse(self, llist):
	self.dblist.append(llist)



#print '<a href="/cgi-bin/table.cgi?page=%s">%s</a><br>' % (tdir + '/' + f, f)
def ShowLibraryTable(pif, pagename):
    tablefile = LibraryTableFile(pif.render.pic_dir + '/' + pagename)
    cols = '' # pif.form.get('cols', '')
    h = 0 # pif.FormInt('h')
    sorty = pif.form.get('sort')

    print pif.render.FormatTableStart()
    hdr = ''
    if h:
	hdr = tablefile.dblist[0]
	table = tablefile.dblist[1:]
    else:
	table = tablefile.dblist

    if sorty:
	global sortfield
	sortfield = int(sorty)
	table.sort(lambda x, y: cmp(x[sortfield].lower(), y[sortfield].lower()))

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
	    for ent in range(0,len(hdr)):
		if ent >= len(cols) or cols[ent].lower() != 'n':
		    #print "<th>"+hdr[ent]+"</th>"
		    print '<th bgcolor="#FFFFCC"><a href="table.cgi?page=%s&sort=%d&h=%d&cols=%s">%s</th>' % (pagename, iarg, h, cols, hdr[ent])
		iarg = iarg + 1
	    print "</tr>\n<tr>"
	print '<tr bgcolor="%s">' % colors[irow]
	row = row - 1
	for ent in range(0,len(line)):
	    if ent >= len(cols) or cols[ent].lower() != 'n':
		print "<td>"+line[ent]+"</td>"
	print "</tr>"
    print pif.render.FormatTableEnd()


def DoLibraryAction(pif, tdir, fn, act):
    print '<div class="warning">'
    nfn = Action(pif, tdir, fn, act)
    print '</div><br>'
    if nfn:
	ShowLibraryPicture(pif, nfn)
    else:
	ShowLibraryLibraryDir(pif, tdir, 0)


def LibraryMain(pif):
    os.environ['PATH'] += ':/usr/local/bin'
    pif.render.PrintHtml()
    pif.Restrict('a')
    #pif.render.title = '<a href="traverse.cgi?d=%s">%s</a>' % (pif.form.get("d", '.'), pif.form.get("d", '.'))
    pif.render.title = pif.render.pic_dir = pif.form.get("d", '.')
    pif.render.title += '/' + pif.form.get("f", "")
    graf = pif.FormInt("g")
    fnam = pif.form.get("f", '')
    patt = pif.form.get("p", '')
    cols = pif.FormInt("c", 5)
    act = pif.FormInt('act')
    cycle = pif.FormInt("cy")

    print pif.render.FormatHead(extra=pif.render.increment_js)
    print pif.form
    if patt:
	ShowLibraryImgs(pif, patt)
    elif act:
	DoLibraryAction(pif, pif.render.pic_dir, fnam, act)
    elif fnam:
	ShowLibraryFile(pif, fnam)
    else:
	ShowLibraryDir(pif, pif.render.pic_dir, graf)
    print pif.render.FormatTail()


# -- thumber

def Thumber(pif):
    os.environ['PATH'] += ':/usr/local/bin'

    #pif.Restrict('a')

    print 'Content-Type: image/gif'
    print

    dir = pif.form.get('d', '.')
    fil = pif.form.get('f', '')
    pth = os.path.join(dir, fil)

    x = 100
    outf = PipeChain(open(pth),
	    ImportFile(pth) + \
	    [["/usr/local/bin/pamscale", "-xsize", str(x)]] + \
	    ExportFile('tmp.gif'), stderr=open('/dev/null', 'w'), verbose=False)

    print outf


if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
