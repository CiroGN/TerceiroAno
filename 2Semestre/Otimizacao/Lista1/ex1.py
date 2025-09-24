import pyomo.environ as pyo

EXEC_PATH = "C:\\glpk-4.65\\w64\\glpsol.exe"
# Modelo
model = pyo.ConcreteModel()

# Variáveis
model.x1 = pyo.Var(within=pyo.NonNegativeReals)  # lingotes
model.x2 = pyo.Var(within=pyo.NonNegativeReals)  # grafite
model.x3 = pyo.Var(within=pyo.NonNegativeReals)  # sucata

# Função objetivo (custos)
model.obj = pyo.Objective(expr=90*model.x1 + 180*model.x2 + 25*model.x3, sense=pyo.minimize)

# Restrição de demanda (10 toneladas de liga)
model.demand = pyo.Constraint(expr=(model.x1 + model.x2 + model.x3) == 10)

# Limites de estoque
model.stock1 = pyo.Constraint(expr=model.x1 <= 5)
model.stock2 = pyo.Constraint(expr=model.x2 <= 5)
model.stock3 = pyo.Constraint(expr=model.x3 <= 12)

# Carbono (0% a 9,5%)
model.carbon_min = pyo.Constraint(expr=(0.005*model.x1 + 0.90*model.x2 + 0.090*model.x3) >= 0.00*10)
model.carbon_max = pyo.Constraint(expr=(0.005*model.x1 + 0.90*model.x2 + 0.090*model.x3) <= 0.095*10)

# Silício (19% a 20%)
model.silicio_min = pyo.Constraint(expr=(0.14*model.x1 + 0.27*model.x3) >= 0.19*10)
model.silicio_max = pyo.Constraint(expr=(0.14*model.x1 + 0.27*model.x3) <= 0.20*10)

# Solver
Otimizador = pyo.SolverFactory('glpk', executable=EXEC_PATH)
Resultado = Otimizador.solve(model)

# Resultados
print("Status:", Resultado.solver.status)
print("Custo mínimo:", pyo.value(model.obj)) # 603,703
print("x1 (Lingotes) =", pyo.value(model.x1)) # 5
print("x2 (Grafite) =", pyo.value(model.x2)) # 0,1851
print("x3 (Sucata)  =", pyo.value(model.x3)) # 4,8148
print("tonelada total =", pyo.value(model.demand)) # 9,99999999999
