import sys
from tokeniser import Token, Tokeniser
from parser1 import Parser

path = sys.argv[2]
f = open(path, 'r', encoding = 'utf-8')
lex = Tokeniser(''.join(f.readlines()))

if sys.argv[1] == 'T':
    while True:
        t = lex.Next()
        if t.tokenType == Token.tokenTypeEOF:
            break
        print(t)
elif sys.argv[1] == 'P':
    p = Parser(lex)
    print(p.ParseExpr())