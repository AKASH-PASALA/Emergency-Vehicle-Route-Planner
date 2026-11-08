import os
import time
import osmnx as ox


class Graph:
    def __init__(self):
        self.road_graph = None
        self.adjacency = {}
        self.coordinates = {}

    def load_road_network(self):
        cache_file = "mangalagiri_roads.graphml"

        if os.path.exists(cache_file):
            print("Loading cached road network...")
            self.road_graph = ox.load_graphml(cache_file)
        else:
            print("Downloading Mangalagiri road network...")

            center = (16.4308, 80.5688)

            for attempt in range(1, 4):
                try:
                    print(f"Download attempt {attempt}/3")

                    self.road_graph = ox.graph_from_point(
                        center,
                        dist=3000,
                        network_type="drive",
                        simplify=True,
                    )
                    break  # success, stop retrying

                except Exception as e:
                    print("Download failed:", e)

                    if attempt == 3:
                        raise

                    wait_time = 10 * (2 ** (attempt - 1))
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)

            # Only cache after a successful download
            ox.save_graphml(self.road_graph, cache_file)

        self.adjacency = {}
        self.coordinates = {}

        # Create graph nodes
        for node, data in self.road_graph.nodes(data=True):
            self.adjacency[node] = []
            self.coordinates[node] = (data["y"], data["x"])

        # Create graph edges
        for u, v, data in self.road_graph.edges(data=True):
            distance = data.get("length", 1)
            self.adjacency[u].append((v, distance))

        print("\nROAD NETWORK LOADED SUCCESSFULLY!")
        print("Total locations:", len(self.adjacency))
        print("Total roads:", self.road_graph.number_of_edges())

        return self.adjacency, self.coordinates