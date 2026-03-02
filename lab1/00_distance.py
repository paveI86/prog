#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть словарь координат городов

sites = {
    'Moscow': (550, 370),
    'London': (510, 510),
    'Paris': (480, 480),
}

# Составим словарь словарей расстояний между ними
# расстояние на координатной сетке - ((x1 - x2)  2 + (y1 - y2)  2) ** 0.5

distances = {}

# Перебираем все пары городов
for city1 in sites:
    distances[city1] = {}  # Создаем вложенный словарь для city1
    for city2 in sites:
        if city1 != city2:  # Не считаем расстояние от города до самого себя
            # Получаем координаты
            x1, y1 = sites[city1]
            x2, y2 = sites[city2]
            
            # Вычисляем расстояние
            distance = ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5
            
            # Записываем расстояние в словарь
            distances[city1][city2] = distance

print(distances)