class Interpretador:
    def __init__(self, instrucoes):
        self.variaveis = {}
        self.labels = {}
        self.ponteiro = 0
        self.instrucoes = instrucoes

    def carregar_labels(self):
        for i, instrucao in enumerate(self.instrucoes):
            if instrucao[0] == "LABEL":
                self.labels[instrucao[1]] = i

    def executar(self):
        while self.ponteiro < len(self.instrucoes):
            instrucao = self.instrucoes[self.ponteiro]
            operador = instrucao[0]
            if operador in ("+", "-", "*", "/", "mod", "div"):
                self.operacao_aritmetica(instrucao)
            elif operador in ("or", "and", "not"):
                self.operacao_logica(instrucao)
            elif operador in ("==", "<>", ">", "<", ">=", "<="):
                self.operacao_relacional(instrucao)
            elif operador == ":=":
                self.atribuicao(instrucao)
            elif operador == "IF":
                self.condicional(instrucao)
            elif operador == "JUMP":
                self.jump(instrucao)
            elif operador == "CALL":
                self.chamada_sistema(instrucao)
            elif operador == "LABEL":
                pass
            else:
                raise ValueError(f"Operador desconhecido: {operador}")
            self.ponteiro += 1
        print(self.labels)
        print(self.variaveis)

    def operacao_aritmetica(self, instrucao):
        operador, guardar, operando1, operando2 = instrucao
        numero1 = 0
        numero2 = 0
        numero1 = (
            operando1
            if isinstance(operando1, int)
            else float(self.variaveis.get(operando1, 0))
        )
        numero2 = (
            operando2
            if isinstance(operando2, int)
            else float(self.variaveis.get(operando2, 0))
        )

        if operador == "+":
            self.variaveis[guardar] = numero1 + numero2
        elif operador == "-":
            self.variaveis[guardar] = numero1 - numero2
        elif operador == "*":
            self.variaveis[guardar] = numero1 * numero2
        elif operador == "/":
            self.variaveis[guardar] = numero1 / numero2
        elif operador == "mod":
            self.variaveis[guardar] = numero1 % numero2
        elif operador == "div":
            self.variaveis[guardar] = numero1 // numero2

    def operacao_logica(self, instrucao):
        operador, guardar, operando1, operando2 = instrucao
        if operador == "or":
            self.variaveis[guardar] = self.variaveis.get(
                operando1, False
            ) or self.variaveis.get(operando2, False)
        elif operador == "and":
            self.variaveis[guardar] = self.variaveis.get(
                operando1, False
            ) and self.variaveis.get(operando2, False)
        elif operador == "not":
            self.variaveis[guardar] = not self.variaveis.get(operando1, False)

    def operacao_relacional(self, instrucao):
        operador, guardar, operando1, operando2 = instrucao
        numero1 = 0
        numero2 = 0

        numero1 = (
            operando1
            if isinstance(operando1, int)
            else float(self.variaveis.get(operando1, 0))
        )
        numero2 = (
            operando2
            if isinstance(operando2, int)
            else float(self.variaveis.get(operando2, 0))
        )

        if operador == "==":
            self.variaveis[guardar] = numero1 == numero2
        elif operador == "<>":
            self.variaveis[guardar] = numero1 != numero2
        elif operador == ">":
            self.variaveis[guardar] = numero1 > numero2
        elif operador == "<":
            self.variaveis[guardar] = numero1 < numero2
        elif operador == ">=":
            self.variaveis[guardar] = numero1 >= numero2
        elif operador == "<=":
            self.variaveis[guardar] = numero1 <= numero2

    def atribuicao(self, instrucao):
        _, guardar, operando1, _ = instrucao
        self.variaveis[guardar] = self.variaveis.get(operando1, 0)

    def condicional(self, instrucao):
        _, condicao, label1, label2 = instrucao
        if self.variaveis.get(condicao, False):
            self.ponteiro = self.labels[label1] - 1
        else:
            self.ponteiro = self.labels[label2] - 1

    def jump(self, instrucao):
        _, label, _, _ = instrucao
        self.ponteiro = self.labels[label] - 1

    def chamada_sistema(self, instrucao):
        _, comando, valor, variavel = instrucao
        if comando == "PRINT":
            print(
                self.variaveis.get(variavel, "Variavel não atribuida")
                if isinstance(variavel, str)
                else valor
            )
        elif comando == "SCAN":
            self.variaveis[valor] = input()
