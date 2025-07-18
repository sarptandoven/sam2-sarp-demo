#!/usr/bin/env python3
"""
Service Startup Script for SAM2 Demo
Starts both backend and frontend services
"""

import os
import subprocess
import time
import threading
import signal
import sys

def setup_environment():
    """Setup environment variables"""
    env_vars = {
        'PYTORCH_ENABLE_MPS_FALLBACK': '1',
        'APP_ROOT': '/content/sam2-sarp-demo',
        'DATA_PATH': '/content/sam2-sarp-demo/demo/data',
        'API_URL': 'http://localhost:7263',
        'MODEL_SIZE': 'small',
        'DEFAULT_VIDEO_PATH': 'gallery/01_dog.mp4',
        'PYTHONPATH': '/content/sam2-sarp-demo'
    }
    
    # Check if GPU is available
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        gpu_available = result.returncode == 0
    except:
        gpu_available = False
    
    if gpu_available:
        env_vars['CUDA_VISIBLE_DEVICES'] = '0'
    else:
        env_vars['SAM2_DEMO_FORCE_CPU_DEVICE'] = '1'
    
    # Set environment variables
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print("✅ Environment configured")
    print(f"GPU mode: {'Enabled' if gpu_available else 'Disabled (CPU)'}")
    
    return gpu_available

def start_backend():
    """Start backend server"""
    print("🚀 Starting backend server...")
    
    # Change to backend directory
    os.chdir("demo/backend/server")
    
    # Start Flask backend
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

def start_frontend():
    """Start frontend server"""
    print("🎨 Starting frontend server...")
    
    # Change to frontend directory
    os.chdir("demo/frontend")
    
    # Start Vite frontend
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
    subprocess.run("wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb", shell=True)
    subprocess.run("dpkg -i cloudflared-linux-amd64.deb", shell=True)
    
    # Start tunnels
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
    """Main function"""
    print("🚀 Starting SAM2 Demo services...")
    
    # Setup environment
    setup_environment()
    
    # Start servers
    backend_process = start_backend()
    frontend_process = start_frontend()
    
    # Setup public access
    backend_url, frontend_url = setup_public_access()
    
    print("\n🎉 Services started!")
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