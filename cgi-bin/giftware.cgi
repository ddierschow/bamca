#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import multip   # noqa: E402
multip.giftware_main('giftware', 'page', dbedit='am')
