import sys
from tokeniser import Token, Tokeniser
from parser1 import Parser
from nodes import *


path = sys.argv[2]
f = open(path, 'r', encoding = 'utf-8')
lex = Tokeniser(''.join(f.readlines()))
cnr = '└ '

def getTree(deep, node):
    #deep +=1
    if isinstance(node, (UnaryOpNode, NotNode)):
        return '  '*deep + str(node) + getTree(deep, node.left)
    elif isinstance(node, BinaryOpNode):
        return str(node) #+ getTree(deep, node.left) + "\n" + getTree(deep, node.right)
    elif isinstance(node, (FunctionCallNode, ProcedureCallNode)):
        return '  '*deep + cnr + node.name + "\n" + "\n".join(map(lambda n: getTree(deep, n), node.parameters.expList.expressions))
    elif isinstance(node, (DesignatorNode, StringNode, NilNode, IOStatmentNode,
                           TypeNode, IdentificatorNode, LiteralFloatNode, WichWayNode, EmptyNode)):
        return '  '*deep + str(node)
    elif type(node) == InStatmentNode:
        return '  '*deep + cnr + node.name + "\n" + "\n".join(map(lambda n: getTree(deep, n), node.designatorList.designators))
    elif type(node) == FunctionHeadingNode or type(node) == ProcedureHeadingNode:
        return '  '*deep + cnr + node.name + "\n" + "\n".join(map(lambda n: getTree(deep, n), node.params.params))
    elif type(node) == OneFormalParamNode:
        return '  '*deep + cnr + node.idsType + "\n" + "\n".join(map(lambda n: getTree(deep, n), node.ids))
    else:
        return '  '*deep + str(node)

def tree(node):
    return str(node)


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
    print(p.ParseProgramModule())
