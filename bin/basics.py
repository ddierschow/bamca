#!/usr/local/bin/python

import config

def GetPageInfo(page_id, form_key='', defval='', args='', dbedit=False):
    import pifile
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
    erf.write("headline = '''%s'''\n" % traceback.format_exception_only(sys.exc_type, sys.exc_value))
    erf.write("tb = '''\n" + str_tb + "\n'''\n")
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

def StartPage(main_fn, page_id, form_key='', defval='', args='', dbedit=False):
    pif = None
    try:
	pif = GetPageInfo(page_id, form_key, defval, args, dbedit)
	ret = main_fn(pif)
	if ret:
	    print ret
    except SystemExit:
	pass
    except:
	HandleException(pif)
	raise

#---- -------------------------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''
