import pyomo.environ as Pyo

EXEC_PATH = "C:\glpk-4.65\w64\glpsol.exe"

Modelo = Pyo.ConcreteModel()

# [V.D.]
Modelo.X_c = Pyo.Var(within=Pyo.NonNegativeIntegers) # X_c >= 0 e inteiro
Modelo.X_t = Pyo.Var(within=Pyo.NonNegativeIntegers) # X_t >= 0 e inteiro

# [F.O.]
Modelo.FO = Pyo.Objective(expr = 12*Modelo.X_c + 60*Modelo.X_t, sense=Pyo.maximize) # MAX Z = 12*X_c + 60*X_t

# [Restrições]
Modelo.R_Usinagem = Pyo.Constraint(expr = 0.25*Modelo.X_c + 0.50*Modelo.X_t <= 36)
Modelo.R_Pintura = Pyo.Constraint(expr = 0.10*Modelo.X_c + 0.75*Modelo.X_t <= 22)
Modelo.R_Montagem = Pyo.Constraint(expr = 0.10*Modelo.X_c + 0.40*Modelo.X_t <= 15)

Otimizador = Pyo.SolverFactory('glpk', executable = EXEC_PATH)
Resultado = Otimizador.solve(Modelo)

# Imprimindo resultados
print(f'Status da otimização:', Resultado.solver.status)
print(f'Critério de Parada:', Resultado.solver.termination_condition)

print(f'Solução Ótima:', Pyo.value(Modelo.FO))
print(f'X_c = ',Pyo.value(Modelo.X_c))
print(f'X_t = ',Pyo.value(Modelo.X_t))