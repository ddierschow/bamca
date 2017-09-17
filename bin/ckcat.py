#!/usr/local/bin/python

import basics
import mbdata

# variation fns to correllate category entries between variation and variation_select.
# variation.category is the old version and cannot be properly joined against.
# variation_select.category is the new version which should be able to replace it.
# vs.category will be useful without vs.ref_id and vs.sub_id so the rest of the site needs to tolerate that.

@basics.command_line
def main(pif):
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
    res = pif.dbh.raw_execute('''select v.category,v.mod_id,v.var,vs.category,vs.ref_id,vs.sub_id,vs.id from variation v,variation_select vs where 
v.category != vs.category and
v.category != '' and
v.mod_id=vs.mod_id and
v.var=vs.var_id
''')
    fmt = pif.dbh.preformat_results(res[0])
    for ent in res[0]:
	vc, vsc = ent[0], ent[3]
	if vsc != 'MB' and vsc not in vc.split():
	    print fmt % ent
    print


def l5p(pif):
    print 'licensed 5 packs'
    res = pif.dbh.raw_execute('''select v.category,vs.category from variation v,pack p,variation_select vs where 
p.page_id='packs.5packs' and
p.section_id='lic5packs' and
vs.ref_id=p.page_id and
vs.sub_id=p.id and
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


def correllation(pif):
    print 'correllation'
    vr_cats = []
    for cat in pif.dbh.raw_execute('select distinct category from variation')[0]:
	vr_cats.extend(cat[0].split(' '))
    vr_cats = set(vr_cats)
    vs_cats = set()
    for cat in pif.dbh.raw_execute('select distinct category from variation_select')[0]:
	vs_cats.add(cat[0])
    db_cats = {x['category.id']: x['category.name'] for x in pif.dbh.fetch_categories()}
    mb_cats = mbdata.categories.keys()
    print 'in var but not in databse:', vr_cats - set(db_cats.keys())
    print 'in vs but not in databse:', vs_cats - set(db_cats.keys())
    print 'in database but not in list:', set(db_cats.keys()) - set(mb_cats)
    for cat in set(mb_cats) - set(db_cats.keys()):
	print "insert into category (id, name, flags, image) values ('%s', '%s', 0, '');" % (cat, mbdata.categories[cat])
    print


def by_ref(pif):
    print 'by ref'
    if pif.filelist:
	refs = pif.filelist
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


if __name__ == '__main__':  # pragma: no cover
    main(page_id='editor', switches='l')
