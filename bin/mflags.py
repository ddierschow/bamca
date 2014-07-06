#!/usr/local/bin/python

import config
import mbdata
import useful

#US|United States Minor Outlying Islands|UM|PA|us

# this version doesn't do subdivisions
class FlagList():
    # interprets "175.dat"
    def __init__(self, pif):
	self.isolist = mbdata.countries
	self.lookup = {x[0]: x[1] for x in self.isolist}
	self.isolist.sort(key=lambda x: x[1])

    def Format(self, code2, hspace=0, also={}):
	if not code2 in self:
	    return ''
	return '<img alt="[%s]" src="../%s/%s"%s>' % (self[code2], config.flagdir, code2, useful.Also({'hspace':hspace}, also))

    def has_key(self, code):
	return self.lookup.has_key(code)

    def __contains__(self, code):
	return code in self.lookup

    def __getitem__(self, code):
	return self.lookup.get(code, '')


if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
