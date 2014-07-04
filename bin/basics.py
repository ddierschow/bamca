#!/usr/local/bin/python

import config
import pifile


def GetPageInfo(page_id, form_key='', defval='', args='', dbedit=False):
    pif = pifile.PageInfoFile(page_id, form_key, defval, args=args, dbedit=dbedit)
    return pif


def WriteTracebackFile(pif):
    import datetime, os, sys, traceback
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
    import sys
    sys.exit()

#---- -------------------------------------------------------------------

# Decorator that wraps web page mains.
def WebPage(main_fn):
    def CallMain(page_id, form_key='', defval='', args='', dbedit=False):
	pif = None
	try:
	    if isinstance(page_id, pifile.PageInfoFile):
		pif = page_id
	    else:
		pif = GetPageInfo(page_id, form_key, defval, args, dbedit)
	    ret = main_fn(pif)
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
    def CallMain(page_id, form_key='', defval='', args='', dbedit=False, switches='', options=''):
	pif = None
	try:
	    if isinstance(page_id, pifile.PageInfoFile):
		pif = page_id
	    else:
		pif = GetPageInfo(page_id, form_key, defval, args, dbedit)
	    import cmdline
	    pif.switch, pif.filelist = cmdline.CommandLine(switches, options)
	    ret = main_fn(pif)
	    if ret:
		print ret
	except SystemExit:
	    pass
    return CallMain

#---- -------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
