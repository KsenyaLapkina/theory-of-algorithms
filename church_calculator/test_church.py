"""
Тесты для калькулятора Чёрча.
"""

import pytest
import sys
import os

# Добавляем путь для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from church import ChurchCalculator, ChurchNumeral, church_to_int, int_to_church
from database import CalculationHistory
import tempfile
import time

class TestChurchNumerals:
    """Тесты для церковных чисел."""
    
    def test_zero(self):
        """Тест церковного нуля."""
        zero = ChurchCalculator.zero()
        assert church_to_int(zero) == 0
    
    def test_from_int(self):
        """Тест преобразования целых чисел в церковные."""
        for i in range(0, 6):
            church_num = int_to_church(i)
            assert church_to_int(church_num) == i
    
    def test_successor(self):
        """Тест функции следования."""
        zero = ChurchCalculator.zero()
        one = ChurchCalculator.succ(zero)
        two = ChurchCalculator.succ(one)
        
        assert church_to_int(one) == 1
        assert church_to_int(two) == 2
    
    def test_addition(self):
        """Тест сложения церковных чисел."""
        # 2 + 3 = 5
        two = int_to_church(2)
        three = int_to_church(3)
        result = ChurchCalculator.add(two, three)
        assert church_to_int(result) == 5
        
        # 0 + 4 = 4
        zero = ChurchCalculator.zero()
        four = int_to_church(4)
        result = ChurchCalculator.add(zero, four)
        assert church_to_int(result) == 4
    
    def test_subtraction(self):
        """Тест вычитания церковных чисел."""
        # 5 - 2 = 3
        five = int_to_church(5)
        two = int_to_church(2)
        result = ChurchCalculator.subtract(five, two)
        assert church_to_int(result) == 3
        
        # 2 - 5 = 0 (отрицательные не поддерживаются)
        result = ChurchCalculator.subtract(two, five)
        assert church_to_int(result) == 0
    
    def test_multiplication(self):
        """Тест умножения церковных чисел."""
        # 3 * 2 = 6
        three = int_to_church(3)
        two = int_to_church(2)
        result = ChurchCalculator.multiply(three, two)
        assert church_to_int(result) == 6
        
        # 5 * 0 = 0
        five = int_to_church(5)
        zero = ChurchCalculator.zero()
        result = ChurchCalculator.multiply(five, zero)
        assert church_to_int(result) == 0
    
    def test_power(self):
        """Тест возведения в степень."""
        # 2^3 = 8
        two = int_to_church(2)
        three = int_to_church(3)
        result = ChurchCalculator.power(two, three)
        assert church_to_int(result) == 8
        
        # 3^2 = 9
        result = ChurchCalculator.power(three, two)
        assert church_to_int(result) == 9
    
    def test_factorial(self):
        """Тест вычисления факториала."""
        # 0! = 1
        zero = ChurchCalculator.zero()
        result = ChurchCalculator.factorial(zero)
        assert church_to_int(result) == 1
        
        # 5! = 120
        five = int_to_church(5)
        result = ChurchCalculator.factorial(five)
        assert church_to_int(result) == 120
    
    def test_negative_input(self):
        """Тест обработки отрицательных чисел."""
        with pytest.raises(ValueError):
            int_to_church(-1)

class TestChurchNumeralMethods:
    """Тесты методов класса ChurchNumeral."""
    
    def test_str_representation(self):
        """Тест строкового представления."""
        church_num = int_to_church(5)
        assert str(church_num) == "5"
    
    def test_callable_behavior(self):
        """Тест вызываемого поведения церковных чисел."""
        church_two = int_to_church(2)
        
        # Тест применения функции два раза
        def increment(x):
            return x + 1
        
        result_function = church_two(increment)
        result = result_function(0)
        assert result == 2

class TestExpressionParser:
    """Тесты для парсера выражений."""
    
    def test_parse_addition(self):
        from church_calculator.church_web import ExpressionParser
        operation, a, b = ExpressionParser.parse_expression("5+3")
        assert operation == "add"
        assert a == 5
        assert b == 3
    
    def test_parse_factorial(self):
        from church_calculator.church_web import ExpressionParser
        operation, a, b = ExpressionParser.parse_expression("5!")
        assert operation == "factorial"
        assert a == 5
        assert b is None
    
    def test_parse_invalid_expression(self):
        from church_calculator.church_web import ExpressionParser
        with pytest.raises(ValueError):
            ExpressionParser.parse_expression("invalid")


class TestDatabase:
    """Тесты для базы данных."""
    
    def test_database_operations(self):
        """Тест операций с базой данных."""
        # Создаем временную базу данных в текущей директории
        db_path = "test_calculator.db"
        
        try:
            # Удаляем файл если существует
            if os.path.exists(db_path):
                os.unlink(db_path)
            
            db = CalculationHistory(db_path)
            
            # Тест сохранения
            assert db.save_calculation("5+3", "8", "add") == True
            
            # Тест получения истории
            history = db.get_calculation_history()
            assert len(history) == 1
            assert history[0]['expression'] == "5+3"
            assert history[0]['result'] == "8"
            assert history[0]['operation_type'] == "add"
            
        finally:
            # Удаляем временный файл с задержкой для Windows
            if os.path.exists(db_path):
                try:
                    # Закрываем соединение с базой
                    if hasattr(db, '_conn'):
                        db._conn.close()
                    # Даем время системе освободить файл
                    time.sleep(0.1)
                    os.unlink(db_path)
                except (PermissionError, OSError):
                    # Если файл все еще занят, пропускаем удаление
                    print(f"⚠️ Не удалось удалить файл {db_path}, он будет удален при следующем запуске")
    
    def test_database_error_handling(self):
        """Тест обработки ошибок базы данных."""
        # Пытаемся создать базу данных в несуществующей папке
        db = CalculationHistory("/invalid/path/database.db")
        # Должно работать без ошибок благодаря обработке исключений
        assert db.save_calculation("2+2", "4", "add") == False
    
    def test_database_multiple_operations(self):
        """Тест нескольких операций с базой данных."""
        db_path = "test_multiple.db"
        
        try:
            if os.path.exists(db_path):
                os.unlink(db_path)
            
            db = CalculationHistory(db_path)
            
            # Сохраняем несколько операций
            operations = [
                ("5+3", "8", "add"),
                ("4*2", "8", "multiply"), 
                ("5!", "120", "factorial")
            ]
            
            for expr, result, op_type in operations:
                assert db.save_calculation(expr, result, op_type) == True
            
            # Проверяем историю
            history = db.get_calculation_history(limit=5)
            assert len(history) == 3
            
            # Проверяем что все операции сохранены (порядок может быть любым)
            expressions = [item['expression'] for item in history]
            expected_expressions = ["5+3", "4*2", "5!"]
            
            for expected in expected_expressions:
                assert expected in expressions
            
            # Проверяем результаты
            results = [item['result'] for item in history]
            expected_results = ["8", "8", "120"]
            
            for expected in expected_results:
                assert expected in results
            
            # Проверяем типы операций
            operation_types = [item['operation_type'] for item in history]
            expected_operations = ["add", "multiply", "factorial"]
            
            for expected in expected_operations:
                assert expected in operation_types
            
        finally:
            if os.path.exists(db_path):
                try:
                    if hasattr(db, '_conn'):
                        db._conn.close()
                    time.sleep(0.1)
                    os.unlink(db_path)
                except (PermissionError, OSError):
                    pass
    
    def test_database_limit(self):
        """Тест ограничения количества записей в истории."""
        db_path = "test_limit.db"
        
        try:
            if os.path.exists(db_path):
                os.unlink(db_path)
            
            db = CalculationHistory(db_path)
            
            # Сохраняем больше записей чем лимит
            for i in range(15):
                assert db.save_calculation(f"{i}+1", str(i+1), "add") == True
            
            # Проверяем что возвращается только лимит записей
            history = db.get_calculation_history(limit=5)
            assert len(history) == 5
            
            history = db.get_calculation_history(limit=10)
            assert len(history) == 10
            
        finally:
            if os.path.exists(db_path):
                try:
                    if hasattr(db, '_conn'):
                        db._conn.close()
                    time.sleep(0.1)
                    os.unlink(db_path)
                except (PermissionError, OSError):
                    pass

def test_integration():
    """Интеграционный тест всего приложения."""
    from church_calculator.church_web import ExpressionParser
    
    # Тест полного цикла вычислений
    expression = "5+3"
    parsed = ExpressionParser.parse_expression(expression)
    operation, a, b = parsed
    
    assert operation == "add"
    
    # Преобразование в церковные числа
    church_a = int_to_church(int(a))
    church_b = int_to_church(int(b))
    
    # Выполнение операции
    result_church = ChurchCalculator.add(church_a, church_b)
    result = church_to_int(result_church)
    
    assert result == 8

if __name__ == "__main__":
    pytest.main([__file__, "-v"])