#!/usr/bin/env python3
"""
Главный файл запуска приложения "Генератор данных"
Лабораторная работа №4
"""

import sys
import os
import logging

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Точка входа в приложение"""
    try:
        print(" Запуск приложения 'Генератор данных'...")
        
        # Проверяем наличие PySide6
        try:
            from PySide6.QtWidgets import QApplication
            print(" PySide6 доступен")
        except ImportError as e:
            print(" PySide6 не установлен!")
            print("Установите его командой: pip install PySide6")
            input("Нажмите Enter для выхода...")
            return 1
        
        # Импортируем GUI
        try:
            from gui.main_window import MainWindow
            print("Модули GUI загружены")
        except ImportError as e:
            print(f" Ошибка загрузки модулей GUI: {e}")
            print("Проверьте структуру проекта:")
            print("lab_04/")
            print("├── main.py (этот файл)")
            print("├── core/")
            print("│   ├── __init__.py")
            print("│   ├── generators.py")
            print("│   └── ...")
            print("└── gui/")
            print("    ├── __init__.py")
            print("    └── main_window.py")
            input("Нажмите Enter для выхода...")
            return 1
        
        # Запускаем приложение
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        
        print(" Приложение успешно запущено")
        print("ℹ  База данных: generator_app.db")
        print("ℹ  Нажмите Ctrl+C в консоли для выхода")
        
        return app.exec()
        
    except Exception as e:
        print(f" Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")
        return 1

if __name__ == "__main__":
    sys.exit(main())