import unittest
import basics
import config
import db
import dbhandler
import pifile
import render

class TestRender(unittest.TestCase):

    def setUp(self):
	import os
	os.putenv('SERVER_NAME', 'www.bamca.org')

#    basics.StartPage(editor.EditorMain, 'editor')
#    basics.StartPage(editor.MassMain, 'editor')
#    basics.StartPage(editor.RoamMain, 'editor')
#    basics.StartPage(editor.ShowCounters, 'counter')

#    basics.StartPage(images.ImaWidget, 'editor')
#    basics.StartPage(images.PicturesMain, 'editor')
#    basics.StartPage(images.StitchMain, 'editor')
#    basics.StartPage(images.Tumblr, 'editor')
#    basics.StartPage(images.UploadMain, 'editor')

    def testL2(self):
	import lineup
	pif = basics.GetPageInfo('editor', args="verbose=0")
	self.assertTrue(lineup.TextMain(pif, 1991, 'U') != '')

    def testLineup(self):
	import lineup
        self.assertTrue(basics.StartPage(lineup.Main, 'year', 'year', args='verbose=0') != '')
        self.assertTrue(basics.StartPage(lineup.Main, 'year', 'year', args='year=1960 region=U hidden=1 submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.Main, 'year', 'year', args='year=1971 region=U nyears=2 submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.Main, 'year', 'year', args='year=1984 region=B submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.Main, 'year', 'year', args='year=1988 region=D submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.Main, 'year', 'year', args='year=1991 region=A submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.Main, 'year', 'year', args='year=1997 region=L unroll=1 submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.Main, 'year', 'year', args='year=1999 region=D large=1 submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.Main, 'year', 'year', args='year=2000 region=A submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.Main, 'year', 'year', args='year=2006 region=A unroll=1 hidden=1 submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.Main, 'year', 'year', args='year=2013 region=U submit=1 verbose=1') != '')
	pif = basics.GetPageInfo('editor', args="verbose=0")
	#self.assertTrue(lineup.TextMain(pif) != '')
	self.assertTrue(lineup.PictureCount(pif, 'U', 2012) != None)
        self.assertTrue(basics.StartPage(lineup.MakesMain, 'makes', args='verbose=1') != '')
        self.assertTrue(basics.StartPage(lineup.MakesMain, 'makes', args='make=text text=austin submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.MakesMain, 'makes', args='make=unk text=austin submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.MakesMain, 'makes', args='make=unl text=austin submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.MakesMain, 'makes', args='make=isu see_the_models=1') != '')
        self.assertTrue(basics.StartPage(lineup.MackLineup, 'mack', args='see_the_models=1 verbose=1') != '')
        self.assertTrue(basics.StartPage(lineup.FullLineup, 'mline', args='year=1960 CAT=1 E=1 RW=1 A=1 M=1 K=1 Y=1 MF=1 MG=1 PS=1 G=1 R=1 CC=1 PZL=1 GW=0 submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.Main, 'year', 'year', args='n=1 num=5 syear=1971 region=U enum= eyear=1980 submit=1') != '')
        self.assertTrue(basics.StartPage(lineup.Main, 'year', 'year', args='n=1 num=5 syear=1971 region=U prodpic=1 enum=15 eyear=1980 submit=1') != '')

    def testLinks(self):
	import links
        self.assertTrue(basics.StartPage(links.Links, 'links', 'page', 'toylinks', args="verbose=1") != '')
        self.assertTrue(basics.StartPage(links.Links, 'links', 'page', 'toylinks', args="page=clubs") != '')
        self.assertTrue(basics.StartPage(links.Links, 'links', 'page', 'toylinks', args="page=dealers") != '')
        self.assertTrue(basics.StartPage(links.Links, 'links', 'page', 'toylinks', args="page=mailorder") != '')
        self.assertTrue(basics.StartPage(links.Links, 'links', 'page', 'toylinks', args="page=manuf") != '')
        self.assertTrue(basics.StartPage(links.Links, 'links', 'page', 'toylinks', args="page=other") != '')
        self.assertTrue(basics.StartPage(links.Links, 'links', 'page', 'toylinks', args="page=rejects") != '')
        self.assertTrue(basics.StartPage(links.Links, 'links', 'page', 'toylinks', args="id=3") != '')
        self.assertTrue(basics.StartPage(links.Links, 'links', 'page', 'toylinks', args="id=286") != '')
        self.assertTrue(basics.StartPage(links.AddPage, 'addlink', args="verbose=0") != '')
#    basics.StartPage(links.EditLinks, 'editor')

    def testManno(self):
	import manno
        self.assertTrue(basics.StartPage(manno.CompareMain, 'compare', args='verbose=1') != '')
        self.assertTrue(basics.StartPage(manno.Main, 'manno', args='section=all listtype= range=all start=1 syear=1953 end=999 eyear=2015 type_a=y type_9=n type_o=m type_c=m type_b=m type_i=m type_2=m type_d=m type_e=m type_j=m type_1=m type_g=m type_r=m type_f=m type_4=m type_m=m type_u=m type_p=m type_z=m type_l=m type_t=m type_8=m type_v=m type_h=m type_5=m type_x=m submit=1') != '')
        self.assertTrue(basics.StartPage(manno.Main, 'manno', args='section=wr listtype= range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(basics.StartPage(manno.Main, 'manno', args='section=sf listtype= range=some start=5 syear=1972 end=9 eyear=1974 nodesc=1 submit=1') != '')
        self.assertTrue(basics.StartPage(manno.Main, 'manno', args='section=wr listtype=adl range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(basics.StartPage(manno.Main, 'manno', args='section=mi listtype=pxl range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(basics.StartPage(manno.Main, 'manno', args='section=wr listtype=thm range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(basics.StartPage(manno.Main, 'manno', args='section=wr listtype=ckl range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(basics.StartPage(manno.Main, 'manno', args='section=wr listtype=vtl range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')

    def testMatrix(self):
	import matrix
	self.assertTrue(basics.StartPage(matrix.Main, 'matrix', 'page', args='page=character verbose=1') != '')
	self.assertTrue(basics.StartPage(matrix.Main, 'matrix', 'page', args='page=coll64') != '')
	self.assertTrue(basics.StartPage(matrix.Main, 'matrix', 'page', args='page=mbhc verbose=1') != '')
	self.assertTrue(basics.StartPage(matrix.Main, 'matrix', 'page', args='page=premiere') != '')
	self.assertTrue(basics.StartPage(matrix.Main, 'matrix', 'page', args='verbose=1') != '')

    def testMultipack(self):
	import multipack
	self.assertTrue(basics.StartPage(multipack.DoPage, 'packs', 'page', args="verbose=1") != '')
	self.assertTrue(basics.StartPage(multipack.DoPage, 'packs', 'page', args="page=5packs id=2000p55alu") != '')

    def testNontoy(self):
	import nontoy
	self.assertTrue(basics.StartPage(nontoy.ActivityMain, 'editor', args="verbose=1") != '')
	self.assertTrue(basics.StartPage(nontoy.Biblio, 'bib', 'page', 'biblio', args="verbose=1 simple=1") != '')
	self.assertTrue(basics.StartPage(nontoy.Biblio, 'bib', 'page', 'biblio', args="page=bayarea sort=1") != '')
	self.assertTrue(basics.StartPage(nontoy.Calendar, 'calendar', args="verbose=1") != '')
#    basics.StartPage(nontoy.Publication, 'pub')

    def testPackage(self):
	import package
	self.assertTrue(basics.StartPage(package.Blister, 'package', 'page', 'blister', args="verbose=1") != '')
#    basics.StartPage(package.Blister, 'package', 'page', 'blister')
#    basics.StartPage(package.ShowBoxes, 'boxart')

    def testSearch(self):
	import search
	self.assertTrue(basics.StartPage(search.RunSearch, 'search', args="query=austin submit=1") != '')
	self.assertTrue(basics.StartPage(search.RunSearch, 'search', args="id=MB700 submit=1") != '')
	self.assertTrue(basics.StartPage(search.RunSearch, 'search', args="id=MW800 submit=1") != '')
	self.assertTrue(basics.StartPage(search.RunSearch, 'search', args="id=MI705 submit=1") != '')
	self.assertTrue(basics.StartPage(search.RunSearch, 'search', args="id=MI205 submit=1") != '')
	self.assertTrue(basics.StartPage(search.RunSearch, 'search', args="id=801 submit=1") != '')
	self.assertTrue(basics.StartPage(search.RunSearch, 'search', args="id=SF01f submit=1") != '')
	self.assertTrue(basics.StartPage(search.RunSearch, 'search', args="id=LR02c submit=1") != '')
	self.assertTrue(basics.StartPage(search.RunSearch, 'search', args="id=LS03c submit=1") != '')
	self.assertTrue(basics.StartPage(search.RunSearch, 'search', args="id= submit=1") != '')
	self.assertTrue(basics.StartPage(search.RunSearch, 'search', args="submit=1") != '')

    def testSets(self):
	import msets
	self.assertTrue(basics.StartPage(msets.SetsMain, 'sets', 'page', args="verbose=1") != '')
	self.assertTrue(basics.StartPage(msets.SetsMain, 'sets', 'page', args="page=kings") != '')
	self.assertTrue(basics.StartPage(msets.SetsMain, 'sets', 'page', args="page=kings set=ks") != '')

    def testSingle(self):
	import single
	self.assertTrue(basics.StartPage(single.ShowSingle, 'single', args="verbose=1") != '')
	self.assertTrue(basics.StartPage(single.ShowSingle, 'single', args="id=MB001") != '')
	self.assertTrue(basics.StartPage(single.ShowSingle, 'single', args="id=RW01d") != '')
	self.assertTrue(basics.StartPage(single.ShowSingle, 'single', args="id=MB366 dir=pic/series pic=00l002 ref=matrix.mb2000 sub=") != '')
	self.assertTrue(basics.StartPage(single.ShowSingle, 'single', args="id=SF02b") != '')
	self.assertTrue(basics.StartPage(single.ShowSingle, 'single', args="id=MB700 dir=pic/mattel pic=2006u57 ref=year.2006 sub=") != '')
	self.assertTrue(basics.StartPage(single.ShowSingle, 'single', args="id=MB109") != '')

    def testTomica(self):
	import tomica
	self.assertTrue(basics.StartPage(tomica.Main, 'tomica', args="verbose=1") != '')

#    basics.StartPage(traverse.Main, 'editor')

#    basics.StartPage(user.ChangePasswordMain, 'user')
#    basics.StartPage(user.LogoutMain, 'user')

    def testVars(self):
	import vars
	self.assertTrue(basics.StartPage(vars.Main, 'vars', args="mod=MB786") != '')
	self.assertTrue(basics.StartPage(vars.Main, 'vars', args="mod=MB001 var=08") != '')
	self.assertTrue(basics.StartPage(vars.Main, 'vars', args="mod=MB320 var=06a") != '')
	self.assertTrue(basics.StartPage(vars.Main, 'vars', args="mod=SF75a list=1") != '')
	self.assertTrue(basics.StartPage(vars.Main, 'vars', args="mod=MB741 var=01") != '')
	self.assertTrue(basics.StartPage(vars.RunSearch, 'search', args="casting=austin codes=1 base= codes=2 body=green interior= wheels= windows= cat= submit=1") != '')

    def testVedit(self):
	import vedit
	self.assertTrue(basics.StartPage(vedit.HandleForm, 'vars', args="d=src/mbxf s=MW990 n=100") != '')
	self.assertTrue(basics.StartPage(vedit.HandleForm, 'vars', args="d=src/mbxf f=MW713") != '')

if __name__ == '__main__': # pragma: no cover
    unittest.main()
