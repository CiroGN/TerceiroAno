import pyomo.environ as pyo

# Dados do problema
cargas = [1, 2, 3, 4]
compartimentos = [1, 2, 3] # 1=Frontal, 2=Central, 3=Traseiro

# Dicionários com os dados
lucro_ton = {1: 320, 2: 400, 3: 360, 4: 290}
peso_disponivel = {1: 20, 2: 16, 3: 25, 4: 13}
volume_pe_cubico = {1: 500, 2: 700, 3: 600, 4: 400}

peso_max_comp = {1: 12, 2: 18, 3: 10}
volume_max_comp = {1: 7000, 2: 9000, 3: 5000}

# Criação do modelo
model = pyo.ConcreteModel()

# Conjuntos
model.cargas = pyo.Set(initialize=cargas)
model.compartimentos = pyo.Set(initialize=compartimentos)

# Variáveis de decisão
model.x = pyo.Var(model.cargas, model.compartimentos, domain=pyo.NonNegativeReals)

# Função Objetivo
def lucro_total(model):
    return sum(lucro_ton[i] * sum(model.x[i, j] for j in model.compartimentos) for i in model.cargas)
model.obj = pyo.Objective(rule=lucro_total, sense=pyo.maximize)

# Restrições
# 1. Restrições de Peso por compartimento
model.peso_comp = pyo.ConstraintList()
for j in model.compartimentos:
    model.peso_comp.add(expr=sum(model.x[i, j] for i in model.cargas) <= peso_max_comp[j])

# 2. Restrições de Volume por compartimento
model.volume_comp = pyo.ConstraintList()
for j in model.compartimentos:
    model.volume_comp.add(expr=sum(volume_pe_cubico[i] * model.x[i, j] for i in model.cargas) <= volume_max_comp[j])

# 3. Restrições de Disponibilidade de Carga
model.carga_disponivel = pyo.ConstraintList()
for i in model.cargas:
    model.carga_disponivel.add(expr=sum(model.x[i, j] for j in model.compartimentos) <= peso_disponivel[i])

# 4. Restrições de Equilíbrio
peso_frontal = sum(model.x[i, 1] for i in model.cargas)
peso_central = sum(model.x[i, 2] for i in model.cargas)
peso_traseiro = sum(model.x[i, 3] for i in model.cargas)

model.equilibrio1 = pyo.Constraint(expr=peso_frontal / peso_max_comp[1] == peso_central / peso_max_comp[2])
model.equilibrio2 = pyo.Constraint(expr=peso_central / peso_max_comp[2] == peso_traseiro / peso_max_comp[3])

# Solucionador
solver = pyo.SolverFactory('glpk')
results = solver.solve(model, tee=False)

# Impressão dos resultados
print(f"Status: {results.solver.status}")
print(f"Condição de Término: {results.solver.termination_condition}")
print(f"\nLucro Total Máximo: ${pyo.value(model.obj):.2f}")

print("\nDistribuição da Carga:")
for i in model.cargas:
    for j in model.compartimentos:
        if pyo.value(model.x[i, j]) > 1e-6:  # Impede valores muito pequenos
            print(f"  - Carga {i} no Compartimento {j}: {pyo.value(model.x[i, j]):.2f} toneladas")

print("\nPesos Totais por Compartimento:")
peso_total_frontal = pyo.value(peso_frontal)
peso_total_central = pyo.value(peso_central)
peso_total_traseiro = pyo.value(peso_traseiro)
print(f"  - Compartimento Frontal: {peso_total_frontal:.2f} toneladas (12 max)")
print(f"  - Compartimento Central: {peso_total_central:.2f} toneladas (18 max)")
print(f"  - Compartimento Traseiro: {peso_total_traseiro:.2f} toneladas (10 max)")

print("\nVerificação do Equilíbrio:")
print(f"  - Frontal/12: {peso_total_frontal/12:.4f}")
print(f"  - Central/18: {peso_total_central/18:.4f}")
print(f"  - Traseiro/10: {peso_total_traseiro/10:.4f}")