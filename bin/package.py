#!/usr/local/bin/python

import copy, glob, os
import basics
import bfiles
import config
import imglib
import mbdata
import useful


# -- package

def print_tree_row(tree, text):
    print tree + text
    print '<br>\n'


def render_tree(pif, ch):
    ostr = ''
    for c in ch:
        if c.isdigit():
            for i in range(0, int(c)):
                ostr += pif.render.format_image_art("treeb"+".gif", also={'align': 'absmiddle', 'height': 24, 'width': 24}) + '\n'
        else:
            ostr += pif.render.format_image_art("tree"+c+".gif", also={'align': 'absmiddle', 'height': 24, 'width': 24}) + '\n'
    return ostr


def show_pic(pif, flist):
    ostr = ''
    for f in flist:
        f = f[f.rfind('/') + 1:-4]
        ostr += pif.render.format_image_as_link([f], f.upper(), also={'target': '_showpic'}) + '\n'
    return ostr


def do_tree_page(pif, dblist):
    for llist in dblist:
        cmd = llist.get_arg()
        if cmd == 'dir':
            pif.render.pic_dir = llist.get_arg()
        elif cmd == 'render':
            useful.render(pif.render.pic_dir + '/' + llist.get_arg())
        elif cmd == 'p':
            print '<p>\n'
        elif cmd == 's':
            print '<p>\n'
            print '<a name="%s"></a>' % llist[1]
            if llist[2]:
                print '<b><u>%s -' % llist[2],
            else:
                print '<b><u>',
            print '%s</u></b>' % llist[3]
            print '<br>\n'
        elif cmd == 'm':
            desc = ''
            if llist[2]:
                desc += ('<b>%s</b> ' % llist[2])
                if llist[3] and not llist[3][0].isupper():
                    desc += "- "
            desc += llist[3]
            #print render_tree(pif, llist[1]) + desc
            #print '<br>\n'
            print_tree_row(render_tree(pif, llist[1]), desc)
        elif cmd == 'n':
            print_tree_row(render_tree(pif, llist[1]), '<font color="#666600"><i>%s</i></font>' % llist[2])
        elif cmd == 'a':
            print_tree_row(render_tree(pif, llist[1]), pif.render.format_image_as_link([llist[2]], llist[3], also={'target': '_showpic'}))
        elif cmd == 'e':
            flist = glob.glob(pif.render.pic_dir + '/' + llist[2] + "*.jpg")
            flist.sort()
            if flist:
                print '<font color="blue">'
                print_tree_row(render_tree(pif, llist[1]), ('<i>Example%s:</i>\n' % useful.plural(flist)) + show_pic(pif, flist))
                print '</font>'


@basics.web_page
def blister(pif):
    pif.render.print_html()
    #global pagename
    #pagename = pif.form.get_str('page', 'blister')

    dblist = bfiles.SimpleFile(os.path.join(config.SRC_DIR, pif.page_name + '.dat'))

    print pif.render.format_head()
    do_tree_page(pif, dblist)
    print pif.render.format_tail()

# -- boxart

# id, mod_id, box_type, pic_id, box_size
# additional_text, bottom, sides, end_flap, year, notes
box_lookups = {
    'box_type': {
	'_title': 'Box Type',
	'A': 'A: line drawing, A Moko LESNEY (script) in scroll, 1953-54',
	'B1': 'B1: line drawing, A MOKO LESNEY (capitals) in scroll, 1955-56',
	'B2': 'B2: line drawing, A MOKO LESNEY (capitals) in scroll, 1957-58',
	'B3': 'B3: line drawing, A MOKO LESNEY (capitals) in scroll, 1958-59',
	'B4': 'B4: line drawing, A MOKO LESNEY (capitals) in scroll, 1959',
	'B5': 'B5: line drawing, A MOKO LESNEY (capitals) in scroll, 1960',
	'C': 'C: line drawing, A LESNEY in scroll, 1961',
	'D1': 'D1: colour picture, "MATCHBOX" Series in arch, 1962',
	'D2': 'D2: colour picture, "MATCHBOX" Series in arch, 1963-66',
	'E1': 'E1: colour picture, "MATCHBOX" in arch, 1964-66',
	'E2': 'E2: colour picture, "MATCHBOX" in arch, 1964-66',
	'E3': 'E3: colour picture, "MATCHBOX" in arch, 1966',
	'E3R': 'E3R: colour picture, "MATCHBOX" in arch with "&reg;", 1968',
	'E4': 'E4: colour picture, "MATCHBOX" in arch, 1967',
	'E4R': 'E4R: colour picture, "MATCHBOX" in arch with "&reg;", 1968',
	'F': 'F: colour picture, "MATCHBOX" straight, 1969',
	'G': 'G: colour picture, "MATCHBOX" italic, 1970-75',
	'H': 'H: colour picture, "MATCHBOX" bold italic with tyre, 1971-76',
	'I': 'I: colour picture, "MATCHBOX" bold italic, 1972-79',
	'J': 'J: colour picture, "MATCHBOX" in oval, number/name in centre, 1975-82',
	'K': 'K: colour picture, "MATCHBOX" in oval, number/name at bottom, 1976-82',
	'L': 'L: colour picture, "MATCHBOX" in oval, colour picture on side, 1977-82',
    },
    'bottom': {
	'_title': 'Bottom Line Text',
	'NONE': 'no text at bottom',
	'C1': 'MADE IN ENGLAND, bottom centre',
	'C2': 'MADE IN ENGLAND, bottom right',
	'AMS':  'A Moko LESNEY PRODUCT (Moko in script)',
	'AML':  'A MOKO LESNEY PRODUCT (MOKO in block capitals)',
	'ALS':  'A LESNEY PRODUCT (scroll)',
	'ALP':  'A LESNEY PRODUCT (straight)',
	'LPC':  'LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND',
	'MIR1': '''"MATCHBOX" IS THE REG'D T.M. OF LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND''',
	'MRT1': '''"MATCHBOX" REG'D T.M. LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND''',
	'MRT2': '''&copy; 197x "MATCHBOX" REG'D T.M. LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND''',
	'MRT3': '''&copy; 197x "MATCHBOX" REG'D T.M. MARCA REGISTRADA LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND''',
	'MRM':  '''MARCA REGISTRADA &copy; 197x "MATCHBOX" REG'D T.M. LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND''',
	'MIR2': '''"MATCHBOX" IS THE REG'D TRADE MARK (MARCA REGISTRADA) OF LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND''',
	'MMR1': '"MATCHBOX", "MARCA REGISTRADA" REGISTERED TRADE MARK OF LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND',
	'MMR2': '"MATCHBOX", "MARCA REGISTRADA" REGISTERED TRADE MARK OF LESNEY PRODUCTS &amp; CO. LTD. LONDON E.9 5PA ENGLAND',
	'CNG':  'CONFORMIT&Eacute; AUX NORMES GARANTIE PAR LESNEY S.A.',
	'CNN':  'CONFORMIT&Eacute; AUX NORMES GARANTIE PAR LESNEY S.A.NE CONVIENT PAS &Agrave; UN ENFANT DE MOINS DE 36 MOIS',
	'MMR3': '"MATCHBOX" (MARCA REGISTRADA) REGISTERED TRADE MARK OF LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND',
	'MIR3': '"MATCHBOX" IS THE REGISTERED TRADE MARK (MARCA REGISTRADA) OF LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND',
	'MIR4': '"MATCHBOX" IS THE REGISTERED TRADE MARK (MARCA REGISTRADA) OF LESNEY PRODUCTS P.L.C. LONDON ENGLAND',
	'NRC': 'Not recommended for children under 3.',
    },
    'box_size': {
	'_title': 'Box Size',
	'1': 'short/very narrow (2.250 x 0.875 x 1.500 inches, 57 x 22 x 38 millimeters)',
	'2': 'short/narrow (2.250 x 1.000 x 1.500 inches, 57 x 26 x 38 millimeters)',
	'3': 'medium/narrow (2.625 x 1.000 x 1.500 inches, 67 x 26 x 38 millimeters)',
	'4': 'medium/wide (2.625 x 1.500 x 1.500 inches, 67 x 38 x 38 millimeters)',
	'5': 'long/narrow (3.063 x 1.000 x 1.500 inches, 78 x 26 x 38 millimeters)',
	'6': 'long/medium (3.063 x 1.250 x 1.500 inches, 78 x 33 x 38 millimeters)',
	'7': 'long/wide (3.063 x 1.500 x 1.500 inches, 78 x 38 x 38 millimeters)',
    },
    'end_flap': {
	'_title': 'End Flap Design',
	'P': 'plain blue',
	'BN': 'black number',
	'BNWC': 'black number in white circle',
	'BNWP': 'black model name in white panel',
	'WM': 'white model name',
	'L': 'model name in upper- and lowercase letters',
	'U': 'model name in uppercase letters only',
	'LWS': 'model name lettering with serifs',
	'LNS': 'model name lettering without serifs',
	'E1': 'model number and name',
	'E2': 'model number, name and detail drawing',
	'E3': 'colour picture',
	'E4': '"MATCHBOX" and colour picture',
	'E4R': '"MATCHBOX" with "&reg;" and colour picture',
	'SCC': 'SPECIFICATION AND COLOUR OF CONTENTS SUBJECT TO AMENDMENT',
	'PO': "PORTI&Egrave;RES OUVRANTES - LICENCE SOLIDO",
	'TM': 'Trademark "MATCHBOX"&reg; Owned By Lesney Products &amp; Co. Ltd.',
	'TME': 'Trademark "MATCHBOX"&reg; Owned By Lesney Products &amp; Co. Ltd. Printed in England. Made in England.',
	'MK': "MARK",
	'MK I': "MARK I",
	'MK 1': "MARK 1",
	'MK 2': "MARK 2",
	'MK 3': "MARK 3",
	'MK 4': "MARK 4",
	'MK 5': "MARK 5",
	'MK 6': "MARK 6",
	'MK 7': "MARK 7",
	'CTC': 'MADE BY LESNEY PRODUCTS &amp; CO. LTD., AND SOLD UNDER PERMISSION FROM CATERPILLAR TRACTOR COMPANY.',
	'N': '"NEW"',
	'NM': '"NEW MODEL"',
    },
    'sides': {

##|Box generations|Years|Lettering|Location|Combined w/ bottom types
#3|--------IJKL|1973-81|&copy; 19xx LESNEY PRODUCTS &amp; CO. LTD. MADE IN ENGLAND|on sides|MIR2 MMR1 MMR2 CNG CNN MMR3 MIR3
#4|--------I---|1974|&copy; 1973 LESNEY PRODUCTS &amp; CO. LTD. PRINTED AND MADE IN ENGLAND|on sides|MIR2 CNG CNN
#5|--------I---|1975|&copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. MADE IN GREAT BRITAIN|on sides|MIR2 CNN
#6|--------I---|1975|&copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. PRINTED AND MADE IN GREAT BRITAIN|on sides|MIR2 CNN
#7|--------I---|1975|&copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND|on sides|MIR2 CNN
#8|-----------L|1981|&copy; 198x LESNEY PRODUCTS &amp; CO. LTD. MADE IN HONG KONG|on sides|MIR3
#9|-----------L|1982|&copy; 1981 LESNEY PRODUCTS P.L.C. MADE IN ENGLAND|on sides|MIR4

	'_title': 'Box Sides',
	'1BS': 'one blue side and one black side',
	'2BS': 'two blue sides',
	'LBS': 'two light blue sides',
	'DR': 'drawings of the model',
	'SF': '"Superfast" lettering',
	'DRA': 'drawings of the model',
	'SFP': '"Superfast" lettering parallel to edge',
	'SFA': '"Superfast outraces them all" at an angle to edge',
	'FCS': "'FAT-WHEEL' CUSHION SUSPENSION",
	'HCS': "HI-SPEED 'CROSS COUNTRY' SUSPENSION",
	'HFS': 'HI-SPEED FREIGHTLINE SUSPENSION',
	'HHR': 'HI-SPEED HEAVY-DUTY ROLLERS',
	'MRS': 'MAG-WHEELS-RACING SUSPENSION',
	'MPT': 'METALLIZED PARTS AND TOWING HOOK',
	'SAF': "SUPERFAST 'AUTOMATIC' FEATURES",
	'STC': 'SUPER TRACTION CATERPILLAR TRACK',
	'WRT': 'WIDE RACING-SLICKS TORSION SPRINGING',
	'PTF': 'WITH PROP-STAND AND TURNING FRONT FORKS',
	'4HS': "4-WHEEL 'HOVERSPRING' SUSPENSION",
	'TST': '"TESTED" mark',
	'RS': 'RACING SUSPENSION / HIGH SPEED MAG-WHEELS',
	'B3': 'black &copy; 197x LESNEY PRODUCTS &amp; CO. LTD. MADE IN ENGLAND',
	'B4': 'black &copy; 1973 LESNEY PRODUCTS &amp; CO. LTD. PRINTED AND MADE IN ENGLAND',
	'B5': 'black &copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. MADE IN GREAT BRITAIN',
	'B6': 'black &copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. PRINTED AND MADE IN GREAT BRITAIN',
	'B7': 'black &copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND',
	'W3': 'white &copy; 197x LESNEY PRODUCTS &amp; CO. LTD. MADE IN ENGLAND',
	'W4': 'white &copy; 1973 LESNEY PRODUCTS &amp; CO. LTD. PRINTED AND MADE IN ENGLAND',
	'W5': 'white &copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. MADE IN GREAT BRITAIN',
	'W6': 'white &copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. PRINTED AND MADE IN GREAT BRITAIN',
	'W7': 'white &copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND',
	'BLK': 'black "TM"',
	'RED': 'red "TM"',
	'Sup': '"Superfast" in script',
	'SUP': '"SUPERFAST" in block capitals',
	'ROL': '"Rola-matics"',
	'1B': '''box also contains one line inside bottom:
CONFORMIT&Eacute; AUX NORMES GARANTIE PAR LESNEY S.A.''',
	'2': '''box containing two lines inside top (English and French):
NOT RECOMMENDED FOR CHILDREN UNDER 36 MONTHS
NE CONVIENT PAS &Agrave; UN ENFANT DE MOINS DE 36 MOIS''',
	'4A': '''box containing four lines inside top (English and French):
CAUTION: CONTAINS SMALL PARTS.
NOT RECOMMENDED FOR CHILDREN UNDER 36 MONTHS.
ATTENTION! CONTIENT PETITES PIECES.
NE CONVIENT PAS &Agrave; UN ENFANT DE MOINS DE 36 MOIS.''',
	'5A': '''box containing five lines inside top (English, French and Italian):
NOT RECOMMENDED FOR CHILDREN UNDER 36 MONTHS.
NE CONVIENT PAS &Agrave; UN ENFANT DE MOINS DE 36 MOIS.
CONFORMIT&Eacute; AUX NORMES GARANTIE PAR LESNEY S.A.
NON ADATTO AD UN BAMBINO DI ETA MINORE AL 36
MESI.  CONFORME PRESCRIZIONE DM 31.7.79.''',
	'8': '''box containing eight lines inside top (English, French and Italian):
CAUTION: CONTAINS SMALL PARTS.
NOT RECOMMENDED FOR CHILDREN UNDER 36 MONTHS.
ATTENTION! CONTIENT DES PETITES PIECES.
NE CONVIENT PAS &Agrave; UN ENFANT DE MOINS DE 36 MOIS.
CONFORMIT&Eacute; AUX NORMES GARANTIE PAR LESNEY S.A.
AVVERTIMENTO: CONTIENE PICCOLI PEZZI.  NON ADATTO
AD UN BAMBINO DI ETA MINORE AL 36 MESI.
CONFORME PRESCRIZIONE DM 31.7.79.''',
	'4B': '''box containing four lines inside top (English, French and Swedish):
NOT RECOMMENDED FOR CHILDREN UNDER 36 MONTHS
NE CONVIENT PAS &Agrave; UN ENFANT DE MOINS DE 36 MOIS
INNEH&Aring;LLER SM&Aring;DELAR EJ L&Auml;PLIGT F&Ouml;R
BARN UNDER 3 &Aring;R.''',
	'5B': '''box containing five lines inside top (English, French, Italian, German and Swedish, used in Australia only):
NOT RECOMMENDED FOR CHILDREN UNDER 36 MONTHS
NE CONVIENT PAS A UN ENFANT DE MOINS DE 36 MOIS
NON ADATTO AD UN BAMBINO DI ET&Aacute; MINORE AI 36 MESI
GEEIGNET F&Uuml;R KINDER AD DERI JAPHEN
INNEH&Aring;LLER SM&Aring;DELAR EI L&Auml;MPLIGT FOR BARN UNDER 3 &Aring;R''',
	'6': '''box containing six lines inside top (English, French, Italian and Swedish):
NOT RECOMMENDED FOR CHILDREN UNDER 36 MONTHS.
NE CONVIENT PAS &Agrave; UN ENFANT DE MOINS DE 36 MOIS.
CONFORMIT&Eacute; AUX NORMES GARANTIE PAR LESNEY S.A.
NON ADATTO AD UN BAMBINO DI ETA MINORE AL 36
MESI. CONFORME PRESCRIZIONE DM 31.7.79.
INNEH&Aring;LLER SM&Aring;DELAR EJ L&Auml;MPLIGT F&Ouml;R BARN UNDER 3 &Aring;R.''',
	'1': '''box containing one line inside top (English, used in USA only):
NOT RECOMMENDED FOR CHILDREN UNDER 36 MONTHS''',
    },
    'additional_text': {
	'_title': 'Additional Text',
	# ABC
	'NO': 'No. with model number',
	# DE
	'NUM': 'Model number',
	# F
	'AST': '"AUTOSTEER"',
	'BSF': 'black "Superfast"',
	'RLB': '"SERIES" in red left of blue number box',
	'RSF': 'red "Superfast"',
	'RUB': '"SERIES" in red under oblong blue number box',
	'WIB': '"SERIES" in white in blue number box',
	# G
	'BLK': 'black "TM"',
	'RED': 'red "TM"',
	# GIKL
	'NON': 'no "TM", no additional lettering',
	# H
	'H1': '''black number inside a red frame, no "Superfast" lettering nor model name''',
	'H2': '''black number without frame, "Superfast" lettering and model name''',
	# HJKL
	'N': '"NEW"',
	# I
	'BNF': 'model number and black "NEW" in red frame',
	'CHO': '"Choppers"',
	'RNF': 'model number and red "NEW" in red frame',
	'XF': 'model number in red frame',
	# IJKL
	'ROL': '"Rola-matics"',
	# J
	'STR': 'Streakers',
    },
    'year': {
	'_title': 'Year on Box',
    },
    'notes': {
	'_title': 'Notes',
    },
}

def single_box(pif, mod, box):
    ign_cols = ['id', 'mod_id', 'pic_id']
    pic_name = ('x_%s-%s%s' % (box['mod_id'], box['box_type'][0], box['pic_id'])).lower()
    pics = pif.render.find_image_files(pic_name + '*')
    if mod:
	ostr = show_model(pif, mod)
    else:
	ostr = box['mod_id'] + '<br>'
    #ostr += pic_name + '<br>\n'
    for col in pif.dbh.get_table_info('box_type')['columns']:
	if col not in ign_cols:
	    if box[col]:
		ostr += '<b>%s</b><ul>\n' % box_lookups.get(col, {}).get('_title', col)
		for spec in box[col].split('/'):
		    ostr += '<li>%s\n' % box_lookups.get(col, {}).get(spec, spec).replace('\n', '<br>')
		ostr += '</ul>\n'
    ostr += '<center>' + pif.render.format_image_selector(pics, pic_name) + '</center>'
    istr = pif.render.format_image_selectable(pics, pic_name)
    if pif.is_allowed('ma'):
	istr = '<a href="upload.cgi?d=%s&n=%s">%s</a>' % (config.IMG_DIR_BOX, pic_name + '.jpg', istr)
    ent = {'inf': ostr, 'pic': istr }
    return ent

def single_box_type(pif):
    pif.render.set_page_extra(pif.render.image_selector_js)
    if pif.form.get_str('box'):
	boxes = pif.dbh.fetch_box_type(pif.form.get_str('box'))
    elif pif.form.get_str('mod'):
	boxes = pif.dbh.fetch_box_type_by_mod(pif.form.get_str('mod'), pif.form.get_str('ty'))
    if not boxes:
	raise useful.SimpleError("No matching boxes found.")
    boxes = pif.dbh.depref('box_type', boxes)
    mod = pif.dbh.fetch_casting_by_id_or_alias(boxes[0]['mod_id'])
    if mod:
	mod = mod[0]
	mod['id'] = mod['alias.id'] if mod['alias.ref_id'] else mod['casting.id']

    lsection = dict(columns=['inf', 'pic'], headers={'inf': 'Box Information', 'pic': 'Box Picture'},
	range=[dict(entry=[single_box(pif, mod, x) for x in boxes], note='')], note='')
    llistix = dict(section=[lsection])
    return llistix

# need to add va, middle to eb_1 style

def get_box_image(pif, picroot, picsize=None, largest='c', compact=False):
    if compact:
	product_image = pif.render.find_image_path(picroot, prefix=picsize + '_')
	pic = pif.render.format_image_art(imglib.image_star(product_image, target_x=mbdata.imagesizes[picsize][0]))
    elif picsize:
	pic = pif.render.format_image_required(picroot, prefix=picsize + '_')
    else:
	pic = pif.render.format_image_required(picroot, largest=largest)
    return pic


def show_model(pif, mod, compact=False):
    img = '' if compact else pif.render.format_image_required(mod['casting.id'], pdir=config.IMG_DIR_MAN, largest='s')
    url = "single.cgi?id=" + mod['casting.id']
    ostr  = '<center><a href="%s">%s<br>%s<br>' % (url, mod['id'], img)
    ostr += '<b>%s</b></a></center>' % mod['base_id.rawname'].replace(';', ' ')
    return ostr


def find_boxes(pif):
    series = pif.form.get_str('series')
    style = pif.form.get_str('style')
    if style == 'all':
	style = ''
    start = pif.form.get_int('start', 1)
    end = pif.form.get_int('end', start)
    boxes = dict()
    for box in pif.dbh.fetch_castings_by_box(series, style):
        box['id'] = box['alias.id'] if box.get('alias.id') else box['casting.id']
	pic_name = ('x_%s-%s%s' % (box['box_type.mod_id'], box['box_type.box_type'][0], box['box_type.pic_id'])).lower()
	is_pic = int(os.path.exists(os.path.join(config.IMG_DIR_BOX, pic_name + '.jpg')))
	sortid = box['id'][2:4] + box['id'][0:2] + box['id'][4:] + box['box_type.box_type'][0]
	if sortid in boxes:
	    boxes[sortid]['count'] += 1
	    boxes[sortid]['pics'] += is_pic
	    continue
        if (series and box['base_id.model_type'] != series) or \
		(style and (style != box['box_type.box_type'][0])) or \
		(int(box['id'][2:4]) < start) or \
		((end and int(box['id'][2:4]) > end) or (not end and int(box['id'][2:4]) != start)):
	    continue
	box['count'] = 1
	box['pics'] = is_pic
	boxes[sortid] = box
    return boxes


def get_pic_roots(mod_id, box_style):
    picroots = glob.glob(os.path.join(config.IMG_DIR_BOX, ('[scm]_' + mod_id + '-' + box_style + '?.jpg').lower()))
    picroots = list(set([(mod_id + '-' + box_style).lower()] + [x[x.rfind('/') + 3:-4] for x in picroots]))
    picroots.sort()
    return picroots


def show_boxes(pif):
    pif.render.print_html()
    if pif.form.get_str('box') or pif.form.get_str('mod'):
	return pif.render.format_template('simplelistix.html', llineup=single_box_type(pif))

    verbose = pif.form.get_bool('verbose')
    compact = pif.form.get_bool('c')
    style = pif.form.get_str('style')
    if style == 'all':
	style = ''
    headers = {'mod': 'Model', 'm': 'M', 'c': 'C', 's': 'S', 'box': 'Box'}
    columns = ['mod', 'm', 'c', 's'] if verbose else ['mod', 'box']

    boxes = find_boxes(pif)

    lrange = dict(note='', entry=list())
    boxids = boxes.keys()
    boxids.sort()
    modids = list(set([x[:5] for x in boxids]))
    modids.sort()
    for mod_id in modids:
	mod_box_ids = [x for x in boxids if x.startswith(mod_id)]
	mod_box_ids.sort()
	ent = {'mod': {'txt': show_model(pif, boxes[mod_box_ids[0]], compact=compact), 'rows': len(mod_box_ids)}}
	ent1 = ent
	for mod_box_id in mod_box_ids:
	    mod = boxes[mod_box_id]
	    box_style = mod['box_type.box_type'][0]
	    picroots = get_pic_roots(mod['id'], box_style)
	    if verbose:
		ent1['mod']['txt'] += '<br>' + '<br>'.join(picroots)
	    hdr = "<b>%s style</b>" % box_style
	    if verbose:
		for picsize in 'mcs':
		    imgs = [get_box_image(pif, picroot, picsize, compact=compact) for picroot in picroots]
		    if compact:
			ostr = hdr + ''.join(imgs)
		    else:
			ostr = "<center>%s</center>" % hdr + '<br>'.join(imgs)
		    if pif.is_allowed('ma'):
			ostr = '<a href="upload.cgi?d=%s&n=%s">%s</a>' % (config.IMG_DIR_BOX, mod['id'].lower() + '-' + box_style.lower() + '.jpg', ostr)
		    ent[picsize] = {'txt': ostr}
		ent['s']['txt'] += '<br>%s box variations - %s' % (mod['count'], pif.render.format_button('see the boxes', link='?mod=%s&ty=%s' % (mod['id'], box_style)))
		ent['s']['txt'] += ' - %s pics' % mod['pics']
	    else:
		largest = 'mmcss'[len(picroots)]
		pic = ''.join([get_box_image(pif, picroot, largest=largest) for picroot in picroots])
		ent['box'] = {'txt': "<center>%s<br>%s" % (hdr, pic)}
		ent['box']['txt'] += '<br>%s box variation%s - %s' % (mod['count'], 's' if mod['count'] != 1 else '', pif.render.format_button('see the boxes', link='?mod=%s&ty=%s' % (mod['id'], box_style)))
		if pif.is_allowed('ma'):
		    ent['box']['txt'] += ' - %s pics' % mod['pics']
		ent['box']['txt'] += '</center>'
	    lrange['entry'].append(ent)
	    ent = dict(mod=None)
    lsection = dict(columns=columns, headers=headers, range=[lrange], note='')
    llistix = dict(section=[lsection])
    return pif.render.format_template('boxes.html', llistix=llistix)


def box_ask(pif):
    pif.render.print_html()
    pif.render.set_page_extra(pif.render.reset_button_js)
    pif.render.set_page_extra(pif.render.increment_js)
    return pif.render.format_template('boxes.html')


@basics.web_page
def box_main(pif):
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/boxart.cgi', 'Lesney Era Boxes')
    if pif.form.form:
	return show_boxes(pif)
    else:
	return box_ask(pif)


def count_boxes(pif):
    series = ""
    style = ""
    boxes = pif.dbh.fetch_castings_by_box(series, style)
    for box in boxes:
        if 'alias.id' in box:
            box['id'] = box['alias.id']
        else:
            box['id'] = box['casting.id']

    pr_count = im_count = 0
    for box in boxes:
        if box['id'].startswith('M'):
            continue
        if series and box['base_id.model_type'] != series:
            continue
        if style and style not in box['box_style.styles']:
            continue

        for c in box['box_style.styles'].replace('-', ''):
            if pif.render.find_image_path(['s_' + box['id'] + '-' + c], pdir=config.IMG_DIR_BOX):
                im_count += 1
            if pif.render.find_image_path(['c_' + box['id'] + '-' + c], pdir=config.IMG_DIR_BOX):
                im_count += 1
            if pif.render.find_image_path(['m_' + box['id'] + '-' + c], pdir=config.IMG_DIR_BOX):
                im_count += 1
            pr_count += 1

    return pr_count, im_count


@basics.command_line
def commands(pif):

    boxes = find_boxes(pif)
    keys = boxes.keys()
    keys.sort()

    for key in keys:
	for picroot in get_pic_roots(boxes[key]['id'], boxes[key]['box_type.box_type'][0]):
	    print '%-9s' % picroot,
	    for picsize in 'mcs':
		img = pif.render.find_image_path(picroot, prefix=picsize + '_', pdir=config.IMG_DIR_BOX)
		if not img:
		    print '.',
		else:
		    imginf = imglib.img_info(img)
		    if imginf[1] < mbdata.imagesizes[picsize][0]:
			print picsize,
		    else:
			print picsize.upper(),
	    print

    check_database(pif)


# not in use, just here so I don't forget how I did it.
def check_database(pif):
    fields = {}
    for e in pif.dbh.fetch('box_type'):
	for f in e:
	    if e[f] and f[9:] not in ('notes', 'year', 'id', 'pic_id', 'mod_id'):
		fields.setdefault(f[9:], set())
		fields[f[9:]].update(e[f].split('/'))
		for h in e[f].split('/'):
		    if h not in box_lookups[f[9:]]:
			print h, e[f], f, e['box_type.id']
    for f in fields:
	print f, fields[f] - set(box_lookups[f].keys()), set(box_lookups[f].keys()) - fields[f] - {'_title'}


if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='')
