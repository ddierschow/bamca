# flake8: noqa

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
        'AMS': 'A Moko LESNEY PRODUCT (Moko in script)',
        'AML': 'A MOKO LESNEY PRODUCT (MOKO in block capitals)',
        'ALS': 'A LESNEY PRODUCT (scroll)',
        'ALP': 'A LESNEY PRODUCT (straight)',
        'LPC': 'LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND',
        'MIR1': '''"MATCHBOX" IS THE REG'D T.M. OF LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND''',
        'MRT1': '''"MATCHBOX" REG'D T.M. LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND''',
        'MRT2': '''&copy; 197x "MATCHBOX" REG'D T.M. LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND''',
        'MRT3': '''&copy; 197x "MATCHBOX" REG'D T.M. MARCA REGISTRADA LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND''',
        'MRM': '''MARCA REGISTRADA &copy; 197x "MATCHBOX" REG'D T.M. LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND''',
        'MIR2': '''"MATCHBOX" IS THE REG'D TRADE MARK (MARCA REGISTRADA) OF LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND''',
        'MMR1': '"MATCHBOX", "MARCA REGISTRADA" REGISTERED TRADE MARK OF LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND',
        'MMR2': '"MATCHBOX", "MARCA REGISTRADA" REGISTERED TRADE MARK OF LESNEY PRODUCTS &amp; CO. LTD. LONDON E.9 5PA ENGLAND',
        'CNG': 'CONFORMIT&Eacute; AUX NORMES GARANTIE PAR LESNEY S.A.',
        'CNGL': 'CONFORMIT&Eacute; AUX NORMES GARANTIE PAR LESNEY S.A. (left)',
        'CNN': 'CONFORMIT&Eacute; AUX NORMES GARANTIE PAR LESNEY S.A.NE CONVIENT PAS &Agrave; UN ENFANT DE MOINS DE 36 MOIS',
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

# # |Box generations|Years|Lettering|Location|Combined w/ bottom types
# 3|--------IJKL|1973-81|&copy; 19xx LESNEY PRODUCTS &amp; CO. LTD. MADE IN ENGLAND|on sides|MIR2 MMR1 MMR2 CNG CNN MMR3 MIR3
# 4|--------I---|1974|&copy; 1973 LESNEY PRODUCTS &amp; CO. LTD. PRINTED AND MADE IN ENGLAND|on sides|MIR2 CNG CNN
# 5|--------I---|1975|&copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. MADE IN GREAT BRITAIN|on sides|MIR2 CNN
# 6|--------I---|1975|&copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. PRINTED AND MADE IN GREAT BRITAIN|on sides|MIR2 CNN
# 7|--------I---|1975|&copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND|on sides|MIR2 CNN
# 8|-----------L|1981|&copy; 198x LESNEY PRODUCTS &amp; CO. LTD. MADE IN HONG KONG|on sides|MIR3
# 9|-----------L|1982|&copy; 1981 LESNEY PRODUCTS P.L.C. MADE IN ENGLAND|on sides|MIR4

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
        # 'B6': 'black &copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. PRINTED AND MADE IN GREAT BRITAIN',
        # 'B7': 'black &copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. LONDON ENGLAND',
        'W3': 'white &copy; 197x LESNEY PRODUCTS &amp; CO. LTD. MADE IN ENGLAND',
        'W4': 'white &copy; 1973 LESNEY PRODUCTS &amp; CO. LTD. PRINTED AND MADE IN ENGLAND',
        # 'W5': 'white &copy; 1974 LESNEY PRODUCTS &amp; CO. LTD. MADE IN GREAT BRITAIN',
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
