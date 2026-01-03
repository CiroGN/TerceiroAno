import random
import numpy as Np
import matplotlib.pyplot as Plt
import pyomo.environ as Pyo

# -------- Solver --------
EXEC_PATH = '/Users/thian/Desktop/Otimização 2024.2/glpk-4.65/w64/glpsol'

def Distancia_Euclidiana(Coordenas):
    n = len(Coordenadas)
    Dist = Np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i == j:
                Dist[i][j] = 10**10
            else:
                Dist[i][j] = int(Np.sqrt((Coordenadas[i][0] - Coordenadas[j][0])**2 +
                                     (Coordenadas[i][1] - Coordenadas[j][1])**2))
    return Dist

def Plotar_Rota(Coord, Rota, Custo):
    Plt.figure(figsize=(8,8))
    Coord_X = [c[0] for c in Coord]
    Coord_Y = [c[1] for c in Coord]

    Plt.scatter(Coord_X, Coord_Y, c='green')
    for i, (xx,yy) in enumerate(Coord):
        Plt.text(xx + 0.3, yy+0.3, str(i), fontsize=8)
    
    for (i,j) in Rota:
        Plt.plot([Coord[i][0],Coord[j][0]],
                  [Coord[i][1],Coord[j][1]], 'b-')
    Plt.title(f'Custo Ótimo = {Custo}')
    Plt.show()

def TSP_MTZ(c_ij):
    n = len(c_ij)
    V = range(n)

    Modelo = Pyo.ConcreteModel()

    #--- Variáveis de Decisão ---
    Modelo.X_ij = Pyo.Var(V, V, domain=Pyo.Binary) # X_ij: {0,1}
    Modelo.u_i = Pyo.Var(V, bounds=(1,n)) # u_i = {1, 2, ..., n}

    #--- Função Objetivo ---
    Modelo.Z = Pyo.Objective(expr = sum(c_ij[i][j] * Modelo.X_ij[i,j]
                                        for i in V for j in V))
    
    #--- Restrições ---
    Modelo.R_Saida = Pyo.ConstraintList()
    for i in V:
        Modelo.R_Saida.add(expr = (sum(Modelo.X_ij[i,j] for j in V)) == 1)

    Modelo.R_Chegada = Pyo.ConstraintList()
    for j in V:
        Modelo.R_Chegada.add(expr = (sum(Modelo.X_ij[i,j] for i in V)) == 1)

    #--- A rota sempre inicia no nó 1 ---
    Modelo.u_i[0].fix(1)

    Modelo.R_MTZ = Pyo.ConstraintList()
    BigM = n
    for i in V:
        for j in V:
            if i != j and j != 0:
                Modelo.R_MTZ.add(Modelo.u_i[j] >= Modelo.u_i[i] + 1 - BigM * (1 - Modelo.X_ij[i,j]))

    #Otimizador = Pyo.SolverFactory('glpk', executable = EXEC_PATH)
    Otimizador = Pyo.SolverFactory('gurobi')
    Resultado = Otimizador.solve(Modelo, tee=True)

    Rota = [(i,j) for i in V for j in V if Pyo.value(Modelo.X_ij[i,j]) > 0.5]

    Sequencia = [0]
    while len(Sequencia) < n:
        Anterior = Sequencia[-1]
        for (i,j) in Rota:
            if i == Anterior:
                Sequencia.append(j)
                break
    
    #--- Apurando o Custo da Rota ---
    Arestas = [(Sequencia[k], Sequencia[(k+1) % n]) for k in range(n)]
    Custo_Total = sum(c_ij[i][j] for (i,j) in Arestas)

    return Arestas, Custo_Total

if __name__ == "__main__":

    semente = 123
    random.seed(semente)
    Np.random.seed(semente)

    #---- Tamanho do Problema ----
    n = 100
    Coordenadas = [(int(random.uniform(0,100)),int((random.uniform(0,100)))) for _ in range(n)]

    #--- Parâmetros ---
    c_ij = Distancia_Euclidiana(Coordenadas)
    Rota_MTZ, Custo_MTZ = TSP_MTZ(c_ij)
    print(f'Rota = {Rota_MTZ}')
    print(f'Custo Total = {Custo_MTZ}')
    Plotar_Rota(Coordenadas,Rota_MTZ,Custo_MTZ)