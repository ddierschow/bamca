#!/usr/local/bin/python

import cgi, copy, os, re, sys
import config
import javascript
import mbdata
import secure
import useful


pseud_re = re.compile(r'''<\$(?P<cmd>\S*)\s(?P<arg>[^>]*)>''')
opt_selected = {True: ' SELECTED', False: ''}
opt_checked = {True: ' CHECKED', False: ''}
graphic_types = ['jpg', 'gif', 'bmp', 'ico', 'png']


# format_table({'also': {}, 'id': '', 'style_id': '', 'rows': []})
# rows=[{'ids': [], 'also': {}, 'cells': []}, ...]
# cells=[{'col': None, 'content': "&nbsp;", 'hdr': False, 'also': {}, 'large': False, 'id': ''}, ...]
class TableClass():
    def __init__(self, pif_render, also={}, id='', style_id=''):
        self.pif_render = pif_render
        self.also = also
        self.id = id
        self.style_id = style_id
        self.rows = list()

    def row(self, ids=[], also={}):
        nrow = dict()
        nrow['ids'] = ids
        nrow['also'] = also
        nrow['cells'] = list()
        self.rows.append(nrow)

    def cell(self, col=None, content='', hdr=False, also={}, large=False, id=''):
        ncell = dict()
        ncell['col'] = col
        ncell['content'] = content
        ncell['hdr'] = hdr
        ncell['also'] = also
        ncell['large'] = large
        ncell['id'] = id
        self.rows[-1]['cells'].append(ncell)

    def render(self):
        ostr = ''
        ostr += self.pif_render.format_table_start(also=self.also, id=self.id, style_id=self.style_id)
        ostr += self.pif_render.format_rows(self.rows)
        ostr += self.pif_render.format_table_end()
        return ostr


class Presentation():
    incrsel_js = javascript.def_increment_select_js
    toggle_display_js = javascript.def_toggle_display_js
    reset_button_js = javascript.def_reset_button_js
    increment_js = javascript.def_increment_js
    increment_select_js = javascript.def_increment_select_js
    def __init__(self, page_id, verbose):
        self.page_id = page_id
        self.art_dir = config.IMG_DIR_ART
        self.isbeta = False
        self.title = 'BAMCA'
        self.description = ''
        self.note = ''
        self.pic_dir = 'pics'
        self.tail = dict()
        self.simple = False
        self.large = False
        self.verbose = verbose
        self.dump_file = None
        self.not_released = False
        self.hide_title = False
        self.flags = 0L
        self.table_count = 0
        self.hierarchy = list()
        self.flag_info = None
        self.shown_flags = set()
        self.secure = None
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
        for row in res:
            self.flags = row['page_info.flags']
            self.format_type = row['page_info.format_type']
            self.title = row['page_info.title']
            self.pic_dir = row['page_info.pic_dir']
            self.description = row['page_info.description']
            self.note = self.fmt_pseudo(row['page_info.note'])
            self.tail = {x: 1 for x in row['page_info.tail'].split(',')}

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
        ostr = ''
        for lvl in self.hierarchy:
            ostr += '<a href="%s">%s</a> &gt; ' % lvl
        ostr += '<br>'
        return ostr

    def hierarchy_append(self, link, txt):
        self.hierarchy.append((link, txt))

    def get_flags(self):
        if not self.flag_info:
            self.flag_info = {x[0]: (x[1], config.FLAG_DIR + '/' + x[0].lower() + '.gif') for x in mbdata.countries}
        return self.flag_info

    def show_flag(self, country):
        flag = self.get_flags().get(country)
        if flag:
            self.shown_flags.add(country)
        return flag

#    def art_loc(self, img):
#       return self.art_dir + '/' + img

#    def art_url(self, img):
#       return '../' + self.art_loc(img)

    def find_art(self, fnames, suffix="gif"):
        return self.find_image_file(fnames, suffix=suffix, art=True)

    def find_image_file(self, fnames, vars=None, nobase=False, prefix='', suffix=None, largest=None, pdir=None, art=False):
        if not fnames:
            self.comment('find_image_file ret', '')
            return ''
        elif isinstance(fnames, str):
            fnames = [fnames]

        if suffix is None:
            suffix = graphic_types
        elif isinstance(suffix, str):
            suffix = [suffix]

        if largest:  # overrides previous setting of prefixes.
            prefix = mbdata.image_size_names
            if largest in prefix:
                prefix = prefix[:prefix.index(largest) + 1]
            prefix.reverse()
        elif isinstance(prefix, str):
            prefix = [prefix]

        if not pdir:
            if art:
                pdir = self.art_dir
            else:
                pdir = self.pic_dir

        if nobase:
            base = []
        else:
            base = ['']
        if not vars:
            vars = base
        elif isinstance(vars, str):
            vars = [vars] + base
        else:
            vars = vars + base

        self.comment("find_image_file", fnames, vars, prefix, suffix, pdir)
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
                            img = self.fmt_img_check(pdir + '/var/' + pfx + fname + '-' + var + suf)
                            if img:
                                self.comment('find_image_file ret', img)
                                return img
                            img = self.fmt_img_check(pdir + '/var/' + (pfx + fname + '-' + var + suf).lower())
                            if img:
                                self.comment('find_image_file ret', img)
                                return img
                        else:
                            img = self.fmt_img_check(pdir + '/' + pfx + fname + suf)
                            if img:
                                self.comment('find_image_file ret', img)
                                return img
                            img = self.fmt_img_check(pdir + '/' + (pfx + fname + suf).lower())
                            if img:
                                self.comment('find_image_file ret', img)
                                return img
        self.comment('find_image_file ret', '')
        return ''

    def find_button_images(self, name, image='', hover='', pdir=None):
        name = name.replace('_', ' ').upper()
        if not image:
            image = name.replace(' ', '_').lower()
        if not hover:
            hover = image
        if not image.startswith('but_'):
            image = 'but_' + image
        if not hover.startswith('hov_'):
            hover = 'hov_' + hover
        if not pdir:
            pdir = self.art_dir
        but_image = self.find_image_file(image, suffix='gif', pdir=pdir, art=True)
        hov_image = self.find_image_file(hover, suffix='gif', pdir=pdir, art=True)
        return name, but_image, hov_image

    # immediate effect functions.

    def comment(self, *args):
        if self.dump_file:  # pragma: no cover
            self.dump_file.write(' '.join([str(x) for x in args]) + '\n')
        elif self.verbose:
            useful.write_comment(*args)

    def comment_dict(self, name, arg):
        if self.verbose:
            useful.dump_dict_comment(name, arg)

    def print_html(self, cookie=None):
        print 'Content-Type: text/html'
        self.print_cookie(cookie)
        print
        print '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
        useful.header_done()
        print

    def print_cookie(self, cookie):  # pragma: no cover
        if cookie:
            print cookie.output()
            os.environ['HTTP_COOKIE'] = cookie.output()
        else:
            if self.secure.cookies:
                incookie = self.secure.cookies
            else:
                incookie = self.secure.get_cookies()
            if not incookie:
                pass
            elif 'id' not in incookie:
                pass
            elif '/' not in incookie['id'].value:
                incookie['id']['expires'] = -1
                print incookie.output()
                del os.environ['HTTP_COOKIE']
            elif incookie['id'].value.split('/')[1] != os.environ['REMOTE_ADDR']:
                incookie['id']['expires'] = -1
                print incookie.output()
                del os.environ['HTTP_COOKIE']

    #---- upper level rendering blocks

    def format_head(self, extra=''):
        pagetitle = self.title
        if self.isbeta:
            pagetitle = 'BETA: ' + pagetitle

        ostr  = '<html>\n<head><meta charset="UTF-8"><title>%s</title>\n' % pagetitle
        ostr += '<link rel="icon" href="http://www.bamca.org/' + self.art_dir + '/favicon.ico" type="image/x-icon" />\n'
        ostr += '<link rel="shortcut icon" href="http://www.bamca.org/' + self.art_dir + '/favicon.ico" type="image/x-icon" />\n'
        ostr += '<link rel="stylesheet" href="/styles/main.css" type="text/css">\n'
        if '.' in self.page_id:
            ostr += '<link rel="stylesheet" href="/styles/%s.css" type="text/css">\n' % self.page_id[:self.page_id.find('.')]
        ostr += '<link rel="stylesheet" href="/styles/%s.css" type="text/css">\n' % self.page_id

        if extra:
            ostr += extra + '\n'
        if not self.isbeta:
            ostr += javascript.def_google_analytics_js
        ostr += '</head>\n<body>\n'
        if self.isbeta:
            ostr += '<table width=100%><tr><td height=24 class="beta">&nbsp;</td></tr><tr><td>\n'
        ostr += self.show_location()
        if not self.hide_title:
            if self.title:
                ostr += '\n<div class="title">' + self.fmt_pseudo(self.title) + '</div>'
            ostr += self.fmt_img(self.page_id.split('.'), also={'class': 'centered'})
            if self.description:
                ostr += '\n<div class="description">' + self.description + '</div>'
        if self.note:
            ostr += '\n<div class="note">' + self.note + '</div>'
        ostr += '\n'
        return ostr

    def format_tail(self):
        ostr = "<p>\n"
#       if not self.simple and self.tail.get('printable'):
#           ostr += '''<a href="%s&simple=1">This list is also available in a more printable form.</a><p>\n''' % (os.environ['REQUEST_URI'])
#       if self.tail.get('vary'):
#           ostr += "Actual model color and decoration probably vary from picture as shown.<p>\n"
        if self.tail.get('effort'):
            ostr += "Every effort has been made to make this as accurate as possible.  If you have corrections, please contact us.<p>\n"
        if self.tail.get('moreinfo'):
            ostr += "Feel free to ask for clarification on these or other models.<p>"
        if self.tail.get('contact'):
            ostr += 'This page is maintained by members of BAMCA.\n'
            ostr += '<a href="../pages/faq.html">See here for information on contacting us.</a><p>\n'
        if self.tail.get('disclaimer'):
            ostr += '''<hr>
BAMCA is a private club and is not affiliated with Tyco Toys, Inc. or Matchbox
Toys (USA) Ltd.  Matchbox and the Matchbox logo are registered trademarks
of Matchbox International Ltd. and are used with permission.
<hr><p>
'''
        if self.tail.get('flags'):
            ball = '%s\n' % self.fmt_art('ball.gif', desc='o')
            ostr += '<center>\n'
            listFlag = list(self.shown_flags)
            listFlag.sort(key=lambda x: self.flag_info[x][0])
            ostr += ball.join(['<nobr>%s %s</nobr> ' % (self.format_image_flag(x), self.flag_info[x][0]) for x in listFlag])
            ostr += '</center><p>\n'

        st = self.tail.get('stat')
        if st:  # pragma: no cover
            ostr += '\n<font size=-1><i>%s</i></font>\n' % st
        if self.isbeta:
            ostr += '</td></tr><tr><td height=24 class="beta">&nbsp;</td></tr></table>\n'
        ostr += "</body>\n</html>\n"
        return ostr

    #---- tables

    def create_table(self, also={}, id='', style_id=''):
        return TableClass(self, also, id, style_id)

    def format_table_single_cell(self, col, content='', talso={}, ralso={}, calso={}, id='', hdr=False):
        ostr = self.format_table_start(also=talso, id=id)
        ostr += self.format_row_start(also=ralso)
        ostr += self.format_cell(col, content, hdr, also=calso)
        ostr += self.format_row_end()
        ostr += self.format_table_end()
        return ostr

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
        if not content:
            content = '&nbsp;'
        ostr = self.format_cell_start(col, hdr, also, large, id)
        ostr += str(content)
        ostr += self.format_cell_end(col, hdr, large)
        return ostr

    def format_cell_start(self, col=None, hdr=False, also={}, large=False, id=''):
        cellstyle = {False: 'eb', True: 'eh'}[hdr]
        celltype = {False: "td", True: "th"}
        also = useful.dict_merge(also, {'class': self.style_name(also.get('class'), cellstyle, col, id)})
        self.comment('format_cell_start', col, hdr, also)
#       if 'class' not in also:
#           also = useful.dict_merge(also, self.style.FindName(' '.join(class_ids), self.simple, self.verbose))
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
        ostr = ''
        for cell in cells:
            ostr += self.format_cell(**cell)
        return ostr

    #----

    def format_warning(self, *message):
        return '<div class="warning">%s</div>\n' % ' '.join(message)

    def format_section(self, content, fn=None, also=None, cols=0, id=''):
        if not fn:
            fn = list()
        if not also:
            also = dict()
        nalso = copy.deepcopy(also)
        nalso['class'] = self.style_name(also.get('class'), 'sh', id)
        if cols:
            nalso['colspan'] = cols
        ostr = ''
        if not self.simple and fn:
            strimg = self.fmt_opt_img(fn)
            if len(strimg) > 6:
                ostr += strimg + '<br>'
        if not self.simple:
#           nalso.update(self.style.FindClassID('sh', simple=self.simple))
            ostr = self.format_row_start()
        ostr += '  <th%s>%s</th>\n' % (useful.fmt_also(nalso), self.fmt_pseudo(content))
        if not self.simple:
            ostr += self.format_row_end()
        return ostr

    def format_section_freestanding(self, content, fn=[], also={}, cols=0, id=''):
        nalso = copy.deepcopy(also)
        nalso['class'] = self.style_name(also.get('class'), 'sh', id)
        ostr = strimg = ''
        if not self.simple and fn:
            strimg = self.fmt_opt_img(fn)
            if len(strimg) > 6:
                strimg += '<br>'
            else:
                strimg = ''
#       if not self.simple:
#           nalso.update(self.style.FindClassID('sh', simple=self.simple))
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


    def format_link(self, url, txt, args={}, nstyle=None, also={}):
        txt = self.fmt_pseudo(txt)
        ostr = ''
        if nstyle:
            ostr += '<span' + useful.fmt_also(nstyle) + '>'
        if not url and not also:
            ostr += txt
        elif not url:
            ostr += '<a%s>%s</a>' % (useful.fmt_also(also), txt)
        elif not txt:
            ostr += '<a href="%s"%s>%s</a>' % (url, useful.fmt_also(also), url)
        else:
            ostr += '<a href="%s"%s>%s</a>' % (url, useful.fmt_also(also), txt)
        if args:
            args = "&".join([x + '=' + args[x] for x in args.keys()])
            if '?' in url:
                url += '&' + args
            else:
                url += '?' + args
        if nstyle:
            ostr += '</span>\n'
        return ostr

    #---- forms

    def format_checkbox(self, name, options, checked=[]):
        #self.comment('format_checkbox', name, options, checked)
        ostr = ''
        for option in options:
            ostr += '<nobr><input type="checkbox" name="%s" value="%s"%s> %s</nobr>\n' % (name, option[0], opt_checked[option[0] in checked], option[1])
        return ostr

    def format_radio(self, name, options, checked='', sep=''):
        ostr = ''
        for option in options:
            ostr += '<input type="radio" name="%s" value="%s"%s> %s\n' % (name, option[0], opt_checked[option[0] == checked], option[1]) + sep
        return ostr

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
            ostr += '<option value="%s"%s>%s\n' % (option[0], opt_selected[option[0] == selected], option[1])
        ostr += '</select>'
        return ostr

    def format_text_input(self, name, maxlength, showlength=24, value=''):
        if not value:
            value = ''
        return '<input name="%s" type="text" size="%d" maxlength="%d" value="%s">\n' % (name, min(showlength, maxlength), maxlength, cgi.escape(str(value), True))

    def format_password_input(self, name, maxlength=80, showlength=24, value=''):
        return '<input name="%s" type="text" size="%d" maxlength="%d" value="%s">\n' % (name, min(showlength, maxlength), maxlength, value)

    def format_hidden_input(self, values):
        return reduce(lambda x, y: x + '<input type="hidden" name="%s" value="%s">\n' % (y, values[y]), values.keys(), '')

    #---- buttons

    def format_button_up_down(self, field):
        ostr = ''
        #up_image = self.format_image_button('up', 'inc')
        #dn_image = self.format_image_button('down', 'dec')
        ostr += '''<a onclick="incrfield(%s, 1);">%s</a>''' % (field, self.format_image_button('up', 'inc'))
        ostr += '''<a onclick="incrfield(%s,-1);">%s</a>''' % (field, self.format_image_button('down', 'dec'))
        return ostr

    def format_button_up_down_select(self, id, vl=1):
        but_max = self.format_image_button("top", 'max')
        but_inc = self.format_image_button("up", 'inc')
        but_dec = self.format_image_button("down", 'dec')
        but_min = self.format_image_button("bottom", 'min')
        ostr = ''
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
        if collapsed:
            fname = 'expand'
        else:
            fname = 'collapse'
        #image = self.art_loc('but_' + fname + '.gif')
        #hover = self.art_loc('hov_' + fname + '.gif')
        but_image = self.find_image_file('but_' + fname, suffix='gif', art=True)
        hov_image = self.find_image_file('hov_' + fname, suffix='gif', art=True)
        also = {'src': '../' + but_image,
                'id': id + '_l',
                'value': fname,
                'onclick': "toggle_visibility('%s','%s_l'); return false;" % (id, id),
                'class': 'button',
                'onmouseover': "this.src='../%s';" % hov_image,
                'onmouseout': "this.src='../%s';" % but_image}
        return '<input type="image"%s>\n' % useful.fmt_also(also)

    def format_button_input(self, bname="submit", name=None, also={}):
        bname, but_image, hov_image = self.find_button_images(bname, pdir=self.art_dir)
        if not name:
            name = bname

        inputname = name.replace(' ', '_').lower()
        altname = bname.replace('_', ' ').upper()
        imalso = {'class': 'button', 'alt': altname}
        self.comment('FormatButtonImage', bname, name, also, but_image, hov_image)
        if not but_image or not useful.is_good(but_image, v=self.verbose):
            imalso = {'class': 'textbutton', 'onmouseover': "this.class='textbuttonh';", 'onmouseout': "this.class='textbutton';"}
            return '<input type="submit" name="%s" value="%s"%s>\n' % (inputname, altname, useful.fmt_also(imalso, also))
        elif not hov_image or not useful.is_good(hov_image, v=self.verbose):
            return '<input type="image" name="%s" src="../%s"%s>' % (inputname, but_image, useful.fmt_also(imalso, also))
        else:
            imalso.update({'onmouseover': "this.src='../%s';" % hov_image, 'onmouseout': "this.src='../%s';" % but_image})
            return '<input type="image" name="%s" src="../%s"%s>' % (inputname, but_image, useful.fmt_also(imalso, also))

    def format_image_button(self, name, image='', hover='', pdir=None, also={}):
        name, but_image, hov_image = self.find_button_images(name, image, hover, pdir)

        imalso = useful.dict_merge({'class': 'button'}, also)
        btn = ''
        if not but_image:
            btn = '<span class="textbutton">%s</span>' % name
        elif not hov_image:
            btn = self.fmt_img_src(but_image, alt=name, also=imalso)
        else:
            imalso.update({'onmouseover': "this.src='../%s';" % hov_image, 'onmouseout': "this.src='../%s';" % but_image})
            btn = self.fmt_img_src(but_image, alt=name, also=imalso)
        return btn

    def format_button(self, bname, link='', image='', args={}, also={}, lalso={}):
        #self.comment('format_button', bname, link)
        #return self.FormatImageLink(bname.replace('_', ' ').upper(), 'but_' + bname.replace(' ', '_').lower(), 'hov_' + bname.replace(' ', '_').lower(), link, args, self.art_dir, also, lalso)
        btn = self.format_image_button(bname, image=image, pdir=self.art_dir, also=also)
        #self.comment('Button image:', btn)
        if link:
            btn = self.format_link(link, btn, args=args, also=lalso)
        return btn + '\n'

    def format_button_reset(self, name):
        return '<img ' + \
                'src="../' + self.art_dir + '/but_reset.gif" ' + \
                'onmouseover="this.src=\'../' + self.art_dir + '/hov_reset.gif\';" ' + \
                'onmouseout="this.src=\'../' + self.art_dir + '/but_reset.gif\';" ' + \
                'border="0" onClick="ResetForm(document.%s)" alt="RESET" class="button">' % name

    def format_button_comment(self, pif, args=None):
        if args:
            args = 'page=%s&%s' % (pif.page_id, args)
        else:
            args = 'page=%s' % pif.page_id
        ostr = self.format_button("comment_on_this_page", link='../pages/comment.php?%s' % args, also={'class': 'comment'}, lalso=dict())
        if pif.is_allowed('a'):  # pragma: no cover
            ostr += self.format_button("pictures", link="traverse.cgi?d=%s" % self.pic_dir, also={'class': 'comment'}, lalso=dict())
            ostr += self.format_button("edit_this_page", link=pif.dbh.get_editor_link('page_info', {'id': pif.page_id}), also={'class': 'comment'}, lalso=dict())
        return ostr

    #---- images

    def format_image_art(self, fname, desc='', hspace=0, also={}):
        return self.fmt_art(fname, desc, hspace, also)

    def format_image_flag(self, code2, name='', hspace=0, also={}):
        return self.fmt_opt_img(code2, alt=name, pdir=config.FLAG_DIR, also=useful.dict_merge({'hspace': hspace}, also))

    def format_image_as_link(self, fnames, txt, pdir=None, also={}):
        return self.format_link('../' + self.find_image_file(fnames, suffix=graphic_types, pdir=pdir), txt, also=also)

    def format_image_optional(self, fnames, alt=None, prefix='', suffix=None, pdir=None, also={}, vars=None, nopad=False):
        return self.fmt_img(fnames, alt=alt, prefix=prefix, suffix=suffix, pdir=pdir, also=also, vars=vars, pad=not nopad)

    def format_image_required(self, fnames, alt=None, vars=None, nobase=False, prefix='', suffix=None, pdir=None, also={}, made=True):
        return self.fmt_img(fnames, alt=alt, vars=vars, nobase=nobase, prefix=prefix, suffix=suffix, pdir=pdir, also=also, made=made, required=True)

    def format_image_list(self, fn, alt=None, wc='', prefix='', suffix='jpg', pdir=None):
        self.comment('format_image_list', fn, alt, wc, prefix, suffix, pdir)
        if not pdir:
            pdir = self.pic_dir
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

    def format_image_sized(self, fnames, vars=None, nobase=False, largest='g', suffix=None, pdir=None, required=False):
        return self.fmt_img(fnames, alt='', vars=vars, nobase=nobase, suffix=suffix, largest=largest, pdir=pdir, required=required)

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

    def fmt_art(self, fname, desc='', hspace=0, also={}):
        return self.fmt_img(fname, alt=desc, pdir=self.art_dir, also=useful.dict_merge(also, {'hspace': hspace}))

    def fmt_img_src(self, pth, alt=None, also={}):
        if useful.is_good(pth, v=self.verbose):
            return '<img src="../' + pth + '"' + useful.fmt_also({'alt': alt}, also) + '>'
        return ''

    def fmt_img_check(self, pth):
        self.comment("fmt_img_check", pth)
        if useful.is_good(pth, v=self.verbose):
            return pth
        return ''

    def fmt_img(self, fnames, alt=None, vars=None, nobase=False, prefix='', suffix=None, pdir=None, largest=None, also={}, made=True, required=False, pad=False):
        img = self.find_image_file(fnames, vars=vars, nobase=nobase, prefix=prefix, suffix=suffix, largest=largest, pdir=pdir)
        if img:
            return self.fmt_img_src(img, alt=alt, also=also)
        if required:
            return self.fmt_no_pic(made, prefix)
        if pad:
            return '&nbsp;'
        return ''

    def fmt_no_pic(self, made=True, prefix=''):
        # prefix not implemented yet!
        pic = {False: 'nopic.gif', True: 'notmade.gif'}[not made]
        return self.fmt_art(pic)

    def fmt_opt_img(self, fnames, alt=None, prefix='', suffix=None, pdir=None, also={}, vars=None, nopad=False):
        return self.fmt_img(fnames, alt=alt, prefix=prefix, suffix=suffix, pdir=pdir, also=also, vars=vars, pad=not nopad)

    def fmt_anchor(self, name):
        if name:
            return '<a name="%s"></a>\n' % name
        return ''

#    def fmt_graphics(self, graphics):
#       ostr = ''
#       for graf in graphics:
#           ostr += self.fmt_opt_img(graf['file'], alt=graf.get('name', ''), pdir=graf.get('pic_dir'), also=graf.get('also', {})) + '\n'
#       return ostr

    def format_bullet_list(self, descs):
        ostr = ''
        descs = filter(None, descs)
        if descs:
            ostr += "   <ul>" + '\n'
            for desc in descs:
                ostr += "    <li>" + desc + '\n'
            ostr += "   </ul>" + '\n'
        return ostr

    # a lineup consists of a header (outside of the table) plus a set of sections, each in its own table.
    #     id, name, note, graphics, columns, tail | section
    # a section consists of a header (inside the table) plus a set of ranges.
    #     id, name, note, anchor, columns, switch, count | range
    # a range consists of a header plus a set of entries.
    #     id, name, note, anchor, graphics | entry
    # an entry contains the contents of a cell plus cell controls
    #     display_id, text, rowspan, colspan, class, st_suff, style, also,

    def format_lineup(self, llineup):
        ostr = '<!-- Starting format_lineup -->\n'
        maxes = {'s': 0, 'r': 0, 'e': 0}
        self.comment_dict('lineup', llineup)
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
            ostr += self.format_row_start()
            ostr += '<td>\n'
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
                    if ent.get('rowspan') or ent.get('colspan'):
                        spans[icol] = [ent.get('colspan', 1), ent.get('rowspan', 1) - 1]
                        also.update({'rowspan': ent.get('rowspan', 1), 'colspan': ent.get('colspan', 1)})
                        also['width'] = '%d%%' % (int(ent.get('colspan', 1)) * 100 / ncols)
                    if ent.get('also'):
                        also.update(ent['also'])
                    if 'width' not in also:
                        also['width'] = '%d%%' % (100/ncols)
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
            ostr += self.format_cell_end()
            ostr += self.format_row_end()
            ostr += self.format_table_end()
            maxes['s'] = max(maxes['s'], sc)
        #print 'sec %(s)d ran %(r)d ent %(e)d<br>' % maxes
        ostr += self.format_box_tail(llineup.get('tail'))
        return ostr

    def format_ul_lineup(self, llineup):
        ostr = '<!-- Starting format_ul_lineup -->\n'
        if llineup.get('graphics'):
            for graf in llineup['graphics']:
                ostr += self.fmt_opt_img(graf, suffix='gif')
        lin_id = llineup.get('id', '')
        if llineup.get('note'):
            ostr += llineup['note'] + '<br>'
        for sec in llineup.get('section', []):
            salso = dict()
            sec_id = sec.get('id', '')
            ostr += self.fmt_anchor(sec.get('anchor'))
            ncols = sec.get('columns', llineup.get('columns', 4))
            if 'switch' in sec:
                ostr += self.format_button_input_visibility(sec_id, sec['switch'])
                ostr += sec.get('count', '')
            if sec.get('name'):
                ostr += self.format_section_freestanding(sec.get('name', ''), cols=ncols, id=sec['id'])
            if sec.get('note'):
                salso['class'] = self.style_name(salso.get('class'), 'sb', sec_id)
                ostr += '<div%s>%s</div>' % (useful.fmt_also(salso), sec['note'])
            for ran in sec.get('range', []):
                ralso = dict()
                ran_id = ran.get('id', '')
                ostr += self.fmt_anchor(ran.get('anchor'))
#               if ran.get('name') or ran.get('graphics'):
#                   ostr += self.format_range(ran.get('name', ''), None, ran.get('graphics', list()), cols=sec['columns'], id=ran.get('id', ''))
                if ran.get('name'):
                    ralso['class'] = self.style_name(ralso.get('class'), 'rh', ran_id)
                    ostr += '<div%s>%s</div>\n' % (useful.fmt_also(ralso), ran['name'])
                if ran.get('note'):
                    #ralso['class'] = self.style_name(ralso.get('class'), 'rb', ran_id)
                    ostr += '<div%s>%s</div>\n' % (useful.fmt_also({'class': 'rb ' + ran_id}), ran['note'])
                ostr += '<ul%s>\n' % useful.fmt_also(ralso)
                for ent in ran.get('entry', []):
                    disp_id = ent.get('display_id')
                    if not disp_id:
                        disp_id = ran_id
                    ealso = {'class': self.style_name(ent.get('class'), 'eb')}
                    if ent.get('style'):
                        ealso['style'] = ent['style']
                    if ent.get('also'):
                        ealso.update(ent['also'])
                    if 'width' not in ealso:
                        ealso['width'] = '%d%%' % (100/ncols)
                    ostr += '<li%s>%s</li>\n' % (useful.fmt_also(ealso), ent['text'])
                ostr += '</ul>\n'
        ostr += self.format_box_tail(llineup.get('tail'))
        return ostr

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


#---- -------------------------------------------------------------------

if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
