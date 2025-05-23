from compiler.ast.values import DataType, Identifier
from compiler.ast.dtypes import (
    UuidDType,
    BoolDType,
    ByteDType,
    CompoundDType,
    DoubleDType,
    FloatDType,
    IntDType,
    LongDType,
    ShortDType,
    StringDType,
    ArrayDType,
    Void,
    FunctionDType,
    ReferenceDType,
    NullableDType,
)

from compiler.ast.minecraft import (
    MinecraftObjDType,
    StorageDType,
    EntityDType,
    BlockDType,
)

from compiler.parser.base import ParserBase, ParserException
from compiler.tokenizer.interfaces import Token

import pcre2
from typing import *


class ParserDataTypes(ParserBase):

    PRIMITIVE_DTYPE_MAP = {
        "int": IntDType,
        "float": FloatDType,
        "double": DoubleDType,
        "long": LongDType,
        "byte": ByteDType,
        "bool": BoolDType,
        "short": ShortDType,
        "string": StringDType,
        "array": ArrayDType,
        "uuid": UuidDType,
        "compound": CompoundDType,
        "void": Void,
        "storage": StorageDType,
        "entity": EntityDType,
        "block": BlockDType,
    }

    # FIXME: Compiler errors for improper formatting don't work
    # Break case: unclosed angle brackets
    def dtype_minecraftobj(
        self, tokens: List[Token]
    ) -> Tuple[int, MinecraftObjDType] | None:
        dtype: MinecraftObjDType = None
        isident: bool = False
        finalidx = 0
        elevation = 0
        for i, token in enumerate(tokens):
            if self.ignore(token):
                continue
            if token.type not in ["PRIMITIVE", "IDENTIFIER", "OPERATOR"]:
                raise ParserException(
                    f"Unexpected '{token.data}'.", token.position
                )
            if token.type == "PRIMITIVE":
                if dtype:
                    raise ParserException(
                        f"Unexpected identifier.", token.position
                    )
                dtype = self.PRIMITIVE_DTYPE_MAP[token.data]("")
            if token.type == "IDENTIFIER":
                if not isident:
                    raise ParserException(
                        f"Unexpected identifier.", token.position
                    )
                dtype.name = token.data
                isident = False
            if token.type == "OPERATOR":
                if token.data == "<":
                    isident = True
                    elevation += 1
                elif token.data == ">":
                    elevation -= 1
                    if elevation < 0:
                        raise ParserException(
                            "Unmatched '>'", token.position
                        )
                    finalidx = i
                    break
        if elevation > 0:
            raise ParserException("Unmatched '<'", tokens[-1].position)
        return finalidx + 1, dtype

    # FIXME: Compiler errors for improper formatting don't work
    # Break case: unclosed angle brackets and parentheses
    def dtype_function(self, tokens: List[Token]) -> Tuple[int, FunctionDType] | None:
        dtype: FunctionDType = FunctionDType(None, [])
        functionmode = "ret_start"
        i = 0
        finalidx = 0
        elevation = 0
        while (i + 1) < len(tokens):
            i += 1
            token = tokens[i]

            if self.ignore(token):
                continue

            if functionmode == "ret_start":
                if token.type != "OPERATOR" or token.data != "<":
                    raise ParserException(
                        "Expected '<' after 'function'.", token.position
                    )
                functionmode = "ret"
                elevation += 1

            elif functionmode == "ret":
                returntype_tokens = []
                rest = tokens[i:]
                for j, t in enumerate(rest):
                    if self.ignore(t):
                        continue
                    if t.type == "OPERATOR":
                        if t.data == "<":
                            elevation += 1
                        if t.data == ">":
                            elevation -= 1
                            if elevation < 0:
                                raise ParserException(
                                    "Unmatched '>'", t.position
                                )
                            i = j + i
                            break
                    returntype_tokens.append(t)
                _, dtype.returnType = self.parse_datatype(returntype_tokens)
                functionmode = "param_start"

            elif functionmode == "param_start":
                if token.type != "GROUP_START":
                    raise ParserException(
                        "Expected '(' after '>'", token.position
                    )
                functionmode = "param"
                elevation += 1

            elif functionmode == "param":
                param_tokens = []
                rest = tokens[i:]
                currentparam = []
                for j, t in enumerate(rest):
                    if self.ignore(t):
                        continue
                    if t.type == "GROUP_START":
                        elevation += 1
                    if t.type == "GROUP_END":
                        elevation -= 1
                        if elevation < 0:
                            raise ParserException(
                                "Unmatched ')'", t.position
                            )
                        finalidx = j + i
                        break
                    if t.type == "LIST_SEPERATOR" and elevation == 0:
                        if len(currentparam) == 0:
                            raise ParserException(
                                "Unexpected ','", t.position
                            )
                        param_tokens.append(currentparam.copy())
                        currentparam = []
                        continue
                    currentparam.append(t)
                if len(currentparam) > 0:
                    param_tokens.append(currentparam)
                param_dtypes = []
                for param in param_tokens:
                    idx, dt = self.parse_datatype(param)
                    param_dtypes.append(dt)
                dtype.parameters = param_dtypes
                break

        if elevation > 0:
            raise ParserException("Unmatched '<' or '('", tokens[-1].position)
        return finalidx, dtype

    # HACK: Find cases where improper formatting doesn't throw a compiler error
    def parse_datatype(self, tokens: List[Token]) -> Tuple[int, DataType] | None:
        dtype: DataType = None

        typeof_dtype = "primitive"

        nextidx = 0
        finalidx = 0

        # Parse regular primitives
        for i, token in enumerate(tokens):
            if self.ignore(token):
                continue

            if token.type not in [
                "PRIMITIVE",
                "IDENTIFIER",
                "OPERATOR",
                "ARRAY_START",
                "ARRAY_END",
            ]:
                finalidx = i
                break

            if token.type == "PRIMITIVE" and token.data == "function":
                typeof_dtype = "function"
                nextidx = i
                break

            if token.type == "PRIMITIVE" and token.data in [
                "entity",
                "storage",
                "block",
            ]:
                typeof_dtype = "mc_object"
                nextidx = i
                break

            if token.type in ["PRIMITIVE", "IDENTIFIER"]:
                if dtype:
                    break
                if token.data in self.PRIMITIVE_DTYPE_MAP:
                    dtype = self.PRIMITIVE_DTYPE_MAP[token.data]()
                else:
                    dtype = Identifier(token.data)

        if typeof_dtype == "function":
            finalidx, dtype = self.dtype_function(tokens[nextidx:])
        elif typeof_dtype == "mc_object":
            finalidx, dtype = self.dtype_minecraftobj(tokens[nextidx:])

        # Account for the offset
        finalidx += nextidx

        # Array, reference, and nullable
        rest = tokens[finalidx + 1 :]
        elevation = 0
        for i, token in enumerate(rest):
            if self.ignore(token):
                continue
            if token.type not in ["ARRAY_START", "ARRAY_END", "OPERATOR"]:
                break

            if token.type == "OPERATOR":
                if token.data == "&":
                    dtype = ReferenceDType(dtype)
                elif token.data == "?":
                    dtype = NullableDType(dtype)
                else:
                    raise ParserException(
                        f"Unexpected '{token.data}'.", token.position
                    )

            if token.type == "ARRAY_START":
                elevation += 1
            if token.type == "ARRAY_END":
                elevation -= 1
                if elevation < 0:
                    raise ParserException(
                        "Unmatched ']' after '['.", token.position
                    )
                dtype = ArrayDType(dtype)

        if elevation > 0:
            raise ParserException("Unmatched '['", tokens[-1].position)

        return finalidx, dtype
