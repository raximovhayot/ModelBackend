FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PORT=5000
ENV DATABASE_URL=sqlite:///ddos_detection.db
ENV REDIS_URL=redis://:root123@redis:6379/0

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "run.py"]
