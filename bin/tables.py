#!/usr/local/bin/python

# readonly hidden select checkbox
# 'add' 'ask' 'clinks' 'columns' 'create' 'elinks' 'extends' 'id' 'readonly' 'titles' 'tlinks'
table_info = {
    #page_info
    'page_info': {
        'id': ['id'],
        'columns': ['id', 'flags', 'health', 'format_type', 'title', 'pic_dir', 'tail', 'description', 'note'],
        'clinks': {
                'id': {'tab': 'page_info', 'id': ['id/id']},
        },
        'tlinks': [
                {'tab': 'section', 'id': ['page_id/id']},
        ],
        'add': {
                'page_info': [],
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
	'extends': {'base_id': 'id/id'},
        'columns': ['id', 'scale', 'vehicle_type', 'country', 'make', 'section_id', 'variation_digits'],
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
                {'tab': 'casting_make', 'id': ['casting_id/id']},
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
        'ask': ['model_id', 'related_id', 'section_id'],
    },
    #attribute
    'attribute': {
        'id': ['id'],
        'columns': ['id', 'mod_id', 'attribute_name', 'definition', 'title', 'visual'],
        'clinks': {
                'id': {'tab': 'attribute', 'id': ['id/id']},
                'mod_id': {'tab': 'casting', 'id': ['id/mod_id']},
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
                'mod_id': {'tab': 'casting', 'id': ['id/mod_id']},
                'attr_id': {'tab': 'attribute', 'id': ['id/attr_id']},
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
                {'name': 'upload', 'url': 'upload.cgi?d=./pic/add&r=%(attr_type)s_%(mod_id)s-%(picture_id)s&m=%(mod_id)s&suff=%(picture_id)s'},
        ],
    },
    #variation
    'variation': {
        'id': ['mod_id', 'var'],
        'columns': ['mod_id', 'var', 'flags',
            'text_description', 'text_base', 'text_body', 'text_interior', 'text_wheels', 'text_windows',
            'base', 'body', 'interior', 'windows',
            'manufacture', 'category', 'area', 'date', 'note', 'picture_id', 'imported', 'imported_from', 'imported_var'],
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
        'id': ['id'],
        'columns': ['id', 'name', 'company_name', 'flags'],
        'clinks': {
                'id': {'tab': 'vehicle_make', 'id': ['id/id']},
        },
        'create': {
                'id': '???',
        },
        'ask': ['id'],
    },
    #casting_make
    'casting_make': {
        'id': ['id'],
        'columns': ['id', 'make_id', 'casting_id', 'flags'],
        'clinks': {
                'id': {'tab': 'casting_make', 'id': ['id/id']},
                'make_id': {'tab': 'vehicle_make', 'id': ['id/make_id']},
                'casting_id': {'tab': 'casting', 'id': ['id/casting_id']},
        },
        'add': {
                'casting_make': ['id/id'],
        },
        'ask': ['id', 'make_id', 'casting_id'],
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
        'ask': ['id', 'page_id', 'section_id', 'mod_id'],
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
        'ask': ['id', 'year', 'number', 'mod_id'],
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
	'extends': {'base_id': 'id/id'},
        'columns': ['id', 'page_id', 'section_id', 'region', 'end_year', 'layout', 'product_code', 'material', 'country', 'note'],
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
	'extends': {'base_id': 'id/id'},
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
        'id': ['id'],
        'columns': ['id', 'ref_id', 'mod_id', 'var_id', 'sub_id', 'category'],
        'create': {
                'ref_id': 'unset',
                'mod_id': 'unset',
                'var_id': 'unset',
                'sub_id': 'unset',
                'category': '',
        },
        'clinks': {
                'mod_id': {'tab': 'base_id', 'id': ['id/mod_id']},
                'var_id': {'tab': 'variation', 'id': ['mod_id/mod_id', 'var/var_id']},
        },
        'tlinks': {
        },
        'add': {
        },
        'ask': ['id', 'ref_id'],
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
    #book
    'book': {
        'id': ['id'],
	'columns': ['id', 'author', 'title', 'publisher', 'year', 'isbn', 'flags', 'pic_id'],
        'ask': ['id'],
        'add': {
		'book': [],
        },
        'clinks': {
                'id': {'tab': 'book', 'id': ['id/id']},
        },
    },
    #bayarea
    'bayarea': {
        'id': ['id'],
	'columns': ['id', 'name', 'address', 'city', 'state', 'phone', 'flags', 'url'],
        'ask': ['id'],
        'add': {
        },
        'clinks': {
                'id': {'tab': 'bayarea', 'id': ['id/id']},
        },
    },
    'token': {
	'id': ['id'],
	'columns': ['id', 'created'],
    },
    #photographer
    'photographer': {
	'id': ['id'],
	'columns': ['id', 'name', 'url'],
        'ask': ['id'],
	'add': {
		'photo_credit': ['photographer_id/id'],
		'photographer': [],
	},
        'tlinks': [
                {'tab': 'photo_credit', 'id': ['id/photographer_id']},
        ],
    },
    #photo_credit
    'photo_credit': {
	'id': ['id'],
	'columns': ['id', 'path', 'name', 'photographer_id'],
	'add': {
		'photo_credit': ['photographer_id/photographer_id'],
	},
        'tlinks': [
	],
        'clinks': {
                'id': {'tab': 'section', 'id': ['id/id']},
                'photographer_id': {'tab': 'photographer', 'id': ['id/photographer_id']},
        },
    },

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
FLAG_MODEL_REVISED_CASTING              =128
FLAG_MODEL_BASEPLATE_VISIBLE            =256

FLAG_SECTION_HIDDEN                     =  1
FLAG_SECTION_DEFAULT_IDS                =  2
FLAG_SECTION_NO_FIRSTS                  =  4
FLAG_SECTION_HIDE_IMAGE                 = 32

FLAG_MAKE_PRIMARY                       =  2

FLAG_PAGE_INFO_HIDDEN                   =  1
FLAG_PAGE_INFO_HIDE_TITLE               =  2
FLAG_PAGE_INFO_UNROLL_MODELS            =  4

FLAG_LINK_LINE_HIDDEN                   =  1
FLAG_LINK_LINE_RECIPROCAL               =  2
FLAG_LINK_LINE_PAYPAL                   =  4
FLAG_LINK_LINE_INDENTED                 =  8
FLAG_LINK_LINE_FORMAT_LARGE             = 16
FLAG_LINK_LINE_NOT_VERIFIABLE           = 32
FLAG_LINK_LINE_ASSOCIABLE               = 64
FLAG_LINK_LINE_NEW                      =128

FLAG_ITEM_HIDDEN                        =  1

#-

if __name__ == '__main__':  # pragma: no cover
    pass
