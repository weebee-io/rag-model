FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      wget \
      apt-transport-https \
      gnupg \
    && \
    wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - && \
    echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" > /etc/apt/sources.list.d/elastic-8.x.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends filebeat && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "filebeat -e & uvicorn app.main:app --host 0.0.0.0 --port 8000"]




# FROM python:3.11-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
