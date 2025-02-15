#!/usr/local/bin/python

import os

import basics
import config
import imglib
import mbdata
import mbmods
import mflags
import render


# -------- makes -----------------------------------


@basics.web_page
def makes_main(pif):
    make_q = pif.dbh.depref(
        'vehicle_make',
        pif.dbh.fetch_vehicle_makes(where='' if pif.is_allowed('a') else f'not (flags & {config.FLAG_ITEM_HIDDEN})'))
    makelist = [(x['id'], x['name']) for x in make_q]
    makedict = {x['id']: x for x in make_q}
    makedict['unl'] = {'id': 'unl', 'name': 'Unlicensed', 'company_name': 'Unlicensed', 'flags': 0}
    makedict['unk'] = {'id': 'unk', 'name': 'unknown', 'company_name': 'Make unknown', 'flags': 0}
    footer = ''
    make = pif.form.get_str('make', '')
    makes = [make]

    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append('/cgi-bin/makes.cgi', 'Models by Make')
    if make:
        pif.ren.title = 'Models by Make: ' + makedict.get(make, {}).get('name', '')
    if make == 'text':
        pif.ren.hierarchy_append(pif.request_uri, 'Search')
    elif make:
        pif.ren.hierarchy_append(pif.request_uri, makedict.get(make, {'name': make})['name'])
    pif.ren.print_html()

    if make == 'text':
        makename = pif.form.get_str('text')
        if makename:
            makes = []
            for m in makelist:
                if m[1].lower().startswith(makename.lower()):
                    makes.append(m[0])
            if not makes:
                makes = ['unk']
        else:
            make = ''
    elif make and make in makedict:
        links = pif.dbh.fetch_link_lines(page_id='makes', section=make)
        footer = '<ul>' + '\n'.join([
            '<li>' + pif.ren.format_link(x['link_line.url'], x['link_line.name']) for x in links]) + '</ul>\n'
        if pif.is_allowed('a'):  # pragma: no cover
            footer += pif.ren.format_button_link(
                'ADD LINK', f'edlinks.cgi?page_id=makes&sec={make}&add=1')

    if make:
        llineup = show_makes(pif, makedict, makes)
    else:
        makes = sorted([x[0] for x in makelist], key=lambda x: makedict[x]['name'])
        llineup = makes_form(pif, makedict, makes)
    pif.ren.set_button_comment(pif, keys={'make': 'make', 'text': 'text'})
    if pif.is_allowed('a'):  # pragma: no cover
        if make and make != 'text':
            footer += pif.ren.format_button_link('edit', link=pif.dbh.get_editor_link('vehicle_make', {'id': make}))
    llineup.footer = footer
    return pif.ren.format_template('simplematrix.html', llineup=llineup.prep())


def makes_form(pif, makedict, makes):
    firsties = sorted(set([x['name'][0].upper() for x in makedict.values()]))
    cols = 8

    def make_make_link(mdict):
        if not mdict:
            return render.Entry(text='')
        pic = pif.ren.fmt_img(mdict['id'], prefix='t', pdir=config.IMG_DIR_MAKE)
        name = (pic + '<br>' + mdict['name']) if pic else mdict['name']
        return render.Entry(text=pif.ren.format_link("makes.cgi?make=" + mdict['id'], name),
                            class_name='bgno' if mdict['flags'] else 'bgok')

    llineup = render.Matrix(
        columns=cols,
        header='<hr>Choose a make:<br>',
        footer='<hr>' + str(len(makedict)),
        section=[render.Section(columns=cols, range=[
            render.Range(name='Other', id='makelist', entry=[
                make_make_link(makedict.get(x)) for x in ['unk', 'unl']] +
                [render.Entry(text='&nbsp;', colspan=cols - 2)])])]
    )
    for first in firsties:
        ents = [make_make_link(makedict.get(x)) for x in makes if x.startswith(first.lower())]
        ents += [render.Entry(text='&nbsp;', colspan=cols - (len(ents) % cols))] if len(ents) % cols else []
        section = render.Section(columns=cols, range=[
            render.Range(name=first, entry=ents, id='makelist')])
        llineup.section.append(section)
    return llineup


def show_make_selection(pif, make_id, makedict):
    casting_make = make_id
    make = makedict.get(make_id, {})
    lsec = render.Section(  # pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
        anchor=make_id, columns=4, name=pif.ren.fmt_img(
            make_id, prefix='t', pdir=config.IMG_DIR_MAKE) + '<br>' + make.get('company_name', make_id)
    )
    lran = render.Range()
    where = '' if pif.is_allowed('a') else "section.page_id='manno'"
    if make_id == 'unk':
        casting_make = ''
    castings = pif.dbh.fetch_casting_list_by_make(casting_make, where=where)
    aliases = []  # pif.dbh.fetch_aliases(where=f"casting.make='{casting_make}'")
    mlist = []

    for mdict in castings:
        mlist.append(pif.dbh.make_man_item(mdict))

    for mdict in aliases:
        manitem = pif.dbh.make_man_item(mdict)
        if manitem.ref_id:
            manitem.picture_id = manitem.id
        mlist.append(manitem)

    mlist.sort(key=lambda x: x.name)
    for manitem in mlist:
        # input manitem:  id, (picture_id), made, country, link, linkid, name, descs, made, unlicensed, scale, (type)
        lran.entry.append(render.Entry(text=mbmods.add_man_item_table_pic_link(pif, manitem, flago=mbmods.flago)))

    lsec.range.append(lran)
    return lsec


def show_makes(pif, makedict, makes):
    llineup = render.Matrix()
    mbmods.flago = mflags.FlagList()

    for make_id in makes:
        lsec = show_make_selection(pif, make_id, makedict)
        llineup.section.append(lsec)
    return llineup


# ---- commands ------------------------------


def add_casting_make(pif, mod_id, make_id):
    make = pif.dbh.fetch_vehicle_make(make_id)
    if make:
        print(make['vehicle_make.name'])
        print(pif.dbh.add_casting_make(mod_id, make_id))
        mod = pif.dbh.fetch_casting(mod_id)
        if not mod['make']:
            print(pif.dbh.write_casting({'make': make_id}, mod_id))
    elif make_id == 'unl':
        print('Unlicensed')
        print(pif.dbh.add_casting_make(mod_id, make_id))
        mod = pif.dbh.fetch_casting(mod_id)
        if not mod['make']:
            print(pif.dbh.write_casting({'make': make_id}, mod_id))
    else:
        print(make_id, 'not found')


def delete_casting_make(pif, mod_id, make_id):
    pif.dbh.delete_casting_make(mod_id, make_id=None)


def unhide_makes(pif, *args):
    # if any casting for a make has a section that is shown, unhide the make
    makes = args if args else [x['vehicle_make.id'] for x in pif.dbh.fetch_vehicle_makes()]
    for make_id in makes:
        res = pif.dbh.fetch(
            'casting,casting_make,section', columns='count(*) as c', one=True,
            where="casting.section_id=section.id and section.page_id='manno' and "
                  f"casting_make.casting_id=casting.id and casting_make.make_id='{make_id}'")
        make = pif.dbh.depref('vehicle_make', pif.dbh.fetch_vehicle_make(make_id))
        flag = 0 if res['c'] else config.FLAG_ITEM_HIDDEN
        print(make, flag)
        pif.dbh.update_vehicle_make(make['id'], {'flags': flag})


def check_makes(pif, *args):
    # if any casting for a make has a section that is shown, unhide the make
    makes = pif.dbh.depref('vehicle_make', pif.dbh.fetch_vehicle_makes())
    makes_d = {x['id']: x for x in makes}
    makes_l = args if args else sorted(makes_d.keys())

    for make_id in makes_l:
        if make_id in ('unk', 'unl'):
            continue
        if make_id in makes_d:
            make = makes_d[make_id]
            if not make['name']:
                print(make_id, 'no name')
            if not make['company_name']:
                print(make_id, 'no company name')
            if not os.path.exists('.' + config.IMG_DIR_MAKE + '/t_' + make_id + '.gif'):
                print(make_id, 'no large logo')
            if not os.path.exists('.' + config.IMG_DIR_MAKE + '/u_' + make_id + '.gif'):
                print(make_id, 'no small logo')
        else:
            print(make_id, 'not found')


def microize(pif, *args):
    makes = args if args else [x['vehicle_make.id'] for x in pif.dbh.fetch_vehicle_makes()]
    for make_id in makes:
        if make_id in ('unk', 'unl'):
            continue
        fpth = pif.ren.find_image_path(make_id, largest='t', pdir=config.IMG_DIR_MAKE)
        if fpth:
            oname = 'u_' + make_id + '.gif'
            ofi = imglib.shrinker(fpth, oname, (0, 0, 100, 60), mbdata.imagesizes['u'], [])
            opth = os.path.join('.' + config.IMG_DIR_MAKE, oname)
            imglib.simple_save(ofi, opth)


def find_make(pif, make_id):
    for make in pif.dbh.fetch_vehicle_makes():
        if make['vehicle_make.id'].startswith(make_id):
            print('%-3s %-15s %s' % (make['vehicle_make.id'], make['vehicle_make.name'],
                                     make['vehicle_make.company_name']))


def create_make(pif, make_id, name, company=''):
    make = pif.dbh.fetch_vehicle_make(make_id)
    if not make:
        print(pif.dbh.add_vehicle_make(make_id, name, company))
        # os.copy('.' + config.IMG_DIR_MAKE + '/t_unk.gif', '.' + config.IMG_DIR_MAKE + '/t_' + make_id + '.gif')


cmds = [
    ('d', delete_casting_make, "delete casting make: mod_id make_id"),
    ('a', add_casting_make, "add casting make: mod_id make_id"),
    ('f', find_make, "find: make_id"),
    ('c', create_make, "create make: make_id, make_name, company"),
    ('m', microize, "microize [id...]"),
    ('u', unhide_makes, "unhide [id...]"),
    ('x', check_makes, "check [id...]"),
]


# ---- ---------------------------------------


if __name__ == '__main__':  # pragma: no cover
    basics.process_command_list(cmds=cmds, dbedit='')
