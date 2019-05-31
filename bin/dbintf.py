#!/usr/local/bin/python

import MySQLdb, datetime, os, sys, traceback
import config
import useful


desc_cols = ['field', 'type', 'null', 'key', 'default', 'extra']


class DB(object):
    dbcs = {}

    def __init__(self, cfg=None, user_id=0, db_logger=None, verbose=False):
        self.verbose = verbose
        self.user_id = user_id
        self.nowrites = False
	self.logger = db_logger
        if cfg['dbuser'] in DB.dbcs:
            self.db = DB.dbcs[cfg['dbuser']]
        else:
            DB.dbcs[cfg['dbuser']] = self.db = MySQLdb.connect(user=cfg['dbuser'], passwd=cfg['dbpass'], db=cfg['dbname'])
        self.lastrowid = None
        self.lastdescription = None

    def __repr__(self):
        return "'<db.DB instance>'"

    def __str__(self):
        return "'<db.DB instance>'"

    def escape_string(self, s):
        return self.db.escape_string(s)

    def execute(self, query, args=None, logargs=True, verbose=None, tag=''):
        if verbose is None:
            verbose = self.verbose
        if tag:
            query = query.split(None, 1) + ['']
            query = query[0] + ' /* ' + tag + ' */ ' + query[1]
        if verbose:
            useful.write_comment('DB.execute q : "%s"' % query)
            if args:
		if logargs:
		    useful.write_comment('     args :', args)
		else:
		    useful.write_comment('     args :', len(args), 'redacted')
            sys.stdout.flush()
        if self.logger:
#            log_name = os.path.join(config.LOG_ROOT, config.ENV + datetime.datetime.now().strftime('.dbq%Y%m.log'))
#            try:
#                open(log_name, 'a').write('%s %s%s %s %s\n' %
#                                          (datetime.datetime.now().strftime('%Y%m%d.%H%M%S'), '/*mock*/' if self.nowrites else '',
#                                           self.user_id, os.environ.get('REMOTE_ADDR', ''), query))
#            except:
#                pass
	    self.logger.info('q %s%s %s' %
			      ('/*mock*/ ' if self.nowrites else '',
			       os.environ.get('REMOTE_ADDR', ''), query))
            if args:
		if logargs:
		    self.logger.info('     args :', args)
		else:
		    self.logger.info('     args :', len(args), 'redacted')
        cu = self.db.cursor()
        try:
	    nrows = cu.execute(query, args)
        except:
	    self.logger.info('x %s%s %s' %
			      ('/*mock*/ ' if self.nowrites else '',
			       os.environ.get('REMOTE_ADDR', ''), traceback.format_exc(0)))
            if verbose:
                traceback.print_exc()
            return ([], cu.description, -1)
        resp = cu.fetchall()
        if verbose:
            useful.write_comment("DB.execute a :", nrows, cu.lastrowid, resp)
            sys.stdout.flush()
        self.lastrowid = cu.lastrowid
        self.lastdescription = cu.description
        self.lastresp = resp
        cu.close()
	self.logger.info('a %s%s %s' %
			  ('/*mock*/ ' if self.nowrites else '',
			   os.environ.get('REMOTE_ADDR', ''), "%s rows %s id" % (len(resp), self.lastrowid)))
        return (resp, self.lastdescription, self.lastrowid)

    def mockexecute(self, query, args=None, verbose=None, tag=''):
        return ([], [], 0)

    # counter function

    def count(self, countid):
        if not self.db:
            return None
        cnt = 0
        res, desc, lid = self.execute("""select value from buser.counter where id='%s'""" % countid, verbose=False)
        if res:
            cnt = int(res[0][0])
        else:
            res, desc, lid = self.execute("""insert buser.counter (id, value) values ('%s', 0)""" % countid, verbose=False)
            self.execute('commit')
        res, desc, lid = self.execute("""update buser.counter set value=%s, timestamp=now() where id='%s'""" %
                                      (cnt + 1, countid), verbose=False)
        self.execute('commit')
        return res

    # page info functions

    def old_page_info(self, table):
        res = self.select("page_info,style",
                          ["page_info.format_type", "page_info.title", "page_info.pic_dir", "page_info.tail", "style.style_type",
                           "style.style_setting"],
                          "page_info.id='" + table + "' and page_info.id=style.page_id")
        if not res:
            return dict()
        ret = {
            "format_type": res[0]["page_info.format_type"],
            "title": res[0]["page_info.title"],
            "pic_dir": res[0]["page_info.pic_dir"],
            "tail": res[0]["page_info.tail"],
            "style": {}
        }
        for r in res:
            if ',' in str(r["style.style_setting"]):
                stt = r["style.style_type"]
                for sts in r["style.style_setting"].split(';'):
                    sts = sts.split(',')
                    ret["style"].setdefault(stt, {})
                    ret["style"][stt][sts[0]] = sts[1]
        return ret

    # generic functions

    def describe(self, table, verbose=None):
        if self.db:
            res, desc, lid = self.execute('desc %s' % table, verbose=verbose)
            if res:
                return [dict(zip(desc_cols, x)) for x in res]
        return list()

    def select(self, table, cols=None, where=None, group=None, order=None, args=None, distinct=False, outcols=None, limit=None,
	       logargs=True, tag='', verbose=None):
        if self.db:
            query = 'select '
            if tag:
                query += "/* %s */ " % tag
	    if distinct:
		query += 'distinct '
            if cols:
                query += '''%s from %s''' % (','.join(cols), table)
            else:
                query += '''* from %s''' % (table)
            if where:
                query += ''' where %s''' % where
            if group:
                query += ''' group by %s''' % group
            if order:
                query += ''' order by %s''' % order
	    if limit:
		query += ''' limit %s''' % limit
	    #useful.write_comment(query)
            res, desc, lid = self.execute(query, args, logargs=logargs, verbose=verbose)
            if not cols:
                cols = [x[0] for x in desc]
	    if not outcols:
		outcols = cols
            if res:
                return [dict(zip(outcols, x)) for x in res]
        return list()

    def rawquery(self, query, args=None, logargs=True, tag='', verbose=None):
        if self.db:
            if tag:
                query.insert(1, '/* %s */' % tag)
            res, desc, lid = self.execute(query, args, logargs, verbose=verbose)
            if not desc:
                return list()
            cols = [x[0] for x in desc]
            if res:
                return [dict(zip(cols, x)) for x in res]
        return list()

    def insert_or_update(self, table, values, args=None, logargs=True, tag='', verbose=None):
        if self.db:
            setlist = ','.join([x + "=" + self.db.literal(str(values[x])) for x in values])
            cols = []
            vals = []
            for item in values.items():
                cols.append(item[0])
                if isinstance(item[1], str):
                    vals.append(repr(item[1]))
                else:
                    vals.append(str(item[1]))
            cols = ','.join(cols)
            vals = ','.join(vals)
            query = 'insert '
            if tag:
                query += "/* %s */ " % tag
            query += '''into %s (%s) values (%s) on duplicate key update %s''' % (table, cols, vals, setlist)
            if self.nowrites:
                res, desc, lid = self.mockexecute(query, args, logargs, verbose=verbose, tag=tag)
            else:
                res, desc, lid = self.execute(query, args, logargs, verbose=verbose, tag=tag)
                self.execute('commit')
            return res
        return list()

    def update(self, table, values, where=None, args=None, logargs=True, tag='', verbose=None):
	if verbose:
	    print 'update', table, values, where, tag
        if self.db:
            query = 'update '
#            if tag:
#                query += "/* %s */ " % tag
	    if isinstance(values, dict):
		setlist = ','.join([x + "=" + (self.db.literal(str(values[x])) if values[x] is not None else 'NULL') for x in values])
	    elif isinstance(values, list):
		setlist = ','.join(values)
	    else:
		setlist = values
            query += '''%s set %s''' % (table, setlist)
            if where:
                query += ''' where %s;''' % where
            if self.nowrites:
                res, desc, lid = self.mockexecute(query, args, logargs, verbose=verbose, tag=tag)
            else:
                res, desc, lid = self.execute(query, args, logargs, verbose=verbose, tag=tag)
                self.execute('commit')
            return res
        return list()

    def updateraw(self, table, values, where=None, args=None, logargs=True, tag='', verbose=None):
        if self.db:
            query = 'update '
            if tag:
                query += "/* %s */ " % tag
            setlist = ','.join([x + "=" + values[x] for x in values])
            query += '''%s set %s''' % (table, setlist)
            if where:
                query += ''' where %s;''' % where
            if self.nowrites:
                res, desc, lid = self.mockexecute(query, args, logargs, verbose=verbose)
            else:
                res, desc, lid = self.execute(query, args, logargs, verbose=verbose)
                self.execute('commit')
            return res
        return list()

    def updateflag(self, table, values, where=None, tag='', verbose=None):
        if self.db:
            query = 'update '
            if tag:
                query += "/* %s */ " % tag
            setlist = ','.join([x + "=" + str(values[x]) for x in values])
            query += '''%s set %s''' % (table, setlist)
            if where:
                query += ''' where %s;''' % where
            if self.nowrites:
                res, desc, lid = self.mockexecute(query, verbose=verbose)
            else:
                res, desc, lid = self.execute(query, verbose=verbose)
                self.execute('commit')
            return res
        return list()

    def insert(self, table, inits={}, args=None, logargs=True, tag='', verbose=None):
        if self.db:
            query = 'insert '
            if tag:
                query += "/* %s */ " % tag
            cols = []
            vals = []
            for key in inits:
                cols.append(key)
                vals.append(self.db.literal(inits[key]))
            query += '''into %s (%s) values (%s)''' % (table, ','.join(cols), ','.join(vals))
            if self.nowrites:
                res, desc, lid = self.mockexecute(query, args, logargs, verbose=verbose)
            else:
                res, desc, lid = self.execute(query, args, logargs, verbose=verbose)
                self.execute('commit')
            return lid
        return -1

    def remove(self, table, where=None, tag='', verbose=None):
        if self.db:
            query = 'delete '
            if tag:
                query += "/* %s */ " % tag
            query += '''from %s''' % table
            if where:
                query += ''' where %s''' % where
            if self.nowrites:
                res, desc, lid = self.mockexecute(query, verbose=verbose)
            else:
                res, desc, lid = self.execute(query, verbose=verbose)
                self.execute('commit')
            return res
        return list()

    def commit(self, tag='Commit'):
	return self.execute('commit', tag=tag)
