from parser.tokenizer import Tokenizer, Token
from parser.base import ParserBase
from parser.statements.varandfunc import VarAndFuncStatements

class Statements(VarAndFuncStatements,ParserBase):
    
    def parse_toplevel():
        pass