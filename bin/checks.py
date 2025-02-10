#!/usr/local/bin/python

top = '''import unittest

# this file is auto generated.  do not modify.


class TestImports(unittest.TestCase):
    def setUp(self):
        pass
'''
fts = '''
    def testImport{}(self):
        import {}  # noqa
'''
bottom = '''

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
'''

if __name__ == '__main__':
    # import updcommits
    # updcommits.write_php_config_file()
    # updcommits.write_jinja2_config_file()

    import glob
    f = glob.glob('*.py')
    open('bamcatests/test0.py', 'w').write(
        top + ''.join([fts.format(x[:-3].capitalize(), x[:-3]) for x in glob.glob('*.py')]) + bottom)

    import unittest
    print("Running unittests.")
    ret = unittest.TextTestRunner(verbosity=1, buffer=1).run(unittest.TestLoader().discover('.'))
