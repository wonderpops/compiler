import sys
from tokeniser import Token, Tokeniser
from parser1 import Parser
from nodes import *

path = sys.argv[2]
f = open(path, 'r', encoding = 'utf-8')
lex = Tokeniser(''.join(f.readlines()))

#def __str__
def parseTree(deep, node):
    deep += 1
    if type(node) == UnaryOpNode:
        return '  '*deep + '└ ' + node.op + "\n" + parseTree(deep, node.left)
    elif type(node) == BinaryOpNode:
        return '  '*deep + '└ ' + node.op + "\n" + parseTree(deep, node.left) + "\n" + parseTree(deep, node.right)
    elif type(node) == FunctionCallNode:
        return '  '*deep + '└ ' + node.name + "\n" + "\n".join(map(lambda n: parseTree(deep, n), node.parameters))
    elif type(node) == VarNode:
        return '  '*deep + '└ ' + node.name
    else:
        return '  '*deep + '└ ' + str(node.value)
        #if type(node) == list :
        #    return ['  '*deep + '└ ' + str(node)]
        #else:
        #    return ['  '*deep + '└ ' + str(node.value)]

def printTree(node):
    if len(node)>1 and type(node) == tuple or type(node) == list:
        for f in node:
            printTree(f)
            if type(f) == str:
                print(''.join(f))


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
    x = parseTree(0, p.ParseExpr())
    print(x)