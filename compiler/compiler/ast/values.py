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
class Block(BaseNode):
    statements: List[BaseNode]

@dataclass
class Identifier(BaseNode):
    ident:str

@dataclass
class Access(BaseNode):
    root:Identifier
    key:Identifier

@dataclass
class OperatorChain(Expression):
    operations:List[str]
    operands:List[Expression]

@dataclass
class UnaryOperation(Expression):
    operator:str
    operand:Expression
    after:bool