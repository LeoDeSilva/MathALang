from lexer.tokens import *
from parse.parser_nodes import *

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

    def peek_char(self):
        try:
            return self.tokens[self.token]
        except IndexError:
            return ""


    def parse(self):
        ast = ProgramNode([])
        while self.next != -1:
            print(self.token)
            self.advance()