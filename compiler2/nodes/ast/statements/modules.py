from dataclasses import dataclass
from typing import *
from nodes.ast.util import CodeBlock

@dataclass
class Import:
    source:str
    alias:str|None
    imports:Literal["*"]|list[Any]

@dataclass
class UsingNamespace:
    namespace:Any

@dataclass
class Namespace:
    namespace:Any
    symbols:CodeBlock|None

@dataclass
class Export:
    symbols:list[Any]|Literal["*"]