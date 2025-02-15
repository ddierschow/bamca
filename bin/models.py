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
            # EVERYBODY has a base_id.  After that, we differentiate.
            self.id = mod['base_id.id']
            self.visual_id = self.default_id(self.id)
            self.first_year = mod['base_id.first_year']
            self.flags = mod['base_id.flags']
            self.made = not (self.flags & config.FLAG_MODEL_NOT_MADE)
            self.model_type = mod['base_id.model_type']
            self.rawname = mod['base_id.rawname']
            self.name = self.rawname.replace(';', ' ')
            self.description = mod['base_id.description']

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
