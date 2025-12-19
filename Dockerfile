FROM python:3.9-slim

WORKDIR /app

# 1. Install System Deps
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# 2. Install PyTorch CPU
RUN pip install --no-cache-dir --default-timeout=1000 torch --index-url https://download.pytorch.org/whl/cpu

# 3. Upgrade pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# 4. Install Library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Kode Project
COPY . .

# Default command
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]