from parser import Parser, AST_COUNT
from lexer import TokenType, Lexer
from lprint import red, blue, yellow, print_debug





"""
BinOp(AST) +
UnaryOp(AST) +
Integer(AST) +
Void(AST) +
SetVariable(AST) +
Variable(AST) +
Block(AST) +
Program(AST) +
Name(AST) +
NameBlock(AST) +
Card(AST) +
String(AST) +
Assign(AST) -
Variable(AST) -
"""

TEST = """\
new Card card_name {
    name: "doofenshmirtz",
    image: "card2.png" * 3
}

new Card var {name: "Mustafa", yas:12, yasboluuc:12/(2+1),
newer:3-8
}

"""

TEST = """\
var mustafa = 12
var mustafa = mustafa + 1
        """


TEST = """\
var mustafa = 0
macro !addone{
    var mustafa = mustafa + 1
    new Card hello {
        name:"Hello",
        image:"hello.png",
        mustafa: mustafa
    }

}
!addone <<1>>
!addone <<2>>
var mustafa2 = mustafa
var mustafa = 0
!addone
!addone
!addone

"""

class Walker:
    def walk(self, ast):
        # print_debug("AST:", ast)
        if ast is None:
            print_debug("="*100)
        ast_name = "walk_" + type(ast).__name__
        # if logs.DEBUG: print(ast_name)
        func = getattr(self, ast_name)
        return func(ast)

assert AST_COUNT == 13, f"You've {red('forgot')}ten to interpret an AST"
class Interpreter(Walker):
    def __init__(self, parser):
        self.global_variables = dict()
        self.global_variables["Cards"] = dict()
        self.parser = parser
    def interpret(self):
        tree = self.parser.parse()
        self.walk(tree)
        # print_debug(self.global_variables)
    def walk_BinOp(self, ast):
        left = self.walk(ast.left_token)
        right = self.walk(ast.right_token)
        operation = ast.op_token.token_type
        # print_debug(f"{left=}, {right=}")
        if operation == TokenType.PLUS:
            return left + right
        if operation == TokenType.MINUS:
            return left - right
        if operation == TokenType.MUL:
            return left * right
        if operation == TokenType.DIV:
            return left / right
        ex = f"There's no operation called {red(operation)}"
        raise Exception(ex)
    def walk_UnaryOp(self, ast):
        right = self.walk(ast.right_token)
        operation = ast.operation
        if operation == TokenType.PLUS:
            return right
        if operation == TokenType.MINUS:
            return -1 *right
    def walk_Integer(self, ast):
        return int(ast.token.token_value)
    def walk_Void(self, ast):
        return
    def walk_SetVariable(self, ast):
        assert False, red("SetVariable is not implemented yet")
    def walk_Variable(self, ast):
        assert False, red("Variable is not implemented yet")
    def walk_Block(self, ast):
        assert False, red("Block is not implemented yet")
    def walk_Program(self, ast):
        ast_list = ast.ast_list
        for new_ast in ast_list:
            self.walk(new_ast)
    def walk_Name(self, ast):
        name = ast.name
        eq = self.walk(ast.eq)
        return (name, eq)
    def walk_NameBlock(self, ast):
        namedblockdict = dict()
        for name in ast.name_list:
            name, exp = self.walk(name)
            namedblockdict[name] = exp
        return namedblockdict
    def walk_Card(self, ast):
        card_name = ast.card_name
        dictionary = self.walk(ast.name_block)
        self.global_variables["Cards"][card_name] = dictionary
    def walk_String(self, ast):
        return ast.token.token_value
    def walk_Assign(self, ast):
        name = ast.token.token_value
        expr = self.walk(ast.expr)
        self.global_variables[name] = expr
    def walk_Variable(self, ast):
        name = ast.token.token_value
        if name in self.global_variables:
            return self.global_variables[name]
        raise Exception(f"{name} variable is never assigned")



if __name__ == "__main__":
    lexer = Lexer(TEST)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print(interpreter.global_variables)
