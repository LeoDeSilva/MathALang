from lexer.tokens import *

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
        
        
    def lex(self):
        tokens = []
        while self.next != -1:
            token = self.lex_char()
            tokens.append(token)
            self.advance()
        return tokens
    
        
    def lex_char(self):
        if self.char == "+":
            return Token(ADD,self.char)
        elif self.char == "-":
            return Token(SUB,self.char)
        elif self.char == "*":
            return Token(MUL,self.char)
        elif self.char == "/":
            return Token(DIV,self.char)
        elif self.char == "%":
            return Token(MOD,self.char)
        elif self.char == "^":
            return Token(POW,self.char)
        elif self.char.isnumeric():
            return Token(INT,self.lex_numeric())
    
    def lex_numeric(self):
        start_pos = self.position
        while self.next != -1 and self.char.isnumeric():
            self.advance()

        int = self.file[start_pos:self.position]
        self.retreat()
        return int
