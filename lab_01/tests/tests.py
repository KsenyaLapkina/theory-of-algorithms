from tasks import task_01_distance, task_02_circle, task_03_operations, task_04_movies, task_05_family, task_06_zoo, task_07_songs, task_08_secret, task_09_garden, task_10_shopping, task_11_store
import pytest

class TestTask1:
    def test_calculate_distances_basic(self):
        cities = {
            'Moscow': (0, 0),
            'SPb': (3, 4),
            'Kazan': (6, 8)
        }
        distances = task_01_distance.calculate_distances(cities)
        assert 'Moscow' in distances
        assert 'SPb' in distances
        assert 'Kazan' in distances
        assert distances['Moscow']['SPb'] == 5.0
        assert distances['Moscow']['Kazan'] == 10.0
        assert distances['SPb']['Kazan'] == 5.0
        assert 'Moscow' not in distances['Moscow']
        assert 'SPb' not in distances['SPb']
        assert 'Kazan' not in distances['Kazan']

    def test_calculate_distances_single_city(self):
        cities = {'Moscow': (0, 0)}
        distances = task_01_distance.calculate_distances(cities)
        assert distances == {'Moscow': {}}


class TestTask2:
    def test_calculate_circle_area_default(self):
        area = task_02_circle.calculate_circle_area()
        expected_area = 3.1415926 * 42**2
        assert area == round(expected_area, 4)

    def test_calculate_circle_area_custom_radius(self):
        area = task_02_circle.calculate_circle_area(radius=10)
        expected_area = 3.1415926 * 100
        assert area == round(expected_area, 4)

    def test_check_point_in_circle_inside(self):
        point = (20, 20) 
        distance = (20**2 + 20**2)**0.5  
        assert task_02_circle.check_point_in_circle(point, 42) is True

    def test_check_point_in_circle_outside(self):
        point = (40, 40)
        assert task_02_circle.check_point_in_circle(point, 42) is False

    def test_check_point_in_circle_on_edge(self):
        point = (42, 0)
        assert task_02_circle.check_point_in_circle(point, 42) is True


class TestTask3:
    def test_calculate_expression(self):
        result = task_03_operations.calculate_expression()
        expected = 1 * (2 + 3) * 4 + 5  # 1 * 5 * 4 + 5 = 20 + 5 = 25
        assert result == expected
        assert result == 25


class TestTask4:
    def test_get_movies_by_index(self):
        movies = task_04_movies.get_movies_by_index()
        
        assert movies['first'] == 'Терминатор'
        assert movies['last'] == 'Назад в будущее'
        assert movies['second'] == 'Пятый элемент'
        assert movies['second_last'] == 'Чужие'
        assert isinstance(movies, dict)
        assert len(movies) == 4


class TestTask5:
    def test_get_family_data_structure(self):
        family_data = task_05_family.get_family_data()
        assert isinstance(family_data, dict)
        assert 'father_height' in family_data
        assert 'total_height' in family_data
        assert 'family_members' in family_data

    def test_get_family_data_values(self):
        family_data = task_05_family.get_family_data()
        assert family_data['father_height'] == 170
        assert family_data['total_height'] == 165 + 170 + 160 + 160 + 175
        assert family_data['family_members'] == ["мама", 'папа', 'сестра', 'бабушка', 'дедушка']


class TestTask6:
    def test_manage_zoo_operations(self):
        zoo_data = task_06_zoo.manage_zoo()
        assert 'final_zoo' in zoo_data
        assert 'lion_cell' in zoo_data
        assert 'lark_cell' in zoo_data
        final_zoo = zoo_data['final_zoo']
        assert 'bear' in final_zoo
        assert 'elephant' not in final_zoo
        assert 'lion' in final_zoo
        assert 'lark' in final_zoo
        assert zoo_data['lion_cell'] == 1
        assert zoo_data['lark_cell'] == final_zoo.index('lark') + 1


class TestTask7:
    def test_calculate_songs_time_structure(self):
        songs_data = task_07_songs.calculate_songs_time()
        assert isinstance(songs_data, dict)
        assert 'list_songs_time' in songs_data
        assert 'dict_songs_time' in songs_data
        assert 'list_songs' in songs_data
        assert 'dict_songs' in songs_data
    def test_calculate_songs_time_values(self):
        songs_data = task_07_songs.calculate_songs_time()
        assert isinstance(songs_data['list_songs_time'], float)
        assert isinstance(songs_data['dict_songs_time'], float)
        assert songs_data['list_songs'] == ['Halo', 'Enjoy the Silence', 'Clean']
        assert songs_data['dict_songs'] == ['Sweetest Perfection', 'Policy of Truth', 'Blue Dress']


class TestTask8:
    def test_decrypt_secret_message(self):
        message = task_08_secret.decrypt_secret_message()
        assert isinstance(message, str)
        words = message.split()
        assert len(words) == 5


class TestTask9:
    def test_analyze_flowers_sets(self):
        flowers_data = task_09_garden.analyze_flowers()
        assert 'all_flowers' in flowers_data
        assert 'common_flowers' in flowers_data
        assert 'garden_only' in flowers_data
        assert 'meadow_only' in flowers_data
        assert isinstance(flowers_data['all_flowers'], set)
        assert isinstance(flowers_data['common_flowers'], set)
        assert isinstance(flowers_data['garden_only'], set)
        assert isinstance(flowers_data['meadow_only'], set)
        garden_set = {'ромашка', 'роза', 'одуванчик', 'гладиолус', 'подсолнух'}
        meadow_set = {'клевер', 'одуванчик', 'ромашка', 'мак'}
        assert flowers_data['all_flowers'] == garden_set | meadow_set
        assert flowers_data['common_flowers'] == garden_set & meadow_set
        assert flowers_data['garden_only'] == garden_set - meadow_set
        assert flowers_data['meadow_only'] == meadow_set - garden_set


class TestTask10:
    def test_create_sweets_price_dict_structure(self):
        sweets_data = task_10_shopping.create_sweets_price_dict()
        expected_products = ['печенье', 'конфеты', 'карамель', 'пирожное']
        for product in expected_products:
            assert product in sweets_data
        for product, prices in sweets_data.items():
            assert isinstance(prices, list)
            assert len(prices) == 2  # Две самые низкие цены
            for price_info in prices:
                assert 'shop' in price_info
                assert 'price' in price_info

    def test_create_sweets_price_dict_sorted(self):
        sweets_data = task_10_shopping.create_sweets_price_dict()
        for product, prices in sweets_data.items():
            # Проверяем, что цены отсортированы по возрастанию
            assert prices[0]['price'] <= prices[1]['price']


class TestTask11:
    def test_calculate_goods_cost_structure(self):
        goods_data = task_11_store.calculate_goods_cost()
        expected_products = ['Лампа', 'Стол', 'Диван', 'Стул']
        for product in expected_products:
            assert product in goods_data
        for product, data in goods_data.items():
            assert 'quantity' in data
            assert 'cost' in data
            assert isinstance(data['quantity'], int)
            assert isinstance(data['cost'], int)

    def test_calculate_goods_cost_calculations(self):
        goods_data = task_11_store.calculate_goods_cost()
        assert goods_data['Лампа']['quantity'] == 27
        assert goods_data['Лампа']['cost'] == 27 * 42
        table_quantity = 22 + 32
        table_cost = 22 * 510 + 32 * 520
        assert goods_data['Стол']['quantity'] == table_quantity
        assert goods_data['Стол']['cost'] == table_cost
        sofa_quantity = 2 + 1
        sofa_cost = 2 * 1200 + 1 * 1150
        assert goods_data['Диван']['quantity'] == sofa_quantity
        assert goods_data['Диван']['cost'] == sofa_cost
        chair_quantity = 50 + 12 + 43
        chair_cost = 50 * 100 + 12 * 95 + 43 * 97
        assert goods_data['Стул']['quantity'] == chair_quantity
        assert goods_data['Стул']['cost'] == chair_cost