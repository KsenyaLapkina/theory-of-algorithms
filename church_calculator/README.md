# Калькулятор с применением кодирования Чёрча

**Технологии**  
- Python 3.13
- PyTest 8.4.2
- Docker 28.5.1
- PySide6 6.10

## Основные классы
- ChurchNumeral - Представление натуральных чисел в кодировке Чёрча
- ChurchCalculator - Реализация арифметических операций над церковными числами
- ExpressionParser -  Анализ математических выражений
- CalculatorWindow - Графический интерфейс приложения

## Особенности

- **Кодирование Чёрча**: Полная реализация λ-исчисления для вычислений
- **Двойной интерфейс**: Графический (PySide6) и веб-версия (Flask)
- **Полное тестирование**: Модульные и интеграционные тесты


## Запуск
```bash
# Клонирование и установка
git clone <repository-url>
cd church-calculator

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt

# Запуск тестов
python -m pytest test_church.py -v

# Запуск GUI приложения
python app/gui.py

# Запуск веб-версии
python run_web.py

## Заключение 
Все тесты успешно проходят.
