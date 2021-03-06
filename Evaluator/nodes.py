from os import environ
from numpy import array

from numpy.lib.arraysetops import isin
from Lexer.tokens import *
from Evaluator.functions import *
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
        if isinstance(self.identifier, str):
            result = eval(self.expression, environment)
            environment.variables[self.identifier] = result
        elif isinstance(self.identifier, IndexNode):
            if isinstance(self.identifier.array, VarAccessNode):
                identifier = self.identifier.array.predict_identifier(environment)
                # environment.variables[identifier] = eval(self.identifier, environment)
                indexes = eval(self.identifier.indexes, environment)
                replaced = self.replace_element(
                    array=eval(self.identifier.array, environment),
                    index=0,
                    indexes=[0] + [eval(i, environment) for i in indexes],
                    value=assign_node(eval(self.expression, environment)),
                )

                environment.variables[identifier] = assign_node(replaced)

    def replace_element(self, array, index, indexes, value):
        if len(indexes) == 1 and index == indexes[0]:
            return value
        elif index == indexes[0]:
            if isinstance(array, list):
                return [
                    self.replace_element(element, i, indexes[1:], value)
                    for i, element in enumerate(array)
                ]
            else:
                return self.replace_element(array, 0, indexes[1:], value)
        else:
            return array

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
                return assign_node(left + right)
            elif self.op == SUB:
                return assign_node(left - right)
            elif self.op == DIV:
                return assign_node(left / right)
            elif self.op == MUL:
                return assign_node(left * right)
            elif self.op == MOD:
                return assign_node(left % right)
            elif self.op == POW:
                return assign_node(left ** right)

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


class IndexNode:
    def __init__(self, array, indexes):
        self.type = INDEX_NODE
        self.array = array
        self.indexes = indexes

    def eval(self, environment):
        array = eval(self.array, environment)
        for index in eval(self.indexes, environment):
            array = array[eval(index, environment)]
        return assign_node(array)

    def __repr__(self):
        return (
            "INDEX_NODE:" + self.array.__repr__() + "[" + self.indexes.__repr__() + "]"
        )


# =============== Atom Nodes ==============


class VarAccessNode:
    def __init__(self, identifier):
        self.type = VAR_ACCESS_NODE
        self.identifier = identifier

    def predict_identifier(self, environment):
        predicted_identifier = {
            "identifier": list(environment.variables)[0],
            "certainty": 0,
        }

        for identifier in list(environment.variables):
            certainty = similarity(self.identifier, identifier)

            if certainty > predicted_identifier["certainty"]:
                predicted_identifier = {
                    "identifier": identifier,
                    "certainty": certainty,
                }
        return predicted_identifier["identifier"]

    def eval(self, environment):
        if (
            self.identifier in environment.variables
            or environment.options["prediction"] != True
        ):
            return environment.variables[self.identifier]

        return environment.variables[self.predict_identifier(environment)]

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
        self.functions = functions

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
        return ArrayNode([assign_node(e) for e in node])
    else:
        return node


def format_result(result):
    if not isinstance(result, (int, float)):
        return result

    if int(result) == result:
        return int(result)
    else:
        # Possibly give option for d.p
        return round(result, 3)


def similarity(a, b):
    sequenceMatcherCertainty = SequenceMatcher(None, a, b).ratio()

    i = 0
    while i < len(a) and i < len(b):
        if a[i] != b[i]:
            break
        i += 1

    consecutiveCertainty = i / len(a)

    return (consecutiveCertainty * 0.4) + (sequenceMatcherCertainty * 0.6)
