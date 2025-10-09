#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# есть список животных в зоопарке
zoo = ['lion', 'kangaroo', 'elephant', 'monkey', ]

# посадите медведя (bear) между львом и кенгуру
zoo.insert(1, 'bear')
print("После добавления медведя:", zoo)

# добавьте птиц из списка birds в последние клетки зоопарка
birds = ['rooster', 'ostrich', 'lark', ]
zoo.extend(birds)
print("После добавления птиц:", zoo)

# уберите слона
zoo.remove('elephant')
print("После удаления слона:", zoo)

# выведите на консоль в какой клетке сидит лев (lion) и жаворонок (lark)
# Нумерация клеток для человека (начиная с 1)
lion_cell = zoo.index('lion') + 1
lark_cell = zoo.index('lark') + 1

print("Лев сидит в клетке №", lion_cell)
print("Жаворонок сидит в клетке №", lark_cell)
