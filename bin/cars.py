#!/usr/local/bin/python

import copy, os
import basics
import bfiles
import config

# ------- ----------------------------------------------------------

class CarsFile(bfiles.ArgFile):
    def __init__(self, fname=os.path.join(config.srcdir, "cars.dat")):
	self.sec = []
	self.ent = []
	self.secname = ''
	bfiles.ArgFile.__init__(self, fname)

    def Parse_c(self, llist):
	self.ParseEnd()
	self.ent = []
	self.secname = llist[1]

    def Parse_m(self, llist):
	self.ent.append(llist.llist[1:3])

    def ParseEnd(self):
	if self.ent:
	    self.sec.append([self.secname, copy.deepcopy(self.ent)])


def RenderCars(pif, cf):
    imax = 0
    print pif.render.FormatTableStart()
    sec = 0
    print pif.render.FormatRowStart()
    for c in cf.sec:
	imax = max(imax, len(c[1]))
	print pif.render.FormatCell(sec, c[0], hdr=True, also={'colspan' : len(c[1][0])})
	sec = sec + len(c[1][0])
    print pif.render.FormatRowEnd()

    for i in range(0, imax):
	print pif.render.FormatRowStart()
	sec = 0
	for c in cf.sec:
	    if i >= len(c[1]):
		for f in c[1][0]:
		    print pif.render.FormatCell(sec, ' ')
		    sec = sec + 1
	    else:
		for f in c[1][i]:
		    if f == 'x':
			print pif.render.FormatCell(sec, pif.render.FormatImageArt('box-sm-x.gif'))
		    elif f:
			print pif.render.FormatCell(sec, "&nbsp;" + f + "&nbsp;")
		    else:
			print pif.render.FormatCell(sec, pif.render.FormatImageArt('box-sm.gif'))
		    sec = sec + 1
	print pif.render.FormatRowEnd()

    print pif.render.FormatTableEnd()


@basics.WebPage
def CarsMain(pif):
    pif.render.PrintHtml()

    db = CarsFile(os.path.join(config.srcdir, pif.FormStr('page', 'cars') + '.dat'))

    print pif.render.FormatHead()
    RenderCars(pif, db)
    print pif.render.FormatTail()

# ------- ----------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
