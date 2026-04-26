FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the app (or copy if building locally)
COPY . .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit and FastAPI ports
EXPOSE 8501
EXPOSE 8000

# Default command to run streamlit
# For FastAPI use: uvicorn api:app --host 0.0.0.0 --port 8000
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
