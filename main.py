import sys
from Lexer.lexer import *
from Parser.parser import *


class Environment:
    def __init__(self):
        self.variables = {}
        self.functions = {}


def print_tokens(tokens):
    for tok in tokens:
        print(tok)


def interpret_line(line, environment, display):
    if len(line) < 1:
        return

    l = Lexer(line.strip())
    tokens = l.lex()

    p = Parser(tokens)
    ast = p.parse()
    print(ast)

    ast.eval(environment, display)


def read_file(filename):
    environment = Environment()
    with open(filename, "r") as f:
        interpret_line(f.read().replace("\n", ""), environment, False)


def start_repl():
    environment = Environment()
    while True:
        line = input(">>")
        interpret_line(line, environment, True)


def main():
    if len(sys.argv) > 1:
        read_file(sys.argv[1])
    else:
        start_repl()


if __name__ == "__main__":
    main()
