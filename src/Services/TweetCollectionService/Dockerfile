FROM python:3.9-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем директорию для базы данных
RUN mkdir -p /app/DataBase

# Устанавливаем переменные окружения
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Открываем порт
EXPOSE 5000

# Запускаем Flask-приложение
CMD ["flask", "run", "--host=0.0.0.0"]