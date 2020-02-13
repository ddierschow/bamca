#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import busers   # noqa: E402
busers.change_password_main('user', dbedit='')
