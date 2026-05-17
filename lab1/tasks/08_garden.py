#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# в саду сорвали цветы
garden = ('ромашка', 'роза', 'одуванчик', 'ромашка', 'гладиолус', 'подсолнух', 'роза', )

# на лугу сорвали цветы
meadow = ('клевер', 'одуванчик', 'ромашка', 'клевер', 'мак', 'одуванчик', 'ромашка', )

# создайте множество цветов, произрастающих в саду и на лугу
garden_set = set(garden)
meadow_set = set(meadow)

# выведите на консоль все виды цветов
all_flowers = garden_set.union(meadow_set)  # или garden_set | meadow_set
print("Все виды цветов:", all_flowers)

# выведите на консоль те, которые растут и там и там
both_flowers = garden_set.intersection(meadow_set)  # или garden_set & meadow_set
print("Цветы, которые растут и в саду, и на лугу:", both_flowers)

# выведите на консоль те, которые растут в саду, но не растут на лугу
only_garden = garden_set.difference(meadow_set)  # или garden_set - meadow_set
print("Цветы, которые растут только в саду:", only_garden)

# выведите на консоль те, которые растут на лугу, но не растут в саду
only_meadow = meadow_set.difference(garden_set)  # или meadow_set - garden_set
print("Цветы, которые растут только на лугу:", only_meadow)

def run():
    """Функция для запуска из верхнеуровневого модуля"""
    # Здесь вызовите основную функцию вашего задания
    # Например:
    main()  # если у вас есть функция main()
    # или просто скопируйте сюда код задания

if __name__ == "__main__":
    run()