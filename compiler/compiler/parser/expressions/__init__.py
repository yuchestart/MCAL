from compiler.parser.base import ParserBase, ParserException
from compiler.parser.expressions.base import ParserExpressionsBase

from compiler.parser.expressions.datatypes import ParserDataTypes
from compiler.parser.expressions.literals import ParserExpressionsLiterals
from compiler.parser.expressions.calculations import ParserExpressionsCalculations
from compiler.parser.expressions.minecraft import ParserExpressionsMinecraft
from compiler.parser.expressions.functions import ParserExpressionsFunctions

from compiler.ast.values import Expression, Identifier

from compiler.tokenizer.interfaces import Token

import sys
sys.setrecursionlimit(50)

import pcre2
from typing import *


class ParserExpressions(
    ParserExpressionsMinecraft,
    ParserExpressionsFunctions,
    ParserExpressionsLiterals,
    ParserExpressionsCalculations,
    ParserDataTypes,
    ParserExpressionsBase,
    ParserBase
):
    def parse_expression_identifier(self, tokens:List[Token]) -> Tuple[int, Identifier | None]:
        ret = None
        idx = 0
        for i,token in enumerate(tokens):
            if self.ignore(token):
                continue
            if token.type == "IDENTIFIER":
                ret = Identifier(token.data)
                idx = i
                break
        return idx,ret
    
    def parse_expression_atom(self, tokens:List[Token]) -> Tuple[int, Expression | None]:
        parsers = [
            self.parse_expression_group,
            self.parse_expression_literal,
            self.parse_expression_assignment,
            self.parse_expression_unaryop,
            self.parse_expression_statement,
            self.parse_expression_identifier,
        ]
        ret: Expression | None = None
        finalpos:int = 0
        for parser in parsers:
            pos, node = parser(tokens)
            if node is not None:
                ret = node
                finalpos = pos
                break
        
        return finalpos,ret

    def parse_expression_statement(self,tokens:List[Token]) -> Tuple[int, Expression | None]:
        parsers = [
            self.parse_function_call,
            self.parse_command_call,
            #self.parse_anonymous_function,
            #self.parse_mcobject_instantiation,
        ]
        ret: Expression | None = None
        finalpos: int = 0
        for parser in parsers:
            pos, node = parser(tokens)
            if node is not None:
                ret = node
                finalpos = pos
                break
        return finalpos, ret

    # Here it gets overridden
    def parse_expression(self, tokens:List[Token]) -> Tuple[int, Expression | None]:
        parsers = [
            self.parse_expression_opchain,
            self.parse_expression_atom
        ]
        ret: Expression | None = None
        finalpos:int = 0
        for parser in parsers:
            print(parser)
            pos, node = parser(tokens)
            if node is not None:
                ret = node
                finalpos = pos
                break
        
        return finalpos,ret

