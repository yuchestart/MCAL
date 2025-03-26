from compiler.parser.base import ParserBase, ParserException
from compiler.parser.expressions.datatypes import ParserDataTypes
from compiler.parser.expressions import ParserExpressions

from compiler.ast.values import Identifier, Value, DataType
from compiler.ast.base import BaseNode
from compiler.ast.variables import (
    VariableDeclaration,
    ScoreboardDeclaration,
)

from compiler.tokenizer.interfaces import Token

import pcre2
from typing import *


class ParserDeclarationVariables(ParserExpressions,ParserDataTypes,ParserBase):
    def parse_variable_declaration(
        self, statement: str
    ) -> Tuple[bool, VariableDeclaration]:
        # [datatype] [[name] = [value]]

        retval = VariableDeclaration(None, [])
        matches = list(map(lambda x: Token(x.lastgroup,x.group(0),x.start()),pcre2.finditer(self.regex, statement)))
        
        index,dtype = self.parse_datatype(matches)
        print(dtype,index)

        retval.dataType = dtype
    

        mode = "identifier" #"identifier" "equal" "value" "seperator"
        name:str = None
        value:Value = None
        i = index
        while (i+1)<len(matches):
            i+=1
            token = matches[i]
            print(token)
            if self.ignore(token):
                continue
            if token.type == "STATEMENT_SEPERATOR":
                if len(retval.declarations) == 0:
                    raise ParserException("Invalid Syntax: Unexpected ';'.",token.position)
                break

            if mode == "identifier":
                if token.type != "IDENTIFIER":
                    raise ParserException(f"Invalid Syntax: Unexpected '{token.data}'.",token.position)
                if name is not None:
                    raise ParserException(f"Invalid Syntax: Unexpected identifier.",token.position)
                name = token.data
                value = None
                mode = "equal"
            elif mode == "equal":
                if token.type == "LIST_SEPERATOR":
                    mode = "identifier"
                    retval.declarations.append((name,value))
                    continue
                if token.type != "OPERATOR" or token.data != "=":
                    raise ParserException(f"Invalid Syntax: Unexpected '{token.data}'.",token.position)
                mode = "value"
            elif mode == "value":
                idx,v = self.parse_expression(matches[i:])
                print(matches[i:],v)
                value = v
                i = idx+i
                mode = "seperator"
                retval.declarations.append((name,value))
            elif mode == "seperator":
                if token.type != "LIST_SEPERATOR":
                    raise ParserException(f"Invalid Syntax: Unexpected '{token.data}'.",token.position)
                
                retval.declarations.append((name,value))
                mode = "identifier"
        return True,retval
    

    def parse_scoreboard_declaration(
        self, statement: str
    ) -> Tuple[bool, ScoreboardDeclaration]:
        pass

