# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies for OpenCV and other libraries
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main application file (corrected filename)
COPY app.py .

# Copy necessary directories only
COPY model/ ./model/
COPY assets/ ./assets/
COPY yolo_dataset/ ./yolo_dataset/

# Set environment variable for port
ENV PORT=8080

# Expose port 8080
EXPOSE 8080

# Run Streamlit app (corrected filename)
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless=true", "--server.enableCORS=false"]