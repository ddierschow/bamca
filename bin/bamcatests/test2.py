import os
import unittest

import basics
import config


class TestRender(unittest.TestCase):

    def assertOut(self, result):
        self.assertNotEqual(result, '')

    def setUp(self):
        os.putenv('LOG_LEVEL', 'CRITICAL')
        self.pif = basics.get_page_info('matrix.matchcaps', args="verbose=0")
        self.pif.ren.verbose = True
        self.pif.ren.verbose = False

    def test_print_html(self):
        self.pif.ren.verbose = True
        self.assertIsNone(self.pif.ren.comment('foo'))
        self.pif.ren.verbose = False
        self.assertIsNone(self.pif.ren.print_html())

    def teststr(self):
        self.assertOut(str(self.pif.ren))

    def test_error_report(self):
        self.assertOut(self.pif.ren.error_report())

    def test_style_name1(self):
        self.assertOut(self.pif.ren.style_name('name', 'eb'))

    def test_style_name2(self):
        self.assertOut(self.pif.ren.style_name('name', 'eb', '1'))

    def test_style_name3(self):
        self.assertOut(self.pif.ren.style_name('name', 'eb', id='foo'))

    def test_style_name4(self):
        self.assertOut(self.pif.ren.style_name('name', 'eb', '1', id='foo'))

    def test_show_location(self):
        self.pif.ren.hierarchy_append('/', 'Home')
        self.assertOut(self.pif.ren.show_location())

    def test_get_flags(self):
        self.assertTrue(isinstance(self.pif.ren.get_flags(), dict))

    def test_show_flag(self):
        self.assertOut(self.pif.ren.show_flag('US'))

    def test_find_image_file01(self):
        self.assertEqual(self.pif.ren.find_image_file(
            '', vars=None, prefix='', largest='l', pdir=config.IMG_DIR_MAN), ('', ''))

    def test_find_image_file02(self):
        self.assertNotEqual(self.pif.ren.find_image_file(
            'mb001', vars=None, prefix='', largest='l', pdir=config.IMG_DIR_MAN), ('', ''))

    def test_find_image_file03(self):
        self.assertNotEqual(self.pif.ren.find_image_file('bamca', vars=None, prefix='', art=True), ('', ''))

    def test_find_image_file04(self):
        self.assertNotEqual(self.pif.ren.find_image_file('BAMCA', vars=None, prefix='', art=True), ('', ''))

    def test_find_image_file05(self):
        self.assertEqual(self.pif.ren.find_image_file('bamca', vars=None, prefix=''), ('', ''))

    def test_find_image_file06(self):
        self.assertEqual(self.pif.ren.find_image_file('bamca.gif', vars=None, prefix=''), ('', ''))

    def test_find_image_file07(self):
        self.assertNotEqual(self.pif.ren.find_image_file(
            'MB001', vars='03', prefix='s', pdir=config.IMG_DIR_MAN), ('', ''))

    def test_find_image_file08(self):
        self.assertNotEqual(self.pif.ren.find_image_file(
            'mb001', vars='03', nobase=True, prefix='s', pdir=config.IMG_DIR_MAN), ('', ''))

    def test_find_image_file09(self):
        self.assertNotEqual(self.pif.ren.find_image_file(
            'mb001', vars=['03'], prefix='s', pdir=config.IMG_DIR_MAN), ('', ''))

    def test_find_image_file10(self):
        self.assertNotEqual(self.pif.ren.find_image_file(
            'mb001', vars=['03'], nobase=True, prefix='s', pdir=config.IMG_DIR_MAN), ('', ''))

    def test_comment(self):
        self.assertIsNone(self.pif.ren.comment('unittest'))
        self.pif.ren.verbose = True
        self.assertIsNone(self.pif.ren.comment('unittest'))
        self.pif.ren.verbose = False

    def test_comment_dict(self):
        self.assertIsNone(self.pif.ren.comment_dict('a', {1: 2}))
        self.pif.ren.verbose = True
        self.assertIsNone(self.pif.ren.comment_dict('a', {1: 2}))
        self.pif.ren.verbose = False

    def test_format_head(self):
        self.assertOut(self.pif.ren.format_head())
        self.pif.ren.isbeta = True
        self.assertOut(self.pif.ren.format_head())
        self.pif.ren.isbeta = False

    def test_format_tail1(self):
        self.assertOut(self.pif.ren.format_tail())

    def test_format_tail2(self):
        self.pif.ren.isbeta = True
        self.pif.ren.tail['moreinfo'] = 1
        self.pif.ren.tail['contact'] = 1
        self.pif.ren.tail['disclaimer'] = 1
        self.pif.ren.tail['flags'] = 1
        self.assertOut(self.pif.ren.format_tail())
        self.pif.ren.isbeta = False

    def test_format_table_start(self):
        pass  # self.assertOut(self.pif.ren.format_table_start(also={}, id='', style_id=''))

    def test_format_table_end(self):
        pass  # self.assertOut(self.pif.ren.format_table_end())

    def test_format_row_start(self):
        pass  # self.assertOut(self.pif.ren.format_row_start(ids=[], also={}))

    def test_format_row_end(self):
        pass  # self.assertOut(self.pif.ren.format_row_end())

    def test_format_cell(self):
        pass  # self.assertOut(self.pif.ren.format_cell(col=1, content="x", hdr=False, also={}, large=False, id=''))

    def test_format_cell_start(self):
        pass  # self.assertOut(self.pif.ren.format_cell_start(col=None, hdr=False, also={}, large=False, id=''))

    def test_format_cell_end(self):
        pass  # self.assertOut(self.pif.ren.format_cell_end(col=0, hdr=False, large=False))

    def test_format_link(self):
        self.assertNotEqual(self.pif.ren.format_link(
            '.?z=1', '.', args={'a': '1'}, nstyle={'class': 'foo'}, also={}), '')
        self.assertOut(self.pif.ren.format_link('.', '.', args={'a': '1'}, nstyle={'class': 'foo'}, also={}))
        self.assertOut(self.pif.ren.format_link('.', '', args={'a': '1'}, nstyle={'class': 'foo'}, also={}))
        self.assertOut(self.pif.ren.format_link('', '.', args={'a': '1'}, nstyle={'class': 'foo'}, also={}))
        self.assertOut(self.pif.ren.format_link('', '.', args={'a': '1'}, nstyle={'class': 'foo'}, also={'a': '1'}))

    def test_format_checkbox(self):
        self.assertOut(self.pif.form.put_checkbox('foo', options=[('1', '1')], checked=[]))

    def test_format_radio(self):
        self.assertOut(self.pif.form.put_radio('bar', options=[('2', '2')], checked='', sep=''))

    def test_format_select(self):
        self.assertOut(self.pif.form.put_select('baz', options=['3'], selected='3', id='a'))

    def test_format_text_input(self):
        self.assertOut(self.pif.form.put_text_input('asdf', 10))
        self.assertOut(self.pif.form.put_text_input('asdf', maxlength=80, showlength=24, value='val'))

    def test_format_password_input(self):
        self.assertOut(self.pif.form.put_password_input('pass', maxlength=80, showlength=24, value=''))

    def test_format_hidden_input(self):
        self.assertOut(self.pif.form.put_hidden_input({'1': '2', '3': '4'}))
        self.assertOut(self.pif.form.put_hidden_input(a='2', c='4'))

    def test_format_button_up_down(self):
        self.assertOut(self.pif.form.put_button_up_down('updn'))

    def test_format_button_up_down_select(self):
        self.assertOut(self.pif.form.put_button_up_down_select('updn', vl=1))
        self.assertOut(self.pif.form.put_button_up_down_select('updn', vl=-1))

    def test_format_button_input_visibility(self):
        self.assertOut(self.pif.form.put_button_input_visibility('updn', collapsed=False))
        self.assertOut(self.pif.form.put_button_input_visibility('updn', collapsed=True))

    def test_format_button_input(self):
        self.assertOut(self.pif.form.put_button_input(bname="submit", also={}))
        self.assertOut(self.pif.form.put_button_input(bname="see the models", also={}))
        self.assertOut(self.pif.form.put_button_input(bname="unittest", name="no really", also={}))

    def test_format_text_button(self):
        self.assertOut(self.pif.form.put_text_button('see the models', also={}))
        self.assertOut(self.pif.form.put_text_button("submit", also={}))
        self.assertOut(self.pif.form.put_text_button("unittest", also={}))
        self.assertOut(self.pif.form.put_text_button("yodel", also={}))

    def test_format_button(self):
        self.assertOut(self.pif.ren.format_button_link('pictures', '', image='', args={}, also={}, lalso={}))

    def test_format_button_reset(self):
        self.assertOut(self.pif.form.put_button_reset('thing'))

    # def test_set_button_comment(self):
    #     self.pif.ren.set_button_comment(self.pif, args=None)
    #     self.assertTrue(self.pif.ren.footer != '')
    #     self.pif.ren.set_button_comment(self.pif, args={'a': 1})
    #     self.assertTrue(self.pif.ren.footer != '')

    def test_format_image_art(self):
        pass  # self.assertOut(self.pif.ren.format_image_art('bamca', desc='', hspace=0, also={}))

    def test_format_image_flag(self):
        pass  # self.assertOut(self.pif.ren.format_image_flag('SE', name='', hspace=0, also={}))

    def test_format_image_as_link(self):
        self.assertOut(self.pif.ren.format_image_as_link('bamca', 'bamca logo', pdir=None, also={}))

    def test_format_image_optional(self):
        self.assertNotEqual(self.pif.ren.format_image_optional(
            'cs-13', alt=None, prefix='', suffix=None, pdir=None, also={}, vars=None, nopad=False), '')

    def test_format_image_required(self):
        self.assertNotEqual(self.pif.ren.format_image_required(
            'foo', alt=None, vars=None, prefix='', suffix=None, pdir=None, also={}, made=True), '')

    def test_format_image_list(self):
        self.assertNotEqual(self.pif.ren.format_image_list(
            'c*', alt=None, wc='', prefix='', suffix='jpg', pdir=None), '')

    def test_format_image_sized(self):
        self.assertNotEqual(self.pif.ren.format_image_sized(
            'mb002', vars=None, largest='g', suffix=None, pdir=config.IMG_DIR_MAN, required=False), '')

    def test_fmt_pseudo(self):
        self.assertOut(self.pif.ren.fmt_pseudo('stuff <$img foo>'))
        self.assertOut(self.pif.ren.fmt_pseudo('stuff <$art foo>'))
        self.assertOut(self.pif.ren.fmt_pseudo('stuff <$button foo>'))

    def test_fmt_markup(self):
        pass  # self.assertOut(self.pif.ren.fmt_markup('a', [{'b': 'c'}]))

    def test_fmt_art(self):
        self.assertOut(self.pif.ren.fmt_art('bamca', desc='', prefix='', also={}))

    def test_fmt_img_src(self):
        self.assertOut(self.pif.ren.fmt_img_src('pic/gfx/bamca.gif', alt=None, also={}))

    def test_fmt_img_check(self):
        pass  # self.assertOut(self.pif.ren.fmt_img_check('foo'))

    def test_fmt_img(self):
        self.pif.ren.verbose = True
        self.pif.ren.verbose = False
        self.assertNotEqual(self.pif.ren.fmt_img(
            'mb003', alt=None, vars=None, prefix='s', suffix=None, pdir=config.IMG_DIR_MAN, largest=None, also={},
            made=True, required=False, pad=False), '')

    def test_fmt_no_pic(self):
        self.assertOut(self.pif.ren.fmt_no_pic(made=True, prefix=''))

    def test_fmt_opt_img(self):
        self.assertNotEqual(self.pif.ren.fmt_opt_img(
            'mb004', alt=None, prefix='s', suffix=None, pdir=config.IMG_DIR_MAN, also={}, vars=None, nopad=False), '')

    def test_fmt_anchor(self):
        self.assertOut(self.pif.ren.fmt_anchor('a'))
        self.assertEqual(self.pif.ren.fmt_anchor(''), '')

    def test_clear_cookie(self):
        self.assertOut(self.pif.ren.secure.clear_cookie(keys=[]))

    def test_cookie_domain(self):
        pass  # self.assertOut(self.pif.ren.secure.cookie_domain())

    def test_make_cookie(self):
        pass  # self.assertOut(self.pif.ren.secure.make_cookie(id, privs, expires=6000))

    def test_get_cookies(self):
        self.assertOut(self.pif.ren.secure.get_cookies())


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
