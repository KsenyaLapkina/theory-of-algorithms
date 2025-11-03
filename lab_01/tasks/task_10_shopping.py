#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def create_sweets_price_dict():
    """Создает словарь цен на сладости с минимальными ценами по магазинам"""
    shops = {
        'ашан': [
            {'name': 'печенье', 'price': 10.99},
            {'name': 'конфеты', 'price': 34.99},
            {'name': 'карамель', 'price': 45.99},
            {'name': 'пирожное', 'price': 67.99}
        ],
        'пятерочка': [
            {'name': 'печенье', 'price': 9.99},
            {'name': 'конфеты', 'price': 32.99},
            {'name': 'карамель', 'price': 46.99},
            {'name': 'пирожное', 'price': 59.99}
        ],
        'магнит': [
            {'name': 'печенье', 'price': 11.99},
            {'name': 'конфеты', 'price': 30.99},
            {'name': 'карамель', 'price': 41.99},
            {'name': 'пирожное', 'price': 62.99}
        ],
    }

    # Создаем словарь для хранения всех цен по продуктам
    product_prices = {}
    
    for shop_name, products in shops.items():
        for product in products:
            name = product['name']
            price = product['price']
            
            if name not in product_prices:
                product_prices[name] = []
            
            product_prices[name].append({'shop': shop_name, 'price': price})
    
    # Сортируем цены по возрастанию и берем 2 минимальные
    sweets = {}
    for product_name, prices in product_prices.items():
        sorted_prices = sorted(prices, key=lambda x: x['price'])
        sweets[product_name] = sorted_prices[:2]
    
    return sweets