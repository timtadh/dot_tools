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
        return self.yacc

    def p_Graph_1(self, t):
        'Graph : GraphType GraphBody'
    def p_Graph_2(self, t):
        'Graph : GraphType ID GraphBody'
    def p_Graph_3(self, t):
        'Graph : STRICT GraphType GraphBody'
    def p_Graph_4(self, t):
        'Graph : STRICT GraphType ID GraphBody'

    def p_GraphType_1(self, t):
        '''
        GraphType : GRAPH
                  | DIGRAPH
        '''

    def p_GraphBody_1(self, t):
        'GraphBody : LCURLY StmtList RCURLY'
    def p_GraphBody_2(self, t):
        'GraphBody : LCURLY RCURLY'

    def p_StmtList_1(self, t):
        'StmtList : Stmt'
    def p_StmtList_2(self, t):
        'StmtList : Stmt SEMI'
    def p_StmtList_3(self, t):
        'StmtList : Stmt StmtList'
    def p_StmtList_4(self, t):
        'StmtList : Stmt SEMI StmtList'

    def p_Stmt_1(self, t):
        'Stmt : ID EQUAL ID'
    def p_Stmt_2(self, t):
        'Stmt : NodeStmt'
    def p_Stmt_3(self, t):
        'Stmt : EdgeStmt'
    def p_Stmt_4(self, t):
        'Stmt : AttrStmt'
    def p_Stmt_5(self, t):
        'Stmt : SubGraph'

    def p_NodeStmt_1(self, t):
        'NodeStmt : NodeId'
    def p_NodeStmt_2(self, t):
        'NodeStmt : NodeId AttrList'

    def p_NodeId_1(self, t):
        'NodeId : ID'
    def p_NodeId_2(self, t):
        'NodeId : ID Port'

    def p_Port_1(self,t):
        'Port : COLON ID'
    def p_Port_2(self,t):
        'Port : COLON ID COLON ID' # where the last id is a compass_pt

    def p_AttrStmt_1(self, t):
        'AttrStmt : AttrType AttrList'

    def p_AttrType_1(self, t):
        '''
        AttrType : NODE
                 | EDGE
                 | GRAPH
        '''

    def p_AttrList_1(self, t):
        'AttrList : LSQUARE RSQUARE'
    def p_AttrList_2(self, t):
        'AttrList : LSQUARE AList RSQUARE'
    def p_AttrList_3(self, t):
        'AttrList : LSQUARE RSQUARE AttrList'
    def p_AttrList_4(self, t):
        'AttrList : LSQUARE AList RSQUARE AttrList'

    def p_AList_1(self, t):
        'AList : AExpr'
    def p_AList_2(self, t):
        'AList : AExpr AList'

    def p_AExpr_1(self, t):
        '''
        AExpr : ID EQUAL ID
              | ID EQUAL ID COMMA
              | ID EQUAL ID SEMI
        '''

    def p_EdgeStmt_1(self, t):
        'EdgeStmt : EdgeReciever EdgeRHS'
    def p_EdgeStmt_2(self, t):
        'EdgeStmt : EdgeReciever EdgeRHS AttrList'

    def p_EdgeReciever_1(self, t):
        'EdgeReciever : NodeId'
    def p_EdgeReciever_2(self, t):
        'EdgeReciever : SubGraph'

    def p_EdgeRHS_1(self, t):
        'EdgeRHS : EdgeOp EdgeReciever'
    def p_EdgeRHS_2(self, t):
        'EdgeRHS : EdgeOp EdgeReciever EdgeRHS'

    def p_EdgeOp_1(self, t):
        '''
        EdgeOp : ARROW
               | DDASH
        '''

    def p_SubGraph_1(self, t):
        'SubGraph : GraphBody'
    def p_SubGraph_2(self, t):
        'SubGraph : SUBGRAPH GraphBody'
    def p_SubGraph_3(self, t):
        'SubGraph : SUBGRAPH ID GraphBody'

