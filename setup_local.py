#!/usr/bin/env python3
"""
Local Setup Script for SAM2 Demo
Ensures all dependencies are installed and environment is configured
"""

import os
import sys
import subprocess
import time
import threading
import platform
from pathlib import Path

def run_command(cmd, check=True, capture_output=False, shell=True):
    """Run a shell command and return result"""
    try:
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=shell, check=check, 
                              capture_output=capture_output, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {cmd}")
        print(f"Error: {e}")
        if not check:
            return None
        raise

def check_and_install_dependencies():
    """Check and install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    # Get the current directory (repository root)
    repo_root = Path.cwd()
    
    # Install SAM2 package in development mode
    run_command("pip install -e .")
    
    # Install interactive demo dependencies
    dependencies = [
        "flask>=3.0.3",
        "flask-cors>=5.0.0", 
        "gunicorn>=23.0.0",
        "strawberry-graphql>=0.243.0",
        "graphene>=3.0",
        "av>=13.0.0",
        "opencv-python>=4.7.0",
        "pillow>=9.4.0",
        "numpy>=1.24.4",
        "tqdm>=4.66.1",
        "dataclasses-json>=0.6.7",
        "imagesize>=1.4.1",
        "pycocotools>=2.0.8"
    ]
    
    for dep in dependencies:
        try:
            run_command(f"pip install '{dep}'")
        except:
            print(f"⚠️  Warning: Could not install {dep}")
    
    # Try to install decord, but don't fail if it doesn't work
    try:
        run_command("pip install eva-decord>=0.6.1", check=False)
        print("✅ Decord installed successfully")
    except:
        print("⚠️  Decord installation failed, will use OpenCV fallback")
    
    print("✅ Python dependencies installed")

def check_system_dependencies():
    """Check system dependencies"""
    print("🔍 Checking system dependencies...")
    
    # Check ffmpeg
    try:
        result = run_command("ffmpeg -version", check=False, capture_output=True)
        if result and result.returncode == 0:
            print("✅ ffmpeg is available")
        else:
            print("⚠️  ffmpeg not found. Install it using:")
            if platform.system() == "Darwin":
                print("   brew install ffmpeg")
            else:
                print("   sudo apt-get install ffmpeg")
    except:
        print("⚠️  ffmpeg not found")
    
    # Check Node.js for frontend
    try:
        result = run_command("node --version", check=False, capture_output=True)
        if result and result.returncode == 0:
            print("✅ Node.js is available")
        else:
            print("⚠️  Node.js not found. Install from https://nodejs.org/")
    except:
        print("⚠️  Node.js not found")

def setup_environment():
    """Setup environment variables"""
    print("⚙️  Setting up environment...")
    
    repo_root = Path.cwd().absolute()
    
    env_vars = {
        'PYTORCH_ENABLE_MPS_FALLBACK': '1',
        'APP_ROOT': str(repo_root),
        'DATA_PATH': str(repo_root / 'demo' / 'data'),
        'API_URL': 'http://localhost:7263',
        'MODEL_SIZE': 'small',  # Use small model for local testing
        'DEFAULT_VIDEO_PATH': 'gallery/01_dog.mp4',
        'PYTHONPATH': str(repo_root),
        'FLASK_APP': 'app.py',
        'FLASK_ENV': 'development'
    }
    
    # Check for GPU
    gpu_available = False
    try:
        import torch
        if torch.cuda.is_available():
            gpu_available = True
            env_vars['CUDA_VISIBLE_DEVICES'] = '0'
        elif torch.backends.mps.is_available():
            gpu_available = True
            print("✅ MPS (Apple Silicon) GPU detected")
        else:
            env_vars['SAM2_DEMO_FORCE_CPU_DEVICE'] = '1'
    except:
        env_vars['SAM2_DEMO_FORCE_CPU_DEVICE'] = '1'
    
    # Set environment variables
    for key, value in env_vars.items():
        os.environ[key] = value
    
    print(f"✅ Environment configured")
    print(f"GPU mode: {'Enabled' if gpu_available else 'Disabled (CPU)'}")
    print(f"Repository root: {repo_root}")
    
    return env_vars

def download_models():
    """Download SAM2 model checkpoints"""
    print("📥 Checking model checkpoints...")
    
    checkpoints_dir = Path("checkpoints")
    if not checkpoints_dir.exists():
        print("Creating checkpoints directory...")
        checkpoints_dir.mkdir()
    
    # Check if models exist
    model_files = [
        "sam2.1_hiera_tiny.pt",
        "sam2.1_hiera_small.pt", 
        "sam2.1_hiera_base_plus.pt"
    ]
    
    missing_models = []
    for model_file in model_files:
        if not (checkpoints_dir / model_file).exists():
            missing_models.append(model_file)
    
    if missing_models:
        print(f"Missing models: {missing_models}")
        print("Run the download script to get models:")
        print("cd checkpoints && bash download_ckpts.sh")
    else:
        print("✅ Model checkpoints are available")

def install_frontend_dependencies():
    """Install frontend dependencies"""
    print("🎨 Installing frontend dependencies...")
    
    frontend_dir = Path("demo/frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Change to frontend directory
    original_dir = os.getcwd()
    try:
        os.chdir(frontend_dir)
        
        # Check if node_modules exists
        if not Path("node_modules").exists():
            print("Installing yarn dependencies...")
            run_command("yarn install --legacy-peer-deps")
        else:
            print("✅ Frontend dependencies already installed")
        
        return True
    except Exception as e:
        print(f"❌ Frontend setup failed: {e}")
        return False
    finally:
        os.chdir(original_dir)

def start_backend_server():
    """Start the backend server"""
    print("🚀 Starting backend server...")
    
    backend_dir = Path("demo/backend/server")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return None
    
    # Change to backend directory
    original_dir = os.getcwd()
    os.chdir(backend_dir)
    
    try:
        # Start Flask backend
        cmd = [sys.executable, "app.py"]
        process = subprocess.Popen(cmd, 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.STDOUT,
                                 text=True,
                                 bufsize=1,
                                 universal_newlines=True)
        
        # Wait a bit for startup
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Backend server started")
            return process
        else:
            print("❌ Backend server failed to start")
            return None
            
    finally:
        os.chdir(original_dir)

def start_frontend_server():
    """Start the frontend server"""
    print("🎨 Starting frontend server...")
    
    frontend_dir = Path("demo/frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return None
    
    # Change to frontend directory
    original_dir = os.getcwd()
    os.chdir(frontend_dir)
    
    try:
        # Start Vite frontend
        cmd = ["yarn", "dev", "--host", "0.0.0.0", "--port", "5173"]
        process = subprocess.Popen(cmd,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 text=True,
                                 bufsize=1,
                                 universal_newlines=True)
        
        # Wait a bit for startup
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Frontend server started")
            return process
        else:
            print("❌ Frontend server failed to start")
            return None
            
    finally:
        os.chdir(original_dir)

def monitor_processes(backend_process, frontend_process):
    """Monitor server processes and handle output"""
    def log_output(process, name):
        if process and process.stdout:
            for line in iter(process.stdout.readline, ''):
                if line:
                    print(f"[{name}] {line.strip()}")
    
    # Start monitoring threads
    if backend_process:
        backend_thread = threading.Thread(target=log_output, args=(backend_process, "BACKEND"))
        backend_thread.daemon = True
        backend_thread.start()
    
    if frontend_process:
        frontend_thread = threading.Thread(target=log_output, args=(frontend_process, "FRONTEND"))
        frontend_thread.daemon = True
        frontend_thread.start()

def main():
    """Main setup and run function"""
    print("🚀 SAM2 Demo Local Setup")
    print("=" * 50)
    
    try:
        # Setup steps
        check_system_dependencies()
        check_and_install_dependencies()
        env_vars = setup_environment()
        download_models()
        
        # Install frontend dependencies
        if not install_frontend_dependencies():
            print("⚠️  Frontend setup failed, but continuing...")
        
        print("\n🎯 Starting servers...")
        print("=" * 30)
        
        # Start backend server
        backend_process = start_backend_server()
        if not backend_process:
            print("❌ Failed to start backend server")
            return 1
        
        # Start frontend server
        frontend_process = start_frontend_server()
        if not frontend_process:
            print("⚠️  Frontend server failed to start")
        
        # Monitor processes
        monitor_processes(backend_process, frontend_process)
        
        print("\n🎉 Setup complete!")
        print("=" * 30)
        print(f"🌐 Backend API: http://localhost:7263/graphql")
        if frontend_process:
            print(f"🎨 Frontend App: http://localhost:5173")
        print("\n📝 Environment variables:")
        for key, value in env_vars.items():
            print(f"   {key}={value}")
        
        print("\n✋ Press Ctrl+C to stop servers")
        
        # Keep running until interrupted
        try:
            while True:
                # Check if processes are still running
                if backend_process and backend_process.poll() is not None:
                    print("❌ Backend process died")
                    break
                if frontend_process and frontend_process.poll() is not None:
                    print("⚠️  Frontend process died")
                    
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Shutting down servers...")
            
        finally:
            # Clean up processes
            if backend_process:
                backend_process.terminate()
            if frontend_process:
                frontend_process.terminate()
                
            print("✅ Servers stopped")
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 