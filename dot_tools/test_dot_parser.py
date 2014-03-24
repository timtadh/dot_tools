#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@gmail.com
#For licensing see the LICENSE file in the top level directory.

from nose.tools import ok_ as ok, eq_ as eq, istest

from dot_parser import Parser

@istest
def yaccs():
    p = Parser()
