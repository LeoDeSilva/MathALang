import sys
from lexer.lexer import *

def print_tokens(tokens):
    for tok in tokens:
        print(tok)

def interpret_line(line):
    if len(line) < 1: return

    l = Lexer(line)
    tokens = l.lex()
    print(tokens)


def read_file(filename):
    with open(filename, "r") as f:
        interpret_line(f.read().replace("\n",""))


def start_repl():
    while True: 
        line = input(">>")
        interpret_line(line)


def main():
    if len(sys.argv) > 1:
        read_file(sys.argv[1])
    else:
        start_repl()

if __name__ == "__main__":
    main()