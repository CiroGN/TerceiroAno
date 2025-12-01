from abc import ABC, abstractmethod
class Calculo(ABC):
    @abstractmethod
    def calcular(self):
        return "calclulando"