from collections import deque
import random
import time


def bfs(lab, start, end):
    rows, cols = len(lab), len(lab[0])
    visited = [[False]*cols for _ in range(rows)]
    queue = deque([(start, [start])])
    
    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x+dx, y+dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if lab[nx][ny] == 0 and not visited[nx][ny]:
                    visited[nx][ny] = True
                    queue.append(((nx, ny), path + [(nx, ny)]))
    
    return "Não foi possível encontrar"

print("Caso 1")
lab = [
    [0, 0, 0, 0],
    [1, 0, 1, 1],
    [1, 0, 1, 1],
    [1, 0, 0, 0]
]
start = (0, 0)
end = (3, 3)

print(bfs(lab, start, end))

print("Caso 2")
lab = [
    [0, 0, 0, 0],
    [1, 0, 1, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 0]
]
start = (0, 0)
end = (3, 3)

print(bfs(lab, start, end))

print("Caso 3")
lab = [
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [1, 0, 1, 0],
    [1, 0, 0, 0]
]
start = (0, 0)
end = (3, 3)


print("")
random.seed(time.time())
tamanho = random.randint(50, 60)
variacao = random.randint(0, 1)
linha = []
matriz = []

for i in range(tamanho):
    linha = []
    for j in range(tamanho):
        linha.append(0)
    matriz.append(linha)

print("matriz inicial: ", matriz)

for i in range(tamanho):
    for j in range(tamanho):
        random.seed = time.time()
        number = random.randint(0, 100)
        if number > 75:
            matriz[i][j] = 1
        else:
            matriz[i][j] = 0

for i in range(tamanho):
    print(matriz[i])
start = (0, 0)
end = (tamanho - 1, tamanho - 1)

retorno = bfs(matriz, start, end)

if retorno != "Não foi possível encontrar" :
    for step in retorno:
        matriz[step[0]][step[1]] = "■"
    for i in range(tamanho):
        for j in range(tamanho):
            matriz[i][j] = str(matriz[i][j])
    for i in range(tamanho):
        print(matriz[i])
    print("Matriz encontrada")
else:
    print(retorno)

print()