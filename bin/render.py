#!/usr/local/bin/python

# TODO: convert much of this to use jinja2 (http://jinja.pocoo.org)

import cgi, copy, glob, httplib, logging, os, re, sys, urllib
import config
import javasc
import mbdata
import secure
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
        self.page_id = page_id
        self.art_dir = config.IMG_DIR_ART
        self.is_beta = False
        self.title = 'BAMCA'
        self.unittest = False
        self.description = ''
        self.note = ''
        self.pic_dir = 'pics'
        self.tail = dict()
        self.large = False
        self.verbose = verbose
        self.dump_file = None
        self.not_released = False
        self.hide_title = False
        self.flags = 0L
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
	#useful.html_done = False
	self.new_cookie = None
	self.footer = ''
	self.bamcamark = 'bamca_sm.gif'
#       if self.verbose:
#           import datetime
#           self.dump_file = open(os.path.join(config.LOG_ROOT, datetime.datetime.now().strftime('%Y%m%d.%H%M%S.log')), 'w')

#    def __str__(self):
#       return str(self.__dict__)

    def __repr__(self):
        return "'<render.Presentation instance>'"

    def __str__(self):
        return "'<render.Presentation instance>'"

    def error_report(self):
        return str(self.__dict__)

    def set_page_info(self, res):
	if res:
	    row = res[0]
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
        ostr += '<br>'
        ostr = ''
        for lvl in self.hierarchy:
            ostr += '<a href="%(link)s">%(name)s</a> &gt;\n' % lvl
        ostr += '<br>'
        return ostr

    def hierarchy_append(self, link, txt):
        self.hierarchy.append({'link': link, 'name': txt})

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
		retfiles.extend(glob.glob(useful.relpath('.', pdir, fname + '.' + sfx))) # + glob.glob(os.path.join(pdir, fname.lower() + '.' + sfx)))
	return retfiles

    def find_image_file(self, fnames, vars=None, nobase=False, prefix='', suffix=None, largest=None, pdir=None, art=False):
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
        for var in vars:
            for fname in fnames:
                fname = useful.clean_name(fname.replace('/', '_'))
#               if not fname:
#                   continue
                if fname.find('.') >= 0:
                    csuffix = [fname[fname.rfind('.') + 1:]]
                    fname = fname[:fname.rfind('.')]
                else:
                    csuffix = suffix

                for pfx in prefix + ['']:
                    if pfx and not pfx.endswith('_'):
                        pfx += '_'
                    for suf in csuffix:
                        suf = '.' + suf
                        if var:
                            img = self.fmt_img_file_check(pdirvar, pfx + fname + '-' + var + suf)
                            if img:
                                self.comment('find_image_file ret', img)
                                return pdirvar, img
                            img = self.fmt_img_file_check(pdirvar, (pfx + fname + '-' + var + suf).lower())
                            if img:
                                self.comment('find_image_file ret', img)
                                return pdirvar, img
                        else:
                            img = self.fmt_img_file_check(pdir, pfx + fname + suf)
                            if img:
                                self.comment('find_image_file ret', img)
                                return pdir, img
                            img = self.fmt_img_file_check(pdir, (pfx + fname + suf).lower())
                            if img:
                                self.comment('find_image_file ret', img)
                                return pdir, img
        self.comment('find_image_file ret', '')
        return ('', '')

    def find_image_path(self, fnames, vars=None, nobase=False, prefix='', suffix=None, largest=None, pdir=None, art=False):
	if not fnames:
	    return ''
	return os.path.join(*self.find_image_file(fnames, vars=vars, nobase=nobase, prefix=prefix, suffix=suffix, largest=largest, pdir=pdir, art=art))

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

                for fname in [orig] + useful.read_dir(patt, pdir):
                    img = self.fmt_img_src(pdir + '/' + fname, alt)
		    if self.fmt_img_file_check(pdir, fname):
                        imgs.append(fname)
        return imgs

    def find_button_name(self, name):
	return name.replace('<br>', '_').replace(' ', '_').lower()

    def find_button_label(self, name):
	return name.replace('_', ' ').upper()

    # immediate effect functions.

    def debug(self, *args):
	if self.verbose:
	    print ' '.join([str(x) for x in args])

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
            print useful.dump_dict_comment(name, arg)

    def print_html(self, content='text/html', status=200):
	if not useful.is_header_done():
	    print 'Content-Type:', content
	    print 'Status:', status, httplib.responses.get(status, '')
	    #useful.html_done = True
	    self.print_cookie()
	    print
	    if content == 'text/html':
		print '<!DOCTYPE html>'
		print
	    useful.header_done()

    def set_cookie(self, cookie):
	self.new_cookie = cookie

    def print_cookie(self):  # pragma: no cover
        if self.new_cookie:
            print self.new_cookie.output()
            os.environ['HTTP_COOKIE'] = self.new_cookie.output()
        else:
	    incookie = self.secure.cookies if self.secure.cookies else self.secure.get_cookies()
            if not incookie:
                pass
            elif 'id' not in incookie:
                pass
            elif '/' not in incookie['id'].value:
                incookie['id']['expires'] = -1
                print incookie.output()
		if 'HTTP_COOKIE' in os.environ:
		    del os.environ['HTTP_COOKIE']
            elif incookie['id'].value.split('/')[1] != os.environ['REMOTE_ADDR']:
                incookie['id']['expires'] = -1
                print incookie.output()
		if 'HTTP_COOKIE' in os.environ:
		    del os.environ['HTTP_COOKIE']

    #---- upper level rendering blocks

    def format_head(self):
        pagetitle = self.title
        if self.is_beta:
            pagetitle = 'BETA: ' + pagetitle

        ostr  = '<html>\n<!-- This page rendered by the old-style rendering engine. -->\n'
        ostr += '<head><meta charset="UTF-8"><title>%s</title>\n' % pagetitle
        ostr += '<link rel="icon" href="' + self.art_dir + '/favicon.ico" type="image/x-icon" />\n'
        ostr += '<link rel="shortcut icon" href="' + self.art_dir + '/favicon.ico" type="image/x-icon" />\n'
        ostr += '<link rel="stylesheet" href="%s" type="text/css">\n' % config.CSS_FILE
        ostr += '<link rel="stylesheet" href="%s" type="text/css">\n' % config.FONTS_FILE
        if '.' in self.page_id:
            ostr += '<link rel="stylesheet" href="%s/%s.css" type="text/css">\n' % (config.CSS_DIR, self.page_id[:self.page_id.find('.')])
        ostr += '<link rel="stylesheet" href="%s/%s.css" type="text/css">\n' % (config.CSS_DIR, self.page_id)

	ostr += self.extra
        if not self.is_beta:
            ostr += javasc.def_google_analytics_js
        ostr += '</head>\n<body>\n'
        if self.is_beta:
            ostr += '<table width="100%"><tr><td height=24 class="beta">&nbsp;</td></tr><tr><td>\n'
        ostr += self.show_location()
        if not self.hide_title:
            if self.title:
                ostr += '\n<div class="title"><span class="titletext">' + self.title + '</span></div>'
            ostr += self.fmt_img(self.page_id.split('.'), also={'class': 'centered'})
            if self.description:
                ostr += '\n<div class="description">' + self.description + '</div>'
        if self.note:
            ostr += '\n<div class="note">' + self.note + '</div>'
        ostr += '\n'
        return ostr

    def format_tail(self):
        ostr = "<p>\n"
        if self.tail.get('effort'):
            ostr += "Every effort has been made to make this as accurate as possible.  If you have corrections, please contact us.<p>\n"
        if self.tail.get('moreinfo'):
            ostr += "Feel free to ask for clarification on these or other models.<p>"
        if self.tail.get('contact'):
            ostr += 'This page is maintained by members of BAMCA.\n'
            ostr += '<a href="../pages/faq.php">See here for information on contacting us.</a><p>\n'
        if self.tail.get('disclaimer'):
            ostr += '''<hr>
BAMCA is a private club and is not affiliated with Tyco Toys, Inc. or Matchbox
Toys (USA) Ltd.  Matchbox and the Matchbox logo are registered trademarks
of Matchbox International Ltd. and are used with permission.
<hr><p>
'''
        if self.tail.get('flags'):
	    ostr += self.format_shown_flags()

        st = self.tail.get('stat')
        if st:  # pragma: no cover
            ostr += '\n<font size=-1><i>%s</i></font>\n' % st
        if self.is_beta:
            ostr += '</td></tr><tr><td height=24 class="beta">&nbsp;</td></tr></table>\n'
        ostr += "</body>\n</html>\n"
        return ostr

    def format_shown_flags(self):
	ball = '<span class="blue">&#x26ab;</span> '
	return '<center>\n' + \
	    ball.join(['<nobr>%s %s</nobr> ' % (self.format_image_flag(x), self.flag_info[x][0]) for x in
		sorted(list(self.shown_flags), key=lambda x: self.flag_info[x][0])]) + '</center><p>\n'

    #---- tables

    def format_table_start(self, also={}, id='', style_id=''):
        also = copy.deepcopy(also)
        self.table_count += 1
        also['class'] = self.style_name(also.get('class'), 'tb', style_id)
        if id:
            also['id'] = id
        return '<table%s>\n' % useful.fmt_also(also)

    def format_table_end(self):
        self.table_count -= 1
        return "</table>\n"

    def format_row_start(self, ids=[], also={}):
        ostr = " <tr%s>\n" % useful.fmt_also(also)
        for id in ids:
            ostr += self.fmt_anchor(id)
        return ostr

    def format_row_end(self):
        return " </tr>\n"

    def format_cell(self, col=None, content="&nbsp;", hdr=False, also={}, large=False, id=''):
        #self.comment('format_cell', col, hdr, also)
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
        return '  <%s%s>' % (celltype[hdr], useful.fmt_also(also))

    def format_cell_end(self, col=0, hdr=False, large=False):
        celltype = {False: "td", True: "th"}
        ostr = '  </' + celltype[hdr] + '>\n'
        if large:
            ostr += " </tr>\n"
        return ostr

    #format_table({'also': {}, 'id': '', 'style_id': '', 'rows': []})
    #rows=[{'ids': [], 'also': {}, 'cells': []}, ...]
    #cells=[{'col': None, 'content': "&nbsp;", 'hdr': False, 'also': {}, 'large': False, 'id': ''}, ...]

    def format_table(self, table):
        ostr = ''
        ostr += self.format_table_start(also=table.get('also', {}), id=table.get('ids', []), style_id=table.get('style_id', ''))
        ostr += self.format_rows(table.get('rows', []))
        ostr += self.format_table_end()
        return ostr

    def format_rows(self, rows):
        ostr = ''
        for row in rows:
            ostr += self.format_row_start(ids=row.get('ids', []), also=row.get('also', {}))
            ostr += self.format_cells(row.get('cells', []))
            ostr += self.format_row_end()
        return ostr

    def format_cells(self, cells):
        return ''.join([self.format_cell(**cell) for cell in cells])

    #----

    def format_section(self, content, fn=None, also=None, cols=0, id=''):
	fn = fn or list()
	also = also or dict()
        nalso = copy.deepcopy(also)
        nalso['class'] = self.style_name(also.get('class'), 'sh', id)
        if cols:
            nalso['colspan'] = cols
        ostr = ''
        if fn:
            strimg = self.fmt_opt_img(fn)
            if len(strimg) > 6:
                ostr += strimg + '<br>'
	ostr = self.format_row_start()
        ostr += '  <th%s>%s</th>\n' % (useful.fmt_also(nalso), self.fmt_pseudo(content))
	ostr += self.format_row_end()
        return ostr

    def format_section_freestanding(self, content, fn=[], also={}, cols=0, id=''):
        nalso = copy.deepcopy(also)
        nalso['class'] = self.style_name(also.get('class'), 'sh', id)
        ostr = strimg = ''
        if fn:
            strimg = self.fmt_opt_img(fn)
            if len(strimg) > 6:
                strimg += '<br>'
            else:
                strimg = ''
        ostr += '  <div%s>%s%s</div>\n' % (useful.fmt_also(nalso), strimg, self.fmt_pseudo(content))
        return ostr

    def format_range(self, content, col, fn=[], also={}, large=False, nstyle=None, cols=3, id=''):
        nalso = copy.deepcopy(also)
        nalso['class'] = self.style_name(also.get('class'), 'rh', col, id)
        ostr = self.format_row_start() + '  <th' + useful.fmt_also(nalso) + '>'
        self.comment(large, cols)
        if large:
            ostr += self.fmt_opt_img(fn) + content + '</th>\n'
        elif cols == 1:
            ostr += self.fmt_opt_img(fn) + '\n'
            ostr += '%s</th>\n' % content
        elif cols == 2:
            ostr += self.fmt_opt_img(fn) + '</th>\n'
            ostr += '  <th' + useful.fmt_also({'colspan': cols - 2}, nalso) + '>%s</th>\n' % content
        else:
            ostr += self.fmt_opt_img(fn) + '</th>\n'
            ostr += '  <th' + useful.fmt_also({'colspan': cols - 2}, nalso) + '>%s</th>\n' % content
            ostr += '  <th' + useful.fmt_also(nalso) + '>&nbsp;</th>\n'
        ostr += self.format_row_end()
        #self.comment('nalso', nalso)
        return ostr

    def format_link(self, url, txt=None, args={}, nstyle=None, also={}):
        txt = self.fmt_pseudo(url if txt is None else txt)
        ostr = ''
        if nstyle:
            ostr += '<span' + useful.fmt_also(nstyle) + '>'
        if args:
            args = "&".join([x + '=' + args[x] for x in args])
            if '?' in url:
                url += '&' + args
            else:
                url += '?' + args
	#url = urllib.quote(url)
	url = url.replace('"', '%22')
        if not url and not also:
            ostr += txt
        elif not url:
            ostr += '<a%s>%s</a>' % (useful.fmt_also(also), txt)
        elif not txt:
            ostr += '<a href="%s"%s>%s</a>' % (url, useful.fmt_also(also), url)
        else:
            ostr += '<a href="%s"%s>%s</a>' % (url, useful.fmt_also(also), txt)
        if nstyle:
            ostr += '</span>\n'
        return ostr

    #---- forms

    def format_form_token(self, token, name="token"):
	return '<input type="hidden" name="%s" value="%s">\n' % (name, token)

    def format_checkbox(self, name, options, checked=[], sep='\n'):
        #self.comment('format_checkbox', name, options, checked)
        return ''.join([
            '<nobr><input type="checkbox" name="%s" value="%s"%s> %s</nobr>%s' % (name, option[0],
		' CHECKED' if option[0] in checked else '', option[1], sep)
	    for option in options])

    def format_radio(self, name, options, checked='', sep='\n'):
        return ['<input type="radio" name="%s" value="%s"%s> %s%s' %
		(name, option[0], ' CHECKED' if option[0] == checked else '', option[1], sep)
	    if option else sep for option in options]

    def format_select_country(self, name, selected='', id=None):
        return self.format_select(name, [('', '')] + mbdata.countries, selected='', id=None)

    def format_select(self, name, options, selected='', id=None):
        ostr = '<select name="%s"' % name
        if id:
            ostr += ' id="%s"' % id
	ostr += '>\n'
        for option in options:
            if isinstance(option, str):
                option = (option, option)
            ostr += '<option value="%s"%s>%s\n' % (option[0], ' SELECTED' if option[0] == selected else '', option[1])
        ostr += '</select>'
        return ostr

    def format_text_input(self, name, maxlength, showlength=24, value='', id=None, also={}):
        if not value:
            value = ''
        return '<input name="%s" type="text" size="%d" maxlength="%d" value="%s"%s%s>\n' % (name, min(showlength, maxlength), maxlength, cgi.escape(str(value), True), useful.fmt_also(also), (' id="%s"' % id) if id else '')

    def format_textarea_input(self, name, showlength=128, showheight=4, value=''):
        if not value:
            value = ''
        return '<textarea name="%s" cols="%d" rows="%d">%s</textarea>\n' % (name, showlength, showheight, cgi.escape(str(value), True))

    def format_password_input(self, name, maxlength=80, showlength=24, value=''):
        return '<input name="%s" type="text" size="%d" maxlength="%d" value="%s">\n' % (name, min(showlength, maxlength), maxlength, value)

    def format_hidden_input(self, values):
	return ''.join(['<input type="hidden" name="%s" value="%s">\n' % (k, v) for k, v in values.items()])

    #---- buttons

    def format_button_up_down(self, field):
        but_inc = '''<div class="textbutton textupdown"><i class="fa fa-angle-up bold" title="UP"></i></div>'''
        but_dec = '''<div class="textbutton textupdown"><i class="fa fa-angle-down bold" title="DOWN"></i></div>'''
        ostr = ''
        ostr += '''<a onclick="incrfield(%s, 1);">%s</a>''' % (field, but_inc)
        ostr += '''<a onclick="incrfield(%s,-1);">%s</a>''' % (field, but_dec)
        return ostr

    def format_button_up_down_select(self, id, vl=1):
        ostr = ''
        but_max = '''<div class="textbutton textupdown"><i class="fa fa-angle-double-up bold" title="TOP"></i></div>'''
        but_inc = '''<div class="textbutton textupdown"><i class="fa fa-angle-up bold" title="UP"></i></div>'''
        but_dec = '''<div class="textbutton textupdown"><i class="fa fa-angle-down bold" title="DOWN"></i></div>'''
        but_min = '''<div class="textbutton textupdown"><i class="fa fa-angle-double-down bold" title="BOTTOM"></i></div>'''
        if vl > 0:
            ostr += "<a onclick=\"settsel('%s');\">%s</a>\n" % (id, but_max)
            ostr += "<a onmousedown=\"toggleOnSel('%s', 1);\" onmouseup=\"toggleOff();\">%s</a>\n" % (id, but_inc)
            ostr += "<a onmousedown=\"toggleOnSel('%s',-1);\" onmouseup=\"toggleOff();\">%s</a>\n" % (id, but_dec)
            ostr += "<a onclick=\"setbsel('%s');\">%s</a>\n" % (id, but_min)
        else:
            ostr += "<a onclick=\"setbsel('%s');\">%s</a>\n" % (id, but_max)
            ostr += "<a onmousedown=\"toggleOnSel('%s',-1);\" onmouseup=\"toggleOff();\">%s</a>\n" % (id, but_inc)
            ostr += "<a onmousedown=\"toggleOnSel('%s', 1);\" onmouseup=\"toggleOff();\">%s</a>\n" % (id, but_dec)
            ostr += "<a onclick=\"settsel('%s');\">%s</a>\n" % (id, but_min)
        return ostr

    def format_button_input_visibility(self, id, collapsed=False):
	fname = 'expand' if collapsed else 'collapse'
        bname = self.find_button_label(fname)
        also = {'id': id + '_l',
                'name': bname,
                'value': bname,
                'onclick': "toggle_visibility('%s','%s_l'); return false;" % (id, id),
                'class': 'textbutton',
	}
        return '<button type="submit"%s>%s</button>\n' % (useful.fmt_also(also), bname)

    def format_button_input(self, bname="submit", name=None, also=None):
        bname = self.find_button_label(bname)
	name = name if name else bname
        value = self.find_button_label(bname)
        altname = self.find_button_label(bname)
	also = also if also else {}
        imalso = {'class': 'textbutton', 'alt': altname}
	#also['onsubmit'] = 'this.disabled=true;'
        inputname = self.find_button_name(name)
	#also['onclick'] = 'this.disabled=true; var e=document.createElement("input"); e.type="text"; e.name="%s"; e.value="1"; this.form.appendChild(e); this.form.submit();' % inputname
	#return '<input type="submit" name="%s" value="%s"%s>\n' % (inputname, value, useful.fmt_also(imalso, also))
	return '<button type="submit" name="%s" value="%s"%s>%s</button>\n' % (inputname, altname, useful.fmt_also(imalso, also), altname)


    def format_text_button(self, name, also={}):
        bname = self.find_button_label(name)
        imalso = dict({'class': 'textbutton'})
	imalso['onsubmit'] = 'this.disabled=true;'
	imalso.update(also)
	btn = '<div%s>%s</div>' % (useful.fmt_also(imalso), bname)
	return btn

    def format_button(self, bname, link='', image='', args={}, also={}, lalso={}):
        btn = self.format_text_button(bname, also=also)
        if link:
            btn = self.format_link(link, btn, args=args, also=lalso)
        return btn + '\n'

    def format_button_input_paste(self, id):
	return self.format_text_button('paste', also={
	    'onclick': "paste_from_clippy('%s'); return false;" % id,
	})

    def format_button_reset(self, name):
	return self.format_text_button('reset', also={'onClick': 'ResetForm(document.%s);' % name})

    def set_button_comment(self, pif, args=None):
        if args:
            args = 'page=%s&%s' % (pif.page_id, unicode(args, errors='ignore'))
        else:
            args = 'page=%s' % pif.page_id
        ostr = self.format_button("comment on<br>this page", link='../pages/comment.php?%s' % args, also={'class': 'textbutton comment'}, lalso=dict())
        if pif.is_allowed('a'):  # pragma: no cover
            ostr += self.format_button("pictures", link="traverse.cgi?d=%s" % self.pic_dir, also={'class': 'textbutton comment'}, lalso=dict())
            ostr += self.format_button("edit_this_page", link=pif.dbh.get_editor_link('page_info', {'id': pif.page_id}), also={'class': 'textbutton comment'}, lalso=dict())
	self.comment_button = '<div class="comment_box">' + ostr + '</div>'

    def set_footer(self, new_footer):
	if new_footer:
	    if self.footer:
		self.footer += '<br>'
	    if isinstance(new_footer, list):
		new_footer = '<br>'.join(new_footer)
	    self.footer += new_footer

    #---- images

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

    def format_image_optional(self, fnames, alt='', prefix='', suffix=None, pdir=None, also={}, vars=None, nopad=False, largest=None):
        return self.fmt_img(fnames, alt=alt, prefix=prefix, suffix=suffix, pdir=pdir, also=also, vars=vars, pad=not nopad, largest=largest)

    def format_image_required(self, fnames, alt='', vars=None, nobase=False, prefix='', suffix=None, pdir=None, also={}, made=True, largest=None):
        return self.fmt_img(fnames, alt=alt, vars=vars, nobase=nobase, prefix=prefix, suffix=suffix, pdir=pdir, also=also, made=made, required=True, largest=largest)

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

    def format_image_sized(self, fnames, vars=None, nobase=False, largest='g', suffix=None, pdir=None, required=False, also={}):
        return self.fmt_img(fnames, alt='', vars=vars, nobase=nobase, suffix=suffix, largest=largest, pdir=pdir, required=required, also=also)

    def format_image_selector(self, pics, select_id):
	if len(pics) < 2:
	    return ''
	select_id = select_id.replace('-', '_')
	ostr = '''<script>var sel_%s = new imageselector("%s", %s);</script>\n''' % (select_id, select_id, str(pics))
	for num in range(len(pics)):
	    ostr += "<a onclick=\"sel_%s.select(%d);\" id=\"%s_%s\">%s</a>\n" % (select_id, num, select_id, num,
		'<i class="fa fa-circle%s green"></i>' % ('-o' if num else '')
	    )
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

    #---- lower level rendering blocks

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
                istr = istr[:mat.start()] + self.fmt_art(mat.group('arg'), also={'align': 'absmiddle'}) + istr[mat.end():]
            elif mat.group('cmd') == 'button':
                istr = istr[:mat.start()] + self.format_button(mat.group('arg')) + istr[mat.end():]
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

    def fmt_img(self, fnames, alt='', vars=None, nobase=False, prefix='', suffix=None, pdir=None, largest=None, also={}, made=True, required=False, pad=False, art=False):
        img = self.find_image_path(fnames, vars=vars, nobase=nobase, prefix=prefix, suffix=suffix, largest=largest, pdir=pdir, art=art)
	return self.fmt_img_file(img, alt=alt, prefix=prefix, largest=largest, also=also, made=made, required=required, unknown=fnames and 'unknown' in fnames, pad=pad)

    def find_alt_image_path(self, img, prefix='', largest=None, made=True, required=False, unknown=False):
        if img:
            return img
	if unknown:
	    return self.find_image_path('nomod', prefix=prefix, suffix='gif', pdir=self.art_dir, largest=largest)
        if required:
	    return self.find_image_path('nopic' if made else 'notmade', prefix=prefix, suffix='gif', pdir=self.art_dir, largest=largest)
        return ''

    def fmt_img_file(self, img, alt='', prefix='', largest=None, also={}, made=True, required=False, unknown=False, pad=False):
        if img:
            return self.fmt_img_src(img, alt=alt, also=also)
	if unknown:
	    return self.fmt_art('nomod.gif', prefix=prefix, largest=largest, also=also)
        if required:
            return self.fmt_no_pic(made, prefix, largest=largest, also=also)
	if alt:
	    return alt
        if pad:
            return '&nbsp;'
        return ''

    def fmt_no_pic(self, made=True, prefix='', largest=None, also={}):
        img = self.fmt_art('nopic.gif' if made else 'notmade.gif', prefix=prefix, largest=largest, also=also)
	if not img:
	    img = self.fmt_art('nopic.gif' if made else 'notmade.gif', largest='s', also=also)
	return img

    def fmt_opt_img(self, fnames, alt='', prefix='', suffix=None, pdir=None, also={}, vars=None, nopad=False):
        return self.fmt_img(fnames, alt=alt, prefix=prefix, suffix=suffix, pdir=pdir, also=also, vars=vars, pad=not nopad)

    def fmt_anchor(self, name):
	return ('<i id="%s"></i>\n' % name) if name else ''

    def format_bullet_list(self, descs):
        ostr = ''
        descs = filter(None, descs)
        if descs:
            ostr += "   <ul>" + '\n'
            for desc in descs:
                ostr += "    <li>" + desc + '\n'
            ostr += "   </ul>" + '\n'
        return ostr

    # a listix consists of a header (outside of the tables) plus a list of sections, each in its own table.
    #     id, name, note, graphics, tail | section
    # a section consists of a header (inside the table) plus a list of entries.
    #     id, name, note, anchor, columns, headers | range
    # a range consists of a header plus a list of entries.
    #     id, name, note, anchor, graphics, styles | entry
    # an entry contains a dict of cells, keys in columns.
    #     <text>

    def format_listix(self, llineup):
        ostr = ''
        #self.comment_dict('lineup', llineup)
        if llineup.get('graphics'):
            for graf in llineup['graphics']:
                ostr += self.fmt_opt_img(graf, suffix='gif')
        lin_id = llineup.get('id', '')
        if llineup.get('note'):
            ostr += llineup['note'] + '<br>'
        for sec in llineup.get('section', []):
            sec_id = sec.get('id', '')
	    ncols = len(sec['columns'])
            ostr += self.fmt_anchor(sec.get('anchor'))
            if sec.get('header'):
                ostr += sec['header']
            ostr += self.format_table_start(style_id=lin_id)
            if sec.get('name'):
                ostr += self.format_section(sec.get('name', ''), id=sec['id'], cols=len(sec['columns']))
            if sec.get('note'):
                ostr += self.format_row_start()
                also = {'colspan': ncols}
                also['class'] = self.style_name(also.get('class'), 'sb', sec_id)
                ostr += self.format_cell(0, sec['note'], also=also)
                ostr += self.format_row_end()

	    if not sec.get('noheaders'):
		ostr += self.format_row_start(also={'class': 'er'})
		for ent in sec['columns']:
		    ostr += self.format_cell(0, sec['headers'].get(ent, ''), hdr=True)
		ostr += self.format_row_end()

	    for ran in sec['range']:
		ran_id = ran.get('id', '')
		ostr += self.fmt_anchor(ran.get('anchor'))
		if ran.get('name'):
		    ostr += self.format_cell(0, ran.get('name', ''), hdr=True, id=ran['id'], also={'colspan': ncols})
		if ran.get('note'):
		    ostr += self.format_row_start()
		    also = {'colspan': ncols}
		    also['class'] = self.style_name(also.get('class'), 'sb', ran_id)
		    ostr += self.format_cell(0, ran['note'], also=also)
		    ostr += self.format_row_end()

		for ent in ran['entry']:
		    ostr += self.format_row_start(also={'class': 'er'})
		    for col in sec['columns']:
			ostr += self.format_cell(ran.get('styles', {}).get(col, '1'), ent.get(col, ''))
		    ostr += self.format_row_end()

            ostr += self.format_table_end()
            if sec.get('footer'):
                ostr += sec['footer']
        ostr += self.format_box_tail(llineup.get('tail'))
        return ostr

    # a matrix consists of a header (outside of the tables) plus a list of sections, each in its own table.
    #     id, name, note, graphics, columns, tail | section
    # a section consists of a header (inside the table) plus a list of ranges.
    #     id, name, note, anchor, columns, switch, count | range
    # a range consists of a header plus a list of entries.
    #     id, name, note, anchor, graphics | entry
    # an entry contains the contents of a cell plus cell controls
    #     display_id, text, rowspan, colspan, class, st_suff, style, also,

    def format_matrix(self, llineup):
        ostr = ''
        maxes = {'s': 0, 'r': 0, 'e': 0}
        #self.comment_dict('lineup', llineup)
        if llineup.get('graphics'):
            for graf in llineup['graphics']:
                ostr += self.fmt_opt_img(graf, suffix='gif')
        lin_id = llineup.get('id', '')
        if llineup.get('note'):
            ostr += llineup['note'] + '<br>'
        sc = 0
        for sec in llineup.get('section', []):
            sc += 1
            sec_id = sec.get('id', '')
            ostr += self.fmt_anchor(sec.get('anchor'))
            ncols = sec.get('columns', llineup.get('columns', 4))
            if 'switch' in sec:
                #exval = {False: 'expand', True: 'collapse'}[sec['switch']]
                #ostr += '''<input id="%s_l" type="button" value="%s" onclick="toggle_visibility('%s','%s_l');">\n''' % (sec_id, exval, sec_id, sec_id)
                ostr += self.format_button_input_visibility(sec_id, sec['switch'])
                ostr += sec.get('count', '')
            ostr += self.format_table_start(style_id=lin_id)
            if sec.get('name'):
                ostr += self.format_section(sec.get('name', ''), cols=ncols, id=sec['id'])
            if sec.get('note'):
                ostr += self.format_row_start()
                also = {'colspan': ncols}
                also['class'] = self.style_name(also.get('class'), 'sb', sec_id)
                ostr += self.format_cell(0, sec['note'], also=also)
                ostr += self.format_row_end()
#            ostr += self.format_row_start()
#            ostr += '<td>\n'
            #ostr += self.format_table_start(id=sec_id, style_id=lin_id, also={'style': "border-width: 0; padding: 0;"})
            rc = 0
            for ran in sec.get('range', []):
                rc += 1
                ran_id = ran.get('id', '')
                ostr += self.fmt_anchor(ran.get('anchor'))
                if ran.get('name') or ran.get('graphics'):
                    ostr += self.format_range(ran.get('name', ''), None, ran.get('graphics', list()), cols=sec['columns'], id=ran.get('id', ''))
                if ran.get('note'):
                    ostr += self.format_row_start()
                    also = {'colspan': ncols}
                    also['class'] = self.style_name(also.get('class'), 'rb', ran_id)
                    ostr += self.format_cell(0, ran['note'], also=also)
                    ostr += self.format_row_end()
                icol = 0
                spans = [[0, 0]] * ncols
                ec = 0
                for ent in ran.get('entry', []):
                    ec += 1
                    if icol == 0:
                        ostr += self.format_row_start(also={'class': 'er'})
                    disp_id = ent.get('display_id')
                    if not disp_id:
                        disp_id = ran_id
                    #disp_id += ent.get('st_suff', '')
                    also = {}
                    if ent.get('class'):
                        also['class'] = ent['class']
                    if ent.get('style'):
                        also['style'] = ent['style']
                    thisspan = spans[icol]
                    if thisspan[1]:
                        spans[icol] = [thisspan[0], thisspan[1] - 1]
                        icol += thisspan[0]
                        if icol >= ncols:
                            ostr += self.format_row_end()
                            icol = 0
                            ostr += self.format_row_start(also={'class': 'er'})
		    also['width'] = '%d%%' % (100/ncols)
                    if ent.get('rowspan', 1) > 1:
                        spans[icol] = [ent.get('colspan', 1), ent['rowspan'] - 1]
                        also['rowspan'] = ent['rowspan']
                    if ent.get('colspan', 1) > 1:
                        also['colspan'] = ent['colspan']
                        also['width'] = '%d%%' % (int(ent['colspan']) * 100 / ncols)
		    also.update(ent.get('also', {}))
                    ostr += self.format_cell(disp_id, ent['text'], also=also)
                    icol += ent.get('colspan', 1)
                    if icol >= ncols:
                        ostr += self.format_row_end()
                        icol = 0
                    maxes['e'] = max(maxes['e'], ec)
                if icol:
                    ostr += self.format_row_end()
                maxes['r'] = max(maxes['r'], rc)
            #ostr += self.format_table_end()
#            ostr += self.format_cell_end()
#            ostr += self.format_row_end()
            ostr += self.format_table_end()
            maxes['s'] = max(maxes['s'], sc)
        #print 'sec %(s)d ran %(r)d ent %(e)d<br>' % maxes
	if any(llineup.get('tail', [])):
	    ostr += self.format_box_tail(llineup.get('tail'))
        return ostr

    def format_matrix_for_template(self, llineup, flip=False):
	maxes = {'s': 0, 'r': 0, 'e': 0}
	#self.comment_dict('lineup', llineup)
	rows = sc = 0
	llineup.setdefault('widthauto', False)
	for sec in llineup.get('section', []):
	    sc += 1
	    sec['columns'] = ncols = sec.get('columns', llineup.get('columns', 4))
	    rc = 0
	    for ran in sec.get('range', []):
		rc += 1
		icol = ec = 0
		spans = [[0, 0]] * ncols
		entries = list()
		if flip:
		    ran['entry'] = useful.reflect(ran.get('entry', []), ncols, {})
		for ent in ran.get('entry', []):
		    ec += 1
		    if icol == 0:
			ent['firstent'] = True
			rows += 1
		    also = {}
		    ent.setdefault('rowspan', 1)
		    ent.setdefault('colspan', 1)
		    if ent.get('class'):
			also['class'] = ent['class']
		    if ent.get('style'):
			also['style'] = ent['style']
		    thisspan = spans[icol]
		    if thisspan[1]:
			spans[icol] = [thisspan[0], thisspan[1] - 1]
			icol += thisspan[0]
			if icol >= ncols:
			    ent['firstent'] = True
			    icol = 0
		    ent['width'] = also['width'] = '%d%%' % (100/ncols)
		    if ent.get('rowspan', 1) > 1:
			spans[icol] = [ent.get('colspan', 1), ent['rowspan'] - 1]
			also['rowspan'] = ent['rowspan']
		    if ent.get('colspan', 1) > 1:
			also['colspan'] = ent['colspan']
			also['width'] = '%d%%' % (int(ent['colspan']) * 100 / ncols)
		    icol += int(ent['colspan'])
		    also.update(ent.get('also', {}))
		    if icol >= ncols:
			icol = 0
			ent['lastent'] = True
                    maxes['e'] = max(maxes['e'], ec)
		    ent['also'] = also
		    entries.append(ent)
		ran['entry'] = entries
                maxes['r'] = max(maxes['r'], rc)
            maxes['s'] = max(maxes['s'], sc)
	llineup['rowcount'] = rows
	llineup['maxes'] = maxes
        #print 'sec %(s)d ran %(r)d ent %(e)d<br>' % maxes
	return llineup

    def format_box_tail(self, tail):
        if not tail:
            return ''
        ostr = self.format_table_start(style_id="tail")
        ostr += self.format_row_start()
        if not isinstance(tail, list):
            tail = [tail]
        ntail = 1
        for tent in tail:
            ostr += self.format_cell("tail_%s" % ntail, tent)
            ntail += 1
        ostr += self.format_row_end()
        ostr += self.format_table_end()
        return ostr

    def format_links(self, llineup):
        ostr = llineup.get('name', '') + '\n'
        lin_id = llineup.get('id', '')
        for sec in llineup.get('section', []):
            sec_id = sec.get('id', '')
            self.fmt_anchor(sec.get('anchor'))
            if sec.get('name'):
                ostr += '<h3>' + sec.get('name', '') + '</h3><p>'
            if sec.get('note'):
                ostr += sec['note'] + '<br>'
            for ran in sec.get('range', []):
                ran_id = ran.get('id', '')
                self.fmt_anchor(ran.get('anchor'))
                if ran.get('name') or ran.get('graphics'):
                    ostr += ran.get('name', '') + '<br>'
                if ran.get('note'):
                    ostr += ran['note'] + '<br>'
                for ent in ran.get('entry', []):
                    if ent['indent']:
                        ostr += '<div class="link-indent">'
                    else:
                        ostr += '<div class="link">'
                    if ent.get('comment'):
                        ostr += self.format_link('?id=%d' % ent['id'], self.format_image_art('comment'))
                    if ent.get('linktype'):
                        ostr += self.format_image_art(ent['linktype'], also={'class': 'bullet'})
                    ostr += ent['text']
                    if ent['large']:
                        ostr += '</div>\n'
                        ostr += '<div class="link-desc">\n'
                    ostr += '<br>'.join(ent['desc'])
                    ostr += '</div>\n'
        return ostr

    def format_modal(self, modal_id, content):
	ostr = '<div id="%s" class="modal">\n' % modal_id
	ostr += '<div class="modal-content"><span class="close" id="%s.close">&times;</span>\n' % modal_id
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

#---- -------------------------------------------------------------------

if __name__ == '__main__':  # pragma: no cover
    pass
