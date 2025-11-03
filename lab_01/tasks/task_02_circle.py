#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Есть значение радиуса круга
def calculate_circle_area(radius=42, pi=3.1415926):
    """Вычисляет площадь круга с заданным радиусом"""
    square = pi * radius**2
    return round(square, 4)

def check_point_in_circle(point, radius=42):
    """Проверяет, лежит ли точка внутри круга с центром в (0, 0)"""
    distance = (point[0]**2 + point[1]**2)**0.5
    return distance <= radius

# Пример вывода на консоль:
#
# 77777.7777
# False
# False


