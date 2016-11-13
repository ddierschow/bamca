#!/usr/local/bin/python

import datetime, glob, logging, os, re, stat, subprocess, sys, time, traceback, urllib, urllib2
from PIL import Image
import basics
import bfiles
import config
import imglib
import imicon
import javasc
import mbdata
import tumblr
import useful

#os.environ['PATH'] += ':/usr/local/bin'


'''  API
images.image_main
images.imawidget_main
images.library_main
images.pictures_main
images.stitch_main
images.thumber_main
images.upload_main
images.bits_main
'''

descriptions_file = os.path.join(config.LOG_ROOT, 'descr.log')

# -- common

def file_log(fn, tdir):
    #open(os.path.join(config.LOG_ROOT, "file.log"), "a").write('|'.join([fn, tdir, str(config.USER_ID)]) + '\n')
    logging.getLogger('file').info('%s %s' % (tdir, fn))

def upload_log(url, pdir):
    #open(os.path.join(config.LOG_ROOT, 'upload.log'), 'a').write(datetime.datetime.now().strftime('%Y%m%d.%H%M%S') + ' %s %s\n' % (url, pdir))
    logging.getLogger('upload').info('%s %s' % (pdir, url))


# for things out of http space:
#print '<img src="/cgi-bin/image.cgi?d=%s&f=%s">' % (pif.render.pic_dir, fn)
def show_picture(pif, fn, pdir=None):
    if pdir:
	pif.render.pic_dir = pdir
    picker(pif, fn)
    root, ext = useful.root_ext(fn.strip())
    useful.write_comment(root, ext)
    print '<table><tr><td></td><td>' + pif.render.format_image_art('hruler.gif') + '</td></tr>'
    print '<tr><td valign="top">' + pif.render.format_image_art('vruler.gif') + '</td><td valign="top">'
    print '<a href="/cgi-bin/image.cgi?d=%s&f=%s"><img src="/cgi-bin/image.cgi?d=%s&f=%s"></a>' % (pif.render.pic_dir, fn, pif.render.pic_dir, fn)
    print '</td></tr></table>'


def picker(pif, fn):
    cycle = pif.form.get_int('cy')
    root, ext = useful.root_ext(fn.strip())
    print '<a href="?d=%s">%s</a> / ' % (pif.render.pic_dir, pif.render.pic_dir)
    print '<a href="/%s/%s">%s</a>' % (pif.render.pic_dir, fn, fn)
    print '<hr>'
    print '<form action="upload.cgi">'

    imglib.ActionForm(pif).read(pif.form).write(pif, fn)

    print '</form>'
    print '<hr>'


def show_var_info(pif, mod_id, var_id):
    ostr = ''
    if mod_id and var_id:
        var = pif.dbh.fetch_variation(mod_id, var_id)
        if var:
            var = pif.dbh.depref('variation', var[0])
	    ostr += pif.render.format_image_sized(mod_id + '-' + var_id, pdir=config.IMG_DIR_VAR, largest=mbdata.IMG_SIZ_MEDIUM, also={'class': 'righty'})
            ostr += '<br>\n%s:<ul>\n' % var_id
            ostr += '<li>description: %s\n' % var['text_description']
            ostr += '<li>base: %s\n' % var['text_base']
            ostr += '<li>body: %s\n' % var['text_body']
            ostr += '<li>interior: %s\n' % var['text_interior']
            ostr += '<li>wheels: %s\n' % var['text_wheels']
            ostr += '<li>windows: %s\n' % var['text_windows']
            ostr += '</ul><hr>\n'
    return ostr

# -- upload

ebay_start = 'http://thumbs.ebaystatic.com/images/g/'
ebay_end = '/s-l225.jpg'
def grab_url_file(url, pdir, fn='', var='', overwrite=False, desc=''):
    if url.startswith(ebay_start) and url.endswith(ebay_end):
	url = 'http://i.ebayimg.com/images/g/' + url[len(ebay_start):-len(ebay_end)] + '/s-l1600.jpg'
    print url, '<br>'
    # mass_upload doesn't know the filename.
    upload_log(url, pdir)
    try:
        up = urllib2.urlopen(url).read()
    except:
        useful.show_error()
        return "Error encountered!  File not uploaded."
    if not fn:
        fn = url[url.rfind('/') + 1:].lower()
    elif '.' not in fn:
        fn += url[url.rfind('.'):].lower()
    fn = useful.file_save(pdir, fn, up, overwrite)
    file_log(pdir + '/' + fn, pdir)
    return fn


class UploadForm(object):
    def __init__(self):
	pass

    def read(self, pif):
	self.mod_id = pif.form.get_str('m')
	self.var_id = pif.form.get_str('v') if self.mod_id else ''
	pif.render.title = 'upload - '
	pif.render.pic_dir = self.tdir = pif.form.get_str('d')
	if not pif.is_allowed('m'):
	    self.tdir = config.INC_DIR
	elif self.mod_id:
	    self.tdir = os.path.join(config.LIB_MAN_DIR, self.mod_id.lower())
	if self.mod_id:
	    pif.render.title += self.mod_id
	    if self.var_id:
		pif.render.title += ' - ' + self.var_id
	elif pif.is_allowed('vma'):
	    pif.render.title += self.tdir
	else:
	    pif.render.title += 'to BAMCA'
	presets = imglib.read_presets(self.tdir)
	presets['cc'] = self.cc = pif.form.get_str('cc', presets.get('cc', ''))
	imglib.write_presets(self.tdir, presets)
	self.fimage = pif.form.get_str('fi')
	self.fname = pif.form.get_str('fi.name')
	self.url_list = filter(None, [x.strip() for x in pif.form.get_str('ul').split('\n')])
	self.url = pif.form.get_str('u')
	self.urlfn = self.url[self.url.rfind('/') + 1:].lower() if self.url else ''
	if pif.form.get_str('n'):
	    self.nfn = pif.form.get_str('n')
	elif self.urlfn:
	    self.nfn = self.urlfn
	elif self.fname:
	    self.nfn = self.fname
	else:
	    self.nfn = ''
	self.scrape = pif.form.get_str('s')
	self.comment = pif.form.get_str('c')
	self.select = pif.form.get_str('select')
	self.replace = pif.form.get_bool('replace') and pif.is_allowed('ma')
	self.mass = pif.form.get_bool('mass')
	self.act = pif.form.get_int('act')
	self.y = pif.form.get_str('y') # I have no idea what this does.
	return self

    def write(self, pif, restrict=False, desc=''):
	var = pif.dbh.fetch_variation(self.mod_id, self.var_id) if self.mod_id and self.var_id else None
	if var:
	    var = pif.dbh.depref('variation', var[0])
	    var['image'] = pif.render.format_image_sized(self.mod_id + '-' + self.var_id, pdir=config.IMG_DIR_VAR, largest=mbdata.IMG_SIZ_MEDIUM, also={'class': 'righty'})
	context = {
	    'form': self,
	    'restrict': restrict,
	    'desc': desc,
	    'var': var,
	}
	return pif.render.format_template('upload.html', **context)

    def scrape_url_pic(self):
	url = self.scrape
	print '<br>', url, ':', self.tdir, '<br>'
	scrape_re = re.compile(r'''<img src="(?P<img>[^"]*)"''', re.I)
	try:
	    up = urllib2.urlopen(url).read()
	except:
	    useful.show_error()
	    return
	url = url[:url.rfind('/') + 1]
	imgs = scrape_re.findall(up)
	sfn = ''
	for img in imgs:
	    fn = img[img.rfind('/') + 1:]
	    print img, self.tdir, fn, '<br>'
	    if not img.startswith('http://'):
		img = url + '/' + img
	    sfn = grab_url_file(img, self.tdir, fn, self.replace)

	    print '<center><h3>Added: ' + sfn + '</h3><p>'
	    print '<img src="../%s/%s"></center>' % (self.tdir, sfn)

    def grab_url_pic(self, pif):
	fn = grab_url_file(self.url, self.tdir, self.nfn, self.var_id, self.replace)
	return fn

    def calc_filename(self):
	ext = '.jpg'
	pth = self.tdir
	fn = self.nfn
	if self.var_id:
	    fn = (self.mod_id + '-' + self.var_id).lower()
	elif self.mod_id:
	    fn = self.mod_id.lower()
	elif not fn:
	    fn = self.fname[:self.fname.rfind('.')]
	if not fn:
	    fn = 'unknown'
	if not self.replace and os.path.exists(os.path.join(pth, fn + ext)):
	    i = 1
	    while os.path.exists(pth + '/' + fn + '-' + str(i) + ext):
		i = i + 1
	    fn = fn + '-' + str(i)
	return fn + ext

    def save_uploaded_file(self):
	fn = self.calc_filename()
	fn = useful.file_save(self.tdir, fn, self.fimage, self.replace)
	file_log(self.tdir + '/' + fn, self.tdir)
	return fn

    def grab_url_file_list(self):
	for url in self.url_list:
	    grab_url_file(url, self.tdir)
	    sys.stdout.flush()
	print '<hr>'

    def restricted_upload(self, pif):
	print pif.render.format_head()
	useful.header_done()
	direc = config.INC_DIR
	descrips = open(descriptions_file).readlines()
	fn = 1
	if descrips:
	    ln = descrips[-1].split()[0]
	    for iln in range(0, len(ln)):
		if not ln[iln].isdigit():
		    ln = ln[:iln]
		    break
	    fn = int(ln) + 1
	fn = '%09d' % fn
	if self.url:
	    fn = grab_url_file(self.url, direc, fn)
	    print self.thanks(pif, fn)
	elif self.fimage:
	    fn = useful.file_save(direc, fn, self.fimage)
	    file_log(direc + '/' + fn, direc)
	    print self.thanks(pif, fn)
	else:
	    self.write(pif, restrict=True)
	print pif.render.format_tail()

    def thanks(self, pif, fn):
	comment = '-'
	if self.comment:
	    comment = re.compile(r'\s\s*').sub(' ', self.comment)
	open(descriptions_file, 'a+').write('\t'.join([fn,
		self.mod_id if self.mod_id else '-',
		self.var_id if self.var_id else '-',
		self.y if self.y else '-',
		comment]) + '\n')
	ostr = '<div class="warning">Thank you for submitting that file.</div><br>/n'
	ostr += "Unfortunately, you will now have to use your browser's BACK button to get back to where you were, as I have no idea where that was."
	return ostr

    def carbon_copy(self, fn):
	if self.cc:
	    useful.file_mover(os.path.join(self.tdir, fn), os.path.join(self.cc, fn), mv=False, ov=False)

# Product upload:   upload.cgi?d=lib/mattel&n=2015u001&c=2015u001
# Variation upload: upload.cgi?d=lib/man/mb979&m=MB979&v=Y15
@basics.web_page
def upload_main(pif):
    os.environ['PATH'] += ':/usr/local/bin'
    upform = UploadForm().read(pif)

    # These will redirect so let's do them before putting anything out.
    if upform.select:
	raise useful.Redirect('traverse.cgi?g=1&d=%s&man=%s&var=%s' % (upform.tdir, upform.mod_id, upform.var_id))
    elif upform.fimage:
	if not pif.is_allowed('u'):
	    return upform.restricted_upload(pif)
	fn = upform.save_uploaded_file()
	upform.carbon_copy(fn)
	raise useful.Redirect('imawidget.cgi?edit=1&d=%s&f=%s&man=%s&newvar=%s' % (upform.tdir, fn, upform.mod_id, upform.var_id))
    elif upform.url:
	fn = upform.grab_url_pic(pif)
	upform.carbon_copy(fn)
	raise useful.Redirect('imawidget.cgi?edit=1&d=%s&f=%s&man=%s&newvar=%s' % (upform.tdir, fn, upform.mod_id, upform.var_id))

    pif.render.print_html()
    pif.render.set_page_extra(pif.render.reset_button_js + pif.render.increment_js + pif.render.paste_from_clippy_js)
    useful.write_message(str(pif.form.get_form()))
    useful.write_message('<hr>')

    try:
	if upform.url_list:
	    print pif.render.format_head()
	    useful.header_done()
	    print show_var_info(pif, upform.mod_id, upform.var_id)
	    upform.grab_url_file_list()
	    print pif.render.format_tail()
	elif upform.scrape:
	    print pif.render.format_head()
	    useful.header_done()
	    print show_var_info(pif, upform.mod_id, upform.var_id)
	    upform.scrape_url_pic()
	    print pif.render.format_tail()
        else:
	    return upform.write(pif, desc=upform.comment, restrict=not pif.is_allowed('uma'))
    except OSError:
        useful.warn('fail:', traceback.format_exc(0))

# -- imawidget

checked = {True: ' checked', False: ''}
def show_editor(pif, eform, pdir=None, fn=None):
    if not pdir:
	pdir = eform.tdir
    if not fn:
	fn = eform.fn
    full_path = os.path.join(pdir, fn)
    if not os.path.exists(full_path):
        useful.warn('%s not found.' % full_path)
        return

    print '<hr><form action="imawidget.cgi" name="myForm">'
    #imglib.ActionForm(pif).read(pif.form).write(pif, fn)
    x, y = eform.write(pif, pdir, fn)
    full_path = os.path.join(pdir, fn)
    root, ext = useful.root_ext(fn.strip())
    print '<table><tr><td></td><td>' + pif.render.format_image_art('hruler.gif') + '</td></tr>'
    print '<tr><td valign="top">' + pif.render.format_image_art('vruler.gif') + '</td><td valign="top">'
    #print '<a href="../' + full_path + '">' + pif.render.format_image_required([root], suffix=ext, also={"border": "0"}) + '</a>'
    dic = {'file': 'http://' + os.environ['SERVER_NAME'] + '/' + full_path, 'width': x, 'height': y}
    print javasc.def_edit_app % dic
    print '</td></tr></table>'
    print '<input type="hidden" value="%s" name="f">' % fn
    #print '<input type="hidden" value="%s" name="d">' % pdir
    print 'Debug: <span id="ima_debug">Debug output here.</span>'
    print '</form><hr>'



def show_redoer(pif, eform):
    if not eform.repl:
	print '<form action="imawidget.cgi" name="myForm">'
	#print '<input type="text" value="" name="q" id="q">'
	eform.write(pif, edit=False)
	#print 'Bounds:', pif.render.format_text_input('q', 20, value=pif.form.get_str('q'))
	print '<input type="hidden" value="%s" name="f">' % eform.fn
	#print '<input type="hidden" value="%s" name="d">' % eform.tdir
	print '</form>'
	print '<hr>'



class EditForm(imglib.ActionForm):
    def __init__(self, pif, tdir='.', fn=''):
	super(EditForm, self).__init__(pif)
	self.edit = False
	self.fn = fn
	self.ot = ''
	self.pr = False
	self.tdir = tdir
	self.nvar = ''
	self.man = ''
	#self.var = ''
	#self.nname = ''
	self.tysz = ''
	self.xts = 0
	self.yts = 0
	self.unlv = False
	self.unlh = False
	self.rf = []
	self.rl = False
	self.rh = False
	self.rr = False
	self.fh = False
	self.fv = False
	self.keep = False
	self.resize = False
	self.crop = False
	self.shrink = False
	self.wipe = False
	self.pad = False
	self.mass = False
	self.clean = False
	self.repl = False
	self.save = False
	self.cc = ''
	self.original_size = self.xos, self.yos = 0, 0
	q = ''
	self.x1, self.y1, self.x2, self.y2 = self.q = [0, 0, 0, 0]
	self.root, self.ext = '', ''
	self.nname = ''
	self.is_edited = False
	self.set_target_size((self.xts, self.yts))
	self.pth = ''

    def read(self, pif, edit=False):
	super(EditForm, self).read(pif.form)
	self.edit = edit or pif.form.get_bool('edit')
	self.fn = pif.form.get_str("f", '')
	self.ot = pif.form.get_str('ot')
	self.pr = pif.form.get_bool('pr')
	self.tdir = pif.form.get_str("d", '.') if pif.is_allowed('avm') else '.'
	if self.tdir.startswith('./'):
	    self.tdir = self.tdir[2:]
	pif.render.pic_dir = self.tdir
	self.nvar = pif.form.get_str("newvar", '')
	self.man = pif.form.get_str("man")
	if not self.man:
	    self.man = self.calc_man()
	#self.var = pif.form.get_str('v')
	#self.nname = pif.form.get_str("newname")
	self.tysz = pif.form.get_str("tysz", "")
	self.xts = pif.form.get_int('x')
	self.yts = pif.form.get_int('y')
	self.unlv =  pif.form.get_bool('unlv')
	self.unlh =  pif.form.get_bool('unlh')
	self.rf = pif.form.checks(*imglib.rot_flip_keys)
	self.rl = pif.form.get_bool('rl')
	self.rh = pif.form.get_bool('rh')
	self.rr = pif.form.get_bool('rr')
	self.fh = pif.form.get_bool('fh')
	self.fv = pif.form.get_bool('fv')
	self.keep = pif.form.get_bool('keep')
	self.resize = pif.form.get_bool('resize')
	self.crop = pif.form.get_bool('crop')
	self.shrink = pif.form.get_bool('shrink')
	self.wipe = pif.form.get_bool('wipe')
	self.pad = pif.form.get_bool('pad')
	self.mass = pif.form.get_bool('mass')
	self.clean = pif.form.get_bool('clean')
	self.repl = pif.form.get_bool('repl')
	self.save = pif.form.get_bool('save')
	self.cc = pif.form.get_str('cc')
	self.read_file(pif.form.get_str('q'))
	if not self.pref:
	    self.pref = pif.form.get_str('tysz')
	if not self.man:
	    self.man = self.nname[:self.nname.rfind('.')] if '.' in self.nname else self.nname
	    self.man = self.man[2:] if self.man[1] == '_' else self.man
	return self

    def read_file(self, q):
	self.original_size = self.xos, self.yos = imglib.get_size(self.tdir + '/' + self.fn)
	if not q:
	    q = '0,0,%d,%d' % self.original_size
	self.x1, self.y1, self.x2, self.y2 = self.q = [int(x) for x in q.split(',')]

	self.root, self.ext = useful.root_ext(self.fn.strip())
	if self.ot:
	    self.ext = self.ot

	if self.tysz in mbdata.imagesizes:
	    self.xts, self.yts = mbdata.imagesizes[self.tysz]
	if self.wipe:
	    self.tysz = 'w'
	elif self.pad:
	    self.tysz = 'p'
	if not self.nname:
	    self.nname = self.fn
	if '.' in self.nname:
	    self.nname = self.nname[:self.nname.rfind('.')]
	if not self.repl and self.tysz and not self.selcat and not self.rename:
	    self.nname = (self.tysz + '_' + self.nname) if self.pr else (self.nname + '_' + self.tysz)
	if self.ot:
	    self.nname += '.' + self.ot
	else:
	    self.nname += '.jpg'
	self.is_edited = self.nname != self.fn
	self.set_target_size((self.xts, self.yts))
	self.pth = os.path.join(self.tdir, self.fn)

    def set_target_size(self, newts):
	xts, yts = newts
	if self.unlv:
	    yts = 0
	if self.unlh:
	    xts = 0
	self.target_size = self.xts, self.yts = (xts, yts)

    def calc_man(self):
	pdir = self.tdir
#	if pdir.startswith('./'):
#	    pdir = pdir[2:]
	if pdir.endswith('/'):
	    pdir = pdir[:-1]

	man = ''
	if pdir.startswith(config.LIB_MAN_DIR):
	    man = pdir[pdir.rfind('/') + 1:]
	elif pdir.startswith(config.IMG_DIR_PACK):
	    if self.fn:
		if len(self.fn) > 2 and self.fn[1] == '_':
		    man = self.fn[2:-4]
		else:
		    man = self.fn[:-4]
	elif pdir.startswith(config.IMG_DIR_CAT):
	    if self.fn:
		if len(self.fn) > 2 and self.fn[1] == '_':
		    man = self.fn[2:-4]
		else:
		    man = self.fn[:-4]
		if '_' in man:
		    man = man[:man.find('_')]
	return man

    def write(self, pif, pdir=None, fn=None, edit=True):
	if not pdir:
	    pdir = self.tdir
	if not fn:
	    fn = self.fn

	print pif.render.format_link('traverse.cgi?d=%s' % pdir, pdir), '/'
	print pif.render.format_link('traverse.cgi?d=%s&f=%s' % (pdir, fn), fn)
	print pif.render.format_button("show", os.path.join('/', pdir, fn))
	print pif.render.format_button("upload", "upload.cgi?d=%s&n=%s" % (pdir, fn))
	print '<br>'

	full_path = os.path.join(pdir, fn)
	if not os.path.exists(full_path):
	    useful.warn('%s not found.<br>' % full_path)
	    return 0, 0

	presets = imglib.read_presets(pdir)

	xs, ys = super(EditForm, self).write(pif, fn)
	print pif.render.format_hidden_input({'c': urllib.quote_plus(pif.form.get_str('c', ''))})
	#xs, ys = imglib.get_size(full_path)
	if edit:
	    print '<div class="lefty">'
	    #print '(%d, %d)' % (xs, ys)
	    print '<input type="radio" name="tysz" value="q"%s>' % (' checked' if presets.get('tysz') == 'q' else '')
	    print 'x: <input name="x" type="text" size="4" value="%s">' % config.DEFAULT_X_SIZE
	    print 'y: <input name="y" type="text" size="4" value="%s">' % config.DEFAULT_Y_SIZE
	    print ''.join(pif.render.format_radio('tysz', [(siz, siz.upper()) for siz in mbdata.image_size_types], presets.get('tysz', mbdata.IMG_SIZ_SMALL)))
	    print '-', pif.render.format_checkbox("unlv", [(1, "V")], presets.get("unlv", []))
	    print pif.render.format_checkbox("unlh", [(1, "H")], presets.get("unlh", []))
	    print pif.render.format_button_input('keep')
	    print pif.render.format_checkbox("rl", [(1, "RL")], presets.get("rl", []))
	    print pif.render.format_checkbox("rh", [(1, "RH")], presets.get("rh", []))
	    print pif.render.format_checkbox("rr", [(1, "RR")], presets.get("rr", []))
	    print pif.render.format_checkbox("fh", [(1, "FH")], presets.get("fh", []))
	    print pif.render.format_checkbox("fv", [(1, "FV")], presets.get("fv", []))
	    print pif.render.format_select('ot', imglib.otypes, 'jpg')
	    print pif.render.format_checkbox("pr", [(1, "pr")], presets.get("pr", []))
	    print '<br>'
	    #print 'Name:', pif.render.format_text_input('newname', 20, value=pif.form.get_str('newname', ''))
	    print pif.render.format_button_input('resize')
	    print pif.render.format_button_input('crop')
	    print pif.render.format_button_input('crop and shrink', 'shrink')
	    print pif.render.format_button_input('wipe')
	    print pif.render.format_button_input('pad')
	    #if pif.is_allowed('m'):  # pragma: no cover
		#print 'Var: ' + pif.render.format_text_input('v', 8, value=pif.form.get_str('v', ''))
	    print pif.render.format_checkbox("repl", [(1, "Replace")], presets.get("repl", []))
	    print pif.render.format_checkbox("save", [(1, "Save")], presets.get("save", []))
	print pif.render.format_button_input('mass')
	print pif.render.format_button_input('clean')
	print '- Bounds: <input type="text" value="%s" name="q" id="q"> <span id="ima_info"></span>' % ','.join([str(x) for x in self.q])
	print pif.render.format_hidden_input({'cc': presets.get('cc', '')})
	return xs, ys

    def save_file(self, ofi):
	nname = self.nname
	if nname:
	    if '.' not in nname:
		nname = nname + self.fn[self.fn.rfind('.'):]
	else:
	    if '.' in self.fn:
		nname = self.fn[:self.fn.rfind('.')] + '_s' + self.fn[self.fn.rfind('.'):]
	    else:
		nname = self.fn + '_s'
	pth = os.path.join(self.tdir, nname)
	if isinstance(ofi, Image.Image):
	    ofi.save(pth)
	else:
	    open(pth, "w").write(ofi)
	file_log(nname, self.tdir)
	print 'saving to', pth, '(%d, %d)<br>' % (imglib.get_size(pth))
	return nname

    def save_presets(self):
	if self.save and os.path.exists(os.path.join(self.tdir, '.ima')):
	    presets = {
		"unlv": [int(self.unlv)],
		"unlh": [int(self.unlh)],
		"rl": [int(self.rl)],
		"rh": [int(self.rh)],
		"rr": [int(self.rr)],
		"fh": [int(self.fh)],
		"fv": [int(self.fv)],
		"pr": [int(self.pr)],
		"repl": [int(self.repl)],
		"tysz": self.tysz,
		"cc": self.cc,
		"ov": self.ov,
		"cpmv": self.cpmv,
	    }
	    imglib.write_presets(self.tdir, presets)
	    #open(os.path.join(self.tdir, '.ima'), 'w').write(str(presets))

    def shape_image(self):
	print 'shape_image', self.pth, self.nname, self.q, self.target_size, self.original_size, self.rf, '<br>'
	ofi = imglib.shaper(self.pth, self.nname, self.q, self.target_size, self.original_size, self.rf)
	return self.save_file(ofi)

    def shrink_image(self):
	ofi = imglib.shrinker(self.pth, self.nname, self.q, self.target_size, self.rf)
	return self.save_file(ofi)

    def crop_image(self):
	ofi = imglib.cropper(self.pth, self.nname, self.q, self.rf)
	return self.save_file(ofi)

    def wipe_image(self):
	ofi = imglib.wiper(self.pth, self.q, self.original_size, self.unlv, self.unlh)
	return self.save_file(ofi)

    def pad_image(self):
	ofi = imglib.padder(self.pth, self.target_size)
	return self.save_file(ofi)

    def mass_clean(self):
	print 'mass_clean', self.pth, '<hr>'
	nname_root = self.fn
	if '.' in nname_root:
	    nname_root = nname_root[:nname_root.rfind('.')]
	for pref in [mbdata.IMG_SIZ_TINY, mbdata.IMG_SIZ_SMALL, mbdata.IMG_SIZ_MEDIUM, mbdata.IMG_SIZ_LARGE]:
	    nname = nname_root + '_' + pref + ('.' + self.ot) if self.ot else ''
	    useful.file_delete(os.path.join(self.tdir, nname))

    def mass_resize(self, desc=''):
	print self.__dict__, '<br>'
	var = self.var.lower()
	man = self.man.lower()
	print 'mass_resize', 'pth', self.pth, 'tdir "%s"' % self.tdir, 'fn', self.fn, 'ot', self.ot, 'os', self.original_size, '|', man, var, '<hr>'

	nname_root = self.man if self.man else self.fn
	if self.suff:
	    nname_root += '-' + self.suff
	if len(nname_root) > 2 and nname_root[0] in mbdata.image_size_types and nname_root[1] == '_':
	    nname_root = nname_root[2:]
	if '.' in nname_root:
	    nname_root = nname_root[:nname_root.rfind('.')]
	xos, yos = self.original_size

	ot = '.' + self.ot if self.ot else self.fn[self.fn.rfind('.') + 1:]
	ddir = self.dest if self.dest else self.tdir
	outnam = '_' + nname_root + ot
	if self.dest == config.IMG_DIR_PACK or self.tdir == config.IMG_DIR_PACK: # or self.tdir == './' + config.IMG_DIR_PACK:
	    prefs = 'scmlh'
	elif self.dest == config.IMG_DIR_BOX or self.tdir == config.IMG_DIR_BOX:
	    prefs = 'scm'
	else:
	    ddir = (config.IMG_DIR_VAR if var else config.IMG_DIR_MAN)
	    prefs = 'tsml'
	    outnam = '_' + man + ('-' + var if var else '') + ot

	largest = None
	for pref in prefs:
	    if xos < mbdata.imagesizes[pref][0]:
		break
	    self.nname = nname_root + '_' + pref + ot
	    self.set_target_size(mbdata.imagesizes[pref])
	    dnam = pref + outnam
	    dpth = os.path.join(ddir, dnam)
	    print 'resizing', self.tdir, self.nname, 'to', dpth, '<br>'
	    if self.unlv and self.unlh:
		nname = self.crop_image()
	    elif self.unlv or self.unlh:
		nname = self.shrink_image()
	    else:
		nname = self.shape_image()
	    useful.file_mover(os.path.join(self.tdir, nname), dpth, mv=True, ov=True)
	    largest = dpth
	    print '<br><img src="/%s"><hr>' % dpth

	if self.mv:
	    useful.file_delete(self.pth, True)

	return largest


@basics.web_page
def imawidget_main(pif):
    pif.render.print_html()
    pif.restrict('v')

    eform = EditForm(pif).read(pif)

    pif.render.title = pif.render.pagetitle = pif.render.pic_dir + '/' + eform.fn
    pif.render.set_page_extra(pif.render.increment_js)
    print pif.render.format_head()
    useful.header_done()

    if not pif.is_allowed('ma'):
	print pif.render.format_image_required(eform.fn)
	return

    if eform.fn and os.path.exists(os.path.join(eform.tdir, 'descr.log')):
	# This is for /inc!  If I delete it again, I'll be pissed.
        descs = open(os.path.join(eform.tdir, 'descr.log')).readlines()
        descs = dict([x.strip().split('\t', 1) for x in descs])
        # mod_id, var_id, year, comment
        print descs.get(os.path.splitext(eform.fn)[0], '').replace('\t', '<br>')
        print '<hr>'

    if eform.keep:
        picker(pif, eform.fn)
        print pif.render.format_image_required([eform.fn[:eform.fn.rfind('.')]], suffix=eform.fn[eform.fn.rfind('.') + 1:], also={"border": "0"}), '<br>'
        print pif.render.format_tail()
        return

    print show_var_info(pif, eform.man, eform.var)

    is_edited = eform.is_edited
    try:
	found = eform.action(pif)
	if found['act']:
	    nfn = found['fn']
	    if os.path.exists(nfn):
		pass
	    elif eform.cycle:
		#dl, gl, ol, sl, xl = imglib.get_dir(eform.tdir)
		files = imglib.get_dir(tdir)
		while files['graf']:
		    if files['graf'][0] == nfn:
			files['graf'].pop()
		    else:
			nfn = files['graf'][0]
			break
	    if nfn:
		#show_picture(pif, nfn)
		print pif.render.format_link('traverse.cgi?d=%s' % eform.tdir, eform.tdir), '/'
		print pif.render.format_link('traverse.cgi?d=%s&f=%s' % (eform.tdir, eform.fn), eform.fn), '<br>'
	    else:
		print pif.render.format_link('traverse.cgi?d=%s' % eform.tdir, eform.tdir), '/'

        elif eform.clean:
            eform.mass_clean()
	    show_editor(pif, eform)
        elif eform.mass:
            largest = eform.mass_resize("from library")
            if eform.man and eform.var:
                print pif.render.format_button("promote", 'vars.cgi?mod=%s&var=%s&promote=1' % (eform.man, eform.var))
	    if largest:# and log_action:
		title = pif.form.get_str('title', '%s-%s' % (eform.man, eform.var))
		url = 'http://www.bamca.org/' + largest
		link = 'http://www.bamca.org/cgi-bin/vars.cgi?mod=%s&var=%s' % (eform.man, eform.var)
		useful.write_message('Post to Tumblr: ', tumblr.tumblr(pif).create_photo(caption=title, source=url, link=link))
        elif eform.wipe:
            eform.save_presets()
            eform.fn = eform.wipe_image()
	    show_editor(pif, eform)
        elif eform.pad:
            eform.save_presets()
            eform.fn = eform.pad_image()
	    show_editor(pif, eform)
        elif eform.resize:
            eform.save_presets()
            eform.fn = eform.shape_image()
	    #show_redoer(pif, eform)
	    #print pif.render.format_image_required([eform.fn], also={"border": "0"}), '<br>'
            show_editor(pif, eform)
        elif eform.crop:
            eform.save_presets()
            eform.fn = eform.crop_image()
	    #show_redoer(pif, eform)
	    #print pif.render.format_image_required([eform.fn], also={"border": "0"}), '<br>'
            show_editor(pif, eform)
        elif eform.shrink:
            eform.save_presets()
            eform.fn = eform.shrink_image()
	    #show_redoer(pif, eform)
	    #print pif.render.format_image_required([eform.fn], also={"border": "0"}), '<br>'
            show_editor(pif, eform)
        else:
            show_editor(pif, eform)
            is_edited = False
    except:
        useful.show_error()
	is_edited = False

    if is_edited:
        print pif.render.format_button('replace', 'upload.cgi?act=1&d=%s&f=%s&newname=%s&rename=1&cpmv=m&ov=1' % (eform.tdir, eform.nname, eform.fn))

    print pif.render.format_tail()


# -- stitch


class StitchForm(object):
    def __init__(self, verbose=False):
	self.verbose = verbose
	super(StitchForm, self).__init__()

    def read(self, pif):
	self.file_count = pif.form.get_int('fc')
	self.fsl = list()
	for file_num in range(0, self.file_count + 1):
	    fs = dict()
	    if pif.form.has('fn_%d' % file_num):
		fs['fn'] = pif.form.get_str('fn_%d' % file_num)
	    fs['n'] = '%d' % file_num
	    if file_num < self.file_count - 2:
		fs['x1'] = pif.form.get_int('x1_%d' % file_num)
		fs['y1'] = pif.form.get_int('y1_%d' % file_num)
		fs['x2'] = pif.form.get_int('x2_%d' % file_num)
		fs['y2'] = pif.form.get_int('y2_%d' % file_num)
	    elif file_num == self.file_count - 2:
		if pif.form.get_str('q') != '':
		    fs['x1'], fs['y1'], fs['x2'], fs['y2'] = [int(x) for x in pif.form.get_str('q').split(',')]
		else:
		    fs['x1'] = fs['y1'] = 0
		    fs['x2'], fs['y2'] = imglib.get_size(fs['fn'])
	    elif file_num == self.file_count - 1:
		if fs.get('fn', '').startswith('http://'):
		    fs['fn'] = fs['fn'][fs['fn'].find('/', 7) + 1:]
	    if self.verbose:
		print file_num, fs, '<br>'
	    self.fsl.append(fs)
	self.limit_x = pif.form.get_int('limit_x', 999999)
	self.limit_y = pif.form.get_int('limit_y', 999999)
	self.finish = pif.form.has('finish')
	self.finalize = pif.form.has('finalize')
	self.in_list = pif.form.get_list('in')
	self.src_dir = pif.form.get_str('f')
	self.dst_dir = pif.form.get_str('o')
	return self

    def write(self, pif):
	header = str(self.fsl) + '<br>'

	header += '''<form action="stitch.cgi" name="myForm" onSubmit="return getValueFromApplet()">\n'''
	header += pif.render.format_hidden_input({'fc': self.file_count + 1})
	columns = ['name', 'image']
	print header
	print pif.render.format_table_start()
	entries = []
	for fs in self.fsl:
	    print pif.render.format_row_start()
	    num = fs['n']
	    fn = fs.get('fn', '').strip()
	    fn_size = ''
	    if fn:
		if 'x1' not in fs and os.path.exists(fn):
		    x, y = imglib.get_size(fn)
		    self.limit_x = min(x, self.limit_x)
		    self.limit_y = min(y, self.limit_y)
		    fn_size = '<br>' + str((x, y))
		print pif.render.format_cell(1, fn + fn_size)
		print pif.render.format_hidden_input({'fn_' + num: fn})
	    else:
		print pif.render.format_cell(1, pif.render.format_text_input('fn_%d' % self.file_count, 80) + '<br>' + self.fsl[0]['fn'].strip())
		print pif.render.format_cell(1, pif.render.format_button_input() + ' ' +
		    pif.render.format_button_input('finalize') + '<br>' +
		    pif.render.format_checkbox('or', [('h', 'horizontal')]),
			also={'colspan': 2})
		print pif.render.format_cell(1, 'x ' + pif.render.format_text_input('limit_x', 5, value=self.limit_x))
		print pif.render.format_cell(1, 'y ' + pif.render.format_text_input('limit_y', 5, value=self.limit_y))
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
		    print pif.render.format_cell(1, self.show_widget(fn), also={'colspan': 4})
	    print pif.render.format_row_end()
	print pif.render.format_table_end()
	footer = '<input type="text" value="" name="q" id="q"><br>\n'  # for imawidget
	footer += 'Debug: <span id="ima_debug">Debug output here.</span>\n'
	footer += '</form>'
	print footer

    def show_widget(self, filepath):
	x, y = imglib.get_size(filepath)
	dic = {'file': 'http://' + os.environ['SERVER_NAME'] + '/' + filepath, 'width': x, 'height': y}
	return javasc.def_edit_app % dic

    def finish_picture(self, pif):
	print pif.form.get_form(), '<hr>'
	for fn in pif.form.get_list('in'):
	    useful.file_mover(fn, os.path.join(config.TRASH_DIR, fn[fn.rfind('/') + 1:]), mv=True, inc=True, trash=False)
	useful.file_mover(pif.form.get_str('f'), pif.form.get_str('o'), mv=True, ov=True)

    def perform(self, pif):
	if pif.form.has('finish'):
	    self.finish_picture(pif)
	elif pif.form.has('finalize'):
	    self.finalize_picture(pif)
	else:
	    self.write(pif)
	return self

    def finalize_picture(self, pif):
	final = self.fsl[-2].get('fn', '').strip()
	if not final:
	    final = self.fsl[0]['fn'].rsplit('.', 1)
	    final = final[0] + '_st.' + final[1]
	self.fsl = self.fsl[:-2]

	fa = list()
	minx = miny = None
	print pif.render.format_table_start()
	input_files = list()
	for fs in self.fsl:
	    print pif.render.format_row_start()
	    img = fs['fn']
	    input_files.append(img)
	    crop_l = int(fs['x1'])
	    crop_r = int(fs['x2'])
	    crop_t = int(fs['y1'])
	    crop_b = int(fs['y2'])
	    x, y = imglib.get_size(img)
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
	imglib.stitcher(final, fa, pif.form.get_str('or') == 'h', minx, miny, self.limit_x, self.limit_y, verbose=False)
	time.sleep(2)
	print '... Finished.<br>'
	sys.stdout.flush()
	#print '<a href="../' + final + '">' + final + '<br>'
	#print '<img src="../' + final + '"></a>'
	d, f = os.path.split(final)
	show_picture(pif, f, d)
	orig = input_files[0][input_files[0].rfind('/') + 1:]
	print '<br><form>Final resting place:'
	print pif.render.format_text_input('o', 80, value='%s' % input_files[0])
	print pif.render.format_hidden_input({'f': '%s/%s' % (d, f)})
	for fn in input_files:
	    print pif.render.format_hidden_input({'in': fn})
	print pif.render.format_button_input('finish')
	print '</form>'


@basics.web_page
def stitch_main(pif, verbose=False):
    pif.render.print_html()

    if 1:
	pif.render.title = 'stitch'
	print pif.render.format_head()
	useful.header_done()

	StitchForm(verbose).read(pif).perform(pif)

	print pif.render.format_tail()
    else:
	return pif.render.format_template('stitch.html', StitchForm(verbose).read(pif).perform(pif))

# -- pictures

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
    pif.render.title = 'pictures - ' + pif.form.get_str('m', '')
    print pif.render.format_head()
    useful.header_done()
    mod_id = pif.form.get_str('m', '')
    if mod_id:
        [casting_pictures(pif, mod_id.lower(), x) for x in [config.IMG_DIR_MAN, config.IMG_DIR_VAR, config.IMG_DIR_ICON, config.IMG_DIR_ADD]]
        lineup_pictures(pif, pif.dbh.fetch_casting_lineups(mod_id))
    else:
        print 'Huh?'
    print pif.render.format_tail()


# -- icon

# understands 0-9 A-Z & ' + - .  /

def create_icon(mod_id, name, logo, isizex=100, isizey=100):
    print ' ', mod_id, '|'.join(name)

    #logo = logo if logo else pif.render.find_art('mb2')

    in_path = os.path.join(config.IMG_DIR_MAN, 's_' + mod_id + '.jpg')
    icon_file = os.path.join(config.IMG_DIR_ICON, 'i_' + mod_id + '.gif')
    open(icon_file, 'w').write(imglib.iconner(in_path, name, logo=None, isizex=100, isizey=100))


def get_man_dict(pif):
    manlist = pif.dbh.fetch_casting_list()
    mans = dict()
    for llist in manlist:
        llist = pif.dbh.modify_man_item(llist)
        mans[llist['id'].lower()] = llist
    return mans


@basics.command_line
def icon_main(pif):

    title = pif.switch['b'][-1] if pif.switch['b'] else 'mb2'
    logo = pif.render.find_art(title)
    mandict = pif.dbh.fetch_casting_dict(pif)

    if pif.switch['a']:
        for man in mandict:
            name = mandict[man]['iconname']
            if pif.switch['n']:
                name = pif.switch['n'][-1].split(';')
            create_icon(man, name, logo)
    elif pif.filelist:
        for man in pif.filelist:
	    man = man.lower()
            if man in mandict:
                name = mandict[man]['iconname']
                if pif.switch['n']:
                    name = pif.switch['n'][-1].split(';')
                create_icon(man, name, logo)
	    else:
		print man, 'not in list'
    else:
        print 'huh?'  # print mandict

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

    yearlist = sorted(years.keys())

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
    cols = pif.form.get_int("c", 5)
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
            elif ext in imglib.itypes:
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
        if root[-2] == '_' and root[-1] in mbdata.image_size_types:
            root = root[:-2]
        fd.setdefault(root, [])
        fd[root].append(f)

    print '<table>'
    for root in sorted(fd.keys()):
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

    #dl, gl, ol, sl, xl = imglib.get_dir(tdir)
    files = imglib.get_dir(tdir)

    show_library_list(pif, files['titles']['dat'], tdir, files['dat'])
    if grafs:
        show_library_graf(files['titles']['graf'], tdir, files['graf'])
    else:
        show_library_list(pif, files['titles']['graf'], tdir, files['graf'])
    show_library_list(pif, files['titles']['dat'], tdir, files['dat'])
    show_library_list(pif, files['titles']['exe'], tdir, files['exe'])
    show_library_list(pif, files['titles']['other'], tdir, files['other'])

    print '<a href="upload.cgi?d=%s&m=%s">%s</a>' % (tdir, tdir[7:], pif.render.format_button('upload'))

    if files['graf']:
        print '<form action="traverse.cgi">'
        print '<a href="traverse.cgi?g=1&d=%s">%s</a> or ' % (tdir, pif.render.format_button('show all pictures'))
        print 'Pattern <input type="text" name="p">'
        print '<input type="hidden" name="d" value="%s">' % tdir
        print pif.render.format_button_input()
        print '</form>'



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
    #print '<input type="hidden" name="pre" value="man">'
    print pif.render.format_button_input()
    print '<a href="upload.cgi?d=%s&r=1">%s</a>' % (pif.form.get_str('d', '.'), pif.render.format_button('upload'))
    print '</form>'


# not functional and not in use
def show_library_file(pif, fn):
    if fn.endswith('.dat'):
        show_library_table(pif, fn)
    else:
        show_picture(pif, fn)



colors = ["#FFFFFF", "#CCCCCC"]


#print '<a href="/cgi-bin/table.cgi?page=%s">%s</a><br>' % (tdir + '/' + f, f)
def show_library_table(pif, pagename):
    tablefile = bfiles.SimpleFile(pif.render.pic_dir + '/' + pagename)
    cols = ''  # pif.form.get_str('cols', '')
    h = 0  # pif.form.get_int('h')
    sorty = pif.form.get_str('sort')

    print '<table>'
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
    print '</table>'


def do_library_action(pif, tdir, fn, act):
    print '<div class="warning">'
    nfn = imglib.ActionForm(pif).action(pif, tdir, fn)
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
    #pif.render.title = '<a href="traverse.cgi?d=%s">%s</a>' % (pif.form.get_str("d", '.'), pif.form.get_str("d", '.'))
    pif.render.title = pif.render.pic_dir = pif.form.get_str("d", '.')
    pif.render.title += '/' + pif.form.get_str("f", "")
    graf = pif.form.get_int("g")
    fnam = pif.form.get_str("f", '')
    patt = pif.form.get_str("p", '')
    cols = pif.form.get_int("c", 5)
    act = pif.form.get_int('act')
    cycle = pif.form.get_int("cy")

    pif.render.set_page_extra(pif.render.increment_js)
    print pif.render.format_head()
    useful.header_done()
    print pif.form.get_form()
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
def image_main(pif):
    fpath = os.path.join(pif.form.get_str('d', '.'), pif.form.get_str('f', ''))
    if not os.path.exists(fpath):
	raise useful.SimpleError(fpath + ' does not exist')
    print 'Content-Type: image/jpeg\n'
    print open(os.path.join(pif.form.get_str('d', '.'), pif.form.get_str('f', '')), "rb").read()


# -- thumber

@basics.web_page
def thumber_main(pif):
    os.environ['PATH'] += ':/usr/local/bin'

    #pif.restrict('a')

    print 'Content-Type: image/gif'
    print

    dir = pif.form.get_str('d', '.')
    fil = pif.form.get_str('f', '')
    pth = os.path.join(dir, fil)

    x = 100
    outf = imglib.pipe_chain(open(pth),
            imglib.import_file(pth) +
            [["/usr/local/bin/pamscale", "-xsize", str(x)]] +
            imglib.export_file('tmp.gif'), stderr=open('/dev/null', 'w'), verbose=False)

    print outf


if __name__ == '__main__':  # pragma: no cover
    icon_main(switches='av', options='bn')
