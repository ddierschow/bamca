import unittest
import basics
import db
import dbhandler
import pifile
import render

class TestPIF(unittest.TestCase):

    def setUp(self):
	self.pif = basics.GetPageInfo('editor')

    def test_1(self):
        self.assertIsInstance(self.pif, pifile.PageInfoFile)

    def test_2(self):
        self.assertIsInstance(self.pif.render, render.Presentation)

    def test_2a(self):
        self.assertIsInstance(self.pif.dbh, dbhandler.dbhandler)

    def test_2b(self):
        self.assertIsInstance(self.pif.dbh.dbi, db.db)

    def test_3(self):
	self.assertTrue(len(self.pif.dbh.Fetch('page_info', where='not health=0', tag='unittest')) == 0)

    def testFormInt(self):
	self.assertTrue(self.pif.FormInt('a', defval=0) == 0)

#    def testUpdate(self):
#	pass#self.assertTrue(self.pif.Update(argfile)

    def testIsAllowed(self):
	self.assertTrue(self.pif.IsAllowed('a') == False)

    def testRestrict(self):
	pass#self.assertTrue(self.pif.Restrict(priv)

    def testDump(self):
	self.assertTrue(self.pif.Dump(True) == None)

    def testErrorReport(self):
	self.assertTrue(self.pif.ErrorReport() != '')

    def testFormFind(self):
	self.assertTrue(self.pif.FormFind('b') == [])

    def testGetForm(self):
	self.assertTrue(self.pif.GetForm() == {})

    def testGetSearch(self):
	self.assertTrue(self.pif.GetSearch('a') == [])

    def testShowError(self):
	self.assertTrue(self.pif.ShowError() == None)

    def testLinks(self):
	import links
	listRejects, blacklist = links.ReadBlacklist(self.pif)
	self.assertTrue(type(listRejects) == list)
	self.assertTrue(len(listRejects) > 0)
	self.assertTrue(type(blacklist) == list)
	self.assertTrue(len(blacklist) > 0)
        self.assertTrue(links.IsBlacklisted('nope', blacklist) == '')
        self.assertTrue(links.FixURL('a/b') == 'a/b')
        self.assertTrue(links.FixURL('a/b/') == 'a/b')
	all_links, highest_disp_order = links.ReadAllLinks(self.pif)
	self.assertTrue(len(all_links) > 0)



if __name__ == '__main__': # pragma: no cover
    unittest.main()
