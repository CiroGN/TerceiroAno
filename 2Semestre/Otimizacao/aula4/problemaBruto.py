import pyomo.environ as Pyo

EXEC_PATH = "C:\glpk-4.65\w64\glpsol.exe"

# Criando o Modelo
Modelo = Pyo.ConcreteModel()

# [V.D.s]
Modelo.X_t = Pyo.Var(within = Pyo.NonNegativeReals) # X_t >=0 e inteira
Modelo.X_s = Pyo.Var(within = Pyo.NonNegativeReals) # X_s >=0 e inteira
Modelo.X_p = Pyo.Var(within = Pyo.NonNegativeReals) # X_p >=0 e inteira

# [F.O.]
Modelo.FO = Pyo.Objective(expr = 6.749*Modelo.X_t + 7*Modelo.X_s + 8*Modelo.X_p, sense=Pyo.maximize)

# [Restrições]

Modelo.R_Alum = Pyo.Constraint(expr = (0.3*Modelo.X_t + 0.2*Modelo.X_s + \
                                       0.1*Modelo.X_p) <= 10000)
Modelo.R_Inj = Pyo.Constraint(expr = (0.003*Modelo.X_t + 0.005*Modelo.X_s + \
                                       0.007*Modelo.X_p) <= 1600)
Modelo.R_Fur = Pyo.Constraint(expr = (0.007*Modelo.X_t + 0.008*Modelo.X_s + \
                                       0.010*Modelo.X_p) <= 800)
Modelo.R_Afi = Pyo.Constraint(expr = (0.033*Modelo.X_t + 0.005*Modelo.X_s + \
                                       0.002*Modelo.X_p) <= 600)

Otimizador = Pyo.SolverFactory('glpk', executable = EXEC_PATH)
Resultado = Otimizador.solve(Modelo)

# Imprimindo resultados
print(f'Status da otimização:', Resultado.solver.status)
print(f'Critério de Parada:', Resultado.solver.termination_condition)

print(f'Solução Ótima:', Pyo.value(Modelo.FO))
print(f'X_t = ',Pyo.value(Modelo.X_t))
print(f'X_s = ',Pyo.value(Modelo.X_s))
print(f'X_p = ',Pyo.value(Modelo.X_p))

print()
print(f'R[Aluminio] = ' + str(Pyo.value(Modelo.R_Alum.body)) + \
      ' <= ' + str(Modelo.R_Alum.upper))
print(f'R[Injeção] = ' + str(Pyo.value(Modelo.R_Inj.body)) + \
      ' <= ' + str(Modelo.R_Inj.upper))
print(f'R[Furação] = ' + str(Pyo.value(Modelo.R_Fur.body)) + \
      ' <= ' + str(Modelo.R_Fur.upper))
print(f'R[Afinação] = ' + str(Pyo.value(Modelo.R_Afi.body)) + \
      ' <= ' + str(Modelo.R_Afi.upper))