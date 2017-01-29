#!/usr/local/bin/python
# small: 200x120
# large: 300x180

import os
import basics
import bfiles
import config
import models
import useful

# interprets "manno.dat"
class MannoFile(bfiles.ArgFile):
    def __init__(self, fname):
        self.slabel = ''
        self.stitle = ''
        self.sdict = {}
        self.tdict = {}
        self.mdlist = []
        self.dictlist = []
        self.mdict = {}
        bfiles.ArgFile.__init__(self, fname)
        self.finish_section()

    def parse_H(self, llist):
        slist = self.parse_data_line(llist)
        self.finish_section()
        self.stitle = slist['title']
        self.slabel = slist['label']
        self.sdict['title'] = self.stitle
        self.sdict['label'] = self.slabel
        self.sdict['comment'] = []
        self.mdlist = []

    def parse_c(self, slist):
        slist = self.parse_data_line(slist)
        self.sdict['comment'].append(slist['text'])

    def parse_m(self, slist):
        slist = self.parse_data_line(slist)
        manitem = get_man_item(slist)
        self.mdlist.append(manitem)
        self.mdict[manitem['id']] = manitem

    def parse_p(self, slist):
        slist = self.parse_data_line(slist)
        slist.setdefault('descs', [])
        if slist.get('description'):
            slist['descs'].extend(slist['description'].split(';'))
        self.mdlist.append(slist)
        self.mdict[slist['id']] = slist

    def parse_t(self, llist):
        self.tdict[llist[1]] = llist[2]

    def finish_section(self):
        if self.slabel:
            self.sdict['models'] = self.mdlist
            self.dictlist.append(self.sdict)
            self.sdict = {}



def get_man_item(llist, data=None):
    if not isinstance(llist, dict):
        mod = dict(zip(data, llist[1:]))
    else:
        mod = llist
    if mod['id'].isdigit():
        mod['id'] = '%03d' % int(mod['id'])
    if mod['subid'].isdigit():
        mod['id'] += '-' + "%02d" % int(mod['subid'])
    mod['name'] = mod['rawname'].replace('*', '').replace(';', ' ')
    mod['unlicensed'] = ' '
    if mod['name'].startswith('-'):
        mod['name'] = mod['name'][1:]
        mod['unlicensed'] = '-'
    elif '*' not in mod['rawname']:
        mod['unlicensed'] = '?'
    mod['made'] = True
    mod['notmade'] = ''
    mod.setdefault('description', '')
    mod.setdefault('descs', [])
    if mod['description']:
        mod['descs'] = mod['description'].split(';')
    if mod['id'][-1] == '*':
        mod['made'] = False
        mod['notmade'] = '*'
        mod['id'] = mod['id'][:-1]
        mod['descs'].append('Not made')
    #mod['link'] = linkurl[linky]
    #mod['linkid'] = linkids[linky](mod)
    return mod


def type_match(t1, t2):
    for c in t2:
        if c in t1:
            return True
    return False


def show_section(pif, manf, sect, start=None, end=None, year=None):
    print '<hr><center><h3 id="%s">%s</h3></center>' % (sect['label'], sect['title'])
    if sect['comment']:
        print '\n'.join(sect['comment']) + '<br>'
    shown = 0
    cols = 4
    this_year = None
    for i in range(len(sect['models']) - 1, -1, -1):
        sect['models'][i]['last_year'] = this_year
	this_year = None if sect['models'][i]['subid'].isdigit() and int(sect['models'][i]['subid']) == 1 \
	    else sect['models'][i]['first_year']

    for slist in sect['models']:

        if slist['subid'] == 'X':
            continue

        if start and end:
            modno = 0
            for c in slist['id']:
                if c.isdigit():
                    modno = 10 * modno + int(c)
            pif.render.comment(start, end, modno)
            if modno < start or modno > end:
                continue

        if year and slist['last_year'] and (year < int(slist['first_year']) or year > int(slist['last_year'])):
	    continue

        slist['link'] = "/cgi-bin/upload.cgi?d=./pic/tomica&r"
        slist['linkid'] = 's_' + slist['id'].lower()
        slist['descs'] = slist.get('desc', '').split(';')

        if shown == 0:
            print "<center><table><tr align=top>"
        shown += 1
        print " <td valign=top width=%d>" % 200
        print models.add_model_table_pic_link(pif, slist)
        print " </td>"
        if (shown == cols):
            print "</tr></table></center>\n"
            shown = 0

    if shown:
        print "</tr></table></center>\n"


def show_section_list(pif, sect):
    cols = 3
    print '<table class="smallprint pagebreak" width="100%" id="%s">' % sect['label']
    print '<tr><td colspan=%d style="text-align: center; font-weight: bold;">%s</td></tr>' % (4 * cols, sect['name'])
    inmods = filter(lambda x: x['subid'] != 'X', sect['models'])
    mods = []
    mpc = len(inmods) / cols
    if len(inmods) % cols:
        mpc += 1
    for col in range(0, cols):
        mods.append(inmods[col * mpc:(col + 1) * mpc])

    while True:
        print ' <tr>'
        found = False
        for col in range(0, cols):
            if mods[col]:
                slist = mods[col].pop(0)
                slist['shortname'] = slist['name']
                print models.add_model_table_list_entry(pif, slist)
                found = True
        print ' </tr>'
        if not found:
            break

    print '<tr>'
    for col in range(0, cols):
        print '<td colspan=4 width=%d%%>&nbsp;</td>' % (100 / cols)
    print '</tr>'

    print "</table>"
    print


def run_file(pif, manf, start=0, end=9999, year=None):
    for sect in manf.dictlist:
        show_section(pif, manf, sect, start, end, year)

    for sect in manf.dictlist:
        sect['name'] = 'Tomica Models'
        show_section_list(pif, sect)



'''<style>
@media print
{
table {page-break-inside:avoid}
}
</style>
'''

@basics.web_page
def main(pif):
    pif.render.print_html()
    print pif.render.format_head()
    useful.header_done()
    manf = MannoFile(useful.relpath(config.SRC_DIR, 'tomica.dat'))
    mans = manf.dictlist
    if pif.form.has('num'):
        print '<meta http-equiv="refresh" content="0;url=single.cgi?id=%s">' % pif.form.get_str('num')
        return
    else:
        run_file(pif, manf, year=pif.form.get_str('year'))
        #print pif.render.format_matrix(llineup)
    print pif.render.format_tail()


if __name__ == '__main__':  # pragma: no cover
    pass
