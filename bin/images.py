#!/usr/local/bin/python

import glob
from io import open
import logging
import os
import re
import requests
import stat
import sys
import time
import traceback

import basics
import bfiles
import config
import imglib
import javasc
import mbdata
import render
import tumblr
import useful

# os.environ['PATH'] += ':/usr/local/bin'


'''  API
images.EditForm
images.grab_url_file
images.image_main
images.imawidget_main
images.library_main
images.photographers
images.pictures_main
images.stitch_main
images.thumber_main
images.upload_main
images.bits_main
'''

descriptions_file = os.path.join(config.LOG_ROOT, 'descr.log')

auto_credits = [
    ('mbx-u.com', 'MBXU'),
    ('publicsafetydiecast.com', 'PSDC'),
    ('chezbois.com', 'LW'),
    ('cfalkensteiner.com', 'CF'),
    ('vintagediecasttoys.com', 'AT'),
]


# -- common


def file_log(fn, tdir):
    # open(os.path.join(config.LOG_ROOT, "file.log"), "a").write('|'.join([fn, tdir, str(config.USER_ID)]) + '\n')
    logging.getLogger('file').info(f'{tdir} {fn}')


def upload_log(url, pdir):
    logging.getLogger('upload').info('{pdir} {url}')


def get_next_upload_filename():
    descrips = open(descriptions_file).readlines()
    fn = 1
    if descrips:
        fn = len(descrips) + 1
        # ln = descrips[-1].split()[0]
        # for iln in range(0, len(ln)):
        #     if not ln[iln].isdigit():
        #         ln = ln[:iln]
        #         break
        # fn = int(ln) + 1
    return '%09d' % fn


# for things out of http space:
# print('<img src="/cgi-bin/image.cgi?d=%s&f=%s">' % (pif.render.pic_dir, fn))
def show_picture(pif, fn, pdir=None):
    if pdir:
        pif.render.pic_dir = pdir
    picker(pif, fn)
    root, ext = useful.root_ext(fn.strip())
    useful.write_comment(root, ext)
    print('<table><tr><td></td><td>' + pif.render.format_image_art('hruler.gif') + '</td></tr>')
    print('<tr><td valign="top">' + pif.render.format_image_art('vruler.gif') + '</td><td valign="top">')
    print('<a href="/cgi-bin/image.cgi?d=%s&f=%s"><img src="/cgi-bin/image.cgi?d=%s&f=%s"></a>' % (
        pif.render.pic_dir, fn, pif.render.pic_dir, fn))
    print('</td></tr></table>')


def picker(pif, fn):
    # cycle = pif.form.get_int('cy')
    root, ext = useful.root_ext(fn.strip())
    print('<a href="?d=%s">%s</a> / ' % (pif.render.pic_dir, pif.render.pic_dir))
    print('<a href="/%s/%s">%s</a>' % (pif.render.pic_dir, fn, fn))
    print('<hr>')
    print('<form action="upload.cgi">' + pif.create_token())

    imglib.ActionForm(pif).read(pif.form).write(pif, fn)

    print('</form>')
    print('<hr>')


def show_var_info(pif, mod_id, var_id):
    ostr = ''
    if mod_id and var_id:
        var = pif.dbh.fetch_variation(mod_id, var_id)
        if var:
            var = pif.dbh.depref('variation', var)
            ostr += pif.render.format_image_sized(
                mod_id + '-' + var_id, pdir='.' + config.IMG_DIR_VAR,
                largest=mbdata.IMG_SIZ_MEDIUM, also={'class': 'righty'})
            ostr += '<br>\n%s:<ul>\n' % var_id
            ostr += '<li>description: %s\n' % var['text_description']
            ostr += '<li>base: %s\n' % var['text_base']
            ostr += '<li>body: %s\n' % var['text_body']
            ostr += '<li>interior: %s\n' % var['text_interior']
            ostr += '<li>wheels: %s\n' % var['text_wheels']
            ostr += '<li>windows: %s\n' % var['text_windows']
            ostr += '<li>with: %s\n' % var['text_with']
            ostr += '<li>note: %s %s\n' % (var['note'], var['date'])
            ostr += '</ul><hr>\n'
    return ostr


# -- upload


ebay_starts = [
    'http://thumbs.ebaystatic.com/images/g/',
    'https://i.ebayimg.com/thumbs/images/g/',
    'http://i.ebayimg.com/images/g/',
]
ebay_ends = [
    '/s-l225.jpg',
    '/s-l300.jpg',
    '/s-l64.jpg',
]


def grab_url_file(url, pdir, fn='', var='', overwrite=False, desc=''):
    url = url.strip()
    found = False
    for ebay_start in ebay_starts:
        for ebay_end in ebay_ends:
            if url.startswith(ebay_start) and url.endswith(ebay_end):
                url = 'http://i.ebayimg.com/images/g/' + url[len(ebay_start):-len(ebay_end)] + '/s-l1600.jpg'
                found = True
                break
        if found:
            break
    useful.write_message(url, '<br>')
    # mass_upload doesn't know the filename.
    upload_log(url, pdir)
    useful.write_message("Attempting upload...", url, '<br>')
    try:
        up = requests.get(url).content
    except Exception as e:
        if useful.is_header_done():
            useful.show_error()
        return "Error encountered!  File not uploaded. ({})".format(e)
    if not fn:
        fn = url[url.rfind('/') + 1:].lower()
    elif '.' not in fn:
        fn += url[url.rfind('.'):].lower()
    if '?' in fn:
        fn = fn[:fn.find('?')]
    fn = useful.file_save(pdir, fn, up, overwrite)
    file_log(pdir + '/' + fn, pdir)
    return fn


class UploadForm(object):
    def __init__(self):
        pass

    def read(self, pif):
        self.mod_id = pif.form.get_id('m')
        self.var_id = pif.form.get_id('v') if self.mod_id else ''
        pif.render.title = 'upload - '
        pif.render.pic_dir = self.tdir = pif.form.get_id('d')
        if not pif.is_allowed('m'):
            self.tdir = config.INC_DIR
        elif self.mod_id:
            self.tdir = useful.relpath('.', config.LIB_MAN_DIR, self.mod_id.lower())
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
        self.fimage = pif.form.get('fi')
        self.fname = pif.form.get_str('fi.name')
        self.url_list = [x.strip() for x in pif.form.get_str('ul').split('\n') if x]
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
        self.suffix = pif.form.get_str('suff')
        self.scrape = pif.form.get_str('s')
        self.comment = pif.form.get_str('c')
        self.who = pif.form.get_str('who')
        self.cred = pif.form.get_str('cred')
        self.select = pif.form.get_str('select')
        self.selsearch = pif.form.get_str('selsearch')
        self.replace = pif.form.get_bool('replace') and pif.is_allowed('ma')
        self.mass = pif.form.get_exists('mass')
        self.act = pif.form.get_int('act')
        self.y = pif.form.get_str('y')  # I have no idea what this does.
        image = pif.render.find_image_file(self.nfn, pdir=self.tdir.replace('lib', 'pic'), largest='e')
        self.image = image if image else None
        return self

    def write(self, pif, restrict=False, desc=''):
        var = pif.dbh.fetch_variation(self.mod_id, self.var_id) if self.mod_id and self.var_id else None
        if var:
            var = pif.dbh.depref('variation', var)
            var['image'] = pif.render.format_image_sized(
                self.mod_id + '-' + self.var_id, pdir='.' + config.IMG_DIR_VAR, largest=mbdata.IMG_SIZ_MEDIUM,
                also={'class': 'righty'})
        context = {
            'form': self,
            'restrict': restrict,
            'desc': desc,
            'var': var,
            'edit': pif.render.format_button_link('edit', 'imawidget.cgi?d=%s&f=%s' % self.image) if self.image else '',
        }
        return pif.render.format_template('upload.html', **context)

    def scrape_url_pic(self):
        url = self.scrape
        print('<br>', url, ':', self.tdir, '<br>')
        scrape_re = re.compile(r'''<img src="(?P<img>[^"]*)"''', re.I)
        try:
            up = requests.get(url).text
        except Exception:
            useful.show_error()
            return
        url = url[:url.rfind('/') + 1]
        imgs = scrape_re.findall(up)
        sfn = ''
        for img in imgs:
            fn = img[img.rfind('/') + 1:]
            print(img, self.tdir, fn, '<br>')
            if not img.startswith('http://'):
                img = url + '/' + img
            sfn = grab_url_file(img, self.tdir, fn, overwrite=self.replace)

            print('<center><h3>Added: ' + sfn + '</h3><p>')
            print('<img src="../%s/%s"></center>' % (self.tdir, sfn))

    def grab_url_pic(self, pif):
        fn = grab_url_file(self.url, self.tdir, self.nfn, self.var_id, overwrite=self.replace)
        return fn

    def calc_filename(self):
        ext = '.jpg'
        pth = self.tdir
        fn = 'unknown'
        if self.nfn:
            fn = self.nfn
        elif self.var_id:
            fn = (self.mod_id + '-' + self.var_id).lower()
        elif self.mod_id:
            fn = self.mod_id.lower()
        elif not fn:
            fn = self.fname[:self.fname.rfind('.')]
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
        print('<hr>')

    def restricted_upload(self, pif):
        print(pif.render.format_head())
        direc = config.INC_DIR
        useful.header_done()
        fn = get_next_upload_filename()
        if self.url:
            fn = grab_url_file(self.url, direc, fn)
            print(self.thanks(pif, fn))
        elif self.fimage:
            fn = useful.file_save(direc, fn, self.fimage)
            file_log(direc + '/' + fn, direc)
            print(self.thanks(pif, fn))
        else:
            self.write(pif, restrict=True)
        print(pif.render.format_tail())

    def thanks(self, pif, fn):
        cred = who = comment = '-'
        if self.comment:
            comment = re.compile(r'\s\s*').sub(' ', self.comment)
        if self.cred:
            cred = re.compile(r'\s\s*').sub(' ', self.cred)
        if self.who:
            who = re.compile(r'\s\s*').sub(' ', self.who)
        open(descriptions_file, 'a+').write('\t'.join(
            [fn,
             self.mod_id if self.mod_id else '-',
             self.var_id if self.var_id else '-',
             self.y if self.y else '-',
             comment, cred, who]) + '\n')
        ostr = ('<div class="warning">Thank you for submitting that file.</div><br>\n'
                "Unfortunately, you will now have to use your browser's BACK button to get back to where you were, "
                "as I have no idea where that was.")
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
        raise useful.Redirect('traverse.cgi?g=1&d=%s&man=%s&var=%s&suff=%s&has=%s' % (
            upform.tdir, upform.mod_id, upform.var_id, upform.suffix, upform.selsearch))
    elif upform.fimage:
        if not pif.is_allowed('u'):
            pif.render.print_html()
            return upform.restricted_upload(pif)
        fn = upform.save_uploaded_file()
        upform.carbon_copy(fn)
        raise useful.Redirect('imawidget.cgi?edit=1&d=%s&f=%s&man=%s&newvar=%s&suff=%s&credit=%s' % (
            upform.tdir, fn, upform.mod_id, upform.var_id, upform.suffix, ''))
    elif upform.url:
        credit = ''
        for ac in auto_credits:
            if ac[0] in upform.url:
                credit = ac[1]
                break
        fn = upform.grab_url_pic(pif)
        upform.carbon_copy(fn)
        raise useful.Redirect('imawidget.cgi?edit=1&d=%s&f=%s&man=%s&newvar=%s&suff=%s&credit=%s' % (
            upform.tdir, fn, upform.mod_id, upform.var_id, upform.suffix, credit))

    pif.render.print_html()
    pif.render.set_page_extra(pif.render.reset_button_js + pif.render.increment_js + pif.render.paste_from_clippy_js)
    useful.write_message(str(pif.form.get_form()))
    useful.write_message('<hr>')

    try:
        if upform.url_list:
            print(pif.render.format_head())
            useful.header_done()
            print(show_var_info(pif, upform.mod_id, upform.var_id))
            upform.grab_url_file_list()
            print(pif.render.format_tail())
        elif upform.scrape:
            print(pif.render.format_head())
            useful.header_done()
            print(show_var_info(pif, upform.mod_id, upform.var_id))
            upform.scrape_url_pic()
            print(pif.render.format_tail())
        else:
            return upform.write(pif, desc=upform.comment, restrict=not pif.is_allowed('uma'))
    except OSError:
        useful.warn('fail:', traceback.format_exc(0))


# -- imawidget


def show_editor(pif, eform, pdir=None, fn=None):
    if not pdir:
        pdir = eform.tdir
    if not fn:
        fn = eform.fn
    full_path = os.path.join(pdir, fn)
    if not os.path.exists(full_path):
        useful.warn('%s not found.' % full_path)
        return

    print('<hr><form action="imawidget.cgi" name="myForm">' + pif.create_token())
    # imglib.ActionForm(pif).read(pif.form).write(pif, fn)
    x, y = eform.write(pif, pdir, fn)
    full_path = os.path.join(pdir, fn)
    root, ext = useful.root_ext(fn.strip())
    print('<table><tr><td></td><td>' + pif.render.format_image_art('hruler.gif') + '</td></tr>')
    print('<tr><td valign="top">' + pif.render.format_image_art('vruler.gif') + '</td><td valign="top">')
    dic = {'file': pif.secure_host + '/' + full_path, 'width': x, 'height': y}
    print(javasc.def_edit_app % dic)
    print('</td></tr></table>')
    print('<input type="hidden" value="%s" name="f">' % fn)
    # print('<input type="hidden" value="%s" name="d">' % pdir)
    print('Debug: <span id="ima_debug">Debug output here.</span>')
    print('</form><hr>')


def show_redoer(pif, eform):
    if not eform.repl:
        print('<form action="imawidget.cgi" name="myForm">' + pif.create_token())
        # print('<input type="text" value="" name="q" id="q">')
        eform.write(pif, edit=False)
        # print('Bounds:', pif.form.put_text_input('q', 20, value=pif.form.get_str('q')))
        print('<input type="hidden" value="%s" name="f">' % eform.fn)
        # print('<input type="hidden" value="%s" name="d">' % eform.tdir)
        print('</form>')
        print('<hr>')


class EditForm(imglib.ActionForm):
    def __init__(self, pif, tdir='.', fn=''):
        super().__init__(pif)
        self.edit = False
        self.fn = fn
        self.ot = ''
        self.pr = False
        self.tdir = tdir
        self.nvar = ''
        self.man = ''
        # self.var = ''
        # self.nname = ''
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
        # q = ''
        self.x1, self.y1, self.x2, self.y2 = self.q = [0, 0, 0, 0]
        self.root, self.ext = '', ''
        self.nname = ''
        self.is_edited = False
        self.set_target_size((self.xts, self.yts))
        self.pth = ''
        self.credfile = imglib.get_credit_file()

    def read(self, pif, edit=False):
        super().read(pif.form)
        self.edit = edit or pif.form.get_exists('edit')
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
        # self.var = pif.form.get_str('v')
        # self.nname = pif.form.get_str("newname")
        self.tysz = pif.form.get_str("tysz", "")
        self.xts = pif.form.get_int('x')
        self.yts = pif.form.get_int('y')
        self.unlv = pif.form.get_bool('unlv')
        self.unlh = pif.form.get_bool('unlh')
        self.rf = pif.form.checks(*imglib.rot_flip_keys)
        self.rl = pif.form.get_bool('rl')
        self.rh = pif.form.get_bool('rh')
        self.rr = pif.form.get_bool('rr')
        self.fh = pif.form.get_bool('fh')
        self.fv = pif.form.get_bool('fv')
        self.keep = pif.form.get_exists('keep')
        self.resize = pif.form.get_exists('resize')
        self.crop = pif.form.get_exists('crop')
        self.shrink = pif.form.get_exists('shrink')
        self.wipe = pif.form.get_exists('wipe')
        self.pad = pif.form.get_exists('pad')
        self.mass = pif.form.get_exists('mass')
        self.clean = pif.form.get_exists('clean')
        self.repl = pif.form.get_bool('repl')
        self.save = pif.form.get_bool('save')
        self.cc = pif.form.get_str('cc')
        self.credit = pif.form.get_str('credit')
        if not self.credit:
            for pref, cred in self.credfile.get(self.tdir[self.tdir.find('/') + 1:], {}).items():
                if self.fn.startswith(pref):
                    self.credit = cred
                    break
        self.read_file(pif.form.get_str('q'))
        if not self.pref:
            self.pref = pif.form.get_str('tysz')
        if not self.man and self.nname:
            self.man = self.nname[:self.nname.rfind('.')] if '.' in self.nname else self.nname
            self.man = self.man[2:] if len(self.man) > 1 and self.man[1] == '_' else self.man
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
        useful.write_comment('calc_man')
        pdir = self.tdir
        if pdir.startswith('./'):
            pdir = pdir[2:]
        if not pdir.startswith('/'):
            pdir = '/' + pdir
        if pdir.endswith('/'):
            pdir = pdir[:-1]

        man = ''
        if pdir.startswith(config.LIB_MAN_DIR):
            man = pdir[pdir.rfind('/') + 1:]
        elif (pdir.startswith('.' + config.IMG_DIR_PROD_PACK) or
              pdir.startswith('.' + config.IMG_DIR_PROD_PLAYSET) or
              pdir.startswith('.' + config.IMG_DIR_SET_PACK) or
              pdir.startswith('.' + config.IMG_DIR_SET_PLAYSET)):
            if self.fn:
                if len(self.fn) > 2 and self.fn[1] == '_':
                    man = self.fn[2:-4]
                else:
                    man = self.fn[:-4]
        elif pdir.startswith('.' + config.IMG_DIR_CAT):
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

        print(pif.render.format_link('traverse.cgi?d=%s' % pdir, pdir), '/')
        print(pif.render.format_link('traverse.cgi?d=%s&f=%s' % (pdir, fn), fn))
        print(pif.render.format_button_link("show", os.path.join('/', pdir, fn)))
        print(pif.render.format_button_link("upload", "upload.cgi?d=%s&n=%s" % (pdir, fn)))
        print('<br>')

        full_path = os.path.join(pdir, fn)
        if not os.path.exists(full_path):
            useful.warn('%s not found.<br>' % full_path)
            return 0, 0

        presets = imglib.read_presets(pdir)

        xs, ys = super().write(pif, fn)
        print(pif.form.put_hidden_input(c=useful.url_quote(pif.form.get_str('c', ''), plus=True)))
        # xs, ys = imglib.get_size(full_path)
        if edit:
            print('<div class="lefty">')
            # print('(%d, %d)' % (xs, ys))
            print(pif.form.put_radio('tysz', [('q', '')], presets.get('tysz', '')))
            print('x: <input name="x" type="text" size="4" value="%s">' % config.DEFAULT_X_SIZE)
            print('y: <input name="y" type="text" size="4" value="%s">' % config.DEFAULT_Y_SIZE)
            print(pif.form.put_radio(
                'tysz', [(siz, siz.upper()) for siz in mbdata.image_size_types],
                presets.get('tysz', mbdata.IMG_SIZ_SMALL)))
            print('-', pif.form.put_checkbox("unlv", [(1, "V")], presets.get("unlv", [])))
            print(pif.form.put_checkbox("unlh", [(1, "H")], presets.get("unlh", [])))
            print(pif.form.put_button_input('keep'))
            print(pif.form.put_checkbox("rl", [(1, "RL")], presets.get("rl", [])))
            print(pif.form.put_checkbox("rh", [(1, "RH")], presets.get("rh", [])))
            print(pif.form.put_checkbox("rr", [(1, "RR")], presets.get("rr", [])))
            print(pif.form.put_checkbox("fh", [(1, "FH")], presets.get("fh", [])))
            print(pif.form.put_checkbox("fv", [(1, "FV")], presets.get("fv", [])))
            print(pif.form.put_select('ot', imglib.otypes, 'jpg'))
            print(pif.form.put_checkbox("pr", [(1, "pr")], presets.get("pr", [])))
            print('<br>')
            # print('Name:', pif.form.put_text_input('newname', 20, value=pif.form.get_str('newname', '')))
            print(pif.form.put_button_input('resize'))
            print(pif.form.put_button_input('crop'))
            print(pif.form.put_button_input('crop/shrink', 'shrink'))
            print(pif.form.put_button_input('wipe'))
            print(pif.form.put_button_input('pad'))
            # if pif.is_allowed('m'):  # pragma: no cover
            #     print('Var: ' + pif.form.put_text_input('v', 8, value=pif.form.get_str('v', '')))
            print(pif.form.put_checkbox("repl", [(1, "Replace")], presets.get("repl", [])))
            print(pif.form.put_checkbox("save", [(1, "Save")], presets.get("save", [])))
        print(pif.form.put_button_input('mass'))
        print(pif.form.put_button_input('clean'))
        photogs = [(x.photographer.id, x.photographer.name)
                   for x in pif.dbh.fetch_photographers(config.FLAG_ITEM_HIDDEN)]
        print(pif.render.format_link('/cgi-bin/mass.cgi?tymass=photogs', 'Credit'))
        print(pif.form.put_select('credit', photogs, selected=self.credit, blank=''))
        print('Bounds: <input type="text" value="%s" name="q" id="q">' % ','.join([str(x) for x in self.q]))
        print('<br><span id="ima_info"></span>&nbsp;')
        print(pif.form.put_hidden_input(cc=presets.get('cc', '')))
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
        imglib.simple_save(ofi, pth)
        file_log(nname, self.tdir)
        print('saving to', pth, '(%d, %d)<br>' % (imglib.get_size(pth)))
        return nname

    def save_presets(self):
        if self.save:  # and os.path.exists(os.path.join(self.tdir, '.ima')):
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
            # open(os.path.join(self.tdir, '.ima'), 'w').write(str(presets))

    def shape_image(self):
        print('shape_image', self.pth, self.nname, self.q, self.target_size, self.original_size, self.rf, '<br>')
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
        print('mass_clean', self.pth, '<hr>')
        nname_root = self.fn
        if '.' in nname_root:
            nname_root = nname_root[:nname_root.rfind('.')]
        for pref in [mbdata.IMG_SIZ_TINY, mbdata.IMG_SIZ_SMALL, mbdata.IMG_SIZ_MEDIUM, mbdata.IMG_SIZ_LARGE]:
            nname = nname_root + '_' + pref + ('.' + self.ot) if self.ot else ''
            useful.file_delete(os.path.join(self.tdir, nname))

    def mass_resize(self, pif, desc=''):
        # print(self.__dict__, '<br>')
        var = self.var.lower()
        man = self.man.lower()
        print('mass_resize', 'pth', self.pth, 'tdir "%s"' % self.tdir, 'fn', self.fn, 'ot', self.ot,
              'os', self.original_size, '|', man, var, '<hr>')

        # nname_root = self.man if self.man else self.fn
        nname_root = self.fn
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
        if self.tdir.startswith('lib/prod') or self.tdir.startswith('./lib/prod'):
            prefs = 'm'
        elif self.tdir.startswith('lib/set') or self.tdir.startswith('./lib/set'):
            prefs = 'smlh'
        elif self.tdir.startswith('lib/pub') or self.tdir.startswith('./lib/pub'):
            if self.dest == '.' + config.IMG_DIR_BOX or self.tdir == '.' + config.IMG_DIR_BOX:
                prefs = 'spm'
            else:
                prefs = 'smlh'
        else:
            ddir = '.' + (config.IMG_DIR_VAR if var else config.IMG_DIR_MAN)
            prefs = 'tsml'
            outnam = '_' + man + ('-' + var if var else '') + ot
        outnam = outnam.lower()

        largest = None
        for pref in prefs:
            if xos < mbdata.imagesizes[pref][0]:
                break
            self.nname = nname_root + '_' + pref + ot
            self.set_target_size(mbdata.imagesizes[pref])
            dnam = pref + outnam
            dpth = os.path.join(ddir, dnam)
            print('resizing', self.tdir, self.nname, 'to', dpth, '<br>')
            if self.unlv and self.unlh:
                nname = self.crop_image()
            elif self.unlv or self.unlh:
                nname = self.shrink_image()
            else:
                nname = self.shape_image()
            useful.file_mover(os.path.join(self.tdir, nname), dpth, mv=True, ov=True)
            useful.file_touch(dpth)
            largest = dpth
            print('<br><img src="/%s"><hr>' % dpth)

        # if not var:
        #     dpth = os.path.join('.' + config.IMG_DIR_MAN_ICON, 'i' + man + '.gif')
        #     print('creating icon', self.tdir, self.nname, 'to', dpth, '<br>'  # no pif)
        #     create_icon(pif, man, name='')
        #     print('<br><img src="/%s"><hr>' % dpth)

        if self.mv:
            useful.file_delete(self.pth, True)

        if largest:  # and log_action:
            # title = pif.form.get_str('title', '%s-%s' % (eform.man, eform.var))
            title = '%s-%s' % (self.man, self.var)
            cred = pif.form.get_str('credit')
            if cred:
                photog = pif.dbh.fetch_photographer(cred)
                if photog and not photog.flags & config.FLAG_PHOTOGRAPHER_PRIVATE:
                    title += ' credited to ' + photog.name
                else:
                    cred = ''
            url = pif.secure_prod + largest
            link = pif.secure_prod + '/cgi-bin/vars.cgi?mod=%s&var=%s' % (self.man, self.var)
            pif.render.message('Post to Tumblr: ',
                               tumblr.Tumblr(pif).create_photo(caption=title, source=url, link=link))
            pif.render.message('Credit added: ', pif.dbh.write_photo_credit(cred, ddir, self.man, self.var))

        return largest


@basics.web_page
def imawidget_main(pif):
    pif.render.print_html()
    pif.restrict('v')

    eform = EditForm(pif).read(pif)

    pif.render.title = pif.render.pagetitle = pif.render.pic_dir + '/' + eform.fn
    pif.render.set_page_extra(pif.render.increment_js)
    print(pif.render.format_head())
    useful.header_done()

    if not pif.is_allowed('ma'):
        print(pif.render.format_image_required(eform.fn))
        return

    if eform.fn and os.path.exists(os.path.join(eform.tdir, 'descr.log')):
        # This is for /inc!  If I delete it again, I'll be pissed.
        descs = open(os.path.join(eform.tdir, 'descr.log')).readlines()
        descs = dict([x.strip().split('\t', 1) for x in descs])
        # mod_id, var_id, year, comment
        print(descs.get(os.path.splitext(eform.fn)[0], '').replace('\t', '<br>'))
        print('<hr>')

    if eform.keep:
        picker(pif, eform.fn)
        print(pif.render.format_image_required(
            [eform.fn[:eform.fn.rfind('.')]], suffix=eform.fn[eform.fn.rfind('.') + 1:], also={"border": "0"}), '<br>')
        print(pif.render.format_tail())
        return

    print(show_var_info(pif, eform.man, eform.var))

    is_edited = eform.is_edited
    try:
        found = eform.action(pif)
        if found['act']:
            nfn = found['fn']
            if os.path.exists(nfn):
                pass
            elif eform.cycle:
                # dl, gl, ol, sl, xl = imglib.get_dir(eform.tdir)
                files = imglib.get_dir(eform.tdir)
                while files['graf']:
                    if files['graf'][0] == nfn:
                        files['graf'].pop()
                    else:
                        nfn = files['graf'][0]
                        break
            if nfn:
                # show_picture(pif, nfn)
                print(pif.render.format_link('traverse.cgi?d=%s' % eform.tdir, eform.tdir), '/')
                print(pif.render.format_link('traverse.cgi?d=%s&f=%s' % (eform.tdir, eform.fn), eform.fn), '<br>')
            else:
                print(pif.render.format_link('traverse.cgi?d=%s' % eform.tdir, eform.tdir), '/')

        elif eform.clean:
            eform.mass_clean()
            show_editor(pif, eform)
        elif eform.mass:
            if eform.man and eform.var:
                print(
                    pif.render.format_button_link("promote", f'editor.cgi?mod={eform.man}&var={eform.var}&promote=1'),
                    *[x for x in 'TSML' if os.path.exists(f'pic/man/{x}_{eform.man.lower()}.jpg')])
            eform.mass_resize(pif, "from library")
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
            # show_redoer(pif, eform)
            # print(pif.render.format_image_required([eform.fn], also={"border": "0"}), '<br>')
            show_editor(pif, eform)
        elif eform.crop:
            eform.save_presets()
            eform.fn = eform.crop_image()
            # show_redoer(pif, eform)
            # print(pif.render.format_image_required([eform.fn], also={"border": "0"}), '<br>')
            show_editor(pif, eform)
        elif eform.shrink:
            eform.save_presets()
            eform.fn = eform.shrink_image()
            # show_redoer(pif, eform)
            # print(pif.render.format_image_required([eform.fn], also={"border": "0"}), '<br>')
            show_editor(pif, eform)
        else:
            show_editor(pif, eform)
            is_edited = False
    except Exception:
        useful.show_error()
        is_edited = False

    if is_edited:
        print(pif.render.format_button_link(
            'replace',
            'upload.cgi?act=1&d=%s&f=%s&newname=%s&rename=1&cpmv=m&ov=1' % (eform.tdir, eform.nname, eform.fn)))

    print(pif.render.format_tail())


# -- stitch


class StitchForm(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        super().__init__()

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
                print(file_num, fs, '<br>')
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

        header += '<form action="stitch.cgi" name="myForm" onSubmit="return getValueFromApplet()">\n{}'.format(
            pif.create_token())
        header += pif.form.put_hidden_input(fc=self.file_count + 1)
        # columns = ['name', 'image']
        print(header)
        print(pif.render.format_table_start())
        # entries = []
        for fs in self.fsl:
            print(pif.render.format_row_start())
            num = fs['n']
            fn = fs.get('fn', '').strip()
            fn_size = ''
            if fn:
                if 'x1' not in fs and os.path.exists(fn):
                    x, y = imglib.get_size(fn)
                    self.limit_x = min(x, self.limit_x)
                    self.limit_y = min(y, self.limit_y)
                    fn_size = '<br>' + str((x, y))
                print(pif.render.format_cell(1, fn + fn_size))
                print(pif.form.put_hidden_input({'fn_' + num: fn}))
            else:
                print(pif.render.format_cell(
                    1, pif.form.put_text_input('fn_%d' % self.file_count, 80) + '<br>' +
                    self.fsl[0]['fn'].strip()))
                print(pif.render.format_cell(
                    1, pif.form.put_button_input() + ' ' +
                    pif.form.put_button_input('finalize') + '<br>' +
                    pif.form.put_checkbox('or', [('h', 'horizontal')]), also={'colspan': 2}))
                print(pif.render.format_cell(1, 'x ' + pif.form.put_text_input('limit_x', 5, value=self.limit_x)))
                print(pif.render.format_cell(1, 'y ' + pif.form.put_text_input('limit_y', 5, value=self.limit_y)))
            if 'x1' in fs:
                print(pif.render.format_cell(1, str(fs['x1']), also={'width': 40}))
                print(pif.form.put_hidden_input({'x1_' + num: fs['x1']}))
                print(pif.render.format_cell(1, str(fs['y1']), also={'width': 40}))
                print(pif.form.put_hidden_input({'y1_' + num: fs['y1']}))
                print(pif.render.format_cell(1, str(fs['x2']), also={'width': 40}))
                print(pif.form.put_hidden_input({'x2_' + num: fs['x2']}))
                print(pif.render.format_cell(1, str(fs['y2']), also={'width': 40}))
                print(pif.form.put_hidden_input({'y2_' + num: fs['y2']}))
            elif fn:
                if not os.path.exists(fn):
                    print(pif.render.format_cell(1, 'Nonexistant: ' + os.getcwd() + '/' + fn, also={'colspan': 4}))
                else:
                    print(pif.render.format_cell(1, self.show_widget(fn), also={'colspan': 4}))
            print(pif.render.format_row_end())
        print(pif.render.format_table_end())
        footer = '<input type="text" value="" name="q" id="q"><br>\n'  # for imawidget
        footer += 'Debug: <span id="ima_debug">Debug output here.</span>\n'
        footer += '</form>'
        print(footer)

    def show_widget(self, filepath):
        x, y = imglib.get_size(filepath)
        dic = {'file': 'https://' + os.environ['SERVER_NAME'] + '/' + filepath, 'width': x, 'height': y}
        return javasc.def_edit_app % dic

    def finish_picture(self, pif):
        print(pif.form.get_form(), '<hr>')
        for fn in pif.form.get_list('in'):
            useful.file_mover(fn, '.' + os.path.join(config.TRASH_DIR, fn[fn.rfind('/') + 1:]),
                              mv=True, inc=True, trash=False)
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
        print(pif.render.format_table_start())
        input_files = list()
        for fs in self.fsl:
            print(pif.render.format_row_start())
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
            # print(fa[-1], '<br>')
            print(pif.render.format_cell(1, str(fs['fn'])))
            print(pif.render.format_cell(1, str(fs['x1']), also={'width': 40}))
            print(pif.render.format_cell(1, str(fs['y1']), also={'width': 40}))
            print(pif.render.format_cell(1, str(fs['x2']), also={'width': 40}))
            print(pif.render.format_cell(1, str(fs['y2']), also={'width': 40}))
            print(pif.render.format_row_end())
        print(pif.render.format_table_end())

        print('Stitching...', final)
        imglib.stitcher(final, fa, pif.form.get_str('or') == 'h', minx, miny, self.limit_x, self.limit_y, verbose=True)
        time.sleep(2)
        print('... Finished.<br>')
        sys.stdout.flush()
        # print('<a href="../' + final + '">' + final + '<br>')
        # print('<img src="../' + final + '"></a>')
        d, f = os.path.split(final)
        show_picture(pif, f, d)    # this right here doesn't work but everything else seems to
        # orig = input_files[0][input_files[0].rfind('/') + 1:]
        print('<br><form>Final resting place:')
        print(pif.create_token())
        print(pif.form.put_text_input('o', 80, value='%s' % input_files[0]))
        print(pif.form.put_hidden_input(f='%s/%s' % (d, f)))
        for fn in input_files:
            print(pif.form.put_hidden_input({'in': fn}))
        print(pif.form.put_button_input('finish'))
        print('</form>')


@basics.web_page
def stitch_main(pif, verbose=False):
    pif.render.print_html()

    if 1:
        pif.render.title = 'stitch'
        print(pif.render.format_head())
        useful.header_done()

        StitchForm(verbose).read(pif).perform(pif)

        print(pif.render.format_tail())
    else:
        return pif.render.format_template('stitch.html', StitchForm(verbose).read(pif).perform(pif))


# -- pictures


def casting_pictures(pif, mod_id, direc):
    fl = glob.glob('%s/%s*.*' % (direc, mod_id)) + glob.glob('%s/?_%s*.*' % (direc, mod_id))
    fl.sort()
    if fl:
        print('<h3>%s</h3>' % direc)
        if direc == '.' + config.IMG_DIR_ADD:
            print(pif.render.format_button_link('describe', pif.dbh.get_editor_link('attribute_picture',
                  {'mod_id': mod_id})) + '<br>')
        for fn in fl:
            print('<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s&man=%s"><img src="../%s">%s</a> ' % (
                direc, fn[fn.rfind('/') + 1:], mod_id, fn, fn))
            print('<br>')
        print('<hr>')


def lineup_pictures(pif, lup_models):
    print('<h3>Lineup Models</h3>')
    lup_models.sort(key=lambda x: x['lineup_model.year'])
    for mod in lup_models:
        if mod['section.img_format']:
            mod['filename'] = mod['section.img_format'] % mod['lineup_model.number'] + '.jpg'
            mod['filepath'] = mod['page_info.pic_dir'] + '/' + mod['filename']
            if os.path.exists(mod['filepath']):
                print('<a href="/cgi-bin/imawidget.cgi?d=%(page_info.pic_dir)s&f=%(filename)s&'
                      'man=%(lineup_model.mod_id)s"><img src="../%(filepath)s">%(filepath)s</a><br>' % mod)
    print('<hr>')


@basics.web_page
def pictures_main(pif):
    pif.render.print_html()
    mod_id = pif.form.get_id('m', defval='')
    pif.render.title = f'pictures - {mod_id}'
    print(pif.render.format_head())
    useful.header_done()
    if mod_id:
        if pif.form.get_bool('t'):
            tilldir = 'lib/tilley'
            prefixes = imglib.get_tilley_file()
            for prefix in prefixes.get(mod_id.lower(), []):
                print(f'<h3>{prefix}</h3>')
                imgs = pif.render.find_image_list(prefix, wc='*', suffix='*', pdir=tilldir)
                for img in imgs:
                    if pif.form.get_bool('import'):
                        useful.file_mover(os.path.join(tilldir, img),
                                          os.path.join('lib', 'man', mod_id.lower(), img), mv=True, ov=False)
                    else:
                        print(pif.render.fmt_img_src(tilldir + '/' + img))
                    print(f'<br>{img}<br>')
            print('<a href="?m={}&t=1&import=1">{}</a>'.format(mod_id, pif.form.put_text_button('import')))
        else:
            for cdir in [config.IMG_DIR_MAN, config.IMG_DIR_VAR, config.IMG_DIR_MAN_ICON, config.IMG_DIR_ADD]:
                casting_pictures(pif, mod_id.lower(), '.' + cdir)
            lineup_pictures(pif, pif.dbh.fetch_casting_lineups(mod_id))
    else:
        print('Huh?')
    print(pif.render.format_tail())


# -- icon

# understands 0-9 A-Z & ' + - .  /

def create_icon(pif, mod_id, name, title='mb2', isizex=100, isizey=100):
    if not name:
        model = pif.dbh.fetch_casting(mod_id)
        name = model['iconname']
    logo = '.' + config.IMG_DIR_ART + '/mb2.gif'
    print(' ', mod_id, '|'.join(name))

    in_path = os.path.join('.' + config.IMG_DIR_MAN, 's_' + mod_id + '.jpg')
    icon_file = os.path.join('.' + config.IMG_DIR_MAN_ICON, 'i_' + mod_id + '.gif')
    image = imglib.iconner(in_path, name, logo=logo, isizex=100, isizey=100)
    if image:
        open(icon_file, 'wb').write(image)


def get_man_dict(pif):
    manlist = pif.dbh.fetch_casting_list()
    mans = dict()
    for llist in manlist:
        llist = pif.dbh.modify_man_item(llist)
        mans[llist['id'].lower()] = llist
    return mans


def icon_main(pif, *mod_ids):
    title = pif.switch['b'][-1] if pif.switch['b'] else 'mb2'
    mandict = pif.dbh.fetch_casting_dict()

    if mod_ids and mod_ids[0] == '-a':
        for man in mandict:
            name = mandict[man]['iconname']
            if pif.switch['n']:
                name = pif.switch['n'][-1].split(';')
            create_icon(pif, man, name, title)
    elif mod_ids:
        for man in mod_ids:
            man = man.lower()
            if man in mandict:
                name = mandict[man]['iconname']
                if pif.switch['n']:
                    name = pif.switch['n'][-1].split(';')
                create_icon(pif, man, name, title)
            else:
                print(man, 'not in list')
    else:
        print('huh?')  # print mandict


# -- bits


@basics.web_page
def bits_main(pif):
    years = {
        '1998': {'d': '.' + config.IMG_DIR_PROD_MT_LAUREL, 'p': '1998', 'r': 'ur'},
        '1999': {'d': '.' + config.IMG_DIR_PROD_MT_LAUREL, 'p': '1999', 'r': 'urd'},
        '2000': {'d': '.' + config.IMG_DIR_PROD_MT_LAUREL, 'p': '2000', 'r': 'urdab'},
        '2002': {'d': '.' + config.IMG_DIR_PROD_MT_LAUREL, 'p': '2002', 'r': 'ur'},
        '2003': {'d': '.' + config.IMG_DIR_PROD_MT_LAUREL, 'p': '2003', 'r': 'ur'},
        '2004': {'d': '.' + config.IMG_DIR_PROD_MT_LAUREL, 'p': '2004', 'r': 'ur'},
        '2008': {'d': '.' + config.IMG_DIR_PROD_EL_SEG, 'p': '2008', 'r': 'u'},
        '2009': {'d': '.' + config.IMG_DIR_PROD_EL_SEG, 'p': '2009', 'r': 'u'},
    }

    colors = {True: "#CCCCCC", False: "#FFFFFF"}

    pif.render.print_html()

    print("<table>")

    yearlist = sorted(years.keys())

    c = False
    print("<tr>")
    print("<th></th>")
    for y in yearlist:
        print('<th bgcolor="%s" colspan=%d>%s</th>' % (colors[c], len(years[y]['r']), y))
        c = not c
    print("</tr>")

    c = False
    print("<tr>")
    print("<th></th>")
    for y in yearlist:
        for r in years[y]['r']:
            print('<th bgcolor="%s">%s</th>' % (colors[c], r.upper()))
        c = not c
    print("</tr>")

    for a in range(1, 21):

        c = False
        print("<tr>")
        print('<th bgcolor="%s">%d</th>' % (colors[True], a))

        for y in yearlist:
            for r in years[y]['r']:

                fmt = "%s/%s%ss%02d.gif"
                f = fmt % (years[y]['d'], years[y]['p'], r, a)

                cstr = '<th bgcolor="%s">' % (colors[c])
                if os.path.exists("../htdocs/" + f):
                    cstr += '<img src="%s">' % ("../" + f)
                else:
                    cstr += "&nbsp;"
                print(cstr + '</th>')
            c = not c
        print("</tr>")
    print("</table>")


# -- library


def show_library_list(pif, title, tdir, fl):
    cols = pif.form.get_int("c", 5)
    if not fl:
        return
    clen = (len(fl) - 1) / cols + 1
    ffl = [fl[(x * clen):((x + 1) * clen)] for x in range(0, cols)]
    print('<h4>%s (%d)</h4>' % (title, len(fl)))
    print("<table width=100%><tr valign=top>")
    for cl in ffl:
        print("<td width=%d%%>" % (100 / cols))
        for f in cl:
            root, ext = useful.root_ext(f.strip())
            fst = os.stat(tdir + '/' + f)
            perms = fst[stat.ST_MODE]
            if f[0] == '.':
                print('<i>%s</i><br>' % f)
            elif stat.S_ISDIR(perms):
                print('<a href="/cgi-bin/traverse.cgi?d=%s">%s</a><br>' % (tdir + '/' + f, f))
            elif f[-4:] == '.dat':
                # print('<a href="/cgi-bin/table.cgi?page=%s">%s</a><br>' % (tdir + '/' + f, f))
                print('<a href="/cgi-bin/traverse.cgi?d=%s&f=%s">%s</a><br>' % (tdir, f, f))
            elif (perms & 5) == 0:
                print('%s<br>' % f)
            elif ext in imglib.itypes:
                # print('<a href="/cgi-bin/traverse.cgi?d=%s&f=%s">%s</a><br>' % (tdir, f, f))
                print('<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s">%s</a><br>' % (tdir, f, f))
            else:
                print('<a href="../%s">%s</a><br>' % (tdir + '/' + f, f))
        print("</td>")
    print("</tr></table>")
    print('<br><hr>')


def show_library_graf(title, tdir, fl):
    if not fl:
        return

    print('<h4>%s (%d)</h4>' % (title, len(fl)))
    fd = {}
    for f in fl:
        root, ext = useful.root_ext(f)
        if root[-2] == '_' and root[-1] in mbdata.image_size_types:
            root = root[:-2]
        fd.setdefault(root, [])
        fd[root].append(f)

    print('<table>')
    for root in sorted(fd.keys()):
        fd[root].sort()
        print('<tr><td>%s</td><td><img src="thumber.cgi?d=%s&f=%s"></td><td>' % (root, tdir, fd[root][0]))
        for f in fd[root]:
            perms = os.stat(tdir + '/' + f)[stat.ST_MODE]
            if (perms & 4) == 0:
                print('%s<br>' % f)
            else:
                print('<a href="imawidget.cgi?d=%s&f=%s&cy=0">%s' % (tdir, f, f))
        print('</td></tr>')
        sys.stdout.flush()
    print('</table>')
    print('<br><hr>')


def show_library_dir(pif, tdir, grafs=0):
    print('<hr>')

    # dl, gl, ol, sl, xl = imglib.get_dir(tdir)
    files = imglib.get_dir(tdir)

    show_library_list(pif, files['titles']['dat'], tdir, files['dat'])
    if grafs:
        show_library_graf(files['titles']['graf'], tdir, files['graf'])
    else:
        show_library_list(pif, files['titles']['graf'], tdir, files['graf'])
    show_library_list(pif, files['titles']['dat'], tdir, files['dat'])
    show_library_list(pif, files['titles']['exe'], tdir, files['exe'])
    show_library_list(pif, files['titles']['other'], tdir, files['other'])

    print('<a href="upload.cgi?d=%s&m=%s">%s</a>' % (tdir, tdir[7:], pif.form.put_text_button('upload')))

    if files['graf']:
        print('<form action="traverse.cgi">' + pif.create_token())
        print('<a href="traverse.cgi?g=1&d=%s">%s</a> or ' % (tdir, pif.form.put_text_button('show all pictures')))
        print('Pattern <input type="text" name="p">')
        print('<input type="hidden" name="d" value="%s">' % tdir)
        print(pif.form.put_button_input())
        print('</form>')


imginputs = '<input type="checkbox" name="rm" value="%(f)s"> rm<input type="checkbox" name="mv" value="%(f)s %(b)s"> mv'
imginput = '''<input type="checkbox" name="rm" value="%(f)s"> rm
<input type="text" name="ren.%(f)s"> rename
'''


def library_img(pif, args, base=''):
    print('<tr>')
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
        inp += ' ' + pif.render.format_button_link('edit', 'imawidget.cgi?d=%s&f=%s&cy=0' % (pif.render.pic_dir, arg))
        inp += ' ' + pif.render.format_button_link('stitch', 'stitch.cgi?fn_0=%s&submit=1&q=&fc=1' % (
            pif.render.pic_dir + '/' + arg))
        print(pif.render.format_cell(0, '<a href="../%s/%s">%s</a><br>%s%s' % (
            pif.render.pic_dir, arg,
            pif.render.format_image_required([root], suffix=ext, also={"border": 0}), arg, inp)))
    print('</tr>')


def show_library_imgs(pif, patt):
    print('<hr>')
    print('<form action="traverse.cgi" method="post">' + pif.create_token())
    plist = patt.split(',')
    for pent in plist:
        flist = useful.read_dir(pent, pif.render.pic_dir)
        flist.sort()
        print('<table>')
        for f in flist:
            library_img(pif, [f])
        print('</table>')
        print('<hr>')
    print('<input type="hidden" name="d" value="%s">' % pif.render.pic_dir)
    print('<input type="hidden" name="sc" value="1">')
    # print('<input type="hidden" name="pre" value="man">')
    print(pif.form.put_button_input())
    print('<a href="upload.cgi?d=%s&r=1">%s</a>' % (pif.form.get_str('d', '.'), pif.form.put_button('upload')))
    print('</form>')


# not functional and not in use
def show_library_file(pif, fn):
    if fn.endswith('.dat'):
        show_library_table(pif, fn)
    else:
        show_picture(pif, fn)


colors = ["#FFFFFF", "#CCCCCC"]


# print('<a href="/cgi-bin/table.cgi?page=%s">%s</a><br>' % (tdir + '/' + f, f))
def show_library_table(pif, pagename):
    tablefile = bfiles.SimpleFile(pif.render.pic_dir + '/' + pagename)
    cols = ''  # pif.form.get_str('cols', '')
    h = 0  # pif.form.get_int('h')
    sorty = pif.form.get_str('sort')

    print('<table>')
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
            print('<tr>')
            for ent in range(0, len(hdr)):
                if ent >= len(cols) or cols[ent].lower() != 'n':
                    # print("<th>" + hdr[ent] + "</th>")
                    print('<th bgcolor="#FFFFCC"><a href="table.cgi?page=%s&sort=%d&h=%d&cols=%s">%s</th>' % (
                        pagename, iarg, h, cols, hdr[ent]))
                iarg = iarg + 1
            print("</tr>\n<tr>")
        print('<tr bgcolor="%s">' % colors[irow])
        row = row - 1
        for ent in range(0, len(line)):
            if ent >= len(cols) or cols[ent].lower() != 'n':
                print("<td>" + line[ent] + "</td>")
        print("</tr>")
    print('</table>')


def do_library_action(pif, tdir, fn, act):
    print('<div class="warning">')
    nfn = imglib.ActionForm(pif).action(pif, tdir, fn)
    print('</div><br>')
    if nfn:
        show_library_imgs(pif, nfn)
    else:
        show_library_dir(pif, tdir, 0)


@basics.web_page
def library_main(pif):
    os.environ['PATH'] += ':/usr/local/bin'
    pif.render.print_html()
    pif.restrict('a')
    # pif.render.title = '<a href="traverse.cgi?d=%s">%s</a>' % (pif.form.get_str("d", '.'), pif.form.get_str("d", '.'))
    pif.render.title = pif.render.pic_dir = pif.form.get_str("d", '.')
    pif.render.title += '/' + pif.form.get_str("f", "")
    graf = pif.form.get_int("g")
    fnam = pif.form.get_str("f", '')
    patt = pif.form.get_str("p", '')
    # cols = pif.form.get_int("c", 5)
    act = pif.form.get_int('act')
    # cycle = pif.form.get_int("cy")

    pif.render.set_page_extra(pif.render.increment_js)
    print(pif.render.format_head())
    useful.header_done()
    print(pif.form.get_form())
    if patt:
        show_library_imgs(pif, patt)
    elif act:
        do_library_action(pif, pif.render.pic_dir, fnam, act)
    elif fnam:
        show_library_file(pif, fnam)
    else:
        show_library_dir(pif, pif.render.pic_dir, graf)
    print(pif.render.format_tail())


# -- image


@basics.web_page
def image_main(pif):
    fpath = os.path.join(pif.form.get_str('d', '.'), pif.form.get_str('f', ''))
    if not os.path.exists(fpath):
        raise useful.SimpleError(fpath + ' does not exist')
    print('Content-Type: image/jpeg\n')
    print(open(os.path.join(pif.form.get_str('d', '.'), pif.form.get_str('f', '')), "rb").read())


# -- thumber


@basics.web_page
def thumber_main(pif):
    os.environ['PATH'] += ':/usr/local/bin'

    # pif.restrict('a')

    print('Content-Type: image/gif')
    print()

    dir = pif.form.get_str('d', '.')
    fil = pif.form.get_str('f', '')
    pth = os.path.join(dir, fil)

    x = 100
    outf = useful.pipe_chain(open(pth),
                             imglib.import_file(pth) + [["/usr/local/bin/pamscale", "-xsize", str(x)]] +
                             imglib.export_file('tmp.gif'), stderr=open('/dev/null', 'w'), verbose=False)

    print(outf)


# -- photographers


def credit_show(pif, cred):
    url = ''
    if cred['photo_credit.path'] == 'pic/man':
        url = 'single.cgi?id=%s' % cred['photo_credit.name']
    elif cred['photo_credit.path'] == 'pic/man/var':
        url = 'vars.cgi?mod=%s&var=%s' % tuple(cred['photo_credit.name'].split('-', 1))
    elif cred['photo_credit.path'] == 'pic/man/add':
        url = 'single.cgi?id=%s' % cred['photo_credit.name'][2:].split('-', 1)[0]
    elif cred['photo_credit.path'] in [
            'pic/prod/lrw', 'pic/prod/lsf', 'pic/prod/univ', 'pic/prod/tyco',
            'pic/prod/mtlaurel', 'pic/prod/elseg', 'pic/prod/mworld']:
        name = cred['photo_credit.name'][2:] if cred['photo_credit.name'][1] == '_' else cred['photo_credit.name']
        url = 'lineup.cgi?year=%s&region=%s&lty=all#%s' % (name[:4], name[4].upper(), int(name[5:]))
    # elif cred['photo_credit.path'] == 'pic/set/convoy':
    return '<div class="entry">%s</div>' % (
        pif.render.format_link(
            url,
            pif.render.format_image_required(
                cred['photo_credit.name'], pdir=cred['photo_credit.path'], made=True,
                largest=mbdata.IMG_SIZ_LARGE, preferred=mbdata.IMG_SIZ_SMALL, also={'width': 200}))
    )


def photog_ind(pif, photog):
    return (
        '<div class="entry"><span class="name">%s</span><br><a href="photogs.cgi?id=%s">%s<br>%d credit%s</a></div>' % (
            pif.render.format_link(photog['photographer.url'], photog['photographer.name']), photog['photographer.id'],
            pif.render.format_image_required(
                photog['c.name'], pdir=photog['c.path'], made=True,
                largest=mbdata.IMG_SIZ_LARGE, preferred=mbdata.IMG_SIZ_SMALL, also={'width': 200}),
            photog['count'], 's' if photog['count'] != 1 else ''))


@basics.web_page
def photographers(pif):
    pif.render.print_html()
    photog_id = pif.form.get_str('id')
    header = footer = ''
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/photogs.cgi', 'Photographers')
    if photog_id:
        photog = pif.dbh.fetch_photographer_counts(photog_id).first
        if not photog:
            raise useful.SimpleError('That photographer was not found.')
        pif.render.hierarchy_append('/cgi-bin/photogs.cgi?id=%s' % photog_id, photog.photographer.name)
        pif.render.title = photog.photographer.name
        page = pif.form.get_int('p')
        entries = [render.Entry(text=credit_show(pif, x))
                   for x in pif.dbh.fetch_photo_credits_page(photog_id, page=page)]
        if page > 0:
            footer += pif.render.format_button_link('previous', 'photogs.cgi?id=%s&p=%d' % (photog_id, page - 1))
        if (page + 1) * 100 < photog['count']:
            if footer:
                footer += ' - '
            footer += pif.render.format_button_link('next', 'photogs.cgi?id=%s&p=%d' % (photog_id, page + 1))
        header += '%s credit%s' % (photog['count'], 's' if photog.count != 1 else '')
        if photog["count"] > 100:
            header += ' - Page %d' % (page + 1)
        if photog.photographer.url:
            header += ' - ' + pif.render.format_button_link('visit website', photog.photographer.url)
    else:
        # hide private
        entries = [render.Entry(text=photog_ind(pif, x)) for x in pif.dbh.fetch_photographer_counts()]
    lsection = render.Section(range=[render.Range(entry=entries)])
    llineup = render.Matrix(section=[lsection], header=header, footer=footer)
    return pif.render.format_template('simplematrix.html', nofooter=True,
                                      llineup=llineup.prep())


# -- commands


def add_credits(pif, photographer_id, *args):
    for fn in args:
        if '/' not in fn:
            print('must have path:', fn)
        else:
            pif.render.message('Credit added: ', pif.dbh.write_photo_credit(photographer_id, *fn.rsplit('/', 1)))


def ren(pth, cas, ov, nv):
    fl = glob.glob(os.path.join(pth, '?_' + cas + '-' + ov + '.jpg'))
    for fn in fl:
        nn = fn[:fn.rfind('-')] + '-' + nv + '.jpg'
        print('ren', fn, nn)
        if not os.path.exists(nn):
            os.rename(fn, nn)


def fix_pix(pif, *caslist):
    pth = '.' + config.IMG_DIR_VAR
    # piclist = []
    casvars = {}

    for pic in glob.glob(os.path.join(pth, '*.jpg')):
        pic = pic[len(pth) + 1:-4]
        if pic[1] != '_' and pic.find('-') < 0:
            print('bad:', pic)
            continue
        pic = pic[2:]
        cas, var = pic.split('-', 1)
        casvars.setdefault(cas, [])
        casvars[cas].append(var)

    if not caslist:
        caslist = sorted(casvars.keys())

    for cas in caslist:
        dbvars = pif.dbh.fetch_variations(cas)
        # casvar = casvars.get(cas, [])
        # print(cas, [x['variation.var'].lower() for x in dbvars])
        for var in casvars[cas]:
            # print(' ', var)
            found = False
            for dbvar in dbvars:
                if dbvar['variation.var'].lower() == var:
                    found = True
                    # print('    Ok', cas, var)
                    break  # ok!
                if ('0' + dbvar['variation.var']).lower() == var:
                    ren(pth, cas, var, var[1:])
                    found = True
                    break
                if ('00' + dbvar['variation.var']).lower() == var:
                    ren(pth, cas, var, var[2:])
                    found = True
                    break
            if not found:
                if os.path.exists('.' + useful.relpath(config.LIB_MAN_DIR, cas)):
                    for src in glob.glob(os.path.join(pth, '?_' + cas + '-' + var + '.jpg')):
                        if not os.path.exists(useful.relpath('.', config.LIB_MAN_DIR, cas + src[src.rfind('/'):])):
                            print('should rename', src,
                                  useful.relpath('.', config.LIB_MAN_DIR, cas + src[src.rfind('/'):]))
                            # os.rename(src, useful.relpath('.', config.LIB_MAN_DIR, cas + src[src.rfind('/'):]))
                else:
                    print('    Bad var:', cas, var, [x['variation.var'] for x in dbvars])

            for dbvar in dbvars:
                if not dbvar['variation.picture_id']:
                    fn = dbvar['variation.mod_id'] + '-' + dbvar['variation.var'] + '.jpg'
                    ensmallen('.' + config.IMG_DIR_VAR, fn)


def ensmallen(pdir, fn):
    ipth = useful.relpath(pdir, 's_' + fn).lower()
    opth = useful.relpath(pdir, 't_' + fn).lower()
    if os.path.exists(ipth) and not os.path.exists(opth):
        print('ensmallen', fn)
        pipes = [['/usr/local/bin/jpegtopnm'], ["/usr/local/bin/pamscale", "-xsize", str(100)],
                 ['/usr/local/bin/pnmtojpeg']]
        open(opth, 'w').write(useful.pipe_chain(open(ipth), pipes))


# ---- count ---------------------------------


def count_blisters(fl):
    fn_re = re.compile(r'[0-9][0-9][a-z][0-9][0-9]*\.')
    cnt = 0
    for fn in fl:
        m = fn_re.match(fn)
        if m:
            pass  # print(fn, 'yes')
            cnt += 1
        else:
            pass  # print(fn, '-')
    return cnt


def count_castings(fl):
    global castings
    fn_re = re.compile(r'[a-z]_(?P<c>[a-z0-9]*)(-[a-z0-9]*)?\.')
    cnt = 0
    for fn in fl:
        m = fn_re.match(fn)
        if m:
            pass  # print(fn, m.group('c'))
            if m.group('c') in castings:
                cnt += 1
        else:
            pass  # print(fn, '-')
    return cnt


def count_all(fl):
    return len(fl)


def zero(fl):
    return 0


def check_library(pif):
    fl = os.listdir('lib/man')
    ml = [x.replace('/', '_').lower() for x in pif.dbh.fetch_casting_ids()]
    for f in sorted(set(fl) - set(ml)):
        if not f.endswith('~') and '.' not in f:
            print(f)


def count_images(pif):
    print("This has not been rewritten to match the moved directories.")
    global castings
    castings = [x.lower() for x in pif.dbh.fetch_casting_ids()]

    dirs = [
        (config.IMG_DIR_ACC, count_all),
        (config.IMG_DIR_ADD, zero),
        (config.IMG_DIR_ADS, zero),
        (config.IMG_DIR_ART, zero),
        (config.IMG_DIR_BLISTER, count_all),
        (config.IMG_DIR_BOOK, zero),
        (config.IMG_DIR_BOX, zero),
        (config.IMG_DIR_CAT, zero),
        (config.IMG_DIR_PROD_CODE_2, count_all),
        (config.IMG_DIR_COLL_43, zero),
        (config.IMG_DIR_PROD_COLL_64, count_all),
        (config.IMG_DIR_CONVOY, zero),
        (config.IMG_DIR_ERRORS, zero),
        (config.IMG_DIR_MAN_ICON, zero),
        (config.IMG_DIR_KING, zero),
        (config.IMG_DIR_LESNEY, zero),
        (config.IMG_DIR_PROD_LRW, count_blisters),
        (config.IMG_DIR_PROD_LSF, count_blisters),
        (config.IMG_DIR_MAKE, zero),
        (config.IMG_DIR_MAN, count_castings),
        (config.IMG_DIR_PROD_MWORLD, count_blisters),
        (config.IMG_DIR_PROD_EL_SEG, count_blisters),
        (config.IMG_DIR_PROD_MT_LAUREL, count_blisters),
        (config.IMG_DIR_PROD_PACK, zero),
        (config.IMG_DIR_PICS, zero),
        (config.IMG_DIR_PROD_SERIES, count_all),
        (config.IMG_DIR_SKY, count_all),
        (config.IMG_DIR_PROD_TYCO, count_blisters),
        (config.IMG_DIR_PROD_UNIV, count_blisters),
        (config.IMG_DIR_VAR, count_castings),
    ]

    t = 0
    for dirpath, counter in dirs:
        fl = os.listdir('.' + dirpath)
        dt = counter(filter(lambda x: x.endswith('.jpg'), fl))
        dt += counter(filter(lambda x: x.endswith('.gif'), fl))
        print(dirpath, dt)
        t += dt
    print(t)


def check_credits(pif):
    creds = pif.dbh.fetch_photo_credits(photographer_id='DT')
    pif.dbh.depref('photo_credit', creds)
    for cred in creds:
        fn = '/'.join(pif.render.find_image_file(cred['name'], prefix='s', pdir=cred['path']))
        if fn:
            sz = imglib.get_size(fn)
            if not sz:
                print('size not found for', fn)
            else:
                print(sz, fn)
        else:
            print('file not found for', fn)


def do_stuff(pif):
    imglib.get_credit_file()


def set_photog_name(pif, photog_id, name):
    photog = pif.dbh.fetch_photographer(photog_id)
    values = photog.todict()
    values['name'] = name
    pif.dbh.write_photographer(photog_id, values, verbose=True)


# ---- ---------------------------------------


cmds = {
    ('i', icon_main, "icon: [-a] [-b banner] [-n name] mod_id ..."),
    ('a', add_credits, "add credit: photog picture ..."),
    ('f', fix_pix, "fix pix: mod_id ..."),
    ('c', count_images, "count"),
    ('l', check_library, "check library"),
    ('k', check_credits, "check credits"),
    ('x', do_stuff, "x"),
    ('n', set_photog_name, "set photographer name <id> <name>"),
}


# ---- ---------------------------------------


if __name__ == '__main__':  # pragma: no cover
    basics.process_command_list(cmds=cmds, dbedit='', switches='av', options='bn')
