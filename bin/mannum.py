#!/usr/local/bin/python

import copy, glob, os, re
import basics
import config
import mbdata
import mflags
import models
import single
import useful

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
        ['9', 'X'],
        ['13', 'H'],
        ['17', 'V'],
        ['90', 'F'],
        ['96', 'D'],
        ['100', 'P'],
        ['365', 'S'],
        ['7881', 'F'],
        ['7187', 'B'],
        ['7379', 'W'],
        ['4560', 'D'],
        ['27', 'P'],
        ['7783', 'V'],
        ['description', 'Description'],
        ['mydesc', 'Mine'],
]
a_links = ['9', '13', '17', '90', '96', '100', '365', '7881', '7187', '7379', '4560', '27', '7783']
admin_fmtb = reduce(lambda x, y: x+'<td>%('+y[0]+')s</td>', admin_cols, '<tr>') + '</tr>'
admin_fmth = reduce(lambda x, y: x+'<th>%('+y[0]+')s</th>', admin_cols, '<tr>') + '</tr>'
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
        ['pic_a', 'All'],
        ['pic_c', 'Core'],
        ['pic_1', 'Code1'],
        ['pic_2', 'Code2'],
        ['pic_f', 'VarF'],
        #[percent_a, percent_c, percent_1, percent_2, percent_f]
        ['description', 'Description'],
]
picture_fmtb = reduce(lambda x, y: x+'<td>%('+y[0]+')s</td>', picture_cols, '<tr>') + '</tr>'
picture_fmth = reduce(lambda x, y: x+'<th>%('+y[0]+')s</th>', picture_cols, '<tr>') + '</tr>'
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
        ['z_', config.IMG_DIR_MAN + '/icon'],
]

#---- the manno object ----------------------

class MannoFile:
    def __init__(self, pif, withaliases=False):
        self.section = None
        self.start = 1
        self.end = 9999
        self.firstyear = 1
        self.lastyear = 9999
        self.nodesc = pif.form_int('nodesc')
        vtypes = pif.dbh.fetch_vehicle_types()
        self.tdict = {x['vehicle_type.ch']: x['vehicle_type.name'] for x in vtypes}
        self.vtypes = {'y': "", 'n': "", 'm': "".join(self.tdict.keys())}
        self.plist = ['manno', 'manls']  # [x['page_info.id'] for x in pif.dbh.fetch_pages({'format_type': 'manno'})]
        if pif.form_str('section', 'all') != 'all':
            slist = pif.dbh.fetch_sections({'id': pif.form_str('section')})  #, 'page_id': pif.page_id})
        else:
            slist = pif.dbh.fetch_sections({'page_id': pif.page_id})
        self.mdict = dict()
        self.sdict = dict()
        self.slist = list()
        for section in slist:
            if section['section.page_id'] in self.plist and (not self.section or section['id'] == self.section):
                section = pif.dbh.depref('section', section)
                section.setdefault('model_ids', list())
                self.sdict[section['id']] = section
                self.slist.append(section)
        self.totalvars = self.totalpics = 0
        self.corevars = self.corepics = 0
        self.c2vars = self.c2pics = 0

        for key in pif.form_keys(start='type_'):
            val = pif.form_str(key)
            t = key[-1]
            self.vtypes.setdefault(val, list())
            self.vtypes[val] += t

        self.section = pif.form_str('section')
        if self.section == 'all':
            self.section = ''
        self.start = pif.form_int('start', 1)
        self.end = pif.form_int('end', 9999)
        self.firstyear = pif.form_int('syear', 1)
        self.lastyear = pif.form_int('eyear', 9999)
        if pif.form_str('range', 'all') == 'all':
            self.start = self.end = None

        for casting in pif.dbh.fetch_casting_list():  #(page_id=pif.page_id):
            self.add_casting(pif, casting)
        if withaliases:
            for alias in pif.dbh.fetch_aliases(where="section_id != ''"):
                #self.add_casting(pif, alias)
                self.add_alias(pif, alias)

    def add_casting(self, pif, casting):
        manitem = pif.dbh.modify_man_item(casting)
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
            if sec['model_ids']:
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

    def show_section_manno(self, pif, sect):
        sect['anchor'] = sect['id']
        sect['id'] = ''
        sect['range'] = [{'entry': models.generate_model_table_pic_link(pif, self.mdict, sect['model_ids'])}]
        return sect

    def run_manno_list(self, pif):
        llineup = dict(columns=4)
        llineup['section'] = self.run_thing(pif, self.show_section_manno)
        return pif.render.format_lineup(llineup) + \
            pif.render.format_button_comment(pif, 'sel=%s&ran=%s&start=%s&end=%s' %
                (pif.form_str('selection'), pif.form_str('range'), pif.form_str('start'), pif.form_str('end')))

    def run(self, pif):
        llineup = {'section': list(), 'columns': 4}
        llineup['section'] = self.run_thing(pif, self.show_section_manno)
        return llineup

    # ----- check list ------------------------------------------

    def show_section_list(self, pif, sect):
        cols = 3
        ostr = '<a name="'+sect['id']+'_list"></a>\n'
        ostr += '<tr><td colspan=%d style="text-align: center; font-weight: bold;">%s</td></tr>' % (4 * cols, sect['name'])
        mods = list()
        smods = sect['model_ids']
        mpc = len(smods) / cols
        if len(smods) % cols:
            mpc += 1
        for col in range(0, cols):
            mods.append(smods[col * mpc:(col + 1) * mpc])

        while True:
            ostr += ' <tr>\n'
            found = False
            for col in range(0, cols):
                if mods[col]:
                    slist = self.mdict[mods[col].pop(0)]
                    ostr += models.add_model_table_list_entry(pif, slist)
                    found = True
            ostr += ' </tr>\n'
            if not found:
                break
        ostr += '<tr>'
        for col in range(0, cols):
            ostr += '<td colspan=4 width=%d%%>&nbsp;</td>' % (100 / cols)
        ostr += '</tr>'
        return ostr

    def run_checklist(self, pif):
        ostr = '<table class="smallprint" width=100%>\n'
        ostr += '\n'.join(self.run_thing(pif, self.show_section_list))
        ostr += "</table>\n\n"
        return ostr

    # ----- thumbnails ------------------------------------------

    def show_section_thumbs(self, pif, sect):
        sect['range'] = list()
        sect['anchor'] = sect['id']
        sect['id'] = ''
        sect['columns'] = 6
        ran = {'entry': list()}
        for mod_id in sect['model_ids']:
            mdict = self.mdict[mod_id]
            mdict['nodesc'] = 1
            mdict['prefix'] = 't'
            ran['entry'].append({'text': models.add_model_table_pic_link(pif, mdict)})
        sect['range'].append(ran)
        return sect

    def run_thumbnails(self, pif):
        llineup = {'section': list(), 'columns': 4}
        llineup['section'] = self.run_thing(pif, self.show_section_thumbs)
        ostr = pif.render.format_lineup(llineup)
        ostr += pif.render.format_button_comment(pif, 'sel=%s&ran=%s&start=%s&end=%s' %
            (pif.form_str('selection', ''), pif.form_str('range', ''), pif.form_str('start', ''), pif.form_str('end', '')))

        return ostr

    # ----- admin list ------------------------------------------

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

    def show_list_var_pics(self, pif, mod_id):
        vars = pif.dbh.fetch_variations(mod_id)
        cpics = cfound = pics = found = 0
        for var in vars:
            is_c2 = False
            if var['variation.var'].startswith('f'):
                continue
            if not var['variation.picture_id']:
                fn = mod_id + '-' + var['variation.var']
            elif var['variation.picture_id'] == var['variation.var']:
                fn = mod_id + '-' + var['variation.picture_id']
            else:
                continue
            self.totalvars += 1
            if not var['variation.category']:
                self.corevars += 1
                cpics += 1
            if var['variation.category'] in mbdata.code2_categories:
                self.c2vars += 1
                is_c2 = True
            else:
                pics += 1
            #pif.render.comment(config.IMG_DIR_VAR + '/' + fn + '.jpg')
            if os.path.exists(config.IMG_DIR_VAR + '/s_' + fn.lower() + '.jpg'):
                if is_c2:
                    self.c2pics += 1
                    continue
                self.totalpics += 1
                found += 1
                if not var['variation.category']:
                    self.corepics += 1
                    cfound += 1
        af = '%d/%d' % (found, pics)
        cf = '%d/%d' % (cfound, cpics)
        if found != pics:
            af = '<font color="red">%s</font>' % af
        if cfound != cpics:
            cf = '<font color="red">%s</font>' % cf
        return af + ' ' + cf


    def show_list_var_years(self, pif, mod_id):
        fy = ly = None
        vars = pif.dbh.fetch_variations(mod_id)
        for var in vars:
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
        return {'fvyear': fy, 'lvyear': ly}

    # ----- admin -----------------------------------------------

    def show_admin_model_table(self, pif, mdict):
        mdict.update({x: '-' for x in a_links})
        for lnk in pif.dbh.fetch_link_lines("single." + mdict['id']):
            mdict[str(lnk['link_line.associated_link'])] = pif.render.format_link(lnk['link_line.url'], 'X')
        mdict['name'] = mades[int(mdict['made'])] % mdict
        mdict.update({'img': self.show_list_pic(pif, ['', config.IMG_DIR_MAN], mdict['id'], 's')[1],
            'fvyear': '', 'lvyear': '',
            'vid': '<a href="vars.cgi?list=1&mod=%(id)s">%(id)s</a>' % mdict,
            'nl': '<a href="%(link)s=%(id)s">%(name)s</a>' % mdict})
        mdict.update(dict([self.show_list_pic(pif, x, mdict['id'], x[0][0]) for x in prefixes]))
        mdict.update(self.show_list_var_years(pif, mdict['id']))
        mdict.setdefault('own', '')
        mdict.setdefault('mydesc', '')
        return admin_fmtb % mdict


    def show_section_admin(self, pif, sect):
        sect['cols'] = len(admin_cols)
        ostr = '<tr><th colspan=%(cols)d><a name="%(id)s">%(name)s</a></th></tr>\n' % sect
        ostr += admin_fmth % dict(admin_cols) + '\n'
        for mod in sect['model_ids']:
            ostr += self.show_admin_model_table(pif, self.mdict[mod]) + '\n'
        return ostr


    def run_admin_list(self, pif):
        ostr = pif.render.format_table_start()
        ostr += '\n'.join(self.run_thing(pif, self.show_section_admin))
        ostr += pif.render.format_table_end()
        self.totalvars = max(self.totalvars, 1)
        self.corevars = max(self.corevars, 1)
        self.c2vars = max(self.c2vars, 1)
        ostr += 'Pictures found: %d of %d (%d%%)<br>' % (self.totalpics, self.totalvars, (100 * self.totalpics / self.totalvars))
        ostr += 'Core pictures found: %d of %d (%d%%)<br>' % (self.corepics, self.corevars, (100 * self.corepics / self.corevars))
        ostr += 'Code 2 pictures found: %d of %d (%d%%)<br>' % (self.c2pics, self.c2vars, (100 * self.c2pics / self.c2vars))
        return ostr

    # ----- picture -----------------------------------------------

    def show_picture_model_table(self, pif, mdict):
        var_pic_keys = ['pic_a', 'pic_c', 'pic_1', 'pic_2', 'pic_f']
        mdict['first_year'] = '<a href="traverse.cgi?g=1&d=%s">%s</a>' % (os.path.join(config.LIB_MAN_DIR, mdict['id'].lower()), mdict['first_year'])
        mdict['name'] = mades[int(mdict['made'])] % mdict
        mdict.update({'img': self.show_list_pic(pif, ['', config.IMG_DIR_MAN], mdict['id'], 's')[1],
            'vid': '<a href="vars.cgi?list=1&mod=%(id)s">%(id)s</a>' % mdict,
            'nl': '<a href="%(link)s=%(id)s">%(name)s</a>' % mdict})
        mdict.update(dict([self.show_list_pic(pif, x, mdict['id'], x[0][0]) for x in prefixes]))
        icon = self.show_list_pic(pif, ['i_', config.IMG_DIR_MAN + '/icon'], mdict['id'], 'i')
        mdict['z_'] = icon[1]
        #mdict['varpic'] = self.show_list_var_pics(pif, mdict['id'])
        vp = single.show_list_var_pics(pif, mdict['id'])
        mdict.update({var_pic_keys[x]: vp[x] for x in range(0, 5)})
        #[percent_a, percent_c, percent_1, percent_2, percent_f]
        return picture_fmtb % mdict


    def show_section_picture(self, pif, sect):
        sect['cols'] = len(picture_cols)
        ostr = '<tr><th colspan=%(cols)d><a name="%(id)s">%(name)s</a></th></tr>\n' % sect
        ostr += picture_fmth % dict(picture_cols) + '\n'
        for mod in sect['model_ids']:
            ostr += self.show_picture_model_table(pif, self.mdict[mod]) + '\n'
        return ostr


    def run_picture_list(self, pif):
        self.totals = [[0, 0]] * 5
        ostr = pif.render.format_table_start()
        ostr += '\n'.join(self.run_thing(pif, self.show_section_picture))
        ostr += pif.render.format_table_end()
        ostr += str(self.totals) + '<br>'
        return ostr

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

    def show_vt_model_table(self, pif, mdict):
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
        return vt_fmtb % mdict

    def show_section_vehicle_type(self, pif, sect):
        sect['cols'] = len(vt_cols)
        ostr = '<tr><th colspan=%(cols)d><a name="%(id)s">%(name)s</a></th></tr>\n' % sect
        ostr += vt_fmth % dict(vt_cols) + '\n'
        for mod in sect['model_ids']:
            ostr += self.show_vt_model_table(pif, self.mdict[mod]) + '\n'
        return ostr

    def run_vehicle_type_list(self, pif):
        ostr = '<form method="post">\n'
        ostr += '<input type="hidden" name="vtset" value="1">\n'
        ostr += pif.render.format_table_start()
        ostr += '\n'.join(self.run_thing(pif, self.show_section_vehicle_type))
        ostr += pif.render.format_table_end()
        ostr += pif.render.format_button_input()
        ostr += '</form>\n'
        return ostr

    # ----- csv -------------------------------------------------

    def show_section_man2csv(self, pif, sect):

        def num_format(t):
            return '"=""%s"""' % t

        def text_format(t):
            if '"' in t or ',' in t:
                t = '"' + t.replace('"', '""') + '"'
            return t

        ret = list()
        for mod_id in sect['model_ids']:
            mod = self.mdict[mod_id]
            ret.append(",".join([mod_id, num_format(mod['first_year']), num_format(mod['scale']), text_format(mod['name']), text_format(', '.join(mod['descs']))]))
        return '\r\n'.join(ret) + '\r\n'

    def run_man2csv(self, pif):
        out_file = open('pages/man.csv', 'w')
        out_file.write("MAN #,Year,Scale,Name,Notes\r\n")
        secs = self.run_thing(pif, self.show_section_man2csv)
        out_file.write(''.join(secs))

#---- useful stuff --------------------------

def rename_base_id(pif, old_mod_id, new_mod_id, force=False):
    rec = pif.dbh.fetch_base_id(new_mod_id)
    if rec:
        if not force:
            print new_mod_id, "exists"
            return
    else:
        pif.dbh.rename_base_id(old_mod_id, new_mod_id)

    # If we're renaming, I'd like to also rename the pictures.
    filename_re = re.compile('(?P<path>.*/)(?P<p>[a-z]_)?(?P<m>[^-.]*)(?P<s>-[^.]*)?(?P<e>\..*)')
    none_blank = {None: ''}
    patts = [
        config.IMG_DIR_MAN + '/?_%s.*' % old_mod_id,
        config.IMG_DIR_MAN + '/%s.*' % old_mod_id,
        config.IMG_DIR_VAR + '/?_%s-*.*' % old_mod_id,
        config.IMG_DIR_VAR + '/%s-*.*' % old_mod_id,
        config.IMG_DIR_MAN + '/icon/?_%s-*.*' % old_mod_id,
        config.IMG_DIR_ADD + '/?_%s.*' % old_mod_id,
        config.IMG_DIR_CAT + '/?_%s.*' % old_mod_id,
        config.IMG_DIR_CAT + '/%s.*' % old_mod_id,
        config.IMG_DIR_PACK + '/?_%s.*' % old_mod_id,
        config.IMG_DIR_PACK + '/%s.*' % old_mod_id,
    ]
    pics = reduce(lambda x, y: x + glob.glob(y.lower()), patts, list())
    for pic in pics:
#       pic_m = filename_re.match(pic)
#       if pic_m:
#           pic_new = ''.join([
#               pic_m.group('path'),
#               none_blank.get(pic_m.group('p'), pic_m.group('p')),
#               pic_m.group('m'),
#               none_blank.get(pic_m.group('s'), pic_m.group('s')),
#               pic_m.group('e'),
#           ])
#           print "rename", pic, pic_new, "<br>"
#           #os.rename(pic, pic_new)
#       else:
#           print "can't resolve name:", pic
        pic_new = pic.replace(old_mod_id.lower(), new_mod_id.lower())
        print "rename", pic, pic_new, "<br>"
        os.rename(pic, pic_new)


def write_vehicle_types(pif):
    for key in pif.form_keys(start='vt_'):
        val = ''.join(pif.form_list(key))
        print key[3:], 'type', val, '<br>'
        pif.dbh.write_casting(values={'vehicle_type': val}, id=key[3:])
    for key in pif.form_keys(start='vm_'):
        print key[3:], 'make', pif.form_str(key), '<br>'
        pif.dbh.write_casting(values={'make': pif.form_str(key)}, id=key[3:])
    for key in pif.form_keys(start='co_'):
        print key[3:], 'country', pif.form_str(key), '<br>'
        pif.dbh.write_casting(values={'country': pif.form_str(key)}, id=key[3:])

#---- main ----------------------------------

@basics.web_page
def main(pif):
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append(pif.request_uri, 'Manufacturing Numbers')
    pif.render.print_html()
    if pif.form_str('num'):
        print '<meta http-equiv="refresh" content="0;url=single.cgi?id=%s">' % pif.form_str('num')
        return
    print pif.render.format_head()
    models.flago = mflags.FlagList(pif)
    if pif.form_has('vtset'):
        write_vehicle_types(pif)
    elif not pif.form_has('section'):
        print "Please select a range to display."
    else:
        listtype = pif.form_str('listtype')
        manf = MannoFile(pif, withaliases=True)
        if listtype == 'adl':
            print manf.run_admin_list(pif)
        elif listtype == 'pxl':
            print manf.run_picture_list(pif)
        elif listtype == 'ckl':
            print manf.run_checklist(pif)
        elif listtype == 'thm':
            print manf.run_thumbnails(pif)
        elif listtype == 'vtl':
            print manf.run_vehicle_type_list(pif)
        else:
            print manf.run_manno_list(pif)
    print pif.render.format_tail()

#---- play ----------------------------------

@basics.web_page
def play_main(pif):
    pif.render.print_html()
    print pif.render.format_head()
    manf = MannoFile(pif)
    llineup = manf.run(pif)
    llineup['section'][0]['range'][0]['entry'][0].update({'rowspan': 2, 'colspan': 2})
    print pif.render.format_lineup(llineup)
    print pif.render.format_tail()

#---- compare -------------------------------

def comparisons(pif, diffs):
    ostr = ''
    imod = 0
    for sec in diffs:

        modsets = {}
        for mod in sec['mods']:
            if mod['c2.rawname']:
                mod['name'] = mod['c2.rawname'].replace(';', ' ')
                mod['mod_id'] = mod['cc.compare_id']
            else:
                mod['name'] = mod['c1.rawname'].replace(';', ' ')
                mod['mod_id'] = mod['cc.mod_id']
            modsets.setdefault(mod['cc.mod_id'], [])
            modsets[mod['cc.mod_id']].append((mod['mod_id'], mod['name'], mod['cc.description'].split(';')))
            #print mod, '<br>'
        keys = modsets.keys()
        keys.sort()

        ostr += pif.render.format_table_start()
        ostr += pif.render.format_section(sec['section.name'], also={'colspan': 3})
        ostr += pif.render.format_row_start()
        ostr += pif.render.format_cell(0, sec['section.note'], also={'colspan': 3})
        ostr += pif.render.format_row_end()
        for main_id in keys:
            modset = modsets[main_id]
            ostr += pif.render.format_row_start(ids=[x[0] for x in modset])
            ostr += pif.render.format_cell_start(imod, hdr=True, also={'colspan': 3})
            names = list()
            for id, name, descs in modset:
                #ostr += pif.render.fmt_anchor(id)
                if name not in names:
                    names.append(name)
            ostr += ", ".join(names)
            ostr += pif.render.format_cell_end(hdr=True)
            ostr += pif.render.format_row_end()
            pic = pif.render.format_image_optional(main_id, prefix='z_')
            for id, name, descs in modset:
                desc = pif.render.format_bullet_list(descs)
                ostr += pif.render.format_row_start()
                ostr += pif.render.format_cell(imod, models.add_model_pic_link_short(pif, id),
                                also={'style': 'text-align: center;'})
                if pic:
                    if desc:
                        ostr += pif.render.format_cell(imod, desc)
                    if id == main_id:
                        ostr += pif.render.format_cell(imod, pif.render.format_image_optional(main_id, prefix='z_'),
                                    also={'rowspan': len(modsets[main_id])})
                else:
                    if desc:
                        ostr += pif.render.format_cell(imod, desc, also={'colspan': 2})
                    else:
                        ostr += pif.render.format_cell(imod, '&nbsp;', also={'colspan': 2})
                ostr += pif.render.format_row_end()
            imod = (imod + 1) % 2
        ostr += pif.render.format_table_end()
    return ostr


@basics.web_page
def compare_main(pif):
    pif.render.print_html()
    secs = pif.dbh.fetch_sections({'page_id': pif.page_id})
    mods = pif.dbh.fetch_casting_compares()
    for sec in secs:
        sec['mods'] = filter(lambda x: x['cc.section_id'] == sec['section.id'], mods)

    print pif.render.format_head()
    print comparisons(pif, secs)
    print pif.render.format_button_comment(pif)
    print pif.render.format_tail()

#---- ---------------------------------------

@basics.command_line
def commands(pif):
    if pif.argv and pif.argv[0] == 'd':
        print "delete not yet implemented"
        pass  # DeleteCasting(pif, pif.argv[1], pif.argv[2])
    elif pif.argv and pif.argv[0] == 'r':
        rename_base_id(pif, pif.argv[1], pif.argv[2], True)
    elif pif.argv and pif.argv[0] == 'f':
        run_search(pif, pif.argv[1:])
    else:
        print "./mannum.py [f|d|r] ..."
        print "  f for find: search-criterion"
        print "  d for delete: mod_id"
        print "  r for rename: old_mod_id new_mod_id"


def search_name(pif, targ):
    where = map(lambda x: "base_id.rawname like '%%%s%%'" % x, targ)
    return pif.dbh.fetch_casting_list(page_id='manno', where=where, verbose=False) + \
            pif.dbh.fetch_casting_list(page_id='manls', where=where, verbose=False)


def run_search(pif, args):
    mods = map(pif.dbh.modify_man_item, search_name(pif, args))
    mods.sort(key=lambda x: x['id'])
    for mod in mods:
        print '%(id)-8s|%(first_year)4s|%(scale)-5s|%(country)2s|%(name)s' % mod


if __name__ == '__main__':  # pragma: no cover
    commands('vars')
