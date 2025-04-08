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
COPY ./src/Services/SentimentAnalysisService/ .

# Создаем структуру директорий
RUN mkdir -p /app/Data /app/src/Services/DataBase

RUN pip install flask-cors

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]