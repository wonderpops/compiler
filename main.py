import sys
from tokeniser import Token, Tokeniser
from parser1 import Parser
from nodes import *
from semanticAnalyser import SemanticAnalyser
import treePrinter

path = sys.argv[2]
f = open(path, 'r', encoding = 'utf-8')
ff = open(path, 'r', encoding = 'utf-8')
lex = Tokeniser(''.join(f.readlines()))
lexx = Tokeniser(''.join(ff.readlines()))

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
    pp = Parser(lexx)
    #x = tree(p.ParseProgramModule())
    semantic = SemanticAnalyser(p)
    semantic.analyse()
    print(treePrinter.getTree('', pp.ParseProgramModule()))
