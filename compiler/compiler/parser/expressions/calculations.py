from compiler.parser.expressions.base import ParserExpressionsBase

from compiler.tokenizer.interfaces import Token


from typing import *
import re
import pcre2


class ParserExpressionsCalculations(ParserExpressionsBase):
    def parse_expression_opchain(self,tokens:List[Token])->Tuple[int,]:
        pass

    def parse_expression_group(self,tokens:List[Token]):
        pass

    def parse_expression_assignment(self,tokens:List[Token]):
        pass
