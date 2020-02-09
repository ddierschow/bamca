#!/usr/local/bin/python

import config
import mbdata
import useful

# US|United States Minor Outlying Islands|UM|PA|us


# this version doesn't do subdivisions
class FlagList(object):  # interprets "175.dat"

    def __init__(self):
        self.isolist = mbdata.countries
        self.lookup = {x[0]: x[1] for x in self.isolist}
        self.isolist.sort(key=lambda x: x[1])

    def format(self, code2, hspace=0, also={}):
        if code2 not in self:
            return ''
        return '<img alt="[%s]" src="..%s/%s"%s>' % (
            self[code2], config.FLAG_DIR, code2, useful.fmt_also({'hspace': hspace}, also))

    def has_key(self, code):
        return code in self.lookup

    def __contains__(self, code):
        return code in self.lookup

    def __getitem__(self, code):
        return self.lookup.get(code, '')
