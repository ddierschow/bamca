#!/usr/local/bin/python

import os, sys
import useful

#---- Web Pages ---------------------------------------------------------

def GetPageInfo(page_id, form_key='', defval='', args='', dbedit=None):
    import pifile
    pif = pifile.PageInfoFile(page_id, form_key, defval, args=args, dbedit=dbedit)
    return pif


def WriteTracebackFile(pif):
    import datetime, traceback
    import config
    str_tb = traceback.format_exc()
    if pif and pif.unittest:
	return str_tb # unit testing should not leave tb files sitting around.
    tb_file_name = os.path.join(config.logroot, datetime.datetime.now().strftime('%Y%m%d.%H%M%S.') + config.env + '.')
    if pif:
	tb_file_name += pif.page_id
    else:
	tb_file_name += 'unknown'
    erf = open(tb_file_name, 'w')
    erf.write("headline = '''%s'''\n" % ' '.join([x.strip() for x in traceback.format_exception_only(sys.exc_type, sys.exc_value)]))
    erf.write("uri = '''%s'''\n" % os.environ.get('REQUEST_URI', ''))
    erf.write("tb = '''\n" + str_tb + "\n'''\n")
    erf.write("env = '''" + str(os.environ) + "'''\n")
    if pif:
	erf.write(pif.ErrorReport())
    erf.close()
    return str_tb


def HandleException(pif):
    str_tb = WriteTracebackFile(pif)
    if not pif or not pif.render or not pif.dbh:
	print 'Content-Type: text/html\n\n'
	print '<!--\n' + str_tb + '-->'
	FinalExit()
    pif.dbh.SetHealth(pif.page_id)
    import useful
    if not useful.header_done:
	print 'Content-Type: text/html\n\n'
	print '<!--\n' + str_tb + '-->'
    while pif.render.table_count > 0:
	print pif.render.FormatTableEnd()
    if not pif.IsAllowed('a'):
	print '<!--\n' + str_tb + '-->'
	FinalExit()


def FinalExit():
    print "<p><h3>An error has occurred that prevents this page from displaying.  Our apologies.<br>"
    print "An alert has been sent and the problem will be fixed as soon as possible.</h3>"
    #print "<p>We're doing some upgrades, and right now, not everything is playing nicely together.<br>"
    #print "We'll get things going as soon as possible."
    sys.exit()

#---- Command Lines -----------------------------------------------------

'''
GetCommandLine front-ends getopt, to make it do stuff I want it to do.
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


def GetCommandLine(switches="", options="", long_options={}, version="", short_help="", long_help="", envar=None, noerror=False, defaults={}, doglob=False):
    import getopt, glob

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

#---- -------------------------------------------------------------------

# Decorator that wraps web page mains.
def WebPage(main_fn):
    def CallMain(page_id, form_key='', defval='', args='', dbedit=None):
	pif = None
	try:
	    import pifile
	    if isinstance(page_id, pifile.PageInfoFile):
		pif = page_id
	    else:
		pif = GetPageInfo(page_id, form_key, defval, args, dbedit)
	    ret = main_fn(pif)
	    useful.WriteComment()
	    if ret:
		print ret
	except SystemExit:
	    pass
	except:
	    HandleException(pif)
	    raise
    return CallMain

#---- -------------------------------------------------------------------

# Decorator that command line mains.
def CommandLine(main_fn):
    def CallMain(page_id, form_key='', defval='', args='', dbedit=None, switches='', options=''):
	pif = None
	try:
	    import pifile
	    if isinstance(page_id, pifile.PageInfoFile):
		pif = page_id
	    else:
		pif = GetPageInfo(page_id, form_key, defval, args, dbedit)
	    pif.switch, pif.filelist = GetCommandLine(switches, options)
	    ret = main_fn(pif)
	    useful.WriteComment()
	    if ret:
		print ret
	except SystemExit:
	    pass
    return CallMain

#---- -------------------------------------------------------------------

# Decorator for standalone (PIFless) command line mains.
def Standalone(main_fn):
    def CallMain(switches="", options="", long_options={}, version="", short_help="", long_help="", envar=None, noerror=False, defaults={}, doglob=False):
	try:
	    switch, filelist = GetCommandLine(switches=switches, options=options, long_options=long_options,
		version=version, short_help=short_help, long_help=long_help, envar=envar, noerror=noerror,
		defaults=defaults, doglob=doglob)
	    ret = main_fn(switch, filelist)
	    useful.WriteComment()
	    if ret:
		print ret
	except SystemExit:
	    pass
    return CallMain

#---- -------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
