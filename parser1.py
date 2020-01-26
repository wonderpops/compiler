from nodes import *
from tokeniser import Token, Tokeniser
from exceptionMesages import ExceptionMessage, ExceptionMessageGenerator


class Parser:

    def __init__(self, tokeniser):
        self.tokeniser = tokeniser
        self.cur = self.tokeniser.Next()
        self.exMesGen = ExceptionMessageGenerator()
        self.exMes = ExceptionMessage
        #foundMessage = self.cur.value + ' found' 


    def ParseProgramModule(self):
        params = ProgramParamsNode([])
        if self.cur.src == 'program':
            self.cur = self.tokeniser.Next()
            if self.cur.tokenType == Token.tokenTypeIdentificator:
                name = IdentificatorNode(self.cur.value)
                self.cur = self.tokeniser.Next()            
            else:
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER201, self.cur))
            if self.cur.src == '(':
                self.cur = self.tokeniser.Next()
                params = self.ParseProgramParams()
            if self.cur.src == ';':
                self.cur = self.tokeniser.Next()
                body = self.ParseBlock()
                if self.cur.src == '.':
                    return ProgramModuleNode(name, params, body)
                else:
                    raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER101, self.cur))
            else:
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER105, self.cur))
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER301, self.cur))

    def ParseProgramParams(self):
        p = self.ParseIdentList()
        if not p:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER302, None))
        else:
            if self.cur.src == ')':
                self.cur = self.tokeniser.Next()
                return ProgramParamsNode(p)
            else:
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER106, self.cur))
    
    def ParseIdentList(self):
        ids = []
        while (self.cur.tokenType == Token.tokenTypeIdentificator):
            ids.append(IdentificatorNode(self.cur.value))
            self.cur = self.tokeniser.Next()
            if self.cur.src == ',':
                self.cur = self.tokeniser.Next()
            elif self.cur.src not in [')', ':'] :
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER102, self.cur))
        if self.cur.src not in [')', ':']:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER202, self.cur))
        else:
            return IdentListNode(ids)

    def ParseBlock(self):
        decl = DeclarationsNode(ConstDefBlockNode([]), VarDeclNode([], ''), SubprogDeclListNode([]))
        sec = ''
        while self.cur.src in ['const', 'var', 'function', 'procedure']:
            decl = self.ParseDeclarations() 
        if self.cur.src == 'begin':
            sec = self.ParseStatementSequence()
        return BlockNode(decl, sec)

    def ParseDeclarations(self):
        c = ConstDefBlockNode([])
        v = VarDeclNode([], '')
        s = SubprogDeclListNode([])
        dec = DeclarationsNode(c, v, s)
        if self.cur.src == 'const':
            c = self.ParseConstantDefBlock()
        if self.cur.src == 'var':
            v = self.ParseVariableDeclBlock()
        if self.cur.src in ['function', 'procedure']:
            s = self.ParseSubprogDeclList()
        dec = DeclarationsNode(c, v, s)
        return dec

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
            ident = IdentificatorNode(self.cur.value)
            self.cur = self.tokeniser.Next()
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER401, self.cur))
        if self.cur.src == '=':
            self.cur = self.tokeniser.Next()
            value = self.ParseConstExpression()
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER108, self.cur))
        if self.cur.src == ';':
            return ConstDefNode(ident, value)
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER104, self.cur))

    def ParseVariableDecl(self):
        t = TypeNode('')
        ids = IdentListNode([])
        if self.cur.tokenType == Token.tokenTypeIdentificator:
            ids = self.ParseIdentList()
            #self.cur = self.tokeniser.Next()
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER401, self.cur))
        if self.cur.src == ':':
            self.cur = self.tokeniser.Next()
            t = self.ParseType()
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER103, self.cur))
        if self.cur.src == ';':
            v = VarDeclNode(ids, t)
            return v
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER104, self.cur))
        

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
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER203, self.cur))   


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
        elif self.cur.value == 'real': 
            self.cur = self.tokeniser.Next()
            return TypeNode('real')
        elif self.cur.value == 'string':
            self.cur = self.tokeniser.Next()
            return TypeNode('string')
        elif self.cur.value == 'array':
            return self.ParseArrayType()
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER204, self.cur))

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
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER107, self.cur))
            if not subranges:
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER205, None))
            self.cur = self.tokeniser.Next()
        if  self.cur.src == 'of':
            self.cur = self.tokeniser.Next()
            t = self.ParseType()
        else:
            print(self.cur)
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER501, self.cur))
        if self.cur.src == ';':
            left = ArrayTypeNode(t, subranges)
            return left
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER104, self.cur))
             
    def ParseSubrange(self):
        p = self.ParseConstFactor()
        if self.cur.src == '..':
            self.cur = self.tokeniser.Next()
            f = self.ParseConstFactor()
            return SubrangeNode(p, f)
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER109, self.cur))

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
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER110, None))
            if not statements:
                left = EmptyNode('empty')
            else:
                left = StatementSequenceNode(statements)
            if self.cur.tokenType != Token.tokenTypeEOF:
                return left
            else:
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER402, None))
            
        
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
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER206, self.cur)) 
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
            left = IdentificatorNode(ident)
        if self.cur.src == '(':
            p = self.ParseActualParameters()
            left = ProcedureCallNode(left, p)
        elif self.cur.src in ['+', '*', ';']:
            left = ProcedureCallNode(left, [])
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER303, self.cur))
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
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER502, self.cur))          
    
    def ParseWhileStatement(self):
        cond = self.ParseExpr()
        if self.cur.src == 'do':
            self.cur = self.tokeniser.Next()
            ifTrue = self.ParseStatement()
            cond = WhileNode(cond, ifTrue)
            return cond
        else:
            raise Exception (self.exMesGen.getExceptionMessage(self.exMes.ER503, self.cur))
    
    def ParseRepeatStatement(self):
        statements = self.ParseStatement()
        self.cur = self.tokeniser.Next()
        if self.cur.src == 'until':
            self.cur = self.tokeniser.Next()
            cond = self.ParseExpr()
            cond = RepeatNode(statements, cond)
            return cond
        else:
            raise Exception (self.exMesGen.getExceptionMessage(self.exMes.ER504, self.cur))

    def ParseForStatement(self):
        name = IdentificatorNode(self.cur.value)
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
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER503, self.cur))
            return ForNode(name, left, right, way, st)
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER207, self.cur))
    
    def ParseWay(self):
        t = self.cur.value
        if self.cur.value == 'to':
            self.cur = self.tokeniser.Next()
            return WichWayNode(t)
        elif self.cur.value == 'downto':
            self.cur = self.tokeniser.Next()
            return WichWayNode(t)
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER505, self.cur))

    def ParseIOStatement(self):
        name = self.cur
        if self.cur.src in ['read', 'readln']:
            d  = self.ParseDesignatorList()            
            if self.cur.src == ';':
                return InStatmentNode(name.value, d)
            else:
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER104, self.cur))
        elif self.cur.src in ['write', 'writeln']:
            e = self.ParseExprList()
            if self.cur.src == ';':
                return OutStatmentNode(name.value, e)
            else:
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER104, self.cur))


    def ParseDesignatorList(self):
        d = []
        self.cur = self.tokeniser.Next()
        if self.cur.src == '(':
            self.cur = self.tokeniser.Next()
        while (self.cur.tokenType == Token.tokenTypeIdentificator):
            d.append(self.ParseDesignator(IdentificatorNode(self.cur.value)))
            self.cur = self.tokeniser.Next()
            if self.cur.src == ',':
                self.cur = self.tokeniser.Next()
        if self.cur.src == ')':
            self.cur = self.tokeniser.Next()
            return DesignatorListNode(d)
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER106, self.cur))

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
        l = []
        self.cur = self.tokeniser.Next()
        if self.cur.src == '(':
            self.cur = self.tokeniser.Next()
        while self.cur.src not in [')', ']']:
            l.append(self.ParseExpr())
            if self.cur.src == ',':
                self.cur = self.tokeniser.Next()
        self.cur = self.tokeniser.Next()
        return ExpListNode(l)       

    def ParseExpr(self):
        left = self.ParseSimpleExpr()
        while self.cur.src in ['<', '>', '<>', '<=', '>=', '=']:
            op = self.cur.value
            self.cur = self.tokeniser.Next()
            right = self.ParseSimpleExpr()
            left = BinaryOpNode(op, left, right)
        if self.cur.src in [';', 'then', 'do', 'to', 'downto', ')', ',', 'else']:
            return left
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER104, self.cur))

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
            left = UnaryOpNode(op, right)
            if self.cur.src in ['+', '-']:
                op = self.cur.src
                self.cur = self.tokeniser.Next()
                right = self.ParseTerm()
                left = BinaryOpNode(op, left, right)
            if self.cur.src in ['*', '/']:
                op = self.cur.src
                self.cur = self.tokeniser.Next()
                right = self.ParseTerm()
                left = BinaryOpNode(op, left, right)
            return left
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
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER106, self.cur))
            self.cur = self.tokeniser.Next()
            return p
        elif self.cur.tokenType == Token.tokenTypeIdentificator:    
            self.cur = self.tokeniser.Next()    
            if self.cur.src == '(':
                return self.ParseFunctionCall(IdentificatorNode(t.value))
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
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER304, self.cur))

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
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER104, self.cur))
        return ProcedureDeclNode(head, block)

    def ParseFunctionDecl(self):
        head = self.ParseFunctionHeading()
        fType = ''
        if self.cur.src == ':':
            self.cur = self.tokeniser.Next()
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER103, self.cur))
        if self.cur.src in ['integer', 'real', 'string']:
            fType = self.ParseType()
        else:
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER204, self.cur))
        if self.cur.src != ';':
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER104, self.cur))
        self.cur = self.tokeniser.Next()
        block = self.ParseBlock()
        if self.cur.src == '.':
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER104, self.cur))
        return FunctionDeclNode(head, fType, block)

    def ParseProcedureHeading(self):
        name = ''
        params = []
        if self.cur.src == 'procedure':
            self.cur = self.tokeniser.Next()
            name = IdentificatorNode(self.cur.value)
            self.cur = self.tokeniser.Next()
            if self.cur.src == '(':
                params = self.ParseFormalParameters()
        if self.cur.src != ';':
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER104, self.cur))
        return ProcedureHeadingNode(name, params)
    
    def ParseFunctionHeading(self):
        name = ''
        params = []
        if self.cur.src == 'function':
            self.cur = self.tokeniser.Next()
            name = IdentificatorNode(self.cur.value)
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
            typ = self.ParseType()    
        return OneFormalParamNode(ids, typ)