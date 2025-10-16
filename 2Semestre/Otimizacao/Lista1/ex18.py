import pyomo.environ as pyo

# 1. Criação do Modelo
model = pyo.ConcreteModel()

# 2. Definição dos Conjuntos e Parâmetros
model.tipos_caixa = pyo.Set(initialize=['alimento', 'agua', 'municao', 'remedios'])

valores = {
    'alimento': 1,
    'agua': 2,
    'municao': 4,
    'remedios': 4
}

necessidades = {
    'alimento': 6,
    'agua': 4,
    'municao': 2,
    'remedios': 2
}

# 3. Definição das Variáveis de Decisão
model.x = pyo.Var(model.tipos_caixa, domain=pyo.NonNegativeIntegers)

# 4. Definição da Função Objetivo
def objetivo_regra(model):
    return sum(valores[i] * model.x[i] for i in model.tipos_caixa)
model.objetivo = pyo.Objective(rule=objetivo_regra, sense=pyo.maximize)

# 5. Definição das Restrições
model.restricoes = pyo.ConstraintList()

# Restrição de Capacidade do Helicóptero
# LHS: sum(model.x) <= RHS: 7
model.restricoes.add(expr=sum(model.x[i] for i in model.tipos_caixa) <= 7)

# Restrições de Necessidade (quantidade máxima útil)
# LHS: model.x[i] <= RHS: necessidades[i]
for i in model.tipos_caixa:
    model.restricoes.add(expr=model.x[i] <= necessidades[i])

# 6. Resolução do Problema
solver = pyo.SolverFactory('glpk')
results = solver.solve(model, tee=False)

# 7. Impressão da Solução
print(f"Status do Solucionador: {results.solver.status}")
print(f"Condição de Término: {results.solver.termination_condition}\n")

print("--- Solução Ótima ---")
print(f"Valor Máximo de Sobrevivência: {pyo.value(model.objetivo)}\n")
print("Quantidade de caixas a serem transportadas:")
for i in model.tipos_caixa:
    print(f"  - {i.capitalize()}: {int(pyo.value(model.x[i]))} caixas")

print("\n--- Verificação das Restrições ---")
# Verificação da Restrição de Capacidade
lhs_capacidade = sum(int(pyo.value(model.x[i])) for i in model.tipos_caixa)
rhs_capacidade = 7
print(f"Restrição de Capacidade: {lhs_capacidade} <= {rhs_capacidade} (LHS <= RHS)")

# Verificação das Restrições de Necessidade
for i in model.tipos_caixa:
    lhs_necessidade = int(pyo.value(model.x[i]))
    rhs_necessidade = necessidades[i]
    print(f"Necessidade de {i.capitalize()}: {lhs_necessidade} <= {rhs_necessidade} (LHS <= RHS)")