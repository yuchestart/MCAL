from parser.tokenizer import Tokenizer, Token
from typing import *
from nodes.util import *


class ParserBase(Tokenizer):
    def delimited(self, start, stop, seperator, parser, hardstop=True):
        nodes = []
        first = True
        if start:
            self.skip_punc(start)
        while not self.eof():
            print(self.token_peek())
            if self.is_punc(stop):
                break
            if first:
                first = False
            else:
                self.skip_punc(seperator)
            nodes.append(parser())
        if hardstop:
            self.skip_punc(stop)
        else:
            if not self.is_punc(stop):
                self.err(f"Expected {stop}")
        print(self.token_peek())
        return nodes

    def is_punc(self, value: str | list[str]) -> bool:
        if self.token_peek() is None:
            return False
        cond = (
            (self.token_peek()["value"] == value)
            if type(value) == str
            else (self.token_peek()["value"] in value)
        )
        return self.token_peek()["type"] == "punc" and cond

    def is_keywords(self, value: str) -> bool:
        if self.token_peek() is None:
            return False
        cond = (
            (self.token_peek()["value"] == value)
            if type(value) == str
            else (self.token_peek()["value"] in value)
        )
        return self.token_peek()["type"] == "keyword" and cond

    def skip_punc(self, value: str | list[str]) -> None:
        if self.token_peek() is None:
            self.err("Unexpected EOF")
        cond = (
            (self.token_peek()["value"] == value)
            if type(value) == str
            else (self.token_peek()["value"] in value)
        )
        if self.token_peek()["type"] == "punc" and cond:
            self.token_next()
            return
        self.err(f"Expected '{value}'")

    def skip_keywords(self, value: str | list[str]) -> bool:
        if self.token_peek() is None:
            self.err("Unexpected EOF")
        cond = (
            (self.token_peek()["value"] == value)
            if type(value) == str
            else (self.token_peek()["value"] in value)
        )
        if self.token_peek()["type"] == "keyword" and cond:
            self.token_next()
            return
        self.err(f"Expected '{value}")

    def parse_identifier(self):
        mode = "ident"
        seenident = False
        identchain = []
        if self.token_peek()["type"] != "ident":
            # print(seenident,identchain,self.token_peek())
            if seenident:
                # HACK: Idk what's going on here but I'm throwing an error
                self.err("Expected identifier")
            return
        seenident = True

        return Identifier(self.token_next()["value"])

    def parse_name(self):
        mode = "namespace"
        ident = ""
        while not self.eof():
            if mode == "namespace":
                if (
                    self.token_peek()["type"] != "ident"
                    and self.token_peek()["type"] != "keyword"
                ):
                    break
                ident += self.token_next()["value"]
                mode = "colon"
            elif mode == "colon":
                if self.token_peek()["type"] != "punc":
                    self.err("Expected ':'")
                ident += self.token_next()["value"]
                mode = "proceed"
            elif mode == "proceed":
                if (
                    self.token_peek()["type"] != "ident"
                    and self.token_peek()["type"] != "keyword"
                ):
                    break
                ident += self.token_next()["value"]
                mode = "seperator"
            elif mode == "seperator":
                if (
                    self.token_peek()["type"] != "punc"
                    or self.token_peek()["value"] not in "/."
                ):
                    break
                ident += self.token_next()["value"]
                mode = "proceed"
        return Name(ident)

    PRIMITIVES_VAR = "int long double short byte bool string compound function uuid coordinate entity block storage function".split(
        " "
    )
    PRIMITIVES_FUNC = PRIMITIVES_VAR + ["void"]
    PRIMITIVES_INTS = "byte short int long"

    def parse_datatype(self) -> Any | None:
        const = False
        extern = None
        if self.is_keywords(["const", "extern"]):
            for i in range(2):
                if self.is_keywords("const"):
                    const = True
                    self.token_next()
                elif self.is_keywords("extern"):
                    self.token_next()
                    self.skip_punc("<")
                    extern = self.parse_name()
                    self.skip_punc(">")

        dtype = None
        if self.token_peek()["type"] == "keyword":
            if self.token_peek()["value"] not in self.PRIMITIVES_FUNC:
                self.err("Expected datatype")
            if self.token_peek()["value"] in self.PRIMITIVES_INTS:
                dtype = IntegerDataType(self.token_next()["value"], True)
            elif self.token_peek()["value"] in ["signed", "unsigned"]:
                signed = self.token_next()["value"] == "signed"
                if (
                    self.token_peek()["type"] != "keyword"
                    or self.token_peek()["value"] not in self.PRIMITIVES_INTS
                ):
                    self.err("Expected 'byte', 'short', 'int', or 'long'")
                dtype = IntegerDataType(self.token_next()["value"], signed)
            else:
                dtype = self.token_next()["value"]

        if dtype is None:
            dtype = self.parse_identifier()

        # If dtype is a primitive
        if type(dtype) == str and dtype in ("function entity block".split(" ")):
            # These three types have a typegroup (<...>), so skip the first bracket
            self.skip_punc("<")
            if dtype == "function":
                ret_type = self.parse_datatype()
                parameters = []
                self.skip_punc(">")
                self.skip_punc("(")
                while True:
                    next = self.parse_datatype()
                    parameters.append(next)
                    # print(next,self.token_peek())
                    if self.is_punc(")"):
                        break
                    elif self.is_punc(","):
                        self.skip_punc(",")
                    else:
                        self.err(f"Expected ',' or ')'")
                dtype = FunctionDataType(ret_type, parameters)
                self.skip_punc(")")
            elif dtype == "entity":
                dtype = EntityDataType(self.parse_name())
                self.skip_punc(">")
            elif dtype == "block":
                dtype = BlockDataType(self.parse_name())
                self.skip_punc(">")

        if type(dtype) == str:
            dtype = PrimitiveDataType(dtype)

        # Parse things like arrays and references
        mode = "none"
        typechain = []
        while not self.eof():
            if self.token_peek()["type"] != "punc":
                break
            elif self.token_peek()["value"] not in "[]&?":
                break
            if mode == "closearr":
                if self.token_peek()["value"] != "]":
                    self.err("Expected ']'")
                mode = "none"
                typechain.append("arr")
                self.token_next()
                continue
            elif self.token_peek()["value"] == "[":
                mode = "closearr"
                self.token_next()
            elif self.token_peek()["value"] == "&":
                typechain.append("reference")
                self.token_next()
            elif self.token_peek()["value"] == "?":
                typechain.append("nullable")
                self.token_next()

        return DataType(
            extern=extern,
            const=const,
            base=dtype,
            chain=typechain
        )

    # These exist so that I can get intellisense on them

    def parse_expression(self):
        pass

    def parse_atom(self):
        pass

    def parse_statement(self):
        pass

    def parse_scope(self):
        pass

    def parse_definition(self, dt=False):
        pass
