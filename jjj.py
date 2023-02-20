import heapq

def ucs(graph, start, goal):
    # initialize the priority queue with the start node
    queue = [(0, start, [])]
    # initialize the set of explored nodes
    explored = set()

    while queue:
        # get the node with the lowest cost
        (cost, node, path) = heapq.heappop(queue)
        print(node)
        # if we have reached the goal node, return the path
        if node == goal:
            return path + [node]
        # if the node has not been explored yet, add it to the explored set
        if node not in explored:
            explored.add(node)
            # consider all neighboring nodes
            for neighbor, neighbor_cost in graph[node].items():
                if neighbor not in explored:
                    print(neighbor)
                    # calculate the total cost of the path to the neighbor
                    total_cost = cost + neighbor_cost
                    # add the neighbor to the priority queue with its total cost
                    heapq.heappush(queue, (total_cost, neighbor, path + [node]))

    # if no path to the goal node was found, return None
    return None
graph = {'A': {'B': 2, 'C': 1},
         'B': {'A': 2, 'C': 3},
         'C': {'A': 1, 'B': 3}}
print(ucs(graph,'A','C'))