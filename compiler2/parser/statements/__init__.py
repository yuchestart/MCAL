from parser.base import ParserBase
from parser.statements.funcandvar import FuncAndVarStatements
from parser.statements.mc import MinecraftStatements
from parser.statements.oop import OOPStatements
from parser.statements.control import ControlFlowStatements
from parser.statements.modules import ModuleStatements
from nodes.ast.util import CodeBlock

class Statements(
    MinecraftStatements,
    OOPStatements,
    ControlFlowStatements,
    ModuleStatements,
    FuncAndVarStatements,
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
            self.parse_dec_variable,
            self.parse_throw,
            self.parse_assert,
            self.parse_expression,
            self.parse_return
        ]
        value = None
        nosm = False
        nosmv = self.loop_parsers(parsersnosm)
        nosm = bool(nosmv)
        if value is None:
            value = self.loop_parsers(parsers)
        print("V",value)
        if use_sm and not nosm:
            self.skip_punc(";")
        return value

    def parse_definition(self):
        parsers = [
            self.parse_namespace,
            self.parse_dec_class,
            self.parse_dec_struct,
            self.parse_dec_function,
            self.parse_dec_variable,
        ]
        return self.loop_parsers(parsers)

    def parse_toplevel(self):
        parsers = [
            self.parse_using_namespace,
            self.parse_import,
            self.parse_export,
            self.parse_definition,
        ]
        value = self.loop_parsers(parsers)
        # print(value)
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