import os, sys
import filecmp
from tokeniser import Token, Tokeniser
from parser1 import Parser
from nodes import *
import treePrinter

tInDir = 'tokeniser_In'
tOutDir = 'tokeniser_Out'
pInDir = 'parser_In'
pOutDir = 'parser_Out'

n = 0
ok = 0

if sys.argv[1] == 'T':
    inFiles = os.listdir(tInDir)
    outFiles = os.listdir(tOutDir)

    for f in outFiles:
        ffile = open(tOutDir + '/' + f[0:7] + '.out', 'w')
        ffile.close()

    for f in inFiles:
        n += 1
        print(f)
        inp = open(tInDir + '/' + f, 'r')
        lex = Tokeniser(''.join(inp.readlines()))
        while True:
            out = open(tOutDir + '/' + f[0:7] + '.out', 'a')
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
                    out = open(tOutDir + '/' + f[0:7] + '.out', 'r')
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
                    out.write(''.join(map(str, [t.tokenType, ' ', t.line, ' ', t.pos, ' ', t.value, ' ', t.src, '\n'])))
elif sys.argv[1] == 'P':
    inFiles = os.listdir(pInDir)
    outFiles = os.listdir(pOutDir)

    for f in outFiles:
        ffile = open(pOutDir + '/' + f[0:7] + '.out', 'w')
        ffile.close()

    for f in inFiles:
        n += 1
        print(f)
        inp = open(pInDir + '/' + f, 'r' ,encoding = 'utf-8')
        lex = Tokeniser(''.join(inp.readlines()))
        out = open(pOutDir + '/' + f[0:7] + '.out', 'a', encoding = 'utf-8')
        p = Parser(lex)
        try:
            r = treePrinter.getTree('', p.ParseProgramModule())
        except Exception as err:
            out.write(''.join(err.args) + '\n')
        else:
            out.write(str(r))
            out.close()
        finally:
            expstr = ''
            exp = open('exp/' + f[0:7] + '.txt', 'r')
            for line in exp:
                expstr += line

            outstr = ''
            out = open(pOutDir + '/' + f[0:7] + '.out', 'r')
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

print(''.join(map(str, ['---RESULT---\n', 'Total:  ', n,'\nOk:\t', ok, '\nFailed: ', n-ok])))