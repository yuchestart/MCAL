from parser import Parser
from nodes.ast.util import PrimitiveDataType

def run_test() -> bool:
    parser = Parser(
"""
import { Parent1 } from "Parent1.mcal";
import { Parent2 } from "Parent2.mcal";
import "game.mcal" as game;

using namespace game;

void myFunction(){
    int[] list = [1,2,3];
}

class MyObject : Parent1, Parent2{
    static const string ENUMTHING = "VALUE";
    public static void main(string[] args){ 
        System.out.println("Java mimick haha");
    } 
    private int add(int a, int b){
        return a + b;
    }
    protected void process(){
        minecraft:tellraw!(@a "I'm processing");
    }
    static SomeRandomObject create(){
        return new SomeRandomObject;
    }
    int five(){
        return 5;
    }
}
""")
    print(parser.parse_program())

    return True