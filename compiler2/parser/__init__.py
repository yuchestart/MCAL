from parser.tokenizer import Tokenizer
from parser.expressions import Expressions
from parser.statements import Statements

class Parser(Statements,Expressions,Tokenizer):
    def __init__(self,code:str):
        self.code = code
        self.init_tokenizer()