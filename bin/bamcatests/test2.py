import unittest
import basics
import config

class TestRender(unittest.TestCase):

    def setUp(self):
	self.pif = basics.get_page_info('matrix.matchcaps', args="verbose=0")
	self.pif.render.verbose = True
	self.pif.render.verbose = False

    def test_print_html(self):
	self.pif.render.verbose = True
	self.assertTrue(self.pif.render.comment('foo') == None)
	self.pif.render.verbose = False
	self.assertTrue(self.pif.render.print_html() == None)

    def test_table(self):
	table = self.pif.render.create_table()
	self.assertTrue(table != None)
	self.assertTrue(table.row() == None)
	self.assertTrue(table.cell(0, 'foo') == None)
	self.assertTrue(table.render() != '')

    def test_FormatTable(self):
	self.assertTrue(self.pif.render.format_table(
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

    def test_format_table_single_cell(self):
	self.assertTrue(self.pif.render.format_table_single_cell(0, content='stuff', talso={}, ralso={}, calso={}, id='ut', hdr=False) != '')

    def teststr(self):
	self.assertTrue(str(self.pif.render) != '')

    def test_error_report(self):
	self.assertTrue(self.pif.render.error_report() != '')

    def test_style_name1(self):
	self.assertTrue(self.pif.render.style_name('name', 'eb') != '')

    def test_style_name2(self):
	self.assertTrue(self.pif.render.style_name('name', 'eb', '1') != '')

    def test_style_name3(self):
	self.assertTrue(self.pif.render.style_name('name', 'eb', id='foo') != '')

    def test_style_name4(self):
	self.assertTrue(self.pif.render.style_name('name', 'eb', '1', id='foo') != '')

    def test_show_location(self):
	self.pif.render.hierarchy_append('/', 'Home')
	self.assertTrue(self.pif.render.show_location() != '')

    def test_get_flags(self):
	self.assertTrue(type(self.pif.render.get_flags()) == dict)

    def test_show_flag(self):
	self.assertTrue(self.pif.render.show_flag('US') != '')

    def test_find_art(self):
	self.assertTrue(self.pif.render.find_art('bamca') != '')

    def test_find_image_file01(self):
	self.assertTrue(self.pif.render.find_image_file('', vars=None, prefix='', largest='l', pdir=config.IMG_DIR_MAN) == '')

    def test_find_image_file02(self):
	self.assertTrue(self.pif.render.find_image_file('mb001', vars=None, prefix='', largest='l', pdir=config.IMG_DIR_MAN) != '')

    def test_find_image_file03(self):
	self.assertTrue(self.pif.render.find_image_file('bamca', vars=None, prefix='', art=True) != '')

    def test_find_image_file04(self):
	self.assertTrue(self.pif.render.find_image_file('BAMCA', vars=None, prefix='', art=True) != '')

    def test_find_image_file05(self):
	self.assertTrue(self.pif.render.find_image_file('bamca', vars=None, prefix='') == '')

    def test_find_image_file06(self):
	self.assertTrue(self.pif.render.find_image_file('bamca.gif', vars=None, prefix='') == '')

    def test_find_image_file07(self):
	self.assertTrue(self.pif.render.find_image_file('MB001', vars='03', prefix='s', pdir=config.IMG_DIR_MAN) != '')

    def test_find_image_file08(self):
	self.assertTrue(self.pif.render.find_image_file('mb001', vars='03', nobase=True, prefix='s', pdir=config.IMG_DIR_MAN) != '')

    def test_find_image_file09(self):
	self.assertTrue(self.pif.render.find_image_file('mb001', vars=['03'], prefix='s', pdir=config.IMG_DIR_MAN) != '')

    def test_find_image_file10(self):
	self.assertTrue(self.pif.render.find_image_file('mb001', vars=['03'], nobase=True, prefix='s', pdir=config.IMG_DIR_MAN) != '')

    def test_comment(self):
	self.assertTrue(self.pif.render.comment('unittest') == None)
	self.pif.render.verbose = True
	self.assertTrue(self.pif.render.comment('unittest') == None)
	self.pif.render.verbose = False

    def test_comment_dict(self):
	self.assertTrue(self.pif.render.comment_dict('a', {1:2}) == None)
	self.pif.render.verbose = True
	self.assertTrue(self.pif.render.comment_dict('a', {1:2}) == None)
	self.pif.render.verbose = False

    def test_format_head(self):
	self.assertTrue(self.pif.render.format_head() != '')
	self.pif.render.isbeta = True
	self.assertTrue(self.pif.render.format_head(extra='<!-- -->') != '')
	self.pif.render.isbeta = False

    def test_format_tail1(self):
	self.assertTrue(self.pif.render.format_tail() != '')

    def test_format_tail2(self):
	self.pif.render.isbeta = True
	self.pif.render.tail['moreinfo'] = 1
	self.pif.render.tail['contact'] = 1
	self.pif.render.tail['disclaimer'] = 1
	self.pif.render.tail['flags'] = 1
	self.assertTrue(self.pif.render.format_tail() != '')
	self.pif.render.isbeta = False

    def test_create_table(self):
	pass#self.assertTrue(self.pif.render.create_table(also={}, id='', style_id='') != '')

    def test_format_table_start(self):
	pass#self.assertTrue(self.pif.render.format_table_start(also={}, id='', style_id='') != '')

    def test_format_table_end(self):
	pass#self.assertTrue(self.pif.render.format_table_end() != '')

    def test_format_row_start(self):
	pass#self.assertTrue(self.pif.render.format_row_start(ids=[], also={}) != '')

    def test_format_row_end(self):
	pass#self.assertTrue(self.pif.render.format_row_end() != '')

    def test_format_cell(self):
	pass#self.assertTrue(self.pif.render.format_cell(col=None, content="&nbsp;", hdr=False, also={}, large=False, id='') != '')

    def test_format_cell_start(self):
	pass#self.assertTrue(self.pif.render.format_cell_start(col=None, hdr=False, also={}, large=False, id='') != '')

    def test_format_cell_end(self):
	pass#self.assertTrue(self.pif.render.format_cell_end(col=0, hdr=False, large=False) != '')

    def test_format_rows(self):
	pass#self.assertTrue(self.pif.render.format_rows(rows) != '')

    def test_format_cells(self):
	pass#self.assertTrue(self.pif.render.format_cells(cells) != '')

    def test_format_section(self):
	self.assertTrue(self.pif.render.format_section('sec') != '')
	self.assertTrue(self.pif.render.format_section('sec', fn='sw-1') != '')
	self.assertTrue(self.pif.render.format_section('sec', cols=2) != '')
	self.assertTrue(self.pif.render.format_section('sec', id='id') != '')

    def test_format_range(self):
	self.assertTrue(self.pif.render.format_range('cont', 1, fn=[], also={}, large=False, nstyle={'color':'black'}, cols=1, id='1') != '')
	self.assertTrue(self.pif.render.format_range('cont', 1, fn=['2'], also={}, large=False, nstyle=None, cols=2, id='') != '')
	self.assertTrue(self.pif.render.format_range('cont', 1, fn=['3'], also={}, large=True, nstyle=None, cols=3, id='') != '')
	self.assertTrue(self.pif.render.format_range('cont', 1, fn=['4'], also={}, large=False, nstyle=None, cols=4, id='') != '')

    def test_format_link(self):
	self.assertTrue(self.pif.render.format_link('.?z=1', '.', args={'a':'1'}, nstyle={'class':'foo'}, also={}) != '')
	self.assertTrue(self.pif.render.format_link('.', '.', args={'a':'1'}, nstyle={'class':'foo'}, also={}) != '')
	self.assertTrue(self.pif.render.format_link('.', '', args={'a':'1'}, nstyle={'class':'foo'}, also={}) != '')
	self.assertTrue(self.pif.render.format_link('', '.', args={'a':'1'}, nstyle={'class':'foo'}, also={}) != '')
	self.assertTrue(self.pif.render.format_link('', '.', args={'a':'1'}, nstyle={'class':'foo'}, also={'a':'1'}) != '')

    def test_format_checkbox(self):
	self.assertTrue(self.pif.render.format_checkbox('foo', options=[('1','1')], checked=[]) != '')

    def test_format_radio(self):
	self.assertTrue(self.pif.render.format_radio('bar', options=[('2', '2')], checked='', sep='') != '')

    def test_format_select(self):
	self.assertTrue(self.pif.render.format_select('baz', options=['3'], selected='3', id='a') != '')

    def test_format_text_input(self):
	self.assertTrue(self.pif.render.format_text_input('asdf', 10) != '')
	self.assertTrue(self.pif.render.format_text_input('asdf', maxlength=80, showlength=24, value='val') != '')

    def test_format_password_input(self):
	self.assertTrue(self.pif.render.format_password_input('pass', maxlength=80, showlength=24, value='') != '')

    def test_format_hidden_input(self):
	self.assertTrue(self.pif.render.format_hidden_input({'1':'2','3':'4'}) != '')

    def test_format_button_up_down(self):
	self.assertTrue(self.pif.render.format_button_up_down('updn') != '')

    def test_format_button_up_down_select(self):
	self.assertTrue(self.pif.render.format_button_up_down_select('updn', vl=1) != '')
	self.assertTrue(self.pif.render.format_button_up_down_select('updn', vl=-1) != '')

    def test_format_button_input_visibility(self):
	self.assertTrue(self.pif.render.format_button_input_visibility('updn', collapsed=False) != '')
	self.assertTrue(self.pif.render.format_button_input_visibility('updn', collapsed=True) != '')

    def test_format_button_input(self):
	self.assertTrue(self.pif.render.format_button_input(bname="submit", also={}) != '')
	self.assertTrue(self.pif.render.format_button_input(bname="unittest", also={}) != '')
	self.assertTrue(self.pif.render.format_button_input(bname="yodel", name="no really", also={}) != '')

    def test_find_button_images(self):
	self.assertTrue(self.pif.render.find_button_images('recalc', image='', hover='', pdir=None) != '')

    def test_format_image_button(self):
	self.assertTrue(self.pif.render.format_image_button('see the models', image='', hover='', pdir=None, also={}) != '')
	self.assertTrue(self.pif.render.format_image_button("submit", also={}) != '')
	self.assertTrue(self.pif.render.format_image_button("unittest", also={}) != '')
	self.assertTrue(self.pif.render.format_image_button("yodel", also={}) != '')

    def test_format_button(self):
	self.assertTrue(self.pif.render.format_button('pictures', link='', image='', args={}, also={}, lalso={}) != '')

    def test_format_button_reset(self):
	self.assertTrue(self.pif.render.format_button_reset('thing') != '')

    def test_format_button_comment(self):
	self.assertTrue(self.pif.render.format_button_comment(self.pif, args=None) != '')
	self.assertTrue(self.pif.render.format_button_comment(self.pif, args={'a':1}) != '')

    def test_format_image_art(self):
	pass#self.assertTrue(self.pif.render.format_image_art('bamca', desc='', hspace=0, also={}) != '')

    def test_format_image_flag(self):
	pass#self.assertTrue(self.pif.render.format_image_flag('SE', name='', hspace=0, also={}) != '')

    def test_format_image_as_link(self):
	self.assertTrue(self.pif.render.format_image_as_link('bamca', 'bamca logo', pdir=None, also={}) != '')

    def test_format_image_optional(self):
	self.assertTrue(self.pif.render.format_image_optional('cs-13', alt=None, prefix='', suffix=None, pdir=None, also={}, vars=None, nopad=False) != '')

    def test_format_image_required(self):
	self.assertTrue(self.pif.render.format_image_required('foo', alt=None, vars=None, prefix='', suffix=None, pdir=None, also={}, made=True) != '')

    def test_format_image_list(self):
	self.assertTrue(self.pif.render.format_image_list('c*', alt=None, wc='', prefix='', suffix='jpg', pdir=None) != '')

    def test_format_image_sized(self):
	self.assertTrue(self.pif.render.format_image_sized('mb002', vars=None, largest='g', suffix=None, pdir=config.IMG_DIR_MAN, required=False) != '')

    def test_fmt_pseudo(self):
	self.assertTrue(self.pif.render.fmt_pseudo('stuff <$img foo>') != '')
	self.assertTrue(self.pif.render.fmt_pseudo('stuff <$art foo>') != '')
	self.assertTrue(self.pif.render.fmt_pseudo('stuff <$button foo>') != '')

    def test_fmt_markup(self):
	pass#self.assertTrue(self.pif.render.fmt_markup('a', [{'b':'c'}]) != '')

    def test_fmt_art(self):
	self.assertTrue(self.pif.render.fmt_art('bamca', desc='', prefix='', also={}) != '')

    def test_fmt_img_src(self):
	self.assertTrue(self.pif.render.fmt_img_src('pic/gfx/bamca.gif', alt=None, also={}) != '')

    def test_fmt_img_check(self):
	pass#self.assertTrue(self.pif.render.fmt_img_check('foo') != '')

    def test_fmt_img(self):
	self.pif.render.verbose = True
	self.pif.render.verbose = False
	self.assertTrue(self.pif.render.fmt_img('mb003', alt=None, vars=None, prefix='s', suffix=None, pdir=config.IMG_DIR_MAN, largest=None, also={}, made=True, required=False, pad=False) != '')

    def test_fmt_no_pic(self):
	self.assertTrue(self.pif.render.fmt_no_pic(made=True, prefix='') != '')

    def test_fmt_opt_img(self):
	self.assertTrue(self.pif.render.fmt_opt_img('mb004', alt=None, prefix='s', suffix=None, pdir=config.IMG_DIR_MAN, also={}, vars=None, nopad=False) != '')

    def test_fmt_anchor(self):
	self.assertTrue(self.pif.render.fmt_anchor('a') != '')
	self.assertTrue(self.pif.render.fmt_anchor('') == '')

    def test_format_bullet_list(self):
	self.assertTrue(self.pif.render.format_bullet_list(['a', 'b', 'c']) != '')

    def test_format_matrix(self):
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
	self.assertTrue(self.pif.render.format_matrix(llineup) != '')

    def test_format_box_tail(self):
	self.assertTrue(self.pif.render.format_box_tail('tail') != '')

    def test_format_links(self):
	pass#self.assertTrue(self.pif.render.format_links(llineup) != '')

    def test_clear_cookie(self):
	self.assertTrue(self.pif.render.secure.clear_cookie(keys=[]) != '')

    def test_cookie_domain(self):
	pass#self.assertTrue(self.pif.render.secure.cookie_domain() != '')

    def test_make_cookie(self):
	pass#self.assertTrue(self.pif.render.secure.make_cookie(id, privs, expires=6000) != '')

    def test_get_cookies(self):
	self.assertTrue(self.pif.render.secure.get_cookies() != '')


if __name__ == '__main__': # pragma: no cover
    unittest.main()
