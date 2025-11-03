#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть словарь кодов товаров

def calculate_goods_cost():
    """Рассчитывает общую стоимость каждого товара на складе"""
    goods = {
        'Лампа': '12345',
        'Стол': '23456',
        'Диван': '34567',
        'Стул': '45678',
    }

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

    results = {}
    
    # Лампа
    lamp_code = goods['Лампа']
    lamps_item = store[lamp_code][0]
    lamps_quantity = lamps_item['quantity']
    lamps_cost = lamps_quantity * lamps_item['price']
    results['Лампа'] = {'quantity': lamps_quantity, 'cost': lamps_cost}
    
    # Стол
    table_code = goods['Стол']
    table_items = store[table_code]
    table_quantity = table_items[0]['quantity'] + table_items[1]['quantity']
    table_cost = (table_items[0]['quantity'] * table_items[0]['price'] + 
                 table_items[1]['quantity'] * table_items[1]['price'])
    results['Стол'] = {'quantity': table_quantity, 'cost': table_cost}
    
    # Диван
    sofa_code = goods['Диван']
    sofa_items = store[sofa_code]
    sofa_quantity = sofa_items[0]['quantity'] + sofa_items[1]['quantity']
    sofa_cost = (sofa_items[0]['quantity'] * sofa_items[0]['price'] + 
                sofa_items[1]['quantity'] * sofa_items[1]['price'])
    results['Диван'] = {'quantity': sofa_quantity, 'cost': sofa_cost}
    
    # Стул
    chair_code = goods['Стул']
    chair_items = store[chair_code]
    chair_quantity = (chair_items[0]['quantity'] + chair_items[1]['quantity'] + 
                     chair_items[2]['quantity'])
    chair_cost = (chair_items[0]['quantity'] * chair_items[0]['price'] + 
                 chair_items[1]['quantity'] * chair_items[1]['price'] + 
                 chair_items[2]['quantity'] * chair_items[2]['price'])
    results['Стул'] = {'quantity': chair_quantity, 'cost': chair_cost}
    
    return results