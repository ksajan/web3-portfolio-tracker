FROM python:3.11-slim

# Install necessary build tools and dependencies
RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y --no-install-recommends \
  gcc \
  build-essential &&\
  apt-get clean &&\
  rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools

# Environment variables to prevent Python from writing bytecode and buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Add user and group
RUN groupadd -g 7777 crypto-quants &&\
  useradd -m -d /home/crypto-quants crypto-quants -s /bin/false -u 7777 -g crypto-quants

# Switch to the newly created user
USER crypto-quants

# Copy requirements file and install Python dependencies
COPY --chown=crypto-quants:crypto-quants requirements.txt /home/crypto-quants/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /home/crypto-quants/requirements.txt

# Create application directory
RUN mkdir /home/crypto-quants/app

# Set working directory
WORKDIR /home/crypto-quants/app

# Copy application files
COPY --chown=crypto-quants:crypto-quants . .

# Ensure scripts are executable
RUN chmod 554 /home/crypto-quants/app/deployment/*.sh

# Update PATH environment variable
ENV PATH="/home/crypto-quants/.local/bin:$PATH"

# Entry point for the container
ENTRYPOINT ["./deployment/app.sh"]

