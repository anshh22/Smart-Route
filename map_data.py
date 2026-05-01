import math

# Approximate coordinates for major cities/districts in North India
districts_data = {
    # Delhi / NCR
    "New Delhi": {"lat": 28.6139, "lng": 77.2090},
    "Gurugram": {"lat": 28.4595, "lng": 77.0266},
    "Faridabad": {"lat": 28.4089, "lng": 77.3178},
    "Noida": {"lat": 28.5355, "lng": 77.3910},
    "Ghaziabad": {"lat": 28.6692, "lng": 77.4538},

    # Haryana
    "Chandigarh": {"lat": 30.7333, "lng": 76.7794},
    "Ambala": {"lat": 30.3782, "lng": 76.7767},
    "Karnal": {"lat": 29.6857, "lng": 76.9905},
    "Panipat": {"lat": 29.3909, "lng": 76.9635},
    "Rohtak": {"lat": 28.8955, "lng": 76.5833},
    "Hisar": {"lat": 29.1492, "lng": 75.7217},

    # Punjab
    "Amritsar": {"lat": 31.6340, "lng": 74.8723},
    "Jalandhar": {"lat": 31.3260, "lng": 75.5762},
    "Ludhiana": {"lat": 30.9010, "lng": 75.8573},
    "Patiala": {"lat": 30.3398, "lng": 76.3869},
    "Bathinda": {"lat": 30.2110, "lng": 74.9455},
    "Pathankot": {"lat": 32.2688, "lng": 75.6457},

    # Rajasthan
    "Jaipur": {"lat": 26.9124, "lng": 75.7873},
    "Jodhpur": {"lat": 26.2389, "lng": 73.0243},
    "Udaipur": {"lat": 24.5854, "lng": 73.7125},
    "Kota": {"lat": 25.2138, "lng": 75.8648},
    "Bikaner": {"lat": 28.0229, "lng": 73.3119},
    "Ajmer": {"lat": 26.4499, "lng": 74.6399},
    "Alwar": {"lat": 27.5530, "lng": 76.6346},

    # Uttarakhand
    "Dehradun": {"lat": 30.3165, "lng": 78.0322},
    "Haridwar": {"lat": 29.9457, "lng": 78.1642},
    "Rishikesh": {"lat": 30.0869, "lng": 78.2676},
    "Nainital": {"lat": 29.3919, "lng": 79.4542},
    "Roorkee": {"lat": 29.8543, "lng": 77.8880},

    # Himachal Pradesh
    "Shimla": {"lat": 31.1048, "lng": 77.1734},
    "Manali": {"lat": 32.2396, "lng": 77.1887},
    "Dharamshala": {"lat": 32.2190, "lng": 76.3234},
    "Mandi": {"lat": 31.5892, "lng": 76.9318},

    # Jammu & Kashmir (Major nodes)
    "Jammu": {"lat": 32.7266, "lng": 74.8570},
    "Srinagar": {"lat": 34.0837, "lng": 74.7973},
    
    # Ladakh
    "Leh": {"lat": 34.1526, "lng": 77.5771},

    # Uttar Pradesh (subset of major cities to keep it balanced)
    "Lucknow": {"lat": 26.8467, "lng": 80.9462},
    "Kanpur": {"lat": 26.4499, "lng": 80.3319},
    "Agra": {"lat": 27.1767, "lng": 78.0081},
    "Varanasi": {"lat": 25.3176, "lng": 82.9739},
    "Prayagraj": {"lat": 25.4358, "lng": 81.8463},
    "Meerut": {"lat": 28.9845, "lng": 77.7064},
    "Bareilly": {"lat": 28.3670, "lng": 79.4304},
    "Gorakhpur": {"lat": 26.7606, "lng": 83.3732},
    "Aligarh": {"lat": 27.8974, "lng": 78.0880},
    "Mathura": {"lat": 27.4924, "lng": 77.6737},
    "Ayodhya": {"lat": 26.7922, "lng": 82.1998},
    "Jhansi": {"lat": 25.4484, "lng": 78.5685},

    # Madhya Pradesh (Northern parts interfacing with UP/RJ)
    "Gwalior": {"lat": 26.2124, "lng": 78.1772},
    "Bhopal": {"lat": 23.2599, "lng": 77.4126},
    "Indore": {"lat": 22.7196, "lng": 75.8577},
    
    # Bihar (Western edge)
    "Patna": {"lat": 25.5941, "lng": 85.1376},
    "Gaya": {"lat": 24.7914, "lng": 85.0002}
}

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance using Haversine formula in km."""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def build_district_graph():
    """Builds an adjacency graph linking nearby cities."""
    graph = {}
    for d1 in districts_data:
        graph[d1] = {}
        # Calculate distances to all other cities
        distances = []
        for d2 in districts_data:
            if d1 != d2:
                dist = calculate_distance(
                    districts_data[d1]['lat'], districts_data[d1]['lng'],
                    districts_data[d2]['lat'], districts_data[d2]['lng']
                )
                distances.append((d2, dist))
        
        # Sort by distance and connect to closest 5-6 cities to form a solid mesh
        distances.sort(key=lambda x: x[1])
        for neighbor, dist in distances[:6]:
            # Add some variation to simulate road distance instead of straight line air distance
            road_dist = int(dist * 1.3)
            graph[d1][neighbor] = road_dist
            
    # Ensure graph is bidirectional
    for d1 in graph:
        for d2, dist in graph[d1].items():
            if d1 not in graph[d2]:
                graph[d2][d1] = dist
            elif graph[d2][d1] != dist:
                # Keep consistent if any mismatch happened
                graph[d2][d1] = dist
                
    return graph

north_india_graph = build_district_graph()
