from parser import Parser
from nodes.util import PrimitiveDataType

def run_test() -> bool:
    parser = Parser("int yousuck;")
    print(parser.parse_dec_variable())

    return True