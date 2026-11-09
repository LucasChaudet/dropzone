# API DropZone : image multi-stage.
# 1) "builder" installe les dépendances dans un environnement virtuel ;
# 2) l'image finale ne reçoit que cet environnement et le code de l'application.

FROM python:3.12-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Les dépendances d'abord : cette couche reste en cache tant que requirements.txt ne change pas.
COPY requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Utilisateur sans privilèges pour lancer l'API.
RUN useradd --create-home --uid 10001 app

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY app ./app
RUN chown app:app /app

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
