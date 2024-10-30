# Use a suitable base image
FROM python:3.11

# Install system dependencies including PortAudio and others
RUN apt-get update && \
    apt-get install -y \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    libsndfile1 \
    ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /flask_webapp/flask_webapp

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Specify the command to run the app
CMD ["gunicorn", "-b", "0.0.0.0:5000", "flask_webapp.app:app"]

