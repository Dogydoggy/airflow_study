FROM apache/airflow:2.10.4-python3.8

USER root

# 시스템 패키지 설치 (예: gcc, libpq-dev 등)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
        build-essential \
        && apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt