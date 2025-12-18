FROM python:3.9-slim

WORKDIR /app

# 1. Install Chrome & System Deps (Layer 1)
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl ca-certificates --no-install-recommends \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 2. Install PyTorch CPU Only (Layer 2)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# 3. Install Library Lain (Layer 3)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Install Sentence Transformers (Layer 4)
RUN pip install --no-cache-dir sentence-transformers

# 5. Copy Kode Project
COPY . .

CMD ["python", "src/scraper_job.py"]