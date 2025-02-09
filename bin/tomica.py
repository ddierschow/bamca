#!/usr/local/bin/python
# small: 200x120
# large: 300x180

import csv
from io import StringIO
import os
import requests

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
        self.stitle = slist['title'] if slist else ''
        self.slabel = slist['label'] if slist else ''
        self.sdict['title'] = self.stitle
        self.sdict['label'] = self.slabel
        self.sdict['comment'] = []
        self.mdlist = []

    def parse_c(self, slist):
        slist = self.parse_data_line(slist)
        self.sdict['comment'].append(slist['text'])

    def parse_m(self, slist):
        pslist = self.parse_data_line(slist)
        if pslist:
            manitem = get_man_item(pslist)
            self.mdlist.append(manitem)
            self.mdict[manitem['id']] = manitem
        else:
            useful.write_message('parse_m fail', slist)

    def parse_p(self, slist):
        pslist = self.parse_data_line(slist)
        if pslist:
            pslist.setdefault('descs', [])
            if pslist.get('description'):
                pslist['descs'].extend(pslist['description'].split(';'))
            self.mdlist.append(pslist)
            self.mdict[pslist['id']] = pslist
        else:
            useful.write_message('parse_p fail', slist)

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
    # mod['link'] = linkurl[linky]
    # mod['linkid'] = linkids[linky](mod)
    return mod


def type_match(t1, t2):
    for c in t2:
        if c in t1:
            return True
    return False


def show_section(pif, manf, sect, start=None, end=None, year=None):
    print('<hr><center><h3 id="%s">%s</h3></center>' % (sect['label'], sect['title']))
    if sect['comment']:
        print('\n'.join(sect['comment']) + '<br>')
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
            pif.ren.comment(start, end, modno)
            if modno < start or modno > end:
                continue

        if year and slist['last_year'] and (year < int(slist['first_year']) or year > int(slist['last_year'])):
            continue

        slist['link'] = "/cgi-bin/upload.cgi?d=./pic/tomica&n"
        slist['linkid'] = 's_' + slist['id'].lower()
        slist['descs'] = slist.get('desc', '').split(';')
        slist['country'] = ''

        if shown == 0:
            print("<center><table><tr align=top>")
        shown += 1
        print(" <td valign=top width=%d>" % 200)
        print(models.add_model_table_pic_link(pif, slist))
        print(" </td>")
        if (shown == cols):
            print("</tr></table></center>\n")
            shown = 0

    if shown:
        print("</tr></table></center>\n")


def show_section_list(pif, sect):
    cols = 3
    print('<table class="smallprint pagebreak" width="100%" id="{}">'.format(sect['label']))
    print('<tr><td colspan=%d style="text-align: center; font-weight: bold;">%s</td></tr>' % (4 * cols, sect['title']))
    inmods = [x for x in sect['models'] if x['subid'] != 'X']
    mods = []
    mpc = len(inmods) // cols
    if len(inmods) % cols:
        mpc += 1
    for col in range(0, cols):
        mods.append(inmods[col * mpc:(col + 1) * mpc])

    while True:
        print(' <tr>')
        found = False
        for col in range(0, cols):
            if mods[col]:
                slist = mods[col].pop(0)
                slist['shortname'] = slist['name']
                print(models.add_model_table_list_entry(pif, slist))
                found = True
        print(' </tr>')
        if not found:
            break

    print('<tr>')
    for col in range(0, cols):
        print('<td colspan=4 width=%d%%>&nbsp;</td>' % (100 / cols))
    print('</tr>')

    print("</table>")
    print()


def run_file(pif, manf, start=0, end=9999, year=None):
    for sect in manf.dictlist:
        show_section(pif, manf, sect, start, end, year)

    for sect in manf.dictlist:
        show_section_list(pif, sect)


'''<style>
@media print { table {page-break-inside:avoid} }
</style>
'''


@basics.web_page
def main(pif):
    pif.ren.print_html()
    print(pif.ren.format_head())
    useful.header_done()
    manf = MannoFile(useful.relpath(config.SRC_DIR, 'tomica.dat'))
    # mans = manf.dictlist
    if pif.form.has('num'):
        print('<meta http-equiv="refresh" content="0;url=single.cgi?id=%s">' % pif.form.get_str('num'))
        return
    else:
        run_file(pif, manf, year=pif.form.get_str('year'))
    print(pif.ren.format_tail())


img_url = 'http://tomicadas.on.coocan.jp/{id}.jpg'  # id=000-00
img_dest = 'pic/tomica/s_{id}.jpg'
url = 'http://tomicadas.on.coocan.jp/catalog_120.htm'


def scrape(pif):
    pass


def pictures(pif):
    manf = MannoFile(useful.relpath(config.SRC_DIR, 'tomica.dat'))
    for sect in manf.dictlist:
        for slist in sect['models']:
            dest = img_dest.format(id=slist.get('id', 'unset').lower())
            if not os.path.exists(dest):
                print(dest)
                open(dest, 'bw').write(requests.get(img_url.format(id=slist['id'])).content)


def refresh(pif):
    minefile = [x.strip().split('|') for x in open(useful.relpath(config.SRC_DIR, 'tomica_mine.csv')).readlines()]
    manf = MannoFile(useful.relpath(config.SRC_DIR, 'tomica.dat'))
    mine = {x[0]: x[3] for x in minefile}
    out_file = StringIO()
    field_names = ["id", "name", "year", "have", "image"]
    writer = csv.DictWriter(out_file, fieldnames=field_names)
    writer.writeheader()
    for sect in manf.dictlist:
        for slist in sect['models']:
            writer.writerow({
                'id': slist['id'],
                'name': slist['name'],
                'year': slist.get('first_year', ''),
                'have': mine.get(slist['id'], 'no'),
                'image': 'http://bamca.org/pic/tomica/s_' + slist['id'].lower() + '.jpg'})
    out_str = out_file.getvalue()
    out_file.close()
    print(out_str)


cmds = [
    ('s', scrape, "scrape"),
    ('p', pictures, "pictures"),
    ('r', refresh, "refresh"),
]


# ---- ---------------------------------------


if __name__ == '__main__':  # pragma: no cover
    basics.process_command_list(cmds=cmds, dbedit='', options='fs')
