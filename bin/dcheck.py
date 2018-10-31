#!/usr/local/bin/python

import datetime, filecmp, glob, os, re, sys, urllib2
import basics
import config
import images
import imglib
import mannum
import mbdata
import useful

verbose = False


def count_tables(pif):
    for tab in pif.dbh.dbi.execute('show tables')[0]:
	cnts = pif.dbh.dbi.execute('select count(*) from ' + tab[0])
	print "%7d %s" % (cnts[0][0][0], tab[0])
	if pif.switch['v']:
	    cols = pif.dbh.dbi.execute('desc ' + tab[0])
	    for col in cols[0]:
		print ' ', col


def check_schema(pif):
    check_schema_db(pif, 'bamca')
    check_schema_db(pif, 'buser')


def check_schema_db(pif, db):
    tablelist = pif.dbh.dbi.execute('show tables in %s' % db)
    for table in tablelist[0]:
        table = table[0]
        print db, table, ':',
        if table in pif.dbh.table_info:
            desc = pif.dbh.dbi.execute('desc %s.%s' % (db, table))
            dbcols = set([x[0] for x in desc[0]])
            ticols = set(pif.dbh.table_info[table]['columns'] + pif.dbh.table_info[table].get('extra_columns', []))
            if dbcols != ticols:
                print "differ"
		print "  db:", sorted(dbcols - ticols)
		print "  ti:", sorted(ticols - dbcols)
            else:
                print "same"
        else:
            print "missing from table_info"


# ------- check tables -------------------------------------------------

ok_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,?!/\'_()#":-%&;*|@<>=$+[]`\\^~'
#0 9 13
#133 145 146 148 150 220 174 178 180 188 194 195 196 201 204 209 214 217 226 228 229 232 233 235 239 169

def check_tables(pif, *filelist):
    if filelist:
	for tab in filelist:
	    check_table(pif, tab)
	    print
    else:
	#found_ch = set()
	tabs = pif.dbh.dbi.execute('show tables')
	for tab in tabs[0]:
	    tab = tab[0]
	    if tab == 'counter':
		continue
	    check_table(pif, tab)
	    print
	#print found_ch


def check_table(pif, tab):
    print tab
    rows = pif.dbh.dbi.execute('select * from ' + tab)[0]
    cols = [desc[0] for desc in pif.dbh.dbi.execute('desc ' + tab)[0]]
    #print cols
    #print rows[0][0]
    for row in rows:
	for icol in range(len(row)):
	    if isinstance(row[icol], long):
		continue
	    elif isinstance(row[icol], int):
		continue
	    elif row[icol] is None:
		continue
	    elif isinstance(row[icol], datetime.datetime):
		continue
	    elif isinstance(row[icol], datetime.timedelta):
		continue
	    elif isinstance(row[icol], str):
		for ch in row[icol]:
		    if not ch in ok_letters:
			print '  ', row
			#found_ch.add(ord(ch))
			break
	    else:
		print tab, cols[icol], row[icol], type(row[icol])

# ------- check dups ---------------------------------------------------

# check for duplicate entries in tables
# existing code silently smushes these so we need to look for them to clean them up

def check_dups(pif):
    check_matrix_model(pif)
    check_lineup_model(pif)
    check_detail(pif)


def check_q(rows):
    problems = set()
    for row in rows:
	if row[-1] > 1:
	    problems.add(row[:-1])
    print problems if problems else 'all ok'


def check_matrix_model(pif):
    print 'matrix_model'
    res = pif.dbh.raw_execute('''select page_id, section_id, range_id, count(*) from matrix_model group by page_id, section_id, range_id''')
    check_q(res[0])


def check_lineup_model(pif):
    print 'lineup_model'
    res = pif.dbh.raw_execute('''select page_id, region, number, count(*) from lineup_model group by page_id, region, number''')
    check_q(res[0])
    return
    problems = set()
    for row in res[0]:
	if row[3] > 1:
	    problems.add(row[:2])
    print problems if problems else 'all ok'


def check_detail(pif):
    print 'detail'
    res = pif.dbh.raw_execute('''select mod_id, var_id, attr_id, count(*) from detail group by mod_id, var_id, attr_id''')
    check_q(res[0])
    return
    problems = set()
    for row in res[0]:
	if row[3] > 1:
	    problems.add(row[:2])
    print problems


def check_base_id(pif):
    ids = pif.dbh.fetch_base_ids();
    for id in ids:
	rn = pif.dbh.icon_name(id['base_id.rawname'])
	if not rn or any([len(x) > 25 for x in rn]):
	    print id['base_id.id'], id['base_id.rawname'], '=>', rn
	if id['base_id.first_year'] is None or int(id['base_id.first_year']) < 1947 or int(id['base_id.first_year']) > 2015:
	    print id['base_id.id'], id['base_id.first_year'], 'not in bounds'
	if id['base_id.model_type'] not in mbdata.model_types:
	    print id['base_id.id'], id['base_id.model_type'], 'not in list'
	#small_pic = os.path.join(config.IMG_DIR_MAN, 's_' + id['base_id.id'].lower() + '.jpg')
	small_pic = os.path.join(*pif.render.find_image_file(pdir=config.IMG_DIR_MAN, prefix=mbdata.IMG_SIZ_SMALL, fnames=id['base_id.id']))
	#if not os.path.exists(small_pic):
	if not small_pic:
	    if not id['base_id.flags'] & pif.dbh.FLAG_MODEL_NOT_MADE:
		print id['base_id.id'], 'no pictures', small_pic
	else:
	    pic_size = imglib.get_size(small_pic)
	    if pic_size != (200, 120):
		print id['base_id.id'], 'bad size', pic_size
    print len(ids), 'entries checked'


def check_attribute_pictures(pif, *filelist):
    fl = os.listdir('.' + config.IMG_DIR_ADD)
    print sorted(list(set([x[0] for x in fl if x.endswith('.jpg')])))

    for pref in filelist:
	print pref
	pics = pif.dbh.fetch_attribute_pictures_by_type(pref)
#{'casting.section_id': 'sf', 'casting.country': 'US', 'attribute_picture.attr_type': 'b', 'attribute_picture.description': 'dark green', 'base_id.model_type': 'SF', 'casting.vehicle_type': 'ud', 'base_id.description': '', 'base_id.flags': 0L, 'attribute_picture.attr_id': 1L, 'attribute_picture.picture_id': 'dgrn', 'attribute_picture.mod_id': 'SF02b', 'base_id.id': 'SF02b', 'base_id.first_year': '1971', 'casting.scale': '1:59', 'casting.make': 'jee', 'casting.id': 'SF02b', 'casting.variation_digits': 2, 'attribute_picture.id': 5L, 'base_id.rawname': 'Jeep Hot Rod'}
	for pic in pics:
	    if pic['attribute_picture.picture_id']:
		pic_name = '%s_%s-%s.jpg' % (pic['attribute_picture.attr_type'], pic['attribute_picture.mod_id'].lower(), pic['attribute_picture.picture_id'])
	    else:
		pic_name = '%s_%s.jpg' % (pic['attribute_picture.attr_type'], pic['attribute_picture.mod_id'].lower())
	    if pic_name in fl:
		fl.remove(pic_name)
	    else:
		print 'no pic for', pic_name
	for fn in fl:
	    if fn.startswith(pref + '_') and fn.endswith('.jpg'):
		fn = fn[2:-4]
		mod_id, pic_id = fn.split('-', 1) if '-' in fn else [fn, '']
		rec = {'mod_id': mod_id, 'attr_id': 0, 'attr_type': pref, 'picture_id': pic_id, 'description': ''}
		print rec
		#pif.dbh.add_attribute_picture(rec)



#def run_models(pif, mods):
#    upics = spics = spfnd = cpics = cpfnd = mpics = mpfnd = apics = apfnd = 0
#    mods = [x[0] for x in mods]
#    mods.sort()
#
#    for mod in mods:
#        uf, af, mf, cf, sf = show_list_var_pics(pif, mod)
#        if (not pif.switch['q']) and \
#           (not pif.switch['s'] or sf[2] < 100) and \
#           (not pif.switch['c'] or cf[2] < 100) and \
#           (not pif.switch['m'] or mf[2] < 100) and \
#           (not pif.switch['a'] or af[2] < 100):
#            print '%-8s%5d | %3d/%3d |%3d%% | %3d/%3d |%3d%% | %3d/%3d |%3d%% | %3d/%3d |%3d%%' % ((mod, uf) + af + mf + cf + sf)
#
#        upics += uf
#        spics += sf[1]
#        spfnd += sf[0]
#        cpics += cf[1]
#        cpfnd += cf[0]
#        mpics += mf[1]
#        mpfnd += mf[0]
#        apics += af[1]
#        apfnd += af[0]
#
#    return upics, spics, spfnd, cpics, cpfnd, mpics, mpfnd, apics, apfnd
#
#
## oh FFS fix this.
#def show_list_var_pics(pif, mod_id):
#    # a = all, u = unique, s = w/ selects, c = core, m = code2?
#    upics = spics = spfnd = cpics = cpfnd = mpics = mpfnd = apics = apfnd = 0
#    varsels = pif.dbh.fetch_variation_selects(mod_id)
#    varsel = {}
#    for vs in varsels:
#        varsel.setdefault(vs['variation_select.ref_id'], [])
#        varsel[vs['variation_select.ref_id']].append(vs['variation_select.var_id'])
#    spics = len(varsel.keys())
#
#    vars = pif.dbh.fetch_variations(mod_id)
#    for var in vars:
#        isorig = 1
#        fn = mod_id + '-' + var['variation.var']
#        if var['variation.picture_id']:
#            fn = mod_id + '-' + var['variation.picture_id']
#            isorig = 0
#        fn = '.' + config.IMG_DIR_MAN + '/var/s_' + fn.lower() + '.jpg'
#        apics += 1
#        if not var['variation.var'].startswith('f'):
#            if not mbdata.categories.get(var['variation.category'], '').startswith('['):
#                mpics += 1
#            if not var['variation.category']:
#                cpics += 1
##        print '<!--', config.IMG_DIR_MAN + '/var/' + fn + '.jpg', '-->'
#        if os.path.exists(fn):
#            apfnd += 1
#            upics += isorig
#            if not var['variation.var'].startswith('f'):
#                if not mbdata.categories.get(var['variation.category'], '').startswith('['):
#                    mpfnd += 1
#                if not var['variation.category']:
#                    cpfnd += 1
#            for vs in varsel:
#                if var['variation.var'] in varsel[vs]:
#                    spfnd += 1
#                    varsel[vs] = []
#    if verbose:
#        print ' '.join(filter(lambda x: varsel[x], varsel))
#    return upics, format_calc(apfnd, apics), format_calc(mpfnd, mpics), format_calc(cpfnd, cpics), format_calc(spfnd, spics)
#
#
#def format_calc(found, pics):
#    if 0:  # found == pics:
#        return (found, pics, '--')
#    if pics:
#        return (found, pics, 100 * found / pics)
#    return (0, 0, 100)
#
#
#def old_ckcas(pif):
#
#    upics = nmods = spics = spfnd = cpics = cpfnd = mpics = mpfnd = apics = apfnd = 0
#
#    if pif.switch['v']:
#        verbose = True
#    if pif.filelist:
#        for spec in pif.filelist:
#            mods = pif.dbh.dbi.execute("select distinct id from casting where id like '%s%%'" % spec)[0]
#            nmods += len(mods)
#            uf, sp, sf, cp, cf, mp, mf, ap, af = run_models(pif, mods)
#
#            upics += uf
#            spics += sp
#            spfnd += sf
#            cpics += cp
#            cpfnd += cf
#            mpics += mp
#            mpfnd += mf
#            apics += ap
#            apfnd += af
#
#    else:
#        mods = pif.dbh.dbi.execute("select distinct id from casting")[0]
#        nmods += len(mods)
#        uf, sp, sf, cp, cf, mp, mf, ap, af = run_models(pif, mods)
#
#        upics += uf
#        spics += sp
#        spfnd += sf
#        cpics += cp
#        cpfnd += cf
#        mpics += mp
#        mpfnd += mf
#        apics += ap
#        apfnd += af
#
#    print
#    print '%7d %5d  %3d/%3d %3d%%  %3d/%3d %3d%%  %3d/%3d %3d%%  %3d/%3d %3d%%' % \
#          ((nmods, upics) +
#           format_calc(apfnd, apics) + format_calc(mpfnd, mpics) + format_calc(cpfnd, cpics) + format_calc(spfnd, spics))

def check_castings(pif):
    #pif.form.set_val('section', 'all')
    sec_ids = [x['section.id'] for x in  pif.dbh.fetch_sections(where={'page_id': pif.page_id})]
    totals = {}
    tags = []
    for sec in sec_ids:
	pif.form.set_val('section', sec)
	manf = mannum.MannoFile(pif, withaliases=True)
	llineup = manf.run_picture_list(pif)
	for ent in  llineup['section'][0]['range'][0]['entry']:
	    pass
	disp = ['%-8s' % sec]
	for tot in llineup['totals']:
	    if tot['tag'] not in tags:
		tags.append(tot['tag'])
		totals[tot['tag']] = [0, 0]
	    totals[tot['tag']][0] += tot['have']
	    totals[tot['tag']][1] += tot['total']
	    disp.extend(['%7d ' % tot['have'], '%7d ' % tot['total']])
	print ''.join(disp)
    disp = ['totals  ']
    for tag in tags:
	disp.extend(['%7d ' % totals[tag][0], '%7d ' % totals[tag][1]])
    print ''.join(disp)


def show_categories(pif):
    vsels = pif.dbh.fetch_variation_select_counts(by_ref=True)
    refs = {}
    for vs in vsels:
	refs.setdefault(vs['variation_select.category'], set())
	if vs['variation_select.ref_id'] and vs['variation_select.category'] != 'MB':
	    refs[vs['variation_select.category']].add(vs['variation_select.ref_id'])
    cats = pif.dbh.fetch_category_counts()
    catl = [(x.id, x.name, 'shown' if (x.flags & 4) else '', 'c2' if (x.flags & 2) else '', x.count, ' '.join(sorted(refs.get(x.id, [])))) for x in cats]
    fmt = pif.dbh.preformat_results(catl)
    for cat in catl:
	print fmt % cat


def check_var_vs_categories(pif):
    wheres = ["variation_select.mod_id=variation.mod_id", "variation_select.var_id=variation.var"]
    vars = {}
    for vvs in pif.dbh.fetch('variation_select,variation', where=wheres, tag='VarVS'):
	key = (vvs['variation.mod_id'], vvs['variation.var'],)
	vars.setdefault(key, dict())
	vars[key]['vc'] = set(vvs['variation.category'].split(' ')) if vvs['variation.category'] else set()
	vars[key].setdefault('vsc', set())
	vars[key]['vsc'].add(vvs['variation_select.category'])
    vl = [key + (' '.join(sorted(vars[key]['vc'])), ' '.join(sorted(vars[key]['vsc'])),) for key in sorted(vars.keys()) if vars[key]['vc'] - vars[key]['vsc']]
    fmt = pif.dbh.preformat_results(vl)
    for v in vl:
	print fmt % v


def cat2matrix(pif, cat, page_id):
    #id base_id section_id display_order page_id range_id mod_id flags shown_id name subname description
    wheres = ["vs.mod_id=v.mod_id", "vs.var_id=v.var", "v.mod_id=b.id", "vs.category='%s'" % cat]
    seen = set()
    vars = {}
    print "base_id|section_id|display_order|page_id|range_id|mod_id|flags|shown_id|name|subname|description"
    fmt = "%s|%s|%2s|%s|%2s|%s|%s|%s|%s|%s|%s"
    ran_id = 1
    for vvs in pif.dbh.fetch('variation_select vs,variation v,base_id b', where=wheres, tag='VarVSCat'):
	iam = (vvs['v.mod_id'], vvs['v.text_description'])
	if iam not in seen:
	    print fmt % ("", cat.lower() + vvs['v.date'][2:4], ran_id, page_id, ran_id, vvs['v.mod_id'], 0, "", vvs['b.rawname'], '', vvs['v.text_description'])
	    ran_id += 1
	    seen.add(iam)


# variation fns to correllate category entries between variation and variation_select.
# variation.category is the old version and cannot be properly joined against.
# variation_select.category is the new version which should be able to replace it.
# vs.category will be useful without vs.ref_id and vs.sec_id so the rest of the site needs to tolerate that.

def check_vs_categories(pif):
    #check_vs(pif)
    long_form(pif)
    #correllation(pif)
    #l5p(pif)
    #by_ref(pif)


def check_vs(pif):
    print "check vs"
    res = pif.dbh.raw_execute('''select vs.*, v.* from variation_select vs left join variation v on vs.mod_id=v.mod_id and vs.var_id=v.var''')
    for ent in res[0]:
	if not ent[6]:
	    print ent[:6]
    print


def long_form(pif):
    print 'long form'
    vs = {}
    for res in pif.dbh.raw_execute('''select mod_id, var_id, category from variation_select''')[0]:
	vs.setdefault(res[0], dict())
	vs[res[0]].setdefault(res[1], set())
	vs[res[0]][res[1]].add(res[2])
    v = []
    for res in pif.dbh.raw_execute('''select mod_id,var,category from variation''')[0]:
	if res[2]:
	    vc = set(res[2].split(' '))
	    vsc = vs.get(res[0], {}).get(res[1], set())
	    if vc - vsc:
		vsc = ' '.join(sorted(vs.get(res[0], {}).get(res[1], [])))
		v.append(res + (vsc,))
    fmt = pif.dbh.preformat_results(v)
    for ent in v:
	print fmt % ent
    print


def l5p(pif):
    print 'licensed 5 packs'
    res = pif.dbh.raw_execute('''select v.category,vs.category from variation v,pack p,variation_select vs where 
p.page_id='packs.5packs' and
p.section_id='lic5packs' and
vs.ref_id=p.page_id and
vs.sec_id=p.id and
v.mod_id=vs.mod_id and
v.var=vs.var_id
''')
    vc = set()
    vsc = set()
    for r in res[0]:
	vc.add(r[0])
	vsc.add(r[1])
    print vc, '/', vsc
    print

''' unidentified
HP - True Heroes
MSN
SW - kingsize only
KP - kingsize only
MX - kingsize only
SC - skybusters only
CLR - yy only
'''

categories = {
    '10P'   : "10-Pack",
    '2K'    : "2000 Logo",
    '3P'    : "3-Pack",
    '50P'   : "50th Anniversary Collection",
    '5P'    : "5-Pack",
    '60'    : "60th Anniversary",
    '75C'   : "75 Challenge",
    'A'     : "Accessories",
    'AA'    : "Across America",
    'AFL'   : "Australian Football League",
    'AP'    : "Action Pack",
    'ARL'   : "Australian Rugby League",
    'ASAP'  : "[Code 2] ASAP Promotional",
    'ASP'   : "Action System Pack",
    'AVN'   : "Avon",
    'AW'    : "Around the World",
    'BH'    : "Matchbox 50th Birthday",
    'BJ'    : "Barrett-Jackson",
    'BK'    : "Battle Kings",
    'BLK'   : "Blank for Code 2 Use",
    'BO'    : "Best of ...",
    'BOB'   : "Best of British",
    'BOI'   : "Best of International",
    'BOM'   : "Best of Muscle",
    'BON'   : "Bonus",
    'BS'    : "Brroomstick",
    'C2'    : "[Code 2]",
    'CA'    : "Cartoon Characters",
    'CAT'   : "Caterpillar",
    'CC'    : "Collectors Choice",
    'CCH'   : "Color Changers",
    'CCI'   : "[Code 2] Color Comp Promotional",
    'CCY'   : "Collectible Convoy",
    'CDR'   : "CD Rom",
    'CF'    : "Commando",
    'CK'    : "Coca-Cola",
    'CKP'   : "Coca-Cola Premiere",
    'CL'    : "Club Models",
    'CNS'   : "Connoisseur Set",
    'COL'   : "Matchbox Collectibles",
    'CQ'    : "[Code 2] Conquer",
    'CR'    : "Code Red",
    'CRO'   : "Crocodile Hunter",
    'CS'    : "Construction",
    'CY'    : "Convoy",
    'DARE'  : "D.A.R.E.",
    'DM'    : "Dream Machines",
    'DT'    : "Days of Thunder",
    'DVD'   : "DVD",
    'DY'    : "Dinky",
    'EE'    : "European Edition",
    'ELC'   : "Early Learning Center",
    'ELV'   : "Elvis Presley Collection",
    'EM'    : "Emergency",
    'F1'    : "Formula 1",
    'FAS'   : "Michael Fischer-Art",
    'FC'    : "Feature Cars",
    'FE'    : "First Edition",
    'FM'    : "Farming",
    'FP'    : "Ford Anniversary",
    'G'     : "Gift Set", # G == GS
    'GC'    : "Gold Collection",
    'GF'    : "Graffic Traffic",
    'GS'    : "Gift Set",
    'GT'    : 'Budget Range / SuperGT',
    'GW'    : "Giftware",
    'HC'    : "Hero City Logo",
    'HD'    : "Harley Davidson",
    'HNH'   : "Hitch 'n' Haul",
    'HP'    : 'True Heroes',
    'HR'    : "Heroes",
    'HS'    : "Hot Stocks",
    'HT'    : "Hunt",
    'IC'    : "Intercom City",
    'IG'    : "Inaugural Collection",
    'IN'    : "Indy",
    'JB'    : "James Bond",
    'JEE'   : "Jeep",
    'JL'    : "Justice League",
    'JR'    : "Jurassic Park",
    'JW'    : "Jurassic World",
    'K'     : "Super Kings (King Size)",
    'LE'    : "Limited Edition Set",
    'LES'   : "Lesney Edition",
    'LL'    : "My First Matchbox (Live & Learn)",
    'LP'    : "Launcher Pack",
    'LR'    : "Lightning",
    'LRV'   : "Land Rover",
    'LT'    : "Lasertronic (Siren Force, Light & Sound)",
    'LW'    : "Laser Wheels",
    'MB'    : "Matchbox 1-75 (1-100) basic range",
    'MBR'   : "Micro Brewery",
    'MC'    : "Motor City",
    'MCC'   : "My Classic Car",
    'MD'    : "Superfast Minis",
    'MLB'   : "Major League Baseball (USA)",
    'MNS'   : "Monsters",
    'MO'    : "Matchbox Originals",
    'MP'    : "Multipack",
    'MT'    : "Matchcaps",
    'MU'    : "Masters of the Universe",
    'NBA'   : "National Basketball Association (USA)",
    'NBL'   : "National Basketball League (AUS)",
    'NC'    : "[Code 2] Nutmeg Collectibles",
    'NFL'   : "National Football League (USA)",
    'NHL'   : "National Hockey League (USA)",
    'NM'    : "Nigel Mansell",
    'NP'    : "National Parks",
    'NR'    : "Neon Racers",
    'NSF'   : "New Superfast",
    'OS'    : "Osbournes",
    'P'     : "Pre-production",
    'PC'    : "Premiere Collection",
    'PG'    : "Power Grabs",
    'PR'    : "Promotional",
    'PRC'   : "Premiere Concept",
    'PS'    : "Playset",
    'PVB'   : "Pleasant Valley Books",
    'PZ'    : "Puzzle",
    'RB'    : "Road Blasters",
    'RT'    : "Real Talkin",
    'SB'    : "Skybusters",
    'SCC'   : "Super Color Changers",
    'SCD'   : "Scooby Doo",
    'SCS'   : "Showcase Collection",
    'SF'    : "Superfast",
    'SFA'   : "Superfast America",
    'SNL'   : "Saturday Night Live",
    'SOC'   : "Stars of Germany (Stars of Cars)",
    'SOG'   : "Stars of Germany (Stars of Cars)",
    'SS'    : "Showstoppers (Motor Show)",
    'ST'    : "Super Trucks",
    'STR'   : "Star Car",
    'TC'    : "Team Convoy (Team Matchbox)",
    'TF'    : "Toy Fair",
    'TH'    : "Triple Heat",
    'TN'    : "Then & Now",
    'TP'    : "Twin Pack (Action System, Adventure Pack)",
    'TV'    : "TV Tie-In",
    'TVP'   : "TV-related Premiere",
    'TX'    : "Texaco Collection",
    'UC'    : "Ultra Collection",
    'WB'    : "Warner Brothers",
    'WC'    : "World Class",
    'WR'    : "[Code 2] White Rose Collectibles",
    'YF'    : "[Code 2] York Fair",
    'YST'   : "Yesteryear Train Set",
}

def correllation(pif):
    print 'correllation'
    vr_cats = []
    for cat in pif.dbh.raw_execute('select distinct category from variation')[0]:
	vr_cats.extend(cat[0].split(' '))
    vr_cats = set(vr_cats)
    vs_cats = set()
    for cat in pif.dbh.raw_execute('select distinct category from variation_select')[0]:
	vs_cats.add(cat[0])
    db_cats = {x['category.id']: x['category.name'] for x in pif.dbh.fetch_category_counts()}
    mb_cats = categories.keys()
    print 'in var but not in databse:', vr_cats - set(db_cats.keys())
    print 'in vs but not in databse:', vs_cats - set(db_cats.keys())
    print 'in database but not in list:', set(db_cats.keys()) - set(mb_cats)
    for cat in set(mb_cats) - set(db_cats.keys()):
	print "insert into category (id, name, flags, image) values ('%s', '%s', 0, '');" % (cat, categories[cat])
    print


def by_ref(pif, *filelist):
    print 'by ref'
    if filelist:
	refs = filelist
    else:
	refs = [x['ref_id'] for x in pif.dbh.fetch_variation_select_refs()]
    for ref in refs:
	cats = set()
	varsels = pif.dbh.fetch_variation_selects_by_ref(ref)
	for varsel in varsels:
	    var = pif.dbh.fetch_variation(varsel['variation_select.mod_id'], varsel['variation_select.var_id'])
	    if not var:
		continue
	    var = var[0]
	    if pif.switch['l']:
		print var['variation.mod_id'], var['variation.var'], var['variation.category'], '/', varsel['variation_select.category']
	    cats.add(var['variation.category'])
	print ref, len(varsels), cats
    print


root = '/usr/local/www/bamca'

'''
Checks photo credits, deleting any that are dups or dangling, reporting
dups that are different.

Current creds only apply to
| pic/man     |
| pic/man/var |
| pic/man/add |
but this will change.

Would like to make sure that all pictures apply to database objects as well.
'''

def check_photo_credits(pif):
    check_credits(pif)
    check_photogs(pif)


def check_photogs(pif):
    for phot in pif.dbh.fetch_photographers():
	if not phot['example_id']:
	    ph_id = phot['id']
	    creds = pif.dbh.fetch_photo_credits(photographer_id=ph_id)
	    if creds:
		print ph_id, pif.dbh.write('photographer', values={'example_id': creds[0]['photo_credit.id']}, where='id="%s"' % ph_id, verbose=True, modonly=True)
	    else:
		print ph_id, 'no creds'


def check_credits(pif):
    pids = {}
    creds = {x['id']: x for x in pif.dbh.depref('photo_credit', pif.dbh.fetch_photo_credits_raw())}
    for cred in creds.values():
	pid = (cred['path'], cred['name'], )
	if pid in pids:
	    if cred['photographer_id'] == creds[pids[pid]]['photographer_id']:
		pif.dbh.delete_photo_credit(cred['id'])
		print 'del', pid, cred['id'], pids[pid]
		continue
	    print 'dup', pid, cred['id'], cred['photographer_id'], pids[pid], creds[pids[pid]]['photographer_id']
	if cred['name'][1] == '_':
	    path = cred['path'] + '/' + cred['name'] + '.*'
	else:
	    path = cred['path'] + '/[tsml]_' + cred['name'] + '.*'
	files = glob.glob(root + '/' + path)
	if not files:
	    print 'n/f', pid, cred['id']
	    pif.dbh.delete_photo_credit(cred['id'])
	    continue
	pids[pid] = cred['id']



def check_single_links():
    src = 'https://www.mbxforum.com/11-Catalogs/02-MB75/MB75-Documents/'
    ln_re = re.compile('''<img src=".*?".*?> <a href="(?P<f>[^"]*)">''')

    flist = urllib2.urlopen(src).readlines()
    olist = glob.glob('orig/*.doc')

    for ln in flist:
        mat = ln_re.match(ln)
        if not mat:
            continue
        if not mat.group('f').endswith('.doc'):
            continue
        if not os.path.exists('orig/' + mat.group('f')):
            print mat.group('f'), 'not on dest'
        else:
            olist.remove('orig/' + mat.group('f'))
    for fn in olist:
        print fn, 'not on source'


def check_images(pif):
    global casting_ids, variation_ids

    casting_ids = [x['base_id.id'].lower() for x in pif.dbh.fetch_base_ids()]
    variation_ids = [x['variation.mod_id'].lower() + '-' + x['variation.var'].lower() for x in pif.dbh.fetch_variations_bare()]

    for key in sorted(checks.keys()):
	if checks[key]:
	    print key
	    checks[key](pif, key)
	    print


def check_blister(pif, dn):
    pass

def check_box(pif, dn):
    pass

def check_man(pif, dn):
    files = glob.glob('.' + dn + '/*.*')
    files.sort()
    c = 0
    for fn in files:
	try:
	    root, ext = os.path.splitext(os.path.basename(fn))
	    if not ext or ext[1:] not in imglib.itypes:
		continue
	    root = root.lower()
	    var = ''
	    if '-' in root:
		root, var = root.rsplit('-', 1)
	    if len(root) > 1 and root[1] == '_':
		root = root[2:]
	    if root not in casting_ids:
		print fn, "missing base", root
	    elif var and (root + '-' + var) not in variation_ids:
		print fn, "missing var", root, var
	    else:
		c += 1
	except Exception as e:
	    print fn, "fail -", e
	    raise
    print c, 'ok'

def check_package(pif, dn):
    pass

def check_set(pif, dn):
    pass


checks = {
    config.IMG_DIR_ACC:              check_set,
    config.IMG_DIR_ADD:              check_man,
    config.IMG_DIR_BLISTER:          check_blister,
    config.IMG_DIR_BOX:              check_box,
    config.IMG_DIR_CAT:              None,
    config.IMG_DIR_PROD_CODE_2:      None,
    config.IMG_DIR_COLL_43:          check_package,
    config.IMG_DIR_PROD_COLL_64:     check_package,
    config.IMG_DIR_MAN_ICON:         check_man,
    config.IMG_DIR_KING:             check_man,
    config.IMG_DIR_LESNEY:           check_set,
    config.IMG_DIR_PROD_LRW:         check_package,
    config.IMG_DIR_PROD_LSF:         check_package,
    config.IMG_DIR_MAN:              check_man,
    config.IMG_DIR_PROD_MWORLD:      check_package,
    config.IMG_DIR_PROD_EL_SEG:      check_package,
    config.IMG_DIR_PROD_MT_LAUREL:   check_package,
    config.IMG_DIR_PROD_PACK:        check_package,
    config.IMG_DIR_PROD_SERIES:      check_package,
    config.IMG_DIR_SKY:              None,
    config.IMG_DIR_PROD_TYCO:        check_package,
    config.IMG_DIR_PROD_UNIV:        check_package,
    config.IMG_DIR_VAR:              check_man,
}


def check_pictures(pif, *filelist):
    mod_id = filelist.pop(0)
    targs = [(x, os.stat(x).st_size) for x in sorted(glob.glob('.' + config.IMG_DIR_VAR + '/l_' + mod_id + '-*.*'))]

    for prefix in filelist:
	srcs = sorted(glob.glob('./lib/man/' + mod_id + '/' + prefix + '*.*'))
	srcs = [(x, os.stat(x).st_size) for x in srcs]
	for sf in srcs:
	    for tf in targs:
		if tf[1] == sf[1] and filecmp.cmp(tf[0], sf[0]):
		    print tf[0], sf[0]
		    break
	    else:
		print 'none', sf[0]


def check_products(pif):
    regions = ''.join(mbdata.regionlist).lower()
    files = {}
    dirs = {}
    direct_files(pif, regions, files, dirs)
    indirect_files(pif, regions, files, dirs)
    show_files(regions, files)


def show_files(regions, files):
    for reg in regions:
	if reg in files:
	    for year in sorted(files[reg]):
		print year, reg, ' '.join(collapse(files[reg][year]))
	    print


def direct_files(pif, regions, files, dirs):
    for pg in pif.dbh.fetch_pages(where={'format_type': 'lineup'}, order='id'):
	year = pg.id[5:]
	dirs[year] = pg.pic_dir
	imgs = glob.glob('%s/%s[%s][0-9][0-9].*' % (pg.pic_dir, year, regions))
	imgs += glob.glob('%s/%s[%s][0-9][0-9][0-9].*' % (pg.pic_dir, year, regions))
	for im in imgs:
	    im = im[len(pg.pic_dir) + 1:]
	    files.setdefault(im[4], dict())
	    files[im[4]].setdefault(im[:4], list())
	    files[im[4]][im[:4]].append(im[5:-4])


def indirect_files(pif, regions, files, dirs):
    for lm in pif.dbh.fetch_simple_lineup_models(region=mbdata.regionlist):
	if lm['lineup_model.picture_id']:
	    year = str(lm['lineup_model.year'])
	    region = lm['lineup_model.region'].lower()
	    num = '%%0%dd' % len(files.get(region, {}).get(year, ['00'])[0]) % lm['lineup_model.number']
	    if num in files.get(region, {}).get(year, ['00']):
		print 'hidden image', year, lm['lineup_model.region'], lm['lineup_model.number'], lm['lineup_model.picture_id']
	    else:
		imgs = glob.glob('%s/%s.*' % (dirs[year], lm['lineup_model.picture_id']))
		if imgs:
		    files[region][year].append(str(num))


def collapse(lst):
    intlist = []
    strlist = []
    maxlen = 0
    for ent in sorted(lst):
	try:
	    val = int(ent)
	except:
	    pass
	else:
	    maxlen = max(maxlen, len(ent))
	    intlist.append(val)
	    continue

	try:
	    ents = ent.split('-', 1)
	    val1 = int(ents[0])
	    val2 = int(ents[1])
	except:
	    pass
	else:
	    maxlen = max(maxlen, len(ent[0]))
	    maxlen = max(maxlen, len(ent[1]))
	    intlist.extend(range(val1, val2 + 1))
	    continue

	strlist.append(ent)

    str1 = "%%0%dd" % maxlen
    str2 = str1 + '-' + str1
    intlist.sort()
    start = None
    prev = None
    for val in intlist:
	if start == None:
	    start = prev = val
	elif val == prev + 1:
	    prev = val
	elif start == prev:
	    strlist.append(str1 % start)
	    start = prev = val
	else:
	    strlist.append(str2 % (start, prev))
	    start = prev = val
    if start != None:
	if start == prev:
	    strlist.append(str1 % start)
	    start = None
	else:
	    strlist.append(str2 % (start, prev))
	    start = None

    return strlist


'''
Given a variation, get the list of attributes
Get list of variations.
Build dictionary of vars where key is tuple of visual attributes.
Categorize vars by these keys.
Find vars that might have common picture but don't reflect that.
Find vars where visual pic violates this list.

filelist - list of mod_id's to check (none means all)
options:
  's' - list of man sections
'''

# Decorator for reading data files
def read_data_file(main_fn):
    def read_dat(fn):
        dat = open(useful.relpath(config.SRC_DIR, fn + '.dat')).readlines()
        dat = filter(lambda x: x and not x.startswith('#'), [ln.strip() for ln in dat])
        return main_fn(dat)
    return read_dat


@read_data_file
def read_attr_change(fil):
    changes = dict()
    for ln in fil:
	try:
	    cols, detfr, detto = ln.split('|')
	except ValueError:
	    print 'ValueError:', ln, '<br>'
	    continue
        for col in cols.split(';'):
            changes.setdefault(col, list())
	    for det in detfr.split(';'):
		changes[col].append([det, detto])
    return changes


def check_variations(pif, *filelist):
    global detail_changes
    detail_changes = read_attr_change('vdetail')
    if filelist:
	check_var_data(pif, filelist)
    elif pif.options['s']:
	for section_id in pif.options['s']:
	    mods = pif.dbh.fetch_casting_list(section_id=section_id)
	    check_var_data(pif, [x['casting.id'] for x in mods])
    else:
	mods = pif.dbh.fetch_casting_list()
	check_var_data(pif, [x['casting.id'] for x in mods])


def modify_detail(attr, desc):
    for det_pair in detail_changes.get(attr, []):
	desc = desc.replace(*det_pair)
#    if attr in ['wheels', 'front_wheels', 'rear_wheels']:
#	return desc.replace(' hollow', '').replace(' mixed', '').replace(' solid', '') \
#	    .replace(' (narrow inner rim)', '').replace(' (wide inner rim)', '')
    return desc


def modify_vars(vars):
    for ivar in range(len(vars)):
	vars[ivar] = modify_var(vars[ivar])
    return vars


def modify_var(var):
    for key in var:
	var[key] = modify_detail(key, var[key])
    return var


def check_var_data(pif, id_list):
    for mod_id in id_list:
	casting = pif.dbh.fetch_casting(mod_id)
	print mod_id, ':', casting['name']
	attrs = pif.dbh.fetch_attributes(mod_id=mod_id, with_global=True)
	attr_dict = {x['attribute.attribute_name']: x for x in attrs}
	if casting['flags'] & pif.dbh.FLAG_MODEL_BASEPLATE_VISIBLE:
	    attr_dict['base']['attribute.visual'] = 1
	visual_keys = sorted([x['attribute.attribute_name'] for x in attrs if x['attribute.visual']])
	print '    ', visual_keys
	vk_set = dict()
	vars = modify_vars(pif.dbh.depref('variation', pif.dbh.fetch_variations(mod_id)))
	vars_dict = {x['var']: x for x in vars}
	for var in vars:
	    var['visual_key'] = tuple([var.get(x, '') for x in visual_keys])
	    vk_set.setdefault(var['visual_key'], list())
	    vk_set[var['visual_key']].append(var['var'])
	for vk in sorted(vk_set):
	    print vk
	    print ' ',
	    for var_id in vk_set[vk]:
		var = vars_dict[var_id]
		if var['visual_key'] == vk:
		    print var['var'],
		    if var['picture_id']:
			print '(%s)' % var['picture_id'],
	    print



# ------- infra --------------------------------------------------------

cmds = [
    ('c', count_tables, "count tables: [-v]"),
    ('sch', check_schema, "check schema"),
    ('tab', check_tables, "check tables: [table ...]"),
    ('dup', check_dups, "check duplicates"),
    ('bid', check_base_id, "check base_id"),
    ('add', check_attribute_pictures, "check attr_pics"),
    ('cas', check_castings, "check castings"),
    ('cat', show_categories, "show_categories"),
    ('vvscat', check_var_vs_categories, "check_var_vs_categories"),
    ('vscat', check_vs_categories, "check_vs_categories"),
    ('cat2mat', cat2matrix, "cat2matrix: cat"),
    ('cred', check_photo_credits, "check_photo_credits"),
    ('lnk', check_single_links, "check_single_links"),
    ('img', check_images, "check_images"),
    ('pic', check_pictures, "check_pictures"),
    ('prod', check_products, "check_products"),
    ('var', check_variations, "check_variations"),
]

@basics.command_line
def commands(pif):
    useful.cmd_proc(pif, './dcheck.py', cmds)

# ------- --------------------------------------------------------------

if __name__ == '__main__':  # pragma: no cover
    commands(dbedit='', switches='vl', options='s')
