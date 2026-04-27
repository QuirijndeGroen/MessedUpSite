FROM python:3.14-slim AS production

ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y \
    bash \
    build-essential \
    gcc \
    libffi-dev \
    musl-dev \
    openssl \
    postgresql \
    libpq-dev

COPY manage.py ./manage.py
COPY MessedUpSite ./MessedUpSite

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY uv.lock ./uv.lock
COPY pyproject.toml ./pyproject.toml

WORKDIR /app/

RUN uv sync --no-dev

EXPOSE 9000


FROM production AS development

RUN uv sync --dev

COPY . .
