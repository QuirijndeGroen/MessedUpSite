FROM python:3.12-slim AS production

ENV PYTHONUNBUFFERED=1
WORKDIR /app/

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

COPY requirements/prod.txt ./requirements/prod.txt
RUN pip install --progress-bar off -r ./requirements/prod.txt

COPY manage.py ./manage.py
COPY setup.cfg ./setup.cfg
COPY MessedUpSite ./MessedUpSite

EXPOSE 9000


FROM production AS development

COPY requirements/dev.txt ./requirements/dev.txt
RUN pip install --progress-bar off -r ./requirements/dev.txt

COPY . .
