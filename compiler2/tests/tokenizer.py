from parser.tokenizer import Tokenizer
import re

def run_test() -> bool:
    tokenizer = Tokenizer()
    tokenizer.code = """
dec_command<minecraft:teleport>!{
  void|<selector[single]>
  void|<selector[multi]> <selector[single]>
  void|<coordinate>
  void|<selector[multi]> <coordinate>
  void|<selector[multi]> <coordinate> <float> <float>
  void|<selector[multi]> <coordinate> facing <coordinate>
  void|<selector[multi]> <coordinate> facing entity <selector[single]>
}

"""
    tokenizer.pos = 0
    tokenizer.init_tokenizer("code")
    print(tokenizer.PUNCTUATION)
    print(re.match(r"\s",tokenizer.input_peek()))
    i = 0
    while tokenizer.token_peek() is not None and i < 10:
        i+=1
        print(tokenizer.token_next())

    return True