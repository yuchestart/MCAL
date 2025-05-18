from parser.base import ParserBase
from nodes.ast.statements.mc import Execute

class MinecraftStatements(ParserBase):
    def parse_dec_command(self):
        pass

    def parse_execute(self):
        if not self.token_peek()["type"] == "execute":
            return
        return Execute(self.token_next()["value"],self.parse_scope())