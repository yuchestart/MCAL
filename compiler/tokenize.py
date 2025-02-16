import re
"""
AST:
{
"type":"type"
"data":""
}

"""

KEYWORD_LIST =\
"""dec
dec_nbt
dec_scoreboard
set
loop
if
elif
else
execute
function
return
module
import
extern
export
struct
entrypoint
namespace""".split("\n")

TOKEN_SPEC = [
    ("STRING",r'"(?:\\.|[^"\\])*"'),
    ("COMMENT",r'(?://.*$)|(?:/\*(?:.|\n)*\*/)'),
    ("STATEMENT_SEPERATOR",r';'),
    ("KEYWORD",r"\b(?:" + r"|".join(KEYWORD_LIST) + r")\b"),
    ("NUMBER",r'\b\d+(\.\d+)?([i|f|d|b|s]?)\b'),
    ("IDENTIFIER",r"\b[a-zA-Z_][a-zA-Z_0-9]*\b"),
    ("BLOCK_START",r"\{"),
    ("BLOCK_END",r"\}"),
    ("COMMAND_CALL",r"!(?=\()"),
    ("GROUP_START",r"\("),
    ("GROUP_END",r"\)"),
    ("TYPEGROUP",r"<(?:[^>\\])*>")
]


def tokenize(code:str):
    tokens = []
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name,pattern in TOKEN_SPEC)
    for match in re.finditer(token_regex,code):
        kind = match.lastgroup
        value = match.group(kind)
        if kind == "COMMENT":
            continue
        tokens.append({"type":kind,"data":value})
    return tokens