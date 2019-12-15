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
    tokenTypeDouble = 2
    tokenTypeString = 3
    tokenTypeIdentificator = 'Ident'
    tokenTypeKeyWord = 'Key'
    tokenTypeOperators = 6
    tokenTypeSeparators = 'sprt'
    tokenTypeEOF = 8

    keyWords = {'and', 'array', 'begin', 'case', 'const', 'div', 'do', 'downto', 'else', 'end', 'file', 'for', 'function',
                'goto', 'if', 'in', 'label', 'mod', 'nil', 'not', 'of', 'or', 'packed', 'procedure', 'program', 'record',
                'repeat', 'set', 'then', 'to', 'type', 'until', 'while', 'var', 'with', 'integer', 'real', 'string', 'break',
                'exit', 'forward', 'writeln', 'write', 'read', 'readln', 'length'}
    operands = {'+', '-', '=', '<>', '>', '<', '<=', '>=', '*', '/', '^', ':=', '+=', '-=', '*=', '/='}
    separators = {'(', ')', '{', '}', '[', ']', ';', ':', "'", ',', '.', '..', '//', '', '', '', '', '', '', ''}

class Tokeniser:
    def __init__(self, str):
        self.str = str
        self.line = 0
        self.pos = 0
        self.lineStart = 0

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


        if self.pos >= len(self.str):
            return Token(Token.tokenTypeEOF, self.line, self.pos - self.line)

        if self.str[self.pos].isdigit():
            p = Token(Token.tokenTypeInt, self.line, self.pos - self.line)
            while self.pos < len(self.str) and self.str[self.pos].isdigit():
                p.src += self.str[self.pos]
                self.pos += 1
            p.value = int(p.src)
            return p
            
        if self.str[self.pos].isalpha():
            p = Token(Token.tokenTypeIdentificator, self.line, self.pos - self.lineStart)
            while self.pos < len(self.str) and (self.str[self.pos].isdigit() or self.str[self.pos].isalpha() or self.str[self.pos] == '_'):
                p.src += self.str[self.pos]
                self.pos += 1
            if p.src in p.keyWords:
                p.tokenType = Token.tokenTypeKeyWord
            p.value = p.src
            return p
        else:
            raise Exception()