import re
import useful

verno = ' abcdefghijklmnopqrstuvwxyz'

regionlist = ['W', 'U', 'R', 'A', 'B', 'D', 'L', 'J']

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
    'J': 'R',
    'L': 'W',
}

model_texts = ['Description', 'Base', 'Body', 'Interior', 'Wheels', 'Windows']

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
HP - True Heroes
MSN
SW - kingsize only
KP - kingsize only
MX - kingsize only
SC - skybusters only
CLR - yy only
'''

categories = {
    '10P'   : "10-Pack",
    '2K'    : "2000 Logo",
    '3P'    : "3-Pack",
    '50P'   : "50th Anniversary Collection",
    '5P'    : "5-Pack",
    '60'    : "60th Anniversary",
    '75C'   : "75 Challenge",
    'A'     : "Accessories",
    'AA'    : "Across America",
    'AFL'   : "Australian Football League",
    'AP'    : "Action Pack",
    'ARL'   : "Australian Rugby League",
    'ASAP'  : "[Code 2] ASAP Promotional",
    'ASP'   : "Action System Pack",
    'AVN'   : "Avon",
    'AW'    : "Around the World",
    'BH'    : "Matchbox 50th Birthday",
    'BJ'    : "Barrett-Jackson",
    'BK'    : "Battle Kings",
    'BLK'   : "Blank for Code 2 Use",
    'BO'    : "Best of ...",
    'BOB'   : "Best of British",
    'BOI'   : "Best of International",
    'BOM'   : "Best of Muscle",
    'BON'   : "Bonus",
    'BS'    : "Brroomstick",
    'C2'    : "[Code 2]",
    'CA'    : "Cartoon Characters",
    'CAT'   : "Caterpillar",
    'CC'    : "Collectors Choice",
    'CCH'   : "Color Changers",
    'CCI'   : "[Code 2] Color Comp Promotional",
    'CCY'   : "Collectible Convoy",
    'CDR'   : "CD Rom",
    'CF'    : "Commando",
    'CK'    : "Coca-Cola",
    'CKP'   : "Coca-Cola Premiere",
    'CL'    : "Club Models",
    'CNS'   : "Connoisseur Set",
    'COL'   : "Matchbox Collectibles",
    'CQ'    : "[Code 2] Conquer",
    'CR'    : "Code Red",
    'CRO'   : "Crocodile Hunter",
    'CS'    : "Construction",
    'CY'    : "Convoy",
    'DARE'  : "D.A.R.E.",
    'DM'    : "Dream Machines",
    'DT'    : "Days of Thunder",
    'DVD'   : "DVD",
    'DY'    : "Dinky",
    'EE'    : "European Edition",
    'ELC'   : "Early Learning Center",
    'ELV'   : "Elvis Presley Collection",
    'EM'    : "Emergency",
    'F1'    : "Formula 1",
    'FAS'   : "Michael Fischer-Art",
    'FC'    : "Feature Cars",
    'FE'    : "First Edition",
    'FM'    : "Farming",
    'FP'    : "Ford Anniversary",
    'G'     : "Gift Set", # G == GS
    'GC'    : "Gold Collection",
    'GF'    : "Graffic Traffic",
    'GS'    : "Gift Set",
    'GT'    : 'Budget Range / SuperGT',
    'GW'    : "Giftware",
    'HC'    : "Hero City Logo",
    'HD'    : "Harley Davidson",
    'HNH'   : "Hitch 'n' Haul",
    'HP'    : 'True Heroes',
    'HR'    : "Heroes",
    'HS'    : "Hot Stocks",
    'HT'    : "Hunt",
    'IC'    : "Intercom City",
    'IG'    : "Inaugural Collection",
    'IN'    : "Indy",
    'JB'    : "James Bond",
    'JEE'   : "Jeep",
    'JL'    : "Justice League",
    'JR'    : "Jurassic Park",
    'JW'    : "Jurassic World",
    'K'     : "Super Kings (King Size)",
    'LE'    : "Limited Edition Set",
    'LES'   : "Lesney Edition",
    'LL'    : "My First Matchbox (Live & Learn)",
    'LP'    : "Launcher Pack",
    'LR'    : "Lightning",
    'LRV'   : "Land Rover",
    'LT'    : "Lasertronic (Siren Force, Light & Sound)",
    'LW'    : "Laser Wheels",
    'MB'    : "Matchbox 1-75 (1-100) basic range",
    'MBR'   : "Micro Brewery",
    'MC'    : "Motor City",
    'MCC'   : "My Classic Car",
    'MD'    : "Superfast Minis",
    'MLB'   : "Major League Baseball (USA)",
    'MNS'   : "Monsters",
    'MO'    : "Matchbox Originals",
    'MP'    : "Multipack",
    'MT'    : "Matchcaps",
    'MU'    : "Masters of the Universe",
    'NBA'   : "National Basketball Association (USA)",
    'NBL'   : "National Basketball League (AUS)",
    'NC'    : "[Code 2] Nutmeg Collectibles",
    'NFL'   : "National Football League (USA)",
    'NHL'   : "National Hockey League (USA)",
    'NM'    : "Nigel Mansell",
    'NP'    : "National Parks",
    'NR'    : "Neon Racers",
    'NSF'   : "New Superfast",
    'OS'    : "Osbournes",
    'P'     : "Pre-production",
    'PC'    : "Premiere Collection",
    'PG'    : "Power Grabs",
    'PR'    : "Promotional",
    'PRC'   : "Premiere Concept",
    'PS'    : "Playset",
    'PVB'   : "Pleasant Valley Books",
    'PZ'    : "Puzzle",
    'RB'    : "Road Blasters",
    'RT'    : "Real Talkin",
    'SB'    : "Skybusters",
    'SCC'   : "Super Color Changers",
    'SCD'   : "Scooby Doo",
    'SCS'   : "Showcase Collection",
    'SF'    : "Superfast",
    'SFA'   : "Superfast America",
    'SNL'   : "Saturday Night Live",
    'SOC'   : "Stars of Germany (Stars of Cars)",
    'SOG'   : "Stars of Germany (Stars of Cars)",
    'SS'    : "Showstoppers (Motor Show)",
    'ST'    : "Super Trucks",
    'STR'   : "Star Car",
    'TC'    : "Team Convoy (Team Matchbox)",
    'TF'    : "Toy Fair",
    'TH'    : "Triple Heat",
    'TN'    : "Then & Now",
    'TP'    : "Twin Pack (Action System, Adventure Pack)",
    'TV'    : "TV Tie-In",
    'TVP'   : "TV-related Premiere",
    'TX'    : "Texaco Collection",
    'UC'    : "Ultra Collection",
    'WB'    : "Warner Brothers",
    'WC'    : "World Class",
    'WR'    : "[Code 2] White Rose Collectibles",
    'YF'    : "[Code 2] York Fair",
    'YST'   : "Yesteryear Train Set",

}
code2_categories = ['ASAP', 'CCI', 'CQ', 'NC', 'WR', 'YF', 'C2']

code2_names = {
    'ASAP'  : 'ASAP Promotional',
    'CCI'   : 'Color Comp Promotional',
    'CQ'    : 'AdTrucks/Conquer',
    'NC'    : 'Nutmeg Collectibles',
    'WR'    : 'White Rose Collectibles',
    'YF'    : 'York Fair',
    'C2'    : 'Miscellaneous Code 2',
}

cat_arts = {
    'CAT'   : 'caterpillar-sm.gif',
    'COL'   : 'collectibles-sm.gif',
    'DARE'  : 'dare-sm.gif',
    'JR'    : 'jurassic_park-sm.gif',
    'MO'    : 'originals-sm.gif',
    'PC'    : 'premiere-sm.gif',
    'WC'    : 'worldclass-sm',
}


model_type_names = {
    'AC': 'Accessory',
    'ET': 'Early toy',
    'KS': 'King size',
    'RW': 'Regular wheel',
    'SB': 'Sky Buster',
    'SF': 'Superfast',
    'BR': 'Budget Range',
    'YY': 'YesterYear',
    'PS': 'Playset',
    'CC': 'Carrying Case',
    'PK': 'Packaging',
    'PC': 'Pocket Catalog',
    'DC': 'Dealer Catalog',
    'RY': 'Roadway',
    'PZ': 'Puzzle',
    'BK': 'Book',
    'AD': 'Ad',
    'MP': 'Multipack',
    'SE': 'Series',
    'LI': 'Lineup',
}

model_types = {
    'AC': 'Casting',           # Accessory
    'ET': 'Casting',           # Early toy
    'KS': 'Casting',           # King size
    'RW': 'Casting',           # Regular wheel
    'SB': 'Casting',           # Sky Buster
    'SF': 'Casting',           # Superfast
    'BR': 'Casting',           # Budget Range
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
country_code_dict = None
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

IMG_SIZ_ENORMOUS = 'e'
IMG_SIZ_GIGANTIC = 'g'
IMG_SIZ_HUGE = 'h'
IMG_SIZ_LARGE = 'l'
IMG_SIZ_MEDIUM = 'm'
IMG_SIZ_PETITE = 'p'
IMG_SIZ_COMPACT = 'c'
IMG_SIZ_SMALL = 's'
IMG_SIZ_TINY = 't'
image_size_names = ["micro", "tiny", "small", "petit", "compact", "medium", "large", "huge", "gigantic", "enormous"]
image_size_types = ['u', 't', 's', 'p', 'c', 'm', 'l', 'h', 'g', 'e']
image_size_sizes = [(50, 30), (100,  60), (200, 120), (300, 180), (300, 180), (400, 240), (600, 360), (800, 480), (1000, 600), (1200, 720)]

imagesizes = dict(zip(image_size_types, image_size_sizes))

image_adds_names = ["advertisement", "baseplate", "comparison", "custom", "detail", "error", "interior", "prototype", "real", "box", "group"]
image_adds_types = ['f', 'b', 'z', 'a', 'd', 'e', 'i', 'p', 'r', 'x', 'g']

model_type_chars = "aob2e1r4uztv59cidjgfmpl8hx"
vehicle_types = {
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
    "o": "i_boat",
    "b": "i_bus",
    "2": "i_coupe",
    "e": "i_equip",
    "1": "i_motor",
    "r": "i_rail",
    "4": "i_sedan",
    "u": "i_suv",
    "z": "i_trail",
    "t": "i_truck",
    "v": "i_van",
    "5": "i_wagon",

    "9": "i_amb",
    "c": "i_comm",
    "i": "i_const",
    "d": "i_conv",
    "j": "i_fant",
    "g": "i_farm",
    "f": "i_fire",
    "m": "i_mil",
    "p": "i_pickup",
    "l": "i_police",
    "8": "i_racer",
    "h": "i_rec",
    "x": "i_taxi",
}

# not complete
model_small_icons = {
    "a": "fa-plane",
    "o": "fa-ship",
    "b": "fa-bus",
    "2": "i_coupe",
    "e": "i_equip",
    "1": "fa-motorcycle",
    "r": "fa-train",
    "4": "fa-car",
    "u": "i_suv",
    "r": "i_trail",
    "t": "fa-truck",
    "v": "i_van",
    "5": "i_wagon",

    "9": "fa-ambulance",
    "c": "i_comm",
    "i": "i_const",
    "d": "i_conv",
    "j": "i_fant",
    "g": "i_farm",
    "f": "i_fire",
    "m": "i_mil",
    "p": "i_pickup",
    "l": "i_police",
    "8": "i_racer",
    "h": "i_rec",
    "x": "fa-taxi",
}


comment_name = {
    'd': 'nonspecific',
    'm': 'no_casting',
    'i': 'no_picture',
    'v': 'no_variation',
    'c': 'product_pic',
    'n': 'not_released',
}

comment_designation = {
    'd': '<i class="fa fa-star blue"></i> - specific model not determined',
    'm': '<i class="fa fa-star green"></i> - casting information not available',
    'i': '<i class="fa fa-star"></i> - actual picture not available',
    'v': '<i class="fa fa-star red"></i> - variation information not available',
    'c': '<i class="fa fa-camera-retro"></i> - product example picture available',
    'n': '<i class="fa fa-ban red"></i> - never released',
}

comment_icon = {
    'd': '<i class="fa fa-star blue"></i>',
    'm': '<i class="fa fa-star green"></i>',
    'i': '<i class="fa fa-star"></i>',
    'v': '<i class="fa fa-star red"></i>',
    'r': '<i class="fa fa-star yellow"></i>',
    'c': '<i class="fa fa-camera-retro"></i>',
    'n': '<i class="fa fa-ban red"></i>',
}


packsize = {'2': '2', '3': '3', '4': '4', '5': '5', '8': '8', 't': '10', 'w': '20'}


materials = {
    'B': 'blisterpack',
    'C': 'cardboard',
    'S': 'square plastic tube',
    'T': 'plastic tube',
    'W': 'window box',
    'X': 'box',
    'L': 'lucite box',
    '': 'unknown',
}


arts = {
    'Rolamatics': 'rola-matics-sm.gif',
    'Choppers': 'choppers-sm.gif',
    'Real Talkin': 'realtalkin-sm.gif',
    'D.A.R.E.': 'dare-sm.gif',
    'Caterpillar': 'caterpillar-sm.gif',
    'Auto Steer': 'autosteer-sm.gif',
    'Collectibles': 'collectibles-sm.gif',
    'Jurassic Park': 'jurassic_park-sm.gif',
    'Originals': 'originals-sm.gif',
    'Premieres': 'premiere-sm.gif',
    'Color Changers': 'colorchangers-sm.gif',
}


LISTTYPE_NORMAL = ''
LISTTYPE_LARGE = 'lrg'
LISTTYPE_CHECKLIST = 'ckl'
LISTTYPE_THUMBNAIL = 'thm'
LISTTYPE_TEXT = 'txt'
LISTTYPE_CSV = 'csv'
LISTTYPE_JSON = 'jsn'
LISTTYPE_ADMIN = 'adl'
LISTTYPE_PICTURE = 'pxl'
LISTTYPE_LINK = 'lnl'
LISTTYPE_VEHICLE_TYPE = 'vtl'
LISTTYPE_MULTIYEAR = 'myr'

mime_types = {
    LISTTYPE_CSV: 'text/csv',
    LISTTYPE_JSON: 'application/json',
    LISTTYPE_TEXT: 'text/plain',
}


ATTRIBUTE_BASE     = 1
ATTRIBUTE_BODY     = 2
ATTRIBUTE_INTERIOR = 3
ATTRIBUTE_WINDOWS  = 4

areas = {
    'ROW': 'Rest of World',
    'LA': "Latin America",
}

# ----------------------------------------------------------------------

def get_mime_type(listtype):
    return mime_types.get(listtype, 'text/html')


def correct_year(year):
    if isinstance(year, str):
        year = int(''.join(filter(lambda x: x.isdigit(), year[:4])))
    return year


def correct_region(region, year):
    if year < 1971:
        region = 'W'
    elif region == 'D':
        if year not in (1999, 2000, 2001):
            region = 'R'
    elif region == 'B':
        if year not in (2000, 2001):
            region = 'R'
    elif region == 'A':
        if year >= 2002:  # is this correct?
            region = 'U'
        elif year not in (1981, 1987, 1991, 1992, 1993, 1997, 2000, 2001):
            region = 'R'
    elif region == 'L':
        if year < 2008 or year > 2011:
            region = 'R'
    elif region == 'J':
        if year < 1977 or year > 1992:
            region = 'R'
    elif region == 'W' or region not in ['R', 'U']:
	region = ''
    return region


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


def get_country_codes():
    global countries, country_code_dict
    if not country_code_dict:
        country_code_dict = dict([(y, x) for x,y in countries])
    country_code_dict.update({x: y for x,y in areas.items()})
    return country_code_dict


def get_country(cc2):
    return get_countries().get(cc2, '')


starting_digits_re = re.compile('\d*')
def normalize_var_id(mod, var_id):
    if var_id[0].isdigit():
	while var_id and var_id[0] == '0':
	    var_id = var_id[1:]
	digs = starting_digits_re.match(var_id).end()
	var_id = '0' * (mod.get('casting.variation_digits', mod.get('variation_digits', 2)) - digs) + var_id
    return var_id


if __name__ == '__main__':  # pragma: no cover
    pass
