from compiler.astnodes.values import DataType, Identifier
from compiler.astnodes.dtypes import (
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
)

from compiler.parser.base import ParserBase, ParserException
from compiler.tokenizer.interfaces import Token

import pcre2
from typing import *


class ParserDataTypes(ParserBase):

    PRIMITIVES = {
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
        "void": Void
    }

    # NOTE: Ignore all of these TODO's I'm rewriting this
    # TODO: Clean me up, this code is horrendous
    # FIXME: Resolve the runtime errors. There are probably like 5 bajillion of them.
    # FIXME: Throw compiler error for unclosed <>, (), and []
    # HACK: Test for edge cases
    def parse_datatype(
        self, tokens: List[Tuple[str, str, int]]
    ) -> Tuple[int, DataType] | None:
        # DATATYPE RULES:
        # If not a function:
        #   Only one identifier/primitive allowed
        #   Other modifiers like arrays and references follow
        # If it is a function:
        #   The outermost set of parentheses dictates the end of the datatype
        dtype: DataType
        isfunction = False
        identifierProvided = False
        functionpos = 0
        finalpos = 0
        finalidx = 0
    
        for i, token in enumerate(tokens):
            token_type, data, pos = token

            if token_type in ["COMMENT", "WHITESPACE"]:
                continue

            if token_type not in ["PRIMITIVE","IDENTIFIER","OPERATOR","ARRAY_START","ARRAY_END"]:
                finalidx = i
                finalpos = pos
                break

            if token_type == "PRIMITIVE" and data == "function":
                isfunction = True
                functionpos = i
                dtype = FunctionDType(None, [])
                continue

            if isfunction:
                break
            else:
                if token_type == "PRIMITIVE" or token_type == "IDENTIFIER":
                    if identifierProvided:
                        finalidx = i-1
                        finalpos = pos
                        break

                    identifierProvided = True
                    if data not in self.PRIMITIVES:
                        dtype = Identifier(data)
                    else:
                        dtype = self.PRIMITIVES[data]()
                    continue
                if token_type == "OPERATOR":
                    if identifierProvided:
                        if data == "&":
                            dtype = ReferenceDType(dtype)
                        finalpos = pos
                        finalidx = i
                        continue
                    else:
                        # HACK: Find an edge case
                        raise ParserException("Invalid Syntax: Unexpected operator", pos)

                if token_type == "ARRAY_START":
                    if identifierProvided:
                        if (len(tokens) == i + 1) or tokens[i + 1][0] != "ARRAY_END":
                            raise ParserException(
                                "Invalid Syntax: Expected ']' after '['", pos
                            )
                        dtype = ArrayDType(dtype)
                    else:
                        # HACK: Find an edge case
                        raise ParserException("Invalid Syntax: Unexpected '['",pos)
                    
                if token_type == "ARRAY_END":
                    if identifierProvided:
                        finalpos = pos
                        finalidx = i
                    else:
                        raise ParserException("Invalid Syntax: Unexpected ']'",pos)

        if isfunction:
            i = functionpos
            functionidx = 0
            while (i+1) < len(tokens):
                i+=1
                token_type = tokens[i][0]
                data = tokens[i][1]
                pos = tokens[i][2]
                if token_type in ["WHITESPACE","COMMENT"]:
                    continue

                if functionidx == 0:
                    # Start the function
                    if token_type != "OPERATOR" or data != "<":
                        raise ParserException(
                            "Invalid Syntax: Expected '<' after 'function'", pos
                        )
                    functionidx += 1
                elif functionidx == 1:
                    # Return type
                    returntype_tokens = []
                    rest = tokens[i:]
                    elevation = 0
                    for j,t in enumerate(rest):
                        if token_type in ["COMMENT", "WHITESPACE"]:
                            continue
                        if t[0] == "OPERATOR" and t[1] == "<":
                            elevation += 1
                        if t[0] == "OPERATOR" and t[1] == ">":
                            elevation -= 1
                            # this indicates the last ) at the end of the return type
                            if elevation < 0:
                                i = j+i
                                break
                        returntype_tokens.append(t)
                    _, dtype.returnType = self.parse_datatype(returntype_tokens)
                    functionidx += 1
                elif functionidx == 2:
                    print(i)
                    if token_type != "GROUP_START":
                        raise ParserException(
                            "Invalid Syntax: Expected '(' after '>'", pos
                        )
                    functionidx += 1
                elif functionidx == 3:
                    print("barney from black mesa", i)
                    # Parameters
                    parametertokens: List[List[Tuple[str, str, int]]] = []
                    rest = tokens[i:]
                    elevation = 0
                    currentparam: List[Tuple[str, str, int]] = []
                    for j,t in enumerate(rest):
                        if token_type in ["COMMENT", "WHITESPACE"]:
                            continue
                        if t[0] == "GROUP_START":
                            elevation += 1
                        if t[0] == "GROUP_END":
                            elevation -= 1
                            if elevation < 0:
                                finalidx = j+i
                                finalpos = t[2]
                                break
                        if t[0] == "LIST_SEPERATOR" and elevation == 0:
                            if len(currentparam) == 0:
                                raise ParserException("Invalid Syntax: Unexpected ','",t[2])
                            parametertokens.append(currentparam.copy())
                            currentparam = []
                            continue
                        currentparam.append(t)
                    parametertokens.append(currentparam)
                    print("PARAMETERS")
                    print(parametertokens)
                    params = []
                    for param in parametertokens:
                        _, pdtype = self.parse_datatype(param)
                        finalpos = _
                        params.append(pdtype)
                    dtype.parameters = params
                    break
            
            i = finalidx-1
            while (i+1) < len(tokens):
                print(i)
                i+=1
                token_type = tokens[i][0]
                data = tokens[i][1]
                pos = tokens[i][2]

                if token_type == "OPERATOR":
                    if data == "&":
                        dtype = ReferenceDType(dtype)
                        finalpos = i
                        continue
                    else:
                        # HACK: Find an edge case
                        raise ParserException("Invalid Syntax: Unexpected operator", pos)

                if token_type == "ARRAY_START":
                    if (len(tokens) == i + 1) or tokens[i + 1][0] != "ARRAY_END":
                        raise ParserException(
                            "Invalid Syntax: Expected ']' after '['", pos
                        )
                    dtype = ArrayDType(dtype)
                    
                if token_type == "ARRAY_END":
                    print(token_type,data,pos)
                    finalpos = pos
                    print(finalpos)
        print(finalpos,isfunction)

        return finalpos,dtype

    def parse_datatype(
        self, tokens: List[Tuple[str,str,int]]
    ) -> Tuple[int,DataType] | None:
        dtype: DataType

        isfunction = False
        
        finalpos = 0
        finalidx = 0

        for i, token in enumerate(tokens):
            token_type, data, pos = token
