#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import multip   # noqa: E402
multip.packs_main('packs', 'page', dbedit='am')
