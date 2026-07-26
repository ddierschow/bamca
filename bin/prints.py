#!/usr/local/bin/python

import glob
from io import open
import itertools
import os

import basics
import bfiles
import bldata
from bxdata import box_lookups
import config
import imglib
import mbdata
import mbmods
import render
import useful


# ----- blister --------------------------------------------------------


@basics.web_page
def blister(pif):
    pif.ren.set_page_extra(pif.ren.modal_js)
    # pif.ren.set_page_extra(pif.ren.toggle_display_js)
    pif.ren.print_html()

    # All this here nonsense is to create the picture entries for the examples.

    bl_aliases = {x['alias.id']: x['alias.ref_id'] for x in pif.dbh.fetch_alias_blisters('BL')}
    lexamples = {}
    rexamples = {}
    cexamples = {}

    for example in bldata.lexamples:
        bpid = example[0][:example[0].find('-') + 2]
        pdir, pic = example[1].rsplit('/', 1)
        img = pif.ren.find_image_path(pic, pdir='pic/' + pdir, largest='m')
        if img:
            lexamples.setdefault(bpid, [])
            lexamples[bpid].append((example[0], img))

    lup_models = {x['lineup_model.base_id'].lower(): x for x in pif.dbh.fetch_lineup_model_blisters(
        [v for k, v in bl_aliases.items() if k[0].isupper()])}

    for example in bl_aliases.items():
        if example[0][0].isupper() and example[1] in lup_models:
            lup_model = lup_models[example[1]]
            bpid = example[0][:example[0].find('-') + 2]
            pdir = lup_model['section.pic_dir'] or lup_model['page_info.pic_dir']
            pic = lup_model['lineup_model.base_id']
            img = pif.ren.find_image_path(pic, pdir=pdir, largest='m')
            if img:
                lexamples.setdefault(bpid, [])
                lexamples[bpid].append((example[0], img))

    for region in bldata.core:
        for btype in region[2]:
            bpid = f'{region[0]}-{btype[0][0]}'
            glist = [
                (x[x.rfind('/') + 1:-4].upper(), x)
                for x in sorted(glob.glob(f'{pif.ren.pic_dir}/{bpid.lower()}*.jpg'))]
            for pic, img in lexamples.get(bpid, []):
                add_to_image_list(glist, pic, img)
            rexamples[bpid] = sorted(glist)

    for cat in bldata.other:
        for btype in cat[2]:
            if pic := btype[0]:
                cexamples[pic] = None
            if len(btype) > 2:
                for subtype in btype[2]:
                    if pic := subtype[0]:
                        cexamples[pic] = None

    mat_models = {x['matrix_model.base_id']: x for x in pif.dbh.fetch_matrix_model_blisters(bl_aliases.values())}
    for cat in cexamples:
        cexamples[cat] = cat_example(pif, cat, mat_models.get(bl_aliases.get(cat)))

    return pif.ren.format_template('blister.html', core=bldata.core, other=bldata.other,
                                   rexamples=rexamples, cexamples=cexamples)


def add_to_image_list(glist, pic, img):
    for ent in glist:
        if ent[0] == pic:
            break
    else:
        glist.append((pic, img))
        return
    c = 2
    while c:
        for ent in glist:
            if ent[0] == f'{pic}{c}':
                break
        else:
            glist.append((f'{pic}{c}', img))
            break
        c += 1


def cat_example(pif, pic, mat_model):
    if mat_model:
        pdir = mat_model['section.pic_dir'] or mat_model['page_info.pic_dir']
        pic = mat_model['matrix_model.base_id']
        img = pif.ren.find_image_path(pic, pdir=pdir, largest='m')
        if img:
            return img
    img = pif.ren.find_image_path(pic, pdir=pif.ren.pic_dir, largest='m')
    return img or None


# ----- boxart ---------------------------------------------------------


def box_lookup(col, val):
    return [box_lookups.get(col, {}).get(x, x) for x in val.split('/')]


def single_box(pif, mod, box):
    ign_cols = ['id', 'mod_id', 'pic_id', 'section_id']
    pic_name = f'x_{box.mod_id}-{box.box_type[0]}{box.pic_id}'.lower()
    pics = pif.ren.find_image_files(pic_name + '*')
    if mod:
        ostr = show_model(pif, mod)
    else:
        ostr = box.mod_id + '<br>'
    # ostr += pic_name + '<br>\n'
    for col in pif.dbh.get_table_data('box_type').columns:
        if col not in ign_cols and box.get(col):
            vals = [x.replace('\n', '<br>') for x in box_lookup(col, box.get(col))]
            ostr += (f"<b>{box_lookup(col, '_title')[0]}</b><ul>\n" +
                     ''.join([f"<li>{x}\n" for x in vals]) +
                     '</ul>\n')
    istr = pif.ren.format_image_selectable(pics, pic_name)
    if pif.is_allowed('ma'):
        istr = f'<a href="upload.cgi?d=.{config.IMG_DIR_BOX}&n={pic_name}.jpg">{istr}</a>'
        istr += '<br>' + pif.ren.format_button_link("edit", pif.dbh.get_editor_link('box_type', id=box.id))
    istr += '<center>' + pif.ren.format_image_selector(pics, pic_name) + '</center>'
    ent = {'inf': ostr, 'pic': istr}
    return ent


# need to add va, middle to eb_1 style


def get_box_image(pif, picroot, picsize=None, largest=mbdata.IMG_SIZ_PETITE, compact=False):
    if compact:
        product_image_path, product_image_file = pif.ren.find_image_file(picroot, prefix=picsize)
        pic = imglib.format_image_star(
            pif, product_image_path, product_image_file, target_x=mbdata.imagesizes[picsize][0])
    elif picsize:
        pic = pif.ren.format_image_required(picroot, prefix=picsize)
    else:
        pic = pif.ren.format_image_required(picroot, largest=largest)
    return pic


def show_model(pif, box, compact=False):
    img = '' if compact else pif.ren.format_image_required(
        box.mod.id, pdir=config.IMG_DIR_MAN, largest=mbdata.IMG_SIZ_SMALL)
    url = f"single.cgi?id={box.mod.id}"
    ostr = f'<center><a href="{url}">{box.id}<br>{img}<br>'
    ostr += f'<b>{box.mod.name}</b></a></center>'
    return ostr


def find_boxes(pif):
    series = pif.form.get_id('series')
    style = pif.form.get_id('style')
    style = '' if style == 'all' else style
    start = pif.form.get_int('start', 1)
    end = pif.form.get_int('end', start)

    boxes = dict()
    for box in pif.dbh.fetch_castings_by_box(series, style):
        manitem = pif.dbh.make_man_item(box)
        boxitem = pif.dbh.make_box_type_item(box)
        boxitem.mod = manitem
        boxitem.id = manitem.id
        man_no = int(manitem.id[2:4])  # specifically lesney boxes only
        if ((series and manitem.model_type != series) or
                (style and (style != boxitem.box_type[0])) or (man_no < start) or
                ((end and man_no > end) or (not end and man_no != start))):
            continue
        pic_name = f'x_{boxitem.mod_id}-{boxitem.box_type[0]}{boxitem.pic_id}'.lower()
        is_pic = int(os.path.exists(useful.relpath('.', config.IMG_DIR_BOX, pic_name + '.jpg')))
        sortid = manitem.id[2:4] + manitem.id[0:2] + manitem.id[4:] + boxitem.box_type[0]
        front = ' / '.join(
                box_lookup('box_type', boxitem.box_type) +
                box_lookup('bottom', boxitem.bottom) +
                box_lookup('additional_text', boxitem.additional_text) +
                [boxitem.notes])
        if sortid in boxes:
            boxes[sortid].count += 1
            boxes[sortid].pics += is_pic
            if front not in boxes[sortid].fronts:
                boxes[sortid].fronts.append(front)
            continue
        boxitem.count = 1
        boxitem.pics = is_pic
        boxitem.fronts = [front]
        boxes[sortid] = boxitem
    return boxes


def get_pic_roots(mod_id, box_style):
    return sorted(set([f'{mod_id}-{box_style}'.lower()] + [
        x[x.rfind('/') + 3:-4] for x in
        glob.glob(useful.relpath('.', config.IMG_DIR_BOX, f'[scm]_{mod_id}-{box_style}?.jpg'.lower()))]))


def show_single_box(pif):
    pif.ren.print_html()

    pif.ren.set_page_extra(pif.ren.image_selector_js)
    if pif.form.get_id('box'):
        boxes = pif.dbh.fetch_box_type(pif.form.get_id('box'))
    elif pif.form.get_id('mod'):
        boxes = pif.dbh.fetch_box_type_by_mod(pif.form.get_id('mod'), pif.form.get_id('ty'))
    if not boxes:
        raise useful.SimpleError("No matching boxes found.", status=404)
    boxes = pif.dbh.make_box_type_items(boxes)
    mod = pif.dbh.fetch_casting_by_id_or_alias(boxes[0].mod_id)
    for box in boxes:
        box.mod = pif.dbh.make_man_item(mod[0])
        box.id = box.mod.id

    lsection = render.Section(colist=['inf', 'pic'], headers={'inf': 'Box Information', 'pic': 'Box Picture'},
                              range=[render.Range(entry=[single_box(pif, box, x) for x in boxes])])
    llistix = render.Listix(section=[lsection])
    return pif.ren.format_template('simplelistix.html', llineup=llistix)


def show_boxes(pif):
    pif.ren.print_html()
    section = pif.dbh.fetch_section('lesney', 'boxart')
    verbose = pif.form.get_bool('verbose')
    style = pif.form.get_id('style')
    if style == 'all':
        style = ''
    headers = {'mod': 'Model', 'm': 'M', 'p': 'P', 's': 'S', 'box': 'Box'}
    columns = ['mod', 'm', 'p', 's'] if verbose else ['mod', 'box']

    boxes = find_boxes(pif)

    lrange = dict(note='', entry=list())
    boxids = sorted(boxes.keys())
    modids = sorted(list(set([x[:5] for x in boxids])))
    for mod_id in modids:
        mod_box_ids = [x for x in boxids if x.startswith(mod_id)]
        mod_box_ids.sort()
        ent = {'mod': {'txt': show_model(pif, boxes[mod_box_ids[0]], compact=False), 'rows': len(mod_box_ids)}}
        ent1 = ent
        for mod_box_id in mod_box_ids:
            mod = boxes[mod_box_id]
            # if verbose and pif.is_allowed('ma'):
            #     print('<br>'.join(mod['fronts']), '<hr>')
            box_style = mod.box_type[0]
            picroots = get_pic_roots(mod.mod.id, box_style)
            if verbose:
                ent1['mod']['txt'] += '<br>' + '<br>'.join(picroots)
            hdr = f"<b>{box_style} style</b>"
            if verbose:
                for picsize in 'mps':
                    imgs = '<br>'.join([get_box_image(pif, picroot, picsize, compact=False) for picroot in picroots])
                    ent[picsize] = {'txt': pif.ren.format_link(
                        f"?mod={mod.mod.id}&ty={box_style}", f"<center>{hdr}</center>{imgs}")}
                ent['s']['txt'] += f'<br>{mod.count}  box variations - {mod.pics} pics'
            else:
                pic = pif.ren.format_link(
                    f"?mod={mod.mod.id}&ty={box_style}",
                    ''.join([get_box_image(pif, picroot, largest='mmpss'[len(picroots)]) for picroot in picroots]))
                ent['box'] = {
                    'txt': f"<center>{hdr}<br>{pic}" +
                           f"<br>{mod.count} box variation{useful.plural(mod.count)}" +
                           (f" - {mod.pics} pics" if pif.is_allowed('ma') else '') +
                           '</center>'
                }
            lrange['entry'].append(ent)
            ent = dict(mod=None)
    lsection = render.Section(section=section, colist=columns, headers=headers, range=[lrange], note='')
    llistix = dict(section=[lsection])
    return pif.ren.format_template('boxes.html', llistix=llistix)


def show_boxes_compact(pif):
    pif.ren.print_html()
    page = pif.dbh.make_page_item(pif.dbh.fetch_page('boxart'))
    section = pif.dbh.make_sec_item(pif.dbh.fetch_section('lesney', 'boxart'))

    boxes = find_boxes(pif)

    lrange = render.Range()
    boxids = sorted(boxes.keys())
    modids = sorted(set([x[:5] for x in boxids]))
    for mod_id in modids:
        mod_box_ids = sorted([x for x in boxids if x.startswith(mod_id)])
        for mod_box_id in mod_box_ids:
            mod = boxes[mod_box_id]
            box_style = mod.box_type[0]
            picroots = get_pic_roots(mod.id, box_style)
            hdr = pif.ren.format_link(f"single.cgi?id={mod.mod.id}", f"{mod.id}")
            for picroot in picroots:
                pic = pif.ren.format_link(f"?mod={mod.id}&ty={box_style}", get_box_image(pif, picroot, picsize='s'))
                ent = render.Entry(text=f"<center><b>{hdr}</b><br>{pic}<br>{box_style} style</center>")
                lrange.entry.append(ent)
    lsection = render.Section(section=section, range=[lrange])
    blineup = render.Matrix(id=page.id, name=page.title, columns=section.columns, header='', footer='', section=[lsection])
    return pif.ren.format_template('simplematrix.html', llineup=blineup.prep())


def box_ask(pif):
    pif.ren.print_html()
    pif.ren.set_page_extra(pif.ren.reset_button_js)
    pif.ren.set_page_extra(pif.ren.increment_js)
    return pif.ren.format_template('boxes.html')


@basics.web_page
def box_main(pif):
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append('/cgi-bin/boxart.cgi', 'Lesney Era Boxes')
    if pif.form.get_id('box') or pif.form.get_id('mod'):
        return show_single_box(pif)
    elif pif.form.has('style'):
        if pif.form.get_bool('c'):
            return show_boxes_compact(pif)
        else:
            return show_boxes(pif)
    return box_ask(pif)


def count_boxes(pif):
    boxes = pif.dbh.fetch_castings_by_box('', '')
    box_styles = set()
    pr_count = im_count = 0
    for box in boxes:
        if 'alias.id' in box:
            box['id'] = box['alias.id']
        else:
            box['id'] = box['casting.id']

        if box['id'].startswith('M'):
            print(box)
            continue

        box_styles.add(box['id'] + '-' + box['box_type.box_type'])
        pr_count += 2
        im_count += len(glob.glob(useful.relpath(
            '.', config.IMG_DIR_BOX,
            'x_' + box['id'] + '-' + box['box_type.box_type'] + box['box_type.pic_id'] + '*.jpg')))

    for box in box_styles:
        if pif.ren.find_image_path(box, pdir=config.IMG_DIR_BOX, prefix=mbdata.IMG_SIZ_SMALL):
            im_count += 1
        if pif.ren.find_image_path(box, pdir=config.IMG_DIR_BOX, prefix=mbdata.IMG_SIZ_PETITE):
            im_count += 1
        if pif.ren.find_image_path(box, pdir=config.IMG_DIR_BOX, prefix=mbdata.IMG_SIZ_MEDIUM):
            im_count += 1
        pr_count += 1

    return pr_count, im_count


# ----- pub ------------------------------------------------------------

picdirs = {
    'PK': 'pic/pub/pkg',
    'PC': 'pic/pub/cat',
    'DC': 'pic/pub/cat',
    'RY': 'pic/pub/game',
    'PZ': 'pic/pub/game',
    'GM': 'pic/pub/game',
    'BK': 'pic/pub/book',
    'AD': 'pic/pub/ads',
    # blister
    # box
}


@basics.web_page
def publication(pif):
    pub_id = pif.form.get_id('id')
    pub_type = pif.form.get_id('ty')
    pif.ren.print_html()
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append('/cgi-bin/pub.cgi', 'Publications')
    pif.ren.set_button_comment(pif)

    if pub_id:
        pif.ren.hide_title = True
        return single_publication(pif, pub_id)
    elif pub_type:
        return publication_list(pif, pub_type)

    def fmt_link(sec):
        txt = mbmods.add_icons(pif, 'p_' + sec['id'], '', '')
        # if sec.id == 'ads':
        #     return pif.ren.format_link('ads.cgi', txt)
        return pif.ren.format_link('?ty=' + sec['category'], txt)

    return mbmods.make_page_list(pif, 'pub', fmt_link)


def get_section_by_model_type(pif, mtype):
    secs = pif.dbh.fetch_sections_by_page_type(mbdata.page_format_type['pub'], category=mtype)
    return secs[0] if secs else {}


def publication_list(pif, mtype):
    sec = get_section_by_model_type(pif, mtype)
    if not sec:
        raise useful.SimpleError("That publication type was not found.", status=404)
    if sec['id'] == 'ads':
        raise useful.Redirect('ads.cgi?title=' + pif.form.get_str('title'))
    sobj = pif.form.search('title')
    pif.ren.pic_dir = sec['page_info.pic_dir']
    pubs = pif.dbh.make_pub_items(pif.dbh.fetch_publications(model_type=mtype))

    def pub_ent(pub):
        ret = {'id': pub.id, 'country': pub.country, 'section_id': pub.section_id, 'isbn': pub.isbn,
               'first_year': pub.first_year}
        if not useful.search_match(sobj, pub.name):
            return None
        ret['name'] = f'<a href="pub.cgi?id={pub.id}">{pub.name}</a>'
        ret['description'] = useful.printablize(pub.description)
        if (os.path.exists(os.path.join(pif.ren.pic_dir, pub.id.lower() + '.jpg')) or
                glob.glob(os.path.join(pif.ren.pic_dir, '?_' + pub.id.lower() + '-*.jpg')) or
                glob.glob(os.path.join(pif.ren.pic_dir, '?_' + pub.id.lower() + '.jpg'))):
            ret['picture'] = mbdata.comment_icon['c']
        return ret

    if 1:
        entry = [pub_ent(pub) for pub in sorted(pubs, key=lambda x: (x.name, x.description))]
        hdrs = {'description': 'Description', 'first_year': 'Year', 'country': 'Country',
                'flags': 'Flags', 'model_type': 'Type', 'id': 'ID', 'name': 'Name', 'picture': ''}
        cols = ['picture', 'name', 'description', 'first_year', 'country']

        lrange = render.Range(entry=[x for x in entry if x], styles=dict(zip(cols, cols)))
        lsection = render.Section(colist=cols, headers=hdrs, range=[lrange], name=sec['name'])
        llistix = render.Listix(section=[lsection])
        return pif.ren.format_template('simplelistix.html', llineup=llistix)

    cols = 4

    def pub_text_link(pub):
        pic = pif.ren.fmt_img(pub.id, prefix='s')
        name = f'{pic}<br>{pub.name}' if pic else pub.name
        return render.Entry(text=pif.ren.format_link(f"makes.cgi?make={pub.id}", name))

    ents = [pub_text_link(pub_ent(x)) for x in pubs]
    llineup = render.Matrix(
        id='', columns=cols, section=[render.Section(columns=cols, range=[render.Range(entry=ents, id='makelist')])])

    return pif.ren.format_template('simplematrix.html', llineup=llineup.prep())


def make_relateds(pif, ref_id, pub_id, imgs):
    pic = imgs[0] if imgs else ''
    relateds = pif.dbh.fetch_casting_relateds(pub_id, section_id='pub')
    vs = pif.dbh.fetch_variation_selects_by_ref(ref_id, pub_id)
    vars = [x for x in vs if x['variation_select.mod_id'] == pub_id]

    def prep_related(related):
        pub_id = related['casting_related.related_id']
        name = related['base_id.rawname'].replace(';', ' ')
        descs = [x.get('variation.text_description', '') for x in vars] + related.get(
            'casting_related.description', '').split(';')
        imgid = [pub_id]
        for s in descs:
            if s.startswith('same as '):
                imgid.append(s[8:])
        descs = '<br>'.join([f'<div class="varentry">{x}</div>' for x in descs if x])

        img = pif.ren.format_image_required(
            imgid, made=not related['base_id.flags'] & config.FLAG_MODEL_NOT_MADE, pdir=config.IMG_DIR_MAN, vars=[
                x['variation_select.var_id'] for x in vars], largest=mbdata.IMG_SIZ_SMALL)
        img = f'<a href="single.cgi?id={pub_id}&dir={pif.ren.pic_dir}&pic={pic}&ref={ref_id}&sec={pub_id}">{img}</a>'

        return render.Entry(
            text=f'<span class="modelnumber">{pub_id}</span><br>\n{img}<br>\n<b>{name}</b>\n<br>{descs}\n')

    return [prep_related(x) for x in relateds]


def single_publication(pif, pub_id):
    man = pif.dbh.fetch_publication(pub_id)
    if not man:
        raise useful.SimpleError("That publication was not found.", status=404)
    man = man[0]
    pif.ren.pic_dir = picdirs.get(man['base_id.model_type'], pif.ren.pic_dir)
    # should just use man.section_id
    sec = get_section_by_model_type(pif, man['base_id.model_type'])
    # pif.set_page_info(sec.page_info.id)  # obviously not right but I don't know what is.
    man['casting_type'] = 'Publication'
    man['name'] = man['base_id.rawname'].replace(';', ' ')
    imgs = pub_images(pif, pub_id.lower())
    relateds = make_relateds(pif, 'pub.' + mbdata.model_type_names[man['base_id.model_type']].lower(), pub_id, imgs)

    left_bar_content = ''
    if pif.is_allowed('a'):  # pragma: no cover
        left_bar_content += f'<p><b><a href="{pif.dbh.get_editor_link("base_id", id=pub_id)}">Base ID</a><br>\n'
        left_bar_content += f'<a href="{pif.dbh.get_editor_link("publication", id=pub_id)}">Publication</a><br>\n'
        left_bar_content += f'<a href="traverse.cgi?d={pif.ren.lib_dir}">Library</a><br>\n'
        left_bar_content += f'<a href="upload.cgi?d={pif.ren.lib_dir}&n={pub_id}&c={pub_id}">Product Upload</a><br>\n'

    upper_box = ''
    if imgs:
        upper_box += pif.ren.format_image_link_image(imgs[0], link_largest=mbdata.IMG_SIZ_HUGE)
    # else:
    #     upper_box += pif.ren.format_image_link_image(img, link_largest=mbdata.IMG_SIZ_LARGE)
    if man['base_id.description']:
        upper_box += '<br>' if upper_box else ''
        upper_box += useful.printablize(man['base_id.description'])

    lran = [render.Range(
        id='ran',
        entry=[render.Entry(text=pif.ren.format_image_link_image(img[img.rfind('/') + 1:]))
               for img in sorted(imgs)] if imgs else [render.Entry(text=pif.ren.format_image_link_image(pub_id))]
    ) if len(imgs) > 1 else render.Range()]
    if relateds:
        lran.append(render.Range(id='related', entry=relateds, name='Related Models'))
    llineup = render.Matrix(id=pub_id, section=[render.Section(id='sec', range=lran, columns=4)], columns=4)

    pif.ren.set_button_comment(pif, f'id={pub_id}')
    llineup.dump()

    left_bar_icons = [pif.ren.format_image_icon('p_' + sec['id'])]

    context = {
        'title': man['name'],
        'note': '',
        'type_id': 'p_' + sec['id'],
        'icon_id': pub_id,
        'vehicle_type': '',
        'rowspan': 5 if upper_box else 4,
        'left_bar_icons': left_bar_icons,
        'left_bar_content': left_bar_content,
        'upper_box': upper_box,
        'llineup': llineup.prep(),
    }
    return pif.ren.format_template('pub.html', **context)


def pub_images(pif, pub_id):
    imgs = glob.glob(os.path.join(pif.ren.pic_dir, '?_' + pub_id + '-*.jpg'))
    imgs = list(set([os.path.split(fn)[1][2:-4] for fn in imgs]))
    if (os.path.exists(os.path.join(pif.ren.pic_dir, pub_id + '.jpg')) or
            glob.glob(os.path.join(pif.ren.pic_dir, '?_' + pub_id + '.jpg'))):
        imgs.insert(0, pub_id)
    imgs.sort()
    return imgs


# ----- advertising ---- the special snowflake -------------------------


@basics.web_page
def ads_main(pif):
    pif.ren.print_html()
    pif.ren.hierarchy_append('/', 'Home')
    pif.ren.hierarchy_append('/database.php', 'Database')
    pif.ren.hierarchy_append('/cgi-bin/ads.cgi', 'Advertisements')
    pif.ren.set_button_comment(pif)
    pic_dir = pif.ren.pic_dir
    lib_dir = pif.ren.lib_dir
    ranges = []
    sobj = pif.form.search('title')

    def fmt_cy(ent):
        cy = ent.get('country', '')
        cyflag = pif.ren.show_flag(cy) if (cy and cy != 'US') else ''
        cyflag = (' <img src="' + cyflag[1] + '">') if cyflag else ''
        return cy, cyflag

    def fmt_vid(ent):
        # sep = pif.ren.format_image_art('wheel.gif', also={'class': 'dlm'})
        # add country
        cy, cyflag = fmt_cy(ent)
        cmt = ent['description']
        ostr = pif.ren.format_link(ent['url'], ent['name'])
        if cmt:
            ostr += ' ' + cmt
        ostr += cyflag
        if pif.is_allowed('ma'):
            ostr += ' ' + pif.ren.format_link(f'edlinks.cgi?id={ent["id"]}', pif.ren.fmt_edit())
        return ostr

    # id page_id section_id display_order flags associated_link last_status link_type country url name description note
    vlinks = [fmt_vid(x) for x in pif.dbh.depref(
        'link_line', pif.dbh.fetch_link_lines(page_id='links.others', section='Lvideoads', order='name'))
        if useful.search_match(sobj, x['name'])]

    def fmt_pub(ent, pdir=None):
        pdir = pdir if pdir else pic_dir
        ldir = pdir.replace('pic', 'lib')
        # ent: id, description, country, first_year, model_type
        cy, post = fmt_cy(ent)
        _, floc = pif.ren.find_image_file(ent['id'], largest='e', pdir=pdir)
        _, lloc = pif.ren.find_image_file(ent['id'], largest='e', pdir=ldir)
        # floc = pdir + '/' + ent['id'] + '.jpg'
        # lloc = floc.replace('/pic/', '/lib/')
        if floc:
            if ent['model_type']:
                url = 'pub.cgi?id=' + ent['id']
            else:
                url = '/' + pdir + '/' + floc
        else:
            url = '/' + ldir + '/' + lloc
        if not useful.search_match(sobj, ent['description']):
            return ''
        name = useful.printablize(ent['description'])
        if ent['first_year']:
            name += ' (' + ent['first_year'] + ')'
        if pif.is_allowed('ma'):
            if ent['model_type']:
                post += ' ' + pif.ren.format_link(
                    pif.dbh.get_editor_link('publication', id=ent['id']), pif.ren.fmt_edit())
            else:
                post += ' ' + pif.ren.format_link(
                    '/cgi-bin/mass.cgi?tymass=ads&id=%s&description=%s&year=%s&country=%s' % (
                        ent['id'], useful.url_quote(ent['description'], plus=True), ent['first_year'], cy),
                    pif.ren.fmt_square(hollow=True))
            if floc:
                post += ' ' + pif.ren.format_link(
                    '/cgi-bin/imawidget.cgi?d=%s&f=%s' % (pdir, floc), pif.ren.fmt_mini(icon='paintbrush'))
            elif lloc:
                post += ' ' + pif.ren.format_link(
                    '/cgi-bin/imawidget.cgi?d=%s&f=%s' % (ldir, lloc), pif.ren.fmt_mini(icon='paintbrush'))
            post += ' ' + pif.ren.format_link(
                '/cgi-bin/upload.cgi?d=%s&n=%s' % (ldir, ent['id']), pif.ren.fmt_mini(icon='upload'))
            name = ent['id'] + ' - ' + name
        if floc:
            return pif.ren.format_link(url, name) + post
        return name + post

    fields = {
        'id': 'base_id.id',
        'description': 'base_id.description',
        'first_year': 'base_id.first_year',
        'country': 'publication.country',
        'model_type': 'base_id.model_type',
        'rawname': 'base_id.rawname',
    }

    def mangle_object(x):
        return {y: x[fields[y]] for y in fields}

    links = {x['base_id.id']: mangle_object(x)
             for x in pif.dbh.fetch_publications(model_type='AD', order='base_id.first_year,base_id.id')}
    pic_ims = ad_images(pic_dir)
    missing_pics = sorted(set(links.keys()) - set(pic_ims))
    lib_ims = sorted(set(ad_images(lib_dir)) - set(links.keys()))
    pic_ims = sorted(set(pic_ims) - set(links.keys()))
    list_ents = {ent[0]: dict(itertools.zip_longest(['id', 'description', 'first_year', 'country', 'model_type'], ent))
                 for ent in [x.strip().split('|') for x in open(pic_dir + '/list.dat').readlines()]}
    list_ids = sorted(set(list_ents.keys()) - set(links.keys()))
    link_ids = sorted(set(links.keys()) - set(missing_pics), key=lambda x: (links[x]['first_year'], links[x]['id']))

    ranges.append(render.Range(entry=[fmt_pub(links[x]) for x in link_ids]))

    plinks = [fmt_pub(list_ents[lid]) for lid in list_ids]
    if plinks:
        ranges.append(render.Range(name='More information is needed on these (year, location).',
                      entry=plinks))

    if pif.is_allowed('ma'):
        plinks = [fmt_pub({'id': ent, 'description': ent, 'first_year': '', 'model_type': ''}, lib_dir)
                  for ent in lib_ims]
        if plinks:
            ranges.append(render.Range(name='<i>Nonpublished ads</i>', entry=plinks))

        missing = [fmt_pub(links[pic_id]) for pic_id in missing_pics]
        if missing:
            ranges.append(render.Range(name='<i>Database entries missing pictures</i>', entry=missing))

    pif.ren.set_footer(pif.ren.format_button_link('back', '/') + ' to the index.')
    if pif.is_allowed('ma'):
        pif.ren.set_footer(
            pif.ren.format_link(f'/cgi-bin/upload.cgi?d={lib_dir}', 'Upload new ad') + ' - ' +
            pif.ren.format_link('/cgi-bin/edlinks.cgi?page_id=links.others&sec=Lvideoads&add=1', 'Add new video'))
    llineup = render.Listix(section=[
        render.Section(id='print', name='Print Advertising', range=ranges),
        render.Section(id='video', name='Video Advertising', range=[render.Range(entry=vlinks)]),
    ])
    return pif.ren.format_template('simpleulist.html', llineup=llineup)


def ad_images(pdir):
    def mangle_name(x):
        x = x[x.rfind('/') + 1:-4]
        return x[2:] if x[1] == '_' else x

    return [mangle_name(x) for x in glob.glob(pdir + '/*.jpg')]


# ----- command line ---------------------------------------------------


def check_boxes(pif):
    boxes = find_boxes(pif)

    for key in sorted(boxes.keys()):
        for picroot in get_pic_roots(boxes[key]['id'], boxes[key]['box_type.box_type'][0]):
            print('%-9s' % picroot,)
            for picsize in 'mcs':
                img = pif.ren.find_image_path(picroot, prefix=picsize + '_', pdir=config.IMG_DIR_BOX)
                if not img:
                    print('.',)
                else:
                    imginf = imglib.img_info(img)
                    if imginf[1] < mbdata.imagesizes[picsize][0]:
                        print(picsize,)
                    else:
                        print(picsize.upper(),)
            print()

    check_database(pif)


def check_database(pif):
    count = 0
    fields = {}
    d = pif.dbh.fetch('box_type')
    for e in d:
        x = ('.' + config.IMG_DIR_BOX + '/x_' + e['box_type.mod_id'] + '-' +
             e['box_type.box_type'][0] + e['box_type.pic_id'] + '.jpg')
        count += int(os.path.exists(x.lower()))
        for f in e:
            if e[f] and f[9:] not in ('notes', 'year', 'id', 'pic_id', 'mod_id', 'model_name'):
                fields.setdefault(f[9:], set())
                fields[f[9:]].update(e[f].split('/'))
                for h in e[f].split('/'):
                    if h not in box_lookups[f[9:]]:
                        print(h, e[f], f, e['box_type.id'])
    for f in fields:
        s1 = fields[f] - set(box_lookups[f].keys())
        s2 = set(box_lookups[f].keys()) - fields[f] - {'_title'}
        if s1 or s2:
            print(f, s1, s2)
    print('x-pics', count, 'of', len(d))


def dump_database(pif):
    cols = ['id', 'pic', 'box_size', 'year', 'additional_text', 'bottom', 'sides', 'end_flap', 'model_name', 'notes']
    titles = {
        'id': 'id',
        'mod_id': 'mod_id',
        'box_type': 'typ',
        'pic_id': 'p',
        'pic': 'pic',
        'box_size': 'z',
        'year': 'year',
        'additional_text': 'addl_text',
        'bottom': 'bottom',
        'sides': 'sides',
        'end_flap': 'end_flap',
        'model_name': 'model_name',
        'notes': 'notes',
    }
    db = pif.dbh.depref('box_type', pif.dbh.fetch('box_type'))
    lens = {col: 0 for col in cols}
    for row in db:
        row['pic'] = '%s-%s%s' % (row['mod_id'], row['box_type'][0], row['pic_id'])
        for col in cols[1:]:
            lens[col] = max(lens[col], len(row[col]))
    lens['id'] = 4
    # id | mod_id | typ | p | z | year | addl_text | bottom | sides | end_flap | model_name | notes
    print(' | '.join([('%%-%ds' % lens[col]) % titles[col] for col in cols]))
    for row in db:
        print(' | '.join([('%%-%ds' % lens[col]) % row[col] for col in cols]).strip())


# saving for later
# select id, mod_id, box_type as typ, pic_id as p, box_size as z, year, additional_text as addl_text, bottom, sides,
# end_flap, model_name, notes from box_type;


def blister_things(pif):
    dblist = bfiles.SimpleFile(useful.relpath(config.SRC_DIR, 'blister.dat'))
    for llist in dblist:
        if llist[0] == 'm':
            if llist[1].endswith('p'):
                print(llist[3])


cmds = [
    ('c', check_boxes, "check boxes"),
    ('d', dump_database, "dump database"),
    ('b', blister_things, "blister things"),
]


# ----- ----------------------------------------------------------------


if __name__ == '__main__':  # pragma: no cover
    basics.process_command_list(cmds=cmds, dbedit='')
