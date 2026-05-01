import heapq

def shortest_path(graph, start, end):
    """
    Finds the shortest path between a start and end node using Dijkstra's algorithm.
    
    :param graph: A dictionary representing the adjacency list of the graph.
                  e.g., {'A': {'B': 1, 'C': 4}, 'B': {'A': 1, 'C': 2}, 'C': {'A': 4, 'B': 2}}
    :param start: The starting node.
    :param end: The ending node.
    :return: A tuple containing the shortest distance and the path.
    """
    if start not in graph or end not in graph:
        return float('inf'), []

    # Priority queue to store (distance, node)
    pq = [(0, start)]
    # Dictionary to store the shortest distance to each node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    # Dictionary to store the path
    previous_nodes = {node: None for node in graph}

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        # If we reached the end node, we can stop
        if current_node == end:
            break

        # If we found a longer path, ignore it
        if current_distance > distances[current_node]:
            continue

        # Explore neighbors
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # If a shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    # Reconstruct the path
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = previous_nodes[current]

    # If the start node is not at the beginning of the path, there is no valid path
    if path and path[0] == start:
        return distances[end], path
    else:
        return float('inf'), []

if __name__ == "__main__":
    # Test case
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 5},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 5, 'C': 1}
    }
    dist, path = shortest_path(graph, 'A', 'D')
    print(f"Shortest distance from A to D: {dist}")
    print(f"Path: {' -> '.join(path)}")
