from nodes import *
from tokeniser import Token

cnr = 'L '
up = '^'

def getTree(deep, node):
    deep += '  '
    if isinstance(node, ProgramModuleNode):
        return deep + cnr + 'Program name: '+getTree(deep, node.name) + getTree(deep, node.params) + getTree(deep, node.body)
    elif isinstance(node, ProgramParamsNode):
        if len(node.params.idents) > 0 :
            return '\n' + deep + cnr + 'params:' + '\n' + getTree(deep, node.params) + ';'
        else:
            return ''
    elif isinstance(node, IdentListNode):
        return deep + cnr + 'idents: ' + ', '.join(map(lambda n: getTree(deep, n), node.idents))
    elif isinstance(node, BlockNode):
        return  '\n' + deep + cnr + 'block: ' +  getTree(deep, node.declarations) + '\n' + deep + '  ' + cnr + 'sequence statement:' + getTree(deep, node.statementSequence)
    elif isinstance(node, EmptyNode):
        return '\n' + deep + '  ' + cnr + node.value
    elif isinstance(node, DeclarationsNode):
        if len(node.constants.constants) > 0 or len(node.variables.variables) > 0 or len(node.subprogs.declList) > 0:
            return '\n' + deep + cnr + 'declarations: ' + getTree(deep + up, node.constants) + getTree(deep + up, node.variables) + getTree(deep + up, node.subprogs)
        else:
           return ''
    elif isinstance(node, ConstDefBlockNode):
        if len(node.constants)>0:
            return '\n' + deep[0:-1] + cnr + 'constants: \n' + '\n'.join(map(lambda n: getTree(deep[0:-1] + up, n), node.constants))
        else:
            return ''
    elif isinstance(node, ConstDefNode):
        return deep[0:-1] + cnr + 'name: ' + getTree(deep,node.ident) + ' ' + getTree(deep, node.value) +';'
    elif isinstance(node, ConstExpressionNode):
        return ' ' + node.op + 'value: ' + str(node.value.value)
    elif isinstance(node, VarDeclBlockNode):
        if len(node.variables)>0:
            return '\n' + deep[0:-1] + cnr + 'variables:' + ''.join(map(lambda n: getTree(deep[0:-1]+up, n), node.variables))
        else:
            return ''
    elif isinstance(node, VarDeclNode):
        return '\n' + deep[0:-1] + cnr + 'names: ' + ', '.join(map(lambda n: getTree(deep, n), node.idents.idents)) + getTree(deep, node.idsType)
    elif isinstance(node, IdentListNode):
        return  ', '.join(map(lambda n: getTree(deep, n), node.idents))
    elif isinstance(node, SubprogDeclListNode):
        if len(node.declList) > 0:
            return  '\n'+ deep + cnr + 'subprog declaration:' + '\n'.join(map(lambda n: getTree(deep, n), node.declList))
        else:
            return ''
    elif isinstance(node, FunctionDeclNode):
        return '\n' + deep + cnr + 'function declaration: \n' + getTree(deep, node.heading) + '\n' + deep + '  ' + cnr + getTree(deep, node.functType) + getTree(deep, node.block)
    elif isinstance(node, ProcedureDeclNode):
        return '\n' + deep + cnr + 'procedure declaration: \n' + getTree(deep, node.heading) + getTree(deep, node.block)
    elif isinstance(node, FunctionHeadingNode):
        return deep+ cnr + 'funtion heading: \n' + deep + up +'  ' + cnr + 'name: '+ getTree(deep+ up, node.name) + getTree(deep+up, node.params)
    elif isinstance(node, ProcedureHeadingNode):
        return deep+ cnr + 'procedure heading: \n' + deep + up + '  ' + cnr + 'name: '+ getTree(deep + up, node.name) + ';' + getTree(deep + up, node.params)
    elif isinstance(node, FormalParametersNode):
        if len(node.params[0].ids.idents) > 0:
            return '\n' + deep+ cnr + 'parameters: \n'+''.join(map(lambda n: getTree(deep, n), node.params))
        else: 
            return ''
    elif isinstance(node, OneFormalParamNode):
        return getTree(deep[0:-2], node.ids) + getTree(deep, node.idsType)
    elif isinstance(node, TypeNode):
        return 'type: ' + node.name + ';'
    elif isinstance(node, StatementSequenceNode):
        return ''.join(map(lambda n: getTree(deep, n), node.statements))
    elif isinstance(node, AssignmentNode):
        return '\n' + deep + cnr + 'assigment:' + getTree(deep, node.varName) + '\n' + deep + '  ' + cnr + 'expression: ' + getTree(deep + '  ', node.expression)
    elif isinstance(node, DesignatorNode):
        return '\n' + deep+ cnr + 'variable name: ' + node.name + ';' + getTree(deep, node.stuff)
    elif isinstance(node, (LiteralIntNode, LiteralFloatNode, StringNode, NilNode)):
        return '\n' + deep[0:-2] + cnr + 'value: ' + str(node.value) + ';'
    elif isinstance(node, ExpListNode):
        return  ''.join(map(lambda n: getTree(deep, n), node.expressions))
    elif isinstance(node, IdentificatorNode):
        return node.name
    elif isinstance(node, FunctionCallNode):
        return '\n' + deep + cnr + 'function call:' + '\n' + deep + '  ' + cnr + 'name: ' + getTree(deep, node.name) + getTree(deep + '  ', node.params) 
    elif isinstance(node, ProcedureCallNode):
        return '\n' + deep+ cnr + 'procedure call:' + '\n' + deep + '  ' + cnr + 'name: ' + getTree(deep, node.name) + getTree(deep, node.params) 
    elif isinstance(node, ActualParametersNode):
        return '\n' + deep[0:-2] + cnr + 'actual parameters: ' + getTree(deep[0:-2], node.params)
    elif isinstance(node, UnaryOpNode):
        return '\n' + deep+ cnr +'op:'+ node.op + getTree(deep + '  ', node.left)
    elif isinstance(node, BinaryOpNode):
        return '\n' + deep + cnr + 'op: ' +node.op + getTree(deep + up, node.left) + getTree(deep, node.right)
    elif isinstance(node, CompleteIfNode):
        deep += up
        return '\n' + deep[0:-1] + cnr + 'if:' + '\n' + deep+'  '+ cnr + 'condition:'+ getTree(deep + '  ' + up, node.condition) + '\n' + deep + '  ' + cnr + 'true statement:' + getTree(deep + '  ' + up, node.trueStatement) + '\n' + (deep+'  ')+ cnr + 'false statement:' + getTree(deep + '  ' + up, node.falseStatement)
    elif isinstance(node, IncompleteIfNode):
        deep += up
        return '\n' + deep[0:-1] + cnr + 'if:' + '\n' + deep+ '  ' + cnr + 'condition:'+ getTree(deep + '  ' + up, node.condition) + '\n' + deep + '  ' + cnr + 'true statement:' + getTree(deep + '  ' + up, node.trueStatement)
    elif isinstance(node, WhileNode):
        deep += up
        return '\n' + deep[0:-1] + cnr +'while:'+ '\n' + deep + '  ' + cnr + 'condition:'+ getTree(deep + '  ' + up, node.condition) + '\n' + deep + '  ' + cnr + 'true statement:' + getTree(deep + '  ' + up, node.trueStatement)
    elif isinstance(node, RepeatNode):
        deep += up
        return '\n' + deep[0:-1] + cnr +'repeat:'+ getTree(deep, node.statements) +'\n' + deep + '  ' + cnr + 'condition:'+ getTree(deep + '  ' + up, node.condition)
    elif isinstance(node, ForNode):
        deep += up
        return '\n' + deep[0:-1] + cnr + 'for:'+ '\n' + deep + '  ' + cnr + 'variable: ' + getTree(deep, node.variable) + ';\n' + deep + '  ' + cnr +'initial value: ' + getTree(deep + '  ', node.initialValue) + '\n' + deep + '  ' + cnr + 'final value: ' + getTree(deep + '  ', node.finalValue) + getTree(deep, node.way) + '\n' + deep + '  ' + cnr + 'statements: ' + getTree(deep + '  ', node.statements)
    elif isinstance(node, WichWayNode):
        return '\n' + deep + cnr + 'direction: '+ node.direction + ';'
    elif isinstance(node, OutStatmentNode):
        return '\n' + deep+ cnr + node.name + getTree(deep, node.expList)
    elif isinstance(node, ArrayTypeNode):
        return '\n' + deep+ cnr + 'array:' + getTree(deep, node.artype) + ''.join(map(lambda n: getTree(deep, n), node.subranges))
    elif isinstance(node, SubrangeNode):
        return '\n' + deep + cnr + 'left:'+getTree(deep, node.left) + '\n' + deep + cnr + 'right:'+getTree(deep, node.right)
    elif isinstance(node, InStatmentNode):
        return '\n' + deep + cnr + node.name + getTree(deep[0:-2], node.designatorList)
    elif isinstance(node, DesignatorListNode):
        return ''.join(map(lambda n: getTree(deep, n), node.designators))
    elif type(node) == OneFormalParamNode:
        return deep + cnr + node.idsType + "\n" + "\n".join(map(lambda n: getTree(deep, n), node.ids))
    elif isinstance(node, list):
        if len(node) == 0:
            return ''
    elif isinstance(node, Token):
        return node.value
    else:
        return deep + str(node)