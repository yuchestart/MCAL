from dataclasses import dataclass
from typing import *

@dataclass
class Loop:
    name:str
    impl:list[Any]
    next:list[Any]

@dataclass
class Continue:
    pass

@dataclass
class Break:
    pass

@dataclass
class If:
    condition:Any
    next:Any