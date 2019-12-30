from nodes import *
from tokeniser import Token, Tokeniser

class Parser:
    def __init__(self, tokeniser):
        self.tokeniser = tokeniser
        self.cur = self.tokeniser.Next()

    def ParseExpr(self):
        left = self.ParseTerm()
        #print('1', left, self.cur)
        while True:
            if self.cur.tokenType == Token.tokenTypeOperators and self.cur.value in ['+', '-']:
                #print('+-')
                op = self.cur
                self.cur = self.tokeniser.Next()
                right = self.ParseTerm()
                left = BinaryOpNode(op, left, right)
            return left          

    def ParseTerm(self):
        left = self.ParseFactor()
        #print('2', left, self.cur)
        while True:
            if self.cur.tokenType == Token.tokenTypeOperators and self.cur.value in ['*', '/']:
                #print('*/')
                op = self.cur
                self.cur = self.tokeniser.Next()
                right = self.ParseFactor()
                left = BinaryOpNode(op, left, right)
            return left  

    def ParseFactor(self):
        t = self.cur
        #print('3', self.cur)
        if self.cur.tokenType == Token.tokenTypeInt:
            self.cur = self.tokeniser.Next()
            return LiteralIntNode(t.value)
        elif self.cur.tokenType == Token.tokenTypeIdentificator:
            self.cur = self.tokeniser.Next()
            return VarNode(t.value)
        elif self.cur.tokenType == Token.tokenTypeDouble:
            self.cur = self.tokeniser.Next()
            return LiteralFloatNode(t.value)
        elif self.cur.value == '(':
            self.cur = self.tokeniser.Next()
            p = self.ParseExpr()
            if self.cur.value != ')':
                raise Exception()
            self.cur = self.tokeniser.Next()
            return p
        else:
            raise Exception()