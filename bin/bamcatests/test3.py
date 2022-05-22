import os
import unittest

import basics


class TestOther(unittest.TestCase):

    def setUp(self):
        os.putenv('SERVER_NAME', 'www.bamca.org')
        os.putenv('LOG_LEVEL', 'CRITICAL')

    def assertOut(self, result):
        self.assertNotEqual(result, '')

    # editor.EditorMain('editor')
    # editor.MassMain('editor')
    # editor.RoamMain('editor')
    # editor.ShowCounters('counter')

    # images.ImaWidget('editor')
    # images.PicturesMain('editor')
    # images.StitchMain('editor')
    # images.Tumblr('editor')
    # images.UploadMain('editor')

    def test_Others(self):
        import others
        self.assertOut(others.compare_main('compare', args='verbose=1'))

    def test_Lineup(self):
        import lineup
        self.assertIsNone(lineup.main('year', 'year', args='verbose=0'))
        self.assertIsNone(lineup.main('year', 'year', args='year=1960 region=U hidden=1 submit=1'))
        self.assertIsNone(lineup.main('year', 'year', args='year=1971 region=U nyears=2 submit=1'))
        self.assertIsNone(lineup.main('year', 'year', args='year=1984 region=B submit=1'))
        self.assertIsNone(lineup.main('year', 'year', args='year=1988 region=D submit=1'))
        self.assertIsNone(lineup.main('year', 'year', args='year=1991 region=A submit=1'))
        self.assertIsNone(lineup.main('year', 'year', args='year=1997 region=L unroll=1 submit=1'))
        self.assertIsNone(lineup.main('year', 'year', args='year=1999 region=D large=1 submit=1'))
        self.assertIsNone(lineup.main('year', 'year', args='year=2000 region=A submit=1'))
        self.assertIsNone(lineup.main('year', 'year', args='year=2006 region=A unroll=1 hidden=1 submit=1'))
        self.assertIsNone(lineup.main('year', 'year', args='year=2013 region=U submit=1 verbose=1'))
        pif = basics.get_page_info('editor', args="verbose=0")
        self.assertIsNotNone(pif)
        # self.assertOut(lineup.text_main(pif))
        # self.assertTrue(lineup.picture_count(pif, 'U', 2012) != None)
        self.assertIsNone(lineup.main('year', 'year', args='n=1 num=5 syear=1971 region=U enum= eyear=1980 submit=1'))
        self.assertIsNone(lineup.main(
            'year', 'year', args='n=1 num=5 syear=1971 region=U prodpic=1 enum=15 eyear=1980 submit=1'))

    def test_mack(self):
        import cmackl
        self.assertIsNone(cmackl.mack_lineup('mack', args='see_the_models=1 verbose=1'))

    def test_links(self):
        import tlinks
        self.assertOut(tlinks.links('links', 'page', 'toylinks', args="verbose=1"))
        self.assertOut(tlinks.links('links', 'page', 'toylinks', args="page=clubs"))
        self.assertOut(tlinks.links('links', 'page', 'toylinks', args="page=dealers"))
        self.assertOut(tlinks.links('links', 'page', 'toylinks', args="page=mailorder"))
        self.assertOut(tlinks.links('links', 'page', 'toylinks', args="page=manuf"))
        # self.assertOut(tlinks.links('links', 'page', 'toylinks', args="page=other"))
        self.assertOut(tlinks.links('links', 'page', 'toylinks', args="page=rejects"))
        self.assertOut(tlinks.links('links', 'page', 'toylinks', args="id=3"))
        self.assertOut(tlinks.links('links', 'page', 'toylinks', args="id=517"))
        self.assertOut(tlinks.add_page('addlink', args="verbose=0"))
#    tlinks.edit_links('editor')

    def test_manno(self):
        import mannum
        self.assertNotEqual(mannum.main(
            'manno', args='section=all listtype= range=all start=1 syear=1953 end=999 eyear=2015 type_a=y type_9=n '
                          'type_o=m type_c=m type_b=m type_i=m type_2=m type_d=m type_e=m type_j=m type_1=m type_g=m '
                          'type_r=m type_f=m type_4=m type_m=m type_u=m type_p=m type_z=m type_l=m type_t=m type_8=m '
                          'type_v=m type_h=m type_5=m type_x=m submit=1'), '')
        self.assertNotEqual(mannum.main(
            'manno', args='section=wr listtype= range=all start=1 syear=1953 end=999 eyear=2015 submit=1'), '')
        self.assertNotEqual(mannum.main(
            'manno', args='section=sf listtype= range=some start=5 syear=1972 end=9 eyear=1974 nodesc=1 '
                          'submit=1'), '')
        self.assertNotEqual(mannum.main(
            'manno', args='section=wr listtype=adl range=all start=1 syear=1953 end=999 eyear=2015 submit=1'), '')
        self.assertNotEqual(mannum.main(
            'manno', args='section=mi listtype=pxl range=all start=1 syear=1953 end=999 eyear=2015 submit=1'), '')
        self.assertNotEqual(mannum.main(
            'manno', args='section=wr listtype=thm range=all start=1 syear=1953 end=999 eyear=2015 submit=1'), '')
        self.assertNotEqual(mannum.main(
            'manno', args='section=wr listtype=ckl range=all start=1 syear=1953 end=999 eyear=2015 submit=1'), '')
        self.assertNotEqual(mannum.main(
            'manno', args='section=wr listtype=vtl range=all start=1 syear=1953 end=999 eyear=2015 submit=1'), '')

    def test_vmakes(self):
        import vmakes
        self.assertIsNone(vmakes.makes_main('makes', args='verbose=1'))
        self.assertIsNone(vmakes.makes_main('makes', args='make=text text=austin submit=1'))
        self.assertIsNone(vmakes.makes_main('makes', args='make=unk text=austin submit=1'))
        self.assertIsNone(vmakes.makes_main('makes', args='make=unl text=austin submit=1'))
        self.assertIsNone(vmakes.makes_main('makes', args='make=isu see_the_models=1'))

    def test_matrix1(self):
        import matrix
        self.assertOut(matrix.main('matrix', 'page', args='page=character verbose=1'))

    def test_Matrix2(self):
        import matrix
        self.assertOut(matrix.main('matrix', 'page', args='page=coll64'))

    def test_Matrix3(self):
        import matrix
        self.assertOut(matrix.main('matrix', 'page', args='page=mbhc verbose=1'))

    def test_Matrix4(self):
        import matrix
        self.assertOut(matrix.main('matrix', 'page', args='page=premiere'))

    def test_Matrix5(self):
        import matrix
        self.assertOut(matrix.main('matrix', 'page', args='verbose=1'))

    def test_Multipack(self):
        import multip
        self.assertOut(multip.packs_main('packs', 'page', args="verbose=1"))
        self.assertOut(multip.packs_main('packs', 'page', args="page=5packs id=2000p55alu"))

    def test_Nontoy(self):
        import nontoy
        self.assertOut(nontoy.biblio('bib', 'page', 'biblio', args="verbose=1 simple=1"))
        self.assertOut(nontoy.biblio('bib', 'page', 'biblio', args="page=bayarea sort=city"))
        self.assertOut(nontoy.calendar('calendar', args="verbose=1"))
    # nontoy.Publication('pub')

    # def test_Package(self):
        # self.assertOut(prints.blister('package', 'page', 'blister', args="verbose=1"))

    # prints.blister('package', 'page', 'blister')
    # prints.show_boxes('boxart')

    def test_Search(self):
        import search
        self.assertOut(search.run_search('search', args="query=austin submit=1"))
        self.assertOut(search.run_search('search', args="id=MB700 submit=1"))
        self.assertOut(search.run_search('search', args="id=MW800 submit=1"))
        self.assertOut(search.run_search('search', args="id=MI705 submit=1"))
        self.assertOut(search.run_search('search', args="id=MI205 submit=1"))
        self.assertOut(search.run_search('search', args="id=801 submit=1"))
        self.assertOut(search.run_search('search', args="id=SF01f submit=1"))
        self.assertOut(search.run_search('search', args="id=LR02c submit=1"))
        self.assertOut(search.run_search('search', args="id=LS03c submit=1"))
        self.assertOut(search.run_search('search', args="id= submit=1"))
        self.assertOut(search.run_search('search', args="submit=1"))

    def test_Sets(self):
        import mbsets
        self.assertOut(mbsets.sets_main('sets', 'page', args="verbose=1"))
        self.assertOut(mbsets.sets_main('sets', 'page', args="page=kings"))
        self.assertOut(mbsets.sets_main('sets', 'page', args="page=kings set=ks"))

    def test_Single(self):
        import single
        self.assertOut(single.show_single('single', args="verbose=1"))
        self.assertOut(single.show_single('single', args="id=MB001"))
        self.assertOut(single.show_single('single', args="id=RW01d"))
        self.assertOut(single.show_single('single', args="id=MB366 dir=pic/series pic=00l002 ref=matrix.mb2000 sub="))
        self.assertOut(single.show_single('single', args="id=SF02b"))
        self.assertOut(single.show_single('single', args="id=MB700 dir=pic/elseg pic=2006u57 ref=year.2006 sub="))
        self.assertOut(single.show_single('single', args="id=MB109"))

    # def test_Tomica(self):
    #     import tomica
    #     self.assertOut(tomica.main('tomica', args="verbose=1"))

    # traverse.main('editor')

    # user.ChangePasswordMain('user')
    # user.LogoutMain('user')

    def test_Vars(self):
        import varias
        self.assertOut(varias.main('vars', args="mod=MB786"))
        self.assertOut(varias.main('vars', args="mod=MB001 var=08"))
        self.assertOut(varias.main('vars', args="mod=MB320 var=06a"))
        self.assertOut(varias.main('vars', args="mod=SF75a list=1"))
        self.assertOut(varias.main('vars', args="mod=MB741 var=01"))
        self.assertOut(varias.run_search('search', args="casting=austin codes=1 base= codes=2 body=green interior= "
                                                        "wheels= windows= cat= submit=1"))

    def test_Vedit(self):
        import vredit
        self.assertOut(vredit.handle_form('vars', args="d=src/mbxf s=MW990 n=100"))
        self.assertOut(vredit.handle_form('vars', args="d=src/mbxf f=MW713"))


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
