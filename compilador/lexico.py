import sys
import codecs

tokens_encontrados = []
def ler_arquivo(nome_arquivo):
    with open(nome_arquivo, "r") as arquivo:
        return arquivo.readlines()

def ler_tokens(nome_arquivo_tokens):
    with open(nome_arquivo_tokens, "r") as arquivo_tokens:
        return arquivo_tokens.readlines()

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def verificar_tokens(palavra_tkn, lista_tokens):
    linha_atual = 0
    for linha in lista_tokens:
        linha_atual += 1
        if palavra_tkn == linha.strip():
            return linha_atual, True
    return linha_atual, False

def throwError(linha, palavra_tkn, index):
    print(tokens_encontrados)
    print("Linha:", linha)
    print("Coluna:", index)
    print("Lexema:", palavra_tkn)
    raise Exception("Erro de token não identificado")

def appendTokensEncotrados(palavra_tkn, lista_tokens, linha, index):
    tokenId, isToken = verificar_tokens(palavra_tkn, lista_tokens)
    if isToken:
        tokens_encontrados.append((tokenId, palavra_tkn, linha, index))
        return
    elif palavra_tkn:
        # is ident 44
        if palavra_tkn[0].isalpha() and palavra_tkn.isalnum():
            tokens_encontrados.append((44, palavra_tkn, linha, index))
        # is hexa 45
        elif palavra_tkn[0] == "0" and palavra_tkn[1] == "x":
            for i, char in enumerate(palavra_tkn):
                if i > 1:
                    if (not char.isnumeric()) and (char not in ("A", "B", "C", "D", "E", "F")):
                        throwError(linha, palavra_tkn, index)
            tokens_encontrados.append((45, palavra_tkn, linha, index))
        # is octal 46
        elif palavra_tkn[0] == "0" :
            for char in palavra_tkn:
                if int(char) > 7:
                    throwError(linha, palavra_tkn, index)
            tokens_encontrados.append((46, palavra_tkn, linha, index))
        # is int 48
        elif palavra_tkn.isnumeric():
            tokens_encontrados.append((48, palavra_tkn, linha, index))
        # is number float 47
        elif not palavra_tkn.isalpha():
            numPoints = 0
            for char in palavra_tkn:
                if char == ".":
                    numPoints+=1
                if (not char.isnumeric() and char != ".") or numPoints > 1:
                    throwError(linha, palavra_tkn, index)
            if palavra_tkn[-1:] == ".":
                throwError(linha, palavra_tkn, index)
            tokens_encontrados.append((47, palavra_tkn, linha, index))
        else:
            throwError(linha, palavra_tkn, index)

def parser(arquivo, lista_tokens):
    linha_atual = 0
    aspas_abertas = ""
    string_lex = ""
    for linha in arquivo:
        linha_atual += 1
        palavra = ""
        pularLinha = False
        for index, caracter in enumerate(linha.strip()):
            #Tratamento de comentario
            if (palavra == "//" and aspas_abertas == "") or pularLinha:
                palavra = ""
                pularLinha = True
            else:
                if aspas_abertas == caracter:
                    string_lex += caracter
                    aspas_abertas = ""
                    tokens_encontrados.append((43, codecs.decode(string_lex, "unicode-escape"), linha_atual, index - (len(string_lex) - 1)))
                    string_lex = ""
                elif caracter == '"' and aspas_abertas == "":
                    aspas_abertas = caracter
                    string_lex += caracter
                elif aspas_abertas != "":
                    string_lex += caracter
                else :
                    if caracter in (" ", ";", ",", "{", "}", "(", ")", ".", "-" , "+","-","*","/","%","!",">","<","="):
                        copiaPalavra = palavra
                        copiaPalavra += caracter
                        if len(linha.strip()) > index + 1 and linha.strip()[index+1] in ("=", "/", "|", "&"):
                            copiaPalavra += linha.strip()[index+1]
                        # tratamento para float
                        if palavra.isnumeric() and caracter == ".":
                            palavra += caracter
                        # tratamento para esse tokens com caracter duplos
                        elif copiaPalavra in ("||","&&","==","!=",">=","<=","+=","-=","*=","/=","%=", "//"):
                            palavra += caracter
                        # para inserir plavars nos tokens encontrados
                        else:
                            appendTokensEncotrados(palavra, lista_tokens, linha_atual, index - len(palavra))
                            palavra = ""
                            if caracter != " ":
                                if caracter in ("+","-","*","/","%","!",">","<","="):
                                    palavra = caracter
                                else:
                                    appendTokensEncotrados(caracter, lista_tokens, linha_atual, index - len(palavra))
                    else:
                        if (caracter.isalnum()) and (not palavra.isalnum()) and (not is_float(palavra)):
                            appendTokensEncotrados(palavra, lista_tokens, linha_atual, index - len(palavra))
                            palavra = caracter
                        else:
                            palavra += caracter
        if string_lex != "" or aspas_abertas != "":
            raise Exception("String não finalizada")
        if palavra != "": appendTokensEncotrados(palavra, lista_tokens, linha_atual, len(linha.strip()) - len(palavra))
    return tokens_encontrados


def main(nome_arquivo):
    nome_arquivo_tokens = "tokens.txt"

    arquivo = ler_arquivo(nome_arquivo)
    lista_tokens = ler_tokens(nome_arquivo_tokens)

    tokens_encontrados = parser(arquivo, lista_tokens)

    lista_lexica = []
    for token_linha, lexima, linha, coluna in tokens_encontrados:
        lista_lexica.append((token_linha, lexima, linha, coluna))
    return lista_lexica


if __name__ == "__main__":
    if len(sys.argv) > 1:
        lista = main(sys.argv[1])
        for i in lista:
            print(i)
