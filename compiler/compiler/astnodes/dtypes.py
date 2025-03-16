from dataclasses import dataclass
from compiler.astnodes.values import DataType
from typing import *


class IntDType(DataType):
    pass


class FloatDType(DataType):
    pass


class DoubleDType(DataType):
    pass


class ShortDType(DataType):
    pass


class LongDType(DataType):
    pass


class ByteDType(DataType):
    pass


class BoolDType(DataType):
    pass


class StringDType(DataType):
    pass


class UuidDType(DataType):
    pass


class CompoundDType(DataType):
    pass


class Void(DataType):
    pass


@dataclass
class ArrayDType(DataType):
    of: DataType


@dataclass
class ReferenceDType(DataType):
    to: DataType


@dataclass
class NullableDType(DataType):
    of: DataType


@dataclass
class FunctionDType(DataType):
    returnType: DataType
    parameters: List[DataType]
