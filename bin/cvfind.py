#!/usr/local/bin/python

import copy

import config
import mbdata
import models
import useful

# ---- the searcher object ----------------------

vfields = {'description': 'text_description', 'base': 'text_base', 'body': 'text_body', 'interior': 'text_interior',
           'wheels': 'text_wheels', 'windows': 'text_windows', 'with': 'text_with', 'text': 'text_text',
           'vid': 'var', 'category': 'category', 'date': 'date', 'area': 'area', 'note': 'note'}
vsfields = {'description': 'text_description', 'base': 'text_base', 'body': 'text_body', 'interior': 'text_interior',
            'wheels': 'text_wheels', 'windows': 'text_windows', 'with': 'text_with', 'text': 'text_text',
            'vid': 'text_var'}
man_sections = ['manno', 'manunf']

'''
    cid=
    cname=
    section=all
    range=all
    idst=1
    idend=9999
    type_?=m add_?=m pic_?=m
    make= makename=

    vid= codes=1 codes=2
    body= base= interior= wheels= windows= text= with=
    plant= area= cat= date= note=

    ltype=c
'''


def read_super_search_form(form, withaliases=False, madeonly=False):

    def get_codes(self, form_codes):
        codes = 0
        for code in form_codes:
            if code not in "123":
                return None
            codes += int(code)
        return codes

    plant = form.get_str('plant', '')  # plant_rd thinks '' is 'unset' so...
    varsq = {vfields[x]: form.search(x) for x in vfields}
    varsq['manufacture'] = mbdata.plant_rd.get(plant, '') if plant else ''
    return dict(
        list_type=form.get_str('ltype'),
        sort_type=form.get_str('stype'),
        start=form.get_int('start', 0),

        # casting section
        withaliases=withaliases,
        madeonly=madeonly,
        section=form.get_id('section'),
        mod_id=form.get_str('cid'),
        mod_id_exact=form.get_bool('cidx'),
        mod_name=form.search('cname'),
        idst=form.get_int('idst', 1),
        idend=form.get_int('idend', 9999),
        make_type=form.get_str('make'),   # = unk isn't working
        make_name=form.get_str('makename'),
        vehtypes=form.get_list_by_value('type', 'ynm'),

        # variation section
        varsq=varsq,
        var_id_exact=form.get_bool('vidx'),
        codes=form.get_list('codes'),
    )


class Searcher(object):
    def __init__(self, form=None, args=None, withaliases=False, madeonly=False):
        if form:
            args = read_super_search_form(form, withaliases, madeonly)

        self.list_type = args.get('list_type') or 'c'
        self.sort_type = args.get('sort_type') or 'i'
        self.start = args.get('start')

        # casting section
        self.withaliases = args.get('withaliases') or False
        self.madeonly = args.get('madeonly') or False
        self.section = args.get('section') or ''
        self.mod_id = args.get('mod_id') or ''
        self.mod_id_exact = args.get('mod_id_exact') or 0
        self.mod_name = args.get('mod_name') or ''
        self.idst = args.get('idst') or 1
        self.idend = args.get('idend') or 9999
        self.make_type = args.get('make_type') or ''   # = unk isn't working
        self.make_name = args.get('make_name') or ''
        self.vehtypes = args.get('vehtypes')

        # variation section
        self.varsq = args.get('varsq') or {'var': ''}
        self.var_id_exact = args.get('var_id_exact') or 0
        self.codes = args.get('codes', 3)  # thinking about this one...

        # internal stuff
        self.is_var_search = any(self.varsq.values()) or self.codes != 3
        self.makes = set()  # massaged form of what we're looking for
        self.makelist = []  # all possible makes
        self.cmakes = {}    # casting makes

        # returns
        self.more = False
        self.cascount = 0
        self.varcount = 0
        self.slist = []  # list of sections, which contains models, which in turn contains variations

    def run_query(self, pif):
        # early exits
        if self.codes is None:
            raise useful.SimpleError("This submission was not created by the form provided.")

        # set up for our queries
        self.mdict = {}
        self.sdict = {}
        slist = pif.dbh.fetch_sections({'id': useful.clean_id(self.section)} if self.section else
                                       {'page_id': 'manno'})  # all
        if not slist:
            raise useful.SimpleError(f'Requested section not found: {self.section}')
        for section in slist:
            if section['section.page_id'] in man_sections and (not self.section or section['id'] == self.section):
                section.setdefault('model_ids', list())
                section.setdefault('models', list())
                self.sdict[section['id']] = section
                self.slist.append(section)

        # get makes
        if self.make_type:
            make_q = pif.dbh.depref('vehicle_make', pif.dbh.fetch_vehicle_makes(
                where='' if pif.is_allowed('a') else f'not (flags & {config.FLAG_ITEM_HIDDEN})'))
            self.makelist = [(x['id'], x['name']) for x in make_q]
            if self.make_type == 'makename':
                self.makes = set([x[0] for x in self.makelist if x[1].lower().startswith(self.make_name.lower())])
            else:
                self.makes = set([self.make_type])
            # casting makes
            for cmake in pif.dbh.fetch_casting_makes_list():
                self.cmakes.setdefault(cmake['casting_make.casting_id'], set())
                self.cmakes[cmake['casting_make.casting_id']].add(cmake['casting_make.make_id'])

        # determine list of castings
        for casting in pif.dbh.fetch_casting_list(section_id=self.section):  # (page_id=pif.page_id):
            self.add_casting(pif, casting)
        if self.withaliases:
            for alias in pif.dbh.fetch_aliases(where=["alias.section_id != ''", "alias.type in ('MP','MB')"]):
                if alias['alias.section_id']:
                    # self.add_casting(pif, alias)
                    self.add_alias(pif, alias)

        # screen by variation filters
        if self.list_type == 'v' or self.is_var_search:
            self.cascount = 0
            vars = pif.dbh.fetch_variation_query(self.varsq, castinglist=self.mdict.keys(), codes=self.codes)
            for var in vars:
                if self.check_thing_id(self.varsq['var'], var['v.var'], self.var_id_exact):
                    if not self.mdict[var['v.mod_id']]['vars']:
                        self.cascount += 1
                    self.varcount += 1
                    var['name'] = self.mdict[var['v.mod_id']]['rawname'].replace(';', ' ')
                    self.mdict[var['v.mod_id']]['vars'].append(var)

        # create outgoing list
        count = 0
        if self.sort_type == 's':
            for section in self.slist:
                for mod in section['model_ids']:
                    count = self.add_to_output(section, self.mdict[mod], count)
                    if self.more:
                        break
                if self.more:
                    break
            return self.slist
        else:
            modlist = []
            for section in self.slist:
                for mod in section['model_ids']:
                    modlist.append(self.mdict[mod])
            if self.sort_type == 'n':
                modlist.sort(key=lambda x: x['name'])
            else:  # i
                modlist.sort(key=lambda x: x['id'])
            rsection = {'models': [], 'id': 'only'}
            rsection['name'] = 'Variations Found' if self.list_type == 'v' else 'Models Found'
            for mod in modlist:
                count = self.add_to_output(rsection, mod, count)
                if self.more:
                    break
            return [rsection]

    def add_to_output(self, rsec, mod, count):
        if self.list_type == 'v':
            rsec['models'].append(mod)
            for var in mod['vars']:
                count += 1
                if count > self.start:
                    if count <= self.start + mbdata.modsperpage:
                        mod['variations'].append(var)
                    else:
                        self.more = True
        elif not self.is_var_search or (self.is_var_search and mod['vars']):  # c
            count += 1
            if count > self.start:
                if count <= self.start + mbdata.modsperpage:
                    rsec['models'].append(mod)
                    mod['variations'] = mod['vars']
                else:
                    self.more = True
        return count

    def add_casting(self, pif, casting, aliases=[]):
        manitem = pif.dbh.modify_man_item(casting)
        aliases = [x for x in aliases if x['alias.type'] == 'mack']
        manitem['mack'] = ','.join(models.get_mack_numbers(pif, manitem['id'], manitem['model_type'], aliases))
        if manitem['section_id'] in self.sdict and manitem['id'] not in self.sdict[manitem['section_id']]['model_ids']:
            self.add_casting_item(pif, manitem['id'], manitem)

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
            self.add_casting_item(pif, manitem['alias.id'], manitem)

    def add_casting_item(self, pif, man_id, manitem):
        manitem.update({
            'makes': ((set([manitem['make']]) if manitem['make'] else set()) | self.cmakes.get(manitem['id'], set()) or
                      set(['unk'])),
            'type_desc': mbdata.text_types(manitem['vehicle_type']),
            'vars': [],
            'variations': [],
        })
        if man_id not in self.mdict and self.is_casting_shown(manitem):
            # add makes
            if self.is_var_search:
                manitem['link'] = 'vars.cgi?' + self.make_var_search_criteria(pif, manitem)
            self.sdict[manitem['section_id']]['model_ids'].append(man_id)
            self.mdict[man_id] = manitem
            self.cascount += 1

    def check_model_number(self, mod_id):
        if not self.idst or not self.idend:
            return True
        modno = 0
        for c in mod_id:
            if c.isdigit():
                modno = 10 * modno + int(c)
        return not (modno < self.idst or modno > self.idend)

    def check_thing_id(self, thing_id_1, thing_id_2, exact):
        if thing_id_1 and isinstance(thing_id_1, list):
            thing_id_1 = thing_id_1[0]
        return not thing_id_1 or (
            thing_id_1.lower() == thing_id_2.lower() if exact else
            thing_id_1.lower() in thing_id_2.lower())

    def is_casting_shown(self, mod):
        '''Makes decision of whether to show casting.'''
        # variation filters get checked later
        return not (
            (not self.check_thing_id(self.mod_id, mod['id'], self.mod_id_exact)) or
            (not useful.search_match(self.mod_name, mod['name'])) or
            (self.makes and not (mod['makes'] & self.makes)) or
            (not self.check_model_number(mod['id'])) or
            (not mbdata.type_check(self.vehtypes['n'], self.vehtypes['y'], mod['vehicle_type'])) or
            (self.madeonly and not mod['made']))

    def make_var_search_criteria(self, pif, mod):  # query for clicking on cas with varsq
        qf = '&'.join(['{}={}'.format(v, pif.form.get_str(k)) for k, v in vsfields.items()])
        if self.varsq['manufacture']:
            qf += f'&manufacture={self.varsq["manufacture"]}'
        for code in pif.form.get_list('codes'):
            qf += f'&c{code}={code}'
        qf += '&hc=1&ci=1&pic0=1&pic1=1&mod'  # reasons
        return qf

    def make_search_criteria(self, pif):   # query for prev/next pages
        qf = pif.form.reformat(vfields, blanks=False)
        qf += '&' + pif.form.reformat([
            'ltype', 'stype', 'section', 'range', 'cid', 'cname', 'idst', 'idend', 'make', 'makename', 'plant'],
            blanks=False)
        if self.vehtypes['y'] or self.vehtypes['n']:
            qf += '&' + pif.form.reformat(pif.form.keys(start='type'), blanks=False)
        if pif.ren.verbose:
            qf += '&verbose=1'
        for code in pif.form.get_list('codes'):
            qf += f'&codes={code}'
        return qf
