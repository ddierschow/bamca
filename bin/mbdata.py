import re

verno = ' abcdefghijklmnopqrstuvwxyz'

regionlist = ['W', 'U', 'R', 'A', 'B', 'D', 'L']

regions = {
    'W': "Worldwide",
    'U': "United States",
    'R': "Rest of World",
    'B': "Britain",
    'D': "Germany",
    'A': "Australia",
    'J': "Japan",
    'L': "Latin America",
    'X': "Worldwide",
}
reverse_regions = {regions[x]: x for x in regions}


regionparents = {
    'W': '',
    'U': 'W',
    'R': 'W',
    'B': 'R',
    'D': 'R',
    'A': 'R',
    'J': 'W',
    'L': 'W',
}

lineup_types = [
    ("man", "Main line models"),
    ("series", "Series"),
    ("ks", "Larger Scale Models"),
    ("acc", "Accessories"),
    ("yy", "Yesteryears and Matchbox Collectibles"),
    ("pack", "Packs and Gift Sets"),
    ("bld", "Buildings"),
    ("pub", "Publications"),
]

''' unidentified
HP - heroes?
MNS
MP-1
MSN
'''

categories = {
    '(IC)'  : 'Intercom City',
    '10P'   : '10-Pack',
    '3P'    : '3-Pack',
    '50P'   : '50th Anniversary Collection',
    '5P'    : '5-Pack',
    '60'    : '60th Anniversary',
    '75C'   : '75 Challenge',
    'A'     : 'Accessories',
    'AA'    : 'Across America',
    'AFL'   : 'Australian Football League',
    'AM'    : 'Across America',
    'AP'    : 'Action Pack',
    'ARL'   : 'Australian Rugby League',
    'ASAP'  : '[Code 2] ASAP Promotional',
    'ASP'   : 'Action System Pack',
    'AVN'   : 'Avon',
    'AW'    : 'Around the World',
    'BB'    : 'Best of British',
    'BH'    : 'Matchbox 50th Birthday',
    'BJ'    : 'Barrett-Jackson',
    'BK'    : 'Battle Kings',
    'BLK'   : 'Blank for Code 2 Use',
    'BOB'   : 'Best of British',
    'BOI'   : 'Best of International',
    'BOM'   : 'Best of Muscle',
    'BON'   : 'Bonus',
    'BS'    : 'Brroomstick',
    'C2'    : '[Code 2]',
    'CA'    : 'Cartoon Characters',
    'CAT'   : 'Caterpillar',
    'CC'    : 'Collectors Choice',
    'CCI'   : '[Code 2] Color Comp Promotional',
    'CCY'   : 'Collectible Convoy',
    'CDR'   : 'CD Rom',
    'CF'    : 'Commando',
    'CK'    : 'Coca-Cola',
    'CKP'   : 'Coca-Cola Premiere',
    'CL'    : 'Club Models',
    'CNS'   : 'Connoisseur Set',
    'COL'   : 'Matchbox Collectibles',
    'CQ'    : '[Code 2] Conquer',
    'CR'    : 'Code Red',
    'CRO'   : 'Crocodile Hunter',
    'CS'    : 'Construction',
    'CY'    : 'Convoy',
    'DARE'  : 'D.A.R.E.',
    'DM'    : 'Dream Machines',
    'DT'    : 'Days of Thunder',
    'DVD'   : 'DVD',
    'DY'    : 'Dinky',
    'EE'    : 'European Edition',
    'ELC'   : 'Early Learning Center',
    'ELV'   : 'Elvis Presley Collection',
    'EM'    : 'Emergency',
    'F1'    : 'Formula 1',
    'FAS'   : 'Michael Fischer-Art',
    'FC'    : 'Feature Cars',
    'FE'    : 'First Edition',
    'FM'    : 'Farming',
    'FOR'   : 'Ford Anniversary',
    'FP'    : 'Ford Anniversary',
    'G'     : 'Gift Set',
    'GC'    : 'Gold Collection',
    'GF'    : 'Graffic Traffic',
    'GS'    : 'Gift Set',
    'GW'    : 'Giftware',
    'H'     : 'Heroes',
    'HD'    : 'Harley Davidson',
    'HNH'   : "Hitch 'n' Haul",
    'HR'    : 'Heroes',
    'HS'    : 'Hot Stocks',
    'HT'    : 'Hunt',
    'IC'    : 'Intercom City',
    'IG'    : 'Inaugural Collection',
    'IN'    : 'Indy',
    'JB'    : 'James Bond',
    'JL'    : 'Justice League',
    'JR'    : 'Jurassic Park',
    'K'     : 'Super Kings (King Size)',
    'LA'    : 'Launcher',
    'LE'    : 'Limited Edition Set',
    'LES'   : 'Lesney Edition',
    'LL'    : 'My First Matchbox (Live & Learn)',
    'LP'    : 'Launcher Pack',
    'LR'    : 'Lightning',
    'LT'    : 'Lasertronic (Siren Force, Light & Sound)',
    'LW'    : 'Laser Wheels',
    'MB'    : 'Matchbox 1-75 (1-100) basic range',
    'MBR'   : 'Micro Brewery',
    'MC'    : 'Motor City',
    'MCC'   : 'My Classic Car',
    'MD'    : 'Superfast Minis',
    'MLB'   : 'Major League Baseball (USA)',
    'MO'    : 'Matchbox Originals',
    'MP'    : 'Multipack',
    'MS'    : 'Monsters',
    'MT'    : 'Matchcaps',
    'MU'    : 'Masters of the Universe',
    'NBA'   : 'National Basketball Association (USA)',
    'NBL'   : 'National Basketball League (AUS)',
    'NC'    : '[Code 2] Nutmeg Collectibles',
    'NFL'   : 'National Football League (USA)',
    'NHL'   : 'National Hockey League (USA)',
    'NM'    : 'Nigel Mansell',
    'NR'    : 'Neon Racers',
    'NSF'   : 'New Superfast',
    'OS'    : 'Osbournes',
    'P'     : 'Pre-production',
    'PB'    : 'Pleasant Books',
    'PC'    : 'Premiere Collection',
    'PR'    : 'Promotional',
    'PRC'   : 'Premiere Concept',
    'PS'    : 'Playset',
    'PVB'   : 'Pleasant Valley Books',
    'PZ'    : 'Puzzle',
    'RB'    : 'Road Blasters',
    'RT'    : 'Real Talkin',
    'SB'    : 'Skybusters',
    'SCC'   : 'Super Color Changers',
    'SCD'   : 'Scooby Doo',
    'SCS'   : 'Showcase Collection',
    'SF'    : 'Superfast',
    'SFA'   : 'Superfast America',
    'SH'    : 'Showcase',
    'SNL'   : 'Saturday Night Live',
    'SOC'   : 'Stars of Germany (Stars of Cars)',
    'SOG'   : 'Stars of Germany (Stars of Cars)',
    'SS'    : 'Showstoppers (Motor Show)',
    'ST'    : 'Super Trucks',
    'STR'   : 'Star Car',
    'TC'    : 'Team Convoy (Team Matchbox)',
    'TF'    : 'Toy Fair',
    'TH'    : 'Triple Heat',
    'TN'    : 'Then & Now',
    'TP'    : 'Twin Pack (Action System, Adventure Pack)',
    'TV'    : 'TV Tie-In',
    'TVP'   : 'TV-related Premiere',
    'TX'    : 'Texaco Collection',
    'TXP'   : 'Texaco',
    'UC'    : 'Ultra Collection',
    'WB'    : 'Warner Brothers',
    'WC'    : 'World Class',
    'WR'    : '[Code 2] White Rose Collectibles',
    'YF'    : '[Code 2] York Fair',
    'YST'   : 'Yesteryear Train Set',
}
code2_categories = ['ASAP', 'C2', 'CCI', 'CQ', 'NC', 'WR', 'YF']


casting_types = {
    'AC': 'Casting',           # Accessory
    'ET': 'Casting',           # Early toy
    'KS': 'Casting',           # King size
    'RW': 'Casting',           # Regular wheel
    'SB': 'Casting',           # Sky Buster
    'SF': 'Casting',           # Superfast
    'YY': 'Casting',           # YesterYear
    'PS': 'Assembly',          # Playset
    'CC': 'Case',              # Carrying Case
    'PK': 'Publication',       # Packaging
    'PC': 'Publication',       # Pocket Catalog
    'DC': 'Publication',       # Dealer Catalog
    'RY': 'Publication',       # Roadway
    'PZ': 'Publication',       # Puzzle
    'BK': 'Publication',       # Book
    'AD': 'Advertisement',     # Ad
    'MP': 'Package',           # Multipack
    'SE': 'Package',           # Series
    'LI': 'Package',           # Lineup
}


countries_dict = None
countries = [
    ('AF', "Afghanistan"),
    ('AL', "Albania"),
    ('DZ', "Algeria"),
    ('AD', "Andorra"),
    ('AO', "Angola"),
    ('AG', "Antigua and Barbuda"),
    ('AR', "Argentina"),
    ('AM', "Armenia"),
    ('AU', "Australia"),
    ('AT', "Austria"),
    ('AZ', "Azerbaijan"),
    ('BS', "Bahamas"),
    ('BH', "Bahrain"),
    ('BD', "Bangladesh"),
    ('BB', "Barbados"),
    ('BY', "Belarus"),
    ('BE', "Belgium"),
    ('BZ', "Belize"),
    ('BJ', "Benin"),
    ('BT', "Bhutan"),
    ('BO', "Bolivia"),
    ('BA', "Bosnia and Herzegovina"),
    ('BW', "Botswana"),
    ('BR', "Brazil"),
    ('BN', "Brunei Darussalam"),
    ('BG', "Bulgaria"),
    ('BF', "Burkina Faso"),
    ('BI', "Burundi"),
    ('KH', "Cambodia"),
    ('CM', "Cameroon"),
    ('CA', "Canada"),
    ('CV', "Cape Verde"),
    ('CF', "Central African Republic"),
    ('TD', "Chad"),
    ('CL', "Chile"),
    ('CN', "China"),
    ('CO', "Colombia"),
    ('KM', "Comoros"),
    ('CD', "Congo Democratic Republic"),
    ('CG', "Congo"),
    ('CR', "Costa Rica"),
    ('CI', "Cote D'Ivoire"),
    ('HR', "Croatia (Hrvatska)"),
    ('CU', "Cuba"),
    ('CY', "Cyprus"),
    ('CZ', "Czech Republic"),
    ('DK', "Denmark"),
    ('DJ', "Djibouti"),
    ('DO', "Dominican Republic"),
    ('DM', "Dominica"),
    ('DD', "East Germany"),
    ('EC', "Ecuador"),
    ('EG', "Egypt"),
    ('SV', "El Salvador"),
    ('GQ', "Equatorial Guinea"),
    ('ER', "Eritrea"),
    ('EE', "Estonia"),
    ('ET', "Ethiopia"),
    ('EU', "Europe"),
    ('FJ', "Fiji"),
    ('FI', "Finland"),
    ('FR', "France"),
    ('GA', "Gabon"),
    ('GM', "Gambia"),
    ('GE', "Georgia"),
    ('DE', "Germany"),
    ('GH', "Ghana"),
    ('GR', "Greece"),
    ('GD', "Grenada"),
    ('GT', "Guatemala"),
    ('GW', "Guinea-bissau"),
    ('GN', "Guinea"),
    ('GY', "Guyana"),
    ('HT', "Haiti"),
    ('HN', "Honduras"),
    ('HK', "Hong Kong"),
    ('HU', "Hungary"),
    ('IS', "Iceland"),
    ('IN', "India"),
    ('ID', "Indonesia"),
    ('IR', "Iran"),
    ('IQ', "Iraq"),
    ('IE', "Ireland"),
    ('IL', "Israel"),
    ('IT', "Italy"),
    ('JM', "Jamaica"),
    ('JP', "Japan"),
    ('JO', "Jordan"),
    ('KZ', "Kazakhstan"),
    ('KE', "Kenya"),
    ('KI', "Kiribati"),
    ('KP', "North Korea"),
    ('KR', "South Korea"),
    ('KW', "Kuwait"),
    ('KG', "Kyrgyzstan"),
    ('LA', "Lao"),
    ('LV', "Latvia"),
    ('LB', "Lebanon"),
    ('LS', "Lesotho"),
    ('LR', "Liberia"),
    ('LY', "Libyan Arab Jamahiriya"),
    ('LI', "Liechtenstein"),
    ('LT', "Lithuania"),
    ('LU', "Luxembourg"),
    ('MK', "Macedonia"),
    ('MG', "Madagascar"),
    ('MW', "Malawi"),
    ('MY', "Malaysia"),
    ('MV', "Maldives"),
    ('ML', "Mali"),
    ('MT', "Malta"),
    ('MH', "Marshall Islands"),
    ('MR', "Mauritania"),
    ('MU', "Mauritius"),
    ('MX', "Mexico"),
    ('FM', "Micronesia"),
    ('MD', "Moldova"),
    ('MC', "Monaco"),
    ('MN', "Mongolia"),
    ('MA', "Morocco"),
    ('MZ', "Mozambique"),
    ('MM', "Myanmar"),
    ('NA', "Namibia"),
    ('NR', "Nauru"),
    ('NP', "Nepal"),
    ('NL', "Netherlands"),
    ('NZ', "New Zealand"),
    ('NI', "Nicaragua"),
    ('NG', "Nigeria"),
    ('NE', "Niger"),
    ('NO', "Norway"),
    ('OM', "Oman"),
    ('PK', "Pakistan"),
    ('PW', "Palau"),
    ('PS', "Palestinian Authority"),
    ('PA', "Panama"),
    ('PG', "Papua New Guinea"),
    ('PY', "Paraguay"),
    ('PE', "Peru"),
    ('PH', "Philippines"),
    ('PL', "Poland"),
    ('PT', "Portugal"),
    ('QA', "Qatar"),
    ('RO', "Romania"),
    ('RU', "Russia"),
    ('RW', "Rwanda"),
    ('KN', "Saint Kitts and Nevis"),
    ('LC', "Saint Lucia"),
    ('VC', "Saint Vincent and the Grenadines"),
    ('WS', "Samoa"),
    ('SM', "San Marino"),
    ('ST', "Sao Tome and Principe"),
    ('SA', "Saudi Arabia"),
    ('SN', "Senegal"),
    ('CS', "Serbia and Montenegro"),
    ('SC', "Seychelles"),
    ('SL', "Sierra Leone"),
    ('SG', "Singapore"),
    ('SK', "Slovakia"),
    ('SI', "Slovenia"),
    ('SB', "Solomon Islands"),
    ('SO', "Somalia"),
    ('ZA', "South Africa"),
    ('ES', "Spain"),
    ('LK', "Sri Lanka"),
    ('SD', "Sudan"),
    ('SR', "Suriname"),
    ('SZ', "Swaziland"),
    ('SE', "Sweden"),
    ('CH', "Switzerland"),
    ('SY', "Syria"),
    ('TW', "Taiwan"),
    ('TJ', "Tajikistan"),
    ('TZ', "Tanzania"),
    ('TH', "Thailand"),
    ('TL', "Timor-Leste"),
    ('TG', "Togo"),
    ('TO', "Tonga"),
    ('TT', "Trinidad and Tobago"),
    ('TN', "Tunisia"),
    ('TR', "Turkey"),
    ('TM', "Turkmenistan"),
    ('TV', "Tuvalu"),
    ('UG', "Uganda"),
    ('UA', "Ukraine"),
    ('AE', "United Arab Emirates"),
    ('GB', "United Kingdom"),
    ('US', "United States"),
    ('UY', "Uruguay"),
    ('UZ', "Uzbekistan"),
    ('VU', "Vanuatu"),
    ('VA', "Vatican (Holy See)"),
    ('VE', "Venezuela"),
    ('VN', "Viet Nam"),
    ('EH', "Western Sahara"),
    ('YE', "Yemen"),
    ('ZM', "Zambia"),
    ('ZW', "Zimbabwe"),
]

image_size_names = ["t", "s", "c", "m", "l", "h", "g"]
image_size_sizes = [(100,  60), (200, 120), (300, 180), (400, 240), (600, 360), (800, 480), (1200, 720)]

imagesizes = dict(zip(image_size_names, image_size_sizes))

model_type_chars = "aob2e1r4uztv59cidjgfmpl8hx"
model_types = {
        "a": "aircraft",
        "o": "boat",
        "b": "bus",
        "2": "coupe",
        "e": "equipment",
        "1": "motorcycle",
        "r": "railroad",
        "4": "sedan",
        "u": "sport/utility",
        "z": "trailer",
        "t": "truck",
        "v": "van",
        "5": "wagon",

        "9": "ambulance",
        "c": "commercial",
        "i": "construction",
        "d": "convertible",
        "j": "fantasy",
        "g": "farm",
        "f": "fire",
        "m": "military",
        "p": "pick-up",
        "l": "police",
        "8": "racer",
        "h": "recreation",
        "x": "taxi",
}

model_icons = {
        "a": "i_air",
        "B": "i_boat",
        "b": "i_bus",
        "c": "i_coupe",
        "e": "i_equip",
        "m": "i_motor",
        "r": "i_rail",
        "s": "i_sedan",
        "u": "i_suv",
        "T": "i_trail",
        "t": "i_truck",
        "v": "i_van",
        "w": "i_wagon",

        "A": "i_amb",
        "C": "i_comm",
        "N": "i_const",
        "V": "i_conv",
        "f": "i_fant",
        "G": "i_farm",
        "F": "i_fire",
        "M": "i_mil",
        "p": "i_pickup",
        "P": "i_police",
        "R": "i_racer",
        "n": "i_rec",
        "x": "i_taxi",
}


comment_designation = {
        'm': '<img src="/pic/gfx/stargreen.gif"> - casting information not available',
        'i': '<img src="/pic/gfx/star.gif"> - actual picture not available',
        'v': '<img src="/pic/gfx/starred.gif"> - variation information not available',
        'c': '<img src="/pic/gfx/camera.gif"> - product example picture available',
        'n': '<img src="/pic/gfx/no.gif"> - never released',
}


packsize = {'2': '2', '3': '3', '4': '4', '5': '5', '8': '8', 't': '10', 'w': '20'}


id_re = re.compile('(?P<p>\D*)(?P<n>\d*)(?P<l>\D*)')
def get_mack_number(cid):
    id_m = id_re.match(cid)
    if id_m:
        if id_m.group('p') == 'SF':
	    return ('MB', int(id_m.group('n')), id_m.group('l'))
	return ('', int(id_m.group('n')), id_m.group('l'))
    return None


def get_region_tree(region):
    line_regions = list()
    lreg = region.upper()
    while lreg:
        line_regions.append(lreg)
        lreg = regionparents.get(lreg, '')
    return line_regions


def get_countries():
    global countries, countries_dict
    if not countries_dict:
        countries_dict = dict(countries)
    return countries_dict


def get_country(cc2):
    return get_countries().get(cc2, '')


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
