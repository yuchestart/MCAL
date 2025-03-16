import sys
import os
from compiler.parser import Parser
from compiler.util import COMPILERVARS
if len(sys.argv) == 1:
    print("MCALC - Minceraft Command Abstraction Language Compiler")
    print("To get help, use:")
    print("mcalc --help")
    exit()
if '--help' in sys.argv:
    with open("help/help.txt") as f:
        print(f.read())
    exit()


pathes = filter(lambda x: not x.startswith("--"), sys.argv[1:])
options = filter(lambda x: x.startswith("--") or x.startswith("-"), sys.argv[1:])

for path in pathes:

    with open(path) as file:
        code = file.read()
        COMPILERVARS.setCode(code,path)
        p = Parser()
        ast = p.parse_file()