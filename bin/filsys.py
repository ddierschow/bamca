#!/usr/local/bin/python

import datetime
import filecmp
import glob
from io import open
import os
import re
import requests
import stat

import basics
import config
import images
import imglib
import tumblr
import useful


def show_list(title, tdir, fl, view=False):
    if not fl:
        return ''
    # mlen = reduce(lambda x, y: max(x, len(y)), fl, 0)
    mlen = max([len(x) for x in fl])
    cols = max(1, 160 // max(1, mlen))
    clen = (len(fl) - 1) // cols + 1
    ffl = [fl[(x * clen):((x + 1) * clen)] for x in range(0, cols)]
    ostr = '<h4>{} ({})</h4>\n'.format(title, len(fl))
    ostr += "<table width=100%><tr valign=top>\n"
    for cl in ffl:
        ostr += "<td width={}%>\n".format(100 // cols)
        for f in cl:
            root, ext = useful.root_ext(f.strip())
            fst = os.stat(tdir + '/' + f)
            perms = fst[stat.ST_MODE]
            if f[0] == '.':
                ostr += '<i>{}</i><br>\n'.format(f)
            elif stat.S_ISDIR(perms):
                ostr += '<a href="/cgi-bin/traverse.cgi?d={}">{}/</a><br>\n'.format(tdir + '/' + f, f)
            elif tdir.startswith('../'):
                ostr += '<a href="/cgi-bin/traverse.cgi?d={}&f={}">{}</a><br>\n'.format(tdir, f, f)
            elif f[-4:] == '.dat':
                ostr += '<a href="/cgi-bin/traverse.cgi?d={}&f={}">{}</a><br>\n'.format(tdir, f, f)
            elif (perms & 5) == 0:
                ostr += '{}<br>\n'.format(f)
            elif ext in imglib.itypes:
                if view:
                    ostr += '<a href="/{}/{}">{}</a><br>\n'.format(tdir, f, f)
                else:
                    ostr += '<a href="/cgi-bin/imawidget.cgi?d={}&f={}">{}</a><br>\n'.format(tdir, f, f)
            else:
                ostr += '<a href="../{}">{}</a><br>\n'.format(tdir + '/' + f, f)
        ostr += "</td>\n"
    ostr += "</tr></table>\n"
    ostr += '<br><hr>\n'
    return ostr


def show_dir(pif, tform):
    targs, credits = make_targs(pif, tform.dirname)
    if not os.path.exists(tform.tdir):
        raise useful.SimpleError('Path does not exist.')

    ostr = '<hr>\n'
    # dl, gl, ol, sl, xl = imglib.get_dir(tform.tdir)
    files = imglib.get_dir(tform.tdir, name_has=tform.has)

    ostr += show_list(files['titles']['dir'], tform.tdir, files['dir'], tform.view)

    if files['graf']:
        if tform.graf:
            ostr += '<h4>{} ({})</h4><div class="glist">\n'.format(files['titles']['graf'], len(files['graf']))
            for f in files['graf']:
                perms = os.stat(tform.tdir + '/' + f)[stat.ST_MODE]
                if (perms & 4) == 0:
                    ostr += '{}<br>\n'.format(f)
                elif tform.graf:
                    ostr += pif.ren.format_link(
                        'imawidget.cgi',
                        '<img src="../{}/{}" border=0>{}<br>'.format(tform.tdir, f, f),
                        {'d': tform.tdir, 'f': f, 'man': tform.mod, 'newvar': tform.var, 'cy': 0, 'suff': tform.suff})
                else:
                    ostr += '<a href="../{}">{}</a><br>\n'.format(tform.tdir + '/' + f, f)
                ostr += check_image(pif, targs, os.path.join(pif.ren.pic_dir, f), credits)
            ostr += '</div><hr>\n'
        else:
            ostr += show_list(files['titles']['graf'], tform.tdir, files['graf'], tform.view)

    ostr += show_list(files['titles']['log'], tform.tdir, files['log'], tform.view)
    ostr += show_list(files['titles']['dat'], tform.tdir, files['dat'], tform.view)
    ostr += show_list(files['titles']['exe'], tform.tdir, files['exe'], tform.view)
    ostr += show_list(files['titles']['other'], tform.tdir, files['other'], tform.view)

    if pif.ren.is_admin:
        ostr += '<a href="upload.cgi?d={}">{}</a>\n'.format(tform.tdir, pif.form.put_text_button('upload'))

    if files['graf']:
        ostr += '<form action="traverse.cgi">\n' + pif.create_token()
        ostr += '<a href="traverse.cgi?g=1&d={}">{}</a> or \n'.format(
            tform.tdir, pif.form.put_text_button('show all pictures'))
        ostr += 'Pattern <input type="text" name="p">\n'
        ostr += '<input type="hidden" name="d" value="{}">\n'.format(tform.tdir)
        ostr += pif.form.put_checkbox('du', [('1', 'Dupes',)])
        ostr += pif.form.put_checkbox('co', [('1', 'Compact',)])
        ostr += pif.form.put_checkbox('th', [('1', 'Thumbs',)])
        ostr += pif.form.put_checkbox('si', [('1', 'Sized',)])
        ostr += pif.form.put_checkbox('mr', [('1', 'Recent',)])
        if pif.ren.is_admin:
            lty = [('nrm', 'Normal',), ('shc', 'Categorize',), ('mss', 'VMass',), ('pms', 'PMass',),
                   ('shm', 'Shelve',), ('suf', 'Resuffix',), ('crd', 'Credit',)]
            ostr += '<br>'
            ostr += pif.form.put_radio('lty', lty, 'nrm')
        ostr += pif.form.put_button_input()
        ostr += '<br>\n'
        ostr += 'Size X <input type="text" name="sx">\n'
        ostr += 'Size Y <input type="text" name="sy">\n'
        ostr += '</form>\n'
    return ostr


def check_image(pif, targs, src, credits):
    ssize = os.stat(src).st_size
    ostr = ''
    for tf in targs:
        if tf[1] == ssize and filecmp.cmp(tf[0], src):
            ostr += tf[0][tf[0].rfind('/') + 1:] + ' ' + credits.get(tf[0], '') + '<br>'
    return ostr


imginputs = '<input type="checkbox" name="rm" value="%(f)s"> rm<input type="checkbox" name="mv" value="%(f)s %(b)s"> mv'
imginput = '''<input type="checkbox" name="rm" value="%(f)s"> rm
<input type="text" name="ren.%(f)s"> rename
'''


def img(pif, args, base='', shlv=False, cate=False, rsuf=False, sx=0, sy=0, mss=False, pms=False, cred=False,
        targs=[], credits={}, mans={}, also={}, cpct=False):
    nalso = {'border': 0}
    nalso.update(also)
    if sx:
        nalso['width'] = sx
    if sy:
        nalso['height'] = sy
    ostr = '' if cpct else '<tr>\n'
    args.sort()
    for arg in args:
        f_st = os.stat(os.path.join(pif.ren.pic_dir, arg))
        f_date = str(datetime.datetime.fromtimestamp(f_st.st_mtime)) if not cpct else ''
        root, ext = useful.root_ext(arg.strip())
        inp = ''
        pic = pif.ren.format_image_required([root], suffix=ext, also=nalso)
        if shlv or cate:
            inp += ''' {}/<input type="text" name="lib.{}"> '''.format("lib" if cate else "lib/man", arg)
            for man in sorted(mans.keys()):
                for pref in mans[man]:
                    if root.startswith(pref):
                        inp += ' ' + man
        elif mss:
            inp += '''<br><input type="text" name="var.{}"> var'''.format(arg)
        elif pms:
            inp += '''<br><input type="text" name="nam.{}"> nam'''.format(arg)
        elif rsuf:
            inp += '''<input type="text" name="rsfx.{}"> rsfx'''.format(arg)
        elif cred:
            fn = arg[:arg.find('.')] if '.' in arg else arg
            fn = fn[2:] if (fn[0] in 'sml' and fn[1] == '_') else fn
            inp += '''<input type="text" name="cred.{}" size="12" value="{}"> cred'''.format(fn, cred.get(fn, ''))
        else:
            pic = '<a href="imawidget.cgi?d={}&f={}&cy=0">{}</a>'.format(pif.ren.pic_dir, arg, pic)
            if arg == base:
                inp = imginputs % {'f': arg, 'b': root + 'z.' + ext}
            elif base:
                inp = imginputs % {'f': arg, 'b': base}
            else:
                inp = imginput % {'f': arg}
        if cpct:
            ostr += '<div class="filc">{}<br>{}<br>{}</div>\n'.format(pic, arg, inp)
        else:
            ostr += pif.ren.format_cell(0, '{}<br>{}{} {}'.format(pic, arg, inp, f_date))
        if mss or pms:
            ostr += '</td><td>'
            ostr += check_image(pif, targs, os.path.join(pif.ren.pic_dir, arg), credits)
    if not cpct:
        ostr += '</tr>\n'
    return ostr


def flist_sort(flist, tform):
    if tform.rcnt and not tform.sizd:
        # stat tdir+fn, get st_mtime, sort by date
        tlist = [os.stat(os.path.join(tform.tdir, fn)).st_mtime for fn in flist]
        flist.sort(key=dict(zip(flist, tlist)).get, reverse=True)
    else:
        flist.sort()


def make_targs(pif, dirname):
    return ([(x, os.stat(x).st_size)
             for x in sorted(glob.glob('.' + config.IMG_DIR_VAR + '/l_' + dirname + '-*.*'))],
            {'.' + config.IMG_DIR_VAR + '/l_' + x['photo_credit.name'] + '.jpg': x['photographer.id']
             for x in pif.dbh.fetch_photo_credits_for_vars(config.IMG_DIR_VAR, dirname)})


def show_imgs(pif, tform):
    credit_file = imglib.get_credit_file()

    def get_cred_for_file(fn):
        for x, y in credit_file.get(tform.tdir, {}).items():
            if fn.startswith(x):
                return y
        return ''

    print('<hr>')
    print('<form action="traverse.cgi" method="post">' + pif.create_token())
    plist = tform.patt.split(',')
    img_args = {'shlv': tform.shlv, 'cate': tform.cate, 'sx': tform.szx, 'sy': tform.szy, 'mss': tform.mss,
                'pms': tform.pms, 'cpct': tform.cpct}
    if tform.mss:
        print('Credit ' + pif.form.put_text_input('credit', 4, value=pif.form.get_str('credit')))
        print('<br>')
        img_args['targs'], img_args['credits'] = make_targs(pif, tform.dirname)
    elif tform.pms:
        # maybe put size here?  assume m_
        print('Credit ' + pif.form.put_text_input('credit', 4))
        print('<input type="hidden" name="tysz" value="m">')
        print('<br>')
        img_args['targs'] = []
    elif tform.shlv and tform.dirname == 'tilley':
        img_args['mans'] = imglib.get_tilley_file()
    if tform.cred:
        img_args['cred'] = {x['photo_credit.name']: x['photographer.id']
                            for x in pif.dbh.fetch_photo_credits(path=tform.tdir)}
    elif tform.tdir.startswith('lib/man'):
        pass  # img_args['cred'] = {
    for pent in plist:
        flist = useful.read_dir(pent, tform.tdir)
        if tform.sizd:
            flist = list(set([x[2:] for x in flist if len(x) > 2 and x[1] == '_']))
        flist_sort(flist, tform)
        img_also = {'width': '200'} if tform.thum else {}
        img_args['also'] = img_also
        if tform.cpct:
            print('<div class="filt">')
            for fp in flist:
                if tform.sizd:
                    for fn in useful.read_dir('?_' + fp, pif.ren.pic_dir):
                        print('<div class="filc">')
                        img_also['title'] = fn
                        print(img(pif, fp, **img_args))
                        print('</div>')
                    print('<br>')
                else:
                    print('<div class="filc">')
                    img_also['title'] = fp
                    print(img(pif, [fp], **img_args))
                    print('</div>')
            print('</div>')

        else:
            print('<table class="glist">')
            for fp in flist:
                if tform.sizd:
                    dlist = useful.read_dir('?_' + fp, pif.ren.pic_dir)
                    flist_sort(dlist, tform)
                    if not tform.dups or len(dlist) > 1:
                        print(img(pif, dlist, **img_args))
                else:
                    img_also['title'] = fp
                    # also sized + dups
                    if tform.dups:
                        root, ext = useful.root_ext(fp)
                        dlist = useful.read_dir(root + '*' + ext, pif.ren.pic_dir)
                        if len(dlist) > 1:
                            flist_sort(dlist, tform)
                            print(img(pif, dlist, fp, **img_args))
                    else:
                        print(img(pif, [fp], rsuf=tform.rsuf, **img_args))
            print('</table>')
            print('<hr>')
    print(f'<input type="hidden" name="d" value="{tform.tdir}">')
    print('<input type="hidden" name="sc" value="1">')
    if tform.cate:
        print('<input type="hidden" name="pre" value="">')
        print('<input type="hidden" name="lty" value="shc">')
    elif tform.shlv:
        print('<input type="hidden" name="pre" value="man">')
        print('<input type="hidden" name="lty" value="shm">')
    elif tform.rsuf:
        print('<input type="hidden" name="lty" value="suf">')
    elif tform.mss:
        print('<input type="hidden" name="lty" value="mss">')
        print('promote <input type="text" name="msspromote">')
    elif tform.pms:
        print('<input type="hidden" name="lty" value="pms">')
    elif tform.cred:
        print('<input type="hidden" name="lty" value="crd">')
    print(pif.form.put_button_input())
    print('<a href="upload.cgi?d=%s&r=unset">%s</a>' % (tform.tdir, pif.form.put_text_button('upload')))
    print('</form>')


def show_script(pif, tform):
    if tform.mss:
        do_var_masses(pif, tform)
        return
    if tform.pms:
        do_prod_masses(pif, tform)
        return
    if tform.rsuf:
        for fn, suf in tform.rsfx:
            root, ext = os.path.splitext(fn)
            if '-' in root:
                root = root[:root.find('-')]
            nfn = root + '-' + suf + ext
            print(fn, root + '-' + suf + ext, '<br>')
            useful.file_mover(os.path.join(tform.tdir, fn), os.path.join(tform.tdir, nfn), mv=True, inc=True)
        return
    if tform.cred:
        for fn, cred in pif.form.get_list(start='cred.'):
            print(fn, cred, '<br>')
            pif.ren.message('Credit added: ', pif.dbh.write_photo_credit(cred, tform.tdir, fn, verbose=False))
        return
    rend = dict(tform.renl)
    print('<pre>')
    for ren in tform.renl:
        fn = ren[1]
        if '.' not in fn:
            fn += ren[0][ren[0].rfind('.'):]
        if not os.path.exists(fn):
            useful.file_mover(os.path.join(tform.tdir, ren[0]), os.path.join(tform.tdir, fn), mv=True, inc=True)
        else:
            print('#ren', os.path.join(tform.tdir, ren[0], os.path.join(tform.tdir, fn)))
    for lb in tform.libl:
        dest = lb[1]  # we might have renamed this...
        if lb[0] in rend:
            lb[0] = rend[lb[0]]
        useful.make_dir(useful.relpath('.', config.LIB_DIR, tform.pre, dest), 0o775)
        useful.file_mover(os.path.join(tform.tdir, lb[0]), useful.relpath('.', config.LIB_DIR, tform.pre, dest, lb[0]),
                          mv=True, inc=True)
    for rm in tform.rml:
        if os.path.exists(os.path.join(tform.tdir, rm)):
            useful.file_mover(os.path.join(tform.tdir, rm), None, mv=True)
    for mv in tform.mvl:
        fsp = mv.split(' ')
        if os.path.exists(os.path.join(tform.tdir, fsp[0])):
            useful.file_mover(os.path.join(tform.tdir, fsp[0]), os.path.join(tform.tdir, fsp[1]), mv=True, inc=True)
    print('</pre>')


def do_var_masses(pif, tform):
    for fn, var in pif.form.get_list(start='var.'):
        print('<hr>')
        print(fn, var, '<br>')
        eform = images.EditForm(pif, tdir=pif.ren.pic_dir, fn=fn)
        eform.ot = 'jpg'
        eform.tysz = 's'
        eform.read_file('')
        eform.man = eform.calc_man()
        eform.var = eform.nvar = var
        eform.mass_resize(pif)
    var_id = pif.form.get('msspromote')
    if var_id:
        mod_id = eform.calc_man()
        imglib.promote_picture(pif, mod_id, var_id)


def do_prod_masses(pif, tform):
    ddir = tform.tdir.replace('lib', 'pic')
    print(pif.form.get_str('credit'), ddir, '<br>')
    if not os.path.exists(ddir):
        raise useful.SimpleError('Path does not exist.')
    siz = pif.form.get('tysz')
    cred = pif.form.get_str('credit')
    if cred:
        photog = pif.dbh.fetch_photographer(cred)
        if not photog:
            cred = ''
    for fn, nam in pif.form.get_list(start='nam.'):
        print('<hr>')
        print(fn, ddir, siz, nam, '<br>')

        rf = [False, False, False, False, False]
        pth = tform.tdir + '/' + fn
        q = (0, 0,) + imglib.get_size(pth)
        nname = ddir + '/' + siz + '_' + nam + '.jpg'
        ts = (400, 0)
        ofi = imglib.shrinker(pth, nname, q, ts, rf)
        imglib.simple_save(ofi, nname)
        images.file_log(nname, tform.tdir)
        url = pif.secure_prod + nname[1:]
        link = pif.secure_prod
        title = nam
        if cred and not photog.flags & config.FLAG_PHOTOGRAPHER_PRIVATE:
            title += ' credited to ' + photog.name
        pif.ren.message('Post to Tumblr: ', tumblr.Tumblr(pif).create_photo(caption=title, source=url, link=link))
        pif.ren.message('Credit added: ', pif.dbh.write_photo_credit(cred, ddir, nam))


def show_file(pif, tform):
    if not os.path.exists(tform.tdir + '/' + tform.fnam):
        raise useful.SimpleError('Path does not exist.')
    print(pif.ren.format_button_link('delete', link=pif.request_uri + '&delete=1&act=1'))
    if os.path.exists(os.path.join(tform.tdir, 'archive')):
        print(pif.ren.format_button_link('archive', link=pif.request_uri + '&archive=1&act=1'))
    if os.path.exists(os.path.join(tform.tdir, 'fixed')):
        print(pif.ren.format_button_link('fixed', link=pif.request_uri + '&fixed=1&act=1'))
    if os.path.exists(os.path.join(tform.tdir, 'spam')) or os.path.exists(os.path.join(tform.tdir, '..', 'spam')):
        print(pif.ren.format_button_link('spam', link=pif.request_uri + '&spam=1&act=1'))
    root, ext = useful.root_ext(tform.fnam)
    if not os.path.exists(tform.tdir + '/' + tform.fnam):
        print("file not found")
    elif ext in imglib.itypes:
        # if tform.tdir.startswith('..'):
        #     print('<img src="/cgi-bin/image.cgi?d=%s&f=%s">' % (tform.tdir, tform.fnam))
        # else:
        show_picture(pif, tform.fnam)
    # elif ext == 'dat':
    #     show_table(pif, tform)
    elif tform.tdir.startswith('../../comments'):
        fil = open(tform.tdir + '/' + tform.fnam).read()
        if '{' in fil and '}' in fil:
            print(fil[:fil.index('{')])
            data = eval(fil[fil.index('{'):fil.rindex('}') + 1])
            print('<p><dl>')
            for key, val in sorted(data.items()):
                print('<dt>', key, '</dt><dd>', val, '</dd>')
            print('</dl>')
            print(fil[fil.rindex('}') + 1])
        else:
            print('<p>', fil)
    elif tform.tdir == '../../logs':
        print('<p><div style="font-family: monospace;">')
        fil = open(tform.tdir + '/' + tform.fnam).readlines()
        for i in range(len(fil)):
            if fil[i].startswith('uri = '):
                fil[i] = """uri = <a href="%s">%s</a>\n""" % (fil[i][9:-4], fil[i][9:-4])
                break
        print('<pre>')
        print(''.join(fil))
        print('</pre>')
        print('</div>')
    else:
        print('<p>')
        fil = open(tform.tdir + '/' + tform.fnam).readlines()
        for i in range(len(fil)):
            if fil[i].startswith('uri = '):
                fil[i] = """uri = <a href="%s">%s</a>\n""" % (fil[i][9:-4], fil[i][9:-4])
                break
        print('<br>'.join(fil))


# for things out of http space:
# print('<img src="/cgi-bin/image.cgi?d=%s&f=%s">' % (pif.ren.pic_dir, fn))
def show_picture(pif, fn, pdir=None):
    if pdir:
        pif.ren.pic_dir = pdir
    # picker(pif, form, fn)
    root, ext = useful.root_ext(fn.strip())
    pif.ren.comment(root, ext)
    print('<table><tr><td></td><td>' + pif.ren.format_image_art('hruler.gif') + '</td></tr>')
    print('<tr><td valign="top">' + pif.ren.format_image_art('vruler.gif') + '</td><td valign="top">')
    print('<a href="/cgi-bin/image.cgi?d=%s&f=%s"><img src="/cgi-bin/image.cgi?d=%s&f=%s"></a>' %
          (pif.ren.pic_dir, fn, pif.ren.pic_dir, fn))
    print('</td></tr></table>')


colors = ["#FFFFFF", "#CCCCCC"]


def do_action(pif, tform):
    print('<div class="warning">')
    # nfn = images.action(pif, tform.tdir, tform.fnam, tform.act)
    nfn = imglib.ActionForm(pif).read(pif.form).action(pif, tform.tdir, tform.fnam)['fn']
    print('</div><br>')
    if nfn:
        show_picture(pif, nfn)
    else:
        tform.graf = 0
        print(show_dir(pif, tform))


class TraverseForm(object):
    def __init__(self):
        pass

    def read(self, pif):
        pif.ren.pic_dir = self.tdir = pif.form.get_str('d', '.')
        if self.tdir.endswith('/'):
            self.dirname = self.tdir[self.tdir[:-1].rfind('/') + 1:-1]
        elif '/' in self.tdir:
            self.dirname = self.tdir[self.tdir.rfind('/') + 1:]
        else:
            self.dirname = self.tdir
        if self.tdir.startswith('./lib') or self.tdir.startswith('lib'):
            self.alt = self.tdir.replace('lib', 'pic')
        elif self.tdir.startswith('./pic') or self.tdir.startswith('pic'):
            self.alt = self.tdir.replace('pic', 'lib')
        else:
            self.alt = ''
        self.libl = pif.form.get_list(start='lib.', defval='')
        self.renl = pif.form.get_list(start='ren.', defval='')
        self.rsfx = pif.form.get_list(start='rsfx.', defval='')
        # cols = ''  # pif.form.get_str('cols')
        # h = 0  # pif.form.get_int('h')
        self.sorty = pif.form.get_int('sort')
        self.view = pif.form.get_bool("v")
        self.graf = pif.form.get_int("g")
        self.fnam = pif.form.get_str("f")
        self.patt = pif.form.get_str("p")
        self.has = pif.form.get_str("has")
        self.suff = pif.form.get_str("suff")
        self.dups = pif.form.get_int("du")
        self.cpct = pif.form.get_int("co")
        self.thum = pif.form.get_int("th")
        self.cate = pif.form.get_radio("lty", "shc")
        self.mss = pif.form.get_radio("lty", "mss")
        self.pms = pif.form.get_radio("lty", "pms")
        self.shlv = pif.form.get_radio("lty", "shm")
        self.rsuf = pif.form.get_radio("lty", "suf")
        self.cred = pif.form.get_radio("lty", "crd")
        self.sizd = pif.form.get_int("si")
        self.rcnt = pif.form.get_int("mr")
        self.scrt = pif.form.get_int('sc')
        self.act = pif.form.get_int('act')
        self.cycle = pif.form.get_int("cy")  # srsly?
        self.mvl = pif.form.get_list('mv')
        self.rml = pif.form.get_list('rm')
        self.pre = pif.form.get_str('pre')
        self.mod = pif.form.get_str('mod')
        if not self.mod:
            self.mod = pif.form.get_str('man')
        self.var = pif.form.get_str('var')
        self.szx = pif.form.get_int("sx")
        self.szy = pif.form.get_int("sy")

        pif.ren.title = self.tdir
        if self.fnam:
            pif.ren.title += '/' + self.fnam
        return self


@basics.web_page
def main(pif):  # traverse main
    os.environ['PATH'] += ':/usr/local/bin'
    pif.ren.print_html()
    pif.restrict('vma')
    tform = TraverseForm().read(pif)

    pif.ren.set_page_extra(pif.ren.increment_js)
    print(pif.ren.format_head())
    useful.header_done()
    print(pif.form.get_form())
    if tform.alt:
        print(pif.ren.format_link('/cgi-bin/traverse.cgi?d=' + tform.alt, tform.alt))
    print('<br>')
    if tform.patt:
        print('show_imgs<br>')
        show_imgs(pif, tform)
    elif tform.scrt:
        print('show_script<br>')
        show_script(pif, tform)
    elif tform.act:
        print('show_action<br>')
        do_action(pif, tform)
    elif tform.fnam:
        print('show_file<br>')
        show_file(pif, tform)
    else:
        print('show_dir<br>')
        print(show_dir(pif, tform))
    print(pif.ren.format_tail())


# ----- updcommits -----------------------------------------------------

'''
This script takes commits from the git log and puts them
into the site activity table in the database.

It also does some other housekeeping: man2csv, and writing
the config file for php's use.
'''


def read_commits(endtime):
    log = useful.simple_process(("/usr/local/bin/git", "log",))
    commits = list()
    # Date:   Fri Jun 13 19:26:34 2014 +0200
    date_re = re.compile(r'Date:\s*(?P<d>... ... \d+ \d+:\d+:\d+ \d+)')
    for log_msg in re.compile(r'\ncommit ', re.M).split(log):
        if log_msg.find('Merge: ') >= 0:
            continue
        m = date_re.search(log_msg)
        if not m:
            continue
        s = m.group('d')
        commit = dict()
        commit['by_user_id'] = 1
        commit['name'] = 'commit'
        commit['description'] = log_msg.split('\n', 4)[4].strip()
        commit['timestamp'] = datetime.datetime.strptime(s, '%a %b %d %X %Y')
        if commit['timestamp'] <= endtime:
            continue
        commits.append(commit)
    commits.sort(key=lambda x: x['timestamp'])
    return commits


def write_php_config_file(pif):
    print("Writing PHP config file.")
    fin = open('../bin/config.py').readlines()
    fout = ['<?php\n', '// Generated file.  Do not modify.\n']
    for ln in fin:
        if ln.startswith('#'):
            ln = '//' + ln[1:]
        elif ln.find('=') >= 0:
            ln = '$' + ln.replace('\n', ';\n')
        fout.append(ln)
    fout.append('?>\n')
    open('../htdocs/config.php', 'w').writelines(fout)
    print()


def write_jinja2_config_file(pif):
    print("Writing Jinja2 config file.")
    fin = open('../bin/config.py').readlines()
    fout = ['{# Generated file.  Do not modify. #}\n']
    for ln in fin:
        if ln.startswith('#!'):
            continue
        elif ln.startswith('#'):
            ln = '{' + ln.strip() + ' #}\n'
        elif '0x' in ln:
            idx = ln.find('0x')
            ln = '{% set ' + ln[:idx] + str(eval(ln[idx:].strip())) + ' %}\n'
        elif '=' in ln:
            ln = '{% set ' + ln.strip() + ' %}\n'
        fout.append(ln)
    open('../templates/config.html', 'w').writelines(fout)
    print()


def check_lib_man(pif):
    man_ids = set([x.lower().replace('/', '_') for x in pif.dbh.fetch_casting_ids()])
    man_lib = set(os.listdir('.' + config.LIB_MAN_DIR))
    print("id's without libraries:")
    print(' '.join(sorted(man_ids - man_lib)))
    print()
    print("libraries without id's:")
    print(' '.join(sorted(man_lib - man_ids)))


def write_version_file(pif):
    print("Writing version file.")
    open('version.txt', 'wt').write('''<?php\n$version = "{}";\n?>\n'''.format(os.environ['BAMCA_VERSION']))


wiki_transform = {
    "References": '',
    "External links": '',
    "1 to 100 range": 'MB',
    "1-100 Series": 'MB',
    "1-100 series": 'MB',
    "1-102 Series": 'MB',
    "1-120 Series": 'MB',
    "1-120 range": 'MB',
    "1-125 Series": 'MB',
    "1-75 Range": 'MB',
    "1-75 Series": 'MB',
    "1-75 range": 'MB',
    "1-75 series": 'MB',
    "10-Packs": '10P',
    "5-Packs": '5P',
    "900 Range": 'TP',
    "900": 'TP',
    "Accesory Packs": 'AP',
    "Accessory Packs": 'AP',
    "Action Farming": 'FM',
    "Additional 2008 releases": 'Other',
    "Additional 2011 Releases": 'Other',
    "Additional 2012 Releases": 'Other',
    "Adventure 2000": 'A2K',
    "Battle Kings": 'BK',
    "Coca-Cola Series": 'CK',
    "Construction": 'CS',
    "Convoy": 'CY',
    "Convoys": 'CY',
    "Dinky Collection": 'DY',
    "Emergency": 'EM',
    "King Size": 'KS',
    "Lesney Editions": 'LE',
    "Licensed 5-Packs": 'L5P',
    "Major Packs": 'MP',
    "Matchbox 75": 'MB',
    "Matchbox Across America 50th Birthday Series": 'AAM',
    "Matchbox Birthday Hunts": 'BH',
    "Matchbox Originals": 'MO',
    "Matchbox Series 1-75": 'MB',
    "Matchbox Series No. 1-42": 'MB',
    "Matchbox Series Nos 1 to 29": 'MB',
    "Matchbox Series Nos. 1-75": 'MB',
    "Matchbox Series": 'MB',
    "Models of Yesteryear": 'MOY',
    "New Superfast": 'NSF',
    "Other Series": 'Other',
    "Other series": 'Other',
    "Real Working Rigs": 'RWR',
    "Sea Kings": 'SeaK',
    "See also": 'Other',
    "Series 1-75": 'MB',
    "Sky Busters": 'SB',
    "Sky-Busters": 'SB',
    "Skybusters": 'SB',
    "Specials": 'Spec',
    "Speed Kings": 'SpK',
    "Super Convoys": 'SCY',
    "Super Kings": 'SK',
    "SuperKings": 'SK',
    "Superkings": 'SK',
    "Two Packs": 'TP',
}


def write_wiki_file(pif):
    url = "https://matchbox.fandom.com/wiki/List_of_{}_Matchbox"
    link_re = re.compile(r'<h2><span class="mw-headline" id="(?P<id>[^"]*)">(?P<n>[^<]*)</span>')
    with open('pages/wikidat.php', 'wt') as fh:
        fh.write('<?php\n\n$dat = [\n')

        # $d = [1 => ['a' => '1', 'b' => 2], ['c' => '3', 'd' => '4']];
        year = 1953
        while (True):
            base_url = url.format(year)
            page = requests.get(base_url)
            if page.status_code != 200:
                break
            fh.write(f'  {year} => [\n    "{year}" => "{base_url}",\n')
            for k, v in link_re.findall(page.text):
                v = wiki_transform.get(v.strip(), v)
                if v:
                    fh.write(f'    "{k}" => "{v}",\n')
            fh.write('  ],\n')
            year += 1
            print('.', end='', flush=True)
        fh.write('];\n?>\n')
    print()


cmds = [
    ('p', write_php_config_file, "write php config"),
    ('j', write_jinja2_config_file, "write jinja2 config"),
    ('m', check_lib_man, "check libarary man id's"),
    ('v', write_version_file, "write version file"),
    ('w', write_wiki_file, "write wiki file"),
]


if __name__ == '__main__':  # pragma: no cover
    basics.process_command_list('editor', cmds=cmds, dbedit='')
