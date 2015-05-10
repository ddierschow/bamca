#!/usr/local/bin/python

import copy, csv, glob, json, os, re, sys
import basics
import config
import mbdata
import mflags
import models
import single
import useful
import vars

# This file could use a complete rewrite.
# Add: order by

#---- manlist stuff -------------------------

vt_cols = [
        ['img', 'pic'],
        ['name', 'name'],
        ['sel', 'sel'],
]
vt_fmtb = reduce(lambda x, y: x+'<td>%('+y[0]+')s</td>', vt_cols, '<tr>') + '</tr>'
vt_fmth = reduce(lambda x, y: x+'<th>%('+y[0]+')s</th>', vt_cols, '<tr>') + '</tr>'
admin_cols = [
        ['own', 'X'],
        ['vid', 'ID'],
        ['unlicensed', ''],
        ['nl', 'Name'],
        ['first_year', 'Year'],
        ['fvyear', 'First'],
        ['lvyear', 'Last'],
        ['scale', 'Scale'],
        ['country', 'CC'],
        ['make', 'Make'],
	['varids', 'Vars'],
        [ '9', 'XF'], #  9 | http://www.mbxforum.com/
        ['13', 'CH'], # 13 | http://www.mboxcommunity.com/
        ['14', 'DB'], # 14 | http://mb-db.co.uk
        ['10', 'CF'], # 10 | http://www.mboxcommunity.com/cfalkens/
        [ '8', 'MD'], #  8 | http://matchbox-dan.com/
        [ '6', 'PS'], #  6 | http://www.publicsafetydiecast.com
        ['12', 'D+'], # 12 | http://www.diecastplus.info/
        [ '1', 'MF'], #  1 | http://cobratoys.com.au/mbcat/
        ['11', 'TB'], # 11 | http://www.kulitjerukbali.net/index.html
        [ '4', 'WK'], #  4 | http://matchbox.wikia.com/wiki/Matchbox_Cars_Wiki
        [ '2', 'XD'], #  2 | http://www.mbxforum.com/ (docs)
        [ '7', 'AP'], #  7 | http://www.areh.de/
        [ '5', 'TV'], #  5 | http://www.toyvan.co.uk/
        ['15', 'MU'], # 15 | http://www.mbx-u.com/
        [ '3', 'BC'], #  3 | /pages/compare.php
	['de', 'De'],
	['fo', 'Fo'],
	['ba', 'Ba'],
	['bo', 'Bo'],
	['in', 'In'],
	['wh', 'Wh'],
	['wi', 'Wi'],
        #['description', 'Description'],
        #['mydesc', 'Mine'],
]
a_links = ['9', '13', '14', '10', '8', '6', '12', '1', '11', '4', '2', '7', '5', '3']

var_pic_keys = ['pic_a', 'pic_c', 'pic_1', 'pic_2', 'pic_f', 'pic_p']
var_pic_hdrs = ['All', 'Core', 'Code 1', 'Code 2', '"F" Vars', '2ndP']
picture_cols = [
        ['vid', 'ID'],
        ['unlicensed', ''],
        ['nl', 'Name'],
        ['first_year', 'Year'],
        ['l_', 'L'],
        ['m_', 'M'],
        ['s_', 'S'],
        ['t_', 'T'],
        ['z_', 'I'],
        ['b_', 'B'],
        ['r_', 'R'],
        ['a_', 'A'],
        ['d_', 'D'],
        ['i_', 'I'],
        ['p_', 'P'],
]
picture_cols += zip(var_pic_keys, var_pic_hdrs) + [['description', 'Description']]
mades = {False: '<i>%(name)s</i>', True: '%(name)s'}
prefixes = [
        ['a_', config.IMG_DIR_ADD],
        ['b_', config.IMG_DIR_ADD],
        ['d_', config.IMG_DIR_ADD],
        ['i_', config.IMG_DIR_ADD],
        ['h_', config.IMG_DIR_MAN],
        ['l_', config.IMG_DIR_MAN],
        ['m_', config.IMG_DIR_MAN],
        ['p_', config.IMG_DIR_ADD],
        ['r_', config.IMG_DIR_ADD],
        ['s_', config.IMG_DIR_MAN],
        ['t_', config.IMG_DIR_MAN],
        ['z_', config.IMG_DIR_ICON],
]
format_attributes = ['format_description', 'format_body', 'format_interior', 'format_windows', 'format_base', 'format_wheels']

#---- the manno object ----------------------

class MannoFile:
    def __init__(self, pif, withaliases=False):
        self.section = None
        self.start = 1
        self.end = 9999
        self.firstyear = 1
        self.lastyear = 9999
        self.nodesc = pif.form.get_int('nodesc')
        vtypes = pif.dbh.fetch_vehicle_types()
        self.tdict = {x['vehicle_type.ch']: x['vehicle_type.name'] for x in vtypes}
        self.vtypes = {'y': "", 'n': "", 'm': "".join(self.tdict.keys())}
        self.plist = ['manno', 'manls']  # [x['page_info.id'] for x in pif.dbh.fetch_pages({'format_type': 'manno'})]
        if pif.form.get_str('section', 'all') != 'all':
            slist = pif.dbh.fetch_sections({'id': pif.form.get_str('section')})  #, 'page_id': pif.page_id})
        else:
            slist = pif.dbh.fetch_sections({'page_id': pif.page_id})
	if not slist:
	    raise useful.SimpleError('Requested section not found. %s' % pif.form.get_str('section'))
	aliases = pif.dbh.fetch_aliases()
	adict = dict()
	for alias in aliases:
	    adict.setdefault(alias['alias.ref_id'], list())
	    adict[alias['alias.ref_id']].append(alias)
        self.mdict = dict()
        self.sdict = dict()
        self.slist = list()
        for section in slist:
            if section['section.page_id'] in self.plist and (not self.section or section['id'] == self.section):
                section = pif.dbh.depref('section', section)
                section.setdefault('model_ids', list())
                self.sdict[section['id']] = section
                self.slist.append(section)

        for key in pif.form.keys(start='type_'):
            val = pif.form.get_str(key)
            t = key[-1]
            self.vtypes.setdefault(val, list())
            self.vtypes[val] += t

        self.section = pif.form.get_str('section')
        if self.section == 'all':
            self.section = ''
        self.start = pif.form.get_int('start', 1)
        self.end = pif.form.get_int('end', 9999)
        self.firstyear = pif.form.get_int('syear', 1)
        self.lastyear = pif.form.get_int('eyear', 9999)
        if pif.form.get_str('range', 'all') == 'all':
            self.start = self.end = None

        for casting in pif.dbh.fetch_casting_list():  #(page_id=pif.page_id):
            self.add_casting(pif, casting, aliases=adict.get(casting['base_id.id'], []))
        if withaliases:
            for alias in pif.dbh.fetch_aliases(where="section_id != ''"):
		if alias['alias.section_id']:
		    #self.add_casting(pif, alias)
		    self.add_alias(pif, alias)

    def add_casting(self, pif, casting, aliases=[]):
        manitem = pif.dbh.modify_man_item(casting)
	aliases = [x['alias.id'] for x in aliases if x['alias.type'] == 'mack']
	manitem['mack'] = ','.join(single.get_mack_numbers(pif, manitem['id'], manitem['model_type'], aliases))
        if manitem['section_id'] in self.sdict and manitem['id'] not in self.sdict[manitem['section_id']]['model_ids']:
            self.add_item(manitem)

    def add_alias(self, pif, alias):
        manitem = pif.dbh.modify_man_item(alias)
        if manitem['alias.section_id'] in self.sdict:
            manitem['id'] = manitem['alias.id']
            if 'ref_id' in manitem:
                refitem = copy.deepcopy(self.mdict[manitem['ref_id']])
                if manitem['first_year']:
                    refitem['first_year'] = manitem['first_year']
                refitem['id'] = manitem['id']
                refitem['descs'] = manitem['descs']
                refitem['descs'].append('same as ' + manitem['ref_id'])
                manitem = refitem
            self.add_item(manitem)

    def add_item(self, manitem):
        if self.is_item_shown(manitem):
            manitem['nodesc'] = self.nodesc
            manitem['type_desc'] = self.types(manitem['vehicle_type'])
            self.sdict[manitem['section_id']]['model_ids'].append(manitem['id'])
            self.mdict[manitem['id']] = manitem

    def types(self, typespec):
        return ', '.join(filter(None, [self.tdict.get(t) for t in typespec]))

    def run_thing(self, pif, FunctionShowSection):
        sections = list()
        for sec in self.slist:
            #if sec['model_ids']:
                sec['model_ids'].sort()
                sections.append(FunctionShowSection(pif, sec))
        return sections

    def is_item_shown(self, mod):
        '''Makes decision of whether to show based on vehicle type, # range, and year range.'''
        if self.start and self.end:
            modno = 0
            for c in mod['id']:
                if c.isdigit():
                    modno = 10 * modno + int(c)
            if modno < self.start or modno > self.end:
                return False

        if mod['first_year'] and (self.firstyear > int(mod['first_year']) or self.lastyear < int(mod['first_year'])):
            return False

        if self.vtypes.get('y') or self.vtypes.get('n'):
            if useful.any_char_match(self.vtypes['n'], mod['vehicle_type']):
                return False
            if self.vtypes['y'] and not useful.any_char_match(self.vtypes['y'], mod['vehicle_type']):
                return False
        return True

    # ----- castings --------------------------------------------

    def show_section_manno_template(self, pif, sect):
        sect['anchor'] = sect['id']
        sect['id'] = ''
        sect['range'] = [{'entry': models.generate_model_table_pic_link_dict(pif, self.mdict, sect['model_ids'])}]
        return sect

    def run_manno_template(self, pif):
        llineup = dict(columns=4)
        llineup['section'] = self.run_thing(pif, self.show_section_manno_template)
	pif.render.format_button_comment(pif, 'sel=%s&ran=%s&start=%s&end=%s' %
                (pif.form.get_str('selection'), pif.form.get_str('range'), pif.form.get_str('start'), pif.form.get_str('end')))
        return pif.render.format_template('mannum.html', llineup=llineup)

    # ----- play ------------------------------------------------

    def run_play(self, pif):
        llineup = {'section': list(), 'columns': 4}
        llineup['section'] = self.run_thing(pif, self.show_section_manno)
        return llineup

    # ----- check list ------------------------------------------

    def get_section_list(self, pif, sect):
        cols = 3
	sect['entry'] = [models.add_model_table_list_entry_dict(pif, self.mdict.get(modid, {})) for modid in useful.reflect(sect['model_ids'], cols)]
	sect['columns'] = cols
	sect['anchor'] = sect['id']
        return sect

    def run_checklist_template(self, pif):
        llineup = dict(columns=3)
        llineup['section'] = self.run_thing(pif, self.get_section_list)
	pif.render.format_button_comment(pif, 'sel=%s&ran=%s&start=%s&end=%s' %
                (pif.form.get_str('selection'), pif.form.get_str('range'), pif.form.get_str('start'), pif.form.get_str('end')))
        return pif.render.format_template('manckl.html', llineup=llineup)

    # ----- thumbnails ------------------------------------------

    def get_section_thumbs(self, pif, sect):
        sect['range'] = list()
        sect['anchor'] = sect['id']
        sect['id'] = ''
        sect['columns'] = 6
        ran = {'entry': list()}
        for mod_id in sect['model_ids']:
            mdict = self.mdict[mod_id]
            mdict['nodesc'] = 1
            mdict['prefix'] = 't'
            ran['entry'].append(models.add_model_table_pic_link_dict(pif, mdict))
        sect['range'].append(ran)
        return sect

    def run_thumbnails_template(self, pif):
        llineup = dict(columns=6)
        llineup['section'] = self.run_thing(pif, self.get_section_thumbs)
	pif.render.format_button_comment(pif, 'sel=%s&ran=%s&start=%s&end=%s' %
                (pif.form.get_str('selection'), pif.form.get_str('range'), pif.form.get_str('start'), pif.form.get_str('end')))
        return pif.render.format_template('manthm.html', llineup=llineup)

    # ----- admin -----------------------------------------------

    def show_list_var_info(self, pif, mod_id):
        mvars = pif.dbh.fetch_variations(mod_id)
	texts = ['text_description', 'text_base', 'text_body', 'text_interior', 'text_wheels', 'text_windows']
	td = {x[5:7]: 0 for x in texts}
        fy = ly = None
	id_set = set()
        for var in mvars:
	    var_id = var['variation.var']
	    if var_id[0].isdigit():
		while not var_id[-1].isdigit():
		    var_id = var_id[:-1]
		id_set.add(int(var_id))
	    for txt in texts:
		if var['variation.' + txt]:
		    td[txt[5:7]] += 1
            dt = var['variation.date'].split('/')
            if len(dt) > 1:
                yr = dt[1].strip()
                if yr.isdigit():
                    yr = int(yr) + 1900
                    if yr < 1953:
                        yr += 100
                    if not fy:
                        fy = yr
                    if not ly:
                        ly = yr
                    fy = min(fy, yr)
                    ly = max(ly, yr)
	if id_set:
	    min_id = min(id_set)
	    max_id = max(id_set)
	    contig = not bool(set(range(min_id, max_id + 1)) - id_set)
	    varids = '<span class="%s">%d-%d</span>' % ('ok' if contig else 'no', min_id, max_id)
	else:
	    varids = '-'
	for key in td:
	    td[key] = pif.render.format_image_art('stargray.gif' if not len(mvars) else
                    'stargreen.gif' if td[key] == len(mvars) else ('starred.gif' if not td[key] else 'starorange.gif'))
        td.update({'fvyear': fy if fy else '-', 'lvyear': ly if ly else '-', 'varids': varids})
        return td

    def get_admin_entries(self, pif, model_ids):
	for mod in model_ids:
	    mdict = self.mdict[mod]
	    mdict.setdefault('own', '')
	    mdict.setdefault('mydesc', '')
	    mdict.update({x: '-' for x in a_links})
	    for lnk in pif.dbh.fetch_link_lines("single." + mdict['id']):
		mdict[str(lnk['link_line.associated_link'])] = pif.render.format_link(lnk['link_line.url'], 'X')
	    mdict['name'] = mades[int(mdict['made'])] % mdict
	    mdict.update({
		'fvyear': '', 'lvyear': '',
		'vid': '<a href="vars.cgi?list=1&mod=%(id)s">%(id)s</a>' % mdict,
		'nl': '<a href="single.cgi?id=%(id)s">%(name)s</a>' % mdict})
	    mdict.update(self.show_list_var_info(pif, mdict['id']))
	    fmt_valid, messages = pif.dbh.check_description_formatting(mdict['id'])
	    mdict['fo'] = pif.render.format_image_art('starred.gif') if fmt_valid else ''
	    if mdict['make']:
		mdict['make'] = pif.render.format_link("http://beta.bamca.org/cgi-bin/makes.cgi?make=" + mdict['make'], mdict['make'])
	    yield mdict

    def get_section_admin(self, pif, sect):
        sect['columns'] = [x[0] for x in admin_cols]
        sect['headers'] = dict(admin_cols)
        sect['range'] = [{'entry': self.get_admin_entries(pif, sect['model_ids'])}]
        return sect

    def run_admin_list_template(self, pif):
        llineup = dict()
        llineup['section'] = self.run_thing(pif, self.get_section_admin)
	pif.render.format_button_comment(pif, 'sel=%s&ran=%s&start=%s&end=%s' %
                (pif.form.get_str('selection'), pif.form.get_str('range'), pif.form.get_str('start'), pif.form.get_str('end')))
        return pif.render.format_template('simplelistix.html', llineup=llineup)

    # ----- picture -----------------------------------------------

    def show_list_pic(self, pif, prefix, id, txt):
        if glob.glob(prefix[1]+'/'+prefix[0]+id.lower()+'.jpg'):
            return [prefix[0], pif.render.format_image_as_link([prefix[0]+id.lower()], txt.upper(), prefix[1])]
        if glob.glob(prefix[1]+'/'+prefix[0]+id.lower()+'-*.jpg'):
            return [prefix[0], pif.render.format_image_as_link([prefix[0]+id.lower()], txt.upper(), prefix[1])]
        if glob.glob(prefix[1]+'/'+prefix[0]+id.lower()+'.gif'):
            return [prefix[0], pif.render.format_image_as_link([prefix[0]+id.lower()], txt.upper(), prefix[1])]
        if glob.glob(prefix[1]+'/'+prefix[0]+id.lower()+'-*.gif'):
            return [prefix[0], pif.render.format_image_as_link([prefix[0]+id.lower()], txt.upper(), prefix[1])]
        return [prefix[0], '-']

    def get_picture_model_entries(self, pif, model_ids):
	for mod in model_ids:
	    mdict = self.mdict[mod]
	    mdict['first_year'] = '<a href="traverse.cgi?g=1&d=%s">%s</a>' % (os.path.join(config.LIB_MAN_DIR, mdict['id'].lower()), mdict['first_year'])
	    mdict['name'] = mades[int(mdict['made'])] % mdict
	    mdict.update({'img': self.show_list_pic(pif, ['', config.IMG_DIR_MAN], mdict['id'], 's')[1],
		'vid': '<a href="vars.cgi?list=1&mod=%(id)s">%(id)s</a>' % mdict,
		'nl': '<a href="single.cgi?id=%(id)s">%(name)s</a>' % mdict})
	    mdict.update(dict([self.show_list_pic(pif, x, mdict['id'], x[0][0]) for x in prefixes]))
	    icon = self.show_list_pic(pif, ['i_', config.IMG_DIR_ICON], mdict['id'], 'i')
	    mdict['z_'] = icon[1]
	    founds, needs, cnts = single.count_list_var_pics(pif, mdict['id'])
	    for ipix in range(0, 6):
		self.totals[ipix]['have'] += founds[ipix]
		self.totals[ipix]['total'] += needs[ipix]
	    mdict.update(dict(zip(var_pic_keys, single.fmt_list_var_pics(founds, needs))))
	    yield mdict

    def get_section_picture(self, pif, sect):
        sect['columns'] = [x[0] for x in picture_cols]
        sect['headers'] = dict(picture_cols)
        sect['range'] = [{'entry': self.get_picture_model_entries(pif, sect['model_ids'])}]
        return sect

    def run_picture_list(self, pif):
	self.totals = [{'tag': x, 'have': 0, 'total':0} for x in var_pic_hdrs]
        llineup = dict()
        llineup['section'] = self.run_thing(pif, self.get_section_picture)
        llineup['totals'] = self.totals
	return llineup

    def run_picture_list_template(self, pif):
	llineup = self.run_picture_list(pif)
	pif.render.format_button_comment(pif, 'sel=%s&ran=%s&start=%s&end=%s' %
                (pif.form.get_str('selection'), pif.form.get_str('range'), pif.form.get_str('start'), pif.form.get_str('end')))
        return pif.render.format_template('manpxl.html', llineup=llineup)

    # currently not in use
    def get_mine(self, dblist, mans):
        dats = dict()
        mine = dict()
        for mdict in dblist:
            if not mdict:
                pass
            #elif llist[0] == 'data':
                #dats[llist[1]] = llist[2].split(',')
            else:
                #mdict = dict(zip(dats[llist[0]], llist[1:]))
                mine[mdict['id']] = mdict

        for man in mans:
            for mod_id in man['model_ids']:
                mod = self.mdict[mod_id]
                mod.setdefault('own', '')
                mod.setdefault('mydesc', '')
                if mod['id'] in mine:
                    mod['own'] = mine[mod['id']].get('own', '')
                    mod['mydesc'] = mine[mod['id']].get('mydesc', '')
        return mine

    # ----- vehicle types ---------------------------------------

    def get_vt_model_table(self, pif, mdict):
        img = ['s_' + mdict['id']]
        if mdict.get('picture_id'):
            img = ['s_' + mdict['picture_id']]
        for s in mdict['descs']:
            if s.startswith('same as '):
                img.append('s_' + s[8:])
        mdict['name'] = mdict['id'] + '<br>' + mdict['rawname']
        mdict['img'] = pif.render.format_image_required(img, None, made=mdict['made'])
        mdict['sel'] = pif.render.format_checkbox('vt_' + mdict['id'],
                [[x, mbdata.model_types[x]] for x in list(mbdata.model_type_chars[:13])],
                checked=mdict['vehicle_type']) + '<br>'
        mdict['sel'] += pif.render.format_checkbox('vt_' + mdict['id'],
                [[x, mbdata.model_types[x]] for x in list(mbdata.model_type_chars[13:])],
                checked=mdict['vehicle_type']) + '<br>'
        mdict['sel'] += 'make: ' + pif.render.format_text_input('vm_' + mdict['id'], 3, 3, value=mdict['make'])
        mdict['sel'] += 'country: ' + pif.render.format_text_input('co_' + mdict['id'], 2, 2, value=mdict['country'])
	return mdict

    def show_vt_model_table(self, pif, mdict):
        return vt_fmtb % self.get_vt_model_table(pif, mdict)

    def show_section_vehicle_type(self, pif, sect):
        sect['cols'] = len(vt_cols)
        ostr = '<tr><th colspan=%(cols)d><a name="%(id)s">%(name)s</a></th></tr>\n' % sect
        ostr += vt_fmth % dict(vt_cols) + '\n'
        for mod in sect['model_ids']:
            ostr += self.show_vt_model_table(pif, self.mdict[mod]) + '\n'
        return ostr

    def show_section_vehicle_type_template(self, pif, sect):
	sect['entry'] = [self.get_vt_model_table(pif, self.mdict[mod]) for mod in sect['model_ids']]
        return sect

    def run_vehicle_type_list_template(self, pif):
        llineup = dict()
	llineup['cols'] = vt_cols
	llineup['num_cols'] = len(vt_cols)
        llineup['section'] = self.run_thing(pif, self.show_section_vehicle_type_template)
	pif.render.format_button_comment(pif, 'sel=%s&ran=%s&start=%s&end=%s' %
                (pif.form.get_str('selection'), pif.form.get_str('range'), pif.form.get_str('start'), pif.form.get_str('end')))
        return pif.render.format_template('manvtl.html', llineup=llineup)

    # ----- csv -------------------------------------------------

    def show_section_man2csv(self, pif, sect):
        ret = list()
        for mod_id in sect['model_ids']:
            mod = self.mdict[mod_id]
	    #aliases = [x['alias.id'] for x in pif.dbh.fetch_aliases(mod_id, 'mack')]
	    #mack_nums = ','.join(single.get_mack_numbers(pif, mod_id, mod['model_type'], aliases))
            ret.append([mod_id, mod['mack'], mod['first_year'], mod['scale'], mod['name'], ', '.join(mod['descs'])])
        return ret

    # called by man2csv and updcommits, both of which will be phased out
    def run_man2csv(self, pif):
	with open('pages/man.csv', 'w') as out_file:
	    self.run_man2csv_out(pif, out_file)

    def run_man2csv_out(self, pif, out_file):
	field_names = ["MAN #", "Mack #", "Year", "Scale", "Name", "Notes"]
	writer = csv.DictWriter(out_file, fieldnames=field_names)
	writer.writeheader()
	secs = self.run_thing(pif, self.show_section_man2csv)
	for sec in secs:
	    for ln in sec:
		writer.writerow(dict(zip(field_names, ln)))

    # ----- json ------------------------------------------------

    def show_section_man2json(self, pif, sect):
	field_keys = ["man", "mack", "year", "scale", "name", "notes"]
        ret = list()
        for mod_id in sect['model_ids']:
            mod = self.mdict[mod_id]
	    #aliases = [x['alias.id'] for x in pif.dbh.fetch_aliases(mod_id, 'mack')]
	    #mack_nums = ','.join(single.get_mack_numbers(pif, mod_id, mod['model_type'], aliases))
            ret.append(dict(zip(field_keys,
		       [mod_id, mod['mack'], mod['first_year'], mod['scale'], mod['name'], ', '.join(mod['descs'])])))
        return ret

    def run_man2json_out(self, pif):
	secs = self.run_thing(pif, self.show_section_man2json)
	print json.dumps(secs)

# currently unused?
def write_vehicle_types(pif):
    for key in pif.form.keys(start='vt_'):
        val = ''.join(pif.form.get_list(key))
        print key[3:], 'type', val, '<br>'
        pif.dbh.write_casting(values={'vehicle_type': val}, id=key[3:])
    for key in pif.form.keys(start='vm_'):
        print key[3:], 'make', pif.form.get_str(key), '<br>'
        pif.dbh.write_casting(values={'make': pif.form.get_str(key)}, id=key[3:])
    for key in pif.form.keys(start='co_'):
        print key[3:], 'country', pif.form.get_str(key), '<br>'
        pif.dbh.write_casting(values={'country': pif.form.get_str(key)}, id=key[3:])

#---- main ----------------------------------

@basics.web_page
def main(pif):
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append(pif.request_uri, 'Manufacturing Numbers')
    listtype = pif.form.get_str('listtype')
    if listtype == 'csv':
	if not pif.form.has('section'):
	    raise useful.SimpleError("Please select a range to display.")

	pif.render.print_html('text/csv')
	manf = MannoFile(pif, withaliases=True)
	manf.run_man2csv_out(pif, sys.stdout)
    elif listtype == 'jsn':
	if not pif.form.has('section'):
	    raise useful.SimpleError("Please select a range to display.")

	pif.render.print_html('application/json')
	manf = MannoFile(pif, withaliases=True)
	manf.run_man2json_out(pif)
    else:
	if pif.form.get_str('num'):
	    raise useful.Redirect(url="0;url=single.cgi?id=" + pif.form.get_str('num'))

	if not pif.form.has('section'):
	    raise useful.SimpleError("Please select a range to display.")

	pif.render.print_html()
	manf = MannoFile(pif, withaliases=True)
	if listtype == 'adl':
	    print manf.run_admin_list_template(pif)
	elif listtype == 'pxl':
	    print manf.run_picture_list_template(pif)
	elif listtype == 'ckl':
	    print manf.run_checklist_template(pif)
	elif listtype == 'thm':
	    print manf.run_thumbnails_template(pif)
	elif listtype == 'vtl':
	    print manf.run_vehicle_type_list_template(pif)
	else:
	    print manf.run_manno_template(pif)

#---- play ----------------------------------

@basics.web_page
def play_main(pif):
    pif.render.print_html()
    print pif.render.format_head()
    manf = MannoFile(pif)
    llineup = manf.run_play(pif)
    llineup['section'][0]['range'][0]['entry'][0].update({'rowspan': 2, 'colspan': 2})
    print pif.render.format_matrix(llineup)
    print pif.render.format_tail()

#---- compare -------------------------------

@basics.web_page
def compare_main(pif):
    pif.render.print_html()
    csecs = pif.dbh.fetch_sections({'page_id': pif.page_id})
    cmods = pif.dbh.fetch_casting_compares()
    llineup = {'section': []}
    for sec in csecs:

	lsec = {'name': sec['section.name'], 'note': sec['section.note'], 'range': []}
	llineup['section'].append(lsec)
        modsets = {}
        for mod in [m for m in cmods if m['cc.section_id'] == sec['section.id']]:
            if mod['c2.rawname']:
                mod['name'] = mod['c2.rawname'].replace(';', ' ')
                mod['mod_id'] = mod['cc.compare_id']
            else:
                mod['name'] = mod['c1.rawname'].replace(';', ' ')
                mod['mod_id'] = mod['cc.mod_id']
            modsets.setdefault(mod['cc.mod_id'], [])
            modsets[mod['cc.mod_id']].append((mod['mod_id'], mod['name'], mod['cc.description'].split(';')))
        keys = modsets.keys()
        keys.sort()

        for main_id in keys:
            modset = modsets[main_id]
            names = list()
            for id, name, descs in modset:
                if name not in names:
                    names.append(name)
	    lran = {'name': ', '.join(names), 'entry': []}
	    lsec['range'].append(lran)
            for id, name, descs in modset:
		lent = [models.add_model_pic_link_short(pif, id),
			filter(None, descs), pif.render.format_image_optional(main_id, prefix='z_', nopad=True)]
		lran['entry'].append(lent)

    return pif.render.format_template('compare.html', lcompare=llineup)

#---- commands ------------------------------

@basics.command_line
def commands(pif):
    if pif.argv and pif.argv[0] == 'd':
        print "delete not yet implemented"
        pass  # DeleteCasting(pif, pif.argv[1], pif.argv[2])
    elif pif.argv and pif.argv[0] == 'r':
        rename_base_id(pif, pif.argv[1], pif.argv[2], True)
    elif pif.argv and pif.argv[0] == 'f':
        run_search(pif, pif.argv[1:])
    elif pif.argv and pif.argv[0] == 'c':
        clone_attributes(pif, pif.argv[1], pif.argv[2])
    elif pif.argv and pif.argv[0] == 'a':
	add_attributes(pif, pif.argv[1], pif.argv[2:])
    else:
        print "./mannum.py [f|d|r|c] ..."
        print "  f for find: search-criterion"
        print "  d for delete: mod_id"
        print "  r for rename: old_mod_id new_mod_id"
        print "  a for add attributes: mod_id attribute_name ..."
        print "  c for clone attributes: old_mod_id new_mod_id"


def search_name(pif, targ):
    sections = ['manno', 'manls']
    fields = ['base_id.rawname'] #, 'base_id.id']
    where = ["%s like '%%%s%%'" % (y, x) for x in targ for y in fields]
    ret = list()
    for section in sections:
	ret += pif.dbh.fetch_casting_list(page_id=section, where=where, verbose=False)
    return ret


def run_search(pif, args):
    mods = [pif.dbh.modify_man_item(x) for x in search_name(pif, args)]
    mods.sort(key=lambda x: x['id'])
    for mod in mods:
        print '%(id)-8s|%(first_year)4s|%(scale)-5s|%(country)2s|%(name)s' % mod


def add_attributes(pif, mod_id, attr_list):
    for attr in attr_list:
	pif.dbh.insert_attribute(mod_id, attr)


def clone_attributes(pif, old_mod_id, new_mod_id):
    pif.dbh.clone_attributes(old_mod_id, new_mod_id)
    vals = pif.dbh.fetch('casting', columns=format_attributes, where={'id': old_mod_id})
    if vals:
	pif.dbh.write('casting', values=vals[0], where="id='%s'" % new_mod_id, modonly=True)
    vals = pif.dbh.fetch('detail', where={'mod_id': old_mod_id, 'var_id': ''})
    print vals
    for val in vals:
	val = pif.dbh.depref('detail', val)
	val['mod_id'] = new_mod_id
	pif.dbh.write('detail', values=val, newonly=True)
    #insert into detail (select 'MB880', '', attr_id, description from detail where mod_id='MB153' and var_id='');


def rename_base_id(pif, old_mod_id, new_mod_id, force=False):
    rec = pif.dbh.fetch_base_id(new_mod_id)
    if rec:
        if not force:
            print new_mod_id, "exists"
            return
    else:
	print "rename", old_mod_id, new_mod_id
        pif.dbh.rename_base_id(old_mod_id, new_mod_id)

    # If we're renaming, I'd like to also rename the pictures.
    filename_re = re.compile('(?P<path>.*/)(?P<p>[a-z]_)?(?P<m>[^-.]*)(?P<s>-[^.]*)?(?P<e>\..*)')
    none_blank = {None: ''}
    patts = [
        config.IMG_DIR_MAN + '/?_%s.*' % old_mod_id,
        config.IMG_DIR_MAN + '/%s.*' % old_mod_id,
        config.IMG_DIR_VAR + '/?_%s-*.*' % old_mod_id,
        config.IMG_DIR_VAR + '/%s-*.*' % old_mod_id,
        config.IMG_DIR_ICON + '/?_%s-*.*' % old_mod_id,
        config.IMG_DIR_ADD + '/?_%s.*' % old_mod_id,
        config.IMG_DIR_CAT + '/?_%s.*' % old_mod_id,
        config.IMG_DIR_CAT + '/%s.*' % old_mod_id,
        config.IMG_DIR_PACK + '/?_%s.*' % old_mod_id,
        config.IMG_DIR_PACK + '/%s.*' % old_mod_id,
    ]
    pics = reduce(lambda x, y: x + glob.glob(y.lower()), patts, list())
    for pic in pics:
        pic_new = pic.replace(old_mod_id.lower(), new_mod_id.lower())
        print "rename", pic, pic_new, "<br>"
        os.rename(pic, pic_new)

#---- ---------------------------------------

if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='')
