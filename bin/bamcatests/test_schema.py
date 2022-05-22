import os
import unittest

import basics
import tables


class TestSchema(unittest.TestCase):

    def setUp(self):
        os.putenv('LOG_LEVEL', 'CRITICAL')
        self.pif = basics.get_page_info('editor')

    def test_schema(self):
        bamca_tablelist = [x[0] for x in self.pif.dbh.dbi.execute('show tables')[0]]
        self.check_tables('bamca', bamca_tablelist)
        buser_tablelist = [x[0] for x in self.pif.dbh.dbi.execute('show tables in buser')[0]]
        self.check_tables('buser', buser_tablelist)

    def check_tables(self, dbname, dblist):
        dblist = [x[0] for x in self.pif.dbh.dbi.execute('show tables in {}'.format(dbname))[0]]
        tilist = [x for x, y in tables.table_data.items() if y.db == dbname]
        for table in dblist:
            if table in tables.table_data:
                t_data = tables.table_data[table]
                if t_data.db != dbname:
                    continue
                desc = self.pif.dbh.dbi.execute('desc ' + table)
                dbcols = set([x[0] for x in desc[0]])
                ticols = set(t_data.columns + t_data.extra_columns)
                if dbcols != ticols:
                    print(table, ':', "differ")
                    print("  db:", sorted(dbcols - ticols))
                    print("  ti:", sorted(ticols - dbcols))
                # else:
                #     print("same")
            else:
                print(table, ':', "missing from table_data")
        for table in set(tilist) - set(dblist):
            print(table, ': missing from database')

        self.assertEqual(set(tilist) - set(dblist), set())


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
