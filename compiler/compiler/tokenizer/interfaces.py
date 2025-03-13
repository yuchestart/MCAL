from dataclasses import dataclass

@dataclass
class Token():
    type:str
    data:str
    position:int