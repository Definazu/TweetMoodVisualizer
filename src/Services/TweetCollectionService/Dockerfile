FROM python:3.9-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    libgeos-c1v5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем requirements.txt из корня проекта
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы сервиса
COPY src/Services/TweetCollectionService/ .

# Создаем структуру директорий
RUN mkdir -p /app/Data /app/src/Services/DataBase

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_PORT=5001

EXPOSE 5001

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]