#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def calculate_songs_time():
    violator_songs_list = [
        ['World in My Eyes', 4.86],
        ['Sweetest Perfection', 4.43],
        ['Personal Jesus', 4.56],
        ['Halo', 4.9],
        ['Waiting for the Night', 6.07],
        ['Enjoy the Silence', 4.20],
        ['Policy of Truth', 4.76],
        ['Blue Dress', 4.29],
        ['Clean', 5.83],
    ]
    violator_songs_dict = {
        'World in My Eyes': 4.76,
        'Sweetest Perfection': 4.43,
        'Personal Jesus': 4.56,
        'Halo': 4.30,
        'Waiting for the Night': 6.07,
        'Enjoy the Silence': 4.6,
        'Policy of Truth': 4.88,
        'Blue Dress': 4.18,
        'Clean': 5.68,
    }
    total_time_list = 0
    for song in violator_songs_list:
        if song[0] in ['Halo', 'Enjoy the Silence', 'Clean']:
            total_time_list += song[1]

    total_time_list_rounded = round(total_time_list, 2)
    total_time_dict = (violator_songs_dict['Sweetest Perfection'] + 
                      violator_songs_dict['Policy of Truth'] + 
                      violator_songs_dict['Blue Dress'])
    
    total_time_dict_rounded = round(total_time_dict, 2)
    return {
        'list_songs_time': total_time_list_rounded,
        'dict_songs_time': total_time_dict_rounded,
        'list_songs': ['Halo', 'Enjoy the Silence', 'Clean'],
        'dict_songs': ['Sweetest Perfection', 'Policy of Truth', 'Blue Dress']
    }