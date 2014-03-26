#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@gmail.com
#For licensing see the LICENSE file in the top level directory.


class SimpleGraph(object):

    def __init__(self):
        self.nodes = dict()
        self.edges = list()

    @staticmethod
    def build(ast):
        self = SimpleGraph()
        self._walk(ast)
        return self

    def _walk(self, root):
        for kid in root.kid('Stmts').children:
            if kid.label == 'Nodes':
                self._walk_nodes(kid)
            elif kid.label == 'Edges':
                self._walk_edges(kid)

    def _walk_nodes(self, n):
        for kid in n.children:
            if kid.label == 'Node':
                self._walk_node(kid)

    def _walk_edges(self, n):
        for kid in n.children:
            if kid.label == '->':
                self._walk_dedge(kid)
            if kid.label == '--':
                self._walk_edge(kid)

    def _walk_node(self, n):
        nid = n.children[0].label
        label = self._get_label(n)
        if label is None:
            label = nid
        self.nodes[nid] = label

    def _walk_edge(self, n):
        aid, bid, label = self._edge_info(n)
        self.edges.append((aid, bid, label))
        self.edges.append((bid, aid, label))

    def _walk_dedge(self, n):
        aid, bid, label = self._edge_info(n)
        self.edges.append((aid, bid, label))

    def _edge_info(self, n):
        aid = n.children[0].label
        bid = n.children[1].label
        if aid not in self.nodes:
            self.nodes[aid] = aid
        if bid not in self.nodes:
            self.nodes[bid] = bid
        label = self._get_label(n)
        if label is None:
            label = ''
        return aid, bid, label

    def _get_label(self, n):
        attrs = n.kid('Attrs')
        if attrs is not None:
            attrs = self._walk_attrs(attrs)
            if 'label' in attrs:
                return attrs['label']
        return None

    def _walk_attrs(self, n):
        attrs = dict()
        for kid in n.children:
            if kid.label == '=':
                self._walk_attr(attrs, kid)
        return attrs

    def _walk_attr(self, attrs, n):
        attrs[n.children[0].label] = n.children[1].label


