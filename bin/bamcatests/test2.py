import unittest
import basics
import config
import db
import dbhandler
import pifile
import render

class TestRender(unittest.TestCase):

    def setUp(self):
	self.pif = basics.GetPageInfo('matrix.matchcaps', args="verbose=0")
	self.pif.render.verbose = True
	self.pif.render.verbose = False

    def testPrintHtml(self):
	self.pif.render.verbose = True
	self.assertTrue(self.pif.render.Comment('foo') == None)
	self.pif.render.verbose = False
	self.assertTrue(self.pif.render.PrintHtml() == None)

    def testtable(self):
	table = self.pif.render.CreateTable()
	self.assertTrue(table != None)
	self.assertTrue(table.row() == None)
	self.assertTrue(table.cell(0, 'foo') == None)
	self.assertTrue(table.render() != '')

    def testFormatTable(self):
	self.assertTrue(self.pif.render.FormatTable(
	    {'also':{'class':'table'}, 'id':'table', 'rows':[
		{'ids':[], 'also':{}, 'cells':[
		    {'col':None, 'content':"&nbsp;", 'hdr':True, 'also':{}, 'large':False, 'id':''}, 
		    {'col':None, 'content':"&nbsp;", 'hdr':True, 'also':{}, 'large':False, 'id':''}
		]}, 
		{'ids':['id'], 'also':{}, 'cells':[
		    {'col':None, 'content':"&nbsp;", 'hdr':False, 'also':{}, 'large':False, 'id':''}, 
		    {'col':None, 'content':"", 'hdr':False, 'also':{}, 'large':False, 'id':''}
		]}, 
		{'ids':['id'], 'also':{}, 'cells':[
		    {'col':None, 'content':"&nbsp;", 'hdr':False, 'also':{}, 'large':True, 'id':'1'}, 
		    {'col':None, 'content':"", 'hdr':False, 'also':{}, 'large':True, 'id':'2'}
		]}
	    ]}) != '')

    def testFormatTableSingleCell(self):
	self.assertTrue(self.pif.render.FormatTableSingleCell(0, content='stuff', talso={}, ralso={}, calso={}, id='ut', hdr=False) != '')

    def teststr(self):
	self.assertTrue(str(self.pif.render) != '')

    def testErrorReport(self):
	self.assertTrue(self.pif.render.ErrorReport() != '')

    def testStyleName1(self):
	self.assertTrue(self.pif.render.StyleName('name', 'eb') != '')

    def testStyleName2(self):
	self.assertTrue(self.pif.render.StyleName('name', 'eb', '1') != '')

    def testStyleName3(self):
	self.assertTrue(self.pif.render.StyleName('name', 'eb', id='foo') != '')

    def testStyleName4(self):
	self.assertTrue(self.pif.render.StyleName('name', 'eb', '1', id='foo') != '')

    def testShowLocation(self):
	self.pif.render.hierarchy.append(('/', 'Home'))
	self.assertTrue(self.pif.render.ShowLocation() != '')

    def testGetFlags(self):
	self.assertTrue(type(self.pif.render.GetFlags()) == dict)

    def testShowFlag(self):
	self.assertTrue(self.pif.render.ShowFlag('US') != '')

    def testFindArt(self):
	self.assertTrue(self.pif.render.FindArt('bamca') != '')

    def testFindImageFile01(self):
	self.assertTrue(self.pif.render.FindImageFile('', vars=None, prefix='', largest='l', pdir=config.imgdir175) == '')

    def testFindImageFile02(self):
	self.assertTrue(self.pif.render.FindImageFile('mb001', vars=None, prefix='', largest='l', pdir=config.imgdir175) != '')

    def testFindImageFile03(self):
	self.assertTrue(self.pif.render.FindImageFile('bamca', vars=None, prefix='', art=True) != '')

    def testFindImageFile04(self):
	self.assertTrue(self.pif.render.FindImageFile('BAMCA', vars=None, prefix='', art=True) != '')

    def testFindImageFile05(self):
	self.assertTrue(self.pif.render.FindImageFile('bamca', vars=None, prefix='') == '')

    def testFindImageFile06(self):
	self.assertTrue(self.pif.render.FindImageFile('bamca.gif', vars=None, prefix='') == '')

    def testFindImageFile07(self):
	self.assertTrue(self.pif.render.FindImageFile('MB001', vars='03', prefix='s', pdir=config.imgdir175) != '')

    def testFindImageFile08(self):
	self.assertTrue(self.pif.render.FindImageFile('mb001', vars='03', nobase=True, prefix='s', pdir=config.imgdir175) != '')

    def testFindImageFile09(self):
	self.assertTrue(self.pif.render.FindImageFile('mb001', vars=['03'], prefix='s', pdir=config.imgdir175) != '')

    def testFindImageFile10(self):
	self.assertTrue(self.pif.render.FindImageFile('mb001', vars=['03'], nobase=True, prefix='s', pdir=config.imgdir175) != '')

    def testComment(self):
	self.assertTrue(self.pif.render.Comment('unittest') == None)
	self.pif.render.verbose = True
	self.assertTrue(self.pif.render.Comment('unittest') == None)
	self.pif.render.verbose = False

    def testCommentDict(self):
	self.assertTrue(self.pif.render.CommentDict('a', {1:2}) == None)
	self.pif.render.verbose = True
	self.assertTrue(self.pif.render.CommentDict('a', {1:2}) == None)
	self.pif.render.verbose = False

    def testFormatHead(self):
	self.assertTrue(self.pif.render.FormatHead() != '')
	self.pif.render.isbeta = True
	self.assertTrue(self.pif.render.FormatHead(extra='<!-- -->') != '')
	self.pif.render.isbeta = False

    def testFormatTail1(self):
	self.assertTrue(self.pif.render.FormatTail() != '')

    def testFormatTail2(self):
	self.pif.render.isbeta = True
	self.pif.render.tail['moreinfo'] = 1
	self.pif.render.tail['contact'] = 1
	self.pif.render.tail['disclaimer'] = 1
	self.pif.render.tail['flags'] = 1
	self.assertTrue(self.pif.render.FormatTail() != '')
	self.pif.render.isbeta = False

    def testCreateTable(self):
	pass#self.assertTrue(self.pif.render.CreateTable(also={}, id='', style_id='') != '')

    def testFormatTableStart(self):
	pass#self.assertTrue(self.pif.render.FormatTableStart(also={}, id='', style_id='') != '')

    def testFormatTableEnd(self):
	pass#self.assertTrue(self.pif.render.FormatTableEnd() != '')

    def testFormatRowStart(self):
	pass#self.assertTrue(self.pif.render.FormatRowStart(ids=[], also={}) != '')

    def testFormatRowEnd(self):
	pass#self.assertTrue(self.pif.render.FormatRowEnd() != '')

    def testFormatCell(self):
	pass#self.assertTrue(self.pif.render.FormatCell(col=None, content="&nbsp;", hdr=False, also={}, large=False, id='') != '')

    def testFormatCellStart(self):
	pass#self.assertTrue(self.pif.render.FormatCellStart(col=None, hdr=False, also={}, large=False, id='') != '')

    def testFormatCellEnd(self):
	pass#self.assertTrue(self.pif.render.FormatCellEnd(col=0, hdr=False, large=False) != '')

    def testFormatRows(self):
	pass#self.assertTrue(self.pif.render.FormatRows(rows) != '')

    def testFormatCells(self):
	pass#self.assertTrue(self.pif.render.FormatCells(cells) != '')

    def testFormatSection(self):
	self.assertTrue(self.pif.render.FormatSection('sec') != '')
	self.assertTrue(self.pif.render.FormatSection('sec', fn='sw-1') != '')
	self.assertTrue(self.pif.render.FormatSection('sec', cols=2) != '')
	self.assertTrue(self.pif.render.FormatSection('sec', id='id') != '')

    def testFormatRange(self):
	self.assertTrue(self.pif.render.FormatRange('cont', 1, fn=[], also={}, large=False, nstyle={'color':'black'}, cols=1, id='1') != '')
	self.assertTrue(self.pif.render.FormatRange('cont', 1, fn=['2'], also={}, large=False, nstyle=None, cols=2, id='') != '')
	self.assertTrue(self.pif.render.FormatRange('cont', 1, fn=['3'], also={}, large=True, nstyle=None, cols=3, id='') != '')
	self.assertTrue(self.pif.render.FormatRange('cont', 1, fn=['4'], also={}, large=False, nstyle=None, cols=4, id='') != '')

    def testFormatLink(self):
	self.assertTrue(self.pif.render.FormatLink('.?z=1', '.', args={'a':'1'}, nstyle={'class':'foo'}, also={}) != '')
	self.assertTrue(self.pif.render.FormatLink('.', '.', args={'a':'1'}, nstyle={'class':'foo'}, also={}) != '')
	self.assertTrue(self.pif.render.FormatLink('.', '', args={'a':'1'}, nstyle={'class':'foo'}, also={}) != '')
	self.assertTrue(self.pif.render.FormatLink('', '.', args={'a':'1'}, nstyle={'class':'foo'}, also={}) != '')
	self.assertTrue(self.pif.render.FormatLink('', '.', args={'a':'1'}, nstyle={'class':'foo'}, also={'a':'1'}) != '')

    def testFormatCheckbox(self):
	self.assertTrue(self.pif.render.FormatCheckbox('foo', options=[('1','1')], checked=[]) != '')

    def testFormatRadio(self):
	self.assertTrue(self.pif.render.FormatRadio('bar', options=[('2', '2')], checked='', sep='') != '')

    def testFormatSelect(self):
	self.assertTrue(self.pif.render.FormatSelect('baz', options=['3'], selected='3', id='a') != '')

    def testFormatTextInput(self):
	self.assertTrue(self.pif.render.FormatTextInput('asdf', 10) != '')
	self.assertTrue(self.pif.render.FormatTextInput('asdf', maxlength=80, showlength=24, value='val') != '')

    def testFormatPasswordInput(self):
	self.assertTrue(self.pif.render.FormatPasswordInput('pass', maxlength=80, showlength=24, value='') != '')

    def testFormatHiddenInput(self):
	self.assertTrue(self.pif.render.FormatHiddenInput({'1':'2','3':'4'}) != '')

    def testFormatButtonUpDown(self):
	self.assertTrue(self.pif.render.FormatButtonUpDown('updn') != '')

    def testFormatButtonUpDownSelect(self):
	self.assertTrue(self.pif.render.FormatButtonUpDownSelect('updn', vl=1) != '')
	self.assertTrue(self.pif.render.FormatButtonUpDownSelect('updn', vl=-1) != '')

    def testFormatButtonInputVisibility(self):
	self.assertTrue(self.pif.render.FormatButtonInputVisibility('updn', collapsed=False) != '')
	self.assertTrue(self.pif.render.FormatButtonInputVisibility('updn', collapsed=True) != '')

    def testFormatButtonInput(self):
	self.assertTrue(self.pif.render.FormatButtonInput(bname="submit", also={}) != '')
	self.assertTrue(self.pif.render.FormatButtonInput(bname="unittest", also={}) != '')
	self.assertTrue(self.pif.render.FormatButtonInput(bname="yodel", name="no really", also={}) != '')

    def testFindButtonImages(self):
	self.assertTrue(self.pif.render.FindButtonImages('recalc', image='', hover='', pdir=None) != '')

    def testFormatImageButton(self):
	self.assertTrue(self.pif.render.FormatImageButton('see the models', image='', hover='', pdir=None, also={}) != '')
	self.assertTrue(self.pif.render.FormatImageButton("submit", also={}) != '')
	self.assertTrue(self.pif.render.FormatImageButton("unittest", also={}) != '')
	self.assertTrue(self.pif.render.FormatImageButton("yodel", also={}) != '')

    def testFormatButton(self):
	self.assertTrue(self.pif.render.FormatButton('pictures', link='', image='', args={}, also={}, lalso={}) != '')

    def testFormatButtonReset(self):
	self.assertTrue(self.pif.render.FormatButtonReset('thing') != '')

    def testFormatButtonComment(self):
	self.assertTrue(self.pif.render.FormatButtonComment(self.pif, args=None) != '')
	self.assertTrue(self.pif.render.FormatButtonComment(self.pif, args={'a':1}) != '')

    def testFormatImageArt(self):
	self.assertTrue(self.pif.render.FormatImageArt('bamca', desc='', hspace=0, also={}) != '')

    def testFormatImageFlag(self):
	self.assertTrue(self.pif.render.FormatImageFlag('SE', name='', hspace=0, also={}) != '')

    def testFormatImageAsLink(self):
	self.assertTrue(self.pif.render.FormatImageAsLink('bamca', 'bamca logo', pdir=None, also={}) != '')

    def testFormatImageOptional(self):
	self.assertTrue(self.pif.render.FormatImageOptional('cs-13', alt=None, prefix='', suffix=None, pdir=None, also={}, vars=None, nopad=False) != '')

    def testFormatImageRequired(self):
	self.assertTrue(self.pif.render.FormatImageRequired('foo', alt=None, vars=None, prefix='', suffix=None, pdir=None, also={}, made=True) != '')

    def testFormatImageList(self):
	self.assertTrue(self.pif.render.FormatImageList('c*', alt=None, wc='', prefix='', suffix='jpg', pdir=None) != '')

    def testFormatImageSized(self):
	self.assertTrue(self.pif.render.FormatImageSized('mb002', vars=None, largest='g', suffix=None, pdir=config.imgdir175, required=False) != '')

    def testFmtPseudo(self):
	self.assertTrue(self.pif.render.FmtPseudo('stuff <$img foo>') != '')
	self.assertTrue(self.pif.render.FmtPseudo('stuff <$art foo>') != '')
	self.assertTrue(self.pif.render.FmtPseudo('stuff <$button foo>') != '')

    def testFmtMarkup(self):
	pass#self.assertTrue(self.pif.render.FmtMarkup('a', [{'b':'c'}]) != '')

    def testFmtArt(self):
	self.assertTrue(self.pif.render.FmtArt('bamca', desc='', hspace=0, also={}) != '')

    def testFmtImgSrc(self):
	self.assertTrue(self.pif.render.FmtImgSrc('pic/gfx/bamca.gif', alt=None, also={}) != '')

    def testFmtImgCheck(self):
	pass#self.assertTrue(self.pif.render.FmtImgCheck('foo') != '')

    def testFmtImg(self):
	self.pif.render.verbose = True
	self.pif.render.verbose = False
	self.assertTrue(self.pif.render.FmtImg('mb003', alt=None, vars=None, prefix='s', suffix=None, pdir=config.imgdir175, largest=None, also={}, made=True, required=False, pad=False) != '')

    def testFmtNoPic(self):
	self.assertTrue(self.pif.render.FmtNoPic(made=True, prefix='') != '')

    def testFmtOptImg(self):
	self.assertTrue(self.pif.render.FmtOptImg('mb004', alt=None, prefix='s', suffix=None, pdir=config.imgdir175, also={}, vars=None, nopad=False) != '')

    def testFmtAnchor(self):
	self.assertTrue(self.pif.render.FmtAnchor('a') != '')
	self.assertTrue(self.pif.render.FmtAnchor('') == '')

    def testFormatBulletList(self):
	self.assertTrue(self.pif.render.FormatBulletList(['a', 'b', 'c']) != '')

    def testFormatLineup(self):
	# a lineup consists of a header (outside of the table) plus a set of sections, each in its own table.
	#     id, name, section, graphics, note, columns, tail
	# a section consists of a header (inside the table) plus a set of ranges.
	#     id, name, anchor, columns, note, range, switch, count
	# a range consists of a header plus a set of entries.
	#     id, name, anchor, note, graphics, entry, note
	# an entry contains the contents of a cell plus cell controls
	#     display_id, text, rowspan, colspan, class, st_suff, style, also,
	llineup = {'id':'a', 'name':'a', 'graphics':'a', 'note':'a', 'columns':1, 'tail':'a'}
	llineup['section'] = [{'id':'b', 'name':'b', 'anchor':'b', 'columns':1, 'note':'b', 'switch':'b', 'count':'b'}]
	llineup['section'][0]['range'] = [{'id':'c', 'name':'c', 'anchor':'c', 'note':'c', 'graphics':'c', 'note':'c'}]
	llineup['section'][0]['range'][0]['entry'] = [{'display_id':'', 'text':'d', 'rowspan':2, 'colspan':2, 'class':'d', 'st_suff':'d', 'style':'d', 'also':{}}]
	self.assertTrue(self.pif.render.FormatLineup(llineup) != '')

    def testFormatBoxTail(self):
	self.assertTrue(self.pif.render.FormatBoxTail('tail') != '')

    def testFormatLinks(self):
	pass#self.assertTrue(self.pif.render.FormatLinks(llineup) != '')

    def testClearCookie(self):
	self.assertTrue(self.pif.render.secure.ClearCookie(keys=[]) != '')

    def testCookieDomain(self):
	pass#self.assertTrue(self.pif.render.secure.CookieDomain() != '')

    def testMakeCookie(self):
	pass#self.assertTrue(self.pif.render.secure.MakeCookie(id, privs, expires=6000) != '')

    def testGetCookies(self):
	self.assertTrue(self.pif.render.secure.GetCookies() != '')


if __name__ == '__main__': # pragma: no cover
    unittest.main()
