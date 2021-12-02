LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
DIGITS = "0123456789"

ADD = "ADD"
SUB = "SUB"
MUL = "MUL"
DIV = "DIV"

MOD = "MOD"
POW = "POW"

SEMICOLON = "SEMICOLON"
COLON = "COLON"
COMMA = "COMMA"
DOT = "DOT"
BACKSLASH = "BACKSLASH"

LPAREN = "LPAREN"
RPAREN = "RPAREN"
LBRACE = "LBRACE"
RBRACE = "RBRACE"
LSQUARE = "LSQUARE"
RSQUARE = "RSQUARE"

INT = "INT"
STRING = "STRING"
IDENTIFIER = "IDENTIFIER"
ARRAY = "ARRAY"

FACTORIAL = "FACTORIAL"


class Token:
    def __init__(self, type, literal):
        self.type = type  
        self.literal = literal 
    
    def __repr__(self):
        return self.type+":"+self.literal


keywords = {
    "factorial":FACTORIAL,
}


def lookup_identifier(identifier):
    if identifier in keywords:
        return keywords[identifier]
    return IDENTIFIER