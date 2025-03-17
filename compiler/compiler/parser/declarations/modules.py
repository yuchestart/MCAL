from compiler.parser.base import ParserBase, ParserException

from compiler.ast.base import BaseNode
from compiler.ast.modules import (
    ModuleDeclarationNode,
    ModuleImportNode,
    NamespaceDeclarationNode,
)

import pcre2
from typing import *


class ParserModules(ParserBase):

    def parse_module_declaration(
        self, statement: str
    ) -> Tuple[bool, ModuleDeclarationNode]:

        retval = ModuleDeclarationNode([], [], [])
        matches = pcre2.finditer(self.regex, statement)

        i = 0
        for match in matches:
            token_type = match.lastgroup
            data = match.group(0)

            if token_type == "WHITESPACE" or token_type == "COMMENT":
                continue

            if i == 0 and token_type != "KEYWORD":
                # module imports always start with keywords
                return False, None

            if i == 0 and data == "extern":
                retval.extern = True
                i += 1
                continue

            if retval.extern and i == 1 or not retval.extern and i == 0:
                if token_type != "KEYWORD" or data != "module":
                    if retval.extern:
                        raise ParserException(
                            "Invalid Syntax: Expected 'module'", match.start()
                        )
                    else:
                        # no extern or module, so probably just another statement
                        return False, None
                i += 1
                continue

            # an identifier must follow module
            if token_type != "IDENTIFIER" and i <= 2:
                raise ParserException(
                    "Invalid Syntax: Expected identifier", match.start()
                )

            # : is not allowed in module names. Use `namespace` for submodules.
            colon = pcre2.match(":",data)
            if colon:
                raise ParserException(
                    "Invalid Syntax: Invalid identifier format", colon.start()
                )

            # set module name
            retval.ident = data
            break

        return True, retval

    def parse_namespace_declaration(self, statement:str) -> Tuple[bool,NamespaceDeclarationNode]:
        retval = NamespaceDeclarationNode("")
        matches = pcre2.finditer(self.regex,statement)

        i = 0
        for match in matches:
            match_type = match.lastgroup
            data = match.group(0)

            if match_type == "WHITESPACE" or match_type == "COMMENT":
                continue
            
            #namespace keyword
            if i == 0:
                if match_type != "KEYWORD" or data != "namespace":
                    return False,None
                i+=1
                continue

            if i == 1 and match_type != "IDENTIFIER":
                raise ParserException("Invalid Syntax: Expected namespace",match.start())

            retval.ident = data
        
        return True,retval

    def parse_module_import(self, statement: str) -> Tuple[bool, ModuleImportNode]:
        retval = ModuleImportNode([], "")
        matches = pcre2.finditer(self.regex, statement)

        i = 0
        for match in matches:
            match_type = match.lastgroup
            data = match.group(0)

            if match_type == "WHITESPACE" or match_type == "COMMENT":
                continue
            
            #import keyword
            if i == 0:
                if match_type != "KEYWORD" or data != "import":
                    return False,None
                i+=1
                continue

            #identifier after import
            if i == 1 and match_type != "IDENTIFIER":
                raise ParserException("Invalid Syntax: Expected identifier",match.start())

            retval.ident = data

        return True, retval