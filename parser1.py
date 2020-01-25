from nodes import *
from tokeniser import Token, Tokeniser

class Parser:

    def __init__(self, tokeniser):
        self.tokeniser = tokeniser
        self.cur = self.tokeniser.Next()
        #foundMessage = self.cur.value + ' found' 


    def ParseProgramModule(self):
        params = []
        if self.cur.src == 'program':
            self.cur = self.tokeniser.Next()
            if self.cur.tokenType == Token.tokenTypeIdentificator:
                name = self.cur.value
                self.cur = self.tokeniser.Next()            
            else:
                raise Exception('ERROR: Incorrect program name: ' + self.cur.value)
            if self.cur.src == '(':
                self.cur = self.tokeniser.Next()
                params = self.ParseProgramParams()
            if self.cur.src == ';':
                self.cur = self.tokeniser.Next()
                body = self.ParseBlock()
                if self.cur.src == '.':
                    return ProgramModuleNode(name, params, body)
                else:
                    raise Exception('ERROR: Period "." was expected, but ' + self.cur.value + ' found')
            else:
                raise Exception('ERROR: Semicolon ";" or program parameters declaration were expected, but ' + self.cur.value + ' found')
        else:
            raise Exception('ERROR: Program declaration was expected, but ' + self.cur.value + ' found')

    def ParseProgramParams(self):
        p = self.ParseIdentList()
        if not p:
            raise Exception('ERROR: Program parameters were expected, but empty found')
        else:
            if self.cur.src == ')':
                self.cur = self.tokeniser.Next()
                return ProgramParamsNode(p)
            else:
                raise Exception('ERROR: Closing bracket ")" was expected, but ' + self.cur.value + ' found')
    
    def ParseIdentList(self):
        ids = []
        while (self.cur.tokenType == Token.tokenTypeIdentificator):
            ids.append(self.cur.value)
            self.cur = self.tokeniser.Next()
            if self.cur.src == ',':
                self.cur = self.tokeniser.Next()
            elif self.cur.src not in [')', ':'] :
                raise Exception('ERROR: Comma "," was expected, but ' + self.cur.value + ' found')
        if self.cur.src not in [')', ':']:
            raise Exception('ERROR: Incorrect parameter '+ self.cur.value)
        else:
            return ids

    def ParseBlock(self):
        decl = []
        sec = ''
        while self.cur.src in ['const', 'var', 'function', 'procedure']:
            decl.append(self.ParseDeclarations())  
        if self.cur.src == 'begin':
            sec = self.ParseStatementSequence()
        return BlockNode(decl, sec)

    def ParseDeclarations(self):
        decl = []
        if self.cur.src == 'const':
            decl.append(self.ParseConstantDefBlock())
        if self.cur.src == 'var':
            decl.append(self.ParseVariableDeclBlock())
        if self.cur.src in ['function', 'procedure']:
            decl.append(self.ParseSubprogDeclList())
        return DeclarationsNode(decl)

    def ParseConstantDefBlock(self):
        constants = []
        self.cur = self.tokeniser.Next()
        constants.append(self.ParseConstantDef())
        while self.cur.src == ';':
            self.cur = self.tokeniser.Next()
            if self.cur.tokenType == Token.tokenTypeIdentificator:
                constants.append(self.ParseConstantDef())
            else:
                break
        return ConstDefBlockNode(constants)

    def ParseVariableDeclBlock(self):
        varbls = []
        self.cur = self.tokeniser.Next()
        varbls.append(self.ParseVariableDecl())
        while self.cur.src == ';':
            self.cur = self.tokeniser.Next()
            if self.cur.tokenType == Token.tokenTypeIdentificator:
                varbls.append(self.ParseVariableDecl())
            else:
                break
        return VarDeclBlockNode(varbls) 

    def ParseConstantDef(self):
        ident = ''
        value = ''
        if self.cur.tokenType == Token.tokenTypeIdentificator:
            ident = self.cur.value
            self.cur = self.tokeniser.Next()
        else:
            raise Exception('ERROR: Identificator was expected, but ' + self.cur.value + ' found')
        if self.cur.src == '=':
            self.cur = self.tokeniser.Next()
            value = self.ParseConstExpression()
        else:
            raise Exception('ERROR: Equality sign "=" was expected, but ' + self.cur.value + ' found')
        if self.cur.src == ';':
            return ConstDefNode(ident, value)
        else:
            raise Exception('ERROR: Semicolon ";" was expected, but ' + self.cur.value + ' found')

    def ParseVariableDecl(self):
        ids = []
        if self.cur.tokenType == Token.tokenTypeIdentificator:
            ids = self.ParseIdentList()
            #self.cur = self.tokeniser.Next()
        else:
            raise Exception('ERROR: Identificator was expected, but ' + self.cur.value + ' found')
        if self.cur.src == ':':
            self.cur = self.tokeniser.Next()
            t = self.ParseType()
        else:
            raise Exception('ERROR: Colon ":" was expected, but ' + self.cur.value + ' found')
        if self.cur.src == ';':
            return VarDeclNode(ids, t)
        else:
            raise Exception('ERROR: Semicolon ";" was expected, but ' + self.cur.value + ' found')
        

    def ParseConstExpression(self):
        op = ''
        value = ''
        if self.cur.src in ['+', '-']:
            op = self.cur.value
            self.cur = self.tokeniser.Next()
        if self.cur.tokenType in [Token.tokenTypeInt, Token.tokenTypeDouble, Token.tokenTypeIdentificator]:
            value = self.ParseConstFactor()
            return ConstExpressionNode(op, value)
        elif self.cur.tokenType == Token.tokenTypeString:
            value = self.cur.value
            return ConstExpressionNode(op, value)
        elif self.cur.src == 'nil':
            value = NilNode().value
            return ConstExpressionNode(op, value)
        else:
            raise Exception('ERROR: Incorrect constant expression: ' + self.cur.value)   


    def ParseConstFactor(self):
        t = self.cur
        if self.cur.tokenType == Token.tokenTypeIdentificator:
            self.cur = self.tokeniser.Next()
            return IdentificatorNode(t.value)
        elif self.cur.tokenType == Token.tokenTypeInt:
            self.cur = self.tokeniser.Next()
            return LiteralIntNode(t.value)
        elif self.cur.tokenType == Token.tokenTypeDouble:
            self.cur = self.tokeniser.Next()
            return LiteralFloatNode(t.value)
        elif self.cur.src == 'nil':
            self.cur = self.tokeniser.Next()
            return NilNode()

    def ParseType(self):
        if self.cur.value == 'integer':
            self.cur = self.tokeniser.Next()
            return TypeNode('integer')
        elif self.cur.value == 'double': 
            self.cur = self.tokeniser.Next()
            return TypeNode('double')
        elif self.cur.value == 'string':
            self.cur = self.tokeniser.Next()
            return TypeNode('string')
        elif self.cur.value == 'array':
            return self.ParseArrayType()
        else:
            raise Exception('ERROR: Incorrect type: ' + self.cur.value)

    def ParseArrayType(self):        
        self.cur = self.tokeniser.Next()
        subranges = []
        if self.cur.src == '[':            
            self.cur = self.tokeniser.Next()
            while self.cur.src != ']':
                if self.cur.src == ',':
                    self.cur = self.tokeniser.Next()
                else:
                    subranges.append(self.ParseSubrange())
            if self.cur.src != ']':
                raise Exception('ERROR: Closing square bracket "]" was expected, but ' + self.cur.value + ' found')
            if not subranges:
                raise Exception('ERROR: Incorrect array range' )
            self.cur = self.tokeniser.Next()
        if  self.cur.src == 'of':
            self.cur = self.tokeniser.Next()
            t = self.ParseType()
        else:
            print(self.cur)
            raise Exception('ERROR: Key word "of" was expected, but ' + self.cur.value + ' found')
        if self.cur.src == ';':
            left = ArrayTypeNode(t, subranges)
            return left
        else:
            raise Exception('ERROR: Semicolon ";" was expected, but ' + self.cur.value + ' found')
             
    def ParseSubrange(self):
        p = self.ParseConstFactor()
        if self.cur.src == '..':
            self.cur = self.tokeniser.Next()
            f = self.ParseConstFactor()
            return SubrangeNode(p, f)
        else:
            raise Exception('ERROR: Double dots ".." were expected, but ' + self.cur.value + ' found')

    def ParseStatementSequence(self):
        if self.cur.src == 'begin':
            statements = []
            self.cur = self.tokeniser.Next()
            while self.cur.src != 'end':
                if self.cur.src == ';':
                    self.cur = self.tokeniser.Next()
                else:
                    statements.append(self.ParseStatement())            
            self.cur = self.tokeniser.Next()
            if self.cur.src == ';':
               self.cur = self.tokeniser.Next()
            elif self.cur.src != '.':
                raise Exception('ERROR: Semicolon ";" or period "." was expected, end of file found')
            if not statements:
                left = EmptyNode('empty')
            else:
                left = StatementSequenceNode(statements)
            if self.cur.tokenType != Token.tokenTypeEOF:
                return left
            else:
                raise Exception('ERROR: Operator was expected but end of file found')
            
        
    def ParseStatement(self):
        t = self.cur
        if self.cur.src == "if":
            self.cur = self.tokeniser.Next()
            left = self.ParseIfStatement()
        elif self.cur.src == "while":
            self.cur = self.tokeniser.Next()
            left = self.ParseWhileStatement()
        elif self.cur.src == "begin":
            left = self.ParseStatementSequence()
        elif self.cur.src == "repeat":
            self.cur = self.tokeniser.Next()
            left = self.ParseRepeatStatement()
        elif self.cur.src == "for":
            self.cur = self.tokeniser.Next()
            left = self.ParseForStatement()
        elif self.cur.src in ['read', 'readln', 'write', 'writeln']:
            left = self.ParseIOStatement()
        elif self.cur.tokenType == Token.tokenTypeIdentificator:
            t = self.cur
            self.cur = self.tokeniser.Next()
            if self.cur.value == ":=" or self.cur.value == '[':
                left = self.ParseAssignment(t)
            else:
                left = self.ParseProcedureCall(t)
        else:
            raise Exception("ERROR: Incorrect statement: " + self.cur.value) 
        return left

    
    def ParseAssignment(self, des):
        left = self.ParseDesignator(des.value)
        self.cur = self.tokeniser.Next()
        right = self.ParseExpr()
        left = AssignmentNode(':=', left, right)
        return left
    
    def ParseProcedureCall(self, ident):
        left = ''
        if ident.tokenType == Token.tokenTypeIdentificator:
            left = ident
        if self.cur.src == '(':
            p = self.ParseActualParameters()
            left = ProcedureCallNode(left, p)
        elif self.cur.src in ['+', '*', ';']:
            left = ProcedureCallNode(left, [])
        else:
            raise Exception('ERROR: Procedure parameters or semicolon ";" were expected, but ' + self.cur.value + ' found')
        return left

    def ParseIfStatement(self):
        cond = self.ParseExpr()
        if self.cur.src == 'then':
            self.cur = self.tokeniser.Next()
            ifTrue = self.ParseStatement()
            if self.cur.src == 'else':
                self.cur = self.tokeniser.Next()
                ifFalse = self.ParseStatement()
                cond = CompleteIfNode(cond, ifTrue, ifFalse)
            else:
                cond = IncompleteIfNode(cond, ifTrue)
            return cond
        else:
            raise Exception('ERROR: Keyword "then" was expected, but ' + self.cur.value + ' found')          
    
    def ParseWhileStatement(self):
        cond = self.ParseExpr()
        if self.cur.src == 'do':
            self.cur = self.tokeniser.Next()
            ifTrue = self.ParseStatement()
            cond = WhileNode(cond, ifTrue)
            return cond
        else:
            raise Exception ('ERROR: Keyword "do" was expected, but ' + self.cur.value + ' found')
    
    def ParseRepeatStatement(self):
        statements = self.ParseStatement()
        self.cur = self.tokeniser.Next()
        if self.cur.src == 'until':
            self.cur = self.tokeniser.Next()
            cond = self.ParseExpr()
            cond = RepeatNode(statements, cond)
            return cond
        else:
            raise Exception ('ERROR: Keyword "until" was expected, but ' + self.cur.value + ' found')

    def ParseForStatement(self):
        name = self.cur
        self.cur = self.tokeniser.Next()
        if self.cur.src == ':=':
            self.cur = self.tokeniser.Next()
            left = self.ParseExpr()
            way = self.ParseWay()
            right = self.ParseExpr()
            if self.cur.src == 'do':
                self.cur = self.tokeniser.Next()
                st = self.ParseStatement()
            else:
                raise Exception('ERROR: Keyword "do" was expected, but ' + self.cur.value + ' found')
            return ForNode(name, left, right, way, st)
        else:
            raise Exception('ERROR: Incorrect syntax of for loop: ' + self.cur.value)
    
    def ParseWay(self):
        t = self.cur.value
        if self.cur.value == 'to':
            self.cur = self.tokeniser.Next()
            return WichWayNode(t)
        elif self.cur.value == 'downto':
            self.cur = self.tokeniser.Next()
            return WichWayNode(t)
        else:
            raise Exception('ERROR: Keywords "to" or "downto" were expected, but ' + self.cur.value + ' found')

    def ParseIOStatement(self):
        name = self.cur
        if self.cur.src in ['read', 'readln']:
            d = DesignatorListNode([])
            d.designators = self.ParseDesignatorList().designators            
            if self.cur.src == ';':
                return InStatmentNode(name.value, d)
            else:
                raise Exception('ERROR: Semicolon ";" was expected, but ' + self.cur.value + ' found')
        elif self.cur.src in ['write', 'writeln']:
            e = ExpListNode([])
            e.expressions = self.ParseExprList().expressions
            if self.cur.src == ';':
                return OutStatmentNode(name.value, e)
            else:
                raise Exception('ERROR: Semicolon ";" was expected, but ' + self.cur.value + ' found')


    def ParseDesignatorList(self):
        d = DesignatorListNode([])
        self.cur = self.tokeniser.Next()
        if self.cur.src == '(':
            self.cur = self.tokeniser.Next()
        while (self.cur.tokenType == Token.tokenTypeIdentificator):
            d.designators.append(self.ParseDesignator(self.cur.value))
            self.cur = self.tokeniser.Next()
            if self.cur.src == ',':
                self.cur = self.tokeniser.Next()
        if self.cur.src == ')':
            self.cur = self.tokeniser.Next()
            return d
        else:
            raise Exception('ERROR: Closing bracket ")" was expected, but ' + self.cur.value + ' found')

    def ParseDesignator(self, name):
        stuff = []
        if self.cur.src == '[':
            stuff = self.ParseDesignatorStuff()
        return DesignatorNode(name, stuff)

    def ParseDesignatorStuff(self):
        return self.ParseExprList()  

    def ParseActualParameters(self):
        p = self.ParseExprList()
        return ActualParametersNode(p)
    
    def ParseExprList(self):
        l = ExpListNode([])
        self.cur = self.tokeniser.Next()
        if self.cur.src == '(':
            self.cur = self.tokeniser.Next()
        while self.cur.src not in [')', ']']:
            l.expressions.append(self.ParseExpr())
            if self.cur.src == ',':
                self.cur = self.tokeniser.Next()
        self.cur = self.tokeniser.Next()
        return l         

    def ParseExpr(self):
        left = self.ParseSimpleExpr()
        while self.cur.src in ['<', '>', '<>', '<=', '>=', '=']:
            op = self.cur.value
            self.cur = self.tokeniser.Next()
            right = self.ParseSimpleExpr()
            left = BinaryOpNode(op, left, right)
        if self.cur.src in [';', 'then', 'do', 'to', 'downto', ')', ',']:
            return left
        else:
            raise Exception('ERROR: Semicolon ";" was expected, but ' + self.cur.value + ' found')

    def ParseSimpleExpr1(self):
        left = self.ParseTerm()
        while self.cur.src in ['+', '-']:
            op = self.cur.value
            self.cur = self.tokeniser.Next()
            right = self.ParseTerm()
            left = BinaryOpNode(op, left, right)
        return left   

    def ParseSimpleExpr(self):
        if self.cur.src in ['+', '-']:
            op = self.cur.value        
            self.cur = self.tokeniser.Next()
            right = self.ParseTerm()
            return UnaryOpNode(op, right)
        else:
            return self.ParseSimpleExpr1()

    def ParseTerm(self):
        left = self.ParseFactor()
        while self.cur.src in ['*', '/']:
            op = self.cur.value
            self.cur = self.tokeniser.Next()
            right = self.ParseFactor()
            left = BinaryOpNode(op, left, right)
        return left  

    def ParseNot(self):
        left = self.ParseFactor()
        return left

    def ParseFactor(self):
        t = self.cur
        if self.cur.tokenType == Token.tokenTypeInt:
            self.cur = self.tokeniser.Next()
            return LiteralIntNode(t.value)
        elif self.cur.src == '(':
            self.cur = self.tokeniser.Next()
            p = self.ParseExpr()
            if self.cur.src != ')':
                raise Exception('ERROR: Closing bracket ")" was expected, but ' + self.cur.value + ' found')
            self.cur = self.tokeniser.Next()
            return p
        elif self.cur.tokenType == Token.tokenTypeIdentificator:    
            self.cur = self.tokeniser.Next()    
            if self.cur.src == '(':
                return self.ParseFunctionCall(t.value)
            else: 
                return self.ParseDesignator(t.value)  
        elif self.cur.tokenType == Token.tokenTypeDouble:
            self.cur = self.tokeniser.Next()
            return LiteralFloatNode(t.value)
        elif self.cur.tokenType == Token.tokenTypeString:
            self.cur = self.tokeniser.Next()
            return StringNode(t.value)
        elif self.cur.src == 'nil':
            self.cur = self.tokeniser.Next()
            return NilNode(t.value)
        elif self.cur.src == 'not':
            self.cur = self.tokeniser.Next()
            p = self.ParseNot()
            return NotNode('not', p)
        else:
            raise Exception('ERROR: Expression was expected, but ' + self.cur.value + ' found')

    def ParseFunctionCall(self, name):               
        p = self.ParseActualParameters()
        return FunctionCallNode(name, p)

    def ParseSubprogDeclList(self):
        DeclList = []
        if self.cur.src == 'function':
            DeclList.append(self.ParseFunctionDecl())
        elif self.cur.src == 'procedure':
            DeclList.append(self.ParseProcedureDecl())
        while self.cur.src == ';':
            self.cur = self.tokeniser.Next()
            if self.cur.src == 'function':
                DeclList.append(self.ParseFunctionDecl())
            elif self.cur.src == 'procedure':
                DeclList.append(self.ParseProcedureDecl())
            else:
                break
        return SubprogDeclListNode(DeclList)          


    def ParseProcedureDecl(self):
        head = self.ParseProcedureHeading()
        self.cur = self.tokeniser.Next()
        block = self.ParseBlock()
        if self.cur.src == '.':
            raise Exception('ERROR: Semicolon ";" was expected, but ' + self.cur.value + ' found')
        return ProcedureDeclNode(head, block)

    def ParseFunctionDecl(self):
        head = self.ParseFunctionHeading()
        fType = ''
        if self.cur.src == ':':
            self.cur = self.tokeniser.Next()
        else:
            raise Exception('ERROR: Colon ":" was expected, but ' + self.cur.value + ' found')
        if self.cur.tokenType == Token.tokenTypeKeyWord:
            fType = self.cur.value
            self.cur = self.tokeniser.Next()
        if self.cur.src != ';':
            raise Exception('ERROR: Semicolon ";" was expected, but ' + self.cur.value + ' found')
        self.cur = self.tokeniser.Next()
        block = self.ParseBlock()
        if self.cur.src == '.':
            raise Exception('ERROR: Semicolon ";" was expected, but ' + self.cur.value + ' found')
        return FunctionDeclNode(head, fType, block)

    def ParseProcedureHeading(self):
        name = ''
        params = []
        if self.cur.src == 'procedure':
            self.cur = self.tokeniser.Next()
            name = self.cur.value
            self.cur = self.tokeniser.Next()
            if self.cur.src == '(':
                params = self.ParseFormalParameters()
        if self.cur.src != ';':
            raise Exception('ERROR: Semicolon ";" was expected, but ' + self.cur.value + ' found')
        return ProcedureHeadingNode(name, params)
    
    def ParseFunctionHeading(self):
        name = ''
        params = []
        if self.cur.src == 'function':
            self.cur = self.tokeniser.Next()
            name = self.cur.value
            self.cur = self.tokeniser.Next()
            if self.cur.src == '(':
                params = self.ParseFormalParameters()
        return FunctionHeadingNode(name, params)

    def ParseFormalParameters(self):
        params = []
        if self.cur.src == '(':
            while self.cur.src != ')':
                self.cur = self.tokeniser.Next()
                if self.cur.src == ';':
                    self.cur == self.tokeniser.Next()
                params.append(self.ParseOneFormalParam())
        self.cur = self.tokeniser.Next()
        return FormalParametersNode(params)


    def ParseOneFormalParam(self):
        ids = []
        typ = ''
        if self.cur.src == 'var':
            self.cur = self.tokeniser.Next()
        ids = self.ParseIdentList()
        if self.cur.src == ':':
            self.cur = self.tokeniser.Next()
            typ = self.cur.value  
            self.cur = self.tokeniser.Next()     
        return OneFormalParamNode(ids, typ)