#!/usr/local/bin/python


if __name__ == '__main__':
    pif = None
    import basics
    try:
	pif = basics.GetPageInfo('user')
	import user
	if pif.form.get('n'):
	    user.Create(pif)
	elif pif.form.get('k'):
	    u = pif.form['u']
	    k = pif.form['k']
	    user.Verify(pif, u, k)
	else:
	    pif.render.PrintHtml()
	    user.PrintSignupForm(pif)
    except:
	basics.HandleException(pif)
	raise
