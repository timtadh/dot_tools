#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@gmail.com
#For licensing see the LICENSE file in the top level directory.

from nose.tools import ok_ as ok, eq_ as eq, istest

from dot_lexer import Lexer

def lexit(s, e, v=None):
    l = Lexer()
    l.input(s)
    print
    for i, (tok, et) in enumerate(zip(l, e)):
        eq(tok.type, et)
        if v:
            eq(tok.value, v[i])
        print tok
    eq(i+1, len(e))

@istest
def reserve():
    s = 'node edge graph digraph subgraph strict'
    e = ['NODE', 'EDGE', 'GRAPH', 'DIGRAPH', 'SUBGRAPH', 'STRICT']
    lexit(s, e)

@istest
def symbols():
    s = '{ } [ ] = , ; : -> --'
    e = ['LCURLY', 'RCURLY', 'LSQUARE', 'RSQUARE', 'EQUAL', 'COMMA', 'SEMI',
        'COLON', 'ARROW', 'DDASH',
    ]
    lexit(s, e)

@istest
def id_name():
    s = 'asdf w1243 ad3_23'
    e = ['ID', 'ID', 'ID', ]
    lexit(s, e)

@istest
def id_string():
    s = r'"word \" asdf" "wae\n awef" "awe \" "'
    e = ['ID', 'ID', 'ID', ]
    v = ['word \\" asdf', 'wae\\n awef', 'awe \\" ']
    lexit(s, e, v)

@istest
def id_html():
    s = '<<html>\n<body>\na"sf"awef\n</body>\n</html>> '
    e = ['ID',]
    v = ['<html>\n<body>\na"sf"awef\n</body>\n</html>']
    lexit(s, e, v)

