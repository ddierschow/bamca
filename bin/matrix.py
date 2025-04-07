#!/usr/local/bin/python

import glob
import os
import re

import basics
import config
import mbdata
import render
import useful

d_re = re.compile(r'%\d*d')


class MatrixFile(object):
    def __init__(self, pif):
        self.tables = []
        self.text = []
        self.dates = set()
        self.page = pif.form.get_str('page')
        self.cat_id = pif.form.get_str('cat')
        self.large = pif.form.get_bool('large')
        if self.page:
            self.from_db(pif)
        elif self.cat_id:
            self.from_cat(pif)

    def create_ent(self, pif, ent, sec):
        ent = pif.dbh.make_mat_item(ent, sec)
        ent.pdir = ent.pdir or pif.ren.pic_dir
        if not ent.sub_id_matches:
            return None

        if ent.model_type == 'MP':
            ent.image = pif.ren.format_image_required(
                ent.mod_id, prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_MAN, nopad=True, blank=True)
        elif ent.is_no_variation:
            ent.image = pif.ren.format_image_optional(
                f'{ent.mod_id}', prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_MAN, nopad=True)
        elif ent.range_id and sec.img_format:
            ent.image = pif.ren.format_image_required(
                useful.clean_name(sec.img_format % ent.range_id, '/'), pdir=ent.pdir)
        elif ent.var.var:
            if self.cat_id:
                ent.image = pif.ren.format_image_required(
                    f'{ent.mod_id}-{ent.var.picture_id}', prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_VAR, nopad=True)
            else:
                ent.image = pif.ren.format_image_optional(
                    f'{ent.mod_id}-{ent.var.picture_id}', prefix=mbdata.IMG_SIZ_SMALL, pdir=config.IMG_DIR_VAR, nopad=True)
        elif '%' in sec.link_format:
            ent.image = pif.ren.format_image_required(
                useful.clean_name(sec.link_format % ent.range_id, '/'), prefix=mbdata.IMG_SIZ_SMALL,
                pdir=ent.pdir, blank=True)
        else:
            ent.image = pif.ren.format_image_required(
                useful.clean_name(sec.link_format, '/'), prefix=mbdata.IMG_SIZ_SMALL, pdir=ent.pdir, blank=True)
        return ent

    def from_db(self, pif):
        pif.ren.hierarchy_append('/cgi-bin/matrix.cgi', 'Series')
        pif.ren.hierarchy_append(f'/cgi-bin/matrix.cgi?page={self.page}', pif.ren.title)
        secs = pif.dbh.make_sec_items(pif.dbh.fetch_sections({'page_id': pif.page_id}))
        ents = pif.dbh.fetch_matrix_models_variations(pif.page_id)
        for sec in secs:
            sec.text = ''
            sec.ents = {}
            for ent in ents:
                if ent['matrix_model.section_id'] == sec.id:
                    if ent := self.create_ent(pif, ent, sec):
                        sec.ents.setdefault(ent.range_id, list())
                        sec.ents[ent.range_id].append(ent)
            self.tables.append(sec)
        self.tables.sort(key=lambda x: x.display_order)

    def from_cat(self, pif):
        if not self.cat_id:
            return
        if not (cat := pif.dbh.fetch_category(self.cat_id)):
            raise useful.SimpleError(f'Category not found. {self.cat_id}')
        pif.ren.title = cat['name']
        pif.ren.hierarchy_append('/database.php#cats', 'By Categories')
        pif.ren.hierarchy_append(f'/cgi-bin/matrix.cgi?cat={self.cat_id}', cat['name'])
        sec = pif.dbh.make_sec_item({  # maybe make this the section for page_id='matrix'?
            'id': 'cat',
            'page_id': 'matrix',
            'display_order': 0,
            'category': cat['name'],
            'flags': 0,
            'name': '',
            'columns': 4,
            'start': 0,
            'pic_dir': pif.ren.pic_dir,
            'disp_format': '',
            'link_format': '',
            'img_format': '',
            'note': '',
        })
        sec.text = ''
        sec.ents = {}

        def add_ent(var):
            range_id = var['v.mod_id'] + '-' + var['v.var']
            if range_id in sec.ents:
                return
            var.update({
                'id': var.get('vs.id') or '',  # exact value is unimportant
                'mod_id': var['v.mod_id'],
                'name': var['base_id.rawname'].replace(';', ' '),
                'shown_id': range_id,
            })
            ent = self.create_ent(pif, var, sec)
            if not ent or self.cat_id != ent.vs.vs_cat and self.cat_id not in ent.var.category:
                return
            ent.range_id = range_id
            sec.ents.setdefault(range_id, list())
            sec.ents[range_id].append(ent)  # should just be an assign but other places expect a list so...
            if date_m := mbdata.year_re.search(ent.var.date):
                self.dates.add(date_m.group('y'))

        vsvars = pif.dbh.fetch_variations_by_vs_category(self.cat_id)
        # weird-ass sort
        vsvars = [x for x in vsvars if x.get('vs.ref_id')] + [x for x in vsvars if not x.get('vs.ref_id')]
        for vsvar in vsvars:
            add_ent(vsvar)

        for var in pif.dbh.fetch_variations_by_category(self.cat_id):
            add_ent(var)

        disp_order = 1
        for range_id in sorted(sec.ents):
            sec.ents[range_id][0].display_order = disp_order
            disp_order += 1
        self.tables.append(sec)

    def matrix(self, pif):
        llineup = render.Matrix(id=pif.page_name, note='\n'.join(self.text), columns=4)
        comments = set()

        for table in self.tables:
            # useful.write_comment('add_table', table)
            section_name = table.name
            if not (table.hide_image) and (table.id not in pif.page_id.split('.')):
                img = pif.ren.format_image_optional(table.id, pdir=table.pic_dir, nopad=True)
                if img:
                    section_name += ('<br>' if section_name else '') + img
            section = render.Section(id=table.id, name=section_name, anchor=table.id, columns=table.columns)
            if pif.is_allowed('a'):  # pragma: no cover
                if section.id == 'cat':
                    dates = sorted(self.dates)
                    if len(self.dates) == 1:
                        section.name += f" {dates[0]}"
                    elif len(self.dates) > 1:
                        section.name += f" {dates[0]}-{dates[-1]}"
                else:
                    lm = pif.dbh.fetch_lineup_model(f"mod_id='{pif.page_id}' and picture_id='{section.id}'")
                    section.name += f' ({pif.page_id}/{section.id}) '
                    section.name += pif.ren.format_link(
                        f"mass.cgi?tymass=lm_series&page_id={pif.page_id}&section_id={section.id}",
                        pif.ren.fmt_star("green" if lm else "red"))
                    section.name += pif.ren.format_button_link(
                        "edit", f"editor.cgi?table=section&page_id={pif.page_id}&id={section.id}") + ' '
                    section.name += pif.ren.format_button_link(
                        "add", f"editor.cgi?table=matrix_model&page_id={pif.page_id}&section_id={section.id}&add=1")

                if self.large:
                    section.columns = 1
            ran = render.Range(entry=[])
            range_ids = list(table.ents.keys())
            range_ids.sort(key=lambda x: table.ents[x][0].display_order)
            for range_id in range_ids:
                if section.id == 'cat':
                    ran.entry.append(self.add_cell(pif, table.ents[range_id], table, comments))
                elif mods := mbdata.find_vs_variations(table.ents[range_id], table.id, str(range_id)):
                    ran.entry.append(self.add_cell(pif, mods, table, comments))
            section.range.append(ran)
            llineup.section.append(section)
        # llineup.tail = [pif.ren.format_image_art('bamca_sm'), '']
        pif.ren.set_button_comment(pif, '')
        llineup.tail = ['', '<br>'.join([mbdata.comment_designation[comment] for comment in sorted(comments)])]
        return llineup

    def add_cell(self, pif, ents, table, comments):
        libdir = pif.ren.lib_dir
        entd = {}
        for ent in ents:
            entd.setdefault(ent.mod_id, [])
            entd[ent.mod_id].append(ent)

        # pif.ren.comment('add_cell', entd)

        varimage = ''
        for mod in entd:
            ent = entd[mod][0]

            for ent2 in entd[mod][1:]:
                if ent.show_all_variations:
                    ent.image += ent2.image
                elif not ent.image:
                    ent.image = ent2.image
                for desc in ent2.description:
                    if desc not in ent.description:
                        ent.description.append(desc)
            if ent.image:
                varimage = ent.image

        if ent.is_no_variation:
            ent.picture_only = ent.no_variation = 1
        elif not ent.mod_id:
            comments.add('m')
            ent.no_casting = 1
            ent.picture_only = 1
        else:
            if not ent.vs.var_id and not ent.var.var:
                comments.add('v')
                ent.no_variation = 1
            if not varimage:
                comments.add('i')
                ent.no_specific_image = 1
        if pif.is_allowed('a') and not ent.vs.ref_id:
            ent.no_vs = 1
        ent.imgstr = varimage

        ent.number = ent.disp_id
        if not ent.shown_id and ent.disp_id:
            ent.shown_id = ent.disp_id
        if ent.no_id:
            ent.shown_id = ''

        ent.product = [ent.link]
        prodpic = (
            pif.ren.find_image_path(ent.product, suffix='jpg', pdir=ent.pdir) or
            pif.ren.find_image_path(ent.product, suffix='jpg', largest='l', pdir=ent.pdir))
        if prodpic:
            comments.add('c')
            ent.is_product_picture = 1
            if pif.is_allowed('a') and self.large:
                ent.prodpic = prodpic
        if ent.not_made:
            comments.add('n')
            ent.picture_only = 1
        ent.spdir = mbdata.dirs_r.get(ent.pdir, ent.pdir)

        ent.href = ''
        if ent.model_type == 'MP':
            ent.href = f"packs.cgi?page=&id={ent.mod_id}"
        elif not ent.mod_id:
            img = pif.ren.find_image_path(ent.link, largest='h')
            if img:
                ent.href = f'/{img}'
        elif ent.vs.ref_id:
            ent.href = (
                f"single.cgi?id={ent.mod_id}&"
                f"dir={ent.spdir}&pic={ent.link}&ref={ent.vs.ref_id}&sec={ent.vs.sec_id}&ran={ent.vs.ran_id}")
        elif ent.var.var:
            ent.href = f"vars.cgi?mod={ent.mod_id}&var={ent.var.var}"
        else:
            ent.href = f"single.cgi?dir={ent.spdir}&pic={ent.link}&id={ent.mod_id}"
        # ent.descriptions = [x for x in ent.description if x]
        # if ent.descriptions and not ent.is_no_variation:
        #     pass
        # elif ent.description:
        #     ent.descriptions = ent.description.split(';')
        # ^ that nonsense means that descriptions only contains the original description.  what?

        desclist = []  # dedup these descs
        for x in ent.description:
            if x and x not in desclist:
                desclist.append(x)
        ent.description = desclist

        ent.additional = ''
        if pif.is_allowed('a'):  # pragma: no cover
            ent.additional += pif.ren.format_button_link("edit", pif.dbh.get_editor_link('matrix_model', id=ent.id))
            pic = ent.link
            ent.additional += pif.ren.format_button_link(
                "upload",
                f"upload.cgi?d={libdir}&n={pic}&c={pic}&link=" + useful.url_quote(f'/cgi-bin/matrix.cgi?page={pif.page_id}'))

        if ent.disp_format:
            if ent.shown_id:
                ent.displayed_id = ent.disp_format % ent.shown_id
        elif ent.shown_id:
            ent.displayed_id = ent.shown_id

        ent.display_id = pif.page_name

        entry = render.Entry(data=ent, class_name='bg_' + ent.style_id)
        # entry.anchor = f'{ent.number}'
        return entry


def select_matrix(pif):
    pif.ren.hierarchy_append('/cgi-bin/matrix.cgi', 'Series')
    dirs = {
        'pic/prod/series': 'Various Series',
        'pic/prod/prcoll': 'Premiere and Collectible',
        'pic/prod/premium': 'Superfast and Other Premium',
        'pic/prod/code2': 'Code 2 Models',
        'pic/prod/odds': 'Odds and Ends',
    }
    ser = pif.dbh.make_page_items(pif.dbh.fetch_pages("id like 'matrix.%'", order='description,title'))
    ents = {x: [] for x in dirs}
    for ent in ser:
        pic_dir = ent.pic_dir if ent.pic_dir in ents else 'pic/prod/odds'
        ent.id = ent.id.split('.', 1)[-1]
        link = f'<b><a href="?page={ent.id}">{ent.title}</a></b> - {ent.description}'
        if not ent.is_hidden:
            ents[pic_dir].append(link)
        elif pif.is_allowed('a'):  # pragma: no cover
            ents[pic_dir].append(f'<i>{link}</i>')

    return render.Listix(section=[render.Section(id='ml', range=[
        render.Range(id='ml', name=title, entry=ents[pic_dir]) for pic_dir, title in dirs.items()])])


@basics.web_page
def main(pif):
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.print_html()
    matf = MatrixFile(pif)
    if matf.tables:
        llineup = matf.matrix(pif)
        return pif.ren.format_template('matrix.html', llineup=llineup.prep())
    return pif.ren.format_template('simpleulist.html', llineup=select_matrix(pif))


def select_cats(pif):
    pif.ren.hierarchy_append('/database.php#cats', 'By Categories')
    lran = render.Range(id='ml', name="Model Categories")
    cats = pif.dbh.fetch_categories()
    for ent in cats:
        link = '<b><a href="?cat=%(id)s">%(name)s</a> (%(id)s)</b>' % ent
        if ent['flags'] & config.FLAG_CATEGORY_INDEXED:
            lran.entry.append(link)
        elif pif.is_allowed('a'):  # pragma: no cover
            lran.entry.append('<i>' + link + '</i>')
    return render.Listix(section=[render.Section(id='ml', range=[lran])])


@basics.web_page
def cats_main(pif):
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.print_html()
    matf = MatrixFile(pif)
    if matf.tables:
        llineup = matf.matrix(pif)
        return pif.ren.format_template('matrix.html', llineup=llineup.prep())
    return pif.ren.format_template('simpleulist.html', llineup=select_cats(pif))


def check_pics(pif):
    fmts = {(x['page_id'], x['id']): x['link_format']
            for x in pif.dbh.fetch_sections(where='page_id like "matrix.%"')}
    probs = {}
    for ent in pif.dbh.fetch_matrix_models():
        fmt = fmts.get((ent['page_id'], ent['section_id']), '')
        is_num_id = d_re.search(fmt)
        range_id = int(ent['range_id'] or 0) if is_num_id else ent['range_id']
        image = useful.clean_name((fmt % range_id) if '%' in fmt else fmt, '/')
        if image != ent['base_id']:
            probs.setdefault(ent['page_id'], set())
            probs[ent['page_id']].add(ent['section_id'])
    for k, v in sorted(probs.items()):
        print(k, ' '.join(sorted(v)))


def check_dups(pif):
    count = {}
    found = []
    for mm in pif.dbh.fetch_matrix_models():
        del mm['id']
        del mm['display_order']
        if mm in found:
            print(mm)
        found.append(mm)
        count.setdefault((mm['page_id'], mm['section_id']), 0)
        count[(mm['page_id'], mm['section_id'])] += 1
#    print(len(found))
#    for k, v in count.items():
#        print(v, '.'.join(k))


def move_section(pif, section_id, old_page_id, new_page_id):
    sec = pif.dbh.fetch_section(sec_id=section_id, page_id=old_page_id)
    if not sec:
        print('no section')
        return
    old_page = pif.dbh.fetch_page(old_page_id)
    if not old_page:
        print('no old_page')
        return
    new_page = pif.dbh.fetch_page(new_page_id)
    if not new_page:
        print('no new_page')
        return
    print('section')
    sec['section.page_id'] = new_page_id
    print(pif.dbh.insert_or_update_section(sec.todict()))
    print('matrix_model')
    for model in pif.dbh.fetch_matrix_models(page_id=old_page_id, section=section_id):
        model['page_id'] = new_page_id
        print(pif.dbh.insert_or_update_matrix_model(model))
    print('variation_select')
    for vs in pif.dbh.fetch_variation_selects_for_ref(old_page_id, section_id):
        vs['ref_id'] = new_page_id
        print(pif.dbh.update_variation_select(vs))
    print('lineup_model')
    for lm in pif.dbh.fetch_lineup_model({'mod_id="{old_page_id}" and picture_id="{section_id}"'}):
        lm['lineup_model.mod_id'] = new_page_id
        print(pif.dbh.update_lineup_model('id={lm["lineup_model.id"]', lm))


def check_base_id(pif, page_id=None, section_id=None):
    found = set()
    for mod in pif.dbh.fetch_matrix_models(page_id=page_id, section=section_id):
        if not mod['base_id']:
            if section_id:
                print(mod['id'], mod['page_id'], mod['section_id'], mod['range_id'], mod['display_order'])
            found.add((mod['page_id'], mod['section_id']))
    for x in sorted(found):
        print(x[0], x[1])


def set_base_id(pif, page_id, section_id, new_lfmt=None):
    sec = pif.dbh.fetch_section(sec_id=section_id, page_id=page_id)
    if not sec:
        print('no section')
        return
    page = pif.dbh.fetch_page(page_id)
    if not page:
        print('no page')
        return
    pdir = sec['pic_dir'] or page['pic_dir']
    old_lfmt = sec['link_format']
    new_lfmt = sec['link_format'] = new_lfmt or sec['link_format']
    is_old_num_id = d_re.search(old_lfmt)
    is_new_num_id = d_re.search(new_lfmt)
    print(sec)
    print(pif.dbh.insert_or_update_section(sec))
    for model in pif.dbh.fetch_matrix_models(page_id=page_id, section=section_id):
        range_id = int(model['range_id'] or 0) if is_old_num_id else model['range_id']
        model['base_id'] = (new_lfmt % int(range_id)) if is_new_num_id else (new_lfmt % range_id)
        model['range_id'] = int(range_id) if is_new_num_id else range_id
        print(pif.dbh.insert_or_update_matrix_model(model))
        rename_series_pictures(pif, pdir, old_lfmt % range_id, model['base_id'])


# want to do r - rename id
# given page_id sec_id old_ran_id new_ran_id
# fix matrix_model
# fix variation_select
# rename pictures
def rename_range_id(pif, page_id, section_id, old_range_id, new_range_id):
    page = pif.dbh.fetch_page(page_id)
    if not page:
        print('no page')
        return
    sec = pif.dbh.fetch_section(sec_id=section_id, page_id=page_id)
    if not sec:
        print('no section')
        return
    pdir = sec['section.pic_dir'] or page['pic_dir']
    lfmt = sec['section.link_format']
    mm = pif.dbh.fetch_matrix_model(page_id, section_id, old_range_id)
    if not mm:
        print('no matrix model')
        return
    is_num_id = d_re.search(lfmt)
    mm['matrix_model.range_id'] = new_range_id
    old_range_id = int(old_range_id or 0) if is_num_id else old_range_id
    new_range_id = int(new_range_id or 0) if is_num_id else new_range_id
    mm['matrix_model.base_id'] = lfmt % new_range_id
    print(lfmt % old_range_id, mm['matrix_model.base_id'])
    print(pif.dbh.insert_or_update_matrix_model(mm))
    rename_series_pictures(pif, pdir, lfmt % old_range_id, mm['matrix_model.base_id'])


def rename_series_pictures(pif, pdir, old_name, new_name):  # pragma: no cover
    old_name = old_name.lower()
    new_name = new_name.lower()
    if old_name == new_name:
        return
    patt1 = useful.relpath('.', pdir, f'?_{old_name}.*')
    pics = glob.glob(patt1)
    for old_pic in pics:
        new_pic = old_pic.replace(f'_{old_name}.', f'_{new_name}.')
        pif.ren.comment("rename", old_pic, new_pic)
        useful.write_message("rename", old_pic, new_pic, "<br>")
        os.rename(old_pic, new_pic)
        pif.dbh.rename_photo_credit(pdir, old_name, new_name)

    patt2 = useful.relpath('.', pdir, f'{old_name}.*')
    pics = glob.glob(patt2)
    for old_pic in pics:
        new_pic = old_pic.replace(f'{old_name}.', f'{new_name}.')
        pif.ren.comment("rename", old_pic, new_pic)
        useful.write_message("rename", old_pic, new_pic, "<br>")
        os.rename(old_pic, new_pic)
        pif.dbh.rename_photo_credit(pdir, old_name, new_name)


# base_id   | section_id | display_order | page_id         | range_id | mod_id | flags | style_id | shown_id | name
# 2023mmp01 | mvp2023    |             1 | matrix.movparts | 1        | MB1368 |     0 |          |          | Bent...
def import_list(pif, page_id, section_id, barfile):  # pragma: no cover
    infile = [x.strip().split('|') for x in open(barfile).readlines()]
    for num, mod_id, name in infile:
        v = {
            'base_id': '',
            'section_id': section_id,
            'display_order': num,
            'page_id': page_id,
            'range_id': num,
            'mod_id': mod_id,
            'flags': 0,
            'style_id': '',
            'shown_id': '',
            'name': name,
        }
        pif.dbh.insert_or_update_matrix_model(v, verbose=True)


cmds = [
    ('p', check_pics, "check pics"),
    ('d', check_dups, "check dups"),
    ('m', move_section, "move section: section_id old_page_id new_page_id"),
    ('cb', check_base_id, "check base id"),
    ('b', set_base_id, "set base id: page_id section_id [new_link_format]"),
    ('r', rename_range_id, "rename range id base id: page_id section_id old_range_id new_range_id"),
    ('i', import_list, "import list: page_id section_id barfile"),
]


# ---- ---------------------------------------


if __name__ == '__main__':  # pragma: no cover
    basics.process_command_list(cmds=cmds, page_id='editor', dbedit='')
