import re

import config
import mbdata
import useful

id_re = re.compile(r'''(?P<a>[a-zA-Z]*)(?P<d>\d*)''')


class ManItem(object):

    def __init__(self, mod):
        self.box_styles = ''
        self.count = 0
        self.country = ''
        self.description = ''
        self.first_year = ''
        self.flags = 0
        self.format_base = ''
        self.format_body = ''
        self.format_description = ''
        self.format_interior = ''
        self.format_text = ''
        self.format_wheels = ''
        self.format_windows = ''
        self.format_with = ''
        self.id = ''
        self.isbn = ''
        self.link = "single.cgi?id"
        self.make = ''
        self.model_type = 'SF'
        self.name = ''
        self.nodesc = False
        self.notes = ''
        self.picture_id = ''
        self.prefix = 's'
        self.rawname = ''
        self.ref_id = ''
        self.scale = ''
        self.section_id = ''
        self.shown_id = ''
        self.subname = ''
        self.unlicensed = '?'
        self.vars = 0
        self.variation_digits = 2
        self.vehicle_type = ''
        self.visual_id = ''

        if isinstance(mod, dict):
            if 'link' in mod:
                self.slurp(mod)

            else:
                self.id = self.ref_id = mod.get('base_id.id') or ''
                self.visual_id = self.default_id(self.id)
                self.first_year = mod.get('base_id.first_year') or ''
                self.flags = mod.get('base_id.flags') or 0
                self.model_type = mod.get('base_id.model_type') or ''
                self.rawname = mod.get('base_id.rawname') or ''
                self.name = self.rawname.replace(';', ' ')
                self.description = mod.get('base_id.description') or ''

                self.scale = mod.get('casting.scale') or ''
                self.vehicle_type = mod.get('casting.vehicle_type') or ''
                self.country = mod.get('casting.country') or ''
                self.make = mod.get('casting.make') or ''
                self.box_styles = mod.get('casting.box_styles') or ''
                self.notes = mod.get('casting.notes') or ''
                self.section_id = mod.get('casting.section_id') or ''
                self.format_description = mod.get('casting.format_description') or ''
                self.format_body = mod.get('casting.format_body') or ''
                self.format_interior = mod.get('casting.format_interior') or ''
                self.format_windows = mod.get('casting.format_windows') or ''
                self.format_base = mod.get('casting.format_base') or ''
                self.format_wheels = mod.get('casting.format_wheels') or ''
                self.format_with = mod.get('casting.format_with') or ''
                self.variation_digits = mod.get('casting.variation_digits') or ''
                self.format_text = mod.get('casting.format_text') or ''

                if mod.get('alias.id'):
                    self.section_id = mod['alias.section_id']
                    self.ref_id = mod['alias.ref_id']
                    if mod.get('alias.first_year'):
                        self.first_year = mod['alias.first_year']
                    self.id = mod['alias.id']
                    if self.ref_id != self.id:
                        self.description += ';same as ' + self.ref_id
                    # self.vehicle_type = mod['vehicle_type'] or ''

                self.vars = mod.get('vars', 0)  # for single only

            self.pack = PackItem(mod)
            self.pub = PubItem(mod)
            self.count = mod.get('count') or 0
            if 'section.id' in mod:
                self.section = SecItem(mod)

        else:
            # EVERYBODY has a base_id.  After that, we differentiate.
            if hasattr(mod, 'rawname'):  # ManItem
                self.id = self.ref_id = mod.id
                self.first_year = mod.first_year
                self.flags = mod.flags
                self.model_type = mod.model_type
                self.rawname = mod.rawname
                self.description = mod.description
                self.format_description = mod.format_description or ''
                self.format_body = mod.format_body or ''
                self.format_interior = mod.format_interior or ''
                self.format_windows = mod.format_windows or ''
                self.format_base = mod.format_base or ''
                self.format_wheels = mod.format_wheels or ''
                self.format_with = mod.format_with or ''
                self.format_text = mod.format_text or ''
            self.visual_id = self.default_id(self.id)
            self.name = self.rawname.replace(';', ' ')

            self.scale = mod.scale
            self.vehicle_type = mod.vehicle_type
            self.country = mod.country
            self.make = mod.make
            self.box_styles = mod.box_styles
            self.notes = mod.notes or ''
            self.section_id = mod.section_id
            self.variation_digits = mod.variation_digits
            self.count = mod.count or 0

            self.pack = PackItem(mod.pack if hasattr(mod, 'pack') else {})
            self.pub = PubItem(mod.pub if hasattr(mod, 'pub') else {})

        if self.pack.id:
            self.link = 'packs.cgi?id'
        self.unlicensed = '-' if self.make == 'unl' else '?' if not self.make else ' '
        self.casting_type = mbdata.model_types.get(self.model_type, 'Casting')
        self.descs = [x for x in self.description.split(';') if x]
        self.filename = self.id.lower()
        self.iconname = self.icon_name(self.rawname)
        self.linkid = self.ref_id
        self.shortname = self.short_name(self.rawname)
        self.libdir = useful.relpath('.', config.LIB_MAN_DIR, self.id.lower())

    def __str__(self):
        return f'ManItem: {self.id}'

    @staticmethod
    def default_id(id):
        if id_m := id_re.match(id):
            return id_m.group('a').upper() + '-' + id_m.group('d')
        return id_m

    def get_attr(self, k, v=''):
        return getattr(self, k, v)

    @staticmethod
    def short_name(name):
        if not name:
            return ''
        if name.startswith('('):
            name = name[name.find(')') + 2:]
        if '(' in name:
            name = name[:name.find('(') - 1] + name[name.find(')') + 1:]
        name = name.replace(';', ' ')
        if name.startswith('-'):
            name = name[1:]
        if name.endswith('/'):
            name = name[:-1]
        if name.endswith('-'):
            name = name[:-1]
        name = name.strip().replace('*', '')
        return name

    @staticmethod
    def icon_name(name):
        if not name:
            return ['']
        name = mbdata.paren_re.sub(' ', name).replace('*', '')

        def mangle_line(n):
            if n.startswith('-'):
                n = name[1:]
            if n.endswith('/'):
                n = n[:-1]
            return n.strip()

        return [mangle_line(n) for n in name.split(';')]

    def slurp(self, slurp_d):
        for k, v in slurp_d.items():
            setattr(self, k, v)

    @property
    def made(self):
        return not (self.flags & config.FLAG_MODEL_NOT_MADE)

    @property
    def not_made(self):
        return bool(self.flags & config.FLAG_MODEL_NOT_MADE)

    @property
    def code_2(self):
        return bool(self.flags & config.FLAG_MODEL_CODE_2)

    @property
    def is_no_variation(self):
        return bool(self.flags & config.FLAG_MODEL_NO_VARIATION)

    @property
    def no_id(self):
        return bool(self.flags & config.FLAG_MODEL_NO_ID)

    @property
    def id_incorrect(self):
        return bool(self.flags & config.FLAG_MODEL_ID_INCORRECT)

    @property
    def show_all_variations(self):
        return bool(self.flags & config.FLAG_MODEL_SHOW_ALL_VARIATIONS)

    @property
    def hide_image(self):
        return bool(self.flags & config.FLAG_MODEL_HIDE_IMAGE)

    @property
    def no_specific_model(self):
        return bool(self.flags & config.FLAG_MODEL_NO_SPECIFIC_MODEL)

    @property
    def casting_revised(self):
        return bool(self.flags & config.FLAG_MODEL_CASTING_REVISED)

    @property
    def variation_verified(self):
        return bool(self.flags & config.FLAG_MODEL_VARIATION_VERIFIED)

    @property
    def baseplate_visible(self):
        return bool(self.flags & config.FLAG_MODEL_BASEPLATE_VISIBLE)


class VSItem(object):

    def __init__(self, vs):
        if isinstance(vs, dict):
            prefix = 'vs.' if 'vs.ref_id' in vs else 'variation_select.' if 'variation_select.ref_id' in vs else ''
            self.id = vs.get(f'{prefix}id')
            self.mod_id = vs.get(f'{prefix}mod_id') or ''
            self.var_id = vs.get(f'{prefix}var_id') or ''
            self.ref_id = vs.get(f'{prefix}ref_id') or ''
            self.sec_id = vs.get(f'{prefix}sec_id') or ''
            self.ran_id = vs.get(f'{prefix}ran_id') or ''
            self.vs_cat = vs.get(f'{prefix}category') or ''
            self.vs_cat_flags = vs.get(f'{prefix}category.flags') or 0
        else:
            self.id = vs.id
            self.mod_id = vs.mod_id or ''
            self.var_id = vs.var_id or ''
            self.ref_id = vs.ref_id or ''
            self.sec_id = vs.sec_id or ''
            self.ran_id = vs.ran_id or ''
            self.vs_cat = vs.vs_cat or ''
            self.vs_cat_flags = vs.vs_cat_flags or 0

    def __str__(self):
        return f'VSItem: {self.id}'


class VarItem(object):

    def __init__(self, var, dets=None, vs=None):
        dets = dets or {}
        if isinstance(var, dict):
            prefix = 'v.' if 'v.var' in var else 'variation.' if 'variation.var' in var else ''
            self.mod_id = var.get(f'{prefix}mod_id') or ''
            self.var = var.get(f'{prefix}var') or ''
            self.flags = var.get(f'{prefix}flags') or 0
            self.text_description = var.get(f'{prefix}text_description') or ''
            self.text_base = var.get(f'{prefix}text_base') or ''
            self.text_body = var.get(f'{prefix}text_body') or ''
            self.text_interior = var.get(f'{prefix}text_interior') or ''
            self.text_wheels = var.get(f'{prefix}text_wheels') or ''
            self.text_windows = var.get(f'{prefix}text_windows') or ''
            self.text_with = var.get(f'{prefix}text_with') or ''
            self.text_text = var.get(f'{prefix}text_text') or ''
            self.manufacture = var.get(f'{prefix}manufacture') or ''
            self.iattrs = {k: v for k, v in (dets.items() or {})}
            self.iattrs.update({
                'base': var.get(f'{prefix}base', '') or dets.get('base', ''),
                'body': var.get(f'{prefix}body', '') or dets.get('body', ''),
                'deco': var.get(f'{prefix}deco', '') or dets.get('deco', ''),
                'deco_type': var.get(f'{prefix}deco_type', '') or dets.get('deco_type', ''),
                'interior': var.get(f'{prefix}interior', '') or dets.get('interior', ''),
                'wheels': var.get(f'{prefix}wheels', '') or dets.get('wheels', ''),
                'windows': var.get(f'{prefix}windows', '') or dets.get('windows', ''),
                'manufacture': self.manufacture or dets.get('manufacture', ''),
                'additional_text': var.get(f'{prefix}additional_text', '') or dets.get('additional_text', ''),
                'base_name': var.get(f'{prefix}base_name', '') or dets.get('base_name', ''),
                'base_number': var.get(f'{prefix}base_number', '') or dets.get('base_number', ''),
                'base_scale': var.get(f'{prefix}base_scale', '') or dets.get('base_scale', ''),
                'tool_id': var.get(f'{prefix}tool_id', '') or dets.get('tool_id', ''),
                'production_id': var.get(f'{prefix}production_id', '') or dets.get('production_id', ''),
                'copyright': var.get(f'{prefix}copyright', '') or dets.get('copyright', ''),
                'company_name': var.get(f'{prefix}company_name', '') or dets.get('company_name', ''),
                'logo_type': var.get(f'{prefix}logo_type', '') or dets.get('logo_type', ''),
                'base_reads': var.get(f'{prefix}base_reads', '') or dets.get('base_reads', ''),
            })
            self.date = var.get(f'{prefix}date') or ''
            self.note = var.get(f'{prefix}note') or ''
            self.picture_id = var.get(f'{prefix}picture_id', '') or self.var
            self.imported = var.get(f'{prefix}imported') or ''
            self.imported_from = var.get(f'{prefix}imported_from') or ''
            self.imported_var = var.get(f'{prefix}imported_var') or ''
            self.category = var.get(f'{prefix}category', '').split()
            self.variation_type = var.get(f'{prefix}variation_type') or ''
            self.area = var.get(f'{prefix}area', '').split(';')
            self.area = ', '.join([mbdata.get_countries().get(x, mbdata.areas.get(x, x)) for x in self.area])
            self.link = f'?mod={self.mod_id}&var={self.var}'
            self._catdefs = {}
            if 'vs' in var:
                self.vs = [VSItem(x) for x in var['vs']]
            else:
                self.vs = [VSItem(var)] if 'vs.ref_id' in var or 'variation_select.ref_id' in var else []
            if vs:
                self.vs.extend([VSItem(x) for x in vs])
        else:
            self.mod_id = var.mod_id or ''
            self.var = var.var or ''
            self.flags = var.flags or 0
            self.text_description = var.text_description or ''
            self.text_base = var.text_base or ''
            self.text_body = var.text_body or ''
            self.text_interior = var.text_interior or ''
            self.text_wheels = var.text_wheels or ''
            self.text_windows = var.text_windows or ''
            self.text_with = var.text_with or ''
            self.text_text = var.text_text or ''
            self.manufacture = var.manufacture or ''
            if hasattr(var, 'iattrs'):
                self.iattrs = {k: v for k, v in var.iattrs.items()}
            else:
                self.iattrs = {
                    'base': var.base or '',
                    'body': var.body or '',
                    'deco': var.deco or '',
                    'deco_type': var.deco_type or '',
                    'interior': var.interior or '',
                    'wheels': var.wheels or '',
                    'windows': var.windows or '',
                    'manufacture': self.manufacture or '',
                    'additional_text': var.additional_text or '',
                    'base_name': var.base_name or '',
                    'base_number': var.base_number or '',
                    'base_scale': var.base_scale or '',
                    'tool_id': var.tool_id or '',
                    'production_id': var.production_id or '',
                    'copyright': var.copyright or '',
                    'company_name': var.company_name or '',
                    'logo_type': var.logo_type or '',
                    'base_reads': var.base_reads or '',
                }
            self.date = var.date or ''
            self.note = var.note or ''
            self.picture_id = var.picture_id or self.var
            self.imported = var.imported or ''
            self.imported_from = var.imported_from or ''
            self.imported_var = var.imported_var or ''
            self.category = var.category
            self.variation_type = var.variation_type or ''
            self.area = var.area.split(';')
            self.area = ', '.join([mbdata.get_countries().get(x, mbdata.areas.get(x, x)) for x in self.area])
            self.link = f'?mod={self.mod_id}&var={self.var}'
            self._catdefs = {}
            self.vs = [VSItem(x) for x in var.vs]
            if vs:
                self.vs.extend([VSItem(x) for x in vs])
            if dets:  # note: doesn't account for model-wide defaults or maybe it does
                self.iattrs.update(dets)

    def __str__(self):
        return f'VarItem: {self.mod_id}-{self.var}'

    def get_attr(self, k, v=''):
        return self.iattrs.get(k, getattr(self, k, v))

    def clear(self):
        self.text_description = ''
        self.picture_id = ''
        self.var = ''
        self.ref_id = ''
        self.sec_id = ''
        self.ran_id = ''

    @property
    def pic_file_name(self):
        return f'{self.mod_id}-{self.picture_id}'.lower()


class PackItem(object):

    def __init__(self, pack):
        if isinstance(pack, dict):
            self.id = pack.get('pack.id') or ''
            self.var = pack.get('pack.var') or ''
            self.page_id = pack.get('pack.page_id') or ''
            self.section_id = pack.get('pack.section_id') or ''
            self.name = pack.get('pack.name') or pack.get('base_id.name') or ''
            self.year = pack.get('pack.year') or ''
            self.end_year = pack.get('pack.end_year') or ''
            self.layout = pack.get('pack.layout') or ''
            self.region = pack.get('pack.region') or ''
            self.product_code = pack.get('pack.product_code') or ''
            self.material = pack.get('pack.material') or ''
            self.country = pack.get('pack.country') or ''
            self.note = pack.get('pack.note') or ''
            self.first_year = pack.get('base_id.first_year') or ''
            self.rawname = pack.get('base_id.rawname') or ''
            self.flags = pack.get('base_id.flags') or 0
            self.model_type = pack.get('base_id.model_type') or ''
            self.rawname = pack.get('base_id.rawname') or ''
            self.name = self.rawname.replace(';', ' ')
            self.description = pack.get('base_id.description') or ''
            self.page_info = PageItem(pack)
            self.section = SecItem(pack)

        else:
            self.id = pack.id or ''
            self.var = pack.var or ''
            self.page_id = pack.page_id or ''
            self.section_id = pack.section_id or ''
            self.name = pack.name or ''
            self.year = pack.year or ''
            self.end_year = pack.end_year or ''
            self.layout = pack.layout or ''
            self.region = pack.region or ''
            self.product_code = pack.product_code or ''
            self.material = pack.material or ''
            self.country = pack.country or ''
            self.note = pack.note or ''
            self.first_year = pack.first_year or ''
            self.rawname = pack.rawname or ''
            self.flags = pack.flags or ''
        self.longid = self.id + ('-' + self.var if self.var else '')
        self.name = self.rawname.replace(';', ' ')
        self.pic = ''
        self.thumb = ''

    def __str__(self):
        return f'PackItem: {self.id}'

    def get(self, k, v=''):
        return getattr(self, k, v)


class PackModelItem(object):

    def __init__(self, pm):
        if isinstance(pm, dict):
            self.id = pm.get('pack_model.id') or 0
            self.pack_id = pm.get('pack_model.pack_id') or ''
            self.pack_var = pm.get('pack_model.pack_var') or ''
            self.mod_id = pm.get('pack_model.mod_id') or ''
            self.flags = pm.get('pack_model.flags') or 0
            self.style_id = pm.get('pack_model.style_id') or ''
            self.display_order = pm.get('pack_model.display_order') or 0
            self.subname = pm.get('pack_model.subname') or ''
            self.vs = VSItem(pm)
            self.v = VarItem(pm)
            self.man = ManItem(pm)
        else:
            self.id = pm.id or 0
            self.pack_id = pm.pack_id or ''
            self.pack_var = pm.pack_var or ''
            self.mod_id = pm.mod_id or ''
            self.flags = pm.flags or 0
            self.style_id = pm.style_id or ''
            self.display_order = pm.display_order or 0
            self.subname = pm.subname or ''
            self.vs = VSItem(pm.vs)
            self.v = VarItem(pm.v)
            self.man = ManItem(pm.man)
        self.name = self.man.name
        self.subnames = []
        self.additional = ''

    def __str__(self):
        return f'PackModelItem: {self.id}/{self.mod_id}'


class PubItem(object):

    def __init__(self, mod):
        if isinstance(mod, dict):
            self.id = mod.get('publication.id') or ''
            self.country = mod.get('publication.country') or ''
            self.section_id = mod.get('publication.section_id') or ''
            self.isbn = mod.get('publication.isbn') or ''
            self.first_year = mod.get('base_id.first_year') or ''
            self.flags = mod.get('base_id.flags') or 0
            self.model_type = mod.get('base_id.model_type') or ''
            self.rawname = mod.get('base_id.rawname') or ''
            self.description = mod.get('base_id.description') or ''
        else:
            self.id = mod.id or ''
            self.country = mod.country or ''
            self.section_id = mod.section_id or ''
            self.isbn = mod.isbn or ''
            self.first_year = mod.first_year
            self.flags = mod.flags
            self.model_type = mod.model_type
            self.rawname = mod.rawname
            self.description = mod.description
        self.name = self.rawname.replace(';', ' ')

    def __str__(self):
        return f'PubItem: {self.id}'


class PageItem(object):

    def __init__(self, pg):
        if isinstance(pg, dict):
            prefix = 'page_info.' if 'page_info.id' in pg else ''
            self.id = pg.get(f'{prefix}id') or ''
            self.flags = pg.get(f'{prefix}flags') or 0
            self.format_type = pg.get(f'{prefix}format_type') or ''
            self.style_id = pg.get(f'{prefix}style_id') or ''
            self.title = pg.get(f'{prefix}title') or ''
            self.pic_dir = pg.get(f'{prefix}pic_dir') or ''
            self.tail = pg.get(f'{prefix}tail') or ''
            self.description = pg.get(f'{prefix}description') or ''
            self.note = pg.get(f'{prefix}note') or ''
        else:
            self.id = pg.id or ''
            self.flags = pg.flags or 0
            self.format_type = pg.format_type or ''
            self.style_id = pg.style_id or ''
            self.title = pg.title or ''
            self.pic_dir = pg.pic_dir or ''
            self.tail = pg.tail or ''
            self.description = pg.description or ''
            self.note = pg.note or ''

    def __str__(self):
        return f'PageItem: {self.id}'

    @property
    def is_hidden(self):
        return bool(self.flags & config.FLAG_PAGE_INFO_HIDDEN)


class SecItem(object):

    def __init__(self, sec):
        if isinstance(sec, dict):
            prefix = 'section.' if 'section.id' in sec else ''
            self.id = sec.get(f'{prefix}id') or ''
            self.page_id = sec.get(f'{prefix}page_id') or ''
            self.display_order = sec.get(f'{prefix}display_order') or 0
            self.category = sec.get(f'{prefix}category') or ''
            self.flags = sec.get(f'{prefix}flags') or 0
            self.name = sec.get(f'{prefix}name') or ''
            self.columns = sec.get(f'{prefix}columns') or 0
            self.start = sec.get(f'{prefix}start') or 0
            self.pic_dir = sec.get(f'{prefix}pic_dir') or ''
            self.disp_format = sec.get(f'{prefix}disp_format') or ''
            self.link_format = sec.get(f'{prefix}link_format') or ''
            self.img_format = sec.get(f'{prefix}img_format') or ''
            self.note = sec.get(f'{prefix}note') or ''
        else:
            self.id = sec.id or ''
            self.page_id = sec.page_id or ''
            self.display_order = sec.display_order or 0
            self.category = sec.category or ''
            self.flags = sec.flags or 0
            self.name = sec.name or ''
            self.columns = sec.columns or 0
            self.start = sec.start or 0
            self.pic_dir = sec.pic_dir or ''
            self.disp_format = sec.disp_format or ''
            self.link_format = sec.link_format or ''
            self.img_format = sec.img_format or ''
            self.note = sec.note or ''
        self.model_ids = []

    def __str__(self):
        return f'SecItem: {self.id}'

    @property
    def is_hidden(self):
        return bool(self.flags & config.FLAG_SECTION_HIDDEN)

    @property
    def default_ids(self):
        return bool(self.flags & config.FLAG_SECTION_DEFAULT_IDS)

    @property
    def no_firsts(self):
        return bool(self.flags & config.FLAG_SECTION_NO_FIRSTS)

    @property
    def show_ids(self):
        return bool(self.flags & config.FLAG_SECTION_SHOW_IDS)

    @property
    def hide_image(self):
        return bool(self.flags & config.FLAG_SECTION_HIDE_IMAGE)

    @property
    def group_singles(self):
        return bool(self.flags & config.FLAG_SECTION_GROUP_SINGLES)


class LineItem(object):

    def __init__(self, mod):
        if isinstance(mod, dict):
            self.man = ManItem(mod)
            self.var = VarItem(mod)
            self.pack = PackItem(mod)
            self.pack_model = PackModelItem(mod)
            self.pub = PubItem(mod)
            self.page = PageItem(mod)
            self.id = mod['lineup_model.id']
            self.base_id = mod['lineup_model.base_id']
            self.mod_id = mod['lineup_model.mod_id']
            self.sub_id = mod['lineup_model.sub_id']
            self.number = mod['lineup_model.number']
            self.display_order = mod['lineup_model.display_order'] or 0
            self.flags = mod['lineup_model.flags']
            self.style_id = mod['lineup_model.style_id']
            self.region = mod['lineup_model.region']
            self.year = mod['lineup_model.year']
            self.name = mod['lineup_model.name']
            self.subname = mod['lineup_model.subname']
            self.page_id = mod['lineup_model.page_id']
            self.vs = VSItem(mod)
        else:
            self.man = ManItem(mod.man)
            self.var = VarItem(mod.var)
            self.pack = PackItem(mod.pack)
            self.pack_model = PackModelItem(mod.pack_model)
            self.pub = PubItem(mod.pub)
            self.page = PageItem(mod.page)
            self.id = mod.id
            self.base_id = mod.base_id
            self.mod_id = mod.mod_id
            self.sub_id = mod.sub_id
            self.number = mod.number
            self.display_order = mod.display_order or 0
            self.flags = mod.flags
            self.style_id = mod.style_id
            self.region = mod.region
            self.year = mod.year
            self.name = mod.name
            self.subname = mod.subname
            self.page_id = mod.page_id
            self.vs = VSItem(mod.vs)
        self.additional = ''
        self.also = {}
        self.cvarlist = []
        self.no_casting = False
        self.no_variation = False
        self.not_made = bool(self.flags & config.FLAG_MODEL_NOT_MADE)
        self.pdir = ''
        self.picture_only = False
        self.show_vars = False
        self.subnames = []

    def __str__(self):
        return f'LineItem: {self.id} ({self.year}.{self.region}.{self.number})'

    def slurp(self, slurp_d):
        for k, v in slurp_d.items():
            setattr(self, k, v)

    def uses_variations(self):
        return self.man.model_type in ['AC', 'ET', 'KS', 'RW', 'SB', 'SF', 'BR', 'YY', 'CH']  # 'MP'?


d_re = re.compile(r'%\d*d')


class MatItem(object):

    def __init__(self, mat, sec=None):
        if not sec and 'section.id' in mat:
            sec = SecItem(mat)
        if 'page_info.id' in mat:
            self.page_info = PageItem(mat)
        self.disp_format = sec.disp_format
        is_num_id = d_re.search(sec.disp_format) or d_re.search(sec.link_format) or d_re.search(sec.img_format)
        self.pdir = sec.pic_dir

        prefix = 'matrix_model.' if 'matrix_model.id' in mat else ''
        self.id = mat.get(f'{prefix}id') or ''
        self.mod_id = mat.get(f'{prefix}mod_id') or ''
        self.sub_id = mat.get(f'{prefix}sub_id') or ''
        self.section_id = mat.get(f'{prefix}section_id') or sec.id
        self.display_order = mat.get(f'{prefix}display_order') or 0
        self.page_id = mat.get(f'{prefix}page_id') or 'matrix'
        self.range_id = mat.get(f'{prefix}range_id') or ''
        self.flags = mat.get(f'{prefix}flags') or 0
        self.shown_id = mat.get(f'{prefix}shown_id') or ''
        self.name = mat.get(f'{prefix}name') or ''
        self.subname = mat.get(f'{prefix}subname') or ''
        self.subnames = self.subname.split(';') if self.subname else []
        self.model_type = mat.get('base_id.model_type') or ''
        self.pack = PackItem(mat)

        self.description = []
        self.var = VarItem(mat)
        if desc := mat.get(f'{prefix}description'):
            self.description.extend(desc.split(';'))
        if self.var.text_description:
            self.description.append(self.var.text_description)
        self.description = [x for x in self.description if x]
        self.descriptions = []
        self.disp_id = self.image = self.link = ''
        # currently this formats all the variations then just uses one.  needs to collate the variations then
        # call format_image_* with that.
        if is_num_id:
            self.range_id = int(self.range_id) if self.range_id else 0
        if self.range_id and sec.disp_format:
            self.disp_id = self.range_id
        if self.range_id and sec.link_format:
            self.link = (useful.clean_name(sec.link_format % self.range_id, '/') if '%' in sec.link_format else
                         useful.clean_name(sec.link_format, '/'))

        self.vs = VSItem(mat)
        subname_id = mbdata.reverse_regions.get(self.subname, '')
        self.sub_id_matches = not (subname_id and self.vs.sec_id and subname_id != self.vs.sec_id)
        self.displayed_id = '&nbsp;'
        self.style_id = 'wh'
        self.section = sec

    def __str__(self):
        return f'MatItem: {self.id} ({self.page_id}.{self.section_id}.{self.range_id})'

    def __repr__(self):
        return str(self.__dict__)

    @property
    def is_no_variation(self):
        return bool(self.flags & config.FLAG_MODEL_NO_VARIATION)

    @property
    def show_all_variations(self):
        return bool(self.flags & config.FLAG_MODEL_SHOW_ALL_VARIATIONS)

    @property
    def no_id(self):
        return bool(self.flags & config.FLAG_MODEL_NO_ID)

    @property
    def not_made(self):
        return bool(self.flags & config.FLAG_MODEL_NOT_MADE)


class LinkLineItem(object):

    def __init__(self, ll):
        if isinstance(ll, dict):
            prefix = 'link_line.' if 'link_line.id' in ll else ''
            self.id = ll[f'{prefix}id']
            self.page_id = ll.get(f'{prefix}page_id') or ''
            self.section_id = ll.get(f'{prefix}section_id') or ''
            self.display_order = ll.get(f'{prefix}display_order') or 0
            self.flags = ll.get(f'{prefix}flags') or 0
            self.associated_link = ll.get(f'{prefix}associated_link') or ''
            self.last_status = ll.get(f'{prefix}last_status') or ''
            self.link_type = ll.get(f'{prefix}link_type') or ''
            self.country = ll.get(f'{prefix}country') or ''
            self.url = ll.get(f'{prefix}url') or ''
            self.name = ll.get(f'{prefix}name') or ''
            self.description = ll.get(f'{prefix}description') or ''
            self.note = ll.get(f'{prefix}note') or ''
        else:
            self.id = ll.id
            self.page_id = ll.page_id
            self.section_id = ll.section_id
            self.display_order = ll.display_order or 0
            self.flags = ll.flags or 0
            self.associated_link = ll.associated_link
            self.last_status = ll.last_status
            self.link_type = ll.link_type
            self.country = ll.country
            self.url = ll.url
            self.name = ll.name
            self.description = ll.description
            self.note = ll.note

    def __str__(self):
        return f'LinkLineItem: {self.id}'

    @property
    def associable(self):
        return bool(self.flags & config.FLAG_LINK_LINE_ASSOCIABLE)

    @property
    def disabled(self):
        return bool(self.flags & config.FLAG_LINK_LINE_DISABLED)

    @property
    def format_large(self):
        return bool(self.flags & config.FLAG_LINK_LINE_FORMAT_LARGE)

    @property
    def hidden(self):
        return bool(self.flags & config.FLAG_LINK_LINE_HIDDEN)

    @property
    def indented(self):
        return bool(self.flags & config.FLAG_LINK_LINE_INDENTED)

    @property
    def new(self):
        return bool(self.flags & config.FLAG_LINK_LINE_NEW)

    @property
    def not_verifiable(self):
        return bool(self.flags & config.FLAG_LINK_LINE_NOT_VERIFIABLE)

    @property
    def paypal(self):
        return bool(self.flags & config.FLAG_LINK_LINE_PAYPAL)

    @property
    def reciprocal(self):
        return bool(self.flags & config.FLAG_LINK_LINE_RECIPROCAL)

    @property
    def raw_html(self):
        return bool(self.flags & config.FLAG_LINK_LINE_RAW_HTML)

    @property
    def bullet(self):
        match self.link_type:
            case 'b':
                return '<i class="fas fa-exclamation-triangle red"></i>'
            case 'f':
                return '<i class="fas fa-folder"></i>'
            case 'l':
                return '<span class="blue">&#x25cf;</span>'
            case 'n':
                return '&nbsp;'
            case 's':
                return '<i class="fas fa-star"></i>'
            case 'x':
                return '&#x1F5D1;'
        return ''

    @property
    def desc(self):
        return self.description.split('|')


class BoxTypeItem(object):

    def __init__(self, bt):
        prefix = 'box_type.' if 'box_type.id' in bt else ''
        self.id = bt[f'{prefix}id']
        self.mod_id = bt[f'{prefix}mod_id']
        self.section_id = bt[f'{prefix}section_id']
        self.box_type = bt[f'{prefix}box_type']
        self.pic_id = bt[f'{prefix}pic_id']
        self.box_size = bt[f'{prefix}box_size']
        self.year = bt[f'{prefix}year']
        self.additional_text = bt[f'{prefix}additional_text']
        self.bottom = bt[f'{prefix}bottom']
        self.sides = bt[f'{prefix}sides']
        self.end_flap = bt[f'{prefix}end_flap']
        self.model_name = bt[f'{prefix}model_name']
        self.notes = bt[f'{prefix}notes']

    def get(self, k, v=''):
        return getattr(self, k, v)
