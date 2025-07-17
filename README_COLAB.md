# 🚀 SAM2 Demo - Google Colab Deployment

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sarptandoven/sam2-sarp-demo/blob/main/SAM2_Colab_Demo.ipynb)

**One-click deployment of SAM2 video segmentation demo on Google Colab with GPU acceleration and public web access.**

## ✨ Features

### 🎯 AI-Powered Video Segmentation
- **Real-time Object Tracking**: Click to track any object in video frames
- **Multi-object Support**: Track multiple objects simultaneously
- **Instant Preview**: See segmentation results in real-time

### 🎨 Interactive Video Editing
- **Background Effects**: Blur, replace, or remove backgrounds
- **Visual Overlays**: Add arrows, text, and effects
- **Professional Export**: Download high-quality processed videos

### 🚀 Optimized for Colab
- **GPU Acceleration**: Optimized for Tesla T4/V100/A100 GPUs
- **Public Access**: Get shareable URLs for any device
- **Zero Setup**: Everything configured automatically

## 🔧 Quick Start

### 1. Open in Colab
Click the badge above or visit: https://colab.research.google.com/github/sarptandoven/sam2-sarp-demo/blob/main/SAM2_Colab_Demo.ipynb

### 2. Enable GPU (Recommended)
- Go to `Runtime` → `Change runtime type`
- Select `T4 GPU` or higher
- Click `Save`

### 3. Run All Cells
- Press `Ctrl+F9` to run all cells
- Or click `Runtime` → `Run all`
- Wait 3-5 minutes for setup

### 4. Access Your Demo
- Look for the public URL in the output
- Click the frontend URL to start using the demo
- Share the URL with others!

## 📊 Technical Specifications

### Performance Metrics
- **Model Loading**: 10-20 seconds
- **Video Processing**: 0.5-1 second per frame
- **GPU Memory Usage**: 2-4GB
- **Initial Setup Time**: 3-5 minutes

### Supported Formats
- **Input Videos**: MP4, WebM, AVI (max 10 seconds, 100MB)
- **Output Videos**: MP4 with H.264 encoding
- **Resolution**: Up to 1080p (720p recommended for speed)

### Model Sizes Available
- **Tiny**: 149MB - Fastest, good for demos
- **Small**: 181MB - **Default** - Balanced speed/accuracy
- **Base Plus**: 688MB - Higher accuracy
- **Large**: 901MB - Best quality (requires more GPU memory)

## 🎮 How to Use

### Basic Workflow
1. **Select Video**: Choose from gallery or upload your own
2. **Track Objects**: Click on objects you want to segment
3. **Apply Effects**: Use toolbar to add backgrounds and overlays
4. **Export Results**: Download your processed video

### Pro Tips
- **Multiple Objects**: Track different objects with different colors
- **Frame Navigation**: Use filmstrip to navigate to specific frames
- **Effect Timing**: Apply effects to specific frame ranges
- **Performance**: Lower resolution videos process faster

## 🛠️ Advanced Configuration

### Change Model Size
Edit the environment variable in the setup cell:
```python
os.environ['MODEL_SIZE'] = 'base_plus'  # tiny, small, base_plus, large
```

### CPU Mode (if GPU unavailable)
```python
os.environ['SAM2_DEMO_FORCE_CPU_DEVICE'] = '1'
```

### Custom Video Limits
```python
os.environ['MAX_VIDEO_DURATION'] = '15'  # seconds
os.environ['MAX_FILE_SIZE'] = '150'      # MB
```

## 🐛 Troubleshooting

### Common Issues

#### "No GPU detected"
- **Solution**: Enable GPU in Runtime settings
- **Fallback**: Code will work on CPU (slower)

#### "Backend not responding"
- **Solution**: Re-run the backend startup cell
- **Check**: Look for port conflicts in the output

#### "Frontend URL not working"
- **Solution**: Wait 30 seconds and try again
- **Alternative**: Use the local URL if on same machine

#### "Video upload fails"
- **Check**: File size under 100MB
- **Check**: Duration under 10 seconds
- **Try**: Different video format (MP4 recommended)

#### "Segmentation is slow"
- **Switch**: To smaller model size
- **Reduce**: Video resolution
- **Check**: GPU is enabled and available

### Restart Everything
If something goes wrong:
1. `Runtime` → `Restart runtime`
2. Run all cells again
3. Wait for complete setup

### Check Service Status
```python
# Backend health check
!curl http://localhost:7263/health

# Check running processes
!ps aux | grep python

# Check GPU usage
!nvidia-smi
```

## 🔧 Development Mode

### Local Development
To run locally instead of Colab:
```bash
git clone https://github.com/sarptandoven/sam2-sarp-demo.git
cd sam2-sarp-demo

# Install dependencies
pip install -e .
pip install -r demo/backend/requirements.txt
cd demo/frontend && yarn install

# Start services
cd ../backend/server && python app.py &
cd ../../frontend && yarn dev
```

### Environment Variables
Key configuration options:
```bash
export MODEL_SIZE="small"                    # Model size
export APP_ROOT="/path/to/sam2-sarp-demo"   # Root directory
export DATA_PATH="/path/to/demo/data"       # Data directory
export API_URL="http://localhost:7263"      # Backend URL
export PYTORCH_ENABLE_MPS_FALLBACK=1        # GPU fallback
```

## 📈 Performance Optimization

### GPU Memory Management
- **T4 GPU**: Use 'small' or 'tiny' model
- **V100/A100**: Can handle 'base_plus' or 'large'
- **Multiple videos**: Clear sessions between videos

### Speed Optimization
- **Lower resolution**: 480p-720p for faster processing
- **Shorter videos**: Under 5 seconds for real-time feel
- **Fewer objects**: Track 1-3 objects for best performance

### Quality vs Speed
- **Quality**: Use 'base_plus' or 'large' model
- **Speed**: Use 'tiny' or 'small' model
- **Balanced**: 'small' model (default)

## 🌐 Sharing Your Demo

### Public URLs
- URLs are valid for ~8 hours
- Work on any device with internet
- No authentication required

### Custom Domains
For persistent URLs, consider:
- ngrok (paid plans)
- serveo.net
- localhost.run

### Embedding
You can embed the demo in websites:
```html
<iframe src="https://your-tunnel-url.trycloudflare.com" 
        width="100%" height="600px">
</iframe>
```

## 🔐 Security & Privacy

### Data Handling
- **Videos**: Processed locally in Colab, not stored
- **Models**: Downloaded from official Meta repositories
- **Privacy**: No data sent to external services

### Network Access
- Cloudflare tunnels provide secure HTTPS
- URLs expire automatically
- No persistent storage

## 🤝 Contributing

This demo is based on Meta's SAM2 model. Contributions welcome!

- **Repository**: https://github.com/sarptandoven/sam2-sarp-demo
- **Issues**: Report bugs and feature requests
- **Pull Requests**: Improvements and new features

## 📚 Resources

### Official SAM2
- **Paper**: [Segment Anything 2](https://ai.meta.com/research/publications/segment-anything-2/)
- **Original Code**: https://github.com/facebookresearch/segment-anything-2
- **Demo**: https://sam2.metademolab.com/

### Related Projects
- **Segment Anything**: Original SAM model
- **ComfyUI**: Use exported masks in ComfyUI workflows
- **Video Editing**: Integration with professional video tools

---

**🚀 Ready to segment anything in your videos? Click the Colab badge above to get started!** 