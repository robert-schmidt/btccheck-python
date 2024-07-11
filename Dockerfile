# Use the official Ubuntu 22.04 image as a base
FROM ubuntu:22.04

ARG ENV
ARG stress_test

# Set environment variables to non-interactive
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    build-essential \
    && apt-get clean


# echo packages versions before upgrading
RUN if [ "$ENV" = "windows" ]; then \
        pip3 install cupy; \
    fi
# Install Python packages
RUN pip3 install numpy bit

# Set the working directory
WORKDIR /app

# Copy the Python script and CSV file into the container
COPY script.py /app/script.py
COPY data.txt /app/data.txt
COPY openssl.conf /usr/local/ssl/openssl.conf
COPY openssl.conf /usr/local/ssl/openssl.cnf
COPY openssl.conf /usr/lib/ssl/openssl.cnf
COPY openssl.conf /etc/ssl/openssl.cnf

# Create the output directory
RUN mkdir -p /app/output
RUN chmod 777 /app/output

# Run the Python script
CMD ["python3", "/app/script.py","--stress-test","0"]
