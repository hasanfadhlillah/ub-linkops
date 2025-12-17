# Gunakan image Python dasar yang ringan
FROM python:3.9-slim

# Set working directory di dalam container
WORKDIR /app

# 1. Install dependency sistem yang dibutuhkan untuk Chrome & Selenium
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 2. Install Google Chrome Stable (Versi Terbaru)
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 3. Copy file requirements dan install library Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy seluruh kodingan ke dalam container
COPY . .

# 5. Command default (Nanti di-override sama docker-compose)
CMD ["python", "src/scraper_job.py"]