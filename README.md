---
title: WeldAI - Welding Defect Detection
emoji: 🔧
colorFrom: blue
colorTo: cyan
sdk: docker
app_port: 7860
pinned: false
---
# Automated Welding Defect Detection

## Overview
Welding quality is critical in industries such as aerospace, defense, construction, and manufacturing. Defects in weld joints can lead to structural failures and safety hazards. Manual inspection methods are time-consuming and require highly skilled inspectors.

This project presents an **Automated Welding Defect Detection System** using **Deep Learning and Computer Vision**. A **RetinaNet object detection model with a ResNet50 backbone** is trained to identify welding defects from images. The system allows users to upload welding images through a web interface and automatically detects defects while visualizing them using bounding boxes.

The application is deployed online so users can test the system directly through a browser.

## Live Demo
You can try the deployed application here:
https://rahul0035-welding-defect-detection.hf.space

## Features
- Upload welding images through a web interface
- Automatic weld defect detection using deep learning
- Bounding box visualization of detected defects
- Confidence score display for each detection
- Real-time prediction using a trained model
- Public deployment accessible via web browser

## System Architecture

User Upload Image  
↓  
Flask Web Interface  
↓  
Image Preprocessing (OpenCV)  
↓  
RetinaNet Deep Learning Model  
↓  
Defect Detection  
↓  
Bounding Box Visualization  
↓  
Result Display  

## Tech Stack

Programming Language  
- Python

Deep Learning Framework  
- PyTorch  
- Torchvision

Computer Vision  
- OpenCV

Backend  
- Flask

Frontend  
- HTML  
- CSS  
- JavaScript

Deployment  
- Docker  
- Hugging Face Spaces

## Model Details

Model Type: RetinaNet Object Detection  
Backbone Network: ResNet50  
Framework: PyTorch  

Classes Detected:
- Background
- Defect Type 1
- Defect Type 2
- Defect Type 3

The model predicts bounding boxes around welding defects along with confidence scores.


## Project Structure

```
Welding-Defect-Detection
│
├── notebooks/                # Training notebooks
├── scripts/                  # Dataset utilities and visualization
│
├── webapp/
│   ├── app.py                # Flask application
│   ├── detect.py             # Prediction and visualization logic
│   ├── model_loader.py       # Model loading
│
│   ├── static/
│   │   ├── style.css
│   │   └── script.js
│
│   └── templates/
│       └── index.html
│
├── Dockerfile
├── requirements.txt
└── README.md
```

## How the System Works

1. The user uploads a welding image through the web interface.
2. The image is sent to the Flask backend.
3. The backend preprocesses the image using OpenCV.
4. The trained RetinaNet model performs object detection.
5. Bounding boxes and labels are drawn on detected defects.
6. The result image is returned to the user interface.

## Results

The system successfully detects welding defects and highlights them using bounding boxes. Users can visually inspect detected defects and identify whether the weld is good or defective.

## Future Improvements

- Real-time welding defect detection from video streams
- Support for additional defect categories
- Integration with industrial inspection systems
- Edge device deployment for factory environments
- Improved detection accuracy with larger datasets

## Conclusion

This project demonstrates the use of deep learning for automated weld inspection. By combining object detection models with a web-based interface, the system provides a practical solution for detecting welding defects efficiently and accurately.

## Author

Rahul Kusumani  
Computer Science Engineering

Project: Welding Defect Detection using Deep Learning
