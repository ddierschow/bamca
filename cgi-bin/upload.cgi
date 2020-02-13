#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import images   # noqa: E402
images.upload_main('editor', dbedit='')
