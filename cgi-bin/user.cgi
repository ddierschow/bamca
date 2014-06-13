#!/usr/local/bin/python


if __name__ == '__main__':
    pif = None
    import basics
    try:
	pif = basics.GetPageInfo('user')
	pif.render.PrintHtml()
	pif.Restrict('a')
	print pif.render.FormatHead(extra=pif.render.reset_button_js)
	import user
	user.UserMain(pif)
	print pif.render.FormatTail()
    except:
	basics.HandleException(pif)
	raise
