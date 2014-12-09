#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import multipack
multipack.do_page('packs', 'page', dbedit='am')
