#!/usr/local/bin/python

import datetime
import functools
import getopt
import glob
import http.client
from io import open
import os
import pprint
import pymysql
import random
import sys
import time
import traceback

import config
import crawls
import logger
import pifile
import useful

config.GURU_ID = ''.join(random.choice('0123456789ABCDEFGHJKLMNPRSTUVWXYZ') for i in range(10))

tb_fmt = """headline = '''{}'''
guru_id = '{}'
uri = '''{}'''
tb = '''
{}
'''
env = {}
"""

# --- Web Pages ---------------------------------------------------------


def get_page_info(page_id, form_key='', defval='', args='', dbedit=None):
    return pifile.PageInfoFile(page_id, form_key, defval, args=args, dbedit=dbedit)


def write_traceback_file(pif, e):
    str_tb = traceback.format_exc()
    if pif and pif.unittest:
        return str_tb  # unit testing should not leave tb files sitting around.
    tb_file_name = os.path.join(config.LOG_ROOT, datetime.datetime.now().strftime('%Y%m%d.%H%M%S.') + config.ENV + '.')
    if pif:
        tb_file_name += pif.page_id
    else:
        tb_file_name += 'unknown'
    erf = open(tb_file_name, 'w')
    erf.write(tb_fmt.format(' '.join([x.strip() for x in traceback.format_exception_only(type(e), e)]),
              config.GURU_ID, os.environ.get('REQUEST_URI', ''), str_tb,
              pprint.pformat(os.environ, indent=2, width=132)))

    if pif:
        erf.write(pif.error_report())
    erf.close()
    return str_tb


def simple_html(status=404):
    if not useful.is_header_done():
        print('Content-Type: text/html\n\n')
        print('Status:', status, http.client.responses.get(status, ''))
    # print('<!--\n' + str(os.environ) + '-->')
    useful.header_done()
    useful.write_comment()


def handle_exception(pif, e, header_done=False, write_traceback=True, status_code='unset'):
    log = pif.log if pif and pif.log else logger.Logger()
    log.exc.error('{} {}'.format(
        os.environ.get('REMOTE_ADDR', '127.0.0.1'),
        os.environ.get('REQUEST_URI', 'unknown')))
    str_tb = write_traceback_file(pif, e) if write_traceback else ''
    log_page_call(pif, status_code=status_code)
    if not pif or not pif.ren or not pif.dbh:
        if not header_done:
            simple_html()
        if str_tb:
            print('<!--\n' + str_tb + '-->')
        final_exit()
    pif.dbh.set_health(pif.page_id)
    if not useful.is_header_done() and not header_done:
        simple_html()
    useful.header_done()
    useful.write_comment()
    while pif.ren.table_count > 0:
        print(pif.ren.format_table_end())
    if not pif.is_allowed('a'):
        print('<!--\n' + str_tb + '-->')
        final_exit()


def final_exit():
    print("<p><h3>An error has occurred that prevents this page from displaying.  Our apologies.<br>")
    print("An alert has been sent and the problem will be fixed as soon as possible.</h3>")
    # print("<p>We're doing some upgrades, and right now, not everything is playing nicely together.<br>")
    # print("We'll get things going as soon as possible.")
    print('<p><p>Guru Meditation ID: {}'.format(config.GURU_ID))
    sys.exit()


def log_page_call(pif, status_code='unset'):
    if pif and (pif.argv or pif.is_allowed('m')):
        return  # it's me!  it's ME!
    status_code = pif.ren.status_printed if pif and pif.ren else status_code
    log = pif.log if pif and pif.log else logger.Logger()
    if os.getenv('HTTP_USER_AGENT', '') in crawls.crawlers:
        log.bot.info('{} {} {}'.format(os.environ.get('REMOTE_ADDR', '127.0.0.1'),
                                       os.environ.get('REQUEST_URI', 'unknown'), status_code))
        return
    if pif:
        pif.dbh.increment_counter(pif.page_id)
        log.count.info(pif.page_id)
        if pif.is_external_referrer():
            log.refer.info(os.environ['HTTP_REFERER'])
    log.url.info('{} {} {}'.format(os.environ.get('REMOTE_ADDR', '127.0.0.1'),
                                   os.environ.get('REQUEST_URI', 'unknown'), status_code))
    if os.getenv('HTTP_USER_AGENT'):
        log.debug.info(os.getenv('HTTP_USER_AGENT'))


# --- Command Lines -----------------------------------------------------


'''
get_command_line front-ends getopt, to make it do stuff I want it to do.
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


def get_req(sw, reqs=[]):
    if isinstance(sw, dict):
        # osw = []
        for opt in sw:
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


def get_command_line(switches="", options="", long_options={}, version="", short_help="",
                     long_help="", envar=None, noerror=False, defaults={}, doglob=False):
    switches, reqs = get_req(switches)
    options, reqs = get_req(options, reqs)
    loptions, reqs = get_req(long_options, reqs)
    switch = dict()
    opts = list()
    files = list()
    coptions = switches
    if options:
        coptions += ':'.join(list(options)) + ':'
    if 'h' not in coptions:
        coptions += 'h'
    if envar and envar in os.environ:
        try:  # get command line
            opts, files = getopt.getopt(os.environ[envar].split(), coptions, loptions)
        except getopt.GetoptError:
            if not noerror:
                print("*** Environment error")
                print(sys.argv[0], short_help, file=sys.stderr)
                sys.exit(1)

    try:  # get command line
        opts2, files2 = getopt.getopt(sys.argv[1:], coptions, loptions)
    except getopt.GetoptError:
        if not noerror:
            print("*** Options error")
            print(sys.argv[0], short_help, file=sys.stderr)
            sys.exit(2)
    opts = opts + opts2
    files = files + files2

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
            print(version, long_help, file=sys.stderr)
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
            print("*** Missing command line argument")
            print(sys.argv[0], short_help, file=sys.stderr)
            sys.exit(4)

    for key in switch:
        if switch[key] is None:
            switch[key] = defaults.get(key, False)
        elif switch[key] == [] and key in defaults:
            switch[key] = [defaults[key]]

    if doglob:
        files = functools.reduce(lambda x, y: x + y, [glob.glob(x) for x in files], [])

    return (switch, files)


# --- -------------------------------------------------------------------


# Decorator that wraps web page mains.
def web_page(main_fn):
    @functools.wraps(main_fn)
    def call_main(page_id, form_key='', defval='', args='', dbedit=None):
        # useful.write_comment('PID', os.getpid(), 'GURU', config.GURU_ID)
        status_code = 'unset'
        pif = None
        try:
            pif = (page_id if isinstance(page_id, pifile.PageInfoFile) else
                   get_page_info(page_id, form_key, defval, args, dbedit))
        except SystemExit:
            pass
        except pymysql.OperationalError as e:
            status_code = 'db'
            simple_html()
            print('The database is currently down, and thus, this page is unable to be shown.<p>')
            write_traceback_file(pif, e)
            handle_exception(pif, e, True, status_code=status_code)
            return
        except Exception as e:
            status_code = 'exc'
            simple_html()
            handle_exception(pif, e, status_code=status_code)
            return

        pif.start()

        try:
            if ('/etc/passwd' in os.environ.get('QUERY_STRING', '') or
                    '%2fetc%2fpasswd' in os.environ.get('QUERY_STRING', '').lower()):
                raise useful.Redirect('https://www.nsa.gov/')
            ret = main_fn(pif)
            if not useful.is_header_done():
                pif.ren.print_html()
            if pif.ren.is_html:
                useful.write_comment("Page:", pif.page_id, 'Time:', time.time() - pif.start_seconds)
            if ret and not pif.unittest:
                print(ret)
        except SystemExit:
            pass  # the happiest exception on earth
            status_code = 'exit'
        except useful.SimpleError as e:
            if not useful.is_header_done():
                status_code = e.status
                pif.ren.print_html(status=e.status)
            print(pif.ren.format_template('error.html', error=[e.value]))
        except useful.Redirect as e:
            if not useful.is_header_done():
                status_code = 302
                pif.ren.print_html(status=302)
            print(pif.ren.format_template('forward.html', url=e.value, delay=e.delay))
        except pymysql.OperationalError as e:
            if not useful.is_header_done():
                status_code = 500
                pif.ren.print_html(status=500)
            print('The database is currently down, and thus, this page is unable to be shown.<p>')
            write_traceback_file(pif, e)
        except Exception as e:
            status_code = 'exc'
            handle_exception(pif, e, status_code=status_code)
            raise
        useful.header_done(True)
        useful.write_comment()
        log_page_call(pif, status_code=status_code)
    return call_main


# --- -------------------------------------------------------------------


# Decorator that wraps command line mains.
def command_line(main_fn):
    @functools.wraps(main_fn)
    def call_main(page_id='cli', form_key='', defval='', args='', dbedit=None, switches='', options=''):
        useful.header_done(False)
        pif = None
        try:
            switch, filelist = get_command_line(switches, options)
            for f in filelist:
                if f.startswith('page_id='):
                    page_id = f[8:]
            if isinstance(page_id, pifile.PageInfoFile):
                pif = page_id
            else:
                pif = get_page_info(page_id, form_key, defval, args, dbedit)
            pif.switch, pif.filelist = switch, filelist
            ret = main_fn(pif)
            useful.write_comment()
            if ret:
                print(ret)
        except SystemExit:
            pass
        except useful.SimpleError as e:
            print('***', e.value)
    return call_main


# --- -------------------------------------------------------------------


# useful.py:def cmd_proc(pif, script, cmds):
# Main that processes command lists.
def process_command_list(page_id='cli', form_key='', defval='', args='', dbedit=None, cmds=[], switches='', options=''):
    pif = None
    try:
        switch, filelist = get_command_line(switches, options)
        pif = get_page_info(page_id, form_key, defval, args, dbedit)
        pif.switch, pif.filelist = switch, filelist
        useful.cmd_proc(pif, './' + os.path.split(sys.argv[0])[1], cmds)
    except SystemExit:
        pass
    except useful.SimpleError as e:
        print('***', e.value)


# --- -------------------------------------------------------------------


# Decorator for standalone (PIFless) command line mains.
def standalone(main_fn):
    @functools.wraps(main_fn)
    def call_main(switches="", options="", long_options={}, version="", short_help="", long_help="",
                  envar=None, noerror=False, defaults={}, doglob=False):
        try:
            switch, filelist = get_command_line(switches=switches, options=options, long_options=long_options,
                                                version=version, short_help=short_help, long_help=long_help,
                                                envar=envar, noerror=noerror,
                                                defaults=defaults, doglob=doglob)
            ret = main_fn(switch, filelist)
            useful.write_comment()
            if ret:
                print(ret)
        except SystemExit:
            pass
    return call_main


# --- -------------------------------------------------------------------


def goaway():
    print('Content-Type: text/html')
    print()
    print('html><body bgcolor="#FFFFFF"><img src="../pic/gfx/tested.gif"></body></html>')


if __name__ == '__main__':  # pragma: no cover
    goaway()
