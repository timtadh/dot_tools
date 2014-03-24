  #!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Tim Henderson
#Email: tim.tadh@gmail.com
#For licensing see the LICENSE file in the top level directory.

from ply import lex
from ply.lex import Token, LexToken

reserved = dict(
    (word.lower(), word) for word in (
        'NODE', 'EDGE', 'GRAPH', 'DIGRAPH', 'SUBGRAPH', 'STRICT',
    )
)

tokens = reserved.values() + [
    'ID',
    'LSQUARE', 'RSQUARE', 'LCURLY', 'RCURLY',
    'EQUAL', 'COMMA', 'SEMI', 'COLON', 'ARROW', 'DDASH',
]

# Common Regex Parts

D = r'[0-9]'
L = r'[a-zA-Z_]'
H = r'[a-fA-F0-9]'
E = r'[Ee][+-]?(' + D + ')+'

'''
An ID is one of the following:
Any string of alphabetic ([a-zA-Z\200-\377]) characters, underscores ('_') or digits ([0-9]), not beginning with a digit;
a numeral [-]?(.[0-9]+ | [0-9]+(.[0-9]*)? );
any double-quoted string ("...") possibly containing escaped quotes (\")1;
an HTML string (<...>). 
'''

class MyLexToken(LexToken):
    def __init__(self, name, value, lineno, lexpos):
        self.type = name
        self.value = value
        self.lineno = lineno
        self.lexpos = lexpos

## Normally PLY works at the module level. I perfer having it encapsulated as
## a class. Thus the strange construction of this class in the new method allows
## PLY to do its magic.
class Lexer(object):

    tokens = tokens

    t_ARROW = r'->'
    t_DDASH = r'--'
    t_COLON = r':'
    t_SEMI = r'\;'
    t_EQUAL = r'='
    t_COMMA = r','
    t_LSQUARE = r'\['
    t_RSQUARE = r'\]'
    t_LCURLY = r'\{'
    t_RCURLY = r'\}'

    # Ignored characters
    t_ignore = " \t"

    def __new__(cls, **kwargs):
        self = super(Lexer, cls).__new__(cls, **kwargs)
        self.lexer = lex.lex(object=self, **kwargs)
        return self.lexer

    name = '(' + L + ')((' + L + ')|(' + D + '))*'
    @Token(name)
    def t_ID_Name(self, token):
        if token.value in reserved: token.type = reserved[token.value]
        else: token.type = 'ID'
        return token

    name = r'-?((\.[0-9]+)|([0-9]+(\.[0-9]*)?))'
    @Token(name)
    def t_ID_Number(self, token):
        token.type = 'ID'
        token.value = float(token.value)
        return token

    name = r'".*?"'
    @Token(name)
    def t_ID_String(self, token):
        token.type = 'ID'
        if token.value[-2] == '\\':
            lexpos = self.lexer.lexpos
            lexdata = self.lexer.lexdata
            lexstart = lexpos - len(token.value)
            while lexpos < self.lexer.lexlen:
                lexpos += 1
                if lexdata[lexpos] == '\n':
                    raise Exception, "could not lex string"
                if lexdata[lexpos] == '"' and lexdata[lexpos-1] != '\\':
                    self.lexer.lexpos = lexpos+1
                    return MyLexToken(
                        'ID', lexdata[lexstart+1:lexpos], token.lineno, lexstart)
            return None
        token.value = token.value[1:-1]
        return token

    name = r'<(.|\n)*>'
    @Token(name)
    def t_ID_Html(self, token):
        token.type = 'ID'
        token.value = token.value[1:-1]
        return token

    @Token(r'\n+')
    def t_newline(self, t):
        t.lexer.lineno += t.value.count("\n")

    @Token(r'\#.*')
    def t_COMMENT(self, token):
        return None

    @Token(r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)')
    def t_COMMENT_C(self, token):
        lines = len(token.value.split('\n')) - 1
        if lines < 0: lines = 0
        token.lexer.lineno += lines

    def t_error(self, t):
        #raise Exception, "Illegal character '%s'" % t
        t.lexer.skip(1)

