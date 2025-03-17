
from typing import *
from dataclasses import dataclass

from compiler.ast.base import BaseNode


class Symbol(BaseNode):
    pass

class DataType(BaseNode):
    pass

class Expression(BaseNode):
    pass

class Value(Expression):
    pass

@dataclass
class Identifier(BaseNode):
    ident:str

class OperationChain(Expression):
    operations:List[str]
    operands:List[Expression]