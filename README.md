---
title: WeldAI - Welding Defect Detection
emoji: 🔧
colorFrom: blue
colorTo: blue
sdk: docker
app_port: 7860
pinned: false
---

# WeldAI — Automated Welding Defect Detection

## Overview
Welding quality is critical in industries such as aerospace, defense, construction, and manufacturing. Defects in weld joints can lead to structural failures and safety hazards. Manual inspection methods are time-consuming and require highly skilled inspectors.

This project presents **WeldAI**, an **Automated Welding Defect Detection System** using **Deep Learning and Computer Vision**. A **RetinaNet object detection model with a ResNet50 backbone** is trained to identify welding defects from images. The system allows users to upload welding images through a modern web interface and automatically detects defects while visualizing them using bounding boxes.

## Live Demo
You can try the deployed application here:
**[WeldAI Live Demo](https://rahul0035-welding-defect-detection.hf.space)**

## Features
- **Interactive Web Interface**: Built with HTML, CSS, JavaScript and a Flask backend.
- **Automatic Defect Detection**: Powered by a trained PyTorch RetinaNet (ResNet50) model.
- **Smart Prediction Logic**: Evaluates the highest-confidence valid detection (threshold 0.30) to determine the primary class, preventing low-confidence noise from overriding a high-confidence Good Weld prediction.
- **Bounding Box Visualization**: Draws distinct bounding boxes on detected defects.
- **Public Deployment**: Fully containerized with Docker and hosted on Hugging Face Spaces.

## System Architecture & Pipeline

1. **Image Input**: User uploads a welding image via the web console.
2. **Preprocessing**: The Flask backend reads the image via OpenCV (BGR format), resizes it to 640×640, and normalizes it to a float tensor.
3. **RetinaNet Detection**: The PyTorch model extracts features and predicts bounding boxes with associated classes.
4. **Classification Logic**: The application extracts the highest-confidence valid detection (above the 0.30 threshold). 
    - A **Good Weld** detection results in a `NO DEFECT DETECTED` status.
    - A **Bad Weld** or **Defect** detection results in a `DEFECT DETECTED` status.
5. **Visual Result**: Bounding boxes are drawn and returned alongside inference telemetry (confidence score, processing time).

## Tech Stack

- **Deep Learning Framework**: PyTorch, Torchvision
- **Computer Vision**: OpenCV
- **Backend API**: Python, Flask
- **Frontend UI**: HTML5, Vanilla CSS, JavaScript
- **Deployment**: Docker, Hugging Face Spaces

## Model Details

- **Model Type**: RetinaNet Object Detection
- **Backbone Network**: ResNet50
- **Input Resolution**: 640×640 (BGR)
- **Detection Threshold**: 0.30
- **Classes Detected**:
  - Background
  - Bad Weld
  - Good Weld
  - Defect

## Project Structure

```
Welding-Defect-Detection
│
├── notebooks/                # Training notebooks
├── scripts/                  # Dataset utilities and visualization
│
├── webapp/
│   ├── app.py                # Flask application backend
│   ├── detect.py             # Inference pipeline and visualization logic
│   ├── model_loader.py       # PyTorch model loading
│   ├── static/               # CSS and JavaScript
│   └── templates/            # HTML views
│
├── Dockerfile                # Deployment container configuration
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Results & Testing

The system has been rigorously tested against local ground-truth images and successfully demonstrates:
- **Good Weld Cases**: Accurately identified with high confidence (e.g., 92%+), correctly suppressing minor noisy detections to output a `NO DEFECT DETECTED` status.
- **Bad Weld Cases**: Successfully localized and flagged as `DEFECT DETECTED`.
- **Crack / Defect Cases**: Detected and flagged as `DEFECT DETECTED`.

## Current Status & Future Improvements
- **Status**: The model and application logic are fully deployed and operational. The preprocessing pipeline accurately reflects the BGR format used during training.
- **Future Improvements**:
  - Real-time welding defect detection from video streams.
  - Expanding the dataset to improve confidence on difficult crack/defect edge cases.
  - Integration with industrial IoT inspection systems on factory edge devices.

## Conclusion

This project demonstrates the use of deep learning for automated weld inspection. By combining state-of-the-art object detection models with a robust web-based interface, the system provides a practical solution for detecting welding defects efficiently and accurately.

## Author

**Rahul Kusumani**  
Computer Science Engineering

Project: Welding Defect Detection using Deep Learning
