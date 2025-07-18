#!/bin/bash
# System Dependencies Installation Script for Google Colab

echo "📦 Installing system dependencies..."

# Update package list
apt-get update -qq

# Install ffmpeg for video processing
apt-get install -y ffmpeg

# Install Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
apt-get install -y nodejs

# Install Yarn
npm install -g yarn

# Verify installations
echo "🔍 Verifying installations:"
ffmpeg -version | head -1
node --version
yarn --version

echo "✅ System dependencies installed!" 