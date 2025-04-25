from dataclasses import dataclass
from typing import *
from nodes.ast.util import CodeBlock

@dataclass
class Number:
    value:float
    signed:bool
    type:str

@dataclass
class String:
    value:str
    substitutes:dict[tuple[int,int],Any]

@dataclass
class Boolean:
    value:bool

@dataclass
class Null:
    pass

@dataclass
class UUID:
    value:list[int]|str|None
    selector:str|None

@dataclass
class Coordinate:
    type:str
    x:Any
    y:Any
    z:Any

@dataclass
class Compound:
    data:dict[str,Any]

@dataclass
class Array:
    elements:list[Any]

@dataclass
class AnonymousFunction:
    returntype:Any
    parameters:list[tuple[str,Any]]
    code:CodeBlock