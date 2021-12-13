import time
from Lexer.tokens import *
from Parser.nodes import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token = tokens[0]
        self.position = 0
        self.next = 1

    def advance(self):
        self.position = self.next
        if len(self.tokens) > self.next and self.next != -1:
            self.next += 1
            self.token = self.tokens[self.position]
        else:
            self.next = -1

    def retreat(self):
        self.next -= 1
        self.position -= 2
        self.token = self.tokens[self.position]

    def peek_token(self):
        try:
            return self.tokens[self.next]
        except IndexError:
            return Token(EOF, "")

    def parse(self):
        ast = ProgramNode([])
        while self.next != -1:
            if self.token.type == EOF:
                break
            expr = self.parse_expression()
            ast.expressions.append(expr)
            self.advance()
        return ast

    def parse_expression(self):
        if self.token.type == LET:
            self.advance()
            return self.parse_assignment()
        elif self.token.type == IDENTIFIER:
            if self.peek_token().type == EQ:
                return self.parse_assignment()
        node = self.parse_comparison()
        return node

    def parse_assignment(self):
        identifier = self.token.literal
        self.advance()
        self.advance()
        expression = self.parse_comparison()
        return VarAssignNode(identifier, expression)

    def parse_comparison(self):
        left_node = self.parse_arith()
        if self.token.type not in (SEMICOLON, EOF):
            if self.token.type in (EE, NE, GT, GTE, LT, LTE):
                op = self.token.type
                self.advance()
                return BinOpNode(left_node, op, self.parse_comparison())
        return left_node

    def parse_arith(self):
        left_node = self.parse_term()
        if self.token.type not in (SEMICOLON, EOF):
            if self.token.type in (ADD, SUB):
                op = self.token.type
                self.advance()
                return BinOpNode(left_node, op, self.parse_arith())
        return left_node

    def parse_term(self):
        left_node = self.parse_atom()
        if self.token.type not in (SEMICOLON, EOF):
            if self.token.type in (MUL, DIV):
                op = self.token.type
                self.advance()
                return BinOpNode(left_node, op, self.parse_term())
        return left_node

    def parse_atom(self):
        left_node = self.parse_factor()
        if self.token.type not in (SEMICOLON, EOF):
            if self.token.type in (POW, MOD):
                op = self.token.type
                self.advance()
                return BinOpNode(left_node, op, self.parse_atom())
        return left_node

    def parse_factor(self):
        node = None
        if self.token.type == INT:
            node = IntNode(int(self.token.literal))

        elif self.token.type == STRING:
            node = StringNode(self.token.literal)

        elif self.token.type == IDENTIFIER:
            node = VarAccessNode(self.token.literal)

        elif self.token.type == LPAREN:
            self.advance()
            expr = self.parse_comparison()
            if self.token.type == RPAREN:
                node = expr
            else:
                print("Expected RPAREN")
                node = expr

        elif self.token.type == SUB:
            self.advance()
            return UnaryOpNode(SUB, self.parse_factor())

        elif self.token.type == NOT:
            self.advance()
            return UnaryOpNode(NOT, self.parse_factor())

        elif self.token.type in (BACKSLASH, DIV):
            self.advance()
            identifier = self.token.literal
            self.advance()

            configs = []
            params = []

            if self.token.type == LSQUARE:
                self.advance()
                configs = self.parse_parameters(RSQUARE)
                self.advance()

            if self.token.type == LBRACE:
                self.advance()
                params = self.parse_parameters(RBRACE)

            return FunctionCallNode(identifier, configs, params)

        elif self.token.type == LSQUARE:
            self.advance()
            nodes = self.parse_parameters(RSQUARE)
            self.advance()
            return ArrayNode(nodes)

        self.advance()
        return node

    def parse_parameters(self, terminate):
        parameters = []
        while self.token.type != terminate and self.token.type != EOF:
            if self.token.type == COMMA:
                continue
            expr = self.parse_comparison()
            parameters.append(expr)

            if self.token.type != terminate:
                self.advance()

        return parameters
