import sys
from Lexer.lexer import *
from Parser.parser import *


class Environment:
    def __init__(self, options):
        self.variables = {}
        self.functions = {}
        self.options = options


def interpret_line(line, environment, display):
    if len(line) < 1:
        return

    l = Lexer(line.strip())
    tokens = l.lex()

    p = Parser(tokens)
    ast = p.parse()

    ast.eval(environment, display)


def read_file(filename):
    environment = Environment({"prediction": True})
    with open(filename, "r") as f:
        interpret_line(f.read().replace("\n", ""), environment, False)


def start_repl():
    environment = Environment({"prediction": True})
    while True:
        try:
            line = input(">>")

        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            break

        if line in ("quit", "break", "exit"):
            break

        interpret_line(line, environment, True)
        print()


def main():
    if len(sys.argv) > 1:
        read_file(sys.argv[1])
    else:
        start_repl()


if __name__ == "__main__":
    main()
