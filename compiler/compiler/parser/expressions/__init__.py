from compiler.parser.base import ParserBase, ParserException
from compiler.parser.expressions.base import ParserExpressionsBase

from compiler.parser.expressions.datatypes import ParserDataTypes
from compiler.parser.expressions.literals import ParserExpressionsLiterals
from compiler.parser.expressions.calculations import ParserExpressionsCalculations

from compiler.ast.values import Expression

from compiler.tokenizer.interfaces import Token

import sys
sys.setrecursionlimit(50)

import pcre2
from typing import *


class ParserExpressions(
    ParserExpressionsLiterals,
    ParserExpressionsCalculations,
    ParserDataTypes,
    ParserExpressionsBase,
    ParserBase
):
    def parse_expression_atom(self, tokens:List[Token]) -> Tuple[int, Expression]:
        parsers = [
            self.parse_expression_group,
            self.parse_expression_literal,
            self.parse_expression_assignment,
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

    # Here it gets overridden
    def parse_expression(self, tokens:List[Token]) -> Tuple[int, Expression]:
        parsers = [
            self.parse_expression_opchain,
            self.parse_expression_atom
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

