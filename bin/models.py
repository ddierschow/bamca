import re

import config
import mbdata
import tables

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
        self.made = False
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
        self.subname = ''
        self.unlicensed = '?'
        self.variation_digits = 2
        self.vehicle_type = ''
        self.visual_id = ''

        if isinstance(mod, dict):
            if 'link' in mod:
                self.slurp(mod)

            else:
                # EVERYBODY has a base_id.  After that, we differentiate.
                self.id = mod['base_id.id'] or ''
                self.visual_id = self.default_id(self.id)
                self.first_year = mod['base_id.first_year'] or ''
                self.flags = mod['base_id.flags'] or 0
                self.made = not (self.flags & config.FLAG_MODEL_NOT_MADE)
                self.model_type = mod['base_id.model_type'] or ''
                self.rawname = mod['base_id.rawname'] or ''
                self.name = self.rawname.replace(';', ' ')
                self.description = mod['base_id.description'] or ''

                if mod.get('publication.id'):
                    self.country = mod['publication.country']
                    self.section_id = mod['publication.section_id']
                    self.isbn = mod['publication.isbn']
                elif mod.get('pack.id'):
                    self.made = True
                    self.subname = mod.get('pack_model.subname', '')
                    self.visual_id = self.default_id(self.id)
                    self.link = "packs.cgi?id"
                    self.vehicle_type = ''
                elif mod.get('id') or mod.get('casting.id'):
                    self.scale = mod['casting.scale']
                    self.vehicle_type = mod['casting.vehicle_type']
                    self.country = mod['casting.country']
                    self.make = mod['casting.make']
                    self.box_styles = mod.get('casting.box_styles', '')
                    self.notes = mod.get('casting.notes', '')
                    self.section_id = mod['casting.section_id']
                    self.format_description = mod.get('casting.format_description', '')
                    self.format_body = mod.get('casting.format_body', '')
                    self.format_interior = mod.get('casting.format_interior', '')
                    self.format_windows = mod.get('casting.format_windows', '')
                    self.format_base = mod.get('casting.format_base', '')
                    self.format_wheels = mod.get('casting.format_wheels', '')
                    self.format_with = mod.get('casting.format_with', '')
                    self.variation_digits = mod.get('casting.variation_digits', '')
                    self.format_text = mod.get('casting.format_text', '')
                if mod.get('alias.id'):
                    self.section_id = mod['alias.section_id']
                    self.ref_id = mod['alias.ref_id']
                    if mod.get('alias.first_year'):
                        self.first_year = mod['alias.first_year']
                    self.id = mod['alias.id']
                    self.description += ';same as ' + self.ref_id
                    # self.vehicle_type = mod['vehicle_type'] or ''

        elif isinstance(mod, tables.Result):
            # EVERYBODY has a base_id.  After that, we differentiate.
            self.id = mod.base_id.id
            self.visual_id = self.default_id(self.id)
            self.first_year = mod.base_id.first_year
            self.flags = mod.base_id.flags
            self.made = not (self.flags & config.FLAG_MODEL_NOT_MADE)
            self.model_type = mod.base_id.model_type
            self.rawname = mod.base_id.rawname
            self.name = self.rawname.replace(';', ' ')
            self.description = mod.base_id.description

            if mod.get('publication', {}).get('id'):
                self.country = mod.publication.country
                self.section_id = mod.publication.section_id
                self.isbn = mod.publication.isbn
            elif mod.get('pack', {}).get('id'):
                self.made = True
                self.subname = mod.pack_model.subname
                self.visual_id = self.default_id(self.id)
                self.link = "packs.cgi?id"
                self.vehicle_type = ''
            elif mod.get('id') or mod.get('casting', {}).get('id'):
                self.scale = mod.scale
                self.vehicle_type = mod.vehicle_type
                self.country = mod.country
                self.make = mod.make
                self.box_styles = mod.get('box_styles', '')
                self.notes = mod.get('notes', '')
                self.section_id = mod.section_id
                self.format_description = mod.get('format_description', '')
                self.format_body = mod.get('format_body', '')
                self.format_interior = mod.get('format_interior', '')
                self.format_windows = mod.get('format_windows', '')
                self.format_base = mod.get('format_base', '')
                self.format_wheels = mod.get('format_wheels', '')
                self.format_with = mod.get('format_with', '')
                self.variation_digits = mod.variation_digits
                self.format_text = mod.get('format_text', '')
            if mod.get('alias.id'):
                self.section_id = mod['alias.section_id']
                self.ref_id = mod['alias.ref_id']
                if mod['first_year']:
                    self.first_year = mod['first_year']
                self.id = mod['id']
                self.description += ';same as ' + self.ref_id
                self.vehicle_type = mod['vehicle_type'] or ''

        self.unlicensed = '-' if self.make == 'unl' else '?' if not self.make else self.make
        self.casting_type = mbdata.model_types.get(self.model_type, 'Casting')
        self.descs = [x for x in self.description.split(';') if x]
        self.filename = self.id.lower()
        self.iconname = self.icon_name(self.rawname)
        self.linkid = self.id
        self.notmade = '' if self.made else '*'
        self.revised = self.flags & config.FLAG_MODEL_CASTING_REVISED != 0
        self.shortname = self.short_name(self.rawname)
        self.count = mod.get('count', 0)

    @staticmethod
    def default_id(id):
        if id_m := id_re.match(id):
            return id_m.group('a').upper() + '-' + id_m.group('d')
        return id_m

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


class VarItem(object):

    def __init__(self, mod):
        self.mod_id = mod.get('v.mod_id', '')
        self.var = mod.get('v.var', '')
        self.flags = mod.get('v.flags', '')
        self.text_description = mod.get('v.text_description', '')
        self.text_base = mod.get('v.text_base', '')
        self.text_body = mod.get('v.text_body', '')
        self.text_interior = mod.get('v.text_interior', '')
        self.text_wheels = mod.get('v.text_wheels', '')
        self.text_windows = mod.get('v.text_windows', '')
        self.text_with = mod.get('v.text_with', '')
        self.text_text = mod.get('v.text_text', '')
        self.base = mod.get('v.base', '')
        self.body = mod.get('v.body', '')
        self.deco = mod.get('v.deco', '')
        self.deco_type = mod.get('v.deco_type', '')
        self.interior = mod.get('v.interior', '')
        self.wheels = mod.get('v.wheels', '')
        self.windows = mod.get('v.windows', '')
        self.manufacture = mod.get('v.manufacture', '')
        self.additional_text = mod.get('v.additional_text', '')
        self.base_name = mod.get('v.base_name', '')
        self.base_number = mod.get('v.base_number', '')
        self.base_scale = mod.get('v.base_scale', '')
        self.tool_id = mod.get('v.tool_id', '')
        self.production_id = mod.get('v.production_id', '')
        self.copyright = mod.get('v.copyright', '')
        self.company_name = mod.get('v.company_name', '')
        self.logo_type = mod.get('v.logo_type', '')
        self.base_reads = mod.get('v.base_reads', '')
        self.area = mod.get('v.area', '')
        self.date = mod.get('v.date', '')
        self.note = mod.get('v.note', '')
        self.picture_id = mod.get('v.picture_id', '')
        self.imported = mod.get('v.imported', '')
        self.imported_from = mod.get('v.imported_from', '')
        self.imported_var = mod.get('v.imported_var', '')
        self.category = mod.get('v.category', '')
        self.variation_type = mod.get('v.variation_type', '')
        self.ref_id = mod.get('vs.ref_id', '')
        self.sec_id = mod.get('vs.sec_id', '')
        self.ran_id = mod.get('vs.ran_id', '')
        self.vs_cat = mod.get('vs.category', '')

    def clear(self):
        self.text_description = ''
        self.picture_id = ''
        self.var = ''
        self.ref_id = ''
        self.sec_id = ''
        self.ran_id = ''


class PackItem(object):

    def __init__(self, mod):
        self.id = mod.get('pack.id', '')
        self.var = mod.get('pack.var', '')
        self.page_id = mod.get('pack.page_id', '')
        self.section_id = mod.get('pack.section_id', '')
        self.name = mod.get('pack.name', '')
        self.year = mod.get('pack.year', '')
        self.end_year = mod.get('pack.end_year', '')
        self.layout = mod.get('pack.layout', '')
        self.region = mod.get('pack.region', '')
        self.product_code = mod.get('pack.product_code', '')
        self.material = mod.get('pack.material', '')
        self.country = mod.get('pack.country', '')
        self.note = mod.get('pack.note', '')

        self.mod_id = mod.get('pack_model.mod_id', '')
        self.flags = mod.get('pack_model.flags', '')
        self.style_id = mod.get('pack_model.style_id', '')
        self.display_order = mod.get('pack_model.display_order', '')
        self.subname = mod.get('pack_model.subname', '')


class PubItem(object):

    def __init__(self, mod):
        self.id = mod.get('publication.id', '')
        self.country = mod.get('publication.country', '')
        self.section_id = mod.get('publication.section_id', '')
        self.isbn = mod.get('publication.isbn', '')


class PageItem(object):

    def __init__(self, mod):
        self.id = mod.get('page_info.id', '')
        self.flags = mod.get('page_info.flags', 0)
        self.format_type = mod.get('page_info.format_type', '')
        self.style_id = mod.get('page_info.style_id', '')
        self.title = mod.get('page_info.title', '')
        self.pic_dir = mod.get('page_info.pic_dir', '')
        self.tail = mod.get('page_info.tail', '')
        self.description = mod.get('page_info.description', '')
        self.note = mod.get('page_info.note', '')


class LineItem(object):

    def __init__(self, mod):
        self.man = ManItem(mod)
        self.var = VarItem(mod)
        self.pack = PackItem(mod)
        self.pub = PubItem(mod)
        self.page = PageItem(mod)
        self.id = mod['lineup_model.id']
        self.base_id = mod['lineup_model.base_id']
        self.mod_id = mod['lineup_model.mod_id']
        self.number = mod['lineup_model.number']
        self.display_order = mod['lineup_model.display_order']
        self.flags = mod['lineup_model.flags']
        self.style_id = mod['lineup_model.style_id']
        self.picture_id = mod['lineup_model.picture_id']
        self.region = mod['lineup_model.region']
        self.year = mod['lineup_model.year']
        self.name = mod['lineup_model.name']
        self.subname = mod['lineup_model.subname']
        self.page_id = mod['lineup_model.page_id']
        self.additional = ''
        self.also = {}
        self.cvarlist = []
        self.no_casting = False
        self.no_variation = False
        self.not_made = False
        self.pdir = ''
        self.picture_only = False
        self.show_vars = False
        self.subnames = []

    def slurp(self, slurp_d):
        for k, v in slurp_d.items():
            setattr(self, k, v)
