#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def analyze_flowers():
    garden_set = {'ромашка', 'роза', 'одуванчик', 'гладиолус', 'подсолнух'}
    meadow_set = {'клевер', 'одуванчик', 'ромашка', 'мак'}

    all_flowers = garden_set | meadow_set 
    common_flowers = garden_set & meadow_set 
    garden_only = garden_set - meadow_set 
    meadow_only = meadow_set - garden_set 

    return {
        'all_flowers': all_flowers,
        'common_flowers': common_flowers,
        'garden_only': garden_only,
        'meadow_only': meadow_only
    }
