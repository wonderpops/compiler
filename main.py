import sys
from tokeniser import Token, Tokeniser
from parser1 import Parser
from nodes import *

path = sys.argv[2]
f = open(path, 'r', encoding = 'utf-8')
lex = Tokeniser(''.join(f.readlines()))
cnr = '└ '

#def __str__
def getTree(deep, node):
    deep += 1
    if type(node) == UnaryOpNode:
        return '  '*deep + cnr + node.op + "\n" + getTree(deep, node.left)
    elif type(node) == BinaryOpNode:
        return '  '*deep + cnr + node.op + "\n" + getTree(deep, node.left) + "\n" + getTree(deep, node.right)
    elif type(node) == FunctionCallNode:
        return '  '*deep + cnr + node.name + "\n" + "\n".join(map(lambda n: getTree(deep, n), node.parameters))
    elif type(node) == DesignatorNode:
        return '  '*deep + cnr + node.name
    else:
        return '  '*deep + cnr + str(node.value)


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
    #x = getTree(0, p.ParseExpr())
    x = p.ParseStatement()
    print(x)