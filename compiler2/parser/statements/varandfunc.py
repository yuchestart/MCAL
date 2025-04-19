from parser.tokenizer import Token
from parser.expressions import Expressions
from parser.base import ParserBase
from nodes.statements.varandfunc import *
from nodes.util import PrimitiveDataType,DataType

class VarAndFuncStatements(Expressions,ParserBase):
    
    def parse_dec_variable_component(self,name=None):
        if name is None:
            if self.token_peek()["type"] != "ident":
                return
            name = self.token_next()["value"]
        value = None
        if self.is_punc("="):
            self.skip_punc("=")
            value = self.parse_expression()
            print(value)
        print(name,value)
        return {
            "name":name,
            "value":value
        }

    def parse_dec_function_parameter(self):
        dtype = self.parse_datatype()
        if self.token_peek()["type"] != "ident":
            self.err("Expected name")
        name = self.token_next()["value"]
        value = None
        if self.is_punc("="):
            self.token_next()
            value = self.parse_expression()
        return {
            "dtype":dtype,
            "name":name,
            "value":value
        }

    def parse_dec_variable(self,dtype:DataType,name:str):
      #  print(dtype)
        if dtype.base == PrimitiveDataType("void"):
            return
        if dtype.extern is not None:
            return
        first = self.parse_dec_variable_component(name)
        if first is None:
            return
        vars = [first]
        if self.token_peek()["type"] == "ident":
            vars += self.delimited("",";",",",self.parse_dec_variable_component,hardstop=False)
        return VariableDeclaration(
            dtype=dtype,
            vars=vars
        )

    
    def parse_dec_function(self,dtype,name:str):
        self.skip_punc("(")
        # print("BRO",self.token_peek())
        parameters = None
        if not self.is_punc(")"):
            parameters = self.delimited("",")",",",self.parse_dec_function_parameter)
        else:
            self.skip_punc(")")
        return FunctionDeclaration(
            name,
            dtype,
            parameters,
            self.parse_scope()
        )
