#!/usr/local/bin/python

'''Old, file-based code.  My ability to care about this is severely limited.'''

import basics
import bfiles
import config
import useful

modnumlist = []


class SetFile(bfiles.ArgFile):
    tablecols = ['prefix', 'cols', 'title', 'digits', 'label', 'style']
    notcols = ['fulldesc', 'insetdesc', 'fullpic']

    def __init__(self, fname):
        self.tables = []
        self.found = False
        self.db = {'model': []}
        self.ncols = 0
        self.header = ''
        self.colheads = {}
        self.dirs = {}
        bfiles.ArgFile.__init__(self, fname)

    def parse_cells(self, llist):
        self.header = llist[1:]
        self.ncols = 0
        for col in self.header:
            if not(col in self.notcols):
                self.ncols += 1
        self.db['ncols'] = self.ncols

    def parse_dir(self, llist):
        self.dirs[llist[1]] = llist[2]

    def parse_field(self, llist):
        self.colheads[llist[1]] = llist[2]

    def parse_table(self, llist):
        if self.found:
            self.tables.append(self.db)
            self.db = {'model': []}
        self.db.update(dict(zip(self.tablecols, llist[1:])))
        self.db['cols'] = self.db['cols'].split(',')
        self.db['header'] = self.header
        self.db['ncols'] = self.ncols

    def parse_t(self, llist):
        self.model = {'text': llist.get_arg('')}
        self.db['model'].append(self.model)

    def parse_s(self, llist):
        self.model = {'section': llist.get_arg('')}
        self.db['model'].append(self.model)

    def parse_m(self, llist):
        self.found = True
        self.model = dict(zip(self.db['cols'], llist[1:]))
        self.model['desc'] = []
        self.db['model'].append(self.model)

    def parse_d(self, llist):
        self.model['desc'].append(llist[1])

    def parse_end(self):
        if self.found:
            self.tables.append(self.db)


def do_set(pif, setfile, set_id=None):
    pif.render.set_button_comment(pif, '')
    tables = setfile.tables

    llineups = []
    for db in tables:
        if len(tables) == 1 or not db['title'] or set_id == db['label'] or set_id == 'all':  # or not set_id
            llineups.append(print_table(pif, db, setfile))
        else:
            llineups.append(print_no_table(pif, db))
    return pif.render.format_template('sets.html', llineups=llineups)


def print_table(pif, db, setfile):
    global modnumlist
    entries = []
    prefix = db['prefix']

    ncols = 0
    for field in db['header']:
        if field in setfile.colheads:
            entries.append({'text': setfile.colheads[field], 'style': str(ncols)})
            ncols = ncols + 1

    for model in db['model']:
        pif.render.comment('print_table', model)
        showme = True
        for field in db['header']:
            if pif.form.has(field):
                if (model.get(field, '') != pif.form.get_str(field) or
                        (not model.get(field, '') and not pif.form.get_str(field))):
                    showme = False
        if not showme:
            continue
        if 'text' in model:
            # Need to calculate the colspan better.
            entries.append({'text': model.get('text', ''), 'colspan': len(db['header']) - 1, 'style': '0'})
            continue
        if 'section' in model:
            # Need to calculate the colspan better.
            entries.append({'text': model.get('section', ''), 'colspan': len(db['header']) - 1, 'class': 'section'})
            continue
        ifield = 0
        for field in db['header']:
            if field == 'desc':
                entries.append({'style': ifield, 'text': mod_desc(model.get(field, ''))})
            elif field == 'fulldesc':
                entries.append({'style': ifield, 'text': mod_desc(model.get('desc', '')), 'colspan': int(db['ncols'])})
            elif field == 'insetdesc':
                entries.append({'style': ifield, 'text': mod_desc(model.get('desc', '')), 'colspan': int(db['ncols']) - 1})
            elif field == 'num':
                modnums = [mod_num(prefix, modnum, model.get('rank')) for modnum in model.get(field, '').split(';')]
                entries.append({'style': ifield,
                                'text': '<nobr>%s</nobr>' % "<br>".join(modnums), 'also': {'height': '8'}})
            elif field == 'pic':
                modnum = model.get('num', '').split(';')
                rowspan = 2 if 'insetdesc' in db['header'] else 1
                entries.append({
                    'style': ifield,
                    'text': img(pif, prefix, modnum, model.get('rank'), int(db['digits']),
                                (model.get('year', '') != 'not made'), dirs=setfile.dirs),
                    'rowspan': rowspan})
            elif field == 'fullpic':
                modnum = model.get('num', '').split(';')
                colspan = 2 if 'insetdesc' in db['header'] else int(db['ncols'])
                entries.append({
                    'style': ifield,
                    'text': img(pif, prefix, modnum, model.get('rank'), int(db['digits']),
                                (model.get('year', '') != 'not made'), dirs=setfile.dirs),
                    'colspan': colspan})
            elif field == 'name':
                entries.append({
                    'style': ifield, 'text': '<center><b>' + model.get(field, '') + '</b></center>'}
                    if model.get(field, '') else {'style': ifield})
            else:
                entries.append({'style': ifield,
                                'text': model.get(field, '')} if model.get(field, '') else {'style': ifield})
            ifield += 1
    llineup = {
        'anchor': db['label'], 'name': db['title'], 'columns': int(ncols), 'widthauto': True,
        'section': [{'id': 'box', 'name': '',
                     'range': [{'entry': entries}]}],
    }
    return pif.render.format_matrix_for_template(llineup)


def print_no_table(pif, db):
    return {
        'anchor': db['label'],
        'header': '<h3><a href="/cgi-bin/sets.cgi?page=' + pif.form.get_str('page') +
        '&set=%(label)s#%(label)s">%(title)s</a></h3>\n' % db}


def mod_desc(desclist):
    if desclist:
        ostr = '<ul>\n'
        for desc in desclist:
            ostr += ' <li>' + desc + '\n'
        ostr += '</ul>\n'
    else:
        ostr = '&nbsp;\n'
    return ostr


def mod_num(prefix, model, suffix):
    return ''.join([(prefix + '-') if prefix else '', model, ('-' + suffix) if suffix else ''])


def img(pif, prefix, model, suffix, digits=0, made=True, dirs={}):
    pif.render.comment(prefix, model, suffix, digits, made)
    if not isinstance(model, list):
        model = [model]
    modnum = []
    for m in model:
        try:
            fmt = "%%0%dd" % digits
            m = fmt % int(m)
        except TypeError:
            pass
        except ValueError:
            pass
        if prefix:
            m = prefix + m
        if suffix:
            m += suffix
        modnum.append(m)
    ostr = pif.render.format_image_required(modnum, alt=mod_num(prefix, model[0], suffix), made=made,
                                            pdir=dirs.get(prefix))
    return '<center>' + ostr + '</center>'


def select_set(pif):
    lran = {
        'name': "A few of the special sets produced by Matchbox in recent years:",
        'entry': ['<b><a href="?page=%s">%s</a></b> - %s' %
                  (ent['page_info.id'][5:], ent['page_info.title'], ent['page_info.description'])
                  for ent in pif.dbh.fetch_pages("id like 'sets.%' and (flags & 1)=0", order='description,title')]}
    llineup = {'section': [{'id': 'i', 'range': [lran]}],
               'tail': [pif.render.format_button("back", link="..") + " to the main index."]}
    return pif.render.format_template('setsel.html', llineup=llineup)


@basics.web_page
def sets_main(pif):
    pif.render.print_html()

    if pif.form.has('page'):
        setfile = SetFile(useful.relpath(config.SRC_DIR, useful.make_alnum(pif.form.get_str('page')) + '.dat'))
        return do_set(pif, setfile, pif.form.get_id('set'))
    else:
        return select_set(pif)
