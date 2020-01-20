from nodes import *
from tokeniser import Token, Tokeniser

class Parser:
    def __init__(self, tokeniser):
        self.tokeniser = tokeniser
        self.cur = self.tokeniser.Next()

    def ParseStatementSequence(self):
        if self.cur.value == "begin":
            statements = []
            self.cur = self.tokeniser.Next()
            while self.cur.value != "end":
                if self.cur.value == ';':
                    self.cur = self.tokeniser.Next()
                statements.append(self.ParseStatement())
                left = StatementSequenceNode(statements)
                return left
        
    def ParseStatement(self):
        t = self.cur
        if self.cur.value == "if":
            self.cur = self.tokeniser.Next()
            left = self.ParseIfStatement()
            self.cur = self.tokeniser.Next()
            return left
        elif self.cur.tokenType == Token.tokenTypeIdentificator:
            self.cur = self.tokeniser.Next()
            return DesignatorNode(t.value) 
        else:
            raise Exception("not a ctatement")   
    
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

    def ParseIOStatement(self):
        name = self.cur.value
        if self.cur.tokenType == Token.tokenTypeKeyWord:
            if name == 'read' or name == 'readln':
                d = DesignatorListNode([])
                d.Designators = self.ParseDesignatorList().Designators
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
            d.Designators.append(self.ParseDesignator(self.cur.value))
            self.cur = self.tokeniser.Next()
            if self.cur.value == ',':
                self.cur = self.tokeniser.Next()
        return d

    def ParseDesignator(self, name):
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
            l.expList.append(self.ParseExpr())
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
        else:
            #print(self.cur)
            raise Exception('end')

    def ParseFunctionCall(self, name):               
        p = self.ParseActualParameters()
        return FunctionCallNode(name, p)