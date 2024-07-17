FROM python:3.11-slim

# Install necessary build tools and dependencies
RUN apt-get update && \
  apt-get -y upgrade && \
  apt-get install -y --no-install-recommends \
  gcc \
  curl \
  build-essential && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN pip install --no-cache-dir --upgrade pip setuptools

# Environment variables to prevent Python from writing bytecode and buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Add user and group
RUN groupadd -g 7777 crypto-quants && \
  useradd -m -d /home/crypto-quants crypto-quants -s /bin/bash -u 7777 -g crypto-quants

# Switch to the newly created user
USER crypto-quants

# Node Version
ENV NVM_DIR /home/crypto-quants/.nvm
ENV NODE_VERSION 22

# Install Nodejs
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && \
  . "$NVM_DIR/nvm.sh" && \
  nvm install $NODE_VERSION && \
  nvm use $NODE_VERSION && \
  nvm alias default $NODE_VERSION && \
  echo 'export NVM_DIR="$HOME/.nvm"' >> /home/crypto-quants/.bashrc && \
  echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> /home/crypto-quants/.bashrc && \
  echo 'export PATH="$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH"' >> /home/crypto-quants/.bashrc

# Add nvm to PATH
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Copy requirements file and install Python dependencies
COPY --chown=crypto-quants:crypto-quants requirements.txt /home/crypto-quants/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /home/crypto-quants/requirements.txt

# Install the zeta market pypi individually to resolve the conflict
RUN pip install --no-cache-dir --upgrade zetamarkets_py

# Create application directory
RUN mkdir /home/crypto-quants/app

# Set working directory
WORKDIR /home/crypto-quants/app

# Copy application files
COPY --chown=crypto-quants:crypto-quants . .

# Ensure scripts are executable
RUN chmod +x /home/crypto-quants/app/deployment/*.sh

# Update PATH environment variable
ENV PATH="/home/crypto-quants/.local/bin:$PATH"

# Entry point for the container
ENTRYPOINT ["bash", "-c", "source /home/crypto-quants/.nvm/nvm.sh && ./deployment/app.sh"]

