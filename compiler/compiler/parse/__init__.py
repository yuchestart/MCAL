from typing import *

from compiler.parse.parser import Parser

keywordParsers = {}

def generate_ast()->list:
    parser = Parser()

    rawAST = parser.parse_file()

    return rawAST
    
    
