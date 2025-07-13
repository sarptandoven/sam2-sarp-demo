# SAM2 Colab Demo - Perfect Setup for Google Colab

This repository contains a perfectly configured version of Meta's SAM2 (Segment Anything Model 2) optimized for Google Colab usage. It includes comprehensive examples, easy setup, and all necessary dependencies.

## 🚀 Features

- ✅ **Plug-and-play Colab setup** - Just run the notebook!
- ✅ **Complete installation guide** - All dependencies handled automatically
- ✅ **Image segmentation examples** - Point, box, and combined prompts
- ✅ **Automatic mask generation** - Segment everything in an image
- ✅ **Video segmentation & tracking** - Track objects through video sequences
- ✅ **Interactive tools** - Build custom segmentation workflows
- ✅ **Performance optimization** - Optimized for Colab GPU instances
- ✅ **Multiple model sizes** - From tiny (fast) to large (accurate)

## 📱 Quick Start

### Option 1: Google Colab (Recommended)

1. **Open in Colab**: Click the "Open in Colab" badge in the notebook
2. **Connect to GPU**: Runtime → Change runtime type → GPU
3. **Run all cells**: Runtime → Run all (or Ctrl+F9)
4. **Start segmenting**: Upload your own images or use the provided examples

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/SAM2-SARP-DEMO/blob/main/sam2_colab_demo.ipynb)

### Option 2: Local Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/SAM2-SARP-DEMO.git
cd SAM2-SARP-DEMO

# Install dependencies (Python 3.10+ required)
pip install torch>=2.5.1 torchvision>=0.20.1
pip install numpy matplotlib opencv-python pillow jupyter
pip install hydra-core iopath av tqdm

# Install SAM2
SAM2_BUILD_CUDA=0 pip install -e .

# Download model checkpoints
cd checkpoints && ./download_ckpts.sh && cd ..

# Launch Jupyter
jupyter notebook sam2_colab_demo.ipynb
```

## 🤖 Model Sizes

Choose the right model for your needs:

| Model | Size | Speed | Accuracy | Use Case |
|-------|------|-------|----------|----------|
| `sam2.1_hiera_tiny` | 38.9M | ⚡ Fastest | Good | Real-time, mobile apps |
| `sam2.1_hiera_small` | 46M | 🚀 Fast | Better | **Recommended for Colab** |
| `sam2.1_hiera_base_plus` | 80.8M | 🔄 Medium | Great | High-quality results |
| `sam2.1_hiera_large` | 224.4M | 🐌 Slow | Best | Maximum accuracy |

## 🎯 Usage Examples

### Image Segmentation with Points

```python
# Click on an object to segment it
input_points = np.array([[500, 375]])  # (x, y) coordinates
input_labels = np.array([1])  # 1 = positive, 0 = negative

masks, scores, logits = image_predictor.predict(
    point_coords=input_points,
    point_labels=input_labels,
    multimask_output=True,
)
```

### Bounding Box Segmentation

```python
# Draw a box around an object
input_box = np.array([x1, y1, x2, y2])  # Bounding box coordinates

masks, scores, logits = image_predictor.predict(
    box=input_box[None, :],
    multimask_output=False,
)
```

### Automatic Mask Generation

```python
# Segment everything in the image automatically
masks = mask_generator.generate(image)
print(f"Found {len(masks)} objects")
```

### Video Object Tracking

```python
# Track objects through video frames
video_predictor = build_sam2_video_predictor(config, checkpoint)
inference_state = video_predictor.init_state(video_path)

# Add tracking points
video_predictor.add_new_points_or_box(
    inference_state, frame_idx=0, obj_id=1, 
    points=points, labels=labels
)

# Propagate through video
for frame_idx, obj_ids, masks in video_predictor.propagate_in_video(inference_state):
    # Process each frame
    pass
```

## 📂 Repository Structure

```
SAM2-SARP-DEMO/
├── sam2_colab_demo.ipynb      # 📓 Main Colab notebook
├── sam2/                      # 🤖 SAM2 source code
├── checkpoints/               # 💾 Model checkpoints
│   ├── sam2.1_hiera_tiny.pt
│   ├── sam2.1_hiera_small.pt
│   ├── sam2.1_hiera_base_plus.pt
│   └── sam2.1_hiera_large.pt
├── notebooks/                 # 📚 Example notebooks
├── configs/                   # ⚙️ Model configurations
├── demo/                      # 🎮 Web demo code
├── training/                  # 🏋️ Training scripts
├── README_DEMO.md             # 📖 This file
└── requirements.txt           # 📋 Dependencies
```

## 🔧 Troubleshooting

### Common Issues

**1. GPU Memory Issues**
```python
# Use smaller model or reduce image resolution
MODEL_NAME = "sam2.1_hiera_tiny"  # Instead of large
```

**2. CUDA Extension Errors**
```python
# Skip CUDA extension (already configured in notebook)
os.environ['SAM2_BUILD_CUDA'] = '0'
```

**3. Installation Problems**
```bash
# Install dependencies separately
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install -e . --no-deps
```

**4. Colab Disconnection**
- Enable "Runtime → Manage sessions" to monitor
- Use "Runtime → Factory reset runtime" if needed
- Save outputs before long runs

### Performance Tips

1. **Use appropriate model size** for your hardware
2. **Reduce image resolution** for faster processing
3. **Use batch processing** for multiple images
4. **Enable mixed precision** (already configured)
5. **Clear GPU memory** between large operations

## 📚 Resources

- **[Original SAM2 Paper](https://ai.meta.com/research/publications/sam-2-segment-anything-in-images-and-videos/)**
- **[Official SAM2 Repository](https://github.com/facebookresearch/sam2)**
- **[SAM2 Demo](https://sam2.metademolab.com/)**
- **[Hugging Face Models](https://huggingface.co/models?search=facebook/sam2)**

## 🎓 What You'll Learn

By running this notebook, you'll learn:

1. **Setup & Installation**: How to configure SAM2 for Colab
2. **Image Segmentation**: Using prompts for precise segmentation
3. **Automatic Segmentation**: Generating masks for all objects
4. **Video Tracking**: Following objects through video sequences
5. **Model Optimization**: Choosing the right model for your needs
6. **Interactive Tools**: Building custom segmentation workflows

## 🤝 Contributing

Feel free to improve this demo:

1. Fork the repository
2. Create your feature branch
3. Submit a pull request

## 📄 License

This project maintains the same license as the original SAM2:
- SAM2 model and code: Apache 2.0
- Demo code: Apache 2.0

## 🙏 Acknowledgments

- **Meta AI Research** for creating SAM2
- **Facebook Research** for the original implementation
- **Google Colab** for providing free GPU access
- **Open source community** for continuous improvements

---

**Ready to start segmenting? Open the notebook and dive in!** 🎯

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/SAM2-SARP-DEMO/blob/main/sam2_colab_demo.ipynb) 