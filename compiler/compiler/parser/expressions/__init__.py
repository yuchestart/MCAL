from compiler.parser.base import ParserBase, ParserException
from compiler.parser.expressions.base import ParserExpressionsBase

from compiler.parser.expressions.datatypes import ParserDataTypes
from compiler.parser.expressions.literals import ParserExpressionsLiterals

from compiler.ast.base import BaseNode

from compiler.tokenizer.interfaces import Token

import pcre2
from typing import *


class ParserExpressions(
    ParserExpressionsLiterals,
    ParserDataTypes,
    ParserExpressionsBase,
    ParserBase
):

    # Here it gets overridden
    def parse_expression(self, tokens:List[Token]) -> Tuple[int, BaseNode]:
        expressionparsers = [
            self.parse_literal
        ]
        ret: BaseNode | None = None
        finalpos:int = 0
        for parser in expressionparsers:
            pos, node = parser(tokens)
            if node is not None:
                ret = node
                finalpos = pos
                break
        
        return finalpos,ret

