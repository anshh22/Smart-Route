import math

# Approximate coordinates for Uttar Pradesh Districts
districts_data = {
    "Agra": {"lat": 27.1767, "lng": 78.0081},
    "Aligarh": {"lat": 27.8974, "lng": 78.0880},
    "Prayagraj": {"lat": 25.4358, "lng": 81.8463}, # Allahabad
    "Ambedkar Nagar": {"lat": 26.4071, "lng": 82.3980},
    "Amethi": {"lat": 26.1623, "lng": 81.8124},
    "Amroha": {"lat": 28.9044, "lng": 78.4674},
    "Auraiya": {"lat": 26.4638, "lng": 79.5222},
    "Ayodhya": {"lat": 26.7922, "lng": 82.1998},
    "Azamgarh": {"lat": 26.0688, "lng": 83.1859},
    "Baghpat": {"lat": 28.9482, "lng": 77.2687},
    "Bahraich": {"lat": 27.5750, "lng": 81.5975},
    "Ballia": {"lat": 25.7594, "lng": 84.1504},
    "Balrampur": {"lat": 27.4293, "lng": 82.1764},
    "Banda": {"lat": 25.4746, "lng": 80.3346},
    "Barabanki": {"lat": 26.9329, "lng": 81.1895},
    "Bareilly": {"lat": 28.3670, "lng": 79.4304},
    "Basti": {"lat": 26.7909, "lng": 82.8988},
    "Bhadohi": {"lat": 25.4055, "lng": 82.5695},
    "Bijnor": {"lat": 29.3724, "lng": 78.1358},
    "Budaun": {"lat": 28.0306, "lng": 79.1272},
    "Bulandshahr": {"lat": 28.4069, "lng": 77.8498},
    "Chandauli": {"lat": 25.2638, "lng": 83.2662},
    "Chitrakoot": {"lat": 25.2014, "lng": 80.9238},
    "Deoria": {"lat": 26.5050, "lng": 83.7845},
    "Etah": {"lat": 27.5583, "lng": 78.6657},
    "Etawah": {"lat": 26.7725, "lng": 79.0253},
    "Farrukhabad": {"lat": 27.3820, "lng": 79.5878},
    "Fatehpur": {"lat": 25.9272, "lng": 80.8143},
    "Firozabad": {"lat": 27.1557, "lng": 78.3956},
    "Gautam Buddha Nagar": {"lat": 28.4744, "lng": 77.5040}, # Noida area
    "Ghaziabad": {"lat": 28.6692, "lng": 77.4538},
    "Ghazipur": {"lat": 25.5804, "lng": 83.5772},
    "Gonda": {"lat": 27.1354, "lng": 81.9616},
    "Gorakhpur": {"lat": 26.7606, "lng": 83.3732},
    "Hamirpur": {"lat": 25.9529, "lng": 80.1481},
    "Hapur": {"lat": 28.7306, "lng": 77.7759},
    "Hardoi": {"lat": 27.3854, "lng": 80.1252},
    "Hathras": {"lat": 27.6033, "lng": 78.0538},
    "Jalaun": {"lat": 26.1438, "lng": 79.3364},
    "Jaunpur": {"lat": 25.7464, "lng": 82.6837},
    "Jhansi": {"lat": 25.4484, "lng": 78.5685},
    "Kannauj": {"lat": 27.0543, "lng": 79.9126},
    "Kanpur Dehat": {"lat": 26.3475, "lng": 79.8824},
    "Kanpur": {"lat": 26.4499, "lng": 80.3319},
    "Kasganj": {"lat": 27.8080, "lng": 78.6441},
    "Kaushambi": {"lat": 25.3582, "lng": 81.4253},
    "Kushinagar": {"lat": 26.7397, "lng": 83.8863},
    "Lakhimpur Kheri": {"lat": 27.9490, "lng": 80.7766},
    "Lalitpur": {"lat": 24.6908, "lng": 78.4140},
    "Lucknow": {"lat": 26.8467, "lng": 80.9462},
    "Maharajganj": {"lat": 27.1472, "lng": 83.5654},
    "Mahoba": {"lat": 25.2929, "lng": 79.8735},
    "Mainpuri": {"lat": 27.2280, "lng": 79.0253},
    "Mathura": {"lat": 27.4924, "lng": 77.6737},
    "Mau": {"lat": 25.9398, "lng": 83.5594},
    "Meerut": {"lat": 28.9845, "lng": 77.7064},
    "Mirzapur": {"lat": 25.1460, "lng": 82.5642},
    "Moradabad": {"lat": 28.8386, "lng": 78.7733},
    "Muzaffarnagar": {"lat": 29.4727, "lng": 77.7085},
    "Pilibhit": {"lat": 28.6310, "lng": 79.8038},
    "Pratapgarh": {"lat": 25.9080, "lng": 81.9961},
    "Rae Bareli": {"lat": 26.2303, "lng": 81.2404},
    "Rampur": {"lat": 28.8150, "lng": 79.0253},
    "Saharanpur": {"lat": 29.9640, "lng": 77.5460},
    "Sambhal": {"lat": 28.5831, "lng": 78.5668},
    "Sant Kabir Nagar": {"lat": 26.7329, "lng": 83.0531},
    "Shahjahanpur": {"lat": 27.8805, "lng": 79.9126},
    "Shamli": {"lat": 29.4475, "lng": 77.3082},
    "Shravasti": {"lat": 27.6974, "lng": 81.9056},
    "Siddharthnagar": {"lat": 27.3175, "lng": 82.8876},
    "Sitapur": {"lat": 27.5670, "lng": 80.6800},
    "Sonbhadra": {"lat": 24.6865, "lng": 83.0645},
    "Sultanpur": {"lat": 26.2579, "lng": 82.0734},
    "Unnao": {"lat": 26.5413, "lng": 80.4851},
    "Varanasi": {"lat": 25.3176, "lng": 82.9739}
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
    """Builds an adjacency graph linking nearby districts."""
    graph = {}
    for d1 in districts_data:
        graph[d1] = {}
        # Find 5 nearest neighbors to ensure graph connectivity without cluttering too much
        distances = []
        for d2 in districts_data:
            if d1 != d2:
                dist = calculate_distance(
                    districts_data[d1]['lat'], districts_data[d1]['lng'],
                    districts_data[d2]['lat'], districts_data[d2]['lng']
                )
                distances.append((d2, dist))
        
        # Sort by distance and connect to closest 5 districts (average branching factor)
        distances.sort(key=lambda x: x[1])
        for neighbor, dist in distances[:6]:
            # Add some slight variation to simulate road distance instead of straight line
            road_dist = int(dist * 1.2)
            graph[d1][neighbor] = road_dist
            
    # Ensure graph is bidirectional
    for d1 in graph:
        for d2, dist in graph[d1].items():
            if d1 not in graph[d2]:
                graph[d2][d1] = dist
            elif graph[d2][d1] != dist:
                # Keep consistent
                graph[d2][d1] = dist
                
    return graph

up_graph = build_district_graph()
