import pyomo.environ as Pyo

EXEC_PATH = "C:\glpk-4.65\w64\glpsol.exe"

#Definição dos COnjuntos
C = {'Milho', 'Feijão', 'Arroz'} # i in C
F = {'Fazenda 1', 'Fazenda 2', 'Fazenda 3'} # j in F

# Parâmetros do Problema
L_i = {('Milho'):5000, ('Arroz'):4000, ('Feijão'):1800} #Lucro em R$/Acre
A_j = {('Fazenda 1'):400, ('Fazenda 2'):650, ('Fazenda 3'):350} # Área disponível em acres
W_j = {('Fazenda 1'):1800, ('Fazenda 2'):2200, ('Fazenda 3'):950}
w_i = {('Milho'):5.5, ('Arroz'):4.0, ('Feijão'):3.5} # Consumo de água por cultura em litros/acre
M_i = {('Milho'):660, ('Arroz'):880, ('Feijão'):440} # Área máxima por cultura, em acres

#Criando o Modelo
Modelo = Pyo.ConcreteModel()

# [V.D.]
Modelo.X_ij = Pyo.Var(C, F, within=Pyo.NonNegativeReals) # X_ij >= 0, i in C, j in F

# [F.O.]
Modelo.FO = Pyo.Objective(expr = sum( sum(L_i[i]*Modelo.X_ij[i,j] for j in F)for i in C), sense = Pyo.maximize)

# Restrição de Área por Fazendas
Modelo.R_AreaFazenda = Pyo.ConstraintList()
for j in F:
    Modelo.R_AreaFazenda.add(expr = sum(Modelo.X_ij[i,j]for i in C) <= A_j[j])

# Restrição de Água por Fazendas
Modelo.R_AguaFazenda = Pyo.ConstraintList()
for j in F:
    Modelo.R_AguaFazenda.add(expr = sum(w_i[i]*Modelo.X_ij[i,j] for i in C) <=W_j[j])

# Restrição de Área por Culturas
Modelo.R_AreaCulturas = Pyo.ConstraintList()
for i in C:
    Modelo.R_AreaCulturas.add(expr = sum(Modelo.X_ij[i,j] for j in F) <= M_i[i])

# Restrição de Proporção de Áreas
Modelo.R_ProporcaoAreas = Pyo.ConstraintList()
u = 0
for j in F:
    u += 1
    v = 0
    for k in F:
        v += 1
        if (v - u) == 1 and (k != j):
            print(f'v = {v}  -  u = {u}')
            Modelo.R_ProporcaoAreas.add(expr = ((1/A_j[j])*sum(Modelo.X_ij[i,j] for i in C) -
                                                (1/A_j[k])*sum(Modelo.X_ij[i,j] for i in C)) == 0)

Otimizador = Pyo.SolverFactory('glpk', executable = EXEC_PATH)
Resultado = Otimizador.solve(Modelo)

# Imprimindo resultados
print(f'Status da otimização:', Resultado.solver.status)
print(f'Critério de Parada:', Resultado.solver.termination_condition)

# Imprimindo a FO Ótima
print(f'Solução Ótima:', Pyo.value(Modelo.FO))

# Imprimindo a Solução
for v in Modelo.component_objects(ctype=Pyo.Var):
    for index in v:
        print('{0} == {1}'.format(v[index], round(Pyo.value(v[index], 2))))

Modelo.pprint()