import os
import unittest

import basics
import tables


class TestTables(unittest.TestCase):

    def setUp(self):
        os.putenv('LOG_LEVEL', 'CRITICAL')
        self.pif = basics.get_page_info('year.1953', args="verbose=0")

    def test_main(self):
        raw = self.pif.dbh.fetch_lineup_models(year='1953', region='W')
        ores = self.pif.dbh.depref('lineup_model', raw)
        ofirst = ores[0]
        fid = ores[0]['id']
