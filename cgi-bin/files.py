#!/usr/local/bin/python

import os, re, sys

import mbdata
import useful
#from config import *

#---- barparse ----------------------------------------------------------

class ArgList:
    def __init__(self, line):
	self.llist = []
	line = line.strip( )
	if len( line ) and line[0] != '#':
	    self.llist = map(lambda x: x.strip(), line.split('|'))
	self.curarg = 0

    def Clean(self):
	self.llist = map(lambda x: x.strip(), self.llist)

    def Args(self):
	return len(self.llist)

    def GetArg(self, defval=None, start=-1):
	ret = defval
	if start >= 0:
	    self.curarg = start
	if self.curarg < self.Args():
	    nval = self.llist[self.curarg].strip()
	    if nval:
		ret = nval
	    self.curarg += 1
	return ret

    def GetArgs( self, defvals, start=-1):
	ret = ()
	if start >= 0:
	    self.curarg = start
	for val in defvals:
	    ret = ret + ( self.GetArg( val ), )
	return ret

    def __len__(self):
	return len(self.llist)

    def Rewind(self):
	self.curarg = 0

    def __getitem__(self, s):
	return self.llist.__getitem__(s)

    def __str__(self):
	return str(self.llist)


class BarFile:
    def __init__(self, fname):
	self.filename = fname
	try:
	    self.handle = open(fname)
	except IOError:
	    print "<!--",fname,"is on crack. -->"
	    print """I'm sorry, that page was not found.  Please use your "BACK" button or try something else."""
	    sys.exit(1)
	self.srcstat = os.fstat(self.handle.fileno())
	self.ignoreoverride = False
	self.dats = {}
	self.Parse()

    def __getitem__(self, arg):
	return self.__dict__[arg]

    def get(self, arg, val=None):
	return self.__dict__.get(arg, val)

    def Read(self):
	return self.ReadFile(self.handle)

    def ReadLine(self, line):
	llist = ArgList(line)
	llist.Clean()
	return llist

    def ReadFile(self, dbh):
	db = dbh.readlines()
	dblist = []
	ignoreflag = False
	for line in db:
	    if line[0] == '#':
		continue
	    llist = self.ReadLine(line)
	    if not llist:
		continue
	    cmd = llist.GetArg()
	    if cmd == 'ignore':
		ignoreflag = not self.ignoreoverride and int(llist.GetArg())
	    elif cmd == 'if':
		ignoreflag = not eval(llist.GetArg())
	    elif cmd == 'endif':
		ignoreflag = False
	    elif ignoreflag:
		continue
	    elif cmd == 'include':
		dblist.extend( self.ReadInclude( llist.GetArg() ) )
	    else:
		llist.Rewind()
		dblist.append( llist )
	return dblist

    def ReadInclude(self, datname):
	try:
	    dbf = file(datname)
	except IOError:
	    return []
	return self.ReadFile(dbf)
	fst = os.fstat(dbf.fileno())
	db = dbf.readlines()
	dblist = []
	for line in db:
	    if line[0] == '#':
		continue
	    llist = self.ReadLine(line)
	    if not llist:
		continue
	    cmd = llist.GetArg()
	    if cmd == 'include':
		dblist.extend( self.ReadInclude( llist.GetArg() ) )
	    else:
		llist.Rewind()
		dblist.append( llist )
	return dblist

    def Peek(self, datname):
	line = self.handle.readline()
	llist = self.ReadLine(line)
	return llist

    def Parse(self):
	self.dblist = []
	rawlist = self.Read()
	for e in rawlist:
	    ent = self.ParseCommand(e)
	    if ent:
		self.dblist.append(ent)
	self.ParseEnd()
	return self.dblist

    def ParseCommand(self, llist):
	cmd = llist.GetArg()
	ent = self.ParseField(self.__class__, str(cmd), llist)
	if ent == None:
	    ent = self.ParseByData(llist)
	if ent == None:
	    ent = self.ParseElse(llist)
	return ent

    def ParseData(self, llist, cmdname="cmd"):
	if llist[0] in self.dats:
	    return dict(zip([cmdname] + self.dats[llist[0]][0], llist.llist))
	return None

    def ParseByData(self, llist):
	return self.ParseData(llist)

    def ParseElse(self, llist):
	return None

    def ParseField(self, pclass, cmd, llist):
	if "Parse_"+cmd in pclass.__dict__:
	    ret = pclass.__dict__['Parse_' + cmd](self, llist)
	    if ret != None:
		return ret
	    return False
	if pclass.__bases__:
	    return pclass.__bases__[0].ParseField(self, pclass.__bases__[0], cmd, llist)
	return None

    def Parse_data(self, llist):
	key = llist.GetArg()
	fld = llist.GetArg()
	typ = llist.GetArg('')
	self.dats[key] = (fld.split(','), typ)

    def ParseEnd(self):
	pass

#---- unfinished file classes -------------------------------------------

# in use
class ArgFile (BarFile):
    def __init__(self, fname):
	self.SetGlobals()
	BarFile.__init__(self, fname)

    def SetGlobals(self):
	self.fmttype = 'main'
	self.pagetitle = self.title = ''
	self.picdir = ''
	self.tail = {}

    def Read(self):
	self.tail['stat'] = self.srcstat
	try:
	    return BarFile.Read(self)
	except IOError:
	    print FormatHead()
	    print "<!--",form,"-->"
	    print "<!--",datname,"is on crack. -->"
	    print """I'm sorry, that page was not found.  Please use your "BACK" button or try something else."""
	    print FormatTail()
	    sys.exit(1)

    def Parse_formatter(self, llist):
	self.picdir = llist.GetArg()
	self.fmttype = llist.GetArg()
	self.pagetitle = llist.GetArg()

    def Parse_style(self, llist):
	pass

    def Parse_page(self, llist):
	pass

    def Parse_title(self, llist):
	self.title = llist.GetArg('')

    def Parse_tail(self, llist):
	arg = llist.GetArg()
	while arg:
	    self.tail[arg] = 1
	    arg = llist.GetArg()

    def Parse_restrict(self, llist):
	Restrict(llist[1])


# in use
class SimpleFile(ArgFile):
    def __init__(self, fname):
	self.dblist = []
	ArgFile.__init__(self, fname)

    def __iter__(self):
	return self.dblist.__iter__()

    def ParseElse(self, llist):
	llist.Rewind()
	self.dblist.append(llist)

    def __len__(self):
	return len(self.dblist)


#---- finished file classes ---------------------------------------------

tablecols = ['prefix', 'cols', 'title', 'digits', 'label', 'style']
notcols = ['fulldesc', 'insetdesc', 'fullpic']
# in use
class SetFile(ArgFile):
    def __init__(self, fname='src/diffs.dat'):
	self.tables = []
	self.found = False
	self.db = {'model': []}
	self.ncols = 0
	self.header = ''
	self.colheads = {}
	self.dirs = {}
	ArgFile.__init__(self, fname)

    def Parse_cells(self, llist):
	self.header = llist[1:]
	self.ncols = 0
	for col in self.header:
	    if not(col in notcols):
		self.ncols += 1
	self.db['ncols'] = self.ncols

    def Parse_dir(self, llist):
	self.dirs[llist[1]] = llist[2]

    def Parse_field(self, llist):
	self.colheads[llist[1]] = llist[2]

    def Parse_table(self, llist):
	if self.found:
	    self.tables.append(self.db)
	    self.db = {'model': []}
	self.db.update(dict(map(None, tablecols, llist[1:])))
	self.db['cols'] = cols = self.db['cols'].split(',')
	self.db['header'] = self.header
	self.db['ncols'] = self.ncols

    def Parse_t(self, llist):
	self.model = { 'text' : llist.GetArg( '' ) }
	self.db['model'].append(self.model)

    def Parse_s(self, llist):
	self.model = { 'section' : llist.GetArg( '' ) }
	self.db['model'].append(self.model)

    def Parse_m(self, llist):
	self.found = True
	self.model = dict(map(None, self.db['cols'], llist[1:]))
	self.model['desc'] = []
	self.db['model'].append(self.model)

    def Parse_d(self, llist):
	self.model['desc'].append( llist[1] )

    def ParseEnd(self):
	if self.found:
	    self.tables.append(self.db)



if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
