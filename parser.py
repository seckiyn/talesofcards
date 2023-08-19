from enum import Enum, auto
from dataclasses import dataclass
from typing import Union, List
from lexer import Lexer, TokenType, Token

TEST = """\
new Card card_name {
    name: "doofenshmirtz",
    image: "card2.png",
}"""


print(TEST)

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
class SetVariable(AST):
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
    name_block: Union[NameBlock, TokenType]


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = self.get_tokens()
        print(*self.tokens, sep="\n")
        self.current_token = None
        self.position = -1
        self.next_token()
        self.program()
    def get_tokens(self):
        token_list = list()
        token = self.lexer.get_next_token()
        while token:
            token_list.append(token)
            token = self.lexer.get_next_token()
        return token_list
            
    def next_token(self):
        """
            advances and sets the current_token
        """
        self.position += 1
        if self.position >= len(self.tokens):
            print(f"Tokens of these makes the wrong {self.tokens}")

        self.current_token = self.tokens[self.position]
    def eat(self, token_type):
        if self.current_token.token_type == token_type:
            self.next_token()
        else:
            ctoken = self.current_token.token_type
            ex = f"{token_type} was expected but {ctoken} found!"
            raise Exception
    def parse(self):
        return self.program()
    def program(self):
        ast_list = list()
        while self.current_token.token_type in (
                TokenType.WORD,
                TokenType.NEW):
            print(f"I'm looking for programs: {self.current_token}")
            if self.current_token.token_type == TokenType.WORD:
                ...
            if self.current_token.token_type == TokenType.NEW:
                self.eat(TokenType.NEW)
                ast_list.append(self.new())

        program = Program(ast_list)
        return program

    def new(self):
        print("Adding new")
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






if __name__ == "__main__":
    lexer = Lexer(TEST)
    parser = Parser(lexer)
    print(parser.parse())
    

