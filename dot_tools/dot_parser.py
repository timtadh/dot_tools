#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@hackthology.com
#For licensing see the LICENSE file in the top level directory.

from ply import yacc
from dot_lexer import tokens, Lexer

from betterast import Node


'''
graph   :   [ strict ] (graph | digraph) [ ID ] '{' stmt_list '}'
stmt_list   :   [ stmt [ ';' ] [ stmt_list ] ]
stmt    :   node_stmt
    |   edge_stmt
    |   attr_stmt
    |   ID '=' ID
    |   subgraph
attr_stmt   :   (graph | node | edge) attr_list
attr_list   :   '[' [ a_list ] ']' [ attr_list ]
a_list  :   ID '=' ID [ (';' | ',') ] [ a_list ]
edge_stmt   :   (node_id | subgraph) edgeRHS [ attr_list ]
edgeRHS     :   edgeop (node_id | subgraph) [ edgeRHS ]
node_stmt   :   node_id [ attr_list ]
node_id     :   ID [ port ]
port        :   ':' ID [ ':' compass_pt ]
            |   ':' compass_pt
subgraph    :   [ subgraph [ ID ] ] '{' stmt_list '}'
compass_pt  :   (n | ne | e | se | s | sw | w | nw | c | _)
'''

## If you are confused about the syntax in this file I recommend reading the
## documentation on the PLY website to see how this compiler compiler's syntax
## works.
class Parser(object):

    tokens = tokens
    precedence = (
    )

    def __new__(cls, **kwargs):
        ## Does magic to allow PLY to do its thing.
        self = super(Parser, cls).__new__(cls, **kwargs)
        self.loc = list()
        self.yacc = yacc.yacc(
            module=self,
            tabmodule="dot_parser_tab",
            debug=0,
            **kwargs
        )
        self.g_id = 1000
        return self.yacc

    def next_g_id(self):
        self.g_id += 1
        return 'graph_%d' % self.g_id

    def p_error(self, t):
        print t
        raise SyntaxError(t)

    def p_Graphs_1(self, t):
        'Graphs : Graph'
        t[0] = Node('Graphs').addkid(t[1])
    def p_Graphs_3(self, t):
        'Graphs : Graphs Graph'
        t[0] = Node('Graphs', children=t[1].children+[t[2]])

    def p_Graph_1(self, t):
        'Graph : GraphStmt'
        t[0] = t[1]
    def p_Graph_2(self, t):
        'Graph : COMMENT'
        t[0] = Node('Comment').addkid(Node(t[1]))

    def p_GraphStmt_1(self, t):
        'GraphStmt : GraphType GraphBody'
        t[0] = Node('Graph').addkid(t[1]).addkid(Node(self.next_g_id())).addkid(t[2])
    def p_GraphStmt_2(self, t):
        'GraphStmt : GraphType ID GraphBody'
        t[0] = Node('Graph').addkid(t[1]).addkid(Node(t[2])).addkid(t[3])
    def p_GraphStmt_3(self, t):
        'GraphStmt : STRICT GraphType GraphBody'
        t[0] = Node('Graph').addkid(t[2].addkid(Node('strict'))).addkid(Node(self.next_g_id())).addkid(t[3])
    def p_GraphStmt_4(self, t):
        'GraphStmt : STRICT GraphType ID GraphBody'
        t[0] = Node('Graph').addkid(t[2].addkid(Node('strict'))).addkid(Node(t[3])).addkid(t[4])

    def p_GraphType_1(self, t):
        '''
        GraphType : GRAPH
                  | DIGRAPH
        '''
        t[0] = Node(t[1])

    def p_GraphBody_1(self, t):
        'GraphBody : LCURLY StmtList RCURLY'
        t[0] = t[2]
    def p_GraphBody_3(self, t):
        'GraphBody : LCURLY RCURLY'
        t[0] = Node('Stmts')

    def p_StmtList_1(self, t):
        '''
        StmtList : Stmt
                 | Stmt SEMI
        '''
        t[0] = Node('Stmts').addkid(t[1])
    def p_StmtList_2(self, t):
        '''
        StmtList : Stmt StmtList
                 | Stmt SEMI StmtList
        '''
        stmts = t[len(t)-1]
        kids = [t[1]] + stmts.children
        types = dict()
        for kid in kids:
            items = types.get(kid.label, list())
            items += kid.children
            types[kid.label] = items
        children = list()
        for k,v in types.iteritems():
            children.append(Node(k, children=v))
        t[0] = Node('Stmts', children=children)

    def p_Stmt_1(self, t):
        'Stmt : ID EQUAL ID'
        t[0] = Node('Assigns').addkid(Node('=').addkid(t[1]).addkid(t[3]))
    def p_Stmt_2(self, t):
        'Stmt : NodeStmt'
        t[0] = Node('Nodes').addkid(t[1])
    def p_Stmt_3(self, t):
        'Stmt : EdgeStmt'
        t[0] = t[1]
    def p_Stmt_4(self, t):
        'Stmt : AttrStmt'
        t[0] = t[1]
    def p_Stmt_5(self, t):
        'Stmt : SubGraph'
        t[0] = t[1]
    def p_Stmt_6(self, t):
        'Stmt : COMMENT'
        t[0] = Node('Comments').addkid(t[1])

    def p_NodeStmt_1(self, t):
        'NodeStmt : NodeId'
        t[0] = Node('Node').addkid(t[1])
    def p_NodeStmt_2(self, t):
        'NodeStmt : NodeId AttrList'
        t[0] = Node('Node').addkid(t[1]).addkid(Node('Attrs', children=t[2]))

    def p_NodeId_1(self, t):
        'NodeId : ID'
        t[0] = Node(t[1])
    def p_NodeId_2(self, t):
        'NodeId : ID Port'
        t[0] = Node(t[1]).addkid(t[2])

    def p_Port_1(self,t):
        'Port : COLON ID'
        t[0] = Node('Port').addkid(Node(t[2]))
    def p_Port_2(self,t):
        'Port : COLON ID COLON ID' # where the last id is a compass_pt
        if t[4] not in ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw', 'c', '_']:
            raise Exception("ID %s is not a compass point" % t[4])
        t[0] = Node('Port').addkid(Node(t[2])).addkid(Node(t[4]))

    def p_AttrStmt_1(self, t):
        'AttrStmt : AttrType AttrList'
        t[0] = Node(t[1]+'Attrs', children=t[2])

    def p_AttrType_1(self, t):
        '''
        AttrType : NODE
                 | EDGE
                 | GRAPH
        '''
        t[0] = t[1]

    def p_AttrList_1(self, t):
        'AttrList : LSQUARE RSQUARE'
        t[0] = []
    def p_AttrList_2(self, t):
        'AttrList : LSQUARE AList RSQUARE'
        t[0] = t[2]
    def p_AttrList_3(self, t):
        'AttrList : LSQUARE RSQUARE AttrList'
        t[0] = t[3]
    def p_AttrList_4(self, t):
        'AttrList : LSQUARE AList RSQUARE AttrList'
        t[0] = t[2] + t[4]

    def p_AList_1(self, t):
        'AList : AExpr'
        t[0] = [t[1]]
    def p_AList_2(self, t):
        'AList : AExpr AList'
        t[0] = [t[1]] + t[2]

    def p_AExpr_1(self, t):
        '''
        AExpr : ID EQUAL ID
              | ID EQUAL ID COMMA
              | ID EQUAL ID SEMI
        '''
        t[0] = Node('=').addkid(Node(t[1])).addkid(Node(t[3]))

    def p_EdgeStmt_1(self, t):
        '''
        EdgeStmt : EdgeReciever EdgeRHS
                 | EdgeReciever EdgeRHS AttrList
        '''
        p = t[1]
        edges = list()
        for op, n in t[2]:
            e = Node(op.label).addkid(p).addkid(n)
            if len(t) == 4:
                e.addkid(Node('Attrs', children=t[3]))
            edges.append(e)
            p = n
        t[0] = Node('Edges', children=edges)

    def p_EdgeReciever_1(self, t):
        'EdgeReciever : NodeId'
        t[0] = t[1]
    def p_EdgeReciever_2(self, t):
        'EdgeReciever : SubGraph'
        t[0] = t[1]

    def p_EdgeRHS_1(self, t):
        'EdgeRHS : EdgeOp EdgeReciever'
        t[0] = [(t[1], t[2])]
    def p_EdgeRHS_2(self, t):
        'EdgeRHS : EdgeOp EdgeReciever EdgeRHS'
        t[0] = [(t[1], t[2])] + t[3]

    def p_EdgeOp_1(self, t):
        '''
        EdgeOp : ARROW
               | DDASH
        '''
        t[0] = Node(t[1])

    def p_SubGraph_1(self, t):
        'SubGraph : GraphBody'
        t[0] = Node('SubGraph').addkid(Node(self.next_g_id())).addkid(t[1])
    def p_SubGraph_2(self, t):
        'SubGraph : SUBGRAPH GraphBody'
        t[0] = Node('SubGraph').addkid(Node(self.next_g_id())).addkid(t[2])
    def p_SubGraph_3(self, t):
        'SubGraph : SUBGRAPH ID GraphBody'
        t[0] = Node('SubGraph').addkid(Node(t[2])).addkid(t[3])

