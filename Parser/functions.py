import random
from Lexer.tokens import *
import Parser.nodes as nodes


def params_to_string(params, environment):
    string = ""
    for param in params:
        string += str(param.eval(environment))
    return string


def handle_print(node, environment):
    string = params_to_string(node.parameters, environment)
    print(string)
    return string


def handle_input(node, environment):
    string = params_to_string(node.parameters, environment)
    return input(string)


def handle_int_input(node, environment):
    string = params_to_string(node.parameters, environment)
    return int(input(string))


def handle_random(node, environment):
    if len(node.configurations) > 1:
        min_value = node.configurations[0].eval(environment)
        max_value = node.configurations[1].eval(environment)
    else:
        max_value = node.configurations[0].eval(environment)
        min_value = 0

    if len(node.parameters) >= 1:
        n = node.parameters[0].eval(environment)
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

    array = flatten_list(node.parameters, environment)

    joined = string.join([str(param.eval(environment)) for param in array])
    return joined


def flatten_list(array, environment):
    if isinstance(array, list):
        flattened_array = []

        for item in array:
            if item.type == ARRAY_NODE:
                flattened_array += flatten_list(item.nodes, environment)
            elif item.type == FUNCTION_CALL_NODE:
                flattened_array += flatten_list(item.eval(environment), environment)
            else:
                flattened_array += flatten_list(item, environment)

        return flattened_array

    if array.type in (INT_NODE, STRING_NODE):
        return [array]
    elif array.type == ARRAY_NODE:
        return flatten_list(array.nodes, environment)
    elif array.type == VAR_ACCESS_NODE:
        return flatten_list(
            flatten_list(environment.variables[array.identifier], environment),
            environment,
        )

    return flattened_array
