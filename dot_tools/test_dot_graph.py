#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@gmail.com
#For licensing see the LICENSE file in the top level directory.


import os, sys

from nose.tools import ok_ as ok, eq_ as eq, istest

from dot_parser import Parser
from dot_lexer import Lexer
from dot_graph import SimpleGraph


@istest
def build_graph():
    t = Parser().parse('''
      strict digraph {
        e [label=<<html>asdf</html>>]
        a -> b -> c -> d;
        d -> e -> f [label=x]
      }
      graph {
        x [label="quantal"];
      }
    ''', lexer=Lexer())
    graphs = [k for k in t.children if k.label == 'Graph']
    g = SimpleGraph.build(graphs[1])
    eq(g.nodes, {'x':'quantal'})
    eq(g.edges, [])

    g = SimpleGraph.build(graphs[0])
    eq(g.nodes, {'a':'a', 'b':'b', 'c':'c', 'd':'d', 'e':'<html>asdf</html>', 'f':'f'})
    eq(set(g.edges),
      set([
        ('a', 'b', ''),
        ('b', 'c', ''),
        ('c', 'd', ''),
        ('d', 'e', 'x'),
        ('e', 'f', 'x'),
      ])
    )

