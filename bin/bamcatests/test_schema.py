import unittest
import basics
import dbintf
import dbhand
import pifile
import render
import tables

class TestSchema(unittest.TestCase):

    def setUp(self):
	self.pif = basics.get_page_info('editor')

    def test_schema(self):
	bamca_tablelist = [x[0] for x in self.pif.dbh.dbi.execute('show tables')[0]]
	buser_tablelist = [x[0] for x in self.pif.dbh.dbi.execute('show tables in buser')[0]]

    def check_tables(self, dbname, tablelisst):
	for table in tablelist:
	    if table in tables.table_info:
		t_info = tables.table_info[table]
		if t_info['db'] != dbname:
		    continue
		desc = self.pif.dbh.dbi.execute('desc ' + table)
		dbcols = set([x[0] for x in desc[0]])
		ticols = set(t_info['columns'] + t_info.get('extra_columns', []))
		if dbcols != ticols:
		    print table, ':', "differ"
		    print "  db:", sorted(dbcols - ticols)
		    print "  ti:", sorted(ticols - dbcols)
    #            else:
    #                print "same"
	    else:
		print table, ':', "missing from table_info"
	for table in set(tables.table_info.keys()) - set(tablelist):
	    print table, ': missing from database'

	self.assertTrue(not (set(tables.table_info.keys()) - set(tablelist)))



if __name__ == '__main__': # pragma: no cover
    unittest.main()
