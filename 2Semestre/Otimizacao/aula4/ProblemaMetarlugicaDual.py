import pyomo.environ as Pyo

#Apenas no Windows
EXEC_PATH = "C:\glpk-4.65\w64\glpsol.exe"

Modelo = Pyo.ConcreteModel()

Modelo.Y_Alu = Pyo.Var(within = Pyo.NonNegativeReals)
Modelo.Y_Inj = Pyo.Var(within = Pyo.NonNegativeReals)
Modelo.Y_Fur = Pyo.Var(within = Pyo.NonNegativeReals)
Modelo.Y_Afi = Pyo.Var(within = Pyo.NonNegativeReals)

# FO
Modelo.FO_Dual = Pyo.Objective(expr = (10000*Modelo.Y_Alum + 1600*Modelo.Y_Inj + 800*Modelo.Y_Fur + 600*Modelo.Y_Afi), sense = Pyo.minimize)

# Restrições
Modelo.R_Tampa = Pyo.Constraint(expr = (0.3*Modelo.Y_Alu + 0.003*Modelo.Y_Inj + 0.007*Modelo.Y_Fur + 0.033*Modelo.Y_Afi) >= 5)
Modelo.R_Sup = Pyo.Constraint(expr = (0.2*Modelo.Y_Alu + 0.005*Modelo.Y_Inj + 0.008*Modelo.Y_Fur + 0.005*Modelo.Y_Afi) >= 7)
Modelo.R_Plac = Pyo.Constraint(expr = (0.1*Modelo.Y_Alu + 0.007*Modelo.Y_Inj + 0.010*Modelo.Y_Fur + 0.002*Modelo.Y_Afi) >= 8)

Otimizador = Pyo.SolverFactory('glpk', executable = EXEC_PATH)
Resultado = Otimizador.solve(Modelo)

print(f'Status da otimização:', Resultado.solver.status)
print(f'Critério de Parada:', Resultado.solver.termination_condition)

print(f'\nSolução Ótima = ', Pyo.value(Modelo.FO))


print(f'Y_Alu = ', Pyo.value(Modelo.Y_Alu))
print(f'Y_Inj = ', Pyo.value(Modelo.Y_Inj))
print(f'Y_Fur = ', Pyo.value(Modelo.Y_Fur))
print(f'Y_Afi = ', Pyo.value(Modelo.Y_Afi))

