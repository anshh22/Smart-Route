document.addEventListener('DOMContentLoaded', () => {
    const startNodeSelect = document.getElementById('startNode');
    const endNodeSelect = document.getElementById('endNode');
    const calculateBtn = document.getElementById('calculateBtn');
    
    const emptyState = document.getElementById('emptyState');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const resultsContent = document.getElementById('resultsContent');
    const totalDistanceEl = document.getElementById('totalDistance');
    const pathTimeline = document.getElementById('pathTimeline');

    let currentGraph = {};
    let coordinates = {};
    let map;
    let markers = {};
    let edgeLines = [];
    let highlightedPathLine = null;

    // Initialize Leaflet Map
    function initMap() {
        // Centered around Uttar Pradesh roughly
        map = L.map('map').setView([26.8467, 80.9462], 6);

        // Add dark-themed tiles (CartoDB Dark Matter)
        L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            subdomains: 'abcd',
            maxZoom: 20
        }).addTo(map);
    }

    initMap();

    // Fetch the default graph when the page loads
    fetch('/api/default_graph')
        .then(response => response.json())
        .then(data => {
            currentGraph = data.graph;
            coordinates = data.coordinates;
            
            populateSelects(Object.keys(currentGraph));
            renderGraphOnMap();
        })
        .catch(error => console.error('Error fetching graph data:', error));

    function populateSelects(nodes) {
        // Sort nodes alphabetically for easier selection
        nodes.sort();
        
        nodes.forEach(node => {
            const startOption = document.createElement('option');
            startOption.value = node;
            startOption.textContent = node;
            startNodeSelect.appendChild(startOption);

            const endOption = document.createElement('option');
            endOption.value = node;
            endOption.textContent = node;
            endNodeSelect.appendChild(endOption);
        });
    }

    function renderGraphOnMap() {
        const drawnEdges = new Set();
        
        // Custom marker icon
        const defaultIcon = L.divIcon({
            className: 'custom-map-marker',
            html: '<div style="width: 8px; height: 8px; background: #3b82f6; border-radius: 50%; border: 2px solid #0b0f19; box-shadow: 0 0 5px rgba(59, 130, 246, 0.8);"></div>',
            iconSize: [12, 12],
            iconAnchor: [6, 6]
        });

        // Add markers for all nodes
        for (const node in coordinates) {
            const lat = coordinates[node].lat;
            const lng = coordinates[node].lng;
            
            const marker = L.marker([lat, lng], {icon: defaultIcon}).addTo(map);
            marker.bindTooltip(node, {
                permanent: false, 
                direction: 'top',
                className: 'map-tooltip'
            });
            markers[node] = marker;
        }

        // Draw edges
        for (const [node, neighbors] of Object.entries(currentGraph)) {
            if (!coordinates[node]) continue;
            const pos1 = [coordinates[node].lat, coordinates[node].lng];
            
            for (const [neighbor, weight] of Object.entries(neighbors)) {
                if (!coordinates[neighbor]) continue;
                
                const edgeKey = [node, neighbor].sort().join('-');
                if (!drawnEdges.has(edgeKey)) {
                    drawnEdges.add(edgeKey);
                    const pos2 = [coordinates[neighbor].lat, coordinates[neighbor].lng];
                    
                    const line = L.polyline([pos1, pos2], {
                        color: 'rgba(255, 255, 255, 0.1)',
                        weight: 1,
                        opacity: 0.5
                    }).addTo(map);
                    
                    edgeLines.push(line);
                }
            }
        }
        
        // Fit map bounds to show all markers
        const group = new L.featureGroup(Object.values(markers));
        map.fitBounds(group.getBounds().pad(0.1));
    }

    calculateBtn.addEventListener('click', () => {
        const start = startNodeSelect.value;
        const end = endNodeSelect.value;

        if (!start || !end) {
            alert('Please select both an origin and destination.');
            return;
        }

        if (start === end) {
            alert('Origin and destination cannot be the same.');
            return;
        }

        // UI State update
        emptyState.classList.add('hidden');
        resultsContent.classList.add('hidden');
        loadingIndicator.classList.remove('hidden');

        const payload = {
            graph: currentGraph,
            start: start,
            end: end
        };

        // Simulate network delay
        setTimeout(() => {
            fetch('/api/calculate_route', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })
            .then(response => response.json())
            .then(data => {
                loadingIndicator.classList.add('hidden');
                
                if (data.success) {
                    renderResults(data.distance, data.path);
                    highlightPathOnMap(data.path);
                } else {
                    alert(data.message || 'Failed to calculate route.');
                    emptyState.classList.remove('hidden');
                }
            })
            .catch(error => {
                console.error('Error calculating route:', error);
                loadingIndicator.classList.add('hidden');
                emptyState.classList.remove('hidden');
                alert('An error occurred while calculating the route.');
            });
        }, 600);
    });

    function renderResults(distance, path) {
        totalDistanceEl.textContent = distance;
        pathTimeline.innerHTML = '';

        path.forEach((node, index) => {
            const item = document.createElement('div');
            item.className = 'timeline-item';
            item.style.animationDelay = `${index * 0.1}s`;

            if (index === 0) item.classList.add('start');
            if (index === path.length - 1) item.classList.add('end');

            let edgeInfo = '';
            if (index < path.length - 1) {
                const nextNode = path[index + 1];
                const edgeWeight = currentGraph[node][nextNode];
                edgeInfo = `<div class="node-edge">Next segment: ${edgeWeight} km</div>`;
            } else {
                edgeInfo = `<div class="node-edge">Destination reached</div>`;
            }

            item.innerHTML = `
                <div class="node-name">${node}</div>
                ${edgeInfo}
            `;
            
            pathTimeline.appendChild(item);
        });

        resultsContent.classList.remove('hidden');
    }

    function highlightPathOnMap(path) {
        // Remove previous highlighted line if exists
        if (highlightedPathLine) {
            map.removeLayer(highlightedPathLine);
        }

        const pathCoords = path.map(node => [coordinates[node].lat, coordinates[node].lng]);

        // Draw new highlighted line
        highlightedPathLine = L.polyline(pathCoords, {
            color: '#10b981', // Success color (green)
            weight: 4,
            opacity: 0.9,
            className: 'glowing-line'
        }).addTo(map);

        // Animate the map to fit the calculated route
        map.fitBounds(highlightedPathLine.getBounds().pad(0.2), {
            animate: true,
            duration: 1.5
        });
    }
});
