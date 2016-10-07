#!/usr/local/bin/python

import copy, os, re, sys
from PIL import Image
import basics
import imicon

sys.path.append('../htdocs/bin')

rgb_re = re.compile('#(?P<r>\w\w)(?P<g>\w\w)(?P<b>\w\w)')


def create_final_image(fn, orig, width, height, palette):
    fn = fn.replace('|', '_').replace(' ', '_').lower() + '.gif'
    image = copy.deepcopy(orig)
    im = Image.new("P", (width, height))

    newpalette = []
    for iP in range(0, 3):
        newpalette.extend(palette[iP])
    im.putpalette(newpalette)
    for iY in range(0, height):
        for iX in range(0, width):
            im.putpixel((iX, iY), image.pop(0))
    print 'writing', fn
    return im


def write(im, fn):
    fn += '.gif'
    im.save(fn, transparency=2)


def dump(image, w, h):
    i = 0
    for y in range(0, h):
        for x in range(0, w):
            print image[i],
            i += 1
        print


def create_base_image(text, font, defaults):
    text = text.upper().replace('_', ' ')
    texts = text.split('|')
    max_width = 0
    for ln in texts:
        width = reduce(lambda x, y: x + y, [font.chars[x][0] for x in ln])
        max_width = max(max_width, width)
    height = (font.height + defaults['padding']) * len(texts) + defaults['padding'] + 2
    width = max_width + 2 + 2 * defaults['padding']
    image = [0] * (width * height)

    # border
    for i in range(0, width):
        image[i] = image[width * (height - 1) + i] = 1
    for i in range(0, height):
        image[width * i] = image[width * i + width - 1] = 1

    # corners
    image[0] = image[width - 1] = image[width * (height - 1)] = image[width * height - 1] = 2
    image[width + 1] = image[2 * width - 2] = image[(height - 2) * width + 1] = image[(height - 1) * width - 2] = 1

    y = defaults['padding'] + 1
    for ln in texts:
        ln_width = reduce(lambda x, y: x + y, [font.chars[x][0] for x in ln])
        x = 1 + defaults['padding'] + (max_width - ln_width) / 2
        for c in ln:
            merge(image, x, y, width, font.height, font.chars[c], 1)
            x = x + font.chars[c][0]
        y += font.height + defaults['padding']

    return image, width, height


def merge(image, start_x, start_y, image_width, char_height, font_entry, val):
    char_width, char_image = font_entry
    for iY in range(char_height - 1, -1, -1):
        for iX in range(char_width - 1, -1, -1):
            if char_image & 1:
                image[(start_y + iY) * image_width + start_x + iX] = val
            char_image >>= 1


def color_eval(spec):
    if spec.startswith('#'):
        rgb_m = rgb_re.match(spec)
        return (eval('0x' + rgb_m.group('r')), eval('0x' + rgb_m.group('g')), eval('0x' + rgb_m.group('b')))
    else:
        return eval(spec)


@basics.standalone
def main(switch, files):  # pragma: no cover
    defaults = {
        'palettepos': {0: (0, 102, 0), 1: (255, 255, 255), 2: (1, 1, 1)},
        'paletteneg': {1: (0, 102, 0), 0: (255, 255, 255), 2: (1, 1, 1)},
        'fontname': 'nx10',
        'padding': 2,
        'direc': '../htdocs/pic/gfx',
    }
    print switch, files

    if not files:
        print "buttonmaker -i -n -b <background> -c <color> -f <font name> -p <padding> -d <dir> button_text ..."
        print "  where -i means noinverse"
        print "  where -n means nofiles"
        print "  -b defaults to", defaults['paletteneg'][0]
        print "  -c defaults to", defaults['palettepos'][0]
        print "  -f defaults to", defaults['fontname']
        print "  -p defaults to", defaults['padding']
        print "  -d defaults to", defaults['direc']
    if switch['b']:
        defaults['paletteneg'][1] = defaults['palettepos'][0] = color_eval(switch['b'][-1])
    if switch['c']:
        defaults['paletteneg'][0] = defaults['palettepos'][1] = color_eval(switch['c'][-1])
    if switch['f']:
        defaults['fontname'] = switch['f'][-1]
    if switch['p']:
        defaults['padding'] = int(switch['p'][-1])
    if switch['d']:
        defaults['direc'] = switch['d'][-1]

    print "NEG:", defaults['paletteneg']
    print "POS:", defaults['palettepos']
    create_files(switch, files, defaults)


def create_files(switch, files, defaults):
    font = imicon.Font(defaults['fontname'] + '.font')
    for fn in files:
        if fn.endswith('.gif'):
            fn = fn[4:-4]

        image, width, height = create_base_image(fn, font, defaults)
        dump(image, width, height)

        im = create_final_image(os.path.join(defaults['direc'], 'but_' + fn), image, width, height, defaults['palettepos'])
        if not switch['n']:
	    write(im, os.path.join(defaults['direc'], 'but_' + fn))
        if not switch['i']:
            im = create_final_image(os.path.join(defaults['direc'], 'hov_' + fn), image, width, height, defaults['paletteneg'])
	    if not switch['n']:
		write(im, os.path.join(defaults['direc'], 'hov_' + fn))


if __name__ == '__main__':
    main("in", "bcfpd", envar="BUTTONMAKER")
