#!/usr/local/bin/python

import copy, re, sys
import db
import mbdata
import tables
import useful

id_re = re.compile('''(?P<a>[a-zA-Z]*)(?P<d>\d*)''')


class DBHandler:
    table_info = tables.table_info
    def __init__(self, config, user_id, db_logger, verbose):
        self.dbi = db.DB(config, user_id, db_logger, verbose)
        if not self.dbi:
            raise 'DB connect failed'
        #self.table_info = tables.table_info
        self.set_constants()

    def __repr__(self):
        return "'<dbhand.DBHandler instance>'"

    def __str__(self):
        return "'<dbhand.DBHandler instance>'"

    def error_report(self):
        return str(self.__dict__) + '\n' + 'dbi = ' + str(self.dbi.__dict__)

    def set_verbose(self, flag):
        self.dbi.verbose = flag

    def escape_string(self, s):
        return self.dbi.escape_string(s)

    def make_id(self, table, values, prefix=''):
        return {x: values.get(prefix + x, '') for x in self.get_table_info(table)['id']}

    def make_values(self, table, values, prefix=''):
        return {x: values.get(prefix + x, '') for x in self.get_table_info(table)['columns']}

    def form_make_values(self, table, form, prefix=''):
        return {x: values.get_str(prefix + x, '') for x in self.get_table_info(table)['columns']}

    def get_table_info(self, table):
        table_info = self.table_info[table]
        #table_info['name'] = table
        return table_info

    def get_editor_link(self, table, args):
        table_info = self.get_table_info(table)
        url = '/cgi-bin/editor.cgi?table=%s' % table
        if table_info:
            for key in args:
                if key in table_info['columns']:
                    url += '&%s=%s' % (key, args[key])
        return url

    def table_cols(self, table):
        return [table + '.' + x for x in self.table_info[table]['columns']]

    def set_constants(self):
        for key in tables.__dict__:
            if key.startswith('FLAG_'):
                self.__dict__[key] = tables.__dict__[key]

    def make_where(self, form, cols=None, prefix=""):
        if not cols:
            cols = form.keys()
        wheres = list()
        for col in cols:
            if prefix + col in form:
                wheres.append(col + "='" + str(form.get(prefix + col, '')) + "'")
        return ' and '.join(wheres)

    def raw_execute(self, query, tag=''):
        return self.dbi.execute(query, tag=tag)

#    def raw_fetch(self, query, tag=''):
#       return self.dbi.rawquery(query, tag=tag)

    def make_columns(self, tab, extras=False, tag=None):
        if not tag:
            tag = tab
        columns = list()
        if tab in self.table_info:
            columns.extend([tag + '.' + x for x in self.table_info[tab]['columns'] + (self.table_info[tab].get('extra_columns', []) if extras else [])])
        else:
            columns.append(tag + '.*')
        return columns

    def fetch(self, table_name, args=None, left_joins=None, columns=None, extras=False, where=None, group=None, order=None, tag='', verbose=False):
        if not columns:
            if isinstance(table_name, str):
                table_name = table_name.split(',')
            columns = list()
            for tab in table_name:
                if ' ' in tab:
                    columns.extend(self.make_columns(tab[:tab.find(' ')], tab[tab.find(' ') + 1:], extras))
                else:
                    columns.extend(self.make_columns(tab, extras))
            table_name = ','.join(table_name)
        if isinstance(where, list):
            where = ' and '.join(where)
        elif isinstance(where, dict):
            where = self.make_where(where)
        if left_joins:
            table_name = '(%s)' % table_name
            for lj in left_joins:
                table_name += ' left join %s on (%s)' % tuple(lj)
		j_tab = lj[0][:lj[0].find(' as ')] if ' as ' in lj[0] else lj[0]
		j_name = lj[0][lj[0].find(' as ') + 4:] if ' as ' in lj[0] else lj[0]
                columns.extend([j_name + '.' + x for x in self.table_info[j_tab]['columns']])
        return self.dbi.select(table_name, columns, args=args, where=where, group=group, order=order, tag=tag, verbose=verbose)

    def describe_dict(self, table):
        return {x['field']: x for x in self.describe(table)}

    def describe(self, table):
        return self.dbi.describe(table)

    def columns(self, table):
        return [x['field'] for x in self.describe(table)]

    def depref(self, table, results):
        if isinstance(results, dict):
            for key in results.keys():
                if key.startswith(table + '.'):
		    if not results.get(key[len(table) + 1:]):
			results[key[len(table) + 1:]] = results[key]
                    del results[key]
        else:
            for result in results:
                self.depref(table, result)
        return results

    def increment(self, table_name, values=None, where=None, tag='', verbose=False):
        values = {x: x + '+1' for x in values}
        return self.dbi.updateraw(table_name, values, where, tag=tag, verbose=verbose)

    def write(self, table_name, values=None, where=None, newonly=False, modonly=False, tag='', verbose=False):
        if newonly:
            return self.dbi.insert(table_name, values, tag=tag, verbose=verbose)
        elif modonly:
            return self.dbi.update(table_name, values, where, tag=tag, verbose=verbose)
        else:
            return self.dbi.insert_or_update(table_name, values, tag=tag, verbose=verbose)

    def delete(self, table, where=None, tag='', verbose=None):
        return self.dbi.remove(table, where, tag=tag, verbose=verbose)

    # end dbi interface section

    #- page_info

    def fetch_page(self, id, verbose=False):
        return self.fetch('page_info', where={'id': id}, tag='Page', verbose=verbose)

    def fetch_pages(self, where, columns=None, group=None, order=None):
        return self.fetch('page_info', columns=columns, where=where, group=group, order=order, tag='Pages')

    def fetch_page_years(self):
        return self.fetch('page_info,lineup_model',
                columns=self.make_columns('page_info') + ['max(lineup_model.number)'],
                where=['page_info.id=lineup_model.page_id', "page_info.id like 'year.%'"],
                group="page_info.id", tag='PageYears')
# select page_info.id, max(lineup_model.number) from page_info, lineup_model where page_info.id=lineup_model.page_id and page_info.id like 'year.%' group by page_info.id;

    def set_health(self, page_id, verbose=False):
        #return self.write('page_info', {'health': 1}, "id='%s'" % page_id, modonly=True, verbose=verbose)
        return self.increment('page_info', ['health'], "id='%s'" % page_id, tag='Health', verbose=verbose)

    def clear_health(self):
        self.write('page_info', {'health': 0}, modonly=True)

    #- country

    def fetch_countries(self):
        return self.fetch('country')

    #- section

    def fetch_section(self, id):
        secs = self.fetch('section', where={'id': id}, tag='Section')
        if secs:
            return secs[0]
        return None

    def fetch_sections(self, where=None):
        return self.fetch('section', where=where, order='display_order', tag='Sections')

    #- base_id

    def fetch_base_ids(self):
        return self.fetch('base_id', tag='BaseIDs')

    def fetch_base_id(self, id):
        return self.fetch('base_id', where="id='%s'" % id, tag='BaseID')

    def rename_base_id(self, old_mod_id, new_mod_id):
        self.write('base_id', {'id': new_mod_id}, where="id='%s'" % old_mod_id, modonly=True)
        self.write('casting', {'id': new_mod_id}, where="id='%s'" % old_mod_id, modonly=True)
        self.write('pack', {'id': new_mod_id}, where="id='%s'" % old_mod_id, modonly=True)
        self.write('publication', {'id': new_mod_id}, where="id='%s'" % old_mod_id, modonly=True)
        self.write('alias', {'ref_id': new_mod_id}, where="ref_id='%s'" % old_mod_id, modonly=True)
        self.write('attribute', {'mod_id': new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
        self.write('attribute_picture', {'mod_id': new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
        self.write('casting_compare', {'mod_id': new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
        self.write('casting_compare', {'compare_id': new_mod_id}, where="compare_id='%s'" % old_mod_id, modonly=True)
        self.write('casting_related', {'model_id': new_mod_id}, where="model_id='%s'" % old_mod_id, modonly=True)
        self.write('casting_related', {'related_id': new_mod_id}, where="related_id='%s'" % old_mod_id, modonly=True)
        self.write('detail', {'mod_id': new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
        self.write('lineup_model', {'mod_id': new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
        self.write('matrix_model', {'mod_id': new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
        self.write('pack_model', {'pack_id': new_mod_id}, where="pack_id='%s'" % old_mod_id, modonly=True)
        self.write('pack_model', {'mod_id': new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
        self.write('variation', {'mod_id': new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
        self.write('variation_select', {'mod_id': new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
        self.write('variation_select', {'sub_id': new_mod_id}, where="sub_id='%s'" % old_mod_id, modonly=True)
        self.write('link_line', {'page_id': 'single.' + new_mod_id}, where="page_id='single.%s'" % old_mod_id, modonly=True)

    def update_base_id(self, id, values):
        self.write('base_id', self.make_values('base_id', values), "id='%s'" % id, modonly=True)

    def add_new_base_id(self, values):
        self.write('base_id', self.make_values('base_id', values), newonly=True, tag="AddNewBaseId")

    def fetch_base_id_model_types(self):
	return self.fetch('base_id', columns=['model_type'], group='model_type', order='model_type', tag='fetch_base_id_model_type')

    def delete_base_id(self, where):
        self.delete('base_id', self.make_where(where))

    #- alias

    def fetch_alias(self, id, extras=False):
        alist = self.fetch("casting,alias,base_id", extras=True, where=["casting.id=alias.ref_id", "alias.id='%s'" % id, "casting.id=base_id.id"], tag='Alias')
        if alist:
            return alist[0]
        return {}

    def fetch_castings_by_box(self, series, style):
        wheres = ['casting.id=base_id.id']
        if series:
            wheres.append("base_id.model_type='%s'" % series)
        if style:
            wheres.append("box_style.styles like '%%%s%%'" % style)
        fet1 = self.fetch('box_style,casting,base_id', where=['box_style.id=casting.id'] + wheres, tag='CastingsByBox', verbose=0)

        #ljoins = [('alias', "base_id.id=alias.ref_id")]  # and alias.section_id != ''")]
        wheres = ['box_style.id=alias.id', 'alias.ref_id=casting.id'] + wheres
        fet2 = self.fetch('box_style,alias,casting,base_id', where=wheres, tag='CastingsByBox', verbose=0)
        return fet1 + fet2

    def fetch_casting_by_alias(self, id):
        manlist = self.fetch('alias,casting', left_joins=[('vehicle_make', 'casting.make=vehicle_make.make')], where="casting.id=alias.ref_id and alias.id='%s'" % id, tag='CastingByAlias')
        if manlist:
            return self.modify_man_item(manlist[0])
        return {}

    def fetch_castings_by_alias(self, id):
        return self.fetch('alias,casting', left_joins=[('vehicle_make', 'casting.make=vehicle_make.make')], where="casting.id=alias.ref_id and alias.id='%s'" % id, tag='CastingsByAlias')

    def fetch_aliases(self, ref_id=None, type_id=None, where=None):
        wheres = ["base_id.id=casting.id", "casting.id=alias.ref_id"]
        if ref_id:
            wheres.append("alias.ref_id='%s'" % ref_id)
        if type_id:
            wheres.append("alias.type='%s'" % type_id)
        if isinstance(where, list):
            wheres += where
        elif isinstance(where, str):
            wheres.append(where)
        return self.fetch("base_id,casting,alias", where=wheres, tag='Aliases')

    #- casting

    def fetch_casting(self, id, extras=False):
        wheres = ['base_id.id=casting.id', 'casting.id="%s"' % id]
        manlist = self.fetch("casting,base_id", left_joins=[("vehicle_make", "casting.make=vehicle_make.make")], where=wheres, extras=extras, tag='Casting')
        if manlist:
            return self.modify_man_item(manlist[0])
        return {}

    def fetch_casting_list(self, section_id=None, page_id=None, where=None, verbose=False):
        wheres = ['base_id.id=casting.id', 'casting.section_id=section.id']
        if page_id:
            wheres.append('section.page_id="%s"' % page_id)
        if isinstance(where, list):
            wheres += where
        elif isinstance(where, str):
            wheres.append(where)
        if section_id:
            wheres.append('section.id="%s"' % section_id)
        return self.fetch('base_id,casting,section', where=wheres, tag='CastingList', verbose=verbose)


    def fetch_casting_dict(self):
	return {x['base_id.id'].lower(): self.modify_man_item(x) for x in self.fetch_casting_list()}

    def write_casting(self, values, id):
        return self.write('casting', values=values, where='id="' + id + '"', modonly=True, tag='Casting', verbose=True)

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

    paren_re = re.compile('\s*\(.*?\)\s*')
    def icon_name(self, name):
	if not name:
	    return ['']
	name = self.paren_re.sub(' ', name).replace('*', '')

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

    def modify_man_items(self, mods):
	for mod in mods:
	    self.modify_man_item(mod)
	return mods

    def modify_man_item(self, mod):
        mod = self.depref('casting', mod)
        mod = self.depref('base_id', mod)
        mod.setdefault('make', '')

        if mod.get('id'):
            mod['name'] = mod['rawname'].replace(';', ' ')
            mod['unlicensed'] = {'unl': '-', '': '?'}.get(mod['make'], ' ')
            mod.setdefault('description', '')
            mod['made'] = not (mod['flags'] & self.FLAG_MODEL_NOT_MADE)
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
        mod['linkid'] = mod.get('mod_id', mod.get('id'))
        mod['link'] = "single.cgi?id"
        mod['descs'] = filter(lambda x: x, mod['description'].split(';'))
        mod['iconname'] = self.icon_name(mod.get('rawname', ''))
        mod['shortname'] = self.short_name(mod.get('rawname', ''))
        mod['casting_type'] = mbdata.casting_types.get(mod.get('model_type', 'SF'), 'Casting')
        return mod

    #- casting_related

    def fetch_casting_related(self, mod_id, rel_id=None, section_id=None):
        wheres = ["casting_related.related_id=base_id.id"]
        wheres.append("casting_related.model_id='%s'" % mod_id)
	if section_id:
	    wheres.append("casting_related.section_id='%s'" % section_id)
	if rel_id:
	    wheres.append("casting_related.related_id='%s'" % rel_id)
        return self.fetch('casting_related,base_id', where=' and '.join(wheres), tag='CastingRelated', verbose=True)

    def fetch_casting_relateds(self, section_id=None):
	#select * from casting_related left join base_id as m on (casting_related.model_id=m.id) left join base_id as r on (casting_related.related_id=r.id) where casting_related.model_id='MB952';
	wheres = []
	if section_id:
	    wheres.append("casting_related.section_id='%s'" % section_id)
        left_joins = [("base_id as m", "casting_related.model_id=m.id")]
        left_joins += [("base_id as r", "casting_related.related_id=r.id")]
	return self.fetch('casting_related', where=' and '.join(wheres), left_joins=left_joins, tag='CastingRelateds', verbose=True)
        return self.fetch('casting_related,base_id m,base_id r', where="casting_related.related_id=r.id and casting_related.model_id=m.id", tag='CastingRelateds', verbose=True)

    def update_casting_related(self, val):
	if val['id']:
	    print 'upd', val, '<br>'
	    self.write('casting_related', values=val, where='id=%s' % val['id'], tag='UpdateCastingRelated')
	else:
	    del val['id']
	    print 'new', val, '<br>'
	    print self.write('casting_related', values=val, newonly=True, tag='UpdateCastingRelated')

    def add_casting_related(self, values):
        return self.write('casting_related', values=values, newonly=True, tag='AddCastingRelated', verbose=True)

    #- attribute

    def fetch_attributes(self, id):
        return self.fetch('attribute', where="mod_id='%s'" % id, tag='Attributes')

    def fetch_attribute(self, id):
        return self.fetch('attribute', where="id='%s'" % id, tag='Attribute')

    def delete_attribute(self, where):
        self.delete('attribute', self.make_where(where))

    def update_attribute(self, values, id):
        self.write('attribute', values, self.make_where({'id': id}), modonly=True)

    def clone_attributes(self, old_mod_id, new_mod_id):
	# insert into attribute (mod_id, attribute_name, definition, title, visual) select 'MB900', attribute_name, definition, title, visual from attribute where mod_id='MB894';
	self.raw_execute("""insert into attribute (mod_id, attribute_name, definition, title, visual) """
		"""select '%s', attribute_name, definition, title, visual from attribute """
		"""where mod_id='%s'""" % (new_mod_id, old_mod_id))

    def insert_attribute(self, mod_id, attr_name):
	rec = {"mod_id": mod_id, "attribute_name": attr_name,
	       "title": attr_name.replace('_', ' ').title(), "definition": 'varchar(64)'}
	self.write("attribute", rec, {"mod_id": mod_id, "attribute_name": attr_name})

    #- attribute_picture

    def fetch_attribute_pictures(self, id):
        ret = self.fetch('attribute_picture', left_joins=[('attribute', 'attribute.id=attribute_picture.attr_id ')],
			 where="attribute_picture.mod_id='%s'" % id, tag='AttributePictures')
	return ret

    def fetch_attribute_picture(self, id):
        return self.fetch('attribute_picture', where="id='%s'" % id, tag='AttributePicture')

    def delete_attribute_picture(self, where):
        self.delete('attribute_picture', self.make_where(where))

    def update_attribute_picture(self, values, id):
        self.write('attribute_picture', values, self.make_where({'id': id}), modonly=True)

    #- variation

    def fetch_variations_bare(self):
        return self.fetch('variation', tag='VariationsBare')

    def fetch_variations(self, id, nodefaults=False):
        varrecs = self.fetch('variation', where="mod_id='%s'" % id, tag='Variations')
        detrecs = self.fetch_details(id, nodefaults=nodefaults)
        if detrecs:
            for varrec in varrecs:
                detrec = detrecs.get(varrec['variation.var'], '')
		for key in detrec:
		    if not varrec.get('variation.' + key):
			varrec['variation.' + key] = detrec[key]
                #varrec.update(detrecs.get(varrec['variation.var'], {}))
        return varrecs

    def fetch_variation(self, id, var):
        varrecs = self.fetch('variation', where="mod_id='%s' and var='%s'" % (id, var), tag='Variation')
        detrecs = self.fetch_details(id, var)
        for var_id in detrecs:
            if var == var_id:
                varrecs[0].update(detrecs[var_id])
        return varrecs

    def fetch_variation_deconstructed(self, id, var):
        varrec = self.fetch('variation', where="mod_id='%s' and var='%s'" % (id, var), tag='VariationDeconstructed')
        detrecs = self.fetch_details(id, var, nodefaults=True)
        return varrec, detrecs

    def fetch_variation_query(self, varsq, castingq, codes=None):
        wheres = ['v.mod_id=casting.id', 'casting.id=base_id.id']
        if codes == 0:
            return list()  # ha-ha
        elif codes == 1:
            wheres.append('(v.flags & %s)=0' % self.FLAG_MODEL_CODE_2)
        elif codes == 2:
            wheres.append('(v.flags & %s)!=0' % self.FLAG_MODEL_CODE_2)
        args = list()
        cols = ['base_id.id', 'base_id.rawname', 'v.mod_id', 'v.var', 'v.text_description', 'v.text_base',
                'v.text_body', 'v.text_interior', 'v.text_wheels', 'v.text_windows', 'v.picture_id']
        for key in varsq:
            wheres.extend(["v.%s like %%s" % (key) for x in varsq[key]])
            args.extend(["%%%%%s%%%%" % (x) for x in varsq[key]])
        for key in castingq:
            wheres.extend(["casting.%s like %%s" % (key) for x in castingq[key]])
            args.extend(["%%%%%s%%%%" % (x) for x in castingq[key]])
	# turn this into a fetch
        varrecs = self.dbi.select('variation v,casting,base_id', cols, where=' and '.join(wheres), args=args)
        return varrecs

    def fetch_variation_by_select(self, mod_id, ref_id, sub_id):
        cols = ['v.text_description', 'v.picture_id', 'v.var', 'vs.ref_id', 'vs.sub_id']
        table = "variation_select vs"
        sub_id = ','.join(["'%s'" % x for x in sub_id])
        where = "vs.mod_id='%s' and vs.ref_id='%s' and vs.sub_id in (%s)" % (mod_id, ref_id, sub_id)
        table += " left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var"
	# turn this into a fetch
        return self.dbi.select(table, cols, where=where)

    def fetch_variation_files(self, mod_id):
        return self.fetch('variation', columns=['imported_from', 'mod_id'], group='imported_from', order='imported_from', where="mod_id='%s'" % mod_id, tag='VariationFiles', verbose=True)

    def insert_variation(self, mod_id, var_id, attributes={}, verbose=False):
        cols = self.table_info['variation']['columns']
        nvar = dict()
        for col in cols:
            nvar[col] = attributes.get(col, '')
        nvar['var'] = var_id
        nvar['mod_id'] = mod_id
        nvar['flags'] = 0
        self.write('variation', nvar, newonly=True, verbose=verbose)
        attribute_list = self.fetch_attributes(mod_id)
        for attr in attribute_list:
            det = {'var_id': nvar['var'], 'mod_id': mod_id, 'attr_id': attr['attribute.id'], 'description': attributes.get(attr['attribute.attribute_name'], '')}
            self.write('detail', det, newonly=True, verbose=verbose)

    def update_variation(self, attributes, where, verbose=False):
	var_cols = self.get_table_info('variation')['columns']
	new_var = {x: attributes[x] for x in (set(attributes.keys()) & set(var_cols))}
        self.write('variation', new_var, self.make_where(where, var_cols), modonly=True, verbose=verbose)
        attribute_list = self.fetch_attributes(where['mod_id'])
        for attr in attribute_list:
	    if attr['attribute.attribute_name'] in attributes:
		det = {'var_id': attributes['var'], 'mod_id': where['mod_id'], 'attr_id': attr['attribute.id'], 'description': attributes.get(attr['attribute.attribute_name'], '')}
		self.write('detail', det, verbose=verbose)

    def delete_variation(self, where):
        self.delete('variation', where=self.make_where(where))

    #- variation_select

    def fetch_variation_selects(self, mod_id, var_id=None):
        wheres = ["variation_select.mod_id='%s'" % mod_id, "variation_select.ref_id=page_info.id"]
        if var_id:
            wheres.append("variation_select.var_id='%s'" % var_id)
        left_joins = [("pack", "variation_select.sub_id=pack.id")]
        left_joins += [("base_id", "pack.id=base_id.id")]
        left_joins += [("lineup_model", "lineup_model.mod_id=variation_select.mod_id and lineup_model.page_id=variation_select.ref_id")]
        return self.fetch('variation_select,page_info', left_joins=left_joins, where=wheres, tag='VariationSelects', verbose=0)

    def update_variation_select(self):
        self.write('variation_select', {'var_id': new_var_id}, where="var_id='%s' and mod_id='%s'" % (old_var_id, mod_id), modonly=True)

    def update_variation_selects(self, mod_id, var_id, ref_ids):
        self.delete('variation_select', where="mod_id='%s' and var_id='%s'" % (mod_id, var_id))
        for ref_id in ref_ids:
            sub_id = ''
            if ref_id.find('/') >= 0:
                ref_id, sub_id = ref_id.split('/', 1)
            self.write('variation_select', {'mod_id': mod_id, 'var_id': var_id, 'ref_id': ref_id, 'sub_id': sub_id}, newonly=True, verbose=1)

    def update_variation_select_subid(self, new_sub_id, ref_id, sub_id):
        self.write('variation_select', {'sub_id': new_sub_id}, where="ref_id='%s' and sub_id='%s'" % (ref_id, sub_id), modonly=True)

    def update_variation_select_pack(self, pms, page_id=None, sub_id=None):
        if page_id and sub_id:
            self.delete('variation_select', where="ref_id='%s' and sub_id='%s'" % (page_id, sub_id))
        for pm in pms:
            if page_id and sub_id:
                for var_id in [x for x in pm['var_id'].split('/') if x]:
                    self.write('variation_select', {'mod_id': pm['mod_id'], 'var_id': var_id, 'ref_id': page_id, 'sub_id': pm['pack_id']}, newonly=True)

    def delete_variation_select(self, where):
        self.delete('variation_select', where=self.make_where(where))

    #- detail

    def delete_detail(self, where):
        self.delete('detail', where=self.make_where(where))

    def fetch_details(self, mod_id, var_id=None, nodefaults=False):
        if nodefaults:
            commondetails = {}
        else:
	    # turn this into a fetch
            commondetails = {x['attribute_name']: x['description'] for x in
                self.dbi.select('detail, attribute',
                    ['detail.mod_id', 'attr_id', 'description', 'attribute_name'],
                    "detail.mod_id='%s' and detail.attr_id=attribute.id and detail.var_id=''" % mod_id)}
        if var_id is not None:
	    # turn this into a fetch
            details = self.dbi.select('detail, attribute',
                ['detail.mod_id', 'var_id', 'attr_id', 'description', 'attribute_name'],
                "detail.mod_id='%s' and detail.var_id='%s' and detail.attr_id=attribute.id" % (mod_id, var_id))
        else:
	    # turn this into a fetch
            details = self.dbi.select('detail, attribute',
                ['detail.mod_id', 'var_id', 'attr_id', 'description', 'attribute_name'],
                "detail.mod_id='%s' and detail.attr_id=attribute.id" % mod_id)

        mvars = {}
        for det in details:
            mvars.setdefault(det['var_id'], copy.deepcopy(commondetails))
            mvars[det['var_id']][det['attribute_name']] = det['description']
        return mvars

    def update_detail(self, values, where, verbose=False):
        self.write('detail', values, where=self.make_where(where), modonly=True, verbose=verbose)

    #- vehicle_make

    def fetch_vehicle_makes(self):
        return self.fetch('vehicle_make', tag='VehicleMakes')

    #- vehicle_type

    def fetch_vehicle_types(self):
        return self.fetch('vehicle_type', tag='VehicleTypes')

    #- counter

    def fetch_counters(self):
        return self.fetch('counter', tag='Counters')

    def increment_counter(self, page_id):
        self.dbi.count(page_id)

    #- lineup_model

    def fetch_simple_lineup_models(self, year='', region='', base_id=''):
        cols = list()
        cols.extend(['lineup_model.id', 'lineup_model.base_id', 'lineup_model.mod_id', 'lineup_model.number', 'lineup_model.style_id', 'lineup_model.region', 'lineup_model.year', 'lineup_model.name', 'lineup_model.picture_id', 'lineup_model.flags'])
        cols.extend(['base_id.id', 'base_id.first_year', 'base_id.rawname', 'base_id.description', 'base_id.flags', 'base_id.model_type'])
        cols.extend(['casting.id', 'casting.scale', 'casting.vehicle_type', 'casting.country', 'casting.make', 'casting.section_id'])
        table = "lineup_model"
        table += " left join base_id on base_id.id=lineup_model.mod_id"
        table += " left join casting on casting.id=lineup_model.mod_id"
        wheres = list()
        if isinstance(region, list):
            wheres.append("lineup_model.region in (" + ','.join(["'" + x + "'" for x in region]) + ')')
        if year:
            wheres.append("lineup_model.year='" + year + "'")
        if base_id:
            wheres.append("lineup_model.base_id='" + base_id + "'")
	# turn this into a fetch
        return self.dbi.select(table, cols, where=' and '.join(wheres))

    def fetch_lineup_models(self, year='', region=''):
        cols = list()
        cols.extend(['lineup_model.id', 'lineup_model.mod_id', 'lineup_model.number', 'lineup_model.style_id', 'lineup_model.region', 'lineup_model.year', 'lineup_model.name', 'lineup_model.picture_id', 'lineup_model.flags', 'lineup_model.base_id'])
        cols.extend(['base_id.id', 'base_id.first_year', 'base_id.rawname', 'base_id.description', 'base_id.flags', 'base_id.model_type'])
        cols.extend(['casting.id', 'casting.scale', 'casting.vehicle_type', 'casting.country', 'casting.make', 'casting.section_id'])
        cols.extend(['pack.id', 'pack.page_id', 'pack.section_id', 'pack.name', 'pack.year', 'pack.region', 'pack.note'])
        cols.extend(['publication.id', 'publication.first_year', 'publication.flags', 'publication.model_type', 'publication.country', 'publication.rawname', 'publication.description', 'publication.section_id'])
        cols.extend(['page_info.id', 'page_info.flags', 'page_info.format_type', 'page_info.title'])
        table = "lineup_model"
        table += " left join base_id on base_id.id=lineup_model.mod_id"
        table += " left join casting on casting.id=lineup_model.mod_id"
        table += " left join pack on pack.id=lineup_model.mod_id"
        table += " left join publication on publication.id=lineup_model.mod_id"
        table += " left join page_info on page_info.id=lineup_model.mod_id"
        wheres = list()
        if isinstance(region, list):
            wheres.append("lineup_model.region in (" + ','.join(["'" + x + "'" for x in region]) + ')')
        if year:
            cols.extend(['v.text_description', 'v.picture_id', 'v.var', 'vs.ref_id', 'vs.sub_id'])
            table += " left join variation_select vs on (vs.ref_id='year.%s')" % year
            table += " and vs.mod_id=lineup_model.mod_id"
            table += " left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var"
            wheres.append("lineup_model.year='" + year + "'")
	# turn this into a fetch
        return self.dbi.select(table, cols, where=' and '.join(wheres))

    def fetch_lineup_models_by_rank(self, rank, syear, eyear):
        cols = [
            'base_id.id', 'base_id.first_year', 'base_id.rawname', 'base_id.description', 'base_id.flags', 'base_id.model_type',
            'casting.id', 'casting.first_year', 'casting.scale', 'casting.vehicle_type', 'casting.country',
            'casting.make', 'casting.section_id',
            'lineup_model.id', 'lineup_model.mod_id', 'lineup_model.number', 'lineup_model.style_id', 'lineup_model.page_id',
            'lineup_model.region', 'lineup_model.year', 'lineup_model.name', 'lineup_model.picture_id',
            'v.text_description', 'v.picture_id', 'v.var', 'vs.ref_id', 'vs.sub_id']
        table = "base_id,casting,lineup_model"
        table += " left join variation_select vs on vs.ref_id=lineup_model.page_id and vs.mod_id=lineup_model.mod_id"
        table += " left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var"
        where = "lineup_model.number=%s" % rank
        where += " and lineup_model.year>=%s" % syear
        where += " and lineup_model.year<=%s" % eyear
        where += " and casting.id=lineup_model.mod_id"
        where += " and base_id.id=casting.id"
	# turn this into a fetch
        return self.dbi.select(table, cols, where=where)

    def fetch_lineup_years(self):
	# turn this into a fetch
        return self.dbi.select("lineup_model", ["year"], group="year")

    def fetch_casting_lineups(self, mod_id):
        where = "lineup_model.mod_id='%s'" % mod_id
        left_joins = [('section', 'section.page_id=lineup_model.page_id and section.id=lineup_model.region'),
                    ('page_info', 'page_info.id=lineup_model.page_id')]
        return self.fetch("lineup_model", left_joins=left_joins, where=where, tag='CastingLineups')

    def fetch_lineup_model(self, where, verbose=None):
        return self.fetch('lineup_model', where=where, tag='LineupModel', verbose=verbose)

    def insert_lineup_model(self, values):
	print values, '<br>'
        self.write('lineup_model', self.make_values('lineup_model', values), newonly=True, verbose=True, tag='InsertLineupModel')

    def update_lineup_model(self, where, values):
	print where, values, '<br>'
        self.write('lineup_model', self.make_values('lineup_model', values), self.make_where(where), modonly=True, verbose=True, tag='UpdateLineupModel')

    def delete_lineup_model(self, where):
        self.delete('lineup_model', self.make_where(where))

    #- region

    def fetch_regions(self):
        regs = self.fetch('region', tag='Regions')
        return {x['id']: x['name'] for x in regs}, {x['id']: x['parent'] for x in regs}

    #- matrix_model

    def fetch_matrix_models(self, page_id, section=None):
        where = "page_id='" + page_id + "'"
        if section:
            where += " and section_id='" + section + "'"
        return self.fetch('matrix_model', where=where, order='display_order', tag='MatrixModels')

    #select * from casting,lineup_model where casting.id=lineup_model.mod_id and lineup_model.year='2006'
    '''
select * from casting,lineup_model
left join variation_select vs on vs.ref_id='year.2006' and vs.mod_id=lineup_model.mod_id left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var
where casting.id=lineup_model.mod_id and lineup_model.year='2006';
    '''

    '''
select
casting.id,casting.first_year,casting.scale,casting.vehicle_type,casting.country,casting.rawname,casting.description,casting.make,casting.flags,casting.section_id,matrix_model.id,matrix_model.mod_id,casting.model_type,matrix_model.section_id,matrix_model.display_order,matrix_model.page_id,matrix_model.range_id,matrix_model.name,matrix_model.subname,matrix_model.description,v.text_description,v.picture_id,v.var,vs.ref_id
from matrix_model left join casting on (casting.id=matrix_model.mod_id) left join variation_select vs on (vs.ref_id='matrix.codered') and vs.mod_id=matrix_model.mod_id left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var where matrix_model.page_id='matrix.codered'
    '''


    # Have to change this to: select matrix_model outer join casting outer join variation_select.
    def fetch_matrix_models_variations(self, page_id, section=None):
        cols = [
            'base_id.id', 'base_id.first_year', 'base_id.model_type', 'base_id.rawname', 'base_id.description', 'base_id.flags',
            'casting.id', 'casting.scale', 'casting.vehicle_type', 'casting.country', 'casting.make', 'casting.section_id',
            'matrix_model.id', 'matrix_model.mod_id', 'matrix_model.flags', 'matrix_model.section_id',
            'matrix_model.display_order', 'matrix_model.page_id', 'matrix_model.range_id', 'matrix_model.name',
            'matrix_model.subname', 'matrix_model.description', 'matrix_model.shown_id']
        table = "matrix_model"
        cols.extend(['v.text_description', 'v.picture_id', 'v.var', 'vs.ref_id', 'vs.sub_id'])
        table += " left join base_id on (base_id.id=matrix_model.mod_id)"
        table += " left join casting on (casting.id=matrix_model.mod_id)"
        table += " left join variation_select vs on (vs.ref_id='%s'" % page_id
        #table += " or vs.ref_id like '%s.%%'" % page_id
        table += ") and vs.mod_id=matrix_model.mod_id left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var"
        where = "matrix_model.page_id='" + page_id + "'"
	# turn this into a fetch
        return self.dbi.select(table, cols, where=where, order='matrix_model.display_order')

    def fetch_matrix_appearances(self, mod_id):
        where = "page_info.id like 'matrix.%%' and page_info.id=matrix_model.page_id and section.id=matrix_model.section_id and matrix_model.mod_id='%s'" % mod_id
	# turn this into a fetch
        return self.dbi.select('matrix_model, page_info, section', ['matrix_model.section_id', 'page_info.id', 'page_info.title', 'page_info.description', 'page_info.flags', 'section.name'], where)

    #- link_line

    def delete_link_line(self, id):
        self.delete('link_line', where="id=%s" % id)

    def update_link_line(self, rec):
        self.write('link_line', rec, 'id=%s' % rec['id'], modonly=True, tag='update_link_line')

    def insert_link_line(self, rec):
        return self.write('link_line', rec, newonly=True, tag='insert_link_line')

    def fetch_link_line(self, id):
	# turn this into a fetch
        link = self.dbi.select('link_line', where="id='%s'" % id)
	return link[0] if link else None

    def fetch_link_lines(self, page_id=None, section=None, where=None, order=None):
        wheres = list()
        if where:
            wheres.append(where)
        if page_id:
            wheres.append("page_id='" + page_id + "'")
        if section:
            wheres.append("section_id='" + section + "'")
        return self.fetch('link_line', where=" and ".join(wheres), order=order, tag='LinkLines')

    def fetch_links_single(self, page_id=None):
        columns = ['l1.page_id', 'l1.associated_link', 'l1.url', 'l1.name', 'l2.id', 'l2.name', 'l2.url', 'l1.flags']
        wheres = ['not l1.flags & 1']
        if page_id:
            wheres.append("l1.page_id='" + page_id + "'")
        wheres.append('l1.associated_link=l2.id')
        return self.fetch('link_line l1, link_line l2', columns=columns, where=" and ".join(wheres), tag='LinksSingle', order="l1.display_order")

    #- blacklist

    def fetch_blacklist(self):
        return self.fetch('blacklist', tag='Blacklist')

    #- publication

    def fetch_publication(self, id):
        return self.fetch('publication,base_id', where="base_id.id=publication.id and base_id.id='%s'" % id, tag='Publication')

    def fetch_publications(self):
        return self.fetch('publication,base_id', where="base_id.id=publication.id", tag='Publications')

    #- pack

    def fetch_pack(self, id):
        return self.fetch('pack,base_id', where="pack.id='%s' and base_id.id='%s'" % (id, id), tag='Pack')

    def fetch_packs(self, page_id='', year='', region=''):
        wheres = ["base_id.id=pack.id"]
        if year:
            wheres.append("year='" + year + "'")
        if region:
            wheres.append("region='" + region + "'")
        if page_id:
            wheres.append("page_id='" + page_id + "'")
        return self.fetch('base_id,pack', where=' and '.join(wheres), tag='Packs')

    def add_new_pack(self, values):
        return self.write('pack', values, newonly=True)

    def insert_pack(self, pack_id, page_id=None):
        section_id = None
        if page_id:
            section_id = page_id[page_id.rfind('.') + 1:]
        self.write('base_id', {'id': pack_id}, newonly=True)
        return self.write('pack', {'id': pack_id, 'page_id': page_id, 'section_id': section_id}, newonly=True)

    def delete_pack(self, id):
        self.delete('pack', "id='%s'" % id)

    def fetch_packs_related(self, id):
        cols = [
            'base_id.id', 'base_id.first_year', 'base_id.model_type', 'base_id.rawname', 'base_id.description', 'base_id.flags',
            'pack.id', 'pack.page_id', 'pack.section_id', 'pack.name', 'pack.year', 'pack.region', 'pack.layout', 'pack.product_code', 'pack.material', 'pack.country', 'pack.note']
        tables = ['casting_related', 'base_id', 'pack']
        wheres = ["casting_related.model_id='%s'" % id, "casting_related.related_id=base_id.id", "casting_related.related_id=pack.id"]
        return self.fetch(tables, columns=cols, where=wheres, tag='PacksRelated')

    def update_pack(self, id, values):
        self.write('pack', self.make_values('pack', values), "id='%s'" % id, modonly=True)

    #- pack_model

    def insert_pack_model(self, pack_id):
        return self.raw_execute("insert into pack_model (pack_id,display_order) select'%s', 1+count(*) from pack_model where pack_id='%s'" % (pack_id, pack_id))

    def add_new_pack_models(self, pms):
        for pm in pms:
            self.write('pack_model', pm)

    def update_pack_models(self, pms):
        for pm in pms:
            self.write('pack_model', pm, where="id=%s" % pm['id'], modonly=True)

    def fetch_pack_model(self, id):
        return self.fetch('pack_model', where='id=%s' % id, tag='PackModel')

#select page_info.title,page_info.pic_dir,style.style_type, style.style_setting
#from page_info left outer join style on page_info.id=style.page_id
#where page_info.id='newpage';

    '''
select
casting.id, casting.first_year, casting.scale, casting.vehicle_type, casting.country, casting.rawname, casting.description,
casting.make, casting.flags, casting.section_id, casting.model_type,
matrix_model.id, matrix_model.mod_id, matrix_model.section_id, matrix_model.display_order, matrix_model.page_id,
matrix_model.range_id, matrix_model.name, matrix_model.subname, matrix_model.description,
v.text_description, v.picture_id, v.var, vs.ref_id
from matrix_model
left join casting on (casting.id=matrix_model.mod_id)
left join variation_select vs on (vs.ref_id='matrix.codered') and vs.mod_id=matrix_model.mod_id
left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var
where matrix_model.page_id='matrix.codered'

select
pack.id,
pack.page_id, pack.section_id, pack.name, pack.year, pack.region, pack.layout, pack.product_code, pack.material, pack.country,
pack_model.mod_id, pack_model.pack_id,
casting.id, casting.rawname,
vs.ref_id, vs.mod_id, vs.var_id, v.text_description, v.picture_id
from pack, pack_model
left join casting on (casting.id=pack_model.mod_id)
left join variation_select vs on (vs.ref_id='pack.5pack.bea01') and vs.mod_id=pack_model.mod_id
left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var
where pack.id=pack_model.pack_id and pack_model.mod_id=casting.id and pack.id='bea01';

'''

    def fetch_pack_models(self, pack_id='', year='', region='', page_id='', sub_id=''):

        wheres = ['pack.id=pack_model.pack_id']
        cols = [
            'base_id.id', 'base_id.first_year', 'base_id.flags', 'base_id.model_type', 'base_id.rawname', 'base_id.description',
            'pack.id', 'pack.page_id', 'pack.section_id', 'pack.name', 'pack.year', 'pack.region', 'pack.layout',
            'pack.product_code', 'pack.material', 'pack.country',
            'pack_model.id', 'pack_model.mod_id', 'pack_model.pack_id', 'pack_model.var_id', 'pack_model.display_order',
            'casting.id', 'casting.first_year', 'casting.scale', 'casting.model_type', 'casting.vehicle_type', 'casting.country',
            'casting.rawname', 'casting.description', 'casting.make', 'casting.section_id',
            'vs.ref_id', 'vs.sub_id', 'vs.mod_id', 'vs.var_id', 'v.text_description', 'v.picture_id']
        if pack_id:
            wheres.append("pack.id='" + pack_id + "'")
        if year:
            wheres.append("pack.year='" + year + "'")
        if region:
            wheres.append("pack.region='" + region + "'")
        froms = "pack, pack_model " + \
                "left join base_id on pack_model.mod_id=base_id.id " + \
                "left join casting on pack_model.mod_id=casting.id " + \
                "left join variation_select vs on (vs.ref_id='%s' and vs.sub_id like '%s%%' and vs.mod_id=pack_model.mod_id)" % (page_id, pack_id)
        if page_id:
            if pack_id:
                froms += " and vs.ref_id='%s' and vs.sub_id like '%s%%'" % (page_id, pack_id)
            else:
                froms += " and vs.ref_id='%s'" % page_id
        froms += " left join variation v on (vs.mod_id=v.mod_id and vs.var_id=v.var)"
        return self.fetch(froms, columns=cols, where=" and ".join(wheres), tag='PackModels')

        pack_model_query = '''
select
pack.page_id, pack.section_id, pack.name, pack.year, pack.region, pack.layout, pack.product_code, pack.material, pack.country,
pack_model.mod_id, pack_model.pack_id,
casting.id, casting.rawname,
vs.ref_id, vs.mod_id, vs.var_id, v.text_description, v.picture_id
from casting, pack, pack_model
left join variation_select vs on (vs.ref_id='%s.%s' and vs.mod_id=pack_model.mod_id)
left join variation v on (vs.mod_id=v.mod_id and vs.var_id=v.var)
where pack.id=pack_model.pack_id and pack_model.mod_id=casting.id and pack.id='%s'
'''
	# turn this into a fetch
        return self.dbi.rawquery(pack_model_query % (page_id, pack_id, pack_id))

    def fetch_pack_model_appearances(self, mod_id):
        return self.fetch('pack, pack_model, page_info, base_id', columns=['pack.id', 'base_id.id', 'base_id.rawname', 'base_id.first_year', 'pack.region', 'pack.layout', 'page_info.title', 'pack.section_id'], where="pack.id=base_id.id and pack_model.mod_id='%s' and pack_model.pack_id=pack.id and page_info.id=pack.page_id" % mod_id, tag='PackModelAppearances')

    def delete_pack_models(self, ref_id, pack_id):
        self.delete('pack_model', "pack_id='%s'" % pack_id)
        self.delete('variation_select', where="ref_id='%s' and sub_id='%s'" % (ref_id, pack_id))

    #- casting_compare

    def fetch_casting_compare(self, mod_id):
        where = "mod_id='%s' or compare_id='%s'" % (mod_id, mod_id)
        return len(self.fetch('casting_compare', where=where, tag='CastingCompare')) > 0

#select cc.id,cc.mod_id,cc.compare_id,cc.section_id,cc.description,c1.id,c1.rawname,c2.id,c2.rawname from casting_compare cc left join casting c1 on (cc.mod_id=c1.id) left join casting c2 on (cc.compare_id=c2.id) ;
    def fetch_casting_compares(self, section_id=None):
        columns = ['cc.id', 'cc.mod_id', 'cc.compare_id', 'cc.section_id', 'cc.description', 'c1.rawname', 'c2.rawname']
        where = 'cc.mod_id=c1.id'
        if section_id:
            where += " and cc.section_id='%s'" % section_id
        table = 'casting_compare cc left join base_id c1 on (cc.mod_id=c1.id) left join base_id c2 on (cc.compare_id=c2.id)'
        return self.fetch(table, columns=columns, where=where, tag='CastingCompares')

    #- user

    def fetch_user(self, id=None, name=None, vkey=None):
        where = list()
        if id:
            where.append("id=%s" % id)
        if name:
            where.append("name='%s'" % name)
        if vkey:
            where.append("vkey='%s'" % vkey)
        return self.fetch('user', where=' and '.join(where), tag='User')

    def fetch_users(self):
        return self.fetch('user', tag='Users')

    def login(self, name, passwd):
        return self.dbi.login(name, passwd)

    def create_user(self, name, passwd, email, vkey):
        return self.dbi.createuser(name, passwd, email, vkey)

    def update_user(self, id, name=None, email=None, passwd=None, privs=None, state=None):
        #'columns': ['id', 'name', 'passwd', 'privs', 'email', 'state', 'vkey'],
        values = {}
        if name is not None:
            values['name'] = name
        if email is not None:
            values['email'] = email
        if passwd is not None:
            values['passwd'] = "PASSWORD('%s')" % passwd
        if state is not None:
            values['state'] = int(state)
        if privs is not None:
            values['privs'] = privs
        self.write('user', values, "id=%s" % id, modonly=True)

    def delete_user(self, id):
        self.delete('user', 'id=%s' % id)

    #- site_activity

    def fetch_activities(self):
        return self.fetch('site_activity,user', where='site_activity.by_user_id=user.id')
    #def fetch(self, table_name, left_joins=None, columns=None, where=None, group=None, order=None, tag='', verbose=False):

    def insert_activity(self, name, user_id, description='', url='', image='', timestamp=None):
        oldrow = self.fetch('site_activity', columns=['id'], order='id desc limit 98,1', tag='insert_activity')
        if oldrow:
            oldrow = oldrow[0]['id']
        else:
            oldrow = 1
        self.raw_execute('''delete from site_activity where id < %d''' % oldrow, 'insert_activity')
        rec = {'name': name, 'description': description, 'url': url, 'image': image, 'by_user_id': user_id}
        if timestamp:
            rec['timestamp'] = timestamp
        return self.write('site_activity', rec, newonly=True, tag='insert_activity', verbose=True)

    def delete_activity(self, id):
        self.delete('site_activity', where=self.make_where({'id': id}), tag='delete_activity')

    #- miscellaneous

    #select detail.mod_id, detail.var_id,attribute.attribute_name, detail.description from detail,attribute where detail.attr_id=attribute.id and attribute.attribute_name like '%wheel%' and description like '%front%' order by detail.mod_id;
    #select distinct description from detail,attribute where detail.attr_id=attribute.id and attribute.attribute_name like '%wheel%';
    # ----- from mkdesc.py ------------------------------------

    # [?][*=&]attr[^prepend][+append][#default]
    # ?... = attribute is optional: "no", "-", or missing just omits it.
    # *attr = value attr
    # =attr = attr value
    # &attr = value
    # ^prepend = prepended text
    # +append = appended text
    # #default if value is blank
    def parse_detail_format(self, fmt):
	attr_re = re.compile(r'%\((?P<a>[^)]*)\)s')
	is_opt = False
	attr_name = fmt_prepend = fmt_append = default = ''

	if fmt.startswith('?'):
	    is_opt = True
	    fmt = fmt[1:]

	if fmt.find('#') >= 0:
	    default = fmt[fmt.find('#') + 1:]
	    fmt = fmt[:fmt.find('#')]

	if fmt.find('+') >= 0:
	    fmt_append = fmt[fmt.find('+') + 1:]
	    fmt = fmt[:fmt.find('+')]
	if fmt.find('^') >= 0:
	    fmt_prepend = fmt[fmt.find('^') + 1:]
	    fmt = fmt[:fmt.find('^')]

	if fmt.startswith('*'):
	    attr_name = fmt[1:]
	    fmt = '%%(%s)s %s' % (attr_name, attr_name.replace('_', ' '))
	elif fmt.startswith('='):
	    attr_name = fmt[1:]
	    fmt = '%s %%(%s)s' % (attr_name.replace('_', ' '), attr_name)
	elif fmt.startswith('&'):
	    attr_name = fmt[1:]
	    fmt = '%%(%s)s' % attr_name
	elif '%' in fmt:  # raw format
	    # MI818 still needs this, at the least.
	    attr_m = attr_re.search(fmt)
	    if attr_m:
		attr_name = attr_m.group('a')
	else:  # literal string
	    attr_name = None
	return attr_name, fmt, default, fmt_prepend, fmt_append, is_opt

    def recalc_description(self, mod_id, showtexts=False, verbose=False):
	cols = ['description', 'body', 'base', 'wheels', 'interior', 'windows']

	# I apologize in advance for this function.
	def fmt_desc(var, casting, field, verbose):

	    def fmt_detail(var, fmt, verbose):
		attr_name, fmt, default, fmt_prepend, fmt_append, is_opt = self.parse_detail_format(fmt)
		if attr_name:
		    if attr_name not in var:
			if verbose:
			    print '!', attr_name
			return ''
		    value = var.get(attr_name)
		    if not value or (is_opt and (value == 'no' or value == '-')):
			return default
		fmt = fmt_prepend + ' ' + fmt + ' ' + fmt_append
		return fmt.strip()

	    fmts = [y for y in [fmt_detail(var, x, verbose) for x in casting[field].split('|')] if y]
	    descs = []
	    for fmt in fmts:
		desc = ''
		try:
		    desc = fmt % var
		except:
		    if verbose:
			print '!', field, fmt
		if descs and descs[-1] == desc:
		    continue
		descs.append(desc)
	    return ', '.join(descs)

	textcols = ['text_' + x for x in cols]
	casting = self.fetch_casting(mod_id, extras=True)
	vars = self.depref('variation', self.fetch_variations(mod_id))
	for var in vars:
	    if verbose:
		print var['var']
	    ovar = {x: '' for x in textcols}
	    ovar.update({'text_' + x: fmt_desc(var, casting, 'format_' + x, verbose) for x in cols})
	    if showtexts:
		for x in cols:
		    print ' ', x[:2], ':', ovar['text_' + x]
	    self.update_variation(ovar, {'mod_id': var['mod_id'], 'var': var['var']})

    def check_description_formatting(self, mod_id, linesep=''):
	cas_cols = ['format_description', 'format_body', 'format_base', 'format_wheels', 'format_interior', 'format_windows']
	var_cols = ['base', 'body', 'interior', 'windows', 'manufacture']
	casting = self.fetch_casting(mod_id, extras=True)
	attributes = var_cols + [x['attribute.attribute_name'] for x in self.fetch_attributes(mod_id)]
	messages = ''
	retval = False
	for cas_col in cas_cols:
	    if casting[cas_col]:
		for fmt in casting[cas_col].split('|'):
		    attr = self.parse_detail_format(fmt)[0]
		    if attr and not attr in attributes:
			messages += '%s ! %s %s%s\n' % (mod_id, cas_col, fmt, linesep)
			retval = True
	for attr in attributes:
	    if attr == 'from_CY_number':
		continue
	    found = False
	    attr_re = re.compile(r'\b%s\b' % attr)
	    for col in cas_cols[1:]:  # ignore description for this check
		attr_m = attr_re.search(casting[col])
		if attr_m:
		    found = True
		    messages += '%s + %s%s\n' % ( mod_id, attr, linesep)
		    break
	    if not found:
		messages += '%s - %s%s\n' % ( mod_id, attr, linesep)
		retval = True
	return retval, messages


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''