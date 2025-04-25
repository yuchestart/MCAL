from parser.tokenizer import Tokenizer,Token
from parser.expressions import Expressions
from parser.statements import Statements
from parser.base import ParserBase

class Parser(Statements,Expressions,ParserBase,Tokenizer):
    def __init__(self,code:str|list[Token],mode = "code"):
        if mode == "code":
            self.code = code
        elif mode == "tokens":
            self.tokens = code
        self.init_tokenizer(mode)
    
    def parse_program(self):
        statements = []
        try:
            while not self.eof():
                statement = self.parse_toplevel()
                if statement is None:
                    break
                statements.append(statement)
        except EOFError:
            return statements
        raise Exception("DAFUQ?")