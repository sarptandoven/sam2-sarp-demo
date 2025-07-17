# 🎬 SAM2 Demo - Google Colab Deployment

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sarptandoven/sam2-demo/blob/main/SAM2_Colab_Demo.ipynb)

## ⚡ Quick Start

**1-Click Deployment**: Click the "Open in Colab" badge above to launch the demo instantly!

This comprehensive Google Colab notebook provides a complete, GPU-accelerated SAM2 video segmentation demo that runs entirely in the cloud with a public web interface.

## 🚀 Features

- **🔥 GPU Acceleration**: Automatically configured for Google Colab's Tesla T4, V100, or A100 GPUs
- **🌐 Public Web Interface**: Access the demo from any device via a public URL
- **📱 Mobile Friendly**: Responsive design works on phones and tablets
- **🎯 Zero Setup**: No local installation required - everything runs in Colab
- **⚡ Fast Inference**: GPU-optimized for real-time video segmentation
- **📹 Video Upload**: Support for custom video uploads (up to 100MB, 10 seconds)
- **🎨 Visual Effects**: Multiple background and overlay effects
- **💾 Export Options**: Download segmented videos and masks

## 🎯 What You Get

### Interactive Video Segmentation
- Click to select objects in any video frame
- Real-time mask generation with SAM2
- Automatic propagation across all frames
- Support for multiple objects simultaneously

### Professional Effects
- Background replacement and blurring
- Object highlighting and overlays
- Custom color schemes and transparency
- High-quality video export

### Technical Features
- **Model**: SAM2 (Segment Anything 2) by Meta AI
- **Backend**: Flask + GraphQL API
- **Frontend**: React + TypeScript with Vite
- **GPU Support**: CUDA acceleration on Colab
- **Public Access**: Cloudflare tunnels for external access

## 📋 Prerequisites

- Google account (for Colab access)
- Modern web browser
- Internet connection

**That's it!** No software installation or setup required.

## 🔧 How It Works

The notebook automatically:

1. **🔧 Environment Setup**: Configures GPU runtime and system dependencies
2. **📥 Code Download**: Clones the latest SAM2 demo repository
3. **🤖 Model Loading**: Downloads and initializes SAM2 model weights
4. **🚀 Service Launch**: Starts backend API and frontend web server
5. **🌐 Public Access**: Creates secure tunnel for external access
6. **📊 Monitoring**: Provides real-time status and health checks

## 🎮 Usage Instructions

### Getting Started
1. Click the "Open in Colab" badge above
2. Go to `Runtime` → `Change runtime type` → Select `GPU`
3. Run all cells in order (or `Runtime` → `Run all`)
4. Wait for the public URL to appear (3-5 minutes)
5. Click the generated link to access the demo

### Using the Demo
1. **Select a Video**: Choose from gallery or upload your own
2. **Add Objects**: Click "Add Object" and select areas in the video
3. **Preview Segmentation**: Watch real-time mask generation
4. **Apply Effects**: Choose background and overlay effects
5. **Export Results**: Download the final segmented video

### Pro Tips
- Start with gallery videos to test the interface
- Upload videos under 10 seconds for best performance
- Use the filmstrip to navigate between frames
- Try different effects for creative results

## 🔧 Troubleshooting

### Common Issues

**Services Not Starting**
- Ensure GPU runtime is selected
- Re-run the setup cells if needed
- Check the service status cell for details

**GPU Not Detected**
- Go to `Runtime` → `Change runtime type` → Select `GPU`
- Restart runtime if necessary

**Video Upload Fails**
- Ensure video is under 100MB and 10 seconds
- Use common formats (MP4, MOV, AVI)
- Check file isn't corrupted

**Slow Performance**
- Verify GPU is being used (check status cell)
- Try smaller model size (change `MODEL_SIZE` to `tiny`)
- Use shorter videos for faster processing

### Advanced Troubleshooting

**Manual Service Control**
```python
# Check if services are running
!ps aux | grep -E "(python.*7263|yarn.*5173)"

# Restart backend if needed
%cd /content/sam2-demo/demo/backend/server
!python app.py &

# Restart frontend if needed  
%cd /content/sam2-demo/demo/frontend
!yarn dev --host 0.0.0.0 --port 5173 &
```

**Debug Logs**
- Backend logs: Check Python process output
- Frontend logs: Check Yarn/Vite build output
- GPU usage: Monitor with status check cell

## 🎯 Technical Architecture

### Backend Services
- **SAM2 Model**: GPU-accelerated inference engine
- **GraphQL API**: Efficient data queries and mutations
- **Video Processing**: FFmpeg-based transcoding and optimization
- **File Management**: Secure upload and storage handling

### Frontend Application
- **React Framework**: Modern, responsive user interface
- **TypeScript**: Type-safe development and better debugging
- **Vite Build**: Fast development and optimized production builds
- **Real-time Updates**: WebSocket-like GraphQL subscriptions

### Infrastructure
- **Google Colab**: Free GPU compute environment
- **Cloudflare Tunnels**: Secure public access without port forwarding
- **Container Architecture**: Isolated, reproducible deployment

## 📊 Performance Metrics

### Typical Performance (Tesla T4)
- **Model Loading**: 10-20 seconds
- **Video Upload**: 2-5 seconds (10MB file)
- **Initial Segmentation**: 1-2 seconds per object
- **Frame Propagation**: 0.5-1 second per frame
- **Effect Rendering**: 2-3 seconds for full video

### Resource Usage
- **GPU Memory**: 2-4GB (depending on video resolution)
- **System RAM**: 1-2GB for services
- **Disk Space**: 3-5GB for models and dependencies
- **Network**: Minimal after initial setup

## 🌟 Advanced Features

### Custom Model Configuration
```python
# Use different model sizes
os.environ['MODEL_SIZE'] = 'tiny'    # Fastest, lower quality
os.environ['MODEL_SIZE'] = 'small'   # Balanced (default)
os.environ['MODEL_SIZE'] = 'base_plus'  # Best quality, slower
```

### Development Mode
```python
# Enable debug mode for development
os.environ['DEBUG'] = 'true'
os.environ['FLASK_ENV'] = 'development'
```

### Custom Video Processing
```python
# Adjust video processing parameters
os.environ['MAX_UPLOAD_FILE_SIZE'] = '50MB'      # Smaller uploads
os.environ['MAX_UPLOAD_DURATION'] = '5'         # Shorter videos
os.environ['VIDEO_RESOLUTION'] = '720p'         # Lower resolution
```

## 🤝 Contributing

This Colab deployment is part of the larger SAM2 demo project. Contributions welcome!

### Local Development
For local development and contributions, see the main [README.md](README.md) for setup instructions.

### Issues and Support
- **Bug Reports**: [GitHub Issues](https://github.com/sarptandoven/sam2-demo/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/sarptandoven/sam2-demo/discussions)
- **Documentation**: [Project Wiki](https://github.com/sarptandoven/sam2-demo/wiki)

## 📜 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Meta AI Research**: For the original SAM2 model and research
- **Google Colab**: For providing free GPU access
- **Cloudflare**: For tunnel infrastructure
- **Open Source Community**: For the amazing tools and libraries

---

**Ready to try it?** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sarptandoven/sam2-demo/blob/main/SAM2_Colab_Demo.ipynb) 