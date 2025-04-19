from parser import Parser
from nodes.util import PrimitiveDataType

def run_test() -> bool:
    parser = Parser("int a(int b = 5, int c){};")
    print(parser.parse_toplevel())

    return True