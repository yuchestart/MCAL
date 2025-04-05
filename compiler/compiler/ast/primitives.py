from compiler.ast.base import BaseNode
from compiler.ast.values import Value,DataType
from dataclasses import dataclass

from typing import *

@dataclass
class Number(Value):
    value:float
    type:DataType
    signed:bool = True

@dataclass
class String(Value):
    value:str
    substitutions:Dict[Tuple[int,int],BaseNode]

@dataclass
class Boolean(Value):
    value:bool

@dataclass
class Array(Value):
    values:List[BaseNode]

@dataclass
class Compound(Value):
    value:Dict[str,BaseNode]

@dataclass
class Coordinate(Value):
    x:Value
    y:Value
    z:Value
    type:str #world local relative
    