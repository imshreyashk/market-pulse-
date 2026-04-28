# Use a lightweight Python image
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some financial libraries)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# The 'default' command (can be overridden by docker-compose)
CMD ["python", "-m", "streamlit", "run", "src/app.py"]