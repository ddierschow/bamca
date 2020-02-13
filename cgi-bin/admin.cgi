#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import mannum   # noqa: E402
mannum.admin_main('editor', dbedit='ma')
