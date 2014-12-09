#!/usr/local/bin/python

import copy, os, sys
import basics
import bfiles
import config
import images
import mbdata
import mflags
import models
import useful

width = [600, 600, 300, 200, 150, 100]

'''
| X.01 | Packaging
| X.02 | Catalogs
| X.03 | Advertisements
| X.21 | Major Packs
| X.22 | King Size
| X.23 | Real Working Rigs
| X.24 | Accessory Packs
| X.31 | Models of Yesteryear
| X.41 | Buildings
| X.61 | Presentation Sets
| X.62 | Gift Sets
| X.63 | 5-Packs
| X.64 | Licensed 5-Packs
| X.65 | 10-Packs
| X.71 | Roadways
'''


def ver_no(rank):
    if rank:
        return chr(96 + rank)
    return ' '


# -------- lineup ----------------------------------


def show_lineup_model(pif, mdict, comments, verbose=False, unroll=False):
    ostr = ''

    pif.render.comment('show_lineup_model', mdict)

    if not mdict:  # pragma: no cover
        return ostr

    mdict = pif.dbh.depref('base_id', mdict)

    # want to add a yellow star here if the picture is from another model
    mdict.setdefault('make', '')
    mdict['name'] = str(mdict.get('rawname', '')).replace(';', ' ')
    mdict['iconname'] = pif.dbh.icon_name(mdict['rawname'])
    mdict['unlicensed'] = {'unl': '-', '': '?'}.get(mdict.get('casting.make', ''), ' ')
    mdict.setdefault('description', '')
    mdict['descs'] = filter(lambda x: x, str(mdict['description']).split(';'))
    if not mdict['flags']:
        mdict['flags'] = 0
    mdict['made'] = not (mdict['flags'] & pif.dbh.FLAG_MODEL_NOT_MADE)
    mdict['notmade'] = {True: '', False: '*'}[mdict['made']]
    mdict['casting_type'] = mbdata.casting_types.get(mdict.get('model_type', 'SF'), 'Casting')
    mdict['name'] = mdict['lineup_model.name']
    mdict['mod_id'] = mdict['lineup_model.mod_id']
    mdict['ref_id'] = mdict['vs.ref_id']
    # won't work.  still figuring it out.
    if pif.render.verbose:
        print 'show_lineup_model', mdict['lineup_model.number']
        print mdict.get('rank_id'), mdict.get('sub_id'), mdict.get('vs.rank_id'), mdict.get('vs.sub_id')
    if mdict['vs.sub_id'] and mdict['vs.sub_id'].isdigit():
        mdict['rank_id'] = mdict['vs.sub_id']
        mdict['sub_id'] = ''
        if pif.render.verbose:
            print 'isdig'
    elif mdict.get('vs.rank_id'):
        mdict['sub_id'] = mdict['vs.rank_id']
        if pif.render.verbose:
            print 'rank_id'
    else:
        mdict['rank_id'] = 0
        mdict['sub_id'] = mdict['vs.sub_id']
        if pif.render.verbose:
            print 'normal'
    if pif.render.verbose:
        print '<hr>'
    mdict['href'] = ""
    mdict['product'] = ''
    mdict['no_variation'] = mdict['is_product_picture'] = 0

    mdict['cvarlist'] = []
    mdict.setdefault('vars', [])
    mdict['vars'].sort()
    for var in mdict['vars']:
        if var[0]:
            found = False
            for cvar in mdict['cvarlist']:
                if var[1] == cvar[1]:
                    if var[2] and var[2] not in cvar[0]:
                        cvar[0].append(var[2])
                    if var[0] not in cvar[0]:
                        cvar[0].append(var[0])
                    found = True
                    break
            if not found:
                mdict['cvarlist'].append([[var[0]], var[1]])
                if var[2]:
                    mdict['cvarlist'][-1][0].append(var[2])

    if mdict['casting.id']:
        # modify this if rank_id exists
        if mdict['lineup_model.picture_id']:
            mdict['product'] = mdict['lineup_model.picture_id']
            mdict['is_reused_product_picture'] = 1
        elif mdict.get('image_format'):
            mdict['product'] = mdict['image_format'] % mdict['lineup_model.number']
        if pif.render.find_image_file([mdict['product']], suffix='jpg', pdir=mdict['pdir']):
            mdict['is_product_picture'] = 1
            comments.add('c')
        mdict['href'] = "single.cgi?dir=%(pdir)s&pic=%(product)s&ref=%(ref_id)s&sub=%(sub_id)s&id=%(mod_id)s" % mdict
    elif mdict['pack.id']:
        if mdict['lineup_model.picture_id']:
            mdict['product'] = mdict['lineup_model.picture_id']
            mdict['is_reused_product_picture'] = 1
        elif mdict.get('image_format'):
            mdict['product'] = mdict['image_format'] % mdict['pack.id']
        if pif.render.format_image_sized([mdict['product']], pdir=mdict['pdir'], largest='g'):
            mdict['is_product_picture'] = 1
            comments.add('c')
        mdict['href'] = "packs.cgi?page=%(pack.page_id)s&id=%(pack.id)s" % mdict
    elif mdict['publication.id']:
        mdict['product'] = mdict['publication.id'] + '_01'
        if pif.render.format_image_sized([mdict['product']], pdir=mdict['pdir'], largest='g'):
            mdict['is_product_picture'] = 1
            comments.add('c')
        mdict['href'] = "pub.cgi?id=%(publication.id)s" % mdict

    if pif.form_bool('large'):
        ostr += '<table><tr><td width=400>'
        img = pif.render.format_image_required(mdict['product'], suffix='jpg', pdir=mdict['pdir'], also={'class': 'largepic'})
        ostr += pif.render.format_link('upload.cgi?d=%s&r=%s' % (mdict['pdir'], mdict['product']), img)
        ostr += '</td><td><center>'
    if unroll and mdict.get('casting.id') and mdict['cvarlist']:
        for desc in mdict['cvarlist']:
            ostr += show_lineup_model_var(pif, mdict, comments, show_var=desc[0][0], verbose=verbose)
    else:
        ostr += show_lineup_model_var(pif, mdict, comments, verbose=verbose)
    if pif.form_bool('large'):
        ostr += '</center></td></tr></table>'
    return ostr


def show_lineup_model_var(pif, mdict, comments, show_var=None, verbose=0):
    ostr = ''

    imglist = []
    mdict['varlist'] = []
    if mdict.get('lineup_model.flags', 0) & pif.dbh.FLAG_MODEL_NOT_MADE:
        mdict['not_made'] = True
        imglist.append(mdict['lineup_model.mod_id'])
        comments.add('n')
    elif mdict.get('lineup_model.mod_id'):
        imglist.append(mdict['lineup_model.mod_id'])
        if show_var:
            for var in mdict['cvarlist']:
                if show_var in var[0]:
                    mdict['varlist'].extend(var[0])
        else:
            for var in mdict['vars']:
                if var[2]:
                    mdict['varlist'].append(var[2])
                elif var[0]:
                    mdict['varlist'].append(var[0])
    pif.render.comment('varlist', mdict['varlist'])
    mdict['imgstr'] = pif.render.format_image_required(imglist, prefix='s_', vars=mdict['varlist'], pdir=config.IMG_DIR_MAN)

    if show_var:
        mdict['descriptions'] = [x[1] for x in filter(lambda y: show_var in y[0], mdict['cvarlist'])]
    else:
        mdict['descriptions'] = [x[1] for x in mdict['vars']]

    mdict['no_specific_image'] = 0
    if mdict['casting.id'] and not mdict.get('not_made'):
        if mdict['imgstr'].find('-') < 0:
            comments.add('i')
            mdict['no_specific_image'] = 1
        if len(mdict['varlist']) < 1:  # pragma: no cover
            comments.add('v')
            mdict['no_variation'] = 1
        # also if there is no description string

    # mdict: imgstr name number pdir product vars
    ostr += models.add_model_table_product_link(pif, mdict)
    return ostr


def set_vars(llineup, mods, regions, ref_id, verbose=0):
    done = False
    for cregion in regions:
        if verbose:  # pragma: no cover
            pass  # print '<p><b>set_vars cregion', cregion, ref_id, '</b><br>'
        for mod in mods:
            mod['number'] = mod['lineup_model.number']
            set_var(mod, llineup, cregion, ref_id, verbose=verbose)
            #if mod['number'] in llineup:
                 #done = True
        if done:
            break
    if verbose:  # pragma: no cover
        print '<hr>'


def set_var(mod, llineup, region, ref_id, verbose=0):
    sub_id = region
    rank_id = 0
    if region == 'W':
        sub_id = ''
    if verbose:  # pragma: no cover
        pass  #print '<hr width=90%> set_var #', mod['number'], 'reg', region, 'ref', ref_id, 'sub', sub_id, 'done', mod['number'] in llineup, 'modreg', mod['lineup_model.region']
        #print 'VS', mod.get('vs.ref_id'), ':', mod.get('vs.rank_id', 'unset'), '/', mod.get('vs.sub_id', 'unset'), '<br>'
        #print mod, '<br>'
    num = mod['number']
    lmod = llineup.get(num)
    mod.setdefault('vs.rank_id', '')
    if lmod and lmod['lineup_model.mod_id'] != mod['lineup_model.mod_id']:  # already done?
        if verbose:  # pragma: no cover
            print "skipdiff<br>"
    elif not mod['vs.sub_id']:
        mod['vs.sub_id'] = ''
    elif mod['vs.sub_id'].isdigit():
        mod['vs.rank_id'] = mod['vs.sub_id']
        mod['vs.sub_id'] = ''
        if verbose:  # pragma: no cover
            print "rank-limited", '<br>'
    if mod['vs.sub_id'] != sub_id:
        if verbose:  # pragma: no cover
            print "skip0", '<br>'
    elif num not in llineup:
        mod = copy.deepcopy(mod)
        mod['vars'] = [(mod['v.var'], mod['v.text_description'], mod['v.picture_id'])]
        llineup[num] = mod
        if verbose:  # pragma: no cover
            print "new", '<br>'
    elif not lmod['vs.ref_id'] or \
                (lmod['vs.ref_id'] == ref_id):  # and (lmod['vs.sub_id'] == sub_id or not lmod['vs.sub_id'])):
        lmod['vars'].append((mod['v.var'], mod['v.text_description'], mod['v.picture_id']))
        #lmod['vs.ref_id'] = mod['vs.ref_id']
        #lmod['vs.sub_id'] = mod['vs.sub_id']
        if verbose:  # pragma: no cover
            print "add", '<br>'
    elif mod['lineup_model.region'] == region:
        mod = copy.deepcopy(mod)
        mod['vars'] = [(mod['v.var'], mod['v.text_description'], mod['v.picture_id'])]
        llineup[num] = mod
        if verbose:  # pragma: no cover
            print "repl", '<br>'
    else:
        pass
        if verbose:  # pragma: no cover
            print "skip1", '<br>'


def create_lineup(mods, parents, year, region, verbose=0):
    if verbose:  # pragma: no cover
        pass  #print 'create_lineup', len(mods), parents, year, region, '<br>'
    #if region == 'X':
        #return {x['lineup_model.number']: x for x in mods}

    rankmods = dict()
    reg_list = []
    cregion = region
    while cregion:
        reg_list.append(cregion)

        for mod in mods:
            if cregion == mod['lineup_model.region']:
                if verbose:  # pragma: no cover
                    pass  #print 'CreateLinup', mod['lineup_model.number'], 'sub', mod['vs.sub_id'], '<br>'
                    #print mod
                mod['number'] = mod['lineup_model.number']
                rankmods.setdefault(mod['number'], [])
                if rankmods[mod['number']] and mod['lineup_model.mod_id'] != rankmods[mod['number']][0]['lineup_model.mod_id']:
                    if verbose:  # pragma: no cover
                        print 'dumped'
                elif not mod['vs.sub_id'] or not mod['vs.sub_id'].isdigit() or mod['number'] == int(mod['vs.sub_id']):
                    rankmods[mod['number']].append(mod)
                    if verbose:  # pragma: no cover
                        print 'kept'
                elif verbose:  # pragma: no cover
                    print 'dropped'
                if verbose:  # pragma: no cover
                    print '<hr>'

        cregion = parents.get(cregion)

    ref_id = 'year.%s' % year
    llineup = dict()

    for rank in rankmods:
        set_vars(llineup, rankmods[rank], reg_list, ref_id, verbose=verbose)

    return llineup


'''
def get_man_sections(pif, year, region):
    # rewrite this!  one query, then deal in code.
    # split out X sections here.
    # order by display_order
    while 1:
        wheres = ["page_id='year.%s'" % year]
        if region:
            wheres.append("id like '%s%%'" % region)
        wheres.append("not id like 'X%'")
        if not pif.render.isbeta:
            wheres.append("not flags & %d" % pif.dbh.FLAG_SECTION_HIDDEN)
        secs = pif.dbh.depref('section', pif.dbh.fetch_sections(wheres))
        if secs:
            break
        if region not in mbdata.regionparents:
            return '', dict(), []
        region = mbdata.regionparents[region]
    return region, secs[0], secs[1:], list()


def get_extra_sections(pif, year):
    where = ["page_id='year.%s'" % year, "id like 'X%'"]
    if not (pif.render.isbeta or pif.form_bool('hidden')):
        where.append(' and not flags & %d' % pif.dbh.FLAG_SECTION_HIDDEN)
    return pif.dbh.depref('section', pif.dbh.fetch_sections(where))
'''


def get_man_sections(pif, year, region):
    # rewrite this!  one query, then deal in code.
    # split out X sections here.
    # order by display_order

    wheres = ["page_id='year.%s'" % year]
    if not pif.render.isbeta:
        wheres.append("not flags & %d" % pif.dbh.FLAG_SECTION_HIDDEN)
    secs = pif.dbh.depref('section', pif.dbh.fetch_sections(wheres))
    secs.sort(key=lambda x: x['display_order'])

    lsecs = list()
    xsecs = filter(lambda x: x['id'].startswith('X'), secs)
    secs = filter(lambda x: not x['id'].startswith('X'), secs)

    while 1:
        lsecs = filter(lambda x: x['id'].startswith(region), secs)
        if lsecs:
            break
        if region not in mbdata.regionparents:
            return '', dict(), lsecs, xsecs
        region = mbdata.regionparents[region]
    return region, lsecs[0], lsecs[1:], xsecs


def get_lineup_models(pif, year, region):
    line_regions = mbdata.get_region_tree(region)
    lmodlist = pif.dbh.fetch_lineup_models(str(year), line_regions)
    lmodlist.sort(key=lambda x: x['lineup_model.number'])
    #print 'get_lineup_models', len(lmodlist), 'models<br>'
#    for mod in lmodlist:
#       pif.render.comment('get_lineup_models:', mod)
    return lmodlist


def generate_man_lineup(pif, year, region):
    pif.render.comment('lineup.generate_man_lineup', year, region)

    if region:
        moddict = create_lineup(get_lineup_models(pif, year, region),
                        mbdata.regionparents, year, region, verbose=pif.render.verbose)

        keylist = moddict.keys()
        keylist.sort()
        #print 'keylist', keylist, '<br>'
        for key in keylist:
            #print 'mod', moddict[key], '<br>'
            moddict[key]['lineup_model.picture_id'] = moddict[key]['lineup_model.picture_id'].replace('W', region)
            yield moddict[key]


def create_extra_lineup(pif, year, secs, verbose=0):  # currently unimplemented # pragma: no cover
    line_regions = [x['id'] for x in secs]
    lmods = pif.dbh.fetch_lineup_models(str(year), line_regions)
    if verbose:  # pragma: no cover
        print 'create_extra_lineup', year, len(lmods), '<br>'

    ref_id = 'year.%s' % year
    for sec in secs:
        if verbose:  # pragma: no cover
            print '<p>sec', sec, '<br>'
        rankmods = dict()
        for mod in lmods:
            if mod['lineup_model.region'] == sec['id']:
                mod['number'] = mod['lineup_model.number']
                rankmods.setdefault(mod['number'], [])
                rankmods[mod['number']].append(mod)
                if verbose:  # pragma: no cover
                    print 'mod', mod['lineup_model.mod_id'], '<br>'

        moddict = dict()
        for rank in rankmods:
            set_vars(moddict, rankmods[rank], [sec['id'], 'W'], ref_id, verbose=verbose)

        sec['mods'] = []
        keylist = moddict.keys()
        keylist.sort()
        #print 'keylist', keylist, '<br>'
        for key in keylist:
            #print 'mod', moddict[key], '<br>'
            sec['mods'].append(moddict[key])


def correct_region(region, year):
    if isinstance(year, str):
        year = int(''.join(filter(lambda x: x.isdigit(), year)))
    if year < 1982:
        region = 'W'
    elif region == 'D':
        if year not in (1999, 2000, 2001):
            region = 'R'
    elif region == 'B':
        if year not in (2000, 2001):
            region = 'R'
    elif region == 'A':
        if year >= 2002:  # is this correct?
            region = 'U'
        if year not in (2000, 2001):
            region = 'R'
    elif region == 'L':
        if year < 2008 or year > 2011:
            region = 'R'
    return region, year


def show_section(pif, lran, mods, lup_region, year, comments):
    pif.render.comment("show_section: range", lran)
    lran['entry'] = list()
    multivars = list()
    unroll = pif.form_bool('unroll')
    if lran['flags'] & pif.dbh.FLAG_SECTION_HIDDEN:
        lran['name'] = '<i>' + lran['name'] + '</i>'
    for mdict in mods:
        mdict['disp_format'] = lran.get('disp_format', '')
        if lran['flags'] & pif.dbh.FLAG_SECTION_DEFAULT_IDS:
            mdict['shown_id'] = pif.dbh.default_id(mdict['lineup_model.mod_id'])
            mdict['disp_format'] = '%s.'
        else:
            mdict['shown_id'] = mdict['lineup_model.number']
        mdict['image_format'] = lran['img_format']
        pdir = pif.render.pic_dir
        if lran.get('pic_dir'):
            pdir = lran['pic_dir']
        mdict['pdir'] = pdir
        if lup_region == 'X':
            mdict['anchor'] = 'X%d' % mdict['number']
        else:
            mdict['anchor'] = '%d' % mdict['number']
        pif.render.comment('mdict2', mdict)
        ent = {
            'text': show_lineup_model(pif, mdict, comments, unroll=unroll),
            'display_id': mdict.get('lineup_model.style_id', 0),
            'st_suff': '', 'style': ''
        }
        if len(mdict['cvarlist']) > 1:
            multivars.append(str(mdict['number']))
        if not (lran['flags'] & pif.dbh.FLAG_SECTION_NO_FIRSTS) and year == mdict['first_year']:
            ent['class'] = 'newcasting'
        lran['entry'].append(ent)
    lran['multivars'] = multivars
    return lran


def run_file(pif, region, year):
    pif.render.comment('lineup.run_file', region, year)
    lup_region, year = correct_region(region, year)
    llineup = {'id': lup_region, 'section': [], 'name': '', 'tail': []}

    lup_region, lsec, secs, xsecs = get_man_sections(pif, year, region)
    if not lup_region:
        return llineup

    modlist = list(generate_man_lineup(pif, year, lup_region))
    if not modlist:
        return llineup

    endv = len(modlist)
    for sec in reversed(secs):
        sec['end'] = endv
        endv = sec['start']

    img = pif.render.format_image_optional(['%ss' % year])
    if img[0] == '<':
        lsec['name'] += '<br>' + img
    lsec['id'] = lup_region
    lsec['range'] = []
    hdr = lsec['name']

    if pif.form_bool('large'):
        lsec['columns'] = 1

    comments = set()
    multivars = list()

    if secs:
        for lran in secs:
            lran.update({
                'id': lup_region + '_' + str(lran['display_order']),
                'graphics': [lran['img_format'][:4] + lup_region + 's%02d' % lran['display_order']]
            })
            lsec['range'].append(show_section(pif, lran, modlist[lran['start']:lran['end']], lup_region, year, comments))
            multivars.extend(lran['multivars'])
    else:
        lran = copy.deepcopy(lsec)
        lran.update({'id': lup_region + '_1', 'name': '', 'note': '', 'graphics': []})
        lsec['range'].append(show_section(pif, lran, modlist, lup_region, year, comments))
        multivars.extend(lran['multivars'])

    #==================================

    #xsecs = get_extra_sections(pif, year)
    create_extra_lineup(pif, year, xsecs, verbose=pif.render.verbose)

    for lran in xsecs:
        lran['anchor'] = 'S' + lran['id'].replace('.', '')
        lran.update({
            'id': 'X_' + str(lran['display_order']),
            'graphics': [lran['img_format'][:2] + lup_region + 's%02d' % lran['display_order']]
        })
        lsec['range'].append(show_section(pif, lran, lran['mods'], 'X', year, comments))

    llineup['section'].append(lsec)
    llineup['tail'] = [pif.render.format_image_art('bamca_sm', also={'class': 'centered'}), '']
    llineup['tail'][1] += pif.render.format_button_comment(pif, 'yr=%s&rg=%s' % (pif.form_str('year'), pif.form_str('region')))
    for comment in comments:
        llineup['tail'][1] += mbdata.comment_designation[comment] + '<br>'
#    if int(year) > config.YEAR_START:
#       llineup['tail'][1] += pif.render.format_button("previous_year", link='http://www.bamca.org/cgi-bin/lineup.cgi?year=%s&region=%s' % (int(year) - 1, region))
#    if int(year) > config.YEAR_END:
#       llineup['tail'][1] += pif.render.format_button("following_year", link='http://www.bamca.org/cgi-bin/lineup.cgi?year=%s&region=%s' % (int(year) + 1, region))
    if pif.is_allowed('a'):  # pragma: no cover
        llineup['tail'][1] += 'multivars %s %s ' % (year, region) + ' '.join(multivars) + '<br>'
    return llineup


def run_multi_file(pif, year, region, nyears):
    pif.render.comment('lineup.run_multi_file', region, year, nyears)
    pages = pif.dbh.fetch_pages('id in (' + ','.join(["'year.%d'" % x for x in range(int(year), int(year) + nyears)]) + ')')

    modlistlist = []
    max_mods = 0
    y = int(year)
    nyears = len(pages)
    for page in pages:
        page['year'] = str(y)
        reg, lsec, secs, xsecs = get_man_sections(pif, str(y), region)
        page['region'] = reg
        page['sec'] = lsec
        page['img_format'] = lsec['img_format']
        page['mods'] = list(generate_man_lineup(pif, str(y), region))
        max_mods = max(max_mods, len(page['mods']))
        #print 'page', y, region, max_mods, '<br>'
        y += 1

    llineup = {'id': pif.page_id, 'section': [], 'name': '', 'tail': ''}
    lsec = pages[0]['sec']
    lsec['columns'] = nyears
    lsec['id'] = 'lineup'
    lsec['range'] = []
    hdr = lsec['name']

    #keylist = list(set(reduce(lambda x, y: x + y.keys(), modlistlist, [])))
    #keylist.sort()
    comments = set()

    lran = {'id': 'range', 'name': '', 'entry': [], 'note': '', 'graphics': []}
    pif.render.comment("run_file: range", lran)
    for inum in range(0, max_mods):
        #print 'mod num', inum, '<br>'
        for iyr in range(0, nyears):
            #print 'year', iyr, '<br>'
            pdir = pages[iyr]['page_info.pic_dir']
            ent = {'text': '', 'display_id': '', 'style': ''}
            if pages[iyr]['mods']:
                mdict = pages[iyr]['mods'].pop(0)
                mdict['disp_format'] = lsec.get('disp_format', '')
                mdict['shown_id'] = mdict['lineup_model.number']
                mdict['image_format'] = pages[iyr]['img_format']
                mdict['pdir'] = pdir
                mdict['anchor'] = '%d' % mdict['number']
                ent['text'] = show_lineup_model(pif, mdict, comments)
                ent['display_id'] = mdict.get('lineup_model.style_id', 0)
                if int(year) + iyr == int(mdict['first_year']):
                    ent['class'] = 'newcasting'
            #print ent, '<br>'
            lran['entry'].append(ent)
    lsec['range'].append(lran)

    llineup['section'].append(lsec)
    llineup['tail'] += pif.render.format_button_comment(pif, 'yr=%s&rg=%s' % (pif.form_str('year'), pif.form_str('region')))
    for comment in comments:
        llineup['tail'] += mbdata.comment_designation[comment] + '<br>'
    #llineup['tail'] += pif.render.format_button("comment_on_this_page", link='../pages/comment.php?page=%s&yr=%s&rg=%s' % (pif.page_id, pif.form_str('year'), pif.form_str('region')), also={'class': 'comment'}, lalso=dict())
    return llineup


'''
# a lineup consists of a header (outside of the table) plus a set of sections, each in its own table.
#     id, name, section
# a section consists of a header (inside the table) plus a set of ranges.
#     id, name, anchor, columns, note, range
# a range consists of a header plus a set of entries.
#     id, name, anchor, note, entry
'''

def select_lineup(pif, region, year):
    pif.dump(True)
    regs = 'URDBAL'
    checked = {True: ' CHECKED', False: ''}
    ostr = '<form>\n'
    #ostr = '<input type="hidden" name="verbose" value="1">\n'
    ostr += pif.render.format_table_start()
    irow = 0
    ostr += pif.render.format_row_start()
    ostr += pif.render.format_cell_start()
    years = pif.dbh.fetch_lineup_years()
    for yr in years:
        y = int(yr['year'])
        ostr += '<input type="radio" name="year" value="%d"%s>%d<br>\n' % (y, checked[int(year) == y], y)
        irow += 1
        if irow == 15:
            irow = 0
            ostr += pif.render.format_cell_end()
            ostr += pif.render.format_cell_start()
    ostr += pif.render.format_cell_end()
    ostr += pif.render.format_cell_start()
    for reg in regs:
        ostr += '<input type="radio" name="region" value="%s"%s>%s<br>\n' % (reg, checked[reg == region], mbdata.regions[reg])
    ostr += '<p>' + pif.render.format_button_input()
    ostr += pif.render.format_cell_end()
    ostr += pif.render.format_row_end()
    ostr += pif.render.format_table_end()
    ostr += '</form>'
    return ostr


def count_lineup_model(pif, mdict):
    ostr = ''

    if mdict:
        mdict = pif.dbh.depref('base_id', mdict)

        if mdict['casting.id']:
            mdict['product'] = ''
            if mdict['lineup_model.picture_id']:
                mdict['product'] = mdict['lineup_model.picture_id']
            elif mdict.get('image_format'):
                mdict['product'] = mdict['image_format'] % mdict['lineup_model.number']
            #pif.render.verbose = 0
            if pif.render.find_image_file([mdict['product']], suffix='jpg', pdir=mdict['pdir']):
                #pif.render.verbose = 0
                return 1
            #pif.render.verbose = 0
    return 0


def count_section(pif, lsec, lran, mods, region, year):
    im_count = pr_count = 0
    for mdict in mods:
        mdict['image_format'] = lran['img_format']
        pdir = pif.render.pic_dir
        if lran.get('pic_dir'):
            pdir = lran['pic_dir']
        mdict['pdir'] = pdir
        pr_count += 1
        im_count += count_lineup_model(pif, mdict)
    return pr_count, im_count


def picture_count(pif, region, year):
    pr_count = im_count = 0
    region, year = correct_region(region, year)
    llineup = {'id': region, 'section': [], 'name': '', 'tail': []}

    region, lsec, secs, xsecs = get_man_sections(pif, year, region)
    if not region:
        return 0

    modlist = list(generate_man_lineup(pif, year, region))

    endv = len(modlist)
    for sec in reversed(secs):
        sec['end'] = endv
        endv = sec['start']

    lsec['id'] = region
    lsec['range'] = []

    if secs:
        for lran in secs:
            lran.update({
                'id': region + '_' + str(lran['display_order']),
                'entry': [],
                'graphics': [lran['img_format'][:2] + region + 's%02d' % lran['display_order']]
            })
            count = count_section(pif, lsec, lran, modlist[lran['start']:lran['end']], region, year)
            pr_count += count[0]
            im_count += count[1]
    else:
        lran = copy.deepcopy(lsec)
        lran.update({'id': region + '_1', 'name': '', 'entry': [], 'note': '', 'graphics': []})
        count = count_section(pif, lsec, lran, modlist, region, year)
        pr_count += count[0]
        im_count += count[1]

    #==================================

    #xsecs = get_extra_sections(pif, year)
    create_extra_lineup(pif, year, xsecs, verbose=pif.render.verbose)

    for lran in xsecs:
        lran.update({
            'id': 'X_' + str(lran['display_order']),
            'entry': [],
            'graphics': [lran['img_format'][:2] + region + 's%02d' % lran['display_order']]
        })
        count = count_section(pif, lsec, lran, lran['mods'], 'X', year)
        pr_count += count[0]
        im_count += count[1]
    return pr_count, im_count


def product_pic_lineup_main(pif):
    pif.render.title = str(pif.form_str('region', 'Matchbox')) + ' Lineup'
    print pif.render.format_head()
    llineup = run_product_pics(pif, pif.form_str('region').upper())
    print pif.render.format_lineup(llineup)


def rank_lineup_main(pif):
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/lineup.cgi', 'Annual Lineup')
    pif.render.hierarchy_append('/cgi-bin/lineup.cgi?n=1&num=%s&region=%s&syear=%s&eyear=%s' % (pif.form_str('num'), pif.form_str('region'), pif.form_str('syear'), pif.form_str('eyear')),
        "%s #%d" % (mbdata.regions.get(pif.form_str('region'), ''), pif.form_int('num')))
    pif.render.title = str(pif.form_str('year', 'Matchbox')) + ' Lineup'
    print pif.render.format_head()
    llineup = run_ranks(pif, pif.form_int('num'), pif.form_str('region', 'U').upper(), pif.form_str('syear', '1953'), pif.form_str('eyear', '2014'))
    print pif.render.format_lineup(llineup)


def multiyear_main(pif):
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/lineup.cgi', 'Annual Lineup')
    pif.render.hierarchy_append('/cgi-bin/lineup.cgi?year=%s&region=%s' % (pif.form_str('year'), pif.form_str('region')),
        pif.form_str('year', '') + ' ' + mbdata.regions.get(pif.form_str('region'), ''))
    pif.render.title = str(pif.form_str('year', 'Matchbox')) + ' Lineup'
    print pif.render.format_head()
    llineup = run_multi_file(pif, pif.form_str('year'), pif.form_str('region').upper(), pif.form_int('nyears'))
    print pif.render.format_lineup(llineup)


def lineup_main(pif):
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/lineup.cgi', 'Annual Lineup')
    pif.render.hierarchy_append('/cgi-bin/lineup.cgi?year=%s&region=%s' % (pif.form_str('year'), pif.form_str('region')),
        pif.form_str('year', '') + ' ' + mbdata.regions.get(pif.form_str('region'), ''))
    pif.render.title = str(pif.form_str('year', 'Matchbox')) + ' Lineup'
    print pif.render.format_head()
    llineup = run_file(pif, pif.form_str('region').upper(), pif.form_str('year'))
    print pif.render.format_lineup(llineup)


@basics.web_page
def main(pif):
    pif.render.print_html()

    if pif.form_has('prodpic'):
        product_pic_lineup_main(pif)
    elif pif.form_int('n'):
        rank_lineup_main(pif)
    elif pif.form_int('nyears', 1) > 1:
        multiyear_main(pif)
    elif pif.form_str('region') and pif.form_str('year'):
        lineup_main(pif)
    else:
        print select_lineup(pif, pif.form_str('region', 'W').upper(), pif.form_str('year', '0'))
        pif.render.title = str(pif.form_str('year', 'Matchbox')) + ' Lineup'
        print pif.render.format_head()
    print pif.render.format_tail()

#--------- text lineup -----------------------------

def text_main(pif, year, region):
    return run_text_file(pif, region.upper(), year)


def show_text_lineup_main(pif, mdict, verbose=0):
    ostr = ''

    if mdict:
        mdict = pif.dbh.depref('base_id', mdict)
        mdict.setdefault('make', '')

        mdict['name'] = str(mdict.get('rawname', '')).replace(';', ' ')
        mdict['iconname'] = pif.dbh.icon_name(mdict['rawname'])
        mdict['unlicensed'] = {'unl': '-', '': '?'}.get(mdict.get('casting.make', ''), ' ')
        mdict.setdefault('description', '')
        mdict['descs'] = filter(lambda x: x, str(mdict['description']).split(';'))
        if not mdict['flags']:
            mdict['flags'] = 0
        mdict['made'] = not (mdict['flags'] & pif.dbh.FLAG_MODEL_NOT_MADE)
        mdict['notmade'] = {True: '', False: '*'}[mdict['made']]
        #mdict['link'] = linkurl[linky]
        #mdict['linkid'] = mdict.get('mod_id', mdict.get('id'))
        mdict['casting_type'] = mbdata.casting_types.get(mdict.get('model_type', 'SF'), 'Casting')

        imglist = []
        mdict['varlist'] = []
        if mdict.get('lineup_model.mod_id'):
            imglist.append(mdict['lineup_model.mod_id'])
            for var in mdict.get('vars', []):
                if var[2]:
                    mdict['varlist'].append(var[2])
                elif var[0]:
                    mdict['varlist'].append(var[0])
        pif.render.comment('varlist', mdict['varlist'])
        mdict['imgstr'] = pif.render.format_image_required(imglist, prefix='s_', vars=mdict['varlist'], pdir=config.IMG_DIR_MAN)
        mdict['product'] = ''

        mdict['name'] = mdict['lineup_model.name']
        mdict['mod_id'] = mdict['lineup_model.mod_id']
        mdict['ref_id'] = mdict['vs.ref_id']
        mdict['sub_id'] = mdict['vs.sub_id']
        mdict['descriptions'] = [x[1] for x in mdict['vars']]
        mdict['href'] = ""
        if mdict['casting.id']:
            if mdict['lineup_model.picture_id']:
                mdict['product'] = mdict['lineup_model.picture_id']
            elif mdict.get('image_format'):
                mdict['product'] = mdict['image_format'] % mdict['lineup_model.number']
            if pif.render.find_image_file([mdict['product']], suffix='jpg', pdir=mdict['pdir']):
                mdict['is_product_picture'] = 1
            mdict['href'] = "single.cgi?dir=%(pdir)s&pic=%(product)s&ref=%(ref_id)s&sub=%(sub_id)s&id=%(mod_id)s" % mdict
            if mdict['imgstr'].find('-') < 0:
                mdict['no_specific_image'] = 1
            if len(mdict['varlist']) < 1:
                mdict['no_variation'] = 1
        elif mdict['pack.id']:
            if mdict['lineup_model.picture_id']:
                mdict['product'] = mdict['lineup_model.picture_id']
            elif mdict.get('image_format'):
                mdict['product'] = mdict['image_format'] % mdict['pack.id']
            if pif.render.format_image_sized([mdict['product']], pdir=mdict['pdir'], largest='g'):
                mdict['is_product_picture'] = 1
            mdict['href'] = "packs.cgi?page=%(pack.page_id)s&id=%(pack.id)s" % mdict
        elif mdict['publication.id']:
            mdict['product'] = mdict['publication.id'] + '_01'
            if pif.render.format_image_sized([mdict['product']], pdir=mdict['pdir'], largest='g'):
                mdict['is_product_picture'] = 1
            mdict['href'] = "pub.cgi?id=%(publication.id)s" % mdict
        #mdict: imgstr name number pdir product vars
        ostr = models.add_model_text_line(pif, mdict)
    return ostr


def show_text_section(pif, lsec, lran, mods, lup_region, year):
    ostr = ''
    for mdict in mods:
        mdict['disp_format'] = lran.get('disp_format', '')
        if lran['flags'] & pif.dbh.FLAG_SECTION_DEFAULT_IDS:
            mdict['shown_id'] = pif.dbh.default_id(mdict['lineup_model.mod_id'])
            mdict['disp_format'] = '%s.'
        else:
            mdict['shown_id'] = mdict['lineup_model.number']
        mdict['image_format'] = lran['img_format']
        pdir = pif.render.pic_dir
        if lran.get('pic_dir'):
            pdir = lran['pic_dir']
        mdict['pdir'] = pdir
        if lup_region == 'X':
            mdict['anchor'] = 'X%d' % mdict['number']
        else:
            mdict['anchor'] = '%d' % mdict['number']
        ent = {
            'text': show_text_lineup_main(pif, mdict),
            'display_id': mdict.get('lineup_model.style_id', 0),
            'st_suff': '', 'style': ''
        }
        ostr += ent['text']
        if not (lran['flags'] & pif.dbh.FLAG_SECTION_NO_FIRSTS) and year == mdict['first_year']:
            ent['class'] = 'newcasting'
        lran['entry'].append(ent)
    lsec['range'].append(lran)
    return ostr


def run_text_file(pif, region, year):
    ostr = ''
    lup_region, year = correct_region(region, year)
    llineup = {'id': lup_region, 'section': [], 'name': '', 'tail': []}

    lup_region, lsec, secs, xsecs = get_man_sections(pif, year, region)
    if not lup_region:
        return ostr

    modlist = list(generate_man_lineup(pif, year, lup_region))

    endv = len(modlist)
    for sec in reversed(secs):
        sec['end'] = endv
        endv = sec['start']

    lsec['id'] = lup_region
    lsec['range'] = []
    hdr = lsec['name']

    if secs:
        for lran in secs:
            lran.update({
                'id': lup_region + '_' + str(lran['display_order']),
                'entry': [],
                'graphics': [lran['img_format'][:2] + lup_region + 's%02d' % lran['display_order']]
            })
            ostr += show_text_section(pif, lsec, lran, modlist[lran['start']:lran['end']], lup_region, year)
    else:
        lran = copy.deepcopy(lsec)
        lran.update({'id': lup_region + '_1', 'name': '', 'entry': [], 'note': '', 'graphics': []})
        ostr += show_text_section(pif, lsec, lran, modlist, lup_region, year)

    #==================================

    #xsecs = get_extra_sections(pif, year)
    create_extra_lineup(pif, year, xsecs, verbose=pif.render.verbose)

    for lran in xsecs:
        lran['anchor'] = 'S' + lran['id'].replace('.', '')
        lran.update({
            'id': 'X_' + str(lran['display_order']),
            'entry': [],
            'graphics': [lran['img_format'][:2] + lup_region + 's%02d' % lran['display_order']]
        })
        ostr += show_text_section(pif, lsec, lran, lran['mods'], 'X', year)

    llineup['section'].append(lsec)
    llineup['tail'] = [pif.render.format_image_art('bamca_sm'), '']
    llineup['tail'][1] += pif.render.format_button_comment(pif, 'yr=%s&rg=%s' % (pif.form_str('year'), pif.form_str('region')))
#    if int(year) > config.YEAR_START:
#       llineup['tail'][1] += pif.render.format_button("previous_year", link='http://www.bamca.org/cgi-bin/lineup.cgi?year=%s&region=%s' % (int(year) - 1, region))
#    if int(year) > config.YEAR_END:
#       llineup['tail'][1] += pif.render.format_button("following_year", link='http://www.bamca.org/cgi-bin/lineup.cgi?year=%s&region=%s' % (int(year) + 1, region))
    return ostr


#--------- ranks -----------------------------------

def generate_rank_lineup(pif, rank, region, syear, eyear):
    verbose = pif.render.verbose
    lmodlist = pif.dbh.fetch_lineup_models_by_rank(rank, syear, eyear)
    lmodlist.sort(key=lambda x: x['lineup_model.year'])
    regionlist = mbdata.get_region_tree(region)
    if verbose:  # pragma: no cover
        print regionlist, '<br>'
    years = dict()
    for mod in lmodlist:
        if verbose:  # pragma: no cover
            print '<hr>', mod
        mod['number'] = int(mod['lineup_model.year'])
        if mod['lineup_model.region'] and mod['lineup_model.region'] not in regionlist:
            if verbose:  # pragma: no cover
                print 'dropreg<br>'
        elif not mod['vs.sub_id'] or mod['lineup_model.region'] == mod['vs.sub_id']:
            years.setdefault(mod['number'], dict())
            years[mod['number']].setdefault(mod['lineup_model.region'], [])
            years[mod['number']][mod['lineup_model.region']].append(mod)
            if verbose:  # pragma: no cover
                print 'keep', mod['number'], mod['lineup_model.region'], '<br>'
        elif verbose:  # pragma: no cover
            print 'drop<br>'
    if verbose:  # pragma: no cover
        print '<hr>'

    lmoddict = dict()
    keys = years.keys()
    keys.sort()
    for year in keys:
        if verbose:  # pragma: no cover
            print year, '<br>'
        #reg, year = correct_region(region, year)
        reg = region

        for line_reg in regionlist:
            if verbose:  # pragma: no cover
                print '<b>', year, line_reg, '</b><br>'
            mod_list = years[year].get(line_reg, [])
            for reg in regionlist:
#               if year in lmoddict:
#                   if verbose:  # pragma: no cover
#                       print "completed %s/%s<br>" % (year, reg)
#                   break
                for mod in mod_list:
                    set_var(mod, lmoddict, reg, 'year.%s' % year, verbose)
        if year in lmoddict:
            if verbose:  # pragma: no cover
                print 'yield', lmoddict[year], '<br>'
            yield lmoddict[year]
            if verbose:  # pragma: no cover
                print '<br>'


def gather_rank_pages(pif, pages, region):
    region_list = mbdata.get_region_tree(region)
    sections = pif.dbh.fetch_sections(where="page_id like 'year.%'")
    sections = [pif.dbh.depref('section', x) for x in sections]
    sections = filter(lambda x: x['id'][0] in region_list, sections)
    sections.sort(key=lambda x: x['start'], reverse=True)
    for rg in region_list:
        for page in pages:
            pages[page].setdefault('section', list())
            for section in sections:
                if section['id'][0] == rg and section['page_id'] == page:
                    pages[page]['section'].append(section)
    # now each page should have the right sections and in the right order
    # the first section found where start < num is the right one


def get_product_image(page, mnum):
    if page:
        for section in page['section']:
            if section['start'] < mnum:
                return section['img_format'], page['page_info.pic_dir']
    return 'xxx%02d', 'unknown'


def run_ranks(pif, mnum, region, syear, eyear):
    if not mnum:
        print 'Lineup number must be a number from 1 to 120.  Please back up and try again.'
        print '<meta http-equiv="refresh" content="10;url=/database.php">'
        return dict()
    pif.render.comment('lineup.run_ranks', mnum, region, syear, eyear)

    pages = {x['page_info.id']: x for x in pif.dbh.fetch_page_years()}
    gather_rank_pages(pif, pages, region)

    lmodlist = generate_rank_lineup(pif, mnum, region, syear, eyear)

    llineup = {'id': pif.page_id, 'section': [], 'name': '', 'tail': ''}
    lsec = {'columns': 5, 'id': 'lineup', 'range': []}
    hdr = "Number %s" % mnum
    comments = set()

    lran = {'id': 'range', 'name': '', 'entry': [], 'note': '', 'graphics': []}
    pif.render.comment("run_ranks: range", lran)
    for mdict in lmodlist:
        if mdict:
            ifmt, pdir = get_product_image(pages.get(mdict.get('lineup_model.page_id', ''), {}), mnum)
            #mdict['number'] = mnum
            mdict['disp_format'] = '%s.'
            mdict['shown_id'] = mdict['lineup_model.year']
            mdict['image_format'] = ifmt
            mdict['pdir'] = pdir
            mdict['anchor'] = '%d' % mdict['number']
            ent = {
                'text': show_lineup_model(pif, mdict, comments, 1),
                'display_id': '0', 'style': ''
            }
            if mdict['lineup_model.year'] == mdict['first_year']:
                ent['class'] = 'newcasting'
            lran['entry'].append(ent)
        else:
            lran['entry'].append({'text': '', 'display_id': ''})
    lsec['range'].append(lran)

    llineup['section'].append(lsec)
    llineup['tail'] = [pif.render.format_image_art('bamca_sm'), '']
    #llineup['tail'][1] += pif.render.format_button("comment_on_this_page", link='../pages/comment.php?page=%s&yr=%s&rg=%s' % (pif.page_id, pif.form_str('year'), pif.form_str('region')), also={'class': 'comment'}, lalso=dict())
    llineup['tail'][1] += pif.render.format_button_comment(pif, 'yr=%s&rg=%s' % (pif.form_str('year'), pif.form_str('region')))
    for comment in comments:
        llineup['tail'][1] += mbdata.comment_designation[comment] + '<br>'
    return llineup


#--------- prodpics --------------------------------

def run_product_pics(pif, region):
    halfstars = dict()
    if os.path.exists('pic/multivars.dat'):
        for ln in open('pic/multivars.dat').readlines():
            ln = ln.strip().split()
            if len(ln) > 1 and ln[1] == region:
                halfstars[ln[0]] = [int(x) for x in ln[2:]]
    pages = pif.dbh.fetch_page_years()
    if pif.form_str('syear'):
        pages = filter(lambda x: x['page_info.id'] >= 'year.' + pif.form_str('syear'), pages)
    if pif.form_str('eyear'):
        pages = filter(lambda x: x['page_info.id'] <= 'year.' + pif.form_str('eyear'), pages)
    pages = {x['page_info.id']: x for x in pages}
    gather_rank_pages(pif, pages, region)
    region_list = mbdata.get_region_tree(region)

    llineup = {'id': pif.page_id, 'section': [], 'name': '', 'tail': ''}
    lsec = {'columns': 1, 'id': 'lineup', 'range': []}
    hdr = ""
    comments = set()

    keys = pages.keys()
    keys.sort()
    for page in keys:
        lmodlist = pif.dbh.fetch_simple_lineup_models(page[5:], region)
        lmodlist = filter(lambda x: x['lineup_model.region'][0] in region_list, lmodlist)
        lmoddict = {x['lineup_model.number']: x for x in lmodlist}
        min_num = 1
        max_num = pages[page]['max(lineup_model.number)']
        if pif.form_str('num'):
            min_num = pif.form_int('num')
        if pif.form_str('enum'):
            max_num = pif.form_int('enum')
        lsec['columns'] = max(lsec['columns'], max_num + 1)
        lran = {'id': pages[page]['page_info.id'], 'name': '', 'entry': [], 'note': '', 'graphics': []}
        ent = {
            'text': page[5:],
            'display_id': '1', 'style': ''
        }
        lran['entry'].append(ent)
        for mnum in range(min_num, max_num + 1):
            ifmt, pdir = get_product_image(pages[page], mnum)
            lmod = lmoddict.get(mnum, {})
            lpic_id = pic_id = lmod.get('lineup_model.picture_id')
            if pic_id:
                lpic_id = pic_id = pic_id.replace('W', region)
                product_image = pif.render.find_image_file(pic_id, suffix='jpg', pdir=pdir)
            else:
                lpic_id = ifmt % mnum
                product_image = pif.render.find_image_file([ifmt % mnum], suffix='jpg', pdir=pdir)
            #http://www.bamca.org/cgi-bin/single.cgi?dir=pic/univ&pic=1982u05&ref=year.1982&sub=&id=MB005
            lnk = "single.cgi?dir=%s&pic=%s&ref=%s&sub=%s&id=%s" % (pdir, lpic_id, page, '', lmod.get('lineup_model.mod_id', ''))
            #def format_link(self, url, txt, args={}, nstyle=None, also={}):
            ent = {
                'text': pif.render.format_link(lnk, images.image_star(pif, product_image, pic_id, mnum in halfstars.get(page[5:], []))),
                'display_id': str(int(mnum % 10 == 0 or page[-1] == '0'))
            }
            lran['entry'].append(ent)
        lsec['range'].append(lran)

    llineup['section'].append(lsec)
    return llineup


# -------- mack ------------------------------------


def show_mack_model(pif, mod):
    # id, man_id, imgstr, name
    mdict = {'id': mod['mack_id'], 'man_id': mod['mod_id'], 'name': mod['name'].strip(),
        'imgstr': pif.render.format_image_required('s_' + mod['mod_id'])
    }
    return models.add_model_link(pif, mdict)


# missing 51s
#id_re = re.compile('(?P<p>\D*)(?P<n>\d*)(?P<l>\D*)')
def lineup_to_mack(pif, start, end, series):
    # mack_id, mod_id, name
    if 'RW' in series:
        if 'SF' in series:
            series = None
        else:
            series = ''
    else:
        series = 'MB'
    rwmods = pif.dbh.fetch_casting_list('rw')
    sfmods = pif.dbh.fetch_casting_list('sf')
    aliases = pif.dbh.fetch_aliases()
    mack = dict()
    for alias in aliases:
        mod_to_mack(mack, alias, 'alias.id', start, end, series)
    for sfmod in sfmods:
        mod_to_mack(mack, sfmod, 'base_id.id', start, end, series)
    for rwmod in rwmods:
        mod_to_mack(mack, rwmod, 'base_id.id', start, end, series)
    return mack


def mod_to_mack(mack, rec, key, start, end, series):
    mack_id = mbdata.get_mack_number(rec[key])
    if not mack_id:
        return
    if int(mack_id[1]) < start:
        return
    if int(mack_id[1]) > end:
        return
    if series is not None and series != mack_id[0]:
        return
    mack_id_fmt = '%s%02s-%s' % mack_id
    mack[mack_id] = {
        'mack_id': mack_id_fmt.upper(),
        'mack_id_unf': mack_id,
        'mod_id': rec['base_id.id'],
        'name': rec['base_id.rawname'].replace(';', ' ')
    }



@basics.web_page
def mack_lineup(pif):
    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append(pif.request_uri, 'Mack Numbers')
    pif.render.print_html()
    region = pif.form_str('region', 'U')
    series = pif.form_str('sect', 'all')
    if series == 'all':
        series = ['RW', 'SF']
    else:
        series = [series.upper()]
    range = pif.form_str('range', 'all')
    start = pif.form_int('start', 1)
    end = pif.form_int('end', 100)
    if range == 'all':
        start = 1
        end = 100

    print pif.render.format_head()

    lsec = pif.dbh.depref('section', pif.dbh.fetch_sections({'page_id': pif.page_id})[0])
    mods = lineup_to_mack(pif, start, end, series)

    modids = mods.keys()
    modids.sort(key=lambda x: (mods[x]['mack_id_unf'][1], mods[x]['mack_id_unf'][0], mods[x]['mack_id_unf'][2]))

    llineup = {'section': [], 'note': ''}
    lsec['range'] = []
    ran = {'entry': []}
    if modids:
        for mod in modids:
            ran['entry'].append({'text': show_mack_model(pif, mods[mod])})
    else:
        llineup['note'] = 'Your request produced no models.'
        if start > 100:
            llineup['note'] += '  Be sure to use numbers from 1 to 100.'
        if start > end:
            llineup['note'] += "  Use a start number that isn't higher than the end number."
    lsec['range'].append(ran)
    llineup['section'].append(lsec)

    print pif.render.format_lineup(llineup)
    #print pif.render.format_button("comment_on_this_page", link='../pages/comment.php?page=%s&rg=%s&sec=%s&start=%s&end=%s' % (pif.page_id, pif.form_str('region', ''), pif.form_str('sect', ''), pif.form_str('start', ''), pif.form_str('end', '')), also={'class': 'comment'}, lalso=dict())
    print pif.render.format_button_comment(pif, 'rg=%s&sec=%s&start=%s&end=%s' % (pif.form_str('region', ''), pif.form_str('sect', ''), pif.form_str('start', ''), pif.form_str('end', '')))
    print pif.render.format_tail()


# -------- makes -----------------------------------


@basics.web_page
def makes_main(pif):
    makelist = [(x['vehicle_make.make'], x['vehicle_make.make_name']) for x in pif.dbh.fetch_vehicle_makes()]
    makedict = dict(makelist + [('unl', 'Unlicensed'), ('', 'Unknown')])
    make = pif.form_str('make', '')
    makes = [make]

    pif.render.hierarchy_append('/', 'Home')
    pif.render.hierarchy_append('/database.php', 'Database')
    pif.render.hierarchy_append('/cgi-bin/makes.cgi', 'Models by Make')
    if make == 'text':
        pif.render.hierarchy_append(pif.request_uri, 'Search')
    elif make:
        pif.render.hierarchy_append(pif.request_uri, makedict.get(make, make))
    pif.render.print_html()
    print pif.render.format_head()

    if make == 'text':
        makename = pif.form_str('text')
        if makename:
            makes = []
            for m in makelist:
                if m[1].lower().startswith(makename.lower()):
                    makes.append(m[0])
            if not makes:
                makes = ['unk']
        else:
            make = ''

    if make:
        llineup = show_makes(pif, makedict, makes)
        print pif.render.format_lineup(llineup)
    else:
        print makes_form(pif, makelist)
    print pif.render.format_button_comment(pif, 'make=%s&text=%s' % (pif.form_str('make', ''), pif.form_str('text', '')))
    print pif.render.format_tail()


def makes_form(pif, makelist):
    cols = 5
    makelist.sort(key=lambda x: x[1])
    rows = ((len(makelist) + 1) / cols) + 1
    ostr = '<center><h2>Matchbox 1-75 Models By Make</h2></center><hr>'
    ostr += 'Choose a make:<br><form>'
    ostr += '<table width="100%%"><tr><td width="%d%%" valign="top">' % (100/cols)
    ostr += '<input type="radio" name="make" value="unk" checked>unknown<br>'
    i = rows - 1
    for ent in [['unl', 'unlicensed']] + makelist:
        ostr += ' <input type="radio" name="make" value="%s">%s' % tuple(ent)
        if pif.is_allowed('a'):  # pragma: no cover
            ostr += ' - ' + ent[0]
        ostr += '<br>'
        i = i - 1
        if i == 0:
            ostr += '</td><td width="%d%%" valign="top">' % (100/cols)
            i = rows
    ostr += '</td></tr></table><hr>'
    ostr += pif.render.format_button_input('see the models')
    ostr += '</form>'
    return ostr


def show_make_selection(pif, make_id, make_dict):
    casting_make = make_id
    if make_id == 'unk':
        casting_make = ''
    lsec = dict()  #pif.dbh.fetch_sections({'page_id': pif.page_id})[0]
    lsec['anchor'] = make_id
    lsec['range'] = []
    lsec['note'] = ''
    lsec['id'] = ''
    lsec['name'] = make_dict.get(make_id, make_id)
    lran = {'id': '', 'name': '', 'anchor': '', 'note': '', 'entry': []}
    castings = pif.dbh.fetch_casting_list(where=["casting.make='%s'" % casting_make, "section.page_id='manno'"])
    aliases = []  #pif.dbh.fetch_aliases(where="casting.make='%s'" % casting_make)
    mlist = []

    for mdict in castings:
        mlist.append(pif.dbh.modify_man_item(mdict))

    for mdict in aliases:
        mdict = pif.dbh.modify_man_item(mdict)
        if mdict.get('alias.ref_id'):
            mdict['picture_id'] = mdict['id']
            mdict['id'] = mdict['alias.id']
            #mdict['descs'] = mdict['descs']
            #mdict['descs'].append('same as ' + mdict['ref_id'])
        mlist.append(mdict)

    mlist.sort(key=lambda x: x['name'])
    for mdict in mlist:
        # input mdict:  id, (picture_id), made, country, link, linkid, name, descs, made, unlicensed, scale, (type)
        lran['entry'].append({'text': models.add_model_table_pic_link(pif, mdict, flago=models.flago)})

    lsec['range'].append(lran)
    return lsec


def show_makes(pif, makedict, makes):
    llineup = {'id': '', 'name': '', 'section': []}
    models.flago = mflags.FlagList(pif)

    for make_id in makes:
        lsec = show_make_selection(pif, make_id, makedict)
        llineup['section'].append(lsec)
    return llineup


# -------- mline -----------------------------------


# Kill it with a stick!
@basics.web_page
def full_lineup(pif):
    pif.render.print_html()
    #pif.ReadForm({'year': '1966'})
    year = pif.form_int('year')

    dblist = bfiles.SimpleFile(os.path.join(config.SRC_DIR, 'mbx.dat'))

    print pif.render.format_head()

    shown = 0
    dirs = dict()

    llineup = {'id': pif.page_id, 'name': "Matchbox Lineup for %d" % year, 'graphics': [], 'section': []}
    ostr = ''

    for llist in dblist:
        cmd = llist.get_arg('', 0)
        if cmd == 'dir':
            dirs[llist.get_arg(start=1)] = llist.get_arg(start=2)
            continue

        startyear = int(llist.get_arg('0', 1))
        endyear = int(llist.get_arg('0', 2))
        modno = llist.get_arg('0', 3)
        rank = int(llist.get_arg('0', 4))
        title = llist.get_arg('', 5)
        desc = llist.get_arg('', 6)

        if year < startyear or year > endyear:
            continue

        if cmd == 'H':
            if rank and pif.form_int(modno):
                if shown:
                    ostr += "</tr></table></center>"
                ostr += "<h3><center>" + title + "</center></h3>"
                shown = 0
                cols = int(rank)
        elif pif.form_str(cmd, '0') != '1':
            pass
        elif cmd == 'CAT':
            llineup['graphics'].append({'file': cmd + modno})
            ostr += "<center><table>"
            ostr += " <tr align=top><td><center>%s</td></tr>" % pif.render.format_image_required([cmd + modno], pdir=dirs.get(cmd))
            ostr += "</table></center>"
            shown = 0
        else:
            if shown == 0:
                ostr += "<center><table><tr align=top>"
            shown += 1

            modelid = ''
            if cmd == 'MB' or cmd == 'RW':
                modelid = "%d" % int(modno)
            elif not (cmd == 'E' or cmd == 'PZL'):
                modelid = "%s-%d" % (cmd, int(modno))

            # id, man_id, imgstr, is_new, name
            mdict = {'id': '', 'man_id': modelid, 'imgstr': '', 'is_new': 0, 'name': ''}
            ostr += " <td valign=top width=%d><center><b>%s</b><br>" % (width[cols], modelid)
            if cmd == 'RW':
                ostr += '<a href="single.cgi?dir=%s&pic=%sw%s&id=%s">%s</a><br>' %\
                    (pif.render.pic_dir, str(year)[2:], modno, cmd + modno + ver_no(int(rank)), pif.render.format_image_required(['s_' + cmd + modno + ver_no(int(rank))], pdir=dirs.get(cmd)))
            else:
                ostr += '%s<br>' %\
                    (pif.render.format_image_required([cmd + modno + ver_no(int(rank)), 's_' + cmd + modno + ver_no(int(rank))], pdir=dirs.get(cmd)))
            if year == startyear:
                ostr += pif.render.format_image_art('new') + ' '
            ostr += title + "</center></td>"
            if (shown == cols):
                ostr += "</tr></table></center>"
                shown = 0

    if shown:
        ostr += "</tr></table></center>"

    ostr += '<hr>'  #'<a href=".">BACK to query</a>'
    ostr += '<p>'

    print ostr
    print pif.render.format_tail()


# --- -------------------------------------------------------------------


if __name__ == '__main__':  # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
