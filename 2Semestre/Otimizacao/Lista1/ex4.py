import pyomo.environ as pyo
from pyomo.opt import SolverFactory # ajuda no lugar de declarar o caminho toda vez

# Modelo
model = pyo.ConcreteModel()

years = [1,2,3,4,5]

# Variáveis
model.A = pyo.Var(years, domain=pyo.NonNegativeReals)
model.B = pyo.Var(years, domain=pyo.NonNegativeReals)
model.C2 = pyo.Var(domain=pyo.NonNegativeReals)  # só t=2
model.D5 = pyo.Var(domain=pyo.NonNegativeReals)  # só t=5
model.R = pyo.Var(years, domain=pyo.NonNegativeReals)  # R1..R5 (reservas após investir no ano t)

# Parâmetro inicial
S1 = 60000.0

# Restrições de fluxo
model.flow1 = pyo.Constraint(expr= model.A[1] + model.B[1] + model.R[1] == S1)

model.flow2 = pyo.Constraint(expr= model.A[2] + model.B[2] + model.C2 + model.R[2] == model.R[1])

model.flow3 = pyo.Constraint(expr= model.A[3] + model.B[3] + model.R[3] == model.R[2] + 1.4*model.A[1])

model.flow4 = pyo.Constraint(expr= model.A[4] + model.B[4] + model.R[4] == model.R[3] + 1.4*model.A[2] + 1.7*model.B[1])

model.flow5 = pyo.Constraint(expr= model.A[5] + model.B[5] + model.D5 + model.R[5] == model.R[4] + 1.4*model.A[3] + 1.7*model.B[2])

# Objetivo: maximizar valor no início do ano 6
model.obj = pyo.Objective(expr= model.R[5] + 1.4*model.A[4] + 1.7*model.B[3] + 1.9*model.C2 + 1.3*model.D5,
                          sense=pyo.maximize)

# Resolver (ajuste o solver/executable conforme seu sistema)
solver = SolverFactory('glpk')
res = solver.solve(model, tee=False)

print("Status:", res.solver.status, res.solver.termination_condition)
print("Valor acumulado no início do ano 6:", pyo.value(model.obj))

# Mostrar investimentos não nulos
for t in years:
    a = pyo.value(model.A[t])
    b = pyo.value(model.B[t])
    r = pyo.value(model.R[t])
    if a and a > 1e-6:
        print(f"A_{t} = {a:,.2f}")
    if b and b > 1e-6:
        print(f"B_{t} = {b:,.2f}")
    if r and r > 1e-6:
        print(f"R_{t} = {r:,.2f}")
if pyo.value(model.C2) > 1e-6:
    print("C2 =", pyo.value(model.C2))
if pyo.value(model.D5) > 1e-6:
    print("D5 =", pyo.value(model.D5))
