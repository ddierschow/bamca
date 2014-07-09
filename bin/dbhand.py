#!/usr/local/bin/python

import copy, re, sys
import db
import mbdata
import tables

linkurl = [
        None,
        "single.cgi?id",
#        "vars.cgi?category=MB&submit.x=1&submit.y=1&mod",
#        "http://mb-db.co.uk/showcar.php?num",
#        "http://www.mbxforum.com/11-Catalogs/00-Software/jnmb75da.php?uSleutel=&uNumber",
#        "http://images.google.com/images?hl=en&um=1&ie=UTF-8&sa=N&tab=wi&q",
#        "traverse.cgi?d=./vars/"
]

id_re = re.compile('''(?P<a>[a-zA-Z]*)(?P<d>\d*)''')


class dbhandler:
    table_info = tables.table_info
    def __init__(self, config, user_id, verbose):
	self.dbi = db.db(config, user_id, verbose)
	if not self.dbi:
	    raise 'DB connect failed'
	#self.table_info = tables.table_info
	self.SetConstants()

    def __repr__(self):
	return "'<dbhand.dbhandler instance>'"

    def __str__(self):
	return "'<dbhand.dbhandler instance>'"

    def ErrorReport(self):
	return str(self.__dict__) + '\n' + 'dbi = ' + str(self.dbi.__dict__)

    def SetVerbose(self, flag):
	self.dbi.verbose = flag

    def escape_string(self, s):
	return self.dbi.escape_string(s)

    def MakeValues(self, table, values):
	return {x: values.get(x, '') for x in self.GetTableInfo(table)['columns']}

    def GetFormTableInfo(self, pif, table=None):
	if not table:
	    table = pif.FormStr('table')
	if not table:
	    return None
	table_info = self.table_info[table]
	table_info['name'] = table
	return table_info

    def GetTableInfo(self, table):
	table_info = self.table_info[table]
	table_info['name'] = table
	return table_info

    def GetEditorLink(self, pif, table, args):
	table_info = self.GetFormTableInfo(pif, table)
	url = '/cgi-bin/editor.cgi?table=%s' % table
	if table_info:
	    for key in args:
		if key in table_info['columns']:
		    url += '&%s=%s' % (key, args[key])
	return url

    def TableCols(self, table):
	return [table + '.' + x for x in self.table_info[table]['columns']]

    def SetConstants(self):
	for key in tables.__dict__:
	    if key.startswith('FLAG_'):
		self.__dict__[key] = tables.__dict__[key]

    def MakeWhere(self, form, cols=None, prefix=""):
	if not cols:
	    cols = form.keys()
	wheres = list()
	for col in cols:
	    if prefix + col in form:
		wheres.append(col + "='" + str(form.get(prefix + col, '')) + "'")
	return ' and '.join(wheres)

    def RawExecute(self, query, tag=''):
	return self.dbi.execute(query, tag=tag)

#    def RawFetch(self, query, tag=''):
#	return self.dbi.rawquery(query, tag=tag)

    def MakeColumns(self, tab, tag=None):
	if not tag:
	    tag = tab
	columns = list()
	if tab in self.table_info:
	    columns.extend([tag + '.' + x for x in self.table_info[tab]['columns']])
	else:
	    columns.append(tag + '.*')
	return columns

    def Fetch(self, table_name, left_joins=None, columns=None, where=None, group=None, order=None, tag='', verbose=False):
	if not columns:
	    if isinstance(table_name, str):
		table_name = table_name.split(',')
	    columns = list()
	    for tab in table_name:
		if ' ' in tab:
		    columns.extend(self.MakeColumns(tab[:tab.find(' ')], tab[tab.find(' ') + 1:]))
		else:
		    columns.extend(self.MakeColumns(tab))
	    table_name = ','.join(table_name)
	if isinstance(where, list):
	    where = ' and '.join(where)
	elif isinstance(where, dict):
	    where = self.MakeWhere(where)
	if left_joins:
	    table_name = '(%s)' % table_name
	    for lj in left_joins:
		table_name += ' left join %s on (%s)' % tuple(lj)
		columns.extend([lj[0] + '.' + x for x in self.table_info[lj[0]]['columns']])
	return self.dbi.select(table_name, columns, where=where, group=group, order=order, tag=tag, verbose=verbose)

    def DescribeDict(self, table):
	return {x['field']: x for x in self.Describe(table)}

    def Describe(self, table):
	return self.dbi.describe(table)

    def Columns(self, table):
	return [x['field'] for x in self.Describe(table)]

    def DePref(self, table, results):
	if isinstance(results, dict):
	    for key in results.keys():
		if key.startswith(table + '.'):
		    results[key[len(table) + 1:]] = results[key]
		    del results[key]
	else:
	    for result in results:
		self.DePref(table, result)
	return results

    def Increment(self, table_name, values=None, where=None, tag='', verbose=False):
	values = {x: x + '+1' for x in values}
	return self.dbi.updateraw(table_name, values, where, tag=tag, verbose=verbose)

    def Write(self, table_name, values=None, where=None, newonly=False, modonly=False, tag='', verbose=False):
	if newonly:
	    return self.dbi.insert(table_name, values, tag=tag, verbose=verbose)
	elif modonly:
	    return self.dbi.update(table_name, values, where, tag=tag, verbose=verbose)
	else:
	    return self.dbi.insert_or_update(table_name, values, tag=tag, verbose=verbose)

    def Delete(self, table, where=None, tag='', verbose=None):
	return self.dbi.remove(table, where, tag=tag, verbose=verbose)

    # end dbi interface section

    #- page_info

    def FetchPage(self, id, verbose=False):
	return self.Fetch('page_info', where={'id' : id}, tag='Page', verbose=verbose)

    def FetchPages(self, where, columns=None, group=None):
	return self.Fetch('page_info', columns=columns, where=where, group=group, tag='Pages')

    def FetchPageYears(self):
	return self.Fetch('page_info,lineup_model',
		columns=self.MakeColumns('page_info') + ['max(lineup_model.number)'],
		where=['page_info.id=lineup_model.page_id', "page_info.id like 'year.%'"],
		group="page_info.id", tag='PageYears')
# select page_info.id, max(lineup_model.number) from page_info, lineup_model where page_info.id=lineup_model.page_id and page_info.id like 'year.%' group by page_info.id;

    def SetHealth(self, page_id, verbose=False):
	#return self.Write('page_info', {'health' : 1}, "id='%s'" % page_id, modonly=True, verbose=verbose)
	return self.Increment('page_info', ['health'], "id='%s'" % page_id, tag='Health', verbose=verbose)

    def ClearHealth(self):
	self.Write('page_info', {'health': 0}, modonly=True)

    #- country

    def FetchCountries(self):
	return self.Fetch('country')

    #- section

    def FetchSection(self, id):
	secs = self.Fetch('section', where={'id' : id}, tag='Section')
	if secs:
	    return secs[0]
	return None

    def FetchSections(self, where=None):
	return self.Fetch('section', where=where, order='display_order', tag='Sections')

    #- base_id

    def FetchBaseIDs(self):
	return self.Fetch('base_id', tag='BaseIDs')

    def FetchBaseID(self, id):
	return self.Fetch('base_id', where="id='%s'" % id, tag='BaseID')

    def RenameBaseID(self, old_mod_id, new_mod_id):
	self.Write('base_id', {'id' : new_mod_id}, where="id='%s'" % old_mod_id, modonly=True)
	self.Write('casting', {'id' : new_mod_id}, where="id='%s'" % old_mod_id, modonly=True)
	self.Write('pack', {'id' : new_mod_id}, where="id='%s'" % old_mod_id, modonly=True)
	self.Write('publication', {'id' : new_mod_id}, where="id='%s'" % old_mod_id, modonly=True)
	self.Write('alias', {'ref_id' : new_mod_id}, where="ref_id='%s'" % old_mod_id, modonly=True)
	self.Write('attribute', {'mod_id' : new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
	self.Write('attribute_picture', {'mod_id' : new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
	self.Write('casting_compare', {'mod_id' : new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
	self.Write('casting_compare', {'compare_id' : new_mod_id}, where="compare_id='%s'" % old_mod_id, modonly=True)
	self.Write('casting_related', {'model_id' : new_mod_id}, where="model_id='%s'" % old_mod_id, modonly=True)
	self.Write('casting_related', {'related_id' : new_mod_id}, where="related_id='%s'" % old_mod_id, modonly=True)
	self.Write('detail', {'mod_id' : new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
	self.Write('lineup_model', {'mod_id' : new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
	self.Write('matrix_model', {'mod_id' : new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
	self.Write('pack_model', {'pack_id' : new_mod_id}, where="pack_id='%s'" % old_mod_id, modonly=True)
	self.Write('pack_model', {'mod_id' : new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
	self.Write('variation', {'mod_id' : new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
	self.Write('variation_select', {'mod_id' : new_mod_id}, where="mod_id='%s'" % old_mod_id, modonly=True)
	self.Write('variation_select', {'sub_id' : new_mod_id}, where="sub_id='%s'" % old_mod_id, modonly=True)
	self.Write('link_line', {'page_id' : 'single.' + new_mod_id}, where="page_id='single.%s'" % old_mod_id, modonly=True)

    def UpdateBaseId(self, id, values):
	self.Write('base_id', self.MakeValues('base_id', values), "id='%s'" % id, modonly=True)

    #- alias

    def FetchAlias(self, id):
	alist = self.Fetch("casting,alias,base_id", where=["casting.id=alias.ref_id", "alias.id='%s'" % id, "casting.id=base_id.id"], tag='Alias')
	if alist:
	    return alist[0]
	return {}

    def FetchCastingsByBox(self, series, style):
	wheres = ['casting.id=base_id.id']
	if series:
	    wheres.append("base_id.model_type='%s'" % series)
	if style:
	    wheres.append("box_style.styles like '%%%s%%'" % style)
	fet1 = self.Fetch('box_style,casting,base_id', where=['box_style.id=casting.id'] + wheres, tag='CastingsByBox', verbose=0)

	#ljoins = [('alias', "base_id.id=alias.ref_id")] # and alias.section_id != ''")]
	wheres = ['box_style.id=alias.id', 'alias.ref_id=casting.id'] + wheres
	fet2 = self.Fetch('box_style,alias,casting,base_id', where=wheres, tag='CastingsByBox', verbose=0)
	return fet1 + fet2

    def FetchCastingByAlias(self, id):
	#manlist = self.dbi.select('alias,casting left outer join vehicle_make on casting.make=vehicle_make.make', where="casting.id=alias.ref_id and alias.id='%s'" % id)
	manlist = self.Fetch('alias,casting', left_joins=[('vehicle_make', 'casting.make=vehicle_make.make')], where="casting.id=alias.ref_id and alias.id='%s'" % id, tag='CastingByAlias')
	if manlist:
	    return self.ModifyManItem(manlist[0])
	return {}

    def FetchCastingsByAlias(self, id):
	#return self.dbi.select('alias,casting left outer join vehicle_make on casting.make=vehicle_make.make', where="casting.id=alias.ref_id and alias.id='%s'" % id)
	return self.Fetch('alias,casting', left_joins=[('vehicle_make', 'casting.make=vehicle_make.make')], where="casting.id=alias.ref_id and alias.id='%s'" % id, tag='CastingsByAlias')

    def FetchAliases(self, ref_id=None, type_id=None, where=None):
	wheres = ["base_id.id=casting.id", "casting.id=alias.ref_id"]
	if ref_id:
	    wheres.append("alias.ref_id='%s'" % ref_id)
	if type_id:
	    wheres.append("alias.type='%s'" % type_id)
	if isinstance(where, list):
	    wheres += where
	elif isinstance(where, str):
	    wheres.append(where)
	return self.Fetch("base_id,casting,alias", where=wheres, tag='Aliases')

    #- casting

    def FetchCasting(self, id):
	#manlist = self.Fetch('casting, vehicle_make', where="id='%s' and casting.make=vehicle_make.make" % id)
	#manlist = self.dbi.select('casting left outer join vehicle_make on casting.make=vehicle_make.make', where="id='%s'" % id)
	wheres = ['base_id.id=casting.id', 'casting.id="%s"' % id]
	manlist = self.Fetch("casting,base_id", left_joins=[("vehicle_make", "casting.make=vehicle_make.make")], where=wheres, tag='Casting')
	if manlist:
	    return self.ModifyManItem(manlist[0])
	return {}

    def FetchCastingList(self, section_id=None, page_id=None, where=None, verbose=False):
	wheres = ['base_id.id=casting.id', 'casting.section_id=section.id']
	if page_id:
	    wheres.append('section.page_id="%s"' % page_id)
	if isinstance(where, list):
	    wheres += where
	elif isinstance(where, str):
	    wheres.append(where)
	if section_id:
	    wheres.append('section.id="%s"' % section_id)
	return self.Fetch('base_id,casting,section', where=wheres, tag='CastingList', verbose=verbose)

    def WriteCasting(self, values, id):
	return self.Write('casting', values=values, where='id="' + id + '"', modonly=True, tag='Casting', verbose=True)

    def ManListToMans(self, manlist):
	mans = {}
	for llist in manlist:
	    man = self.ModifyManItem(llist)
	    mans[man['id']] = man
	return mans

    def ShortName(self, name):
	if not name:
	    return ''
	if name[0] == '(':
	    name = name[name.find(')') + 2:]
	if '(' in name:
	    name = name[:name.find('(') - 1] + name[name.find(')') + 1:]
	name = name.replace(';', ' ')
	if name[0] == '-':
	    name = name[1:]
	if name[-1] == '/':
	    name = name[:-1]
	if name[-1] == '-':
	    name = name[:-1]
	name = name.strip().replace('*', '')
	return name

    def IconName(self, name):
	if not name:
	    return ''
	if name[0] == '(':
	    name = name[name.find(')') + 2:]
	if '(' in name:
	    name = name[:name.find('(') - 1] + name[name.find(')') + 1:]
	names = list()
	for n in name.split(';'):
	    if n[0] == '-':
		n = n[1:]
	    if n[-1] == '/':
		n = n[:-1]
	    if n[-1] == '-':
		n = n[:-1]
	    names.append(n.strip().replace('*', ''))
	return names

    def DefaultID(self, id):
	id_m = id_re.match(id)
	if not id_m:
	    return id_m
	return id_m.group('a').upper() + '-' + id_m.group('d')

    def ModifyManItem(self, mod):
	mod = self.DePref('casting', mod)
	mod = self.DePref('base_id', mod)
	mod.setdefault('make', '')

	if mod.get('id'):
	    mod['name'] = mod['rawname'].replace(';', ' ')
	    mod['unlicensed'] = {'unl': '-', '': '?'}.get(mod['make'], ' ')
	    mod.setdefault('description', '')
	    mod['made'] = not (mod['flags'] & self.FLAG_MODEL_NOT_MADE)
	    mod['visual_id'] = self.DefaultID(mod['id'])
	else:
	    mod['id'] = ''
	    mod['name'] = ''
	    mod['iconname'] = ''
	    mod['unlicensed'] = '?'
	    mod['description'] = ''
	    mod['made'] = False
	    mod['visual_id'] = ''
	mod['notmade'] = {True: '', False: '*'}[mod['made']]
	mod['linkid'] = mod.get('mod_id', mod.get('id'))
	mod['link'] = "single.cgi?id"
	mod['descs'] = filter(lambda x:x, mod['description'].split(';'))
	mod['iconname'] = self.IconName(mod.get('rawname', ''))
	mod['shortname'] = self.ShortName(mod.get('rawname', ''))
	mod['casting_type'] = mbdata.casting_types.get(mod.get('model_type', 'SF'), 'Casting')
	return mod

    #- casting_related

    def FetchCastingRelated(self, mod_id):
	return self.Fetch('casting_related,base_id', where="casting_related.model_id='%s' and casting_related.related_id=base_id.id" % mod_id, tag='CastingRelated', verbose=True)

    #- attribute

    def FetchAttributes(self, id):
	return self.Fetch('attribute', where="mod_id='%s'" % id, tag='Attributes')

    def FetchAttribute(self, id):
	return self.Fetch('attribute', where="id='%s'" % id, tag='Attribute')

    def DeleteAttribute(self, where):
	self.Delete('attribute', self.MakeWhere(where))

    def UpdateAttribute(self, values, id):
	self.Write('attribute', values, self.MakeWhere({'id':id}), modonly=True)

    #- attribute_picture

    def FetchAttributePictures(self, id):
	return self.Fetch('attribute_picture', where="mod_id='%s'" % id, tag='AttributePictures')

    def FetchAttributePicture(self, id):
	return self.Fetch('attribute_picture', where="id='%s'" % id, tag='AttributePicture')

    def DeleteAttributePicture(self, where):
	self.Delete('attribute_picture', self.MakeWhere(where))

    def UpdateAttributePicture(self, values, id):
	self.Write('attribute_picture', values, self.MakeWhere({'id':id}), modonly=True)

    #- variation

    def FetchVariationsBare(self):
	return self.Fetch('variation', tag='VariationsBare')

    def FetchVariations(self, id, nodefaults=False):
	varrecs = self.Fetch('variation', where="mod_id='%s'" % id, tag='Variations')
	detrecs = self.FetchDetails(id, nodefaults=nodefaults)
	if detrecs:
	    for varrec in varrecs:
		varrec.update(detrecs.get(varrec['variation.var'], ''))
	return varrecs

    def FetchVariation(self, id, var):
	varrecs = self.Fetch('variation', where="mod_id='%s' and var='%s'" % (id, var), tag='Variation')
	detrecs = self.FetchDetails(id, var)
	for var_id in detrecs:
	    if var == var_id:
		varrecs[0].update(detrecs[var_id])
	return varrecs

    def FetchVariationQuery(self, varsq, castingq, codes=None):
	wheres = ['v.mod_id=casting.id', 'casting.id=base_id.id']
	if codes == 0:
	    return list() # ha-ha
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
	varrecs = self.dbi.select('variation v,casting,base_id', cols, where=' and '.join(wheres), args=args)
	return varrecs

    def FetchVariationBySelect(self, mod_id, ref_id, sub_id):
	cols = ['v.text_description', 'v.picture_id', 'v.var', 'vs.ref_id', 'vs.sub_id']
	table = "variation_select vs"
	sub_id = ','.join(["'%s'" % x for x in sub_id])
	where = "vs.mod_id='%s' and vs.ref_id='%s' and vs.sub_id in (%s)" % (mod_id, ref_id, sub_id)
	table += " left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var"
	return self.dbi.select(table, cols, where=where)

    def FetchVariationFiles(self, mod_id):
	return self.Fetch('variation', columns=['imported_from'], group='imported_from', order='imported_from', where="mod_id='%s'" % mod_id, tag='VariationFiles', verbose=True)

    def InsertVariation(self, mod_id, var, attributes={}):
	cols = self.table_info['variation']['columns']
	nvar = dict()
	for col in cols:
	    nvar[col] = attributes.get(col, '')
	nvar['var'] = var
	nvar['mod_id'] = mod_id
	nvar['flags'] = 0
	self.Write('variation', nvar, newonly=True)
	attribute_list = self.FetchAttributes(mod_id)
	for attr in attribute_list:
	    det = {'var_id' : nvar['var'], 'mod_id' : mod_id, 'attr_id' : attr['attribute.id'], 'description' : attributes.get(attr['attribute.attribute_name'], '')}
	    self.Write('detail', det, newonly=True)

    def UpdateVariation(self, values, id, verbose=False):
	self.Write('variation', values, self.MakeWhere(id), modonly=True, verbose=verbose)

    def DeleteVariation(self, where):
	self.Delete('variation', where=self.MakeWhere(where))

    #- variation_select

    def FetchVariationSelects(self, mod_id, var_id=None):
	wheres = ["variation_select.mod_id='%s'" % mod_id, "variation_select.ref_id=page_info.id"]
	if var_id:
	    wheres.append("variation_select.var_id='%s'" % var_id)
	left_joins = [("pack", "variation_select.sub_id=pack.id")]
	left_joins += [("base_id", "pack.id=base_id.id")]
	left_joins += [("lineup_model", "lineup_model.mod_id=variation_select.mod_id and lineup_model.page_id=variation_select.ref_id")]
	return self.Fetch('variation_select,page_info', left_joins=left_joins, where=wheres, tag='VariationSelects', verbose=0)

    def UpdateVariationSelect(self):
	self.Write('variation_select', {'var_id' : new_var_id}, where="var_id='%s' and mod_id='%s'" % (old_var_id, mod_id), modonly=True)

    def UpdateVariationSelects(self, mod_id, var_id, ref_ids):
	self.Delete('variation_select', where="mod_id='%s' and var_id='%s'" % (mod_id, var_id))
	for ref_id in ref_ids:
	    sub_id = ''
	    if ref_id.find('/') >= 0:
		ref_id, sub_id = ref_id.split('/', 1)
	    self.Write('variation_select', {'mod_id' : mod_id, 'var_id' : var_id, 'ref_id' : ref_id, 'sub_id' : sub_id}, newonly=True, verbose=1)

    def UpdateVariationSelectSub(self, new_sub_id, ref_id, sub_id):
	self.Write('variation_select', {'sub_id' : new_sub_id}, where="ref_id='%s' and sub_id='%s'" % (ref_id, sub_id), modonly=True)

    def DeleteVariationSelect(self, where):
	self.Delete('variation_select', where=self.MakeWhere(where))

    #- detail

    def DeleteDetail(self, where):
	self.Delete('detail', where=self.MakeWhere(where))

    def FetchDetails(self, mod_id, var_id=None, nodefaults=False):
	if nodefaults:
	    commondetails = {}
	else:
	    commondetails = {x['attribute_name']: x['description'] for x in
		self.dbi.select('detail, attribute',
		    ['detail.mod_id', 'attr_id', 'description', 'attribute_name'],
		    "detail.mod_id='%s' and detail.attr_id=attribute.id and detail.var_id=''" % mod_id)}
	if var_id != None:
	    details = self.dbi.select('detail, attribute',
		['detail.mod_id', 'var_id', 'attr_id', 'description', 'attribute_name'],
		"detail.mod_id='%s' and detail.var_id='%s' and detail.attr_id=attribute.id" % (mod_id, var_id))
	else:
	    details = self.dbi.select('detail, attribute',
		['detail.mod_id', 'var_id', 'attr_id', 'description', 'attribute_name'],
		"detail.mod_id='%s' and detail.attr_id=attribute.id" % mod_id)

	mvars = {}
	for det in details:
	    mvars.setdefault(det['var_id'], copy.deepcopy(commondetails))
	    mvars[det['var_id']][det['attribute_name']] = det['description']
	return mvars

    def UpdateDetail(self, values, where, verbose=False):
	self.Write('detail', values, where=self.MakeWhere(where), modonly=True, verbose=verbose)

    #- vehicle_make

    def FetchVehicleMakes(self):
	return self.Fetch('vehicle_make', tag='VehicleMakes')

    #- vehicle_type

    def FetchVehicleTypes(self):
	return self.Fetch('vehicle_type', tag='VehicleTypes')

    #- counter

    def FetchCounters(self):
	return self.Fetch('counter', tag='Counters')

    def IncrementCounter(self, page_id):
	self.dbi.count(page_id)

    #- lineup_model

    def FetchSimpleLineupModels(self, year='', region='', base_id=''):
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
	return self.dbi.select(table, cols, where=' and '.join(wheres))

    def FetchLineupModels(self, year='', region=''):
	cols = list()
	cols.extend(['lineup_model.id', 'lineup_model.mod_id', 'lineup_model.number', 'lineup_model.style_id', 'lineup_model.region', 'lineup_model.year', 'lineup_model.name', 'lineup_model.picture_id', 'lineup_model.flags'])
	cols.extend(['base_id.id', 'base_id.first_year', 'base_id.rawname', 'base_id.description', 'base_id.flags', 'base_id.model_type'])
	cols.extend(['casting.id', 'casting.scale', 'casting.vehicle_type', 'casting.country', 'casting.make', 'casting.section_id'])
	cols.extend(['pack.id', 'pack.page_id', 'pack.section_id', 'pack.name', 'pack.year', 'pack.region', 'pack.note'])
	cols.extend(['publication.id', 'publication.first_year', 'publication.flags', 'publication.model_type', 'publication.country', 'publication.rawname', 'publication.description', 'publication.section_id'])
	table = "lineup_model"
       	table += " left join base_id on base_id.id=lineup_model.mod_id"
       	table += " left join casting on casting.id=lineup_model.mod_id"
       	table += " left join pack on pack.id=lineup_model.mod_id"
       	table += " left join publication on publication.id=lineup_model.mod_id"
	wheres = list()
	if isinstance(region, list):
	    wheres.append("lineup_model.region in (" + ','.join(["'" + x + "'" for x in region]) + ')')
	if year:
	    cols.extend(['v.text_description', 'v.picture_id', 'v.var', 'vs.ref_id', 'vs.sub_id'])
	    table += " left join variation_select vs on (vs.ref_id='year.%s')" % year
	    table += " and vs.mod_id=lineup_model.mod_id"
	    table += " left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var"
	    wheres.append("lineup_model.year='" + year + "'")
	return self.dbi.select(table, cols, where=' and '.join(wheres))

    def FetchLineupModelsByRank(self, rank, syear, eyear):
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
	return self.dbi.select(table, cols, where=where)

    def FetchLineupYears(self):
	return self.dbi.select("lineup_model", ["year"], group="year")

    def FetchCastingLineups(self, mod_id):
	where = "lineup_model.mod_id='%s'" % mod_id
	left_joins = [('section', 'section.page_id=lineup_model.page_id and section.id=lineup_model.region'),
		    ('page_info', 'page_info.id=lineup_model.page_id')]
	return self.Fetch("lineup_model", left_joins=left_joins, where=where, tag='CastingLineups')
	#return self.dbi.select("lineup_model", where=where)

    def UpdateLineupModel(self, where, values):
	self.Write('lineup_model', self.MakeValues('lineup_model', values), self.MakeWhere(where), modonly=True, verbose=True)

    #- region

    def FetchRegions(self):
	regs = self.Fetch('region', tag='Regions')
	return {x['id']: x['name'] for x in regs}, {x['id']: x['parent'] for x in regs}

    #- matrix_model

    def FetchMatrixModels(self, page_id, section=None):
	where = "page_id='" + page_id + "'"
	if section:
	    where += " and section_id='" + section + "'"
	return self.Fetch('matrix_model', where=where, order='display_order', tag='MatrixModels')

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
    def FetchMatrixModelsVariations(self, page_id, section=None):
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
	return self.dbi.select(table, cols, where=where, order='matrix_model.display_order')

    def FetchMatrixAppearances(self, mod_id):
	where = "page_info.id like 'matrix.%%' and page_info.id=matrix_model.page_id and section.id=matrix_model.section_id and matrix_model.mod_id='%s'" % mod_id
	return self.dbi.select('matrix_model, page_info, section', ['matrix_model.section_id', 'page_info.id', 'page_info.title', 'page_info.description', 'page_info.flags', 'section.name'], where)

    #- link_line

    def DeleteLinkLine(self, id):
	self.Delete('link_line', where="id=%s" % id)

    def UpdateLinkLine(self, rec):
	self.Write('link_line', rec, 'id=%s' % rec['id'], modonly=True, tag='UpdateLinkLine')

    def InsertLinkLine(self, rec):
	return self.Write('link_line', rec, newonly=True, tag='InsertLinkLine')

    def FetchLinkLine(self, id):
	link = self.dbi.select('link_line', where="id='%s'" % id)
	if link:
	    return link[0]
	return None

    def FetchLinkLines(self, page_id=None, section=None, where=None, order=None):
	wheres = list()
	if where:
	    wheres.append(where)
	if page_id:
	    wheres.append("page_id='" + page_id + "'")
	if section:
	    wheres.append("section_id='" + section + "'")
	return self.Fetch('link_line', where=" and ".join(wheres), order=order, tag='LinkLines')

    def FetchLinksSingle(self, page_id=None):
	columns = ['l1.page_id', 'l1.associated_link', 'l1.url', 'l1.name', 'l2.id', 'l2.name', 'l2.url', 'l1.flags']
	wheres = ['not l1.flags & 1']
	if page_id:
	    wheres.append("l1.page_id='" + page_id + "'")
	wheres.append('l1.associated_link=l2.id')
	return self.Fetch('link_line l1, link_line l2', columns=columns, where=" and ".join(wheres), tag='LinksSingle')

    #- blacklist

    def FetchBlacklist(self):
	return self.Fetch('blacklist', tag='Blacklist')

    #- publication

    def FetchPublication(self, id):
	return self.Fetch('publication,base_id', where="base_id.id=publication.id and base_id.id='%s'" % id, tag='Publication')

    def FetchPublications(self):
	return self.Fetch('publication,base_id', where="base_id.id=publication.id", tag='Publications')

    #- pack

    def FetchPack(self, id):
	return self.Fetch('pack,base_id', where="pack.id='%s' and base_id.id='%s'" % (id, id), tag='Pack')

    def FetchPacks(self, page_id='', year='', region=''):
	wheres = ["base_id.id=pack.id"]
	if year:
	    wheres.append("year='" + year + "'")
	if region:
	    wheres.append("region='" + region + "'")
	if page_id:
	    wheres.append("page_id='" + page_id + "'")
	return self.Fetch('base_id,pack', where=' and '.join(wheres), tag='Packs')

    def InsertPack(self, pack_id, page_id=None):
	section_id = None
	if page_id:
	    section_id = page_id[page_id.rfind('.') + 1:]
	self.Write('base_id', {'id' : pack_id}, newonly=True)
	return self.Write('pack', {'id' : pack_id, 'page_id' : page_id, 'section_id' : section_id}, newonly=True)

    def DeletePack(self, id):
	self.Delete('pack', "id='%s'" % id)

    def FetchPacksRelated(self, id):
	cols = [
	    'base_id.id', 'base_id.first_year', 'base_id.model_type', 'base_id.rawname', 'base_id.description', 'base_id.flags',
	    'pack.id', 'pack.page_id', 'pack.section_id', 'pack.name', 'pack.year', 'pack.region', 'pack.layout', 'pack.product_code', 'pack.material', 'pack.country', 'pack.note']
	tables = ['casting_related', 'base_id', 'pack']
	wheres = ["casting_related.model_id='%s'" % id, "casting_related.related_id=base_id.id", "casting_related.related_id=pack.id"]
	return self.Fetch(tables, columns=cols, where=wheres, tag='PacksRelated')

    def UpdatePack(self, id, values):
	self.Write('pack', self.MakeValues('pack', values), "id='%s'" % id, modonly=True)

    #- pack_model

    def InsertPackModel(self, pack_id):
	return self.dbi.execute("insert into pack_model (pack_id,display_order) select'%s', 1+count(*) from pack_model where pack_id='%s'" % (pack_id, pack_id))

    def UpdatePackModels(self, pms, page_id=None, sub_id=None):
	if page_id and sub_id:
	    self.Delete('variation_select', where="ref_id='%s' and sub_id='%s'" % (page_id, sub_id))
	for pm in pms:
	    self.Write('pack_model', pm, where="id=%s" % pm['id'], modonly=True)
	    if page_id and sub_id:
		for var_id in filter(None, pm['var_id'].split('/')):
		    self.Write('variation_select', {'mod_id' : pm['mod_id'], 'var_id' : var_id, 'ref_id' : page_id, 'sub_id' : pm['pack_id']}, newonly=True)

    def FetchPackModel(self, id):
	return self.Fetch('pack_model', where='id=%s' % id, tag='PackModel')

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

    def FetchPackModels(self, pack_id='', year='', region='', page_id='', sub_id=''):

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
	return self.Fetch(froms, columns=cols, where=" and ".join(wheres), tag='PackModels')

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
	return self.dbi.rawquery(pack_model_query % (page_id, pack_id, pack_id))

    def FetchPackModelAppearances(self, mod_id):
	return self.Fetch('pack, pack_model, page_info, base_id', columns=['pack.id', 'base_id.id', 'base_id.rawname', 'base_id.first_year', 'pack.region', 'pack.layout', 'page_info.title', 'pack.section_id'], where="pack.id=base_id.id and pack_model.mod_id='%s' and pack_model.pack_id=pack.id and page_info.id=pack.page_id" % mod_id, tag='PackModelAppearances')

    def DeletePackModels(self, ref_id, pack_id):
	self.Delete('pack_model', "pack_id='%s'" % pack_id)
	self.Delete('variation_select', where="ref_id='%s' and sub_id='%s'" % (ref_id, pack_id))

    #- casting_compare

    def FetchCastingCompare(self, mod_id):
	where = "mod_id='%s' or compare_id='%s'" % (mod_id, mod_id)
	return len(self.Fetch('casting_compare', where=where, tag='CastingCompare')) > 0

#select cc.id,cc.mod_id,cc.compare_id,cc.section_id,cc.description,c1.id,c1.rawname,c2.id,c2.rawname from casting_compare cc left join casting c1 on (cc.mod_id=c1.id) left join casting c2 on (cc.compare_id=c2.id) ;
    def FetchCastingCompares(self, section_id=None):
	columns = ['cc.id', 'cc.mod_id', 'cc.compare_id', 'cc.section_id', 'cc.description', 'c1.rawname', 'c2.rawname']
	where = 'cc.mod_id=c1.id'
	if section_id:
	    where += " and cc.section_id='%s'" % section_id
	table = 'casting_compare cc left join base_id c1 on (cc.mod_id=c1.id) left join base_id c2 on (cc.compare_id=c2.id)'
	return self.Fetch(table, columns=columns, where=where, tag='CastingCompares')

    #- user

    def FetchUser(self, id=None, name=None, vkey=None):
	where = list()
	if id:
	    where.append("id=%s" % id)
	if name:
	    where.append("name='%s'" % name)
	if vkey:
	    where.append("vkey='%s'" % vkey)
	return self.Fetch('user', where=' and '.join(where), tag='User')

    def FetchUsers(self):
	return self.Fetch('user', tag='Users')

    def Login(self, name, passwd):
	return self.dbi.login(name, passwd)

    def CreateUser(self, name, passwd, email, vkey):
	return self.dbi.createuser(name, passwd, email, vkey)

    def UpdateUser(self, id, name=None, email=None, passwd=None, privs=None, state=None):
	#'columns' : ['id', 'name', 'passwd', 'privs', 'email', 'state', 'vkey'],
	values = {}
	if name != None:
	    values['name'] = name
	if email != None:
	    values['email'] = email
	if passwd != None:
	    values['passwd'] = "PASSWORD('%s')" % passwd
	if state != None:
	    values['state'] = int(state)
	if privs != None:
	    values['privs'] = privs
	self.Write('user', values, "id=%s" % id, modonly=True)

    def DeleteUser(self, id):
	self.Delete('user', 'id=%s' % id)

#pif.dbh.RawFetch("update variation set imported_from='was %s' where imported_from='%s' and mod_id='%s'" % (pif.FormStr('current_file'), pif.FormStr('current_file'), mod_id))
#attrs = pif.dbh.RawFetch("select id, attribute_name from attribute where mod_id='" + mod_id + "'")

    #- site_activity

    def FetchActivities(self):
	return self.Fetch('site_activity,user', where='site_activity.user_id=user.id')
    #def Fetch(self, table_name, left_joins=None, columns=None, where=None, group=None, order=None, tag='', verbose=False):

    def InsertActivity(self, name, user_id, description='', url='', image='', timestamp=None):
	oldrow = self.Fetch('site_activity', columns=['id'], order='id desc limit 98,1', tag='InsertActivity')
	if oldrow:
	    oldrow = oldrow[0]['id']
	else:
	    oldrow = 1
	self.RawExecute('''delete from site_activity where id < %d''' % oldrow, 'InsertActivity')
	rec = {'name' : name, 'description' : description, 'url' : url, 'image' : image, 'user_id' : user_id}
	if timestamp:
	    rec['timestamp'] = timestamp
	return self.Write('site_activity', rec, newonly=True, tag='InsertActivity', verbose=True)

    def DeleteActivity(self, id):
	self.Delete('site_activity', where=self.MakeWhere({'id':id}), tag='DeleteActivity')

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
