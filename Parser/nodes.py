from Lexer.tokens import *
from Parser.functions import *


class ProgramNode:
    def __init__(self, expressions):
        self.type = PROGRAM_NODE
        self.expressions = expressions

    def eval(self, environment):
        for expr in self.expressions:
            print(expr.eval(environment))

    def __repr__(self):
        return "PROGRAM_NODE:" + ",".join(str(exp) for exp in self.expressions)


class VarAssignNode:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
        self.type = VAR_ASSIGN_NODE

    def eval(self, environment):
        result = self.expression.eval(environment)
        environment.variables[self.identifier] = result
        return result

    def __repr__(self):
        return (
            "VAR_ACCESS:"
            + self.identifier.__repr__()
            + "="
            + self.expression.__repr__()
        )


class ArrayNode:
    def __init__(self, nodes):
        self.type = ARRAY_NODE
        self.nodes = nodes

    def eval(self, environment):
        array = []
        for node in self.nodes:
            array.append(node.eval(environment))
        return array

    def __repr__(self):
        return "ARRAY NODE:" + "[" + ",".join(str(exp) for exp in self.nodes) + "]"


class BinOpNode:
    def __init__(self, left, op, right):
        self.type = BIN_OP_NODE
        self.left = left
        self.op = op
        self.right = right

    def eval(self, environment):
        if self.op == ADD:
            return self.left.eval(environment) + self.right.eval(environment)
        elif self.op == SUB:
            return self.left.eval(environment) - self.right.eval(environment)
        elif self.op == DIV:
            return self.left.eval(environment) / self.right.eval(environment)
        elif self.op == MUL:
            return self.left.eval(environment) * self.right.eval(environment)
        elif self.op == MOD:
            return self.left.eval(environment) % self.right.eval(environment)
        elif self.op == POW:
            return self.left.eval(environment) ** self.right.eval(environment)

        elif self.op == EE:
            return (
                1 if self.left.eval(environment) == self.right.eval(environment) else 0
            )
        elif self.op == NE:
            return (
                1 if self.left.eval(environment) != self.right.eval(environment) else 0
            )
        elif self.op == GT:
            return (
                1 if self.left.eval(environment) > self.right.eval(environment) else 0
            )
        elif self.op == GTE:
            return (
                1 if self.left.eval(environment) >= self.right.eval(environment) else 0
            )
        elif self.op == LT:
            return (
                1 if self.left.eval(environment) < self.right.eval(environment) else 0
            )
        elif self.op == LTE:
            return (
                1 if self.left.eval(environment) <= self.right.eval(environment) else 0
            )

    def __repr__(self):
        return (
            "("
            + self.left.__repr__()
            + ":"
            + self.op
            + ":"
            + self.right.__repr__()
            + ")"
        )


class UnaryOpNode:
    def __init__(self, op, right):
        self.type = UNARY_OP_NODE
        self.op = op
        self.right = right

    def eval(self, environment):
        if self.op == SUB:
            return -(self.right.eval(environment))
        elif self.op == NOT:
            return 1 if self.right.eval(environment) == 0 else 0

    def __repr__(self):
        return self.op + "(" + self.right.__repr__() + ")"


class VarAccessNode:
    def __init__(self, identifier):
        self.type = VAR_ACCESS_NODE
        self.identifier = identifier

    def eval(self, environment):
        return environment.variables[self.identifier]

    def __repr__(self):
        return "VAR_ACCESS:" + self.identifier


class StringNode:
    def __init__(self, value):
        self.type = STRING_NODE
        self.value = value

    def eval(self, environment):
        return self.value

    def __repr__(self):
        return "STRING:" + self.value


class IntNode:
    def __init__(self, value):
        self.type = INT_NODE
        self.value = value

    def eval(self, environment):
        return self.value

    def __repr__(self):
        return "INT:" + str(self.value)


class FunctionCallNode:
    def __init__(self, identifier, configurations, parameters):
        self.identifier = identifier
        self.configurations = configurations
        self.parameters = parameters
        self.type = FUNCTION_CALL_NODE

        self.functions = {
            "print": handle_print,
            "input": handle_input,
            "intInput": handle_int_input,
            "random": handle_random,
            "join": handle_join,
        }

    def __repr__(self):
        return (
            self.identifier
            + "["
            + ",".join(str(exp) for exp in self.configurations)
            + "]"
            + "{"
            + ",".join(str(exp) for exp in self.parameters)
            + "}"
        )

    def eval(self, environment):
        if self.identifier in self.functions:
            return self.functions[self.identifier](self, environment)
