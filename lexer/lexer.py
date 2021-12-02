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


    def eat_whitespace(self):
        while self.char.isspace():
            self.advance()
    
        
    def lex_char(self):
        self.eat_whitespace()

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

        elif self.char == ";":
            return Token(SEMICOLON,self.char)
        elif self.char == ":":
            return Token(COLON,self.char)
        elif self.char == "\\":
            return Token(BACKSLASH,self.char)
        elif self.char == ".":
            return Token(DOT,self.char)
        elif self.char == ",":
            return Token(COMMA,self.char)

        elif self.char == "(":
            return Token(LPAREN,self.char)
        elif self.char == ")":
            return Token(RPAREN,self.char)
        elif self.char == "[":
            return Token(LSQUARE,self.char)
        elif self.char == "]":
            return Token(RSQUARE,self.char)
        elif self.char == "{":
            return Token(LBRACE,self.char)
        elif self.char == "}":
            return Token(RBRACE,self.char)
        
        elif self.char == '"':
            return Token(STRING,self.lex_string())

        elif self.char.isnumeric():
            return Token(INT,self.lex_numeric())

        elif self.char in LETTERS:
            return Token(IDENTIFIER,self.lex_identifier())

    
    def lex_string(self):
        self.advance()

        start_pos = self.position 
        while self.char != '"':
            self.advance()

        return self.file[start_pos:self.position]


    def lex_identifier(self):
        start_pos = self.position
        while self.next != -1 and self.char in LETTERS:
            self.advance()

        return self.retreat_and_return(start_pos)
    
    
    def lex_numeric(self):
        start_pos = self.position
        while self.next != -1 and self.char.isnumeric():
            self.advance()

        return self.retreat_and_return(start_pos)

    def retreat_and_return(self, start_pos):
        value = self.file[start_pos:self.position]
        self.retreat()
        return value
