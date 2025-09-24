import pyomo.environ as pyo

# Dados do problema
areas = {1:1500, 2:2000, 3:1200, 4:800}

# Produção anual esperada (m³/ha)
producao = {
    (1,'Pinus'):17, (1,'Carvalho'):14, (1,'Nogueira'):13, (1,'Araucaria'):16,
    (2,'Pinus'):16, (2,'Carvalho'):15, (2,'Nogueira'):11, (2,'Araucaria'):18,
    (3,'Pinus'):12, (3,'Carvalho'):13, (3,'Nogueira'):10, (3,'Araucaria'):17,
    (4,'Pinus'):10, (4,'Carvalho'):11, (4,'Nogueira'): 8, (4,'Araucaria'):15,
}

# Renda anual esperada (R$/ha)
renda = {
    (1,'Pinus'):12, (1,'Carvalho'):20, (1,'Nogueira'):18, (1,'Araucaria'):16,
    (2,'Pinus'):11, (2,'Carvalho'):22, (2,'Nogueira'):20, (2,'Araucaria'):18,
    (3,'Pinus'):10, (3,'Carvalho'):18, (3,'Nogueira'):16, (3,'Araucaria'):17,
    (4,'Pinus'): 9, (4,'Carvalho'):15, (4,'Nogueira'):14, (4,'Araucaria'):13,
}

# Produção mínima exigida (1000 m³)
prod_min = {'Pinus':9, 'Carvalho':4.8, 'Nogueira':3.6, 'Araucaria':8.5}

cidades = [1,2,3,4]
especies = ['Pinus','Carvalho','Nogueira','Araucaria']

# Modelo
model = pyo.ConcreteModel()

# Variáveis de decisão
model.x = pyo.Var(cidades, especies, domain=pyo.NonNegativeReals)

# Função objetivo
model.obj = pyo.Objective(
    expr=sum(renda[(i,j)] * model.x[i,j] for i in cidades for j in especies),
    sense=pyo.maximize
)

# Restrições de área
model.area = pyo.ConstraintList()
for i in cidades:
    model.area.add(sum(model.x[i,j] for j in especies) <= areas[i])

# Restrições de produção mínima
model.prod = pyo.ConstraintList()
for j in especies:
    model.prod.add(sum(producao[(i,j)] * model.x[i,j] for i in cidades) >= prod_min[j]*1000)

# Resolução
solver = pyo.SolverFactory('glpk')
solver.solve(model, tee=False)

# Saída organizada
print("=== SOLUÇÃO DO PROBLEMA ===")
print(f"Função objetivo ótima (renda máxima): {pyo.value(model.obj):.2f}\n")

print("Variáveis de decisão (área alocada em hectares):")
for i in cidades:
    for j in especies:
        val = pyo.value(model.x[i,j])
        if val > 1e-6:
            print(f"  Cidade {i}, {j}: {val:.2f}")

print("\nRestrições (LHS ≤ RHS para área, LHS ≥ RHS para produção):")
for i in cidades:
    lhs = sum(pyo.value(model.x[i,j]) for j in especies)
    print(f"  Área cidade {i}: {lhs:.2f} ≤ {areas[i]}")

for j in especies:
    lhs = sum(producao[(i,j)] * pyo.value(model.x[i,j]) for i in cidades)
    print(f"  Produção {j}: {lhs:.2f} ≥ {prod_min[j]*1000}")
