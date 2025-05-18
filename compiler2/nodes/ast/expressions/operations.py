from dataclasses import dataclass
from typing import *

@dataclass
class Opchain:
    operations:list[str]
    operands:list[Any]

@dataclass
class WrapperOpchain:
    prefix:list[str]
    postfix:list[str|tuple[Literal['cast'],Any]]
    operand:Any