#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import tlinks   # noqa: E402
tlinks.edit_links('editor', dbedit='am')
