import random
import math # para calcular a hipotenusa
import numpy as Np
import matplotlib.pyplot as Plt
import pyomo.environ as Pyo


def Dist_Euclidiana(Coord_X, Coord_Y):
    return int(round(math.hypot(Coord_X[0] - Coord_Y[0], Coord_X[1] - Coord_Y[1])))



# -------- Solver --------
EXEC_PATH = '/Users/thian/Desktop/Otimização 2024.2/glpk-4.65/w64/glpsol'

# --- Tamanho do Problema ---
N_Clientes = 100
N_Facilidades = 10
Pi = 5

# --- Para gerar coordenadas, capacidades e demandas -----
SEED = 12345
random.seed(SEED)
Np.random.seed(SEED)

# ---- Coordenadas dos Clientes e das Facilidades ----
Coord_Clientes = {i: (int(x), int(y)) for i, (x,y) in enumerate(Np.random.randint(0, 101, (N_Clientes, 2)), start=1)}
Coord_Facilidades = {j: (int(x), int(y)) for j, (x,y) in enumerate(Np.random.randint(0, 101, (N_Facilidades, 2)), start=1)}

# --- Demandas dos clientes ---
d_i = {i: int(v) for i, v in zip(range(1, N_Clientes + 1), Np.random.randint(1, 11, N_Clientes))}

# --- Distâncias entre Clientes e Facilidades ----
c_ij = {(i, j): Dist_Euclidiana(Coord_Clientes[i], Coord_Facilidades[j])\
        for i in Coord_Clientes for j in Coord_Facilidades}

# --- Capacidades das Facilidades Potenciais ----
Demanda_Total = sum(d_i.values())
Phi_Medio = int(Demanda_Total / Pi)

Phi_j = {j: Np.random.randint(int(1.1*Phi_Medio), int(1.2*Phi_Medio)) for j in range(1, N_Facilidades + 1)}

print(f'Demanda Total = {Demanda_Total}')
print(f'Capacidade Total = {sum(Phi_j.values())}')

# --- Custo de Instalação ---
f_j = {j: int(Phi_j[j] * random.uniform(1.1, 1.2)) for j in range(1, N_Facilidades + 1)}
print(f_j)

# ----- Modelo Pyomo -----
Modelo = Pyo.ConcreteModel()

# --- Conjuntos ---
Modelo.C = Pyo.Set(initialize=list(Coord_Clientes.keys())) # Conjunto de Clientes
Modelo.F = Pyo.Set(initialize=list(Coord_Facilidades.keys())) # Conjunto de Facilidades

# --- Parâmetros ---
Modelo.Pi = Pyo.Param(initialize=Pi)
Modelo.c_ij = Pyo.Param(Modelo.C, Modelo.F, initialize=c_ij)
Modelo.d_i = Pyo.Param(Modelo.C, initialize=d_i)
Modelo.Phi_j = Pyo.Param(Modelo.F, initialize=Phi_j)
Modelo.f_j = Pyo.Param(Modelo.F, initialize=f_j)

# --- Variáveis de Decisão ---
Modelo.Y_j = Pyo.Var(Modelo.F, domain=Pyo.Binary)
Modelo.X_ij = Pyo.Var(Modelo.C, Modelo.F, domain=Pyo.Binary)

# --- Função Objetivo ----
Modelo.Z = Pyo.Objective(expr = (sum(Modelo.f_j[j] * Modelo.Y_j[j] for j in Modelo.F) + \
                                 sum(Modelo.c_ij[i,j] * Modelo.X_ij[i,j] for i in Modelo.C for j in Modelo.F)))

# --- Restrições ---
Modelo.R_Demanda = Pyo.ConstraintList()
for i in Modelo.C:
    Modelo.R_Demanda.add(expr = sum(Modelo.X_ij[i,j] for j in Modelo.F) == 1)

Modelo.R_Oferta = Pyo.ConstraintList()
for j in Modelo.F:
    Modelo.R_Oferta.add(expr = sum(Modelo.d_i[i]*Modelo.X_ij[i,j] for i in Modelo.C) <= Modelo.Phi_j[j] * Modelo.Y_j[j])

Modelo.R_Max = Pyo.ConstraintList()
Modelo.R_Max.add(expr = sum(Modelo.Y_j[j] for j in Modelo.F) <= Modelo.Pi)

#Otimizador = Pyo.SolverFactory('glpk', executable = EXEC_PATH)
Otimizador = Pyo.SolverFactory('gurobi')
Resultado = Otimizador.solve(Modelo, tee=True)

# ---------- Resultados ----------
open_facs = [j for j in Modelo.F if Pyo.value(Modelo.Y_j[j]) > 0.5]
assignments = [(i, j) for i in Modelo.C for j in Modelo.F if Pyo.value(Modelo.X_ij[i, j]) > 0.5]

total_cost = Pyo.value(Modelo.Z)
print(f"\nFacilidades abertas: {open_facs}")
print(f"Custo total: {total_cost:.2f}\n")

# Mostrar capacidade usada em cada instalação (percentual)
for j in open_facs:
    assigned_clients = [i for i in Modelo.C if Pyo.value(Modelo.X_ij[i, j]) > 0.5]
    used = sum(Pyo.value(Modelo.d_i[i]) for i in assigned_clients)
    perc = 100 * used / Pyo.value(Modelo.Phi_j[j])
    print(f"\nFacility {j}: capacidade usada = {used:.1f} / {Pyo.value(Modelo.Phi_j[j]):.1f} --> {perc:.2f}%")
    print(f"Clientes designados ({len(assigned_clients)}): {assigned_clients}")

# ---------- Visualização ----------
Plt.figure(figsize=(8, 8))

# Clientes
for i, (x, y) in Coord_Clientes.items():
    Plt.scatter(x, y, c='blue', s=10, alpha=0.6)

# Instalações abertas e fechadas
for j in Modelo.F:
    xf, yf = Coord_Facilidades[j]
    if j in open_facs:
        Plt.scatter(xf, yf, c='red', marker='s', s=100, edgecolor='black', zorder=5)
    else:
        Plt.scatter(xf, yf, c='gray', marker='s', s=70, alpha=0.5, zorder=4)

for i, j in assignments:
    x1, y1 = Coord_Clientes[i]
    x2, y2 = Coord_Facilidades[j]
    Plt.plot([x1, x2], [y1, y2], color='lightgray', lw=1.2, alpha=0.9, zorder=1)

Plt.xlabel('Coordenada X')
Plt.ylabel('Coordenada Y')
Plt.title(f'Custo Total = {total_cost:.1f}')
Plt.grid(True, alpha=0.3)
Plt.show()