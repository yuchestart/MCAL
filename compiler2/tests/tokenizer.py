from parser.tokenizer import Tokenizer
import re

def run_test() -> bool:
    tokenizer = Tokenizer()
    tokenizer.code = "!{tellraw @a \'1+1 is ${1+1}\'}"
    tokenizer.pos = 0
    tokenizer.init_tokenizer()
    print(tokenizer.PUNCTUATION)
    print(re.match(r"\s",tokenizer.input_peek()))
    i = 0
    while tokenizer.token_peek() is not None and i < 10:
        i+=1
        print(tokenizer.next_token())

    return True