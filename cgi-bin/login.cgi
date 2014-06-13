#!/usr/local/bin/python


if __name__ == '__main__':
    pif = None
    import basics
    try:
	pif = basics.GetPageInfo('user')
	import user
	user.LoginMain(pif)

    except:
	basics.HandleException(pif)
	raise
