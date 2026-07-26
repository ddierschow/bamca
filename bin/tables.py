#!/usr/local/bin/python

import mbdata

# add ask bits clinks columns create db defaults editable elinks extends id readonly title tlinks
table_info = {
    # page_info
    'page_info': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'flags', 'format_type', 'style_id', 'title', 'pic_dir', 'tail', 'description', 'note'],
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
            'flags': [],
        },
        'ask': ['id', 'format_type'],
        'defaults': {
            'flags': 0,
            'health': 0,
        },
        'bits': {
            'flags': [
                ('0001', 'Hidden'),
                ('0002', 'Hide Title'),
                ('0010', 'Public'),
                ('0080', 'Admin'),
            ]
        },
    },
    # country
    'country': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'name', 'region'],
        'clinks': {
            'id': {'tab': 'country', 'id': ['id/id']},
        },
        'add': {
            'country': ['id/id'],
        },
        'create': {
            'id': '??',
        },
    },
    # section
    'section': {
        'db': 'bamca',
        'ids': ['id', 'page_id'],
        'saveid': True,
        'columns': [
            'id', 'page_id', 'display_order', 'category', 'flags', 'name', 'columns', 'start', 'pic_dir',
            'disp_format', 'link_format', 'img_format', 'note'
        ],
        'clinks': {
            'id': {'tab': 'section', 'id': ['id/id', 'page_id/page_id']},
            'page_id': {'tab': 'page_info', 'id': ['id/page_id']},
            'region': {'tab': 'region', 'id': ['id/region']},
        },
        'tlinks': [
            {'tab': 'matrix_model', 'id': ['section_id/id', 'page_id/page_id'],
             'if': "dat and dat['page_id'].startswith('matrix.')"},
            {'tab': 'lineup_model', 'id': ['year/*dat["page_id"][5:]', 'region/*dat["id"][0]'],
             'if': "dat and dat['page_id'].startswith('year.')"},
            {'tab': 'lineup_model', 'id': ['year/*dat["page_id"][5:]', 'region/id'],
             'if': "dat and dat['page_id'].startswith('year.')"},
            {'tab': 'link_line', 'id': ['section_id/id', 'page_id/page_id'],
             'if': "dat and dat['page_id'].startswith('links.')"},
            {'tab': 'pack', 'id': ['section_id/id', 'page_id/page_id'],
             'if': "dat and dat['page_id'].startswith('packs.')"},
        ],
        'add': {
            'section': ['page_id/page_id'],
            'matrix_model': ['page_id/page_id', 'section_id/id'],
            'lineup_model': ['page_id/page_id', 'region/id'],
            'pack': ['page_id/page_id', 'section_id/id'],
            'link_line': ['page_id/page_id', 'section_id/id'],
        },
        'create': {
            'id': 'newsection',
            'flags': [],
        },
        'ask': ['id', 'page_id'],
        'bits': {
            'flags': [
                ('0001', 'Hidden'),
                ('0002', 'Def IDs'),
                ('0004', 'No 1sts'),
                ('0008', 'ShowIDs'),
                ('0010', 'HideImg'),
                ('0020', 'GrpSngl'),
            ]
        },
    },
    # base_id
    'base_id': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
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
            'model_type': '',
            'rawname': '',
            'description': '',
            'flags': [],
        },
        'ask': ['id', 'first_year', 'model_type'],
        'selects': {'model_type': mbdata.model_type_names_list},
        'bits': {
            'flags': [
                ('0001', 'NotMade'),
                ('0080', 'Revised'),
                ('0100', 'BP Vis'),
            ]
        },
    },
    # casting
    'casting': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'extends': {'base_id': 'id/id'},
        'columns': ['id', 'scale', 'vehicle_type', 'country', 'make', 'section_id', 'variation_digits', 'notes', 'designer'],
        'extra_columns': [
            'format_description', 'format_body', 'format_interior', 'format_windows', 'format_base',
            'format_wheels', 'format_with', 'format_text'],
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
        'defaults': {
            'format_description': '&body',
            'format_body': '&body',
            'format_interior': '&interior',
            'format_windows': '&windows',
            'format_base': '&base|&manufacture',
            'format_wheels': '&wheels',
            'variation_digits': 2,
        },
        'formats': ['description', 'body', 'base', 'wheels', 'interior', 'windows', 'with', 'text'],
    },
    # casting_related
    'casting_related': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'model_id', 'related_id', 'section_id', 'picture_id', 'description', 'flags'],
        'clinks': {
            'id': {'tab': 'casting_related', 'id': ['id/id']},
            'model_id': {'tab': 'base_id', 'id': ['id/model_id']},
            'related_id': {'tab': 'base_id', 'id': ['id/related_id']},
        },
        'create': {
            'model_id': 'unset',
            'related_id': 'unset',
            'flags': [],
        },
        'ask': ['model_id', 'related_id', 'section_id'],
        'bits': {
            'flags': [
                ('0002', 'Shared'),
            ]
        },
    },
    # attribute
    'attribute': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'mod_id', 'attribute_name', 'definition', 'title', 'visual', 'flags'],
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
            'flags': [],
        },
        'bits': {
            'flags': [
                ('0001', 'Sparse'),
                ('0002', 'Visual'),
            ]
        },
    },
    # attribute_picture
    'attribute_picture': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
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
            {'name': 'upload',
             'url':
                 'upload.cgi?d=./pic/add&r=%(attr_type)s_%(mod_id)s-%(picture_id)s&m=%(mod_id)s&suff=%(picture_id)s'},
        ],
    },
    # variation
    'variation': {
        'db': 'bamca',
        'ids': ['mod_id', 'var'],
        'saveid': True,
        'columns': [
            'mod_id', 'var', 'flags', 'text_description',
            'text_base', 'text_body', 'text_interior', 'text_wheels', 'text_windows', 'text_with', 'text_text',
            'base', 'body', 'deco', 'deco_type', 'interior', 'wheels', 'windows',
            'manufacture', 'additional_text', 'base_name', 'base_number', 'base_scale', 'tool_id', 'production_id',
            'copyright', 'company_name', 'logo_type', 'base_reads', 'area', 'date',
            'note', 'picture_id', 'imported', 'imported_from', 'imported_var', 'category', 'variation_type'
        ],
        'title': {
            'mod_id': 'Model ID', 'var': 'Variation ID', 'flags': 'Flags', 'text_description': 'Description',
            'text_base': 'Base', 'text_body': 'Body', 'text_interior': 'Interior', 'text_wheels': 'Wheels',
            'text_windows': 'Windows', 'text_with': 'With', 'text_text': 'Base Text',
            'tool_id': 'Tool ID', 'production_id': 'Production ID', 'picture_id': 'Picture ID',
            'base': 'Base', 'body': 'Body', 'deco': 'Deco', 'deco_type': 'Deco Type', 'interior': 'Interior',
            'wheels': 'Wheels', 'windows': 'Windows',
        },
        'clinks': {
            'var': {'tab': 'variation', 'id': ['mod_id/mod_id', 'var/var']},
            'mod_id': {'tab': 'casting', 'id': ['id/mod_id']},
        },
        'tlinks': [
            {'tab': 'detail', 'id': ['mod_id/mod_id', 'var_id/var'],
             'ref': {'attr_id': ['attribute', 'id', 'attribute_name']}},
        ],
        'add': {
            'variation': ['mod_id/mod_id'],
        },
        'create': {
            'var': 'unset',
            'flags': [],
        },
        'selects': {'deco_type': mbdata.deco_types},
        'bits': {
            'flags': [
                ('0002', 'Code2'),
                ('0008', 'Incorrect'),
                ('0080', 'Verified'),
            ]
        },
        'internals': [
            'base', 'body', 'interior', 'wheels', 'windows', 'deco',
            'manufacture', 'additional_text', 'base_name', 'base_number', 'tool_id',
            'copyright', 'company_name', 'production_id', 'base_scale', 'base_reads',  # 'logo_type',
        ],
        'meta': [
            'mod_id', 'var', 'flags', 'text_description', 'text_base', 'text_body', 'text_interior', 'text_wheels',
            'text_windows', 'text_with', 'text_text', 'area', 'date', 'note', 'picture_id', 'imported',
            'imported_from', 'imported_var', 'category', 'variation_type'],
    },
    # detail
    'detail': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'mod_id', 'var_id', 'attr_id', 'description'],
        'clinks': {
            'attr_id': {'tab': 'attribute', 'id': ['id/attr_id']},
        },
        'create': {
            'mod_id': 'unset',
            'var_id': 'unset',
            'attr_id': 'unset',
        }
    },
    # wheel
    'wheel': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'description'],
        'create': {
            'id': 'unset',
        }
    },
    # alias
    'alias': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['pk', 'id', 'first_year', 'ref_id', 'section_id', 'type', 'flags'],
        'clinks': {
            'id': {'tab': 'alias', 'id': ['id/id']},
            'ref_id': {'tab': 'base_id', 'id': ['id/ref_id']},
        },
        'add': {
            'alias': ['ref_id/ref_id'],
        },
        'create': {
            'id': 'unset',
            'flags': [],
        },
        'ask': ['id', 'ref_id', 'type'],
        'bits': {
            'flags': [
                ('0002', 'Shared'),
            ]
        },
    },
    # vehicle_type
    'vehicle_type': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'ch', 'name'],
        'clinks': {
            'id': {'tab': 'vehicle_type', 'id': ['id/id']},
        },
    },
    # counter
    'counter': {
        'db': 'buser',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'value', 'timestamp', 'health'],
        'clinks': {
            'id': {'tab': 'counter', 'id': ['id/id']},
        },
    },
    # vehicle_make
    'vehicle_make': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'name', 'company_name', 'flags'],
        'clinks': {
            'id': {'tab': 'vehicle_make', 'id': ['id/id']},
        },
        'create': {
            'id': '???',
            'flags': [],
        },
        'ask': ['id'],
        'bits': {
            'flags': [
                ('0001', 'Hidden'),
            ]
        },
    },
    # casting_make
    'casting_make': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
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
        'create': {
            'flags': [],
        },
        'bits': {
            'flags': [
                ('0001', 'Hidden'),
                ('0002', 'Primary'),
            ]
        },
    },
    # matrix_model
    'matrix_model': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'extends': {'base_id': 'base_id/id'},
        'columns': [
            'id', 'base_id', 'page_id', 'section_id', 'display_order', 'range_id', 'mod_id', 'sub_id',
            'style_id', 'shown_id', 'name', 'subname', 'description', 'flags'
        ],
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
        # select distinct flags from alias;
        'create': {
            'flags': [],
        },
        'bits': {
            'flags': [
                ('0001', 'Hidden'),
                ('0004', 'NoVar'),
                ('0008', 'NoID'),
                ('0010', 'ShowAllVar'),
            ]
        },
    },
    # region
    'region': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
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
    # lineup_model
    'lineup_model': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'extends': {'base_id': 'base_id/id'},
        'columns': [
            'id', 'base_id', 'mod_id', 'sub_id', 'number', 'display_order', 'flags', 'style_id', 'picture_id',
            'region', 'year', 'name', 'subname', 'page_id'
        ],
        'clinks': {
            'id': {'tab': 'lineup_model', 'id': ['id/id']},
            'mod_id': {'tab': 'base_id', 'id': ['id/mod_id']},
            'year': {'tab': 'lineup_model', 'id': ['year/year']},
        },
        'tlinks': [
            {'tab': 'base_id', 'id': ['base_id/id']},
            {'tab': 'variation_select', 'id': ['mod_id/mod_id']},
        ],
        'add': {
            'lineup_model': [],
        },
        'ask': ['id', 'year', 'region', 'number', 'mod_id'],
        'create': {
            'flags': [],
        },
        'bits': {
            'flags': [
                ('0001', 'Hidden'),
                ('0002', 'MultiVar'),
                ('0008', 'NoID'),
            ]
        },
    },
    # link_line
    'link_line': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': [
            'id', 'page_id', 'section_id', 'display_order', 'flags', 'associated_link', 'last_status', 'link_type',
            'country', 'url', 'name', 'description', 'note'
        ],
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
        'create': {
            'flags': [],
        },
        'selects': {'link_type': [
            ('b', 'bad'),
            ('f', 'folder'),
            ('g', 'graphic'),
            ('l', 'normal'),
            ('n', 'none'),
            ('p', 'button'),
            ('s', 'star'),
            ('t', 'text'),
            ('x', 'trash'),
        ]},
        'bits': {
            'flags': [
                ('0001', 'Hid'),
                ('0002', 'Recip'),
                ('0004', 'Paypal'),
                ('0008', 'Indent'),
                ('0010', 'Large'),
                ('0020', 'NoVer'),
                ('0040', 'Assoc'),
                ('0080', 'New'),
                ('0100', 'Dis'),
            ]
        },
    },
    # blacklist
    'blacklist': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'reason', 'target'],
        'clinks': {
            'id': {'tab': 'blacklist', 'id': ['id/id']},
        },
        'add': {
            'blacklist': [],
        },
    },
    # user
    'user': {
        'db': 'buser',
        'ids': ['id'],
        'saveid': False,
        'columns': [
            'id', 'user_id', 'privs', 'email', 'vkey', 'first_name', 'last_name', 'location', 'interests', 'flags',
            'photographer_id', 'last_login',
        ],
        'editable': [
            'user_id', 'email', 'first_name', 'last_name', 'location', 'interests',
        ],
        'title': {
            'id': 'ID', 'user_id': 'User ID', 'privs': 'Privs', 'email': 'Email', 'vkey': 'VKey',
            'first_name': 'First Name', 'last_name': 'Last Name', 'location': 'Location',
            'interests': 'Interests', 'flags': 'Flags', 'photographer_id': 'Photographer ID',
            'last_login': 'Last Login', 'ckey': 'CKey',
        },
        'ask': ['id', 'user_id', 'first_name', 'last_name'],
        'clinks': {
            'id': {'tab': 'user', 'id': ['id/id']},
        },
        'readonly': ['id', 'passwd', 'vkey', 'last_login'],
        'bits': {
            'flags': [
                ('0001', 'Hidden'),
                ('0010', 'BAMCA Mem'),
                ('0020', 'Verified'),
                ('0080', 'New'),
                ('0100', 'PW Rec'),
            ]
        },
    },
    # pack
    'pack': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': True,
        'extends': {'base_id': 'id/id'},
        'columns': [
            'id', 'var', 'page_id', 'section_id', 'region', 'end_year', 'layout', 'product_code', 'material',
            'country', 'note'
        ],
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
    # pack_model
    'pack_model': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'pack_id', 'pack_var', 'mod_id', 'flags', 'style_id', 'display_order', 'subname'],
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
        'bits': {
            'flags': [
                ('0040', 'NoMan'),
            ]
        },
    },
    # publication
    'publication': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': True,
        'extends': {'base_id': 'id/id'},
        'columns': ['id', 'country', 'section_id', 'isbn'],
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
            'publication': [],
            'lineup_model': ['mod_id/id'],
        },
        'create': {
            'id': 'unset',
        },
        'ask': ['id', 'section_id'],
    },
    # variation_select
    'variation_select': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': True,
        'columns': ['id', 'ref_id', 'mod_id', 'var_id', 'sec_id', 'ran_id', 'category'],
        'create': {
            'ref_id': 'unset',
            'mod_id': 'unset',
            'var_id': 'unset',
            'sec_id': '',
            'ran_id': '',
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
    # box_type
    'box_type': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': [
            'id', 'mod_id', 'section_id', 'box_type', 'pic_id', 'box_size', 'additional_text', 'bottom', 'sides',
            'end_flap', 'model_name', 'year', 'notes'
        ],
        'clinks': {
            'id': {'tab': 'box_type', 'id': ['id/id']},
        },
        # 'tlinks': [
        #         {'tab': 'alias', 'id': ['id/mod_id']},
        #         {'tab': 'casting', 'id': ['id/mod_id']},
        # ],
    },
    # book - reference books and magazines
    'book': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'author', 'title', 'publisher', 'year', 'isbn', 'flags', 'pic_id'],
        'ask': ['id'],
        'add': {
            'book': [],
        },
        'clinks': {
            'id': {'tab': 'book', 'id': ['id/id']},
        },
        'create': {
            'flags': [],
        },
        'bits': {
            'flags': [
                ('0001', 'Hidden'),
                ('0010', 'Mag'),
            ]
        },
    },
    # periodical
    'periodical': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': True,
        'columns': ['id', 'pub_id', 'volume', 'issue', 'date', 'pages'],
        'clinks': {
            'book': {'tab': 'book', 'id': ['id/pub_id']},
        },
        'add': {
            'article': ['mod_id/id'],
        },
        'create': {
        },
        'ask': ['pub_id', 'volume', 'issue', 'date'],
    },
    # article
    'article': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': True,
        'columns': ['id', 'per_id', 'title', 'author', 'page'],
        'clinks': {
            'pub_id': {'tab': 'periodical', 'id': ['id/per_id']},
        },
        'add': {
        },
        'create': {
        },
        'ask': ['id', 'per_id', 'title'],
    },
    # bayarea
    'bayarea': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'name', 'address', 'city', 'state', 'phone', 'flags', 'url'],
        'ask': ['id'],
        'add': {
        },
        'clinks': {
            'id': {'tab': 'bayarea', 'id': ['id/id']},
        },
    },
    # token
    'token': {
        'db': 'buser',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'created'],
    },
    # photographer
    'photographer': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': True,
        'columns': ['id', 'name', 'url', 'flags', 'example_id'],
        'ask': ['id'],
        'add': {
            'photo_credit': ['photographer_id/id'],
            'photographer': [],
        },
        'tlinks': [
            {'tab': 'photo_credit', 'id': ['photographer_id/id']},
        ],
        'clinks': {
            'id': {'tab': 'photo_credit', 'id': ['example_id/id']},
        },
        'create': {
            'flags': [],
        },
        'bits': {
            'flags': [
                ('0001', 'Hidden'),
            ]
        },
    },
    # photo_credit
    'photo_credit': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
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
    # credit_pattern
    'credit_pattern': {  # c|man/bk001|DT|BeachCar
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'directory', 'photographer_id', 'pattern'],
        'add': {
            'photo_credit': ['photographer_id/photographer_id'],
        },
        'tlinks': [
        ],
        'clinks': {
            'id': {'tab': 'section', 'id': ['id/id']},
            'photographer_id': {'tab': 'photographer', 'id': ['id/photographer_id']},
        },
        'ask': ['directory', 'photographer_id', 'pattern'],
    },
    # category
    'category': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'name', 'flags', 'image'],
        'add': {
            'category': ['id/id'],
        },
        'tlinks': [
        ],
        'clinks': {
        },
        'create': {
            'flags': [],
        },
        'ask': ['id', 'name'],
        'bits': {
            'flags': [
                ('0001', 'Hidden'),
                ('0002', '2'),
                ('0004', 'Indexed'),
            ]
        },
    },
    # user_item
    'user_item': {
        'db': 'buser',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'user_id', 'base_id', 'flags', 'own_type', 'comment'],
        'add': {
            'user_item': ['id/id'],
        },
        'tlinks': [
        ],
        'clinks': {
        },
        'ask': ['id', 'user_id', 'base_id'],
    },
    # tumblr
    'tumblr': {
        'db': 'buser',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'payload', 'response', 'post_type'],
    },
    # mbusa
    'mbusa': {
        'db': 'bamca',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'mod_id', 'var_id', 'model', 'variation', 'description', 'date', 'file'],
    },
    # cookie
    'cookie': {
        'db': 'buser',
        'ids': ['id'],
        'saveid': False,
        'columns': ['id', 'ckey', 'user_id', 'ip', 'expires'],
    },
}
home_db = 'bamca'


class TableData(object):

    def __init__(self, name, db, add=None, ask=None, bits=None, clinks=None, columns=None, create=None,
                 defaults=None, editable=None, elinks=None, extends=None, extra_columns=None, formats=None, hidden=None,
                 ids=None, internals=None, meta=None, readonly=None, saveid=False, selects=None, title=None, tlinks=None):
        self.db = db
        self.name = name
        self.add = add or {}
        self.ask = ask or []
        self.bits = bits or {}
        self.clinks = clinks or {}
        self.columns = columns or []
        self.create = create or {}
        self.defaults = defaults or {}
        self.editable = editable or []
        self.elinks = elinks or []
        self.extends = extends or {}
        self.extra_columns = extra_columns or []
        self.formats = formats or []
        self.hidden = hidden or []
        self.ids = ids or []
        self.internals = internals or []
        self.meta = meta or []
        self.readonly = readonly or []
        self.saveid = saveid
        self.selects = selects or []
        self.title = title or {}
        self.tlinks = tlinks or {}


table_data = {x: TableData(x, **y) for x, y in table_info.items()}

# -
