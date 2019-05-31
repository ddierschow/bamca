#!/usr/local/bin/python

import copy, glob, itertools, os
import basics
import bfiles
import config
import imglib
import mbdata
import models
import useful


# ----- package --------------------------------------------------------

def tree_row(tree, text):
    return "%s%s\n<br>\n" % (tree, text)


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
    ostr = ''
    for llist in dblist:
        cmd = llist.get_arg()
        if cmd == 'dir':
            pif.render.pic_dir = llist.get_arg()
        elif cmd == 'render':
            ostr += useful.render_file(pif.render.pic_dir + '/' + llist.get_arg())
        elif cmd == 'p':
            ostr += '<p>\n'
        elif cmd == 's':
            ostr += '<p>\n<b id="%s"><u>' % llist[1]
            if llist[2]:
                ostr += ' %s - ' % llist[2]
            ostr += '%s</u></b><br>\n' % llist[3]
        elif cmd == 'm':
            desc = ''
            if llist[2]:
                desc += ('<b>%s</b> ' % llist[2])
                if llist[3] and not llist[3][0].isupper():
                    desc += " - "
            desc += llist[3]
	    if llist[1].endswith('p'):
                desc = '<b>%s</b>' % desc
            #ostr += render_tree(pif, llist[1]) + desc
            #ostr += '<br>\n'
            ostr += tree_row(render_tree(pif, llist[1]), desc)
        elif cmd == 'n':
            ostr += tree_row(render_tree(pif, llist[1]), '<font color="#666600"><i>%s</i></font>' % llist[2])
        elif cmd == 'a':
            ostr += tree_row(render_tree(pif, llist[1]), pif.render.format_image_as_link([llist[2]], llist[3], also={'target': '_showpic'}))
        elif cmd == 'e':
            flist = sorted(glob.glob(pif.render.pic_dir + '/' + llist[2] + "*.jpg"))
            if flist:
                ostr += '<font color="blue">'
                ostr += tree_row(render_tree(pif, llist[1]), ('<i>Example%s:</i>\n' % useful.plural(flist)) + show_pic(pif, flist))
                ostr += '</font>\n'
    return ostr


@basics.web_page
def blister(pif):
    pif.render.print_html()
    #global pagename
    #pagename = pif.form.get_str('page', 'blister')

    dblist = bfiles.SimpleFile(useful.relpath(config.SRC_DIR, pif.page_name + '.dat'))

    print pif.render.format_head()
    useful.header_done()
    print do_tree_page(pif, dblist)
    print pif.render.format_tail()

# ----- boxart ---------------------------------------------------------

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
	'CNGL':  'CONFORMIT&Eacute; AUX NORMES GARANTIE PAR LESNEY S.A. (left)',
	'CNN':  'CONFORMIT&Eacute; AUX NORMES GARANTIE PAR LESNEY S.A.NE CONVIENT PAS &Agrave; UN ENFANT DE MOINS DE 36 MOIS',
	'MMR3': '"MATCHBOX" (MARCA REGISTRADA) REGISTERED TRADE MARK OF LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND',
	'MIR3': '"MATCHBOX" IS THE REGISTERED TRADE MARK (MARCA REGISTRADA) OF LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND',
	'MIR4': '"MATCHBOX" IS THE REGISTERED TRADE MARK (MARCA REGISTRADA) OF LESNEY PRODUCTS P.L.C. LONDON ENGLAND',
	'NRC': 'Not recommended for children under 3.',
	'NRCC': 'Not recommended for children under 3. (central)',
	'3L': 'text on three lines',
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
	'E3': 'model number, name and colour picture',
	'E4': 'model number, name, "MATCHBOX" and colour picture',
	'E4R': 'model number, name, "MATCHBOX" with "&reg;" and colour picture',
	'SCC': 'SPECIFICATION AND COLOUR OF CONTENTS SUBJECT TO AMENDMENT',
	'PO': "PORTI&Egrave;RES OUVRANTES - LICENCE SOLIDO",
	'TM': 'Trademark "MATCHBOX"&reg; Owned By Lesney Products &amp; Co. Ltd.',
	'TME': 'Trademark "MATCHBOX"&reg; Owned By Lesney Products &amp; Co. Ltd. Printed in England. Made in England.',
	'MK': "MARK",
	'MKI': "MARK I",
	'MK1': "MARK 1",
	'MK2': "MARK 2",
	'MK3': "MARK 3",
	'MK4': "MARK 4",
	'MK5': "MARK 5",
	'MK6': "MARK 6",
	'MK7': "MARK 7",
	'CTC': 'MADE BY LESNEY PRODUCTS &amp; CO. LTD., AND SOLD UNDER PERMISSION FROM CATERPILLAR TRACTOR COMPANY.',
	'N': '"NEW"',
	'NM': '"NEW MODEL"',
	'SD': 'small digits',
	'LD': 'large digits',
    },
    'sides': {
	'?': 'unknown',

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
	#'B6': 'black &copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. PRINTED AND MADE IN GREAT BRITAIN',
	#'B7': 'black &copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND',
	'W3': 'white &copy; 197x LESNEY PRODUCTS &amp; CO. LTD. MADE IN ENGLAND',
	'W4': 'white &copy; 1973 LESNEY PRODUCTS &amp; CO. LTD. PRINTED AND MADE IN ENGLAND',
	#'W5': 'white &copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. MADE IN GREAT BRITAIN',
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
	'_title': 'Additional Text on Front',
	# ABC
	'NO': '"No." with model number',
	'REGD': 'with "REG.D"',
	'NOREGD': 'without "REG.D"',
	# DE
	'NUM': 'model number',
	'WN': 'wider model number',
	'NN': 'narrower model number',
	'LNWS': 'large number with serifs',
	'NFM': 'number far from model',
	'NNM': 'number near by model',
	'SNWS': 'small number with serifs',
	'SNNS': 'small number without serifs',
	'VSNWS': 'very small number with serifs',
	# F
	'AST': '"AUTOSTEER"',
	'BSF': 'black "Superfast"',
	'SBSF': 'small black "Superfast"',
	'LBSF': 'large black "Superfast"',
	'RLB': '"SERIES" in red left of blue number box',
	'RSF': 'red "Superfast"',
	'RUB': '"SERIES" in red under oblong blue number box',
	'WIB': '"SERIES" in white in blue number box',
	# G
	'BLK': 'black "TM"',
	'RED': 'red "TM"',
	'RT.M.': 'red "T.M."',
	'TM1': '"TM" on one front only',
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
	# K
	'SJ': '1952-1977 Silver Jubilee',
    },
    'year': {
	'_title': 'Year on Box',
    },
    'model_name': {
	'_title': 'Model Name',
    },
    'notes': {
	'_title': 'Notes',
    },
}

def box_lookup(col, val):
    return [box_lookups.get(col, {}).get(x, x) for x in val.split('/')]

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
		ostr += '<b>%s</b><ul>\n' % box_lookup(col, '_title')[0]
		for spec in box_lookup(col, box[col]):
		    ostr += '<li>%s\n' % spec.replace('\n', '<br>')
		ostr += '</ul>\n'
    istr = pif.render.format_image_selectable(pics, pic_name)
    if pif.is_allowed('ma'):
	istr = '<a href="upload.cgi?d=.%s&n=%s">%s</a>' % (config.IMG_DIR_BOX, pic_name + '.jpg', istr)
	istr += '<br>' + pif.render.format_button("edit", link=pif.dbh.get_editor_link('box_type', {'id': box['id']}))
    istr += '<center>' + pif.render.format_image_selector(pics, pic_name) + '</center>'
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

def get_box_image(pif, picroot, picsize=None, largest=mbdata.IMG_SIZ_PETITE, compact=False):
    if compact:
	product_image_path, product_image_file = pif.render.find_image_file(picroot, prefix=picsize)
	pic = imglib.format_image_star(pif, product_image_path, product_image_file, target_x=mbdata.imagesizes[picsize][0])
    elif picsize:
	pic = pif.render.format_image_required(picroot, prefix=picsize)
    else:
	pic = pif.render.format_image_required(picroot, largest=largest)
    return pic


def show_model(pif, mod, compact=False):
    img = '' if compact else pif.render.format_image_required(mod['casting.id'], pdir=config.IMG_DIR_MAN, largest=mbdata.IMG_SIZ_SMALL)
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
        if (series and box['base_id.model_type'] != series) or \
		(style and (style != box['box_type.box_type'][0])) or \
		(int(box['id'][2:4]) < start) or \
		((end and int(box['id'][2:4]) > end) or (not end and int(box['id'][2:4]) != start)):
	    continue
	pic_name = ('x_%s-%s%s' % (box['box_type.mod_id'], box['box_type.box_type'][0], box['box_type.pic_id'])).lower()
	is_pic = int(os.path.exists(useful.relpath('.', config.IMG_DIR_BOX, pic_name + '.jpg')))
	sortid = box['id'][2:4] + box['id'][0:2] + box['id'][4:] + box['box_type.box_type'][0]
	front = ' / '.join(
		box_lookup('box_type', box['box_type.box_type']) +
		box_lookup('bottom', box['box_type.bottom']) +
		box_lookup('additional_text', box['box_type.additional_text']) +
		[box['box_type.notes']])
	if sortid in boxes:
	    boxes[sortid]['count'] += 1
	    boxes[sortid]['pics'] += is_pic
	    if front not in boxes[sortid]['fronts']:
		boxes[sortid]['fronts'].append(front)
	    continue
	box['count'] = 1
	box['pics'] = is_pic
	box['fronts'] = [front]
	boxes[sortid] = box
    return boxes


def get_pic_roots(mod_id, box_style):
    picroots = glob.glob(useful.relpath('.', config.IMG_DIR_BOX, ('[scm]_' + mod_id + '-' + box_style + '?.jpg').lower()))
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
    headers = {'mod': 'Model', 'm': 'M', 'p': 'P', 's': 'S', 'box': 'Box'}
    columns = ['mod', 'm', 'p', 's'] if verbose else ['mod', 'box']

    boxes = find_boxes(pif)

    lrange = dict(note='', entry=list())
    boxids = sorted(boxes.keys())
    modids = sorted(list(set([x[:5] for x in boxids])))
    for mod_id in modids:
	mod_box_ids = [x for x in boxids if x.startswith(mod_id)]
	mod_box_ids.sort()
	ent = {'mod': {'txt': show_model(pif, boxes[mod_box_ids[0]], compact=compact), 'rows': len(mod_box_ids)}}
	ent1 = ent
	for mod_box_id in mod_box_ids:
	    mod = boxes[mod_box_id]
#	    if verbose and pif.is_allowed('ma'):
#		print '<br>'.join(mod['fronts']), '<hr>'
	    box_style = mod['box_type.box_type'][0]
	    picroots = get_pic_roots(mod['id'], box_style)
	    if verbose:
		ent1['mod']['txt'] += '<br>' + '<br>'.join(picroots)
	    hdr = "<b>%s style</b>" % box_style
	    if verbose:
		for picsize in 'mps':
		    imgs = [get_box_image(pif, picroot, picsize, compact=compact) for picroot in picroots]
		    if compact:
			ostr = hdr + ''.join(imgs)
		    else:
			ostr = "<center>%s</center>" % hdr + '<br>'.join(imgs)
		    if pif.is_allowed('ma'):
			ostr = '<a href="upload.cgi?d=.%s&n=%s">%s</a>' % (config.IMG_DIR_BOX, mod['id'].lower() + '-' + box_style.lower() + '.jpg', ostr)
		    ent[picsize] = {'txt': ostr}
		ent['s']['txt'] += '<br>%s box variations - %s' % (mod['count'], pif.render.format_button('see the boxes', link='?mod=%s&ty=%s' % (mod['id'], box_style)))
		ent['s']['txt'] += ' - %s pics' % mod['pics']
	    else:
		largest = 'mmpss'[len(picroots)]
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
    boxes = pif.dbh.fetch_castings_by_box('', '')
    box_styles = set()
    pr_count = im_count = 0
    for box in boxes:
        if 'alias.id' in box:
            box['id'] = box['alias.id']
        else:
            box['id'] = box['casting.id']

        if box['id'].startswith('M'):
	    print box
            continue

	box_styles.add(box['id'] + '-' + box['box_type.box_type'])
	pr_count += 2
	im_count += len(glob.glob(useful.relpath('.', config.IMG_DIR_BOX, 'x_' + box['id'] + '-' + box['box_type.box_type'] + box['box_type.pic_id'] + '*.jpg')))

    for box in box_styles:
	if pif.render.find_image_path(box, pdir=config.IMG_DIR_BOX, prefix=mbdata.IMG_SIZ_SMALL):
	    im_count += 1
	if pif.render.find_image_path(box, pdir=config.IMG_DIR_BOX, prefix=mbdata.IMG_SIZ_PETITE):
	    im_count += 1
	if pif.render.find_image_path(box, pdir=config.IMG_DIR_BOX, prefix=mbdata.IMG_SIZ_MEDIUM):
	    im_count += 1
	pr_count += 1

    return pr_count, im_count

# ----- pub ------------------------------------------------------------

@basics.web_page
def publication(pif):
    pub_id = pif.form.get_str('id')
    pub_type = pif.form.get_str('ty')
    pif.render.print_html()
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/pub.cgi', 'Publications')
    pif.render.set_button_comment(pif)

    if pub_id:
	return single_publication(pif, pub_id)
    elif pub_type:
	return publication_list(pif, pub_type)
    pubs = pif.dbh.fetch_publication_types()

    def fmt_link(sec):
	txt = models.add_icons(pif, 'p_' + sec.id, '', '')
#	if sec.id == 'ads':
#	    return pif.render.format_link('ads.cgi', txt)
	return pif.render.format_link('?ty=' + sec.category, txt)

    return models.make_page_list(pif, 'pub', fmt_link)


def get_section_by_model_type(pif, mtype):
    for sec in pif.dbh.fetch_sections_by_page_type(mbdata.page_format_type['pub']):
	if sec.category == mtype:
	    return sec
    return {}


def publication_list(pif, mtype):
    sec = get_section_by_model_type(pif, mtype)
    if sec.id == 'ads':
	raise useful.Redirect('ads.cgi?title=' + pif.form.get_str('title'))
    sobj = pif.form.search('title')
    pif.render.pic_dir = sec.page_info.pic_dir
    pubs = pif.dbh.fetch_publications(model_type=mtype)

    def pub_ent(pub):
	ret = pub.todict()
	ret.update(ret['base_id'])
	if not useful.search_match(sobj, ret['rawname']):
	    return None
	ret['name'] = '<a href="pub.cgi?id=%s">%s</a>' % (ret['id'], ret['rawname'].replace(';', ' '))
	ret['description'] = useful.printablize(ret['description'])
	if (os.path.exists(os.path.join(pif.render.pic_dir, ret['id'].lower() + '.jpg')) or
		glob.glob(os.path.join(pif.render.pic_dir, '?_' + ret['id'].lower() + '_*.jpg')) or
		glob.glob(os.path.join(pif.render.pic_dir, '?_' + ret['id'].lower() + '.jpg'))):
	    ret['picture'] = mbdata.comment_icon['c']
	return ret

    if 1:
	entry = [pub_ent(pub) for pub in pubs]
	hdrs = {'description': 'Description', 'first_year': 'Year', 'country': 'Country',
		'flags': 'Flags', 'model_type': 'Type', 'id': 'ID', 'name': 'Name', 'picture': ''}
	cols = ['picture', 'name', 'description', 'first_year', 'country']

	lrange = dict(entry=[x for x in entry if x], styles=dict(zip(cols, cols)))
	lsection = dict(columns=cols, headers=hdrs, range=[lrange], note='', name=sec.name)
	llistix = dict(section=[lsection])
	return pif.render.format_template('simplelistix.html', llineup=llistix)


    cols = 4

    def pub_text_link(pub):
	pic = pif.render.fmt_img(pub['id'], prefix='s')
	name = pic + '<br>' + pub['name'] if pic else pub['name']
	return {'text': pif.render.format_link("makes.cgi?make=" + pub['id'], name)}

    ents = [pub_text_link(pub_ent(x)) for x in pubs]
    llineup = {'id': '', 'name': '', 'columns': cols, 'header': '', 'footer': '',
	'section': [{'columns': cols, 'range': [{'entry': ents, 'id': 'makelist'}]}]}

    pif.render.format_matrix_for_template(llineup)
    return pif.render.format_template('simplematrix.html', llineup=llineup)


def make_relateds(pif, ref_id, pub_id, imgs):
    pic = imgs[0] if imgs else ''
    relateds = pif.dbh.fetch_casting_relateds(pub_id, section_id='pub')
    vs = pif.dbh.fetch_variation_selects_by_ref(ref_id, pub_id)
    retval = []
    for related in relateds:
	related['id'] = related['casting_related.related_id']
	vars = [x for x in vs if x['variation_select.mod_id'] == related['id']]
	descs = [x.get('variation.text_description', '') for x in vars] + related.get('casting_related.description', '').split(';')
	related = pif.dbh.modify_man_item(related)
	related['descs'] = [x for x in descs if x]
	related['imgid'] = [related['id']]
	for s in related['descs']:
	    if s.startswith('same as '):
		related['imgid'].append(s[8:])
	related['img'] = pif.render.format_image_required(related['imgid'], made=related['made'], pdir=config.IMG_DIR_MAN, vars=[x['variation_select.var_id'] for x in vars], largest=mbdata.IMG_SIZ_SMALL)
	if related['link']:
	    related['link'] = '%s=%s&dir=%s&pic=%s&ref=%s&sec=%s' % (related['link'], related['linkid'], pif.render.pic_dir, pic, ref_id, pub_id)
	    related['img'] = '<a href="%(link)s">%(img)s</a>' % related
	related['descs'] = '<br>'.join(['<div class="varentry">%s</div>' % x for x in related['descs']])
	retval.append({'text': '''<span class="modelnumber">%(id)s</span><br>\n%(img)s<br>\n<b>%(name)s</b>\n<br>%(descs)s\n''' % related})
    return retval


def single_publication(pif, pub_id):
    man = pif.dbh.fetch_publication(pub_id).first
    if not man:
	raise useful.SimpleError("That publication was not found.")
    # should just use man.section_id
    sec = get_section_by_model_type(pif, man.base_id.model_type)
    pif.set_page_info(sec.page_info.id)
    man['casting_type'] = 'Publication'
    man['name'] = man['base_id.rawname'].replace(';', ' ')
    imgs = pub_images(pif, pub_id.lower())
    relateds = make_relateds(pif, 'pub.' + mbdata.model_type_names[man['base_id.model_type']].lower(), pub_id, imgs)

    left_bar_content = ''
    if pif.is_allowed('a'):  # pragma: no cover
        left_bar_content += '<p><b><a href="%s">Base ID</a><br>\n' % pif.dbh.get_editor_link('base_id', {'id': pub_id})
        left_bar_content += '<a href="%s">Publication</a><br>\n' % pif.dbh.get_editor_link('publication', {'id': pub_id})
        left_bar_content += '<a href="traverse.cgi?d=%s">Library</a><br>\n' % pif.render.pic_dir.replace('pic', 'lib')
	left_bar_content += '<a href="upload.cgi?d=%s&n=%s&c=%s">Product Upload</a><br>\n' % (pif.render.pic_dir.replace('pic', 'lib'), pub_id, pub_id)

    upper_box = ''
    if imgs:
	upper_box += pif.render.format_image_link_image(imgs[0], link_largest=mbdata.IMG_SIZ_LARGE)
#    else:
#	upper_box += pif.render.format_image_link_image(img, link_largest=mbdata.IMG_SIZ_LARGE)
    if man['base_id.description']:
	upper_box += '<br>' if upper_box else ''
	upper_box += useful.printablize(man['base_id.description'])

    lran = [{'id': 'ran', 'entry':
	[{'text': pif.render.format_image_link_image(img[img.rfind('/') + 1:])} for img in sorted(imgs)] if imgs else
	[{'text': pif.render.format_image_link_image(pub_id)}]
    } if len(imgs) > 1 else {}]
    if relateds:
	lran.append({'id': 'related', 'entry': relateds, 'name': 'Related Models'})
    llineup = {'id': pub_id, 'name': '', 'section': [{'id': 'sec', 'range': lran, 'columns': 4}], 'columns': 4}

    pif.render.set_button_comment(pif, 'id=%s' % pub_id)
    pif.render.format_matrix_for_template(llineup)
    context = {
	'title': man.get('name', ''),
	'note': '',
	'type_id': 'p_' + sec.id,
	#'icon_id': pub_id,
	'vehicle_type': '',
	'rowspan': 5 if upper_box else 4,
	'left_bar_content': left_bar_content,
	'upper_box': upper_box,
	'llineup': llineup,
    }
    return pif.render.format_template('pub.html', **context)


def pub_images(pif, pub_id):
    imgs = glob.glob(os.path.join(pif.render.pic_dir, '?_' + pub_id + '_*.jpg'))
    imgs = list(set([os.path.split(fn)[1][2:-4] for fn in imgs]))
    if (os.path.exists(os.path.join(pif.render.pic_dir, pub_id + '.jpg')) or
	    glob.glob(os.path.join(pif.render.pic_dir, '?_' + pub_id + '.jpg'))):
	imgs.insert(0, pub_id)
    imgs.sort()
    return imgs

# ----- advertising ---- the special snowflake -------------------------

@basics.web_page
def ads_main(pif):
    pif.render.print_html()
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/ads.cgi', 'Advertisements')
    pif.render.set_button_comment(pif)
    pic_dir = pif.render.pic_dir
    lib_dir = pic_dir.replace('pic', 'lib')
    ranges = []
    sobj = pif.form.search('title')

    def fmt_cy(ent):
	cy = ent.get('country', '')
	cyflag = pif.render.show_flag(cy) if (cy and cy != 'US') else ''
	cyflag = (' <img src="' + cyflag[1] + '">') if cyflag else ''
	return cy, cyflag

    def fmt_vid(ent):
	#sep = pif.render.format_image_art('wheel.gif', also={'class': 'dlm'})
	# add country
	cy, cyflag = fmt_cy(ent)
	cmt = ent['description']
	ostr = pif.render.format_link(ent['url'], ent['name'])
	if cmt:
	    ostr += ' ' + cmt
	ostr += cyflag
	ostr += (' ' + pif.render.format_link('edlinks.cgi?id=%s' % ent['id'], '<i class="fas fa-edit"></i>')) if pif.is_allowed('ma') else ''
	return ostr

    #id, page_id, section_id, display_order, flags, associated_link, last_status, link_type, country, url, name, description, note
    vlinks = [fmt_vid(x) for x in
	pif.dbh.depref('link_line', pif.dbh.fetch_link_lines(page_id='links.others', section='Lvideoads', order='name'))
	if useful.search_match(sobj, x['name'])
    ]

    def fmt_pub(ent, pdir=None):
	pdir = pdir if pdir else pic_dir
	ldir = pdir.replace('pic', 'lib')
	# ent: id, description, country, first_year, model_type
	cy, post = fmt_cy(ent)
	_, floc = pif.render.find_image_file(ent['id'], largest='e', pdir=pdir)
	_, lloc = pif.render.find_image_file(ent['id'], largest='e', pdir=ldir)
	#floc = pdir + '/' + ent['id'] + '.jpg'
	#lloc = floc.replace('/pic/', '/lib/')
	if floc:
	    if ent['model_type']:
		url = 'pub.cgi?id=' + ent['id']
	    else:
		url = '/' + pdir + '/' + floc
	else:
	    url = '/' + ldir + '/' + lloc
	if not useful.search_match(sobj, ent['description']):
	    return ''
	name = useful.printablize(ent['description'])
	if ent['first_year']:
	    name += ' (' + ent['first_year'] + ')'
	if pif.is_allowed('ma'):
	    if ent['model_type']:
		post += ' ' + pif.render.format_link(pif.dbh.get_editor_link('publication', {'id': ent['id']}), '<i class="fas fa-edit"></i>')
	    else:
		post += ' ' + pif.render.format_link(
'/cgi-bin/mass.cgi?type=ads&id=%s&description=%s&year=%s&country=%s' % (ent['id'], useful.url_quote(ent['description'], plus=True), ent['first_year'], cy)
, '<i class="far fa-plus-square"></i>'
)
	    if floc:
		post += ' ' + pif.render.format_link('/cgi-bin/imawidget.cgi?d=%s&f=%s' % (pdir, floc), '<i class="fas fa-paint-brush"></i>')
	    elif lloc:
		post += ' ' + pif.render.format_link('/cgi-bin/imawidget.cgi?d=%s&f=%s' % (ldir, lloc), '<i class="fas fa-paint-brush"></i>')
	    post += ' ' + pif.render.format_link('/cgi-bin/upload.cgi?d=%s&n=%s' % (ldir, ent['id']), '<i class="fas fa-upload"></i>')
	    name = ent['id'] + ' - ' + name
	if floc:
	    return pif.render.format_link(url, name) + post
	return name + post

    fields = {
	'id': 'id',
	'description': 'base_id.description',
	'first_year': 'base_id.first_year',
	'country': 'country',
	'model_type': 'base_id.model_type',
	'rawname': 'base_id.rawname',
    }
    def mangle_object(x):
	return {y: x[fields[y]] for y in fields}

    links = {x.id: mangle_object(x) for x in pif.dbh.fetch_publications(model_type='AD', order='base_id.first_year,base_id.id')}
    pic_ims = ad_images(pic_dir)
    missing_pics = sorted(set(links.keys()) - set(pic_ims))
    lib_ims = sorted(set(ad_images(lib_dir)) - set(links.keys()))
    pic_ims = sorted(set(pic_ims) - set(links.keys()))
    list_ents = {ent[0]: dict(itertools.izip_longest(['id', 'description', 'first_year', 'country', 'model_type'], ent))
	for ent in [x.strip().split('|') for x in open(pic_dir + '/list.dat').readlines()]}
    list_ids = sorted(set(list_ents.keys()) - set(links.keys()))
    link_ids = sorted(set(links.keys()) - set(missing_pics), key=lambda x: (links[x]['first_year'], links[x]['id']))

    plinks = list()
    for pic_id in link_ids:
	plinks.append(fmt_pub(links[pic_id]))
    ranges.append({'entry': plinks})

    plinks = [fmt_pub(list_ents[lid]) for lid in list_ids]
    if plinks:
	ranges.append({'name': 'More information is needed on these (year, location).', 'entry': plinks})

    if pif.is_allowed('ma'):
	plinks = [fmt_pub({'id': ent, 'description': ent, 'first_year': '', 'model_type': ''}, lib_dir)
	    for ent in lib_ims]
	if plinks:
	    ranges.append({'name': '<i>Nonpublished ads</i>', 'entry': plinks})

	missing = [fmt_pub(links[pic_id]) for pic_id in missing_pics]
	if missing:
	    ranges.append({'name': '<i>Database entries missing pictures</i>', 'entry': missing})

    lsecs = [
	{'id': 'print', 'name': 'Print Advertising', 'range': ranges},
	{'id': 'video', 'name': 'Video Advertising', 'range': [{'entry': vlinks}]},
    ]

    pif.render.set_footer(pif.render.format_button('back', '/') + ' to the index.')
    if pif.is_allowed('ma'):
	pif.render.set_footer(
	    pif.render.format_link('/cgi-bin/upload.cgi?d=%s' % lib_dir, 'Upload new ad') + ' - ' +
	    pif.render.format_link('/cgi-bin/edlinks.cgi?page_id=links.others&sec=Lvideoads&add=1', 'Add new video')
    )
    llineup = {'section': lsecs}
    return pif.render.format_template('simpleulist.html', llineup=llineup)


def ad_images(pdir):
    def mangle_name(x):
	x = x[x.rfind('/') + 1:-4]
	return x[2:] if x[1] == '_' else x

    return [mangle_name(x) for x in glob.glob(pdir + '/*.jpg')]

# ----- command line ---------------------------------------------------

def check_boxes(pif):
    boxes = find_boxes(pif)

    for key in sorted(boxes.keys()):
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


def check_database(pif):
    count = 0
    fields = {}
    d = pif.dbh.fetch('box_type')
    for e in d:
	x = '.' + config.IMG_DIR_BOX + '/x_' + e['box_type.mod_id'] + '-' + e['box_type.box_type'][0] + e['box_type.pic_id'] + '.jpg'
	count += int(os.path.exists(x.lower()))
	for f in e:
	    if e[f] and f[9:] not in ('notes', 'year', 'id', 'pic_id', 'mod_id', 'model_name'):
		fields.setdefault(f[9:], set())
		fields[f[9:]].update(e[f].split('/'))
		for h in e[f].split('/'):
		    if h not in box_lookups[f[9:]]:
			print h, e[f], f, e['box_type.id']
    for f in fields:
	s1 = fields[f] - set(box_lookups[f].keys())
        s2 = set(box_lookups[f].keys()) - fields[f] - {'_title'}
	if s1 or s2:
	    print f, s1, s2
    print 'x-pics', count, 'of', len(d)


def dump_database(pif):
    cols = ['id', 'pic', 'box_size', 'year', 'additional_text', 'bottom', 'sides', 'end_flap', 'model_name', 'notes']
    titles = {
	'id': 'id',
	'mod_id': 'mod_id',
	'box_type': 'typ',
	'pic_id': 'p',
	'pic': 'pic',
	'box_size': 'z',
	'year': 'year',
	'additional_text': 'addl_text',
	'bottom': 'bottom',
	'sides': 'sides',
	'end_flap': 'end_flap',
	'model_name': 'model_name',
	'notes': 'notes',
    }
    db = pif.dbh.depref('box_type', pif.dbh.fetch('box_type'))
    lens = {col: 0 for col in cols}
    for row in db:
	row['pic'] = '%s-%s%s' % (row['mod_id'], row['box_type'][0], row['pic_id'])
	for col in cols[1:]:
	    lens[col] = max(lens[col], len(row[col]))
    lens['id'] = 4
#id   | mod_id | typ | p | z | year | addl_text | bottom      | sides          | end_flap        | model_name                  | notes
    print ' | '.join([('%%-%ds' % lens[col]) % titles[col] for col in cols])
    for row in db:
	print ' | '.join([('%%-%ds' % lens[col]) % row[col] for col in cols]).strip()


# saving for later
#select id, mod_id, box_type as typ, pic_id as p, box_size as z, year, additional_text as addl_text, bottom, sides, end_flap, model_name, notes from box_type;

def blister_things(pif):
    dblist = bfiles.SimpleFile(useful.relpath(config.SRC_DIR, 'blister.dat'))
    for llist in dblist:
	if llist[0] == 'm':
	    if llist[1].endswith('p'):
		print llist[3]


cmds = [
    ('c', check_boxes, "check boxes"),
    ('d', dump_database, "dump database"),
    ('b', blister_things, "blister things"),
]


@basics.command_line
def commands(pif):
    useful.cmd_proc(pif, './prints.py', cmds)

# ----- ----------------------------------------------------------------

if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='')
