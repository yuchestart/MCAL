from compiler.parser.expressions.base import ParserExpressionsBase, ParserException

from compiler.tokenizer.interfaces import Token

from compiler.astnodes.values import Value
from compiler.astnodes.primitives import Compound, Array, Number, String, Boolean
from compiler.astnodes.dtypes import (
    IntDType,
    LongDType,
    ByteDType,
    ShortDType,
    FloatDType,
    DoubleDType,
)

from typing import *
import pcre2
from compiler.tokenizer.regex import S


class ParserExpressionsLiterals(ParserExpressionsBase):

    REGEX_NUMBER_SPLITTER = r"(-?\d+(?:\.\d+)?)(u|s|U|S)?([bsSlLfFdD]?)\b"
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
            if token.type in ["COMMENT", "WHITESPACE"]:
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
            if token.type in ["COMMENT", "WHITESPACE"]:
                continue

            if token.type != "NUMBER":
                break

            match = pcre2.match(self.REGEX_NUMBER_SPLITTER, token.data)
            groups: Tuple[str] = match.groups()
            ret = Number(groups[0])

            if len(groups) == 3:
                ret.signed = groups[1].lower() == "s"
                ret.dataType = self.NUMBER_SUFFIX_DTYPES[groups[2].lower()]()
            elif len(groups) >= 2:
                ret.dataType = self.NUMBER_SUFFIX_DTYPES[groups[1].lower()]()

            break
        return finalidx, ret

    def parse_expression_string(self, tokens: List[Token]) -> Tuple[int, String | None]:
        finalidx = 0
        ret: String = None
        raw_str: str = ""
        for i, t in enumerate(tokens):
            if t.type in ["COMMENT", "WHITESPACE"]:
                continue
            if t.type != "STRING":
                return finalidx, ret
            raw_str = t.data
            break

        escape = False
        escaped_str = ""
        for i, char in enumerate(raw_str):
            if escape:
                escaped_str += char
                escape = False
                continue
            if char == "\\":
                escape = True
                continue
            escaped_str += char

        # String substitution expressions, like ${}
        # Any string breaking characters inside one still must be escaped with \
        # NOTE: Maybe add backtick strings like with JS
        sub_str = {}
        final_str = ""
        state = "none"
        i = -1  # Kinda wish there was do-while in python, but alas
        while (i + 1) < len(escaped_str):
            i += 1
            char = escaped_str[i]
            if char == "$":
                state = "check"
            if state == "check":
                if char != "{":
                    state = "none"
                else:
                    state = "substituting"
                    continue
            if state == "substituting":
                rest = map(
                    lambda x: Token(x.lastgroup, x.group(0), x.start()),
                    pcre2.finditer(self.regex, raw_str[i:]),
                )
                cursub = []
                elevation = 0
                nexti = 0
                for j,t in enumerate(rest):
                    if t.type in ["COMMENT", "WHITESPACE"]:
                        continue
                    if t.type == "BLOCK_START":
                        elevation += 1
                    if t.type == "BLOCK_END":
                        elevation -= 1
                        if elevation < 0:
                            nexti = j
                            break
                    cursub.append(t)
                sub_str[(i, nexti)] = cursub
                i = nexti
                state = "none"
            final_str += char

        sub_ast = {}
        for k in sub_str:
            sub_ast[k] = self.parse_expression(sub_str[k])

        ret = String(final_str, sub_ast)

        return finalidx, ret

    def parse_expression_array(self, tokens: List[Token]) -> Tuple[int, Array | None]:
        ret: Array = Array([])
        finalidx = 0

        state = "begin"
        i = -1
        while (i + 1) < len(tokens):
            i += 1
            token = tokens[i]
            if token.type in ["COMMENT", "WHITESPACE"]:
                continue
            if token.type == "ARRAY_START":
                if state != "begin":
                    raise ParserException(
                        "Invalid Syntax: Unexpected '['", token.position
                    )
                state = "value"

            if state == "value":
                rest = tokens[i:]
                valtokens = []
                nexti = 0
                elevation = 0
                for j, t in enumerate(rest):
                    if t.type in ["COMMENT","WHITESPACE"]:
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

            if state == "seperator":
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
        pass
