from parser.tokenizer import Token
from parser.expressions import Expressions
from parser.base import ParserBase
from nodes.statements.varandfunc import *
from nodes.util import PrimitiveDataType

class VarAndFuncStatements(Expressions,ParserBase):
    
    def parse_dec_variable_component(self):
        print("X",self.token_peek())
        name = self.parse_identifier()
        value = None
        if self.is_punc("="):
            value = self.parse_expression()
        return {
            "name":name,
            "value":value
        }


    def parse_dec_variable(self):
        dtype = self.parse_datatype()
        print(dtype)
        if dtype == PrimitiveDataType("void"):
            self.err("'void' not allowed for variable declarations.")
        vars = self.delimited("",";",",",self.parse_dec_variable_component)
        return VariableDeclaration(
            dtype=dtype,
            vars=vars
        )

    
    def parse_dec_function(self):
        return_type = self.parse_datatype()
