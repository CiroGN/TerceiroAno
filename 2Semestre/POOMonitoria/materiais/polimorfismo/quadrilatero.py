from abc import ABC, abstractmethod

class Quadrilatero(ABC):
    def __init__(self, b, a):
        self.base = b
        self.altura = a
    @abstractmethod
    def calcular_area(self):
        pass

class Retangulo(Quadrilatero):
    def __init__(self, b, a):
        super().__init__(b, a)
    def calcular_area(self):
        return self.base * self.altura

class Quadrado(Quadrilatero):
    def __init__(self, b):
        super().__init__(b, b)
    def calcular_area(self):
        return self.base ** 2
    
class Paralelogramo(Quadrilatero):
    def __init__(self, b, a, angulo):
        super().__init__(b, a)
        self.angulo = angulo
    def calcular_area(self):
        from math import sin, radians
        return self.base * self.altura * sin(radians(self.angulo))
    
class Trapezio(Quadrilatero):
    def __init__(self, B, b, a):
        super().__init__(b, a)
        self.base_maior = B
    def calcular_area(self):
        return (self.base_maior + self.base) * self.altura / 2

# Teste de polimorfismo
formas = [
    Retangulo(10, 5),
    Quadrado(6),
    Paralelogramo(8, 4, 30), #base, altura, angulo 
    Trapezio(10, 6, 4) #base_maior, base_menor, altura
]

for f in formas:
    print(f"{f.__class__.__name__}:")
    print(f"  Área = {f.calcular_area():.2f}")
