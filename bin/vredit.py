#!/usr/local/bin/python
# -*- coding: latin-1 -*-

import basics
import config
import editor
import mbdata
import render
import useful
import varias

var_record_cols = ['var', 'body', 'base', 'windows', 'interior', 'deco', 'deco_type', 'wheels',
                   'area', 'date', 'note', 'manufacture', 'additional_text']


def show_details(pif, mod):
    mod_id = mod['id']

    fvars = {varitem.var: varitem for varitem in [
        varias.mangle_variation(pif, pif.dbh.make_var_item(*x), {}) for x in pif.dbh.fetch_variations_deconstructed(mod_id)]}

    dbattrs = pif.dbh.depref('attribute', pif.dbh.fetch_attributes(mod_id, with_global=True))
    attrs = ['var', 'body', 'base', 'windows', 'interior', 'deco', 'deco_type', 'wheels']
    for x in dbattrs:
        if x['attribute_name'] not in attrs:
            attrs.append(x['attribute_name'])

    def attr_edit(v, x):
        return f'{v.get_attr(x, "")}<br>' + (
            pif.form.put_select(f'{v.var}.{x}', mbdata.deco_types, selected=v.get_attr(x, '')) if x == 'deco_type' else
            pif.form.put_hidden_input({f'{v.var}.var': v.var}) if x == 'var' else
            pif.form.put_text_input(f'{v.var}.{x}', 128, 20, v.get_attr(x, '')) if x == 'deco' else
            pif.form.put_text_input(f'{v.var}.{x}', 80, 10, v.get_attr(x, '')))

    return render.Section(
        header=f'<h3>Details ({len(fvars)})</h3><form action="vars.cgi">', colist=attrs,
        footer=f"{pif.form.put_button_input('save', 'save details')}{pif.form.put_hidden_input(mod=mod_id)}</form>",
        range=[render.Range(id='ran', entry=[{x: attr_edit(v, x) for x in attrs} for var_id, v in sorted(fvars.items())])])

# mbdata.ListType.ADMIN listix
# the old stuff could do searching so we might think about it here
# def do_model_editor(pif, manitem, vsform, dvars, photogs):
#     attrs = ['var'] + [x['attribute_name'] for x in vsform.attr_recs]
#
#     def attr_edit(v, x):
#         return v.get_attr(x, '') + '<br>' + pif.form.put_text_input(v.var + '.' + x, 80, 16, v.get_attr(x, ''))
#
#     lran = render.Range(
#         id='ran', entry=[{x: attr_edit(v, x) for x in attrs} for var_id, v in sorted(dvars.items())])
#
#     return render.Listix(
#         id='vars',
#         footer=(related_casting_links(pif, manitem.id, url="vars.cgi?vdt=1&mod=") +
#                 pif.form.put_button_input('save') + pif.form.put_hidden_input(mod=manitem.id) + '</form>'),
#         section=[render.Section(
#             id='ed', name='All Models', colist=attrs, header='<form action="vars.cgi">',
#             count=f'{len(lran.entry)} entries' if len(lran.entry) > 1 else '1 entry', range=[lran])])


def show_attrs(pif, mod, hdrs, var_desc):
    mod_id = mod['id']
    attrs = pif.dbh.depref('attribute', pif.dbh.fetch_attributes(mod_id))
    common_attrs = pif.dbh.depref('attribute', pif.dbh.fetch_attributes(''))
    visual_base = bool(mod['flags'] & config.FLAG_MODEL_BASEPLATE_VISIBLE)
    dets = pif.dbh.fetch_details(mod_id, "").get('', {})
    dets = pif.dbh.depref('detail', dets)
    table_data = pif.dbh.get_table_data('variation')

    entries = []
    for attr in attrs:
        attr_id = attr['id']
        entries.append({
            'id': f'<a href="{pif.dbh.get_editor_link("attribute", id=attr_id)}">{attr_id}</a></td>',
            'name': pif.form.put_text_input(f"attribute_name.{attr_id}", 16, 16, attr["attribute_name"]),
            'def': pif.form.put_text_input(f"definition.{attr_id}", 12, 12, attr["definition"]),
            'title': pif.form.put_text_input(f"title.{attr_id}", 32, 32, attr["title"]),
            'v': pif.form.put_checkbox(f"visual.{attr_id}", [(1, '')], [attr['visual']]),
            'default': pif.form.put_text_input(f"description.{attr_id}", 64, 32, dets.get(attr["attribute_name"], "")),
            'buttons':
                pif.form.put_button_input(bname="save", name=f'renattr.{attr_id}') +
                pif.ren.format_button_link("delete", f"?delattr={attr_id}")
        })
        var_desc[attr["attribute_name"]] = attr["definition"]

    for attr in common_attrs:
        attr_id = attr['id']
        entries.append({
            'id': f'<a href="{pif.dbh.get_editor_link("attribute", id=attr_id)}">{attr_id}</a></td>',
            'name':
                attr["attribute_name"] + pif.form.put_hidden_input(**{f"attribute_name.{attr_id}": attr["attribute_name"]}),
            'def': attr["definition"],
            'title': table_data.title[attr["attribute_name"]],
            'v':
                pif.form.put_checkbox("visualbase", [(1, '')], [1 if visual_base else 0])
                if attr['attribute_name'] == 'base' else 'X' if attr['visual'] else '',
            'default':
                pif.form.put_text_input(f"description.{attr_id}", 64, 32, dets.get(attr["attribute_name"], "")),
            'buttons':
                pif.form.put_button_input(bname="save", name=f'renattr.{attr_id}') +
                pif.ren.format_link(
                    '/cgi-bin/vedit.cgi', txt=pif.form.put_text_button("none"),
                    args={f'attribute_name.{attr_id}': attr['attribute_name'], 'd': 'src/mbxf',
                          f'description.{attr_id}': 'none', 'f': 'unset', 'm': mod_id, 'mod_id': mod_id,
                          f'renattr.{attr_id}': 'SAVE'})
        })

    return render.Section(
        colist=['id', 'name', 'def', 'title', 'v', 'default', 'buttons'],
        range=[render.Range(entry=entries)],
        header=f'<h3>Attributes</h3><form method="post">{pif.create_token()}\n'
               '<input type="hidden" name="mod_id" value="{mod_id}">',
        headers={'id': 'ID', 'name': 'Name', 'def': 'Defintion', 'title': 'Title',
                 'v': 'V', 'default': 'Default', 'buttons': ''})


def show_base_id(pif, mod):
    return render.Section(
        colist=['column', 'new value'], noheaders=True,
        range=[render.Range(entry=editor.make_form_fields(pif, pif.dbh.get_table_data('base_id'), mod, maxwidth=80))],
        header=f'<h3>Base ID</h3>\n<form method="post" name="base_id">\n{pif.create_token()}',
        footer=f"{pif.form.put_button_input('save', 'save base id')}</form>")


def show_casting(pif, mod):
    fmt_invalid, messages, missing = pif.dbh.check_description_formatting(mod['id'], linesep='<br>')
    return render.Section(
        colist=['column', 'new value'], noheaders=True,
        range=[render.Range(entry=editor.make_form_fields(pif, pif.dbh.get_table_data('casting'), mod, maxwidth=128))],
        header=f'<h3>Casting</h3><form method="post" name="casting">{pif.create_token()}',
        footer=f"{pif.form.put_button_input('save', 'save casting')}</form>\n{messages if fmt_invalid else ''}")


@basics.web_page
def handle_form(pif):
    if not pif.is_allowed('a'):
        raise useful.SimpleError('Not authorized.', status=401)
    pif.ren.print_html()
    mod_id = pif.form.get_raw('m') or pif.form.get_raw('mod_id')
    pif.ren.title = mod_id
    pif.dbh.set_verbose(True)

    header = 'duplicate form submission detected' if pif.duplicate_form else do_action(pif, mod_id)
    mod = pif.dbh.fetch_casting(mod_id, extras=True)
    if not mod:
        if mod := pif.dbh.fetch_alias(mod_id):
            mod = pif.dbh.depref('alias', mod)
            mod['id'] = mod['ref_id']
        else:
            raise useful.SimpleError('That casting cannot be found.', status=404)
    mod = pif.dbh.depref('casting,base_id', mod)
    mod_id = mod['id']
    attrs = pif.dbh.fetch_attributes(mod_id)
    attr_names = var_record_cols + [x['attribute.attribute_name'] for x in attrs]
    var_desc = dict([(x['field'], x['type']) for x in pif.dbh.describe_dict('variation').values()])

    header += f'<i id="{mod_id}"></i>'
    header += f'<br><center><h2><a href="single.cgi?id={mod_id}">{mod_id}</a>'
    header += f"<h3>{mod.get('rawname', 'no rawname?')}</h3></center>"
    header += pif.ren.format_image_optional(mod_id, largest=mbdata.IMG_SIZ_MEDIUM,
                                            pdir='pic/man', also={'align': 'right'})
    header += "<br>"

    sections = [
        show_base_id(pif, mod),
        show_casting(pif, mod),
        show_attrs(pif, mod, attr_names, var_desc),
        show_details(pif, mod),
    ]

    return pif.ren.format_template('simplelistix.html', llineup=render.Listix(section=sections, header=header))


def save_attribute(pif, attr_id, mod_id):
    attr = pif.dbh.fetch_attribute(attr_id)
    attr = pif.dbh.depref('attribute', attr)
    ostr = f"save_attribute {pif.form.get_form()} {attr_id} {attr}<br>"
    if len(attr) == 1:
        attr = attr[0]
        if attr_id > 4:
            for key in attr:
                if pif.form.has(f'{key}.{attr_id}'):
                    attr[key] = pif.form.get_raw(f'{key}.{attr_id}')
            pif.dbh.update_attribute(attr, attr_id)

        if pif.form.get_raw(f"description.{attr_id}") != "":
            rec = {"mod_id": mod_id, "var_id": "", "attr_id": attr_id,
                   "description": pif.form.get_raw(f"description.{attr_id}")}
            where = {"mod_id": mod_id, "var_id": "", "attr_id": attr_id}
            ostr += f'detail {rec} {where} {pif.dbh.write("detail", rec, where)}<br>\n'
        if attr_id == 1:
            pif.dbh.update_flag_sets(
                'base_id', mask=config.FLAG_MODEL_BASEPLATE_VISIBLE, enable=pif.form.get_bool("visualbase"),
                where=f'id="{mod_id}"')
    else:
        ostr += f'{len(attr)} attributes returned!'
    return ostr


def do_action(pif, mod_id):
    # useful.write_message(f'{pif.form.get_form()}<br>\n')
    ostr = ''  # f'{pif.form.get_form()}<br>\n'
    if pif.form.has("save_base_id"):
        ostr += "save base_id<br>\n"
        rec = {k: sum(int(x, 16) for x in pif.form.get_list('base_id.flags')) if k == 'flags' else v
               for k, v in pif.form.get_dict(start='base_id.', raw=True).items()}
        ostr += str(pif.dbh.write("base_id", rec, {"id": rec["id"]}, tag='VREbaseid', modonly=True))
    elif pif.form.has("save_casting"):
        ostr += "save casting<br>"
        table_data = pif.dbh.get_table_data('casting')
        rec = {x: pif.form.get_raw(x) for x in table_data.columns + table_data.extra_columns if x in pif.form}
        pif.dbh.write("casting", rec, {"id": rec['id']}, tag='VREcasting', modonly=True)
        pif.dbh.recalc_description(rec['id'])
    elif pif.form.has("save_details"):
        ostr += "save details<br>"
        varias.save_model(pif, mod_id)
    elif pif.form.find('renattr'):
        for key in pif.form.find('renattr'):
            attr_id = int(key[8:])
            ostr += f"renattr {attr_id}<br>"
            ostr += str(save_attribute(pif, attr_id, mod_id)) + '<br>'
        pif.dbh.recalc_description(mod_id)
    elif pif.form.has("delattr"):
        ostr += "delattr<br>"
        ostr += str(pif.dbh.delete_attribute({'id': pif.form.get_raw('delattr')})) + '<br>'
        ostr += str(pif.dbh.delete_detail({'attr_id': pif.form.get_raw('delattr')})) + '<br>'
    return ostr
