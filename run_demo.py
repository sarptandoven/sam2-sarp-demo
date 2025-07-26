#!/usr/bin/env python3
"""
Simple script to run SAM2 demo locally
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def setup_environment():
    """Set up environment variables"""
    repo_root = Path.cwd().absolute()
    
    os.environ.update({
        'PYTORCH_ENABLE_MPS_FALLBACK': '1',
        'APP_ROOT': str(repo_root),
        'DATA_PATH': str(repo_root / 'demo' / 'data'),
        'API_URL': 'http://localhost:7263',
        'MODEL_SIZE': 'small',
        'DEFAULT_VIDEO_PATH': 'gallery/01_dog.mp4',
        'PYTHONPATH': str(repo_root),
        'PORT': '7263',
        'SAM2_DEMO_FORCE_CPU_DEVICE': '1'  # Force CPU for compatibility
    })
    
    print("✅ Environment configured")

def start_backend():
    """Start backend server"""
    print("🚀 Starting backend server...")
    
    os.chdir("demo/backend/server")
    
    # Start Flask app
    process = subprocess.Popen([sys.executable, "app.py"])
    
    # Wait for startup
    time.sleep(3)
    
    print("✅ Backend started on http://localhost:7263")
    return process

def start_frontend():
    """Start frontend server"""
    print("🎨 Starting frontend server...")
    
    os.chdir("../../../demo/frontend")
    
    # Start Vite dev server
    try:
        process = subprocess.Popen(["yarn", "dev", "--host", "0.0.0.0", "--port", "5173"])
        time.sleep(3)
        print("✅ Frontend started on http://localhost:5173")
        return process
    except FileNotFoundError:
        print("⚠️  Yarn not found, skipping frontend")
        return None

def main():
    """Main function"""
    print("🚀 Starting SAM2 Demo")
    print("=" * 30)
    
    # Setup environment
    setup_environment()
    
    # Start backend
    backend = start_backend()
    
    # Start frontend
    frontend = start_frontend()
    
    print("\n🎉 Demo is running!")
    print("📱 Frontend: http://localhost:5173")
    print("🔧 Backend: http://localhost:7263")
    print("🔍 GraphQL: http://localhost:7263/graphql")
    print("\n✋ Press Ctrl+C to stop")
    
    try:
        backend.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        backend.terminate()
        if frontend:
            frontend.terminate()
        print("✅ Stopped")

if __name__ == "__main__":
    main() 