def is_safe(graph, color, v, c):
    # проверяем, можем ли назначить выбранный цвет вершине v
    for i in range(len(graph)):
        if graph[v][i] == 1 and color[i] == c:
            return False
    return True


def rec_graph_coloring(graph, k, color, v):
    n = len(graph)
    # проверка, раскрашены ли все вершины
    if v == n:
        return True
    # проверка всех цветов для вершин
    for c in range(1, k + 1):
        if is_safe(graph, color, v, c):
            color[v] = c
            # пробуем рекурсивно раскрасить оставшиеся вершины
            if rec_graph_coloring(graph, k, color, v + 1):
                return True
            # backtracking: убираем цвет, если решение не найдено
            color[v] = 0
    return False


def graph_coloring(n, k, graph):
    color = [0] * n  # инициализация всех цвета как 0 (не раскрашено)
    if rec_graph_coloring(graph, k, color, 0):
        return True, color
    else:
        return False, None


n, k = map(int, input().split())
graph = []

for _ in range(n):
    row = list(input().strip())
    graph.append([int(x) for x in row])
result, coloring = graph_coloring(n, k, graph)

if result:
    print("YES")
    print(" ".join(map(str, coloring)))
else:
    print("NO")