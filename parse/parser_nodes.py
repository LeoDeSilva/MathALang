from lexer.tokens import *

class ProgramNode:
    def __init__(self,expressions):
        self.type = PROGRAM_NODE
        self.expressions = expressions