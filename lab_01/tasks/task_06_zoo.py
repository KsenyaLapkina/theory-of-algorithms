#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def manage_zoo():
    zoo = ['lion', 'kangaroo', 'elephant', 'monkey']
    # Посадить медведя между львом и кенгуру
    zoo.insert(1, 'bear')
    # Добавить птиц в последние клетки
    birds = ['rooster', 'ostrich', 'lark']
    zoo.extend(birds)
    # Убрать слона
    zoo.remove('elephant')
    # Найти номера клеток (нумерация с 1 для человека)
    lion_cell = zoo.index('lion') + 1
    lark_cell = zoo.index('lark') + 1
    return {
        'final_zoo': zoo,
        'lion_cell': lion_cell,
        'lark_cell': lark_cell
    }