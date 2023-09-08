import sys
from enum import Enum, auto
from dataclasses import dataclass
from typing import Union, List, Literal
from lexer import Lexer, TokenType, Token
from lprint import print_debug, red, blue, yellow, green


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

TEST = """

func Poison(tours) {
    var Health = 20
    }

Poison(tours="Deneme")

"""

TEST2 = """

func Poison(tours) {
    Health = 20 + deneme + deneme2 + tours
    if Health < deneme {
        Health = Health - 1
    }
}

"""

# Function Test
TEST = """
<< Define function no arguments >>
func deffunc1() { var a = 12 }
<< Define function one argument >>
func deffunc2(app) { var a = 12 }
<< Define function multiple arguments >>
func deffunc3(app, mapp, tapp) { var a = 12 }
<< Define function with default argument >>
func deffunc4(app=41) { var a = 12 }
<< Define function with multiple default argument >>
func deffunc5(app=51, mapp=52, tapp=53) { var a = 12 }


<< Call function no arguments >>
func1()
<< Call function one argument >>
func2(251)
<< Call function multiple arguments >>
func3(351, 352, 353)
<< Call function with default argument >>
func4(app=451)
<< Call function with multiple default argument >>
func5(app=551, mapp=552, tapp=553)

<< Mixed >>
func6(651, mapp=231, tapp=41)

<< Void function and void call >>
func deffunc6(){}
deffunc6()

"""

TEST = """\
func function(hello, cello) {
    var mustafa = hello + cello
}

var what = 12
function(12, what, hello=12)
"""
# print_debug(TEST)
# assing variable a function
TEST = """\
func a() {}
var b = a()
"""

TEST = """\
func return1() {return 1}
var b = return1()
"""

TEST = """\
var mustafa = 12 + 1 == 12 - -1
"""

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

GAMEVARIABLES = (
        "HEALTH",
        "SHIELD",
        )

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


AST_COUNT += 1
@dataclass
class DefineFunction(AST):
    token: Union[Token, AST]
    namespace: AST
    block: AST

AST_COUNT += 1
@dataclass
class NameSpace(AST):
    namespace: List[Token]

AST_COUNT += 1
@dataclass
class DefineName(AST):
    name: AST
    default: Union[AST, None]

AST_COUNT += 1
class CallName(AST):
    namespace: List[Token]


AST_COUNT += 1
@dataclass
class CallNameSpace(AST):
    value: AST
    name: Union[AST, None]

AST_COUNT += 1
@dataclass
class CallFunction(AST):
    name: AST
    namespace: AST

AST_COUNT += 1
@dataclass
class Return(AST):
    exp: AST



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
    def peek_token(self):
        position = self.position + 1
        if position >= len(self.tokens):
            print_debug(f"Tokens of these makes the wrong {self.tokens}")

        return self.tokens[position]

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
                TokenType.MACRO,
                TokenType.DEFINEFUNCTION,
                TokenType.RETURN):
            # print_debug(f"I'm looking for programs: {self.current_token}")
            if self.current_token.token_type == TokenType.WORD:
                # print_debug("I've found a WORD token")
                name_token = self.current_token
                self.eat(TokenType.WORD)
                if self.current_token.token_type == TokenType.LPAREN:
                    ast_func = self.functioncall(name_token)
                    ast_list.append(ast_func)
                    continue
                tok = self.current_token
                pos = tok.column, tok.row

                assert False, (red(f"{tok}:{pos}VARIABLES NOT IMPLEMENTED YET"))
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
            if self.current_token.token_type == TokenType.DEFINEFUNCTION:
                function = self.function()
                ast_list.append(function)
                continue
            if self.current_token.token_type == TokenType.RETURN:
                self.eat(TokenType.RETURN)
                exp = self.exp()
                ast_list.append(Return(exp))
                continue
            assert False, f"{self.current_token}: You shouldn't be here"

        # print_debug(f"{ast_list =}")
        if (self.position+1 < len(self.tokens)):
            print_debug(red("There are still tokens to parse"))
            print_debug(self.tokens[self.position])
        program = Program(ast_list)
        return program
    def function(self):
        self.eat(TokenType.DEFINEFUNCTION)
        name_token = self.current_token
        self.eat(TokenType.WORD)
        namespace = self.functionnamespace()
        block = self.functionblock()
        return DefineFunction(name_token, namespace, block)
    def functionnamespace(self):
        self.eat(TokenType.LPAREN)
        """
            (WORD | WORD=EXP) | NULL (, WORD | WORD=EXP)*
        """
        namespace_list = list()
        if self.current_token.token_type == TokenType.WORD:
            default = None
            name_token = self.current_token
            self.eat(TokenType.WORD)
            if self.current_token.token_type == TokenType.ASSIGN:
                self.eat(TokenType.ASSIGN)
                default = self.exp()
                name_ast = DefineName(name_token, default)
            else:
                name_ast = DefineName(name_token, default)



            namespace_list.append(name_ast)

        while self.current_token.token_type == TokenType.SEP:
            self.eat(TokenType.SEP)
            name_token = self.current_token
            self.eat(TokenType.WORD)
            name_ast = None
            default = None
            print_debug(green("*"*20))
            print_debug(green(name_token), green(self.current_token))
            if self.current_token.token_type == TokenType.ASSIGN:
                self.eat(TokenType.ASSIGN)
                default = self.exp()
                print_debug(blue(self.current_token))
                name_ast = DefineName(name_token, default)
            else:
                name_ast = DefineName(name_token, default)
            print_debug("Adding", yellow(name_ast))
            namespace_list.append(name_ast)
        print_debug(red(self.current_token))
        self.eat(TokenType.RPAREN)
        return NameSpace(namespace_list)
    def functioncall_namespace(self):
        namespace_list = list()
        name_ast = None
        print_debug(green("Namespace current token:"), red(self.current_token))
        self.eat(TokenType.LPAREN)
        if self.current_token.token_type != TokenType.RPAREN:
            name = None
            if self.current_token.token_type == TokenType.WORD and self.peek_token() == TokenType.ASSIGN:
                name = self.current_token
                self.eat(TokenType.WORD)
                self.eat(TokenType.ASSIGN)
                value = self.exp()
                name_ast = CallNameSpace(value, name)
                namespace_list.append(name_ast)
            value = self.exp()
            name_ast = CallNameSpace(value, name)
            namespace_list.append(name_ast)




        while self.current_token.token_type == TokenType.SEP:
            self.eat(TokenType.SEP)
            name_ast = None
            print_debug(green("Namespace current token:"), red(self.current_token))
            name = None
            print_debug(red("Comp:"), self.peek_token().token_type, self.current_token.token_type, self.current_token.token_type == TokenType.WORD and self.peek_token() == TokenType.ASSIGN)
            if self.current_token.token_type == TokenType.WORD and self.peek_token().token_type == TokenType.ASSIGN:
                name = self.current_token
                self.eat(TokenType.WORD)
                self.eat(TokenType.ASSIGN)
                value = self.exp()
                name_ast = CallNameSpace(value, name)
                namespace_list.append(name_ast)
            else:
                value = self.exp()
                name_ast = CallNameSpace(value, name)
                namespace_list.append(name_ast)
        print_debug(red(self.current_token))
        print_debug(namespace_list)
        self.eat(TokenType.RPAREN)
        return NameSpace(namespace_list)


    def functionblock(self):
        """ TODO: Game should be a ast walker (interpreter)
            gameSOMETHING = what
            what = gameSOMETHING + 1
        """
        ast_list: List
        self.eat(TokenType.OPEN_CBRACKET)
        ast_list = self.program()
        return Block(ast_list)


    def assignmacro(self):
        self.eat(TokenType.ASSIGNMACRO)
        print_debug("I'm macroing here")
        self.eat(TokenType.MACRO)
        name_token = self.current_token
        self.eat(TokenType.WORD)
        self.eat(TokenType.OPEN_CBRACKET)
        ast_list = self.program()
        name = name_token.token_value
        print_debug("I'm here")
        self.macros[name] = ast_list
    def macro(self):
        self.eat(TokenType.MACRO)
        name_token = self.current_token
        self.eat(TokenType.WORD)
        print_debug(self.macros)
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
        node = self.mad()
        while self.current_token.token_type in (
                TokenType.EQ,
                TokenType.NOTEQ,
                TokenType.GT,
                TokenType.LT,
                TokenType.GTEQ,
                TokenType.LTEQ,
                ):
            token = self.current_token
            if token.token_type == TokenType.EQ:
                self.eat(TokenType.EQ)
            if token.token_type == TokenType.NOTEQ:
                self.eat(TokenType.NOTEQ)
            if token.token_type == TokenType.GT:
                self.eat(TokenType.GT)
            if token.token_type == TokenType.LT:
                self.eat(TokenType.LT)
            if token.token_type == TokenType.GTEQ:
                self.eat(TokenType.GTEQ)
            if token.token_type == TokenType.LTEQ:
                self.eat(TokenType.LTEQ)
            node = BinOp(node, token, self.mad())
        return node

    def mad(self):
        """ exp: (STR|INT|VARIABLE) ((PLUS|MINUS|MUL|DIV) (STR|INT|VARIABLE))*"""
        node = self.term()
        while self.current_token.token_type in (
                TokenType.PLUS,
                TokenType.MINUS
                ):
            token = self.current_token
            if token.token_type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            if token.token_type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinOp(node, token, self.term())
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
        if self.current_token.token_type == TokenType.WORD and self.peek_token().token_type == TokenType.LPAREN:
            name_token = self.current_token
            self.eat(TokenType.WORD)
            token = self.functioncall(name_token)
            return token
        if self.current_token.token_type == TokenType.WORD:
            token = self.current_token
            self.eat(TokenType.WORD)
            return Variable(token)
    def functioncall(self, name_token):
        """FUNCTION_NAME NAMESPACE"""
        function_name = name_token
        print_debug("Function name:", yellow(function_name))
        print_debug("Current token:", yellow(self.current_token))
        function_namespace = self.functioncall_namespace()
        ast = CallFunction(function_name, function_namespace)
        return ast






def main():
    lexer = Lexer(TEST)
    parser = Parser(lexer)
    print(parser.parse())



if __name__ == "__main__": main()


# print(AST_COUNT)
