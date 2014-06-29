#!/usr/local/bin/python
# -*- coding: latin-1

import getopt, glob, os, sys

'''
CommandLine front-ends getopt, to make it do stuff I want it to do.
Uses unix-style options, not Gnu-style.

switches - binary switches, like -v for verbose
options - switches that need an argument, like -f <file>
   switches or options can be prefixed with '+' to make them required
long_options - dictionary of long options
   keys are long option name (followed by '=' if it needs an argument)
   values are the short option/switch to map to (if any)
   keys can be prefixed with '+' to make them required
version - application version string, for display purposes
short_help - one-line help
long_help - multiline help
envar - an environment variable (if any) that can specify arguments
noerror - don't fail on getopt errors, just ignore them
defaults - dictionary of default values
   for switches use False/True, for options use the argument (NOT in a list)
doglob - run glob.glob over 'files'

Please use named arguments for everything after the first three.
All arguments are optional.

-DD, developed over several years
'''

def Req(sw, reqs=[]):
    if type(sw) == dict:
	osw = []
	for opt in sw.keys():
	    if opt[0] == '+':
		if sw[opt]:
		    reqs.append(sw[opt])
		else:
		    if opt[-1] == '=':
			reqs.append(opt[1:-1])
		    else:
			reqs.append(opt[1:])
		sw[opt[1:]] = sw[opt]
    else:
	while '+' in sw:
	    reqs.append(sw[sw.find('+') + 1])
	    sw = sw.replace('+', '', 1)
    return sw, reqs


def CommandLine(switches="", options="", long_options={}, version="", short_help="", long_help="", envar=None, noerror=False, defaults={}, doglob=False):
    switches, reqs = Req(switches)
    options, reqs = Req(options, reqs)
    loptions, reqs = Req(long_options, reqs)
    switch = FlagClass()
    opts = files = []
    coptions = switches
    if options:
	coptions += ':'.join(list(options)) + ':'
    if not 'h' in coptions:
	coptions += 'h'
    if envar and os.environ.has_key(envar):
	try: # get command line
	    import string
	    opts, files = getopt.getopt(string.split(os.environ[envar]), coptions, loptions)
	except getopt.GetoptError:
	    if not noerror:
		print "*** Environment error"
		print >> sys.stderr, sys.argv[0], short_help
		sys.exit(1)

    try: # get command line
	opts2, files2 = getopt.getopt(sys.argv[1:], coptions, loptions)
	opts = opts + opts2
	files = files + files2
    except getopt.GetoptError:
	if not noerror:
	    print "*** Options error"
	    print >> sys.stderr, sys.argv[0], short_help
	    sys.exit(2)

    for opt in switches:
	switch[opt] = None
    for opt in options:
	switch[opt] = []
    for opt in long_options:
	if not long_options[opt]:
	    if opt[-1] == '=':
		switch[opt[:-1]] = []
	    else:
		switch[opt] = None

    for opt in opts:
	if opt[0] == "-h" and 'h' not in switches + options:
	    print >> sys.stderr, version, long_help
	    sys.exit(3)
	elif opt[0][0:2] == '--':
	    if opt[0][2:] in long_options:
		if long_options[opt[0][2:]]:
		    switch[long_options[opt[0][2:]]] = not switch.get(long_options[opt[0][2:]], False)
		else:
		    switch[opt[0][2:]] = not switch.get(opt[0][2:], False)
	    elif opt[0][2:] + '=' in long_options:
		if long_options[opt[0][2:] + '=']:
		    sw = switch.get(long_options[opt[0][2:] + '='], [])
		    switch[long_options[opt[0][2:] + '=']] = sw + [opt[1]]
		else:
		    sw = switch.get(opt[0][2:], [])
		    switch[opt[0][2:]] = sw + [opt[1]]
	elif opt[0][1] in options:
	    sw = switch.get(opt[0][1], [])
	    switch[opt[0][1]] = sw + [opt[1]]
	else:
	    switch[opt[0][1]] = not switch.get(opt[0][1], False)

    for req in reqs:
	if not switch[req]:
	    print "*** Missing command line argument"
	    print >> sys.stderr, sys.argv[0], short_help
	    sys.exit(4)

    for key in switch:
	if switch[key] == None:
	    switch[key] = defaults.get(key, False)
	elif switch[key] == [] and key in defaults:
	    switch[key] = [defaults[key]]

    if doglob:
	files = reduce(lambda x,y: x+y, [glob.glob(x) for x in files], [])

    return (switch, files)


class FlagClass:
    def __init__(self, switch={}, flagmap={}, OPTIONS=''):
	for flag in OPTIONS:
	    self[flag] = []
	if flagmap:
	    for flag in flagmap:
		if flag in switch:
		    self[flagmap[flag]] = switch.get(flag)
		elif OPTIONS.find(flag) >= 0:
		    self[flagmap[flag]] = []
		else:
		    self[flagmap[flag]] = False
	else:
	    for flag in switch:
		self[flag] = switch[flag]

    def __str__(self):
	return 'FlagClass(%s)' % str(self.__dict__)

    def __getattr__(self, attr):
	return self.__dict__.get(attr)

    def __getitem__(self, attr):
	return self.__dict__.get(attr)

    def __setitem__(self, attr, value):
	self.__dict__[attr] = value

    def __nonzero__(self):
	return bool(self.__dict__)

    def __iter__(self):
	return self.__dict__.__iter__()

    def __contains__(self, a):
	return a in self.__dict__

    def get(self, attr, value=None):
	return self.__dict__.get(attr, value)

    def teg(self, arg, key, value=None):
	if arg == None:
	    arg = self.__dict__.get(key, value)
	return arg

    def getnum(self, attr, value=None):
	if not attr in self.__dict__:
	    return value
	dval = self.__dict__[attr]
	if type(dval) == int:
	    return dval
	elif type(dval) == str:
	    return int(dval)
	elif not dval:
	    return value
	return int(dval[-1])

    def getstr(self, attr, value=None):
	if not attr in self.__dict__:
	    return value
	dval = self.__dict__[attr]
	if type(dval) == str:
	    return dval
	elif not dval:
	    return value
	return dval[-1]

def MakeFlags(switch, flagmap, OPTIONS):
    return FlagClass(switch, flagmap, OPTIONS)


if __name__ == '__main__': # pragma: no voer
    print CommandLine('fv', '+od', {"force":'f', "output=":'o', "test":None, "arg=":None}, '0', 'Short', 'Long', 'TEST')
    pass
