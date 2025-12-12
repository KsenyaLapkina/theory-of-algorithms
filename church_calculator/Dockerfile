FROM python:3.11-slim

WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт для веб-сервера
EXPOSE 5000

# Команда для запуска
CMD ["python", "run_web.py"]