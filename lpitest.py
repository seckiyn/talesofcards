#!/usr/bin/env python3
"""
    Test tool for lexer, parser and interpreter
"""
import sys
import readline
from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from lprint import print_debug, print_error, red, blue, yellow


OPTIONS = {
        "step": False

        }
def exception(*args, ex=None, **kwargs):
    sep = kwargs.get("sep", " ")
    extext = red(sep.join(args))

    if not ex:
        ex = Exception(extext)
        raise ex
    raise ex(extext)
def print_help(filename):
    my_help = """\
Help:
PROGRAM [OPTIONS] <filename>

OPTIONS:
    --help: Print help
    --lex: Lex the file
    --parse: Parse the file
    --interpret: Interpret the file
    --step: Step by step(only for lex)"""
    print(my_help)

def read_and_return(filename):
    to_read = None
    print_debug(f"Reading file {filename}")
    with open(filename) as file:
        to_read = file.read()
    if not to_read:
        exception(f"File: \"{filename}\" is empty")
    return to_read


def handle_lex_next(inp):
    if inp == "exit":
        sys.exit()


def lex(filename):
    to_lex = read_and_return(filename)
    lexer = Lexer(to_lex)
    step = OPTIONS["step"]
    token = lexer.get_next_token()
    pt = lambda tok: print(yellow("[Token]"), tok)
    pt(token)
    while token.token_value:
        if step:
            handle_lex_next(input("Next: "))
        token = lexer.get_next_token()
        pt(token)




def lex_and_parse(filename):
    to_parse = read_and_return(filename)
    lexer = Lexer(to_parse)
    parser = Parser(lexer)
    ast = parser.parse()
    print(blue("[AST_LIST]"), ast.ast_list)

def lex_and_parse_and_interpret(filename):
    to_interpret = read_and_return(filename)
    lexer = Lexer(to_interpret)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.interpret()
    global_variables = interpreter.global_variables
    print_debug(global_variables)

def parse_args():
    ARGUMENTS = (
            "--step",
            "--lex",
            "--parse",
            "--interpret",
            "--help")
    if len(sys.argv) == 1:
        print(red("Not enough arguments"))
        print_help(sys.argv[0])
        sys.exit()
    if len(sys.argv) == 2:
        script_name, filename = sys.argv
        lex_and_parse_and_interpret(filename)
    if len(sys.argv) >= 3:
        script_name, *options, filename = sys.argv
        for option in options:
            if option not in ARGUMENTS:
                exception(f"I don't know this option: {option}")
        if "--step" in options:
            OPTIONS["step"] = True
        if "--lex" in options:
            lex(filename)
        if "--parse" in options:
            lex_and_parse(filename)
        if "--interpret" in options:
            lex_and_parse_and_interpret(filename)
        if "--help" in options:
            print_help()
    print("Exiting the program...")
    script_name, *arguments, filename = sys.argv



if __name__ == "__main__":
#    OPTIONS["step"] = True
#    lex_and_parse_and_interpret("try.toc")
#    lex_and_parse("try.toc")
#    lex("try.toc")
    parse_args()


