# используем официальный образ Nginx
FROM nginx:latest

# Создаем директорию для статики Django
RUN mkdir -p /app/staticfiles

# Копируем файл конфигурации Nginx в контейнер
COPY nginx.conf /etc/nginx/nginx.conf

# открываем порт для hhtp трафика
EXPOSE 80