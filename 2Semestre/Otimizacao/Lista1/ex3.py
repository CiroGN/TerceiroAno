import pyomo.environ as pyo
from pyomo.opt import SolverFactory

# Dados
months = [1,2,3,4,5]
demand = {1:30000, 2:20000, 3:40000, 4:10000, 5:50000}
cost = {1:65, 2:100, 3:135, 4:160, 5:190}

# Conjuntos de pares (i,k) válidos
pairs = [(i,k) for i in months for k in cost.keys() if i + k - 1 <= 5]

model = pyo.ConcreteModel()

# Índice para pares
model.P = pyo.Set(initialize=pairs, dimen=2)

# Variáveis y[i,k] >= 0
model.y = pyo.Var(model.P, domain=pyo.NonNegativeReals)

# Objetivo
model.obj = pyo.Objective(
    expr=sum(cost[k] * model.y[i,k] for (i,k) in model.P),
    sense=pyo.minimize
)

# Restrições de demanda
def demand_rule(m, t):
    return sum(m.y[i,k] for (i,k) in m.P if i <= t <= i+k-1) >= demand[t]
model.demand_constr = pyo.Constraint(months, rule=demand_rule)

# Solver (ajuste o caminho do executável se necessário)
# Otimizador = SolverFactory('glpk', executable="C:\\caminho\\glpsol.exe")
Otimizador = SolverFactory('glpk')  # assume glpk disponível no PATH
res = Otimizador.solve(model, tee=False)

print("Status:", res.solver.status, res.solver.termination_condition)
print("Custo mínimo:", pyo.value(model.obj))
for (i,k) in model.P:
    val = pyo.value(model.y[i,k])
    if val is None:
        val = 0.0
    if val > 1e-6:
        print(f"y[{i},{k}] = {val:,.0f} sq.ft.  (inicia no mês {i}, duração {k} meses)")
