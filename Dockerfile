# Minimal py 3.12 image
FROM python:3.12-alpine

# Setup workdir
WORKDIR /app

# Copy files (.dockerignore)
COPY . .

# Setup deps
RUN pip install --no-cache-dir -r requirements.txt

# Run application
CMD ["python", "main.py"]