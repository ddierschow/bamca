#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import busers   # noqa: E402
busers.register_main('user', dbedit='')
