FROM python:3.11-slim

WORKDIR /app

# Install required system dependencies for Playwright Chromium
RUN apt-get update && apt-get install -y \
    wget gnupg curl ca-certificates \
    fonts-liberation libnss3 libxss1 libasound2 \
    libatk1.0-0 libatk-bridge2.0-0 libcups2 libx11-xcb1 \
    libxcomposite1 libxdamage1 libxrandr2 libgbm1 \
    libpango-1.0-0 libpangocairo-1.0-0 libxshmfence-dev \
    libglib2.0-0 libgtk-3-0 libdrm2 libxext6 libxfixes3 \
    libxcb1 libx11-6 libxcursor1 libxinerama1 libxrender1 \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Playwright and its browsers
RUN pip install playwright && playwright install chromium

# Copy source files
COPY . .

# Run the script
CMD ["python", "main.py"]
