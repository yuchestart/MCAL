
from dataclasses import dataclass
from compiler.ast.values import DataType
from typing import *

@dataclass
class MinecraftObjDType(DataType):
    name:str

@dataclass
class EntityDType(MinecraftObjDType):
    name: str

@dataclass
class BlockDType(MinecraftObjDType):
    name: str

@dataclass
class StorageDType(MinecraftObjDType):
    name: str