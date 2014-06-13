#!/usr/local/bin/python

import useful


def GetPageInfo(page_id, form_key='', defval='', args=''):
    import pifile
    pif = pifile.PageInfoFile(page_id, form_key, defval)
    return pif


def HandleException(pif):
    import traceback
    str_tb = traceback.format_exc()
    import datetime
    if pif:
	erf = open("../htdocs/tb/" + datetime.datetime.now().strftime('%Y%m%d.%H%M%S') + '.' + pif.page_id, 'w')
    else:
	erf = open("../htdocs/tb/" + datetime.datetime.now().strftime('%Y%m%d.%H%M%S') + '.unknown', 'w')
    erf.write("tb = '''\n" + str_tb + "\n'''\n")
    if pif:
	erf.write(pif.ErrorReport())
    erf.close()
    if not pif or not pif.render or not pif.dbh:
	print 'Content-Type: text/html\n\n'
	print '<!--\n' + str_tb + '-->'
	FinalExit()
    pif.dbh.SetHealth(pif.page_id)
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

def StartPage(main_fn, page_id, form_key='', defval='', args=''):
    import sys
    pif = None
    try:
	import pifile
	pif = pifile.PageInfoFile(page_id, form_key, defval, args=args)
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
