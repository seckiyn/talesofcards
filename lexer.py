from enum import Enum, auto
from dataclasses import dataclass
from typing import Union, Tuple
from lprint import print_debug, print_error, red, blue, yellow

class TokenType(Enum):
    WORD = auto()
    NEW = auto()
    INTEGER = auto()
    DOT = auto()

    OPEN_CBRACKET = auto()
    CLOSE_CBRACKET = auto()

    COLON = auto()
    SEP = auto()
    STR = auto()


    EOF = auto()

    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()

    LPAREN = auto()
    RPAREN = auto()

    MACRO = auto()
    ASSIGNMACRO = auto()

    SETVARIABLE = auto()
    ASSIGN = auto()

    LT = auto()
    EQ = auto()
    GT = auto()
    LTEQ = auto()
    GTEQ = auto()

    DEFINEFUNCTION = auto()
    CALLFUNCTION = auto()

    EXPRESSION = auto()




@dataclass
class Token:
    """
        Container for token
    """
    token_type: TokenType
    token_value: Union[int, str, None]
    row: int
    column: int

KEYWORDS = {
        "new": TokenType.NEW,
        "var": TokenType.SETVARIABLE,
        "func": TokenType.DEFINEFUNCTION,
        "macro": TokenType.ASSIGNMACRO,
        "exp": TokenType.EXPRESSION
        }
IGNORE_CHARACTERS = " \n"
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pointer = -1
        self.current_char = None
        self.row = 1
        self.column = 1
        self.advance()
    def advance(self):
        self.pointer += 1
        if len(self.text) > self.pointer:
            self.current_char = self.text[self.pointer]
            if self.current_char == "\n":
                self.row = 1
                self.column += 1
            else:
                self.row += 1
        else:
            self.current_char = None
    def peek(self):
        pointer = self.pointer + 1
        if len(self.text) > pointer:
            return self.text[pointer]
        else:
            return None
    def get_word(self):
        string = ""
        while len(self.text) > self.pointer and (self.current_char.isalnum() or self.current_char=="_"):
            string += self.current_char
            self.advance()

        tokentype = KEYWORDS.get(string, TokenType.WORD)
        return Token(tokentype, string, *(self.row, self.column))

    def get_integer(self):
        integer = ""
        while len(self.text) > self.pointer and self.current_char.isdigit():
            integer += self.current_char
            self.advance()
        return Token(TokenType.INTEGER, integer, *(self.row, self.column))
    def get_string(self):
        string = ""
        self.advance()
        while len(self.text) > self.pointer and self.current_char != '"':
            string += self.current_char
            self.advance()
        self.advance()
        return string
    def get_math_token(self):
        if self.current_char == "+":
            token = Token(TokenType.PLUS, self.current_char, *(self.row, self.column))
            self.advance()
            return token
        if self.current_char == "-":
            token = Token(TokenType.MINUS, self.current_char, *(self.row, self.column))
            self.advance()
            return token
        if self.current_char == "*":
            token = Token(TokenType.MUL, self.current_char, *(self.row, self.column))
            self.advance()
            return token
        if self.current_char == "/":
            token = Token(TokenType.DIV, self.current_char, *(self.row, self.column))
            self.advance()
            return token

    def get_assign_token(self):
        if self.current_char == "=" and self.peek() == "=":
            token = Token(TokenType.EQ,
                          self.current_char,
                          self.row,
                          self.column)
            return token
        if self.current_char == "=":
            token = Token(TokenType.ASSIGN,
                          self.current_char,
                          self.row,
                          self.column)
            return token
        if self.current_char == "!":
            token = Token(TokenType.MACRO,
                          self.current_char,
                          self.row,
                          self.column)
            return token
    def get_comparison_token(self):
        if self.current_char == "<" and self.peek() == "=":
            token = Token(TokenType.LTEQ,
                          self.current_char,
                          self.row,
                          self.column)
            self.advance()
            return token
        if self.current_char == ">" and self.peek() == "=":
            token = Token(TokenType.GTEQ,
                          self.current_char,
                          self.row,
                          self.column)
            self.advance()
            return token
        if self.current_char == "<":
            token = Token(TokenType.LT,
                          self.current_char,
                          self.row,
                          self.column)
            return token
        if self.current_char == ">":
            token = Token(TokenType.GT,
                          self.current_char,
                          self.row,
                          self.column)
            return token


    def get_next_token(self):
        while self.current_char != None:
            # print(self.current_char)
            if self.current_char in IGNORE_CHARACTERS:
                self.advance()
                continue
            if self.current_char.isalpha():
                return self.get_word()
            if self.current_char == "{":
                token = Token(TokenType.OPEN_CBRACKET, self.current_char, *(self.row, self.column))
                self.advance()
                return token
            if self.current_char == "}":
                token = Token(TokenType.CLOSE_CBRACKET, self.current_char, *(self.row, self.column))
                self.advance()
                return token
            if self.current_char == ":":
                token = Token(TokenType.COLON, self.current_char, *(self.row, self.column))
                self.advance()
                return token
            if self.current_char == '"':
                string = self.get_string()
                token = Token(TokenType.STR, string, *(self.row, self.column))
                return token
            if self.current_char == ",":
                token = Token(TokenType.SEP, self.current_char, *(self.row, self.column))
                self.advance()
                return token
            if self.current_char.isdigit():
                token = self.get_integer()
                return token
            if self.current_char == ".":
                token = Token(TokenType.DOT, self.current_char, *(self.row, self.column))
                self.advance()
                return token
            if self.current_char == "(":
                token = Token(TokenType.LPAREN, self.current_char, *(self.row, self.column))
                self.advance()
                return token
            if self.current_char == ")":
                token = Token(TokenType.RPAREN, self.current_char, *(self.row, self.column))
                self.advance()
                return token
            if self.current_char in "+-/*":
                token = self.get_math_token()
                return token
            if self.current_char == "<" and self.peek() == "<":
                self.comment()
                continue
            if self.current_char in "=!":
                token = self.get_assign_token()
                self.advance()
                return token
            if self.current_char in "<>":
                token = self.get_comparison_token()
                self.advance()
                return token

            ex = f"You shouldn't be here: {red(f'{self.current_char}')}"
            raise Exception(ex)
        return Token(TokenType.EOF, None, *(self.row, self.column))
    def comment(self):
        while not(self.current_char == ">" and self.peek() == ">"):
            self.advance()
        self.advance() # past >
        self.advance() # past other >



