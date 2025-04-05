from compiler.parser.base import ParserBase, ParserException


from compiler.tokenizer.interfaces import Token

from compiler.ast.base import BaseNode

import pcre2
from typing import *


class ParserExpressionsBase(ParserBase):
    def parse_expression_statement(
        self, tokens: List[Token]
    ) -> Tuple[int, BaseNode | None]:
        pass

    def parse_expression_atom(self, tokens: List[Token]) -> Tuple[int, BaseNode | None]:
        pass

    def parse_expression(self, tokens: List[Token]) -> Tuple[int, BaseNode]:
        pass
