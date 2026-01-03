# -*- coding: utf-8 -*-
"""FLP_GRASP_VNS.py

Algoritmo GRASP com VNS para Problema de Localização de Facilidades (FLP)
OBJETIVO: Minimizar custo de transporte = Soma(Demanda × Distância)
CUSTO ALVO: 4032.00
"""

import math
import random
import time
import matplotlib.pyplot as plt

# ============================================================================
# 1. CLASSE INSTÂNCIA
# ============================================================================

class Instance:
    def __init__(self):
        self.num_clients = 0
        self.num_facilities = 0
        self.p_max = 0
        self.clients = []  # Lista de dicts: {'id':, 'x':, 'y':, 'demand':}
        self.facilities = []  # Lista de dicts: {'id':, 'x':, 'y':, 'capacity':, 'cost':}
        self.dist_matrix = []  # Matriz [cliente][facilidade]
        self.sorted_dist_indices = []  # Para cada cliente, índices das fac ordenadas por distância
        self.reference_solution = None  # Para armazenar solução de referência

    def calc_euclidean_distance(self, c, f):
        return math.sqrt((c['x'] - f['x'])**2 + (c['y'] - f['y'])**2)

    def precompute_distances(self):
        # Pré-calcula distâncias e ordenações
        self.dist_matrix = [[0.0] * self.num_facilities for _ in range(self.num_clients)]
        self.sorted_dist_indices = [[] for _ in range(self.num_clients)]
        
        for i in range(self.num_clients):
            dist_list = []
            for j in range(self.num_facilities):
                dist = self.calc_euclidean_distance(self.clients[i], self.facilities[j])
                self.dist_matrix[i][j] = dist
                dist_list.append((dist, j))
            
            # Ordena por distância crescente
            dist_list.sort(key=lambda x: x[0])
            self.sorted_dist_indices[i] = [idx for _, idx in dist_list]

# ============================================================================
# 2. PARSER
# ============================================================================

def parse_file(file_path):
    instance = Instance()

    with open(file_path, 'r') as f:
        lines = f.readlines()

    mode = None
    temp_cli_coords = {}
    temp_cli_demand = {}
    temp_fac_coords = {}
    temp_fac_cap = {}
    temp_fac_cost = {}
    
    # Para armazenar solução de referência
    reference_cost = None
    reference_facilities = []
    reference_allocations = {}

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("# N_Clientes"):
            instance.num_clients = int(line.split("=")[1].strip())
        elif line.startswith("# N_Facilidades"):
            instance.num_facilities = int(line.split("=")[1].strip())
        elif "# P (" in line or "P =" in line:
            # Extrai o número de P
            parts = line.split("=")
            if len(parts) >= 2:
                value_part = parts[1].strip()
                # Remove "facilidades" e pega o número
                numbers = [int(s) for s in value_part.split() if s.isdigit()]
                if numbers:
                    instance.p_max = numbers[0]

        elif "Coordenadas dos Clientes" in line:
            mode = "cli_coord"
        elif "Demandas dos Clientes" in line:
            mode = "cli_dem"
        elif "Coordenadas das Facilidades" in line:
            mode = "fac_coord"
        elif "Capacidades das Facilidades" in line:
            mode = "fac_cap"
        elif "Custos Fixos" in line:
            mode = "fac_cost"
        elif "Matriz" in line:
            mode = "ignore"
        elif "SOLUÇÃO ENCONTRADA" in line:
            mode = "solution_ref"

        elif mode == "cli_coord" and line[0].isdigit():
            parts = line.split()
            if len(parts) >= 3:
                temp_cli_coords[int(parts[0])] = (float(parts[1]), float(parts[2]))

        elif mode == "cli_dem" and line[0].isdigit():
            parts = line.split()
            if len(parts) >= 2:
                temp_cli_demand[int(parts[0])] = float(parts[1])

        elif mode == "fac_coord" and line[0].isdigit():
            parts = line.split()
            if len(parts) >= 3:
                temp_fac_coords[int(parts[0])] = (float(parts[1]), float(parts[2]))

        elif mode == "fac_cap" and line[0].isdigit():
            parts = line.split()
            if len(parts) >= 2:
                temp_fac_cap[int(parts[0])] = float(parts[1])

        elif mode == "fac_cost" and line[0].isdigit():
            parts = line.split()
            if len(parts) >= 2:
                temp_fac_cost[int(parts[0])] = float(parts[1])
                
        elif mode == "solution_ref":
            if "Custo total =" in line:
                parts = line.split("=")
                if len(parts) >= 2:
                    reference_cost = float(parts[1].strip())
            elif "Facilidades abertas:" in line:
                # Extrai lista do formato: "# Facilidades abertas: [1, 5, 6, ...]"
                if "[" in line and "]" in line:
                    start = line.find("[")
                    end = line.find("]")
                    list_str = line[start+1:end]
                    reference_facilities = [int(x.strip()) for x in list_str.split(",")]
            elif "Facility" in line and "->" in line:
                # Formato: "# Facility X -> clientes: [lista]"
                try:
                    # Remove o # inicial
                    line_clean = line.replace("#", "").strip()
                    parts = line_clean.split("->")
                    if len(parts) >= 2:
                        # Extrai ID da facility - formato: "Facility X"
                        fac_part = parts[0].strip()
                        fac_id = int(fac_part.split()[-1])  # Pega o último elemento (número)
                        
                        # Extrai lista de clientes
                        clients_part = parts[1].strip()
                        start = clients_part.find("[")
                        end = clients_part.find("]")
                        if start != -1 and end != -1:
                            list_str = clients_part[start+1:end]
                            client_list = [int(x.strip()) for x in list_str.split(",")]
                            reference_allocations[fac_id] = client_list
                except:
                    pass  # Ignora erros de parsing

    # Constrói instância
    for i in range(1, instance.num_clients + 1):
        instance.clients.append({
            'id': i,
            'x': temp_cli_coords[i][0],
            'y': temp_cli_coords[i][1],
            'demand': temp_cli_demand[i]
        })

    for i in range(1, instance.num_facilities + 1):
        instance.facilities.append({
            'id': i,
            'x': temp_fac_coords[i][0],
            'y': temp_fac_coords[i][1],
            'capacity': temp_fac_cap[i],
            'cost': temp_fac_cost[i]
        })

    # Armazena solução de referência
    if reference_facilities:
        instance.reference_solution = {
            'cost': reference_cost,
            'facilities': reference_facilities,
            'allocations': reference_allocations
        }

    instance.precompute_distances()
    print(f"Instância Carregada: {instance.num_facilities} Facilidades, {instance.num_clients} Clientes.")
    
    if instance.reference_solution:
        print(f"Solução de referência carregada: custo alvo = {reference_cost:.2f}")
        print(f"Facilidades de referência: {reference_facilities}")
    
    return instance

# ============================================================================
# 3. ESTRUTURAS DE SOLUÇÃO E FUNÇÕES DE AVALIAÇÃO
# ============================================================================

class Solution:
    """Classe para representar uma solução completa"""
    def __init__(self, instance):
        self.instance = instance
        self.open_facilities = [0] * instance.num_facilities  # 0/1
        self.client_assignments = [-1] * instance.num_clients  # índice da fac ou -1
        self.used_capacity = [0] * instance.num_facilities
        self.total_cost = float('inf')
        self.is_feasible = False
        self.transport_cost = 0

    def copy(self):
        """Cria uma cópia profunda da solução"""
        new_sol = Solution(self.instance)
        new_sol.open_facilities = self.open_facilities.copy()
        new_sol.client_assignments = self.client_assignments.copy()
        new_sol.used_capacity = self.used_capacity.copy()
        new_sol.total_cost = self.total_cost
        new_sol.is_feasible = self.is_feasible
        new_sol.transport_cost = self.transport_cost
        return new_sol

    def evaluate(self, penalty_factor=10000):
        """
        Avalia a solução atual e atualiza seu custo
        OBJETIVO: Minimizar SOMA(Demanda × Distância)
        Custo alvo: 4032.00 (do arquivo TXT)
        """
        instance = self.instance
        
        # Conta facilidades abertas
        open_count = sum(self.open_facilities)
        
        # Verifica restrições básicas (capacidade e P máximo)
        if open_count == 0 or open_count > instance.p_max:
            self.is_feasible = False
            self.total_cost = float('inf')
            return float('inf'), False
        
        # RESETA valores
        self.transport_cost = 0
        self.used_capacity = [0] * instance.num_facilities
        penalty = 0
        self.client_assignments = [-1] * instance.num_clients
        
        # Para cada cliente, encontra a facilidade aberta mais próxima
        for c_idx in range(instance.num_clients):
            client = instance.clients[c_idx]
            client_demand = client['demand']
            min_distance = float('inf')
            best_facility = -1
            
            # Procura a facilidade aberta mais próxima
            for f_idx in range(instance.num_facilities):
                if self.open_facilities[f_idx]:
                    # Verifica capacidade
                    if self.used_capacity[f_idx] + client_demand <= instance.facilities[f_idx]['capacity']:
                        distance = instance.dist_matrix[c_idx][f_idx]
                        if distance < min_distance:
                            min_distance = distance
                            best_facility = f_idx
            
            # Se encontrou facilidade válida
            if best_facility != -1 and min_distance != float('inf'):
                self.used_capacity[best_facility] += client_demand
                self.client_assignments[c_idx] = best_facility
                # CUSTO: demanda × distância
                self.transport_cost += client_demand * min_distance
            else:
                # Não conseguiu alocar - penaliza
                penalty += penalty_factor * client_demand
        
        # Custo total é APENAS transporte + penalidade
        self.total_cost = self.transport_cost + penalty
        self.is_feasible = (penalty == 0)
        
        return self.total_cost, self.is_feasible

    def get_allocations(self):
        """Retorna alocações no formato do arquivo"""
        allocations = {}
        
        for fac_idx, is_open in enumerate(self.open_facilities):
            if is_open:
                fac_id = self.instance.facilities[fac_idx]['id']
                clients_for_fac = []
                
                for client_idx, assigned_fac in enumerate(self.client_assignments):
                    if assigned_fac == fac_idx:
                        client_id = self.instance.clients[client_idx]['id']
                        clients_for_fac.append(client_id)
                
                allocations[fac_id] = sorted(clients_for_fac)
        
        return allocations

    def print_solution_format(self):
        """Imprime a solução no formato do arquivo TXT"""
        print("\n" + "=" * 60)
        print("SOLUÇÃO ENCONTRADA")
        print("=" * 60)
        print(f"# Custo total = {self.total_cost:.2f}")
        
        # Facilidades abertas
        open_fac_ids = []
        for i, is_open in enumerate(self.open_facilities):
            if is_open:
                open_fac_ids.append(self.instance.facilities[i]['id'])
        
        print(f"# Facilidades abertas: {sorted(open_fac_ids)}")
        
        # Alocações
        allocations = self.get_allocations()
        for fac_id in sorted(allocations.keys()):
            clients = allocations[fac_id]
            print(f"# Facility {fac_id} -> clientes: {clients}")

# ============================================================================
# 4. CONSTRUTOR GRASP (FASE DE CONSTRUÇÃO)
# ============================================================================

def grasp_construction(instance, alpha=0.3, max_tries=5):
    """
    Construção GRASP para gerar solução inicial
    Objetivo: Minimizar custo de transporte (demanda × distância)
    """
    best_solution = None
    best_cost = float('inf')
    
    for try_num in range(max_tries):
        # Tenta começar com solução de referência na primeira tentativa
        solution = Solution(instance)
        
        if instance.reference_solution and try_num == 0:
            # Usa facilidades da referência como ponto de partida
            ref_facilities = instance.reference_solution['facilities']
            for fac_id in ref_facilities:
                for idx, fac in enumerate(instance.facilities):
                    if fac['id'] == fac_id:
                        solution.open_facilities[idx] = 1
                        break
        else:
            # Construção aleatória/gulosa
            # Escolhe P facilidades aleatórias
            all_facilities = list(range(instance.num_facilities))
            chosen = random.sample(all_facilities, instance.p_max)
            for idx in chosen:
                solution.open_facilities[idx] = 1
        
        # Avalia a solução
        cost, feasible = solution.evaluate()
        
        # Se não for viável, tenta corrigir
        if not feasible:
            solution = repair_solution(solution)
            cost, feasible = solution.evaluate()
        
        if feasible and cost < best_cost:
            best_cost = cost
            best_solution = solution
    
    return best_solution

def repair_solution(solution):
    """
    Tenta reparar uma solução inviável
    """
    instance = solution.instance
    new_solution = solution.copy()
    
    # Conta quantas facilidades estão abertas
    open_count = sum(new_solution.open_facilities)
    
    # Se não tem facilidades abertas, abre algumas
    if open_count == 0:
        # Abre as P facilidades com maior capacidade
        facilities_by_capacity = []
        for idx, fac in enumerate(instance.facilities):
            facilities_by_capacity.append((fac['capacity'], idx))
        
        facilities_by_capacity.sort(reverse=True)
        for i in range(min(instance.p_max, len(facilities_by_capacity))):
            new_solution.open_facilities[facilities_by_capacity[i][1]] = 1
    
    # Se tem muitas abertas, fecha algumas
    elif open_count > instance.p_max:
        # Fecha as com menor utilização
        open_indices = [i for i, val in enumerate(new_solution.open_facilities) if val == 1]
        # Avalia para ver utilização
        new_solution.evaluate()
        # Ordena por utilização (menor primeiro)
        utilization = []
        for idx in open_indices:
            used = new_solution.used_capacity[idx]
            total = instance.facilities[idx]['capacity']
            util = used / total if total > 0 else 0
            utilization.append((util, idx))
        
        utilization.sort()  # Menor utilização primeiro
        # Fecha as menos utilizadas
        to_close = open_count - instance.p_max
        for i in range(to_close):
            idx = utilization[i][1]
            new_solution.open_facilities[idx] = 0
    
    return new_solution

def greedy_initial_solution(instance):
    """Solução inicial gulosa como fallback"""
    solution = Solution(instance)
    
    # Ordena fac por capacidade (maior primeiro)
    fac_capacity = []
    for f_idx, fac in enumerate(instance.facilities):
        fac_capacity.append((fac['capacity'], f_idx))
    
    fac_capacity.sort(reverse=True)
    
    # Abre as P facilidades com maior capacidade
    open_count = min(instance.p_max, instance.num_facilities)
    for i in range(open_count):
        solution.open_facilities[fac_capacity[i][1]] = 1
    
    solution.evaluate()
    return solution

# ============================================================================
# 5. VARIABLE NEIGHBORHOOD SEARCH (VNS)
# ============================================================================

def vns_search(initial_solution, max_time=30, shaking_neighborhoods=3):
    """
    Busca VNS com múltiplas estruturas de vizinhança
    """
    current = initial_solution.copy()
    best = current.copy()
    history = [best.total_cost]
    
    start_time = time.time()
    iteration = 0
    
    while time.time() - start_time < max_time:
        k = 1  # Vizinhança atual
        
        while k <= shaking_neighborhoods:
            iteration += 1
            
            # 1. SHAKING: Gera solução aleatória na k-ésima vizinhança
            shaken = shaking(current, k)
            
            # 2. BUSCA LOCAL intensiva na solução agitada
            improved = local_search_intensive(shaken)
            
            # 3. CRITÉRIO DE ACEITAÇÃO (melhora estrita)
            if improved.total_cost < current.total_cost:
                current = improved
                k = 1  # Reinicia com primeira vizinhança
                
                # Atualiza melhor global
                if current.total_cost < best.total_cost:
                    best = current.copy()
                    history.append(best.total_cost)
            else:
                k += 1  # Tenta próxima vizinhança
            
            # Verifica tempo
            if time.time() - start_time > max_time:
                break
    
    return best, history

def shaking(solution, k):
    """Gera solução perturbada (shaking)"""
    new_sol = solution.copy()
    instance = solution.instance
    
    if k == 1:  # Troca uma fac aberta por uma fechada
        open_facs = [i for i, val in enumerate(new_sol.open_facilities) if val == 1]
        closed_facs = [i for i, val in enumerate(new_sol.open_facilities) if val == 0]
        
        if open_facs and closed_facs:
            close_idx = random.choice(open_facs)
            open_idx = random.choice(closed_facs)
            
            new_sol.open_facilities[close_idx] = 0
            new_sol.open_facilities[open_idx] = 1
    
    elif k == 2:  # Fecha duas, abre duas diferentes
        open_facs = [i for i, val in enumerate(new_sol.open_facilities) if val == 1]
        closed_facs = [i for i, val in enumerate(new_sol.open_facilities) if val == 0]
        
        if len(open_facs) >= 2 and len(closed_facs) >= 2:
            to_close = random.sample(open_facs, 2)
            to_open = random.sample(closed_facs, 2)
            
            for idx in to_close:
                new_sol.open_facilities[idx] = 0
            for idx in to_open:
                new_sol.open_facilities[idx] = 1
    
    elif k >= 3:  # Reabertura aleatória
        num_changes = random.randint(2, min(4, instance.num_facilities // 3))
        
        for _ in range(num_changes):
            idx = random.randint(0, instance.num_facilities - 1)
            new_sol.open_facilities[idx] = 1 - new_sol.open_facilities[idx]
    
    # Garante que não excede p_max
    open_count = sum(new_sol.open_facilities)
    if open_count > instance.p_max:
        open_indices = [i for i, val in enumerate(new_sol.open_facilities) if val == 1]
        to_close = random.sample(open_indices, open_count - instance.p_max)
        for idx in to_close:
            new_sol.open_facilities[idx] = 0
    
    # Garante que abre pelo menos uma
    if open_count == 0:
        idx = random.randint(0, instance.num_facilities - 1)
        new_sol.open_facilities[idx] = 1
    
    new_sol.evaluate()
    return new_sol

def local_search_intensive(solution):
    """
    Busca local intensiva com múltiplos movimentos
    """
    best = solution.copy()
    improved = True
    max_iterations = 50
    iterations = 0
    
    while improved and iterations < max_iterations:
        improved = False
        iterations += 1
        
        # Movimento 1: Swap exaustivo (testa todos os pares)
        open_facs = [i for i, val in enumerate(best.open_facilities) if val == 1]
        closed_facs = [i for i, val in enumerate(best.open_facilities) if val == 0]
        
        best_swap = best.copy()
        
        for open_idx in open_facs:
            for closed_idx in closed_facs:
                # Testa o swap
                new_sol = best.copy()
                new_sol.open_facilities[open_idx] = 0
                new_sol.open_facilities[closed_idx] = 1
                
                cost, feasible = new_sol.evaluate()
                
                if feasible and cost < best_swap.total_cost:
                    best_swap = new_sol
        
        if best_swap.total_cost < best.total_cost:
            best = best_swap
            improved = True
            continue
        
        # Movimento 2: Add (se não estourar p_max)
        if sum(best.open_facilities) < solution.instance.p_max:
            best_add = best.copy()
            
            for closed_idx in range(solution.instance.num_facilities):
                if best.open_facilities[closed_idx] == 0:
                    new_sol = best.copy()
                    new_sol.open_facilities[closed_idx] = 1
                    
                    cost, feasible = new_sol.evaluate()
                    
                    if feasible and cost < best_add.total_cost:
                        best_add = new_sol
            
            if best_add.total_cost < best.total_cost:
                best = best_add
                improved = True
                continue
        
        # Movimento 3: Drop (se tiver mais de 1 aberta)
        if sum(best.open_facilities) > 1:
            best_drop = best.copy()
            
            for open_idx in range(solution.instance.num_facilities):
                if best.open_facilities[open_idx] == 1:
                    new_sol = best.copy()
                    new_sol.open_facilities[open_idx] = 0
                    
                    cost, feasible = new_sol.evaluate()
                    
                    if feasible and cost < best_drop.total_cost:
                        best_drop = new_sol
            
            if best_drop.total_cost < best.total_cost:
                best = best_drop
                improved = True
    
    return best

# ============================================================================
# 6. GRASP PRINCIPAL
# ============================================================================

def grasp_vns(instance, max_iterations=20, max_time=120):
    """
    Algoritmo GRASP principal com VNS melhorado
    """
    best_solution = None
    best_cost = float('inf')
    history = []
    
    start_time = time.time()
    
    for iteration in range(max_iterations):
        # Verifica tempo
        if time.time() - start_time > max_time:
            print(f"Tempo limite atingido após {iteration} iterações")
            break
        
        # 1. FASE DE CONSTRUÇÃO (GRASP)
        solution = grasp_construction(instance, alpha=0.3)
        
        # 2. FASE DE BUSCA LOCAL (VNS)
        remaining_time = max_time - (time.time() - start_time)
        if remaining_time <= 0:
            break
            
        vns_time = min(remaining_time, max_time / max_iterations * 2)
        improved_solution, local_history = vns_search(
            solution, 
            max_time=vns_time,
            shaking_neighborhoods=3
        )
        
        # Atualiza melhor global
        if improved_solution.is_feasible and improved_solution.total_cost < best_cost:
            best_cost = improved_solution.total_cost
            best_solution = improved_solution
            history.extend(local_history)
            print(f"Iteração {iteration + 1}: Novo melhor custo = {best_cost:.2f}")
            
            # Se encontrou custo igual ou melhor que referência, pode parar
            if instance.reference_solution and best_cost <= instance.reference_solution['cost']:
                print(f"✅ Custo de referência alcançado!")
                break
    
    # Se não encontrou solução viável, usa gulosa
    if best_solution is None:
        print("Nenhuma solução viável encontrada. Usando solução gulosa...")
        best_solution = greedy_initial_solution(instance)
        best_solution.evaluate()
    
    return best_solution, history

# ============================================================================
# 7. FUNÇÕES PARA VERIFICAÇÃO E COMPARAÇÃO
# ============================================================================

def verify_reference_solution(instance):
    """Verifica a solução de referência do arquivo"""
    if not instance.reference_solution:
        print("Nenhuma solução de referência disponível.")
        return None
    
    ref = instance.reference_solution
    
    # Cria solução com as facilidades de referência
    ref_solution = Solution(instance)
    
    # Abre as facilidades da referência
    for fac_id in ref['facilities']:
        for idx, fac in enumerate(instance.facilities):
            if fac['id'] == fac_id:
                ref_solution.open_facilities[idx] = 1
                break
    
    # Avalia a solução
    cost, feasible = ref_solution.evaluate()
    
    print("\n" + "=" * 60)
    print("VERIFICAÇÃO DA SOLUÇÃO DE REFERÊNCIA")
    print("=" * 60)
    print(f"Custo reportado no arquivo: {ref['cost']:.2f}")
    print(f"Custo calculado por nós: {cost:.2f}")
    print(f"Solução viável: {'Sim' if feasible else 'Não'}")
    
    if abs(cost - ref['cost']) < 0.01:
        print("✅ Custo calculado está consistente com o arquivo!")
    else:
        print(f"⚠️  Discrepância de {abs(cost - ref['cost']):.2f} encontrada.")
    
    return ref_solution

def compare_with_reference(our_solution, ref_solution):
    """Compara nossa solução com a de referência"""
    if not ref_solution:
        return
    
    print("\n" + "=" * 60)
    print("COMPARAÇÃO COM REFERÊNCIA")
    print("=" * 60)
    
    print(f"Custo da referência: {ref_solution.total_cost:.2f}")
    print(f"Nosso custo: {our_solution.total_cost:.2f}")
    
    gap = ((our_solution.total_cost - ref_solution.total_cost) / ref_solution.total_cost) * 100
    print(f"Gap: {gap:+.2f}%")
    
    # Verifica se são as mesmas facilidades
    our_facilities = []
    for i, is_open in enumerate(our_solution.open_facilities):
        if is_open:
            our_facilities.append(our_solution.instance.facilities[i]['id'])
    
    ref_facilities = []
    for i, is_open in enumerate(ref_solution.open_facilities):
        if is_open:
            ref_facilities.append(ref_solution.instance.facilities[i]['id'])
    
    print(f"\nNossas facilidades: {sorted(our_facilities)}")
    print(f"Facilidades de referência: {sorted(ref_facilities)}")
    
    if set(our_facilities) == set(ref_facilities):
        print("✅ Encontramos as mesmas facilidades que a referência!")
    else:
        diff = set(our_facilities).symmetric_difference(set(ref_facilities))
        print(f"Diferença nas facilidades: {sorted(list(diff))}")

# ============================================================================
# 8. VISUALIZAÇÃO
# ============================================================================

def plot_solution(instance, solution, title="Solução Encontrada"):
    """Plota a solução final"""
    plt.figure(figsize=(12, 10))
    
    # Plota linhas de conexão (limitadas para não sobrecarregar)
    connection_count = 0
    for c_idx, f_idx in enumerate(solution.client_assignments):
        if f_idx != -1 and connection_count < 100:  # Limita a 100 conexões
            client = instance.clients[c_idx]
            facility = instance.facilities[f_idx]
            
            plt.plot([client['x'], facility['x']], [client['y'], facility['y']],
                    color='lightgray', linewidth=0.5, zorder=1, alpha=0.6)
            connection_count += 1
    
    # Plota clientes
    client_x = [c['x'] for c in instance.clients]
    client_y = [c['y'] for c in instance.clients]
    plt.scatter(client_x, client_y, c='blue', s=30, alpha=0.7, 
               zorder=2, label='Clientes', edgecolors='black', linewidth=0.5)
    
    # Plota facilidades
    open_x = []
    open_y = []
    closed_x = []
    closed_y = []
    
    for i, fac in enumerate(instance.facilities):
        if solution.open_facilities[i] == 1:
            open_x.append(fac['x'])
            open_y.append(fac['y'])
        else:
            closed_x.append(fac['x'])
            closed_y.append(fac['y'])
    
    plt.scatter(open_x, open_y, c='red', marker='D', s=150, 
               zorder=3, label='Facilidades Abertas', edgecolors='black', linewidth=1.5)
    plt.scatter(closed_x, closed_y, c='gray', marker='x', s=100, 
               zorder=2, label='Facilidades Fechadas', alpha=0.5)
    
    # Adiciona IDs das fac abertas
    for i, fac in enumerate(instance.facilities):
        if solution.open_facilities[i] == 1:
            plt.text(fac['x'], fac['y'] + 3, str(fac['id']), 
                    fontsize=9, fontweight='bold', ha='center', 
                    color='darkred', zorder=4)
    
    plt.title(f"{title}\nCusto Total: {solution.total_cost:.2f} (Alvo: 4032.00)")
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()

def plot_convergence(history):
    """Plota convergência do algoritmo"""
    if not history:
        return
        
    plt.figure(figsize=(10, 6))
    plt.plot(history, marker='o', markersize=3, linestyle='-', linewidth=1)
    plt.title("Convergência do GRASP-VNS")
    plt.xlabel("Iteração/Melhoria")
    plt.ylabel("Custo Total")
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Adiciona linha do alvo (4032.00)
    plt.axhline(y=4032.00, color='green', linestyle='--', 
               linewidth=2, label=f'Alvo: 4032.00')
    
    # Adiciona linha do melhor custo
    best_cost = min(history)
    plt.axhline(y=best_cost, color='r', linestyle='--', 
               linewidth=1, label=f'Melhor: {best_cost:.2f}')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

# ============================================================================
# 9. FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal de execução"""
    ARQUIVO_ALVO = "Instancia_FLP_2.txt"
    
    print("=" * 80)
    print("GRASP-VNS para Problema de Localização de Facilidades")
    print(f"OBJETIVO: Minimizar Custo de Transporte = Soma(Demanda × Distância)")
    print(f"VALOR ALVO (ótimo): 4032.00")
    print("=" * 80)
    
    # 1. Ler instância
    print(f"\n[1] Lendo instância: {ARQUIVO_ALVO}")
    instancia = parse_file(ARQUIVO_ALVO)
    
    # 2. Mostrar objetivo
    print(f"\n[2] CONFIGURAÇÃO DO PROBLEMA:")
    print(f"  • Clientes: {instancia.num_clients}")
    print(f"  • Facilidades disponíveis: {instancia.num_facilities}")
    print(f"  • Facilidades a abrir (P): {instancia.p_max}")
    print(f"  • Demanda total: {sum(c['demand'] for c in instancia.clients)}")
    print(f"  • OBJETIVO: Encontrar custo próximo de 4032.00")
    
    if instancia.reference_solution:
        print(f"  • Solução de referência disponível para comparação")
    
    # 3. Verificar solução de referência
    ref_solution = verify_reference_solution(instancia)
    
    # 4. Executar GRASP-VNS
    max_time = 180  # 3 minutos
    max_iterations = 30
    
    print(f"\n[3] Executando GRASP-VNS (max {max_time}s, {max_iterations} iterações)")
    print(f"    Alvo: 4032.00")
    start_time = time.time()
    
    best_solution, history = grasp_vns(
        instancia, 
        max_iterations=max_iterations,
        max_time=max_time
    )
    
    end_time = time.time()
    
    # 5. Resultados
    print("\n" + "=" * 80)
    print("RESULTADOS FINAIS")
    print("=" * 80)
    print(f"Tempo total: {end_time - start_time:.2f} segundos")
    
    # Imprimir solução no formato do arquivo
    best_solution.print_solution_format()
    
    # Comparação com o alvo
    print(f"\nCOMPARAÇÃO COM O OBJETIVO:")
    print(f"  • Custo encontrado: {best_solution.total_cost:.2f}")
    print(f"  • Custo alvo (ótimo): 4032.00")
    
    gap = ((best_solution.total_cost - 4032.00) / 4032.00) * 100
    print(f"  • Gap: {gap:+.2f}%")
    
    if gap <= 0:
        print(f"\n🎉🎉🎉 OBJETIVO SUPERADO! Custo melhor que a referência! 🎉🎉🎉")
    elif gap < 1.0:
        print(f"\n✅ Excelente! Custo muito próximo do alvo (dentro de 1%)")
    elif gap < 5.0:
        print(f"\n⚠️  Bom resultado, mas pode melhorar (dentro de 5%)")
    elif gap < 10.0:
        print(f"\n🔍 Resultado aceitável (dentro de 10%)")
    else:
        print(f"\n❌ Precisa melhorar o algoritmo (acima de 10%)")
    
    # Comparação com referência se disponível
    if ref_solution:
        compare_with_reference(best_solution, ref_solution)
    
    # Estatísticas
    print(f"\nESTATÍSTICAS:")
    open_count = sum(best_solution.open_facilities)
    print(f"  • Facilidades abertas: {open_count} (deve ser {instancia.p_max})")
    
    # Facilidades abertas com utilização
    for i, is_open in enumerate(best_solution.open_facilities):
        if is_open:
            fac = instancia.facilities[i]
            used = best_solution.used_capacity[i]
            total = fac['capacity']
            util = (used / total * 100) if total > 0 else 0
            print(f"  • Fac {fac['id']}: {used:.1f}/{total:.0f} ({util:.1f}%)")
    
    # Clientes atendidos
    unassigned = sum(1 for x in best_solution.client_assignments if x == -1)
    assigned = len(best_solution.client_assignments) - unassigned
    print(f"  • Clientes atendidos: {assigned}/{len(best_solution.client_assignments)}")
    
    if unassigned > 0:
        print(f"  ⚠️  ATENÇÃO: {unassigned} clientes não foram atendidos!")
    
    # 6. Visualizações
    print("\n[4] Gerando visualizações...")
    if history:
        plot_convergence(history)
    
    plot_solution(instancia, best_solution, "Solução GRASP-VNS")
    
    print("\n" + "=" * 80)
    print("EXECUÇÃO CONCLUÍDA!")
    print("=" * 80)

# ============================================================================
# 10. EXECUÇÃO
# ============================================================================

if __name__ == "__main__":
    main()