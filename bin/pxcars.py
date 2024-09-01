#!/usr/local/bin/python

import copy

import basics
import bfiles
import config
import useful


# ------- ----------------------------------------------------------


class CarsFile(bfiles.ArgFile):
    def __init__(self, fname=useful.relpath(config.SRC_DIR, "cars.dat")):
        self.sec = []
        self.ent = []
        self.secname = ''
        bfiles.ArgFile.__init__(self, fname)

    def parse_c(self, llist):
        self.parse_end()
        self.ent = []
        self.secname = llist[1]

    def parse_m(self, llist):
        self.ent.append(llist.llist[1:3])

    def parse_end(self):
        if self.ent:
            self.sec.append([self.secname, copy.deepcopy(self.ent)])


def render_cars(pif, cf):
    imax = 0
    print(pif.render.format_table_start())
    sec = 0
    print(pif.render.format_row_start())
    for c in cf.sec:
        imax = max(imax, len(c[1]))
        print(pif.render.format_cell(sec, c[0], hdr=True, also={'colspan': len(c[1][0])}))
        sec = sec + len(c[1][0])
    print(pif.render.format_row_end())

    for i in range(0, imax):
        print(pif.render.format_row_start())
        sec = 0
        for c in cf.sec:
            if i >= len(c[1]):
                for f in c[1][0]:
                    print(pif.render.format_cell(sec, ' '))
                    sec = sec + 1
            else:
                for f in c[1][i]:
                    if f == 'x':
                        print(pif.render.format_cell(sec, pif.render.format_image_art('box-sm-x.gif')))
                    elif f:
                        print(pif.render.format_cell(sec, "&nbsp;" + f + "&nbsp;"))
                    else:
                        print(pif.render.format_cell(sec, pif.render.format_image_art('box-sm.gif')))
                    sec = sec + 1
        print(pif.render.format_row_end())

    print(pif.render.format_table_end())


@basics.web_page
def cars_main(pif):
    pif.render.print_html()

    db = CarsFile(useful.relpath(config.SRC_DIR, pif.form.get_str('page', 'cars') + '.dat'))

    print(pif.render.format_head())
    render_cars(pif, db)
    print(pif.render.format_tail())
