#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import busers
busers.change_password_main('user', dbedit='')
