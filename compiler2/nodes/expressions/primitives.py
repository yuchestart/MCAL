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