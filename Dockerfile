# Use the official Python image as a base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Copy the data directory
COPY data/ ./data/

# Copy the .streamlit folder
COPY .streamlit/ .streamlit/

# Expose the Streamlit port
EXPOSE 8501

# Run define_schema.py and ingest_games.py before starting Streamlit
CMD ["bash", "-c", "python define_schema.py && python ingest_games.py && streamlit run app.py"]
