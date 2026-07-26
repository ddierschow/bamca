#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import vredit   # noqa: E402
vredit.handle_form('editor', dbedit='am')
