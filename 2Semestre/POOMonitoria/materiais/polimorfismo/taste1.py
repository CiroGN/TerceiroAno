from teste import Calculo

class jfhwsk(Calculo):
    pass

class Soma(Calculo):
    def calcular(self, a, b):
        print(a + b)

class Subtracao(Calculo):
    def __init__(self):
        pass
    def calcular(self, a, b):
        print(a - b)

soma = Soma()
soma.calcular(1, 2)
subtracao = Subtracao()
subtracao.calcular(1, 2)

srgs = jfhwsk()
print(srgs.calcular())