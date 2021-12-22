from os import environ
from Lexer.tokens import *
from Parser.functions import *
from difflib import SequenceMatcher

# =============== Generic Nodes ================


class ProgramNode:
    def __init__(self, expressions):
        self.type = PROGRAM_NODE
        self.expressions = expressions

    def eval(self, environment, display=False):
        for expr in self.expressions:
            result = eval(expr, environment)

            if isinstance(result, ErrorNode):
                return eval(result, environment)

            if display:
                evalled = eval(result, environment)
                if evalled is not None:
                    print(evalled)

    def __repr__(self):
        return "PROGRAM_NODE:" + ",".join(str(exp) for exp in self.expressions)


class VarAssignNode:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
        self.type = VAR_ASSIGN_NODE

    def eval(self, environment):
        result = eval(self.expression, environment)
        environment.variables[self.identifier] = result
        # return result

    def __repr__(self):
        return (
            "VAR_ASSIGN:"
            + self.identifier.__repr__()
            + "="
            + self.expression.__repr__()
        )


class BinOpNode:
    def __init__(self, left, op, right):
        self.type = BIN_OP_NODE
        self.left = left
        self.op = op
        self.right = right

    def eval(self, environment):  # sourcery no-metrics
        left = eval(self.left, environment)
        right = eval(self.right, environment)

        if isinstance(left, ErrorNode):
            return left
        elif isinstance(right, ErrorNode):
            return right
        try:
            if self.op == ADD:
                return IntNode(format_result(left + right))
            elif self.op == SUB:
                return IntNode(format_result(left - right))
            elif self.op == DIV:
                return IntNode(format_result(left / right))
            elif self.op == MUL:
                return IntNode(format_result(left * right))
            elif self.op == MOD:
                return IntNode(format_result(left % right))
            elif self.op == POW:
                return IntNode(format_result(left ** right))

            elif self.op == EE:
                return IntNode(1 if left == right else 0)
            elif self.op == NE:
                return IntNode(1 if left != right else 0)
            elif self.op == GT:
                return IntNode(1 if left > right else 0)
            elif self.op == GTE:
                return IntNode(1 if left >= right else 0)
            elif self.op == LT:
                return IntNode(1 if left < right else 0)
            elif self.op == LTE:
                return IntNode(1 if left <= right else 0)

        except TypeError:
            return ErrorNode(
                "Binary Operation Error: "
                + str(left)
                + ":"
                + self.op
                + ":"
                + str(right)
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
        right = eval(self.right, environment)
        if isinstance(right, ErrorNode):
            return right
        if self.op == SUB:
            return IntNode(-(right))
        elif self.op == NOT:
            return IntNode(1 if right == 0 else 0)

    def __repr__(self):
        return self.op + "(" + self.right.__repr__() + ")"


# =============== Atom Nodes ==============


class VarAccessNode:
    def __init__(self, identifier):
        self.type = VAR_ACCESS_NODE
        self.identifier = identifier

    def eval(self, environment):
        if (
            self.identifier in environment.variables
            or environment.options["prediction"] != True
        ):
            return environment.variables[self.identifier]

        predicted_identifier = {
            "identifier": list(environment.variables)[0],
            "certainty": 0,
        }

        for identifier in list(environment.variables):
            certainty = SequenceMatcher(None, self.identifier, identifier).ratio()

            if certainty > predicted_identifier["certainty"]:
                predicted_identifier = {
                    "identifier": identifier,
                    "certainty": certainty,
                }

        return environment.variables[predicted_identifier["identifier"]]

    def __repr__(self):
        return "VAR_ACCESS:" + self.identifier


class ArrayNode:
    def __init__(self, nodes):
        self.type = ARRAY_NODE
        self.nodes = nodes

    def eval(self, environment):
        return [eval(node, environment) for node in self.nodes]

    def __repr__(self):
        return "ARRAY NODE:" + "[" + ",".join(str(exp) for exp in self.nodes) + "]"


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


class ErrorNode:
    def __init__(self, message):
        self.message = message
        self.type = ERROR

    def eval(self, environment):
        if self.message != "":
            print(self.message)
        return None

    def __repr__(self):
        return "ERROR:" + self.message


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
            "intput": handle_int_input,
            "random": handle_random,
            "join": handle_join,
            "frac": handle_frac,
            "sqrt": handle_sqrt,
            "root": handle_sqrt,
            "sum": handle_sum,
            "len": handle_len,
            "str": handle_str,
            "int": handle_int,
            "quadratic": handle_quadratic,
            "quad": handle_quadratic,
            "percentage": handle_percentage,
            "perc": handle_percentage,
            "average":handle_average,
            "avg":handle_average,
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
            # TODO CUSTOM DEFENITIONS
        else:
            return ErrorNode("Function Not Defined")


# =============== Quality Of Life ==============


def eval(node, environment):
    if not isinstance(node, (int, str, float, list)) and node != None:
        return eval(node.eval(environment), environment)

    elif isinstance(node, ErrorNode):
        return node.eval(environment)

    return node


def assign_node(node):
    if isinstance(node, (int, float)):
        return IntNode(format_result(node))
    elif isinstance(node, str):
        return StringNode(node)
    elif isinstance(node, list):
        return ArrayNode(node)


def format_result(result):
    if not isinstance(result, (int, float)):
        return result

    if int(result) == result:
        return int(result)
    else:
        # Possibly give option for d.p
        return round(result, 3)
