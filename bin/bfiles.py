#!/usr/local/bin/python

import os, re, sys, time

import mbdata
import useful


# --- barparse ----------------------------------------------------------


class ArgList:
    def __init__(self, line):
        self.llist = []
        line = line.strip()
        if len(line) and line[0] != '#':
            self.llist = [x.strip() for x in line.split('|')]
        self.curarg = 0

    def clean(self):
        self.llist = [x.strip() for x in self.llist]

    def args(self):
        return len(self.llist)

    def get_arg(self, defval=None, start=-1):
        ret = defval
        if start >= 0:
            self.curarg = start
        if self.curarg < self.args():
            nval = self.llist[self.curarg].strip()
            if nval:
                ret = nval
            self.curarg += 1
        return ret

    def get_args(self, defvals, start=-1):
        ret = ()
        if start >= 0:
            self.curarg = start
        for val in defvals:
            ret = ret + (self.get_arg(val),)
        return ret

    def __len__(self):
        return len(self.llist)

    def rewind(self):
        self.curarg = 0

    def __getitem__(self, s):
        return self.llist.__getitem__(s)

    def __str__(self):
        return str(self.llist) + ' (+%d)' % self.curarg


class BarFile:
    def __init__(self, fname):
        self.filename = fname
        try:
            self.handle = open(fname)
        except IOError:
            print "<!--", fname, "is on crack. -->"
            print """I'm sorry, that page was not found.  Please use your "BACK" button or try something else."""
            sys.exit(1)
        self.srcstat = os.fstat(self.handle.fileno())
        self.ignoreoverride = False
        self.dats = {}
        self.parse()

    def __getitem__(self, arg):
        return self.__dict__[arg]

    def get(self, arg, val=None):
        return self.__dict__.get(arg, val)

    def read(self):
        return self.read_file(self.handle)

    def read_line(self, line):
        llist = ArgList(line)
        llist.clean()
        return llist

    def read_file(self, dbh):
        db = dbh.readlines()
        dblist = []
        ignoreflag = False
        for line in db:
            if line[0] == '#':
                continue
            llist = self.read_line(line)
            if not llist:
                continue
            cmd = llist.get_arg()
            if cmd == 'ignore':
                ignoreflag = not self.ignoreoverride and int(llist.get_arg())
            elif cmd == 'if':
                ignoreflag = not eval(llist.get_arg())
            elif cmd == 'endif':
                ignoreflag = False
            elif ignoreflag:
                continue
            elif cmd == 'include':
                dblist.extend(self.read_include(llist.get_arg()))
            else:
                llist.rewind()
                dblist.append(llist)
        return dblist

    def read_include(self, datname):
        try:
            dbf = open(datname)
        except IOError:
            return []
        return self.read_file(dbf)
        fst = os.fstat(dbf.fileno())
        db = dbf.readlines()
        dblist = []
        for line in db:
            if line[0] == '#':
                continue
            llist = self.read_line(line)
            if not llist:
                continue
            cmd = llist.get_arg()
            if cmd == 'include':
                dblist.extend(self.read_include(llist.get_arg()))
            else:
                llist.rewind()
                dblist.append(llist)
        return dblist

    def peek(self, datname):
        line = self.handle.readline()
        llist = self.read_line(line)
        return llist

    def parse(self):
        self.dblist = []
        rawlist = self.read()
        for e in rawlist:
            ent = self.parse_command(e)
            if ent:
                self.dblist.append(ent)
        self.parse_end()
        return self.dblist

    def parse_command(self, llist):
        cmd = llist.get_arg()
        ent = self.parse_field_line(self.__class__, str(cmd), llist)
        if ent is None:
            ent = self.parse_by_data(llist)
        if ent is None:
            ent = self.parse_else(llist)
        return ent

    def parse_data_line(self, llist, cmdname="cmd"):
        if llist[0] in self.dats:
            return dict(zip([cmdname] + self.dats[llist[0]][0], llist.llist))
        return None

    def parse_by_data(self, llist):
        return self.parse_data_line(llist)

    def parse_else(self, llist):
        return None

    def parse_field_line(self, pclass, cmd, llist):
        if "parse_" + cmd in pclass.__dict__:
            ret = pclass.__dict__['parse_' + cmd](self, llist)
            if ret is not None:
                return ret
            return False
        if pclass.__bases__:
            return pclass.__bases__[0].parse_field_line(self, pclass.__bases__[0], cmd, llist)
        return None

    def parse_data(self, llist):
        llist.rewind()
        key = llist.get_arg()
        fld = llist.get_arg()
        typ = llist.get_arg('')
        self.dats[key] = (fld.split(','), typ)

    def parse_end(self):
        pass


# --- unfinished file classes -------------------------------------------


# in use
class ArgFile(BarFile):
    def __init__(self, fname):
        self.set_globals()
        BarFile.__init__(self, fname)

    def set_globals(self):
        self.fmttype = 'main'
        self.pagetitle = self.title = ''
        self.picdir = ''
        self.tail = {}

    def read(self):
        self.tail['stat'] = time.strftime('Last updated %A, %d %B %Y at %I:%M:%S %p %Z.', time.localtime(self.srcstat.st_mtime))
        try:
            return BarFile.read(self)
        except IOError:
            print format_head()
            print "<!--", form, "-->"
            print "<!--", datname, "is on crack. -->"
            print """I'm sorry, that page was not found.  Please use your "BACK" button or try something else."""
            print format_tail()
            sys.exit(1)

    def parse_formatter(self, llist):
        self.picdir = llist.get_arg()
        self.fmttype = llist.get_arg()
        self.pagetitle = llist.get_arg()

    def parse_style(self, llist):
        pass

    def parse_page(self, llist):
        pass

    def parse_title(self, llist):
        self.title = llist.get_arg('')

    def parse_tail(self, llist):
        arg = llist.get_arg()
        while arg:
            self.tail[arg] = 1
            arg = llist.get_arg()

    def parse_restrict(self, llist):
        restrict(llist[1])


# in use
class SimpleFile(ArgFile):
    def __init__(self, fname):
        self.dblist = []
        ArgFile.__init__(self, fname)

    def __iter__(self):
        return self.dblist.__iter__()

    def parse_else(self, llist):
        llist.rewind()
        self.dblist.append(llist)

    def __len__(self):
        return len(self.dblist)


# --- finished file classes ---------------------------------------------


# in use
class SetFile(ArgFile):
    tablecols = ['prefix', 'cols', 'title', 'digits', 'label', 'style']
    notcols = ['fulldesc', 'insetdesc', 'fullpic']

    def __init__(self, fname='src/diffs.dat'):
        self.tables = []
        self.found = False
        self.db = {'model': []}
        self.ncols = 0
        self.header = ''
        self.colheads = {}
        self.dirs = {}
        ArgFile.__init__(self, fname)

    def parse_cells(self, llist):
        self.header = llist[1:]
        self.ncols = 0
        for col in self.header:
            if not(col in self.notcols):
                self.ncols += 1
        self.db['ncols'] = self.ncols

    def parse_dir(self, llist):
        self.dirs[llist[1]] = llist[2]

    def parse_field(self, llist):
        self.colheads[llist[1]] = llist[2]

    def parse_table(self, llist):
        if self.found:
            self.tables.append(self.db)
            self.db = {'model': []}
        self.db.update(dict(map(None, self.tablecols, llist[1:])))
        self.db['cols'] = cols = self.db['cols'].split(',')
        self.db['header'] = self.header
        self.db['ncols'] = self.ncols

    def parse_t(self, llist):
        self.model = {'text': llist.get_arg('')}
        self.db['model'].append(self.model)

    def parse_s(self, llist):
        self.model = {'section': llist.get_arg('')}
        self.db['model'].append(self.model)

    def parse_m(self, llist):
        self.found = True
        self.model = dict(map(None, self.db['cols'], llist[1:]))
        self.model['desc'] = []
        self.db['model'].append(self.model)

    def parse_d(self, llist):
        self.model['desc'].append(llist[1])

    def parse_end(self):
        if self.found:
            self.tables.append(self.db)


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
