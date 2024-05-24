FROM python:3.12-slim

# Set working directory
WORKDIR /app

ENV BASE_DIR /data/muse/

# Install CMake and other necessary build tools
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential

# Copy the backend requirements file
COPY requirements.txt /app/

# Install backend dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy everything into docker containe
COPY . /app/ 

EXPOSE 5000

CMD ["python3", "core/stream.py"]