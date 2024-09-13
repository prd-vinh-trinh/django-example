FROM python:3.12

WORKDIR /app


RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container's working directory
COPY Backend/ /app

# Open port 8000 to allow traffic
EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
