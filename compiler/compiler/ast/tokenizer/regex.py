from compiler.ast.tokenizer.keywords import KEYWORDS
from compiler.ast.tokenizer.primitives import PRIMITIVES
from compiler.ast.tokenizer.operators import OPERATORS
from typing import *

TOKEN_PRIORITY =\
"""STRING
COMMENT
STATEMENT_SEPERATOR
LIST_SEPERATOR
KEYWORD
PRIMITIVE
NUMBER
COORDINATE
IDENTIFIER
COMMAND_CALL
FUNCTION_CALL
TYPEGROUP
OPERATOR
BLOCK_START
BLOCK_END
GROUP_START
GROUP_END
ARRAY_START
ARRAY_END
WHITESPACE
UNKNOWN""".split("\n")

TOKEN_REGEXES = {
    #Strings
    "STRING" : r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'',

    #Punctuation
    "STATEMENT_SEPERATOR" : r';',
    "LIST_SEPERATOR" : r',',
    "OPERATOR" : OPERATORS,
    "BLOCK_START" : r"\{",
    "BLOCK_END": r"\}",
    "GROUP_START" : r"\(",
    "GROUP_END" : r"\)",
    "ARRAY_START" : r"\[",
    "ARRAY_END" : r"\]",

    #Keywords
    "KEYWORD" : r"\b(?:" + r"|".join(KEYWORDS) + r")\b",
    "PRIMITIVE" : r"\b(?:" + r"|".join(PRIMITIVES) + r")\b",
    
    #Literals
    "NUMBER" : r'-?\d+(\.\d+)?(?:[b|s|S|l|L|f|F|d|D]?)\b',
    "COORDINATE" : r"(?:(?:~|\^)?-?\d*\.?\d+|(?:~|\^)) (?:(?:~|\^)?-?\d*\.?\d+|(?:~|\^)) (?:(?:~|\^)?-?\d*\.?\d+|(?:~|\^))",
    "NBT_OBJECT" : r"(\{(?:(?>[^{}\"'\/]+)|(?>\"(?:(?>[^\\\"]+)|\\.)*\")|(?>'(?:(?>[^\\']+)|\\.)*')|(?>\/\/.*\n)|(?>\/\*.*?\*\/)|(?-1))*\})",
    
    #Identifiers
    "IDENTIFIER" : r"\b[a-zA-Z_](?:[a-zA-Z_0-9.]|::|:)*\b",
    "FUNCTION_CALL" : r"(?=(?:\b[a-zA-Z_](?:[a-zA-Z_0-9.]|::|:)*\b)\s*\((?:.|\s)*\))",


    #Commands
    "COMMAND_CALL" : r"!(?:\(.*\))",

    #Misc.
    "COMMENT" : r'(?:\/\/.*$)|(?:\/\*(?:.|\n)*\*\/)',
    "TYPEGROUP" : r"(?<!\\)\<(?:[^\<\>\n]|\\[\<\>])*(?<!\\)\>",
    "SUBSTITUTION" : r"(?<!\\)\$\{(?:[^\{\}\n]|\\[\{\}])*(?<!\\)\}",

    "WHITESPACE" : r"\s",
    "UNKNOWN" : r"."
}

def subset_regex(priorities:List[str]) -> str:
    final = []
    for type in TOKEN_PRIORITY:
        if type not in priorities:
            continue
        final.append(f"(?P<{type}>(?:{TOKEN_REGEXES[type]}))")
    return r"|".join(final)