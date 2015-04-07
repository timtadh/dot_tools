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
    eq(g.nodes, {'x':{'label': 'quantal'}})
    eq(g.edges, [])

    g = SimpleGraph.build(graphs[0])
    eq(g.nodes, {'a':{}, 'b':{}, 'c':{}, 'd':{}, 'e':{'label':'<html>asdf</html>'}, 'f':{}})
    eq(set(g.edges),
      set([
        ('a', 'b', ''),
        ('b', 'c', ''),
        ('c', 'd', ''),
        ('d', 'e', 'x'),
        ('e', 'f', 'x'),
      ])
    )

@istest
def simple_dot_equality():
    t = Parser().parse('''
      digraph G {
        a [label="wizard"];
        b [label="wally"];
        c [label="wonky"];
        d [label="wozniac"];
        a->b [label=""];
        a->c [label=""];
        c->d [label=""];
        d->a [label="backref"];
      }
    ''', lexer=Lexer())
    t2 = Parser().parse(SimpleGraph.build(t.kid('Graph')).dotty('G'), lexer=Lexer())
    for a, b in zip(t, t2):
        print a.label, b.label
    eq(t, t2)

