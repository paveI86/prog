#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть словарь кодов товаров

goods = {
    'Лампа': '12345',
    'Стол': '23456',
    'Диван': '34567',
    'Стул': '45678',
}

# Есть словарь списков количества товаров на складе.

store = {
    '12345': [
        {'quantity': 27, 'price': 42},
    ],
    '23456': [
        {'quantity': 22, 'price': 510},
        {'quantity': 32, 'price': 520},
    ],
    '34567': [
        {'quantity': 2, 'price': 1200},
        {'quantity': 1, 'price': 1150},
    ],
    '45678': [
        {'quantity': 50, 'price': 100},
        {'quantity': 12, 'price': 95},
        {'quantity': 43, 'price': 97},
    ],
}

# Рассчитать на какую сумму лежит каждого товара на складе

# Лампа
lamp_code = goods['Лампа']
lamp_item = store[lamp_code][0]
lamp_quantity = lamp_item['quantity']
lamp_price = lamp_item['price']
lamp_cost = lamp_quantity * lamp_price
print('Лампа -', lamp_quantity, 'шт, стоимость', lamp_cost, 'руб')

# Стол (две партии)
table_code = goods['Стол']
table_item_1 = store[table_code][0]
table_item_2 = store[table_code][1]

table_quantity = table_item_1['quantity'] + table_item_2['quantity']
table_cost = (table_item_1['quantity'] * table_item_1['price']) + (table_item_2['quantity'] * table_item_2['price'])
print('Стол -', table_quantity, 'шт, стоимость', table_cost, 'руб')

# Диван (две партии)
sofa_code = goods['Диван']
sofa_item_1 = store[sofa_code][0]
sofa_item_2 = store[sofa_code][1]

sofa_quantity = sofa_item_1['quantity'] + sofa_item_2['quantity']
sofa_cost = (sofa_item_1['quantity'] * sofa_item_1['price']) + (sofa_item_2['quantity'] * sofa_item_2['price'])
print('Диван -', sofa_quantity, 'шт, стоимость', sofa_cost, 'руб')

# Стул (три партии)
chair_code = goods['Стул']
chair_item_1 = store[chair_code][0]
chair_item_2 = store[chair_code][1]
chair_item_3 = store[chair_code][2]

chair_quantity = chair_item_1['quantity'] + chair_item_2['quantity'] + chair_item_3['quantity']
chair_cost = (chair_item_1['quantity'] * chair_item_1['price']) + (chair_item_2['quantity'] * chair_item_2['price']) + (chair_item_3['quantity'] * chair_item_3['price'])
print('Стул -', chair_quantity, 'шт, стоимость', chair_cost, 'руб')