import sys
import os

# Добавляем родительскую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.generators import GeneratorTasks

def test_combinations_generator():
    """Тест генератора комбинаций"""
    print("Тест 1: Генератор комбинаций")
    generator = GeneratorTasks()
    gen = generator.task1_generator()
    
    # Проверяем первые 5 значений
    first_values = [next(gen) for _ in range(5)]
    expected = [0, 1, 2, 3, 4]
    
    assert first_values == expected, f"Ожидалось {expected}, получено {first_values}"
    print("   Первые 5 значений корректны")
    
    # Проверяем еще немного значений
    for _ in range(5):
        next(gen)  # Пропускаем
    
    value = next(gen)
    assert value == 10, f"Ожидалось 10, получено {value}"
    print("   Значение 10 корректно")
    
    print("   Тест пройден успешно\n")

def test_dictionary_sort():
    """Тест сортировки словаря"""
    print("🧪 Тест 2: Сортировка словаря")
    generator = GeneratorTasks()
    
    test_dict = {
        'cat': 'кот',
        'horse': 'лошадь', 
        'tree': 'дерево',
        'dog': 'собака',
        'book': 'книга'
    }
    
    result = generator.get_sort(test_dict)
    expected = ['дерево', 'лошадь', 'собака', 'кот', 'книга']
    
    assert result == expected, f"Ожидалось {expected}, получено {result}"
    print("   Сортировка работает корректно")
    print("   Тест пройден успешно\n")

def test_function_generator():
    """Тест генератора функции"""
    print("Тест 3: Генератор функции")
    generator = GeneratorTasks()
    
    # Простая тестовая функция
    func = lambda x: x * 2
    gen = generator.task2_generator(0, 0.02, func)
    
    values = [next(gen) for _ in range(3)]
    expected = [0.0, 0.02, 0.04]
    
    for i, (val, exp) in enumerate(zip(values, expected)):
        assert abs(val - exp) < 0.0001, f"Ожидалось {exp}, получено {val}"
    
    print("   Значения функции корректны")
    print("   Тест пройден успешно\n")

def main():
    """Запуск всех тестов"""
    print("Запуск тестов генераторов\n")
    
    try:
        test_combinations_generator()
        test_dictionary_sort()
        test_function_generator()
        
        print("🎉 Все тесты успешно пройдены!")
        return 0
        
    except AssertionError as e:
        print(f"Тест не пройден: {e}")
        return 1
    except Exception as e:
        print(f"Ошибка во время тестирования: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())