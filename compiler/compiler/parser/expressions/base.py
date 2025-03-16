from compiler.parser.base import ParserBase, ParserException

from compiler.tokenizer.interfaces import Token
from compiler.astnodes.base import BaseNode

import pcre2
from typing import *


class ParserExpressionsBase(ParserBase):
    # This method is gonna get overridden by ParserExpressions
    # I'm doing this soley so I can use mixins
    # Also I tested that it actually works trust me please
    def parse_expression(self,token:List[Token])->Tuple[int,BaseNode]:
        pass
