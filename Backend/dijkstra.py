import heapq
import time


def dijkstra(graph, start, end):
    start_time = time.perf_counter()

    if start not in graph or end not in graph:
        return None

    distances = {node: float('inf') for node in graph}
    previous = {}

    distances[start] = 0

    queue = [(0, start)]
    explored = 0

    while queue:
        current_distance, current = heapq.heappop(queue)

        # Ignore outdated queue entries
        if current_distance > distances[current]:
            continue

        explored += 1

        if current == end:
            break

        for neighbor, weight in graph[current]:
            new_distance = current_distance + weight

            if new_distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_distance
                previous[neighbor] = current
                heapq.heappush(queue, (new_distance, neighbor))

    if distances[end] == float('inf'):
        return None

    path = []
    current = end

    while current != start:
        path.append(current)
        current = previous[current]

    path.append(start)
    path.reverse()

    return {
        "path": path,
        "distance": distances[end],
        "explored_nodes": explored,
        "execution_time_ms": (time.perf_counter() - start_time) * 1000,
    }