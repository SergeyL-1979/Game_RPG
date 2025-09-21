# =========================
# Dockerfile (корень проекта)
# =========================
FROM python:3.9-slim

# Базовые настройки Python/pip
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Рабочая директория
WORKDIR /srv

# Устанавливаем зависимости
COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем исходники и игровые данные
COPY app/ ./app/
COPY data/ ./data/

# Нерутовый пользователь (без shell)
RUN useradd -m -r -s /usr/sbin/nologin appuser && \
    chown -R appuser:appuser /srv
USER appuser

# Порт приложения
ENV PORT=5000
EXPOSE 5000

# Запуск через Gunicorn (2 воркера)
# ВАЖНО: грузим как пакет app.wsgi:app — тогда относительные импорты внутри app/ работают корректно.
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "app.wsgi:app"]
