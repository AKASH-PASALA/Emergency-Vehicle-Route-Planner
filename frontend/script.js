const API = "http://127.0.0.1:8000";

const map = L.map("map").setView([16.4308, 80.5688], 14);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors"
}).addTo(map);

// Selected locations
let startPoint = null;
let endPoint = null;

// Map markers
let startMarker = null;
let endMarker = null;

// Route layers
let dijkstraLayer = null;
let astarLayer = null;

// Select locations by clicking map
map.on("click", function (event) {
    const lat = event.latlng.lat;
    const lon = event.latlng.lng;

    if (!startPoint) {
        startPoint = { lat, lon };

        startMarker = L.marker([lat, lon])
            .addTo(map)
            .bindPopup("Starting Location")
            .openPopup();

        document.getElementById("start").value =
            `${lat.toFixed(5)}, ${lon.toFixed(5)}`;
    } else if (!endPoint) {
        endPoint = { lat, lon };

        endMarker = L.marker([lat, lon])
            .addTo(map)
            .bindPopup("Destination")
            .openPopup();

        document.getElementById("end").value =
            `${lat.toFixed(5)}, ${lon.toFixed(5)}`;
    } else {
        alert("Reset locations before selecting new points.");
    }
});

// Calculate routes
document.getElementById("calculate").addEventListener("click", calculateRoute);

async function calculateRoute() {
    if (!startPoint || !endPoint) {
        alert("Please select both locations on the map.");
        return;
    }

    const button = document.getElementById("calculate");
    button.disabled = true;
    button.innerText = "CALCULATING...";

    try {
        const params = new URLSearchParams({
            start_lat: startPoint.lat,
            start_lon: startPoint.lon,
            end_lat: endPoint.lat,
            end_lon: endPoint.lon
        });

        const response = await fetch(`${API}/route?${params.toString()}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Route calculation failed");
        }

        // Remove previous routes
        if (dijkstraLayer) map.removeLayer(dijkstraLayer);
        if (astarLayer) map.removeLayer(astarLayer);

        // Dijkstra route
        dijkstraLayer = L.polyline(data.dijkstra.coordinates, {
            color: "#ff3b3b",
            weight: 6
        }).addTo(map);

        // A* route
        astarLayer = L.polyline(data.astar.coordinates, {
            color: "#3399ff",
            weight: 4,
            dashArray: "8, 8"
        }).addTo(map);

        // Dijkstra results
        document.getElementById("dijkstra-distance").innerText =
            data.dijkstra.distance_km + " km";
        document.getElementById("dijkstra-path").innerText =
            `Explored: ${data.dijkstra.explored_nodes} nodes | ` +
            `Time: ${data.dijkstra.execution_time_ms.toFixed(3)} ms`;

        // A* results
        document.getElementById("astar-distance").innerText =
            data.astar.distance_km + " km";
        document.getElementById("astar-path").innerText =
            `Explored: ${data.astar.explored_nodes} nodes | ` +
            `Time: ${data.astar.execution_time_ms.toFixed(3)} ms`;

        // Vehicle information
        const vehicle = document.getElementById("vehicle").value;
        document.getElementById("vehicle-info").innerText =
            `Selected Vehicle: ${vehicle}`;

        // Fit map to both routes
        const combinedRoutes = L.featureGroup([dijkstraLayer, astarLayer]);
        map.fitBounds(combinedRoutes.getBounds(), { padding: [40, 40] });

    } catch (error) {
        console.error(error);
        alert(error.message);
    } finally {
        button.disabled = false;
        button.innerText = "FIND OPTIMAL ROUTE";
    }
}   // <-- this closing brace was missing

// Reset map selections
document.getElementById("reset").addEventListener("click", function () {
    startPoint = null;
    endPoint = null;

    if (startMarker) map.removeLayer(startMarker);
    if (endMarker) map.removeLayer(endMarker);
    if (dijkstraLayer) map.removeLayer(dijkstraLayer);
    if (astarLayer) map.removeLayer(astarLayer);

    startMarker = null;
    endMarker = null;
    dijkstraLayer = null;
    astarLayer = null;

    document.getElementById("start").value = "";
    document.getElementById("end").value = "";

    document.getElementById("dijkstra-distance").innerText = "--";
    document.getElementById("astar-distance").innerText = "--";
    document.getElementById("dijkstra-path").innerText = "Waiting for calculation";
    document.getElementById("astar-path").innerText = "Waiting for calculation";
});

// Update vehicle information when selection changes
document.getElementById("vehicle").addEventListener("change", function () {
    document.getElementById("vehicle-info").innerText =
        `Selected Vehicle: ${this.value}`;
});