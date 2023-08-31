import sys
from enum import Enum, auto
from dataclasses import dataclass
from typing import Union, List
from lexer import Lexer, TokenType, Token
from lprint import print_debug, red, blue, yellow


TEST = """\
var mustafa = 12
new Card card_name {
    name: "doofenshmirtz",
    image: "card2.png"
}
<< This is a comment ya know >>
"""

TEST = """\
var mustafa = 12
var mustafa = mustafa + 1
        """

TEST = """\
var mustafa = 0
macro !addone{
    var mustafa = mustafa + 1
}
!addone
!addone
!addone
!addone
!addone
!addone
!addone
!addone
!addone
!addone
!addone
!addone
}
        """


# print_debug(TEST)

"""
PROGRAM: (NEW|SETVARIABLE|EXP)
    NEW CARD|new
        CARD: cardname open_brackets SETS close_brackets
        cardname:set
        SETS:
            [key:EXP] (SEP(,), key:EXP)*
    SETVARIABLE WORD EQ EXP
    EXP:
        [INT|STR|VARIABLE] ((MUL|DIV|PLUS|MIN) [INT|STR]) *

"""

NEW_TYPES = (
        "Card"
        )


AST_COUNT = 0
PROGRAM_COUNT = 0


AST_COUNT += 1
@dataclass
class AST:
    """ Main AST class """
    pass

AST_COUNT += 1
@dataclass
class BinOp(AST):
    left_token: Union[AST, TokenType]
    op_token: Union[AST, TokenType]
    right_token: Union[AST, TokenType]

AST_COUNT += 1
@dataclass
class UnaryOp(AST):
    op_token: Union[AST, TokenType]
    right_token: Union[AST, TokenType]

AST_COUNT += 1
@dataclass
class Integer(AST):
    """
        AST container for Integers
    """
    token: Union[AST, TokenType]

AST_COUNT += 1
@dataclass
class Void(AST):
    """
        AST for none
    """
    pass

AST_COUNT += 1
@dataclass
class Assign(AST):
    """
        AST variable for setting variables
    """
    token: Token
    expr: AST

AST_COUNT += 1
@dataclass
class Variable(AST):
    """
        AST for return variable
    """
    token: Token

AST_COUNT += 1
@dataclass
class Block(AST):
    """
        AST for blocks
    """
    ast_list: List[AST]

AST_COUNT += 1
@dataclass
class Program(AST):
    """
        AST class for whole program
    """
    ast_list: List[AST]

AST_COUNT += 1
@dataclass
class Name(AST):
    name: Union[AST, TokenType]
    eq: AST

AST_COUNT += 1
@dataclass
class NameBlock(AST):
    name_list: List[Name]


AST_COUNT += 1
@dataclass
class Card(AST):
    card_name: str
    name_block: Union[NameBlock, TokenType]

AST_COUNT += 1
@dataclass
class String(AST):
    token: Union[Token, AST]



class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = self.get_tokens()
        # print_debug(*self.tokens, sep="\n")
        self.current_token = None
        self.position = -1
        self.next_token()
        self.macros = dict()
    def get_tokens(self):
        token_list = list()
        token = self.lexer.get_next_token()
        # print_debug(blue(token))
        while token.token_value:
            token_list.append(token)
            token = self.lexer.get_next_token()
            # print_debug(blue(token))
        token_list.append(token)
        return token_list
            
    def next_token(self):
        """
            advances and sets the current_token
        """
        self.position += 1
        if self.position >= len(self.tokens):
            print_debug(f"Tokens of these makes the wrong {self.tokens}")

        self.current_token = self.tokens[self.position]
    def eat(self, token_type):
        # print_debug(blue("[Token]"), self.current_token)
        if self.current_token.token_type == token_type:
            self.next_token()
        else:
            ctoken = self.current_token.token_type
            token = self.current_token
            row, column = token.row, token.column
            ex = f"({row}:{column}){red(token_type)} was expected but {red(ctoken)} found!"
            raise Exception(ex)
    def parse(self):
        return self.program()
    def program(self):
        ast_list = list()
        while self.current_token.token_type in (
                TokenType.WORD,
                TokenType.NEW,
                TokenType.SETVARIABLE,
                TokenType.ASSIGNMACRO,
                TokenType.CLOSE_CBRACKET,
                TokenType.MACRO):
            # print_debug(f"I'm looking for programs: {self.current_token}")
            if self.current_token.token_type == TokenType.WORD:
                # print_debug("I've found a WORD token")
                assert False, (red("VARIABLES NOT IMPLEMENTED YET"))
                continue
            if self.current_token.token_type == TokenType.NEW:
                self.eat(TokenType.NEW)
                ast_list.append(self.new())
                # print_debug("I've found a NEW token")
                continue
            if self.current_token.token_type == TokenType.SETVARIABLE:
                "var WORD ASSIGN EXP"
                ast_list.append(self.assign())
                continue
            if self.current_token.token_type == TokenType.ASSIGNMACRO:
                self.assignmacro()
                continue
            if self.current_token.token_type == TokenType.CLOSE_CBRACKET:
                self.eat(TokenType.CLOSE_CBRACKET)
                return ast_list
            if self.current_token.token_type == TokenType.MACRO:
                ast_list.extend(self.macro())
                continue
            assert False, "You shouldn't be here"

        # print_debug(f"{ast_list =}")
        if (self.position+1 < len(self.tokens)):
            print(red("There are still tokens to parse"))
            print(self.tokens[self.position])
        program = Program(ast_list)
        return program
    def assignmacro(self):
        self.eat(TokenType.ASSIGNMACRO)
        print("I'm macroing here")
        self.eat(TokenType.MACRO)
        name_token = self.current_token
        self.eat(TokenType.WORD)
        self.eat(TokenType.OPEN_CBRACKET)
        ast_list = self.program()
        name = name_token.token_value
        print("I'm here")
        self.macros[name] = ast_list
    def macro(self):
        self.eat(TokenType.MACRO)
        name_token = self.current_token
        self.eat(TokenType.WORD)
        print(self.macros)
        name = name_token.token_value
        if name not in self.macros:
            raise Exception(red(f"{name} is not assigned to a macro before"))
        ast_of_macro = self.macros[name]
        return ast_of_macro
    def assign(self):
        "var WORD ASSIGN EXP"
        self.eat(TokenType.SETVARIABLE)
        name_token = self.current_token
        self.eat(TokenType.WORD)
        self.eat(TokenType.ASSIGN)
        exp = self.exp()
        return Assign(name_token, exp)


    def new(self):
        # print_debug("Adding new")
        if self.current_token.token_type == TokenType.WORD:
            token = self.current_token
            self.eat(TokenType.WORD)
            type_of_the_new = token.token_value
            assert len(NEW_TYPES) != 1, "You forgot a NEW type"
            if type_of_the_new == "Card":
                return self.card()
    def card(self):
        token = self.current_token
        self.eat(TokenType.WORD)
        card_name = token.token_value
        name_block = self.name_block()
        return Card(card_name, name_block)
    def name_block(self):
        # print_debug(blue("[EATING]"), "OPEN_CBRACKET")
        self.eat(TokenType.OPEN_CBRACKET)
        """(name:exp) (,name:exp) *"""
        names = list()
        names.append(self.name())
        while self.current_token.token_type == TokenType.SEP:
            self.eat(TokenType.SEP)
            names.append(self.name())
        self.eat(TokenType.CLOSE_CBRACKET)
        return NameBlock(names)
    def name(self):
        last_token = self.current_token
        self.eat(TokenType.WORD)
        name = last_token.token_value
        self.eat(TokenType.COLON)
        exp = self.exp()
        return Name(name,exp)
    def exp(self):
        """ exp: (STR|INT|VARIABLE) ((PLUS|MINUS|MUL|DIV) (STR|INT|VARIABLE))*"""
        node = self.term()
        while self.current_token.token_type in (
                TokenType.PLUS,
                TokenType.MINUS):
            token = self.current_token
            if token.token_type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            if token.token_type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinOp(node, token, self.factor())
        return node

    def term(self):
        node = self.factor()
        while self.current_token.token_type in (
                TokenType.MUL,
                TokenType.DIV):
            token = self.current_token
            if token.token_type == TokenType.MUL:
                self.eat(TokenType.MUL)
            if token.token_type == TokenType.DIV:
                self.eat(TokenType.DIV)
            node = BinOp(node, token, self.factor())
        return node
    def factor(self):
        if self.current_token.token_type == TokenType.INTEGER:
            token = self.current_token
            self.eat(TokenType.INTEGER)
            return Integer(token)
        if self.current_token.token_type == TokenType.PLUS:
            token = self.current_token
            self.eat(TokenType.PLUS)
            return UnaryOp(token, self.factor())
        if self.current_token.token_type == TokenType.MINUS:
            token = self.current_token
            self.eat(TokenType.MINUS)
            return UnaryOp(token, self.factor())
        if self.current_token.token_type == TokenType.LPAREN:
            token = self.current_token
            self.eat(TokenType.LPAREN)
            node = self.exp()
            self.eat(TokenType.RPAREN)
            return node
        if self.current_token.token_type == TokenType.STR:
            token = self.current_token
            self.eat(TokenType.STR)
            return String(token)
        if self.current_token.token_type == TokenType.WORD:
            token = self.current_token
            self.eat(TokenType.WORD)
            return Variable(token)






def main():
    lexer = Lexer(TEST)
    parser = Parser(lexer)
    print(parser.parse())



if __name__ == "__main__": main()


# print(AST_COUNT)
