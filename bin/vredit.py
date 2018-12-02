#!/usr/local/bin/python
# -*- coding: latin-1 -*-

"""Variation Importer

This module (with vrdata) imports variations from the Word files
that are kept on mbxforum.nl.

This was grown over the course of several years, and at this point
I'm not completely sure how it works.  If you go forward from here
and try to understand it, I take no responsibility for your sanity.

Everything happens in two contexts: doing the index, and doing the
individual model editor.  So you'll see very similar looking functions
in some cases.

Good luck.
"""

import glob, itertools, os, re, sys, time

import basics
import config
import mbdata
import tables
import useful
import varias
import vrdata

IS_GOOD = 0
IS_NO_MODEL = 1
IS_DIFFERENT_NUMBER = 2
IS_CHANGED_SCHEMA = 3
IS_CHANGED = 4
IS_INVALID = 5
IS_NEW_VAR = 6

file_list_class = {
    IS_GOOD: 'good',
    IS_CHANGED_SCHEMA: 'changed_schema',
    IS_CHANGED: 'changed',
    IS_INVALID: 'changed',
    IS_NEW_VAR: 'changed',
    IS_NO_MODEL: 'no_model',
    IS_DIFFERENT_NUMBER: 'different',
}

var_record_cols = ['var', 'body', 'base', 'windows', 'interior', 'area', 'date', 'note', 'manufacture', 'base_text',
                   'imported_from', 'imported_var']


# ----- general helpers ------------------------------------------------


def parse_file(pif, vid, fdir, fn, args=''):
    modids, fitabs = read_file(pif, vid, fdir, fn)
    if not modids:
	modids = [pif.form.get_str('m')]
    varfile = {
        'filename': fn,
        'stat': {IS_GOOD},
        'modids': [x for x in modids],
        'tabs': list(),
        'var_lup': dict(),
    }

    mod = dict()

    def make_fitab():
	return {
            'stat': set(),
            'is_valid': False,
            'modid': '',
            'preface': '',
            'filehead': [],
            'gridhead': [],
            'body': list(),
            'epilog': '',
            'dbvars': [],
            'attrs': [],
            'casting': {},
	    'attr_names': [],
        }
    if not fitabs:
	fitab = make_fitab()
        varfile['tabs'].append(fitab)
        mn = modids.pop(0)
	get_casting_info(pif, mn, mod, fitab)
        fitab['gridhead'] = fitab['attr_names']
        for row in fitab['dbvars']:
	    if fitab['dbvars'][row]['imported_from'] == fn:
		fitab['body'].append(fitab['dbvars'][row])
	return varfile
    if not modids:
        varfile['stat'].add(IS_NO_MODEL)
	print 'no model<br>'
        return varfile

    for arg in args.split(' '):
        if '=' in arg:
            ovar, nvar = arg.split('=')
            varfile['var_lup'][ovar] = nvar

    for rawfitab in fitabs:
	fitab = make_fitab()
        varfile['tabs'].append(fitab)

        if not rawfitab:
            fitab['stat'].add(IS_NO_MODEL)
            continue
        fitab['preface'] = rawfitab[0].strip()
        if len(rawfitab) < 2 or not len(rawfitab[1]):
            fitab['stat'].add(IS_NO_MODEL)
            continue
        modtab = rawfitab[1]
        if len(rawfitab) > 2:
            fitab['epilog'] = rawfitab[2]

        hdrs = [vid.transform_header(x) for x in modtab[0]]
        if hdrs[0] != 'var' or fitab['preface'].find("BOX TYPES") >= 0:
            fitab['stat'].add(IS_NO_MODEL)
            fitab['body'] = modtab
            continue
        fitab['filehead'] = hdrs
        fitab['is_valid'] = True
        num_file_hdrs = len(hdrs)  # not including imported_from
        hdrs.append('imported_from')
        fitab['gridhead'] = nhdrs = vid.header_column_change(fn, hdrs)

        mn = modids.pop(0)

	get_casting_info(pif, mn, mod, fitab)

        for hdr in nhdrs:
            if hdr not in fitab['attr_names']:
                varfile['stat'].add(IS_CHANGED_SCHEMA)

        for row in modtab[1:]:
            row = vid.transform_row(row)
            if not reduce(lambda x, y: x or bool(y), row[1:], False):
                continue
            rowd = dict(itertools.izip_longest(hdrs, row, fillvalue=""))
            nrow = vid.row_column_change(fn, rowd)
	    nrow['var'] = mbdata.normalize_var_id(fitab['casting'], nrow['var'])
            if nrow.get('is_valid'):
                fitab['body'].append(nrow)

    return varfile


def get_casting_info(pif, mn, mod, fitab):
    fitab['modid'] = mn
    mod = get_model_rec(pif, mn)
    fitab['casting'] = mod
    if not mod:
	fitab['stat'].add(IS_NO_MODEL)
    else:
	fitab['attrs'] = pif.dbh.fetch_attributes(mod['id'])
	fitab['attr_names'] = var_record_cols + [x['attribute.attribute_name'] for x in fitab['attrs']]

	varis = pif.dbh.fetch_variations(mod['id'], nodefaults=True)
	varis = pif.dbh.depref('variation', varis)
	dbvars = {x['var']: x for x in varis}
	fitab['dbvars'] = dbvars



def read_file(pif, vid, fdir, fn):
    modids, fitabs = list(), list()
    if os.path.exists(fdir + '/' + fn + '.html'):
        modids, fitabs = read_html_file(pif, vid, fdir, fn)
    elif os.path.exists(fdir + '/' + fn + '.htm'):
        modids, fitabs = read_html_file(pif, vid, fdir, fn)
    elif os.path.exists(fdir + '/' + fn + '.dat'):
        modids, fitabs = read_dat_file(pif, vid, fdir, fn)
    return modids, fitabs


def read_html_file(pif, vid, fdir, fn):
    modids = vid.get_model_ids(fn)
    fitabs = list(), ''
    if not modids:
        pass
    elif os.path.exists(fdir + '/' + fn + '.html'):
        fitabs = vrdata.get_html_tables(fdir + '/' + fn + '.html')
    elif os.path.exists(fdir + '/' + fn + '.htm'):
        fitabs = vrdata.get_html_tables(fdir + '/' + fn + '.htm')
    return modids, fitabs


def read_dat_file(pif, vid, fdir, fn):
    fn = fdir + '/' + fn + '.dat'
    modids = list()
    fitabs = list()
    fitab = list()
    fidesc = ''
    for ln in open(fn).readlines():
        ln = ln.strip()
        if not ln:
            continue
        if ln[0] == '#':
            continue
        ln = ln.split('|')
        if ln[0] == 't':
            if fitab:
                fitabs.append((fidesc, fitab))
            ln = ln + ['', '', '']
            modids.append(ln[1])
            fidesc = 'Name: %s\nYear: %s\n' % (ln[2].title(), ln[3])
            fitab = list()
        else:
            fitab.append(ln[1:])
    if fitab:
        fitabs.append((fidesc, fitab))
    return modids, fitabs


def show_file_link(fn, ft, show_as):
    fp = os.path.join('src/mbxf', fn + '.' + ft.lower())
    if os.path.exists(fp):
        print '<a href="/%s">%s</a>' % (fp, show_as)


def get_model_rec(pif, mn):
    modrec = pif.dbh.fetch_casting(mn, extras=True)
    modrec = pif.dbh.depref('casting', modrec)

    #debug("fetch_casting", mn, modrec)
    if not modrec:
        modrec = pif.dbh.fetch_alias(mn)
        #debug("fetch_alias", mn, modrec)
        if modrec:
            modrec = pif.dbh.depref('alias', modrec)
            modrec = pif.dbh.depref('casting', modrec)
            modrec = pif.dbh.depref('base_id', modrec)
            modrec['id'] = modrec['ref_id']

    #debug('GetModRec', modrec)
    return modrec


def check_row(dbrow, firow, fihdrs):
    #pif.render.comment("db", dbrow)
    for hdr in fihdrs:
        dbdet = str(dbrow.get(hdr, ''))
        fidet = firow.get(hdr, '')
        if hdr == 'var':
            continue  # doesn't figure in
        elif dbdet != fidet:
            #pif.render.comment('#', hdr, ':', dbdet, '|', fidet)
            return False
        #pif.render.comment('=', hdr, ':', dbdet, '|', fidet)
    #pif.render.comment("match found")
    return True


def find_record(fn, dbvars, firow, fihdrs):
    # match up to existing record
    #pif.render.comment("fh", fihdrs)
    #pif.render.comment("fi", firow)
    for dbvar in dbvars:
        imported_var = dbvars[dbvar].get('imported_var', dbvars[dbvar]['var'])
        if dbvars[dbvar].get('imported_from', '') == fn and imported_var == firow['var']:
            return dbvars[dbvar]
    for dbvar in dbvars:
        if check_row(dbvars[dbvar], firow, fihdrs):
            return dbvars[dbvar]
    return dict()


# ----- overview functions ---------------------------------------------


def check_file(pif, vid, fdir, fn):
    varfile = parse_file(pif, vid, fdir, fn)

    for fitab in varfile['tabs']:
        if not fitab.get('is_valid'):
            continue
        for row in fitab['body']:
            dbvar = find_record(fn, fitab['dbvars'], row, fitab['gridhead'])
            if dbvar:
                for col in fitab['gridhead']:
                    if col != 'var' and row.get(col, '') != dbvar.get(col, ''):
                        #pif.render.comment('changed', col, row.get(col, ''), dbvar.get(col, ''))
                        varfile['stat'].add(IS_CHANGED)
		if not vrdata.compare_var_ids(dbvar['var'], row['var']) and row['var'][0] != 'f':
                #if dbvar['var'] != row['var'] and row['var'][0] != 'f':
                    #pif.render.comment('diff#', dbvar['var'], row['var'])
                    varfile['stat'].add(IS_DIFFERENT_NUMBER)
            else:
                varfile['stat'].add(IS_NEW_VAR)
                break

    return varfile


def get_file_list(fdir):
    dats = list()
    for ext in ['htm', 'html', 'dat']:
        dats += [x[x.rfind('/') + 1:x.rfind('.')] for x in glob.glob(fdir + '/*.' + ext)]
    dats = list(set(dats))
    dats.sort()
    return dats


# ff: 0 = all, 1 = changed or differing var id, 2 = changed only
def show_index(pif, vid, fdir, start=None, num=100, ff=0):
    cols = 4
    dats = get_file_list(fdir)
    if not dats:
        print "no files?"
        return
    print pif.render.format_link("?ff=1&d=" + fdir + "&s=" + start + "&n=" + str(num), 'Diff-ID'), '-'
    print pif.render.format_link("?ff=2&d=" + fdir + "&s=" + start + "&n=" + str(num), 'Diff'), '-'
    for i in range(0, len(dats), num):
        if start == dats[i]:
            print '<b>' + pif.render.format_link("?s=" + dats[i] + "&n=" + str(num), str(i / num + 1)) + '</b>', '-'
        else:
            print pif.render.format_link("?d=" + fdir + "&s=" + dats[i] + "&n=" + str(num), str(i / num + 1)), '-'
    prev = dats[0]
    if start in dats:
        i = dats.index(start)
        if i - num > 0:
            prev = dats[i - num]
        dats = dats[i:]
    if len(dats) >= num:
        next = dats[num]
    else:
        next = dats[-1]
#    dats = dats[:num]
    rows = (num - 1) / cols + 1
    print pif.render.format_button("next", "?d=" + fdir + "&s=" + next + "&n=" + str(num)), '-'
    print pif.render.format_button("previous", "?d=" + fdir + "&s=" + prev + "&n=" + str(num))
    print '<table width="100%"><tr>'
    for col in range(0, cols):
        irow = 0
        print '<td valign="top" width="%d%%">' % (100 / cols)
        while 1:
            if not dats:
                break
            fn = dats.pop(0)
            varfile = check_file(pif, vid, fdir, fn)
            mod_update = max(varfile['stat'])
            if ff and (mod_update == IS_GOOD or mod_update == IS_NO_MODEL):
                continue
            if ff == 2 and mod_update == IS_DIFFERENT_NUMBER:
                continue
            sclass = ' '.join([file_list_class[x] for x in varfile['stat']])
            print '<a href="?d=%s&f=%s"><span class="%s">%s</span></a>' % (fdir, fn, sclass, fn)
            show_file_link(fn, 'doc', 'w')
            show_file_link(fn, 'htm', 'h')
            show_file_link(fn, 'html', 'h')
#            print list(varfile['stat'])
            print '<br>'
            irow += 1
            sys.stdout.flush()
            if irow == rows:
                break
        print '</td>'
    print "</tr></table>"
    print 'done'


# ----- single file importer -------------------------------------------


#{'definition': 'varchar(64)', 'mod_id': 'MB652', 'attribute_name': 'dump', 'id': 1L}
def show_attrs(pif, file_id, mod, hdrs, var_desc):
    print "<h3>Attributes</h3>"
    mod_id = mod['id']
    attrs = pif.dbh.fetch_attributes(mod_id)
    attrs = pif.dbh.depref('attribute', attrs)
    common_attrs = pif.dbh.fetch_attributes('')
    common_attrs = pif.dbh.depref('attribute', common_attrs)
    visual_base = bool(mod['flags'] & pif.dbh.FLAG_MODEL_BASEPLATE_VISIBLE)
    print '<form method="post">' + pif.create_token()
    print '<input type="hidden" name="mod_id" value="%s">' % mod_id
    dets = pif.dbh.fetch_details(mod_id, "").get('', dict())
    dets = pif.dbh.depref('detail', dets)
    print "<table border=1>"
    print "<tr><th>ID</th><th>Name</th><th>Definition</th><th>Title</th><th>V</th><th>Default</th></tr>"
    for attr in attrs:
        #visuals = {True: ['visual.%(id)d' % attr], False: list()}
        #pif.render.comment(attr, visuals)
        print "<tr>"
        print '<td style="background-color: %s">' % bg_color[attr['attribute_name'] in hdrs + var_record_cols]
        print '<a href="%s">%s</a></td>' % (pif.dbh.get_editor_link('attribute', {'id': attr['id']}), attr['id'])
        print "<td>%s</td>" % pif.render.format_text_input("attribute_name.%(id)d" % attr, 32, 32, attr["attribute_name"])
        print "<td>%s</td>" % pif.render.format_text_input("definition.%(id)d" % attr, 32, 32, attr["definition"])
        print "<td>%s</td>" % pif.render.format_text_input("title.%(id)d" % attr, 32, 32, attr["title"])
        print "<td>%s</td>" % pif.render.format_checkbox("visual.%(id)d" % attr, [(1, '')], [attr['visual']])
        print "<td>%s</td>" % pif.render.format_text_input("description.%(id)d" % attr, 64, 32, dets.get(attr["attribute_name"], ""))
        print "<td>%s</td>" % pif.render.format_button_input(bname="save", name='renattr.%d' % attr['id'])
        print "<td>%s</td>" % pif.render.format_button("delete", "?f=%s&delattr=%d" % (file_id, attr['id']))
        print "</tr>"
        var_desc[attr["attribute_name"]] = attr["definition"]
    for attr in common_attrs:
        print "<tr>"
        print '<td style="background-color: %s">' % bg_color[attr['attribute_name'] in hdrs + var_record_cols]
        print '<a href="%s">%s</a></td>' % (pif.dbh.get_editor_link('attribute', {'id': attr['id']}), attr['id'])
        print "<td>%s</td>" % (attr["attribute_name"] +
	    pif.render.format_hidden_input({"attribute_name.%(id)d" % attr: attr["attribute_name"]}))
        print "<td>%s</td>" % attr["definition"]
        print "<td>%s</td>" % attr["title"]
	if attr['attribute_name'] == 'base':
	    print "<td>%s</td>" % pif.render.format_checkbox("visualbase", [(1, '')], [1 if visual_base else 0])
	else:
	    print "<td>%s</td>" % ('X' if attr['visual'] else '')
        print "<td>%s</td>" % pif.render.format_text_input("description.%(id)d" % attr, 64, 32, dets.get(attr["attribute_name"], ""))
        print "<td>%s</td>" % pif.render.format_button_input(bname="save", name='renattr.%d' % attr['id'])
        print "<td></td>"
        print "<td>%s</td>" % pif.render.format_link('/cgi-bin/vedit.cgi', txt=pif.render.format_button(bname="none"),
		args={'attribute_name.%s' % attr['id']: attr['attribute_name'], 'd': 'src/mbxf', 'description.%s' % attr['id']: 'none', 'f': file_id, 'm': mod_id, 'mod_id': mod_id, 'renattr.%s' % attr['id']: 'SAVE'})
        print "</tr>"
    cnt = 1
    for hdr in hdrs:
        if hdr not in var_record_cols and hdr not in [x['attribute_name'] for x in attrs]:
            print "<tr>"
            print "<td>new</td>"
            print "<td>%s</td>" % pif.render.format_text_input("%dn.attribute_name" % cnt, 32, 32, hdr)
            print "<td>%s</td>" % pif.render.format_text_input("%dn.definition" % cnt, 32, 32, "varchar(64)")
            print "</tr>"
            cnt += 1
            var_desc[hdr] = "varchar(64)"
    print "</table>"
    print pif.render.format_button_input('add')
    print pif.render.format_button_input('add new')
    print "</form>"


base_id_flag_names = [
    ('0001', 'NotMade'),
    ('0080', 'Revised'),
    ('0100', 'BP Vis'),
]

def show_base_id(pif, mod):
    # base id form
    print "<h3>Base ID</h3>"
    base_id_info = pif.dbh.describe_dict('base_id')
    base_id_tab = tables.table_info['base_id']
    print '<form method="post" name="base_id">' + pif.create_token()
    print "<table border=1>"
    print "<tr><th>Column</th><th>Value</th></tr>"
    for col in base_id_tab['columns']:
	print "<tr><td>%s</td><td>" % col
	if col in base_id_tab.get('bits', {}):
	    print pif.render.format_checkbox("base_id." + col, base_id_tab['bits'][col], useful.bit_list(mod[col], format='%04x'))
	else:
	    flen = int(paren_re.search(base_id_info[col]['type']).group('len'))
	    print pif.render.format_text_input("base_id." + col, flen, min(80, flen), mod[col])
        print "</td></tr>"
    print "</table>"
    print pif.render.format_button_input('save', 'save base id')
    print "</form>"


def show_casting(pif, mod, file_id):
    # casting form
    print "<h3>Casting</h3>"
    casting_info = pif.dbh.describe_dict('casting')
    print '<form method="post" name="casting">' + pif.create_token()
    print "<table border=1>"
    print "<tr><th>Column</th><th>Value</th><th>&nbsp;</th></tr>"
    for col in tables.table_info['casting']['columns'] + tables.table_info['casting']['extra_columns']:
	if casting_info[col]['type'] == 'text':
	    flen = 65535
	    # make this a text box instead of a text input.
	    print "<tr><td>%s</td><td>%s</td>" \
		% (col, pif.render.format_textarea_input("casting." + col, 80, 4, mod[col]))
	else:
	    flen = int(paren_re.search(casting_info[col]['type']).group('len'))
	    print "<tr><td>%s</td><td>%s</td>" \
		% (col, pif.render.format_text_input("casting." + col, flen, min(flen, 128), mod[col]))
        print "<td>%s</td></tr>" % casting_help(pif, col, mod)
    print "</table>"
    print pif.render.format_button_input('save', 'save casting')
    print "</form>"

    fmt_invalid, messages, missing =  pif.dbh.check_description_formatting(mod['id'], '<br>')
    for attr in missing:
        print pif.render.format_button("add", "?f=%s&m=%s&addattr=%s" % (file_id, mod['id'], attr)), attr, '<br>'
    if fmt_invalid:
	print messages
    print '<br>'


def find_var_id(dbvars, firow, ids_used):
    # fabricate unique id with no record
    varid = firow['var']
    if varid not in dbvars:
        return varid
    if varid[-1] >= 'A':
        varid = varid[:-1]
    trailer = ''
    while 1:
        if (varid + trailer) not in ids_used:
            for dbvar in dbvars:
                if dbvar == varid + trailer:
                    break
            else:
                return varid + trailer
        trailer = chr(ord(trailer) + 1) if trailer else 'a'


def casting_help(pif, col, mod):
    if col == 'rawname':
        return ' | '.join(mod.get('iconname', list()))
    if col == 'vehicle_type':
        return pif.render.format_button("help", "../pages/types.php", lalso={'target': '_blank'})
    if col == 'country':
        return pif.render.format_button("help", "../pages/countries.php", lalso={'target': '_blank'})
    if col == 'make':
        return pif.render.format_button("help", "../pages/makes.php", lalso={'target': '_blank'})
    if col == 'flags':
        return "NOT_MADE = 1"
    if col == 'section_id':
        return "man - rwr - mi - orig - promo - wr - fea - sf - rn - rw"
    return "&nbsp;"


text_color = {True: '#0000FF', False: '#FF0000'}
bg_color = {True: '#FFFFFF', False: '#FFCCCC'}
paren_re = re.compile(r'\((?P<len>\d*)\)')


def show_file(pif, vid, fdir, fn, args):
    varfile = parse_file(pif, vid, fdir, fn, args)

    print '<br>'
    print list(varfile['stat']), '-'
    print list(varfile['modids']), '-'

    show_file_link(fn, 'html', 'HTML')
    show_file_link(fn, 'htm', 'HTM')
    show_file_link(fn, 'doc', 'DOC')
    show_file_link(fn, 'dat', 'DAT')
    print '-', pif.render.format_link(pif.request_uri + "&settings=1", "settings"), '-'
    for id in varfile['modids']:
        print '<a href="#%s">%s</a>' % (id, id)
    varfile['var_desc'] = dict([(x['field'], x['type']) for x in pif.dbh.describe_dict('variation').values()])

    for fitab in varfile['tabs']:
        if fitab['casting']:
            show_model_table(pif, varfile, fitab)
        else:
            show_no_model(pif, varfile, fitab)
        print fitab['epilog']


def show_no_model(pif, varfile, fitab):
    print pif.render.format_image_optional(fitab['modid'], largest=mbdata.IMG_SIZ_MEDIUM,
	pdir='pic/man', also={'align': 'right'})
    print fitab['preface'], "<br>"
    print "<table border=1>"
    for row in [fitab['gridhead']] + fitab['body']:
        print "<tr>"
        for cel in row:
            print "<td>" + cel + "</td>"
        print "</tr>"
    print "</table>"


def show_model_table(pif, varfile, fitab):
    # header info
    print '<i id="%s"></i>' % fitab['modid']
    mod = fitab['casting']

    for vf in filter(None, [x['imported_from'] for x in pif.dbh.fetch_variation_files(mod['id'])]):
        print '<a href="?f=%s">%s</a>' % (vf, vf)
    print '<br>'
    print '<center><h2><a href="single.cgi?id=%s">%s</a>' % (mod['id'], mod['id'])
    print "<h3>", mod.get('rawname', 'no rawname?'), "</h3></center>"

    print pif.render.format_image_optional(fitab['modid'], largest=mbdata.IMG_SIZ_MEDIUM,
	pdir='pic/man', also={'align': 'right'})
    print fitab['preface'], "<br>"

    # base id form
    show_base_id(pif, mod)

    # casting form
    show_casting(pif, mod, varfile['filename'])

    # attributes form
    show_attrs(pif, varfile['filename'], mod, fitab['gridhead'], varfile['var_desc'])

    # variations form
    print '<form method="post">' + pif.create_token()
    print '<input type="hidden" name="current_file" value="%s">' % varfile['filename']
    print '<input type="hidden" name="mod_id" value="%s">' % mod['id']
    show_variations(pif, varfile, fitab, mod['id'])

    print pif.render.format_button_input('save')
    print pif.render.format_button_input('recalc')
    print pif.render.format_button_input('delete all')
    print pif.render.format_button_input('fix numbers')
    print pif.render.format_button_input('delete orphans')
    print '</form>'


def show_variations(pif, varfile, fitab, mod_id):
    print "<h3>Variations</h3>"
    dbvars = fitab['dbvars']
    print "<table border=1><tr><th></th>"
    for hdr in fitab['gridhead']:
        print "<th>" + hdr + "</th>"
    print "</tr>"
    print "<tr><th></th>"
    for hdr in fitab['gridhead']:
        print "<td>" + varfile['var_desc'][hdr] + "</td>"
    print "</tr>"
    ids_used = list()
    for rec in fitab['body']:
        is_new = False
        orignum = rec['var']
        if rec["var"] in varfile['var_lup']:
            rec["var"] = varfile['var_lup'].get(rec["var"], rec["var"])
            dbvar = dbvars.get(rec['var'], dict())
        else:
            dbvar = find_record(varfile['filename'], dbvars, rec, fitab['gridhead'])
        if not dbvar:
            dbvar = {'var': find_var_id(dbvars, rec, ids_used)}
            is_new = True
        else:  # gray
            del dbvars[dbvar['var']]  # gray
        ids_used.append(dbvar['var'])
	pic = os.path.join(*pif.render.find_image_file(pdir=config.IMG_DIR_MAN, fnames=mod_id, vars=dbvar.get('var', ''), largest=mbdata.IMG_SIZ_LARGE, nobase=True))
        print '<tr><td style="font-weight: bold; color: %s">' % (text_color[rec['var'] == dbvar.get('var')])
        print '<input type="hidden" name="%s.orignum" value="%s">' % (rec['var'], dbvar.get('var'))
        if dbvar.get('var'):
            print '<a href="/cgi-bin/vars.cgi?mod=%s&edit=1&var=%s" style="color: %s">%s</a>' % \
                  (mod_id, dbvar['var'], text_color[vrdata.compare_var_ids(rec['var'], dbvar.get('var'))], rec['var'])
        else:
            print rec['var']
        #if os.path.exists(pic):
        if pic:
            print '<br><a href="../%s">PIC</a>' % pic
        elif is_new:
            print '<br>new'
	elif dbvar.get('picture_id'):
	    print '<br><i>pic</i>'
        print '</td>'
        rec['var'] = dbvar.get('var', rec.get('var', ''))
        print '<input type="hidden" name="%s.imported_var" value="%s">' % (rec['var'], orignum)
        for hdr in fitab['gridhead']:
            dbdet = str(dbvar.get(hdr, ''))
            fidet = rec.get(hdr, '')
            print '<td style="color: %s; background-color: %s">' % (text_color[dbdet == fidet], bg_color[dbdet == fidet])
            print str(dbvar.get(hdr, '')) + "<br>"
            if dbdet != fidet or hdr == 'var':
		print pif.render.format_text_input(rec['var'] + '.' + hdr, int(varfile['var_desc'][hdr][8:-1]), 16, fidet if fidet else '\\b')
            elif hdr == 'imported_from':
                print '<input type="hidden" name="%s.imported_from" value="%s">' % (rec['var'], varfile['filename'])
                print dbvar.get('imported_var', 'unset')
	    char_test(fidet)
            print "</td>"
        print "</tr>"
    for varid in sorted(dbvars.keys()):
        dbvar = dbvars[varid]
        is_same_file = dbvar.get('imported_from') == varfile['filename']
        #pif.render.comment(str(dbvar))
	pic = os.path.join(*pif.render.find_image_file(pdir=config.IMG_DIR_MAN, fnames=mod_id, vars=dbvar.get('var', ''), largest=mbdata.IMG_SIZ_LARGE, nobase=True))
        #pif.render.comment("pic", pic)
        if is_same_file:
            print '<input type="hidden" name="orphan" value="%s">' % varid
        print '<tr><th style="background-color: #CCCCCCC">'
        if dbvar.get('var'):
            print '<a href="/cgi-bin/vars.cgi?mod=%s&edit=1&var=%s" style="color: #000000">%s</a>' % \
                  (mod_id, dbvar['var'], dbvar['var'])
        else:
            print '%s' % dbvar['var']
        if pic:
            print '<br><a href="../%s">PIC</a>' % pic
        print '</th>'
        for hdr in fitab['gridhead']:
            dbdet = str(dbvar.get(hdr, ''))
            if is_same_file:
                print '<td style="color: %s; background-color: %s">' % ('#990000', '#CCCCCC')
            else:
                print '<td style="color: %s; background-color: %s">' % ('#000000', '#CCCCCC')
            print str(dbvar.get(hdr, '')) + "<br>"
            print "</td>"
        print "</tr>"
    print "</table>"


def char_test(fidet):
    pass
    noch = []
    if fidet:
	for ch in fidet:
	    if ch not in vrdata.ok_letters:
		noch.append(ord(ch))
	if noch:
	    print '<br>', noch


def show_settings(pif, vid, fn):
    print '<h3>File Settings</h3>'
    vid.show_file_settings(fn)
    print '<h3>Global Settings</h3>'
    vid.show_global_settings()


# ----- mainlike functions ---------------------------------------------


@basics.web_page
def handle_form(pif):
    pif.render.print_html()
    mod_id = pif.form.get_str('m')
    if not mod_id:
	mod_id = pif.form.get_str('mod_id')
    if mod_id:
        pif.render.title = 'Variations - ' + mod_id
    elif pif.form.has('f'):
        pif.render.title = 'Variations - ' + pif.form.get_str('f')
    print pif.render.format_head()
    useful.header_done()
    if not pif.is_allowed('a'):
        return

    pif.dbh.set_verbose(True)
    vid = vrdata.VariationImportData()
    vid.verbose = pif.render.verbose
    nvars = list()
    file_dir = pif.form.get_str('d', 'src/mbxf')

    print pif.form, '<br>'
    if pif.form.has("recalc"):  # doesn't really fit the pattern
        print "recalc<br>"
        for k in pif.form.keys(end='.var'):
            nvars.append(k[0:-4] + "=" + pif.form.get_str(k))
    elif pif.duplicate_form: #not pif.dbh.insert_token(pif.form.get_str('token')):
	print 'duplicate form submission detected'
    else:
        do_action(pif, mod_id)
    print "<br><hr>"

    args = ''
    if pif.form.has('settings'):
	show_settings(pif, vid, pif.form.get_str('f'))
    elif pif.form.has('f'):
        show_file(pif, vid, file_dir, pif.form.get_str('f'), ' '.join(nvars))
    else:
        show_index(pif, vid, file_dir, start=pif.form.get_str('s'), num=pif.form.get_int('n', 100), ff=int(pif.form.get_int('ff')))

    print pif.render.format_tail()


def save_attribute(pif, attr_id, mod_id):
    attr = pif.dbh.fetch_attribute(attr_id)
    attr = pif.dbh.depref('attribute', attr)
    print "save_attribute", pif.form.get_form(), attr_id, attr, '<br>'
    if len(attr) == 1:
        attr = attr[0]
	if attr_id > 4:
	    for key in attr:
		if pif.form.has(key + '.%d' % attr_id):
		    attr[key] = pif.form.get_str(key + '.%d' % attr_id)
	    pif.dbh.update_attribute(attr, attr_id)

        if pif.form.get_str("description.%d" % attr_id) != "":
            rec = {"mod_id": mod_id, "var_id": "", "attr_id": attr_id,
                   "description": pif.form.get_str("description.%d" % attr_id)}
            where = {"mod_id": mod_id, "var_id": "", "attr_id": attr_id}
	    print 'detail', rec, where
            print pif.dbh.write("detail", rec, where)
	    print '<br>'
	if attr_id == 1:
	    if pif.form.get_bool("visualbase"):
		pif.dbh.update_flags('base_id', turn_on=pif.dbh.FLAG_MODEL_BASEPLATE_VISIBLE, where='id="%s"' % mod_id)
	    else:
		pif.dbh.update_flags('base_id', turn_off=pif.dbh.FLAG_MODEL_BASEPLATE_VISIBLE, where='id="%s"' % mod_id)
    else:
        print '%d attributes returned!' % len(attr)


def do_action(pif, mod_id):
    if pif.form.has("add"):
        print "add<br>"
	print pif.form.get_form(), '<br>'
        for k in pif.form.keys(end='n.definition'):  # pretty sure these are the new guys
            attr = k[0:-12]
            print "n_def", k, attr
            rec = {"mod_id": mod_id, "attribute_name": pif.form.get_str(attr + "n.attribute_name"),
                   "title": pif.form.get_str(attr + "n.attribute_name").replace('_', ' ').title(),
                   "definition": pif.form.get_str(k)}
            pif.dbh.write("attribute", rec, {"mod_id": mod_id, "attribute_name": pif.form.get_str(attr + "n.attribute_name")})
        for k in pif.form.keys(start='attribute_name.'):
            attr = k[15:]
            print "def", k, attr
            rec = {"mod_id": mod_id, "attribute_name": pif.form.get_str('attribute_name.' + attr),
                   "title": pif.form.get_str('title.' + attr),
                   "definition": pif.form.get_str(k), "visual": pif.form.get_str("visual." + attr, '1')}
            pif.dbh.write("attribute", rec, {"id": attr}, modonly=True)
            if pif.form.get_str("description." + attr, '') != "":
                rec = {"mod_id": mod_id, "var_id": "", "attr_id": attr, "description": pif.form.get_str("description." + attr)}
                where = {"mod_id": mod_id, "var_id": "", "attr_id": attr}
		print "detail", rec, where, "<br>"
                pif.dbh.write("detail", rec, where)
	pif.dbh.recalc_description(mod_id)
    elif pif.form.has("add_new"):
        print "add new<br>"
        pif.dbh.write("attribute", {"mod_id": mod_id}, list())
    elif pif.form.find('renattr'):
        keys = pif.form.find('renattr')
        print "renattr", keys, "<br>"
        for key in keys:
            attr_id = int(key[8:])
            save_attribute(pif, attr_id, mod_id)
	pif.dbh.recalc_description(mod_id)
    elif pif.form.has("save_base_id"):
        print "save base_id<br>"
        rec = dict()
        for k in pif.form.keys(start='base_id.'):
	    if k == 'base_id.flags':
		rec['flags'] = sum(int(x, 16) for x in pif.form.get_list('base_id.flags'))
	    else:
		rec[k[8:]] = pif.form.get_str(k)
        pif.dbh.write("base_id", rec, {"id": pif.form.get_str("base_id.id")})
    elif pif.form.has("save_casting"):
        print "save casting<br>"
        rec = dict()
	for k in tables.table_info['casting']['columns'] + tables.table_info['casting']['extra_columns']:
            rec[k] = pif.form.get_str('casting.' + k)
        pif.dbh.write("casting", rec, {"id": pif.form.get_str("casting.id")})
	pif.dbh.recalc_description(pif.form.get_str('casting.id'))
    elif pif.form.has("save"):
        print "save"
        pif.dbh.update_variation({'imported_from': 'was ' + pif.form.get_str('current_file')},
                                 {'imported_from': pif.form.get_str('current_file'), 'mod_id': mod_id})
        attrs = pif.dbh.fetch_attributes(mod_id)
        attr_lup = dict()
        for attr in attrs:
            print attr, '<br>'
            attr_lup[attr['attribute.attribute_name']] = attr.get('attribute.id')
        var_cols = pif.dbh.columns("variation")
        for k in pif.form.keys(end='.var'):
            rec = {"mod_id": mod_id}
            rec["imported"] = time.time()
            det = dict()
            for vk in pif.form.keys(start=pif.form.get_str(k)):
                vv = pif.form.get_str(vk)
                kk = vk[len(pif.form.get_str(k)) + 1:]
                if vv == '\\b':
                    vv = ''
                if kk == 'orignum':
                    pass
                elif kk in var_cols:
                    rec[kk] = vv
                else:
                    det[kk] = vv
            pif.dbh.write("variation", rec, {"mod_id": mod_id, "var": k[0:-4]})
            print 'variation', rec, '<br>'
            for dk in det:
                if dk in attr_lup:
                    detrec = {"mod_id": mod_id, "var_id": k[0:-4], "attr_id": attr_lup[dk], "description": det[dk]}
                    pif.dbh.write("detail", detrec, {"mod_id": mod_id, "var_id": k[0:-4], "attr_id": attr_lup[dk]})
                    print 'detail', detrec, '<br>'
	pif.dbh.recalc_description(mod_id)
        print "done"
    elif pif.form.has("delete_orphans"):
        print "delete orphans<br>"
        orphans = pif.form.get_list('orphan', list())
        for var_id in orphans:
            print 'deleting', mod_id, var_id, '<br>'
            varias.delete_variation(pif, mod_id, var_id)
    elif pif.form.has("delete_all"):
        print "delete all<br>"
        pif.dbh.delete_detail(where={"mod_id": mod_id})
        pif.dbh.delete_variation(where={"mod_id": mod_id})
    elif pif.form.has("delattr"):
        print "delattr<br>"
        pif.dbh.delete_attribute({"id": pif.form.get_str('delattr')})
        pif.dbh.delete_detail({"attr_id": pif.form.get_str('delattr')})
    elif pif.form.has("addattr"):
        print "addattr<br>"
	print 'adding', mod_id, pif.form.get_str('addattr')
	print pif.dbh.insert_attribute(mod_id, pif.form.get_str('addattr')), '<br>'
    elif pif.form.has("fix_numbers"):
        print "fix numbers<br>"
        for k in pif.form.keys(end='.orignum'):
	    # somewhere right around here we want to use vrdata.compare_var_ids
            if pif.form.get_str(k) != k[0:-8]:
                retvar = -999
                varias.rename_variation(pif, mod_id, pif.form.get_str(k), k[0:-8])
