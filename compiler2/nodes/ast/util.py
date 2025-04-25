from dataclasses import dataclass
from typing import *

@dataclass
class ArrayAccess:
    to:Any

@dataclass
class Identifier:
    ident:str

@dataclass
class Name:
    name:str

@dataclass
class PrimitiveDataType:
    dtype:str

@dataclass
class IntegerDataType:
    dtype:str
    signed:bool

@dataclass
class FunctionDataType:
    return_type:Any
    parameters:list[Any]

@dataclass
class EntityDataType:
    name:str

@dataclass
class BlockDataType:
    name:str

@dataclass
class DataType:
    extern:Name|None
    const:bool
    base:Any
    chain:list[str]

@dataclass
class AccessChain:
    of:Any
    what:list[tuple[str,Identifier|Any]]

@dataclass
class New:
    of:Any

CodeBlock = List[Any]