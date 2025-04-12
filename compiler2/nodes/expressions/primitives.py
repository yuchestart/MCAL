from dataclasses import dataclass
from typing import *

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
    value:list[int]

@dataclass
class Coordinate:
    type:str
    x:Any
    y:Any
    z:Any