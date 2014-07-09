import unittest
import useful

class TestUseful(unittest.TestCase):

    def setUp(self):
	import os
	os.putenv('SERVER_NAME', 'www.bamca.org')

    def testFormInt(self):
	pass#self.assertTrue(useful.FormInt('', 0) == '0')
	pass#self.assertTrue(useful.FormInt(0, 0) == '0')

    def testReadDir(self):
	pass#self.assertTrue(useful.ReadDir(patt, tdir) == '')

    def testRootExt(self):
	self.assertTrue(useful.RootExt('foo') == ('foo',''))
	self.assertTrue(useful.RootExt('foo.bar') == ('foo','bar'))

    def testCleanName(self):
	pass#self.assertTrue(useful.CleanName(f, morebad='') == '')

    def testIsGood(self):
	pass#self.assertTrue(useful.IsGood(fname, v=True) == '')

    def testRender(self):
	pass#self.assertTrue(useful.Render(fname) == '')

    def testImgSrc(self):
	pass#self.assertTrue(useful.ImgSrc(pth, alt=None, also={}) == '')

    def testPlural(self):
	pass#self.assertTrue(useful.Plural(thing) == '')

    def testDumpDictComment(self):
	pass#self.assertTrue(useful.DumpDictComment(t, d, keys={}) == '')

    def testDumpDict(self):
	pass#self.assertTrue(useful.DumpDict(t, d, keys={}) == '')

    def testAlso(self):
	pass#self.assertTrue(useful.Also(also={}, style={}) == '')

    def testDictMerge(self):
	pass#self.assertTrue(useful.DictMerge(*dicts) == '')

    def testSetAndAddList(self):
	pass#self.assertTrue(useful.SetAndAddList(d, k, l) == '')

    def testAnyCharMatch(self):
	pass#self.assertTrue(useful.AnyCharMatch(t1, t2) == '')

    def testBitList(self):
	pass#self.assertTrue(useful.BitList(val, format="%02x") == '')

    def testSearchMatch(self):
	pass#self.assertTrue(useful.SearchMatch(sobj, targ) == '')

    def testFileMover(self):
	pass#self.assertTrue(useful.FileMover(src, dst, mv=False, ov=False, inc=False, trash=False) == '')

    def testFileMove(self):
	pass#self.assertTrue(useful.FileMove(src, dst, ov=False, trash=False) == '')

    def testFileDelete(self):
	pass#self.assertTrue(useful.FileDelete(src, trash=False) == '')

    def testFileCopy(self):
	pass#self.assertTrue(useful.FileCopy(src, dst, trash=False) == '')

    def testHeaderDone(self):
	pass#self.assertTrue(useful.HeaderDone() == '')

    def testWriteComment(self):
	pass#self.assertTrue(useful.WriteComment(*args) == '')


if __name__ == '__main__': # pragma: no cover
    unittest.main()
