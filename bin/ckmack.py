#!/usr/local/bin/python

import basics


@basics.command_line
def main(pif):
    aliases = pif.dbh.fetch_aliases()
    lmodels = pif.dbh.fetch_lineup_models()

    a_dict = {x['alias.id']: x for x in aliases}
    for lmodel in lmodels:
        if lmodel['lineup_model.letter']:
            id = '%(base_id.model_type)s%(lineup_model.number)02d%(lineup_model.letter)s' % lmodel
            if id == lmodel['base_id.id']:
                pass
            elif id not in a_dict:
                print 'new', id, lmodel['base_id.id']
            elif lmodel['base_id.id'] != a_dict[id]['alias.ref_id']:
                print 'bad', id, lmodel['base_id.id'], a_dict[id]['alias.ref_id']


if __name__ == '__main__':  # pragma: no cover
    main('vars')
