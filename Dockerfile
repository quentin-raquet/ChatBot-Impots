# Use an official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# Install dependencies needed for building SQLite from source
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libreadline-dev \
    && rm -rf /var/lib/apt/lists/*

# Download and install SQLite 3.45.3
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3450300.tar.gz \
    && tar xzf sqlite-autoconf-3450300.tar.gz \
    && cd sqlite-autoconf-3450300 \
    && ./configure --prefix=/usr/local \
    && make \
    && make install \
    && cd .. \
    && rm -rf sqlite-autoconf-3450300* \
    && apt-get remove -y build-essential wget libreadline-dev \
    && apt-get autoremove -y

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

ENV FLASK_APP=app.py

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]