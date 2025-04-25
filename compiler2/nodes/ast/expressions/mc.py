from dataclasses import dataclass
from typing import *

@dataclass
class CommandCall:
    name:str
    call:str
    sub:dict[int,Any]

@dataclass
class EntityInit:
    type:str
    target:Any|None

@dataclass
class BlockInit:
    type:str
    coordinate:Any

@dataclass
class StorageInit:
    name:Any
