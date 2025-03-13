from compiler.parser.base import ParserBase, ParserException
from compiler.parser.datatypes import ParserDataTypes

from compiler.astnodes.values import Identifier, Value, DataType
from compiler.astnodes.base import BaseNode

from compiler.astnodes.variables import (
    VariableDeclaration,
    ScoreboardDeclaration,
)

import pcre2
from typing import *


class ParserVariables(ParserDataTypes,ParserBase):

    def parse_variable_declaration(
        self, statement: str
    ) -> Tuple[bool, VariableDeclaration]:
        # [datatype] [[name] = [value]]

        retval = VariableDeclaration(None, [])
        matches = list(map(lambda x: (x.lastgroup,x.group(0),x.start()),pcre2.finditer(self.regex, statement)))
        
        dtype = self.parse_datatype(matches)
        

        # SINGLE, NO VALUE
        # look at last identifier, and then parse the datatype to the left

        # SINGLE, WITH VALUE
        # look at the 

        # SPECIAL CASE WITH FUNCTION

    


    def parse_scoreboard_declaration(
        self, statement: str
    ) -> Tuple[bool, ScoreboardDeclaration]:
        pass

    def parse_cast_expression(self, statement: str) -> BaseNode:
        pass
