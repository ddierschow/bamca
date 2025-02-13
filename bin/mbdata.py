import re

import config

modsperpage = 100  # a laudable goal

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


model_type_names = {
    'AC': 'Accessory',
    'ET': 'Early Toy',
    'KS': 'King Size',
    'RW': 'Regular Wheel',
    'SB': 'Sky Buster',
    'SF': 'Superfast',
    'BR': 'Budget Range',
    'YY': 'YesterYear',
    'CH': 'Character Car',
    'PS': 'Playset',
    'CC': 'Carrying Case',
    'PK': 'Packaging',
    'PC': 'Pocket Catalog',
    'DC': 'Dealer Catalog',
    'RY': 'Roadway',
    'PZ': 'Puzzle',
    'GM': 'Game',
    'BK': 'Book',
    'PD': 'Periodical',
    'AD': 'Advertisement',
    'MP': 'Multipack',
    'SE': 'Series',
    'LI': 'Lineup',
}

model_types = {
    'AC': 'Casting',            # Accessory
    'ET': 'Casting',            # Early toy
    'KS': 'Casting',            # King size
    'RW': 'Casting',            # Regular wheel
    'SB': 'Casting',            # Sky Buster
    'SF': 'Casting',            # Superfast
    'BR': 'Casting',            # Budget Range
    'YY': 'Casting',            # YesterYear
    'CH': 'Casting',            # Character Cars
    'PS': 'Assembly',           # Playset
    'CC': 'Case',               # Carrying Case
    'PK': 'Publication',        # Packaging
    'PC': 'Publication',        # Pocket Catalog
    'DC': 'Publication',        # Dealer Catalog
    'RY': 'Publication',        # Roadway
    'PZ': 'Publication',        # Puzzle
    'BK': 'Publication',        # Book
    'GM': 'Publication',        # Game
    'PD': 'Publication',        # Periodical
    'AD': 'Advertisement',      # Ad
    'MP': 'Package',            # Multipack
    'SE': 'Package',            # Series
    'LI': 'Package',            # Lineup
}

page_format_type = {
    'biblio': 'biblio',
    'boxart': 'boxart',
    'calendar': 'calendar',
    'compare': 'compare',
    'lineup': 'lineup',
    'links': 'links',
    'makes': 'makes',
    'manno': 'manno',
    'matrix': 'matrix',
    'others': 'others',
    'package': 'package',
    'packs': 'packs',
    'php': 'php',
    'playset': 'playset',
    'pub': 'pub',
    'python': 'python',
    'sets': 'sets',
    'single': 'single',
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
    ('MO', "Macau"),
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

IMG_SIZ_LARGEST = IMG_SIZ_ENORMOUS = 'e'
IMG_SIZ_GIGANTIC = 'g'
IMG_SIZ_HUGE = 'h'
IMG_SIZ_LARGE = 'l'
IMG_SIZ_MEDIUM = 'm'
IMG_SIZ_PETITE = 'p'
IMG_SIZ_COMPACT = 'c'
IMG_SIZ_SMALL = 's'
IMG_SIZ_TINY = 't'
IMG_SIZ_MICRO = 'u'
IMG_SIZ_VERY_SMALL = 'v'
image_size_names = ["very small", "micro", "tiny", "small", "petite", "medium", "large", "huge", "gigantic", "enormous",
                    "tomica"]
image_size_types = ['v', 'u', 't', 's', 'p', 'm', 'l', 'h', 'g', 'e', 'z']
image_size_sizes = [(25, 15), (50, 30), (100, 60), (200, 120), (300, 180), (400, 240), (600, 360), (800, 480),
                    (1000, 600), (1200, 720), (180, 125)]

imagesizes = dict(zip(image_size_types, image_size_sizes))

image_adds_names = ["advertisement", "baseplate", "comparison", "custom", "detail", "error", "interior", "prototype",
                    "real", "box", "group"]
image_adds_types = ['f', 'b', 'z', 'a', 'd', 'e', 'i', 'p', 'r', 'x', 'g']
image_adds_list = zip(image_adds_types, image_adds_names)

model_type_chars_1 = "aonb2e1r4uztv5"
model_type_chars_2 = "9cidjgfqmpl8hx"
model_type_chars = model_type_chars_1 + model_type_chars_2
vehicle_types = {
    "a": "aircraft",
    "o": "boat",
    "n": "building",
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
    "q": "horse-drawn",
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
    "n": "i_build",
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
    "q": "i_horse",
    "m": "i_mil",
    "p": "i_pickup",
    "l": "i_police",
    "8": "i_racer",
    "h": "i_rec",
    "x": "i_taxi",
}

# not complete
model_small_icons = {  # not in use
    "a": "fa-plane",
    "o": "fa-ship",
    "b": "fa-bus",
    "2": "i_coupe",
    "e": "i_equip",
    "1": "fa-motorcycle",
    "r": "fa-train",
    "4": "fa-car",
    "u": "i_suv",
    "z": "i_trail",
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
    'd': '<i class="fas fa-star blue"></i> - specific model not determined',
    'm': '<i class="fas fa-star green"></i> - casting information not available',
    'i': '<i class="fas fa-star"></i> - actual picture not available',
    'v': '<i class="fas fa-star red"></i> - variation information not available',
    'c': '<i class="fas fa-camera-retro"></i> - product example picture available',
    'n': '<i class="fas fa-ban red"></i> - never released',
}

comment_icon = {
    'd': '<i class="fas fa-star blue"></i>',
    'm': '<i class="fas fa-star green"></i>',
    'i': '<i class="fas fa-star"></i>',
    'v': '<i class="fas fa-star red"></i>',
    'r': '<i class="fas fa-star yellow"></i>',
    'c': '<i class="fas fa-camera-retro"></i>',
    'n': '<i class="fas fa-ban red"></i>',
}


desc_attributes = ['description', 'base', 'body', 'interior', 'wheels', 'windows', 'with', 'text']


packsize = {'2': '2', '3': '3', '4': '4', '5': '5', '8': '8', 't': '10', 'w': '20'}


materials = {
    'B': 'blisterpack',
    'C': 'cardboard',
    'S': 'square plastic tube',
    'T': 'plastic tube',
    'W': 'window box',
    'X': 'box',
    'L': 'lucite box',
    'P': 'plastic',
    'U': 'unknown',
    '': 'unknown',
}


casting_arts = {
    'Rolamatics': 'c_rola-matics',
    'Choppers': 'c_choppers',
    'Real Talkin': 'c_realtalkin',
    'D.A.R.E.': 'c_dare',
    'Caterpillar': 'c_caterpillar',
    'Auto Steer': 'c_autosteer',
    'Collectibles': 'c_collectibles',
    'Jurassic Park': 'c_jurassic_park',
    'Jurassic World': 'c_jurassic_world',
    'Originals': 'c_originals',
    'Premieres': 'c_premiere',
    'Color Changers': 'c_colorchangers',
    'Convoy': 'c_convoy',
    'Moving Parts': 'c_movingparts',
    'Speed Kings': 'c_speed-kings',
    'Mattel Creations': 'c_mattelcreations',
    'SuperGT': 'c_supergt',
    'Super Kings': 'c_super-kings',
    'Skybusters': 'c_skybusters',
}


model_adds = [
    # prefix, title, separator, columns
    ["b_", "Sample Base%(s)s", "<p>", 1],
    ["d_", "Detail%(s)s", " ", 1],
    ["i_", "Interior%(s)s", "<p>", 1],
    ["p_", "Prototype%(s)s or Preproduction Model%(s)s", "<p>", 1],
    ["r_", "Real Vehicle Example%(s)s", "<p>", 1],
    ["a_", "Customization%(s)s", "<p>", 1],
    ["f_", "Advertisement%(s)s", "<p>", 1],
    ["e_", "Error Model%(s)s", "<p>", 1],
]

var_adds = [
    ["b_", "Base%(s)s", "<p>", 1],
    ["d_", "Detail%(s)s", " ", 1],
    ["i_", "Interior%(s)s", "<p>", 1],
]

var_types = {
    'c': 'Core',
    '1': 'C1',
    '2': 'C2',
    'f': 'F',
    'p': '2P',
}

LISTTYPE_NORMAL = ''
LISTTYPE_LARGE = 'lrg'
LISTTYPE_CHECKLIST = 'ckl'
LISTTYPE_THUMBNAIL = 'thm'
LISTTYPE_TEXT = 'txt'
LISTTYPE_CSV = 'csv'
LISTTYPE_VAR_CSV = 'vcs'
LISTTYPE_JSON = 'jsn'
LISTTYPE_ADMIN = 'adl'
LISTTYPE_PICTURE = 'pxl'
LISTTYPE_LINK = 'lnl'
LISTTYPE_VEHICLE_TYPE = 'vtl'
LISTTYPE_MULTIYEAR = 'myr'
LISTTYPE_TILLEY = 'til'
LISTTYPE_EDITOR = 'edt'
LISTTYPE_DETAIL = 'vdt'
LISTTYPE_DESCR = 'vds'

mime_types = {
    LISTTYPE_CSV: 'text/csv',
    LISTTYPE_VAR_CSV: 'text/csv',
    LISTTYPE_JSON: 'application/json',
    LISTTYPE_TEXT: 'text/plain',
}


ATTRIBUTE_BASE = 1
ATTRIBUTE_BODY = 2
ATTRIBUTE_INTERIOR = 3
ATTRIBUTE_WINDOWS = 4

areas = {
    'ROW': 'Rest of World',
    'LA': "Latin America",
}

plants = (
    ('Brazil', 'BR'),
    ('Bulgaria', 'BG'),
    ('China', 'CN'),
    ('England', 'GB'),
    ('Hong Kong', 'HK'),
    ('Hungary', 'HU'),
    ('Japan', 'JP'),
    ('Macau', 'MO'),
    ('Thailand', 'TH'),
    ('no origin', 'none'),
    ('unset', ''),
)
plant_d = dict(plants)
plant_rd = {v: k for k, v in plants}
other_plants = ['Brazil', 'Bulgaria', 'Hungary', 'Japan']

code2_cats = set(['ASAP', 'C2', 'CCI', 'CQ', 'NC', 'WR', 'YF'])

img_dir_name = {
    config.IMG_DIR_ACC: 'Accessories',
    config.IMG_DIR_ADD: 'Additional model pictures',
    config.IMG_DIR_ADS: 'Advertising',
    config.IMG_DIR_ART: 'Art',
    config.IMG_DIR_BLISTER: 'Blister packs',
    config.IMG_DIR_BOOK: 'Books (reference)',
    config.IMG_DIR_PROD_BOOK: 'Books (toys)',
    config.IMG_DIR_BOX: 'Boxes',
    config.IMG_DIR_CAT: 'Catalogs',
    config.IMG_DIR_COLL_43: '1:43 Collectibles',
    config.IMG_DIR_CONVOY: 'Convoys',
    config.IMG_DIR_ERRORS: 'Errors',
    config.IMG_DIR_MAN_ICON: 'Icons',
    config.IMG_DIR_KING: 'King Size',
    config.IMG_DIR_LESNEY: 'Lesney',
    config.IMG_DIR_MAKE: 'Makes',
    config.IMG_DIR_MAN: 'Model Pictures',
    config.IMG_DIR_PICS: 'Miscellaneous',
    config.IMG_DIR_PROD_CODE_2: 'Code 2 Models',
    config.IMG_DIR_PROD_COLL_64: '1:64 Collectibles',
    config.IMG_DIR_PROD_EL_SEG: 'Mattel El Segundo',
    config.IMG_DIR_PROD_LRW: 'Lesney RW',
    config.IMG_DIR_PROD_LSF: 'Lesney SF',
    config.IMG_DIR_PROD_MT_LAUREL: 'Mattel Mt. Laurel',
    config.IMG_DIR_PROD_MWORLD: 'Mattel Matchbox World',
    config.IMG_DIR_PROD_ODDS: 'Odd Castings',
    config.IMG_DIR_PROD_PACK: 'Multi Packs',
    config.IMG_DIR_PROD_PLAYSET: 'Playsets',
    config.IMG_DIR_PROD_PROMOS: 'Promos',
    config.IMG_DIR_SET_PACK: 'Multi Packs (contents)',
    config.IMG_DIR_SET_PLAYSET: 'Playsets (contents)',
    config.IMG_DIR_PROD_SERIES: 'Series',
    config.IMG_DIR_PROD_TYCO: 'Tyco',
    config.IMG_DIR_PROD_UNIV: 'Universal',
    config.IMG_DIR_SKY: 'Skybusters',
    config.IMG_DIR_VAR: 'Variations',
    config.IMG_DIR_GAME: 'Games',
    config.IMG_DIR_ICON: 'Icons',
    config.IMG_DIR_PACKAGE: 'Packaging',
}

# not included: man/ mbusa/ mbxf/ old/ pics/ prod/ set/ submitted/ tilley/ tomica/ trash/
img_sel_cat = [
    ('unsorted', 'unsorted'),
    ('acc', 'Accessories'),
    ('ads', 'Advertising'),
    ('bigmx', 'BigMX'),
    ('blister', 'Blister'),
    ('box', 'Box'),
    ('cat', 'Catalogs'),
    ('cc', 'Carrying Case'),
    ('coll', 'Collectibles'),
    ('commando', 'Commando'),
    ('copies', 'Copies'),
    ('convoy', 'Convoys'),
    ('custom', 'Customs'),
    ('disp', 'Displays'),
    ('docs', 'Documents'),
    ('early', 'Early'),
    ('game', 'Games'),
    ('gfx', 'Grafix'),
    ('gs', 'Giftsets'),
    ('gw', 'Giftware'),
    ('ks', 'Kings'),
    ('mattel', 'Mattel'),
    ('moko', 'Moko'),
    ('mult', 'Multiples'),
    ('mw', 'Motorways'),
    ('other', 'Other'),
    ('orig', 'Originals'),
    ('packs', 'Packs'),
    ('prem', 'Premieres'),
    ('proto', 'Prototypes'),
    ('ps', 'Play Sets'),
    ('rb', 'Roadblasters'),
    ('robotech', 'RoboTech'),
    ('rt', 'Real Talkin'),
    ('ry', 'Roadway'),
    ('sb', 'Sky Busters'),
    ('supergt', 'SuperGT'),
    ('tp', 'TwinPacks'),
    ('tyco', 'Tyco'),
    ('wd', 'Walt Disney'),
    ('wr', 'White Rose'),
    ('zing', 'Zings'),
]


base_logo = [
    ('', '(unknown)'),
    ('0', '(no logo)'),
    ('a', 'straight "MATCHBOX"'),
    ('b', 'straight "MATCHBOX" SERIES'),
    ('c', 'straight MATCHBOX (R)'),
    ('d', 'italic "MATCHBOX"'),
    ('e', 'italic MATCHBOX TM'),
    ('f', 'italic MATCHBOX (R)'),
    ('g', 'elliptical MATCHBOX'),
    ('h', 'rectangular "MATCHBOX"'),
    ('i', 'rectangular "MATCHBOX" small (R)'),
    ('j', 'rectangular MATCHBOX small TM'),
    ('k', 'rectangular MATCHBOX large TM'),
    ('l', 'rectangular MATCHBOX (R) outside'),
    ('m', 'rectangular MATCHBOX (R) inside'),
]
base_logo_dict = dict(base_logo)

base_logo_2 = [
    ('', ''),
    ('1', 'straight SUPERFAST'),
    ('2', 'italic SUPERFAST'),
    ('3', 'Superfast with wheel'),
    ('4', 'straight MAJOR PACK'),
    ('5', 'straight KING SIZE'),
    ('6', 'script Super Kings'),
    ('7', 'script Speed Kings'),
    ('8', 'straight MODELS OF YESTERYEAR'),
    ('9', 'italic MODELS OF YESTERYEAR'),
    ('y', 'italic DINKY'),
    ('z', 'elephant'),
]
base_logo_2_dict = dict(base_logo_2)

dirs = {
    'pbads': config.IMG_DIR_ADS[1:],
    'pbblis': config.IMG_DIR_BLISTER[1:],
    'pbbook': config.IMG_DIR_BOOK[1:],
    'pbbox': config.IMG_DIR_BOX[1:],
    'pbcat': config.IMG_DIR_CAT[1:],
    'pbgame': config.IMG_DIR_GAME[1:],
    'pbpkg': config.IMG_DIR_PACKAGE[1:],
    'pgfx': config.IMG_DIR_ART[1:],
    'picon': config.IMG_DIR_ICON[1:],
    'pmadd': config.IMG_DIR_ADD[1:],
    'pmake': config.IMG_DIR_MAKE[1:],
    'pman': config.IMG_DIR_MAN[1:],
    'pmicon': config.IMG_DIR_MAN_ICON[1:],
    'pmvar': config.IMG_DIR_VAR[1:],
    'ppbook': config.IMG_DIR_PROD_BOOK[1:],
    'ppcode2': config.IMG_DIR_PROD_CODE_2[1:],
    'ppelseg': config.IMG_DIR_PROD_EL_SEG[1:],
    'ppics': config.IMG_DIR_PICS[1:],
    'pplrw': config.IMG_DIR_PROD_LRW[1:],
    'pplsf': config.IMG_DIR_PROD_LSF[1:],
    'ppmtl': config.IMG_DIR_PROD_MT_LAUREL[1:],
    'ppmworld': config.IMG_DIR_PROD_MWORLD[1:],
    'ppodds': config.IMG_DIR_PROD_ODDS[1:],
    'pppack': config.IMG_DIR_PROD_PACK[1:],
    'ppplay': config.IMG_DIR_PROD_PLAYSET[1:],
    'pppromo': config.IMG_DIR_PROD_PROMOS[1:],
    'ppprem': config.IMG_DIR_PROD_COLL_64[1:],
    'ppseries': config.IMG_DIR_PROD_SERIES[1:],
    'pptyco': config.IMG_DIR_PROD_TYCO[1:],
    'ppuniv': config.IMG_DIR_PROD_UNIV[1:],
    'psacc': config.IMG_DIR_ACC[1:],
    'psconvoy': config.IMG_DIR_CONVOY[1:],
    'pserror': config.IMG_DIR_ERRORS[1:],
    'psking': config.IMG_DIR_KING[1:],
    'psles': config.IMG_DIR_LESNEY[1:],
    'psmcoll': config.IMG_DIR_COLL_43[1:],
    'pspack': config.IMG_DIR_SET_PACK[1:],
    'psplay': config.IMG_DIR_SET_PLAYSET[1:],
    'pssky': config.IMG_DIR_SKY[1:],
}
dirs_r = {v: k for k, v in dirs.items()}

deco_types = (
    ('', ''),
    ('d', 'decal'),
    ('ds', 'decals'),
    ('l', 'label'),
    ('ls', 'labels'),
    ('t', 'tampo'),
    ('n', 'no'),
    ('c', 'cast'),
    ('h', 'handpainted'),
    ('m', 'molded plastic'),
    ('f', 'fusion printed'),
    ('i', 'inkjet printed'),
)
deco_types_dict = dict(deco_types)
components = {
    'wheels': {'h': 'hub', 'r': 'rim', 's': 'spoke', 't': 'tire', '_': ''},
    'deco': {'b': 'body', 'c': 'cab', 'h': 'hood', 'r': 'roof', 's': 'side', 'w': 'wing', '_': ','},
}

# -------- regular expressions -----------------------------------------

mack_id_re = re.compile(r'(?P<p>\D*)(?P<n>\d*)(?P<l>\D*)')
starting_digits_re = re.compile(r'\d*')
paren_re = re.compile(r'\s*\(.*?\)\s*')
num_paren_re = re.compile(r'\((?P<n>\d*)\)')
angle_re = re.compile(r'''<.*?>''', re.M | re.S)
multi_spaces_re = re.compile(r'\s\s*')
commit_date_re = re.compile(r'Date:\s*(?P<d>... ... \d+ \d+:\d+:\d+ \d+)')
commit_re = re.compile(r'\ncommit ', re.M)
illegal_form_re = re.compile('[^-A-Za-z0-9_ ]+')
sql_fieldwidth_re = re.compile(r'\w+\((?P<w>\d+)\)')

# ----------------------------------------------------------------------


def get_mime_type(listtype):
    return mime_types.get(listtype, 'text/html')


def correct_year(year):
    if isinstance(year, str):
        year = int(''.join([x for x in year[:4] if x.isdigit()]))
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
    elif region not in ['R', 'U']:
        region = ''
    return region


def get_mack_number(cid):
    id_m = mack_id_re.match(cid)
    if id_m:
        if id_m.group('p') == 'SF':
            return ('MB', int(id_m.group('n')), id_m.group('l'))
        if id_m.group('p') == 'RW':
            return ('', int(id_m.group('n')), id_m.group('l'))
    return (None, None, None)


def get_region_tree(region):
    if region.startswith('X'):
        return [region]
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
        country_code_dict = dict([(y, x) for x, y in countries])
    country_code_dict.update({x: y for x, y in areas.items()})
    return country_code_dict


def get_country(cc2):
    return get_countries().get(cc2, '')


def normalize_var_id(mod, var_id):
    if var_id[0].isdigit():
        while var_id and var_id[0] == '0':
            var_id = var_id[1:]
        digs = starting_digits_re.match(var_id).end()
        var_id = '0' * (mod.get('casting.variation_digits', mod.get('variation_digits', 2)) - digs) + var_id
    return var_id


def bamcamark(year=9999):
    if year <= 1969:
        return 'bamca-1.gif'
    if year <= 1974:
        return 'bamca-2.gif'
    if year <= 2000:
        return 'bamca-3.gif'
    if year <= 2005:
        return 'bamca-4.gif'
    return 'bamca-5.gif'


def find_vs_variations(ents, sec_id, ran_id):
    # given a list of ents with "vs.sec_id" and "vs.ran_id", give back the relevant ones
    if sec_id and ran_id:
        mods = [x for x in ents if x['vs.sec_id'] == sec_id and x['vs.ran_id'] == ran_id]
        if mods:
            return mods
    if sec_id:
        mods = [x for x in ents if x['vs.sec_id'] == sec_id]
        if mods:
            return mods
    mods = [x for x in ents if x['vs.sec_id'] == '']
    return mods


def type_check(prop_n, prop_y, avail):
    def type_match(t1, t2):
        return not (set(t1 or '') - set(t2 or ''))

    if prop_n or prop_y:
        if prop_n and any([type_match(x, avail) for x in prop_n]):
            return False
        if prop_y and not type_match(prop_y, avail):
            return False
    return True


def text_types(typespec):
    return ', '.join([vehicle_types.get(t) for t in typespec or [] if t])
