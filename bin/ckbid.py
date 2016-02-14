#!/usr/local/bin/python

import os
import basics
import config
import images
import imglib
import mbdata

@basics.command_line
def main(pif):
    ids = pif.dbh.fetch_base_ids();
    for id in ids:
	rn = pif.dbh.icon_name(id['base_id.rawname'])
	if not rn or any([len(x) > 25 for x in rn]):
	    print id['base_id.id'], id['base_id.rawname'], '=>', rn
	if id['base_id.first_year'] is None or int(id['base_id.first_year']) < 1947 or int(id['base_id.first_year']) > 2015:
	    print id['base_id.id'], id['base_id.first_year'], 'not in bounds'
	if id['base_id.model_type'] not in mbdata.casting_types:
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

if __name__ == '__main__':  # pragma: no cover
    main()
