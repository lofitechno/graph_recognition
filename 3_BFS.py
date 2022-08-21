from collections import deque

def init_graph():
    graph = {}
    graph[1] = [2, 5]
    graph[2] = [1, 3, 5]
    graph[3] = [4, 2]
    graph[4] = [2, 3, 5, 6]
    graph[5] = [1, 2, 4, 6]
    graph[6] = [4 ,5]
    return graph

def search(graph, start, end):
    search_queue = deque()
    search_queue += graph[start]
    searched = []
    searched.append(start) #???
    path = [] #???
    while search_queue:
        node  = search_queue.popleft()
        if not node in searched:
            if node == end:
                print(searched)
                #TODO: выделить поиск пути в отдульную функцию
                path.append(end)
                for i in searched[::-1]:
                    if i in graph[path[-1]]:
                        path.append(i)
                #path.append(start)
                print(path[::-1])
                return True
            else:
                search_queue += graph[node]
                searched.append(node)
    return False

def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a
        # new path and push it into the queue
        for adjacent in graph.get(node): #, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


print(search(init_graph(), 2 ,6))

print(bfs(init_graph(), 3 ,6))