#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# создайте множество цветов, произрастающих в саду и на лугу
garden_set = {'ромашка', 'роза', 'одуванчик', 'гладиолус', 'подсолнух'}
meadow_set = {'клевер', 'одуванчик', 'ромашка', 'мак'}

# выведите на консоль все виды цветов
all_flowers = garden_set | meadow_set 
print("Все виды цветов:", all_flowers)

# выведите на консоль те, которые растут и там и там
common_flowers = garden_set & meadow_set 
print("Цветы, которые растут и там и там:", common_flowers)

# выведите на консоль те, которые растут в саду, но не растут на лугу
garden_only = garden_set - meadow_set 
print("Цветы, которые растут только в саду:", garden_only)

# выведите на консоль те, которые растут на лугу, но не растут в саду
meadow_only = meadow_set - garden_set 
print("Цветы, которые растут только на лугу:", meadow_only)
