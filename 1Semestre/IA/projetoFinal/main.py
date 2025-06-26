from collections import deque

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

print(bfs(lab, start, end))
