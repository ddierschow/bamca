import glob, re, unittest

class TestCirc(unittest.TestCase):

    def setUp(self):
	pass

    def test_circular_imports(self):
	import_re = re.compile('''\w*import\w+(?P<f>[^#]*)''')
	from_re = re.compile('''\w*from\w+(?P<f>[^#]*)\w+import''')
	data = {}
	for py in glob.glob('../bin/*.py'):
	    fn = py[py.rfind('/') + 1:-3]
	    data[fn] = list()
	    for ln in open(py).readlines():
		import_m = import_re.match(ln)
		if import_m:
		    data[fn].extend([x.strip() for x in import_m.group('f').split(',')])
	changed = True
	while changed:
	    changed = False
	    for key in sorted(data):
		data[key] = [x for x in sorted(data[key]) if x in data]
	    for key in sorted(data):
		if not data[key]:
		    del data[key]
		    changed = True
	self.assertTrue(not data)

# ---- ----------------------------------------------------

if __name__ == '__main__': # pragma: no cover
    unittest.main()
