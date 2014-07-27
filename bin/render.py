#!/usr/local/bin/python

import cgi, copy, os, re, sys
import config
import javascript
import mbdata
import secure
import useful


pseud_re = re.compile(r'''<\$(?P<cmd>\S*)\s(?P<arg>[^>]*)>''')
opt_selected = {True : ' SELECTED', False : ''}
opt_checked = {True : ' CHECKED', False : ''}
graphic_types = [ 'jpg', 'gif', 'bmp', 'ico', 'png' ]


    #FormatTable({'also':{}, 'id':'', 'style_id':'', 'rows':[]})
    #rows=[{'ids':[], 'also':{}, 'cells':[]}, ...]
    #cells=[{'col':None, 'content':"&nbsp;", 'hdr':False, 'also':{}, 'large':False, 'id':''}, ...]
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
	ostr += self.pif_render.FormatTableStart(also=self.also, id=self.id, style_id=self.style_id)
	ostr += self.pif_render.FormatRows(self.rows)
	ostr += self.pif_render.FormatTableEnd()
	return ostr


class Presentation():
    incrsel_js = javascript.def_increment_select_js
    toggle_display_js = javascript.def_toggle_display_js
    reset_button_js = javascript.def_reset_button_js
    increment_js = javascript.def_increment_js
    increment_select_js = javascript.def_increment_select_js
    def __init__(self, page_id, verbose):
	self.page_id = page_id
	self.art_dir = config.imgdirArt
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
#	if self.verbose:
#	    import datetime
#	    self.dump_file = open(os.path.join(config.logroot, datetime.datetime.now().strftime('%Y%m%d.%H%M%S.log')), 'w')

#    def __str__(self):
#	return str(self.__dict__)

    def __repr__(self):
	return "'<render.Presentation instance>'"

    def __str__(self):
	return "'<render.Presentation instance>'"

    def ErrorReport(self):
	return str(self.__dict__)

    def SetPageInfo(self, res):
	for row in res:
	    self.flags = row['page_info.flags']
	    self.format_type = row['page_info.format_type']
	    self.title = row['page_info.title']
	    self.pic_dir = row['page_info.pic_dir']
	    self.description = row['page_info.description']
	    self.note = self.FmtPseudo(row['page_info.note'])
	    self.tail = {x: 1 for x in row['page_info.tail'].split(',')}

    def StyleName(self, previous, prefix, col=None, id=None):
	class_ids = list()
	if previous:
	    class_ids.append(previous)
	if col != None and col != '':
	    if id:
		class_ids.append(prefix + '_' + str(col) + '_' + id)
	    class_ids.append(prefix + '_' + str(col))
	if id:
	    class_ids.append(prefix + '_' + id)
	class_ids.append(prefix)
	return ' '.join(class_ids)

    def ShowLocation(self):
	ostr = ''
	for lvl in self.hierarchy:
	    ostr += '<a href="%s">%s</a> &gt; ' % lvl
	ostr += '<br>'
	return ostr

    def GetFlags(self):
	if not self.flag_info:
	    self.flag_info = {x[0]: (x[1], config.flagdir + '/' + x[0].lower() + '.gif') for x in mbdata.countries}
	return self.flag_info

    def ShowFlag(self, country):
	flag = self.GetFlags().get(country)
	if flag:
	    self.shown_flags.add(country)
	return flag

#    def ArtLoc(self, img):
#	return self.art_dir + '/' + img

#    def ArtURL(self, img):
#	return '../' + self.ArtLoc(img)

    def FindArt(self, fnames, suffix="gif"):
	return self.FindImageFile(fnames, suffix=suffix, art=True)

    def FindImageFile(self, fnames, vars=None, nobase=False, prefix='', suffix=None, largest=None, pdir=None, art=False):
	if not fnames:
	    self.Comment('FindImageFile ret', '')
	    return ''
	elif isinstance(fnames, str):
	    fnames = [fnames]

	if suffix == None:
	    suffix = graphic_types
	elif isinstance(suffix, str):
	    suffix = [suffix]

	if largest: # overrides previous setting of prefixes.
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

	self.Comment("FindImageFile", fnames, vars, prefix, suffix, pdir)
	for var in vars:
	    for fname in fnames:
		fname = useful.CleanName(fname.replace('/', '_'))
#		if not fname:
#		    continue
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
			    img = self.FmtImgCheck(pdir + '/var/' + pfx + fname + '-' + var + suf)
			    if img:
				self.Comment('FindImageFile ret', img)
				return img
			    img = self.FmtImgCheck(pdir + '/var/' + (pfx + fname + '-' + var + suf).lower())
			    if img:
				self.Comment('FindImageFile ret', img)
				return img
			else:
			    img = self.FmtImgCheck(pdir + '/' + pfx + fname + suf)
			    if img:
				self.Comment('FindImageFile ret', img)
				return img
			    img = self.FmtImgCheck(pdir + '/' + (pfx + fname + suf).lower())
			    if img:
				self.Comment('FindImageFile ret', img)
				return img
	self.Comment('FindImageFile ret', '')
	return ''

    def FindButtonImages(self, name, image='', hover='', pdir=None):
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
	but_image = self.FindImageFile(image, suffix='gif', pdir=pdir, art=True)
	hov_image = self.FindImageFile(hover, suffix='gif', pdir=pdir, art=True)
	return name, but_image, hov_image

    # immediate effect functions.

    def Comment(self, *args):
	if self.dump_file: # pragma: no cover
	    self.dump_file.write(' '.join([str(x) for x in args]) + '\n')
	elif self.verbose:
	    useful.WriteComment(*args)

    def CommentDict(self, name, arg):
	if self.verbose:
	    useful.DumpDictComment(name, arg)

    def PrintHtml(self, cookie=None):
	print 'Content-Type: text/html'
	self.PrintCookie(cookie)
	print
	print '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'
	useful.HeaderDone()
	print

    def PrintCookie(self, cookie): # pragma: no cover
	if cookie:
	    print cookie.output()
	    os.environ['HTTP_COOKIE'] = cookie.output()
	else:
	    if self.secure.cookies:
		incookie = self.secure.cookies
	    else:
		incookie = self.secure.GetCookies()
	    if not incookie:
		pass
	    elif not 'id' in incookie:
		pass
	    elif not '/' in incookie['id'].value:
		incookie['id']['expires'] = -1
		print incookie.output()
		del os.environ['HTTP_COOKIE']
	    elif incookie['id'].value.split('/')[1] != os.environ['REMOTE_ADDR']:
		incookie['id']['expires'] = -1
		print incookie.output()
		del os.environ['HTTP_COOKIE']

    #---- upper level rendering blocks

    def FormatHead(self, extra=''):
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
	    ostr += '<table width=100%><tr><td height=24 class="beta">&nbsp;</td></tr><tr><td>\n';
	ostr += self.ShowLocation()
	if not self.hide_title:
	    if self.title:
		ostr += '\n<div class="title">' + self.FmtPseudo(self.title) + '</div>'
	    ostr += self.FmtImg(self.page_id.split('.'), also={'class':'centered'})
	    if self.description:
		ostr += '\n<div class="description">' + self.description + '</div>'
	if self.note:
	    ostr += '\n<div class="note">' + self.note + '</div>'
	ostr += '\n'
	return ostr

    def FormatTail(self):
	ostr = "<p>\n"
#	if not self.simple and self.tail.get('printable'):
#	    ostr += '''<a href="%s&simple=1">This list is also available in a more printable form.</a><p>\n''' % (os.environ['REQUEST_URI'])
#	if self.tail.get('vary'):
#	    ostr += "Actual model color and decoration probably vary from picture as shown.<p>\n"
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
	    ball = '%s\n' % self.FmtArt('ball.gif', desc='o')
	    ostr += '<center>\n'
	    listFlag = list(self.shown_flags)
	    listFlag.sort(key=lambda x: self.flag_info[x][0])
	    ostr += ball.join(['<nobr>%s %s</nobr> ' % (self.FormatImageFlag(x), self.flag_info[x][0]) for x in listFlag])
	    ostr += '</center><p>\n'

	st = self.tail.get('stat')
	if st: # pragma: no cover
	    ostr += '\n<font size=-1><i>%s</i></font>\n' % st
	if self.isbeta:
	    ostr += '</td></tr><tr><td height=24 class="beta">&nbsp;</td></tr></table>\n';
	ostr += "</body>\n</html>\n"
	return ostr

    #---- tables

    def CreateTable(self, also={}, id='', style_id=''):
	return TableClass(self, also, id, style_id)

    def FormatTableSingleCell(self, col, content='', talso={}, ralso={}, calso={}, id='', hdr=False):
	ostr = self.FormatTableStart(also=talso, id=id)
	ostr += self.FormatRowStart(also=ralso)
	ostr += self.FormatCell(col, content, hdr, also=calso)
	ostr += self.FormatRowEnd()
	ostr += self.FormatTableEnd()
	return ostr

    def FormatTableStart(self, also={}, id='', style_id=''):
	also = copy.deepcopy(also)
	self.table_count += 1
	also['class'] = self.StyleName(also.get('class'), 'tb', style_id)
	if id:
	    also['id'] = id
	return '<table%s>\n' % useful.Also(also)

    def FormatTableEnd(self):
	self.table_count -= 1
	return "</table>\n"

    def FormatRowStart(self, ids=[], also={}):
	ostr = " <tr%s>\n" % useful.Also(also)
	for id in ids:
	    ostr += self.FmtAnchor(id)
	return ostr

    def FormatRowEnd(self):
	return " </tr>\n"

    def FormatCell(self, col=None, content="&nbsp;", hdr=False, also={}, large=False, id=''):
	#self.Comment('FormatCell', col, hdr, also)
	if not content:
	    content = '&nbsp;'
	ostr = self.FormatCellStart(col, hdr, also, large, id)
	ostr += str(content)
	ostr += self.FormatCellEnd(col, hdr, large)
	return ostr

    def FormatCellStart(self, col=None, hdr=False, also={}, large=False, id=''):
	cellstyle = { False : 'eb', True : 'eh' }[hdr]
	celltype = {False : "td", True : "th"}
	also = useful.DictMerge(also, {'class' : self.StyleName(also.get('class'), cellstyle, col, id)})
	self.Comment('FormatCellStart', col, hdr, also)
#	if 'class' not in also:
#	    also = useful.DictMerge(also, self.style.FindName(' '.join(class_ids), self.simple, self.verbose))
	return '  <%s%s>' % (celltype[hdr], useful.Also(also))

    def FormatCellEnd(self, col=0, hdr=False, large=False):
	celltype = {False : "td", True : "th"}
	ostr = '  </' + celltype[hdr] + '>\n'
	if large:
	    ostr += " </tr>\n"
	return ostr

    #FormatTable({'also':{}, 'id':'', 'style_id':'', 'rows':[]})
    #rows=[{'ids':[], 'also':{}, 'cells':[]}, ...]
    #cells=[{'col':None, 'content':"&nbsp;", 'hdr':False, 'also':{}, 'large':False, 'id':''}, ...]

    def FormatTable(self, table):
	ostr = ''
	ostr += self.FormatTableStart(also=table.get('also', {}), id=table.get('ids', []), style_id=table.get('style_id', ''))
	ostr += self.FormatRows(table.get('rows', []))
	ostr += self.FormatTableEnd()
	return ostr

    def FormatRows(self, rows):
	ostr = ''
	for row in rows:
	    ostr += self.FormatRowStart(ids=row.get('ids', []), also=row.get('also', {}))
	    ostr += self.FormatCells(row.get('cells', []))
	    ostr += self.FormatRowEnd()
	return ostr

    def FormatCells(self, cells):
	ostr = ''
	for cell in cells:
	    ostr += self.FormatCell(**cell)
	return ostr

    #----

    def FormatWarning(self, *message):
	return '<div class="warning">%s</div>\n' % ' '.join(message)

    def FormatSection(self, content, fn=None, also=None, cols=0, id=''):
	if not fn:
	    fn = list()
	if not also:
	    also = dict()
	nalso = copy.deepcopy(also)
	nalso['class'] = self.StyleName(also.get('class'), 'sh', id)
	if cols:
	    nalso['colspan'] = cols
	ostr = ''
	if not self.simple and fn:
	    strimg = self.FmtOptImg(fn)
	    if len(strimg) > 6:
		ostr += strimg + '<br>'
	if not self.simple:
#	    nalso.update(self.style.FindClassID('sh', simple=self.simple))
	    ostr = self.FormatRowStart()
	ostr += '  <th%s>%s</th>\n' % (useful.Also(nalso), self.FmtPseudo(content))
	if not self.simple:
	    ostr += self.FormatRowEnd()
	return ostr

    def FormatSectionFreestanding(self, content, fn=[], also={}, cols=0, id=''):
	nalso = copy.deepcopy(also)
	nalso['class'] = self.StyleName(also.get('class'), 'sh', id)
	ostr = strimg = ''
	if not self.simple and fn:
	    strimg = self.FmtOptImg(fn)
	    if len(strimg) > 6:
		strimg += '<br>'
	    else:
		strimg = ''
#	if not self.simple:
#	    nalso.update(self.style.FindClassID('sh', simple=self.simple))
	ostr += '  <div%s>%s%s</div>\n' % (useful.Also(nalso), strimg, self.FmtPseudo(content))
	return ostr


    def FormatRange(self, content, col, fn=[], also={}, large=False, nstyle=None, cols=3, id=''):
	nalso = copy.deepcopy(also)
	nalso['class'] = self.StyleName(also.get('class'), 'rh', col, id)
	ostr = self.FormatRowStart() + '  <th' + useful.Also(nalso) + '>'
	self.Comment(large, cols)
	if large:
	    ostr += self.FmtOptImg(fn) + content + '</th>\n'
	elif cols == 1:
	    ostr += self.FmtOptImg(fn) + '\n'
	    ostr += '%s</th>\n' % content
	elif cols == 2:
	    ostr += self.FmtOptImg(fn) + '</th>\n'
	    ostr += '  <th' + useful.Also({'colspan' : cols - 2}, nalso) + '>%s</th>\n' % content
	else:
	    ostr += self.FmtOptImg(fn) + '</th>\n'
	    ostr += '  <th' + useful.Also({'colspan' : cols - 2}, nalso) + '>%s</th>\n' % content
	    ostr += '  <th' + useful.Also(nalso) + '>&nbsp;</th>\n'
	ostr += self.FormatRowEnd()
	#self.Comment('nalso', nalso)
	return ostr


    def FormatLink(self, url, txt, args={}, nstyle=None, also={}):
	txt = self.FmtPseudo(txt)
	ostr = ''
	if nstyle:
	    ostr += '<span' + useful.Also(nstyle) + '>'
	if not url and not also:
	    ostr += txt
	elif not url:
	    ostr += '<a%s>%s</a>' % (useful.Also(also), txt)
	elif not txt:
	    ostr += '<a href="%s"%s>%s</a>' % (url, useful.Also(also), url)
	else:
	    ostr += '<a href="%s"%s>%s</a>' % (url, useful.Also(also), txt)
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

    def FormatCheckbox(self, name, options, checked=[]):
	#self.Comment('FormatCheckbox', name, options, checked)
	ostr = ''
	for option in options:
	    ostr += '<nobr><input type="checkbox" name="%s" value="%s"%s> %s</nobr>\n' % (name, option[0], opt_checked[option[0] in checked], option[1])
	return ostr

    def FormatRadio(self, name, options, checked='', sep=''):
	ostr = ''
	for option in options:
	    ostr += '<input type="radio" name="%s" value="%s"%s> %s\n' % (name, option[0], opt_checked[option[0] == checked], option[1]) + sep
	return ostr

    def FormatSelectCountry(self, name, selected='', id=None):
	return self.FormatSelect(name, [('', '')] + mbdata.countries, selected='', id=None)

    def FormatSelect(self, name, options, selected='', id=None):
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

    def FormatTextInput(self, name, maxlength, showlength=24, value=''):
	if not value:
	    value = ''
	return '<input name="%s" type="text" size="%d" maxlength="%d" value="%s">\n' % (name, min(showlength, maxlength), maxlength, cgi.escape(str(value), True))

    def FormatPasswordInput(self, name, maxlength=80, showlength=24, value=''):
	return '<input name="%s" type="text" size="%d" maxlength="%d" value="%s">\n' % (name, min(showlength, maxlength), maxlength, value)

    def FormatHiddenInput(self, values):
	return reduce(lambda x, y: x + '<input type="hidden" name="%s" value="%s">\n' % (y, values[y]), values.keys(), '')

    #---- buttons

    def FormatButtonUpDown(self, field):
	#up_image = self.FormatImageButton('up', 'inc')
	#dn_image = self.FormatImageButton('down', 'dec')
	ostr =  '''<a onclick="incrfield(%s, 1);">%s</a>''' % (field, self.FormatImageButton('up', 'inc'))
	ostr += '''<a onclick="incrfield(%s,-1);">%s</a>''' % (field, self.FormatImageButton('down', 'dec'))
	return ostr

    def FormatButtonUpDownSelect(self, id, vl=1):
	but_max = self.FormatImageButton("top", 'max')
	but_inc = self.FormatImageButton("up", 'inc')
	but_dec = self.FormatImageButton("down", 'dec')
	but_min = self.FormatImageButton("bottom", 'min')
	if vl > 0:
	    ostr =  "<a onclick=\"settsel('%s');\">%s</a>\n" % (id, but_max)
	    ostr += "<a onmousedown=\"toggleOnSel('%s', 1);\" onmouseup=\"toggleOff();\">%s</a>\n" % (id, but_inc)
	    ostr += "<a onmousedown=\"toggleOnSel('%s',-1);\" onmouseup=\"toggleOff();\">%s</a>\n" % (id, but_dec)
	    ostr += "<a onclick=\"setbsel('%s');\">%s</a>\n" % (id, but_min)
	else:
	    ostr =  "<a onclick=\"setbsel('%s');\">%s</a>\n" % (id, but_max)
	    ostr += "<a onmousedown=\"toggleOnSel('%s',-1);\" onmouseup=\"toggleOff();\">%s</a>\n" % (id, but_inc)
	    ostr += "<a onmousedown=\"toggleOnSel('%s', 1);\" onmouseup=\"toggleOff();\">%s</a>\n" % (id, but_dec)
	    ostr += "<a onclick=\"settsel('%s');\">%s</a>\n" % (id, but_min)
	return ostr

    def FormatButtonInputVisibility(self, id, collapsed=False):
	if collapsed:
	    fname = 'expand'
	else:
	    fname = 'collapse'
	#image = self.ArtLoc('but_' + fname + '.gif')
	#hover = self.ArtLoc('hov_' + fname + '.gif')
	but_image = self.FindImageFile('but_' + fname, suffix='gif', art=True)
	hov_image = self.FindImageFile('hov_' + fname, suffix='gif', art=True)
	also = {'src' : '../' + but_image,
		'id' : id + '_l',
		'value' : fname,
		'onclick' : "toggle_visibility('%s','%s_l'); return false;" % (id, id),
		'class' : 'button',
		'onmouseover' : "this.src='../%s';" % hov_image,
		'onmouseout' : "this.src='../%s';" % but_image}
	return '<input type="image"%s>\n' % useful.Also(also)

    def FormatButtonInput(self, bname="submit", name=None, also={}):
	bname, but_image, hov_image = self.FindButtonImages(bname, pdir=self.art_dir)
	if not name:
	    name = bname

	inputname = name.replace(' ', '_').lower()
	altname = bname.replace('_', ' ').upper()
	imalso = {'class' : 'button' ,'alt' : altname}
	self.Comment('FormatButtonImage', bname, name, also, but_image, hov_image)
	if not but_image or not useful.IsGood(but_image, v=self.verbose):
	    imalso = {'class':'textbutton', 'onmouseover':"this.class='textbuttonh';", 'onmouseout':"this.class='textbutton';"}
	    return '<input type="submit" name="%s" value="%s"%s>\n' % (inputname, altname, useful.Also(imalso, also))
	elif not hov_image or not useful.IsGood(hov_image, v=self.verbose):
	    return '<input type="image" name="%s" src="../%s"%s>' % (inputname, but_image, useful.Also(imalso, also))
	else:
	    imalso.update({'onmouseover':"this.src='../%s';" % hov_image, 'onmouseout':"this.src='../%s';" % but_image})
	    return '<input type="image" name="%s" src="../%s"%s>' % (inputname, but_image, useful.Also(imalso, also))

    def FormatImageButton(self, name, image='', hover='', pdir=None, also={}):
	name, but_image, hov_image = self.FindButtonImages(name, image, hover, pdir)

	imalso = useful.DictMerge({'class': 'button'}, also)
	btn = ''
	if not but_image:
	    btn = '<span class="textbutton">%s</span>' % name
	elif not hov_image:
	    btn = self.FmtImgSrc(but_image, alt=name, also=imalso)
	else:
	    imalso.update({'onmouseover':"this.src='../%s';" % hov_image, 'onmouseout':"this.src='../%s';" % but_image})
	    btn = self.FmtImgSrc(but_image, alt=name, also=imalso)
	return btn

    def FormatButton(self, bname, link='', image='', args={}, also={}, lalso={}):
	#self.Comment('FormatButton', bname, link)
	#return self.FormatImageLink(bname.replace('_', ' ').upper(), 'but_' + bname.replace(' ', '_').lower(), 'hov_' + bname.replace(' ', '_').lower(), link, args, self.art_dir, also, lalso)
	btn = self.FormatImageButton(bname, image=image, pdir=self.art_dir, also=also)
	#self.Comment('Button image:', btn)
	if link:
	    btn = self.FormatLink(link, btn, args=args, also=lalso)
	return btn + '\n'

    def FormatButtonReset(self, name):
	return '<img ' + \
		'src="../' + self.art_dir + '/but_reset.gif" ' + \
		'onmouseover="this.src=\'../' + self.art_dir + '/hov_reset.gif\';" ' + \
		'onmouseout="this.src=\'../' + self.art_dir + '/but_reset.gif\';" ' + \
		'border="0" onClick="ResetForm(document.%s)" alt="RESET" class="button">' % name

    def FormatButtonComment(self, pif, args=None):
	if args:
	    args = 'page=%s&%s' % (pif.page_id, args)
	else:
	    args = 'page=%s' % pif.page_id
	ostr = self.FormatButton("comment_on_this_page", link='../pages/comment.php?%s' % args, also={'class' : 'comment'}, lalso=dict())
	if pif.IsAllowed('a'): # pragma: no cover
	    ostr += self.FormatButton("pictures", link="traverse.cgi?d=%s" % self.pic_dir, also={'class' : 'comment'}, lalso=dict())
	    ostr += self.FormatButton("edit_this_page", link=pif.dbh.GetEditorLink('page_info', {'id' : pif.page_id}), also={'class' : 'comment'}, lalso=dict())
	return ostr

    #---- images

    def FormatImageArt(self, fname, desc='', hspace=0, also={}):
	return self.FmtArt(fname, desc, hspace, also)

    def FormatImageFlag(self, code2, name='', hspace=0, also={}):
	return self.FmtOptImg(code2, alt=name, pdir=config.flagdir, also=useful.DictMerge({'hspace' : hspace}, also))

    def FormatImageAsLink(self, fnames, txt, pdir=None, also={}):
	return self.FormatLink('../' + self.FindImageFile(fnames, suffix=graphic_types, pdir=pdir), txt, also=also)

    def FormatImageOptional(self, fnames, alt=None, prefix='', suffix=None, pdir=None, also={}, vars=None, nopad=False):
	return self.FmtImg(fnames, alt=alt, prefix=prefix, suffix=suffix, pdir=pdir, also=also, vars=vars, pad=not nopad)

    def FormatImageRequired(self, fnames, alt=None, vars=None, nobase=False, prefix='', suffix=None, pdir=None, also={}, made=True):
	return self.FmtImg(fnames, alt=alt, vars=vars, nobase=nobase, prefix=prefix, suffix=suffix, pdir=pdir, also=also, made=made, required=True)

    def FormatImageList(self, fn, alt=None, wc='', prefix='', suffix='jpg', pdir=None):
	self.Comment('FormatImageList', fn, alt, wc, prefix, suffix, pdir)
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

		for fname in [orig] + useful.ReadDir(patt, pdir):
		    img = self.FmtImgSrc(pdir + '/' + fname, alt)
		    if img:
			imgs.append(img)
	return imgs

    def FormatImageSized(self, fnames, vars=None, nobase=False, largest='g', suffix=None, pdir=None, required=False):
	return self.FmtImg(fnames, alt='', vars=vars, nobase=nobase, suffix=suffix, largest=largest, pdir=pdir, required=required)

    #---- lower level rendering blocks

    def FmtPseudo(self, istr):
	if not istr:
	    return ''
	while 1:
	    mat = pseud_re.search(istr)
	    if not mat:
		break
	    if mat.group('cmd') == 'img':
		istr = istr[:mat.start()] + self.FmtOptImg(mat.group('arg')) + istr[mat.end():]
	    elif mat.group('cmd') == 'art':
		istr = istr[:mat.start()] + self.FmtArt(mat.group('arg'), also={'align':'absmiddle'}) + istr[mat.end():]
	    elif mat.group('cmd') == 'button':
		istr = istr[:mat.start()] + self.FormatButton(mat.group('arg')) + istr[mat.end():]
	return istr

    def FmtMarkup(self, cmd, args):
	carg = dict()
	for arg in reversed(args):
	    carg.update(arg)
	return '<' + cmd + useful.Also(args) + '>'

    def FmtArt(self, fname, desc='', hspace=0, also={}):
	return self.FmtImg(fname, alt=desc, pdir=self.art_dir, also=useful.DictMerge(also, {'hspace' : hspace}))

    def FmtImgSrc(self, pth, alt=None, also={}):
	if useful.IsGood(pth, v=self.verbose):
	    return '<img src="../' + pth + '"' + useful.Also({'alt':alt}, also) + '>'
	return ''

    def FmtImgCheck(self, pth):
	self.Comment("FmtImgCheck", pth)
	if useful.IsGood(pth, v=self.verbose):
	    return pth
	return ''

    def FmtImg(self, fnames, alt=None, vars=None, nobase=False, prefix='', suffix=None, pdir=None, largest=None, also={}, made=True, required=False, pad=False):
	img = self.FindImageFile(fnames, vars=vars, nobase=nobase, prefix=prefix, suffix=suffix, largest=largest, pdir=pdir)
	if img:
	    return self.FmtImgSrc(img, alt=alt, also=also)
	if required:
	    return self.FmtNoPic(made, prefix)
	if pad:
	    return '&nbsp;'
	return ''

    def FmtNoPic(self, made=True, prefix=''):
	# prefix not implemented yet!
	pic = {False : 'nopic.gif', True : 'notmade.gif'}[not made]
	return self.FmtArt(pic)

    def FmtOptImg(self, fnames, alt=None, prefix='', suffix=None, pdir=None, also={}, vars=None, nopad=False):
	return self.FmtImg(fnames, alt=alt, prefix=prefix, suffix=suffix, pdir=pdir, also=also, vars=vars, pad=not nopad)

    def FmtAnchor(self, name):
	if name:
	    return '<a name="%s"></a>\n' % name
	return ''

#    def FmtGraphics(self, graphics):
#	ostr = ''
#	for graf in graphics:
#	    ostr += self.FmtOptImg(graf['file'], alt=graf.get('name', ''), pdir=graf.get('pic_dir'), also=graf.get('also', {})) + '\n'
#	return ostr

    def FormatBulletList(self, descs):
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

    def FormatLineup(self, llineup):
	ostr = '<!-- Starting FormatLineup -->\n'
	maxes = {'s':0, 'r':0, 'e':0}
	self.CommentDict('lineup', llineup)
	if llineup.get('graphics'):
	    for graf in llineup['graphics']:
		ostr += self.FmtOptImg(graf, suffix='gif')
	lin_id = llineup.get('id', '')
	if llineup.get('note'):
	    ostr += llineup['note'] + '<br>'
	sc = 0
	for sec in llineup.get('section', []):
	    sc += 1
	    sec_id = sec.get('id', '')
	    ostr += self.FmtAnchor(sec.get('anchor'))
	    ncols = sec.get('columns', llineup.get('columns', 4))
	    if 'switch' in sec:
		#exval = {False:'expand', True:'collapse'}[sec['switch']]
		#ostr += '''<input id="%s_l" type="button" value="%s" onclick="toggle_visibility('%s','%s_l');">\n''' % (sec_id, exval, sec_id, sec_id)
		ostr += self.FormatButtonInputVisibility(sec_id, sec['switch'])
		ostr += sec.get('count', '')
	    ostr += self.FormatTableStart(style_id=lin_id)
	    if sec.get('name'):
		ostr += self.FormatSection(sec.get('name', ''), cols=ncols, id=sec['id'])
	    if sec.get('note'):
		ostr += self.FormatRowStart()
		also = {'colspan': ncols}
		also['class'] = self.StyleName(also.get('class'), 'sb', sec_id)
		ostr += self.FormatCell(0, sec['note'], also=also)
		ostr += self.FormatRowEnd()
	    ostr += self.FormatRowStart()
	    ostr += '<td>\n'
	    #ostr += self.FormatTableStart(id=sec_id, style_id=lin_id, also={'style':"border-width: 0; padding: 0;"})
	    rc = 0
	    for ran in sec.get('range', []):
		rc += 1
		ran_id = ran.get('id', '')
		ostr += self.FmtAnchor(ran.get('anchor'))
		if ran.get('name') or ran.get('graphics'):
		    ostr += self.FormatRange(ran.get('name', ''), None, ran.get('graphics', list()), cols=sec['columns'], id=ran.get('id', ''))
		if ran.get('note'):
		    ostr += self.FormatRowStart()
		    also = {'colspan': ncols}
		    also['class'] = self.StyleName(also.get('class'), 'rb', ran_id)
		    ostr += self.FormatCell(0, ran['note'], also=also)
		    ostr += self.FormatRowEnd()
		icol = 0
		spans = [[0, 0]] * ncols
		ec = 0
		for ent in ran.get('entry', []):
		    ec += 1
		    if icol == 0:
			ostr += self.FormatRowStart(also={'class' : 'er'})
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
			    ostr += self.FormatRowEnd()
			    icol = 0
			    ostr += self.FormatRowStart(also={'class' : 'er'})
		    if ent.get('rowspan') or ent.get('colspan'):
			spans[icol] = [ent.get('colspan', 1), ent.get('rowspan', 1) - 1]
			also.update({'rowspan' : ent.get('rowspan', 1), 'colspan' : ent.get('colspan', 1)})
			also['width'] = '%d%%' % (int(ent.get('colspan', 1)) * 100 / ncols)
		    if ent.get('also'):
			also.update(ent['also'])
		    if not 'width' in also:
			also['width'] = '%d%%' % (100/ncols)
		    ostr += self.FormatCell(disp_id, ent['text'], also=also)
		    icol += ent.get('colspan', 1)
		    if icol >= ncols:
			ostr += self.FormatRowEnd()
			icol = 0
		    maxes['e'] = max(maxes['e'], ec)
		if icol:
		    ostr += self.FormatRowEnd()
		maxes['r'] = max(maxes['r'], rc)
	    #ostr += self.FormatTableEnd()
	    ostr += self.FormatCellEnd()
	    ostr += self.FormatRowEnd()
	    ostr += self.FormatTableEnd()
	    maxes['s'] = max(maxes['s'], sc)
	#print 'sec %(s)d ran %(r)d ent %(e)d<br>' % maxes
	ostr += self.FormatBoxTail(llineup.get('tail'))
	return ostr

    def FormatULLineup(self, llineup):
	ostr = '<!-- Starting FormatULLineup -->\n'
	if llineup.get('graphics'):
	    for graf in llineup['graphics']:
		ostr += self.FmtOptImg(graf, suffix='gif')
	lin_id = llineup.get('id', '')
	if llineup.get('note'):
	    ostr += llineup['note'] + '<br>'
	for sec in llineup.get('section', []):
	    salso = dict()
	    sec_id = sec.get('id', '')
	    ostr += self.FmtAnchor(sec.get('anchor'))
	    ncols = sec.get('columns', llineup.get('columns', 4))
	    if 'switch' in sec:
		ostr += self.FormatButtonInputVisibility(sec_id, sec['switch'])
		ostr += sec.get('count', '')
	    if sec.get('name'):
		ostr += self.FormatSectionFreestanding(sec.get('name', ''), cols=ncols, id=sec['id'])
	    if sec.get('note'):
		salso['class'] = self.StyleName(salso.get('class'), 'sb', sec_id)
		ostr += '<div%s>%s</div>' % (useful.Also(salso), sec['note'])
	    for ran in sec.get('range', []):
		ralso = dict()
		ran_id = ran.get('id', '')
		ostr += self.FmtAnchor(ran.get('anchor'))
#		if ran.get('name') or ran.get('graphics'):
#		    ostr += self.FormatRange(ran.get('name', ''), None, ran.get('graphics', list()), cols=sec['columns'], id=ran.get('id', ''))
		if ran.get('name'):
		    ralso['class'] = self.StyleName(ralso.get('class'), 'rh', ran_id)
		    ostr += '<div%s>%s</div>\n' % (useful.Also(ralso), ran['name'])
		if ran.get('note'):
		    #ralso['class'] = self.StyleName(ralso.get('class'), 'rb', ran_id)
		    ostr += '<div%s>%s</div>\n' % (useful.Also({'class':'rb ' + ran_id}), ran['note'])
		ostr += '<ul%s>\n' % useful.Also(ralso)
		for ent in ran.get('entry', []):
		    disp_id = ent.get('display_id')
		    if not disp_id:
			disp_id = ran_id
		    ealso = {'class': self.StyleName(ent.get('class'), 'eb')}
		    if ent.get('style'):
			ealso['style'] = ent['style']
		    if ent.get('also'):
			ealso.update(ent['also'])
		    if not 'width' in ealso:
			ealso['width'] = '%d%%' % (100/ncols)
		    ostr += '<li%s>%s</li>\n' % (useful.Also(ealso), ent['text'])
		ostr += '</ul>\n'
	ostr += self.FormatBoxTail(llineup.get('tail'))
	return ostr

    def FormatBoxTail(self, tail):
	if not tail:
	    return ''
	ostr = self.FormatTableStart(style_id="tail")
	ostr += self.FormatRowStart()
	if not isinstance(tail, list):
	    tail = [tail]
	ntail = 1
	for tent in tail:
	    ostr += self.FormatCell("tail_%s" % ntail, tent)
	    ntail += 1
	ostr += self.FormatRowEnd()
	ostr += self.FormatTableEnd()
	return ostr

    def FormatLinks(self, llineup):
	ostr = llineup.get('name', '') + '\n'
	lin_id = llineup.get('id', '')
	for sec in llineup.get('section', []):
	    sec_id = sec.get('id', '')
	    self.FmtAnchor(sec.get('anchor'))
	    if sec.get('name'):
		ostr += '<h3>' + sec.get('name', '') + '</h3><p>'
	    if sec.get('note'):
		ostr += sec['note'] + '<br>'
	    for ran in sec.get('range', []):
		ran_id = ran.get('id', '')
		self.FmtAnchor(ran.get('anchor'))
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
			ostr += self.FormatLink('?id=%d' % ent['id'], self.FormatImageArt('comment'))
		    if ent.get('linktype'):
			ostr += self.FormatImageArt(ent['linktype'], also={'class':'bullet'})
		    ostr += ent['text']
		    if ent['large']:
			ostr += '</div>\n'
			ostr += '<div class="link-desc">\n'
		    ostr += '<br>'.join(ent['desc'])
		    ostr += '</div>\n'
	return ostr


#---- -------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''

