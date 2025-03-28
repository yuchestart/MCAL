
from dataclasses import dataclass
from compiler.ast.values import DataType,Expression,Value
from compiler.ast.primitives import String, Coordinate
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

@dataclass
class MinecraftObjInstantiation(Expression):
    pass

@dataclass
class EntityInstantiation(MinecraftObjInstantiation):
    entity: str
    uuid: Value

@dataclass
class BlockInstantiation(MinecraftObjInstantiation):
    block: str
    coordinate: Coordinate

@dataclass
class StorageInstantiation(MinecraftObjInstantiation):
    name: str

@dataclass
class CommandCall(Expression):
    command: str
    parameters: String