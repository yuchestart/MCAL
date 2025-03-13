from compiler.util.vars import COMPILERVARS

def get_rowcol(pos:int):
    sp = COMPILERVARS.code[:pos+1].splitlines(keepends=True)
    row = len(sp)
    col = len(sp[-1])
    return row,col

def printError(descr:str,pos:int):
    lines = COMPILERVARS.code.splitlines()

    row,col = get_rowcol(pos)

    print("\x1b[33m"+str(row)+"\x1b[0m",lines[row-1],sep="|")
    print("\x1b[31m",end="")
    print(" "*(col+len(str(row)))+"^")
    print(f"ERROR @ {COMPILERVARS.path} {row}:{col}: {descr}")
    print("\x1b[0m",end="")

def printWarning(descr:str, pos:int):
    lines = COMPILERVARS.code.splitlines()

    row,col = get_rowcol(pos)

    print("\x1b[34m"+str(row)+"\x1b[0m",lines[row-1],sep="|")
    print("\x1b[33m",end="")
    print(" "*(col+len(str(row)))+"^")
    print(f"WARN @ {COMPILERVARS.path} {row}:{col}: {descr}")
    print("\x1b[0m",end="")