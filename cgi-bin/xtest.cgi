#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import cgi      # noqa: E402
import multipart
import os       # noqa: E402
import basics   # noqa: E402
import http.cookies as Cookie   # noqa: E402
import useful   # noqa: E402

if __name__ == '__main__':
    pwd = os.getcwd()
    pif = basics.get_page_info('editor')
    pif.ren.print_html()
    print(pif.ren.format_head())
    print(useful.dump_dict("Globals", globals()), '<p>')
    print(useful.dump_dict("Basics", basics.__dict__), '<p>')
    print(useful.dump_dict("PIF", pif.__dict__), '<p>')
    print(useful.dump_dict("Render", pif.ren.__dict__), '<p>')
    '''
FieldStorage/MiniFieldStorage has no direct replacement, but can typically be replaced by using
multipart (for POST and PUT requests) or

# import sys, os, multipart
# 
# environ = dict(os.environ.items())
# environ['wsgi.input'] = sys.stdin.buffer
# forms, files = multipart.parse_form_data(environ)

urllib.parse.parse_qsl (for GET and HEAD requests)
    '''
    if os.environ.get('REQUEST_METHOD') == 'POST':
        cgi_form = cgi.FieldStorage()
        post = '\n'.join([f'{key}: {str(cgi_form[key].field)}' for key in cgi_form])
        print('POST', post, '<p>')
    print('<hr><form method="post">')
    print(pif.form.put_button_input('reset'))
    print(pif.form.put_button_input('submit'))
    print(pif.form.put_button_input('yodel'))
    print(pif.form.put_text_input('thing', 24))
    print('</form>')
#    print(pif.ren.format_button('yodeltext'))
    cgi.print_environ()
#    if pif.cgiform:
#        cgi.print_form(pif.cgiform)
    print("<h3>Processed form</h3>", pif.form)
    cgi.print_directory()
    print("was", pwd)
    cgi.print_environ_usage()
    print("<p><h3>Cookies</h3><p>")
#    c = pif.ren.get_cookies()

    print('HTTP_COOKIE =', os.environ.get('HTTP_COOKIE'), '<br>')
    cookie = Cookie.SimpleCookie()
#    cookie.load(os.environ.get('HTTP_COOKIE', ''))

#    open(os.environ['DOCUMENT_ROOT'] + '/bin/value-http', 'w').write(
#        os.environ['HTTP_COOKIE'])
#    print(c,'<br>')
#    if c:
#        print("id =", c['id'].value, '<br>')
    print(useful.dump_dict("Sys", sys.__dict__))

    pif.dbh.increment_counter('test')

    print('<form action="xtest.cgi">')
    print(pif.form.put_button_input())
    print(pif.form.put_button_input('delete'))
    print(pif.form.put_button_input('yodel'))
    print('</form>')

    print(pif.ren.format_tail())
