import numpy as np
import matplotlib.pyplot as plt
import math
import time
from typing import List, Tuple, Dict

def ler_arquivo_tsp(filename: str) -> Dict[int, Tuple[float, float]]:
    """Lê o arquivo TSP e extrai as coordenadas"""
    coordenadas = {}
    
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
        
        # Encontrar onde começam as coordenadas
        start_idx = 0
        for i, line in enumerate(lines):
            if 'Coordenadas:' in line:
                start_idx = i + 1
                break
        
        # Ler coordenadas
        i = start_idx
        while i < len(lines) and not lines[i].startswith('Matriz') and ':' in lines[i]:
            line = lines[i].strip()
            if ':' in line:
                parts = line.split(': ')
                if len(parts) >= 2:
                    idx = int(parts[0])
                    coords_str = parts[1]
                    if ', ' in coords_str:
                        coords = coords_str.split(', ')
                        if len(coords) == 2:
                            try:
                                x = float(coords[0])
                                y = float(coords[1])
                                coordenadas[idx] = (x, y)
                            except ValueError:
                                print(f"Aviso: Não foi possível converter coordenadas na linha: {line}")
            i += 1
            
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        raise
    
    return coordenadas, filename

def calcular_distancia(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calcula a distância euclidiana entre dois pontos"""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def construir_matriz_distancias(coordenadas: Dict[int, Tuple[float, float]]) -> np.ndarray:
    """Constrói a matriz de distâncias entre todas as cidades"""
    n = len(coordenadas)
    distancias = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i + 1, n):
            dist = calcular_distancia(coordenadas[i], coordenadas[j])
            distancias[i][j] = dist
            distancias[j][i] = dist
    
    return distancias

def calcular_distancia_total(rota: List[int], distancias: np.ndarray) -> float:
    """Calcula a distância total de uma rota"""
    distancia = 0
    n = len(rota)
    for i in range(n):
        cidade_atual = rota[i]
        proxima_cidade = rota[(i + 1) % n]
        distancia += distancias[cidade_atual][proxima_cidade]
    return distancia

def tsp_vizinho_mais_proximo_melhorado(distancias: np.ndarray, n_tentativas: int = 10) -> Tuple[List[int], float]:
    """
    Resolve TSP usando vizinho mais próximo com múltiplas tentativas.
    Escolhe a melhor rota entre várias cidades iniciais diferentes.
    """
    n = len(distancias)
    melhor_rota = None
    melhor_distancia = float('inf')
    
    # Testar diferentes cidades iniciais
    for tentativa in range(min(n_tentativas, n)):
        cidade_inicial = tentativa  # Usar diferentes cidades iniciais
        
        visitadas = [False] * n
        rota = [cidade_inicial]
        visitadas[cidade_inicial] = True
        distancia_total = 0
        
        for _ in range(n - 1):
            cidade_atual = rota[-1]
            
            # Encontrar K vizinhos mais próximos
            k = min(5, n - len(rota))  # Considerar os 5 mais próximos
            
            # Obter todas as cidades não visitadas com suas distâncias
            candidatos = []
            for j in range(n):
                if not visitadas[j]:
                    candidatos.append((j, distancias[cidade_atual][j]))
            
            # Ordenar por distância e pegar os K mais próximos
            candidatos.sort(key=lambda x: x[1])
            melhores_candidatos = candidatos[:k]
            
            # Escolher o melhor candidato
            if len(melhores_candidatos) > 1:
                # Heurística: escolher a cidade que também tem vizinhos próximos
                melhor_score = float('inf')
                melhor_cidade = melhores_candidatos[0][0]
                
                for cidade, dist in melhores_candidatos:
                    # Calcular a distância média aos outros não visitados
                    dists_para_outros = []
                    for j in range(n):
                        if not visitadas[j] and j != cidade:
                            dists_para_outros.append(distancias[cidade][j])
                    
                    if dists_para_outros:
                        media_distancias = np.mean(dists_para_outros)
                        # Score combina distância atual e distância futura
                        score = dist * 0.7 + media_distancias * 0.3
                    else:
                        score = dist
                    
                    if score < melhor_score:
                        melhor_score = score
                        melhor_cidade = cidade
                
                proxima_cidade = melhor_cidade
                dist_min = distancias[cidade_atual][proxima_cidade]
            else:
                proxima_cidade = melhores_candidatos[0][0]
                dist_min = melhores_candidatos[0][1]
            
            rota.append(proxima_cidade)
            visitadas[proxima_cidade] = True
            distancia_total += dist_min
        
        # Fechar o ciclo
        distancia_total += distancias[rota[-1]][rota[0]]
        
        # Verificar se é a melhor rota
        if distancia_total < melhor_distancia:
            melhor_distancia = distancia_total
            melhor_rota = rota
    
    return melhor_rota, melhor_distancia

def reorganizar_rota_para_iniciar_em(rota: List[int], cidade_inicial: int) -> List[int]:
    """Reorganiza a rota para iniciar na cidade especificada"""
    if rota[0] == cidade_inicial:
        return rota
    
    try:
        idx = rota.index(cidade_inicial)
        return rota[idx:] + rota[:idx]
    except ValueError:
        # Se a cidade não estiver na rota, retorna a rota original
        return rota

def tsp_insercao_mais_barata(distancias: np.ndarray, cidade_inicial: int = 0) -> Tuple[List[int], float]:
    """
    Algoritmo de inserção mais barata.
    Começa com um triângulo a partir da cidade inicial especificada e insere as demais cidades na posição que menos aumenta a distância.
    """
    n = len(distancias)
    
    if n < 3:
        # Para menos de 3 cidades, usar vizinho mais próximo
        rota, distancia = tsp_vizinho_mais_proximo_melhorado(distancias, n_tentativas=1)
        # Se houver uma cidade inicial específica, reorganizar a rota para começar nela
        if cidade_inicial != 0:
            rota = reorganizar_rota_para_iniciar_em(rota, cidade_inicial)
        return rota, distancia
    
    # Garantir que a cidade inicial está no range válido
    cidade_inicial = cidade_inicial % n
    
    # Iniciar com um sub-tour simples (a cidade inicial + 2 outras mais próximas)
    nao_visitadas = list(range(n))
    nao_visitadas.remove(cidade_inicial)
    
    # Encontrar as 2 cidades mais próximas da cidade inicial
    distancias_inicial = [(j, distancias[cidade_inicial][j]) for j in nao_visitadas]
    distancias_inicial.sort(key=lambda x: x[1])
    duas_mais_proximas = [distancias_inicial[0][0], distancias_inicial[1][0]]
    
    rota = [cidade_inicial] + duas_mais_proximas
    nao_visitadas = [i for i in range(n) if i not in rota]
    
    # Inserir as demais cidades
    while nao_visitadas:
        melhor_custo_aumento = float('inf')
        melhor_cidade = None
        melhor_posicao = -1
        
        for cidade in nao_visitadas:
            # Encontrar a melhor posição para inserir esta cidade
            for pos in range(len(rota)):
                cidade_antes = rota[pos]
                cidade_depois = rota[(pos + 1) % len(rota)]
                
                # Custo de inserção = nova distância - distância antiga
                custo_aumento = (distancias[cidade_antes][cidade] + 
                               distancias[cidade][cidade_depois] - 
                               distancias[cidade_antes][cidade_depois])
                
                if custo_aumento < melhor_custo_aumento:
                    melhor_custo_aumento = custo_aumento
                    melhor_cidade = cidade
                    melhor_posicao = pos + 1  # Inserir após cidade_antes
        
        # Inserir a cidade na melhor posição
        rota.insert(melhor_posicao, melhor_cidade)
        nao_visitadas.remove(melhor_cidade)
    
    # Calcular distância total
    distancia_total = calcular_distancia_total(rota, distancias)
    
    return rota, distancia_total

def two_opt(rota: List[int], distancias: np.ndarray, max_iteracoes: int = 1000) -> Tuple[List[int], float]:
    """Otimização 2-opt com limite de iterações"""
    n = len(rota)
    melhor_rota = rota[:]
    melhor_distancia = calcular_distancia_total(rota, distancias)
    melhorou = True
    iteracoes = 0
    
    while melhorou and iteracoes < max_iteracoes:
        melhorou = False
        iteracoes += 1
        
        for i in range(n - 1):
            for j in range(i + 2, n):
                # Para não mexer na conexão final
                if j == n - 1 and i == 0:
                    continue
                
                # Calcular ganho potencial
                cidade_i = melhor_rota[i]
                cidade_i1 = melhor_rota[(i + 1) % n]
                cidade_j = melhor_rota[j % n]
                cidade_j1 = melhor_rota[(j + 1) % n]
                
                ganho = (distancias[cidade_i][cidade_i1] + 
                        distancias[cidade_j][cidade_j1] - 
                        distancias[cidade_i][cidade_j] - 
                        distancias[cidade_i1][cidade_j1])
                
                if ganho > 0.0001:  # Se houver ganho significativo
                    # Inverter o segmento entre i+1 e j
                    nova_rota = melhor_rota[:]
                    
                    # Corrigir índices para inverter o segmento corretamente
                    if j < n:
                        nova_rota[i+1:j+1] = melhor_rota[j:i:-1]
                    else:
                        # Lidar com caso de índice circular
                        segmento = melhor_rota[i+1:] + melhor_rota[:j-n+1]
                        segmento_invertido = segmento[::-1]
                        nova_rota[i+1:] = segmento_invertido[:n-i-1]
                        nova_rota[:j-n+1] = segmento_invertido[n-i-1:]
                    
                    nova_distancia = melhor_distancia - ganho
                    
                    melhor_rota = nova_rota
                    melhor_distancia = nova_distancia
                    melhorou = True
                    break  # Recomeçar busca
            
            if melhorou:
                break
    
    return melhor_rota, melhor_distancia

def three_opt(rota: List[int], distancias: np.ndarray, max_iter: int = 100) -> Tuple[List[int], float]:
    """Otimização 3-opt simplificada"""
    n = len(rota)
    melhor_rota = rota[:]
    melhor_distancia = calcular_distancia_total(rota, distancias)
    
    for _ in range(max_iter):
        melhorou = False
        
        for i in range(n):
            for j in range(i + 2, min(i + 10, n)):  # Limitar busca para ser mais rápido
                for k in range(j + 2, min(j + 10, n)):
                    
                    # Calcular distância atual deste segmento
                    dist_atual = (distancias[melhor_rota[i]][melhor_rota[(i+1)%n]] +
                                 distancias[melhor_rota[j]][melhor_rota[(j+1)%n]] +
                                 distancias[melhor_rota[k]][melhor_rota[(k+1)%n]])
                    
                    # Testar diferentes permutações
                    permutacoes = [
                        # Trocar dois segmentos
                        [i, j, k],
                        [i, k, j],
                        [j, i, k],
                    ]
                    
                    for perm in permutacoes:
                        # Criar nova rota com esta permutação
                        nova_rota = melhor_rota[:]
                        # Reordenar os segmentos
                        seg1 = nova_rota[i:j+1]
                        seg2 = nova_rota[j+1:k+1]
                        seg3 = nova_rota[k+1:] + nova_rota[:i]
                        
                        # Montar nova rota com a permutação
                        if perm == [i, j, k]:
                            nova_rota = seg3 + seg1 + seg2
                        elif perm == [i, k, j]:
                            nova_rota = seg2 + seg1 + seg3
                        elif perm == [j, i, k]:
                            nova_rota = seg1 + seg3 + seg2
                        
                        # Rotacionar para começar no mesmo ponto
                        idx_inicio = nova_rota.index(melhor_rota[0])
                        nova_rota = nova_rota[idx_inicio:] + nova_rota[:idx_inicio]
                        
                        nova_distancia = calcular_distancia_total(nova_rota, distancias)
                        
                        if nova_distancia < melhor_distancia - 0.001:
                            melhor_rota = nova_rota
                            melhor_distancia = nova_distancia
                            melhorou = True
                            break
                    
                    if melhorou:
                        break
                if melhorou:
                    break
            if melhorou:
                break
    
    return melhor_rota, melhor_distancia

def algoritmo_hierarquico_tsp(distancias: np.ndarray, cidade_inicial: int = 0) -> Tuple[List[int], float]:
    """
    Algoritmo hierárquico que combina múltiplas técnicas:
    1. Inserção mais barata para estrutura inicial
    2. 2-opt para refinamento local
    """
    print("  Fase 1: Construção inicial com inserção mais barata...")
    rota, distancia = tsp_insercao_mais_barata(distancias, cidade_inicial)
    print(f"    Distância inicial: {distancia:.2f}")
    
    print("  Fase 2: Otimização local com 2-opt...")
    rota, distancia = two_opt(rota, distancias, max_iteracoes=500)
    print(f"    Após 2-opt: {distancia:.2f}")
    
    print("  Fase 3: Otimização com 3-opt...")
    if len(distancias) < 500:  # 3-opt é lento para muitos pontos
        rota, distancia = three_opt(rota, distancias, max_iter=50)
        print(f"    Após 3-opt: {distancia:.2f}")
    
    return rota, distancia

def analisar_salto_longo(rota: List[int], distancias: np.ndarray, limite: float = None) -> List[Tuple[int, int, float]]:
    """Identifica saltos muito longos na rota"""
    if limite is None:
        # Calcular limite como 2x a distância média
        limite = np.mean(distancias[distancias > 0]) * 2
    
    saltos_longo = []
    n = len(rota)
    
    for i in range(n):
        cidade_atual = rota[i]
        proxima_cidade = rota[(i + 1) % n]
        distancia = distancias[cidade_atual][proxima_cidade]
        
        if distancia > limite:
            saltos_longo.append((cidade_atual, proxima_cidade, distancia))
    
    return saltos_longo

def suavizar_rota_localmente(rota: List[int], distancias: np.ndarray, max_iter: int = 50) -> Tuple[List[int], float]:
    """Tenta reduzir saltos longos localmente"""
    melhor_rota = rota[:]
    melhor_distancia = calcular_distancia_total(rota, distancias)
    
    for iteracao in range(max_iter):
        saltos_longo = analisar_salto_longo(melhor_rota, distancias)
        
        if not saltos_longo:
            break
        
        # Escolher o pior salto
        pior_salto = max(saltos_longo, key=lambda x: x[2])
        idx_saida, idx_chegada, _ = pior_salto
        
        # Encontrar posições na rota
        try:
            pos_saida = melhor_rota.index(idx_saida)
            pos_chegada = melhor_rota.index(idx_chegada)
        except ValueError:
            # Se não encontrar, continuar
            continue
        
        n = len(melhor_rota)
        
        # Testar diferentes ordenações do segmento entre os pontos problemáticos
        melhorias = []
        
        for tentativa in range(5):  # Testar 5 variações
            nova_rota = melhor_rota[:]
            
            # Determinar segmento
            if pos_chegada > pos_saida:
                segmento_tamanho = pos_chegada - pos_saida + 1
                inicio = pos_saida
            else:
                segmento_tamanho = n - pos_saida + pos_chegada + 1
                inicio = pos_saida
            
            # Para segmentos pequenos, não vale a pena modificar muito
            if segmento_tamanho < 4:
                continue
            
            # Criar nova ordenação para o segmento (exceto os extremos)
            if tentativa == 0:
                # Ordem original
                pass
            elif tentativa == 1:
                # Inverter ordem interna do segmento
                if pos_chegada > pos_saida:
                    meio = (pos_saida + pos_chegada) // 2
                    nova_rota[pos_saida+1:pos_chegada] = melhor_rota[pos_chegada-1:pos_saida:-1]
                else:
                    # Caso circular - mais complexo, pular por enquanto
                    continue
            else:
                # Embaralhar aleatoriamente parte do segmento
                if segmento_tamanho > 6:
                    if pos_chegada > pos_saida:
                        # Selecionar parte do segmento para embaralhar
                        meio_inicio = pos_saida + 2
                        meio_fim = pos_chegada - 2
                        if meio_fim > meio_inicio:
                            segmento_meio = nova_rota[meio_inicio:meio_fim]
                            np.random.shuffle(segmento_meio)
                            nova_rota[meio_inicio:meio_fim] = segmento_meio
            
            nova_distancia = calcular_distancia_total(nova_rota, distancias)
            
            if nova_distancia < melhor_distancia - 0.001:
                melhorias.append((nova_rota, nova_distancia))
        
        if melhorias:
            # Escolher a melhor melhoria
            melhor_rota, melhor_distancia = min(melhorias, key=lambda x: x[1])
    
    return melhor_rota, melhor_distancia

def plotar_rota(coordenadas: Dict[int, Tuple[float, float]], rota: List[int], 
                titulo: str, destaque_saltos: bool = False, distancias: np.ndarray = None):
    """Plota a rota do caixeiro viajante"""
    # Extrair coordenadas x e y
    x = [coordenadas[i][0] for i in rota] + [coordenadas[rota[0]][0]]
    y = [coordenadas[i][1] for i in rota] + [coordenadas[rota[0]][1]]
    
    fig, ax = plt.subplots(figsize=(14, 12))
    
    # Plotar todas as cidades em cinza claro
    todas_x = [coordenadas[i][0] for i in range(len(coordenadas))]
    todas_y = [coordenadas[i][1] for i in range(len(coordenadas))]
    ax.scatter(todas_x, todas_y, c='lightgray', s=30, alpha=0.5, 
               edgecolors='gray', linewidth=0.5, label='Todas as cidades')
    
    # Destacar pontos da rota
    ax.scatter(x[:-1], y[:-1], c='red', s=50, alpha=0.8, 
               edgecolors='black', linewidth=1, zorder=5, label='Cidades da rota')
    
    # Plotar rota
    ax.plot(x, y, 'b-', linewidth=1.5, alpha=0.7, zorder=4, label='Rota TSP')
    
    # Destacar saltos longos se solicitado
    if destaque_saltos and distancias is not None:
        saltos_longo = analisar_salto_longo(rota, distancias)
        
        for saida, chegada, dist in saltos_longo:
            x_saida = coordenadas[saida][0]
            y_saida = coordenadas[saida][1]
            x_chegada = coordenadas[chegada][0]
            y_chegada = coordenadas[chegada][1]
            
            ax.plot([x_saida, x_chegada], [y_saida, y_chegada], 
                   'r--', linewidth=2, alpha=0.8, zorder=3, label='Saltos longos' if saida == saltos_longo[0][0] else "")
    
    # Adicionar seta indicando direção (no meio do percurso)
    if len(x) > 3:
        meio = len(x) // 2
        if meio + 1 < len(x):
            dx = x[meio+1] - x[meio]
            dy = y[meio+1] - y[meio]
            # Normalizar para seta de tamanho fixo
            norma = math.sqrt(dx**2 + dy**2)
            if norma > 0:
                dx_norm = dx / norma * 10
                dy_norm = dy / norma * 10
                ax.arrow(x[meio], y[meio], dx_norm, dy_norm, 
                        head_width=3, head_length=5, fc='green', ec='green', zorder=6)
    
    ax.set_title(titulo, fontsize=14, fontweight='bold')
    ax.set_xlabel('Coordenada X', fontsize=12)
    ax.set_ylabel('Coordenada Y', fontsize=12)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.axis('equal')
    
    # Adicionar legenda (evitando duplicatas)
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper right', fontsize=10)
    
    plt.tight_layout()
    plt.show()

def salvar_solucao_arquivo(coordenadas: Dict[int, Tuple[float, float]], 
                          rota: List[int], distancia: float, 
                          distancias: np.ndarray, filename: str = 'solucao_tsp.txt'):
    """Salva a solução encontrada em um arquivo de texto formatado"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # Cabeçalho
            f.write("MELHOR SOLUÇÃO ENCONTRADA\n")
            f.write("=" * 60 + "\n")
            f.write(f"Distância total: {distancia:.4f}\n\n")
            
            # Informações gerais
            f.write("INFORMAÇÕES GERAIS\n")
            f.write("-" * 60 + "\n")
            f.write(f"Número de cidades: {len(rota)}\n")
            
            # Calcular estatísticas
            distancias_segmentos = []
            for i in range(len(rota)):
                cidade_atual = rota[i]
                proxima_cidade = rota[(i + 1) % len(rota)]
                distancias_segmentos.append(distancias[cidade_atual][proxima_cidade])
            
            distancia_media = np.mean(distancias_segmentos)
            distancia_max = np.max(distancias_segmentos)
            distancia_min = np.min(distancias_segmentos)
            
            f.write(f"Distância média entre cidades: {distancia_media:.4f}\n")
            f.write(f"Maior distância entre cidades consecutivas: {distancia_max:.4f}\n")
            f.write(f"Menor distância entre cidades consecutivas: {distancia_min:.4f}\n\n")
            
            # Rota completa
            f.write("ROTA COMPLETA\n")
            f.write("-" * 60 + "\n")
            f.write("Rota (arestas no formato i -> j):\n")
            
            # Imprimir todas as arestas
            for i in range(len(rota)):
                cidade_atual = rota[i]
                proxima_cidade = rota[(i + 1) % len(rota)]
                distancia_aresta = distancias[cidade_atual][proxima_cidade]
                
                # Formato: i -> j
                f.write(f"{cidade_atual} -> {proxima_cidade}\n")
                
            # Lista sequencial das cidades
            f.write("\nSEQUÊNCIA DE CIDADES\n")
            f.write("-" * 60 + "\n")
            f.write("Ordem de visitação:\n")
            
            # Agrupar em linhas de 10 cidades para melhor leitura
            for i in range(0, len(rota), 10):
                linha_cidades = rota[i:i+10]
                linha_str = "  ".join(f"{cidade:3d}" for cidade in linha_cidades)
                f.write(f"{linha_str}\n")
            
            # Primeira linha: início da sequência
            f.write("\nCiclo completo (início -> ... -> retorno ao início):\n")
            f.write(f"{rota[0]} -> ... -> {rota[-1]} -> {rota[0]}\n")
            
        print(f"✓ Solução salva em '{filename}'")
        
    except Exception as e:
        print(f"✗ Erro ao salvar solução: {e}")

def main():
    print("="*70)
    print("SOLUÇÃO PARA O PROBLEMA DO CAIXEIRO VIAJANTE (TSP)")
    print("="*70)
    
    # Ler dados do arquivo
    print("\n1. LENDO ARQUIVO DE DADOS...")
    try:
        filename = '200_tsp.txt'
        coordenadas, filename = ler_arquivo_tsp(filename)
        
        if not coordenadas:
            print("ERRO: Nenhuma coordenada foi carregada do arquivo.")
            return
        
        n_cidades = len(coordenadas)
        print(f"   ✓ {n_cidades} cidades carregadas")
        
        # Verificar se todas as cidades de 0 a n-1 estão presentes
        if set(coordenadas.keys()) != set(range(n_cidades)):
            print("   ⚠  Aviso: As cidades não estão numeradas de 0 a n-1")
            print(f"   ⚠  Cidades encontradas: {sorted(coordenadas.keys())[:10]}...")
        
        x_vals = [c[0] for c in coordenadas.values()]
        y_vals = [c[1] for c in coordenadas.values()]
        print(f"   ✓ Coordenadas X: {min(x_vals):.1f} a {max(x_vals):.1f}")
        print(f"   ✓ Coordenadas Y: {min(y_vals):.1f} a {max(y_vals):.1f}")
        
    except Exception as e:
        print(f"ERRO ao ler arquivo: {e}")
        return
    
    # Construir matriz de distâncias
    print("\n2. CALCULANDO MATRIZ DE DISTÂNCIAS...")
    try:
        distancias = construir_matriz_distancias(coordenadas)
        distancia_media = np.mean(distancias[distancias > 0])
        print(f"   ✓ Matriz {n_cidades}x{n_cidades} calculada")
        print(f"   ✓ Distância média entre cidades: {distancia_media:.2f}")
    except Exception as e:
        print(f"ERRO ao calcular matriz de distâncias: {e}")
        return
    
    # Resolver TSP com algoritmo hierárquico
    print("\n3. RESOLVENDO TSP COM ALGORITMO HIERÁRQUICO...")
    start_time = time.time()
    try:
        # Definir cidade inicial (0 = primeira cidade)
        cidade_inicial = 0
        rota_otimizada, dist_otimizada = algoritmo_hierarquico_tsp(distancias, cidade_inicial)
        
        # Garantir que a rota começa na cidade inicial
        rota_otimizada = reorganizar_rota_para_iniciar_em(rota_otimizada, cidade_inicial)
        
        print(f"   ✓ Distância após algoritmo hierárquico: {dist_otimizada:.2f}")
        print(f"   ✓ Rota inicia na cidade: {cidade_inicial}")
    except Exception as e:
        print(f"ERRO ao resolver TSP: {e}")
        return
    
    # Tentar suavizar saltos longos
    print("\n4. SUAVIZANDO SALTOS LONGOS...")
    try:
        rota_suavizada, dist_suavizada = suavizar_rota_localmente(rota_otimizada, distancias, max_iter=20)
        
        if dist_suavizada < dist_otimizada - 0.01:
            print(f"   ✓ Melhoria adicional: {dist_otimizada:.2f} → {dist_suavizada:.2f}")
            rota_final = rota_suavizada
            dist_final = dist_suavizada
        else:
            rota_final = rota_otimizada
            dist_final = dist_otimizada
            print(f"   ✓ Distância mantida: {dist_otimizada:.2f}")
        
        # Garantir que a rota final começa na cidade inicial
        rota_final = reorganizar_rota_para_iniciar_em(rota_final, cidade_inicial)
        
    except Exception as e:
        print(f"   ⚠  Aviso ao suavizar rota: {e}")
        rota_final = rota_otimizada
        dist_final = dist_otimizada
    
    tempo_total = time.time() - start_time
    
    # Analisar qualidade da rota
    print("\n5. ANALISANDO QUALIDADE DA SOLUÇÃO...")
    try:
        saltos_longo = analisar_salto_longo(rota_final, distancias)
        n_saltos_longo = len(saltos_longo)
        
        # Calcular distâncias dos segmentos
        distancias_segmentos = []
        for i in range(n_cidades):
            cidade_atual = rota_final[i]
            proxima_cidade = rota_final[(i + 1) % n_cidades]
            distancias_segmentos.append(distancias[cidade_atual][proxima_cidade])
        
        # Exibir resultados
        print("\n" + "="*70)
        print("RESULTADOS FINAIS")
        print("="*70)
        
        print(f"\n📊 ESTATÍSTICAS GERAIS:")
        print(f"   • Número de cidades: {n_cidades}")
        print(f"   • Tempo de execução: {tempo_total:.2f} segundos")
        print(f"   • Distância total da rota: {dist_final:.4f}")
        print(f"   • Cidade inicial: {cidade_inicial}")
        
        print(f"\n📈 ANÁLISE DA ROTA:")
        print(f"   • Distância média entre cidades consecutivas: {np.mean(distancias_segmentos):.4f}")
        print(f"   • Desvio padrão: {np.std(distancias_segmentos):.4f}")
        print(f"   • Distância máxima: {np.max(distancias_segmentos):.4f}")
        print(f"   • Distância mínima: {np.min(distancias_segmentos):.4f}")
        
        limite_salto = distancia_media * 2
        print(f"   • Número de saltos longos (> {limite_salto:.1f}): {n_saltos_longo}")
        
        if n_saltos_longo > 0:
            print(f"   • Piores saltos:")
            saltos_longo.sort(key=lambda x: x[2], reverse=True)
            for i, (saida, chegada, dist) in enumerate(saltos_longo[:3]):
                print(f"     {i+1}. Cidade {saida:3d} → Cidade {chegada:3d}: {dist:7.2f} (limite: {limite_salto:.1f})")
        
        print(f"\n📍 PRIMEIRAS 10 CIDADES DA ROTA:")
        for i in range(min(10, n_cidades)):
            cidade = rota_final[i]
            x, y = coordenadas[cidade]
            print(f"   {i+1:2d}. Cidade {cidade:3d} - Posição: ({x:6.1f}, {y:6.1f})")
        
        if n_cidades > 10:
            print(f"   ... e mais {n_cidades - 10} cidades")
        
        print(f"\n🔄 ROTA COMPLETA (ciclo fechado):")
        rota_str = " → ".join(str(c) for c in rota_final[:8])
        print(f"   {rota_str} → ... → {rota_final[0]}")
        
        # Plotar rota
        print("\n📊 GERANDO VISUALIZAÇÕES...")
        plotar_rota(coordenadas, rota_final, 
                   f'Rota TSP Otimizada (Início: cidade {cidade_inicial})\n{n_cidades} cidades, Distância total: {dist_final:.2f}',
                   destaque_saltos=True, distancias=distancias)
        
        # SALVAR SOLUÇÃO EM ARQUIVO
        print("\n💾 SALVANDO SOLUÇÃO EM ARQUIVO...")
        base_name = filename.rsplit('.', 1)[0] if '.' in filename else filename
        salvar_solucao_arquivo(coordenadas, rota_final, dist_final, distancias, f'melhor_solucao_{base_name}.txt')
        
        # Gráfico de distribuição das distâncias
        fig, axs = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histograma das distâncias entre cidades consecutivas
        axs[0].hist(distancias_segmentos, bins=30, edgecolor='black', alpha=0.7, color='skyblue')
        axs[0].axvline(np.mean(distancias_segmentos), color='red', linestyle='--', 
                      label=f'Média: {np.mean(distancias_segmentos):.2f}')
        axs[0].axvline(distancia_media, color='green', linestyle=':', 
                      label=f'Média global: {distancia_media:.2f}')
        axs[0].axvline(limite_salto, color='orange', linestyle=':', 
                      label=f'Limite salto longo: {limite_salto:.1f}')
        axs[0].set_xlabel('Distância entre cidades consecutivas')
        axs[0].set_ylabel('Frequência')
        axs[0].set_title('Distribuição das distâncias na rota')
        axs[0].legend()
        axs[0].grid(True, alpha=0.3)
        
        # Distâncias acumuladas
        distancias_acumuladas = np.cumsum(distancias_segmentos)
        axs[1].plot(range(n_cidades), distancias_acumuladas, 'b-', linewidth=2)
        axs[1].fill_between(range(n_cidades), 0, distancias_acumuladas, alpha=0.3)
        axs[1].set_xlabel('Número de cidades visitadas')
        axs[1].set_ylabel('Distância acumulada')
        axs[1].set_title('Distância acumulada ao longo da rota')
        axs[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"ERRO na análise final: {e}")
    
    print("\n" + "="*70)
    print("SOLUÇÃO COMPLETA! ✓")
    print("="*70)

if __name__ == "__main__":
    main()