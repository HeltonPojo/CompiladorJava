# Objetivo

Esse projeto é um trabalho de compiladores no qual o objetivo é desenvolver um interpretador de java--.

# Etapas

## - [x] Analisador Lexico

Desenvolver uma classe capaz de de dado um código de entrada retorna uma lista de tuplas no seguinte formato:
`[(tokenId, lexema, linha, coluna)]`

## - [x] Analisador Sintatico

Desenvolver uma classe com métodos baseados na gramática fornecida `java.gmr` para que seja possivel analisar se a sequencia de tokens fornecidos pelo analisador lexico faz sentido.

> Caso ocorra algum erro o compilador deve retornar o lexema a linha e coluna onde o erro ocorreu

## - [ ] Conversão em código para o Interpretador

## - [ ] Interpretador

# Modos de Uso

Esse projeto não contém depencias e portanto todos os códigos podem ser executados das seguintes formas

## Analisador Lexico

`cd ./compilador`
`python lexico.py ./../testes/errado1.java`

## Analisador Sintatico

`cd ./compilador`
`python sintatico.py ./../testes/errado1.java`

## Teste

`cd ./compilador`
`python teste.py`
