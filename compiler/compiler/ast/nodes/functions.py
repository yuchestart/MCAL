from typing import *
from compiler.ast.nodes.values import Symbol,DataType,Value
from compiler.ast.nodes.base import BaseNode

class FunctionDataType(DataType):
    returnType:DataType


class FunctionSymbolDeclaration(Symbol):
    name:str
    entrypoint:str|None = None
    parameters:List[Tuple[DataType,str,Value|None]]
    code:List[BaseNode]

class AnonymousFunction(Value):
    returnType:DataType
    parameters:List[Tuple[DataType,str,Value|None]]
    code:List[BaseNode]