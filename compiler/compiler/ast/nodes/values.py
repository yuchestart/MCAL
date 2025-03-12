
from typing import *
from dataclasses import dataclass

from compiler.ast.nodes.base import BaseNode

class Identifier(BaseNode):
    ident:str

class Symbol(BaseNode):
    pass

class DataType(BaseNode):
    pass

class Value(BaseNode):
    dataType:DataType

class Expression(BaseNode):
    pass
