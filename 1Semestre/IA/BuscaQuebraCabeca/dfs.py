# Estado objetivo
objetivo = (1, 2, 3,
            4, 5, 6,
            7, 8, 0)

# Movimento possível: cima, baixo, esquerda, direita
movimentos = {
    0: [1, 3], 1: [0, 2, 4], 2: [1, 5],
    3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
    6: [3, 7], 7: [4, 6, 8], 8: [5, 7]
}

def mostrar(estado, passo):
    print(f"Movimento {passo}")
    for i in range(0, 9, 3): # imprime a matriz 3x3 em 3 espacos de cada
        print(estado[i:i+3])
    print()

def trocar(estado, i, j): # i = 0, j = vizinho
    lst = list(estado)
    lst[i], lst[j] = lst[j], lst[i] # troca a posição do 0 pelo vizinho
    return tuple(lst) # lista imutavel do novo estado

def dfs(inicial, limite):
    visitados = set() # armazena estados ja visitados

    def recursao(atual, caminho, prof):
        if prof > limite: # evita a busca alem da profundidade limite
            return False
        if atual == objetivo:
            for i, passo in enumerate(caminho + [atual]):
                mostrar(passo, i)
            return True
        visitados.add(atual) # estado atual vai como visitado
        zero = atual.index(0) 
        for m in movimentos[zero]:
            novo = trocar(atual, zero, m) # cria novo estado
            if novo not in visitados: # se nao visitado, faz recursao
                if recursao(novo, caminho + [atual], prof + 1):
                    return True
        return False

    return recursao(inicial, [], 0)

inicial = (1, 3, 2,
           4, 5, 7,
           0, 6, 8)

print("\nDFS:")
if not dfs(inicial, limite=50):
    print("Solução não encontrada.")