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
    if isinstance(sw, dict):
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
    switch = dict()
    opts = list()
    files = list()
    coptions = switches
    if options:
	coptions += ':'.join(list(options)) + ':'
    if not 'h' in coptions:
	coptions += 'h'
    if envar and os.environ.has_key(envar):
	try: # get command line
	    opts, files = getopt.getopt(os.environ[envar].split(), coptions, loptions)
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
	switch[opt] = list()
    for opt in long_options:
	if not long_options[opt]:
	    if opt[-1] == '=':
		switch[opt[:-1]] = list()
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
		    sw = switch.get(long_options[opt[0][2:] + '='], list())
		    switch[long_options[opt[0][2:] + '=']] = sw + [opt[1]]
		else:
		    sw = switch.get(opt[0][2:], list())
		    switch[opt[0][2:]] = sw + [opt[1]]
	elif opt[0][1] in options:
	    sw = switch.get(opt[0][1], list())
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


if __name__ == '__main__': # pragma: no voer
    print CommandLine('fv', '+od', {"force":'f', "output=":'o', "test":None, "arg=":None}, '0', 'Short', 'Long', 'TEST')
    pass
