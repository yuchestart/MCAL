from typing import *
from compiler.astnodes.values import Symbol, DataType, Value
from compiler.astnodes.base import BaseNode


class FunctionDeclaration(Symbol):
    name: str
    entrypoint: str | None = None
    parameters: List[Tuple[DataType, str, Value | None]]
    code: List[BaseNode]


class AnonymousFunction(Value):
    returnType: DataType
    parameters: List[Tuple[DataType, str, Value | None]]
    code: List[BaseNode]
