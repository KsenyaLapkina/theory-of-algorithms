from tasks import task_01_distance, task_02_circle, task_03_operations, task_04_movies, task_05_family, task_06_zoo, task_07_songs, task_08_secret, task_09_garden, task_10_shopping, task_11_store

def run_task_1():
    print("\n--- Задача 1: Расчет расстояний между городами ---")
    cities = {
        'Moscow': (0, 0),
        'SPb': (3, 4),
        'Kazan': (6, 8),
        'Sochi': (8, 6)
    }
    distances = task_01_distance.calculate_distances(cities)
    print("Координаты городов:", cities)
    print("Расстояния между городами:")
    for city1 in distances:
        for city2 in distances[city1]:
            print(f"  {city1} -> {city2}: {distances[city1][city2]}")

def run_task_2():
    print("\n--- Задача 2: Работа с кругом ---")
    radius = float(input("Введите радиус круга (по умолчанию 42): ") or 42)
    area = task_02_circle.calculate_circle_area(radius)
    print(f"Площадь круга с радиусом {radius}: {area}")
    
    x = float(input("Введите координату X точки: "))
    y = float(input("Введите координату Y точки: "))
    point = (x, y)
    is_inside = task_02_circle.check_point_in_circle(point, radius)
    print(f"Точка {point} находится внутри круга: {is_inside}")

def run_task_3():
    print("\n--- Задача 3: Вычисление выражения ---")
    result = task_03_operations.calculate_expression()
    print(f"Результат выражения 1 * (2 + 3) * 4 + 5 = {result}")

def run_task_4():
    print("\n--- Задача 4: Работа со строками (фильмы) ---")
    movies = task_04_movies.get_movies_by_index()
    print("Результаты:")
    for key, value in movies.items():
        print(f"  {key}: {value}")

def run_task_5():
    print("\n--- Задача 5: Данные о семье ---")
    family_data = task_05_family.get_family_data()
    print("Результаты:")
    print(f"  Члены семьи: {family_data['family_members']}")
    print(f"  Рост отца: {family_data['father_height']} см")
    print(f"  Общий рост семьи: {family_data['total_height']} см")

def run_task_6():
    print("\n--- Задача 6: Управление зоопарком ---")
    zoo_data = task_06_zoo.manage_zoo()
    print("Результаты:")
    print(f"  Финальный зоопарк: {zoo_data['final_zoo']}")
    print(f"  Клетка льва: {zoo_data['lion_cell']}")
    print(f"  Клетка жаворонка: {zoo_data['lark_cell']}")

def run_task_7():
    print("\n--- Задача 7: Расчет времени песен ---")
    songs_data = task_07_songs.calculate_songs_time()
    print("Результаты:")
    print(f"  Песни из списка: {songs_data['list_songs']}")
    print(f"  Общее время: {songs_data['list_songs_time']} минут")
    print(f"  Песни из словаря: {songs_data['dict_songs']}")
    print(f"  Общее время: {songs_data['dict_songs_time']} минут")

def run_task_8():
    print("\n--- Задача 8: Расшифровка секретного сообщения ---")
    message = task_08_secret.decrypt_secret_message()
    print(f"Расшифрованное сообщение: {message}")

def run_task_9():
    print("\n--- Задача 9: Анализ цветов ---")
    flowers_data = task_09_garden.analyze_flowers()
    print("Результаты:")
    print(f"  Все цветы: {flowers_data['all_flowers']}")
    print(f"  Общие цветы: {flowers_data['common_flowers']}")
    print(f"  Только в саду: {flowers_data['garden_only']}")
    print(f"  Только на лугу: {flowers_data['meadow_only']}")

def run_task_10():
    print("\n--- Задача 10: Словарь цен сладостей ---")
    sweets_data = task_10_shopping.create_sweets_price_dict()
    print("Две самые низкие цены для каждого продукта:")
    for product, prices in sweets_data.items():
        print(f"  {product}:")
        for price_info in prices:
            print(f"    {price_info['shop']}: {price_info['price']} руб")

def run_task_11():
    print("\n--- Задача 11: Расчет стоимости товаров ---")
    goods_data = task_11_store.calculate_goods_cost()
    print("Стоимость товаров на складе:")
    for product, data in goods_data.items():
        print(f"  {product}: количество={data['quantity']}, стоимость={data['cost']} руб")

def main():
    while True:
        print("\n" + "=" * 60)
        print("ВЫБЕРИТЕ ЗАДАЧУ ДЛЯ ВЫПОЛНЕНИЯ")
        print("=" * 60)
        print("1. Расчет расстояний между городами")
        print("2. Работа с кругом (площадь и проверка точки)")
        print("3. Вычисление арифметического выражения")
        print("4. Работа со строками (фильмы)")
        print("5. Данные о семье")
        print("6. Управление зоопарком")
        print("7. Расчет времени песен")
        print("8. Расшифровка секретного сообщения")
        print("9. Анализ цветов в саду и на лугу")
        print("10. Создание словаря цен сладостей")
        print("11. Расчет стоимости товаров на складе")
        print("0. ВЫХОД")
        print("-" * 60)
        
        choice = input("Введите номер задачи (0-11): ").strip()
        
        tasks = {
            '1': run_task_1,
            '2': run_task_2,
            '3': run_task_3,
            '4': run_task_4,
            '5': run_task_5,
            '6': run_task_6,
            '7': run_task_7,
            '8': run_task_8,
            '9': run_task_9,
            '10': run_task_10,
            '11': run_task_11
        }
        
        if choice == '0':
            print("Выход из программы.")
            break
        elif choice in tasks:
            try:
                tasks[choice]()
            except Exception as e:
                print(f"Произошла ошибка при выполнении задачи: {e}")
        else:
            print("Неверный выбор. Пожалуйста, введите число от 0 до 11.")
        
        if choice != '0':
            input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    main()