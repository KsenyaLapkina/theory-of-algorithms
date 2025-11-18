#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_family_data():
    my_family = ["мама", 'папа', 'сестра', 'бабушка', 'дедушка']
    
    my_family_height = [
        ['мама', 165],
        ['папа', 170],
        ['сестра', 160],
        ['бабушка', 160],
        ['дедушка', 175],
    ]
    father_height = None
    for member in my_family_height:
        if member[0] == 'папа':
            father_height = member[1]
            break
    total_height = 0
    for member in my_family_height:
        total_height += member[1]
    return {
        'father_height': father_height,
        'total_height': total_height,
        'family_members': my_family
    }
