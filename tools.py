from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
import os
from os.path import join
from lprint import print_debug, print_error, red, blue, yellow
import sys

def get_path(path="dir"):
    PATHS = ("dir", "path", "current")
    script_path = os.path.realpath(__file__)
    script_dir = os.path.dirname(script_path)
    if path == "dir": return script_dir
    if path == "path": return script_path
    if path == "current": return os.getcwd()
    raise Exception(f"There's no {path} you can only choose from {PATHS}")



def interpret_file(filename: str) -> dict:
    print_debug(f"Filename is {filename}", level="high")
    if not filename.endswith(".toc"):
        print_error("This is not a *.toc file")
        return -1
    toc_path = join(get_path("current"), filename)
    if not os.path.exists(toc_path):
        print_error(f"{toc_path} {red('does not exists')}")
        return -1
    with open(toc_path) as file:
        lexer = Lexer(file.read())
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        interpreter.interpret()
        return interpreter





from pprint import pprint

def dene():
    pprint(interpret_file("try.toc").global_variables)


if __name__ == "__main__":
    dene()
