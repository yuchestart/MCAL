from dataclasses import dataclass
from typing import *

@dataclass
class NewStack:
    pass

@dataclass
class DisposeStack:
    pass

@dataclass
class StoreStack:
    name:str
    value:Any

@dataclass
class GetStack:
    name:str

@dataclass
class StoreHeap:
    value:Any

@dataclass
class GetHeap:
    pointer:Any

@dataclass
class StoreGlobal:
    name:str
    value:Any

@dataclass
class StoreHeap:
    name:str
    value:Any

@dataclass
class Delete:
    pointer:Any