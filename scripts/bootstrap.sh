#!/bin/bash

set -e

echo "Updating package index..."
apt-get update

echo "Upgrading installed packages..."
DEBIAN_FRONTEND=noninteractive apt-get upgrade -y

echo "Installing base packages..."
apt-get install -y \
    curl \
    wget \
    git \
    unzip \
    ca-certificates \
    gnupg \
    lsb-release \
    software-properties-common \
    apt-transport-https

echo "Installing Docker..."

# Create directory for Docker GPG key
install -m 0755 -d /etc/apt/keyrings

# Download Docker official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository
tee /etc/apt/sources.list.d/docker.sources > /dev/null <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

echo "Updating package index after adding Docker repository..."
apt-get update

echo "Installing Docker packages..."
apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin

echo "Enabling and starting Docker service..."
systemctl enable docker
systemctl start docker

echo "Adding vagrant user to docker group..."
usermod -aG docker vagrant

echo "Bootstrap complete."