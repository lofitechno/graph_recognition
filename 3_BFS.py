#Инициализация графа с рисунка из задания
def init_graph():
    graph = {}
    graph[1] = [2, 5]
    graph[2] = [1, 3, 5]
    graph[3] = [4, 2]
    graph[4] = [2, 3, 5, 6]
    graph[5] = [1, 2, 4, 6]
    graph[6] = [4 ,5]
    return graph

# реализация алгоритма поиска в ширину, но с возвращением искомого пути
def search(graph, start, end):
    # очередь путей
    queue = []
    # первый путь в очередь
    queue.append([start])
    while queue:
        # получаем первый путь из очереди
        path = queue.pop(0)
        # получаем крайний узел из пути
        node = path[-1]
        # если путь найден
        if node == end:
            return path
        # перебираем соседние узлы, создаем новый путь и отправляем в очередь
        for adjacent in graph.get(node): #, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)

print(search(init_graph(), 3 ,6))