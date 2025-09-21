# Базовый образ
FROM python:3.9-slim

# Базовые настройки Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Рабочая директория контейнера
WORKDIR /srv

# Устанавливаем зависимости
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходники и игровые данные
COPY app/ ./app/
COPY data/ ./data/

# Открываем порт приложения
EXPOSE 5000

# Запуск через Gunicorn (2 воркера; при желании увеличьте)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--chdir", "app", "wsgi:app", "-w", "2"]
