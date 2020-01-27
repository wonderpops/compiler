from tokeniser import Token, Tokeniser
from parser1 import Parser
from symbolTable import ScopedSymbolTable, VarSymbol, ConstSymbol
from nodes import *

class SemanticAnalyser:
    def __init__(self, parser: Parser):
        self.parser = parser
        self.curScope: ScopedSymbolTable = None

    def analyse(self):
        t = self.parser.ParseProgramModule()
        self.treeSearch(t)
    
    def treeSearch(self, node):
        if isinstance(node,ProgramModuleNode):
            self.programModule(node)
        elif isinstance(node, IdentificatorNode):
            self.ident(node, None)
        elif isinstance(node, ProgramParamsNode):
            pass
        elif isinstance(node, BlockNode):
            self.block(node)
        elif isinstance(node, ConstDefBlockNode):
            self.constBlock(node) 
        elif isinstance(node, ConstDefNode):
            self.const(node)
        elif isinstance(node, DeclarationsNode):
            self.decl(node)
        elif isinstance(node, VarDeclBlockNode):
            self.varBlock(node)   
        elif isinstance(node, VarDeclNode):
            self.var(node)
        elif isinstance(node, SubprogDeclListNode):
            self.subprogDeclList(node)   
        elif isinstance(node, FunctionDeclNode):
            self.funcDecl(node)
        elif isinstance(node, OneFormalParamNode):
            self.oneFormalParam(node) 
        elif isinstance(node, StatementSequenceNode):
            self.statementSequence(node)  
        elif isinstance(node, AssignmentNode):
            self.assignment(node) 
        elif isinstance(node, BinaryOpNode):
            return self.binaryOp(node)
        elif isinstance(node, LiteralIntNode):
            return self.int_(node)
        elif isinstance(node, LiteralFloatNode):
            return self.float_(node)
        elif isinstance(node, StringNode):
            return self.str_(node)
        elif isinstance(node, DesignatorNode):
            return self.design(node)
        elif isinstance(node, FunctionCallNode):
            return self.funcCall(node)
        elif isinstance(node, ProcedureDeclNode):
            return self.procDecl(node)
        elif isinstance(node, ProcedureCallNode):
            return self.procCall(node)
        elif isinstance(node, IncompleteIfNode):
            self.incompIf(node)
        elif isinstance(node, CompleteIfNode):
            self.compIf(node)
        elif isinstance(node, WhileNode):
            self.while_(node)
        elif isinstance(node, RepeatNode):
            self.repeat_(node)
        elif isinstance(node, ForNode):
            self.for_(node)
        elif isinstance(node, InStatmentNode):
            self.in_(node)
        elif isinstance(node, OutStatmentNode):
            self.out_(node)
        elif isinstance(node, NotNode):
            return self.not_(node)
        elif isinstance(node, UnaryOpNode):
            return self.unaryOp(node)
        elif isinstance(node, ArrayTypeNode):
            return self.arrayType(node)
    
    def programModule(self, node):
        scope = ScopedSymbolTable('main')
        self.curScope = scope
        self.treeSearch(node.name)
        self.treeSearch(node.params)
        self.treeSearch(node.body)
    
    #No type identifiers (procedures, program name etc)
    def ident(self, node, type_):
        identName = node.name
        identSymbol = VarSymbol(identName, type_)        
        if self.curScope.search(identName, True):#true or false?
            raise Exception('ERROR: Ident "' + identName + '" already exist')
        self.curScope.insert(identSymbol)
        print(self.curScope.name, identSymbol)

    def block(self, node):
        self.treeSearch(node.declarations)
        self.treeSearch(node.statementSequence)
        

    def decl(self, node):
        self.treeSearch(node.constants)
        self.treeSearch(node.variables)
        self.treeSearch(node.subprogs)
    
    def statementSequence(self, node):
        for s in node.statements:
            self.treeSearch(s)

    def assignment(self, node):
        varName = node.varName.name
        if not self.curScope.search(varName, False):
            raise Exception('ERROR: Ident "' + varName + '" does not exist')
        exprType = self.treeSearch(node.expression)
        varType = self.curScope.search(varName).varType
        if varType == 'real' and exprType in ['real', 'integer']:
            pass
        elif varType == 'string' and exprType == 'string':
            pass
        elif varType == 'integer' and exprType == 'integer':
            pass
        else:
            raise Exception('ERROR: Can not assign type "' + exprType + '" to "' + varType + '"')

    def constBlock(self, node):
        for c in node.constants:
            self.treeSearch(c)
    
    def const(self, node):
        self.treeSearch(node.ident)
        constValue = node.value.value
        constName = self.curScope.search(node.ident.name, True).name
        constSymbol = ConstSymbol(constName, constValue)
        self.curScope.insert(constSymbol)
        print(constSymbol)

    def varBlock(self, node):
        for v in node.variables:
            self.treeSearch(v)

    def var(self, node):
        varType = node
        if isinstance(varType.idsType, ArrayTypeNode):
            arType = self.arrayType(varType.idsType)
            for i in varType.idents.idents:
                self.ident(i, arType)
        else:
            for i in node.idents.idents:
                self.ident(i, varType.idsType.name)
    
    def subprogDeclList(self, node):
        for d in node.declList:
            self.treeSearch(d)
    
    def funcDecl(self, node):
        funcName = node.heading.name
        funcType = node.functType.name
        self.ident(funcName, funcType)
        
        scope = ScopedSymbolTable(funcName.name)
        scope.outScope = self.curScope
        self.curScope = scope

        for p in node.heading.params.params:
            self.treeSearch(p)
        self.treeSearch(node.block)
        self.curScope = self.curScope.outScope
    
    def procDecl(self, node):
        procName = node.heading.name
        self.ident(procName, None)
        
        scope = ScopedSymbolTable(procName.name)
        scope.outScope = self.curScope
        self.curScope = scope

        for p in node.heading.params.params:
            self.treeSearch(p)
        self.treeSearch(node.block)
        self.curScope = self.curScope.outScope

    def oneFormalParam(self, node):
        idsType = node.idsType
        for i in node.ids.idents:
            self.ident(i, idsType.name)

    def binaryOp(self, node):
        leftType = self.treeSearch(node.left)
        rightType = self.treeSearch(node.right)
        #print(leftType)
        #print(rightType)
        if leftType == 'integer':
            if rightType == 'integer':
                return 'integer'
            elif rightType == 'real':
                return 'real'
            else:
                raise Exception('ERROR: missmatch types')
        elif leftType == 'real':
            if rightType == 'string':
                raise Exception('ERROR: missmatch types')
            else:
                return 'real'
        elif leftType == 'string':
            if rightType != 'string':
               raise Exception('ERROR: missmatch types') 
            else:
                return 'string'

    def int_(self, node):
        return 'integer'

    def float_(self, node):
        return 'real'

    def str_(self, node):
        return 'string'

    def arrayType(self, node):
        for s in node.subranges:
            left = self.treeSearch(s.left)
            right = self.treeSearch(s.right)
            if left != 'integer' or right != 'integer':
                raise Exception('ERROR: Incorrect array range')
        return node.artype.name
    
    def design(self, node):
        d = self.curScope.search(node.name)
        if d:
            return d.varType
        else:
            raise Exception('ERROR: Ident "' + node.name + '" does not exist')
        return 'string'

    def funcCall(self, node):
        d = self.curScope.search(node.name.name)
        if d:
            return d.varType
        else:
            raise Exception('ERROR: Ident "' + node.name + '" does not exist')
        return 'string'

    def procCall(self, node):
        d = self.curScope.search(node.name.name)
        if d:
            pass
        else:
            raise Exception('ERROR: Ident "' + node.name.name + '" does not exist')
        return 'string'
    
    def incompIf(self, node):
        self.treeSearch(node.condition)
        self.treeSearch(node.trueStatement)

    def compIf(self, node):
        self.treeSearch(node.condition)
        self.treeSearch(node.trueStatement)
        self.treeSearch(node.falseStatement)
    
    def while_(self, node):
        self.treeSearch(node.condition)
        self.treeSearch(node.trueStatement)
    
    def repeat_(self, node):
        self.treeSearch(node.statements)
        self.treeSearch(node.condition)

    def for_(self, node):
        d = self.curScope.search(node.variable.name)
        if d:
            if d.varType != 'integer':
                raise Exception('ERROR: Ident "' + d.name + '" must be integer type')                
        else:
            raise Exception('ERROR: Ident "' + node.variable.name + '" does not exist')

        start = self.treeSearch(node.initialValue)
        final = self.treeSearch(node.finalValue)
        if start!= 'integer':
            raise Exception('ERROR: Ident "' + start.name + '" must be integer type')

        if final != 'integer':
            raise Exception('ERROR: Ident "' + final.name + '" must be integer type')
        self.treeSearch(node.statements)

    def in_(self, node):
        if node.designatorList:
            for d in node.designatorList.designators:            
                self.treeSearch(d)
    
    def out_(self, node):
        if node.expList:
            for d in node.expList.expressions:            
                self.treeSearch(d)

    def not_(self, node):
        d = self.treeSearch(node.left)
        return d

    def unaryOp(self, node):
        d = self.treeSearch(node.left)
        if d != 'string':
            return d
        else:
            raise Exception('ERROR: Can not use unary operator with string type')
        
    



        
