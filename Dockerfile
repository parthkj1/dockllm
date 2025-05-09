FROM python:3.10-slim

# Set environment variable for Ray Serve
ENV RAY_SERVE_HOST=0.0.0.0

# Install Git and clean up cache
RUN apt-get update && apt-get install -y git && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Clone your GitHub repo (replace with your actual repo if needed)
RUN git clone https://github.com/parthkj1/dockllm.git . 

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "serve_app.py"]

# Expose FastAPI and Ray ports
EXPOSE 8000 6379 8265
