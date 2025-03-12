from typing import *
from compiler.ast.nodes.values import DataType,Expression,Value
from compiler.ast.nodes.base import BaseNode

class Int(DataType):
    pass

class Float(DataType):
    pass

class Double(DataType):
    pass

class Short(DataType):
    pass

class Long(DataType):
    pass

class Byte(DataType):
    pass

class Bool(DataType):
    pass

class String(DataType):
    pass

class UUID(DataType):
    pass

class Compound(DataType):
    pass

class Array(DataType):
    of:DataType


class VariableDeclarationExpression(Expression):
    dataType:DataType
    name:str
    value:Value|None

class ScoreboardDeclaration(BaseNode):
    criteria:str
    name:str