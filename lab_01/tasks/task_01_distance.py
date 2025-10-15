def calculate_distances(cities_coords):
    distances = {}
    for city1, coords1 in cities_coords.items():
        distances[city1] = {}
        for city2, coords2 in cities_coords.items():
            if city1 != city2:
                x1, y1 = coords1
                x2, y2 = coords2
                distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
                distances[city1][city2] = round(distance, 2)
    return distances