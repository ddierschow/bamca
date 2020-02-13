import unittest
import basics
import dbintf
import dbhand
import pifile
import render


class TestPIF(unittest.TestCase):

    def setUp(self):
        self.pif = basics.get_page_info('editor')

    def test_1(self):
        self.assertIsInstance(self.pif, pifile.PageInfoFile)

    def test_2(self):
        self.assertIsInstance(self.pif.render, render.Presentation)

    def test_2a(self):
        self.assertIsInstance(self.pif.dbh, dbhand.DBHandler)

    def test_2b(self):
        self.assertIsInstance(self.pif.dbh.dbi, dbintf.DB)

    def test_3(self):
        self.assertEqual(len(self.pif.dbh.fetch('page_info', where='not health=0', tag='unittest')), 0)

    def test_form_int(self):
        self.assertEqual(self.pif.form.get_int('a', defval=0), 0)

    # def test_Update(self):
    #     pass  # self.assertTrue(self.pif.Update(argfile)

    def test_is_allowed(self):
        self.assertFalse(self.pif.is_allowed('a'))

    def test_restrict(self):
        pass  # self.assertTrue(self.pif.restrict(priv)

    def test_error_report(self):
        self.assertNotEqual(self.pif.error_report(), '')

    def test_form_find(self):
        self.assertEqual(self.pif.form.find('b'), [])

    def test_get_form(self):
        pass  # self.assertEqual(self.pif.form.get_form(), {})

    def test_form_search(self):
        self.assertEqual(self.pif.form.search('a'), [])

    def test_show_error(self):
        self.assertIsNone(self.pif.show_error())

    def test_links(self):
        import tlinks
        listRejects, blacklist = tlinks.read_blacklist(self.pif)
        self.assertTrue(isinstance(listRejects, list))
        self.assertTrue(len(listRejects) > 0)
        self.assertTrue(isinstance(blacklist, list))
        self.assertTrue(len(blacklist) > 0)
        self.assertEqual(tlinks.is_blacklisted('nope', blacklist), '')
        self.assertEqual(tlinks.fix_url('a/b'), 'a/b')
        self.assertEqual(tlinks.fix_url('a/b/'), 'a/b')
        all_links, highest_disp_order = tlinks.read_all_links(self.pif)
        self.assertTrue(len(all_links) > 0)


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
