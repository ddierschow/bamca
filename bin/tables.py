#!/usr/local/bin/python

# readonly hidden select checkbox
# 'add' 'ask' 'clinks' 'columns' 'create' 'elinks' 'id' 'readonly' 'titles' 'tlinks'
table_info = {
    #page_info
    'page_info': {
        'id': ['id'],
        'columns': ['id', 'flags', 'health', 'format_type', 'title', 'pic_dir', 'tail', 'description', 'note'],
        'clinks': {
                'id': {'tab': 'page_info', 'id': ['id/id']},
        },
        'tlinks': [
                #{'tab': 'style', 'id': ['page_id/id']},
                {'tab': 'section', 'id': ['page_id/id']},
        ],
        'add': {
                'page_info': [],
                #'style': ['page_id/id'],
                'section': ['page_id/id'],
        },
        'create': {
                'id': 'newpage',
        },
        'ask': ['id', 'format_type'],
    },
    #country
    'country': {
        'id': ['id'],
        'columns': ['id', 'name', 'region'],
        'clinks': {
                'id': {'tab': 'country', 'id': ['id/id']},
        },
        'add': {
                'country': ['id/id'],
        },
        'create': {
                'id': '??',
        }
    },
    #section
    'section': {
        'id': ['id', 'page_id'],
        'columns': ['id', 'page_id', 'display_order', 'category', 'flags', 'name', 'columns', 'start', 'pic_dir', 'disp_format', 'link_format', 'img_format', 'note'],
        'clinks': {
                'id': {'tab': 'section', 'id': ['id/id', 'page_id/page_id']},
                'page_id': {'tab': 'page_info', 'id': ['id/page_id']},
                'region': {'tab': 'region', 'id': ['id/region']},
        },
        'tlinks': [
                {'tab': 'matrix_model', 'id': ['section_id/id', 'page_id/page_id'], 'if': "dats and dats[0]['page_id'].startswith('matrix.')"},
                {'tab': 'lineup_model', 'id': ['year/*dat["page_id"][5:]', 'region/*dats[0]["id"][0]'], 'if': "dats and dats[0]['page_id'].startswith('year.')"},
                {'tab': 'lineup_model', 'id': ['year/*dat["page_id"][5:]', 'region/id'], 'if': "dats and dats[0]['page_id'].startswith('year.')"},
                {'tab': 'link_line', 'id': ['section_id/id', 'page_id/page_id'], 'if': "dats and dats[0]['page_id'].startswith('links.')"},
                {'tab': 'pack', 'id': ['section_id/id', 'page_id/page_id'], 'if': "dats and dats[0]['page_id'].startswith('packs.')"},
        ],
        'add': {
                'section': ['page_id/page_id'],
                'matrix_model': ['page_id/page_id', 'section_id/id'],
                'pack': ['page_id/page_id', 'section_id/id'],
                'link_line': ['page_id/page_id', 'section_id/id'],
        },
        'create': {
                'id': 'newsection',
        }
    },
    #base_id
    'base_id': {
        'id': ['id'],
        'columns': ['id', 'first_year', 'model_type', 'rawname', 'description', 'flags'],
        'clinks': {
                'id': {'tab': 'base_id', 'id': ['id/id']},
                'country': {'tab': 'country', 'id': ['id/country']},
                'section_id': {'tab': 'section', 'id': ['id/section_id']},
        },
        'tlinks': [
                {'tab': 'alias', 'id': ['ref_id/id']},
                {'tab': 'casting', 'id': ['id/id']},
                {'tab': 'pack', 'id': ['id/id']},
                {'tab': 'publication', 'id': ['id/id']},
        ],
        'add': {
                'base_id': [],
                'casting': ['id/id'],
        },
        'create': {
                'id': 'unset',
                'first_year': '',
                'flags': 0,
                'model_type': '',
                'rawname': '',
                'description': '',
        },
        'ask': ['id', 'first_year', 'model_type'],
    },
    #casting
    'casting': {
        'id': ['id'],
        'columns': ['id', 'scale', 'vehicle_type', 'country', 'make', 'section_id'],
	'extra_columns': ['notes',
	    'format_description', 'format_body', 'format_interior', 'format_windows', 'format_base', 'format_wheels'],
        'clinks': {
                'id': {'tab': 'casting', 'id': ['id/id']},
                'country': {'tab': 'country', 'id': ['id/country']},
                'section_id': {'tab': 'section', 'id': ['id/section_id']},
        },
        'tlinks': [
                {'tab': 'base_id', 'id': ['id/id']},
                {'tab': 'attribute', 'id': ['mod_id/id']},
                {'tab': 'attribute_picture', 'id': ['mod_id/id']},
                {'tab': 'variation', 'id': ['mod_id/id']},
                {'tab': 'alias', 'id': ['ref_id/id']},
                {'tab': 'casting_related', 'id': ['model_id/id']},
                {'tab': 'casting_related', 'id': ['related_id/id']},
                {'tab': 'matrix_model', 'id': ['mod_id/id']},
                {'tab': 'lineup_model', 'id': ['mod_id/id']},
                {'tab': 'pack_model', 'id': ['mod_id/id']},
                {'tab': 'variation_select', 'id': ['mod_id/id']},
        ],
        'add': {
                'casting': [],
                'attribute': ['mod_id/id'],
                'attribute_picture': ['mod_id/id'],
                'variation': ['mod_id/id'],
                'alias': ['ref_id/id'],
                'casting_related': [],
                'matrix_model': ['mod_id/id'],
                'lineup_model': ['mod_id/id'],
        },
        'create': {
                'id': 'unset',
        },
        'ask': ['id', 'make', 'section_id'],
    },
    #casting_related
    'casting_related': {
        'id': ['id'],
        'columns': ['id', 'model_id', 'related_id', 'section_id', 'picture_id', 'description'],
        'clinks': {
                'id': {'tab': 'casting_related', 'id': ['id/id']},
                'model_id': {'tab': 'base_id', 'id': ['id/model_id']},
                'related_id': {'tab': 'base_id', 'id': ['id/related_id']},
        },
        'create': {
                'model_id': 'unset',
                'related_id': 'unset',
        },
        'ask': ['model_id', 'related_id'],
    },
    #attribute
    'attribute': {
        'id': ['id'],
        'columns': ['id', 'mod_id', 'attribute_name', 'definition', 'title', 'visual'],
        'clinks': {
                'id': {'tab': 'attribute', 'id': ['id/id']},
                'mod_id': {'tab': 'casting', 'id': ['mod_id/id']},
                'attribute_picture': ['mod_id/mod_id', 'attr_id/id'],
        },
        'add': {
                'attribute': ['mod_id/mod_id'],
                'attribute_picture': ['mod_id/mod_id', 'attr_id/id'],
                'detail': ['mod_id/mod_id', 'attr_id/id'],
        },
        'tlinks': [
                {'tab': 'detail', 'id': ['attr_id/id']},
                {'tab': 'attribute_picture', 'id': ['mod_id/mod_id']},
        ],
        'create': {
                'mod_id': 'unset',
        },
    },
    #attribute_picture
    'attribute_picture': {
        'id': ['id'],
        'columns': ['id', 'mod_id', 'attr_id', 'attr_type', 'picture_id', 'description'],
        'clinks': {
                'id': {'tab': 'attribute_picture', 'id': ['id/id']},
                'mod_id': {'tab': 'casting', 'id': ['mod_id/id']},
                'attr_id': {'tab': 'attribute', 'id': ['attr_id/id']},
        },
        'add': {
                'attribute_picture': ['mod_id/mod_id'],
        },
        'tlinks': [
                {'tab': 'attribute', 'id': ['mod_id/mod_id']},
        ],
        'create': {
                'mod_id': 'unset',
                'attr_id': '0',
        },
        'elinks': [
                {'name': 'upload', 'url': 'upload.cgi?d=./pic/add&r=%(attr_type)s_%(mod_id)s-%(picture_id)s&m=%(mod_id)s'},
        ],
    },
    #variation
    'variation': {
        'id': ['mod_id', 'var'],
        'columns': ['mod_id', 'var', 'flags',
            'text_description', 'text_base', 'text_body', 'text_interior', 'text_wheels', 'text_windows',
            'base', 'body', 'interior', 'windows',
            'manufacture', 'category', 'area', 'date', 'note', 'other', 'picture_id', 'imported', 'imported_from', 'imported_var'],
        'titles': ['Model ID', 'Variation ID', 'Flags',
            'Description', 'Base', 'Body', 'Interior', 'Wheels', 'Windows',
            'Base', 'Body', 'Interior', 'Windows',
            'Manufacture', 'Category', 'Area', 'Date', 'Note', 'Other', 'Picture ID', 'Imported', 'Imported From', 'Imported Var'],
        'clinks': {
                'var': {'tab': 'variation', 'id': ['mod_id/mod_id', 'var/var']},
                'mod_id': {'tab': 'casting', 'id': ['id/mod_id']},
        },
        'tlinks': [
                {'tab': 'detail', 'id': ['mod_id/mod_id', 'var_id/var'], 'ref': {'attr_id': ['attribute', 'id', 'attribute_name']}},
        ],
        'add': {
                'variation': ['mod_id/mod_id'],
        },
        'create': {
                'var': 'unset',
        }
    },
    #detail
    'detail': {
        'id': ['mod_id', 'var_id', 'attr_id'],
        'columns': ['mod_id', 'var_id', 'attr_id', 'description'],
        'clinks': {
                'attr_id': {'tab': 'attribute', 'id': ['id/attr_id']},
        },
        'create': {
                'mod_id': 'unset',
                'var_id': 'unset',
                'attr_id': 'unset',
        }
    },
    #wheel
    'wheel': {
        'id': ['id'],
        'columns': ['id', 'description'],
        'create': {
                'id': 'unset',
        }
    },
    #alias
    'alias': {
        'id': ['id'],
        'columns': ['id', 'first_year', 'ref_id', 'section_id', 'type'],
        'clinks': {
                'id': {'tab': 'alias', 'id': ['id/id']},
                'ref_id': {'tab': 'base_id', 'id': ['id/ref_id']},
        },
        'add': {
                'alias': ['ref_id/ref_id'],
        },
        'create': {
                'id': 'unset',
        }
    },
    #vehicle_type
    'vehicle_type': {
        'id': ['id'],
        'columns': ['id', 'ch', 'name'],
        'clinks': {
                'id': {'tab': 'vehicle_type', 'id': ['id/id']},
        },
    },
    #counter
    'counter': {
        'id': ['id'],
        'columns': ['id', 'value', 'timestamp'],
        'clinks': {
                'id': {'tab': 'counter', 'id': ['id/id']},
        },
    },
    #vehicle_make
    'vehicle_make': {
        'id': ['make'],
        'columns': ['make', 'make_name'],
        'clinks': {
                'id': {'tab': 'vehicle_make', 'make': ['make/make']},
        },
        'create': {
                'make': '???',
        },
        'ask': ['make'],
    },
    #matrix_model
    'matrix_model': {
        'id': ['id'],
        'columns': ['id', 'base_id', 'page_id', 'section_id', 'display_order', 'range_id', 'mod_id', 'flags', 'shown_id', 'name', 'subname', 'description'],
        'clinks': {
                'id': {'tab': 'matrix_model', 'id': ['id/id']},
                'section_id': {'tab': 'section', 'id': ['id/section_id', 'page_id/page_id']},
                'mod_id': {'tab': 'base_id', 'id': ['id/mod_id']},
                'page_id': {'tab': 'page_info', 'id': ['id/page_id']},
        },
        'tlinks': [
                {'tab': 'variation_select', 'id': ['mod_id/mod_id']},
        ],
        'add': {
                'matrix_model': ['page_id/page_id', 'section_id/section_id'],
        },
        'ask': ['id', 'page_id', 'mod_id'],
    },
    #region
    'region': {
        'id': ['id'],
        'columns': ['id', 'parent', 'name'],
        'clinks': {
                'id': {'tab': 'region', 'id': ['id/id']},
                'parent': {'tab': 'region', 'id': ['id/parent']},
        },
        'add': {
                'region': [],
        },
        'create': {
                'id': '?',
        },
    },
    #lineup_model
    'lineup_model': {
        'id': ['id'],
        'columns': ['id', 'base_id', 'mod_id', 'number', 'flags', 'style_id', 'picture_id', 'region', 'year', 'name', 'page_id'],
        'clinks': {
                'id': {'tab': 'lineup_model', 'id': ['id/id']},
                'mod_id': {'tab': 'base_id', 'id': ['id/mod_id']},
                'year': {'tab': 'lineup_model', 'id': ['year/year']},
        },
        'tlinks': [
                {'tab': 'variation_select', 'id': ['mod_id/mod_id']},
        ],
        'add': {
                'lineup_model': [],
        },
        'ask': ['id', 'year', 'region', 'number', 'mod_id'],
    },
    #link_line
    'link_line': {
        'id': ['id'],
        'columns': ['id', 'page_id', 'section_id', 'display_order', 'flags', 'associated_link', 'last_status', 'link_type', 'country', 'url', 'name', 'description', 'note'],
        'readonly': ['last_status'],
        'clinks': {
                'id': {'tab': 'link_line', 'id': ['id/id']},
        },
        'add': {
                'link_line': ['page_id/page_id', 'section_id/section_id'],
        },
        'tlinks': [
                {'tab': 'blacklist'},
        ],
        'ask': ['id', 'page_id', 'section_id'],
    },
    #blacklist
    'blacklist': {
        'id': ['id'],
        'columns': ['id', 'reason', 'target'],
        'clinks': {
                'id': {'tab': 'blacklist', 'id': ['id/id']},
        },
        'add': {
                'blacklist': [],
        },
    },
    #user
    'user': {
        'id': ['id'],
        'columns': ['id', 'name', 'passwd', 'privs', 'email', 'state', 'vkey'],
        'clinks': {
                'id': {'tab': 'user', 'id': ['id/id']},
        },
        'readonly': ['id'],
    },
    #pack
    'pack': {
        'id': ['id'],
        'columns': ['id', 'page_id', 'section_id', 'region', 'layout', 'product_code', 'material', 'country', 'note'],
        'add': {
                'pack': [],
                'pack_model': ['pack_id/id'],
        },
        'create': {
                'id': 'newpack',
        },
        'clinks': {
                'id': {'tab': 'pack', 'id': ['id/id']},
                'page_id': {'tab': 'page_info', 'id': ['id/page_id']},
        },
        'tlinks': [
                {'tab': 'pack_model', 'id': ['pack_id/id']},
        ],
        'ask': ['id', 'page_id', 'section_id', 'region'],
    },
    #pack_model
    'pack_model': {
        'id': ['id'],
        'columns': ['id', 'pack_id', 'mod_id', 'var_id', 'flags', 'display_order'],
        'clinks': {
                'id': {'tab': 'pack_model', 'id': ['id/id']},
                'mod_id': {'tab': 'base_id', 'id': ['id/mod_id']},
        },
        'tlinks': [
                {'tab': 'variation_select', 'id': ['mod_id/mod_id']},
        ],
        'add': {
                'pack_model': ['pack_id/pack_id'],
        },
    },
    #publication
    'publication': {
        'id': ['id'],
        'columns': ['id', 'country', 'section_id'],
        'clinks': {
                'id': {'tab': 'base_id', 'id': ['id/id']},
                'country': {'tab': 'country', 'id': ['id/country']},
                'section_id': {'tab': 'section', 'id': ['id/section_id']},
        },
        'tlinks': [
                {'tab': 'lineup_model', 'id': ['mod_id/id']},
                {'tab': 'base_id', 'id': ['id/id']},
        ],
        'add': {
                'lineup_model': ['mod_id/id'],
        },
        'create': {
                'id': 'unset',
        },
        'ask': ['id', 'section_id'],
    },
    #variation_select
    'variation_select': {
        'id': ['ref_id', 'mod_id', 'var_id', 'sub_id'],
        'columns': ['ref_id', 'mod_id', 'var_id', 'sub_id'],
        'create': {
                'ref_id': 'unset',
                'mod_id': 'unset',
                'var_id': 'unset',
                'sub_id': 'unset',
        },
        'clinks': {
                'mod_id': {'tab': 'base_id', 'id': ['id/mod_id']},
                'var_id': {'tab': 'variation', 'id': ['mod_id/mod_id', 'var/var_id']},
        },
        'tlinks': {
        },
        'add': {
        },
        'ask': ['ref_id'],
    },
    #box_type
    'box_type': {
        'id': ['id'],
        'columns': ['id', 'mod_id', 'box_type', 'pic_id', 'box_size', 'additional_text', 'bottom', 'sides', 'end_flap', 'model_name', 'year', 'notes'],
        'clinks': {
                'id': {'tab': 'box_type', 'id': ['id/id']},
        },
#        'tlinks': [
#                {'tab': 'alias', 'id': ['id/mod_id']},
#                {'tab': 'casting', 'id': ['id/mod_id']},
#        ],
    },
    #box_style
    'box_style': {
        'id': ['id'],
        'columns': ['id', 'styles'],
        'create': {
                'id': 'unset',
                'styles': '',
        },
        'clinks': {
        },
        'tlinks': [
                {'tab': 'alias', 'id': ['id/id']},
                {'tab': 'casting', 'id': ['id/id']},
        ],
    },
    #site_activity
    'site_activity': {
        'id': ['id'],
        'columns': ['id', 'name', 'description', 'url', 'image', 'by_user_id', 'timestamp'],
    }

}
for key in table_info:
    table_info[key]['name'] = key

#-

FLAG_MODEL_NOT_MADE                     =  1
FLAG_MODEL_CODE_2                       =  2
FLAG_MODEL_NO_VARIATION                 =  4
FLAG_MODEL_NO_ID                        =  8
FLAG_MODEL_SHOW_ALL_VARIATIONS          = 16
FLAG_MODEL_HIDE_IMAGE                   = 32
FLAG_MODEL_NO_SPECIFIC_MODEL            = 64

FLAG_SECTION_NO_FIRSTS                  =  1
FLAG_SECTION_DEFAULT_IDS                =  2
FLAG_SECTION_HIDDEN                     = 16

FLAG_PAGE_INFO_NOT_RELEASED             =  1
FLAG_PAGE_INFO_HIDE_TITLE               =  2
FLAG_PAGE_INFO_UNROLL_MODELS            =  4

FLAG_LINK_LINE_NEW                      =  1
FLAG_LINK_LINE_RECIPROCAL               =  2
FLAG_LINK_LINE_PAYPAL                   =  4
FLAG_LINK_LINE_INDENTED                 =  8
FLAG_LINK_LINE_FORMAT_LARGE             = 16
FLAG_LINK_LINE_NOT_VERIFIABLE           = 32
FLAG_LINK_LINE_ASSOCIABLE               = 64
FLAG_LINK_LINE_HIDDEN                   = 128

#-

'''
site_activity
    id                      int(11)         NO      PRI     NULL                  auto_increment
    name                    varchar(128)    NO
    description             varchar(256)    NO
    url                     varchar(256)    NO
    by_user_id              int(11)         NO              NULL
    timestamp               timestamp       NO              CURRENT_TIMESTAMP     on update CURRENT_TIMESTAMP
alias
    id                      varchar(12)     NO      PRI
    first_year              varchar(4)      YES
    ref_id                  varchar(12)     NO      PRI
    section_id              varchar(20)     YES
    type                    varchar(16)     YES
attribute
    id                      int(11)         NO      PRI     NULL    auto_increment
    mod_id                  varchar(12)     YES     MUL     NULL
    attribute_name          varchar(32)     YES
    definition              varchar(32)     YES
    title                   varchar(32)     YES
    visual                  tinyint(1)      YES             1
attribute_picture
    id                      int(11)         NO      PRI     NULL    auto_increment
    mod_id                  varchar(8)      NO
    attr_id                 int(11)         YES
    picture_id              varchar(8)      NO
    description             varchar(128)    YES
base_id
    id                      varchar(12)     NO      PRI     NULL
    first_year              varchar(4)      NO              NULL
    flags                   int(11)         NO              0
    model_type              varchar(2)      NO              NULL
    rawname                 varchar(64)     NO              NULL
    description             varchar(128)    NO
blacklist
    id                      int(11)         NO      PRI     NULL    auto_increment
    reason                  varchar(6)      YES
    target                  varchar(32)     YES
box_style
    id                      varchar(12)     NO              NULL
    styles                  varchar(16)     NO              NULL
casting
    id                      varchar(12)     NO      PRI
    first_year              varchar(4)      YES
    flags                   int(11)         YES             0
    scale                   varchar(6)      YES
    model_type              varchar(2)      YES
    vehicle_type            varchar(3)      NO
    country                 varchar(2)      YES
    rawname                 varchar(64)     NO
    make                    varchar(3)      YES
    box_styles              varchar(8)      YES
    description             varchar(64)     YES
    section_id              varchar(20)     YES
    format_description                      varchar(128)    YES      &body
    format_body             varchar(128)    YES             *body
    format_interior         varchar(128)    YES             @interior
    format_windows          varchar(128)    YES             @windows
    format_base             varchar(128)    YES             @base|&manufacture
    format_wheels           varchar(128)    YES             &wheels
casting_related
    model_id                varchar(12)     NO      PRI
    related_id              varchar(12)     NO      PRI
counter
    id                      varchar(32)     NO      PRI
    value                   int(11)         YES             0
    timestamp               datetime        YES             NULL
country
    id                      varchar(2)      NO      PRI     NULL
    name                    varchar(32)     YES
    region                  varchar(2)      YES
detail
    mod_id                  varchar(12)     NO      PRI
    var_id                  varchar(8)      NO      PRI     NULL
    attr_id                 int(11)         NO      PRI     NULL
    description             varchar(256)    YES             NULL
lineup_model
    id                      int(11)         NO      PRI     NULL    auto_increment
    mod_id                  varchar(12)     YES             NULL
    number                  int(3)          YES             0
    style_id                varchar(3)      YES             NULL
    picture_id              varchar(12)     YES
    region                  varchar(4)      YES             NULL
    year                    varchar(6)      YES
    page_id                 varchar(32)     YES
    name                    varchar(64)     YES
link_line
    id                      int(11)         NO      PRI     NULL    auto_increment
    page_id                 varchar(20)     NO
    section_id              varchar(20)     YES
    display_order           int(3)          YES             0
    flags                   int(11)         YES             0
    associated_link         int(11)         YES             0
    last_status             varchar(5)      YES             NULL
    link_type               varchar(1)      YES
    country                 varchar(2)      YES
    url                     varchar(256)    YES
    name                    varchar(128)    YES
    description             varchar(512)    YES
    note                    varchar(256)    YES
matrix_model
    id                      int(11)         NO      PRI     NULL    auto_increment
    section_id              varchar(20)     YES
    display_order           int(3)          YES             0
    page_id                 varchar(20)     YES
    range_id                varchar(16)     YES
    mod_id                  varchar(12)     YES             NULL
    flags                   int(11)         YES             0
    shown_id                varchar(12)     YES
    name                    varchar(64)     YES
    subname                 varchar(64)     YES
    description             varchar(128)    YES
pack
    id                      varchar(12)     NO      PRI
    page_id                 varchar(16)     YES
    section_id              varchar(20)     YES
    name                    varchar(64)     YES
    year                    varchar(4)      YES
    layout                  varchar(3)      YES             5v
    region                  varchar(1)      YES
    product_code            varchar(8)      YES
    material                varchar(1)      YES
    country                 varchar(2)      YES
    note                    varchar(32)     YES
pack_model
    id                      int(11)         NO      PRI     NULL    auto_increment
    pack_id                 varchar(12)     YES
    mod_id                  varchar(12)     YES             NULL
    var_id                  varchar(20)     YES             NULL
    display_order           int(2)          YES             0
page_info
    id                      varchar(20)     NO      PRI
    flags                   int(11)         YES             0
    health                  int(11)         YES             0
    format_type             varchar(16)     YES
    title                   varchar(80)     YES
    pic_dir                 varchar(80)     YES
    tail                    varchar(128)    YES
    description             varchar(256)    YES
    note                    varchar(256)    YES
publication
    id                      varchar(12)     NO              NULL
    first_year              varchar(4)      YES
    flags                   int(11)         YES             0
    model_type              varchar(2)      YES
    country                 varchar(2)      YES
    rawname                 varchar(64)     NO
    description             varchar(128)    YES             NULL
    section_id              varchar(2)      YES
region
    id                      varchar(1)      NO      PRI
    parent                  varchar(1)      YES
    name                    varchar(20)     YES
section
    id                      varchar(20)     NO      PRI
    page_id                 varchar(16)     NO      PRI
    display_order           int(3)          YES             0
    category                varchar(8)      YES
    flags                   int(11)         YES             0
    name                    varchar(80)     YES
    columns                 int(1)          YES             4
    start                   int(3)          YES             0
    pic_dir                 varchar(80)     YES
    disp_format             varchar(20)     YES
    link_format             varchar(20)     YES
    img_format              varchar(20)     YES
    note                    varchar(255)    YES
user
    id                      int(11)         NO      PRI     NULL    auto_increment
    name                    varchar(32)     NO      UNI
    passwd                  varchar(41)     NO
    privs                   varchar(16)     YES
    email                   varchar(80)     NO
    state                   int(4)          YES             0
    vkey                    varchar(10)     YES             NULL
variation
    mod_id                  varchar(12)     NO      PRI
    var                     varchar(8)      NO      PRI     NULL
    flags                   int(11)         YES             0
    text_body               varchar(256)    YES
    text_interior           varchar(128)    YES
    text_windows            varchar(128)    YES
    text_base               varchar(128)    YES
    text_wheels             varchar(128)    YES
    text_description                        varchar(128)    YES
    body                    varchar(64)     YES
    base                    varchar(64)     YES
    windows                 varchar(64)     YES
    interior                varchar(64)     YES
    category                varchar(32)     YES
    area                    varchar(32)     YES
    date                    varchar(32)     YES
    note                    varchar(256)    YES
    other                   varchar(64)     YES
    picture_id              varchar(8)      YES
    manufacture             varchar(32)     YES
    imported                time            YES             NULL
    imported_from           varchar(16)     YES
    imported_var            varchar(8)      YES             NULL
variation_select
    ref_id                  varchar(32)     NO      PRI
    mod_id                  varchar(12)     NO      PRI
    var_id                  varchar(8)      NO      PRI
    sub_id                  varchar(16)     NO      PRI
vehicle_make
    make                    varchar(3)      NO      PRI
    make_name               varchar(32)     YES
vehicle_type
    id                      int(2)          NO      PRI     NULL    auto_increment
    ch                      varchar(1)      YES
    name                    varchar(32)     YES
wheel
    id                      varchar(11)     NO      PRI
    description             varchar(128)    YES
'''

if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
