import os
import filecmp
from tokeniser import Token, Tokeniser

direct = 'in'
files = os.listdir(direct)

directOut = 'out'
ffiles = os.listdir(direct)

for f in ffiles:
    ffile = open('out/' + f, 'w')
    ffile.close()

n = 0

for f in files:
    print(f)
    inp = open('in/' + f, 'r')
    lex = Tokeniser(''.join(inp.readlines()))
    while True:
        t = lex.Next()
        out = open('out/' + f, 'a')
        if t.tokenType == Token.tokenTypeUndefind:
           out.write(str(t.tokenType)+'\n') 
        else:
            out.write(str(t.tokenType) + ' ' + str(t.line)  + ' ' + str(t.pos)  + ' ' + str(t.value) + ' ' + str(t.src) + '\n')
        if t.tokenType == Token.tokenTypeEOF:
            expstr = ''
            exp = open('exp/' + f, 'r')
            for line in exp:
                expstr += line

            out.close()
            out = open('out/' + f, 'r')
            outstr = ''
            for line in out:
                outstr += line

            if expstr == outstr:
                print('ok')
                n +=1
            else:
                print('failed')
                print(outstr)
            break
print('ok: ', n, 'failed: ', 76-n)