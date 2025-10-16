import pyomo.environ as Pyo
from pyomo.opt import SolverStatus, TerminationCondition

#Apenas no Windows
EXEC_PATH = "C:\glpk-4.65\w64\glpsol.exe"

#Definindo os conjuntos
C = ['Milho', 'Arroz', 'Feijao'] # i
F = ['Fazenda 1', 'Fazenda 2', 'Fazenda 3'] # j

#Definindo os Parâmetros
L = {('Milho') : 5000, ('Arroz') : 4000, ('Feijao') : 1900} # Lucro por cultura
A = {('Fazenda 1') : 400, ('Fazenda 2') : 650, ('Fazenda 3') : 350} # Área disponível em cada fazenda
alfa = {('Milho') : 5.5, ('Arroz') : 4.0, ('Feijao') : 3.5} # consumo de água por acre cultivado com cada cultura
W = {('Fazenda 1') : 1800, ('Fazenda 2') : 2201, ('Fazenda 3') : 950} # Água disponível por fazenda
U = {('Milho') : 660, ('Arroz') : 880, ('Feijao') : 440} # Área máxima por cultura

#Criando o Modelo
Modelo = Pyo.ConcreteModel()

#Declarando as Variáveis de Decisão
Modelo.X = Pyo.Var(C, F, within=Pyo.NonNegativeReals) # X_ij >= 0

#Modelando a Função Objetivo
Modelo.FO = Pyo.Objective(expr = sum(L[i] * sum(Modelo.X[i,j] for j in F) for i in C), sense=Pyo.maximize)

#Modelando as Restrições

# 1 - Área por Fazenda
Modelo.R_AreaFazenda = Pyo.ConstraintList()
for j in A:
    Modelo.R_AreaFazenda.add(expr = sum(Modelo.X[i,j] for i in C) <= A[j])

# 2 - Água por Fazenda
Modelo.R_AguaFazenda = Pyo.ConstraintList()
for j in W:
    Modelo.R_AguaFazenda.add(expr = sum(alfa[i] * Modelo.X[i,j] for i in C) <= W[j])

# 3 - Área por Cultura
Modelo.R_AreaCultura = Pyo.ConstraintList()
for i in U:
    Modelo.R_AreaCultura.add(expr = sum(Modelo.X[i,j] for j in F) <= U[i])

# 4 - Proporção de Áreas por Fazenda
Modelo.R_ProporcaoAreas = Pyo.ConstraintList()
u = 0
for j in A:
    u += 1
    v = 0
    for k in A:
        v += 1
        if (v - u) ==  1:
            Modelo.R_ProporcaoAreas.add(expr = sum(Modelo.X[i,j] for i in C)/A[j] == sum(Modelo.X[i,k] for i in C)/A[k])

Modelo.pprint()

#Setup do Solver
Solver = Pyo.SolverFactory('glpk', executable=EXEC_PATH)

#Resolvendo o Modelo
Solucao = Solver.solve(Modelo)
Pyo.assert_optimal_termination(Solucao)

# Imprimindo a Solução
if (Solucao.Solver.status == SolverStatus.ok) and (Solucao.Solver.termination_condition == TerminationCondition.optimal):
    #Solução Ótima Encontrada
    print() # pula uma linha
    print('Solucao Otima = $', round(Pyo.value(Modelo.FO),2)) # $ ------,00
    print() # pula uma linha

    #Imprimindo a solução ótima nas VD's
    for v in Modelo.component_objects(ctype=Pyo.Var):
        for index in v:
            print('{0} == {1}'.format(v[index], round(Pyo.value(v[index]),2)))
    print() # pula uma linha

    #Imprimindo as Restrições
    print('Área por Fazenda')
    f = 0 
    for j in A:
        f += 1
        LHS_Area_Fazenda = sum(Pyo.value(Modelo.X[i,j]) for i in C)
        print('Fazenda ' + str(f) + ':' + str(round(LHS_Area_Fazenda,2)) + " <= " + str(A[j]) + '  Percentual = ' + str(round(100*LHS_Area_Fazenda/A[j],2)) + "%")

    print() # pula uma linha
    print('Consumo de Água por Fazenda')
    f = 0 
    for j in W:
        f += 1
        LHS_Agua_Fazenda = sum(Pyo.value(alfa[i]*Modelo.X[i,j]) for i in C)
        print('Fazenda ' + str(f) + ':' + str(round(LHS_Agua_Fazenda,2)) + " <= " + str(W[j]) + '  Percentual = ' + str(round(100*LHS_Agua_Fazenda/W[j],2)) + "%")

    print() # pula uma linha
    print('Área por Cultura')
    c = 0
    for i in U:
        LHS_Area_Cultura = sum(Pyo.value(Modelo.X[i,j]) for j in F)
        print(str(list(U.keys())[c]) + ' : ' + str(round(LHS_Area_Cultura,2)) + " <= " + str(U[i]))
        c += 1
else:
    print('Deu ruim')