#!/usr/bin/env python3
"""
Test script to verify SAM2 installation and basic functionality.
Run this script to check if SAM2 is properly installed and working.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__} imported successfully")
        print(f"   CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        import torchvision
        print(f"✅ TorchVision {torchvision.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ TorchVision import failed: {e}")
        return False
    
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__} imported successfully")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print(f"✅ Matplotlib imported successfully")
    except ImportError as e:
        print(f"❌ Matplotlib import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print(f"✅ PIL/Pillow imported successfully")
    except ImportError as e:
        print(f"❌ PIL/Pillow import failed: {e}")
        return False
    
    # Test SAM2 imports
    try:
        from sam2.build_sam import build_sam2, build_sam2_video_predictor
        print("✅ SAM2 build functions imported successfully")
    except ImportError as e:
        print(f"❌ SAM2 build functions import failed: {e}")
        return False
    
    try:
        from sam2.sam2_image_predictor import SAM2ImagePredictor
        print("✅ SAM2ImagePredictor imported successfully")
    except ImportError as e:
        print(f"❌ SAM2ImagePredictor import failed: {e}")
        return False
    
    try:
        from sam2.automatic_mask_generator import SAM2AutomaticMaskGenerator
        print("✅ SAM2AutomaticMaskGenerator imported successfully")
    except ImportError as e:
        print(f"❌ SAM2AutomaticMaskGenerator import failed: {e}")
        return False
    
    return True

def test_model_files():
    """Test if model configuration files exist."""
    print("\n🔍 Testing model configuration files...")
    
    config_files = [
        "configs/sam2.1/sam2.1_hiera_t.yaml",
        "configs/sam2.1/sam2.1_hiera_s.yaml",
        "configs/sam2.1/sam2.1_hiera_b+.yaml",
        "configs/sam2.1/sam2.1_hiera_l.yaml"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ {config_file} found")
        else:
            print(f"❌ {config_file} not found")
    
    return True

def test_checkpoints():
    """Test if model checkpoints exist."""
    print("\n🔍 Testing model checkpoints...")
    
    checkpoint_files = [
        "checkpoints/sam2.1_hiera_tiny.pt",
        "checkpoints/sam2.1_hiera_small.pt",
        "checkpoints/sam2.1_hiera_base_plus.pt",
        "checkpoints/sam2.1_hiera_large.pt"
    ]
    
    found_checkpoints = []
    for checkpoint_file in checkpoint_files:
        if os.path.exists(checkpoint_file):
            size = os.path.getsize(checkpoint_file) / (1024**2)
            print(f"✅ {checkpoint_file} found ({size:.1f} MB)")
            found_checkpoints.append(checkpoint_file)
        else:
            print(f"⚠️  {checkpoint_file} not found")
    
    if len(found_checkpoints) == 0:
        print("❌ No checkpoints found. Run 'cd checkpoints && ./download_ckpts.sh' to download them.")
        return False
    else:
        print(f"✅ {len(found_checkpoints)} checkpoint(s) available")
        return True

def test_model_loading():
    """Test if a model can be loaded."""
    print("\n🔍 Testing model loading...")
    
    try:
        import torch
        from sam2.build_sam import build_sam2
        
        # Find the first available checkpoint
        checkpoint_files = [
            ("checkpoints/sam2.1_hiera_tiny.pt", "configs/sam2.1/sam2.1_hiera_t.yaml"),
            ("checkpoints/sam2.1_hiera_small.pt", "configs/sam2.1/sam2.1_hiera_s.yaml"),
            ("checkpoints/sam2.1_hiera_base_plus.pt", "configs/sam2.1/sam2.1_hiera_b+.yaml"),
            ("checkpoints/sam2.1_hiera_large.pt", "configs/sam2.1/sam2.1_hiera_l.yaml")
        ]
        
        for checkpoint_path, config_path in checkpoint_files:
            if os.path.exists(checkpoint_path) and os.path.exists(config_path):
                device = "cuda" if torch.cuda.is_available() else "cpu"
                print(f"   Loading {checkpoint_path} on {device}...")
                
                model = build_sam2(config_path, checkpoint_path, device=device)
                param_count = sum(p.numel() for p in model.parameters()) / 1e6
                print(f"✅ Model loaded successfully!")
                print(f"   Parameters: {param_count:.1f}M")
                print(f"   Device: {device}")
                return True
        
        print("❌ No valid checkpoint/config pair found")
        return False
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 SAM2 Installation Test")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Configuration Files Test", test_model_files),
        ("Checkpoint Test", test_checkpoints),
        ("Model Loading Test", test_model_loading)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! SAM2 is ready to use.")
        print("📓 You can now run the Colab notebook: sam2_colab_demo.ipynb")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("💡 Try running the installation commands again or check the README.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 