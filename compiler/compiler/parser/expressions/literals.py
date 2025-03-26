from compiler.parser.expressions.base import ParserExpressionsBase, ParserException

from compiler.tokenizer.interfaces import Token

from compiler.ast.values import Value
from compiler.ast.primitives import Compound, Array, Number, String, Boolean
from compiler.ast.dtypes import (
    IntDType,
    LongDType,
    ByteDType,
    ShortDType,
    FloatDType,
    DoubleDType,
)

from typing import *
import re
import pcre2


class ParserExpressionsLiterals(ParserExpressionsBase):
    # Use regular RE for this, as pcre2 throws an error
    REGEX_NUMBER_SPLITTER = r"(-?\d+(?:\.\d+)?)(u|s|U|S)?([bBsSiIlLfFdD])?\b"
    NUMBER_SUFFIX_DTYPES = {
        "i": IntDType,
        "l": LongDType,
        "b": ByteDType,
        "s": ShortDType,
        "f": FloatDType,
        "d": DoubleDType,
    }

    def parse_expression_bool(self, tokens: List[Token]) -> Tuple[int, Boolean | None]:
        finalidx = 0
        ret: Boolean = None
        for i, token in enumerate(tokens):
            if self.ignore(token):
                continue
            if token.type != "BOOLEAN":
                break

            ret = Boolean(token.data == "true")

            break
        return finalidx, ret

    def parse_expression_number(self, tokens: List[Token]) -> Tuple[int, Number | None]:
        finalidx = 0
        ret: Number = None
        for i, token in enumerate(tokens):
            if self.ignore(token):
                continue

            if token.type != "NUMBER":
                break

            match = re.match(self.REGEX_NUMBER_SPLITTER, token.data)
            groups: Tuple[str] = list(filter(lambda x: x is not None,match.groups()))
            ret = Number(groups[0],IntDType())

            if len(groups) == 3:
                ret.signed = groups[1].lower() == "s"
                ret.type = self.NUMBER_SUFFIX_DTYPES[groups[2].lower()]()
            elif len(groups) == 2:
                ret.type = self.NUMBER_SUFFIX_DTYPES[groups[1].lower()]()
            break

        return finalidx, ret

    def parse_expression_string(self, tokens: List[Token]) -> Tuple[int, String | None]:
        finalidx = 0
        ret: String = None
        raw_str: str = ""
        for i, t in enumerate(tokens):
            if self.ignore(t):
                continue
            if t.type != "STRING":
                return finalidx, ret
            raw_str = t.data[1:-1] # Remove the quotes
            break
        

        # String substitution expressions, like ${}
        # Any string breaking characters inside one still must be escaped with \
        # NOTE: Maybe add backtick strings like with JS
        sub_str = {}
        final_str = ""
        state = "none"
        escape = False
        i = -1  # Kinda wish there was do-while in python, but alas
        while (i + 1) < len(raw_str):
            i += 1
            char = raw_str[i]
            if escape:
                final_str += char
                escape = False
                continue
            if char == "\\":
                escape = True
                continue
            if char == "$":
                state = "check"
            elif state == "check":
                if char != "{":
                    state = "none"
                state = "substituting"
                #delete the $
                final_str = final_str[:-1]
                continue
            elif state == "substituting":
                rest = map(
                    lambda x: Token(x.lastgroup, x.group(0), x.start()),
                    pcre2.finditer(self.regex, raw_str[i:]),
                )
                cursub = []
                elevation = 0
                nexti = 0
                print(i)
                for j,t in enumerate(rest):
                    if self.ignore(t):
                        continue
                    if t.type == "BLOCK_START":
                        elevation += 1
                    if t.type == "BLOCK_END":
                        elevation -= 1
                        if elevation < 0:
                            nexti = j
                            break
                    cursub.append(t)
                sub_str[(i, i+nexti)] = cursub
                i += nexti
                state = "none"
            final_str += char

        sub_ast = {}
        for k in sub_str:
            sub_ast[k] = self.parse_expression(sub_str[k])[1]

        ret = String(final_str, sub_ast)

        return finalidx, ret

    def parse_expression_array(self, tokens: List[Token]) -> Tuple[int, Array | None]:
        ret: Array = None
        finalidx = 0

        state = "begin"
        i = -1
        while (i + 1) < len(tokens):
            i += 1
            token = tokens[i]
            if self.ignore(token):
                continue
            if state == "begin":
                if token.type != "ARRAY_START":
                    break
                state = "value"

            elif state == "value":
                rest = tokens[i:]
                valtokens = []
                nexti = 0
                elevation = 0
                for j, t in enumerate(rest):
                    if self.ignore(t):
                        continue
                    if t.type == "ARRAY_START":
                        elevation += 1
                    elif t.type == "ARRAY_END":
                        elevation -= 1
                        if elevation < 0:
                            nexti = j
                            break
                    valtokens.append(t)
                val = self.parse_expression(valtokens)
                i = nexti
                ret.values.append(val)
                state = "seperator"

            elif state == "seperator":
                if token.type == "LIST_SEPERATOR":
                    state = "value"
                elif token.type == "ARRAY_END":
                    break
                else:
                    raise ParserException(
                        f"Invalid Syntax: Expected ',' or ']' but got {token}",
                        token.position
                    )

        return finalidx, ret

    def parse_expression_compound(
        self, tokens: List[Token]
    ) -> Tuple[int, Value | None]:
        #TODO: Implement
        return 0, None

    def parse_expression_literal(
        self, tokens:List[Token]
    ) -> Tuple[int, Value | None]:
        parsers = [
            self.parse_expression_array,
            self.parse_expression_bool,
            self.parse_expression_compound,
            self.parse_expression_number,
            self.parse_expression_string
        ]
        ret: Value | None = None
        finalpos:int = 0
        for parser in parsers:
            pos, node = parser(tokens)
            if node is not None:
                ret = node
                finalpos = pos
                break
        
        return finalpos,ret
