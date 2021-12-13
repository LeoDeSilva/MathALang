import random


def params_to_string(node, environment):
    string = ""
    for param in node.parameters:
        string += str(param.eval(environment))
    return string


def handle_print(node, environment):
    string = params_to_string(node, environment)
    print(string)
    return string


def handle_input(node, environment):
    string = params_to_string(node, environment)
    return input(string)


def handle_int_input(node, environment):
    string = params_to_string(node, environment)
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
        return [random.randint(min_value, max_value) for _ in range(n)]
    else:
        return random.randint(min_value, max_value)
