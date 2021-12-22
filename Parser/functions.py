from os import environ
import random
import math
from Lexer.tokens import *
import Parser.nodes as nodes


# =============== Miscellaneous ==============
def handle_int(node, environment):
    if len(node.parameters) < 1:
        return nodes.ErrorNode("INT takes at least 1 parameter")
    return nodes.IntNode(int(nodes.eval(node.parameters[0], environment)))


def handle_str(node, environment):
    return nodes.StringNode(params_to_string(node.parameters, environment))


def handle_len(node, environment):
    return nodes.IntNode(len(params_to_string(node.parameters, environment)))


def handle_print(node, environment):
    print(params_to_string(node.parameters, environment))


def handle_input(node, environment):
    return nodes.StringNode(input(params_to_string(node.parameters, environment)))


def handle_int_input(node, environment):
    return nodes.IntNode(
        nodes.format_result(
            float(input(params_to_string(node.parameters, environment)))
        )
    )


def handle_random(node, environment):
    if len(node.parameters) < 1:
        if len(node.configurations) >= 1:
            n = nodes.eval(node.configurations[0], environment)
            return nodes.ArrayNode(
                [nodes.IntNode(nodes.format_result(random.random())) for _ in range(n)]
            )
        return nodes.IntNode(nodes.format_result(random.random()))

    if len(node.parameters) > 1:
        min_value = nodes.eval(node.parameters[0], environment)
        max_value = nodes.eval(node.parameters[1], environment)
    else:
        max_value = nodes.eval(node.parameters[0], environment)
        min_value = 0

    if len(node.configurations) >= 1:
        n = nodes.eval(node.configurations[0], environment)
        return nodes.ArrayNode(
            [nodes.IntNode(random.randint(min_value, max_value)) for _ in range(n)]
        )
    else:
        return nodes.IntNode(random.randint(min_value, max_value))


def handle_join(node, environment):
    if len(node.configurations) < 1:
        string = ","
    else:
        string = params_to_string(node.configurations, environment)

    return nodes.StringNode(
        string.join(
            [
                str(nodes.eval(param, environment))
                for param in flatten_list(node.parameters, environment)
            ]
        )
    )


# =============== Math ==============


def handle_sqrt(node, environment):
    root = 2
    if len(node.configurations) > 0:
        root = nodes.eval(node.configurations[0], environment)
    return nodes.IntNode(
        nodes.format_result(nodes.eval(node.parameters[0], environment) ** (1 / root))
    )


def handle_sum(node, environment):
    array = nodes.ArrayNode(
        nodes.eval(flatten_list(node.parameters, environment), environment)
    )
    return nodes.IntNode(nodes.format_result(sum(nodes.eval(array, environment))))


def handle_frac(node, environment):
    if len(node.parameters) < 2:
        return nodes.ErrorNode("FRAC takes at least 2 parameters")

    op_node = nodes.BinOpNode(node.parameters[0], "DIV", node.parameters[1])
    return nodes.IntNode(nodes.eval(op_node, environment))


def handle_quadratic(node, environment):
    if len(node.parameters) < 3:
        return nodes.ErrorNode("QUADRATIC takes at least 3 parameters")
    calculation = params_to_string(node.configurations, environment)

    a = nodes.eval(node.parameters[0], environment)
    b = nodes.eval(node.parameters[1], environment)
    c = nodes.eval(node.parameters[2], environment)

    positive = nodes.IntNode(
        nodes.format_result(-b + math.sqrt(b ** 2 - (4 * a * c))) / (2 * a)
    )
    negative = nodes.IntNode(
        nodes.format_result(-b - math.sqrt(b ** 2 - (4 * a * c))) / (2 * a)
    )

    if calculation.lower() in ("positive", "add", "+"):
        return positive
    if calculation.lower() in ("negative", "sub", "neg", "-"):
        return negative
    else:
        return nodes.ArrayNode([positive, negative])


# =============== Quality Of Life ==============


def params_to_string(params, environment):
    return "".join(
        str(nodes.eval(param, environment))
        for param in flatten_list(params, environment)
    )


def flatten_list(array, environment):
    if isinstance(array, list):
        flattened_array = []
        for item in array:
            flattened_array += flatten_list(item, environment)
        return flattened_array

    elif isinstance(array, (int, str, float)) or array.type in (INT_NODE, STRING_NODE):
        return [array]

    elif array.type == ARRAY_NODE:
        return flatten_list(array.nodes, environment)

    elif array.type == FUNCTION_CALL_NODE:
        return flatten_list(nodes.eval(array, environment), environment)

    if array.type == ARRAY_NODE:
        return flatten_list(array.nodes, environment)

    elif array.type == VAR_ACCESS_NODE:
        return flatten_list(
            flatten_list(environment.variables[array.identifier], environment),
            environment,
        )
