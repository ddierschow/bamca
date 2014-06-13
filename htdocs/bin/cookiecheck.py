#!/usr/local/bin/python

import datetime, os, sys

def GetCookies(rawcookie):
    #fl = open('/usr/local/www/bamca/rel6/htdocs/tb/cookies', 'a')
    sys.path.append('../cgi-bin')
#    import CryptCookie
    #fl.write(datetime.datetime.now().strftime('%s') + ' ckpt 1\n')
#    cook = CryptCookie.CryptCookie(rawcookie.replace(' ', '+'))
    #fl.write(datetime.datetime.now().strftime('%s') + ' ckpt 2\n')
#    if not cook:
#	return {}
#    return dict(zip(['id','ip','pr'], cook['id'].value.split('/')))

    import secure
    security = secure.Security()
    cookieval = security.cookie_decode(cookie['id'].value)
    if not '/' in cookieval:
	#sys.stderr.write("cookie format error\n")
	return {}
    try:
	ret = dict(zip(['id','ip','pr'], cookieval.split('/')))
    except:
	#sys.stderr.write("cookie split error\n")
	#sys.stderr.write("  '%s' -> '%s'\n" % (cookie['id'].value, cookieval))
	return {}
    ret['co'] = cookie
    return ret


if __name__ == '__main__':
    cook = GetCookies(sys.argv[2])
    if sys.argv[1] == 'id':
	sys.exit(int(cook.get('id', 0)))
    elif sys.argv[1] in 'vuma':
	if sys.argv[1] in cook.get('pr', ''):
	    sys.exit(1)
	sys.exit(0)
