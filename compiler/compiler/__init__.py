from typing import *

from compiler.parser import Parser

keywordParsers = {}

def generate_ast()->list:
    parser = Parser()

    rawAST = parser.parse_file()

    return rawAST
    
    
