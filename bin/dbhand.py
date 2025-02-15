#!/usr/local/bin/python

import copy
import datetime
from functools import reduce
import re
import time

import config
import dbintf
import mbdata
import models
import tables
import useful

id_re = re.compile(r'''(?P<a>[a-zA-Z]*)(?P<d>\d*)''')


class DBHandler(object):
    table_data = tables.table_data

    def __init__(self, config, user_id, db_logger, verbose):
        self.dbi = dbintf.DB(config, user_id, db_logger, verbose)
        if not self.dbi:
            raise 'DB connect failed'

    def set_config(self, config):
        self.dbi.set_config(config)

    def __repr__(self):
        return "'<dbhand.DBHandler instance>'"

    def __str__(self):
        return "'<dbhand.DBHandler instance>'"

    def error_report(self):
        import pprint
        return (pprint.pformat(self.__dict__, indent=2, width=132) + '\ndbi = ' +
                pprint.pformat(self.dbi.__dict__, indent=2, width=132))

    def set_verbose(self, flag):
        self.dbi.verbose = flag

    def escape_string(self, s):
        return self.dbi.escape_string(s)

    def make_id(self, table, values, prefix=''):
        return {x: values.get(prefix + x, '') for x in self.get_table_data(table).id}

    def make_values(self, table, values, prefix=''):
        return {x: values.get(prefix + x, values.get(x, '')) for x in self.get_table_data(table).columns}

    def form_make_values(self, table, form, prefix=''):
        return {x: form.get_str(prefix + x, '') for x in self.get_table_data(table).columns}

    def get_table_data(self, table):
        return self.table_data.get(table)

    def get_editor_link(self, table, args):
        table_data = self.get_table_data(table)
        url = f'/cgi-bin/editor.cgi?table={table}'
        if table_data:
            for key, arg in args.items():
                if key in table_data.columns:
                    url += f'&{key}={arg}'
        return url

    def table_cols(self, table):
        return [f'{table}.{x}' for x in self.get_table_data(table).columns]

    def make_where(self, form, cols=None, prefix=""):
        wheres = list()
        if isinstance(form, dict):
            for col in cols or form:
                if prefix + col in form:
                    wheres.append(col + "='" + str(form.get(prefix + col, '')) + "'")
        elif isinstance(form, list):
            wheres.extend(form)
        elif form:
            wheres.append(form)
        return ' and '.join(wheres)

    def raw_execute(self, query, args=None, logargs=True, tag='RawExecute'):
        ret = self.dbi.execute(query, args=args, logargs=logargs, tag=tag)
        self.dbi.commit(tag=tag)
        return ret

    def make_columns(self, tab='', name='', tabs=[], extras=False):
        if tabs:
            return reduce(lambda x, y: x + y, [self.make_columns(x) for x in tabs], list())
        name = name if name else tab

        table_data = self.get_table_data(tab)
        if not table_data:
            raise ValueError(f'unknown table: {tab}')
        return [f'{name}.{x}' for x in table_data.columns + (table_data.extra_columns if extras else [])]

    def make_tablename(self, tab):
        tab, name = tab.split(' ', 1) if ' ' in tab else (tab, '')
        table_data = self.get_table_data(tab)
        if not table_data:
            raise ValueError(f'unknown table: {tab}')
        db = table_data.db
        if db != tables.home_db:
            tab = f'{db}.{tab}'
        return f'{tab} {name}' if name else tab

    def fetch(self, table_name, args=None, left_joins=None, columns=None, extras=False, where=None, group=None,
              order=None, one=False, distinct=False, limit=None, logargs=True, tag='Fetch', verbose=False):
        # useful.write_comment('fetch', 't', table_name, 'a', args, 'l', left_joins, 'c', columns, 'e', extras,
        #                      'w', where, 'g', group, 'o', order, 'd', distinct, tag)
        if isinstance(table_name, str):
            table_name = table_name.split(',')
        if not columns:
            columns = list()
            for tab in table_name:
                if ' ' in tab:
                    tab, name = tab.split(' ', 1)
                    columns.extend(self.make_columns(tab, name, extras=extras))
                elif self.get_table_data(tab).db != tables.home_db:
                    columns.extend(self.make_columns(tab, tab, extras=extras))
                else:
                    columns.extend(self.make_columns(tab, extras=extras))
        elif isinstance(columns, str):
            columns = columns.split(',')
        if isinstance(where, list):
            where = ' and '.join(where)
        elif isinstance(where, dict):
            where = self.make_where(where)
        table_name = [self.make_tablename(x) for x in table_name]
        table_name = ','.join(table_name)
        if left_joins:
            table_name = f'({table_name})'
            for lj in left_joins:
                # do make_tablename on lj[0]
                table_name += f' left join {lj[0]} on ({lj[1]})'
                j_tab = lj[0][:lj[0].find(' as ')] if ' as ' in lj[0] else lj[0]
                j_name = lj[0][lj[0].find(' as ') + 4:] if ' as ' in lj[0] else lj[0]
                columns.extend([f'{j_name}.{x}' for x in self.get_table_data(j_tab).columns])
        outcols = [x if ' as ' not in x else x[x.find(' as ') + 4:] for x in columns]
        if limit:
            if isinstance(limit, int):
                limit = str(limit)
            elif isinstance(limit, str):
                pass
            elif len(limit) == 1:
                limit = str(limit[0])
            elif limit[1] == -1:
                limit = '{},{}'.format(limit[0], 99999999)
            else:
                limit = '{},{}'.format(*limit)
        results = self.dbi.select(table_name, cols=columns, args=args, where=where, group=group, order=order,
                                  distinct=distinct, limit=limit, logargs=logargs, tag=tag, verbose=verbose,
                                  outcols=outcols)
        if one:
            return results[0] if results else None
        return results

    def describe_dict(self, table):
        def do_field(f):
            ft = f['type']
            f['length'] = int(ft[ft.index('(') + 1:ft.index(')')]) if '(' in ft else 16
            return f

        return {x['field']: do_field(x) for x in self.describe(table)}

    def describe(self, table):
        table = self.make_tablename(table)
        return self.dbi.describe(table)

    def columns(self, table):
        return [x['field'] for x in self.describe(table)]

    def copykeys(self, table, source):
        return {f'{table}.{col}': source.get(f'{table}.{col}') for col in self.get_table_data(table).columns}

    def depref(self, tables, results):
        if isinstance(tables, str):
            tables = tables.split(',')
        if results is None:
            # Aw, come on.
            return None
        if results:
            if isinstance(results, dict):
                for table in tables:
                    keys = list(results.keys())
                    for key in keys:
                        if key.startswith(table + '.'):
                            if not results.get(key[len(table) + 1:]):
                                results[key[len(table) + 1:]] = results[key]
                            if results[key[len(table) + 1:]] == results[key]:
                                del results[key]
            else:
                for result in results:
                    self.depref(tables, result)
        return results

    def increment(self, table_name, values=None, where=None, tag='Increment', verbose=False):
        table_name = self.make_tablename(table_name)
        values = {x: x + '+1' for x in values}
        return self.dbi.updateraw(table_name, values, where, tag=tag, verbose=verbose)

    def write(self, table_name, values=None, where=None, newonly=False, modonly=False, args=None, logargs=True,
              tag='Write', verbose=False):
        table_name = self.make_tablename(table_name)
        if newonly:
            return self.dbi.insert(table_name, values, args, logargs, tag=tag, verbose=verbose)
        elif modonly:
            return self.dbi.update(table_name, values, self.make_where(where), args, logargs, tag=tag, verbose=verbose)
        else:
            return self.dbi.insert_or_update(table_name, values, args, logargs, tag=tag, verbose=verbose)

    def delete(self, table, where=None, tag='Delete', verbose=None):
        table = self.make_tablename(table)
        return self.dbi.remove(table, where, tag=tag, verbose=verbose)

    def update_flags(self, table_name, turn_on=0, turn_off=0, where=None, tag='UpdateFlags', verbose=False):
        table_name = self.make_tablename(table_name)
        # update table set flags = flags & ~turn_off | turn_on where
        return self.dbi.updateraw(
            table_name,
            {'flags': f'flags & ~{turn_off} | {turn_on}'}, where, tag=tag, verbose=verbose)

    # end dbi interface section

    # - page_info

    def fetch_page(self, id, verbose=False):
        return tables.Results('page_info', self.fetch('page_info', where={'id': id}, tag='Page', verbose=verbose)).first

    def fetch_pages(self, where, columns=None, group=None, order=None):
        return tables.Results('page_info', self.fetch('page_info', columns=columns, where=where, group=group,
                                                      order=order, tag='Pages'))

    def fetch_page_years(self):
        return tables.Results('page_info', self.fetch(
            'page_info,lineup_model',
            columns=self.make_columns('page_info') + ['max(lineup_model.number) as max_lineup_number'],
            where=['page_info.id=lineup_model.page_id', "page_info.id like 'year.%'"],
            group="page_info.id", tag='PageYears'))

    def insert_or_update_page(self, values, verbose=False):
        return self.write('page_info', values=values, tag='InsertOrUpdatePage', verbose=verbose)

    # - country

    def fetch_countries(self):
        return self.fetch('country', 'Country')

    # - section

    def fetch_section(self, sec_id=None, page_id=None, category=None, verbose=False):
        wheres = {}
        if sec_id:
            wheres['id'] = sec_id
        if page_id:
            wheres['page_id'] = page_id
        if category:
            wheres['category'] = category
        return tables.Results('section', self.fetch('section', where=wheres, tag='Section', verbose=verbose)).first

    def fetch_sections_by_page_type(self, page_type, sec_id=None, verbose=False):
        where = f'section.page_id=page_info.id and page_info.format_type="{page_type}"'
        if sec_id:
            where += f' and section.id="{sec_id}"'
        secs = self.fetch('section,page_info', where=where, order='display_order', tag='SectionByPageType',
                          verbose=verbose)
        return tables.Results('section', secs)

    def fetch_sections(self, where=None):
        return tables.Results('section', self.fetch('section', where=where, order='display_order', tag='Sections'))

    def insert_or_update_section(self, values, verbose=False):
        return self.write('section', values=values, tag='InsertOrUpdateSection', verbose=verbose)

    # - base_id

    def fetch_base_ids(self):
        return tables.Results('base_id', self.fetch('base_id', tag='BaseIDs'))

    def fetch_base_id(self, id):
        return tables.Results('base_id', self.fetch('base_id', where=f"id='{id}'", tag='BaseID')).first

    def fetch_base_id_model_types(self):
        return tables.Results('base_id', self.fetch('base_id', columns=['model_type'], group='model_type',
                              order='model_type', tag='BaseIdModelType'))

    def rename_base_id(self, old_mod_id, new_mod_id):
        tag = 'RenameBaseId'
        self.write('base_id', values={'id': new_mod_id}, where=f"id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('casting', values={'id': new_mod_id}, where=f"id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('pack', values={'id': new_mod_id}, where=f"id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('publication', values={'id': new_mod_id}, where=f"id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('alias', values={'ref_id': new_mod_id}, where=f"ref_id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('attribute', values={'mod_id': new_mod_id}, where=f"mod_id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('attribute_picture', values={'mod_id': new_mod_id}, where=f"mod_id='{old_mod_id}'",
                   modonly=True, tag=tag)
        self.write('casting_related', values={'model_id': new_mod_id}, where=f"model_id='{old_mod_id}'",
                   modonly=True, tag=tag)
        self.write('casting_related', values={'related_id': new_mod_id}, where=f"related_id='{old_mod_id}'",
                   modonly=True, tag=tag)
        self.write('detail', values={'mod_id': new_mod_id}, where=f"mod_id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('lineup_model', values={'mod_id': new_mod_id}, where=f"mod_id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('matrix_model', values={'mod_id': new_mod_id}, where=f"mod_id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('pack_model', values={'pack_id': new_mod_id}, where=f"pack_id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('pack_model', values={'mod_id': new_mod_id}, where=f"mod_id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('variation', values={'mod_id': new_mod_id}, where=f"mod_id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('variation_select', values={'mod_id': new_mod_id}, where=f"mod_id='{old_mod_id}'",
                   modonly=True, tag=tag)
        self.write('variation_select', values={'sec_id': new_mod_id}, where=f"sec_id='{old_mod_id}'",
                   modonly=True, tag=tag)
        self.write('box_type', values={'mod_id': new_mod_id}, where=f"mod_id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('link_line', values={'page_id': f'single.{new_mod_id}'}, where=f"page_id='single.{old_mod_id}'",
                   modonly=True, tag=tag)
        self.write('mbusa', values={'mod_id': new_mod_id}, where=f"mod_id='{old_mod_id}'", modonly=True, tag=tag)
        self.write('casting_make', values={'casting_id': new_mod_id}, where=f"casting_id='{old_mod_id}'",
                   modonly=True, tag=tag)

    def update_base_id(self, id, values):
        return self.write('base_id', values=self.make_values('base_id', values), where=f"id='{id}'", modonly=True,
                          tag='UpdateBaseId')

    def add_new_base_id(self, values, verbose=False):
        return self.write('base_id', values=self.make_values('base_id', values), newonly=True, tag="AddNewBaseId",
                          verbose=verbose)

    def delete_base_id(self, where):
        return self.delete('base_id', self.make_where(where))

    # - alias

    def fetch_alias(self, id, extras=False):
        alist = self.fetch("casting,alias,base_id", extras=True, where=[
            "casting.id=alias.ref_id", f"alias.id='{id}'", "casting.id=base_id.id"], one=True, tag='Alias')
        return alist

    def fetch_castings_by_box(self, series, style):
        wheres = ['casting.id=base_id.id']
        if series:
            wheres.append(f"base_id.model_type='{series}'")
        if style:
            wheres.append(f"box_type.box_type like '{style}%'")
        fet1 = self.fetch('box_type,casting,base_id', where=[
            'box_type.mod_id=casting.id'] + wheres, tag='CastingsByBox', verbose=0)

        # ljoins = [('alias', "base_id.id=alias.ref_id")]  # and alias.section_id != ''")]
        wheres = ['box_type.mod_id=alias.id', 'alias.ref_id=casting.id'] + wheres
        fet2 = self.fetch('box_type,alias,casting,base_id', where=wheres, tag='CastingsByBox', verbose=0)
        return fet1 + fet2

    def fetch_casting_by_alias(self, id, extras=False):
        manlist = self.fetch(
            'alias,casting,base_id', left_joins=[('vehicle_make', 'casting.make=vehicle_make.id')],
            where=f"casting.id=alias.ref_id and alias.id='{id}'", one=True, extras=extras, tag='CastingByAlias')
        if manlist:
            return self.modify_man_item(manlist)
        return {}

    def fetch_castings_by_alias(self, alias_id):
        wheres = ["base_id.id=casting.id", "casting.id=alias.ref_id", f"alias.id='{alias_id}'",
                  'casting.section_id=section.id', 'section.page_id=page_info.id', 'page_info.format_type="manno"']
        # "casting.id=alias.ref_id and alias.id=f'{id}'"
        return self.fetch('base_id,alias,casting,section,page_info', where=wheres,
                          left_joins=[('vehicle_make', 'casting.make=vehicle_make.id')], tag='CastingsByAlias')

    def fetch_aliases(self, ref_id=None, type_id=None, where=None):
        wheres = ["base_id.id=alias.ref_id"]
        # 'alias.section_id=section.id', 'section.page_id=page_info.id', 'page_info.format_type="manno"']
        left_joins = [
            # ('page_info', 'page_info.format_type="manno"'),
            # ('section', 'alias.section_id=section.id'),
            ('casting', "casting.id=base_id.id"),
            ('pack', "pack.id=base_id.id"),
        ]
        if ref_id:
            wheres.append(f"alias.ref_id='{ref_id}'")
        if type_id:
            wheres.append(f"alias.type='{type_id}'")
        if isinstance(where, list):
            wheres += where
        elif isinstance(where, str):
            wheres.append(where)
        return self.fetch("alias,base_id", where=wheres, left_joins=left_joins,
                          extras=True, tag='Aliases', verbose=False)

    def update_alias(self, pk, values):
        return self.write('alias', values=values, where=f"pk={pk}", modonly=True, tag='UpdateAlias')

    def add_alias(self, values):
        return self.write('alias', values=values, newonly=True, tag='AddAlias')

    def delete_alias(self, pk):
        return self.delete('alias', f'pk={pk}', tag='DeleteAlias')

    # - casting

    def fetch_casting_limits(self):
        # ranswer = fetch("select min(year), max(year), max(number) from lineup_model", $pif);
        wheres = ['base_id.id=casting.id']
        return self.fetch('casting,base_id', columns=['min(base_id.first_year)', 'max(base_id.first_year)'],
                          where=wheres, one=True, tag='CastingLimits', verbose=False)

    def fetch_casting_ids(self, section_id=None, tag='CastingIDs'):
        where = [f'section.id="{section_id}"'] if section_id else None
        return [x['casting.id'] for x in self.fetch('casting', where=where, tag='CastingIDs')]

    def fetch_casting_raw(self, mod_id, verbose=False, tag='CastingRaw'):
        cols = self.make_columns('casting', extras=True)
        recs = self.fetch('casting', columns=cols, where=f'id="{mod_id}"')
        return recs[0] if recs else None

    def fetch_casting(self, id, extras=False, verbose=False, tag='Casting'):
        verbose = True

        wheres = ['base_id.id=casting.id', f'casting.id="{id}"',
                  'casting.section_id=section.id', 'section.page_id="manno"']
        cols = (
            self.make_columns('base_id', extras=extras) +
            self.make_columns('casting', extras=extras) +
            self.make_columns('section', extras=extras) +
            ['(select count(*) from variation where variation.mod_id=casting.id) as vars'])
        manlist = self.fetch(
            "casting,base_id,section", left_joins=[("vehicle_make", "casting.make=vehicle_make.id")], columns=cols,
            where=wheres, extras=extras, one=True, tag=tag, verbose=verbose)
        if manlist:
            return self.modify_man_item(manlist)
        return {}

    def fetch_casting_list(self, section_id=None, page_id=None, where=None, verbose=False):
        wheres = ['base_id.id=casting.id', 'casting.section_id=section.id', 'section.page_id=page_info.id',
                  'page_info.format_type="manno"']
        if page_id:
            wheres.append(f'section.page_id="{page_id}"')
        if isinstance(where, list):
            wheres += where
        elif isinstance(where, str):
            wheres.append(where)
        if section_id:
            wheres.append(f'section.id="{section_id}"')
        return self.fetch('base_id,casting,section,page_info', where=wheres, extras=True, tag='CastingList',
                          verbose=verbose)

    def fetch_casting_list_by_make(self, make_id, section_id=None, page_id=None, where=None, verbose=False):
        verbose = True
        wheres = ['base_id.id=casting.id', 'casting.section_id=section.id', 'section.page_id=page_info.id',
                  'page_info.format_type="manno"']
        tables = 'base_id,casting,section,page_info'
        if not make_id:
            wheres.append('casting.id not in (select casting_id from casting_make)')
        else:
            wheres.append('casting.id=casting_make.casting_id')
            wheres.append(f'casting_make.make_id="{make_id}"')
            tables += ',casting_make'
        if page_id:
            wheres.append(f'section.page_id="{page_id}"')
        if where and isinstance(where, list):
            wheres += where
        elif where and isinstance(where, str):
            wheres.append(where)
        if section_id:
            wheres.append(f'section.id="{section_id}"')
        return self.fetch(tables, where=wheres, tag='CastingListMake', verbose=verbose)

    def fetch_casting_dict(self):
        return {x['id'].lower(): x for x in self.modify_man_items(self.fetch_casting_list())}

    def fetch_casting_by_id_or_alias(self, id):
        return self.fetch('base_id,casting', left_joins=[('alias', 'casting.id=alias.ref_id')],
                          where=f"base_id.id=casting.id and (casting.id='{id}' or alias.id='{id}')",
                          tag='CastingsByIdOrAlias')

    def write_casting(self, values, id, verbose=False):
        return self.write('casting', values=values, where=f'id="{id}"', modonly=True, tag='Casting',
                          verbose=verbose)

    def add_new_casting(self, values):
        return self.write('casting', values=values, newonly=True, tag='AddNewCasting', verbose=True)

    def short_name(self, name):
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

    def icon_name(self, name):
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

    def default_id(self, id):
        id_m = id_re.match(id)
        if not id_m:
            return id_m
        return id_m.group('a').upper() + '-' + id_m.group('d')

    def make_man_items(self, mods):
        return [self.make_man_item(mod) for mod in mods]

    def make_man_item(self, mod):
        return models.ManItem(mod)

    def modify_man_items(self, mods):
        return [self.modify_man_item(mod) for mod in mods]

    def modify_man_item(self, mod):
        mod = self.depref('casting,publication,base_id', mod)
        # mod = tables.Results('casting', [mod])
        # mods = mod.depref('publication,base_id')
        # mod = mods[0]
        mod.setdefault('make', '')
        mod['subname'] = mod.get('pack_model.subname', '')
        mod['link'] = "single.cgi?id"

        if mod.get('pack.id'):
            mod['name'] = mod.get('rawname', '').replace(';', ' ')
            mod['unlicensed'] = '?'
            mod.setdefault('description', '')
            mod['made'] = True
            mod['visual_id'] = self.default_id(mod['id'])
            mod['link'] = "packs.cgi?id"
            mod['vehicle_type'] = ''
        elif mod.get('id'):
            mod['name'] = mod.get('rawname', '').replace(';', ' ')
            mod['unlicensed'] = {'unl': '-', '': '?'}.get(mod['make'], ' ')
            mod.setdefault('description', '')
            mod['made'] = not (mod.get('flags', 0) & config.FLAG_MODEL_NOT_MADE)
            mod['visual_id'] = self.default_id(mod['id'])
        else:
            mod['id'] = mod['visual_id'] = ''
            mod['name'] = ''
            mod['unlicensed'] = '?'
            mod['description'] = ''
            mod['made'] = False
        mod['filename'] = mod['id'].lower()
        mod['notmade'] = '' if mod['made'] else '*'
        mod['revised'] = (((mod.get('flags', 0) if mod else 0) or 0) & config.FLAG_MODEL_CASTING_REVISED) != 0
        mod['linkid'] = mod.get('mod_id', mod.get('id'))
        mod['descs'] = [x for x in mod['description'].split(';') if x]
        mod['iconname'] = self.icon_name(mod.get('rawname', ''))
        mod['shortname'] = self.short_name(mod.get('rawname', ''))
        mod['casting_type'] = mbdata.model_types.get(mod.get('model_type', 'SF'), 'Casting')
        return mod

    def fetch_castings_by_category(self, page_id, category, verbose=False):
        wheres = [
            'base_id.id=casting.id',
            'base_id.id=variation_select.mod_id', f"variation_select.category='{category}'"
        ]
        columns = self.make_columns('base_id') + ['count(*)']
        return self.fetch('base_id,casting,variation_select', where=wheres, tag='CastingByCat', verbose=verbose,
                          columns=columns, group='base_id.id', order='base_id.id')

    def fetch_castings_by_plant(self, plant_name, verbose=False):
        columns = self.make_columns('base_id') + self.make_columns('casting') + ["count(*) as count"]
        wheres = ['base_id.id=casting.id', 'casting.id=variation.mod_id', f'variation.manufacture="{plant_name}"']
        return tables.Results(
            'casting', self.fetch('casting,base_id,variation', columns=columns, where=wheres,
                                  group='base_id.id', order='base_id.id', tag='CastingByPlant', verbose=verbose))

    def delete_casting(self, where):
        return self.delete('casting', self.make_where(where))

    # - casting_related

    def fetch_casting_relateds(self, mod_id=None, rel_id=None, section_id=None, flags=0, verbose=False):
        wheres = ["casting_related.related_id=base_id.id"]
        if mod_id:
            wheres.append(f"casting_related.model_id='{mod_id}'")
        if rel_id:
            wheres.append(f"casting_related.related_id='{rel_id}'")
        if section_id:
            wheres.append(f"casting_related.section_id='{section_id}'")
        if flags:
            wheres.append(f"casting_related.flags & {flags}")
        return self.fetch('casting_related,base_id', where=wheres, tag='CastingRelated', verbose=verbose)

    def fetch_casting_related_models(self, section_id=None):
        # select * from casting_related left join base_id as m on (casting_related.model_id=m.id) left join base_id
        # as r on (casting_related.related_id=r.id) where casting_related.model_id='MB952';
        wheres = []
        if section_id:
            wheres.append(f"casting_related.section_id='{section_id}'")
        left_joins = [("base_id as m", "casting_related.model_id=m.id")]
        left_joins += [("base_id as r", "casting_related.related_id=r.id")]
        return self.fetch('casting_related', where=wheres, left_joins=left_joins, tag='CastingRelateds',
                          verbose=False)
        # return self.fetch('casting_related,base_id m,base_id r', where="casting_related.related_id=r.id and
        # casting_related.model_id=m.id", tag='CastingRelateds', verbose=True)

    def fetch_casting_related_compares(self, section_id=None):
        columns = ['cr.id', 'cr.model_id', 'cr.related_id', 'cr.section_id', 'cr.picture_id', 'cr.description',
                   'c1.rawname', 'c2.rawname', 'c1.first_year', 'c2.first_year']
        where = 'cr.model_id=c1.id'
        if section_id:
            where += f" and cr.section_id='{section_id}'"
        table = 'casting_related cr'
        lj = [('base_id as c1', '(cr.model_id=c1.id)'), ('base_id as c2', '(cr.related_id=c2.id)')]
        return self.fetch(table, columns=columns, where=where, left_joins=lj, tag='CastingRelatedCompares')

    def fetch_casting_related_exists(self, mod_id, section_id):
        where = f"(model_id='{mod_id}' or related_id='{mod_id}') and section_id='{section_id}'"
        return len(self.fetch('casting_related', where=where, tag='CastingRelatedExists')) > 0

    def update_casting_related(self, val):
        if val['id']:
            # useful.write_message('upd', val, '<br>')
            self.write('casting_related', values=val, where=f"id={val['id']}", tag='UpdateCastingRelatedU',
                       verbose=True)
        else:
            if 'id' in val:
                del val['id']
            # useful.write_message('new', val, '<br>')
            # useful.write_message(self.write('casting_related', values=val, newonly=True, tag='UpdateCastingRelatedN',
            #                                   verbose=True))

    def add_casting_related(self, values):
        return self.write('casting_related', values=values, newonly=True, tag='AddCastingRelated', verbose=True)

    # - attribute

    def fetch_attributes_by_name(self, attr_name=None):
        where = f"attribute_name='{attr_name}'" if attr_name else ''
        return self.fetch('attribute', where=where, tag='AttributesByName')

    def fetch_attributes(self, mod_id, with_global=False):
        where = f"mod_id='{mod_id}'"
        if with_global:
            where += "or mod_id=''"
        return self.fetch('attribute', where=where, tag='Attributes')

    def fetch_attribute(self, id):
        return self.fetch('attribute', where=f"id='{id}'", tag='Attribute')

    def delete_attribute(self, where):
        self.delete('attribute', self.make_where(where))

    def update_attribute(self, values, id):
        self.write('attribute', values=values, where=self.make_where({'id': id}), modonly=True, tag='UpdateAttr')

    def clone_attributes(self, old_mod_id, new_mod_id):
        # insert into attribute (mod_id, attribute_name, definition, title, flags) select 'MB900', attribute_name,
        # definition, title, flags from attribute where mod_id='MB894';
        self.raw_execute(
            "insert into attribute (mod_id, attribute_name, definition, title, flags) "
            f"select '{new_mod_id}', attribute_name, definition, title, flags from attribute "
            f"where mod_id='{old_mod_id}'")

    def update_attribute_for_mod(self, mod_id, attr_name):
        rec = {"mod_id": mod_id, "attribute_name": attr_name,
               "title": attr_name.replace('_', ' ').title(), "definition": 'varchar(64)'}
        return self.write("attribute", values=rec, where={"mod_id": mod_id, "attribute_name": attr_name},
                          modonly=True, tag='UpdateAttrForMod')

    def insert_attribute(self, mod_id, attr_name):
        rec = {"mod_id": mod_id, "attribute_name": attr_name,
               "title": attr_name.replace('_', ' ').title(), "definition": 'varchar(64)'}
        return self.write("attribute", values=rec, newonly=True, tag='InsertAttr')

    # - attribute_picture

    def fetch_attribute_pictures(self, mod_id):
        ret = self.fetch('attribute_picture', left_joins=[('attribute', 'attribute.id=attribute_picture.attr_id ')],
                         where=f"attribute_picture.mod_id='{mod_id}'", tag='AttributePictures')
        return ret

    def fetch_attribute_pictures_by_type(self, attr_type, order=None):
        left_joins = [("base_id", "attribute_picture.mod_id=base_id.id")]
        left_joins += [("casting", "attribute_picture.mod_id=casting.id")]
        ret = self.fetch('attribute_picture',
                         where=f"attribute_picture.attr_type='{attr_type}'",
                         left_joins=left_joins, order=order,
                         tag='AttributePicturesByType')
        return ret

    def fetch_attribute_picture(self, id):
        return self.fetch('attribute_picture', where=f"id='{id}'", tag='AttrPic')

    def update_attribute_picture(self, values, id):
        return self.write('attribute_picture', values=values, where=self.make_where({'id': id}), modonly=True,
                          tag='UpdateAttrPic')

    def add_attribute_picture(self, values):
        return self.write('attribute_picture', values=values, newonly=True, tag='AddAttrPic')

    def delete_attribute_picture(self, rec_id):
        return self.delete('attribute_picture', where=f'id={rec_id}', tag='DeleteAttrPic')

    # - variation

    def fetch_variations_bare(self, mod_id=None):
        where = []
        if mod_id:
            where += [f"mod_id='{mod_id}'"]
        return self.fetch('variation', where=where, tag='VariationsBare')

    def fetch_variation_bare(self, mod_id, var_id):
        return self.fetch('variation', where=f"mod_id='{mod_id}' and var='{var_id}'", tag='VariationBare')

    def fetch_variations(self, mod_id, nodefaults=False):
        vsrecs = self.fetch('variation_select,category', where=[
            f"mod_id='{mod_id}'", "variation_select.category=category.id"])
        varrecs = self.fetch('variation', where=[f"variation.mod_id='{mod_id}'"], tag='Variations')
        # "variation.category=category.id",  # needs to be a left join
        detrecs = self.fetch_details(mod_id, nodefaults=nodefaults)
        for varrec in varrecs:
            detrec = detrecs.get(varrec['variation.var'], {})
            for key in detrec:
                if not varrec.get(f'variation.{key}'):
                    varrec[f'variation.{key}'] = detrec[key]
            varrec['vs'] = []
            for vs in vsrecs:
                if vs['variation_select.var_id'] == varrec['variation.var']:
                    varrec['vs'].append(vs)
        return varrecs

    def fetch_variations_by_date(self, dt, wildcard=False):
        dtq = f"variation.date like '{dt}%'" if wildcard else f"variation.date='{dt}'"
        varrecs = self.fetch('variation,base_id', where=f"base_id.id=variation.mod_id and {dtq}",
                             order='variation.mod_id, variation.var', tag='VariationsByDate')
        return varrecs

    def fetch_variation_dates(self, yr=None):
        where = f"date like '{yr}%'" if yr else ''
        return self.dbi.select('variation', cols=['date', 'count(*)'], where=where, group='date', order='date',
                               tag='VariationDates')

    def fetch_variation(self, mod_id, var):
        varrecs = self.fetch('variation', where=f"mod_id='{mod_id}' and var='{var}'", tag='Variation')
        if not varrecs:
            return None
        varrec = varrecs[0]
        detrecs = self.fetch_details(mod_id, var)
        for var_id in detrecs:
            if var == var_id:
                varrec.update(detrecs[var_id])
        return varrec

    def fetch_variation_deconstructed(self, mod_id, var_id, nodefaults=True):
        varrec = self.fetch('variation',
                            where=f"mod_id='{mod_id}' and var='{var_id}'", tag='VariationDeconstructed')
        detrecs = self.fetch_details(mod_id, var_id, nodefaults=nodefaults)
        if varrec:
            varrec[0]['vs'] = self.fetch('variation_select,category', where=[
                f"mod_id='{mod_id}'", f"var_id='{var_id}'", "variation_select.category=category.id"])
        return varrec, detrecs

    def fetch_variation_query(self, varsq, castingq=None, castinglist=None, codes=None):
        wheres = ['v.mod_id=casting.id', 'casting.id=base_id.id']
        if codes == 0:
            return list()  # ha-ha
        elif codes == 1:
            wheres.append(f'(v.flags & {config.FLAG_MODEL_CODE_2})=0')
        elif codes == 2:
            wheres.append(f'(v.flags & {config.FLAG_MODEL_CODE_2})!=0')
        args = list()
        cols = ['base_id.id', 'base_id.rawname', 'v.mod_id', 'v.var', 'v.date', 'v.text_description', 'v.text_base',
                'v.text_body', 'v.text_interior', 'v.text_wheels', 'v.text_windows', 'v.text_with', 'v.picture_id',
                'v.manufacture']
        for key in varsq:
            wheres.extend([f"v.{key} like %s" for x in varsq[key]])
            args.extend([f"%%{x}%%" for x in varsq[key]])
        if castingq:
            for key in castingq:
                wheres.extend([f"casting.{key} like %s" for x in castingq[key]])
                args.extend([f"%%{x}%%" for x in castingq[key]])
        if castinglist:
            idlist = [f'"{x}"' for x in castinglist]
            wheres.append(f"v.mod_id in ({','.join(idlist)})")
        # turn this into a fetch
        varrecs = self.dbi.select('variation v,casting,base_id', cols=cols, where=' and '.join(wheres), args=args,
                                  tag='VariationQuery')
        return varrecs

    def fetch_variation_query_by_id(self, mod_id, var_id):
        wheres = ['v.mod_id=casting.id', 'casting.id=base_id.id']
        cols = ['base_id.id', 'base_id.rawname', 'v.mod_id', 'v.var', 'v.date', 'v.text_description', 'v.text_base',
                'v.text_body', 'v.text_interior', 'v.text_wheels', 'v.text_windows', 'v.text_with', 'v.picture_id']
        wheres.append(f'casting.id="{mod_id}"')
        wheres.append(f'v.var="{var_id}"')
        # turn this into a fetch
        varrecs = self.dbi.select('variation v,casting,base_id', cols=cols, where=' and '.join(wheres),
                                  tag='VariationIdQuery')
        return varrecs

    def fetch_variation_by_select(self, mod_id=None, ref_id=None, sec_id="", ran_id="", category=None, verbose=False):
        cols = ['v.mod_id', 'v.text_description', 'v.picture_id', 'v.var', 'v.date',
                'vs.ref_id', 'vs.sec_id', 'vs.ran_id', 'vs.category', 'b.id', 'b.rawname']
        table = "variation_select vs"
        wheres = []
        if mod_id:
            wheres.append(f"vs.mod_id='{mod_id}'")
        if ref_id:
            wheres.append(f"vs.ref_id='{ref_id}'")
        if sec_id:
            if isinstance(sec_id, str):
                wheres.append(f"vs.sec_id='{sec_id}'")
            else:
                sec_id = ','.join([f"'{x}'" for x in sec_id])
                wheres.append(f"vs.sec_id in ({sec_id})")
            if ran_id:
                if isinstance(ran_id, str):
                    wheres.append(f"vs.ran_id='{ran_id}'")
                else:
                    ran_id = ','.join([f"'{x}'" for x in ran_id])
                    wheres.append(f"vs.ran_id in ({ran_id})")
        if category:
            wheres.append(f"vs.category='{category}'")
        table += " left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var left join base_id b on b.id=v.mod_id"
        # turn this into a fetch
        return self.dbi.select(table, cols=cols, where=' and '.join(wheres), verbose=verbose, tag='VarBySelect')

    def fetch_variations_by_plant(self, mod_id, plant, verbose=False):
        cols = ['v.mod_id', 'v.date', 'v.text_description', 'v.picture_id', 'v.var', 'v.manufacture']
        where = f"v.mod_id='{mod_id}' and v.manufacture='{plant}'"
        table = 'variation v'
        # turn this into a fetch
        return self.dbi.select(table, cols=cols, where=where, verbose=verbose, tag='VarByPlant')

    def fetch_variations_by_vs_category(self, category, verbose=False):
        # if the same cat appears in 2 vs's, this should only produce one var.  not sure it does right now.
        # dammit this is producing vs's, not vars.  gotta fix that.
        cols = ['v.mod_id', 'v.text_description', 'v.picture_id', 'v.var', 'v.date']
        cols += self.make_columns('variation_select', 'vs')
        cols += self.make_columns(tabs=['casting', 'base_id'])
        table = "variation_select vs"
        where = f"vs.category='{category}'"
        table += " left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var"
        table += " left join casting on vs.mod_id=casting.id"
        table += " left join base_id on vs.mod_id=base_id.id"
        # turn this into a fetch
        return self.dbi.select(table, cols=cols, where=where, verbose=verbose, tag='VarsByVSCat')

    def fetch_variations_by_category(self, category, verbose=False):
        # if the same cat appears in 2 vs's, this should only produce one var.  not sure it does right now.
        # dammit this is producing vs's, not vars.  gotta fix that.
        cols = ['mod_id', 'text_description', 'picture_id', 'var', 'date', 'category']
        cols += self.make_columns(tabs=['casting', 'base_id'])
        table = "variation v"
        where = f"category like '%{category}%'"
        table += " left join casting on v.mod_id=casting.id"
        table += " left join base_id on v.mod_id=base_id.id"
        # turn this into a fetch
        return self.dbi.select(table, cols=cols, where=where, verbose=verbose, tag='VarsByCat')

    def fetch_variation_files(self, mod_id):
        return self.fetch('variation', columns=['imported_from', 'mod_id'], group='imported_from',
                          order='imported_from', where=f"mod_id='{mod_id}'", tag='VariationFiles', verbose=False)

    def fetch_variation_plant_counts(self, mod_id):
        return self.fetch(
            'variation', columns=['manufacture', 'count(*) as count'],
            where=[f"mod_id='{mod_id}'"], group='manufacture', order='manufacture',
            tag='VarPlantCounts', verbose=False)

    def fetch_variation_base_names(self, mod_id):
        return self.fetch('variation', columns=['base_name'], where=[f"mod_id='{mod_id}'", "base_name != ''"],
                          distinct=True, tag='VarBaseNames', verbose=False)

    def insert_variation(self, mod_id, var_id, attributes={}, verbose=False):
        cols = self.get_table_data('variation').columns
        nvar = dict()
        for col in cols:
            nvar[col] = attributes.get(col, '')
        nvar['var'] = var_id
        nvar['mod_id'] = mod_id
        nvar['flags'] = 0
        nvar['imported'] = nvar['imported'] or None
        self.write('variation', values=nvar, newonly=True, tag='InsertVar', verbose=verbose)
        attribute_list = self.fetch_attributes(mod_id)
        for attr in attribute_list:
            det = {'var_id': nvar['var'], 'mod_id': mod_id, 'attr_id': attr['attribute.id'],
                   'description': attributes.get(attr['attribute.attribute_name'], '')}
            self.write('detail', values=det, newonly=True, verbose=verbose, tag='InsertVar')

    def update_variation_bare(self, var, verbose=False):
        where = {'mod_id': var.get('variation.mod_id', ''), 'var': var.get('variation.var', '')}
        return self.write('variation', values=var, where=self.make_where(where), modonly=True, tag="UpdateVarBare",
                          verbose=verbose)

    def update_variation(self, attributes, where, verbose=False):
        var_cols = self.get_table_data('variation').columns
        new_var = {x: attributes[x] for x in (set(attributes.keys()) & set(var_cols))}
        self.write('variation', values=new_var, where=self.make_where(where, var_cols), modonly=True, tag="UpdateVar",
                   verbose=verbose)
        attribute_list = self.fetch_attributes(where['mod_id'])
        for attr in attribute_list:
            if attr['attribute.attribute_name'] in attributes:
                det = {'var_id': attributes['var'], 'mod_id': where['mod_id'], 'attr_id': attr['attribute.id'],
                       'description': attributes.get(attr['attribute.attribute_name'], '')}
                self.write('detail', values=det, tag="UpdateVar", verbose=verbose)

    def delete_variation(self, where):
        self.delete('variation', where=self.make_where(where))

    # - variation_select

    def fetch_variation_selects_for_ref(self, ref_id, sec_id='', ran_id=''):
        wheres = [f"ref_id='{ref_id}'"]
        if sec_id:
            wheres.append(f"sec_id='{sec_id}'")
            if ran_id:
                wheres.append(f"ran_id='{ran_id}'")
        return self.fetch('variation_select', where=wheres, tag='VariationSelectsForRef')

    def fetch_variation_selects(self, mod_id=None, var_id=None, ref_id=None, sec_id=None, ran_id=None, category=None,
                                bare=False):
        wheres = []
        if mod_id:
            wheres.append(f"variation_select.mod_id='{mod_id}'")
            if var_id:
                wheres.append(f"variation_select.var_id='{var_id}'")
        if ref_id:
            wheres.append(f"variation_select.ref_id='{ref_id}'")
            if sec_id:
                wheres.append(f"variation_select.sec_id='{sec_id}'")
                if ran_id:
                    wheres.append(f"variation_select.ran_id='{ran_id}'")
        if category:
            wheres.append(f"variation_select.category='{category}'")
        left_joins = [("category", "variation_select.category=category.id")]
        if not bare:
            left_joins += [
                ("page_info", "variation_select.ref_id=page_info.id"),
                ("section", "variation_select.ref_id=section.page_id and variation_select.sec_id=section.id"),
                ("pack", "variation_select.sec_id=pack.id"),
                ("base_id", "pack.id=base_id.id"),
                ("lineup_model",
                 "variation_select.ref_id != '' and lineup_model.mod_id=variation_select.mod_id and "
                 "lineup_model.page_id=variation_select.ref_id"),
                ("publication", "variation_select.sec_id=publication.id"), ("base_id as pub", "pub.id=publication.id")]
        return tables.Results(
            'variation_select',
            self.fetch('variation_select', left_joins=left_joins, where=wheres, tag='VariationSelects', verbose=0))

    def fetch_variation_select_counts(self, mod_id=None, by_ref=False):
        wheres = ['variation_select.category=category.id']
        if mod_id:
            wheres += [f"variation_select.mod_id='{mod_id}'"]
        columns = ['variation_select.mod_id', 'variation_select.ref_id', 'variation_select.category', 'count(*)',
                   'category.name', 'category.flags']
        group_by = 'variation_select.category,variation_select.ref_id' if by_ref else 'variation_select.category'
        return self.fetch('variation_select,category', where=wheres, tag='VariationSelectCounts', verbose=0,
                          columns=columns, group=group_by, order='variation_select.category')

    def fetch_variation_select_refs(self):
        return self.fetch('variation_select', columns=['ref_id'], group='ref_id', tag='VarSelRefs')

    def fetch_variation_selects_by_ref(self, ref_id, sec_id=''):
        left_joins = [('variation',
                       'variation_select.mod_id=variation.mod_id and variation_select.var_id=variation.var'),
                      ('base_id', 'variation_select.mod_id=base_id.id')]
        where = [f'ref_id="{ref_id}"']
        if sec_id:
            where.append(f'sec_id="{sec_id}"')
        return self.fetch('variation_select', where=where, left_joins=left_joins, tag='VarSelByRef')

    # def update_variation_select(self):
    #     self.write('variation_select', values={'var_id': new_var_id}, where="var_id='%s' and mod_id='%s'" %
    #                                            (old_var_id, mod_id), modonly=True)

    def update_variation_selects_for_variation(self, mod_id, var_id, ref_ids):
        o_vs = self.depref('variation_select',
                           self.fetch('variation_select', where=f"mod_id='{mod_id}' and var_id='{var_id}'"))
        for ref_id in ref_ids:
            cat_id = sec_id = ran_id = ''
            if ref_id.find(':') >= 0:
                ref_id, cat_id = ref_id.split(':', 1)
            if ref_id.find('/') >= 0:
                ref_id, sec_id = ref_id.split('/', 1)
            sec_id, ran_id = sec_id.split('.') if '.' in sec_id else (sec_id, '')

            for vs in o_vs:
                if (vs['ref_id'] == ref_id and vs['sec_id'] == sec_id and vs['ran_id'] == ran_id and
                        vs['category'] == cat_id):
                    o_vs.remove(vs)
                    break
            else:
                values = {'mod_id': mod_id, 'var_id': var_id, 'ref_id': ref_id, 'sec_id': sec_id, 'ran_id': ran_id,
                          'category': cat_id}
                self.write('variation_select', values=values, newonly=True, verbose=1, tag='UpdateVSForV')
        for vs in o_vs:
            self.delete_variation_select(where=f'id={vs["id"]}')

    def update_variation_select(self, values):
        id = values.get('id', values.get('variation_select.id', ''))
        if id:
            return self.write('variation_select', values=values, where=f"id='{id}'", modonly=True, tag='UpdateVarSel')
        else:
            return self.write('variation_select', values=values, newonly=True, tag='UpdateVarSel')

    # this needs to be native sec_id.ran_id instead of sub_id
    def update_variation_select_subid(self, new_sub_id, ref_id, sub_id):
        sec_id, ran_id = sub_id.split('.') if '.' in sub_id else (sub_id, '')
        self.write('variation_select', values={'sec_id': sec_id, 'ran_id': ran_id},
                   where=f"ref_id='{ref_id}' and sec_id='{sec_id}' and ran_id='{ran_id}'",
                   modonly=True, tag='UpdateVarSelSubId')

    # some packs use ran_id and this might not work for them
    def update_variation_select_pack(self, pms, page_id=None, sec_id='', verbose=False):
        if not sec_id or not page_id:
            return
        self.delete('variation_select', where=f"ref_id='{page_id}' and sec_id='{sec_id}'", verbose=verbose)
        sec_id, ran_id = sec_id.split('.') if sec_id and '.' in sec_id else (sec_id, '')
        for pm in pms:
            for var_id in list(set([x for x in pm['var_id'].split('/') if x])):
                self.write('variation_select', values={
                    'mod_id': pm['mod_id'], 'var_id': var_id, 'ref_id': page_id, 'sec_id': pm['pack_id']},
                    newonly=True, tag='UpdateVarSelPack', verbose=verbose)

    # working through sub_id
    def update_variation_selects_for_ref(self, mod_vars, ref_id='', sec_id='', category=''):
        # mod vars is list of tuple (mod_id, var_id)
        old_vs = self.fetch_variation_selects_for_ref(ref_id=ref_id, sec_id=sec_id)
        for vs in old_vs:
            modvar = (vs['variation_select.mod_id'], vs['variation_select.var_id'])
            if modvar not in mod_vars:
                self.delete('variation_select', f"id={vs['variation_select.id']}")
            else:
                mod_vars.remove(modvar)
                if vs['variation_select.category'] != category:
                    self.write(
                        'variation_select',
                        values={'mod_id': vs['variation_select.mod_id'], 'var_id': vs['variation_select.var_id'],
                                'ref_id': ref_id, 'sec_id': sec_id, 'category': category},
                        where=f"id={vs['variation_select.id']}", tag='UVSFRcat')

        for modvar in mod_vars:
            self.write('variation_select', values={'mod_id': modvar[0], 'var_id': modvar[1], 'ref_id': ref_id,
                                                   'category': category}, newonly=True, tag='UVSFRcat2')

    def delete_variation_select(self, where):
        self.delete('variation_select', where=self.make_where(where))

    # - detail

    def fetch_details(self, mod_id, var_id=None, nodefaults=False):
        if nodefaults:
            commondetails = {}
        else:
            # turn this into a fetch
            commondetails = {x['attribute_name']: x['description'] for x in self.dbi.select(
                'detail, attribute',
                cols=['detail.mod_id', 'attr_id', 'description', 'attribute_name'],
                where=f"detail.mod_id='{mod_id}' and detail.attr_id=attribute.id and detail.var_id=''",
                tag='Details')}
        if var_id is not None:
            # turn this into a fetch
            details = self.dbi.select(
                'detail, attribute',
                cols=['detail.mod_id', 'var_id', 'attr_id', 'description', 'attribute_name'],
                where=f"detail.mod_id='{mod_id}' and detail.var_id='{var_id}' and detail.attr_id=attribute.id",
                tag='Details')
        else:
            # turn this into a fetch
            details = self.dbi.select(
                'detail, attribute',
                cols=['detail.mod_id', 'var_id', 'attr_id', 'description', 'attribute_name'],
                where=f"detail.mod_id='{mod_id}' and detail.attr_id=attribute.id", tag='Details')

        mvars = {}
        for det in details:
            mvars.setdefault(det['var_id'], copy.deepcopy(commondetails))
            mvars[det['var_id']][det['attribute_name']] = det['description']
        return mvars

    def update_detail(self, values, where, verbose=False):
        return self.write('detail', values=values, where=self.make_where(where), verbose=verbose, tag='UpdateDet')
        # modonly=True,

    def update_details(self, mod_id, var_id, details, verbose=False):
        for attr, val in details.items():
            where = {'mod_id': mod_id, 'var_id': var_id, 'attr_id': attr}
            det = {'description': val}
            det.update(where)
            self.update_detail(det, where=where)

    def add_or_update_detail(self, values, where, newonly=False, verbose=False):
        return self.write('detail', values=values, where=self.make_where(where), newonly=newonly, verbose=verbose,
                          tag='AddOrUpdateDet')

    def delete_detail(self, where):
        return self.delete('detail', where=self.make_where(where))

    # - vehicle_make

    def fetch_vehicle_makes(self, where='', verbose=False):
        return self.fetch('vehicle_make', where=where, tag='VehicleMakes', order='name', verbose=verbose)

    def fetch_vehicle_make(self, make_id, verbose=False):
        return self.fetch('vehicle_make', where={'id': make_id}, tag='VehicleMake', verbose=verbose, one=True)

    def update_vehicle_make(self, make_id, values, verbose=False):
        make = self.fetch_vehicle_make(make_id, verbose=verbose)
        if make:
            return self.write('vehicle_make', values=values, where=f"id='{make_id}'", modonly=True,
                              tag='UpdateVehicleMake', verbose=verbose)

    def add_vehicle_make(self, make_id, name, company=None, verbose=False):
        if not company:
            company = name
        rec = {
            'id': make_id,
            'name': name,
            'company_name': company,
            'flags': 1,
        }
        return self.write('vehicle_make', values=rec, newonly=True, tag='AddVehicleMake', verbose=verbose)

    # - casting_make

    def fetch_casting_makes(self, mod_id, verbose=False):
        wheres = [
            f'casting_make.casting_id="{mod_id}"',
        ]
        left_joins = [('vehicle_make', 'vehicle_make.id=casting_make.make_id')]
        return self.fetch('casting_make', where=wheres, left_joins=left_joins, tag='CastingMakes', verbose=verbose)

    def fetch_casting_makes_list(self, verbose=False):
        # left_joins = [('vehicle_make', 'vehicle_make.id=casting_make.make_id')]
        return self.fetch('casting_make', tag='CastingMakesList', verbose=verbose)

    def add_casting_make(self, mod_id, make_id, verbose=False):
        makes = self.fetch_casting_makes(mod_id, verbose=verbose)
        values = {'make_id': make_id, 'casting_id': mod_id, 'flags': 0 if makes else 2}
        return self.write('casting_make', values=values, newonly=True, tag='AddCastingMake', verbose=verbose)

    def update_casting_make(self, mod_id, make_id, verbose=False):
        makes = self.fetch_casting_makes(mod_id, verbose=verbose)
        values = {'make_id': make_id, 'casting_id': mod_id, 'flags': 0 if makes else 2}
        return self.write('casting_make', values=values, tag='UpdateCastingMake', verbose=verbose)

    def delete_casting_make(self, mod_id, make_id=None, verbose=False):
        where = {'casting_id': mod_id}
        if make_id:
            where['make_id'] = make_id
        return self.delete('casting_make', self.make_where(where), tag='DeleteCastingMake', verbose=verbose)

    # - vehicle_type

    def fetch_vehicle_types(self):
        return self.fetch('vehicle_type', tag='VehicleTypes')

    # - counter

    def fetch_counter(self, page_id):
        return self.fetch('counter', where=f"id='{page_id}'", tag='Counter')

    def fetch_counters(self, where=None, columns=None, group=None, order=None):
        return self.fetch('counter', columns=columns, where=where, group=group, order=order, tag='Counters')

    def set_counter(self, page_id, new_count):
        return self.write('counter', values={'id': page_id, 'value': new_count}, where=f"id='{page_id}'",
                          modonly=True, tag='SetCounter')

    def delete_counter(self, page_id):
        where = {'id': page_id}
        return self.delete('counter', self.make_where(where), tag='DeleteCounter')

    def set_health(self, page_id, verbose=False):
        self.write('counter', values={'id': page_id}, newonly=True, tag='SetHealth')
        return self.increment('counter', ['health'], f"id='{page_id}'", tag='SetHealth', verbose=verbose)

    def clear_health(self):
        return self.write('counter', values={'health': 0}, modonly=True, tag='ClearHealth')

    def increment_counter(self, page_id, tag='Count'):
        self.dbi.count(page_id, tag=tag)

    # - lineup_model

    def fetch_lineup_limits(self):
        # ranswer = fetch("select min(year), max(year), max(number) from lineup_model", $pif);
        return self.fetch('lineup_model', columns=['min(year)', 'max(year)', 'max(number)'],
                          one=True, tag='LineupLimits', verbose=False)

    def make_lineup_item(self, rec):
        result = {col: rec.get('lineup_model.' + col, '') for col in self.get_table_data('lineup_model').columns}
        result.update(self.copykeys('base_id', rec))
        result.update(self.copykeys('casting', rec))
        result.update(self.copykeys('pack', rec))
        result.update(self.copykeys('publication', rec))
        result.update(self.copykeys('page_info', rec))
        result['ref_id'] = rec.get('vs.ref_id', '')
        result['sec_id'] = rec.get('vs.sec_id', '')
        result['ran_id'] = rec.get('vs.ran_id', '')
        result['made'] = not (result['flags'] & config.FLAG_MODEL_NOT_MADE)
        result['notmade'] = '' if result['made'] else '*'
        result['class_name'] = result['href'] = result['product'] = ''
        result['no_variation'] = result['is_product_picture'] = 0
        result['cvarlist'] = list()
        result['vars'] = list()
        return result

    def fetch_lineup_models_bare(self, year=None, region=None, verbose=False):
        cols = self.make_columns('lineup_model')
        table = "lineup_model"
        wheres = []
        if region:
            wheres += [f'region="{region}"']
        if year:
            wheres += [f'year={year}']
        return self.dbi.select(table, cols=cols, where=' and '.join(wheres), verbose=verbose, tag='BareLineupModels')

    def fetch_simple_lineup_models(self, year='', region='', base_id='', verbose=False):
        cols = list()
        cols.extend(['lineup_model.id', 'lineup_model.base_id', 'lineup_model.mod_id', 'lineup_model.number',
                     'lineup_model.style_id', 'lineup_model.region', 'lineup_model.year', 'lineup_model.name',
                     'lineup_model.picture_id', 'lineup_model.flags', 'lineup_model.page_id', 'lineup_model.subname'])
        cols.extend(['base_id.id', 'base_id.first_year', 'base_id.rawname', 'base_id.description', 'base_id.flags',
                     'base_id.model_type'])
        cols.extend(['casting.id', 'casting.scale', 'casting.vehicle_type', 'casting.country', 'casting.make',
                     'casting.section_id'])
        table = "lineup_model"
        table += " left join base_id on base_id.id=lineup_model.mod_id"
        table += " left join casting on casting.id=lineup_model.mod_id"
        wheres = list()
        if isinstance(region, list) and region:
            wheres.append("lineup_model.region in (" + ','.join(["'" + x + "'" for x in region]) + ')')
        if year:
            wheres.append(f"lineup_model.year='{year}'")
        if base_id:
            wheres.append(f"lineup_model.base_id='{base_id}'")
        # turn this into a fetch
        return self.dbi.select(table, cols=cols, where=' and '.join(wheres), verbose=verbose, tag='SimpleLineupModels')

    def fetch_lineup_models(self, year='', region=''):
        cols = self.make_columns('lineup_model')
        cols += self.make_columns('base_id')
        cols += self.make_columns('casting')
        cols += self.make_columns('pack')
        cols += self.make_columns('publication')
        cols += self.make_columns('page_info')
        table = "lineup_model"
        table += " left join base_id on base_id.id=lineup_model.mod_id"
        table += " left join casting on casting.id=lineup_model.mod_id"
        table += " left join pack on pack.id=lineup_model.mod_id"
        table += " left join publication on publication.id=lineup_model.mod_id"
        table += " left join page_info on page_info.id=lineup_model.mod_id"
        wheres = list()
        if isinstance(region, list) and region:
            wheres.append("lineup_model.region in (" + ','.join(["'" + x + "'" for x in region]) + ')')
        elif region:
            wheres.append(f"lineup_model.region='{region}'")
        if year:
            cols.extend(['v.text_description', 'v.picture_id', 'v.var', 'vs.ref_id', 'vs.sec_id', 'vs.ran_id'])
            table += f" left join variation_select vs on (vs.ref_id='year.{year}')"
            table += " and vs.mod_id=lineup_model.mod_id"
            table += " left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var"
            wheres.append(f"lineup_model.year='{year}'")
        # turn this into a fetch
        return self.dbi.select(table, cols=cols, where=' and '.join(wheres), tag='LineupModels')

    def fetch_lineup_models_by_rank(self, rank, syear, eyear):
        cols = self.make_columns('lineup_model')
        cols += self.make_columns('base_id')
        cols += self.make_columns('casting')
        cols.extend(['v.text_description', 'v.picture_id', 'v.var', 'vs.ref_id', 'vs.sec_id'])
        table = "base_id,casting,lineup_model"
        table += " left join variation_select vs on vs.ref_id=lineup_model.page_id and vs.mod_id=lineup_model.mod_id"
        table += " left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var"
        where = f"lineup_model.number={rank}"
        where += f" and lineup_model.year>={syear}"
        where += f" and lineup_model.year<={eyear}"
        where += " and casting.id=lineup_model.mod_id"
        where += " and base_id.id=casting.id"
        # turn this into a fetch
        return self.dbi.select(table, cols=cols, where=where, tag='LineupModelsByRank')

    def fetch_lineup_years(self):
        # turn this into a fetch
        return self.dbi.select("lineup_model", cols=["year"], group="year", tag='LineupYears')

    def fetch_casting_lineups(self, mod_id):
        where = f"lineup_model.mod_id='{mod_id}'"
        left_joins = [('section', 'section.page_id=lineup_model.page_id and section.id=lineup_model.region'),
                      ('page_info', 'page_info.id=lineup_model.page_id')]
        return self.fetch("lineup_model", left_joins=left_joins, where=where, tag='CastingLineups')

    def fetch_lineup_model(self, where, verbose=None):
        return self.fetch('lineup_model', where=where, tag='LineupModel', verbose=verbose)

    def insert_lineup_model(self, values, newonly=True):
        # useful.write_message(values, '<br>')
        values = self.make_values('lineup_model', values)
        del values['id']
        return self.write('lineup_model', values=values, newonly=newonly, verbose=True, tag='InsertLineupModel')

    def update_lineup_model(self, where, values, verbose=False):
        # useful.write_message(where, values, '<br>')
        return self.write('lineup_model', values=self.make_values('lineup_model', values, 'lineup_model.'),
                          where=self.make_where(where), modonly=True, tag='UpdateLineupModel', verbose=verbose)

    def delete_lineup_model(self, where):
        self.delete('lineup_model', self.make_where(where))

    # - region

    def fetch_regions(self):
        regs = self.fetch('region', tag='Regions')
        return {x['id']: x['name'] for x in regs}, {x['id']: x['parent'] for x in regs}

    # - matrix_model

    def fetch_matrix_model(self, page_id, section_id, range_id):
        where = [f"page_id='{page_id}'", f"section_id='{section_id}'", f"range_id='{range_id}'"]
        return self.fetch('matrix_model', where=self.make_where(where), one=True, tag='MatrixModel')

    def fetch_matrix_models(self, page_id=None, section=None):
        where = []
        if page_id:
            where.append(f"page_id='{page_id}'")
        if section:
            where.append(f"section_id='{section}'")
        return tables.Results(
            'matrix_model',
            self.fetch('matrix_model', where=self.make_where(where), order='display_order', tag='MatrixModels'))

    # select * from casting,lineup_model where casting.id=lineup_model.mod_id and lineup_model.year='2006'
    '''
select * from casting,lineup_model
left join variation_select vs on vs.ref_id='year.2006' and vs.mod_id=lineup_model.mod_id
left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var
where casting.id=lineup_model.mod_id and lineup_model.year='2006';
    '''

    '''
select
casting.id,casting.first_year,casting.scale,casting.vehicle_type,casting.country,casting.rawname,casting.description,
casting.make,casting.flags,casting.section_id,matrix_model.id,matrix_model.mod_id,casting.model_type,
matrix_model.section_id,matrix_model.display_order,matrix_model.page_id,matrix_model.range_id,matrix_model.name,
matrix_model.subname,matrix_model.description,v.text_description,v.picture_id,v.var,vs.ref_id
from matrix_model left join casting on (casting.id=matrix_model.mod_id) left join variation_select vs on
(vs.ref_id='matrix.codered') and vs.mod_id=matrix_model.mod_id left join variation v on vs.mod_id=v.mod_id and
vs.var_id=v.var where matrix_model.page_id='matrix.codered'
    '''

    def fetch_matrix_models_variations(self, page_id, section=None):
        # Have to change this to: select matrix_model outer join casting outer join variation_select.
        table = "matrix_model"
        cols = self.make_columns(tabs=['base_id', 'casting', 'matrix_model', 'pack'])
        cols.extend(['v.text_description', 'v.picture_id', 'v.var', 'v.date'])
        cols.extend(self.make_columns('variation_select', 'vs'))
        table += " left join base_id on (base_id.id=matrix_model.mod_id)"
        table += " left join casting on (casting.id=matrix_model.mod_id)"
        table += " left join pack on (pack.id=matrix_model.mod_id)"
        table += f" left join variation_select vs on (vs.ref_id='{page_id}'"
        # table += f" or vs.ref_id like '{page_id}.%'"
        table += ") and vs.mod_id=matrix_model.mod_id left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var"
        where = "matrix_model.page_id='" + page_id + "'"
        if section:
            where += f" and matrix_model.section_id='{section}'"
        # turn this into a fetch
        return self.dbi.select(table, cols=cols, where=where, order='matrix_model.display_order',
                               tag='MatrixModelsVariations')

    def fetch_matrix_appearances(self, mod_id):
        wheres = [
            "page_info.id like 'matrix.%'",
            "page_info.id=matrix_model.page_id",
            "section.id=matrix_model.section_id",
            f"matrix_model.mod_id='{mod_id}'",
            f"page_info.flags & {config.FLAG_PAGE_INFO_HIDDEN} = 0",
        ]
        # turn this into a fetch
        return self.fetch('matrix_model,page_info,section', where=wheres, tag='MatrixAppearances')

    def insert_or_update_matrix_model(self, values, verbose=False):
        return self.write('matrix_model', values=values, tag='InsertOrUpdateMatrixModel', verbose=verbose)

    def delete_matrix_models(self, page_id, sec_id):
        return self.delete('matrix_model', where=f"page_id='{page_id}' and section_id='{sec_id}'")

    # - link_line

    def delete_link_line(self, id):
        self.delete('link_line', where=f"id={id}")

    def update_link_line(self, rec):
        return self.write('link_line', values=rec, where=f"id={rec['id']}", modonly=True, tag='UpdateLinkLine')

    def insert_link_line(self, rec, verbose=False):
        return self.write('link_line', values=rec, newonly=True, tag='InsertLinkLine', verbose=verbose)

    def fetch_link_line(self, id):
        # turn this into a fetch
        return self.dbi.select('link_line', where=f"id='{id}'", tag='LinkLine')

    def fetch_link_line_url(self, url):
        # turn this into a fetch
        return self.dbi.select('link_line', where=f"url='{url}'", tag='LinkLineURL')

    def clear_link_line_statuses(self, page_id=None, section=None, where=None, flags=None, verbose=False):
        wheres = list()
        if where:
            wheres.append(where)
        if page_id:
            wheres.append(f"page_id='{page_id}'")
        if section:
            wheres.append(f"section_id='{section}'")
        if flags:
            wheres.append(f"flags & {flags}")
        return self.write('link_line', values={'last_status': None}, where=" and ".join(wheres),
                          tag='LinkLineStatuses', modonly=True, verbose=verbose)

    def fetch_link_lines(self, page_id=None, section=None, where=None, flags=None, not_flags=None, order=None,
                         verbose=False):
        wheres = list()
        if where:
            if isinstance(where, list):
                wheres.extend(where)
            else:
                wheres.append(where)
        if page_id:
            wheres.append(f"page_id='{page_id}'")
        if section:
            wheres.append(f"section_id='{section}'")
        if flags:
            wheres.append(f"flags & {flags}")
        if not_flags:
            wheres.append(f"not(flags & {not_flags})")
        return self.fetch('link_line', where=" and ".join(wheres), order=order, tag='LinkLines', verbose=verbose)

    def fetch_links_single(self, page_id=None):
        columns = ['l1.page_id', 'l1.associated_link', 'l1.url', 'l1.name', 'l2.id', 'l2.name', 'l2.url', 'l1.flags']
        wheres = [
            f'not l1.flags & {config.FLAG_LINK_LINE_NEW | config.FLAG_LINK_LINE_HIDDEN}',
            'l1.associated_link=l2.id',
        ]
        if page_id:
            wheres.append(f"l1.page_id='{page_id}'")
        return tables.Results(
            'link_line', self.fetch('link_line l1,link_line l2', columns=columns, where=" and ".join(wheres),
                                    tag='LinksSingle', order="l1.display_order"))

    def fetch_link_statuses(self, where):
        return self.fetch('link_line', where=where, columns=['last_status', 'count(*)'], group='last_status',
                          tag='LinkStatuses', verbose=False)

    # - blacklist

    def fetch_blacklist(self):
        return self.fetch('blacklist', tag='Blacklist')

    # - publication

    def fetch_publication(self, id):
        return tables.Results('publication', self.fetch(
            'publication,base_id', where=["base_id.id=publication.id", f"base_id.id='{id}'"], tag='Publication'))

    def fetch_publication_types(self):
        cols = self.make_columns('publication') + self.make_columns('base_id') + ['count(*) as count']
        return tables.Results('publication', self.fetch(
            'publication,base_id', where=["base_id.id=publication.id"],
            columns=cols, group='base_id.model_type', tag='PublicationTypes'))

    def fetch_publications(self, year=None, country=None, model_type=None, order=None, verbose=False):
        wheres = ['base_id.id=publication.id']
        if model_type:
            wheres.append(f'base_id.model_type="{model_type}"')
        if year:
            wheres.append(f'base_id.first_year="{year}"')
        if country:
            wheres.append(f'publication.country="{country}"')
        return tables.Results('publication', self.fetch('publication,base_id', where=wheres, order=order,
                                                        tag='Publications', verbose=verbose))

    def add_new_publication(self, values):
        return self.write('publication', values=values, newonly=True, tag='AddNewPublication', verbose=True)

    # - pack

    def fetch_pack(self, id, var=''):
        wheres = [f"pack.id='{id}'", "pack.id=base_id.id"]
        if var:
            wheres.append(f"pack.var='{var}'")
        return self.fetch('pack,base_id', where=wheres, tag='Pack')

    def fetch_pack_results(self, id, var=''):
        wheres = [f"pack.id='{id}'", "pack.id=base_id.id"]
        if var:
            wheres.append(f"pack.var='{var}'")
        return tables.Results('pack', self.fetch('pack,base_id', where=wheres, tag='Pack'))

    def fetch_packs(self, page_id='', year='', region=''):
        wheres = ["base_id.id=pack.id"]
        if year:
            wheres.append(f"year='{year}'")
        if region:
            wheres.append(f"region='{region}'")
        if page_id:
            wheres.append(f"page_id='{page_id}'")
        return self.fetch('base_id,pack', where=wheres, tag='Packs')

    def add_new_pack(self, values, verbose=False):
        return self.write('pack', values=values, newonly=True, tag='AddNewPack', verbose=verbose)

    def insert_pack(self, pack_id, page_id=None):
        section_id = None
        if page_id:
            section_id = page_id[page_id.rfind('.') + 1:]
        self.write('base_id', values={'id': pack_id}, newonly=True, tag='InsertPack')
        return self.write('pack', values={'id': pack_id, 'page_id': page_id, 'section_id': section_id}, newonly=True,
                          tag='InsertPack')

    def delete_pack(self, id):
        self.delete('pack', f"id='{id}'")

    def fetch_packs_related(self, id):
        cols = self.table_cols('base_id') + self.table_cols('pack')
        tables = ['casting_related', 'base_id', 'pack']
        wheres = [f"casting_related.model_id='{id}'", "casting_related.related_id=base_id.id",
                  "casting_related.related_id=pack.id", "casting_related.section_id='packs'"]
        return self.fetch(tables, columns=cols, where=wheres, tag='PacksRelated')

    def update_pack(self, id, values):
        self.write('pack', values=self.make_values('pack', values), where=f"id='{id}'", modonly=True, tag='UpdPack')

    # - pack_model

    def insert_pack_model(self, pack_id):
        return self.raw_execute("insert into pack_model (pack_id,display_order) "
                                f"select'{pack_id}', 1+count(*) from pack_model where pack_id='{pack_id}'")

    def add_new_pack_models(self, pms, verbose=False):
        for pm in pms:
            self.write('pack_model', values=pm, tag='AddNewPackModels', verbose=verbose)

    def update_pack_models(self, pms):
        for pm in pms:
            self.write('pack_model', values=pm, where=f"id={pm['id']}", tag='UpdatePackModels')

    def fetch_pack_model(self, id):
        return self.fetch('pack_model', where=f'id={id}', tag='PackModel')

# select page_info.title,page_info.pic_dir,style.style_type, style.style_setting
# from page_info left outer join style on page_info.id=style.page_id
# where page_info.id='newpage';

    def fetch_pack_models(self, pack_id='', pack_var='', page_id='', verbose=False):
        long_pack_id = pack_id + ('-' + pack_var if pack_var else '')
        wheres = ["pack_model.pack_id='" + pack_id + "'", "pack_model.pack_var='" + pack_var + "'"]
        cols = [
            'base_id.id', 'base_id.first_year', 'base_id.flags', 'base_id.model_type', 'base_id.rawname',
            'base_id.description', 'pack_model.id', 'pack_model.mod_id', 'pack_model.pack_id', 'pack_model.pack_var',
            'pack_model.var_id', 'pack_model.display_order', 'pack_model.style_id', 'pack_model.subname',
            'casting.id', 'casting.scale', 'casting.vehicle_type', 'casting.country', 'casting.make',
            'casting.section_id', 'vs.ref_id', 'vs.sec_id', 'vs.ran_id', 'vs.mod_id', 'vs.var_id',
            'v.text_description', 'v.picture_id', 'v.date']
        froms = ("pack_model "
                 "left join base_id on pack_model.mod_id=base_id.id "
                 "left join casting on pack_model.mod_id=casting.id "
                 "left join variation_select vs on "
                 f"(vs.ref_id='{page_id}' and vs.sec_id='{long_pack_id}' and vs.mod_id=pack_model.mod_id)")
        froms += " left join variation v on (vs.mod_id=v.mod_id and vs.var_id=v.var)"
        return self.fetch(froms, columns=cols, where=" and ".join(wheres), tag='PackModels', verbose=verbose)

    def fetch_pack_model_appearances(self, mod_id):
        wheres = [
            "pack.id=base_id.id",
            f"pack_model.mod_id='{mod_id}'",
            "pack_model.pack_id=pack.id",
            "page_info.id=pack.page_id",
            "pack.page_id=section.page_id",
            "section.id=pack.section_id",
        ]
        return self.fetch(
            'pack,pack_model,page_info,base_id,section',
            columns=['pack.id', 'base_id.id', 'base_id.rawname', 'base_id.first_year', 'pack.page_id', 'pack.region',
                     'pack.layout', 'page_info.title', 'pack.section_id', 'section.name'],
            where=wheres,
            tag='PackModelAppearances')

    def delete_pack_models(self, ref_id, pack_id):
        self.delete('pack_model', f"pack_id='{pack_id}'")
        self.delete('variation_select', where=f"ref_id='{ref_id}' and sec_id='{pack_id}'")

    # - box_type

    def fetch_box_type(self, box_id):
        return self.fetch('box_type', where={"id": box_id}, verbose=False, tag='BoxTypes')

    def fetch_box_type_by_mod(self, mod_id, box_style=None):
        # this sucks so hard
        where1 = f'box_type.mod_id="{mod_id}"'
        where2 = f'(box_type.mod_id=alias.id and alias.ref_id="{mod_id}")'
        where3 = f' and box_type.box_type like "{box_style}%"' if box_style else ''
        return (self.fetch('box_type', where=where1 + where3, verbose=False) +
                self.fetch('box_type,alias', where=where2 + where3, verbose=False, tag='BoxTypeByMod'))

    # - user

    def fetch_user(self, id=None, user_id=None, vkey=None, passwd=None, email=None):
        args = []
        where = []
        if id:
            where.append(f"id={id}")
        if user_id:
            where.append(f"user_id='{user_id}'")
        if vkey:
            where.append(f"vkey='{vkey}'")
        if passwd:
            where.append("passwd=PASSWORD(%s)")
            args.append(passwd)
        if email:
            where.append(f"email='{email}'")
        return tables.Results('user', self.fetch('user', where=where, args=args, logargs=False, tag='User')).first

    def fetch_users(self):
        return tables.Results('user', self.fetch('user', tag='Users'))

    def login(self, id=None, user_id=None, passwd=None):
        table_name = self.make_tablename('user')
        args = (passwd,)
        if id:
            query = f"select id, privs from {table_name} where id='{id}'"
        else:
            query = f"select id, privs from {table_name} where user_id='{user_id}'"
        if 0:
            query += ' and passwd=PASSWORD(%s)'
        else:
            args = None
        res, desc, lid = self.raw_execute(query, args=args, logargs=False, tag='Login')
        if res:
            return res[0][0], res[0][1]
        return None, None

    def create_user(self, passwd, vkey, **kwargs):
        table_data = self.get_table_data('user')
        cols = ['vkey', 'flags'] + [x for x in table_data.editable if x in kwargs]
        vals = [vkey, config.FLAG_USER_NEW] + [kwargs[x] for x in table_data.editable if x in kwargs]
        values = dict(zip(cols, vals))
        values['name'] = values['first_name'] + ' ' + values['last_name']
        ret = self.write('user', values=values, newonly=True, logargs=False, tag='CreateUser')
        if ret > 0:
            self.update_password(ret, passwd)
        return ret

    def update_user(self, rec_id, **kwargs):
        values = {x: kwargs[x] for x in self.get_table_data('user').columns if x in kwargs}
        self.write('user', values=values, where=f"id={rec_id}", modonly=True, tag='UpdateUser')

    def update_profile(self, user, **kwargs):
        rec_id = user['id']
        values = {x: kwargs[x] for x in self.get_table_data('user').editable if x in kwargs and user[x] != kwargs[x]}
        if 'user_id' in values:
            other_user = self.fetch_user(user_id=values['user_id'])
            if other_user and other_user['buser.id'] != rec_id:
                return None
        if user['email'] != values['email']:
            values['flags'] = user['flags'] & ~config.FLAG_USER_VERIFIED
        self.write('user', values=values, where=f"id={rec_id}", modonly=True, tag='UpdateUser')

    def update_password(self, rec_id, passwd):
        self.write('user', values='passwd=PASSWORD(%s)', where=f"id={rec_id}", modonly=True, args=(passwd,),
                   logargs=False, tag='UpdatePassword')

    def verify_user(self, user_id):
        return self.update_flags('user', turn_on=config.FLAG_USER_VERIFIED, where={'user_id': user_id},
                                 tag='VerifyUser')

    def update_user_last_login(self, user_id):
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.write('user', values={'last_login': timestamp}, where=f"id={user_id}", modonly=True,
                   tag='UpdateUserLogin')

    def write_user(self, values):
        self.write('user', values=values, where=f"id={values['id']}", modonly=True, tag='WriteUser')

    def delete_user(self, id):
        self.delete('user', f'id={id}')

    # - cookie

    def delete_cookie(self, user_id, ip):
        self.delete('cookie',
                    where=f'(user_id={user_id} and ip="{ip}") or (expire < NOW())',
                    tag='DeleteCookie')

    def insert_cookie(self, user_id, ckey, ip, expires):
        values = {'user_id': user_id, 'ckey': ckey, 'ip': ip, 'expires': expires}
        return self.write('cookie', values=values, newonly=True, tag='WriteCookie')

    def fetch_cookie(self, ckey):
        wheres = [
            f'cookie.ckey="{ckey}"',
            'expires > NOW()',
            'user.id=cookie.user_id',
        ]
        return tables.Results('cookie',
                              self.fetch('cookie,user', where=wheres, tag='GetCookie')).last

    # - token

    def create_token(self):  # render.format_form_token is not currently using this.  sigh
        return useful.generate_token(6)

    def insert_token(self, token_id, verbose=False):
        self.delete('token', where='current_timestamp()-created > 20', tag='InsertToken', verbose=None)
        retval = True
        if token_id:
            self.raw_execute('lock tables buser.token write', tag='InsertToken')
            ret = self.fetch('token', where={'id': token_id}, tag='InsertToken', verbose=verbose)
            if not ret:
                ret = self.write('token', values={'id': token_id}, newonly=True, tag='InsertToken', verbose=verbose)
            else:
                retval = False
            self.raw_execute('unlock tables', tag='InsertToken')
        return retval

    # - photographer

    def fetch_photographer(self, photographer_id):
        return tables.Results('photographer',
                              self.fetch('photographer', where=f'id="{photographer_id}"', tag='Photographer')).first

    def fetch_photographers(self, notflags=0):
        return tables.Results('photographer',
                              self.fetch('photographer', where=f'(flags & {notflags}) = 0', tag='Photographers'))

    def fetch_photographer_counts(self, photographer_id=None):
        cols = self.make_columns('photographer') + ['count(*) as count'] + self.make_columns('photo_credit', 'c')
        wheres = ['photographer.id=photo_credit.photographer_id', 'c.id=photographer.example_id']
        if photographer_id:
            wheres.append(f'photo_credit.photographer_id="{photographer_id}"')
        rows = self.fetch('photographer,photo_credit,photo_credit c', where=wheres,
                          columns=cols, group='photo_credit.photographer_id', tag='PhotographerCounts', verbose=False)
        return tables.Results('photographer', rows)

    def write_photographer(self, photographer_id, values, verbose=False):
        where = f"id='{photographer_id}'"
        return self.write('photographer', values=values, where=where, tag='WritePhotographer', verbose=verbose)

    # - photo_credit

    def fetch_photo_credit(self, path, name, suffix='', verbose=False):
        if path.startswith('./'):
            path = path[2:]
        if len(name) > 2 and name[0] in 'sml' and name[1] == '_':
            name = name[2:]
        if '.' in name:
            name = name[:name.find('.')]
        if suffix:
            name += '-' + suffix
        return self.fetch('photo_credit,photographer',
                          where=['photo_credit.photographer_id=photographer.id', f'photo_credit.path="{path}"',
                                 f'photo_credit.name="{name}"'],
                          tag='PhotoCredit', verbose=verbose, one=True)

    def fetch_photo_credits(self, photographer_id='', path='', name='', suffix='', verbose=False):
        if path.startswith('./'):
            path = path[2:]
        if len(name) > 2 and name[0] in 'sml' and name[1] == '_':
            name = name[2:]
        if '.' in name:
            name = name[:name.find('.')]
        if suffix:
            name += '-' + suffix
        wheres = ['photo_credit.photographer_id=photographer.id']
        if path:
            wheres.append(f'photo_credit.path="{path}"')
        if name:
            wheres.append(f'photo_credit.name="{name}"')
        if photographer_id:
            wheres.append(f'photo_credit.photographer_id="{photographer_id}"')
        return self.fetch('photo_credit,photographer', where=wheres, tag='PhotoCredit', verbose=verbose)

    def fetch_photo_credits_page(self, photographer_id='', pagesize=100, page=0, verbose=False):
        # useful.write_comment('fetch_photo_credits_page', photographer_id, pagesize, page, verbose)
        wheres = [f'photo_credit.photographer_id="{photographer_id}"']
        return self.fetch('photo_credit', where=wheres, order='path,name', limit=(page * pagesize, pagesize,),
                          tag='PhotoCreditPage', verbose=verbose)

    def fetch_photo_credits_raw(self):
        return self.fetch('photo_credit', tag='PhotoCreditRaw')

    def fetch_photo_credits_for_models(self, path, verbose=False):
        if path.startswith('./'):
            path = path[2:]
        wheres = ['photo_credit.photographer_id=photographer.id',
                  f'photo_credit.path="{path}"']
        return self.fetch('photo_credit,photographer', where=wheres, tag='PhotoCreditMods', verbose=verbose)

    def fetch_photo_credits_for_vars(self, path, name, verbose=False):
        if path.startswith('./'):
            path = path[2:]
        if path.startswith('/'):
            path = path[1:]
        wheres = ['photo_credit.photographer_id=photographer.id',
                  f'photo_credit.name like "%{name}%"',
                  f'photo_credit.path="{path}"']
        return self.fetch('photo_credit,photographer', where=wheres, tag='PhotoCreditVars', verbose=verbose)

    def fetch_photographer_category_counts(self, photog_id):
        cols = self.make_columns('photo_credit') + ['count(*) as count']
        rows = self.fetch('photo_credit', where=f'photo_credit.photographer_id="{photog_id}"',
                          columns=cols, group='photo_credit.path', tag='PhotographerCatCounts')
        return tables.Results('photo_credit', rows)

    def write_photo_credit(self, photographer_id, path, name, suffix='', verbose=False):
        if path and name:
            if path.startswith('./'):
                path = path[2:]
            if len(name) > 2 and name[0] in 'sml' and name[1] == '_':
                name = name[2:]
            if '.' in name:
                name = name[:name.find('.')]
            if suffix:
                name += '-' + suffix
            path = path.lower()
            name = name.lower()
            if photographer_id:
                ovalues = self.fetch_photo_credits(path=path, name=name, verbose=verbose)
                nvalues = {
                    'path': path,
                    'name': name,
                    'photographer_id': photographer_id,
                }
                where = ''
                if ovalues:
                    nvalues['id'] = ovalues[0]['photo_credit.id']
                    where = f"photo_credit.id={nvalues['id']}"
                    for ovalue in ovalues[1:]:
                        self.delete_photo_credit(ovalue['photo_credit.id'])
                return self.write('photo_credit', values=nvalues, where=where, tag='WritePhotoCredit', verbose=verbose)
            else:
                where = self.make_where({
                    'path': path,
                    'name': name})
                return self.delete('photo_credit', where=where, tag='DeletePhotoCredit', verbose=verbose)

    def rename_photo_credit(self, pdir, old_name, new_name):
        return self.write(
            'photo_credit', {'name': new_name}, self.make_where({'name': old_name, 'path': pdir}),
            modonly=True, tag='RenamePictures')

    def delete_photo_credit(self, id=None, path='', name=''):
        if id:
            return self.delete('photo_credit', where=f'id={id}', tag='DeletePhotoCreditID')
        return self.delete('photo_credit', where=f'path="{path}" and name="{name}"', tag='DeletePhotoCreditName')

    # - category

    def fetch_category(self, cat_id):
        return tables.Results('category', self.fetch('category', where=f"id='{cat_id}'", tag="Cat")).first

    def fetch_categories(self):
        return tables.Results('category', self.fetch('category', tag='Cats'))

    def fetch_category_counts(self):
        cols = self.make_columns('category') + ['count(*) as count']
        rows = self.fetch('category,variation_select', where='category.id=variation_select.category',
                          columns=cols, group='variation_select.category', tag='CatCounts')
        return tables.Results('category', rows)
        # return tables.Results('category', self.fetch('category', tag="Cats"))

    def insert_category(self, cat, name, flags=0):
        return self.write('category', values={'id': cat, 'name': name, 'flags': flags}, newonly=True, tag='WriteCat')

    # - tumblr

    def fetch_tumblr_post(self):
        return tables.Results('tumblr', self.fetch('tumblr', columns=self.make_columns('tumblr'), limit=1,
                              tag='Tumblr')).first

    def fetch_tumblr_posts(self):
        return tables.Results('tumblr', self.fetch('tumblr', columns=self.make_columns('tumblr'), tag='Tumblrs'))

    def insert_tumblr(self, ty_post, response, payload):
        return self.write('tumblr', values={'post_type': ty_post, 'payload': payload, 'response': response},
                          newonly=True, tag="InsertTumblr")

    def delete_tumblr(self, post_id):
        return self.delete('tumblr', where=f'id={post_id}', tag='DeleteTumblr')

    # - mbusa

    def fetch_mbusa_entry(self, entry_id):
        return tables.Results('mbusa', self.fetch('mbusa', where={'id': entry_id}, tag='MBUSAEntry'))

    # - miscellaneous

    def fetch_counts(self):
        cols = ['base_id.model_type', 'count(*) as count']
        rows1 = self.fetch('base_id', columns=cols, group='base_id.model_type', tag='CountsBaseId')

        cols = ['base_id.model_type', 'count(variation.var) as count']
        rows2 = self.fetch('base_id,variation', columns=cols, where='base_id.id=variation.mod_id',
                           group='base_id.model_type', tag='CountsVars')
        return tables.Results('base_id', rows1), tables.Results('base_id', rows2)

    # ----- from mkdesc.py ------------------------------------

    # [?][*=&]attr[^prepend][+append][#default]
    # ?... = attribute is optional: "no", "-", or missing just omits it.
    # *attr = value attr
    # =attr = attr value
    # &attr = value
    # @attr1/attr2/attr3 = *attr1, *attr2 if different, else &attr1+attr3 -- not implemented
    # ^prepend = prepended text
    # +append = appended text
    # #default if value is blank
    # |~ for field splitting - want to figure out a way to do this for wheels
    def parse_detail_format(self, fmt, deco_type):

        def get_title(attr_name):
            return self.titles.get(attr_name, {}).get(deco_type, attr_name.replace('_', ' '))

        def opt_split(val, by):
            return val.split(by, 1) if by in val else (val, '')

        attr_name = ''
        attr_re = re.compile(r'%\((?P<a>[^)]*)\)s')

        if is_opt := fmt.startswith('?'):
            fmt = fmt[1:]

        fmt, default = opt_split(fmt, '#')
        fmt, fmt_append = opt_split(fmt, '+')
        fmt, fmt_prepend = opt_split(fmt, '^')

        if fmt.startswith('*'):
            attr_name = fmt[1:]
            fmt = f'%({attr_name})s {get_title(attr_name)}'
        elif fmt.startswith('='):
            attr_name = fmt[1:]
            fmt = f'{get_title(attr_name)} %({attr_name})s'
        elif fmt.startswith('&'):
            attr_name = fmt[1:]
            fmt = f'%({attr_name})s'
        elif '%' in fmt:  # raw format
            # MI818 still needs this, at the least.
            if attr_m := attr_re.search(fmt):
                attr_name = attr_m.group('a')
        else:  # literal string
            attr_name = None
        return attr_name, f'{fmt_prepend} {fmt} {fmt_append}'.strip(), default, is_opt

    titles = {'deco': mbdata.deco_types_dict}

    def recalc_description(self, mod_id, showtexts=False, verbose=False):
        '''Main call to create text_* from format_* and attributes.'''
        # verbose = showtexts = True
        useful.verbose = verbose
        cas_dat = self.get_table_data('casting')
        var_dat = self.get_table_data('variation')
        cols = cas_dat.formats
        casting = self.fetch_casting(mod_id, extras=True, tag='Recalc', verbose=verbose)
        varign = var_dat.meta + ['vs']

        # I apologize in advance for this function.
        def fmt_desc(var, casting, field):

            def fmt_detail(fmt):

                def fmt_subdetail(sfmt):
                    attr_name, sfmt, default, is_opt = self.parse_detail_format(sfmt, var['deco_type'])
                    if attr_name:
                        if attr_name not in var:
                            useful.write_debug_message('!', attr_name)
                            return attr_name, ''
                        value = var.get(attr_name)
                        if not value or (is_opt and (value == 'no' or value == '-')):
                            return attr_name, default
                    return attr_name, sfmt

                if fmt[0] == '@':
                    return [fmt_subdetail(subformat) for subformat in fmt[1:].split('/')]
                else:
                    return fmt_subdetail(fmt)[1]

            fmts = [y for y in [fmt_detail(x) for x in casting.get(field, '').split('|') if x] if y]
            descs = []
            for fmt in fmts:
                desc = ''
                try:
                    # YES I'm still using '%'!  Hate me if you want.
                    if isinstance(fmt, str):
                        desc = fmt % var
                    elif var[fmt[0][0]] == var[fmt[1][0]]:
                        desc = fmt[2][1] % var
                    else:
                        desc = ', '.join([fmt[0][1] % var, fmt[1][1] % var])
                except Exception:
                    useful.write_debug_message('!', field, fmt)
                if descs and descs[-1] == desc:
                    continue
                descs.append(desc.replace('  ', ' '))
            if showtexts:
                useful.write_message(' ', field[7:10], ':', descs)
            return ', '.join(descs)

        # useful.write_comment('recalc casting', casting)
        for orig_var in self.depref('variation', self.fetch_variations(mod_id)):
            useful.write_debug_message(var_id := orig_var['var'])
            var = {}
            for k, v in orig_var.items():
                cmps = mbdata.components.get(k, {})
                v = v or ''
                if k not in varign:
                    val = _val = ''
                    for w in v.split('|'):
                        t = ''
                        if '~' in w:
                            t, w = w.split('~')
                            t = cmps.get(t, t)
                        val += (cmps.get('_', '') if val and w else '') + f' {w} {t}'
                        _val += (cmps.get('_', '') if _val and w else '') + f' {w}'
                    var[k] = val.strip()
                    var['_' + k] = _val.strip()
            self.update_variation(
                {f'text_{x}': fmt_desc(var, casting, f'format_{x}') for x in cols},
                {'mod_id': mod_id, 'var': var_id})

    def check_description_formatting(self, mod_id, linesep=''):
        cas_cols = ['format_' + x for x in self.get_table_data('casting').formats]
        var_cols = self.get_table_data('variation').internals
        casting = self.fetch_casting(mod_id, extras=True)
        attributes = var_cols + [x['attribute.attribute_name'] for x in self.fetch_attributes(mod_id)]
        messages = ''
        retval = False
        missing = []
        if not casting.get('made'):
            return retval, messages, missing
        for cas_col in cas_cols:
            if casting.get(cas_col):
                for fmt in casting[cas_col].split('|'):
                    attr = self.parse_detail_format(fmt, 't')[0]
                    if attr and (attr[1:] if attr.startswith('_') else attr) not in attributes:
                        messages += f'{mod_id} ! {cas_col} {fmt}{linesep}\n'
                        missing.append(attr)
                        retval = True
        for attr in attributes:
            found = False
            attr_re = re.compile(r'\b%s\b' % attr)
            for col in cas_cols[1:]:  # ignore description for this check
                attr_m = attr_re.search(casting[col])
                if attr_m:
                    found = True
                    messages += f'{mod_id} + {attr}{linesep}\n'
                    break
            if not found:
                messages += f'{mod_id} - {attr}{linesep}\n'
                retval = True
        return retval, messages, missing

    def fetch_tables(self):
        return self.raw_execute('show tables')

    def fetch_table(self, table):
        return self.raw_execute(f'desc {table}')

    def preformat_results(self, results):
        if not results:
            return ''
        lengths = [0] * len(results[0])

        def sign(x, y):
            return -1 if not y or x < 0 else 1

        for result in results:
            for col in range(len(result)):
                lengths[col] = (max(len(str(result[col])), abs(lengths[col])) *
                                sign(lengths[col], str(result[col]).isdigit()))
        return '| ' + (' | '.join([f'%{x}s' for x in lengths])) + ' |'


class ManItem(object):
    '''
    base_id
        columns: [id, first_year, model_type, rawname, description, flags]
    casting
        columns: [id, scale, vehicle_type, country, make, section_id, variation_digits]
        extra_columns:
                 [notes, format_description, format_body, format_interior, format_windows, format_base,
                  format_wheels, format_with, format_text]
    matrix_model
        columns: [id, base_id, page_id, section_id, display_order, range_id, mod_id, flags, shown_id,
                  name, subname, description]
    lineup_model
        columns: [id, base_id, mod_id, number, display_order, flags, style_id, picture_id, region, year,
                  name, page_id]
    pack
        columns: [id, var, page_id, section_id, region, end_year, layout, product_code, material,
                  country, note]
    pub
        columns: [id, country, section_id, isbn]
    '''

    def __init__(self, mod):

        if mod.get('id'):
            mod['name'] = mod.get('rawname', '').replace(';', ' ')
            mod['unlicensed'] = {'unl': '-', '': '?'}.get(mod['make'], ' ')
            mod.setdefault('description', '')
            mod['made'] = not (mod.get('flags', 0) & config.FLAG_MODEL_NOT_MADE)
            mod['visual_id'] = self.default_id(mod['id'])
        else:
            mod['id'] = ''
            mod['name'] = ''
            mod['iconname'] = ''
            mod['unlicensed'] = '?'
            mod['description'] = ''
            mod['made'] = False
            mod['visual_id'] = ''
        mod['filename'] = mod['id'].lower()
        mod['notmade'] = '' if mod['made'] else '*'
        mod['revised'] = (((mod.get('flags', 0) if mod else 0) or 0) & config.FLAG_MODEL_CASTING_REVISED) != 0
        mod['linkid'] = mod.get('mod_id', mod.get('id'))
        mod['link'] = "single.cgi?id"
        mod['descs'] = [x for x in mod['description'].split(';') if x]
        mod['iconname'] = self.icon_name(mod.get('rawname', ''))
        mod['shortname'] = self.short_name(mod.get('rawname', ''))
        mod['casting_type'] = mbdata.model_types.get(mod.get('model_type', 'SF'), 'Casting')
        return mod
