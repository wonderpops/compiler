import sys
from tokeniser import Token, Tokeniser
from parser1 import Parser
from nodes import *
import treePrinter

path = sys.argv[2]
f = open(path, 'r', encoding = 'utf-8')
lex = Tokeniser(''.join(f.readlines()))

if sys.argv[1] == 'T':
    while True:
        try:
            t = lex.Next()
        except Exception as err:
            print(''.join(err.args))
        else:
            if t.tokenType == Token.tokenTypeEOF:
                break
            print(t)
elif sys.argv[1] == 'P':
    p = Parser(lex)
    #x = tree(p.ParseProgramModule())
    print(treePrinter.getTree(0, p.ParseProgramModule()))