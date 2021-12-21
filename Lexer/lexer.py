from Lexer.tokens import *


class Lexer:
    def __init__(self, file):
        self.file = file
        self.char = file[0]
        self.position = 0
        self.next = 1

    def advance(self):
        self.position = self.next
        if len(self.file) > self.next and self.next != -1:
            self.next += 1
            self.char = self.file[self.position]
        else:
            self.next = -1

    def retreat(self):
        self.next -= 1
        self.position -= 2
        self.char = self.file[self.position]

    def peek_char(self):
        try:
            return self.file[self.next]
        except IndexError:
            return ""

    def lex(self):
        tokens = []
        while self.next != -1:
            token = self.lex_char()
            tokens.append(token)
            try:
                self.advance()
            except IndexError:
                break

        return tokens + [Token(EOF, "")]

    def eat_whitespace(self):
        while self.char.isspace():
            self.advance()

    def lex_char(self):
        self.eat_whitespace()

        if self.char == "+":
            return Token(ADD, self.char)
        elif self.char == "-":
            return Token(SUB, self.char)
        elif self.char == "*":
            return Token(MUL, self.char)
        elif self.char == "/":
            return Token(DIV, self.char)
        elif self.char == "%":
            return Token(MOD, self.char)
        elif self.char == "^":
            return Token(POW, self.char)

        elif self.char == ";":
            return Token(SEMICOLON, self.char)
        elif self.char == ":":
            return Token(COLON, self.char)
        elif self.char == "\\":
            return Token(BACKSLASH, self.char)
        elif self.char == ".":
            return Token(DOT, self.char)
        elif self.char == ",":
            return Token(COMMA, self.char)

        elif self.char == "=":
            return self.lex_double(EQ, "=", EE)
        elif self.char == "!":
            return self.lex_double(NOT, "=", NE)
        elif self.char == ">":
            return self.lex_double(GT, "=", GTE)
        elif self.char == "<":
            return self.lex_double(LT, "=", LTE)

        elif self.char == "(":
            return Token(LPAREN, self.char)
        elif self.char == ")":
            return Token(RPAREN, self.char)
        elif self.char == "[":
            return Token(LSQUARE, self.char)
        elif self.char == "]":
            return Token(RSQUARE, self.char)
        elif self.char == "{":
            return Token(LBRACE, self.char)
        elif self.char == "}":
            return Token(RBRACE, self.char)

        elif self.char == '"':
            return Token(STRING, self.lex_string())

        elif self.char.isnumeric():
            return Token(INT, self.lex_numeric())

        elif self.char in LETTERS:
            identifier = self.lex_identifier()
            return Token(lookup_identifier(identifier), identifier)

    def lex_double(self, first_type, next_char, next_type):
        char = self.char
        if self.peek_char() == next_char:
            self.advance()
            return Token(next_type, char + self.char)
        return Token(first_type, char)

    def lex_string(self):
        self.advance()

        start_pos = self.position
        while self.char != '"':
            self.advance()

        return self.file[start_pos : self.position]

    def lex_identifier(self):
        return self.extract_string(LETTERS)

    def lex_numeric(self):
        return self.extract_string("1234567890.")

    def extract_string(self, chars):
        start_pos = self.position
        while self.next != -1 and self.char in chars:
            self.advance()
        return self.retreat_and_return(start_pos)

    def retreat_and_return(self, start_pos):
        value = self.file[start_pos : self.position]
        self.retreat()
        return value
