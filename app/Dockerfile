# Выкачиваем из dockerhub образ с python версии 3.9
FROM python:3.10.6-slim

# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /app

# Устанавливаем зависимости
COPY ../requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 5000

# Приложение запускаем через gunicorn (совместимо с compose+nginx)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
