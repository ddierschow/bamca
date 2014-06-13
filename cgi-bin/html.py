import re

cm_re = re.compile(r'<!--.*?-->', re.S)
hl_re = re.compile(r'\\hline')
ml_re = re.compile(r'<[^>]*>', re.S)
tab_re = re.compile(r'<table[^>]*>(?P<c>.*?)</table>', re.S)
row_re = re.compile(r'<tr[^>]*>(?P<c>.*?)</tr>', re.S)
cel_re = re.compile(r'<t(?P<t>[hd])[^>]*>(?P<c>.*?)</t[hd]>', re.S)
div_re = re.compile('</?div.*?>', re.S | re.M)

def GetHtmlTables(fn):
    f = open(fn).read()
    f = cm_re.sub('', f)
    f = hl_re.sub('', f)
    f = div_re.sub('', f)

    tables = list()
    while 1:
	fitab = tab_re.search(f)
	if not fitab:
	    rest = f
	    break

	pred = f[:fitab.start()]
	tab_con = fitab.group('c')
	rows = list()
	while 1:
	    row = row_re.search(tab_con)
	    if not row:
		break

	    row_con = row.group('c')
	    cels = list()
	    while 1:
		cel = cel_re.search(row_con)
		if not cel:
		    break

		cel_con = ml_re.sub('', cel.group('c'))
		cels.append(cel_con)

		row_con = row_con[cel.end():]
	    tab_con = tab_con[row.end():]
	    rows.append(cels)
	f = f[fitab.end():]
	tables.append([pred, rows, ''])
    if tables:
	tables[-1][-1] = rest
    else:
	tables.append(['', list(), rest])
    return tables


if __name__ == '__main__': # pragma: no cover
    print '''Content-Type: text/html\n\n<html><body bgcolor="#FFFFFF"><img src="../pics/tested.gif"></body></html>'''

