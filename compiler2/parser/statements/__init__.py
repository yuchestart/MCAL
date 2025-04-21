from parser.base import ParserBase
from parser.statements.varandfunc import VarAndFuncStatements
from parser.statements.mc import MinecraftStatements
from parser.statements.oop import OOPStatements
from parser.statements.control import ControlFlowStatements
from parser.statements.modules import ModuleStatements
from nodes.util import CodeBlock

class Statements(
    MinecraftStatements,
    OOPStatements,
    ControlFlowStatements,
    ModuleStatements,
    VarAndFuncStatements,
    ParserBase
):
    
    def parse_statement(self,use_sm=True):
        #print(self.token_peek())
        parsersnosm = [
            self.parse_if,
            self.parse_loop_for,
            self.parse_loop_while,
            self.parse_try,
        ]
        parsers = [
            self.parse_throw,
            self.parse_assert,
            self.parse_expression
        ]
        value = None
        nosm = False
        for parser in parsersnosm:
            value = parser()
            if value is not None:
                nosm = True
                break
        if value is None:
            for parser in parsers:
                value = parser()
                if value is not None:
                    break
        if value is None:
            dt = self.parse_datatype()
            if dt.base is None:
                self.err("dafuq?")
            if self.token_peek()["type"] != "ident":
                self.err("Expected identifier")
            name = self.token_next()["value"]
            value = self.parse_dec_variable(dt,name)
        if use_sm and not nosm:
            self.skip_punc(";")
        return value

    def parse_definition(self,dt=None,name:str=None):
        nodtparser = [
            self.parse_namespace,
        ]
        dtparser = [
            self.parse_dec_function,
            self.parse_dec_variable,
        ]
        if dt.base is None:
            value = None
            for parser in nodtparser:
                value = parser()
                if value is not None:
                    break
        else:
            value = None
            for parser in dtparser:
                value = parser(dt,name)
                if value is not None:
                    break
            if value is None:
                self.err("Expected definition")
        return value

    def parse_toplevel(self):
        parsers = [
            self.parse_using_namespace,
            self.parse_import,
            self.parse_export,
            self.parse_definition,
        ]
        dt = self.parse_datatype()
        if dt.base is not None:
            if self.token_peek()["type"] != "ident":
                self.err("Expected name")
            name = self.token_next()["value"]
            value = self.parse_definition(dt,name)
        else:
            value = None
            for parser in parsers:
                value = parser()
                if value is not None:
                    break
        # print(value)
        self.skip_punc(";")
        return value

    def parse_scope(self,toplevel = False,singular=False):
        parser = self.parse_statement
        if toplevel:
            parser = self.parse_toplevel
        if singular and not self.is_punc("{"):
            return [parser()]
        self.skip_punc("{")
        statements = []
        while not self.eof():
            if self.is_punc("}"):
                break
            s = parser()
        # If some guy just spammed semicolons then add this so he can do that
            if s is None:
                continue
            statements.append(s)
        self.skip_punc("}")
        return statements