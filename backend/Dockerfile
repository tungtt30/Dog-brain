FROM python:3.10-slim

# Install requirements
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Makedir
WORKDIR /app

# Copy source
COPY . /app

# Setup Python
RUN pip install --no-cache-dir -r requirements.txt

# Expose port Flask
EXPOSE 5000

# Run app Flask
CMD ["python", "app.py"]
