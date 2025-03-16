from compiler.parser.base import ParserBase, ParserException
from compiler.parser.expressions.base import ParserExpressionsBase

from compiler.parser.expressions.datatypes import ParserDataTypes
from compiler.parser.expressions.literals import ParserExpressionsLiterals


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
    def parse_expression(self, token) -> Tuple[int, List[Token]]:
        pass
