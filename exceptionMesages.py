class ExceptionMessage:
    ER101 = '_101: Period "." was expected, but found'
    ER102 = '_102: Comma "," was expected, but found'
    ER103 = '_103: Colon ":" was expected, but found'
    ER104 = '_104: Semicolon ";" was expected, but found'
    ER105 = '_105: Semicolon ";" or program parameters declaration were expected, but found'
    ER106 = '_106: Closing bracket ")" was expected, but found'
    ER107 = '_107: Closing square bracket "]" was expected, but found'
    ER108 = '_108: Equality sign "=" was expected, but found'
    ER109 = '_109: Double dots ".." were expected, but found'
    
    ER201 = '_201: Incorrect program name:'
    ER202 = '_202: Incorrect parameter'
    ER203 = '_203: Incorrect constant expression:'
    ER204 = '_204: Incorrect type:'
    ER205 = '_205: Incorrect array range'
    ER206 = '_206: Incorrect statement:'
    ER207 = '_207: Incorrect syntax of for loop:'

    ER301 = '_301: Program declaration was expected, but found'
    ER302 = '_302: Program parameters were expected, but empty found'
    ER303 = '_303: Procedure parameters or semicolon ";" were expected, but found'
    ER304 = '_304: Expression was expected, but found'
    
    ER401 = '_401: Identificator was expected, but found'
    ER402 = '_402: Operator was expected, but end of file found'
    ER403 = '_403: Integer or real expected, but found'
    ER404 = '_404: Operand was expected, but found'
    ER405 = '_405: String was expected, but found'
    ER406 = '_406: Unexpected was found'

    ER501 = '_501: Keyword "of" was expected, but found'
    ER502 = '_502: Keyword "then" was expected, but found'
    ER503 = '_503: Keyword "do" was expected, but found'
    ER504 = '_504: Keyword "until" was expected, but found'
    ER505 = '_505: Keywords "to" or "downto" were expected, but found'
    
    ER601 = '_601: Value of integer out of range'
    ER602 = '_602: Value of real out of range'
    ER603 = '_603: Ident length out of range'
    ER604 = '_604: String length out of range'

class ExceptionMessageGenerator:
    def getExceptionMessage(self, exceptionMessage, token):
        if token:
            return ('[' + str(token.pos) + ', ' + str(token.line) + '] ' +
                    'ERROR' + exceptionMessage + ' "' + token.value + '"')
        else :
            return  ('ERROR'+exceptionMessage)   