from nodes.expressions.primitives import *
from parser.base import ParserBase

class PrimitiveExpressions(ParserBase):

    def parse_null(self):
        if self.token_peek()["type"] != "keyword" or self.token_peek()["value"] != "null":
            return None
        self.token_next()
        return Null()

    def parse_bool(self):
        if self.token_peek()["type"] != "keyword" or self.token_peek()["value"] not in ["true","false"]:
            return None
        return Boolean(self.token_next()["value"] == "true")

    def parse_uuid():
        pass

    def parse_string(self):
        pass

    def parse_number(self):
        if self.token_peek()["type"] == "":
            pass

    def parse_coordinate():
        pass