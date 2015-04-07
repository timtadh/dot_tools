#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@gmail.com
#For licensing see the LICENSE file in the top level directory.

import cgi

class SimpleGraph(object):

    def __init__(self):
        self.nodes = dict()
        self.index = dict()
        self.edges = list()

    @staticmethod
    def build(ast):
        self = SimpleGraph()
        self._walk(ast)
        return self

    def dotty_nid(self, nid):
        return str(nid)

    def dotty(self, name, no_header_footer=False, html=False):
        def string(label):
            if html:
                label = (
                    label.replace("'", "\\'").
                    replace('"', '\\"').
                    replace('\n', '\\n')
                )
                label = cgi.escape(label).encode('ascii', 'xmlcharrefreplace')
                s = ''.join(
                    '<tr><td align="left">' + line + "</td></tr>"
                    for line in label.split('\\n')
                )
            else:
                s = (
                    label.replace('"', '').
                    replace('"', '').
                    replace('\\', '').
                    replace('\n', '')
                )
            return s

        header = 'digraph %s {' % name
        footer = '}'
        if html:
            node = '%s [shape=rect, fontname="Courier", label=<<table border="0">%s</table>>];'
        else:
            node = '%s [label="%s"];'
        edge = '%s->%s [label="%s"];'
        nodes = list()
        edges = list()

        keys = sorted(self.nodes.keys())
        for nid in keys:
            nodes.append(node % (self.dotty_nid(nid), string(self.nodes[nid].get('label', nid))))

        for s, t, label in self.edges:
            edges.append(edge % (self.dotty_nid(s), self.dotty_nid(t), label))

        if no_header_footer:
            return (
                '\n'.join(nodes) + '\n' +
                '\n'.join(edges) + '\n'
            )
        return (
            header + '\n' +
            '\n'.join(nodes) + '\n' +
            '\n'.join(edges) + '\n' +
            footer + '\n'
        )

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
        attrs = self._walk_attrs(n.kid('Attrs'))
        label = self._get_label(attrs)
        self.nodes[nid] = attrs
        if label is not None:
            self.index[label] = nodes = self.index.get(label, list())
            nodes.append(nid)

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
            self.nodes[aid] = {}
        if bid not in self.nodes:
            self.nodes[bid] = {}
        attrs = self._walk_attrs(n.kid('Attrs'))
        label = self._get_label(attrs)
        if label is None:
            label = ''
        return aid, bid, label

    def _get_label(self, attrs):
        if attrs is not None:
            if 'label' in attrs:
                return attrs['label']
        return None

    def _walk_attrs(self, n):
        if n is None:
            return {}
        attrs = dict()
        for kid in n.children:
            if kid.label == '=':
                self._walk_attr(attrs, kid)
        return attrs

    def _walk_attr(self, attrs, n):
        attrs[n.children[0].label] = n.children[1].label


