from dataclasses import dataclass
from typing import *

@dataclass
class ClassDeclaration:
    declarations:list[dict[str,Any|str|bool]]
    extends:list[Any]
    name:str

@dataclass
class StructDeclaration:
    declarations:list[Any]
    name:str