import os
import filecmp
from tokeniser import Token, Tokeniser

direct = 'in'
files = os.listdir(direct)

directOut = 'out'
ffiles = os.listdir(direct)

for f in ffiles:
    ffile = open('out/' + f[0:7] + '.out', 'w')
    ffile.close()

n = 0
ok = 0

for f in files:
    n += 1
    print(f)
    inp = open('in/' + f, 'r')
    lex = Tokeniser(''.join(inp.readlines()))
    while True:
        out = open('out/' + f[0:7] + '.out', 'a')
        try:
            t = lex.Next()
        except Exception as err:
            out.write(''.join(err.args) + '\n')
        else:
            if t.tokenType == Token.tokenTypeEOF:
                expstr = ''
                exp = open('exp/' + f[0:7] + '.txt', 'r')
                for line in exp:
                    expstr += line

                out.close()
                out = open('out/' + f[0:7] + '.out', 'r')
                outstr = ''
                for line in out:
                    outstr += line

                if expstr == outstr:
                    print('ok')
                    ok += 1
                else:
                    print('failed')
                    print('----------------------------')
                    print(outstr)
                    print('----------------------------')
                break
            else:
                out.write(str(t.tokenType) + ' ' + str(t.line)  + ' ' + str(t.pos)  + ' ' + str(t.value) + ' ' + str(t.src) + '\n')
print('ok: ', ok, 'failed: ', n-ok)