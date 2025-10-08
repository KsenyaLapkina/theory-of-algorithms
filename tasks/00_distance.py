#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть словарь координат городов
sites = {
    'Moscow': (550, 370),
    'London': (510, 510),
    'Paris': (480, 480),
}

# Составим словарь словарей расстояний между ними
distances = {}

for city1, coords1 in sites.items():
    distances[city1] = {}
    for city2, coords2 in sites.items():
        if city1 != city2:
            x1, y1 = coords1
            x2, y2 = coords2
            distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            distances[city1][city2] = round(distance, 2)

print(distances)




