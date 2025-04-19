from nodes.expressions.primitives import *
from parser.base import ParserBase

class PrimitiveExpressions(ParserBase):

    def parse_null(self) -> Null | None:
        if not self.is_keywords("null"):
            return
        self.token_next()
        return Null()

    def parse_bool(self) -> Boolean | None:
        if not self.is_keywords(["true","false"]):
            return
        return Boolean(self.token_next()["value"] == "true")

    def parse_uuid(self) -> UUID | None:
        #TODO: Implement
        self.err("UUIDs are not implemented by MCAL yet")

    def parse_string(self) -> String | None:
        if self.token_peek()["type"] != "string":
            return
        s = self.token_next()
        subs = {}
        rawsub = s["substitutions"]
        for k in rawsub:
            p = self.__class__([x for x in rawsub[k]],mode="tokens")
            exp = p.parse_expression()
            subs[k] = exp
        return String(s["value"],subs)
    
    def parse_number(self) -> Number | None:
        if self.token_peek()["type"] != "number":
            return
        numstring:str = self.token_next()["value"]
        numtype = "int"
        explicit_type = False
        explicit_sign = False
        signed = True
        modifier = 0
        if numstring[-1] in self.NUMTYPES:
            rawtype = numstring[-1].lower()
            if rawtype == "i":
                numtype = "int"
            elif rawtype == "f":
                numtype = "float"
            elif rawtype == "l":
                numtype = "long"
            elif rawtype == "d":
                numtype = "double"
            elif rawtype == "s":
                numtype = "short"
            elif rawtype == "b":
                numtype = "byte"
            modifier = 1
            explicit_type = True
        elif numstring[-1] in "uUsS":
            signed = numstring[-1].lower() == "s"
            modifier = 2
            explicit_sign = True
        if len(numstring) >= 2 and numstring[-2] in "uUsS":
            if modifier == 2:
                self.err(f"Unexpected '{numstring[-2]}'")
            signed = numstring[-2].lower() == "s"
            modifier = 3
            explicit_sign = True
        numeralcutoff = 0 if modifier == 0 else 1 if modifier < 3 else 2
        try:
            numerals = float(numstring if numeralcutoff == 0 else numstring[:-numeralcutoff])
            if numerals % 1 != 0:
                if not explicit_type:
                    numtype = "double"
                elif numtype in self.PRIMITIVES_INTS:
                    self.err(f"Expected integer")
                if explicit_sign:
                    self.err(f"Sign notation is for integers only.")
        except ValueError as e:
            self.err(f"Invalid numeral: '{e}'")
        return Number(numerals,signed,numtype)


    def parse_coordinate(self) -> Coordinate | None:
        if not self.is_keywords("coordinate"):
            return
        self.token_next()
     #   print(self.token_peek())
        self.skip_punc("(")
        type = ""
        components = []
        for i in range(3):
            if type != "" and type != "world":
                self.skip_punc(type)
            elif self.is_punc("^") or self.is_punc("~"):
                if type == "world":
                    self.err("Unexpected coordinate type denoter")
                type = self.token_next()["value"]
            if type == "":
                type = "world"
            components.append(self.parse_expression())
      #  print(self.token_peek())
        self.skip_punc(")")
        type = "local" if type == "^" else "relative" if type == "~" else "world"
        return Coordinate(type,*components)
