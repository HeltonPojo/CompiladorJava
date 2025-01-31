def createTokensLib(nomeArquivo):
    with open(nomeArquivo, "r") as arquivoTokens:
        linhasTokens = arquivoTokens.readlines()
        linhaAtual = 0
        libTokens = {}
        for linha in linhasTokens:
            linhaAtual += 1
            libTokens[linha.strip()] = linhaAtual
        libTokens['STR'] = 43
        libTokens['IDENT'] = 44
        libTokens['NumHex'] = 45
        libTokens['NumOctal'] = 46
        libTokens['NumFloat'] = 47
        libTokens['NumInt'] = 48
        return libTokens

class conversorIntermediario:
    def __init__(self, lista):
        self.tokens = createTokensLib('tokens.txt')
        self.lista = lista
        self.index = 0
        self.listaInterpretador = []

    def consome(self, tokenEsperado):
        tokenEsperadoId = self.tokens[tokenEsperado]
        token, _, _, _= self.lista[self.index]
        if token == tokenEsperadoId:
            self.index += 1
            return
        else:
            self.throwError(f"Erro na função consumo\nTOKEN ESPERADO: {tokenEsperado}")
    
    def appendIntermediaro(self, operantion):
        result, label1, label2 = 'None', 'None', 'None'
        if operantion == '=':
            label1 = 'a'
            label2 = 'b'
        self.listaInterpretador.append((operantion, result, label1, label2))

    def throwError(self, msg):
        _, lexema, linha, coluna = self.lista[self.index]
        print("Elemento da Lista: ", self.lista[self.index])
        print("LINHA: ", linha)
        print("COLUNA: ", coluna)
        print("LEXEMA: ", lexema)
        raise Exception(msg)
    #------------------------------------
    # o programa sera numa funcao main
    #------------------------------------

    #<function*> -> <type> 'IDENT' '(' ')' <bloco> ;
    def function(self):
        self.type()
        self.consome('IDENT')
        self.consome('(')
        self.consome(')')
        self.bloco()
        return
    #<type> -> 'int' | 'float' | 'string ;
    def type(self):
        token , _, _, _ = self.lista[self.index]
        if token == self.tokens['int']:
            self.consome('int')
        elif token == self.tokens['float']:
            self.consome('float')
        elif token == self.tokens['string']:
            self.consome('string')
        else:
            self.throwError("Erro na função type")
        return
    #<bloco> -> '{' <stmtList> '}' ;
    def bloco(self):
        self.consome('{')
        self.stmtList()
        self.consome('}')
        return
    #<stmtList> -> <stmt> <stmtList> | & ;
    def stmtList(self):
        token, lex, _, _ = self.lista[self.index]
        if lex in ('for','system','while', '!', '+', '-', '(', 'if', '{', 'break', 'continue', 'int', 'float', 'string', ';') or token in (self.tokens['STR'], self.tokens['IDENT'], self.tokens['NumHex'], self.tokens['NumOctal'], self.tokens['NumInt'], self.tokens['NumFloat']):
            self.stmt()
            self.stmtList()
        return
    #<stmt> -> <forStmt> | <ioStmt>| <whileStmt>| <atribu> ';' | <ifStmt> | <bloco> | 'break'| 'continue'| <declaration>| ';' ;
    def stmt(self):
        token, lex, _, _ = self.lista[self.index]
        if lex == 'for':
            self.forStmt()
        elif lex == 'system':
            self.ioStmt()
        elif lex == 'while':
            self.whileStmt()
        elif lex == '!' or lex == '+' or lex == '-' or lex == '(' or token == self.tokens['STR'] or token == self.tokens['IDENT'] or token == self.tokens['NumHex'] or token == self.tokens['NumOctal'] or token == self.tokens['NumInt'] or token == self.tokens['NumFloat']:
            self.atrib()
            self.consome(';')
        elif lex == 'if':
            self.ifStmt()
        elif lex == '{':
            self.bloco()
        elif lex == 'break':
            self.consome('break')
        elif lex == 'continue':
            self.consome('continue')
        elif lex == 'int' or lex == 'float' or lex == 'string':
            self.declaration()
        elif lex == ';':
            self.consome(';')
        else:
            self.throwError("Erro na função stmt")
        return

    #---------------------------
    # descricao das instrucoes
    #---------------------------

    #<declaration> -> <type> <identList> ';' ;
    def declaration(self):
        self.type()
        self.identList()
        self.consome(';')
        return
    #<identList> -> 'IDENT' <restoIdentList> ;
    def identList(self):
        self.consome('IDENT')
        self.restoIdentList()
        return
    #<restoIdentList> -> ',' 'IDENT' <restoIdentList> | & ;
    def restoIdentList(self):
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens[',']:
            self.consome(',')
            self.consome('IDENT')
            self.restoIdentList()
        return

    # comando for
    #<forStmt> -> 'for' '(' <optAtrib> ';' <optExpr> ';' <optAtrib> ')' <stmt> ;
    def forStmt(self):
        self.consome('for')
        self.consome('(')
        self.optAtrib()
        self.consome(';')
        self.optExpr()
        self.consome(';')
        self.optAtrib()
        self.consome(')')
        self.stmt()
        return

    #<optExpr> -> <expr> | & ;
    def optExpr(self):
        token, lex, _, _ = self.lista[self.index]
        if lex == '!' or lex == '+' or lex == '-' or lex == '(' or token == self.tokens['STR'] or token == self.tokens['IDENT'] or token == self.tokens['NumHex'] or token == self.tokens['NumOctal'] or token == self.tokens['NumInt'] or token == self.tokens['NumFloat']:
            self.expr()
        return
    #<optAtrib> -> <atrib> | & ;
    def optAtrib(self):
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens['IDENT']:
            self.atrib()
        return

    # comandos de IO
    #<ioStmt> -> 'system' '.' 'out' '.' 'print'  '(' <type> ',' 'IDENT' ')' ';' | 'system' '.' 'in' '.' 'scan' '(' <outList> ')' ';' ;
    def ioStmt(self):
        self.consome('system')
        self.consome('.')
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens['out']:
            self.consome('out')
            self.consome('.')
            self.consome('print')
            self.consome('(')
            self.outList()
            self.consome(')')
            self.consome(';')
        elif token == self.tokens['in']:
            self.consome('in')
            self.consome('.')
            self.consome('scan')
            self.consome('(')
            self.type()
            self.consome(',')
            self.consome('IDENT')
            self.consome(')')
            self.consome(';')
        else:
            self.throwError("Erro na função ioStmt")
        return
    #<outList> -> <out> <restoOutList> ;         
    def outList(self):
        self.out()
        self.restoOutList()
        return
    #<out> -> 'STR' | 'IDENT' | 'NUMdec' | 'NUMfloat' | 'NUMoct' | 'NUMhex';
    def out(self):
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens['STR']:
            self.consome('STR')
        elif token == self.tokens['IDENT']:
            self.consome('IDENT')
        elif token == self.tokens['NumInt']:
            self.consome('NumInt')
        elif token == self.tokens['NumFloat']:
            self.consome('NumFloat')
        elif token == self.tokens['NumOctal']:
            self.consome('NumOctal')
        elif token == self.tokens['NumHex']:
            self.consome('NumHex')
        else:
            self.throwError("Erro na função out")
        return
    #<restoOutList> -> ',' <out> <restoOutList> | & ;
    def restoOutList(self):
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens[',']:
            self.consome(',')
            self.out()
            self.restoOutList()
        return

    # comando while
    #<whileStmt> -> 'while' '(' <expr> ')' <stmt> ;
    def whileStmt(self):
        self.consome('while')
        self.consome('(')
        self.expr()
        self.consome(')')
        self.stmt()
        return

    # comando if
    #<ifStmt> -> 'if' '(' <expr> ')' <stmt> <elsePart> ;
    def ifStmt(self):
        self.consome('if')
        self.consome('(')
        self.expr()
        self.consome(')')
        self.stmt()
        self.elsePart()
        return
    #<elsePart> -> 'else' <stmt> | & ;
    def elsePart(self):
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens['else']:
            self.consome('else')
            self.stmt()
        return

    #------------------------------
    # expressoes
    #------------------------------
    #<atrib> -> 'IDENT' '=' <expr> | 'IDENT' ':=' <expr> | 'IDENT' '+=' <expr> | 'IDENT' '-=' <expr> | 'IDENT' '*=' <expr> | 'IDENT' '/=' <expr> | 'IDENT' '%=' <expr>;
    def atrib(self):
        self.consome('IDENT')
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens['=']:
            self.consome('=')
        elif token == self.tokens['+=']:
            self.consome('+=')
        elif token == self.tokens['-=']:
            self.consome('-=')
        elif token == self.tokens['*=']:
            self.consome('*=')
        elif token == self.tokens['/=']:
            self.consome('/=')
        elif token == self.tokens['%=']:
            self.consome('%=')
        else:
            self.throwError("Erro na função atrib")
        self.expr()
        return

    #<expr> -> <or> ;
    def expr(self):
        self.orFunc()
        return
    #<or> -> <and> <restoOr> ;
    def orFunc(self):
        self.andFunc()
        self.restoOr()
        return
    #<restoOr> -> '||' <and> <restoOr> | & ;
    def restoOr(self):
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens['||']:
            self.consome('||')
            self.andFunc()
            self.restoOr()
        return
    #<and> -> <not> <restoAnd> ;
    def andFunc(self):
        self.notFunc()
        self.restoAnd()
        return
    #<restoAnd> -> '&&' <not> <restoAnd> | & ;
    def restoAnd(self):
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens['&&']:
            self.consome('&&')
            self.notFunc()
            self.restoAnd
        return
    #<not> -> '!' <not> | <rel> ;
    def notFunc(self):
        token, lex, _, _ = self.lista[self.index]
        if token == self.tokens['!']:
            self.consome('!')
            self.notFunc()
        elif lex == '+' or lex == '-' or lex == '(' or token == self.tokens['STR'] or token == self.tokens['IDENT'] or token == self.tokens['NumHex'] or token == self.tokens['NumOctal'] or token == self.tokens['NumInt'] or token == self.tokens['NumFloat']:
            self.rel()
        else:
            self.throwError("Erro na função notFunc")
        return
    #<rel> -> <add> <restoRel> ;
    def rel(self):
        self.add()
        self.restoRel()
        return
    #<restoRel> -> '==' <add> | '!=' <add>| '<' <add> | '<=' <add> | '>' <add> | '>=' <add> | & ;
    def restoRel(self):
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens['==']:
            self.consome('==')
            self.add()
        elif token == self.tokens['!=']:
            self.consome('!=')
            self.add()
        elif token == self.tokens['<']:
            self.consome('<')
            self.add()
        elif token == self.tokens['<=']:
            self.consome('<=')
            self.add()
        elif token == self.tokens['>']:
            self.consome('>')
            self.add()
        elif token == self.tokens['>=']:
            self.consome('>=')
            self.add()
        return
    #<add> -> <mult> <restoAdd> ;
    def add(self):
        self.mult()
        self.restoAdd()
        return
    #<restoAdd> -> '+' <mult> <restoAdd> | '-' <mult> <restoAdd> | & ;
    def restoAdd(self):
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens['+']:
            self.consome('+')
            self.mult()
            self.restoAdd()
        elif token == self.tokens['-']:
            self.consome('-')
            self.mult()
            self.restoAdd()
        return
    #<mult> -> <uno> <restoMult> ;
    def mult(self):
        self.uno()
        self.restoMult()
        return
    #<restoMult> -> '*' <uno> <restoMult>|  '/' <uno> <restoMult> |  '%' <uno> <restoMult> | & ;
    def restoMult(self):
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens['*']:
            self.consome('*')
            self.uno()
            self.restoMult()
        elif token == self.tokens['/']:
            self.consome('/')
            self.uno()
            self.restoMult()
        elif token == self.tokens['%']:
            self.consome('%')
            self.uno()
            self.restoMult()
        return
    #<uno> -> '+' <uno> | '-' <uno> | <fator> ;
    def uno(self):
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens['+']:
            self.consome('+')
            self.uno()
        elif token == self.tokens['-']:
            self.consome('-')
            self.uno()
        elif token in (self.tokens['NumInt'], self.tokens['NumFloat'], self.tokens['NumHex'], self.tokens['NumOctal'], self.tokens['IDENT'], self.tokens['('], self.tokens['STR']):
            self.fator()
        else:
            self.throwError("Erro na função uno")
        return
    #<fator> -> 'NUMint' | 'NUMfloat' | 'NUMoct' | 'NUMhex' | 'IDENT'  | '(' <expr> ')' | 'STR';
    def fator(self):
        token, _, _, _ = self.lista[self.index]
        if token == self.tokens['NumInt']:
            self.consome('NumInt')
        elif token == self.tokens['NumFloat']:
            self.consome('NumFloat')
        elif token == self.tokens['NumHex']:
            self.consome('NumHex')
        elif token == self.tokens['NumOctal']:
            self.consome('NumOctal')
        elif token == self.tokens['IDENT']:
            self.consome('IDENT')
        elif token == self.tokens['(']:
            self.consome('(')
            self.expr()
            self.consome(')')
        elif token == self.tokens['STR']:
            self.consome('STR')
        else:
            self.throwError("Erro na função fator")
        return

    #---------
    # the end
    #---------	  
    
if __name__ == "__main__":
    import lexico, sys

    if len(sys.argv) > 1:
        
        lista = lexico.main(sys.argv[1])
        AnSint = conversorIntermediario(lista)
        listaDoInterpretador = AnSint.function()
        print("Lista de instruções gerada pelo sintático:")
        print(listaDoInterpretador)