#!/usr/bin/env python

from web import *
import os

os.environ['PYTHONINSPECT'] = 'True'

ctx = app.test_request_context()
ctx.push()
