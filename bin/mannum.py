#!/usr/local/bin/python

import copy
import csv
from functools import reduce
import glob
from io import StringIO
import json
import os
import sys

import basics
import config
import imglib
import mbdata
import mflags
import models
import render
import useful
import varias

# API
#  main

# This file could use a complete rewrite.
# Add: order by

man_sections = ['manno', 'manls', 'manunf']

# ---- manlist stuff -------------------------

vt_cols = [
    ['img', 'pic'],
    ['name', 'name'],
    ['sel', 'sel'],
]
vt_fmtb = '<tr>{}</tr>'.format(''.join(['<td>%({})s</td>'.format(y[0]) for y in vt_cols]))
vt_fmth = '<tr>{}</tr>'.format(''.join(['<th>%({})s</th>'.format(y[0]) for y in vt_cols]))
admin_cols = [
    ['own', 'X'],
    ['vid', 'ID'],
    ['unlicensed', ''],
    ['nl', 'Name'],
    ['first_year', 'Year'],
    ['fvyear', 'First'],
    ['lvyear', 'Last'],
    ['scale', 'Scale'],
    ['alias', 'Aliases'],
    ['rel', 'Rel'],
    ['vehicle_type', 'VT'],
    ['country', 'CC'],
    ['make', 'Make'],
    ['varids', 'Vars'],
    ['varl', 'VarL'],
    ['notes', 'Nt'],
    ['attr', 'Attr'],
    ['im', 'Im'],
    ['de', 'De'],
    ['fo', 'Fo'],
    ['ba', 'Ba'],
    ['bo', 'Bo'],
    ['in', 'In'],
    ['wh', 'Wh'],
    ['wi', 'Wi'],
    ['w/', 'W/'],
    ['bt', 'BT'],
    # ['description', 'Description'],
    # ['mydesc', 'Mine'],
]
admin2_cols = [
    ['own', 'X'],
    ['vid', 'ID'],
    ['unlicensed', ''],
    ['nl', 'Name'],
    ['first_year', 'Year'],
    ['fvyear', 'First'],
    ['lvyear', 'Last'],
    ['scale', 'Scale'],
    ['alias', 'Aliases'],
    ['rel', 'Rel'],
    ['vehicle_type', 'VT'],
    ['country', 'CC'],
    ['make', 'Make'],
    ['varids', 'Vars'],
    ['varl', 'VarL'],
    ['description', 'Description'],
    ['notes', 'Nt'],
    # ['mydesc', 'Mine'],
]
links_cols = [
    ['vid', 'ID'],
    ['nl', 'Name'],
    ['first_year', 'Year'],
    ['9', 'XF'],   # |  9 | http://www.mbxforum.com/
    ['14', 'DB'],  # | 14 | http://mb-db.co.uk
    ['10', 'CF'],  # | 10 | http://www.mboxcommunity.com/cfalkens/
    ['8', 'MD'],   # |  8 | http://matchbox-dan.com/
    ['6', 'PS'],   # |  6 | http://www.publicsafetydiecast.com
    ['12', 'D+'],  # | 12 | http://www.diecastplus.info/
    ['11', 'TB'],  # | 11 | http://www.kulitjerukbali.net/index.html
    ['4', 'WK'],   # |  4 | http://matchbox.wikia.com/wiki/Matchbox_Cars_Wiki
    ['2', 'XD'],   # |  2 | http://www.mbxforum.com/ (docs)
    ['7', 'AP'],   # |  7 | http://www.areh.de/
    ['5', 'TV'],   # |  5 | http://www.toyvan.co.uk/
    ['15', 'MU'],  # | 15 | http://www.mbx-u.com/
    ['3', 'BC'],   # |  3 | /pages/compare.php
    # ['description', 'Description'],
    # ['mydesc', 'Mine'],
]
l_links = ['9', '13', '14', '10', '8', '6', '12', '1', '11', '4', '2', '7', '5', '3']

var_pic_keys = ['pic_a', 'pic_c', 'pic_1', 'pic_2', 'pic_f', 'pic_p']
var_pic_hdrs = ['All', 'Core', 'C1', 'C2', 'F', '2P']
picture_cols = [
    ['vid', 'ID'],
    ['unlicensed', ''],
    ['nl', 'Name'],
    ['first_year', 'Year'],
    ['credit', 'Cr'],
    ['credvars', 'CrV'],
    [mbdata.IMG_SIZ_LARGE + '_', 'L'],
    [mbdata.IMG_SIZ_MEDIUM + '_', 'M'],
    [mbdata.IMG_SIZ_TINY + '_', 'T'],
    ['icon', 'I'],
    ['b_', 'B'],
    ['r_', 'R'],
    ['a_', 'A'],
    ['e_', 'E'],
    ['i_', 'I'],
    ['p_', 'P'],
    ['z_', 'Z'],
    ['d_', 'D'],
    # ['bx', 'Bx'],
    # ['bx2', 'Bx'],
]
picture_cols += list(zip(var_pic_keys, var_pic_hdrs)) + [['description', 'Description']]
mades = {False: '<i>%(name)s</i>', True: '%(name)s'}
format_attributes = ['format_description', 'format_body', 'format_interior', 'format_windows', 'format_base',
                     'format_wheels', 'format_with']


# ---- the manno object ----------------------


class MannoFile(object):
    def __init__(self, pif, withaliases=False, madeonly=False):
        self.madeonly = madeonly
        self.section = pif.form.get_id('section')
        if self.section == 'all':
            self.section = ''
        self.mod_id = pif.form.get_str('mod_id')
        self.start = pif.form.get_int('start', 1)
        self.end = pif.form.get_int('end', 9999)
        self.firstyear = pif.form.get_int('syear', 1)
        self.lastyear = pif.form.get_int('eyear', 9999)
        self.nodesc = pif.form.get_int('nodesc')
        self.revised = pif.form.get_int('revised')
        self.model_type = pif.form.get_str('mtype')
        self.tdict = {x['vehicle_type.ch']: x['vehicle_type.name'] for x in pif.dbh.fetch_vehicle_types()}
        self.vehtypes = pif.form.get_list_by_value('type', 'ynm')
        self.addtypes = pif.form.get_list_by_value('add', 'ynm')
        self.pictypes = pif.form.get_list_by_value('pic', 'ynm')
        self.plist = man_sections  # [x['page_info.id'] for x in pif.dbh.fetch_pages({'format_type': 'manno'})]
        slist = pif.dbh.fetch_sections({'id': useful.clean_id(self.section)}  # , 'page_id': pif.page_id})
                                       if self.section else {'page_id': pif.page_id})
        if not slist:
            raise useful.SimpleError(f'Requested section not found: {self.section}')
#        aliases = pif.dbh.fetch_aliases()
        adict = {}
#        for alias in aliases:
#            adict.setdefault(alias['alias.ref_id'], list())
#            adict[alias['alias.ref_id']].append(alias)
        self.mdict = {}
        self.sdict = {}
        self.slist = []
        for section in slist:
            if section['section.page_id'] in self.plist and (not self.section or section['id'] == self.section):
                section.setdefault('model_ids', list())
                self.sdict[section['id']] = section
                self.slist.append(section)

        # useful.write_message(self.start, self.end, self.firstyear, self.lastyear, self.model_type, self.nodesc)
        for casting in pif.dbh.fetch_casting_list(section_id=self.section):  # (page_id=pif.page_id):
            self.add_casting(pif, casting, aliases=adict.get(casting['base_id.id'], []))
        if withaliases:
            for alias in pif.dbh.fetch_aliases(where=["alias.section_id != ''", "alias.type in ('MP','MB')"]):
                if alias['alias.section_id']:
                    # self.add_casting(pif, alias)
                    self.add_alias(pif, alias)

    def add_casting(self, pif, casting, aliases=[]):
        manitem = pif.dbh.modify_man_item(casting)
        aliases = [x for x in aliases if x['alias.type'] == 'mack']
        manitem['mack'] = ','.join(models.get_mack_numbers(pif, manitem['id'], manitem['model_type'], aliases))
        if manitem['section_id'] in self.sdict and manitem['id'] not in self.sdict[manitem['section_id']]['model_ids']:
            self.add_item(manitem['id'], manitem)

    def add_alias(self, pif, alias):
        if alias['alias.section_id'] in self.sdict:
            manitem = pif.dbh.modify_man_item(alias)
            manitem['section_id'] = manitem['alias.section_id']
            if 'ref_id' in manitem:
                refitem = copy.deepcopy(self.mdict[manitem['ref_id']])
                if manitem['first_year']:
                    refitem['first_year'] = manitem['first_year']
                refitem['id'] = manitem['id']
                refitem['descs'] = manitem['descs']
                refitem['descs'].append('same as ' + manitem['ref_id'])
                refitem['vehicle_type'] = manitem['vehicle_type'] or ''
                manitem = refitem
            self.add_item(manitem['alias.id'], manitem)

    def add_item(self, man_id, manitem):
        if self.is_item_shown(manitem) and man_id not in self.mdict:
            manitem['nodesc'] = self.nodesc
            manitem['type_desc'] = self.types(manitem['vehicle_type'])
            self.sdict[manitem['section_id']]['model_ids'].append(man_id)
            self.mdict[man_id] = manitem
            # useful.write_message('ai', manitem['id'])

    def types(self, typespec):
        return ', '.join([self.tdict.get(t, '') for t in typespec or [] if t])

    def run_thing(self, pif, FunctionShowSection):
        sections = list()
        for sec in self.slist:
            # if sec['model_ids']:
            sec['model_ids'].sort()
            sections.append(FunctionShowSection(pif, sec))
        return sections

    def is_item_shown(self, mod):
        '''Makes decision of whether to show based on vehicle type, # range, and year range.'''
        if self.model_type and mod['model_type'] != self.model_type:
            return False

        if self.revised and not mod['revised']:
            return False

        if self.start and self.end:
            modno = 0
            for c in mod['id']:
                if c.isdigit():
                    modno = 10 * modno + int(c)
            if modno < self.start or modno > self.end:
                return False

        if mod['first_year'] and (self.firstyear > int(mod['first_year']) or self.lastyear < int(mod['first_year'])):
            return False

        at_y = self.addtypes.get('y', [])
        at_n = self.addtypes.get('n', [])
        pt_y = self.pictypes.get('y', [])
        pt_n = self.pictypes.get('n', [])
        if not mbdata.type_check(self.vehtypes['n'], self.vehtypes['y'], mod['vehicle_type']):
            return False

        if at_y or at_n:
            add_pics = ''.join(set([os.path.basename(x)[0] for x in glob.glob(
                useful.relpath('.', config.IMG_DIR_ADD, "?_" + mod['id'].lower() + '*.*'))]))
            if not mbdata.type_check(at_n, at_y, add_pics):
                return False

        if pt_y or pt_n:
            mod_pics = ''.join(set([os.path.basename(x)[0] for x in glob.glob(
                useful.relpath('.', config.IMG_DIR_MAN, "?_" + mod['id'].lower() + '*.*'))]))
            if not mbdata.type_check(pt_n, pt_y, mod_pics):
                return False

        if self.madeonly and not mod['made']:
            return False

        return True

    # ----- castings --------------------------------------------

    def show_section_manno_template(self, pif, sect):
        lsec = render.Section(
            section=sect,
            anchor=sect['id'],
            range=[render.Range(entry=[
                render.Entry(data=x)
                for x in models.generate_model_table_pic_link_dict(pif, self.mdict, sect['model_ids'])])]
        )
        if pif.form.get_bool('large'):
            lsec.columns = 1
        return lsec

    def run_manno_template(self, pif):
        llineup = render.Matrix(columns=4)
        llineup.section = self.run_thing(pif, self.show_section_manno_template)
        pif.ren.set_button_comment(pif, keys={'sel': 'selection', 'ran': 'range', 'start': 'start', 'end': 'end'})
        return pif.ren.format_template('mannum.html', llineup=llineup.prep())

    # ----- check list ------------------------------------------

    def get_section_list(self, pif, sect):
        cols = 3
        sect['entry'] = [models.add_model_table_list_entry_dict(pif, self.mdict.get(modid, {}))
                         for modid in useful.reflect(sect['model_ids'], cols)]
        sect['columns'] = cols
        sect['anchor'] = sect['id']
        return sect

    def run_checklist_template(self, pif):
        llineup = dict(columns=3)
        llineup['section'] = self.run_thing(pif, self.get_section_list)
        pif.ren.set_button_comment(pif, keys={'sel': 'selection', 'ran': 'range', 'start': 'start', 'end': 'end'})
        return pif.ren.format_template('manckl.html', llineup=llineup)

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
            mdict['prefix'] = mbdata.IMG_SIZ_TINY
            ran['entry'].append(models.add_model_table_pic_link_dict(pif, mdict))
        sect['range'].append(ran)
        return sect

    def run_thumbnails_template(self, pif):
        llineup = dict(columns=6)
        llineup['section'] = self.run_thing(pif, self.get_section_thumbs)
        pif.ren.set_button_comment(pif, keys={'sel': 'selection', 'ran': 'range', 'start': 'start', 'end': 'end'})
        return pif.ren.format_template('manthm.html', llineup=llineup)

    # ----- admin -----------------------------------------------

    def show_list_var_info(self, pif, mdict):
        mvars = pif.dbh.fetch_variations(mdict['id'])
        fields = ['description', 'base', 'body', 'interior', 'wheels', 'windows', 'with', 'text']
        keys = ['de', 'ba', 'bo', 'in', 'wh', 'wi', 'w/', 'bt']
        ver = set()
        t2k = dict(zip(fields, keys))
        td = {x: 0 for x in keys}
        fy = ly = None
        id_set = set()
        varc = varl = 0
        for var in mvars:
            if var['variation.variation_type'] != '2':
                varl += 1
                if var.get('vs'):
                    varc += 1
            var_id = var['variation.var']
            if var_id[0].isdigit():
                while not var_id[-1].isdigit():
                    var_id = var_id[:-1]
                id_set.add(int(var_id))
            for txt in fields:
                if not mdict.get('format_' + txt):
                    td[t2k[txt]] = None
                elif var['variation.text_' + txt] or not mdict['format_' + txt]:
                    td[t2k[txt]] += 1
            yr = var['variation.date'].strip()[:4]
            if yr.isdigit():
                if not fy:
                    fy = yr
                if not ly:
                    ly = yr
                fy = min(fy, yr)
                ly = max(ly, yr)
            ver.add(var['variation.flags'] & (config.FLAG_MODEL_ID_INCORRECT | config.FLAG_MODEL_VARIATION_VERIFIED))
        if id_set:
            min_id = min(id_set)
            max_id = max(id_set)
            contig = not bool(set(range(min_id, max_id + 1)) - id_set)
            varids = f'<span class="{"ok" if contig else "no"}">{min_id}-{max_id}</span>'
        else:
            varids = '-'
        for key in td:
            td[key] = (
                pif.ren.fmt_star('gray', hollow=True) if not len(mvars) or td[key] is None else
                pif.ren.fmt_star('green') if td[key] == len(mvars) else
                pif.ren.fmt_star('red') if not td[key] else
                pif.ren.fmt_star('orange'))
        varl = (f'<a href="vars.cgi?list=1&mod={mdict["id"]}">'
                f'<span class="{pif.ren.fmt_okno(varc == varl)}">{varc}/{varl}</span></a>')
        td.update({'fvyear': fy if fy else '-', 'lvyear': ly if ly else '-',
                   'varids': varids, 'varl': varl, 'ver': ver})
        return td

    def get_admin_entries(self, pif, model_ids):
        vers = {
            config.FLAG_MODEL_ID_INCORRECT | config.FLAG_MODEL_VARIATION_VERIFIED: "fas fa-times red",
            config.FLAG_MODEL_VARIATION_VERIFIED: "fas fa-check black",
            0: "far fa-circle gray",
        }
        # 'alias' : list of aliases, separated by br
        aliases = {}
        for alias in pif.dbh.fetch_aliases():
            aliases.setdefault(alias['alias.ref_id'], [])
            aliases[alias['alias.ref_id']].append(alias['alias.id'])
        for mod in model_ids:
            mdict = self.mdict[mod]
            mdict.setdefault('own', '')
            mdict.setdefault('mydesc', '')
            mdict['name'] = mades[int(mdict['made'])] % mdict
            mdict['alias'] = '<br>'.join(aliases.get(mod, []))
            mdict.update({
                'fvyear': '', 'lvyear': '',
                'notes': 'N' if mdict.get('notes') else '',
                'vid': '<a href="vars.cgi?edt=1&mod=%(id)s">%(id)s</a>' % mdict,
                'nl': '<a href="single.cgi?id=%(id)s">%(name)s</a>' % mdict})
            if mdict['flags'] & config.FLAG_MODEL_CASTING_REVISED:
                mdict['vid'] = '<nobr>' + mdict['vid'] + pif.ren.fmt_circle('green') + '<nobr>'
            mdict.update(self.show_list_var_info(pif, mdict))
            if not mdict['vehicle_type']:
                mdict['vehicle_type'] = '<i class="fas fa-ban red"></i>'
            fmt_bad, _, _ = pif.dbh.check_description_formatting(mdict['id'])
            mdict['fo'] = pif.ren.fmt_times('red') if fmt_bad else ''
            mdict['im'] = ''.join([f'<i class="{vers[x]}"></i>' for x in sorted(mdict['ver'])])
            makes = pif.dbh.fetch_casting_makes(mod)
            mdict['make'] = '<br>'.join([
                pif.ren.format_link(f"/cgi-bin/makes.cgi?make={x['vehicle_make.id']}", str(x['vehicle_make.name']))
                for x in makes
            ])
            mdict['attr'] = '<br>'.join(sorted([x['attribute.attribute_name'] for x in pif.dbh.fetch_attributes(mod)]))
            if mdict['make']:
                mdict['make'] = pif.ren.format_link("/cgi-bin/makes.cgi?make=" + mdict['make'], mdict['make'])
            relateds = [x['casting_related.related_id']
                        for x in pif.dbh.fetch_casting_relateds(mod, section_id='single')]
            mdict['rel'] = '<br>'.join([pif.ren.format_link('/cgi-bin/single.cgi', x, {'id': x}) for x in relateds])
            yield mdict

    def get_section_admin(self, pif, sect):
        cols = admin2_cols if pif.form.get_bool('t') else admin_cols
        return render.Section(
            section=sect,
            colist=[x[0] for x in cols],
            headers=dict(cols),
            range=[render.Range(
                entry=self.get_admin_entries(pif, sect.model_ids),
                styles={x[0]: x[0] for x in cols})
            ])

    def run_admin_list_template(self, pif):
        llistix = render.Listix()
        llistix.section = self.run_thing(pif, self.get_section_admin)
        pif.ren.set_button_comment(pif, keys={'sel': 'selection', 'ran': 'range', 'start': 'start', 'end': 'end'})
        return pif.ren.format_template('simplelistix.html', llineup=llistix)

    # ----- links -----------------------------------------------

    def get_links_entries(self, pif, model_ids):
        for mod in model_ids:
            mdict = self.mdict[mod]
            mdict.update({x: '-' for x in l_links})
            for lnk in pif.dbh.fetch_link_lines("single." + mdict['id']):
                mdict[str(lnk['link_line.associated_link'])] = pif.ren.format_link(lnk['link_line.url'], 'X')
            mdict['name'] = mades[int(mdict['made'])] % mdict
            mdict.update({
                'vid': '<a href="vars.cgi?list=1&mod=%(id)s">%(id)s</a>' % mdict,
                'nl': '<a href="single.cgi?id=%(id)s">%(name)s</a>' % mdict})
            yield mdict

    def get_section_links(self, pif, sect):
        return render.Section(
            section=sect,
            colist=[x[0] for x in links_cols],
            headers=dict(links_cols),
            range=[render.Range(
                entry=self.get_links_entries(pif, sect['model_ids']),
                styles={x[0]: x[0] for x in links_cols})],
        )

    def run_links_list_template(self, pif):
        llistix = render.Listix()
        llistix.section = self.run_thing(pif, self.get_section_links)
        pif.ren.set_button_comment(pif, keys={'sel': 'selection', 'ran': 'range', 'start': 'start', 'end': 'end'})
        return pif.ren.format_template('simplelistix.html', llineup=llistix)

    # ----- picture -----------------------------------------------

    picprefixes = [
        ['a_', 'a'],
        ['b_', 'a'],
        ['d_', 'a'],
        ['e_', 'a'],
        ['i_', 'a'],
        ['p_', 'a'],
        ['r_', 'a'],
        ['z_', 'a'],

        ['l_', 'm'],
        ['m_', 'm'],
        ['s_', 'm'],
        ['t_', 'm'],

        ['icon', 'i'],
    ]

    def show_list_pic(self, pif, prefix, mod_id, txt):
        mod_id = mod_id.replace('/', '_').lower()
        pset = self.addpics.get(mod_id, set()) if prefix[1] == 'a' else self.manpics.get(mod_id, set())
        return [prefix[0], txt.upper() if prefix[0][0] in pset else '-']

    def show_box_pics(self, box_types):

        def mkpth(ty):
            return useful.relpath(
                '.', config.IMG_DIR_BOX,
                'x_' + mod_id + '-' + ty['box_type.box_type'][0] + ty['box_type.pic_id'] + '*.jpg').lower()

        if box_types:
            mod_id = box_types[0]['box_type.mod_id']
            base_box_types = list(set([box['box_type.box_type'][0] for box in box_types]))
            base_box_count = sum([int(bool(len(glob.glob(useful.relpath(
                '.', config.IMG_DIR_BOX, mbdata.IMG_SIZ_SMALL + '_' + mod_id + '-' + ty + '*.jpg').lower()))))
                for ty in base_box_types])
            box_count = sum([int(bool(len(glob.glob(mkpth(ty))))) for ty in box_types])
            return {'bx': models.fmt_var_pic(base_box_count, len(base_box_types)),
                    'bx2': models.fmt_var_pic(box_count, len(box_types))}
        return {'bx': '-', 'bx2': '-'}

    def show_attr_pics(self, pif, mod_id):
        cnt = tot = 0
        var_id = ''
        for attr_pic in pif.dbh.depref('attribute_picture', pif.dbh.fetch_attribute_pictures(mod_id)):
            tot += 1
            img_id = (mod_id + ('-' + var_id if var_id else '')).lower() + (
                '-' + attr_pic['picture_id'] if attr_pic['picture_id'] else '')
            pdir = config.IMG_DIR_VAR if var_id else config.IMG_DIR_ADD
            if pif.ren.find_image_path(img_id, prefix=attr_pic['attr_type'], pdir='.' + pdir):
                cnt += 1
        return cnt, tot

    def count_list_var_pics(self, pif, mod_id):
        vars = pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id))
        needs_c = needs_f = needs_a = needs_1 = needs_2 = needs_p = 0
        found_c = found_f = found_a = found_1 = found_2 = found_p = 0
        # nf = []
        for var in vars:
            if not var['picture_id']:
                is_found = var['var'] in self.varpics.get(var['mod_id'], {})
                ty_var = models.calc_var_type(pif, var), is_found

                needs_a += 1
                found_a += is_found
                if ty_var == 'p':
                    needs_p += 1
                    found_p += is_found
                elif ty_var == 'f':
                    needs_f += 1
                    found_f += is_found
                elif ty_var == 'c':
                    needs_c += 1
                    found_c += is_found
                elif ty_var == '2':
                    needs_2 += 1
                    found_2 += is_found
                else:
                    needs_1 += 1
                    found_1 += is_found
        return (found_a, found_c, found_1, found_2, found_f, found_p), \
               (needs_a, needs_c, needs_1, needs_2, needs_f, needs_p), \
               (None,)

    def get_picture_model_entries(self, pif, model_ids):
        photogs = {x['photo_credit.name'].lower(): x['photographer.id']
                   for x in pif.dbh.fetch_photo_credits_for_models('.' + config.IMG_DIR_MAN)}
        for mod in model_ids:
            vcredits = {x['photo_credit.name'].lower(): x['photographer.id']
                        for x in pif.dbh.fetch_photo_credits_for_vars(path=config.IMG_DIR_VAR[1:], name=mod)}
            mdict = self.mdict[mod]
            mdict.update(dict([self.show_list_pic(pif, x, mdict['id'], x[0][0]) for x in self.picprefixes]))
            mdict.update({
                'img': self.show_list_pic(pif, ['s_', '.' + config.IMG_DIR_MAN], mdict['id'], mbdata.IMG_SIZ_SMALL)[1],
                'vid': '<a href="vars.cgi?edt=1&mod=%(id)s">%(id)s</a>' % mdict,
                'first_year': '<a href="traverse.cgi?g=1&d=%s">%s</a>' % (
                    useful.relpath(config.LIB_MAN_DIR, mdict['id'].lower()), mdict['first_year']),
                'name': mades[int(mdict['made'])] % mdict,
                'nl': '<a href="single.cgi?id=%(id)s">%(name)s</a>' % mdict,
                'credit': '<a href="vars.cgi?vdt=1&mod=%s">%s</a>' % (mod, photogs.get(mod.lower(), '--')),
                'icon': self.show_list_pic(pif, ['i_', '.' + config.IMG_DIR_MAN_ICON], mdict['id'], 'i')[1]})
            founds, needs, _, id_set = models.count_list_var_pics(pif, mdict['id'])
            # mdict.update(self.show_box_pics(pif.dbh.fetch_box_type_by_mod(mdict['id'])))
            for ipix in range(0, 6):
                self.totals[ipix]['have'] += founds[ipix]
                self.totals[ipix]['total'] += needs[ipix]
            mdict.update(dict(zip(var_pic_keys, models.fmt_var_pics(founds, needs))))
            mdict['credvars'] = '<span class="%s">%d/%d</span>' % (
                'ok' if len(vcredits) == founds[0] else 'no', len(vcredits), founds[0])
            if mdict['flags'] & config.FLAG_MODEL_CASTING_REVISED:
                mdict['vid'] = '<nobr>' + mdict['vid'] + pif.ren.fmt_circle('green') + '<nobr>'
            if not mdict['made']:
                mdict['nl'] = '<i>' + mdict['nl'] + '</i>'
            mdict['d_'] = models.fmt_var_pic(*self.show_attr_pics(pif, mod))
            # useful.write_comment(mdict)
            yield mdict

    def get_section_picture(self, pif, sect):
        return render.Section(
            colist=[x[0] for x in picture_cols],
            headers=dict(picture_cols),
            range=[render.Range(
                entry=[x for x in self.get_picture_model_entries(pif, sect['model_ids'])],
                styles={x[0]: x[0] for x in picture_cols},
            )])

    def run_picture_list(self, pif):
        self.totals = [{'tag': x, 'have': 0, 'total': 0} for x in var_pic_hdrs]
        llineup = render.Listix()
        llineup.section = self.run_thing(pif, self.get_section_picture)
        llineup.totals = self.totals
        return llineup

    def run_picture_list_template(self, pif):
        def pathsplit(x):  # a_b-c.d
            _, b = os.path.split(x)
            b, d = os.path.splitext(b)
            c = b.rfind('-') if '-' in b else 0  # it's never zero
            b, c = (b[:c], b[c + 1:]) if c else (b, '')
            return b[0:1], b[2:], c, d[1:] if d and d[1:] in render.graphic_types else ''

        self.manpics = {}
        for pic in glob.glob('.' + config.IMG_DIR_MAN + '/?_*.*') + glob.glob('.' + config.IMG_DIR_MAN_ICON + '/?_*.*'):
            a, b, c, d = pathsplit(pic)
            if d:
                self.manpics.setdefault(b, set())
                self.manpics[b].add(a)

        self.varpics = {}
        for pic in glob.glob('.' + config.IMG_DIR_VAR + '/?_*.*'):
            a, b, c, d = pathsplit(pic)
            if d and c:
                self.varpics.setdefault(b, set())
                self.varpics[b].add(c)

        self.addpics = {}
        for pic in glob.glob('.' + config.IMG_DIR_ADD + '/?_*.*'):
            a, b, c, d = pathsplit(pic)
            if d:
                self.addpics.setdefault(b, set())
                self.addpics[b].add(a)

        llineup = self.run_picture_list(pif)
        pif.ren.set_button_comment(pif, keys={'sel': 'selection', 'ran': 'range', 'start': 'start', 'end': 'end'})
        return pif.ren.format_template('manpxl.html', llineup=llineup)

    # currently not in use
    def get_mine(self, dblist, mans):
        # dats = dict()
        mine = dict()
        for mdict in dblist:
            if not mdict:
                pass
            # elif llist[0] == 'data':
                # dats[llist[1]] = llist[2].split(',')
            else:
                # mdict = dict(zip(dats[llist[0]], llist[1:]))
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

    def get_vt_model_table(self, pif, mdict, flago):
        img = [mbdata.IMG_SIZ_SMALL + '_' + mdict['id']]
        if mdict.get('picture_id'):
            img = [mbdata.IMG_SIZ_SMALL + '_' + mdict['picture_id']]
        for s in mdict['descs']:
            if s.startswith('same as '):
                img.append(mbdata.IMG_SIZ_SMALL + '_' + s[8:])
        lnk = 'single.cgi?id=%(id)s' % mdict
        mdict['flag'] = (mdict.get('country', '') or "") + ' '
        if mdict.get('country') in flago:
            mdict['flag'] += pif.ren.format_image_flag(mdict['country'], flago[mdict['country']])
        elif mdict['unlicensed'] == '-':
            mdict['flag'] = pif.ren.format_image_art('mbx.gif')
        mdict['makename'] = ' - '.join([
            pif.ren.format_link("/cgi-bin/makes.cgi?make={}".format(
                x.get('vehicle_make.id', '???') or 'unl'), x.get('vehicle_make.name', 'unset') or 'unlicensed')
            for x in pif.dbh.fetch_casting_makes(mdict['id'])
        ])
        mdict['name'] = pif.ren.format_link(
            lnk, mdict['id'] + '<br>' + mdict['rawname'] + '<br>' + mdict['flag'] + '<br>' + mdict['makename'])
        mdict['img'] = pif.ren.format_link(lnk, pif.ren.format_image_required(img, made=mdict['made']))
        mdict['sel'] = pif.form.put_checkbox(
            'vt_' + mdict['id'],
            [[x, mbdata.vehicle_types[x]] for x in list(mbdata.model_type_chars[:14])],
            checked=mdict['vehicle_type']) + '<br>'
        mdict['sel'] += pif.form.put_checkbox(
            'vt_' + mdict['id'],
            [[x, mbdata.vehicle_types[x]] for x in list(mbdata.model_type_chars[14:])],
            checked=mdict['vehicle_type']) + '<br>'
        mdict['sel'] += 'make: ' + pif.form.put_text_input('vm_' + mdict['id'], 3, 3, value=mdict['make'])
        mdict['sel'] += 'country: ' + pif.form.put_text_input('co_' + mdict['id'], 2, 2, value=mdict['country'])
        return mdict

    def show_vt_model_table(self, pif, mdict, flago):
        return vt_fmtb % self.get_vt_model_table(pif, mdict, flago)

    def show_section_vehicle_type_template(self, pif, sect):
        flago = mflags.FlagList()
        sect['entry'] = [self.get_vt_model_table(pif, self.mdict[mod], flago) for mod in sect['model_ids']]
        return sect

    def write_vehicle_types(self, pif):
        for key in pif.form.keys(start='vt_'):
            val = ''.join(pif.form.get_list(key))
            # useful.write_message(key[3:], 'type', val, '<br>')
            pif.dbh.write_casting(values={'vehicle_type': val}, id=key[3:])
        for key in pif.form.keys(start='vm_'):
            # useful.write_message(key[3:], 'make', pif.form.get_str(key), '<br>')
            pif.dbh.write_casting(values={'make': pif.form.get_str(key)}, id=key[3:])
            pif.dbh.update_casting_make(key[3:], pif.form.get_str(key), verbose=True)
        for key in pif.form.keys(start='co_'):
            # useful.write_message(key[3:], 'country', pif.form.get_str(key), '<br>')
            pif.dbh.write_casting(values={'country': pif.form.get_str(key)}, id=key[3:])

    def run_vehicle_type_list_template(self, pif):
        if pif.form.get('vtset'):
            self.write_vehicle_types(pif)
        llineup = dict()
        llineup['cols'] = vt_cols
        llineup['num_cols'] = len(vt_cols)
        llineup['section'] = self.run_thing(pif, self.show_section_vehicle_type_template)
        pif.ren.set_button_comment(pif, keys={'sel': 'selection', 'ran': 'range', 'start': 'start', 'end': 'end'})
        return pif.ren.format_template('manvtl.html', llineup=llineup)

    # ----- csv -------------------------------------------------

    def show_section_man2csv(self, pif, sect):
        ret = list()
        for mod_id in sect['model_ids']:
            mod = self.mdict[mod_id]
            # aliases = [x['alias.id'] for x in pif.dbh.fetch_aliases(mod_id, 'mack')]
            # mack_nums = ','.join(models.get_mack_numbers(pif, mod_id, mod['model_type'], aliases))
            ret.append(
                [mod_id, mod.get('mack', ''), mod['first_year'], mod['scale'], mod['name'], ', '.join(mod['descs'])])
        return ret

    def run_man2csv_out(self, pif):
        out_file = StringIO()
        field_names = ["MAN #", "Mack #", "Year", "Scale", "Name", "Notes"]
        writer = csv.DictWriter(out_file, fieldnames=field_names)
        writer.writeheader()
        secs = self.run_thing(pif, self.show_section_man2csv)
        for sec in secs:
            for ln in sec:
                writer.writerow(dict(zip(field_names, ln)))
        out_str = out_file.getvalue()
        out_file.close()
        return out_str

    # ----- var csv ---------------------------------------------

    def show_section_man2varcsv(self, pif, sect):
        ret = list()
        for mod_id in sect['model_ids']:
            mod = self.mdict[mod_id]
            for var in pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)):
                img = pif.ren.find_image_path([mod_id], nobase=True, vars=var['picture_id'] or var['var'],
                                              largest='IMG_SIZ_LARGEST')
                ret.append(
                    [mod_id, mod['first_year'], mod['name'], var['var'], var['text_description'], img])
        return ret

    def run_man2varcsv_out(self, pif):
        out_file = StringIO()
        field_names = ["MAN #", "Year", "Name", "Var", "Description", "Image"]
        writer = csv.DictWriter(out_file, fieldnames=field_names)
        writer.writeheader()
        secs = self.run_thing(pif, self.show_section_man2varcsv)
        for sec in secs:
            for ln in sec:
                writer.writerow(dict(zip(field_names, ln)))
        out_str = out_file.getvalue()
        out_file.close()
        return out_str

    # ----- json ------------------------------------------------

    def show_section_man2json(self, pif, sect):
        field_keys = ["man", "mack", "year", "scale", "name", "notes"]
        ret = list()
        for mod_id in sect['model_ids']:
            mod = self.mdict[mod_id]
            # aliases = [x['alias.id'] for x in pif.dbh.fetch_aliases(mod_id, 'mack')]
            # mack_nums = ','.join(models.get_mack_numbers(pif, mod_id, mod['model_type'], aliases))
            ret.append(dict(zip(field_keys,
                       [mod_id, mod['mack'], mod['first_year'], mod['scale'], mod['name'], ', '.join(mod['descs'])])))
        return ret

    def run_man2json_out(self, pif):
        secs = self.run_thing(pif, self.show_section_man2json)
        return json.dumps(secs)

    # ----- text ------------------------------------------------

    def show_section_text_list(self, pif, sect):
        field_keys = ["man", "mack", "year", "scale", "name", "notes"]
        ret = list()
        for mod_id in sect['model_ids']:
            mod = self.mdict[mod_id]
            # aliases = [x['alias.id'] for x in pif.dbh.fetch_aliases(mod_id, 'mack')]
            # mack_nums = ','.join(models.get_mack_numbers(pif, mod_id, mod['model_type'], aliases))
            ret.append(dict(zip(field_keys,
                       [mod_id, mod['mack'], mod['first_year'], mod['scale'], mod['name'], ', '.join(mod['descs'])])))
        return ret

    def run_text_list(self, pif):
        secs = self.run_thing(pif, self.show_section_text_list)
        fmt = '[_] %(man)-8s  %(name)-48s  %(year)s\n'
        return ''.join([''.join([fmt % y for y in x]) for x in secs])

    # ----- tilley list -----------------------------------------

    var_pic_cols = ['ID', 'Description', 'Type', 'Date', 'Cat', 'Cred', 'Pic', 'T', 'S', 'M', 'L']

    def get_section_credit_list(self, pif, sect):
        ents = []
        for mod_id in sect['model_ids']:
            mod_row, var_rows = self.list_var_pics(pif, self.mdict[mod_id])
            if var_rows:
                ents.extend([mod_row] + var_rows)
        section = render.Section(section=sect, colist=self.var_pic_cols, anchor=sect['id'], id='',
                                 range=[render.Range(entry=ents)])
        return section

    def run_var_credit_list(self, pif):
        self.pic0 = pif.form.get_str('pic0')
        self.pic1 = pif.form.get_str('pic1')
        self.photog = pif.form.get_str('photog')
        self.photognot = pif.form.get_str('photognot')
        self.var_type = pif.form.get_list('vtype')
        self.til_list = imglib.get_tilley_file()

        # a listix consists of a header (outside of the tables) plus a list of sections, each in its own table.
        #     id, name, note, graphics, tail | section
        # a section consists of a header (inside the table) plus a list of entries.
        #     id, name, note, anchor, columns, headers | range
        # a range consists of a header plus a list of entries.
        #     id, name, note, anchor, graphics, styles | entry
        # an entry contains a dict of cells, keys in columns.
        #     <text>

        llineup = render.Listix()
        llineup.section = self.run_thing(pif, self.get_section_credit_list)
        return llineup

    def list_var_pics(self, pif, mod):

        def mk_star(has_thing):
            return pif.ren.fmt_star('green' if has_thing else 'white')

        mod_id = mod['id']
        var_rows = []
        phcred = pif.dbh.fetch_photo_credit(path=config.IMG_DIR_MAN[1:], name=mod_id)
        mod_row = {
            'ID': mod['id'],
            'Description': mod['name'],
            'Cat': '',
            'Date': '',
            'Type': mod['model_type'],
            'Cred': phcred['photographer.id'] if phcred else '',
            'Pic': '',
        }
        mod_row.update(varias.check_picture_sizes(config.IMG_DIR_MAN, mod_id + '.jpg', mk_star))
        credits = {x['photo_credit.name'].lower(): x['photographer.id'] for x in
                   pif.dbh.fetch_photo_credits_for_vars(path=config.IMG_DIR_VAR[1:], name=mod_id, verbose=False)}
        varlist = pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id))
        count_var = 0
        count_cred = 0
        for var in varlist:
            if var['picture_id']:
                continue
            if var['variation_type'] and var['variation_type'] not in self.var_type:
                continue
            # var['varsel'] = pif.dbh.fetch_variation_selects(var['mod_id'], var['var'])
            var['phcred'] = credits.get(('%s-%s' % (var['mod_id'], var['var'])).lower(), '')
            # var['ty_var'], var['is_found'], var['has_de'], var['has_ba'], var['has_bo'], var['has_in'],
            # var['has_wh'], var['has_wi'], var['has_wt'] = models.calc_var_pics(pif, var)
            count_var += 1
            if self.photog and var['phcred'] == self.photog:
                count_cred += 1
                if self.photognot:
                    continue
            elif not self.photognot:
                continue
            # cat_vs = set([x['variation_select.category'] for x in var['varsel']])
            cat = var['category']  # .join(cat_vs)
            var_row = {
                'ID': var['mod_id'] + '-' + var['var'],
                'Description': var['text_description'],
                'Cat': cat,
                'Date': var['date'],
                'Type': mbdata.var_types.get(var['variation_type'], var['variation_type']),
                'Cred': var['phcred'],
                'Pic': var['picture_id'],
            }
            var_row.update(varias.check_picture_sizes(
                config.IMG_DIR_VAR, var['mod_id'] + '-' + var['var'] + '.jpg', mk_star))
            if not self.pic0 and not var_row['_any']:
                continue
            if not self.pic1 and var_row['_any']:
                continue
            # for sz in mbdata.image_size_types:
            #     var_row[sz.upper()] = mk_star(
            #         os.path.exists(useful.relpath('.', config.IMG_DIR_VAR,
            #                   sz + '_' + var['mod_id'] + '-' + var + '.jpg').lower()))
            var_row['ID'] = '<a href="/cgi-bin/vars.cgi?mod=%s&var=%s">%s</a>' % (
                var['mod_id'], var['var'], var_row['ID'])
            var_rows.append(var_row)
        mod_row['Cat'] = ''
        mod_row['Pic'] = ('(zero)' if not count_var else '(all)' if count_var == count_cred else
                          ('%d/%d' % (count_cred, count_var)))
        mod_row['Description'] = '<a href="/cgi-bin/single.cgi?id=%s">%s</a>' % (mod['id'], mod['name'])
        mod_row['ID'] = '<a href="/cgi-bin/vars.cgi?mod=%s&vdt=1">%s</a>' % (
            mod['id'], mod['id']) + ' ' + mk_star(mod_id.lower() in self.til_list)
        mod_row['style'] = '2'
        # if self.photog:
        #     if self.photognot and mod_row['Cred'] == self.photog:# and count_var == count_cred:
        #         return [mod_row, {'Description': 'all relevant pictures credited'}]
        #     if not self.photognot and mod_row['Cred'] != self.photog:
        #         return [mod_row, {'Description': 'no relevant pictures credited'}]
        # useful.write_comment(str([mod_row] + var_rows))
        return mod_row, var_rows

    # ----- main ------------------------------------------------

    formatters = {
        mbdata.LISTTYPE_CSV: run_man2csv_out,
        mbdata.LISTTYPE_JSON: run_man2json_out,
        mbdata.LISTTYPE_ADMIN: run_admin_list_template,
        mbdata.LISTTYPE_LINK: run_links_list_template,
        mbdata.LISTTYPE_PICTURE: run_picture_list_template,
        mbdata.LISTTYPE_CHECKLIST: run_checklist_template,
        mbdata.LISTTYPE_THUMBNAIL: run_thumbnails_template,
        mbdata.LISTTYPE_VEHICLE_TYPE: run_vehicle_type_list_template,
        mbdata.LISTTYPE_TEXT: run_text_list,
        mbdata.LISTTYPE_TILLEY: run_var_credit_list,
        mbdata.LISTTYPE_VAR_CSV: run_man2varcsv_out,
    }

    def format_output(self, pif, listtype):
        pif.ren.print_html(mbdata.get_mime_type(listtype))
        return self.formatters.get(listtype, MannoFile.run_manno_template)(self, pif)


# ---- main ----------------------------------


@basics.web_page
def main(pif):
    # useful.write_comment(pif.form)
    if pif.form.has('submit'):
        # make new form and redirect
        form = {x: pif.form.get_str(x) for x in ['end', 'eyear', 'listtype', 'range', 'section', 'start', 'syear']}
        pics = pif.form.get_flags('pic_')
        adds = pif.form.get_flags('add_')
        types = pif.form.get_flags('type_')
        form.update({'addn': adds.get('n', ''), 'addy': adds.get('y', ''),
                     'picn': pics.get('n', ''), 'picy': pics.get('y', ''),
                     'typen': types.get('n', ''), 'typey': types.get('y', '')})
        raise useful.Redirect('manno.cgi?' + '&'.join([f'{x}={y}' for x, y in form.items() if y]))

    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append(pif.request_uri, 'Manufacturing Numbers')
    listtype = pif.form.get_str('listtype')
    if pif.form.get_str('num'):
        raise useful.Redirect(url="0;url=single.cgi?id=" + pif.form.get_str('num'))

    if not pif.form.has('section'):
        raise useful.SimpleError("Please select a range to display.")

    manf = MannoFile(pif, withaliases=True)
    return manf.format_output(pif, listtype)


# ---- admin main ----------------------------


@basics.web_page
def admin_main(pif):
    pif.ren.print_html()
    if pif.form.has('section'):
        manf = MannoFile(pif, madeonly=True)
        llineup = manf.format_output(pif, mbdata.LISTTYPE_TILLEY)
        return pif.ren.format_template('manadm.html', pagetype=1, llineup=llineup)
    else:
        sections = pif.dbh.fetch_sections({'page_id': 'manno'})
        limits = pif.dbh.fetch_casting_limits()
        first_year = int(limits['min(base_id.first_year)'])
        last_year = int(limits['max(base_id.first_year)'])
        # listtype = pif.form.get_str('listtype')
        llineup = render.Listix()
        return pif.ren.format_template(
            'manadm.html',
            pagetype=0,
            first_year=first_year,
            last_year=last_year,
            sections=sections,
            photogs=[(x.photographer.id, x.photographer.name) for x in pif.dbh.fetch_photographers()],
            llineup=llineup)

# ---- commands ------------------------------


def delete_casting(pif, mod_id, *args, **kwargs):
    pif.ren.message("delete", mod_id)
    pif.dbh.delete_base_id({'id': mod_id})
    pif.dbh.delete_casting({'id': mod_id})
    pif.dbh.delete_attribute({'mod_id': mod_id})
    pif.dbh.delete_variation({'mod_id': mod_id})
    pif.dbh.delete_detail({'mod_id': mod_id})

    patts = [
        '.' + config.IMG_DIR_MAN + '/?_%s.*' % mod_id,
        '.' + config.IMG_DIR_MAN + '/%s.*' % mod_id,
        '.' + config.IMG_DIR_VAR + '/?_%s-*.*' % mod_id,
        '.' + config.IMG_DIR_VAR + '/%s-*.*' % mod_id,
        '.' + config.IMG_DIR_MAN_ICON + '/?_%s-*.*' % mod_id,
        '.' + config.IMG_DIR_ADD + '/?_%s.*' % mod_id,
        '.' + config.IMG_DIR_CAT + '/?_%s.*' % mod_id,
        '.' + config.IMG_DIR_CAT + '/?_%s_*.*' % mod_id,
        '.' + config.IMG_DIR_CAT + '/%s.*' % mod_id,
        '.' + config.IMG_DIR_ADS + '/%s.*' % mod_id,
        '.' + config.IMG_DIR_SET_PLAYSET + '/?_%s.*' % mod_id,
        '.' + config.IMG_DIR_SET_PACK + '/?_%s.*' % mod_id,
        '.' + config.IMG_DIR_PROD_PLAYSET + '/?_%s.*' % mod_id,
        '.' + config.IMG_DIR_PROD_PACK + '/?_%s.*' % mod_id,
        '.' + config.IMG_DIR_PROD_PACK + '/%s.*' % mod_id,
    ]
    pif.ren.message("abandoning the following pics")
    pics = reduce(lambda x, y: x + glob.glob(y.lower()), patts, list())
    for pic in pics:
        pif.ren.message(pic)


def search_name(pif, targ):
    sections = man_sections
    fields = ['base_id.rawname']  # , 'base_id.id']
    where = ["%s like '%%%s%%'" % (y, x) for x in targ for y in fields]
    ret = list()
    for section in sections:
        ret += pif.dbh.fetch_casting_list(page_id=section, where=where, verbose=False)
    return ret


def run_text_search(pif, *args):
    if not args:
        return
    mods = [pif.dbh.modify_man_item(x) for x in search_name(pif, args)]
    mods.sort(key=lambda x: x['id'])
    for mod in mods:
        print_model(pif, mod)


def add_attributes(pif, mod_id=None, *attr_list):
    if not mod_id or not attr_list:
        return
    model = pif.dbh.fetch_casting(mod_id)
    if not model:
        print(f'{mod_id} does not exist.')
    for attr in attr_list:
        pif.dbh.insert_attribute(mod_id, attr)


def list_attributes(pif, mod_id):
    attrs = pif.dbh.depref('attribute', pif.dbh.fetch_attributes(mod_id, with_global=True))
    for attr in attrs:
        print(attr['attribute_name'],)
    print()


def clone_attributes(pif, old_mod_id=None, new_mod_id=None, *args, **kwargs):
    if not old_mod_id or not new_mod_id:
        return
    pif.dbh.clone_attributes(old_mod_id, new_mod_id)
    vals = pif.dbh.fetch('casting', columns=format_attributes, where={'id': old_mod_id})
    if vals:
        pif.dbh.write_casting(values=vals[0], id=new_mod_id)
    vals = pif.dbh.fetch('detail', where={'mod_id': old_mod_id, 'var_id': ''})
    # print(vals)
    for val in vals:
        val = pif.dbh.depref('detail', val)
        val['mod_id'] = new_mod_id
        pif.dbh.write_detail(values=val, where=None, newonly=True)
    # insert into detail (select 'MB880', '', attr_id, description from detail where mod_id='MB153' and var_id='');


def rename_base_id(pif, old_mod_id=None, new_mod_id=None, force=False, *args, **kwargs):
    if not old_mod_id or not new_mod_id:
        return
    rec = pif.dbh.fetch_base_id(new_mod_id)
    if rec and rec.id.lower() != new_mod_id.lower():
        if not force:
            # print(new_mod_id, "exists")
            return
    else:
        pif.ren.message("rename", old_mod_id, new_mod_id)
        pif.dbh.rename_base_id(old_mod_id, new_mod_id)

    dirs = [
        config.IMG_DIR_MAN,
        config.IMG_DIR_MAN,
        config.IMG_DIR_VAR,
        config.IMG_DIR_VAR,
        config.IMG_DIR_MAN_ICON,
        config.IMG_DIR_ADD,
        config.IMG_DIR_CAT,
        config.IMG_DIR_CAT,
        config.IMG_DIR_CAT,
        config.IMG_DIR_SET_PLAYSET,
        config.IMG_DIR_SET_PACK,
        config.IMG_DIR_PROD_PLAYSET,
        config.IMG_DIR_PROD_PACK,
        config.IMG_DIR_PROD_PACK,
        config.IMG_DIR_PACKAGE,
        config.IMG_DIR_ADS,
        config.IMG_DIR_BLISTER,
        config.IMG_DIR_BOOK,
        config.IMG_DIR_BOX,
        config.IMG_DIR_CAT,
        config.IMG_DIR_GAME,
    ]
    old_root = old_mod_id.lower()
    for x in dirs:
        for y in (glob.glob('.' + x + f'/{old_root}.*') +
                  glob.glob('.' + x + f'/?_{old_root}.*') +
                  glob.glob('.' + x + f'/?_{old_root}-*.*')):
            pic_new = y.replace(old_root, new_mod_id.lower())
            pif.ren.message("rename", y, pic_new, "<br>")
            os.rename(y, pic_new)


def copy_casting(pif, old_mod_id=None, new_mod_id=None, *args, **kwargs):
    if not old_mod_id or not new_mod_id:
        return

    if pif.dbh.fetch_base_id(new_mod_id) or pif.dbh.fetch_casting(new_mod_id):
        print(new_mod_id, "exists")
        return

    cas = pif.dbh.fetch_casting_raw(old_mod_id)
    bid = pif.dbh.fetch_base_id(old_mod_id).todict()
    if not cas or not bid:
        print(old_mod_id, "does not exist")
        return
    cas = pif.dbh.depref('casting', cas)
    cas['id'] = bid['id'] = new_mod_id

    # copy base_id casting attributes
    pif.ren.message("copy", old_mod_id, new_mod_id)
    print('base_id', pif.dbh.add_new_base_id(bid))
    print('casting', pif.dbh.add_new_casting(cas))
    clone_attributes(pif, old_mod_id, new_mod_id)


def print_model(pif, mod):
    if mod.get('description'):
        pif.ren.message('%(id)-8s|%(first_year)4s|%(scale)-5s|%(country)2s|%(name)-36s|%(description)s' % mod)
    else:
        pif.ren.message('%(id)-8s|%(first_year)4s|%(scale)-5s|%(country)2s|%(name)s' % mod)


def casting_info(pif, mod_id):
    mod = pif.dbh.fetch_casting(mod_id)
    print_model(pif, mod)


'''
    'casting_type': 'Casting',
    'country': 'GB',
    'description': '',
    'descs': [],
    'filename': 'mb138',
    'first_year': '1984',
    'flags': 0L,
    'iconname': ['Jaguar XK 120'],
    'id': 'MB138',
    'link': 'single.cgi?id',
    'linkid': 'MB138',
    'made': True,
    'make': 'jag'
    'model_type': 'SF',
    'name': 'Jaguar XK 120',
    'notmade': '',
    'rawname': 'Jaguar XK 120',
    'scale': '1:57',
    'section_id': 'man',
    'shortname': 'Jaguar XK 120',
    'unlicensed': ' ',
    'variation_digits': 2,
    'vars': 62L,
    'vehicle_make.company_name': 'Jaguar',
    'vehicle_make.flags': 0L,
    'vehicle_make.id': 'jag',
    'vehicle_make.name': 'Jaguar',
    'vehicle_type': '2d',
    'visual_id': 'MB-138',
'''


def update_descriptions(pif, *args):
    count = 0
    showtexts = verbose = False
    verbose = True
    # showtexts = True
    if not args:
        castings = pif.dbh.fetch_casting_ids()
    elif args[0][0] >= 'a':
        castings = pif.dbh.fetch_casting_ids(section_id=pif.filelist[0])
    else:
        castings = args
        verbose = True
    for casting in castings:
        # sys.stdout.write(casting + ' ')
        sys.stdout.flush()
        print(casting, end=' ')
        fmt_invalid, messages, missing = pif.dbh.check_description_formatting(casting)
        if fmt_invalid:
            print('*')
            if verbose:
                print(messages)
            count += 1
        else:
            print()
        pif.dbh.recalc_description(casting, showtexts, verbose)
    print()
    print(count, "to go *")


def check_castings(pif, *args):
    mods = pif.dbh.depref('casting', pif.dbh.fetch_casting_list())
    mods_d = {x['id']: x for x in mods}
    mods_l = args if args else sorted(mods_d.keys())
    vt1 = set(mbdata.model_type_chars_1)
    vt2 = set(mbdata.model_type_chars_2)
    for mod_id in mods_l:
        mod = mods_d.get(mod_id)
        if not mod:
            print(mod_id, 'not found')
            continue
        if not (mod['base_id.flags'] & config.FLAG_MODEL_NOT_MADE):
            if not mod['vehicle_type']:
                print(mod_id, 'has blank vt')
            elif len(set(mod['vehicle_type']) & vt1) not in (1, 2):
                print(mod_id, 'has bad vt 1 :', set(mod['vehicle_type']) & vt1)
            if len(set(mod['vehicle_type']) & vt2) > 2:
                print(mod_id, 'has bad vt 2 :', set(mod['vehicle_type']) & vt2)
            if set(mod['vehicle_type']) - (vt1 | vt2):
                print(mod_id, 'has vt with bad chars :', set(mod['vehicle_type']) - (vt1 | vt2))
        name = mod.get('base_id.rawname', '')
        if not name:
            print(mod_id, 'has blank name')
        else:
            for x in pif.dbh.icon_name(name):
                if len(x.strip()) > 36:
                    print(mod_id, 'has illegal name:', name)
                    break


def fix_formats(pif):
    for cas in pif.dbh.fetch_casting_list():
        print(cas['casting.id'])
        if cas['casting.format_description'] == '':
            print('  desc')
            pif.dbh.write_casting({'format_description': '&body|&tampo'}, cas['casting.id'])
        if cas['casting.format_body'] == '':
            print('  body')
            pif.dbh.write_casting({'format_body': '*body|*tampo'}, cas['casting.id'])
        if cas['casting.format_interior'] == '':
            print('  int')
            pif.dbh.write_casting({'format_interior': '&interior'}, cas['casting.id'])
        if cas['casting.format_windows'] == '':
            print('  windows')
            pif.dbh.write_casting({'format_windows': '&windows'}, cas['casting.id'])
        if cas['casting.format_base'] == '':
            print('  base')
            pif.dbh.write_casting({'format_base': '&base|&manufacture'}, cas['casting.id'])
        if cas['casting.format_wheels'] == '':
            print('  wheels')
            pif.dbh.write_casting({'format_wheels': '&wheels'}, cas['casting.id'])


def ck_model(pif, mod):
    yrs = pif.dbh.dbi.execute("select distinct year from lineup_model where mod_id='%s'" % mod)[0]
    yrs = [x[0] for x in yrs]
    yrs.sort()

    sel = pif.dbh.dbi.execute("select distinct ref_id from variation_select where mod_id='%s'" % mod)[0]
    sel = [x[0][:9] for x in sel]

    missing = []
    for yr in yrs:
        if not 'year.' + yr in sel:
            missing.append(yr)
    bad = []
    for pg in sel:
        if pg.startswith('year.') and not pg[5:9] in yrs:
            bad.append(pg)
    return missing, bad


def show_list_var_pics(pif, mod_id):
    vars = pif.dbh.fetch_variations(mod_id)
    cpics = cfound = pics = found = 0
    for var in vars:
        var = pif.dbh.depref('variation', var)
        code2 = False
        core = False
        for vs in var['vs']:
            if vs['category.flags'] & config.FLAG_MODEL_CODE_2:
                code2 = True
            if vs['category.id'] == 'MB':
                core = True
        if var['var'].startswith('f') or code2:
            continue
        elif not var['picture_id']:
            fn = mod_id + '-' + var['var']
            pid = var['var']
        elif var['picture_id'] == var['var']:
            fn = mod_id + '-' + var['picture_id']
            pid = var['picture_id']
        else:
            continue
        pic_path = pif.ren.find_image_file(fnames=fn, vars=pid, prefix=mbdata.IMG_SIZ_SMALL)
        pics += 1
        if core:
            cpics += 1
        if pic_path:
            found += 1
            if core:
                cfound += 1
    af = '%d/%d' % (found, pics)
    cf = '%d/%d' % (cfound, cpics)
    if found == pics:
        af = '--'
    if cfound == cpics:
        cf = '--'
    return af, cf


def check_core(pif, *specs):  # b0rken

    sw = []
    if specs[0][0] == '0':
        sw = list(specs[0][1:])
        specs = specs[1:]

    for spec in specs:
        mods = pif.dbh.dbi.execute("select distinct id from casting where id like '%s%%'" % spec)[0]
        mods = [x[0] for x in mods]
        mods.sort()

        for mod in mods:
            missing, bad = ck_model(pif, mod)
            af, cf = show_list_var_pics(pif, mod)

            if 'a' in sw or 'p' in sw or missing or bad or af != '--' or cf != '--':
                print(mod,)
            if 'p' in sw or af != '--' or cf != '--':
                print(af, cf,)
            if missing:
                print('needs', ' '.join(missing),)

            if bad:
                print('has bad', ' '.join(bad),)

            if 'a' in sw or 'p' in sw or missing or bad or af != '--' or cf != '--':
                print()


# currently produces duplicates

def add_casting_related(pif, *mod_ids):
    mod_ids = list(mod_ids)
    section = pif.switch['s']
    section = section[-1] if section else 'single'
    while mod_ids:
        curr_id = mod_ids.pop(0)
        rels = [x['casting_related.related_id'] for x in pif.dbh.fetch_casting_relateds(curr_id, section_id=section)]
        for mod_id in mod_ids:
            if mod_id not in rels:
                print("insert into casting_related (model_id, related_id, section_id) values ('%s', '%s', '%s');" % (
                    curr_id, mod_id, section))
                if not pif.dbh.fetch_casting_relateds(mod_id, curr_id, section_id=section):
                    print("insert into casting_related (model_id, related_id, section_id) "
                          "values ('%s', '%s', '%s');" % (mod_id, curr_id, section))


def check_casting_related(pif):
    section = pif.switch['s']
    section = section[-1] if section else 'single'
    crs = pif.dbh.fetch_casting_relateds(section_id=section)
    mods = []
    rels = {}
    for cr in crs:
        m = cr['casting_related.model_id']
        r = cr['casting_related.related_id']
        mods.append((m, r))
        rels.setdefault(m, set([m]))
        rels[m].add(r)

    # check that if a is related to b, then b is related to a
    cnt = 0
    for mod in mods:
        if (tuple(reversed(mod)) not in mods):
            print(mod)
            cnt += 1
    print(cnt, 'of', len(mods))

    # check groups of relateds to make sure they all relate to each other
    added = set()
    for m in rels:
        for r in rels[m]:
            for mod in rels[m] - rels[r]:
                if (r, mod,) not in added:
                    print("insert into casting_related (model_id, related_id, section_id) "
                          "values ('%s', '%s', '%s');" % (r, mod, section))
                    added.add((r, mod,))


def add_casting_file(pif, *args):
    keys = ('id', 'model_type', 'year', 'make', 'country', 'section_id', 'rawname')
    for fn in args:
        with open(fn, 'rt') as fh:
            for ln in fh:
                ln = dict(zip(keys, ln.strip().split('|')))
                if pif.dbh.fetch_base_id(ln.get('id')):
                    print("That ID is already in use.")
                    continue
                # base_id: id, first_year, model_type, rawname, description, flags
                # casting: id, country, make, section_id
                print(pif.dbh.add_new_base_id({
                    'id': ln.get('id', ''),
                    'first_year': ln.get('year', ''),
                    'model_type': ln.get('model_type', ''),
                    'rawname': ln.get('rawname', ''),
                    'description': ln.get('description', ''),
                    'flags': 0,
                }))
                print(pif.dbh.add_new_casting({
                    'id': ln.get('id', ''),
                    'country': ln.get('country', ''),
                    'make': ln.get('make', ''),
                    'section_id': ln.get('section_id', ''),
                    'notes': '',
                }))
                add_attributes(pif, ln.get('id', ''), *ln.get('attributes', '').split(' '))
            print(ln.get('id'), 'added')


def add_linkline(pif, mod_id, ass_link, dest):
    # 15 is mbxu
    page_id = 'single.' + mod_id
    section_id = 'single'
    if ass_link == '15':
        url = f'http://www.mbx-u.com/models-detail-ver-listing.php?model={dest}'

    # load for mod_id/ass_link/dest
    lines = pif.dbh.fetch_link_lines(
        page_id=page_id, section=section_id, where=[f'name="{dest}"', f'associated_link="{ass_link}"'])
    if lines:
        print(mod_id, ass_link, dest, 'already exists')
    else:
        rec = {
            'page_id': page_id, 'section_id': section_id, 'display_order': 0, 'flags': 0, 'associated_link': ass_link,
            'last_status': '--', 'link_type': 'l', 'name': dest, 'url': url}
        print(pif.dbh.insert_link_line(rec, verbose=True))

# page_id       | sect_id | do | flags | ass_link | lt | url                      | name   |
#
# single.MB1003 | single  |  7 |     0 |       15 | l  | http://www.mbx-u.com/... | SF0950 |
# single.MB1004 | single  |  1 |     0 |       15 | l  | http://www.mbx-u.com/... | SF0951 |


def fix_variation(pif, *args):
    for mod_id in args:
        # attrs = {x['attribute.attribute_name']: x for x in pif.dbh.fetch_attributes(mod_id)}
        # mod = pif.dbh.fetch_casting(mod_id, extras=True)
        vdets = pif.dbh.fetch_details(mod_id, nodefaults=False)
        for var in pif.dbh.fetch_variations(mod_id):
            var_id = var['variation.var']
            nvar = {'variation.var': var['variation.var'], 'variation.mod_id': var['variation.mod_id']}
            if 1:  # wheels
                dets = vdets.get(var_id, {})
                desc = []
                if var.get('variation.wheels'):
                    desc.append(var['variation.wheels'])
                if dets.get('wheels_hubs'):
                    desc.append(dets['wheels_hubs'] + ' hub')
                if dets.get('front_wheels'):
                    if dets['front_wheels'] == dets.get('rear_wheels'):
                        desc.append(dets['front_wheels'])
                    else:
                        desc.append(dets['front_wheels'] + ' front')
                if dets.get('rear_wheels'):
                    if dets.get('front_wheels') != dets['rear_wheels']:
                        desc.append(dets['rear_wheels'] + ' rear')
                if dets.get('hubs'):
                    desc.append(dets['hubs'] + ' hub')
                if dets.get('tires'):
                    desc.append(dets['tires'] + ' tire')
                nvar['variation.wheels'] = ', '.join(desc)
                print(var_id, '>', nvar['variation.wheels'])
            elif 0:  # deco
                dets = vdets.get(var_id, {})
                label = dets.get('label', '')
                if label and label != 'no':
                    nvar['variation.deco_type'] = 'l'
                    nvar['variation.deco'] = label
                print(var_id, '>', nvar['variation.deco_type'], nvar['variation.deco'])
            pif.dbh.update_variation_bare(nvar)


def make_dirs(pif, *args):
    for mod_id in pif.dbh.fetch_casting_ids():
        path = os.path.join('lib', 'man', mod_id.lower().replace('/', '_'))
        if not os.path.exists(path):
            print(mod_id)
            os.mkdir(path)


cmds = [
    ('d', delete_casting, "delete: mod_id"),
    ('r', rename_base_id, "rename: old_mod_id new_mod_id"),
    ('c', copy_casting, "copy: old_mod_id new_mod_id"),
    ('s', run_text_search, "search: search-criterion"),
    ('ca', clone_attributes, "clone attributes: old_mod_id new_mod_id"),
    ('a', add_attributes, "add attributes: mod_id attribute_name ..."),
    ('l', list_attributes, "list attributes: mod_id"),
    ('i', casting_info, "info: mod_id"),
    ('u', update_descriptions, "update descriptions: ..."),
    ('x', check_castings, "check castings: mod_id ..."),
    ('f', fix_formats, "fix formats"),
    ('cc', check_core, "check core: mod_id ..."),
    ('crc', check_casting_related, "check casting_related"),
    ('cra', add_casting_related, "add casting_related [-s section] mod_id mod_id ..."),
    ('cf', add_casting_file, "add casting file"),
    ('ll', add_linkline, "add link line"),
    ('fv', fix_variation, "fix variation mod_id ..."),
    ('md', make_dirs, "make dirs"),
]


# ---- ---------------------------------------


if __name__ == '__main__':  # pragma: no cover
    basics.process_command_list(cmds=cmds, dbedit='', options='fs')
