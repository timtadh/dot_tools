#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@gmail.com
#For licensing see the LICENSE file in the top level directory.

import os, sys

from nose.tools import ok_ as ok, eq_ as eq, istest

from dot_parser import Parser
from dot_lexer import Lexer

@istest
def yaccs():
    t = Parser().parse('''
      # witch
      strict digraph { // comment
        a [label="asf"]
        q=r;
        /* asdfa */
        graph [x=y]
        b:a:ne # wizard
        a -> b;
        b->a [label=backedge]
        subgraph sq { c -> d} -> subgraph {e->f}
      }# junk
      # what
      graph {
        x;
      }
    ''', lexer=Lexer())
    eq(t.label, 'Graphs')
    eq(
      [k.label for k in t.children],
      ['Comment','Graph','Comment','Comment','Graph']
    )
    graphs = [k for k in t.children if k.label == 'Graph']

    graph = graphs[1]
    eq(
      [k.label for k in graph.kid('Stmts').children],
      ['Nodes']
    )
    n = graph.descendent('Node')
    eq(n.children[0].label, 'x')

    graph = graphs[0]
    eq(
      set([k.label for k in graph.kid('Stmts').children]),
      set(['Nodes', 'Edges', 'Comments', 'graphAttrs', 'Assigns'])
    )

