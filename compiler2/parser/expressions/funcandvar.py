from parser.base import ParserBase
from typing import *

from nodes.expressions.primitives import AnonymousFunction
from nodes.util import FunctionDataType

class FuncAndVarExpressions(ParserBase):
    def parse_anonymous_function(self):
        dtype:FunctionDataType = self.parse_datatype()
        scope = self.parse_scope()

        return AnonymousFunction(dtype.return_type,dtype.parameters,scope)
