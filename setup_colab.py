#!/usr/bin/env python3
"""
Google Colab Setup Script for SAM2 Demo
Handles all installation, configuration, and environment setup
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

def run_command(cmd, check=True, capture_output=True):
    """Run a shell command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, check=check, 
                              capture_output=capture_output, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(f"Error: {e}")
        return None

def check_gpu():
    """Check if GPU is available"""
    try:
        result = run_command("nvidia-smi", check=False)
        if result and result.returncode == 0:
            print("🚀 GPU detected and available")
            return True
        else:
            print("⚠️  No GPU detected, will use CPU")
            return False
    except:
        print("⚠️  GPU check failed, assuming CPU mode")
        return False

def install_system_dependencies():
    """Install system dependencies"""
    print("📦 Installing system dependencies...")
    
    # Update package list
    run_command("apt-get update -qq")
    
    # Install ffmpeg
    run_command("apt-get install -y ffmpeg")
    
    # Install Node.js 18
    run_command("curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -")
    run_command("apt-get install -y nodejs")
    
    # Install Yarn
    run_command("npm install -g yarn")
    
    print("✅ System dependencies installed")

def install_python_dependencies():
    """Install Python dependencies with specific versions"""
    print("🐍 Installing Python dependencies...")
    
    # Install PyTorch with specific versions to avoid conflicts
    run_command("pip install torch==2.0.1 torchvision==0.15.2 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118")
    
    # Install SAM2 and other requirements
    run_command("pip install -e .")
    run_command("pip install flask flask-cors graphene strawberry-graphql[fastapi] gunicorn")
    run_command("pip install av opencv-python pillow numpy tqdm")
    
    # Try to install decord
    try:
        run_command("pip install decord")
        print("✅ Decord installed successfully")
    except:
        print("⚠️  Decord installation failed, will use OpenCV fallback")
    
    print("✅ Python dependencies installed")

def download_models():
    """Download SAM2 model checkpoints"""
    print("🤖 Downloading SAM2 model checkpoints...")
    
    if os.path.exists("checkpoints/download_ckpts.sh"):
        run_command("cd checkpoints && bash download_ckpts.sh")
        print("✅ Model checkpoints downloaded")
    else:
        print("⚠️  Model download script not found")

def install_frontend_dependencies():
    """Install frontend dependencies"""
    print("🎨 Installing frontend dependencies...")
    
    if os.path.exists("demo/frontend"):
        run_command("cd demo/frontend && yarn install --legacy-peer-deps")
        print("✅ Frontend dependencies installed")
    else:
        print("⚠️  Frontend directory not found")

def setup_environment(gpu_available):
    """Setup environment variables"""
    print("🌍 Setting up environment variables...")
    
    env_vars = {
        'PYTORCH_ENABLE_MPS_FALLBACK': '1',
        'APP_ROOT': '/content/sam2-sarp-demo',
        'DATA_PATH': '/content/sam2-sarp-demo/demo/data',
        'API_URL': 'http://localhost:7263',
        'MODEL_SIZE': 'small',  # Use small model for Colab
        'DEFAULT_VIDEO_PATH': 'gallery/01_dog.mp4',
        'PYTHONPATH': '/content/sam2-sarp-demo'
    }
    
    if gpu_available:
        env_vars['CUDA_VISIBLE_DEVICES'] = '0'
    else:
        env_vars['SAM2_DEMO_FORCE_CPU_DEVICE'] = '1'
    
    # Set environment variables
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("✅ Environment configured")
    print(f"Model size: {env_vars['MODEL_SIZE']}")
    print(f"GPU mode: {'Enabled' if gpu_available else 'Disabled (CPU)'}")

def start_backend_server():
    """Start the backend server"""
    print("🚀 Starting backend server...")
    
    # Change to backend directory
    os.chdir("demo/backend/server")
    
    # Start Flask backend in background
    backend_process = subprocess.Popen(
        ['python', 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    # Wait for startup
    time.sleep(10)
    
    # Check if backend is running
    try:
        import requests
        response = requests.get('http://localhost:7263/graphql', timeout=5)
        if response.status_code == 405:  # Method not allowed (GET on GraphQL endpoint)
            print("✅ Backend server is running on http://localhost:7263")
        else:
            print(f"⚠️  Backend responded with status: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Could not verify backend: {e}")
    
    return backend_process

def start_frontend_server():
    """Start the frontend server"""
    print("🎨 Starting frontend server...")
    
    # Change to frontend directory
    os.chdir("demo/frontend")
    
    # Start Vite frontend in background
    frontend_process = subprocess.Popen(
        ['yarn', 'dev', '--host', '0.0.0.0', '--port', '5173'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    # Wait for startup
    time.sleep(8)
    
    print("✅ Frontend server is running on http://localhost:5173")
    return frontend_process

def setup_public_access():
    """Setup public access with Cloudflare Tunnel"""
    print("🌐 Setting up public access...")
    
    # Install cloudflared
    run_command("wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb")
    run_command("dpkg -i cloudflared-linux-amd64.deb")
    
    # Start tunnels for both services
    def start_tunnel(port, name):
        cmd = ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}']
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        
        # Wait for URL to appear
        for line in iter(process.stdout.readline, ''):
            if 'trycloudflare.com' in line:
                import re
                url_match = re.search(r'https://[\w-]+\.trycloudflare\.com', line)
                if url_match:
                    url = url_match.group(0)
                    print(f"🌐 {name}: {url}")
                    return url
        return None
    
    # Start tunnels in background
    backend_url = start_tunnel(7263, "Backend API")
    frontend_url = start_tunnel(5173, "Frontend App")
    
    return backend_url, frontend_url

def main():
    """Main setup function"""
    print("🚀 Starting SAM2 Demo setup for Google Colab...")
    
    # Check GPU
    gpu_available = check_gpu()
    
    # Install dependencies
    install_system_dependencies()
    install_python_dependencies()
    
    # Download models
    download_models()
    
    # Install frontend dependencies
    install_frontend_dependencies()
    
    # Setup environment
    setup_environment(gpu_available)
    
    # Start servers
    backend_process = start_backend_server()
    frontend_process = start_frontend_server()
    
    # Setup public access
    backend_url, frontend_url = setup_public_access()
    
    print("\n🎉 Setup complete!")
    print(f"Frontend URL: {frontend_url}")
    print(f"Backend URL: {backend_url}")
    print("\nAccess the demo using the Frontend URL above!")
    
    # Keep processes running
    try:
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main() 