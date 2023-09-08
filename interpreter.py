from parser import Parser, AST_COUNT
from lexer import TokenType, Lexer
from lprint import red, blue, yellow, print_debug, green





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

TEST = """\
func function(hello, cello) {
    var mustafa = hello + cello
}

var what = 12
function(11, what, hello=13)

func deneme(){}
deneme()
"""

# assing variable a function
TEST = """\
func a() {}
var b = a()
"""
# TEST = """func function(one, two, tree) {} function()"""


TEST = """\
var c = 12

func a() {
    var b = 12
    return b
}

var b = a()
var c = 12

func addone(toadd) {return toadd + 1}

var twoplusone = addone(2)

"""

TEST = """\
var kustafa = -1
<<var mustafa = 12 + 1 == 12 - -1>>
"""


class Walker:
    def walk(self, ast):
        # print_debug("AST:", ast)
        if ast is None:
            print_debug("="*100)
        ast_name = "walk_" + type(ast).__name__
        print(yellow("Walking"), ast_name, yellow("right now"))
        # if logs.DEBUG: print(ast_name)
        func = getattr(self, ast_name)
        return func(ast)

## assert AST_COUNT == 13, f"You've {red('forgot')}ten to interpret an AST"
class Interpreter(Walker):
    def __init__(self, parser):
        self.global_variables = dict()
        self.global_variables["Cards"] = dict()
        self.functions = dict()
        self.parser = parser
        if parser:
            self.tree = self.parser.parse()
        else:
            self.tree = None
    def interpret(self):
        tree = self.tree
        print(yellow("Tree"), tree)
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
        operation = ast.op_token
        if operation.token_type == TokenType.PLUS:
            return right
        if operation.token_type == TokenType.MINUS:
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
        to_walk = ast.ast_list
        for new_ast in to_walk:
            self.walk(new_ast)
    def walk_Program(self, ast):
        print(yellow("Program"), ast)
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
    def walk_DefineFunction(self, ast):
        print(ast)
        name = ast.token.token_value
        namespace = self.walk(ast.namespace) #
        block = ast.block
        self.functions[name] = (namespace, block)
    def walk_NameSpace(self, ast):
        namespace = ast.namespace
        namedefaults = list()
        for callfunction in namespace:
            name, default = self.walk(callfunction)
            namedefaults.append((name, default))
        return namedefaults
    def walk_DefineName(self, ast):
        print(ast)
        name = ast.name.token_value
        default = None
        if ast.default:
            default = self.walk(default)
        return name, default
    def walk_CallFunction(self, ast):
        print(ast)
        name = ast.name.token_value
        namespace = ast.namespace.namespace
        int_namespace = [self.walk(name) for name in namespace]
        # TODO: special exceptions
        # TODO: raise exceptions if no function
        defined_function_namespace = self.functions[name][0]
        print(red(int_namespace))
        print(red(defined_function_namespace))
        # TODO: exhaustive variable exception
        defined_function_variables = [i[0] for i in defined_function_namespace]
        arguments = dict()
        # TODO: raise exception if positional arg after keyword arg
        for index, e in enumerate(int_namespace):
            if e[0] in defined_function_variables:
                arguments[e[0]] = e[1]
            else:
                arguments[defined_function_variables[index]] = e[1]

        print(yellow(arguments))
        function_walker = FunctionWalker(self, name, arguments)

        print(namespace)
        print("="*40)
        # print(self.walk(namespace))
        return function_walker.walkme()

    def walk_CallNameSpace(self, ast):
        print(ast)
        name = None
        if not ast.name:
            name = None
        else:
            name = ast.name.token_value
        value = self.walk(ast.value)
        return name, value


class FunctionWalker(Interpreter):
    def __init__(self, interpreter: Interpreter,function_name: str, function_variables:dict):
        function = interpreter.functions[function_name]
        print(yellow(len(function)))
        namespace = function[0]
        namespacenames = [i[0] for i in namespace]
        block = function[1]
        last_variables = dict()
        #TODO: Handle default variables later
        if len(namespace) != len(function_variables):
            raise Exception("Variables don't match")
        print(green(f"{namespace=}\n{function_variables=}\n{block=}"))

        for key, value in function_variables.items():
            if isinstance(key, int):
                my_name = namespace[key]
                last_variables[my_name] = value
            elif isinstance(key, str):
                if key in namespacenames:
                    last_variables[key] = value
        print(red(str(last_variables)))
        self.global_variables = interpreter.global_variables.copy()
        self.global_variables.update(last_variables)
        print(self.global_variables)
        self.tree = block
        self.to_return = None
        self.interpret()
    def walkme(self):
        return self.to_return
    def walk_Return(self, ast):
        self.to_return = self.walk(ast.exp)
















if __name__ == "__main__":
    lexer = Lexer(TEST)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    print(red("GLOBAL VARIABLES"))
    print(interpreter.global_variables)
    print(interpreter.functions)

