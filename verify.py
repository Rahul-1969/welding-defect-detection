import os
import cv2
import torch
import torchvision
from torchvision.models.detection.retinanet import RetinaNetClassificationHead
import json
import glob
import urllib.request

def verify():
    print("--- TASK 2 & 7: CHECKPOINT AND MODEL LOADING ---")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "models", "weld_final.pth")
    
    if os.path.exists(MODEL_PATH):
        size_mb = os.path.getsize(MODEL_PATH) / (1024*1024)
        print(f"Checkpoint path: {MODEL_PATH}")
        print(f"Checkpoint size: {size_mb:.2f} MB")
    else:
        print("Checkpoint missing locally!")

    try:
        model = torchvision.models.detection.retinanet_resnet50_fpn(weights=None, weights_backbone=None)
        num_anchors = model.head.classification_head.num_anchors
        in_channels = model.backbone.out_channels
        num_classes = 4
        
        model.head.classification_head = RetinaNetClassificationHead(
            in_channels,
            num_anchors,
            num_classes
        )
        print(f"Model Architecture: retinanet_resnet50_fpn")
        print(f"Number of classes: {num_classes}")
        print(f"Classification head cls_logits weight shape: {model.head.classification_head.cls_logits.weight.shape}")
        
        state_dict = torch.load(MODEL_PATH, map_location="cpu")
        print("torch.load succeeds: YES")
        
        res = model.load_state_dict(state_dict, strict=False)
        print(f"load_state_dict succeeds: YES")
        print(f"Missing keys: {len(res.missing_keys)}")
        print(f"Unexpected keys: {len(res.unexpected_keys)}")
        print(f"Model device: {next(model.parameters()).device}")
        
        model.eval()
        print(f"model.eval() status: model is in eval mode (training={model.training})")
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    print("\n--- TASK 4: RETINANET OUTPUT SEMANTICS ---")
    dummy_img = torch.rand(1, 3, 640, 640)
    with torch.no_grad():
        dummy_out = model(dummy_img)
    print(f"Type of output: {type(dummy_out)}")
    print(f"Length of output: {len(dummy_out)}")
    print(f"Keys in output[0]: {dummy_out[0].keys()}")
    print("Does torchvision filter scores? RetinaNet has a default score_thresh (usually 0.05) and topk detections (usually 100).")
    print(f"Post-NMS? Yes, torchvision RetinaNet applies NMS internally before returning.")

    print("\n--- TASK 3 & 5: RUN LOCAL INFERENCE ON KNOWN IMAGES ---")
    
    # Find images
    v2_label_dir = os.path.join(BASE_DIR, "The Welding Defect Dataset - v2", "train", "labels")
    v2_img_dir = os.path.join(BASE_DIR, "The Welding Defect Dataset - v2", "train", "images")
    
    def find_image_by_class(cls_id):
        for lbl_file in glob.glob(os.path.join(v2_label_dir, "*.txt")):
            with open(lbl_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith(f"{cls_id} "):
                        img_name = os.path.basename(lbl_file).replace(".txt", ".jpg")
                        return os.path.join(v2_img_dir, img_name), lbl_file
        return None, None

    img_paths = {
        "Defect (2)": find_image_by_class(2),
        "Bad Weld (0)": find_image_by_class(0),
        "Good Weld (1)": find_image_by_class(1)
    }

    CLASS_NAMES = ["background", "defect_1", "defect_2", "defect_3"]
    
    for cls_name, (img_path, lbl_path) in img_paths.items():
        print(f"\nTesting {cls_name}")
        if img_path and os.path.exists(img_path):
            print(f"Filename: {os.path.basename(img_path)}")
            with open(lbl_path, "r") as f:
                print(f"True YOLO labels: {[line.split()[0] for line in f.readlines()]}")
            
            img = cv2.imread(img_path)
            img = cv2.resize(img, (640, 640))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = torch.tensor(img).permute(2, 0, 1).float() / 255.0
            img = img.unsqueeze(0).to("cpu")
            
            with torch.no_grad():
                outputs = model(img)
            
            raw_scores = outputs[0]["scores"].detach().cpu().tolist()
            raw_labels = outputs[0]["labels"].detach().cpu().tolist()
            boxes = outputs[0]["boxes"].detach().cpu()
            
            raw_n = len(raw_scores)
            max_score = max(raw_scores) if raw_scores else 0.0
            max_label = raw_labels[raw_scores.index(max_score)] if raw_scores else -1
            above_thr = sum(1 for s in raw_scores if s >= 0.3)
            
            print(f"Raw model result BEFORE UI filtering:")
            print(f"  output type: {type(outputs[0])}")
            print(f"  number of boxes: {raw_n}")
            print(f"  box tensor shape: {boxes.shape}")
            # print(f"  raw scores: {raw_scores[:5]}")
            # print(f"  raw labels: {raw_labels[:5]}")
            print(f"  maximum score: {max_score:.6f}")
            print(f"  maximum-score label: {max_label}")
            print(f"  number of detections after threshold=0.3: {above_thr}")
        else:
            print("Image not found!")

    print("\n--- TASK 6: TRAINING VS INFERENCE PREPROCESSING ---")
    notebook_path = os.path.join(BASE_DIR, "notebooks", "Training_Model.ipynb")
    if os.path.exists(notebook_path):
        with open(notebook_path, "r", encoding="utf-8") as f:
            nb = json.load(f)
            for cell in nb.get("cells", []):
                if cell["cell_type"] == "code":
                    src = "".join(cell.get("source", []))
                    if "__getitem__" in src and "class " in src:
                        print("Found __getitem__ in training notebook:")
                        print("----------")
                        for line in src.split("\n"):
                            if "cv2.imread" in line or "resize" in line or "/ 255" in line or "transform" in line or "permute" in line:
                                print(line.strip())
                        print("----------")

if __name__ == "__main__":
    verify()
