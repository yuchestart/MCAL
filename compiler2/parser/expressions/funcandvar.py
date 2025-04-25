from parser.base import ParserBase
from typing import *

from nodes.ast.expressions.primitives import AnonymousFunction
from nodes.ast.util import FunctionDataType

class FuncAndVarExpressions(ParserBase):
    def parse_anonymous_function(self):

        dtype:FunctionDataType = self.parse_datatype()
        if type(dtype) != FunctionDataType:
            return
        scope = self.parse_scope()

        return AnonymousFunction(dtype.return_type,dtype.parameters,scope)
