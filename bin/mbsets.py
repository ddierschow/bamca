#!/usr/local/bin/python

'''Old, file-based code.  My ability to care about this is severely limited.'''

import os
import basics
import bfiles
import config

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
        self.db.update(dict(map(None, self.tablecols, llist[1:])))
        self.db['cols'] = cols = self.db['cols'].split(',')
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
        self.model = dict(map(None, self.db['cols'], llist[1:]))
        self.model['desc'] = []
        self.db['model'].append(self.model)

    def parse_d(self, llist):
        self.model['desc'].append(llist[1])

    def parse_end(self):
        if self.found:
            self.tables.append(self.db)


def do_set(pif, setfile, set_id=None, dups=False):
    tables = setfile.tables

    ostr = '<center>'
    for db in tables:
        if len(tables) == 1 or not db['title'] or set_id == db['label'] or set_id == 'all':  # or not set_id
            ostr += print_table(pif, db, setfile, dups)
        else:
            ostr += print_no_table(pif, db)
    ostr += '</center>\n'
    ostr += pif.render.format_button_comment(pif, '')
    return pif.render.format_head() + ostr + pif.render.format_tail()


def print_table(pif, db, setfile, dups=False):
    global modnumlist
    ostr = '<a name="%(label)s"></a>\n' % db
    if db['title']:
        ostr += '<h3>%s</h3>\n' % db['title']
    ostr += pif.render.format_table_start()
    prefix = db['prefix']

    ncols = 0
    ostr += '\n' + pif.render.format_row_start()
    for field in db['header']:
        if field in setfile.colheads:
            #ostr += '    <th align=center>%s</th>' % setfile.colheads[field]
            ostr += pif.render.format_cell(ncols, setfile.colheads[field], True)
            ncols = ncols + 1
    ostr += pif.render.format_row_end()

    for model in db['model']:
        showme = True
        for field in db['header']:
            if pif.form.has(field):
                if model[field] != pif.form.get_str(field) or (not model[field] and not pif.form.get_str(field)):
                    showme = False
        if not showme:
            continue
        ostr += pif.render.format_row_start()
        if 'text' in model:
            # Need to calculate the colspan better.
            ostr += pif.render.format_cell(0, model['text'], False, {'colspan': len(db['header']) - 1})
            ostr += pif.render.format_row_end()
            continue
        if 'section' in model:
            # Need to calculate the colspan better.
            #ostr += '    <th colspan=%d valign=top>\n' % (len(db['header']) - 1)
            #ostr += model['section']
            #ostr += '</th></tr>\n'
            ostr += pif.render.format_section(None, model['section'], also={'colspan': (len(db['header']) - 1)})
            continue
        ifield = 0
        for field in db['header']:
            if field == 'desc':
                ostr += pif.render.format_cell(ifield, mod_desc(model[field]))
            elif field == 'fulldesc':
                ostr += pif.render.format_row_end()
                ostr += pif.render.format_row_start()
                ostr += pif.render.format_cell(ifield, mod_desc(model['desc']), False, {'colspan': repr(db['ncols'])})
            elif field == 'insetdesc':
                ostr += pif.render.format_row_end()
                ostr += pif.render.format_row_start()
                ostr += pif.render.format_cell(ifield, mod_desc(model['desc']), False, {'colspan': repr(db['ncols'] - 1)})
            elif field == 'num':
                modnums = []
                for modnum in model[field].split(';'):
                    modnum = mod_num(prefix, modnum, model.get('rank'))
                    if dups:
                        if modnum in modnumlist:
                            model['desc'].append('duplicate!')
                        modnumlist.append(modnum)
                    modnums.append(modnum)
                ostr += pif.render.format_cell(ifield, '<nobr>%s</nobr>' % "<br>".join(modnums), False, {'height': '8'})
            elif field == 'pic':
                modnum = model['num'].split(';')
                also = {}
                if 'insetdesc' in db['header']:
                    also = {'rowspan': '2'}
                ostr += pif.render.format_cell(ifield, img(pif, prefix, modnum, model.get('rank'), int(db['digits']), (model['year'] != 'not made'), dirs=setfile.dirs), False, also)
            elif field == 'fullpic':
                ostr += pif.render.format_row_end()
                ostr += pif.render.format_row_start()
                modnum = model['num'].split(';')
                also = {'colspan': repr(db['ncols'])}
                if 'insetdesc' in db['header']:
                    also = {'rowspan': '2'}
                ostr += pif.render.format_cell(ifield, img(pif, prefix, modnum, model.get('rank'), int(db['digits']), (model['year'] != 'not made'), dirs=setfile.dirs), False, also)
            elif field == 'name':
                if model[field]:
                    ostr += pif.render.format_cell(ifield, '<center><b>' + model[field] + '</b></center>')
                else:
                    ostr += pif.render.format_cell(ifield)
            else:
                if model[field]:
                    ostr += pif.render.format_cell(ifield, model[field])
                else:
                    ostr += pif.render.format_cell(ifield)
            ifield += 1
        ostr += pif.render.format_row_end()
    ostr += '</table>\n'
    return ostr


def print_no_table(pif, db):
    ostr = '<a name="%(label)s">\n' % db
    ostr += '<h3><a href="/cgi-bin/sets.cgi?page=' + pif.form.get_str('page') + '&set=%(label)s#%(label)s">%(title)s</a></h3>\n' % db
    return ostr


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
    ostr = model
    if prefix:
        ostr = prefix + '-' + ostr
    if suffix:
        ostr += '-' + suffix
    return ostr


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
    ostr = pif.render.format_image_required(modnum, mod_num(prefix, model[0], suffix), made=made, pdir=dirs.get(prefix))
    return '<center>' + ostr + '</center>'


def select_set(pif):
    lran = {'name': "A few of the special sets produced by Matchbox in recent years:", 'entry':
	['<b><a href="?page=%s">%s</a></b> - %s' %
	    (ent['page_info.id'][5:], ent['page_info.title'], ent['page_info.description'])
	    for ent in pif.dbh.fetch_pages("id like 'sets.%' and (flags & 1)=0", order='description,title')]}
    llineup = {'section': [{'id': 'i', 'range': [lran]}],
	       'tail': [pif.render.format_button("back", link="..") + " to the main index."]}
    return pif.render.format_template('setsel.html', llineup=llineup)


@basics.web_page
def sets_main(pif):
    pif.render.print_html()

    if pif.form.has('page'):
        set_id = pif.form.get_str('set')
        dups = pif.form.get_int('dups')
        setfile = SetFile(os.path.join(config.SRC_DIR, pif.form.get_str('page') + '.dat'))
        print do_set(pif, setfile, set_id, dups=dups)
    else:
        print select_set(pif)



if __name__ == '__main__':  # pragma: no cover
    pass
