import heapq
import math
import time


def heuristic(node, end, coordinates):
    lat1, lon1 = coordinates[node]
    lat2, lon2 = coordinates[end]

    R = 6371000  # Earth radius in meters

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    dlat = lat2 - lat1
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )

    return 2 * R * math.asin(math.sqrt(a))


def astar(graph, start, end, coordinates):
    start_time = time.perf_counter()

    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    previous = {}

    queue = [(heuristic(start, end, coordinates), 0, start)]

    explored = 0

    while queue:
        _, current_g, current = heapq.heappop(queue)

        # Ignore outdated queue entries
        if current_g > g_score[current]:
            continue

        explored += 1

        if current == end:
            path = []
            node = end

            while node != start:
                path.append(node)
                node = previous[node]

            path.append(start)
            path.reverse()

            return {
                "path": path,
                "distance": g_score[end],
                "explored_nodes": explored,
                "execution_time_ms": (time.perf_counter() - start_time) * 1000,
            }

        for neighbor, weight in graph.get(current, []):
            tentative_g = current_g + weight

            if tentative_g < g_score.get(neighbor, float('inf')):
                previous[neighbor] = current
                g_score[neighbor] = tentative_g

                f_score = tentative_g + heuristic(neighbor, end, coordinates)
                heapq.heappush(queue, (f_score, tentative_g, neighbor))

    return None  # no path found