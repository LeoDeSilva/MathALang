from os import replace
import random
import math
from numpy import integer
from numpy.core.fromnumeric import var
import periodictable
from sympy import sympify, solve, Symbol, Integer
from Lexer.tokens import *
import Evaluator.nodes as nodes

elements = periodictable.core.default_table()
periodictable.core.define_elements(elements, globals())


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
    print(*nodes.eval(nodes.ArrayNode(node.parameters), environment))


def handle_input(node, environment):
    return nodes.StringNode(input(params_to_string(node.parameters, environment)))


def handle_int_input(node, environment):
    return nodes.assign_node(
        float(input(params_to_string(node.parameters, environment)))
    )


def handle_random(node, environment):
    if len(node.parameters) < 1:
        if len(node.configurations) >= 1:
            n = nodes.eval(node.configurations[0], environment)
            return nodes.ArrayNode(
                [nodes.assign_node(random.random()) for _ in range(n)]
            )
        return nodes.assign_node(random.random())

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


def handle_index(node, environment):
    index = 0
    if len(node.parameters) < 1:
        return nodes.ErrorNode("INDEX takes at least 1 parameter")

    if len(node.parameters) > 1:
        index = nodes.eval(node.parameters[1], environment)

    if len(node.configurations) > 0:
        index = nodes.eval(node.configurations[0], environment)

    return nodes.eval(node.parameters[0], environment)[index]


# =============== Math ==============


def handle_sqrt(node, environment):
    root = 2
    if len(node.configurations) > 0:
        root = nodes.eval(node.configurations[0], environment)
    return nodes.assign_node(nodes.eval(node.parameters[0], environment) ** (1 / root))


def handle_sum(node, environment):
    array = nodes.ArrayNode(
        nodes.eval(flatten_list(node.parameters, environment), environment)
    )
    return nodes.IntNode(sum(nodes.eval(array, environment)))


def handle_frac(node, environment):
    if len(node.parameters) < 2:
        return nodes.ErrorNode("FRAC takes at least 2 parameters")

    op_node = nodes.BinOpNode(node.parameters[0], "DIV", node.parameters[1])
    return nodes.assign_node(nodes.eval(op_node, environment))


def handle_quadratic(node, environment):
    if len(node.parameters) < 3:
        return nodes.ErrorNode("QUADRATIC takes at least 3 parameters")
    calculation = params_to_string(node.configurations, environment)

    a = nodes.eval(node.parameters[0], environment)
    b = nodes.eval(node.parameters[1], environment)
    c = nodes.eval(node.parameters[2], environment)

    positive = nodes.assign_node((-b + math.sqrt(b ** 2 - (4 * a * c))) / (2 * a))
    negative = nodes.assign_node((-b - math.sqrt(b ** 2 - (4 * a * c))) / (2 * a))

    if calculation.lower() in ("positive", "add", "+"):
        return positive
    if calculation.lower() in ("negative", "sub", "neg", "-"):
        return negative
    else:
        return nodes.ArrayNode([positive, negative])


def handle_percentage(node, environment):
    if len(node.parameters) < 1:
        return nodes.ErrorNode("PERCENTAGE takes at least 1 parameter")

    denomenator = 100
    if len(node.parameters) > 1:
        denomenator = nodes.eval(node.parameters[1], environment)

    return nodes.assign_node(
        (nodes.eval(node.parameters[0], environment) / denomenator) * 100
    )


def handle_average(node, environment):
    if len(node.parameters) < 1:
        return nodes.ErrorNode("AVERAGE takes at least 1 parameter")

    params = flatten_list(node.parameters, environment)
    return nodes.assign_node(sum(params) / len(params))


def handle_solve(node, environment):
    if len(node.parameters) < 1:
        return nodes.ErrorNode("AVERAGE takes at least 1 parameter")

    eq = params_to_string(node.parameters, environment)
    sympy_eq = sympify("Eq(" + eq.replace("=", ",").replace("^", "**") + ")")

    if len(node.configurations) > 0:
        solved = [
            solve(
                sympy_eq,
                Symbol(params_to_string(node.configurations, environment)),
                list=True,
            )
        ]

    else:
        solved = [solve(sympy_eq, sym, list=True) for sym in sympy_eq.free_symbols]

    solutions = []
    for i, variable in enumerate(solved):
        solutions.append([])
        for solution in variable:
            if isinstance(solution, list):
                for sol in solution:
                    try:
                        solutions[i].append(
                            nodes.assign_node(
                                eval(str(sol).replace("sqrt", "math.sqrt"))
                            )
                        )
                    except:
                        solutions[i].append(
                            nodes.assign_node(str(sol).replace("sqrt", "math.sqrt"))
                        )

            else:
                try:
                    solutions[i].append(
                        nodes.assign_node(
                            eval(str(solution).replace("sqrt", "math.sqrt"))
                        )
                    )
                except:
                    solutions[i].append(
                        nodes.assign_node(str(solution).replace("sqrt", "math.sqrt"))
                    )

    if len(solutions) == 1:
        solutions = solutions[0]
    if len(solutions) == 1:
        solutions = solutions[0]

    return nodes.assign_node(solutions)


# =============== Chemistry ==============


def handle_mass(node, environment):
    if len(node.parameters) < 1:
        return nodes.ErrorNode("MASS takes at least 1 parameter")

    element = globals()[params_to_string(node.parameters, environment)]
    return nodes.assign_node(element.mass)


# =============== Quality Of Life ==============


def params_to_string(params, environment):
    return " ".join(
        str(nodes.eval(param, environment))
        for param in flatten_list(params, environment)
    )


def flatten_list(array, environment):
    if isinstance(array, list):
        flattened_array = []
        for item in array:
            flattened_array += flatten_list(item, environment)
        return flattened_array

    elif isinstance(array, (int, str, float)):
        return [array]

    else:
        return flatten_list(nodes.eval(array, environment), environment)


# =============== Function Dictionary ===============

functions = {
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
    "average": handle_average,
    "avg": handle_average,
    "mass": handle_mass,
    "solve": handle_solve,
    "index": handle_index,
}
