#!/usr/bin/env python3
"""
Запуск веб-приложения на порту 5629
"""

import os
import sys

def main():
    """Запуск приложения"""
    print("Запуск приложения...")
    print("Сервер будет доступен по адресу: http://localhost:5629")
    print("Нажмите Ctrl+C для остановки")
    
    # Проверяем наличие папки templates
    if not os.path.exists("templates"):
        print("Создаю папку templates...")
        os.makedirs("templates")
    
    # Проверяем зависимости
    try:
        import fastapi
        import uvicorn
    except ImportError:
        print("Устанавливаю зависимости...")
        os.system(f"{sys.executable} -m pip install fastapi uvicorn")
        print("Зависимости установлены")
    
    try:
        import uvicorn
        uvicorn.run(
            "web_app:app",
            host="0.0.0.0",
            port=5629,
            reload=True
        )
    except KeyboardInterrupt:
        print("Остановка сервера...")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()



    