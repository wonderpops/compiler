import os
from tokeniser import Token, Tokeniser

directory = 'tests'
files = os.listdir(directory)

for f in files:
    path = 'tests/' + f
    op = open(path, 'r')
    lex = Tokeniser(''.join(op.readlines()))
    print('--------------'+f+'--------------')
    print('|row|-|column|-|type|-|value|--|src|')
    while True:
        t = lex.Next()
        if t.tokenType == Token.tokenTypeEOF:
            break
        print(t)
    print('_____________________________________')