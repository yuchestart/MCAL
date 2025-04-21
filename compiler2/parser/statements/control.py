from parser.base import ParserBase
from parser.statements.varandfunc import VarAndFuncStatements
from nodes.statements.control import *

class ControlFlowStatements(VarAndFuncStatements,ParserBase):
    def parse_if(self):
        if not self.is_keywords("if"):
            return
        blocks = []
        self.token_next()
        self.skip_punc("(")
        condition = self.parse_expression()
        self.skip_punc(")")
        blocks.append(('if',condition,self.parse_scope(singular=True)))
        while not self.eof():
            if not self.is_keywords(["elif","else"]):
                break
            if self.is_keywords('elif'):
                self.token_next()
                self.skip_punc("(")
                condition = self.parse_expression()
                self.skip_punc(")")
                blocks.append(('elif',condition,self.parse_scope(singular=True)))
            else:
                self.token_next()
                blocks.append(('else',None,self.parse_scope(singular=True)))
        return If(blocks)
    
    def parse_loop_while(self):
        if not self.is_keywords(["while","do"]):
            return
        scope = None
        condition = None
        if self.is_keywords("do"):
            # do while
            self.token_next()
            scope = self.parse_scope(singular=True)
            self.skip_keywords("while")
            self.skip_punc("(")
            condition = self.parse_expression()
            self.skip_punc(")")
            self.skip_punc(";")
            return While(condition,scope,"dowhile")
        else:
            self.token_next()
            self.skip_punc("(")
            condition = self.parse_expression()
            self.skip_punc(")")
            scope = self.parse_scope(singular=True)
            return While(condition,scope,"while")

    def parse_loop_for(self):
        if not self.is_keywords("for"):
            return
        self.token_next()
        self.skip_punc("(")
        dtype = self.parse_datatype()
        
        print(self.token_peek(),dtype)
        init = None
        if dtype.base is not None:
           # if dtype.base 
            if self.token_peek()["type"] != "ident":
                self.err("Expected name")
            init = self.parse_dec_variable(dtype,self.token_next()["value"])
        else:
            init = self.parse_expression()
        self.skip_punc(";")
        condition = self.parse_expression()
        self.skip_punc(";")
        increment = self.parse_expression()
        self.skip_punc(")")
        return For(init,condition,increment,self.parse_scope(singular=True))

    def parse_try(self):
        if not self.is_keywords("try"):
            return
        self.token_next()
        tryblock = self.parse_scope()
        catchblocks = []
        finallyblock = None
        while not self.eof():
            if self.is_keywords("catch"):
                self.token_next()
                vardec = None
                if self.is_punc("("):
                    self.token_next()
                    datatype = self.parse_datatype()
                    if self.token_peek()["type"] != "ident":
                        self.err("Expected name")
                    vardec = self.parse_dec_variable(datatype,self.token_next()["value"])
                    self.skip_punc(")")
                scope = self.parse_scope()
                catchblocks.append((vardec,scope))
            elif self.is_keywords("finally"):
                self.token_next()
                finallyblock = self.parse_scope()
                break
            else:
                break
        return Try(tryblock,catchblocks,finallyblock)

    def parse_throw(self):
        if not self.is_keywords("throw"):
            return
        self.token_next()
        return Throw(self.parse_expression())

    def parse_assert(self):
        if not self.is_keywords("assert"):
            return
        self.token_next()
        condition = self.parse_expression()
        error = None
        if self.is_punc(","):
            self.token_next()
            error = self.parse_expression()
        return Assert(condition,error)