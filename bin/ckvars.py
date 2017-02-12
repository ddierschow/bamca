#!/usr/local/bin/python

import os, re
import basics
import config
import useful

'''
Given a variation, get the list of attributes
Get list of variations.
Build dictionary of vars where key is tuple of visual attributes.
Categorize vars by these keys.
Find vars that might have common picture but don't reflect that.
Find vars where visual pic violates this list.

filelist - list of mod_id's to check (none means all)
options:
  's' - list of man sections
'''

# Decorator for reading data files
def read_data_file(main_fn):
    def read_dat(fn):
        dat = open(useful.relpath(config.SRC_DIR, fn + '.dat')).readlines()
        dat = filter(lambda x: x and not x.startswith('#'), [ln.strip() for ln in dat])
        return main_fn(dat)
    return read_dat


@read_data_file
def read_attr_change(fil):
    changes = dict()
    for ln in fil:
	try:
	    cols, detfr, detto = ln.split('|')
	except ValueError:
	    print 'ValueError:', ln, '<br>'
	    continue
        for col in cols.split(';'):
            changes.setdefault(col, list())
	    for det in detfr.split(';'):
		changes[col].append([det, detto])
    return changes

@basics.command_line
def main(pif):
    global detail_changes
    detail_changes = read_attr_change('vdetail')
    if pif.filelist:
	check_var_data(pif, pif.filelist)
    elif pif.options['s']:
	for section_id in pif.options['s']:
	    mods = pif.dbh.fetch_casting_list(section_id=section_id)
	    check_var_data(pif, [x['casting.id'] for x in mods])
    else:
	mods = pif.dbh.fetch_casting_list()
	check_var_data(pif, [x['casting.id'] for x in mods])


def modify_detail(attr, desc):
    for det_pair in detail_changes.get(attr, []):
	desc = desc.replace(*det_pair)
#    if attr in ['wheels', 'front_wheels', 'rear_wheels']:
#	return desc.replace(' hollow', '').replace(' mixed', '').replace(' solid', '') \
#	    .replace(' (narrow inner rim)', '').replace(' (wide inner rim)', '')
    return desc


def modify_vars(vars):
    for ivar in range(len(vars)):
	vars[ivar] = modify_var(vars[ivar])
    return vars


def modify_var(var):
    for key in var:
	var[key] = modify_detail(key, var[key])
    return var


def check_var_data(pif, id_list):
    for mod_id in id_list:
	casting = pif.dbh.fetch_casting(mod_id)
	print mod_id, ':', casting['name']
	attrs = pif.dbh.fetch_attributes(mod_id=mod_id, with_global=True)
	attr_dict = {x['attribute.attribute_name']: x for x in attrs}
	if casting['flags'] & pif.dbh.FLAG_MODEL_BASEPLATE_VISIBLE:
	    attr_dict['base']['attribute.visual'] = 1
	visual_keys = sorted([x['attribute.attribute_name'] for x in attrs if x['attribute.visual']])
	print '    ', visual_keys
	vk_set = dict()
	vars = modify_vars(pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)))
	vars_dict = {x['var']: x for x in vars}
	for var in vars:
	    var['visual_key'] = tuple([var[x] for x in visual_keys])
	    vk_set.setdefault(var['visual_key'], list())
	    vk_set[var['visual_key']].append(var['var'])
	for vk in sorted(vk_set):
	    print vk
	    print ' ',
	    for var_id in vk_set[vk]:
		var = vars_dict[var_id]
		if var['visual_key'] == vk:
		    print var['var'],
		    if var['picture_id']:
			print '(%s)' % var['picture_id'],
	    print

if __name__ == '__main__':  # pragma: no cover
    main(options='s')
