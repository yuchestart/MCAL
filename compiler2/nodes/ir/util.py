from dataclasses import dataclass
from typing import *

@dataclass
class Constant:
    value:str

@dataclass
class Command:
    value:str
    macros:list[Any]

@dataclass
class Execute:
    to:str
    impl:list[Any]

@dataclass
class CallFunc:
    name:str
    params:list[Any]

@dataclass
class GetParam:
    id:str

@dataclass
class DefineFunc:
    name:str
    impl:list[Any]
    extern:bool = False

@dataclass
class Operation:
    a:Any
    b:Any
    op:str