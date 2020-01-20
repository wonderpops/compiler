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
                else:
                    statements.append(self.ParseStatement())
                    #print(statements)
                    #print(self.cur)
            left = StatementSequenceNode(statements)
            print('334234', left)
            return left
        
    def ParseStatement(self):
        t = self.cur
        if self.cur.value == "if":
            self.cur = self.tokeniser.Next()
            left = self.ParseIfStatement()
            self.cur = self.tokeniser.Next()
            return left
        elif self.cur.value == "while":
            self.cur = self.tokeniser.Next()
            left = self.ParseWhileStatement()
            self.cur = self.tokeniser.Next()
            return left
        elif self.cur.value == "begin":
            left = self.ParseStatementSequence()
            self.cur = self.tokeniser.Next()
            return left
        elif self.cur.value == "repeat":
            self.cur = self.tokeniser.Next()
            left = self.ParseRepeatStatement()
            self.cur = self.tokeniser.Next()
            return left
        elif self.cur.tokenType == Token.tokenTypeIdentificator:
            self.cur = self.tokeniser.Next()
           # print(t.value)
            return VarNode(t.value) 
        else:
            print(self.cur, t.value)
            raise Exception("not a statement")
            
    
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
        elif self.cur.tokenType == Token.tokenTypeIdentificator:    
            self.cur = self.tokeniser.Next()    
            if self.cur.value == '(':
                name = t.value               
                p = self.ParseActualParameters()
                return FunctionCallNode(name, p)
            else: 
                return VarNode(t.value)   
        elif self.cur.tokenType == Token.tokenTypeDouble:
            self.cur = self.tokeniser.Next()
            return LiteralFloatNode(t.value)
        elif self.cur.value == '(':
            self.cur = self.tokeniser.Next()
            p = self.ParseExpr()
            if self.cur.value != ')':
                raise Exception('no right )')
            self.cur = self.tokeniser.Next()
            return p
        elif self.cur.tokenType == Token.tokenTypeString:
            self.cur = self.tokeniser.Next()
            return StringNode(t.value)
        else:
            raise Exception('end')

    
    def ParseActualParameters(self):
        self.cur = self.tokeniser.Next()
        p = self.ParseExprList()
        #print('acpar', p)
        return p
    
    def ParseExprList(self):
        l = []
        while self.cur.value != ')':
            if self.cur.value == ',':
                self.cur = self.tokeniser.Next()
            l.append(self.ParseExpr())
            #print('exprlist', l, self.cur)
        return l

