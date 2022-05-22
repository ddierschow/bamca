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
        r = tables.Results('lineup_model', raw)
        ores = self.pif.dbh.depref('lineup_model', raw)
        nfirst = r.first
        ofirst = ores[0]
        fid = ores[0]['id']
        self.assertEqual(len(r), len(ores))
        self.assertEqual(nfirst['id'], fid)
        self.assertEqual(nfirst.id, fid)
        self.assertEqual(nfirst.casting.id, ofirst['casting.id'])
        self.assertEqual(nfirst.base_id.rawname, ofirst['base_id.rawname'])

        # print 's2'
        # print r.name
        # print r.id
        # print r.columns
        # print len(r)
        # print r.first.keys()
        # print r.first['lineup_model.number']
        # print r.first['base_id.id']
        # for l in r:
        #     print l.lineup_model.number
        # r.first['lineup_model.number'] = 23
        # print r.first['lineup_model.number']
        # print r.first.lineup_model['number']
        # print r.first.lineup_model.number
        # print r.first.number
        #
        # print 's3'
        # q = self.pif.dbh.fetch_pack('1996p5ccr1')
        # print q
        # r = tables.Results('pack', q).first
        # print r
        # print bool(r)
        # print r.first
        # print r.layout
        # print r.pack.layout
        # print r.base_id.rawname
        #
        # print 's4'
        # q = self.pif.dbh.fetch_pack('nonexistant')
        # print q
        # r = tables.Results('pack', q).first
        # print r
        # print bool(r)
        # print r.first
        # print r.layout
        # print r.pack.layout
        # print r.base_id.rawname
