from parser.base import ParserBase
from typing import *
from nodes.ast.expressions.primitives import *

class CompoundExpressions(ParserBase):
    def parse_compound(self):
        if not self.is_punc("{"):
            return
        self.token_next()
        mode = "key"
        vals = {}
        curkey = None
        while not self.eof():
            if mode == "key":
                if self.is_punc('}'):
                    break
              #  print(self.token_peek())
                if self.token_peek()["type"] != "string":
                    self.err("Unexpected key")
                s = self.token_next()
                if len(s["substitutions"]) > 0:
                    self.err("Substitutions not allowed in compound keys")
                curkey = s["value"]
             #   print("ZXC")
                mode = "sep"
            if mode == "sep":
                self.skip_punc(":")
                mode = "value"
            if mode == "value":
             #   print(vals)
                vals[curkey] = self.parse_expression()
                mode = "comma"
            if mode == "comma":
                if not self.is_punc([",","}"]):
                    self.err("Expected ',' or '}'")
                if self.token_peek()["value"] == "}":
                    self.token_next()
                    break
                mode = "key"
        if mode not in ["comma","key"]:
            self.err("Unexpected end of expression")
        return Compound(vals)

    def parse_array(self):
        if not self.is_punc("["):
            return
        self.token_next()
        return Array(
            elements=self.delimited("","]",",",self.parse_expression)
        )
