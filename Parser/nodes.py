from lexer.tokens import *

class ProgramNode:
    def __init__(self,expressions):
        self.type = PROGRAM_NODE
        self.expressions = expressions

    def __repr__(self):
        return ",".join(str(exp) for exp in self.expressions)

class BinOpNode:
    def __init__(self,left,op,right):
        self.type = BIN_OP_NODE
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return "(" + self.left.__repr__() +":"+ self.op +":"+ self.right.__repr__() + ")"

class UnaryOpNode:
    def __init__(self,op,right):
        self.type = UNARY_OP_NODE
        self.op = op 
        self.right = right


class VarAccessNode:
    def __init__(self,identifier):
        self.type = VAR_ACCESS_NODE
        self.identifier = identifier

class StringNode:
    def __init__(self,value):
        self.type = STRING_NODE
        self.value = value

class IntNode:
    def __init__(self,value):
        self.type = INT_NODE
        self.value = value
    
    def __repr__(self):
        return str(self.value)