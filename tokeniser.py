from exceptionMesages import ExceptionMessage, ExceptionMessageGenerator

class Token:
    def __init__(self, tokenType, line, pos, value = None, src = ''):
        self.tokenType = tokenType
        self.value = value
        self.src = src
        self.line = line + 1
        self.pos = pos + 1
    def __str__(self):
        return'\t'.join(map(str, [self.line, self.pos, self.tokenType, self.value, self.src]))

    tokenTypeInt = 'Int'
    tokenTypeDouble = 'Dbl'
    tokenTypeString = 'Str'
    tokenTypeIdentificator = 'Ident'
    tokenTypeKeyWord = 'Key'
    tokenTypeOperators = 'Oper'
    tokenTypeSeparators = 'Sprt'
    tokenTypeEOF = 'EOF'
    tokenTypeUndefind = 'Undef'
    tokenTypeDoubleDot = 'DDot'
    tokenTypeComment = 'Comment'

    keyWords = {'and', 'array', 'begin', 'case', 'const', 'div', 'do', 'downto', 'else', 'end', 'file', 'for', 'function',
                'goto', 'if', 'in', 'label', 'mod', 'nil', 'not', 'of', 'or', 'packed', 'procedure', 'program', 'record',
                'repeat', 'set', 'then', 'to', 'type', 'until', 'while', 'var', 'with', 'integer', 'real', 'string', 'break',
                'exit', 'forward', 'writeln', 'write', 'read', 'readln', 'length'}
    simpleOperands = {'+', '-', '=',  '>', '<',  '*', '/', '^', ':'}
    complexOperands = {'<>', '<=', '>=', ':=', '+=', '-=', '*=', '/='}

    separators = {'(', ')', '{', '}', '[', ']', ';', ',', '.'}
    CyrSymb = {'q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m'}


class Tokeniser:
    def __init__(self, str):
        self.str = str
        self.line = 0
        self.pos = 0
        self.lineStart = 0
        self.exMesGen = ExceptionMessageGenerator()
        self.exMes = ExceptionMessage

    def Next(self):
        while self.pos < len(self.str):
            if self.str[self.pos] == ' ':
                self.pos += 1
            elif self.str[self.pos] == '\n':
                self.line +=1
                self.pos += 1
                self.lineStart = self.pos
            else:
                break

        #End of file
        if self.pos >= len(self.str):
            return Token(Token.tokenTypeEOF, self.line, self.pos - self.lineStart)

        #DoubleDot
        if self.str[self.pos] == '.' and (self.pos < len(self.str) -1):
            self.pos += 1
            if self.str[self.pos] == '.':
                p = Token(Token.tokenTypeDoubleDot, self.line, self.pos -1 - self.lineStart)
                p.src = '..'
                p.value = '..'
                self.pos += 1
                return p
            else:
                self.pos += -1
                
        #Comment
        if self.str[self.pos] == '/':
            p = Token(Token.tokenTypeComment, self.line, self.pos - self.lineStart)
            p.src = self.str[self.pos]
            self.pos += 1            
            if self.pos < len(self.str) and self.str[self.pos] == '/':
                p.src += self.str[self.pos]
                self.pos += 1
                while self.pos < len(self.str) and self.str[self.pos] != '\n':
                    p.src += self.str[self.pos]
                    self.pos += 1
                p.value = p.src[2:len(p.src)]
                return p
            else:
                self.pos -= 1


        #Int and Double
        if self.str[self.pos].isdigit():
            p = Token(Token.tokenTypeInt, self.line, self.pos - self.lineStart)
            while self.pos < len(self.str) and (self.str[self.pos].isdigit() or self.str[self.pos] == '.'):
                if self.str[self.pos] == '.' and (self.pos < len(self.str) - 1) and self.str[self.pos + 1] == '.':
                    p.value = int(p.src)
                    if p.value > 32767:
                        raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER601, None))
                    else:
                        return p
                else:
                    p.src += self.str[self.pos]
                    self.pos += 1
                

            if p.src.find('.') == p.src.rfind('.') and p.src.find('.') != -1:
                if p.src[len(p.src)-1] == '.':
                    raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER407, p))
                p.tokenType = Token.tokenTypeDouble
                p.value = float(p.src)
                if p.value > 1.7*(10**38):
                    raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER602, None))
                return p
            elif (p.src.find('.') < 0):
                p.value = int(p.src)
                if p.value > 32767:
                    raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER601, None))
                else:
                    return p
            else:
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER403, p))

        #Operands
        if self.str[self.pos] in Token.simpleOperands:
            p = Token(Token.tokenTypeOperators, self.line, self.pos - self.lineStart)
            while self.pos < len(self.str):
                p.src += self.str[self.pos]
                self.pos += 1
                if self.pos < len(self.str):
                    if p.src + self.str[self.pos] in Token.complexOperands:
                        p.src += self.str[self.pos]
                        self.pos += 1
                        p.value = p.src
                        return p
                    elif p.src in Token.simpleOperands:
                        p.value = p.src
                        return p
                    else:
                        raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER404, p))
                elif p.src in Token.simpleOperands:
                    p.value = p.src
                    return p
                else:
                    raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER404, p))
        
        #Separators
        if self.str[self.pos] in Token.separators:
            p = Token(Token.tokenTypeSeparators, self.line, self.pos - self.lineStart)
            p.src += self.str[self.pos]
            p.value = p.src
            self.pos += 1
            return p

        #Identificator
        if self.str[self.pos].lower() in Token.CyrSymb or self.str[self.pos] == '_':
            t = Token(Token.tokenTypeIdentificator, self.line, self.pos - self.lineStart)
            lenStr = 0
            while (self.pos < len(self.str) and
                (self.str[self.pos].isdigit() or self.str[self.pos].isalpha() or self.str[self.pos] == '_')):
                t.src += self.str[self.pos]
                lenStr += 1  
                if lenStr > 127:
                    raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER603, None))
                self.pos += 1
            if t.src in Token.keyWords:
                t.tokenType = Token.tokenTypeKeyWord
            t.value = t.src 
            return t

       

        #String
        if self.str[self.pos] == "'":
            t = Token(Token.tokenTypeString, self.line, self.pos - self.lineStart)
            t.src += self.str[self.pos]
            self.pos += 1
            lenStr = 0
            while (self.pos < len(self.str) and self.str[self.pos] != "'"):
                t.src += self.str[self.pos] 
                lenStr += 1  
                if lenStr > 255:
                    raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER604, None))
                else:
                    if (self.str[self.pos] == '\n'):
                        self.line += 1
                        self.pos += 1
                        self.lineStart = self.pos
                    self.pos += 1

            t.value = t.src[1:]    
            
            if (self.pos < len(self.str)):
                t.src += self.str[self.pos]
            else:
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER405, t))

            if (t.src.find('\n') != -1):
                self.pos += 1
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER405, t))

            #self.pos += 1
            if  self.str[self.pos] != '\n' or self.str[self.pos] != ' ':
                self.pos += 1
                return t
            else:
                raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER405, t))          
        else:
            t = Token(Token.tokenTypeUndefind, self.line, self.pos - self.lineStart)
            t.src += self.str[self.pos]
            self.pos += 1
            while ((self.pos < len(self.str)) and (self.str[self.pos] != '\n') and (self.str[self.pos] != ' ')):
                t.src += self.str[self.pos]
                self.pos += 1
            raise Exception(self.exMesGen.getExceptionMessage(self.exMes.ER406, t))
