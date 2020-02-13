#!/usr/local/bin/python

import sys
sys.path.append("../bin")

import editor   # noqa: E402
editor.editor_main('editor', dbedit='am')
