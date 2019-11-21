from Exceptions import(LexException, ParseException)
from enum import Enum

def parse(text):
    return prog(lex(text))

####################################################################
# Lexer
# converts a string of characters into a list of tokens
# so "a && b -> T"
# becomes [Token(TVAR,0,"a"), Token(TAND,2), Token(TVAR,5,"b"),
#          Token(TARROW,7), Token(TTRUE,10)]
####################################################################


class TType(Enum):
    TCOMMA  = ","
    TARROW  = ":-"
    TPERIOD = "."
    TVAR    = "<var>"
    TEOF    = "<EOF>"
    def __init__(self, n):
        self.n = n
    def __str__(self):
        return self.n

class Token():
    def __init__(self, ttype, row, col, val):
        self.ttype = ttype
        self.row = row
        self.col = col
        self.val = val
    def __str__(self):
        return "<"+self.val+","+str(self.row)+","+str(self.col)+","+str(self.ttype)+">"

def alpha(c):
    return 'a' <= c <= 'z' or 'A' <= c <= 'Z'


def lex(text):
    row = 0
    col = 0
    i = 0
    tokens = []
    while i < len(text):
        c = text[i]
        if i+1 < len(text):
            n = text[i+1]
        else:
            n = ""

        if c in " \t": # skip whitespace
            pass
        elif c in "\r\n": # next line
            row += 1 
            col = 0
        elif c == ',':
            tokens.append(Token(TType.TCOMMA,row,col,","))
        elif c == '.':
            tokens.append(Token(TType.TPERIOD,row,col,"."))
        elif c+n == ':-':
            tokens.append(Token(TType.TARROW,row,col,":-"))
            i += 1
            col += 1
        elif alpha(c):
            j = 0
            var = ""
            while i+j < len(text) and alpha(text[i+j]):
                var += text[i+j]
                j += 1
            tokens.append(Token(TType.TVAR,row,col,var))
            i += (j-1)

        else:
            raise LexException(row,col,c)

        i += 1
        col += 1
    tokens.append(Token(TType.TEOF,row,col,"<EOF>"))
    return tokens

# P => R*
# R => <var> :- (<var>,)* <var>.
# R => <var>.

def prog(tokens):
    program = {}
    while tokens[0].ttype != TType.TEOF:
        (v,rule) = readClause(tokens)
        if v not in program:
            program[v] = [rule]
        else:
            program[v].append(rule)
    return program

def readClause(tokens):
    if tokens[0].ttype != TType.TVAR:
        raise ParseException(tokens[0].row,tokens[0].col,[TType.TVAR],tokens[0].val)
    v = tokens.pop(0).val
    if tokens[0].ttype == TType.TARROW:
        tokens.pop(0)
        if tokens[0].ttype != TType.TVAR:
            raise ParseException(tokens[0].row,tokens[0].col,[TType.TVAR],tokens[0].val)
        clause = [tokens.pop(0).val]
        while tokens[0].ttype != TType.TPERIOD:
            if tokens[0].ttype != TType.TCOMMA:
                raise ParseException(tokens[0].row,tokens[0].col,[TType.TVAR],tokens[0].val)
            if tokens[1].ttype != TType.TVAR:
                raise ParseException(tokens[1].row,tokens[1].col,[TType.TVAR],tokens[1].val)
            clause.append(tokens[1].val)
            tokens.pop(0)
            tokens.pop(0)
        tokens.pop(0)
        return (v,clause)
    if tokens[0].ttype == TType.TPERIOD:
        tokens.pop(0)
        return (v,[])
    raise ParseException(tokens[0].row,tokens[0].col,[TType.TARROW,TType.TPERIOD],tokens[0].val)

