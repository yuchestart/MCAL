import sys
import os
from tokenize import tokenize

print("Minecraft Command Compiler")

path = sys.argv[1]

print(path)

with open(path) as file:
    print("\n".join(map(str,tokenize(file.read()))))