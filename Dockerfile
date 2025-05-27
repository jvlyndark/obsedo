# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set Flask app
ENV FLASK_APP=run.py

# Expose port
EXPOSE 5000

# Run migrations then start the app
CMD ["sh", "-c", "flask db upgrade && gunicorn -b 0.0.0.0:5000 run:app"]