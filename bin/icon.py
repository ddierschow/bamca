#!/usr/local/bin/python

import os, sys
import Image

#==========================

# The icon class!

class icon:
    def __init__(self, w, h):
	self.width = w
	self.height = h
	self.image = [ 0 ] * (w*h)
	self.chars = font("5x6.font")
	#self.charset("5x6.font")
	self.palette = { 0 : (255,255,255), 1 : (0,0,0) }
	self.fgcolor = 1
	self.bgcolor = 0

    def set(self, x, y, v=1):
	if v:
	    v = self.fgcolor
	elif self.bgcolor == None:
	    return
	else:
	    v = self.bgcolor
	if (y < self.height and x < self.width):
	    self.image[y * self.width + x] = v

    def get(self, x, y):
	if (y < self.height and x < self.width):
	    return self.image[y * self.width + x]
	return 0

    def tog(self, x, y):
	if (y < self.height and x < self.width):
	    if self.image[y * self.width + x] == self.bgcolor:
		self.image[y * self.width + x] = self.fgcolor
	    elif self.bgcolor != None:
		self.image[y * self.width + x] = self.bgcolor
	    else:
		self.image[y * self.width + x] = 0

    def saveicn(self, f):
	'''Old-style, SUN format, monochrome icon files.'''
	iX = iY = 0
	uVal = 0
	iBit = 0
	iImg = 0
	BPW = 16

	icnhdr = "/* Format_version=1, Width=%d, Height=%d, Depth=1, Valid_bits_per_item=%d\n */\n"

	f.write(icnhdr % (self.width, self.height, BPW ))
	for iY in range(0, self.height):
	    f.write("\t")
	    for iX in range(0, (self.width - 1)/ BPW + 1):
		uVal = iBit = 0
		while ( (iX * BPW + iBit < self.width) and (iBit < BPW)):
		    val = int(not not self.image[iImg])
		    uVal = uVal | val << (15 - iBit)
		    iImg = iImg + 1
		    iBit = iBit + 1
		f.write( "0x%4.4X" % (uVal & 0xFFFF) )
		f.write( "," )
	    f.write( "\n" )

    def invert(self, x, y, w, h):
	for iY in range(0, h):
	    for iX in range(0, w):
		self.tog(x + iX, y + iY)

    def merge(self, x, y, w, h, lImage):
	for iY in range(h-1, -1, -1):
	    for iX in range(w-1, -1, -1):
		self.set(x + iX, y + iY, lImage & 1)
		lImage >>= 1

    def box(self, x, y, w, h):
	for iCh in range(y, y+h):
	    self.set(x, iCh)
	    self.set(x + w, iCh)
	for iCh in range(x, x+w):
	    self.set(iCh, y)
	    self.set(iCh, y + h)

    def string(self, x, y, s):
	xt = x
	for c in s:
	    if c == '\n':
		xt = x
		y = y + self.chars.height + 1
		continue
	    ch = self.chars.get(c, (0,0))
	    if xt + ch[0] > self.width:
		xt = x 
		y = y + self.chars.height + 1
	    self.merge(xt, y, ch[0], self.chars.height, ch[1])
	    xt += ch[0] + 1

    def number(self, x, y, v):
	t = abs(v)
	c = 0
	st = ''
	while t:
	    ch = str(t % 10)
	    st = ch + st
	    t /= 10
	    c = c + self.chars[ch][0] + 1
	self.string(x, y, st)

    def save(self, fname, fmt=None):
	im = self.getimage()
	im.save(fname, fmt)

    def getimage(self):
	im = Image.new("RGBA", (self.width, self.height))

	for iY in range(0, self.height):
	    for iX in range(0, self.width):
		im.putpixel((iX, iY), self.palette[self.get(iX, iY)])

	return im

    def background(self, rgb):
	c = self.setpalette(rgb)
	self.bgcolor = c

    def foreground(self, rgb):
	c = self.setpalette(rgb)
	self.fgcolor = c

    def setpalette(self, rgb):
	c = 0
	for i in self.palette.items():
	    if i[1] == rgb:
		return i[0]
	    if i[0] > c:
		c = i[0]
	self.palette[c + 1] = rgb
	return c + 1


#==========================

# The font class!

class font:
    def __init__(self, fname):
	f = None
	for path in sys.path:
	    try:
		fp = os.path.join(path, fname)
		f = open(fp)
	    except:
		continue
	    break

	if f:
	    inp = f.readlines()

	    self.chars = {}
	    xall = x = y = 0
	    v = 0L
	    c = None
	    for line in inp:
		if line[0] == '\t':
		    if not c:
			print '*** badly formed input'
		    line = line[1:] + " " * x
		    line = line[:x]
		    for p in line:
			v = v * 2
			if p == '#':
			    v = v + 1
		elif line[0] == 'x':
		    x = xall = int(line[1:])
		elif line[0] == 'y':
		    self.height = y = int(line[1:])
		elif line[0] == '=':
		    if c:
			self.chars[c] = (x,v)
			self.chars.setdefault(c.lower(), (x,v))
		    c = line[1]
		    v = 0
		    if not xall:
			x = int(line[2:])
	    if c:
		self.chars[c] = (x,v)
		self.chars.setdefault(c.lower(), (x,v))

    def __get__(self, key):
	return self.chars[key]

    def get(self, key, defval=None):
	return self.chars.get(key, defval)


if __name__ == '__main__':
    pass


if __name__ == '__main__': # pragma: no cover
    pass

