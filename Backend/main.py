from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import osmnx as ox

from graph import Graph
from dijkstra import dijkstra
from astar import astar

app = FastAPI(title="Emergency Vehicle Route Planner")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

road_network = Graph()


@app.on_event("startup")
def startup():
    print("Loading Mangalagiri road network...")
    road_network.load_road_network()
    print("Emergency Route Planner is ready!")


@app.get("/")
def home():
    return {
        "message": "Emergency Vehicle Route Planner Online",
        "area": "Mangalagiri"
    }


@app.get("/route")
def calculate_route(
    start_lat: float,
    start_lon: float,
    end_lat: float,
    end_lon: float
):

    G = road_network.road_graph

    try:
        start = ox.distance.nearest_nodes(
            G, start_lon, start_lat
        )

        end = ox.distance.nearest_nodes(
            G, end_lon, end_lat
        )

        graph = road_network.adjacency
        coordinates = road_network.coordinates

        if start == end:
            raise HTTPException(
                status_code=400,
                detail="Select two different locations."
            )

        result_dijkstra = dijkstra(graph, start, end)

        result_astar = astar(
            graph, start, end, coordinates
        )

        if not result_dijkstra or not result_astar:
            raise HTTPException(
                status_code=404,
                detail="No route found."
            )

        return {
            "dijkstra": {
                **result_dijkstra,
                "distance_km": round(
                    result_dijkstra["distance"] / 1000, 2
                ),
                "coordinates": [
                    coordinates[node]
                    for node in result_dijkstra["path"]
                ]
            },

            "astar": {
                **result_astar,
                "distance_km": round(
                    result_astar["distance"] / 1000, 2
                ),
                "coordinates": [
                    coordinates[node]
                    for node in result_astar["path"]
                ]
            }
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )