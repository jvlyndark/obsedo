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

# Create startup script that runs migrations then starts the app
RUN echo '#!/bin/bash\nflask db upgrade\ngunicorn -b 0.0.0.0:5000 run:app' > start.sh
RUN chmod +x start.sh

# Run the startup script
CMD ["./start.sh"]