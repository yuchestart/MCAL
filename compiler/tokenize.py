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
    ("NUMBER",r'\b\d+(\.\d+)?([i|f|d|b|s]?)\b'),
    ("IDENTIFIER",r"\b[a-zA-Z_][a-zA-Z_0-9]*\b"),
    ("KEYWORD",r"\b(?:" + r"|".join(KEYWORD_LIST) + r")\b")
]


def tokenize(code:str):
    tokens = []
    token_regex = '|'.join(f'(?P<{name}{pattern}>)' for name,pattern in TOKEN_SPEC)
    

    return tokens