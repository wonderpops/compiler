import sys
from tokeniser import Token, Tokeniser
from parser1 import Parser
from nodes import *
import networkx as nx  # importing networkx package
import matplotlib.pyplot as plt # importing matplotlib package and pyplot is for displaying the graph on canvas 

path = sys.argv[2]
f = open(path, 'r', encoding = 'utf-8')
lex = Tokeniser(''.join(f.readlines()))
cnr = '└ '

def getTree(deep, node):
    deep +=1
    if isinstance(node, ProgramModuleNode):
        return '  '* deep + cnr + '\n'.join(['Program name: '+getTree(deep, node.name), getTree(deep, node.params), getTree(deep, node.body)])
    elif isinstance(node, ProgramParamsNode):
        return '  '* deep + cnr + 'params:' + '\n' + getTree(deep, node.params) + ';'
    elif isinstance(node, IdentListNode):
        return '  '* deep + cnr + 'idents: ' + ', '.join(map(lambda n: getTree(deep, n), node.idents))
    elif isinstance(node, BlockNode):
        return '  '*deep + cnr + 'block: ' + '\n'+ getTree(deep, node.declarations) + getTree(deep, node.statementSequence) +';'
    elif isinstance(node, EmptyNode):
        return '  '*deep + cnr + 'empty'
    elif isinstance(node, DeclarationsNode):
        if len(node.constants.constants) > 0 or len(node.variables.idents) > 0 or len(node.subprogs.declList) > 0:
            return '  '*deep + cnr + 'declarations: \n' + getTree(deep, node.constants) + '\n' + getTree(deep, node.variables) + '\n' + getTree(deep, node.subprogs) + '\n'
        else:
            return ''
    elif isinstance(node, ConstDefBlockNode):
        if len(node.constants)>0:
            return '  '* deep + cnr + 'constants: \n' + '\n'.join(map(lambda n: getTree(deep, n), node.constants))
        else:
            return ''
    elif isinstance(node, ConstDefNode):
        return '  '* deep + cnr + 'name: ' + getTree(deep,node.ident) + ' ' + getTree(deep, node.value) +';'
    elif isinstance(node, ConstExpressionNode):
        return ' ' + node.op + 'value: ' + str(node.value.value)
    elif isinstance(node, VarDeclBlockNode):
        return '  '* deep + cnr + 'variables: \n' + '\n'.join(map(lambda n: getTree(deep, n), node.variables))
    elif isinstance(node, VarDeclNode):
        if not isinstance (node.idents, list):
            return '  '* deep + cnr + 'names: ' + ', '.join(map(lambda n: getTree(deep, n), node.idents.idents)) + getTree(deep, node.idsType) +';'
        else:
            return ''
    elif isinstance(node, IdentListNode):
        return  ', '.join(map(lambda n: getTree(deep, n), node.idents))
    elif isinstance(node, SubprogDeclListNode):
        return  '  '* deep + cnr + 'subprog declaration: \n' + '\n'.join(map(lambda n: getTree(deep, n), node.declList))
    elif isinstance(node, FunctionDeclNode):
        return '  '* deep + cnr + 'function declaration: \n' + getTree(deep, node.heading) + '\n' + '  '* (deep+1) + cnr + getTree(deep, node.functType) +';\n' + getTree(deep, node.block)
    elif isinstance(node, FunctionHeadingNode):
        return '  '*deep+ cnr + 'funtion heading: \n' + '  '*(deep+1) + cnr + 'name: '+ getTree(deep, node.name) + ';' + getTree(deep, node.params)
    elif isinstance(node, FormalParametersNode):
        if len(node.params[0].ids.idents) > 0:
            return '\n' + '  '*deep+ cnr + 'parameters: \n'+'\n'.join(map(lambda n: getTree(deep, n), node.params))
        else: 
            return ''
    elif isinstance(node, OneFormalParamNode):
        return getTree(deep-1, node.ids) + getTree(deep, node.idsType) + ';'
    elif isinstance(node, TypeNode):
        return ' type: ' + node.name
    elif isinstance(node, (UnaryOpNode, NotNode)):
        return '  '*deep + str(node) + getTree(deep, node.left)
    elif isinstance(node, BinaryOpNode):
        return str(node) #+ getTree(deep, node.left) + "\n" + getTree(deep, node.right)
    elif isinstance(node, (DesignatorNode, StringNode, NilNode, IOStatmentNode,
                           TypeNode, IdentificatorNode, LiteralFloatNode, WichWayNode)):
        return str(node.name)
    elif type(node) == InStatmentNode:
        return '  '*deep + cnr + node.name + "\n" + "\n".join(map(lambda n: getTree(deep, n), node.designatorList.designators))
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
    print(getTree(0, p.ParseProgramModule()))
