from nodes import *
from tokeniser import Token, Tokeniser

class Parser:
    def __init__(self, tokeniser):
        self.tokeniser = tokeniser
        self.cur = self.tokeniser.Next()

    def ParseIdentList(self):
        ids = []
        while (self.cur.tokenType == Token.tokenTypeIdentificator):
            ids.append(self.cur)
            self.cur = self.tokeniser.Next()
            if self.cur.value == ',':
                self.cur = self.tokeniser.Next()
        return ids

    def ParseBlock(self):
        pass

    def ParseDeclaration(self):
        pass

    def ParseConstantDefBlock(self):
        constants = []
        if self.cur.value == 'const' and self.cur.tokenType == Token.tokenTypeKeyWord:
            self.cur = self.tokeniser.Next()
            constants.append(self.ParseConstantDef())
            while self.cur.value == ';' and self.cur.tokenType == Token.tokenTypeSeparators:
                self.cur = self.tokeniser.Next()
                if self.cur.tokenType == Token.tokenTypeIdentificator:
                    constants.append(self.ParseConstantDef())
                else:
                    break
        return ConstDefBlockNode(constants)

    def ParseVariableDecBlock(self):
        pass

    def ParseConstantDef(self):
        ident = ''
        value = ''
        if self.cur.tokenType == Token.tokenTypeIdentificator:
            ident = self.cur.value
            self.cur = self.tokeniser.Next()
        if self.cur.value == '=' and self.cur.tokenType == Token.tokenTypeOperators:
            self.cur = self.tokeniser.Next()
            value = self.ParseConstExpression()
        return ConstDefNode(ident, value)

    def ParseVariableDec(self):
        ids = []
        if self.cur.tokenType == Token.tokenTypeIdentificator:
            ids = self.ParseIdentList()
        if self.cur.value == ':' and self.cur.tokenType == Token.tokenTypeSeparators:
            self.cur = self.tokeniser.Next()
        return #VarDecNode(ids,)

    def ParseConstExpression(self):
        op = ''
        value = ''
        if self.cur.value in ['+', '-']:
            op = self.cur.value
            self.cur = self.tokeniser.Next()
            value = self.ParseConstFactor()
        elif self.cur.tokenType == Token.tokenTypeString:
            value = self.cur.value
        elif self.cur.tokenType == Token.tokenTypeKeyWord and self.cur.value == 'nil':
            value = NilNode().value
        return ConstExpressionNode(op, value)


    def ParseConstFactor(self):
        t = self.cur
        if self.cur.tokenType == Token.tokenTypeIdentificator:
            self.cur = self.tokeniser.Next()
            return IdentificatorNode(t.name)
        elif self.cur.tokenType == Token.tokenTypeInt:
            self.cur = self.tokeniser.Next()
            return LiteralIntNode(t.value)
        elif self.cur.tokenType == Token.tokenTypeDouble:
            self.cur = self.tokeniser.Next()
            return LiteralFloatNode(t.value)
        elif self.cur.tokenType == Token.tokenTypeKeyWord and self.cur.value == 'nil':
            self.cur = self.tokeniser.Next()
            return NilNode()

    def ParseType(self):
        t = self.cur
        if self.cur.value == "integer":
            return TypeNode('integer')
        elif self.cur.value == "double": 
            return TypeNode('double')
        elif self.cur.value == "string":
            return TypeNode('string')
        elif self.cur.value == "array":
            return self.ParseArrayType()
        else:
            raise Exception("expected array type")

    def ParseArrayType(self):
        if self.cur.value == "array":
            self.cur = self.tokeniser.Next()
            if self.cur.value == "[":
                subranges = []
                self.cur = self.tokeniser.Next()
                while self.cur.value != "]":
                    if self.cur.value == ',':
                        self.cur = self.tokeniser.Next()
                    else:
                        subranges.append(self.ParseSubrange())
                if  self.cur.value == "of":
                    self.cur = self.tokeniser.Next()
                    return self.ParseType()
                else:
                    raise Exception("expected type of array")
                left = SubrangeArrayTypeNode(subranges)
                return left
            else:
                raise Exception("expected [") 
    
    def ParseSubrange(self):
        p = self.ParseConstFactor()
        self.cur = self.tokeniser.Next()
        if self.cur.value == "..":
            self.cur = self.tokeniser.Next()
            f = self.ParseConstFactor()
            return f
        return p

    def ParseStatementSequence(self):
        if self.cur.value == "begin":
            statements = []
            self.cur = self.tokeniser.Next()
            while self.cur.value != "end":
                if self.cur.value == ';':
                    self.cur = self.tokeniser.Next()
                else:
                    statements.append(self.ParseStatement())
            left = StatementSequenceNode(statements)
            return left
        
    def ParseStatement(self):
        t = self.cur
        if self.cur.tokenType == Token.tokenTypeKeyWord:
            if self.cur.value == "if":
                self.cur = self.tokeniser.Next()
                left = self.ParseIfStatement()
                #self.cur = self.tokeniser.Next()
                return left
            elif self.cur.value == "while":
                self.cur = self.tokeniser.Next()
                left = self.ParseWhileStatement()
                #self.cur = self.tokeniser.Next()
                return left
            elif self.cur.value == "begin":
                left = self.ParseStatementSequence()
                #self.cur = self.tokeniser.Next()
                return left
            elif self.cur.value == "repeat":
                self.cur = self.tokeniser.Next()
                left = self.ParseRepeatStatement()
                #self.cur = self.tokeniser.Next()
                return left
            elif self.cur.value == "for":
                self.cur = self.tokeniser.Next()
                left = self.ParseForStatement()
                return left
            elif self.cur.value in ['read', 'readln', 'write', 'writeln']:
                left = self.ParseIOStatement()
                #self.cur = self.tokeniser.Next()
                return left
            else:
                raise Exception("not a statement")
        elif self.cur.tokenType == Token.tokenTypeIdentificator:
            t = self.cur
            self.cur = self.tokeniser.Next()
            if self.cur.value == ":=":
                left = self.ParseAssignment(t)
                #self.cur = self.tokeniser.Next()
                return left
            else:
                left = self.ParseProcedureCall(t)
                #self.cur = self.tokeniser.Next()
                return left
        else:
            raise Exception("not a statement")   
    
    def ParseAssignment(self, des):
        left = self.ParseDesignator(des.value)
        self.cur = self.tokeniser.Next()
        right = self.ParseExpr()
        left = AssignmentNode(':=', left, right)
        return left
    
    def ParseProcedureCall(self, ident):
        left = self.ParseDesignator(ident.value)
        print(self.cur)
        if self.cur == '(':
            p = self.ParseActualParameters()
            left = ProcedureCallNode(left, p)
        elif self.cur.value in ['+', '*', ';']:
            left = ProcedureCallNode(left, [])
        else:
            print(self.cur)
            raise Exception('incorrect procedure call')
        return left

    def ParseIfStatement(self):
        cond = self.ParseExpr()
        if self.cur.value == "then":
            self.cur = self.tokeniser.Next()
            ifTrue = self.ParseStatement()
            if self.cur.value == "else":
                self.cur = self.tokeniser.Next()
                ifFalse = self.ParseStatement()
                cond = CompleteIfNode(cond, ifTrue, ifFalse)
            else:
                cond = IncompleteIfNode(cond, ifTrue)
            return cond
        else:
            raise Exception("keyword 'then' was expected")          
    
    def ParseWhileStatement(self):
        cond = self.ParseExpr()
        if self.cur.value == "do":
            self.cur = self.tokeniser.Next()
            ifTrue = self.ParseStatement()
            cond = WhileNode(cond, ifTrue)
            return cond
        else:
            raise Exception ("keyword 'do' was expected")
    
    def ParseRepeatStatement(self):
        statements = self.ParseStatement()
        if self.cur.value == "until":
            self.cur = self.tokeniser.Next()
            cond = self.ParseExpr()
            cond = RepeatNode(statements, cond)
            return cond
        else:
            print(self.cur)
            raise Exception ("keyword 'until' was expected")

    def ParseForStatement(self):
        name = self.ParseDesignator(self.cur.value)
        self.cur = self.tokeniser.Next()
        if self.cur.value == ':=':
            self.cur = self.tokeniser.Next()
            left = self.ParseExpr()
            way = self.ParseWay()
            right = self.ParseExpr()
            if self.cur.value == 'do':
                self.cur = self.tokeniser.Next()
                st = self.ParseStatement()
            else:
                raise Exception('"do" was expected')
            return ForNode(name, left, right, way, st)
        else:
            print(self.cur)
            raise Exception('invalid "for" syntax')
    
    def ParseWay(self):
        t = self.cur.value
        if self.cur.value == 'to':
            self.cur = self.tokeniser.Next()
            return WichWayNode(t)
        elif self.cur.value == 'downto':
            self.cur = self.tokeniser.Next()
            return WichWayNode(t)
        else:
            raise Exception('"to" or "downto" were expected')

    def ParseIOStatement(self):
        name = self.cur.value
        if self.cur.tokenType == Token.tokenTypeKeyWord:
            if name == 'read' or name == 'readln':
                d = DesignatorListNode([])
                d.designators = self.ParseDesignatorList().designators
                return InStatmentNode(name, d)
            elif name == 'write' or name == 'writeln':
                e = ExpListNode([])
                e.expList = self.ParseExprList().expList
                return OutStatmentNode(name, e)

    def ParseDesignatorList(self):
        d = DesignatorListNode([])
        self.cur = self.tokeniser.Next()
        if self.cur.value == '(':
            self.cur = self.tokeniser.Next()
        while (self.cur.tokenType == Token.tokenTypeIdentificator):
            d.designators.append(self.ParseDesignator(self.cur.value))
            self.cur = self.tokeniser.Next()
            if self.cur.value == ',':
                self.cur = self.tokeniser.Next()
        return d

    def ParseDesignator(self, name):
        #print(self.cur)
        return DesignatorNode(name)  

    def ParseActualParameters(self):
        p = self.ParseExprList()
        #print('acpar', p)
        return ActualParametersNode(p)
    
    def ParseExprList(self):
        l = ExpListNode([])
        self.cur = self.tokeniser.Next()
        if self.cur.value == '(':
            self.cur = self.tokeniser.Next()
        while self.cur.value != ')':
            l.expressions.append(self.ParseExpr())
            if self.cur.value == ',':
                self.cur = self.tokeniser.Next()
            #print('exprlist', l, self.cur)
        return l         

    def ParseExpr(self):
        left = self.ParseSimpleExpr()
        #print('expr', self.cur)
        while self.cur.tokenType == Token.tokenTypeOperators and self.cur.value in ['<', '>', '<>', '<=', '>=', '=']:
            #print('+-')
            op = self.cur.value
            self.cur = self.tokeniser.Next()
            right = self.ParseSimpleExpr()
            left = BinaryOpNode(op, left, right)
        return left

    def ParseSimpleExpr1(self):
        left = self.ParseTerm()
        #print('simpleexpr1', self.cur)
        while self.cur.tokenType == Token.tokenTypeOperators and self.cur.value in ['+', '-']:
            #print('+-')
            op = self.cur.value
            self.cur = self.tokeniser.Next()
            right = self.ParseTerm()
            left = BinaryOpNode(op, left, right)
        return left   

    def ParseSimpleExpr(self):
        #print('simpleexpr', self.cur)
        if self.cur.value in ['+', '-']:
            op = self.cur.value        
            self.cur = self.tokeniser.Next()
            right = self.ParseTerm()
            return UnaryOpNode(op, right)
        else:
            return self.ParseSimpleExpr1()

    def ParseTerm(self):
        left = self.ParseFactor()
        #print('term', self.cur)
        while self.cur.tokenType == Token.tokenTypeOperators and self.cur.value in ['*', '/']:
            if type(left) != StringNode:
                op = self.cur.value
                self.cur = self.tokeniser.Next()
                right = self.ParseFactor()
                left = BinaryOpNode(op, left, right)
            else:
                raise Exception('string in */')
        return left  

    def ParseNot(self):
        left = self.ParseFactor()
        return left

    def ParseFactor(self):
        t = self.cur
        #print('factor', t)
        if self.cur.tokenType == Token.tokenTypeInt:
            self.cur = self.tokeniser.Next()
            return LiteralIntNode(t.value)
        elif self.cur.value == '(':
            self.cur = self.tokeniser.Next()
            p = self.ParseExpr()
            if self.cur.value != ')':
                raise Exception('no right )')
            self.cur = self.tokeniser.Next()
            return p
        elif self.cur.tokenType == Token.tokenTypeIdentificator:    
            self.cur = self.tokeniser.Next()    
            if self.cur.value == '(':
                return self.ParseFunctionCall(t.value)
            else: 
                return self.ParseDesignator(t.value)  
        elif self.cur.tokenType == Token.tokenTypeDouble:
            self.cur = self.tokeniser.Next()
            return LiteralFloatNode(t.value)
        elif self.cur.tokenType == Token.tokenTypeString:
            self.cur = self.tokeniser.Next()
            return StringNode(t.value)
        elif self.cur.value == 'nil':
            self.cur = self.tokeniser.Next()
            return NilNode(t.value)
        elif self.cur.value == 'not':
            self.cur = self.tokeniser.Next()
            p = self.ParseNot()
            return NotNode('not', p)
        else:
            print(self.cur)
            raise Exception('end')

    def ParseFunctionCall(self, name):               
        p = self.ParseActualParameters()
        return FunctionCallNode(name, p)

    def ParseSubprogDeclList(self):
        pass

    def ParseProcedureDecl(self):
        pass

    def ParseProcedureHeading(self):
        name = ''
        params = []
        if self.cur.value == 'procedure' and self.cur.tokenType == Token.tokenTypeKeyWord:
            self.cur = self.tokeniser.Next()
            name = self.cur.value
            self.cur = self.tokeniser.Next()
            if self.cur.value == '(':
                params = self.ParseFormalParameters()
        return ProcedureHeadingNode(name, params)
    
    def ParseFunctionHeading(self):
        name = ''
        params = []
        if self.cur.value == 'function' and self.cur.tokenType == Token.tokenTypeKeyWord:
            self.cur = self.tokeniser.Next()
            name = self.cur.value
            self.cur = self.tokeniser.Next()
            if self.cur.value == '(':
                params = self.ParseFormalParameters()
        return FunctionHeadingNode(name, params)

    def ParseFormalParameters(self):
        params = []
        if self.cur.value == '(':
            while self.cur.value != ')':
                self.cur = self.tokeniser.Next()
                if self.cur == ';':
                    self.cur == self.tokeniser.Next()
                params.append(self.ParseOneFormalParam())
        return FormalParametersNode(params)


    def ParseOneFormalParam(self):
        ids = []
        typ = ''
        if self.cur.value == 'var' and self.cur.tokenType == Token.tokenTypeKeyWord:
            self.cur = self.tokeniser.Next()
        ids = self.ParseIdentList()
        if self.cur.value == ':':
            self.cur = self.tokeniser.Next()
            typ = self.cur.value  
            self.cur = self.tokeniser.Next()     
        return OneFormalParamNode(ids, typ)