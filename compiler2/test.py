import tests.tokenizer as tokenizer
import tests.parser as parser

# if tokenizer.run_test():
#     print("SUCCESS: Tokenizer")
# else:
#     print("FAILURE: Tokenizer")

if parser.run_test():
   print("SUCCESS: Parser")
else:
   print("FAILURE: Parser")