from compiler.parser.expressions.base import ParserExpressionsBase
from compiler.parser.base import ParserException

from compiler.tokenizer.interfaces import Token
from compiler.ast.values import Identifier
from compiler.ast.minecraft import CommandCall, MinecraftObjInstantiation

import pcre2

class ParserExpressionsMinecraft(ParserExpressionsBase):
    def parse_command_call(self, tokens: list[Token]) -> tuple[int, CommandCall]:
        ret = None
        idx = 0
        ident = None
        did = False
        arguments = ""

        state = "ident"
        i = -1
        while i < len(tokens) - 1:
            i+=1
            token = tokens[i]

            if self.ignore(token):
                continue

            if state == "ident":
                if token.type != "IDENTIFIER":
                    break
                ident = token.data
                state = "command"
            elif state == "command":
                if token.type != "OPERATOR" or token.data != "!":
                    break
                did = True
                state = "openbracket"
            elif state == "openbracket":
                if token.type != "GROUP_START":
                    raise ParserException("Expected '(' after '!'.",token.position)
                state = "arguments"
            elif state == "arguments":
                elevation = 0
                for j,t in enumerate(tokens[i:]):
                    if t.type == "GROUP_START":
                        elevation += 1
                    elif t.type == "GROUP_END":
                        elevation -= 1
                        if elevation < 0:
                            i=j
                            break
                    arguments += t.data
                idx = i
                break

        if did:
            sub_str = {}
            final = ""
            state = "none"
            escape = False
            i = -1
            while i < len(arguments) - 1:
                i += 1
                char = arguments[i]
                if escape:
                    final += char
                    escape = False
                    continue
                if char == "\\":
                    escape = True
                    continue
                if char == "$":
                    state = "check"
                elif state == "check":
                    if char != "{":
                        state = "none"
                    state = "substituting"
                    final = final[:-1]
                    continue
                elif state == "substituting":
                    rest = map(
                        lambda x: Token(x.lastgroup, x.group(0), x.start),
                        pcre2.finditer(self.regex, arguments[i:])
                    )
                    cursub = []
                    elevation = 0
                    nexti = 0
                    for j, t in enumerate(rest):
                        if self.ignore(t):
                            continue
                        if t.type == "BLOCK_STARFT":
                            elevation += 1
                        if t.type == "BLOCK_END":
                            elevation -= 1
                            if elevation < 0:
                                nexti = j
                                break
                        cursub.append(t)
                    sub_str[(i,i+nexti)] = cursub
                    i += nexti
                    state = "none"
                final += char

            sub_ast = {}
            for k in sub_str:
                sub_ast[k] = self.parse_expression(sub_str[k])[1]

            ret = CommandCall(ident,final,sub_ast)

        return idx, ret


    def parse_mcobject_instantiation(
        self, tokens: list[Token]
    ) -> tuple[int, MinecraftObjInstantiation]:
        pass

    