#!/usr/local/bin/python

from functools import reduce
import glob
from io import open
import os
from PIL import Image, ImageDraw
import stat
import sys

import bfiles
import config
import imicon
import mbdata
import tumblr
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
    'webp': 'Content-Type: image/webp',
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
    # 'webp': [['/usr/local/bin/dwebp', '-pam']],
    'xbm': [['/usr/local/bin/xbmtopbm']],
    # '': [['/usr/local/bin/jpegtopnm']],
}
itypes = ['bmp', 'gif', 'ico', 'jpg', 'jpeg', 'png', 'tif', 'xbm']

image_outputter = {
    'bmp': [['/usr/local/bin/ppmtobmp']],
    'gif': [['/usr/local/bin/pnmquant', '256'], ['/usr/local/bin/ppmtogif']],
    # 'gif': [['/usr/local/bin/ppmtogif']],
    'ico': [['/usr/local/bin/ppmtowinicon']],
    'jpg': [['/usr/local/bin/pnmtojpeg']],
    'jpeg': [['/usr/local/bin/pnmtojpeg']],
    'png': [['/usr/local/bin/pnmtopng']],
    # 'webp': [['/usr/local/bin/cwebp']],
    '': [['/usr/local/bin/pnmtojpeg']],
}
otypes = ['', 'bmp', 'gif', 'ico', 'jpg', 'png']

s = '_abcdefghijklmnopqrstuvwxyz-'
t = '0123456789012345678901234567'

img_dir_name = {'.' + x: y for x, y in mbdata.img_dir_name.items()}

movetos = [
    config.IMG_DIR_PROD_MWORLD,
    config.IMG_DIR_PROD_EL_SEG,
    config.IMG_DIR_PROD_MT_LAUREL,
    config.IMG_DIR_PROD_TYCO,
    config.IMG_DIR_PROD_UNIV,
    config.IMG_DIR_PROD_LSF,
    config.IMG_DIR_PROD_LRW,
    config.IMG_DIR_LESNEY,
    config.IMG_DIR_ACC,
    config.IMG_DIR_ADS,
    config.IMG_DIR_BLISTER,
    config.IMG_DIR_BOOK,
    config.IMG_DIR_PROD_BOOK,
    config.IMG_DIR_BOX,
    config.IMG_DIR_CAT,
    config.IMG_DIR_PROD_CODE_2,
    config.IMG_DIR_COLL_43,
    config.IMG_DIR_CONVOY,
    config.IMG_DIR_ERRORS,
    config.IMG_DIR_GAME,
    config.IMG_DIR_ICON,
    config.IMG_DIR_KING,
    config.IMG_DIR_MAKE,
    config.IMG_DIR_PROD_ODDS,
    config.IMG_DIR_PROD_PROMOS,
    config.IMG_DIR_PACKAGE,
    config.IMG_DIR_PICS,
    config.IMG_DIR_SET_PLAYSET,
    config.IMG_DIR_SET_PACK,
    config.IMG_DIR_PROD_PLAYSET,
    config.IMG_DIR_PROD_PACK,
    config.IMG_DIR_PROD_COLL_64,
    config.IMG_DIR_PROD_SERIES,
    config.IMG_DIR_SKY,
]


def open_input_file(pth):
    return open(pth, 'rb')


def open_write_dev_null():
    return open('/dev/null', 'wb')


def get_size(fn):
    try:
        p = useful.pipe_chain(open_input_file(fn), import_file(fn) + [["/usr/local/bin/pamfile"]],
                              stderr=useful.PIPE, verbose=False)
    except IOError:
        raise useful.SimpleError('Could not read ' + fn)
    # print('get_size', p)
    f = p.split()
    try:
        x = int(f[3])
        y = int(f[5])
    except Exception:
        x = y = 0
    return (x, y)


def img_info(f):
    img = Image.open(f)
    return (img_is_anim(img), img.size[0], img.size[1])


def pipe_convert(src, dst, verbose=False):
    if src == dst:
        return open_input_file(src).read()
    ctypes = import_file(src) + export_file(dst)
    return useful.pipe_chain(open_input_file(src), ctypes, stderr=open_write_dev_null(), verbose=verbose)


def import_file(fn):
    # fn = fn[fn.rfind('/') + 1:]
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
        pval = img.getpixel((0, oy // 2))
    elif pixel == 'll':
        pval = img.getpixel((0, oy - 1))
    elif pixel == 'um':
        pval = img.getpixel((ox // 2, 0))
    elif pixel == 'mm':
        pval = img.getpixel((ox // 2, oy // 2))
    elif pixel == 'lm':
        pval = img.getpixel((ox // 2, oy - 1))
    elif pixel == 'ur':
        pval = img.getpixel((ox - 1, 0))
    elif pixel == 'mr':
        pval = img.getpixel((ox - 1, ox // 2))
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
    except Exception:
        return False
    return img_is_anim(img)


def mangler(ofn, ops, nfn):
    intermediate = useful.pipe_chain(open_input_file(ofn), import_file(ofn) + ops,
                                     stderr=open_write_dev_null(), verbose=True)
    open('/tmp/imgfile', 'wb').write(intermediate)
    if nfn.endswith('.gif'):
        pass
        # pnmcolormap 256 myimage.pnm >/tmp/colormap.pnm
        # pnmremap -mapfile=/tmp/colormap.pnm myimage.pnm >myimage256.pnm
        open('/tmp/colormap.pnm', 'wb').write(
            useful.pipe_chain(open('/tmp/imgfile', 'rb'), [['/usr/local/bin/pnmcolormap', '256']],
                              stderr=open_write_dev_null(), verbose=True))
        intermediate = useful.pipe_chain(
            open('/tmp/imgfile', 'rb'), [['/usr/local/bin/pnmremap', '-mapfile=/tmp/colormap.pnm']],
            stderr=open_write_dev_null(), verbose=True)
        open('/tmp/imgfile', 'wb').write(intermediate)
        os.remove('/tmp/colormap.pnm')
    final = useful.pipe_chain(open('/tmp/imgfile', 'rb'), export_file(nfn, ofn),
                              stderr=open_write_dev_null(), verbose=True)
    os.remove('/tmp/imgfile')
    return final


# transforms

rot_flip_keys = ['rr', 'rh', 'rl', 'fh', 'fv']
rot_flip_transforms = [
    ['/usr/local/bin/pamflip', '-r270'],
    ['/usr/local/bin/pamflip', '-r180'],
    ['/usr/local/bin/pamflip', '-r90'],
    ['/usr/local/bin/pamflip', '-lr'],
    ['/usr/local/bin/pamflip', '-tb'],
]
# rot_flip_axes = [True, False, True, False, False]
rot_flip_axes = [False, False, False, False, False]


def rot_flip(rf):
    return [rot_flip_transforms[x] for x in range(len(rf)) if rf[x]]


def fix_axes(rf, xts, yts):
    if reduce(lambda x, y: x != y, [True for x in range(len(rf)) if rf[x] and rot_flip_axes[x]], False):
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
    return [["/usr/local/bin/pamcut", "-top", str(y1), "-height", str(y2 - y1), "-left", str(x1),
             "-width", str(x2 - x1)]]


# Reshaping assemblers

def set_shape_sizes(x1, x2, y1, y2, xts, yts, xos, yos):
    # xos, yos = get_size(tdir + '/' + fil)
    xcs = x2 - x1
    ycs = y2 - y1
    ratio = float(xts) / float(yts)
    useful.write_message("set_shape_sizes", x1, y1, "/", x2, y2, ';', xts, yts, ';', xcs, ycs, ';', xos, yos,
                         ';', ratio)
    if xcs < xts:
        if xos < xts:  # this one doesn't work right
            useful.write_message("fix x to orig /", nonl=True)
            x1 = 0
            x2 = xos - 1
        else:
            useful.write_message("fix x to target /", nonl=True)
            x1 = max(0, x1 - (xts - xcs) // 2)
            x2 = x1 + xts
    if ycs < yts:
        if yos < yts:
            useful.write_message("fix y to orig /", nonl=True)
            y1 = 0
            y2 = yos - 1
        else:
            useful.write_message("fix y to target /", nonl=True)
            y1 = max(0, y1 - (yts - ycs) // 2)
            y2 = y1 + yts
    useful.write_message("(", x1, y1, "/", x2, y2, ")", nonl=True)
    xcs = x2 - x1
    ycs = y2 - y1
    # might revisit this, for images that are off center this might not be right
    if xts <= xos and yts <= yos and xcs <= xts and ycs <= yts:
        useful.write_message("shape expanding x and y")
        x1 = x1 - (xts - xcs) // 2
        x2 = x1 + xts
        y1 = y1 - (yts - ycs) // 2
        y2 = y1 + yts
        useful.write_message("(", x1, y1, ") (", x2, y2, ")", nonl=True)
        x1, x2, y1, y2 = normalize(x1, x2, y1, y2, xos, yos)
    elif xcs < int(float(ycs) * ratio):
        # too tall - expand x
        useful.write_message("shape expanding x", nonl=True)
        nxs = int(float(ycs) * ratio)
        nx1 = x1 - (nxs - xcs) // 2
        nx2 = nx1 + nxs
        if nxs > xos:
            useful.write_message("off both edges")
            nx1 = 0
            nx2 = xos
        elif nx1 < 0:
            useful.write_message("off the left")
            nx2 = nx2 - nx1
            nx1 = 0
        elif nx2 > xos:
            useful.write_message("off the right")
            nx1 = nx1 - (nx2 - xos)
            nx2 = xos
        else:
            pass
            useful.write_message("on")
        x1 = nx1
        x2 = nx2
    elif xcs > int(float(ycs) * ratio):
        # too wide - expand y
        useful.write_message("shape expanding y", nonl=True)
        nys = int(float(xcs) // ratio)
        ny1 = y1 - (nys - ycs) // 2
        ny2 = ny1 + nys
        if nys > yos:
            useful.write_message("off both edges")
            ny1 = 0
            ny2 = yos
        elif ny1 < 0:
            useful.write_message("off the top")
            ny2 = nys
            ny1 = 0
        elif ny2 > yos:
            useful.write_message("off the bottom")
            # ny1 = ny1 - (ny2 - yos)
            ny1 = yos - nys
            ny2 = yos
        else:
            pass
            useful.write_message("on")
        y1 = ny1
        y2 = ny2
    else:
        useful.write_message("shape as is")
        # hit the jackpot, Mel!
        pass
    useful.write_message('set_shape_sizes returned', x1, y1, '/', x2, y2, '->', x2 - x1, y2 - y1)
    return x1, x2, y1, y2


def normalize(x1, x2, y1, y2, xm, ym):
    useful.write_message('normalize', x1, y1, "/", x2, y2, "orig", xm, ym, nonl=True)
    if x1 < 0:
        x2 = x2 - x1
        x1 = 0
        useful.write_message("x1", nonl=True)
    if y1 < 0:
        y2 = y2 - y1
        y1 = 0
        useful.write_message("y1", nonl=True)
    if x2 >= xm:
        x1 = x1 - (x2 - xm)
        x2 = xm
        useful.write_message("x2", nonl=True)
    if y2 >= ym:
        y1 = y1 - (y2 - ym)
        y2 = ym
        useful.write_message("y2", nonl=True)
    useful.write_message('returns', x1, y1, "/", x2, y2)
    return x1, x2, y1, y2


def shaper(pth, nname, bound, target_size, original_size, rf):
    xts, yts = target_size
    x1, y1, x2, y2 = bound
    xcs = x2 - x1
    ycs = y2 - y1
    xos, yos = original_size

    useful.write_message('Shape :', pth, ': bounds', x1, y1, x2, y2, 'bound size', xcs, ycs, 'target size', xts, yts)
    if xts and yts:
        x1, x2, y1, y2 = set_shape_sizes(x1, x2, y1, y2, xts, yts, xos, yos)
        xcs = x2 - x1
        ycs = y2 - y1

        if xcs > xts:
            useful.write_message("shrinking", nonl=True)
            xts, yts = fix_axes(rf, xts, yts)
            ofi = useful.pipe_chain(open_input_file(pth),
                                    import_file(pth) + cut(x1, y1, x2, y2) + rot_flip(rf) + resize(x=xts) +
                                    export_file(nname, pth),
                                    stderr=open_write_dev_null(), verbose=True)
        elif xcs < xts:
            # dx = xts - xcs
            # dy = yts - ycs
            x1, x2, y1, y2 = normalize(x1, x2, y1, y2, xts, yts)
            useful.write_message("expanding", x1, x2, y1, y2, nonl=True)
            xts, yts = fix_axes(rf, xts, yts)
            ofi = useful.pipe_chain(open_input_file(pth),
                                    import_file(pth) + cut(x1, y1, x2, y2) + rot_flip(rf) + export_file(nname, pth),
                                    stderr=open_write_dev_null(), verbose=True)
        elif xos == xts and yos == yts and xos == xcs and yos == ycs:
            useful.write_message("copying", nonl=True)
            ofi = open_input_file(pth).read()
        else:
            useful.write_message("cutting", nonl=True)
            xts, yts = fix_axes(rf, xts, yts)
            ofi = useful.pipe_chain(open_input_file(pth),
                                    import_file(pth) + cut(x1, y1, x2, y2) + rot_flip(rf) + export_file(nname, pth),
                                    stderr=open_write_dev_null(), verbose=True)

    else:

        if xts < x2 - x1:
            useful.write_message("trim shrinking x", nonl=True)
            xts, yts = fix_axes(rf, xts, yts)
            ofi = useful.pipe_chain(open_input_file(pth),
                                    import_file(pth) + cut(x1, y1, x2, y2) + rot_flip(rf) + resize(x=xts) +
                                    export_file(nname, pth),
                                    stderr=open_write_dev_null(), verbose=True)
        elif yts < y2 - y1:
            useful.write_message("trim shrinking y", nonl=True)
            xts, yts = fix_axes(rf, xts, yts)
            ofi = useful.pipe_chain(open_input_file(pth),
                                    import_file(pth) + cut(x1, y1, x2, y2) + rot_flip(rf) + resize(y=yts) +
                                    export_file(nname, pth),
                                    stderr=open_write_dev_null(), verbose=True)
        else:
            useful.write_message("trim cutting", nonl=True)
            xts, yts = fix_axes(rf, xts, yts)
            ofi = useful.pipe_chain(open_input_file(pth),
                                    import_file(pth) + cut(x1, y1, x2, y2) + rot_flip(rf) + export_file(nname, pth),
                                    stderr=open_write_dev_null(), verbose=True)

    useful.write_message('')
    return ofi


def shrinker(pth, nname, bound, maxsize, rf):
    useful.write_message('shrinker', pth, nname, bound, maxsize)
    x1, y1, x2, y2 = bound
    xcs = x2 - x1
    ycs = y2 - y1
    xts, yts = maxsize
    if not xts:
        xts = xcs
    if not yts:
        yts = ycs
    useful.write_message(x1, y1, x2, y2, ':', xcs, ycs, ':', xts, yts)
    useful.write_message(pth)
    if xcs == xts and ycs == yts:
        useful.write_message("cutting")
        xts, yts = fix_axes(rf, xts, yts)
        ofi = useful.pipe_chain(open_input_file(pth),
                                import_file(pth) + cut(x1, y1, x1 + xcs, y1 + ycs) + rot_flip(rf) +
                                export_file(nname, pth),
                                stderr=open_write_dev_null(), verbose=True)
    elif xts // xcs < yts // ycs:
        useful.write_message("shrinking x")
        xts, yts = fix_axes(rf, xts, yts)
#        ofi = useful.pipe_chain(open_input_file(pth),
#                                import_file(pth) + cut(x1, y1, x1 + xcs, y1 + ycs) + rot_flip(rf) +
#                                resize(x=xts) + export_file(nname, pth),
#                                stderr=open_write_dev_null(), verbose=True)
        ofi = mangler(pth, cut(x1, y1, x1 + xcs, y1 + ycs) + rot_flip(rf) + resize(x=xts), nname)
    else:
        useful.write_message("shrinking y")
        xts, yts = fix_axes(rf, xts, yts)
#        ofi = useful.pipe_chain(open_input_file(pth),
#                                import_file(pth) + cut(x1, y1, x1 + xcs, y1 + ycs) + rot_flip(rf) +
#                                resize(y=yts) + export_file(nname, pth),
#                                stderr=open_write_dev_null(), verbose=True)
        ofi = mangler(pth, cut(x1, y1, x1 + xcs, y1 + ycs) + rot_flip(rf) + resize(y=yts), nname)
    return ofi


def cropper(pth, nname, bound, rf):
    x1, y1, x2, y2 = bound
    useful.write_message('crop', x1, y1, x2, y2, ':', x2 - x1, y2 - y1, ':', rf)
    useful.write_message(pth, '=>', nname)
    ofi = useful.pipe_chain(open_input_file(pth),
                            import_file(pth) + cut(x1, y1, x2, y2) + rot_flip(rf) + export_file(nname, pth),
                            stderr=open_write_dev_null(), verbose=True)
    return ofi


def resizer(pth, nname, x=None, y=None):
    if not x and not y:
        return None  # why did you wake me?
    useful.write_message('resize', x, y)
    useful.write_message(pth, '=>', nname)
    ofi = useful.pipe_chain(open_input_file(pth),
                            import_file(pth) + resize(x, y) + export_file(nname, pth),
                            stderr=open_write_dev_null(), verbose=True)
    return ofi


# PIL based
def wiper(pth, bound, original_size, wipev, wipeh):
    useful.write_message('wiper', pth, bound, original_size, wipev, wipeh)
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
    useful.write_message('padder', pth, target_size)
    img = Image.open(pth)
    img = img.convert('RGB')

    xos, yos = img.size
    xts = target_size[0] if target_size[0] else xos
    yts = target_size[1] if target_size[1] else yos
    if img.size == (xts, yts):
        return img
    if xos > xts or yos > yts:
        useful.write_message("original larger than new", nonl=True)
        return img
    img = img.convert('RGB')

    nc = (0, 0, 0)
    # bc = None

    sx = (xts - xos) // 2
    sy = (yts - yos) // 2
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
        useful.write_message('no original file', in_path, nonl=True)
        return

    thumb = Image.open(in_path)
    if thumb.size[1] != 120:
        useful.write_message('bad original size', thumb.size, nonl=True)
        return
    thumb = thumb.resize((isizex, isizex * thumb.size[1] // thumb.size[0]), Image.NEAREST)
    banner = Image.open(logo)

    text = imicon.Icon(isizex, isizey)
    # top = banner.size[1] + thumb.size[1]
    texttop = isizey - 6 - (6 * len(name)) // 2
    for n in name:
        if len(n) > isizex // 6:
            text.charset("3x5.font")
            left = 50 - len(n) * 2
        else:
            text.charset("5x5.font")
            left = 50 - len(n) * 3
        text.string(left, texttop, n.upper())
        texttop = texttop + 6
    iconimage = text.getimage()

    iconimage.paste(banner, ((isizex - banner.size[0]) // 2, 0))
    iconimage.paste(thumb, ((isizex - thumb.size[0]) // 2, banner.size[1]))

    # write out as png and job off the final conversion to netpbm.
    # doing this because I don't like how PIL disses GIFs.
    tmp_pth = '/tmp/iconner.png'
    iconimage.save(tmp_pth)
    ofi = pipe_convert(tmp_pth, '.gif')
    return ofi


def stitcher(ofn, fa, is_horiz, minx, miny, limit_x, limit_y, verbose=False):
    if is_horiz:
        useful.write_message('horizontal', nonl=True)

        if limit_y:
            miny = min(miny, limit_y)
        resize_x = 0
        resize_y = miny
        cat = ['pnmcat', '-lr']

    else:
        useful.write_message('vertical', nonl=True)

        if limit_x:
            minx = min(minx, limit_x)
        resize_x = minx
        resize_y = 0
        cat = ['pnmcat', '-tb']

    for f in fa:
        pipes = import_file(f[0]) + cut(f[3], f[4], f[5], f[6]) + resize(x=resize_x, y=resize_y)
        outf = useful.pipe_chain(open_input_file(f[0]), pipes, verbose=verbose,
                                 stderr=open_write_dev_null())
        if verbose:
            useful.write_message('>', f[0] + '.pnm')
        open(f[0] + '.pnm', 'wb').write(outf)
        cat.append(f[0] + '.pnm')
    outf = useful.pipe_chain(open_input_file('/dev/null'), [cat] + export_file(ofn), verbose=verbose,
                             stderr=open_write_dev_null())

    if verbose:
        useful.write_message('>', ofn)
    open(ofn, 'wb').write(outf)

    if not verbose:
        for f in fa:
            os.unlink(f[0] + '.pnm')


class Drawer(object):

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
        self.cx, self.cy = [int(x) for x in args[0].split(',')]

    def line(self, args):
        if args[0]:
            self.cx, self.cy = [int(x) for x in args[0].split(',')]
        for arg in args[1:]:
            nx, ny = [int(x) for x in arg.split(',')]
            self.drw.line(((self.cx, self.cy), (nx, ny)), fill=self.col)
            self.cx, self.cy = nx, ny

    def fill(self, args):
        if args[0]:
            self.cx, self.cy = [int(x) for x in args[0].split(',')]
        nx, ny = [int(x) for x in args[1].split(',')]
        self.drw.rectangle(((self.cx, self.cy), (nx, ny)), fill=self.col, outline=self.col)
        self.cx, self.cy = nx, ny

    def box(self, args):
        if args[0]:
            self.cx, self.cy = [int(x) for x in args[0].split(',')]
        nx, ny = [int(x) for x in args[1].split(',')]
        self.drw.rectangle(((self.cx, self.cy), (nx, ny)), outline=self.col)
        self.cx, self.cy = nx, ny

    def point(self, args):
        self.cx, self.cy = [int(x) for x in args[0].split(',')]
        self.drw.point((self.cx, self.cy), fill=self.col)

    def arc(self, args):
        nx, ny = [int(x) for x in args[0].split(',')]
        self.drw.arc((self.cx, self.cy, nx, ny), int(args[1]), int(args[2]), fill=self.col)

    def chord(self, args):
        nx, ny = [int(x) for x in args[0].split(',')]
        self.drw.chord((self.cx, self.cy, nx, ny), int(args[1]), int(args[2]), fill=self.col)

    def pie(self, args):
        nx, ny = [int(x) for x in args[0].split(',')]
        self.drw.pieslice((self.cx, self.cy, nx, ny), int(args[1]), int(args[2]), fill=self.col)

    def write(self, args):
        self.drw.text((self.cx, self.cy), args[0], fill=self.col)

    def color(self, args):
        self.col = tuple([int(x) for x in args[0].split(',')])

    def polygon(self, args):
        lst = []
        if not args[0]:
            lst = [(self.cx, self.cy)]
            args = args[1:]
        lst.extend([(int(x) for x in y.split(',')) for y in args])
        self.drw.polygon(lst, outline=self.col)

    def polyfil(self, args):
        lst = []
        if not args[0]:
            lst = [(self.cx, self.cy)]
            args = args[1:]
        lst.extend([(int(x) for x in y.split(',')) for y in args])
        self.drw.polygon(lst, outline=self.col, fill=self.col)

    def process(self):
        for cmd in open(self.cmdfile).readlines():
            cmd, args = cmd.strip().split('\t', 1)
            arg = args.split(';')
            if cmd == 'canvas':
                sz = arg[0].split(',')
                self.sx = int(sz[0])
                self.sy = int(sz[1])
                self.col = (int(x) for x in arg[1].split(','))
                self.img = Image.new("RGB", (self.sx, self.sy), self.col)
                self.drw = ImageDraw.Draw(self.img)
            elif cmd in self.__class__.__dict__:
                # print('+', cmd, arg, file=sys.stderr)
                self.__class__.__dict__[cmd](self, arg)
            else:
                pass  # print('?', cmd, args, file=sys.stderr)

    def save(self, ofn):
        if ofn:
            self.img.save(ofn)
        else:
            self.img.save(sys.stdout, 'PPM')


class ActionForm(object):
    def __init__(self, pif):
        self.tdir = ''
        self.fn = ''
        self.nname = ''
        self.man = ''
        self.cat = ''
        self.ov = False
        self.cpmv = 'c'
        self.mv = self.cpmv == 'm'
        self.archive = False
        self.spam = False
        self.delete = False
        self.trash = False
        self.selcat = False
        self.dest = ''
        self.rename = False
        self.lib = False
        self.mvbin = False
        self.select = False
        self.var = ''
        self.suff = ''
        self.pref = ''
        self.ptype = ''
        self.inc = ''
        self.cycle = False
        self.tumblr = True
        self.title = ''
        self.link = ''

    def read(self, form):
        self.tdir = form.get_str('d')
        self.fn = form.get_str('fi')
        self.nname = form.get_str('newname')
        self.man = form.get_str('man')
        self.cat = form.get_str('cat')
        self.ov = form.get_bool('ov', False)
        self.cpmv = form.get_str('cpmv', 'c')
        self.mv = self.cpmv == 'm'
        self.archive = form.get_exists('archive')
        self.spam = form.get_exists('spam')
        self.fixed = form.get_exists('fixed')
        self.delete = form.get_exists('delete')
        self.trash = form.get_exists('trash')
        self.selcat = form.get_exists('selcat')
        self.dest = form.get_str('moveto')
        if not self.dest:
            if self.tdir.startswith('lib'):
                self.dest = './' + self.tdir.replace('lib', 'pic')
            elif self.tdir.startswith('./lib'):
                self.dest = self.tdir.replace('lib', 'pic')
        self.rename = form.get_exists('rename')
        self.lib = form.get_bool('lib')
        self.mvbin = form.get_bool('mvbin')
        self.select = form.get_exists('select')
        self.var = form.get_str('newvar')
        self.suff = form.get_str('suff')
        if not self.var:
            self.var = form.get_str('v')
        pref = form.get_str('pref')
        self.pref = pref[1:] if pref and pref != 'n' else ''
        self.ptype = form.get_str('pref')[0] if form.get_str('pref') else ''
        self.inc = form.get_str('inc')
        self.cycle = form.get_bool('cy')
        self.tumblr = form.get_bool('tu', False)
        self.title = form.get_str('title', self.nname)
        self.link = form.get_str('link')

        # szname = ''
        # self.sx = self.sy = 0
        # if os.path.exists(self.tdir + '/' + fn):
        #     x, y = get_size(self.tdir + '/' + fn)
        #     print((x, y))
        #     for (szname, szxy) in zip(mbdata.image_size_types, mbdata.image_size_sizes):
        #         if x <= szxy[0]:
        #             break
        return self

    def action(self, pif, tdir=None, fn=None):
        log_action = False
        if not fn:
            fn = self.fn
        if not tdir:
            tdir = self.tdir
        ret = {'fn': fn, 'dir': tdir, 'act': True}
        from_path = os.path.join(tdir, fn)
        to_dir = to_name = ''
        if self.delete:
            useful.file_delete(from_path)
        elif self.trash:
            useful.file_mover(from_path, os.path.join('.' + config.TRASH_DIR, from_path[from_path.rfind('/') + 1:]),
                              mv=True, inc=True, trash=False)
        elif self.archive:
            useful.file_mover(from_path, os.path.join(tdir, 'archive', fn), mv=True)
            ret['fn'] = ''
        elif self.spam:
            path = '../spam' if os.path.exists(os.path.join(tdir, '..', 'spam')) else 'spam'
            useful.file_mover(from_path, os.path.join(tdir, path, fn), mv=True)
            ret['fn'] = ''
        elif self.fixed:
            useful.file_mover(from_path, os.path.join(tdir, 'fixed', fn), mv=True)
            ret['fn'] = ''
        elif self.rename:
            if not self.nname:
                useful.warn('What? (rename, no name)')
            else:
                to_dir = tdir
                to_name = self.nname
        elif self.lib:
            if not self.man:
                useful.warn('What? (lib, no man)')
            elif not os.path.exists(useful.relpath('.' + config.LIB_MAN_DIR, self.man)):
                # man2 = pif.dbh.fetch_alias(self.man)
                # if not man2:
                useful.warn('bad destination')
                # else:
                #     useful.file_mover(from_path, os.path.join('.' + config.LIB_MAN_DIR, man2['ref_id'].lower(), fn),
                #                       mv=self.mv, ov=self.ov)
            else:
                to_dir = useful.relpath('.' + config.LIB_MAN_DIR, self.man)
                to_name = self.nname
        elif self.mvbin:
            if not os.path.exists(os.path.join('lib', self.cat)):
                useful.warn('bad destination')
            else:
                to_dir = os.path.join('lib', self.cat)
                to_name = self.nname
        elif self.selcat:
            if not (self.man or self.nname) or not self.dest:
                useful.warn('What? (selcat, no name or dest)')
            else:
                ddir = self.dest
                dnam = self.man if self.man else self.nname
                if self.pref:
                    dnam = self.pref + '_' + dnam
                    if self.ptype == 't':
                        ddir = '.' + config.IMG_DIR_ADD
                        if self.suff:
                            dnam += '-' + self.suff
                if dnam:
                    to_name = dnam.lower() + '.jpg'
                    to_dir = ddir
                log_action = True
        elif self.select:
            # inc = self.inc
            if not self.man:
                # self.man = tdir[tdir.rfind('/') + 1:]
                useful.warn('Huh? (select, no man)')
            else:
                ddir = '.' + config.IMG_DIR_MAN
                dnam = self.man
                if self.var:
                    ddir = '.' + config.IMG_DIR_VAR
                    dnam = dnam + '-' + self.var
                    if self.pref:
                        dnam = self.pref + '_' + dnam
                elif self.pref:
                    if self.pref != 'n':
                        dnam = self.pref + '_' + dnam
                    if self.ptype == 't':
                        ddir = '.' + config.IMG_DIR_ADD
                        if self.suff:
                            dnam += '-' + self.suff
                        self.inc = True
                else:
                    useful.warn("What? (select, no var or pref)")
                    dnam = ''
                if dnam:
                    to_name = dnam.lower() + '.jpg'
                    to_dir = ddir
                log_action = True
        else:
            ret['act'] = False
        if to_dir:
            cred = pif.form.get_str('credit')
            if cred:
                photog = pif.dbh.fetch_photographer(cred)
                if not photog or not photog.flags & config.FLAG_PHOTOGRAPHER_PRIVATE:
                    cred = ''
            useful.file_mover(from_path, os.path.join(to_dir, to_name), mv=self.mv, ov=self.ov, inc=self.inc)
            ret['fn'] = to_name
            ret['dir'] = to_dir
            if log_action and self.tumblr:
                title = pif.form.get_str('title', to_name)
                url = pif.secure_prod + os.path.join(to_dir, to_name)
                link = pif.secure_prod + self.link
                title = to_name
                if cred:
                    title += ' credited to ' + photog.name
                pif.ren.message('Post to Tumblr: ',
                                tumblr.Tumblr(pif).create_photo(caption=title, source=url, link=link))
            pif.ren.message('Credit added: ', pif.dbh.write_photo_credit(cred, to_dir, to_name))
        return ret

    def picture_prefixes(self):
        return ([('n', 'no prefix')] +
                [('s' + x[0], x[1]) for x in zip(mbdata.image_size_types, mbdata.image_size_names)] +
                [('t' + x[0], x[1]) for x in zip(mbdata.image_adds_types, mbdata.image_adds_names)])

    sel_moveto = [('.' + x, mbdata.img_dir_name.get(x, x),) for x in movetos]

    def write(self, pif, fn):
        # root, ext = useful.root_ext(fn.strip())
        # print(f'<a href="?d={self.tdir}">{self.tdir}</a> / ')
        # print(f'<a href="/{self.tdir}/{fn}">{fn}</a>')
        # print('<hr>')
        # print('<self action="upload.cgi">')

        szname = ''
        x = y = 0
        if os.path.exists(self.tdir + '/' + fn):
            x, y = get_size(self.tdir + '/' + fn)
            print((x, y))
            for (szname, szxy) in zip(mbdata.image_size_types, mbdata.image_size_sizes):
                if x <= szxy[0]:
                    break
        self.pref = 's' + szname
        print('<input type=hidden name="act" value="1">')
        print(f'<input type=hidden name="d" value="{self.tdir}">')
        print(f'<input type=hidden name="fi" value="{fn}">')
        print(f'<a href="/cgi-bin/imawidget.cgi?d={self.tdir}&f={fn}&v={self.var}&cy={self.cycle}">' +
              pif.form.put_text_button('edit') + '</a>')
        print(pif.form.put_button_input('delete'))
        print(pif.form.put_button_input('trash'))
        print(pif.ren.format_button_link('stitch', f'stitch.cgi?fn_0={self.tdir}/{fn}&submit=1&q=&fc=1'))
        print(f'New name: <input type="text" size="32" name="newname" value="{fn}">')
        print(pif.form.put_button_input('rename'))
        print(pif.form.put_radio('cpmv', [('c', 'copy'), ('m', 'move')], self.cpmv))
        if pif.is_allowed('m'):  # pragma: no cover
            if self.ov:
                print('<input type=checkbox name="ov" value="1" checked>')
            else:
                print('<input type=checkbox name="ov" value="1">')
            print('overwrite<br>')
            print(f'Man: <input type="text" size="12" name="man" value="{self.man}">')
            print(pif.form.put_button_up_down('man'))
            print(pif.form.put_button_input('move to library', 'lib'))
            print('Category:', pif.form.put_select('cat', mbdata.img_sel_cat, self.cat))
            print(pif.form.put_button_input('move to bin', 'mvbin'))
            print(pif.form.put_checkbox("cy", [("1", "cycle")], checked=[str(int(self.cycle))]))
            print(pif.form.put_checkbox("tu", [("1", "tumblr")], checked=[str(int(self.tumblr))]))
            print('<input type=checkbox name="inc" value="1"> increment name')
            print(f'<br>Variation: <input type="text" size="5" name="newvar" value="{self.var}">')
            print('Prefix:', pif.form.put_select('pref', self.picture_prefixes(), self.pref, blank=''))
            print(f'Suffix: <input type="text" size="5" name="suff" value="{self.suff}">')
            print(pif.form.put_button_input('select to casting', 'select'))
            print('Move to:', pif.form.put_select('moveto', self.sel_moveto, self.dest, blank=''))
            print(pif.form.put_button_input('select to category', 'selcat'))
            print('<br>')

        return x, y


def get_dir(tdir, name_has=''):
    titles = {'dir': 'Directories', 'graf': 'Graphics', 'dat': 'Data Files',
              'exe': 'Executable Files', 'other': 'Other Files', 'log': 'Log Files'}
    fl = os.listdir(tdir)
    fl.sort()
    files = {'dir': list(), 'graf': list(), 'dat': list(),
             'exe': list(), 'other': list(), 'log': list(),
             'titles': titles}
    for f in fl:
        if name_has and name_has not in f:
            continue
        root, ext = useful.root_ext(f)
        if os.path.exists(tdir + '/' + f):
            if f[-1] == '~' or f == '.crcs' or f[-4:] == '.pyc':
                continue
            fstat = os.stat(tdir + '/' + f)
            perms = fstat.st_mode
            if os.path.isdir(tdir + '/' + f):
                files['dir'].append(f)
            elif ext == 'dat':
                files['dat'].append(f)
            elif ext == 'log':
                files['log'].append(f)
            elif ext in image_inputter:
                files['graf'].append(f)
            elif stat.S_IMODE(perms) & stat.S_IXUSR or ext in ['html', 'php']:
                files['exe'].append(f)
            else:
                files['other'].append(f)
    return files


def format_image_star(pif, image_path, image_file, pic_id='', halfstar=False, target_x=400, target_y=0):
    if pic_id is None:
        return pif.ren.fmt_star('white')
    if not os.path.exists(os.path.join(image_path, image_file)):
        if pic_id:
            return pif.ren.fmt_star('yellow', half=halfstar)
        return pif.ren.fmt_star('black', hollow=True)
    try:
        img = Image.open(os.path.join(image_path, image_file))
    except Exception:
        return pif.ren.fmt_star('yellow', half=halfstar)
    ix, iy = img.size
    if target_x:
        if ix < target_x // 2:
            return pif.ren.fmt_star('red', half=halfstar)
        if ix < target_x:
            return pif.ren.fmt_star('green', half=halfstar)
        if ix > target_x:
            return pif.ren.fmt_star('blue', half=halfstar)
    else:
        if iy < target_y // 2:
            return pif.ren.fmt_star('red', half=halfstar)
        if iy < target_y:
            return pif.ren.fmt_star('green', half=halfstar)
        if iy > target_y:
            return pif.ren.fmt_star('blue', half=halfstar)
    return pif.ren.fmt_star('black', half=halfstar)


def read_presets(pdir):
    if os.path.exists(os.path.join(pdir, '.ima')):
        presets = eval(open(os.path.join(pdir, '.ima')).read())
        print('read_presets:', presets, '<br>')
        presets['save'] = [1]
        return presets
    return dict()


def write_presets(pdir, presets, force=False):
    if force or os.path.exists(os.path.join(pdir, '.ima')):
        print('write_presets:', presets, '<br>')
        open(os.path.join(pdir, '.ima'), 'w').write(str(presets))


def update_presets(pdir, values):
    if os.path.exists(os.path.join(pdir, '.ima')):
        presets = read_presets(pdir)
        presets.update(values)
        write_presets(pdir, presets)


def promote_picture(pif, mod_id, var_id):
    photo_id = f'{mod_id.lower()}-{var_id.lower()}'
    credit = pif.dbh.fetch_photo_credit(f'.{config.IMG_DIR_VAR}', f'{photo_id}.*')
    pif.ren.message('promoting picture for', mod_id, 'var', var_id, 'to',
                    credit['photographer.id'] if credit else 'uncredited')
    for pic in glob.glob(f'.{config.IMG_DIR_VAR}/?_{photo_id}.*'):
        ofn = pic[pic.rfind('/') + 1:]
        nfn = ofn[:ofn.find('-')] + ofn[ofn.find('.'):]
        useful.file_copy(pic, f'.{config.IMG_DIR_MAN}/{nfn}')
    # transfer credit
    if credit:
        pif.ren.message('Credit added: ', pif.dbh.write_photo_credit(credit['photographer.id'],
                        config.IMG_DIR_MAN[1:], mod_id))


def demote_picture(pif, mod_id, var_id):
    credit = pif.dbh.fetch_photo_credit('.' + config.IMG_DIR_MAN, mod_id.lower() + '.*')
    pif.ren.message('demoting picture for', mod_id, 'var', var_id, 'to',
                    credit['photographer.id'] if credit else 'uncredited')
    for pic in glob.glob(f'.{config.IMG_DIR_MAN}/?_{mod_id.lower()}.*'):
        ofn = pic[pic.rfind('/') + 1:]
        nfn = ofn[:ofn.rfind('.')] + '-' + var_id.lower() + pic[pic.rfind('.'):]
        useful.file_copy(pic, '.' + config.IMG_DIR_VAR + '/' + nfn)
    # transfer credit
    if credit:
        pif.ren.message('Credit added: ', pif.dbh.write_photo_credit(credit['photographer.id'],
                        config.IMG_DIR_VAR[1:], f'{mod_id.lower()}-{var_id.lower()}.*'))


def simple_save(ofi, opth):
    if isinstance(ofi, Image.Image):
        ofi.save(opth)
    else:
        open(opth, "wb").write(ofi)


def get_credit_file():
    ents = bfiles.SimpleFile('src/credits.dat')
    dirs = {}
    for ent in ents:
        if ent[0] == 'c':
            dirs.setdefault(ent[1], dict())
            dirs[ent[1]][ent[3]] = ent[2]
    return dirs


def get_tilley_file():
    ents = bfiles.SimpleFile('src/credits.dat')
    mans = {}
    for ent in ents:
        if ent[0] == 'c' and ent[2] == 'DT' and ent[1].startswith('man/'):
            mans.setdefault(ent[1][4:], list())
            mans[ent[1][4:]].append(ent[3])
    return mans


def webp_to_png(pth, fn):
    nfn = fn[:fn.rfind('.')] + '.png'
    ofi = useful.pipe_chain(None,
                            [['/usr/local/bin/dwebp', pth + '/' + fn, '-o', '-']],
                            stderr=open_write_dev_null(), verbose=True)
    # print('WTP', pth + '/' + fn, pth + '/' + nfn)
    open(pth + '/' + nfn, 'wb').write(ofi)
    os.unlink(pth + '/' + fn)
    return nfn
