from parser.tokenizer import Token
from parser.expressions import Expressions
from parser.base import ParserBase
from nodes.ast.statements.varandfunc import *
from nodes.ast.util import PrimitiveDataType,DataType

class FuncAndVarStatements(Expressions,ParserBase):
    
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
        print("BRUH",self.token_peek(),dtype)
        if self.token_peek()["type"] != "ident":
            self.err("Expected name")
        name = self.token_next()["value"]
        value = None
        if self.is_punc("="):
            self.token_next()
            print(self.token_peek())
            value = self.parse_expression()
        print("YO",value)
        return {
            "dtype":dtype,
            "name":name,
            "value":value
        }

    def parse_dec_variable(self):
        dtype = self.parse_datatype()
        if (dtype.base is None or
        dtype.base == PrimitiveDataType("void") or
        dtype.extern is not None):
            return
        if self.token_peek()["type"] != "ident":
            return
        name = self.token_next()["value"]
      #  print(dtype
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

    
    def parse_dec_function(self,canextern=False):
        dtype = self.parse_datatype()
        print(dtype)
        if not canextern:
            if dtype.extern:
                self.err("'extern' not allowed.")
        if dtype.base is None:
            return
        print(self.token_peek())
        if self.token_peek()["type"] != "ident":
            return
        name = self.token_next()["value"]
        if not self.is_punc("("):
            return
        self.skip_punc("(")
        # print("BRO",self.token_peek())
        parameters = None
        if not self.is_punc(")"):
            parameters = self.delimited("",")",",",self.parse_dec_function_parameter)
        else:
            self.skip_punc(")")
        print("BRO")
        return FunctionDeclaration(
            name,
            dtype,
            parameters,
            self.parse_scope()
        )

    def parse_return(self):
        if not self.is_keywords("return"):
            return
        self.token_next()
        return ReturnStatement(self.parse_expression())