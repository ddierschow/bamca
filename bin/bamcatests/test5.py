import os
import unittest

import basics
import editor
import masses


class TestEditor(unittest.TestCase):

    def assertOut(self, result):
        self.assertNotEqual(result, '')

    def setUp(self):
        os.putenv('SERVER_NAME', 'www.bamca.org')
        os.putenv('LOG_LEVEL', 'CRITICAL')
        self.pif = basics.get_page_info('editor')
        self.pif.privs = set(list('vuma'))

    def test_editor_ask(self):
        self.assertOut(editor.editor_main('editor', args="verbose=1"))

    def test_mass_ask(self):
        self.assertOut(masses.mass('editor', args="verbose=1"))
