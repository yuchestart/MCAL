from parser.tokenizer import Tokenizer
from parser.expressions import Expressions
from parser.statements import Statements
from parser.base import ParserBase

class Parser(Statements,Expressions,ParserBase,Tokenizer):
    def __init__(self,code:str):
        self.code = code
        self.init_tokenizer()
