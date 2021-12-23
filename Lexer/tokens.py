LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
DIGITS = "0123456789"

EOF = "EOF"
ERROR = "ERROR"

ADD = "ADD"
SUB = "SUB"
MUL = "MUL"
DIV = "DIV"

MOD = "MOD"
POW = "POW"

EQ = "EQ"
EE = "EE"
NE = "NE"
LT = "LT"
GT = "GT"
LTE = "LTE"
GTE = "GTE"
NOT = "NOT"

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

LET = "LET"
DEFINE = "DEFINE"

PROGRAM_NODE = "PROGRAM_NODE"
BIN_OP_NODE = "BIN_OP_NODE"
UNARY_OP_NODE = "UNARY_OP_NODE"
VAR_ASSIGN_NODE = "VAR_ASSIGN_NODE"
FUNCTION_CALL_NODE = "FUNCTION_CALL_NODE"
INDEX_NODE = "INDEX_NODE"

INT_NODE = "INT_NODE"
STRING_NODE = "STRING_NODE"
VAR_ACCESS_NODE = "VAR_ACCESS_NODE"
ARRAY_NODE = "ARRAY_NODE"


class Token:
    def __init__(self, type, literal):
        self.type = type
        self.literal = literal

    def __repr__(self):
        return self.type + ":" + self.literal


keywords = {
    "let": LET,
    "define": DEFINE,
    "per": DIV,
    "for": DIV,
    "add": ADD,
    "and": ADD,
    "by": MUL,
    "times": MUL,
    "is": EQ,
    "take": SUB,
}


def lookup_identifier(identifier):
    if identifier in keywords:
        return keywords[identifier]
    return IDENTIFIER
