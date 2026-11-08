#  Emergency Vehicle Route Planner

### Intelligent Emergency Response Navigation Using Graph Algorithms

An intelligent web-based navigation system designed to calculate optimal routes for emergency vehicles using **Dijkstra's Algorithm and A* (A-Star) Algorithm**.

The system uses real-world road network data from OpenStreetMap to identify the shortest available routes between two selected locations in Mangalagiri, Andhra Pradesh.

It provides a visual comparison of both algorithms, including route distance, execution time, and explored nodes.

---

##  Project Overview

During emergencies, reaching the destination as quickly as possible is critical.

Traditional navigation systems provide routes, but this project focuses on implementing and comparing graph-based shortest-path algorithms on a real-world road network.

The application allows users to:

- Select emergency vehicle types.
- Select starting and destination locations directly on an interactive map.
- Calculate optimal routes using Dijkstra's Algorithm.
- Calculate optimal routes using A* Algorithm.
- Compare the calculated routes.
- View route distances and algorithm performance.
- Visualize both routes simultaneously.

### Supported Emergency Vehicles

-  Ambulance
-  Fire Engine
-  Police Vehicle
-  Rescue Vehicle
-  Disaster Response Vehicle

**Note:** Vehicle selection currently provides interface-level configuration. Vehicle-specific routing priorities and restrictions are planned for future development.

---

##  Project Objectives

1. Implement shortest-path algorithms using Python.
2. Understand real-world applications of graph theory.
3. Integrate OpenStreetMap road network data.
4. Compare Dijkstra's and A* algorithm performance.
5. Develop an interactive navigation interface.
6. Demonstrate how algorithmic optimization can support emergency response systems.

---

##  Technologies Used

### Backend
- Python
- FastAPI
- Uvicorn
- NetworkX
- OSMnx
- Pydantic

### Frontend
- HTML5
- CSS3
- JavaScript
- Leaflet.js

### Mapping and Geographic Data
- OpenStreetMap
- OSMnx
- OpenStreetMap Road Network Data

### Algorithms
- Dijkstra's Shortest Path Algorithm
- A* Search Algorithm
- Priority Queue (Min Heap)
- Haversine Distance Formula

---

##  Project Structure

```text
Emergency-Vehicle-Route-Planner/
│
├── Backend/
│   │
│   ├── main.py
│   ├── graph.py
│   ├── dijkstra.py
│   ├── astar.py
│   ├── test_astar.py
│   ├── requirements.txt
│   │
│   ├── mangalagiri_roads.graphml
│   │
│   └── cache/
│
├── frontend/
│   │
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .gitignore
└── README.md
```

### Backend Files

| File | Responsibility |
|---|---|
| `main.py` | FastAPI application and route API |
| `graph.py` | Loads road network and constructs graph |
| `dijkstra.py` | Implements Dijkstra's algorithm |
| `astar.py` | Implements A* algorithm |
| `test_astar.py` | Tests A* implementation |
| `requirements.txt` | Python dependencies |
| `mangalagiri_roads.graphml` | Stored road network |

### Frontend Files

| File | Responsibility |
|---|---|
| `index.html` | Application structure |
| `style.css` | User interface styling |
| `script.js` | Map interaction and API communication |

---

##  Algorithms Explained

### 1. Dijkstra's Algorithm

Dijkstra's Algorithm finds the shortest path between a starting node and a destination node in a weighted graph with non-negative edge weights.

**Working Principle:**

1. Initialize the distance of every node to infinity.
2. Set the starting node distance to zero.
3. Insert the starting node into a priority queue.
4. Extract the node with the minimum distance.
5. Explore its neighboring nodes.
6. Update distances whenever a shorter path is discovered.
7. Continue until the destination is reached.
8. Reconstruct the shortest path using previous-node information.

**Time Complexity:**

Using a binary heap priority queue:

`O((V + E) log V)`

Where:
- V = Number of vertices.
- E = Number of edges.

**Advantages:**
- Guarantees the shortest path for non-negative edge weights.
- Does not require a heuristic.
- Suitable for weighted road networks.

### 2. A* (A-Star) Algorithm

A* is an informed search algorithm that uses a heuristic function to guide the search toward the destination.

It calculates:

`f(n) = g(n) + h(n)`

Where:

- `g(n)` = Actual cost from the starting node to the current node.
- `h(n)` = Estimated cost from the current node to the destination.
- `f(n)` = Estimated total cost of the path.

**Working Principle:**

1. Initialize the starting node.
2. Calculate the heuristic distance to the destination.
3. Insert the starting node into a priority queue.
4. Select the node with the minimum estimated total cost.
5. Explore neighboring nodes.
6. Calculate the updated path cost.
7. Update the priority queue when a better path is found.
8. Stop when the destination is reached.
9. Reconstruct the optimal path.

**Heuristic Function:**

This project uses the Haversine Formula to calculate the geographical distance between two latitude and longitude coordinates.

The Earth's radius is considered approximately 6,371,000 meters.

**Advantages:**
- Uses geographical information to guide the search.
- Can explore fewer nodes than Dijkstra's Algorithm.
- Efficient for many geographical pathfinding problems.

---

##  How the System Works

The application follows this workflow:

### Step 1: Road Network Loading

The system loads the Mangalagiri road network using OSMnx.

The road network is stored in GraphML format.

### Step 2: Graph Construction

The road network is represented as a weighted graph.

- Vertices represent geographical road locations.
- Edges represent connections between road locations.
- Edge weights represent road distances in meters.

The graph is converted into an adjacency-list representation for efficient processing.

### Step 3: Location Selection

The user selects two locations by clicking on the interactive map.

- First click → Starting location.
- Second click → Destination.

The selected coordinates are passed to the backend.

### Step 4: Nearest Node Identification

The backend identifies the nearest road network nodes corresponding to the selected geographical coordinates using OSMnx.

### Step 5: Route Calculation

Both algorithms execute independently:

- Dijkstra's Algorithm.
- A* Algorithm.

### Step 6: Performance Measurement

The system calculates:

- Total route distance.
- Number of explored nodes.
- Algorithm execution time.

### Step 7: Route Visualization

The calculated routes are returned to the frontend and displayed on the Leaflet map.

-  Red line → Dijkstra's route.
-  Blue line → A* route.

---

##  Data Flow Architecture

```text
              USER
               |
               v
       FRONTEND (HTML/CSS/JS)
               |
               v
       LEAFLET INTERACTIVE MAP
               |
               v
       USER SELECTS LOCATIONS
               |
               v
          FASTAPI BACKEND
               |
               v
       NEAREST ROAD NODE
               |
               v
        GRAPH REPRESENTATION
               |
          +----+----+
          |         |
          v         v
      DIJKSTRA     A*
      ALGORITHM  ALGORITHM
          |         |
          v         v
       SHORTEST   OPTIMAL
         PATH      PATH
          |         |
          +----+----+
               |
               v
       PERFORMANCE ANALYSIS
               |
               v
         JSON RESPONSE
               |
               v
        FRONTEND VISUALIZATION
               |
               v
       ROUTE COMPARISON
```

---

##  API Documentation

The backend is developed using FastAPI.

### Base URL

```text
http://127.0.0.1:8000
```

### 1. Home Endpoint

**GET /**

Checks whether the backend is running.

Example response:

```json
{
    "message": "Emergency Vehicle Route Planner Online",
    "area": "Mangalagiri"
}
```

### 2. Route Calculation Endpoint

**GET /route**

Calculates routes using both algorithms.

Parameters:

| Parameter | Description |
|---|---|
| `start_lat` | Starting latitude |
| `start_lon` | Starting longitude |
| `end_lat` | Destination latitude |
| `end_lon` | Destination longitude |

Example:

```text
http://127.0.0.1:8000/route?start_lat=16.4308&start_lon=80.5688&end_lat=16.4350&end_lon=80.5700
```

The response contains:

- Dijkstra route information.
- A* route information.
- Distance in kilometers.
- Explored nodes.
- Execution time.
- Route coordinates.

### Interactive API Documentation

FastAPI automatically generates API documentation.

```text
http://127.0.0.1:8000/docs
```

---

##  Installation and Execution

### Prerequisites

Install the following:

- Python 3.10 or later.
- Visual Studio Code.
- Git.
- Modern web browser.

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate into the project:

```bash
cd Emergency-Vehicle-Route-Planner
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies

Navigate to the Backend folder:

```bash
cd Backend
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### Step 4: Start the Backend

Run:

```bash
uvicorn main:app --reload
```

The backend will start at:

```text
http://127.0.0.1:8000
```

On startup, the application loads the stored Mangalagiri road network.

If the GraphML file is unavailable, the application attempts to download the road network using OSMnx.

### Step 5: Start the Frontend

Open the `frontend` folder.

Open `index.html` using the VS Code Live Server extension.

Alternatively, open the HTML file directly in your browser.

### Step 6: Use the Application

1. Open the frontend in your browser.
2. Select an emergency vehicle.
3. Click on the map to select the starting location.
4. Click again to select the destination.
5. Click **FIND OPTIMAL ROUTE**.
6. View both calculated routes.
7. Compare the distances and algorithm performance.

---

##  Performance Comparison

The application measures three important parameters:

| Parameter | Description |
|---|---|
| Distance | Total distance of the calculated route |
| Execution Time | Time taken by the algorithm |
| Explored Nodes | Number of nodes processed during the search |

Both algorithms calculate shortest paths using road-distance edge weights.

Their execution times and explored-node counts can be compared to understand their performance on the same road network.

---

##  Geographic Coverage

**Current Implementation:** Mangalagiri, Andhra Pradesh, India.

The project uses OpenStreetMap road network data.

The geographical center used for downloading the road network:

```text
Latitude:  16.4308
Longitude: 80.5688
```

Network configuration:

- Search radius: 3,000 meters.
- Network type: Driving roads.
- Graph representation: Weighted directed graph.
- Road distance: Meters.

---

##  Future Enhancements

The project can be extended with the following features:

1. **Real-Time Traffic Integration**
   - Consider traffic congestion while calculating routes.

2. **Emergency Priority Routing**
   - Introduce emergency vehicle-specific routing priorities.

3. **Dynamic Road Closures**
   - Avoid blocked roads and unavailable routes.

4. **Multi-Vehicle Coordination**
   - Support multiple emergency vehicles simultaneously.

5. **Live GPS Tracking**
   - Track emergency vehicles in real time.

6. **Expanded Geographic Coverage**
   - Support multiple cities and larger geographical regions.

7. **Advanced Route Optimization**
   - Optimize routes using multiple parameters such as distance, travel time, and road conditions.

8. **Mobile Application**
   - Develop a mobile interface for emergency response teams.

---

##  Current Limitations

- The current road network covers a limited geographical area.
- Traffic congestion is not yet considered.
- Route optimization currently focuses on road distance.
- Emergency vehicle selection does not yet change the routing algorithm.
- The application requires an internet connection for map tiles and initial road network downloads when no local graph is available.

---

##  Project Information

**Project Name:** Emergency Vehicle Route Planner

**Domain:** Graph Theory | Algorithms | Web Development | Intelligent Navigation

**Backend:** Python + FastAPI

**Frontend:** HTML + CSS + JavaScript

**Mapping:** OpenStreetMap + Leaflet

**Core Algorithms:** Dijkstra's Algorithm and A* Algorithm

---

##  License

This project is developed for educational and research purposes.

OpenStreetMap data is available under the Open Database License (ODbL).

---

##  Acknowledgements

- OpenStreetMap for geographical and road network data.
- OSMnx for road network acquisition and processing.
- FastAPI for backend API development.
- Leaflet.js for interactive map visualization.
- Python for implementing graph algorithms.

---

**If you find this project interesting, consider giving the repository a ⭐ on GitHub!**