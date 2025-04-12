from parser.tokenizer import Tokenizer,Token
from typing import *
from nodes.util import *

class ParserBase(Tokenizer):
    def delimited(self,start,stop,seperator,parser:function):
        nodes = []
        first = True
        if start:
            self.skip_punc(start)
        while not self.eof():
            if self.is_punc(stop):
                break
            if first:
                first = False
            else:
                self.skip_punc(seperator)
            nodes.append(parser())
        self.skip_punc(stop)
        return nodes
    
    def is_punc(self,value:str) -> bool:
        if self.token_peek() is None:
            return False
        return self.token_peek()["type"] == "punc" and self.token_peek()["value"] == value

    def skip_punc(self,value:str) -> None:
        if self.token_peek() is None:
            self.err("Unexpected EOF")
        if self.token_peek()["type"] == "punc" and self.token_peek()["value"] == value:
            self.token_next()
        self.err(f"Expected '{value}'")

    def parse_identifier(self):
        mode = "ident"
        seenident = False
        identchain = []
        while not self.eof():
            if mode == "ident":
                if self.token_peek()["type"] != "ident":
                    print(seenident,identchain,self.token_peek())
                    if not seenident:
                        # HACK: Idk what's going on here but I'm throwing an error
                        self.err("Expected identifier")
                    break
                seenident = True
                identchain.append(self.token_next()["value"])
                mode = "seperator"
            elif mode == "seperator":
                # I'm gonna assume that the datatype ends here for these guards
                if self.token_peek()["type"] != "punc":
                    break
                elif self.token_peek()["value"] not in [".","::"]:
                    break
                identchain.append(self.token_peek()["value"])
                self.token_next()
                mode = "ident"
        
        return Identifier(identchain)

    def parse_name(self):
        mode = "namespace"
        ident = ""
        while not self.eof():
            if mode == "namespace":
                if self.token_peek()["type"] != "ident" and self.token_peek()["type"] != "keyword":
                    break
                ident += self.token_next()["value"]
                mode = "colon"
            elif mode == "colon":
                if self.token_peek()["type"] != "punc":
                    self.err("Expected ':'")
                ident += self.token_next()["value"]
                mode = "proceed"
            elif mode == "proceed":
                if self.token_peek()["type"] != "ident" and self.token_peek()["type"] != "keyword":
                    break
                ident += self.token_next()["value"]
                mode = "seperator"
            elif mode == "seperator":
                if self.token_peek()["type"] != "punc" or self.token_peek()["value"] != "/":
                    break
                ident += self.token_next()["value"]
                mode = "proceed"
        return Name(ident)


    PRIMITIVES_VAR = "int long double short byte bool string compound function uuid coordinate entity block storage function".split(" ")
    PRIMITIVES_FUNC = PRIMITIVES_VAR + ["void"]
    PRIMITIVES_INTS = "byte short int long"
    def parse_datatype(self) -> Any | None:
        dtype = None
        if (self.token_peek()["type"] == "keyword"):
            if self.token_peek()["value"] not in self.PRIMITIVES_FUNC:
                self.err("Expected datatype")
            if self.token_peek()["value"] in self.PRIMITIVES_INTS:
                dtype = IntegerDataType(self.token_next()["value"],True)
            elif self.token_peek()["value"] in ["signed","unsigned"]:
                signed = self.token_next()["value"] == "signed"
                if self.token_peek()["type"] != "keyword" or self.token_peek()["value"] not in self.PRIMITIVES_INTS:
                    self.err("Expected 'byte', 'short', 'int', or 'long'")
                dtype = IntegerDataType(self.token_next()["value"],signed)
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
                    print(next,self.token_peek())
                    if self.is_punc(")"):
                        break
                    elif self.is_punc(","):
                        self.skip_punc(",")
                    else:
                        self.err(f"Expected ',' or ')'")
                dtype = FunctionDataType(ret_type,parameters)
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
        
        if len(typechain) > 0:
            return ModifiedDataType(dtype,typechain)
        return dtype

    def parse_scope(self):
        pass
