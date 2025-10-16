import pyomo.environ as pyo
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

J = [1,2,3,4,5]

# parâmetros
cost = {1:22, 2:20, 3:25, 4:24, 5:27}
tin  = {1:0.60, 2:0.25, 3:0.45, 4:0.20, 5:0.50}
zinc = {1:0.10, 2:0.15, 3:0.45, 4:0.50, 5:0.40}
lead = {1:0.30, 2:0.60, 3:0.10, 4:0.30, 5:0.10}

# variáveis (fração de 1 lb)
model.x = pyo.Var(J, domain=pyo.NonNegativeReals)

# objetivo
model.obj = pyo.Objective(expr=sum(cost[j]*model.x[j] for j in J), sense=pyo.minimize)

# restrições de composição
model.tin_constr  = pyo.Constraint(expr=sum(tin[j]*model.x[j]  for j in J) == 0.40)
model.zinc_constr = pyo.Constraint(expr=sum(zinc[j]*model.x[j] for j in J) == 0.35)
model.lead_constr = pyo.Constraint(expr=sum(lead[j]*model.x[j] for j in J) == 0.25)

# (opcional) balanço de massa
model.mass = pyo.Constraint(expr=sum(model.x[j] for j in J) == 1.0)

# solver (ajuste se precisar especificar caminho)
solver = SolverFactory('glpk')
res = solver.solve(model, tee=False)

print("Status:", res.solver.status, res.solver.termination_condition)
print("Custo mínimo por lb: $", pyo.value(model.obj))
for j in J:
    v = pyo.value(model.x[j])
    if v is None: v = 0.0
    if v > 1e-8:
        print(f"x{j} = {v:.9f} lb")
