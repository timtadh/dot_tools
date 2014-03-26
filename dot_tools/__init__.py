#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@gmail.com
#For licensing see the LICENSE file in the top level directory.


import dot_parser, dot_lexer

def parse(string):
    return dot_parser.Parser().parse(string, lexer=dot_lexer.Lexer())

