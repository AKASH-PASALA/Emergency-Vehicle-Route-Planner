from astar import astar

graph = {
    "A": [("B", 4), ("C", 2)],
    "B": [("D", 5)],
    "C": [("D", 3)],
    "D": []
}

coordinates = {
    "A": (16.50, 80.64),
    "B": (16.51, 80.65),
    "C": (16.52, 80.64),
    "D": (16.53, 80.66)
}

result = astar(graph, "A", "D", coordinates)

print("A* Result:", result)