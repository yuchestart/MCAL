from parser.base import ParserBase
from typing import *
from nodes.ast.expressions.mc import *

class MinecraftExpressions(ParserBase):
    def parse_command_call(self) -> CommandCall | None:
        if self.token_peek()["type"] not in ["ident","keyword"]:
            return
        name = self.parse_name()
        if name is None:
            return
        if self.token_peek()["type"] != "command" or self.token_peek()["start"] != "(":
            return
        s = self.token_next()
        subs = {}
        rawsub = s["substitutions"]
        for k in rawsub:
            p = self.__class__([x for x in rawsub[k]],mode="tokens")
            exp = p.parse_expression()
            subs[k] = exp

        return CommandCall(name,s["value"],subs)
    
    def parse_init_entity(self):
        if not self.is_keywords(["entity"]):
            return
        self.token_next()
        self.skip_punc("<")
        type = self.parse_name()
        self.skip_punc(">")
        self.skip_punc("(")
        exp = self.parse_expression()
        self.skip_punc(")")
        return EntityInit(type,exp)

    def parse_init_block(self):
        if not self.is_keywords(["block"]):
            return
        self.token_next()
        self.skip_punc("<")
        type = self.parse_name()
        self.skip_punc(">")
        self.skip_punc("(")
        exp = self.parse_expression()
        self.skip_punc(")")
        return BlockInit(type,exp)

    def parse_init_storage(self):
        if not self.is_keywords(["storage"]):
            return
        self.token_next()
        self.skip_punc("<")
        target = self.parse_name()
        self.skip_punc(">")
        return StorageInit(target)