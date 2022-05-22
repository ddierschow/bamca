#!/usr/local/bin/python

# TODO: convert much of this to use jinja2 (http://jinja.pocoo.org)

import copy
import glob
import html
import http.client
import os
import re

import config
import javasc
import mbdata
import useful

pseud_re = re.compile(r'''<\$(?P<cmd>\S*)\s(?P<arg>[^>]*)>''')
graphic_types = ['jpg', 'gif', 'bmp', 'ico', 'png']


class Presentation(object):
    modal_js = javasc.def_modal_js
    incrsel_js = javasc.def_increment_select_js
    toggle_display_js = javasc.def_toggle_display_text_js
    reset_button_js = javasc.def_reset_button_js
    increment_js = javasc.def_increment_js
    increment_select_js = javasc.def_increment_select_js
    google_analytics_js = javasc.def_google_analytics_js
    image_selector_js = javasc.def_image_selector_js
    paste_from_clippy_js = javasc.def_paste_from_clippy_js
    font_awesome_js = javasc.def_font_awesome_js

    def __init__(self, page_id, verbose):
        self.is_html = False
        self.page_id = page_id
        self.art_dir = config.IMG_DIR_ART
        self.is_beta = False
        self.is_alpha = False
        self.title = 'BAMCA'
        self.unittest = False
        self.description = ''
        self.note = ''
        self.pic_dir = 'pic/pics'
        self.tail = dict()
        self.large = False
        self.verbose = verbose
        self.dump_file = None
        self.not_released = False
        self.hide_title = False
        self.flags = 0
        self.table_count = 0  # for making tables go away upon error
        self.hierarchy = list()
        self.flag_info = None
        self.shown_flags = set()
        self.secure = None
        self.styles = list(('main', 'fonts'))
        if '.' in self.page_id:
            self.styles.append(self.page_id[:self.page_id.find('.')])
        self.styles.append(self.page_id)
        self.extra = self.font_awesome_js
        self.comment_button = ''
        self.is_admin = False
        self.is_moderator = False
        self.is_user = False
        self.new_cookie = None
        self.footer = ''
        self.bamcamark = mbdata.bamcamark()
        self.filename = 'matchbox.csv'
        self.status_printed = 'unset'
        # if self.verbose:
        #     import datetime
        #     self.dump_file = open(os.path.join(config.LOG_ROOT,
        #                                        datetime.datetime.now().strftime('%Y%m%d.%H%M%S.log')), 'w')

    def __repr__(self):
        return "'<render.Presentation instance>'"

    def __str__(self):
        return "'<render.Presentation instance>'"

    def error_report(self):
        import pprint
        return pprint.pformat(self.__dict__, indent=2, width=132)

    def set_page_info(self, row):
        self.flags = row['page_info.flags'] or 0
        self.format_type = row['page_info.format_type']
        self.title = self.fmt_pseudo(row['page_info.title'])
        self.pic_dir = row['page_info.pic_dir']
        self.description = row['page_info.description']
        self.note = self.fmt_pseudo(row['page_info.note'])
        self.tail = {x: 1 for x in row['page_info.tail'].split(',')}

    def set_page_extra(self, extra):
        self.extra += extra

    def style_name(self, previous, prefix, col=None, id=None):
        class_ids = list()
        if previous:
            class_ids.append(previous)
        if col is not None and col != '':
            if id:
                class_ids.append(prefix + '_' + str(col) + '_' + id)
            class_ids.append(prefix + '_' + str(col))
        if id:
            class_ids.append(prefix + '_' + id)
        class_ids.append(prefix)
        return ' '.join(class_ids)

    def show_location(self):
        return ''.join(['<a href="%(link)s">%(name)s</a> &gt;\n' % lvl for lvl in self.hierarchy]) + '<br>'

    def hierarchy_append(self, link, txt):
        self.hierarchy.append({'link': link, 'name': txt})

    # immediate effect functions.

    def debug(self, *args):
        if self.verbose:
            print(' '.join([str(x) for x in args]))

    def message(self, *args):
        if self.dump_file:  # pragma: no cover
            self.dump_file.write(' '.join([str(x) for x in args]) + '\n')
        useful.write_message(*args)

    def comment(self, *args):
        if self.dump_file:  # pragma: no cover
            self.dump_file.write(' '.join([str(x) for x in args]) + '\n')
        elif self.verbose:
            useful.write_comment(*args)

    def comment_dict(self, name, arg):
        if self.verbose:
            print(useful.dump_dict_comment(name, arg))

    def print_html(self, content='text/html', status=200):
        if not useful.is_header_done():
            print('Content-Type:', content)
            if content == 'text/csv':
                print("Content-Description: File Transfer\nContent-Disposition: attachment; "
                      f"filename={self.filename}\nExpires: 0")
            print('Status:', status, http.client.responses.get(status, ''))
            self.status_printed = status
            # useful.html_done = True
            self.print_cookie()
            print()
            if content == 'text/html':
                self.is_html = True
                print('<!DOCTYPE html>')
            useful.header_done()

    def set_cookie(self, cookie):
        self.new_cookie = cookie

    def print_cookie(self):  # pragma: no cover
        if self.new_cookie:
            print(self.new_cookie.output())
            os.environ['HTTP_COOKIE'] = self.new_cookie.output()
        else:
            incookie = self.secure.cookies if self.secure.cookies else self.secure.get_cookies()
            if incookie and 'id' in incookie:
                incookie['id']['expires'] = -1
                print(incookie.output())
                if 'HTTP_COOKIE' in os.environ:
                    del os.environ['HTTP_COOKIE']

    # ---- upper level rendering blocks

    def format_head(self):
        pagetitle = ('BETA: ' if self.is_beta else 'ALPHA: ' if self.is_alpha else '') + self.title
        pageclass = self.page_id[:self.page_id.find('.')] if '.' in self.page_id else ''
        banner = 'beta' if self.is_beta else 'alpha' if self.is_alpha else ''

        ostr = ''.join([
            '<html>\n',  # '<html>\n<!-- This page rendered by the old-style rendering engine. -->\n'
            f'<head><meta charset="UTF-8"><title>{pagetitle}</title>\n',
            f'<link rel="icon" href="{self.art_dir}/favicon.ico" type="image/x-icon" />\n',
            f'<link rel="shortcut icon" href="{self.art_dir}/favicon.ico" type="image/x-icon" />\n',
            f'<link rel="stylesheet" href="{config.CSS_FILE}" type="text/css">\n',
            f'<link rel="stylesheet" href="{config.FONTS_FILE}" type="text/css">\n',
            f'<link rel="stylesheet" href="{config.CSS_DIR}/{pageclass}.css" type="text/css">\n' if pageclass else '',
            f'<link rel="stylesheet" href="{config.CSS_DIR}/{self.page_id}.css" type="text/css">\n',

            self.extra,
            javasc.def_google_analytics_js if not banner else '',
            '</head>\n<body>\n',
            f'<table width="100%"><tr><td height=24 class="{banner}">&nbsp;</td></tr><tr><td>\n' if banner else '',
            self.show_location(),
        ])
        if not self.hide_title:
            if self.title:
                ostr += f'\n<div class="title"><span class="titletext">{self.title}</span></div>'
            ostr += self.fmt_img(self.page_id.split('.'), also={'class': 'centered'})
            if self.description:
                ostr += f'\n<div class="description">{self.description}</div>'
        if self.note:
            ostr += f'\n<div class="note">{self.note}</div>'
        ostr += '\n'
        return ostr

    def format_tail(self):
        ostr = "<p>\n"
        if self.tail.get('effort'):
            ostr += ("Every effort has been made to make this as accurate as possible.  "
                     "If you have corrections, please contact us.<p>\n")
        if self.tail.get('moreinfo'):
            ostr += "Feel free to ask for clarification on these or other models.<p>"
        if self.tail.get('contact'):
            ostr += 'This page is maintained by members of BAMCA.\n'
            ostr += '<a href="../pages/faq.php">See here for information on contacting us.</a><p>\n'
        if self.tail.get('disclaimer'):
            ostr += '''<hr>
BAMCA is a private club and is not affiliated with Tyco Toys, Inc. or Matchbox
Toys (USA) Ltd.  Matchbox&reg; and the Matchbox logo are registered trademarks
of Matchbox International Ltd. and are used with permission.
<hr><p>
'''
        if self.tail.get('flags'):
            ostr += self.format_shown_flags()

        st = self.tail.get('stat')
        if st:  # pragma: no cover
            ostr += f'\n<font size=-1><i>{st}</i></font>\n'
        if self.is_beta:
            ostr += '</td></tr><tr><td height=24 class="beta">&nbsp;</td></tr></table>\n'
        elif self.is_alpha:
            ostr += '</td></tr><tr><td height=24 class="alpha">&nbsp;</td></tr></table>\n'
        ostr += "</body>\n</html>\n"
        return ostr

    def format_shown_flags(self):
        ball = '<span class="blue">&#x25cf;</span> '
        return '<center>\n' + \
            ball.join(['<nobr>{} {}</nobr> '.format(self.format_image_flag(x), self.flag_info[x][0]) for x in
                       sorted(list(self.shown_flags), key=lambda x: self.flag_info[x][0])]) + '</center><p>\n'

    # ---- tables

    def format_table_start(self, also={}, id='', style_id=''):
        also = copy.deepcopy(also)
        self.table_count += 1
        also['class'] = self.style_name(also.get('class'), 'tb', style_id)
        if id:
            also['id'] = id
        return '<table{}>\n'.format(useful.fmt_also(also))

    def format_table_end(self):
        self.table_count -= 1
        return "</table>\n"

    def format_row_start(self, ids=[], also={}):
        ostr = " <tr{}>\n".format(useful.fmt_also(also))
        for id in ids:
            ostr += self.fmt_anchor(id)
        return ostr

    def format_row_end(self):
        return " </tr>\n"

    def format_cell(self, col=None, content="&nbsp;", hdr=False, also={}, large=False, id=''):
        # self.comment('format_cell', col, hdr, also)
        ostr = self.format_cell_start(col, hdr, also, large, id)
        ostr += str(content or '&nbsp;')
        ostr += self.format_cell_end(col, hdr, large)
        return ostr

    def format_cell_start(self, col=None, hdr=False, also={}, large=False, id=''):
        cellstyle = {False: 'eb', True: 'eh'}[hdr]
        celltype = {False: "td", True: "th"}
        also = copy.deepcopy(also)
        also.update({'class': self.style_name(also.get('class'), cellstyle, col, id)})
        self.comment('format_cell_start', col, hdr, also)
        return '  <{}{}>'.format(celltype[hdr], useful.fmt_also(also))

    def format_cell_end(self, col=0, hdr=False, large=False):
        celltype = {False: "td", True: "th"}
        ostr = '  </' + celltype[hdr] + '>\n'
        if large:
            ostr += " </tr>\n"
        return ostr

    # ---- forms

    def format_form_token(self, token, name="token"):
        return f'<input type="hidden" name="{name}" value="{token}">\n'

    # ---- links

    def format_link(self, url, txt=None, args={}, nstyle=None, also={}):
        txt = self.fmt_pseudo(url if txt is None else txt)
        ostr = ''
        if nstyle:
            ostr += '<span' + useful.fmt_also(nstyle) + '>'
        if args:
            url += ('&' if '?' in url else '?') + "&".join([f'{x}={v}' for x, v in args.items()])
        url = url.replace('"', '%22')  # useful.url_quote(url)
        falso = useful.fmt_also(also)
        if not url and not also:
            ostr += txt
        elif not url:
            ostr += f'<a{falso}>{txt}</a>'
        elif not txt:
            ostr += f'<a href="{url}"{falso}>{url}</a>'
        else:
            ostr += f'<a href="{url}"{falso}>{txt}</a>'
        if nstyle:
            ostr += '</span>\n'
        return ostr

    def format_button_link(self, bname, link, image='', args={}, also={}, lalso={}):
        imalso = dict({
            'class': 'textbutton',
            'onsubmit': 'this.disabled=true;',
        })
        imalso.update(also)
        btn = '<div{}>{}</div>'.format(useful.fmt_also(imalso), useful.make_button_label(bname))
        if link:
            btn = self.format_link(link, btn, args=args, also=lalso)
        return btn + '\n'

    def set_button_comment(self, pif, args=None):
        args = f'page={pif.page_id}' + (f'&{args}' if args else '')
        ostr = self.format_button_link("comment on<br>this page", f'../pages/comment.php?{args}',
                                  also={'class': 'textbutton comment'}, lalso=dict())
        if pif.is_allowed('a'):  # pragma: no cover
            ostr += self.format_button_link(
                "pictures", f"traverse.cgi?d={self.pic_dir}", also={'class': 'textbutton comment'}, lalso=dict())
            ostr += self.format_button_link("edit_this_page", pif.dbh.get_editor_link(
                'page_info', {'id': pif.page_id}), also={'class': 'textbutton comment'}, lalso=dict())
        self.comment_button = '<div class="comment_box">' + ostr + '</div>'

    def set_footer(self, new_footer):
        if new_footer:
            if self.footer:
                self.footer += '<br>'
            if isinstance(new_footer, list):
                new_footer = '<br>'.join(new_footer)
            self.footer += new_footer

    # ---- images

    def get_flags(self):
        if not self.flag_info:
            self.flag_info = {x[0]: (x[1], config.FLAG_DIR + '/' + x[0].lower() + '.gif') for x in mbdata.countries}
        return self.flag_info

    def show_flag(self, country):
        flag = self.get_flags().get(country)
        if flag:
            self.shown_flags.add(country)
        return flag

    def find_image_files(self, fnames, suffix=None, pdir=None, art=False):
        if isinstance(fnames, str):
            fnames = [fnames]
        if suffix is None:
            suffix = graphic_types
        elif isinstance(suffix, str):
            suffix = [suffix]
        pdir = useful.relpath(pdir if pdir else self.art_dir if art else self.pic_dir)
        retfiles = list()
        for fname in fnames:
            for sfx in suffix:
                retfiles.extend(glob.glob(useful.relpath('.', pdir, fname + '.' + sfx)))
                # + glob.glob(os.path.join(pdir, fname.lower() + '.' + sfx)))
        return retfiles

    def find_image_file(self, fnames, vars=None, nobase=False, prefix='', suffix=None, largest=None, preferred=None,
                        pdir=None, art=False):
        self.comment('START find_image_file', fnames, 'vars', vars, 'nobase', nobase, 'prefix', prefix,
                     'suffix', suffix, 'largest', largest, 'preferred', prefix, 'pdir', pdir, 'art', art)
        if not fnames:
            self.comment('find_image_file ret', '')
            return ('', '')
        elif isinstance(fnames, str):
            fnames = [fnames]

        suffix = graphic_types if suffix is None else [suffix] if isinstance(suffix, str) else suffix

        if largest:  # overrides previous setting of prefixes.
            prefix = list(reversed(mbdata.image_size_types))
            if largest in prefix:
                prefix = prefix[prefix.index(largest):]
        elif isinstance(prefix, str):
            prefix = [prefix]

        pdir = useful.relpath(pdir if pdir else self.art_dir if art else self.pic_dir)
        pdirvar = useful.relpath(pdir, 'var')

        base = [] if nobase else ['']
        vars = base if not vars else [vars] + base if isinstance(vars, str) else vars + base

        self.comment("find_image_file", 'f:', fnames, 'v:', vars, 'p:', prefix, 's:', suffix, 'd:', pdir)
        fimg = fdir = ''
        for var in vars:
            for fname in fnames:
                fname = useful.clean_name(fname.replace('/', '_'))
                # if not fname:
                #     continue
                if fname.find('.') >= 0:
                    csuffix = [fname[fname.rfind('.') + 1:]]
                    fname = fname[:fname.rfind('.')]
                else:
                    csuffix = suffix

                for pfx in prefix + ['']:
                    rdir, rimg = self.find_prefixed_image(fname, pdir, pdirvar, pfx, csuffix, var)
                    if rimg:
                        if not preferred or preferred == pfx:
                            return rdir, rimg
                        fdir, fimg = rdir, rimg
        self.comment('find_image_file ret', fdir, fimg)
        return fdir, fimg

    def find_prefixed_image(self, fname, pdir, pdirvar, pfx, csuffix, var):
        if pfx and not pfx.endswith('_'):
            pfx += '_'
        for suf in csuffix:
            suf = '.' + suf
            self.comment('find_prefixed_image trying', pdir, pfx + fname + suf)
            if var:
                img = self.fmt_img_file_check(pdirvar, pfx + fname + '-' + var + suf)
                if img:
                    self.comment('find_prefixed_image ret', img)
                    return pdirvar, img
                img = self.fmt_img_file_check(pdirvar, (pfx + fname + '-' + var + suf).lower())
                if img:
                    self.comment('find_prefixed_image ret', img)
                    return pdirvar, img
            else:
                img = self.fmt_img_file_check(pdir, pfx + fname + suf)
                if img:
                    self.comment('find_prefixed_image ret', img)
                    return pdir, img
                img = self.fmt_img_file_check(pdir, (pfx + fname + suf).lower())
                if img:
                    self.comment('find_prefixed_image ret', img)
                    return pdir, img
        return ('', '')

    def find_image_path(self, fnames, vars=None, nobase=False, prefix='', suffix=None, largest=None, preferred=None,
                        pdir=None, art=False):
        if not fnames:
            return ''
        return os.path.join(*self.find_image_file(fnames, vars=vars, nobase=nobase, prefix=prefix, suffix=suffix,
                            largest=largest, preferred=preferred, pdir=pdir, art=art))

    def find_image_list(self, fn, alt='', wc='', prefix='', suffix='jpg', pdir=None):
        self.comment('find_image_list', fn, alt, wc, prefix, suffix, pdir)
        pdir = useful.relpath(pdir if pdir else self.pic_dir)
        if isinstance(suffix, str):
            suffix = [suffix]
        if isinstance(prefix, str):
            prefix = [prefix]
        imgs = list()

        for suf in suffix:
            for pref in prefix:
                orig = (pref + fn + '.' + suf)
                patt = (pref + fn + wc + '.' + suf)

                for fname in useful.read_dir(orig, pdir) + useful.read_dir(patt, pdir):
                    # img = self.fmt_img_src(pdir + '/' + fname, alt)
                    if self.fmt_img_file_check(pdir, fname):
                        imgs.append(fname)
        return imgs

    def format_image_icon(self, fname, desc='', also={}):
        if fname.endswith('-sm'):  # TEMPORARY
            fname = fname[:-3]
        return self.fmt_img(fname, alt=desc, pdir=config.IMG_DIR_ICON, also=also)

    def format_image_art(self, fname, desc='', also={}):
        return self.fmt_art(fname, desc=desc, also=also)

    def format_image_flag(self, code2, name='', also={}):
        return self.fmt_opt_img(code2, alt=name, pdir=config.FLAG_DIR, also=also)

    def format_image_link_image(self, img, link_largest=mbdata.IMG_SIZ_SMALL, image_largest=mbdata.IMG_SIZ_GIGANTIC):
        txt = self.format_image_sized(img, largest=link_largest)
        if txt:
            lnk = self.find_image_path(img, largest=image_largest)
            return self.format_link(os.path.join('..', lnk), txt)
        return ''

    def format_image_as_link(self, fnames, txt, pdir=None, also={}):
        return self.format_link('../' + self.find_image_path(fnames, suffix=graphic_types, pdir=pdir), txt, also=also)

    def format_image_optional(self, fnames, alt='', nobase=False, prefix='', suffix=None, pdir=None, vars=None,
                              also={}, nopad=False, largest=None):
        return self.fmt_img(fnames, alt=alt, vars=vars, nobase=nobase, prefix=prefix, suffix=suffix, pdir=pdir,
                            also=also, pad=not nopad, largest=largest)

    def format_image_required(self, fnames, **kwargs):
        if 'nopad' in kwargs:
            kwargs['pad'] = not kwargs['nopad']
            del kwargs['nopad']
        return self.fmt_img(fnames, required=True, **kwargs)

    def format_image_list(self, fn, alt='', wc='', prefix='', suffix='jpg', pdir=None):
        self.comment('format_image_list', fn, alt, wc, prefix, suffix, pdir)
        pdir = useful.relpath(pdir if pdir else self.pic_dir)
        if isinstance(suffix, str):
            suffix = [suffix]
        if isinstance(prefix, str):
            prefix = [prefix]
        imgs = list()

        for suf in suffix:
            for pref in prefix:
                orig = (pref + fn + '.' + suf)
                patt = (pref + fn + wc + '.' + suf)

                for fname in [orig] + useful.read_dir(patt, pdir):
                    img = self.fmt_img_src(pdir + '/' + fname, alt)
                    if img:
                        imgs.append(img)
        return imgs

    def format_image_sized(self, fnames, vars=None, nobase=False, largest='g', suffix=None, pdir=None,
                           required=False, also={}):
        return self.fmt_img(fnames, alt='', vars=vars, nobase=nobase, suffix=suffix, largest=largest, pdir=pdir,
                            required=required, also=also)

    def format_image_selector(self, pics, select_id):
        if len(pics) < 2:
            return ''
        select_id = select_id.replace('-', '_')
        ostr = '''<script>var sel_%s = new imageselector("%s", %s);</script>\n''' % (select_id, select_id, str(pics))
        for num in range(len(pics)):
            ostr += "<a onclick=\"sel_%s.select(%d);\" id=\"%s_%s\">%s</a>\n" % (
                select_id, num, select_id, num,
                '<i class="fa%s fa-circle green"></i>' % ('r' if num else 's'))
        return ostr

    def format_image_selectable(self, pics, select_id):
        if not pics:
            return self.fmt_no_pic()
        if len(pics) == 1:
            return self.fmt_img_src(pics[0])
        select_id = select_id.replace('-', '_')
        return '\n'.join([self.fmt_img_src(pics[0], also={'id': select_id, 'class': 'shown'})] +
                         [self.fmt_img_src(pics[n], also={'class': 'hidden'})
                          for n in range(1, len(pics))])

    # ---- lower level rendering blocks

    def fmt_pseudo(self, istr):
        if not istr:
            return ''
        while 1:
            mat = pseud_re.search(istr)
            if not mat:
                break
            if mat.group('cmd') == 'img':
                istr = istr[:mat.start()] + self.fmt_opt_img(mat.group('arg')) + istr[mat.end():]
            elif mat.group('cmd') == 'art':
                istr = istr[:mat.start()] + self.fmt_art(
                    mat.group('arg'), also={'align': 'absmiddle'}) + istr[mat.end():]
            elif mat.group('cmd') == 'button':
                istr = istr[:mat.start()] + self.format_button_link(mat.group('arg'), '') + istr[mat.end():]
        return istr

    def fmt_markup(self, cmd, args):
        carg = dict()
        for arg in reversed(args):
            carg.update(arg)
        return '<' + cmd + useful.fmt_also(args) + '>'

    def fmt_art(self, fname, desc='', prefix='', also={}, largest=None):
        return self.fmt_img(fname, alt=desc, prefix=prefix, pdir=self.art_dir, also=also, largest=largest)

    def fmt_img_src(self, pth, alt='', also={}):
        if isinstance(pth, tuple):
            pth = '/'.join(pth)
        if useful.is_good(pth, v=self.verbose):
            return '<img src="../' + pth + '"' + useful.fmt_also({'alt': alt}, also) + '>'
        return ''

    def fmt_img_file_check(self, pdir, fn):
        self.comment("fmt_img_check", pdir, fn)
        return fn if useful.is_good(useful.relpath('.', pdir, fn), v=self.verbose) else ''

    def fmt_img_check(self, pth):
        self.comment("fmt_img_check", pth)
        return pth if useful.is_good(pth, v=self.verbose) else ''

    def fmt_img(self, fnames, alt='', vars=None, nobase=False, prefix='', suffix=None, pdir=None, largest=None,
                preferred=None, also={}, made=True, required=False, blank=False, pad=False, art=False):
        img = self.find_image_path(fnames, vars=vars, nobase=nobase, prefix=prefix, suffix=suffix, largest=largest,
                                   preferred=preferred, pdir=pdir, art=art)
        return self.fmt_img_file(img, alt=alt, prefix=prefix, largest=largest, also=also, made=made, required=required,
                                 blank=blank, unknown=fnames and 'unknown' in fnames, pad=pad)

    def find_alt_image_path(self, img, prefix='', largest=None, made=True, required=False, unknown=False):
        if img:
            return img
        if unknown:
            return self.find_image_path('nomod', prefix=prefix, suffix='gif', pdir=self.art_dir, largest=largest)
        if required:
            return self.find_image_path('nopic' if made else 'notmade', prefix=prefix, suffix='gif', pdir=self.art_dir,
                                        largest=largest)
        return ''

    def fmt_img_file(self, img, alt='', prefix='', largest=None, also={}, made=True, required=False, blank=False,
                     unknown=False, pad=False):
        if img:
            return self.fmt_img_src(img, alt=alt, also=also)
        if unknown:
            return self.fmt_art('nomod.gif', prefix=prefix, largest=largest, also=also)
        if required:
            return self.fmt_no_pic(made, prefix, largest=largest, blank=blank, also=also)
        if alt:
            return alt
        if pad:
            return '&nbsp;'
        return ''

    def fmt_no_pic(self, made=True, prefix='', blank=False, largest=None, also={}):
        img = self.fmt_art('notmade.gif' if not made else 'blank.gif' if blank else 'nopic.gif', prefix=prefix,
                           largest=largest, also=also)
        if img:
            return img
        return self.fmt_art('notmade.gif' if not made else
                            'blank.gif' if blank else 'nopic.gif', largest='s', also=also)

    def fmt_opt_img(self, fnames, alt='', prefix='', suffix=None, pdir=None, also={}, vars=None, nopad=False):
        return self.fmt_img(fnames, alt=alt, prefix=prefix, suffix=suffix, pdir=pdir, also=also, vars=vars,
                            pad=not nopad)

    def fmt_anchor(self, name):
        return f'<i id="{name}"></i>\n' if name else ''

#    def format_bullet_list(self, descs):
#        ostr = ''
#        descs = filter(None, descs)
#        if descs:
#            ostr += "   <ul>" + '\n'
#            for desc in descs:
#                ostr += "    <li>" + desc + '\n'
#            ostr += "   </ul>" + '\n'
#        return ostr

#    def format_box_tail(self, tail):
#        if not tail:
#            return ''
#        ostr = self.format_table_start(style_id="tail")
#        ostr += self.format_row_start()
#        if not isinstance(tail, list):
#            tail = [tail]
#        ntail = 1
#        for tent in tail:
#            ostr += self.format_cell(f"tail_{ntail}", tent)
#            ntail += 1
#        ostr += self.format_row_end()
#        ostr += self.format_table_end()
#        return ostr

    def format_modal(self, modal_id, content):
        ostr = f'<div id="{modal_id}" class="modal">\n'
        ostr += f'<div class="modal-content"><span class="close" id="{modal_id}.close">&times;</span>\n'
        ostr += content + '\n'
        ostr += '</div>\n</div>\n'
        return ostr

    def format_template(self, template, **kwargs):
        if self.tail.get('flags'):
            self.flag_list = list(self.shown_flags)
            self.flag_list.sort(key=lambda x: self.flag_info[x][0])
        titleimage = self.find_image_path(self.page_id.split('.'))
        if titleimage:
            titleimage = '/' + titleimage
        page_info = {
            'messages': useful.header_done(silent=True),
            'hierarchy': self.hierarchy,
            'is_beta': self.is_beta,
            'is_alpha': self.is_alpha,
            'styles': self.styles,
            'title': self.title,
            'hide_title': self.hide_title,
            'is_admin': self.is_admin,
            'is_moderator': self.is_moderator,
            'is_user': self.is_user,
            'titleimage': titleimage,
            'tail': self.tail,
            'page_id': self.page_id,
            'description': self.description,
            'note': self.note,
            'pic_dir': self.pic_dir,
            'large': self.large,
            'verbose': self.verbose,
            'not_released': self.not_released,
            'flags': self.flags,
            'flag_info': self.flag_info,
            'shown_flags': self.shown_flags,
            'secure': self.secure,
            'extra': self.extra,
            'comment_button': self.comment_button,
            'footer': self.footer,
            'bamcamark': self.bamcamark,
            'token': self.format_form_token(useful.generate_token(6)),
        }
        output = useful.render_template(template, page=page_info, config_context=config, **kwargs)
        if self.unittest:
            return "[redacted]"
        return output


class Listix(object):
    # a listix consists of a header (outside of the tables) plus a list of sections, each in its own table.
    #     id, name, note, graphics, tail | section

    def __init__(self, id=None, name='', note='', graphics='', tail=None, section=None):
        self.id = id
        self.name = name
        self.note = note
        self.graphics = None
        self.tail = tail or []
        self.section = section or []

    def dump(self):
        useful.write_comment('Listix', 'id', self.id, 'name', self.name, 'note', self.note,
                             'graphics', self.graphics, 'tail', self.tail)
        for section in self.section:
            section.dump()

    def prep(self):
        return self


class Matrix(object):
    # a matrix consists of a header (outside of the tables) plus a list of sections, each in its own table.
    #    id, name, note, graphics, columns, tail | section

    def __init__(self, id=None, name='', note='', graphics='', columns=4, tail=None, header='', footer='',
                 widthauto=False, section=None):
        self.id = id
        self.name = name
        self.note = note
        self.graphics = graphics
        self.columns = columns
        self.header = header
        self.footer = footer
        self.tail = tail or []
        self.widthauto = widthauto
        self.section = section or []
        if isinstance(columns, list):
            raise ValueError('columns is list')

    def dump(self):
        useful.write_comment('Matrix', 'id', self.id, 'name', self.name, 'note', self.note,
                             'graphics', self.graphics, 'columns', self.columns, 'tail', self.tail,
                             'header', self.header, 'footer', self.footer)
        for section in self.section:
            section.dump()

    def prep(self, flip=False):
        maxes = {'s': 0, 'r': 0, 'e': 0}
        rows = sc = 0
        for sec in self.section:
            sc += 1
            sec.columns = ncols = sec.columns or self.columns
            rc = 0
            for ran in sec.range:
                rc += 1
                icol = ec = 0
                spans = [[0, 0]] * ncols
                if flip:
                    ran.entry = useful.reflect(ran.entry, ncols, {})
                for ent in ran.entry:
                    also = dict()
                    if ent.class_name:
                        also['class'] = ent.class_name
                    if ent.style:
                        also['style'] = ent.style
                    ec += 1

                    if icol == 0:
                        ent.firstent = True
                        rows += 1
                    thisspan = spans[icol]
                    if thisspan[1]:
                        spans[icol] = [thisspan[0], thisspan[1] - 1]
                        icol += thisspan[0]
                        if icol >= ncols:
                            ent.firstent = True
                            icol = 0
                    else:
                        spans[icol] = [0, 0]
                    if ent.rowspan > 1:
                        spans[icol] = [ent.colspan, ent.rowspan - 1]
                        also['rowspan'] = ent.rowspan
                    if ent.colspan > 1:
                        also['colspan'] = ent.colspan
                    icol += ent.colspan
                    if icol >= ncols:
                        icol = 0
                        ent.lastent = True

                    also['width'] = f'{ent.colspan * 100 // ncols}%'
                    if rc == 1:
                        ent.width = also['width']
                    also.update(ent.also)
                    ent.also = also
                    maxes['e'] = max(maxes['e'], ec)
                maxes['r'] = max(maxes['r'], rc)
            maxes['s'] = max(maxes['s'], sc)
        self.rowcount = rows
        self.maxes = maxes
        return self


class Section(object):
    # listix: id, name, note, anchor, columns, headers | range
    # matrix: id, name, note, anchor, columns, switch, count | range
    # section table: 'id', 'page_id', 'display_order', 'category', 'flags', 'name', 'columns', 'start', 'pic_dir',
    # 'disp_format', 'link_format', 'img_format', 'note'

    def __init__(self, id=None, name='', note='', anchor='', count='', columns=4, colist=None, headers=None,
                 switch=None, header='', footer='', noheaders=False, section=None, range=None):
        self.id = id
        self.name = name
        self.note = note
        self.anchor = anchor
        self.columns = columns  # matrix
        self.colist = colist or []  # listix
        self.headers = headers or {}  # listix
        self.switch = switch
        self.count = count
        self.header = header
        self.footer = footer
        self.noheaders = noheaders
        self.range = range or []
        if isinstance(columns, list):
            raise ValueError('columns is list')
        if colist:
            if not headers:
                self.headers = {x: x for x in colist}
            elif isinstance(headers, list):
                self.headers = dict(zip(colist, headers))
        if section:
            self.id = self.id or section.id
            self.name = self.name or section.name
            self.note = self.note or section.note

    def dump(self):
        useful.write_comment(' Section', 'id', self.id, 'name', self.name, 'note', self.note,
                             'anchor', self.anchor, 'columns', self.columns,
                             'colist', self.colist, 'headers', self.headers, 'noheaders', self.noheaders,
                             'switch', self.switch, 'count', self.count, 'header', self.header, 'footer', self.footer)
        for range in self.range:
            range.dump()


class Range(object):
    # listix: id, name, note, anchor, graphics, styles | entry
    # matrix: id, name, note, anchor, graphics | entry

    def __init__(self, id=None, name='', note='', anchor='', graphics='', styles=None, entry=None):
        self.id = id
        self.name = name
        self.note = note
        self.anchor = anchor
        self.graphics = graphics
        self.styles = styles or {}  # listix
        self.entry = entry or []

    def dump(self):
        useful.write_comment('  Range', 'id', self.id, 'name', self.name, 'note', self.note,
                             'anchor', self.anchor, 'graphics', self.graphics, 'styles', self.styles)
        for entry in self.entry:
            if isinstance(entry, Entry):
                entry.dump()
            else:
                useful.write_comment('   ', type(entry), entry)


class Entry(object):
    # listix: <dict> (so, like, not this.)
    # matrix: display_id, text, rowspan, colspan, class_name, style, also,

    def __init__(self, display_id=None, text='', rowspan=1, colspan=1, class_name=None,
                 style=None, also=None, data=None):
        self.display_id = display_id
        self.text = text
        self.rowspan = rowspan
        self.colspan = colspan
        self.class_name = class_name
        self.style = style
        self.also = also or {}
        self.firstent = False
        self.lastent = False
        self.data = data or {}

    def dump(self):
        useful.write_comment('   Entry', 'display_id', self.display_id, 'rowspan', self.rowspan,
                             'colspan', self.colspan, 'class_name', self.class_name,
                             'style', self.style, 'also', self.also, 'firstent', self.firstent,
                             'lastent', self.lastent, 'data', self.data)
        useful.write_comment('   ', self.text)
