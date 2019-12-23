import sys
from tokeniser import Token, Tokeniser

path = sys.argv[1]
f = open(path, 'r', encoding = 'utf-8')
lex = Tokeniser(''.join(f.readlines()))

while True:
    t = lex.Next()
    if t.tokenType == Token.tokenTypeEOF:
        break
    print(t)