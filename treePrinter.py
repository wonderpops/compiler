from nodes import *
from tokeniser import Token

cnr = '└ '

def getTree(deep, node):
    deep +=1
    if isinstance(node, ProgramModuleNode):
        return '  '* deep + cnr + 'Program name: '+getTree(deep, node.name) + getTree(deep, node.params) + getTree(deep, node.body)
    elif isinstance(node, ProgramParamsNode):
        if len(node.params) > 0 :
            return '\n' + '  '* deep + cnr + 'params:' + '\n' + getTree(deep, node.params) + ';'
        else:
            return ''
    elif isinstance(node, IdentListNode):
        return '  '* deep + cnr + 'idents: ' + ', '.join(map(lambda n: getTree(deep, n), node.idents))
    elif isinstance(node, BlockNode):
        return  '\n' + '  '*deep + cnr + 'block: ' +  getTree(deep, node.declarations) + '\n' + '  ' * (deep + 1) + cnr + 'sequence statement:' + getTree(deep, node.statementSequence)
    elif isinstance(node, EmptyNode):
        return '\n' + '  '*(deep+1) + cnr + node.value
    elif isinstance(node, DeclarationsNode):
        if len(node.constants.constants) > 0 or len(node.variables.variables) > 0 or len(node.subprogs.declList) > 0:
            return '\n' + '  '*deep + cnr + 'declarations: ' + getTree(deep, node.constants) + getTree(deep, node.variables) + getTree(deep, node.subprogs)
        else:
            return ''
    elif isinstance(node, ConstDefBlockNode):
        if len(node.constants)>0:
            return '\n' + '  '* deep + cnr + 'constants: \n' + '\n'.join(map(lambda n: getTree(deep, n), node.constants))
        else:
            return ''
    elif isinstance(node, ConstDefNode):
        return '  '* deep + cnr + 'name: ' + getTree(deep,node.ident) + ' ' + getTree(deep, node.value) +';'
    elif isinstance(node, ConstExpressionNode):
        return ' ' + node.op + 'value: ' + str(node.value.value)
    elif isinstance(node, VarDeclBlockNode):
        if len(node.variables)>0:
            return '\n' + '  '* deep + cnr + 'variables:' + ''.join(map(lambda n: getTree(deep, n), node.variables))
        else:
            return ''
    elif isinstance(node, VarDeclNode):
        return '\n' + '  '* deep + cnr + 'names: ' + ', '.join(map(lambda n: getTree(deep, n), node.idents.idents)) + getTree(deep, node.idsType)
    elif isinstance(node, IdentListNode):
        return  ', '.join(map(lambda n: getTree(deep, n), node.idents))
    elif isinstance(node, SubprogDeclListNode):
        if len(node.declList) > 0:
            return  '\n' + '  '* deep + cnr + 'subprog declaration:' + '\n'.join(map(lambda n: getTree(deep, n), node.declList))
        else:
            return ''
    elif isinstance(node, FunctionDeclNode):
        return '\n' + '  '* deep + cnr + 'function declaration: \n' + getTree(deep, node.heading) + '\n' + '  '* (deep+1) + cnr + getTree(deep, node.functType) +';\n' + getTree(deep, node.block)
    elif isinstance(node, ProcedureDeclNode):
        return '\n' + '  '* deep + cnr + 'procedure declaration: \n' + getTree(deep, node.heading) +'\n' + getTree(deep, node.block)
    elif isinstance(node, FunctionHeadingNode):
        return '  '*deep+ cnr + 'funtion heading: \n' + '  '*(deep+1) + cnr + 'name: '+ getTree(deep, node.name) + ';' + getTree(deep, node.params)
    elif isinstance(node, ProcedureHeadingNode):
        return '  '*deep+ cnr + 'procedure heading: \n' + '  '*(deep+1) + cnr + 'name: '+ getTree(deep, node.name) + ';' + getTree(deep, node.params)
    elif isinstance(node, FormalParametersNode):
        if len(node.params[0].ids.idents) > 0:
            return '\n' + '  '*deep+ cnr + 'parameters: \n'+'\n'.join(map(lambda n: getTree(deep, n), node.params))
        else: 
            return ''
    elif isinstance(node, OneFormalParamNode):
        return getTree(deep-1, node.ids) + getTree(deep, node.idsType) + ';'
    elif isinstance(node, TypeNode):
        return ' type: ' + node.name + ';'
    elif isinstance(node, StatementSequenceNode):
        return '\n'.join(map(lambda n: getTree(deep, n), node.statements))
    elif isinstance(node, AssignmentNode):
        return '\n' + '  ' * deep + cnr + 'assigment:' + getTree(deep, node.varName) + '\n' + '  '*(deep+1)+ cnr + 'expression: ' + getTree(deep +1, node.expression)
    elif isinstance(node, DesignatorNode):
        return '\n' + '  '*deep+ cnr + 'variable name: ' + node.name + ';' + getTree(deep, node.stuff)
    elif isinstance(node, (LiteralIntNode, LiteralFloatNode, StringNode, NilNode)):
        return '\n' + '  '*deep+ cnr + 'value: ' + str(node.value) + ';'
    elif isinstance(node, ExpListNode):
        return  ''.join(map(lambda n: getTree(deep, n), node.expressions))
    elif isinstance(node, IdentificatorNode):
        return node.name
    elif isinstance(node, FunctionCallNode):
        return '\n' + '  '*deep+ cnr + 'function call:' + '\n' + '  '* (deep + 1) + cnr + 'name: ' + getTree(deep, node.name) + getTree(deep+1, node.params) 
    elif isinstance(node, ProcedureCallNode):
        return '\n' + '  '*deep+ cnr + 'procedure call:' + '\n' + '  '* (deep + 1) + cnr + 'name: ' + getTree(deep, node.name) + getTree(deep+1, node.params) 
    elif isinstance(node, ActualParametersNode):
        return '\n' + '  '*deep+ cnr + 'actual parameters: ' + getTree(deep-1, node.params)
    elif isinstance(node, UnaryOpNode):
        return '\n' + '  '*deep+ cnr +'op:'+ node.op + getTree(deep, node.left)
    elif isinstance(node, BinaryOpNode):
        return '\n' + '  '*deep+ cnr + 'op: ' +node.op + getTree(deep, node.left) + getTree(deep, node.right)
    elif isinstance(node, CompleteIfNode):
        return '\n' + '  '*deep+ cnr + 'if:' + '\n' + '  '*(deep+1)+ cnr + 'condition:'+ getTree(deep + 1, node.condition) + '\n' + '  '*(deep+1)+ cnr + 'true statement:' + getTree(deep + 1, node.trueStatement) + '\n' + '  '*(deep+1)+ cnr + 'false statement:' + getTree(deep + 1, node.falseStatement)
    elif isinstance(node, IncompleteIfNode):
        return '\n' + '  '*deep+ cnr + 'if:' + '\n' + '  '*(deep+1)+ cnr + 'condition:'+ getTree(deep + 1, node.condition) + '\n' + '  '*(deep+1)+ cnr + 'true statement:' + getTree(deep + 1, node.trueStatement)
    elif isinstance(node, WhileNode):
        return '\n' + '  '*deep+ cnr +'while:'+ '\n' + '  '*(deep+1)+ cnr + 'condition:'+ getTree(deep + 1, node.condition) + '\n' + '  '*(deep+1)+ cnr + 'true statement:' + getTree(deep, node.trueStatement)
    elif isinstance(node, RepeatNode):
        return '\n' + '  '*deep+ cnr +'repeat:'+ getTree(deep, node.statements) +'\n' + '  '*(deep+1)+ cnr + 'condition:'+ getTree(deep + 1, node.condition)
    elif isinstance(node, ForNode):
        return '\n' + '  '*deep+ cnr +'for:'+ '\n' + '  '*(deep+1)+ cnr +'variable: ' + getTree(deep, node.variable) + ';\n' + '  '*(deep+1)+ cnr +'initial value: ' + getTree(deep+1, node.initialValue) + '\n' + '  '*(deep+1)+ cnr +'final value: ' + getTree(deep+1, node.finalValue) + getTree(deep, node.way) + '\n' + '  '*(deep+1)+ cnr +'statements: ' + getTree(deep+1, node.statements)
    elif isinstance(node, WichWayNode):
        return '\n' + '  '*deep+ cnr +'direction: '+ node.direction + ';'
    elif isinstance(node, OutStatmentNode):
        return '\n' + '  '*deep+ cnr + node.name + getTree(deep-1, node.expList)
    elif isinstance(node, ArrayTypeNode):
        return '\n' + '  '*deep+ cnr + 'array:' + getTree(deep, node.artype) + ''.join(map(lambda n: getTree(deep, n), node.subranges))
    elif isinstance(node, SubrangeNode):
        return '\n' + '  '*(deep)+ cnr + 'left:'+getTree(deep, node.left) + '\n' + '  '*(deep)+ cnr + 'right:'+getTree(deep, node.right)
    elif isinstance(node, InStatmentNode):
        return '\n' + '  '*deep+ cnr + node.name + getTree(deep-1, node.designatorList)
    elif isinstance(node, DesignatorListNode):
        return ''.join(map(lambda n: getTree(deep, n), node.designators))
    elif type(node) == OneFormalParamNode:
        return '  '*deep + cnr + node.idsType + "\n" + "\n".join(map(lambda n: getTree(deep, n), node.ids))
    elif isinstance(node, list):
        if len(node) == 0:
            return ''
    elif isinstance(node, Token):
        return node.value
    else:
        return '  '*deep + str(node)