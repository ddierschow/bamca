#!/usr/local/bin/python

import copy, os, re, sys
import cmdline
import imicon
import Image

sys.path.append('../htdocs/bin')

palettepos = {0: (0,102,0), 1: (255,255,255), 2: (1,1,1)}
paletteneg = {1: (0,102,0), 0: (255,255,255), 2: (1,1,1)}
fontname = 'nx10'
padding = 2
direc = '../htdocs/pic/gfx'

def write(fn, orig, width, height, palette):
    fn = fn.replace('|', '_').replace(' ', '_').lower() + '.gif'
    image = copy.deepcopy(orig)
    im = Image.new("P", (width, height))

    newpalette = []
    for iP in range(0,3):
	newpalette.extend(palette[iP])
    im.putpalette(newpalette)
    for iY in range(0, height):
	for iX in range(0, width):
	    im.putpixel((iX, iY), image.pop(0))
    im.save(fn, transparency=2)


def dump(image, w, h):
    i = 0
    for y in range(0, h):
	for x in range(0, w):
	    print image[i],
	    i += 1
	print


def create_base_image(text, font):
    text = text.upper().replace('_', ' ')
    texts = text.split('|')
    max_width = 0
    for ln in texts:
	width = reduce(lambda x,y: x+y, [font.chars[x][0] for x in ln])
	max_width = max(max_width, width)
    height = (font.height + padding) * len(texts) + padding + 2
    width = max_width + 2 + 2 * padding
    image = [ 0 ] * (width*height)

    # border
    for i in range(0, width):
	image[i] = image[width * (height - 1) + i] = 1
    for i in range(0, height):
	image[width * i] = image[width * i + width - 1] = 1

    # corners
    image[0] = image[width - 1] = image[width * (height - 1)] = image[width * height - 1] = 2
    image[width + 1] = image[2 * width - 2 ] = image[(height - 2) * width + 1] = image[(height - 1) * width - 2] = 1

    y = padding + 1
    for ln in texts:
	ln_width = reduce(lambda x,y: x+y, [font.chars[x][0] for x in ln])
	x = 1 + padding + (max_width - ln_width) / 2
	for c in ln:
	    merge(image, x, y, width, font.height, font.chars[c], 1)
	    x = x + font.chars[c][0]
	y += font.height + padding

    return image, width, height


def merge(image, start_x, start_y, image_width, char_height, font_entry, val):
    char_width, char_image = font_entry
    for iY in range(char_height - 1, -1, -1):
	for iX in range(char_width - 1, -1, -1):
	    if char_image & 1:
		image[(start_y + iY) * image_width + start_x + iX] = val
	    char_image >>= 1


rgb_re = re.compile('#(?P<r>\w\w)(?P<g>\w\w)(?P<b>\w\w)')
def color_eval(spec):
    if spec.startswith('#'):
	rgb_m = rgb_re.match(spec)
	return (eval('0x' + rgb_m.group('r')), eval('0x' + rgb_m.group('g')), eval('0x' + rgb_m.group('b')))
    else:
	return eval(spec)


def Main():
    global paletteneg, palettepos, fontname, padding, direc
    switch, files = cmdline.CommandLine("n", "bcfpd", envar="BUTTONMAKER")
    print switch, files

    if not files:
	print "buttonmaker -n -b <background> -c <color> -f <font name> -p <padding> -d <dir> button_text ..."
	print "  where -n means noinverse"
	print "  -b defaults to", paletteneg[0]
	print "  -c defaults to", palettepos[0]
	print "  -f defaults to", fontname
	print "  -p defaults to", padding
	print "  -d defaults to", direc
    if switch['b']:
	paletteneg[1] = palettepos[0] = color_eval(switch['b'][-1])
    if switch['c']:
	paletteneg[0] = palettepos[1] = color_eval(switch['c'][-1])
    if switch['f']:
	fontname = switch['f'][-1]
    if switch['p']:
	padding = int(switch['p'][-1])
    if switch['d']:
	direc = switch['d'][-1]
    font = imicon.font(fontname + '.font')

    print "NEG:", paletteneg
    print "POS:", palettepos
    for fn in files:
	if fn.endswith('.gif'):
	    fn = fn[4:-4]

	image, width, height = create_base_image(fn, font)
	dump(image, width, height)

	write(os.path.join(direc, 'but_' + fn), image, width, height, palettepos)
	if not switch['n']:
	    write(os.path.join(direc, 'hov_' + fn), image, width, height, paletteneg)


if __name__ == '__main__':
    Main()
