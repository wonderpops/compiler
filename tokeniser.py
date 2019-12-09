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
    tokenTypeKeyWords = 5
    tokenTypeOperators = 6
    tokenTypeSiparators = 7
    tokenTypeEOF = 8

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
            p.value = p.src
            return p
        else:
            raise Exception()