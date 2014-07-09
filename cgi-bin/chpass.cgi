#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import busers
busers.ChangePasswordMain('user', dbedit='')
