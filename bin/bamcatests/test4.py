import unittest
import useful


class TestUseful(unittest.TestCase):

    def setUp(self):
        import os
        os.putenv('SERVER_NAME', 'www.bamca.org')

    def test_form_int(self):
        pass  # self.assertEqual(useful.form_int('', 0), '0')
        pass  # self.assertEqual(useful.form_int(0, 0), '0')

    def test_read_dir(self):
        pass  # self.assertEqual(useful.read_dir(patt, tdir), '')

    def test_root_ext(self):
        self.assertEqual(useful.root_ext('foo'), ('foo', ''))
        self.assertEqual(useful.root_ext('foo.bar'), ('foo', 'bar'))

    def test_clean_name(self):
        pass  # self.assertEqual(useful.clean_name(f, morebad=''), '')

    def test_is_good(self):
        pass  # self.assertEqual(useful.is_good(fname, v=Equal), '')

    def test_render(self):
        pass  # self.assertEqual(useful.render(fname), '')

    def test_img_src(self):
        pass  # self.assertEqual(useful.img_src(pth, alt=None, also={}), '')

    def test_plural(self):
        pass  # self.assertEqual(useful.plural(thing), '')

    def test_dump_dict_comment(self):
        pass  # self.assertEqual(useful.dump_dict_comment(t, d, keys={}), '')

    def test_dump_dict(self):
        pass  # self.assertEqual(useful.dump_dict(t, d, keys={}), '')

    def test_also(self):
        pass  # self.assertEqual(useful.also(also={}, style={}), '')

    def test_dict_merge(self):
        pass  # self.assertEqual(useful.dict_merge(*dicts), '')

    def test_set_and_add_list(self):
        pass  # self.assertEqual(useful.set_and_add_list(d, k, l), '')

    def test_any_char_match(self):
        pass  # self.assertEqual(useful.any_char_match(t1, t2), '')

    def test_bit_list(self):
        pass  # self.assertEqual(useful.bit_list(val, format="%02x"), '')

    def test_search_match(self):
        pass  # self.assertEqual(useful.search_match(sobj, targ), '')

    def test_file_mover(self):
        pass  # self.assertEqual(useful.file_mover(src, dst, mv=False, ov=False, inc=False, trash=False), '')

    def test_file_move(self):
        pass  # self.assertEqual(useful.file_move(src, dst, ov=False, trash=False), '')

    def test_file_delete(self):
        pass  # self.assertEqual(useful.file_delete(src, trash=False), '')

    def test_file_copy(self):
        pass  # self.assertEqual(useful.file_copy(src, dst, trash=False), '')

    def test_header_done(self):
        pass  # self.assertEqual(useful.header_done(), '')

    def test_write_comment(self):
        pass  # self.assertEqual(useful.write_comment(*args), '')


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
