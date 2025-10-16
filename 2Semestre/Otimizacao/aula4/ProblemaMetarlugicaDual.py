import pyomo.environ as Pyo

EXEC_PATH = "C:\glpk-4.65\w64\glpsol.exe"

# Criando o Modelo
Modelo = Pyo.ConcreteModel()

# [V.D.s]
Modelo.Y_Alu = Pyo.Var(within = Pyo.NonNegativeReals) # Y_Alu >=0
Modelo.Y_Inj = Pyo.Var(within = Pyo.NonNegativeReals) # Y_Inj >=0
Modelo.Y_Fur = Pyo.Var(within = Pyo.NonNegativeReals) # Y_Fur >=0
Modelo.Y_Afi = Pyo.Var(within = Pyo.NonNegativeReals) # Y_Afi >=0

# [F.O.]
Modelo.FO_Dual = Pyo.Objective(expr = (10000*Modelo.Y_Alu + 1600*Modelo.Y_Inj+\
                                       800*Modelo.Y_Fur + 600*Modelo.Y_Afi),\
                                        sense=Pyo.minimize)

# [Restrições]
Modelo.R_Tampa = Pyo.Constraint(expr = (0.3*Modelo.Y_Alu + 0.003*Modelo.Y_Inj +\
                                        0.007*Modelo.Y_Fur + 0.033*Modelo.Y_Afi) >= 5)

Modelo.R_Sup = Pyo.Constraint(expr = (0.2*Modelo.Y_Alu + 0.005*Modelo.Y_Inj +\
                                        0.008*Modelo.Y_Fur + 0.005*Modelo.Y_Afi) >= 7)

Modelo.R_Plaq = Pyo.Constraint(expr = (0.1*Modelo.Y_Alu + 0.007*Modelo.Y_Inj +\
                                        0.010*Modelo.Y_Fur + 0.002*Modelo.Y_Afi) >= 8)

Otimizador = Pyo.SolverFactory('glpk', executable = EXEC_PATH)
Resultado = Otimizador.solve(Modelo)

# Imprimindo resultados
print(f'Status da otimização:', Resultado.solver.status)
print(f'Critério de Parada:', Resultado.solver.termination_condition)

print(f'Solução Ótima:', Pyo.value(Modelo.FO_Dual))
print(f'Y_Alu = ',Pyo.value(Modelo.Y_Alu))
print(f'Y_Inj = ',Pyo.value(Modelo.Y_Inj))
print(f'Y_Fur = ',Pyo.value(Modelo.Y_Fur))
print(f'Y_Afi = ',Pyo.value(Modelo.Y_Afi))

print()
print(f'R[Tampa] = ' + str(Pyo.value(Modelo.R_Tampa.body)) + \
      ' >= ' + str(Modelo.R_Tampa.lower))
print(f'R[Sup] = ' + str(Pyo.value(Modelo.R_Sup.body)) + \
      ' >= ' + str(Modelo.R_Sup.lower))
print(f'R[Plaq] = ' + str(Pyo.value(Modelo.R_Plaq.body)) + \
      ' >= ' + str(Modelo.R_Plaq.lower))