import unittest
import basics

class TestRender(unittest.TestCase):

    def setUp(self):
	import os
	os.putenv('SERVER_NAME', 'www.bamca.org')

#    editor.EditorMain('editor')
#    editor.MassMain('editor')
#    editor.RoamMain('editor')
#    editor.ShowCounters('counter')

#    images.ImaWidget('editor')
#    images.PicturesMain('editor')
#    images.StitchMain('editor')
#    images.Tumblr('editor')
#    images.UploadMain('editor')

    def testL2(self):
	import lineup
	pif = basics.GetPageInfo('editor', args="verbose=0")
	self.assertTrue(lineup.TextMain(pif, 1991, 'U') != '')

    def testLineup(self):
	import lineup
        self.assertTrue(lineup.Main('year', 'year', args='verbose=0') != '')
        self.assertTrue(lineup.Main('year', 'year', args='year=1960 region=U hidden=1 submit=1') != '')
        self.assertTrue(lineup.Main('year', 'year', args='year=1971 region=U nyears=2 submit=1') != '')
        self.assertTrue(lineup.Main('year', 'year', args='year=1984 region=B submit=1') != '')
        self.assertTrue(lineup.Main('year', 'year', args='year=1988 region=D submit=1') != '')
        self.assertTrue(lineup.Main('year', 'year', args='year=1991 region=A submit=1') != '')
        self.assertTrue(lineup.Main('year', 'year', args='year=1997 region=L unroll=1 submit=1') != '')
        self.assertTrue(lineup.Main('year', 'year', args='year=1999 region=D large=1 submit=1') != '')
        self.assertTrue(lineup.Main('year', 'year', args='year=2000 region=A submit=1') != '')
        self.assertTrue(lineup.Main('year', 'year', args='year=2006 region=A unroll=1 hidden=1 submit=1') != '')
        self.assertTrue(lineup.Main('year', 'year', args='year=2013 region=U submit=1 verbose=1') != '')
	pif = basics.GetPageInfo('editor', args="verbose=0")
	#self.assertTrue(lineup.TextMain(pif) != '')
	self.assertTrue(lineup.PictureCount(pif, 'U', 2012) != None)
        self.assertTrue(lineup.MakesMain('makes', args='verbose=1') != '')
        self.assertTrue(lineup.MakesMain('makes', args='make=text text=austin submit=1') != '')
        self.assertTrue(lineup.MakesMain('makes', args='make=unk text=austin submit=1') != '')
        self.assertTrue(lineup.MakesMain('makes', args='make=unl text=austin submit=1') != '')
        self.assertTrue(lineup.MakesMain('makes', args='make=isu see_the_models=1') != '')
        self.assertTrue(lineup.MackLineup('mack', args='see_the_models=1 verbose=1') != '')
        self.assertTrue(lineup.FullLineup('mline', args='year=1960 CAT=1 E=1 RW=1 A=1 M=1 K=1 Y=1 MF=1 MG=1 PS=1 G=1 R=1 CC=1 PZL=1 GW=0 submit=1') != '')
        self.assertTrue(lineup.Main('year', 'year', args='n=1 num=5 syear=1971 region=U enum= eyear=1980 submit=1') != '')
        self.assertTrue(lineup.Main('year', 'year', args='n=1 num=5 syear=1971 region=U prodpic=1 enum=15 eyear=1980 submit=1') != '')

    def testLinks(self):
	import tlinks
        self.assertTrue(tlinks.Links('links', 'page', 'toylinks', args="verbose=1") != '')
        self.assertTrue(tlinks.Links('links', 'page', 'toylinks', args="page=clubs") != '')
        self.assertTrue(tlinks.Links('links', 'page', 'toylinks', args="page=dealers") != '')
        self.assertTrue(tlinks.Links('links', 'page', 'toylinks', args="page=mailorder") != '')
        self.assertTrue(tlinks.Links('links', 'page', 'toylinks', args="page=manuf") != '')
        self.assertTrue(tlinks.Links('links', 'page', 'toylinks', args="page=other") != '')
        self.assertTrue(tlinks.Links('links', 'page', 'toylinks', args="page=rejects") != '')
        self.assertTrue(tlinks.Links('links', 'page', 'toylinks', args="id=3") != '')
        self.assertTrue(tlinks.Links('links', 'page', 'toylinks', args="id=286") != '')
        self.assertTrue(tlinks.AddPage('addlink', args="verbose=0") != '')
#    tlinks.EditLinks('editor')

    def testManno(self):
	import mannum
        self.assertTrue(mannum.CompareMain('compare', args='verbose=1') != '')
        self.assertTrue(mannum.Main('manno', args='section=all listtype= range=all start=1 syear=1953 end=999 eyear=2015 type_a=y type_9=n type_o=m type_c=m type_b=m type_i=m type_2=m type_d=m type_e=m type_j=m type_1=m type_g=m type_r=m type_f=m type_4=m type_m=m type_u=m type_p=m type_z=m type_l=m type_t=m type_8=m type_v=m type_h=m type_5=m type_x=m submit=1') != '')
        self.assertTrue(mannum.Main('manno', args='section=wr listtype= range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(mannum.Main('manno', args='section=sf listtype= range=some start=5 syear=1972 end=9 eyear=1974 nodesc=1 submit=1') != '')
        self.assertTrue(mannum.Main('manno', args='section=wr listtype=adl range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(mannum.Main('manno', args='section=mi listtype=pxl range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(mannum.Main('manno', args='section=wr listtype=thm range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(mannum.Main('manno', args='section=wr listtype=ckl range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(mannum.Main('manno', args='section=wr listtype=vtl range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')

    def testMatrix(self):
	import matrix
	self.assertTrue(matrix.Main('matrix', 'page', args='page=character verbose=1') != '')
	self.assertTrue(matrix.Main('matrix', 'page', args='page=coll64') != '')
	self.assertTrue(matrix.Main('matrix', 'page', args='page=mbhc verbose=1') != '')
	self.assertTrue(matrix.Main('matrix', 'page', args='page=premiere') != '')
	self.assertTrue(matrix.Main('matrix', 'page', args='verbose=1') != '')

    def testMultipack(self):
	import multipack
	self.assertTrue(multipack.DoPage('packs', 'page', args="verbose=1") != '')
	self.assertTrue(multipack.DoPage('packs', 'page', args="page=5packs id=2000p55alu") != '')

    def testNontoy(self):
	import nontoy
	self.assertTrue(nontoy.ActivityMain('editor', args="verbose=1") != '')
	self.assertTrue(nontoy.Biblio('bib', 'page', 'biblio', args="verbose=1 simple=1") != '')
	self.assertTrue(nontoy.Biblio('bib', 'page', 'biblio', args="page=bayarea sort=1") != '')
	self.assertTrue(nontoy.Calendar('calendar', args="verbose=1") != '')
#    nontoy.Publication('pub')

    def testPackage(self):
	import package
	self.assertTrue(package.Blister('package', 'page', 'blister', args="verbose=1") != '')
#    package.Blister('package', 'page', 'blister')
#    package.ShowBoxes('boxart')

    def testSearch(self):
	import search
	self.assertTrue(search.RunSearch('search', args="query=austin submit=1") != '')
	self.assertTrue(search.RunSearch('search', args="id=MB700 submit=1") != '')
	self.assertTrue(search.RunSearch('search', args="id=MW800 submit=1") != '')
	self.assertTrue(search.RunSearch('search', args="id=MI705 submit=1") != '')
	self.assertTrue(search.RunSearch('search', args="id=MI205 submit=1") != '')
	self.assertTrue(search.RunSearch('search', args="id=801 submit=1") != '')
	self.assertTrue(search.RunSearch('search', args="id=SF01f submit=1") != '')
	self.assertTrue(search.RunSearch('search', args="id=LR02c submit=1") != '')
	self.assertTrue(search.RunSearch('search', args="id=LS03c submit=1") != '')
	self.assertTrue(search.RunSearch('search', args="id= submit=1") != '')
	self.assertTrue(search.RunSearch('search', args="submit=1") != '')

    def testSets(self):
	import mbsets
	self.assertTrue(mbsets.SetsMain('sets', 'page', args="verbose=1") != '')
	self.assertTrue(mbsets.SetsMain('sets', 'page', args="page=kings") != '')
	self.assertTrue(mbsets.SetsMain('sets', 'page', args="page=kings set=ks") != '')

    def testSingle(self):
	import single
	self.assertTrue(single.ShowSingle('single', args="verbose=1") != '')
	self.assertTrue(single.ShowSingle('single', args="id=MB001") != '')
	self.assertTrue(single.ShowSingle('single', args="id=RW01d") != '')
	self.assertTrue(single.ShowSingle('single', args="id=MB366 dir=pic/series pic=00l002 ref=matrix.mb2000 sub=") != '')
	self.assertTrue(single.ShowSingle('single', args="id=SF02b") != '')
	self.assertTrue(single.ShowSingle('single', args="id=MB700 dir=pic/mattel pic=2006u57 ref=year.2006 sub=") != '')
	self.assertTrue(single.ShowSingle('single', args="id=MB109") != '')

    def testTomica(self):
	import tomica
	self.assertTrue(tomica.Main('tomica', args="verbose=1") != '')

#    traverse.Main('editor')

#    user.ChangePasswordMain('user')
#    user.LogoutMain('user')

    def testVars(self):
	import vars
	self.assertTrue(vars.Main('vars', args="mod=MB786") != '')
	self.assertTrue(vars.Main('vars', args="mod=MB001 var=08") != '')
	self.assertTrue(vars.Main('vars', args="mod=MB320 var=06a") != '')
	self.assertTrue(vars.Main('vars', args="mod=SF75a list=1") != '')
	self.assertTrue(vars.Main('vars', args="mod=MB741 var=01") != '')
	self.assertTrue(vars.RunSearch('search', args="casting=austin codes=1 base= codes=2 body=green interior= wheels= windows= cat= submit=1") != '')

    def testVedit(self):
	import vedit
	self.assertTrue(vedit.HandleForm('vars', args="d=src/mbxf s=MW990 n=100") != '')
	self.assertTrue(vedit.HandleForm('vars', args="d=src/mbxf f=MW713") != '')

if __name__ == '__main__': # pragma: no cover
    unittest.main()
