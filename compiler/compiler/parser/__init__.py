from compiler.util import COMPILERVARS, printError
from compiler.parser.base import ParserBase,ParserException
from compiler.tokenizer.regex import subset_regex, TOKEN_PRIORITY

from compiler.astnodes.base import BaseNode

from compiler.parser.modules import ParserModules
from compiler.parser.variables import ParserVariables
from compiler.parser.datatypes import ParserDataTypes

import pcre2
from typing import *


class Parser(ParserModules, ParserVariables, ParserDataTypes, ParserBase):
    def __init__(self):
        self.code = COMPILERVARS.code
        self.regex = subset_regex(TOKEN_PRIORITY)

    def parse_file(self) -> List[BaseNode] | None:
        # Parse toplevel statements
        statements = []
        matches = pcre2.finditer(self.regex, self.code)
        lastposition = 0

        elevation = 0

        for match in matches:
            match_type = match.lastgroup
            #  print(match.lastgroup)
            # Toplevel statement
            if match_type == "STATEMENT_SEPERATOR" and elevation == 0:
                statements.append(self.code[lastposition : match.start() + 1])
                lastposition = match.start() + 1
            elif match_type == "BLOCK_START":
                elevation += 1
            elif match_type == "BLOCK_END":
                elevation -= 1
                if elevation == 0:
                    statements.append(self.code[lastposition : match.start() + 1])
                    lastposition = match.start() + 1
                    
        # If a { wasn't closed
        if elevation != 0:
            # TODO: Provide error message
            print("A bracket wasn't closed")
            return

        # Parse each statement
        ast: List[BaseNode] = []
        for statement in statements:
            try:
                succeeded, node = self.parse_toplevel(statement)
                if succeeded:
                    ast.append(node)
            except ParserException as e:
                e.print()
        return ast

    def parse_toplevel(self, statement: str) -> Tuple[bool, BaseNode | None]:
        toplevelparsers = [
            self.parse_module_declaration,
            self.parse_module_import,
            self.parse_namespace_declaration
        ]
        parsedNode: BaseNode | None = None
        succeeded: bool = False

        for parser in toplevelparsers:
            succeeded, parsedNode = parser(statement)
            if succeeded:
                break
            break

        return succeeded, parsedNode
