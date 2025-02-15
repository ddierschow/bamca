#!/usr/local/bin/python

from io import open
import os
import time

import useful


# --- barparse ----------------------------------------------------------


class ArgList(object):
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
        return '{} (+{})'.format(self.llist, self.curarg)


class ArgFile(object):
    def __init__(self, fname):
        if fname.startswith('/'):
            fname = fname[1:]
        self.filename = fname
        useful.write_comment('trying to open', fname)
        self.set_globals()
        try:
            self.handle = open(fname)
        except IOError:
            raise useful.SimpleError(
                """I'm sorry, that page was not found.  Please use your "BACK" button or try something else.""")
        self.srcstat = os.fstat(self.handle.fileno())
        self.ignoreoverride = False
        self.dats = {}
        self.parse()

    def set_globals(self):
        self.fmttype = 'main'
        self.pagetitle = self.title = ''
        self.picdir = ''
        self.tail = {}

    def read(self):
        self.tail['stat'] = time.strftime('Last updated %A, %d %B %Y at %I:%M:%S %p %Z.',
                                          time.localtime(self.srcstat.st_mtime))
        try:
            return self.read_file(self.handle)
        except IOError:
            raise useful.SimpleError(
                """I'm sorry, that page was not found.  Please use your "BACK" button or try something else.""")

    def __getitem__(self, arg):
        return self.__dict__[arg]

    def get(self, arg, val=None):
        return self.__dict__.get(arg, val)

    def __iter__(self):
        return self.dblist.__iter__()

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
        # fst = os.fstat(dbf.fileno())
        # db = dbf.readlines()
        # dblist = []
        # for line in db:
        #     if line[0] == '#':
        #         continue
        #     llist = self.read_line(line)
        #     if not llist:
        #         continue
        #     cmd = llist.get_arg()
        #     if cmd == 'include':
        #         dblist.extend(self.read_include(llist.get_arg()))
        #     else:
        #         llist.rewind()
        #         dblist.append(llist)
        # return dblist

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
        # useful.write_message('pdl', llist, cmdname, self.dats)
        if llist[0] in self.dats:
            return dict(zip([cmdname] + self.dats[llist[0]][0], llist.llist))
        return None

    def parse_by_data(self, llist):
        return self.parse_data_line(llist)

    def parse_else(self, llist):
        return None

    def parse_field_line(self, pclass, cmd, llist):
        # useful.write_message('pfl', str(pclass.__name__), str(pclass.__dict__.keys()), cmd, llist)
        # if "parse_" + cmd in pclass.__dict__:
        if hasattr(self, 'parse_' + cmd):
            try:
                # ret = pclass.__dict__['parse_' + cmd](self, llist)
                # ret = eval('self.parse_' + cmd + '(llist)')
                parser = getattr(self, 'parse_' + cmd)
                ret = parser(llist)
            except Exception as e:
                useful.write_comment('Exception:', str(e))
                return False
            if ret is not None:
                # useful.write_message('...', ret)
                return ret
            # useful.write_message('...', False)
            return False
        # if pclass.__bases__:
        #     return pclass.__bases__[0].parse_field_line(self, pclass.__bases__[0], cmd, llist)
        # useful.write_message('...', None)
        return None

    def parse_data(self, llist):
        # llist.rewind()
        # useful.write_message('pd', llist)
        key = llist.get_arg()
        fld = llist.get_arg()
        typ = llist.get_arg('')
        self.dats[key] = (fld.split(','), typ)

    def parse_end(self):
        pass

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

    # def parse_restrict(self, llist):
    #     restrict(llist[1])

    def __len__(self):
        return len(self.dblist)


class SimpleFile(ArgFile):
    def __init__(self, fname):
        self.dblist = []
        super().__init__(fname)

    def parse_else(self, llist):
        llist.rewind()
        self.dblist.append(llist)
