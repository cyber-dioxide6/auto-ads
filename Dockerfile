FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Playwright browsers
RUN apt-get update && apt-get install -y wget gnupg curl ca-certificates fonts-liberation libnss3 libxss1 libasound2 libatk1.0-0 libatk-bridge2.0-0 libcups2 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 libpangocairo-1.0-0 libxshmfence-dev && \
    pip install playwright && playwright install chromium

# Copy project files
COPY . .

# Run the Python script
CMD ["python", "auto_clicker.py"]
