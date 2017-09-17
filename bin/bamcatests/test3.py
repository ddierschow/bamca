import unittest
import basics

class TestOther(unittest.TestCase):

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

    def test_Lineup(self):
	import lineup
        self.assertTrue(lineup.main('year', 'year', args='verbose=0') is None)
        self.assertTrue(lineup.main('year', 'year', args='year=1960 region=U hidden=1 submit=1') is None)
        self.assertTrue(lineup.main('year', 'year', args='year=1971 region=U nyears=2 submit=1') is None)
        self.assertTrue(lineup.main('year', 'year', args='year=1984 region=B submit=1') is None)
        self.assertTrue(lineup.main('year', 'year', args='year=1988 region=D submit=1') is None)
        self.assertTrue(lineup.main('year', 'year', args='year=1991 region=A submit=1') is None)
        self.assertTrue(lineup.main('year', 'year', args='year=1997 region=L unroll=1 submit=1') is None)
        self.assertTrue(lineup.main('year', 'year', args='year=1999 region=D large=1 submit=1') is None)
        self.assertTrue(lineup.main('year', 'year', args='year=2000 region=A submit=1') is None)
        self.assertTrue(lineup.main('year', 'year', args='year=2006 region=A unroll=1 hidden=1 submit=1') is None)
        self.assertTrue(lineup.main('year', 'year', args='year=2013 region=U submit=1 verbose=1') is None)
	pif = basics.get_page_info('editor', args="verbose=0")
	#self.assertTrue(lineup.text_main(pif) != '')
	#self.assertTrue(lineup.picture_count(pif, 'U', 2012) != None)
        self.assertTrue(lineup.main('year', 'year', args='n=1 num=5 syear=1971 region=U enum= eyear=1980 submit=1') is None)
        self.assertTrue(lineup.main('year', 'year', args='n=1 num=5 syear=1971 region=U prodpic=1 enum=15 eyear=1980 submit=1') is None)

    def test_Mack(self):
	import cmackl
        self.assertTrue(cmackl.mack_lineup('mack', args='see_the_models=1 verbose=1') is None)

    def test_Links(self):
	import tlinks
        self.assertTrue(tlinks.links('links', 'page', 'toylinks', args="verbose=1") != '')
        self.assertTrue(tlinks.links('links', 'page', 'toylinks', args="page=clubs") != '')
        self.assertTrue(tlinks.links('links', 'page', 'toylinks', args="page=dealers") != '')
        self.assertTrue(tlinks.links('links', 'page', 'toylinks', args="page=mailorder") != '')
        self.assertTrue(tlinks.links('links', 'page', 'toylinks', args="page=manuf") != '')
        #self.assertTrue(tlinks.links('links', 'page', 'toylinks', args="page=other") != '')
        self.assertTrue(tlinks.links('links', 'page', 'toylinks', args="page=rejects") != '')
        self.assertTrue(tlinks.links('links', 'page', 'toylinks', args="id=3") != '')
        self.assertTrue(tlinks.links('links', 'page', 'toylinks', args="id=517") != '')
        self.assertTrue(tlinks.add_page('addlink', args="verbose=0") != '')
#    tlinks.edit_links('editor')

    def test_Manno(self):
	import mannum
        self.assertTrue(mannum.compare_main('compare', args='verbose=1') != '')
        self.assertTrue(mannum.main('manno', args='section=all listtype= range=all start=1 syear=1953 end=999 eyear=2015 type_a=y type_9=n type_o=m type_c=m type_b=m type_i=m type_2=m type_d=m type_e=m type_j=m type_1=m type_g=m type_r=m type_f=m type_4=m type_m=m type_u=m type_p=m type_z=m type_l=m type_t=m type_8=m type_v=m type_h=m type_5=m type_x=m submit=1') != '')
        self.assertTrue(mannum.main('manno', args='section=wr listtype= range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(mannum.main('manno', args='section=sf listtype= range=some start=5 syear=1972 end=9 eyear=1974 nodesc=1 submit=1') != '')
        self.assertTrue(mannum.main('manno', args='section=wr listtype=adl range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(mannum.main('manno', args='section=mi listtype=pxl range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(mannum.main('manno', args='section=wr listtype=thm range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(mannum.main('manno', args='section=wr listtype=ckl range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')
        self.assertTrue(mannum.main('manno', args='section=wr listtype=vtl range=all start=1 syear=1953 end=999 eyear=2015 submit=1') != '')

    def test_Vmakes(self):
	import vmakes
        self.assertTrue(vmakes.makes_main('makes', args='verbose=1') is None)
        self.assertTrue(vmakes.makes_main('makes', args='make=text text=austin submit=1') is None)
        self.assertTrue(vmakes.makes_main('makes', args='make=unk text=austin submit=1') is None)
        self.assertTrue(vmakes.makes_main('makes', args='make=unl text=austin submit=1') is None)
        self.assertTrue(vmakes.makes_main('makes', args='make=isu see_the_models=1') is None)

    def test_Matrix1(self):
	import matrix
	self.assertTrue(matrix.main('matrix', 'page', args='page=character verbose=1') != '')

    def test_Matrix2(self):
	import matrix
	self.assertTrue(matrix.main('matrix', 'page', args='page=coll64') != '')

    def test_Matrix3(self):
	import matrix
	self.assertTrue(matrix.main('matrix', 'page', args='page=mbhc verbose=1') != '')

    def test_Matrix4(self):
	import matrix
	self.assertTrue(matrix.main('matrix', 'page', args='page=premiere') != '')

    def test_Matrix5(self):
	import matrix
	self.assertTrue(matrix.main('matrix', 'page', args='verbose=1') != '')

    def test_Multipack(self):
	import multipack
	self.assertTrue(multipack.do_page('packs', 'page', args="verbose=1") != '')
	self.assertTrue(multipack.do_page('packs', 'page', args="page=5packs id=2000p55alu") != '')

    def test_Nontoy(self):
	import nontoy
	self.assertTrue(nontoy.biblio('bib', 'page', 'biblio', args="verbose=1 simple=1") != '')
	self.assertTrue(nontoy.biblio('bib', 'page', 'biblio', args="page=bayarea sort=city") != '')
	self.assertTrue(nontoy.calendar('calendar', args="verbose=1") != '')
#    nontoy.Publication('pub')

    def test_Package(self):
	import package
	#self.assertTrue(package.blister('package', 'page', 'blister', args="verbose=1") != '')
#    package.blister('package', 'page', 'blister')
#    package.show_boxes('boxart')

    def test_Search(self):
	import search
	self.assertTrue(search.run_search('search', args="query=austin submit=1") != '')
	self.assertTrue(search.run_search('search', args="id=MB700 submit=1") != '')
	self.assertTrue(search.run_search('search', args="id=MW800 submit=1") != '')
	self.assertTrue(search.run_search('search', args="id=MI705 submit=1") != '')
	self.assertTrue(search.run_search('search', args="id=MI205 submit=1") != '')
	self.assertTrue(search.run_search('search', args="id=801 submit=1") != '')
	self.assertTrue(search.run_search('search', args="id=SF01f submit=1") != '')
	self.assertTrue(search.run_search('search', args="id=LR02c submit=1") != '')
	self.assertTrue(search.run_search('search', args="id=LS03c submit=1") != '')
	self.assertTrue(search.run_search('search', args="id= submit=1") != '')
	self.assertTrue(search.run_search('search', args="submit=1") != '')

    def test_Sets(self):
	import mbsets
	self.assertTrue(mbsets.sets_main('sets', 'page', args="verbose=1") != '')
	self.assertTrue(mbsets.sets_main('sets', 'page', args="page=kings") != '')
	self.assertTrue(mbsets.sets_main('sets', 'page', args="page=kings set=ks") != '')

    def test_Single(self):
	import single
	self.assertTrue(single.show_single('single', args="verbose=1") != '')
	self.assertTrue(single.show_single('single', args="id=MB001") != '')
	self.assertTrue(single.show_single('single', args="id=RW01d") != '')
	self.assertTrue(single.show_single('single', args="id=MB366 dir=pic/series pic=00l002 ref=matrix.mb2000 sub=") != '')
	self.assertTrue(single.show_single('single', args="id=SF02b") != '')
	self.assertTrue(single.show_single('single', args="id=MB700 dir=pic/elseg pic=2006u57 ref=year.2006 sub=") != '')
	self.assertTrue(single.show_single('single', args="id=MB109") != '')

#    def test_Tomica(self):
#	import tomica
#	self.assertTrue(tomica.main('tomica', args="verbose=1") != '')

#    traverse.main('editor')

#    user.ChangePasswordMain('user')
#    user.LogoutMain('user')

    def test_Vars(self):
	import vars
	self.assertTrue(vars.main('vars', args="mod=MB786") != '')
	self.assertTrue(vars.main('vars', args="mod=MB001 var=08") != '')
	self.assertTrue(vars.main('vars', args="mod=MB320 var=06a") != '')
	self.assertTrue(vars.main('vars', args="mod=SF75a list=1") != '')
	self.assertTrue(vars.main('vars', args="mod=MB741 var=01") != '')
	self.assertTrue(vars.run_search('search', args="casting=austin codes=1 base= codes=2 body=green interior= wheels= windows= cat= submit=1") != '')

    def test_Vedit(self):
	import vedit
	self.assertTrue(vedit.handle_form('vars', args="d=src/mbxf s=MW990 n=100") != '')
	self.assertTrue(vedit.handle_form('vars', args="d=src/mbxf f=MW713") != '')

if __name__ == '__main__': # pragma: no cover
    unittest.main()
