from typing import *
from compiler.astnodes.values import DataType, Expression, Value, Symbol, Identifier
from compiler.astnodes.base import BaseNode
from dataclasses import dataclass


@dataclass
class VariableDeclaration(Symbol):
    dataType: DataType
    declarations: List[Tuple[str, Value]]


@dataclass
class ScoreboardDeclaration(Symbol):
    criteria: str
    declarations: List[Tuple[str, Value]]


@dataclass
class AssignmentExpression(Expression):
    ident: Identifier
    value: Value
    type: str = "="
