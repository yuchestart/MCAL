from parser.base import ParserBase
from parser.statements.funcandvar import FuncAndVarStatements
#from parser
from nodes.ast.statements.oop import *

class OOPStatements(FuncAndVarStatements,ParserBase):
    def parse_dec_class_symbol(self):
        if self.is_keywords("using"):
            #GTFO THIS IS A USING STATEMENT
            self.token_next()
            users = self.delimited("",";",",",self.parse_access_chain(["::"]))
            if len(users) == 0:
                self.err("Expected identifier")
            return {"type":"using","symbols":users}
        
        accessmode = "public"
        if self.is_keywords(["public","private","protected"]):
            accessmode = self.token_next()["value"]
        static = False
        if self.is_keywords('static'):
            self.token_next()
            static = True
        print(self.token_peek())
        value = self.loop_parsers([lambda: self.parse_dec_function(False)])
        if value is None:
            value = self.loop_parsers([self.parse_dec_variable])
            self.skip_punc(";")
        return {
            "type":"declaration",
            "access":accessmode,
            "static":static,
            "dec":value
        }

    def parse_dec_class(self):
        if not self.is_keywords("class"):
            return
        self.token_next()
        if not self.token_peek()["type"] == "ident":
            self.err("Expected name")
        name = self.token_next()["value"]
        extenders = []
        if self.is_punc(":"):
            self.token_next()
            extenders = self.delimited("","{",",",self.parse_access_chain,False)

        self.skip_punc("{")

        declarations = []
        while not self.eof():
            print("GETOUT")
            if self.is_punc("}"):
                break
            symbol = self.parse_dec_class_symbol()
            if symbol is None:
                break
            declarations.append(symbol)

        self.skip_punc("}")
        
        return ClassDeclaration(declarations=declarations,extends=extenders,name = name)

    def parse_dec_struct(self):
        if not self.is_keywords("struct"):
            return
        self.token_next()
        special = None
        if self.is_keywords(["entity","block"]):
            special = [self.token_next()["value"],0]
            self.skip_punc("<")
            special[1] = self.parse_name()
            self.skip_punc(">")

        if not self.token_peek()["type"] == "ident":
            self.err("Expected name")
        name = self.token_next()["value"]
        self.skip_punc("{")

        declarations = []

        while not self.eof():
            if self.is_punc("}"):
                break
            symbol = self.parse_dec_variable()
            print(symbol)
            if symbol is None:
                self.err("Expected variable declaration or whatever")
            if len(symbol.vars) > 1:
                self.err("Dude you can't do that")
            declarations.append(symbol)
            self.skip_punc(";")
        self.skip_punc("}")
        return StructDeclaration(declarations,name)