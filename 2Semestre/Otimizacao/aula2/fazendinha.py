import pyomo.environ as Pyo

EXEC_PATH = "C:\glpk-4.65\w64\glpsol.exe"

# Definindo o conjunto
P = ['Milho', 'Soja', 'Trigo'] # i \in P

# Definição dos parâmetros
c_i = {('Milho'):2000, ('Soja'):1400, ('Trigo'):2400} # custo de plantio em $/ha
t_i = {('Milho'):20, ('Soja'):24, ('Trigo'):30} # trabalho para o plantio em homem-dia/ha
L_i = {('Milho'):600, ('Soja'):400, ('Trigo'):800} # lucro em $/ha
A = 400
B = 800000
T = 9000

# Definindo o ambiente
Modelo = Pyo.ConcreteModel()

# [V.D]
Modelo.X_i = Pyo.Var(P, within=Pyo.NonNegativeReals) # X_i >=0, i \in P

# [F.O.]
Modelo.FO = Pyo.Objective(expr = sum(L_i[i] * Modelo.X_i[i] for i in P), \
                          sense = Pyo.maximize)

# Restrições
Modelo.R_Area = Pyo.Constraint(expr = sum(Modelo.X_i[i] for i in P) <= A)
Modelo.R_Trabalho = Pyo.Constraint(expr = sum(t_i[i] * Modelo.X_i[i] for i in P) <= T)
Modelo.R_Orcamento = Pyo.Constraint(expr = sum(c_i[i] * Modelo.X_i[i] for i in P) <= B)

Otimizador = Pyo.SolverFactory('glpk', executable = EXEC_PATH)
Resultado = Otimizador.solve(Modelo)

# Status
print(f'Status da otimização:', Resultado.solver.status)
print(f'Critério de Parada:', Resultado.solver.termination_condition)

# Solução ótima
print(f'\nLucro Máximo = ', Pyo.value(Modelo.FO))

# Valor das V.Ds
for i in P:
    print(str(Modelo.X_i[i]) + ' = ' + str(Pyo.value(Modelo.X_i[i])))

# LHS das Restrições
print(f'Área Total Cultivada = ' + str(Pyo.value(Modelo.R_Area.body)))
print(f'Custo Total = ' + str(Pyo.value(Modelo.R_Orcamento.body)))
print(f'Força de Trabalho Total = ' + str(Pyo.value(Modelo.R_Trabalho.body)))