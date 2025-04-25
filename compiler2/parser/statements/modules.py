from parser.base import ParserBase
from parser.expressions import Expressions
from typing import *

from nodes.ast.statements.modules import *

class ModuleStatements(Expressions,ParserBase):

    def parse_symboldef(self):
        print(self.token_peek())
        return self.parse_access_chain(["::"])

    def parse_import(self):
        if not self.is_keywords("import"):
            return
        self.token_next()
        source = None
        alias = None
        imports = "*"
        if self.token_peek()["type"] == "string" and len(self.token_peek()["substitutions"]) == 0:
            source = self.token_next()["value"]
            if self.is_keywords("as"):
                self.token_next()
                if self.token_peek()["type"] != "ident":
                    self.err("Expected identifier")
                alias = self.token_next()
        else:
            print(self.token_peek())
            imports = self.delimited("{","}",",",self.parse_symboldef)
            self.skip_keywords("from")
            if self.token_peek()["type"] != "string":
                self.err("Expected filepath")
            elif len(self.token_peek()["substitutions"]) > 0:
                self.err("Substitutions aren't allowed in imports")
            source = self.token_next()["value"]
        self.skip_punc(";")
        return Import(source,alias,imports)

    def parse_export(self):
        if not self.is_keywords("export"):
            return
        self.token_next()
        # Export everything
        if self.is_punc("*"):
            self.skip_punc("*")
            self.skip_punc(";")
            return Export("*")
        
        exports = []

        symbol = self.parse_definition()
        if symbol is None:
            id = self.parse_access_chain(["::"])
            if id is None:
                self.err("Expected symbol")
            mode = "sep"
            while not self.eof():
                if mode == "ident":
                    id = self.parse_access_chain(["::"])
                    if id is None:
                        self.err("Expected identifier")
                    exports.append(id)
                    mode = "sep"
                if mode == "sep":
                    if not self.is_punc(","):
                        break
                    self.token_next()
                    mode = "ident"
            self.skip_punc(";")
        else:
            exports = [symbol]
        return Export(exports)


    # This is toplevel only
    def parse_using_namespace(self):
        if not self.is_keywords("using"):
            return
        self.token_next()
        if not self.is_keywords("namespace"):
            return
        self.token_next()
        ns = self.parse_symboldef()
        self.skip_punc(";")
        return UsingNamespace(ns)

    def parse_namespace(self):
        if not self.is_keywords("namespace"):
            return
        self.token_next()
        if not self.token_peek()["type"] == "ident":
            self.err("Expected identifier")
        ident = self.token_next()["value"]
        block = None
        if self.is_punc("{"):
            block = self.parse_scope(True)
        else:
            self.skip_punc(";")
        return Namespace(ident,block)