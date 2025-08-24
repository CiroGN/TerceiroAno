import pyomo.environ as Pyo

EXEC_PATH = "C:\glpk-4.65\w64\glpsol.exe"

Modelo = Pyo.ConcreteModel()

# Conjuntos
P = ['Carrinho', 'Triciclo']
R = ['Usinagem', 'Pintura', 'Montagem']

# Parâmetros
L_i = {('Carrinho'):12, ('Triciclo'):60}
D_j = {('Usinagem'):36, ('Pintura'):22, ('Montagem'):15}
t_ij = {('Carrinho','Usinagem'):0.25, ('Carrinho','Pintura'):0.10, ('Carrinho','Montagem'):0.10,\
        ('Triciclo','Usinagem'):0.50, ('Triciclo','Pintura'):0.75, ('Triciclo','Montagem'):0.40}

# [V.D.]
Modelo.X = Pyo.Var(P, within=Pyo.NonNegativeReals) # X_i >=0 \forall i \in P

# [F.O.]
Modelo.FO = Pyo.Objective(expr = sum(L_i[i] * Modelo.X[i] for i in P), sense=Pyo.maximize)

# Restrições
Modelo.R = Pyo.ConstraintList()
for j in R:
    Modelo.R.add(expr = sum(t_ij[i,j] * Modelo.X[i] for i in P) <= D_j[j])

Otimizador = Pyo.SolverFactory('glpk', executable = EXEC_PATH)
Resultado = Otimizador.solve(Modelo)

# Imprimindo resultados
print(f'Status da otimização:', Resultado.solver.status)
print(f'Critério de Parada:', Resultado.solver.termination_condition)

print(f'Solução ótima = ', Pyo.value(Modelo.FO))

for i in P:
    print(str(Modelo.X[i]) + ' = ' + str(Pyo.value(Modelo.X[i])))

for j in Modelo.R:
    print(str(Modelo.R[j]) + ' = ' + str(Pyo.value(Modelo.R[j].body)) + ' <= ' +\
          str(Pyo.value(Modelo.R[j].upper)))