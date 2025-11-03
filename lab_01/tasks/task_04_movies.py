#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Выведите на консоль с помощью индексации строки, последовательно:
#   первый фильм
#   последний
#   второй
#   второй с конца

# Запятая не должна выводиться.  Переопределять my_favorite_movies нельзя
# Использовать .split() или .find()или другие методы строки нельзя - пользуйтесь только срезами,
# как указано в задании!

def get_movies_by_index():
    """Получает фильмы из строки с помощью индексации"""
    my_favorite_movies = 'Терминатор, Пятый элемент, Аватар, Чужие, Назад в будущее'
    
    first_movie = my_favorite_movies[:10]
    last_movie = my_favorite_movies[-15:]
    second_movie = my_favorite_movies[12:25]
    second_last_movie = my_favorite_movies[-22:-17]
    
    return {
        'first': first_movie,
        'last': last_movie,
        'second': second_movie,
        'second_last': second_last_movie
    }