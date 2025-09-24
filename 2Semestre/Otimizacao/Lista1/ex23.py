import pyomo.environ as pyo
from pyomo.opt import SolverFactory

# PROBLEMA PRIMAL
print("--- RESOLUÇÃO DO PROBLEMA PRIMAL (Minimizar Custo) ---")
primal_model = pyo.ConcreteModel()

# Variáveis (toneladas)
primal_model.A = pyo.Var(domain=pyo.NonNegativeReals)
primal_model.B = pyo.Var(domain=pyo.NonNegativeReals)
primal_model.S = pyo.Var(domain=pyo.NonNegativeReals)

# Parâmetros
costA = 60.0
costB = 30.0
costS = 2500.0
Fe_req = 240.0

# Objetivo (Minimizar)
primal_model.obj = pyo.Objective(expr = costA*primal_model.A + costB*primal_model.B + costS*primal_model.S, sense=pyo.minimize)

# Restrições
primal_model.fe = pyo.Constraint(expr = 0.60*primal_model.A + 0.40*primal_model.B + 1.00*primal_model.S == Fe_req)
primal_model.si_fe = pyo.Constraint(expr = 0.30*primal_model.A - 0.20*primal_model.B + 1.00*primal_model.S >= 0)

# Resolver
solver = SolverFactory('glpk')
solver.solve(primal_model, tee=False)

# Saída organizada do Primal
print("\n--- Solução do Primal ---")
print("Valor ótimo (custo mínimo) = R$ {:.2f}".format(pyo.value(primal_model.obj)))
print("\nVariáveis de Decisão:")
print("A = {:.4f} t".format(pyo.value(primal_model.A)))
print("B = {:.4f} t".format(pyo.value(primal_model.B)))
print("S = {:.4f} t".format(pyo.value(primal_model.S)))

print("\nRestrições do Primal:")
print("LHS Fe = {:.4f} == RHS 240".format(pyo.value(primal_model.fe.expr)))
print("LHS Si-Fe = {:.4f} >= RHS 0".format(pyo.value(primal_model.si_fe.expr)))

print("\n" + "="*50 + "\n")

# PROBLEMA DUAL
print("--- RESOLUÇÃO DO PROBLEMA DUAL (Maximizar Valor das Restrições) ---")
dual_model = pyo.ConcreteModel()

# Variáveis duais
dual_model.pi = pyo.Var(domain=pyo.Reals)
dual_model.mu = pyo.Var(domain=pyo.Reals)

# Correção na definição do domínio da variável mu
# A restrição do primal `si_fe` (>= 0) corresponde a uma variável dual `mu` com domínio `NonNegativeReals`.
# O erro no código original é que `mu` é definido como `Reals`, o que é incorreto.
# Corrigindo para o código mesclado.
dual_model.pi = pyo.Var(domain=pyo.Reals)
dual_model.mu = pyo.Var(domain=pyo.NonNegativeReals)

# Objetivo (Maximizar)
dual_model.obj = pyo.Objective(expr = 240*dual_model.pi + 0*dual_model.mu, sense=pyo.maximize)

# Restrições do dual (ligadas a A, B, S)
dual_model.consA = pyo.Constraint(expr = 0.60*dual_model.pi + 0.30*dual_model.mu <= 60)
dual_model.consB = pyo.Constraint(expr = 0.40*dual_model.pi - 0.20*dual_model.mu <= 30)
dual_model.consS = pyo.Constraint(expr = 1.00*dual_model.pi + 1.00*dual_model.mu <= 2500)

# Resolver
solver = SolverFactory('glpk')
solver.solve(dual_model, tee=False)

# Saída organizada do Dual
print("\n--- Solução do Dual ---")
print("Valor ótimo (receita máxima) = R$ {:.2f}".format(pyo.value(dual_model.obj)))
print("\nVariáveis de Decisão:")
print("pi = {:.4f}".format(pyo.value(dual_model.pi)))
print("mu = {:.4f}".format(pyo.value(dual_model.mu)))

print("\nRestrições do Dual:")
print("LHS consA = {:.4f} <= RHS 60".format(pyo.value(dual_model.consA.expr)))
print("LHS consB = {:.4f} <= RHS 30".format(pyo.value(dual_model.consB.expr)))
print("LHS consS = {:.4f} <= RHS 2500".format(pyo.value(dual_model.consS.expr)))

print("\n" + "="*50 + "\n")
print("--- VERIFICAÇÃO DA TEORIA DA DUALIDADE ---")
if abs(pyo.value(primal_model.obj) - pyo.value(dual_model.obj)) < 1e-6:
    print("Os valores da função objetivo dos modelos Primal e Dual são iguais.")
    print("Isso confirma a Teoria da Dualidade Forte.")
else:
    print("Os valores da função objetivo dos modelos Primal e Dual são diferentes.")
    print("Isso pode indicar um erro de formulação ou na solução.")