FROM python:3.13-slim

WORKDIR /app

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копирование файла с зависимостями в контейнер
COPY requirements.txt ./

# Установка зависимостей python без сохранения в кэш
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода (копируем весь код проекта в контейнер)
COPY . .

# Создание директорий для статики и медиа
RUN mkdir -p /app/static /app/media

# Открытие порта
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]