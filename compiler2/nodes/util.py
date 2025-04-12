from dataclasses import dataclass
from typing import *

@dataclass
class ArrayAccess:
    to:Any

@dataclass
class Identifier:
    chain:list[str|ArrayAccess]

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
class ModifiedDataType:
    dtype:Any
    chain:list[str]

@dataclass
class CodeBlock:
    statements:list[any]