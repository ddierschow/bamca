#!/usr/local/bin/python

import datetime, os, stat, subprocess, sys, time
import config
import Image, ImageDraw
import imicon
import mbdata
import useful

os.environ['PATH'] += ':/usr/local/bin'

image_content_type = {
    'bmp': 'Content-Type: image/bmp',
    'gif': 'Content-Type: image/gif',
    'ico': 'Content-Type: image/x-icon',
    'jpg': 'Content-Type: image/jpeg',
    'jpeg': 'Content-Type: image/jpeg',
    'png': 'Content-Type: image/png',
    'tif': 'Content-Type: image/tiff',
    'xbm': 'Content-Type: image/x-xbitmap',
    '': 'Content-Type: image/jpeg',
}

image_inputter = {
    'bmp': [['/usr/local/bin/bmptopnm']],
    'gif': [['/usr/local/bin/giftopnm']],
    'ico': [['/usr/local/bin/winicontoppm']],
    'jpg': [['/usr/local/bin/jpegtopnm']],
    'jpeg': [['/usr/local/bin/jpegtopnm']],
    'png': [['/usr/local/bin/pngtopnm']],
    'tif': [['/usr/local/bin/tifftopnm']],
    'xbm': [['/usr/local/bin/xbmtopbm']],
#    '': [['/usr/local/bin/jpegtopnm']],
}
itypes = ['bmp', 'gif', 'ico', 'jpg', 'jpeg', 'png', 'tif', 'xbm']

image_outputter = {
    'bmp': [['/usr/local/bin/ppmtobmp']],
    'gif': [['/usr/local/bin/pnmquant', '256'], ['/usr/local/bin/ppmtogif']],
    'ico': [['/usr/local/bin/ppmtowinicon']],
    'jpg': [['/usr/local/bin/pnmtojpeg']],
    'jpeg': [['/usr/local/bin/pnmtojpeg']],
    'png': [['/usr/local/bin/pnmtopng']],
    '': [['/usr/local/bin/pnmtojpeg']],
}
otypes = ['', 'bmp', 'gif', 'ico', 'jpg', 'png']

s = '_abcdefghijklmnopqrstuvwxyz-'
t = '0123456789012345678901234567'



def get_size(fn):
    try:
	l = pipe_chain(open(fn), import_file(fn) + [["/usr/local/bin/pamfile"]], subprocess.PIPE, verbose=False)
    except IOError:
	raise useful.SimpleError('Could not read ' + fn)
    f = l.split()
    try:
        x = int(f[3])
        y = int(f[5])
    except:
        x = y = 0
    return (x, y)


def img_info(f):
    img = Image.open(f)
    return (img_is_anim(img), img.size[0], img.size[1])


def pipe_chain(inp, pipes, stderr=None, verbose=True):
    ch = '%'
    for pipe in pipes:
        if verbose:
            useful.write_comment(ch, ' '.join(pipe), nonl=True)
        ch = '|'
        proc = subprocess.Popen(pipe, stdin=inp, stdout=subprocess.PIPE, stderr=stderr, close_fds=True)
        inp = proc.stdout
    if verbose:
        useful.write_comment()
    return proc.communicate()[0]


def pipe_convert(src, dst, verbose=False):
    if src == dst:
	return inpf.read()
    ctypes = import_file(src) + export_file(dst)
    return pipe_chain(open(src), ctypes, stderr=subprocess.PIPE, verbose=verbose)


def import_file(fn):
    fn = fn[fn.rfind('/') + 1:]
    fex = fn[fn.rfind('.') + 1:]
    if '?' in fex:
        fex = fex[:fex.find('?')]
    return image_inputter.get(fex, image_inputter['jpg'])


def export_file(nfn, ofn=''):
    nfn = nfn[nfn.rfind('/') + 1:]
    if '.' in nfn:
        fex = nfn[nfn.rfind('.') + 1:]
    else:
        fex = ofn[ofn.rfind('.') + 1:]
    return image_outputter.get(fex, image_outputter['jpg'])


def get_palette(img):
    lut = img.resize((256, 1))
    lut.putdata(range(256))
    return lut.convert("RGB").getdata() 


def corner_color(img, pixel):
    ox, oy = img.size
    if pixel == 'ul':
	pval = img.getpixel((0, 0))
    elif pixel == 'ml':
	pval = img.getpixel((0, oy / 2))
    elif pixel == 'll':
	pval = img.getpixel((0, oy - 1))
    elif pixel == 'um':
	pval = img.getpixel((ox / 2, 0))
    elif pixel == 'mm':
	pval = img.getpixel((ox / 2, oy / 2))
    elif pixel == 'lm':
	pval = img.getpixel((ox / 2, oy - 1))
    elif pixel == 'ur':
	pval = img.getpixel((ox - 1, 0))
    elif pixel == 'mr':
	pval = img.getpixel((ox - 1, ox / 2))
    elif pixel == 'lr':
	pval = img.getpixel((ox - 1, oy - 1))
    else:
	return None
    if img.mode == 'P':
	palette = get_palette(img)
	pval = palette[pval]
    return pval


def img_is_anim(img):
    try:
	img.seek(1)
	return True
    except EOFError:
	return False


def is_anim(f):
    try:
	img = Image.open(f)
    except:
	return False
    return img_is_anim(img)

# transforms

rot_flip_keys = ['rr', 'rh', 'rl', 'fh', 'fv']
rot_flip_transforms = [
    ['/usr/local/bin/pamflip', '-r270'],
    ['/usr/local/bin/pamflip', '-r180'],
    ['/usr/local/bin/pamflip', '-r90'],
    ['/usr/local/bin/pamflip', '-lr'],
    ['/usr/local/bin/pamflip', '-tb'],
]
rot_flip_axes = [True, False, True, False, False]
def rot_flip(rf):
    return [rot_flip_transforms[x] for x in range(len(rf)) if rf[x]]


def fix_axes(rf, xts, yts):
    if reduce(lambda x,y: x != y, [True for x in range(len(rf)) if rf[x] and rot_flip_axes[x]], False):
	return yts, xts
    return xts, yts


def resize(x=None, y=None):
    if not x and not y:
        return []
    if not y:
        return [["/usr/local/bin/pamscale", "-xsize", str(x)]]
    if not x:
        return [["/usr/local/bin/pamscale", "-ysize", str(y)]]
    return [["pamscale", "-xsize", str(x), "-ysize", str(y)]]


def cut(x1, y1, x2, y2):
    return [["/usr/local/bin/pamcut", "-top", str(y1), "-height", str(y2 - y1), "-left", str(x1), "-width", str(x2 - x1)]]


# Reshaping assemblers

def set_shape_sizes(x1, x2, y1, y2, xts, yts, xos, yos):
    #xos, yos = get_size(tdir + '/' + fil)
    xcs = x2 - x1
    ycs = y2 - y1
    ratio = float(xts) / float(yts)
    print "set_shape_sizes", x1, y1, "/", x2, y2, ';', xts, yts, ';', xcs, ycs, ';', xos, yos, ';', ratio, "<br>"
    if xcs < xts:
        if xos < xts:
            print "fix x to orig /"
            x1 = 0
            x2 = xos - 1
        else:
            print "fix x to target /"
            x1 = max(0, x1 - (xts - xcs) / 2)
            x2 = x1 + xts
    if ycs < yts:
        if yos < yts:
            print "fix y to orig /"
            y1 = 0
            y2 = yos - 1
        else:
            print "fix y to target /"
            y1 = max(0, y1 - (yts - ycs) / 2)
            y2 = y1 + yts
    print "(", x1, y1, "/", x2, y2, ")"
    xcs = x2 - x1
    ycs = y2 - y1
    # might revisit this, for images that are off center this might not be right
    if xts <= xos and yts <= yos and xcs <= xts and ycs <= yts:
        print "shape expanding x and y<br>"
        x1 = x1 - (xts - xcs) / 2
        x2 = x1 + xts
        y1 = y1 - (yts - ycs) / 2
        y2 = y1 + yts
        print "(", x1, y1, ") (", x2, y2, ")"
        x1, x2, y1, y2 = normalize(x1, x2, y1, y2, xos, yos)
    elif xcs < int(float(ycs) * ratio):
        # too tall - expand x
        print "shape expanding x"
        nxs = int(float(ycs) * ratio)
        nx1 = x1 - (nxs - xcs) / 2
        nx2 = nx1 + nxs
        if nxs > xos:
            print "off both edges<br>"
            nx1 = 0
            nx2 = xos
        elif nx1 < 0:
            print "off the left<br>"
            nx2 = nx2 - nx1
            nx1 = 0
        elif nx2 > xos:
            print "off the right<br>"
            nx1 = nx1 - (nx2 - xos)
            nx2 = xos
        else:
            pass
            print "on<br>"
        x1 = nx1
        x2 = nx2
    elif xcs > int(float(ycs) * ratio):
        # too wide - expand y
        print "shape expanding y"
        nys = int(float(xcs) / ratio)
        ny1 = y1 - (nys - ycs) / 2
        ny2 = ny1 + nys
        if nys > yos:
            print "off both edges<br>"
            ny1 = 0
            ny2 = yos
        elif ny1 < 0:
            print "off the top<br>"
            ny2 = nys
            ny1 = 0
        elif ny2 > yos:
            print "off the bottom<br>"
            #ny1 = ny1 - (ny2 - yos)
            ny1 = yos - nys
            ny2 = yos
        else:
            pass
            print "on<br>"
        y1 = ny1
        y2 = ny2
    else:
        print "shape as is<br>"
        # hit the jackpot, Mel!
        pass
    print 'set_shape_sizes returned', x1, y1, '/', x2, y2, '->', x2 - x1, y2 - y1, '<br>'
    return x1, x2, y1, y2


def normalize(x1, x2, y1, y2, xm, ym):
    print 'normalize', x1, y1, "/", x2, y2, "orig", xm, ym
    if x1 < 0:
        x2 = x2 - x1
        x1 = 0
        print "x1"
    if y1 < 0:
        y2 = y2 - y1
        y1 = 0
        print "y1"
    if x2 >= xm:
        x1 = x1 - (x2 - xm)
        x2 = xm
        print "x2"
    if y2 >= ym:
        y1 = y1 - (y2 - ym)
        y2 = ym
        print "y2"
    print 'returns', x1, y1, "/", x2, y2, '<br>'
    return x1, x2, y1, y2


def shaper(pth, nname, bound, target_size, original_size, rf):
    xts, yts = target_size
    x1, y1, x2, y2 = bound
    xcs = x2 - x1
    ycs = y2 - y1
    xos, yos = original_size

    print 'Shape :', pth, ': bounds', x1, y1, x2, y2, 'bound size', xcs, ycs, 'target size', xts, yts, '<br>'
    if xts and yts:
        x1, x2, y1, y2 = set_shape_sizes(x1, x2, y1, y2, xts, yts, xos, yos)
        xcs = x2 - x1
        ycs = y2 - y1

        if xcs > xts:
            print "shrinking"
	    xts, yts = fix_axes(rf, xts, yts)
            ofi = pipe_chain(open(pth),
                    import_file(pth) +
                    cut(x1, y1, x2, y2) +
                    rot_flip(rf) +
                    resize(x=xts) +
                    export_file(nname, pth))
        elif xcs < xts:
            dx = xts - xcs
            dy = yts - ycs
            x1, x2, y1, y2 = normalize(x1, x2, y1, y2, xts, yts)
            print "expanding", x1, x2, y1, y2
	    xts, yts = fix_axes(rf, xts, yts)
            ofi = pipe_chain(open(pth),
                    import_file(pth) +
                    cut(x1, y1, x2, y2) +
                    rot_flip(rf) +
                    export_file(nname, pth))
        elif xos == xts and yos == yts and xos == xcs and yos == ycs:
            print "copying"
            ofi = open(pth).read()
        else:
            print "cutting"
	    xts, yts = fix_axes(rf, xts, yts)
            ofi = pipe_chain(open(pth),
                    import_file(pth) +
                    cut(x1, y1, x2, y2) +
                    rot_flip(rf) +
                    export_file(nname, pth))

    else:

        if xts < x2 - x1:
            print "trim shrinking x"
	    xts, yts = fix_axes(rf, xts, yts)
            ofi = pipe_chain(open(pth),
                    import_file(pth) +
                    cut(x1, y1, x2, y2) +
                    rot_flip(rf) +
                    resize(x=xts) +
                    export_file(nname, pth))
        elif yts < y2 - y1:
            print "trim shrinking y"
	    xts, yts = fix_axes(rf, xts, yts)
            ofi = pipe_chain(open(pth),
                    import_file(pth) +
                    cut(x1, y1, x2, y2) +
                    rot_flip(rf) +
                    resize(y=yts) +
                    export_file(nname, pth))
        else:
            print "trim cutting"
	    xts, yts = fix_axes(rf, xts, yts)
            ofi = pipe_chain(open(pth),
                    import_file(pth) +
                    cut(x1, y1, x2, y2) +
                    rot_flip(rf) +
                    export_file(nname, pth))

    print '<br>'
    return ofi


def shrinker(pth, nname, bound, maxsize, rf):
    print 'shrinker', pth, nname, bound, maxsize, '<br>'
    x1, y1, x2, y2 = bound
    xcs = x2 - x1
    ycs = y2 - y1
    xts, yts = maxsize
    if not xts:
        xts = xcs
    if not yts:
        yts = ycs
    print x1, y1, x2, y2, ':', xcs, ycs, ':', xts, yts, '<br>', pth, '<br>'
    if xcs == xts and ycs == yts:
        print "cutting", '<br>'
	xts, yts = fix_axes(rf, xts, yts)
        ofi = pipe_chain(open(pth),
                import_file(pth) +
                cut(x1, y1, x1 + xcs, y1 + ycs) +
                rot_flip(rf) +
                export_file(nname, pth))
    elif xts/xcs < yts/ycs:
        print "shrinking x", '<br>'
	xts, yts = fix_axes(rf, xts, yts)
        ofi = pipe_chain(open(pth),
                import_file(pth) +
                cut(x1, y1, x1 + xcs, y1 + ycs) +
                rot_flip(rf) +
                resize(x=xts) +
                export_file(nname, pth))
    else:
        print "shrinking y", '<br>'
	xts, yts = fix_axes(rf, xts, yts)
        ofi = pipe_chain(open(pth),
                import_file(pth) +
                cut(x1, y1, x1 + xcs, y1 + ycs) +
                rot_flip(rf) +
                resize(y=yts) +
                export_file(nname, pth))
    return ofi


def cropper(pth, nname, bound, rf):
    x1, y1, x2, y2 = bound
    print 'crop', x1, y1, x2, y2, ':', x2-x1, y2-y1, ':', rf, '<br>', pth, '<br>'
    print "cutting", '<br>'
    ofi = pipe_chain(open(pth),
            import_file(pth) +
            cut(x1, y1, x2, y2) +
            rot_flip(rf) +
            export_file(nname, pth))
    return ofi


# PIL based
def wiper(pth, bound, original_size, wipev, wipeh):
    print 'wiper', pth, bound, original_size, wipev, wipeh, '<br>'
    img = Image.open(pth)
    img = img.convert('RGB')
    xos, yos = original_size
    xl, yt, xr, yb = bound
    if xl > xr:
        x = xl
        xl = xr
        xr = x
    if yt > yb:
        y = yt
        yt = yb
        yb = y
    xr -= 1
    yb -= 1
    x1, y1, x2, y2 = xl, yt, xr, yb

    def wiper_copy(img, xf1, yf1, xf2, yf2, xt1, yt1, xt2, yt2):
	#print ('%3d ' * 8) % (xf1, yf1, xf2 + 1, yf2 + 1, xt1, yt1, xt2 + 1, yt2 + 1)
	cp = img.crop((xf1, yf1, xf2 + 1, yf2 + 1))
	img.paste(cp, (xt1, yt1, xt2 + 1, yt2 + 1))

    while 1:
        if x1 > x2 or y1 > y2:
            break
        if wipev:
            if y1 != 0:
                wiper_copy(img, x1, yt, x2, yt, x1, y1, x2, y1)
                y1 += 1
            if x1 > x2 or y1 > y2:
                break
            if y2 != yos - 1:
                wiper_copy(img, x1, yb, x2, yb, x1, y2, x2, y2)
                y2 -= 1
        elif wipeh:
            if x1 != 0:
                wiper_copy(img, xl, y1, xl, y2, x1, y1, x1, y2)
                x1 += 1
            if x1 > x2 or y1 > y2:
                break
            if x2 != xos - 1:
                wiper_copy(img, xr, y1, xr, y2, x2, y1, x2, y2)
                x2 -= 1
        else:
            if y1 != 0:
                wiper_copy(img, x1, yt, x2, yt, x1, y1, x2, y1)
                y1 += 1
            if x1 != 0:
                wiper_copy(img, xl, y1, xl, y2, x1, y1, x1, y2)
                x1 += 1
            if x1 > x2 or y1 > y2:
                break
            if y2 != yos - 1:
                wiper_copy(img, x1, yb, x2, yb, x1, y2, x2, y2)
                y2 -= 1
            if x2 != xos - 1:
                wiper_copy(img, xr, y1, xr, y2, x2, y1, x2, y2)
                x2 -= 1
    return img


# PIL based
def padder(pth, target_size):
    print 'padder', pth, target_size, '<br>'
    img = Image.open(pth)
    img = img.convert('RGB')

    xos, yos = img.size
    xts = target_size[0] if target_size[0] else xos
    yts = target_size[1] if target_size[1] else yos
    if img.size == (xts, yts):
	return img
    if xos > xts or yos > yts:
	print "original larger than new"
	return img
    img = img.convert('RGB')

    nc = (0,0,0)
    bc = None

    sx = (xts - xos) /2
    sy = (yts - yos) /2
    ex = sx + xos - 1
    ey = sy + yos - 1

    # |0   |s       e|    |n
    # |    |<-- o -->|    |
    # |<------- n ------->|

    nimg = Image.new(img.mode, (xts, yts), nc)
    for x in range(0, xos):
	for y in range(0, yos):
	    nimg.putpixel((sx + x, sy + y), img.getpixel((x, y)))
    for x in range(0, sx):
	for y in range(0, yts):
	    nimg.putpixel((x, y), nimg.getpixel((sx, y)))
    for x in range(ex + 1, xts):
	for y in range(0, yts):
	    nimg.putpixel((x, y), nimg.getpixel((ex, y)))
    for y in range(0, sy):
	for x in range(0, xts):
	    nimg.putpixel((x, y), nimg.getpixel((x, sy)))
    for y in range(ey + 1, yts):
	for x in range(0, xts):
	    nimg.putpixel((x, y), nimg.getpixel((x, ey)))

    return nimg


# understands 0-9 A-Z & ' + - .  /

def iconner(in_path, name, logo=None, isizex=100, isizey=100):
    if not os.path.exists(in_path):
        print 'no original file', in_path
        return

    thumb = Image.open(in_path)
    if thumb.size[1] != 120:
        print 'bad original size', thumb.size
        return
    thumb = thumb.resize((isizex, isizex * thumb.size[1] / thumb.size[0]), Image.NEAREST)
    banner = Image.open(logo)

    text = imicon.Icon(isizex, isizey)
    top = banner.size[1] + thumb.size[1]
    texttop = isizey - 6 - (6 * len(name)) / 2
    for n in name:
        if len(n) > isizex / 6:
            text.charset("3x5.font")
            left = 50 - len(n) * 2
        else:
            text.charset("5x5.font")
            left = 50 - len(n) * 3
        text.string(left, texttop, n.upper())
        texttop = texttop + 6
    iconimage = text.getimage()

    iconimage.paste(banner, ((isizex - banner.size[0]) / 2, 0))
    iconimage.paste(thumb, ((isizex - thumb.size[0]) / 2, banner.size[1]))

    # write out as png and job off the final conversion to netpbm.
    # doing this because I don't like how PIL disses GIFs.
    tmp_pth = '/tmp/iconner.png'
    iconimage.save(tmp_pth)
    ofi = pipe_convert(tmp_pth, '.gif', verbose=True)
    os.unlink(tmp_path)
    return ofi


def stitcher(ofn, fa, is_horiz, minx, miny, limit_x, limit_y, verbose=False):
    if is_horiz:
        print 'horizontal'

	if limit_y:
	    miny = min(miny, limit_y)
	resize_x = 0
	resize_y = miny
	cat = ['pnmcat', '-lr']

    else:
        print 'vertical'

	if limit_x:
	    minx = min(minx, limit_x)
	resize_x = minx
	resize_y = 0
	cat = ['pnmcat', '-tb']

    for f in fa:
	pipes = import_file(f[0]) + \
		cut(f[3], f[4], f[5], f[6]) + \
		resize(x=resize_x, y=resize_y)
	outf = pipe_chain(open(f[0]), pipes, verbose=verbose)
	if verbose:
	    print '>', f[0] + '.pnm', '<br>'
	open(f[0] + '.pnm', 'w').write(outf)
	cat.append(f[0] + '.pnm')
    outf = pipe_chain(open('/dev/null'), [cat] + export_file(ofn), verbose=verbose)

    if verbose:
	print '>', ofn, '<br>'
    open(ofn, 'w').write(outf)

    if not verbose:
	for f in fa:
	    os.unlink(f[0] + '.pnm')




class Drawer:

    def __init__(self, fn, ofn=None):
	self.cmdfile = fn
	self.sx = 100
	self.sy = 100
	self.cx = 0
	self.cy = 0
	self.col = (0, 0, 0)
	self.drw = None
	self.img = None

	self.process()
	self.save(ofn)

    def at(self, args):
	self.cx, self.cy = map(int, args[0].split(','))

    def line(self, args):
	if args[0]:
	    self.cx, self.cy = map(int, args[0].split(','))
	for arg in args[1:]:
	    nx, ny = map(int, arg.split(','))
	    self.drw.line(((self.cx, self.cy), (nx, ny)), fill=self.col)
	    self.cx, self.cy = nx, ny

    def fill(self, args):
	if args[0]:
	    self.cx, self.cy = map(int, args[0].split(','))
	nx, ny = map(int, args[1].split(','))
	self.drw.rectangle(((self.cx, self.cy), (nx, ny)), fill=self.col, outline=self.col)
	self.cx, self.cy = nx, ny

    def box(self, args):
	if args[0]:
	    self.cx, self.cy = map(int, args[0].split(','))
	nx, ny = map(int, args[1].split(','))
	self.drw.rectangle(((self.cx, self.cy), (nx, ny)), outline=self.col)
	self.cx, self.cy = nx, ny

    def point(self, args):
	self.cx, self.cy = map(int, args[0].split(','))
	self.drw.point((self.cx, self.cy), fill=self.col)

    def arc(self, args):
	nx, ny = map(int, args[0].split(','))
	self.drw.arc((self.cx, self.cy, nx, ny), int(args[1]), int(args[2]), fill=self.col)

    def chord(self, args):
	nx, ny = map(int, args[0].split(','))
	self.drw.chord((self.cx, self.cy, nx, ny), int(args[1]), int(args[2]), fill=self.col)

    def pie(self, args):
	nx, ny = map(int, args[0].split(','))
	self.drw.pieslice((self.cx, self.cy, nx, ny), int(args[1]), int(args[2]), fill=self.col)

    def write(self, args):
	self.drw.text((self.cx, self.cy), args[0], fill=self.col)

    def color(self, args):
	self.col = tuple(map(int, args[0].split(',')))

    def polygon(self, args):
	lst = []
	if not args[0]:
	    lst = [(self.cx, self.cy)]
	    args = args[1:]
	lst.extend(map(lambda x: tuple(map(int, x.split(','))), args))
	self.drw.polygon(lst, outline=self.col)

    def polyfil(self, args):
	lst = []
	if not args[0]:
	    lst = [(self.cx, self.cy)]
	    args = args[1:]
	lst.extend(map(lambda x: tuple(map(int, x.split(','))), args))
	self.drw.polygon(lst, outline=self.col, fill=self.col)

    def process(self):
	for cmd in open(self.cmdfile).readlines():
	    cmd, args = cmd.strip().split('\t', 1)
	    arg = args.split(';')
	    if cmd == 'canvas':
		sz = arg[0].split(',')
		self.sx = int(sz[0])
		self.sy = int(sz[1])
		self.col = tuple(map(int, arg[1].split(',')))
		self.img = Image.new("RGB", (self.sx, self.sy), self.col)
		self.drw = ImageDraw.Draw(self.img)
	    elif cmd in self.__class__.__dict__:
		print >> sys.stderr, '+', cmd, arg
		ret = self.__class__.__dict__[cmd](self, arg)
	    else:
		print >> sys.stderr, '?', cmd, args

    def save(self, ofn):
	if ofn:
	    self.img.save(ofn)
	else:
	    self.img.save(sys.stdout, 'PPM')


class ActionForm(object):
    def __init__(self):
	pass

    def read(self, form):
	self.tdir = form.get_str('d')
	self.fn = form.get_str('fi')
	self.nname = form.get_str('newname')
	self.man = form.get_str('man')
	self.cat = form.get_str('cat')
	self.ov = form.get_bool('ov', False)
	self.cpmv = form.get_str('cpmv', 'c')
	self.mv = self.cpmv == 'm'
	self.delete = form.get_bool('delete')
	self.selcat = form.get_bool('selcat')
	self.dest = form.get_str('moveto')
	self.rename = form.get_bool('rename')
	self.lib = form.get_bool('lib')
	self.mvbin = form.get_bool('mvbin')
	self.select = form.get_bool('select')
	self.var = form.get_str('newvar')
	self.suff = form.get_str('suff')
	if not self.var:
	    self.var = form.get_str('v')
	self.pref = form.get_str('pref')
	self.inc = form.get_str('inc')
	self.cycle = form.get_bool('cy')
	return self

    def action(self, pif, tdir=None, fn=None):
	if not fn:
	    fn = self.fn
	if not tdir:
	    tdir = self.tdir
	ret = {'fn': fn, 'dir': tdir, 'act': True}
	from_path = os.path.join(tdir, fn)
	to_dir = to_name = ''
	if self.delete:
	    useful.file_delete(from_path)
	elif self.selcat:
	    if not self.nname or not self.dest:
		useful.warn('What?')
	    else:
		to_dir = self.dest
		to_name = self.nname
	elif self.rename:
	    if not self.nname:
		useful.warn('What?')
	    else:
		to_dir = tdir
		to_name = self.nname
	elif self.lib:
	    if not self.man:
		useful.warn('What?')
	    elif not os.path.exists(os.path.join(config.LIB_MAN_DIR, self.man)):
#		man2 = pif.dbh.fetch_alias(self.man)
#		if not man2:
		    useful.warn('bad destination')
#		else:
#		    useful.file_mover(from_path, os.path.join(config.LIB_MAN_DIR, man2['ref_id'].lower(), fn), mv=self.mv, ov=self.ov)
	    else:
		to_dir = os.path.join(config.LIB_MAN_DIR, man)
		to_name = self.nname
	elif self.mvbin:
	    if not os.path.exists(os.path.join('lib/new', self.cat)):
		useful.war('bad destination')
	    else:
		to_dir = os.path.join('lib', 'new', self.cat)
		to_name = self.nname
	elif self.select:
	    inc = self.inc
	    if not self.man:
		#self.man = tdir[tdir.rfind('/') + 1:]
		useful.warn('Huh? (select, no man)')
	    else:
		ddir = './' + config.IMG_DIR_MAN
		dnam = self.man
		if self.var:
		    ddir = './' + config.IMG_DIR_VAR
		    dnam = dnam + '-' + self.var
		    if self.pref:
			dnam = self.pref + '_' + dnam
		elif self.pref and self.adds.find(self.pref) >= 0:
		    ddir = './' + config.IMG_DIR_ADD
		    dnam = self.pref + '_' + dnam
		    if self.suff:
			dnam += '-' + self.suff
		    self.inc = True
		elif self.pref:
		    dnam = self.pref + '_' + dnam
		else:
		    useful.warn("What?")
		    dnam = ''
		if dnam:
		    to_name = dnam.lower() + '.jpg'
		    to_dir = ddir
	else:
	    ret['act'] = False
	if to_dir:
	    useful.file_mover(from_path, os.path.join(to_dir, to_name), mv=self.mv, ov=self.ov, inc=self.inc)
	    ret['fn'] = to_name
	    ret['dir'] = to_dir
	return ret

    sel_cat = [
	['unsorted', 'unsorted'],
	['a',       'Accessories'],
	['bigmx',   'BigMX'],
	['blister', 'Blister'],
	['cc',      'Carrying Case'],
	['cat',     'Catalogs'],
	['coll',    'Collectibles'],
	['commando', 'Commando'],
	['cy',      'Convoys'],
	['copies',  'Copies'],
	['disp',    'Displays'],
	['e',       'Early'],
	['game',    'Games'],
	['g',       'Giftsets'],
	['gw',      'Giftware'],
	['gf',      'Graffic'],
	['k',       'Kings'],
	['moko',    'Moko'],
	['mw',      'Motorways'],
	['mult',    'Multiples'],
	['o',       'Other'],
	['packs',   'Packs'],
	['ps',      'Play Sets'],
	['prem',    'Premieres'],
	['rt',      'Real Talkin'],
	['rb',      'Roadblasters'],
	['r',       'Roadway'],
	['robotech', 'RoboTech'],
	['sb',      'Sky Busters'],
	['supergt', 'SuperGT'],
	['tp',      'TwinPacks'],
	['wr',      'White Rose'],
	['zing',    'Zings'],
    ]

    adds = 'abdefipr'
    sel_pref = [
	['', ''],
	['t', 'thumbnail'],
	['s', 'small'],
	['c', 'compact'],
	['m', 'medium'],
	['l', 'large'],
	['h', 'huge'],
	['g', 'gigantic'],

	['f', 'advertisement'],
	['b', 'baseplate'],
	['z', 'comparison'],
	['a', 'custom'],
	['d', 'detail'],
	['e', 'error'],
	['i', 'interior'],
	['p', 'prototype'],
	['r', 'real'],
	['x', 'box'],
    ]

    sel_moveto = [
	['',        ''],
	[config.IMG_DIR_MATTEL,     'mattel'],
	[config.IMG_DIR_MT_LAUREL,  'mtlaurel'],
	[config.IMG_DIR_TYCO,       'tyco'],
	[config.IMG_DIR_UNIV,       'univ'],
	[config.IMG_DIR_LSF,        'lsf'],
	[config.IMG_DIR_LRW,        'lrw'],
	[config.IMG_DIR_LESNEY,     'lesney'],
	[config.IMG_DIR_ACC,        'acc'],
	[config.IMG_DIR_ADS,        'ads'],
	[config.IMG_DIR_BLISTER,    'blister'],
	[config.IMG_DIR_BOX,        'box'],
	[config.IMG_DIR_COLL_43,    'mcoll'],
	[config.IMG_DIR_ERRORS,     'errors'],
	[config.IMG_DIR_KING,       'king'],
	[config.IMG_DIR_PACK,       'packs'],
	[config.IMG_DIR_COLL_64,    'prem'],
	[config.IMG_DIR_SERIES,     'series'],
	[config.IMG_DIR_SKY,        'sky'],
    ]

    def write(self, pif, fn):
#	root, ext = useful.root_ext(fn.strip())
#	print '<a href="?d=%s">%s</a> / ' % (self.tdir, self.tdir)
#	print '<a href="/%s/%s">%s</a>' % (self.tdir, fn, fn)
#	print '<hr>'
#	print '<self action="upload.cgi">'

	szname = ''
	x = y = 0
	if os.path.exists(self.tdir + '/' + fn):
	    x, y = get_size(self.tdir + '/' + fn)
	    print (x, y)
	    for (szname, szxy) in zip(mbdata.image_size_names, mbdata.image_size_sizes):
		if x <= szxy[0]:
		    break
	print '<input type=hidden name="act" value="1">'
	print '<input type=hidden name="d" value="%s">' % self.tdir
	print '<input type=hidden name="fi" value="%s">' % fn
	print '<a href="/cgi-bin/imawidget.cgi?d=%s&f=%s&v=%s&cy=%s">%s</a>' % (self.tdir, fn, self.var, self.cycle, pif.render.format_button('edit'))
	print pif.render.format_button_input('delete')
	print pif.render.format_button('stitch', 'stitch.cgi?fn_0=%s&submit=1&q=&fc=1' % (self.tdir + '/' + fn))
	print 'New name: <input type="text" size="32" name="newname" value="%s">' % fn
	print pif.render.format_button_input('rename')
	print ''.join(pif.render.format_radio('cpmv', [('c', 'copy'), ('m', 'move')], self.cpmv))
	if pif.is_allowed('m'):  # pragma: no cover
	    if self.ov:
		print '<input type=checkbox name="ov" value="1" checked>'
	    else:
		print '<input type=checkbox name="ov" value="1">'
	    print 'overwrite<br>'
	    print 'Man: <input type="text" size="12" name="man" value="%s">' % self.man #get_man(pif)
	    print pif.render.format_button_up_down('man')
	    print pif.render.format_button_input('move to library', 'lib')
	    print 'Category:', pif.render.format_select('cat', self.sel_cat, self.cat)
	    print pif.render.format_button_input('move to bin', 'mvbin')
	    print pif.render.format_checkbox("cy", [("1", "cycle")], checked=[str(int(self.cycle))])
	    print '<input type=checkbox name="inc" value="1"> increment name'
	    print '<br>Variation: <input type="text" size="5" name="newvar" value="%s">' % self.var
	    print 'Prefix:', pif.render.format_select('pref', self.sel_pref, self.pref)
	    print 'Suffix: <input type="text" size="5" name="suff" value="">'
	    print pif.render.format_button_input('select to casting', 'select')
	    print 'Move to:', pif.render.format_select('moveto', self.sel_moveto, self.dest)
	    print pif.render.format_button_input('select to category', 'selcat')

	return x, y


def get_dir(tdir):
    fl = os.listdir(tdir)
    fl.sort()
    dl = list()  # directories
    gl = list()  # graphics
    ol = list()  # other files
    sl = list()  # dat files
    xl = list()  # executables

    for f in fl:
        root, ext = useful.root_ext(f)
        if os.path.exists(tdir + '/' + f):
            if f[-1] == '~' or f == '.crcs' or f[-4:] == '.pyc':
                continue
            fstat = os.stat(tdir + '/' + f)
            perms = fstat.st_mode
            if os.path.isdir(tdir + '/' + f):
                dl.append(f)
            elif ext == 'dat':
                sl.append(f)
            elif ext in image_inputter:
                gl.append(f)
            elif stat.S_IMODE(perms) & stat.S_IXUSR:
                xl.append(f)
            else:
                ol.append(f)
    return dl, gl, ol, sl, xl


def image_star(image_path, pic_id='', halfstar=False, target_x=400, target_y=0):
    if pic_id is None:
        return 'stargray.gif'
    if not os.path.exists(image_path):
        if pic_id:
            return 'staryellow.gif'
        return 'starwhite.gif'
    try:
        img = Image.open(image_path)
    except:
        return 'staryellow.gif'
    ix, iy = img.size
    if target_x:
	if ix < target_x / 2:
	    return 'starred.gif'
	if ix < target_x:
	    return 'stargreen.gif'
	if ix > target_x:
	    return 'starblue.gif'
	if halfstar:
	    return 'starhalf.gif'
    else:
	if iy < target_y / 2:
	    return 'starred.gif'
	if iy < target_y:
	    return 'stargreen.gif'
	if iy > target_y:
	    return 'starblue.gif'
	if halfstar:
	    return 'starhalf.gif'
    return 'star.gif'


def read_presets(pdir):
    if os.path.exists(os.path.join(pdir, '.ima')):
	presets = eval(open(os.path.join(pdir, '.ima')).read())
	#print 'read_presets:', presets, '<br>'
	return presets
    return dict()


def write_presets(pdir, presets, force=False):
    if force or os.path.exists(os.path.join(pdir, '.ima')):
	#print 'write_presets:', presets, '<br>'
	open(os.path.join(pdir, '.ima'), 'w').write(str(presets))


def update_presets(pdir, values):
    if os.path.exists(os.path.join(pdir, '.ima')):
	presets = read_presets(pdir)
	presets.update(values)
	write_presets(pdir, presets)
