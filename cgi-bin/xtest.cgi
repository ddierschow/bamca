#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import cgi, os
import basics
import Cookie
import useful

if __name__ == '__main__':
    pwd = os.getcwd()
    pif = basics.get_page_info('editor')
    pif.render.print_html()
    print pif.render.format_head()
    useful.dump_dict("Globals", globals())
    useful.dump_dict("Basics", basics.__dict__)
    useful.dump_dict("PIF", pif.__dict__)
    useful.dump_dict("Render", pif.render.__dict__)
    print pif.render.format_button('reset')
    print pif.render.format_button('yodel')
    cgi.print_environ()
    if pif.cgiform:
        cgi.print_form(pif.cgiform)
    print "<h3>Processed form</h3>", pif.form
    cgi.print_directory()
    print "was", pwd
    cgi.print_environ_usage()
    print "<p><h3>Cookies</h3><p>"
#    c = pif.render.get_cookies()

    print 'HTTP_COOKIE =', os.environ.get('HTTP_COOKIE'), '<br>'
    cookie = Cookie.SimpleCookie()
#    cookie.load(os.environ.get('HTTP_COOKIE', ''))

#    file(os.environ['DOCUMENT_ROOT'] + '/bin/value-http', 'w').write(os.environ['HTTP_COOKIE'])
#    print c,'<br>'
#    if c:
#        print "id =", c['id'].value, '<br>'
    useful.dump_dict("Sys", sys.__dict__)

    pif.dbh.increment_counter('test')

    print '<form action="xtest.cgi">'
    print pif.render.format_button_input()
    print pif.render.format_button_input('delete')
    print pif.render.format_button_input('yodel')
    print '</form>'

    print pif.render.format_tail()
