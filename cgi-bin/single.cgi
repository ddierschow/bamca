#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import single   # noqa: E402
single.show_single('single', dbedit='am')
