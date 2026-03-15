import torch
import torchvision
import os
import gdown

device = "cpu"

num_classes = 4

MODEL_PATH = "models/weld_final.pth"

# download model if not present
if not os.path.exists(MODEL_PATH):

    os.makedirs("models", exist_ok=True)

    print("Downloading model from Google Drive...")

    url = "https://drive.google.com/uc?id=1t20qdH6Jc4Zd2-sDrDndg-nD3usui5KU"

    gdown.download(url, MODEL_PATH, quiet=False)


model = torchvision.models.detection.retinanet_resnet50_fpn(weights=None)

num_anchors = model.head.classification_head.num_anchors
in_channels = model.backbone.out_channels

model.head.classification_head = torchvision.models.detection.retinanet.RetinaNetClassificationHead(
    in_channels,
    num_anchors,
    num_classes
)

model.load_state_dict(torch.load(MODEL_PATH, map_location=device))

model.to(device)
model.eval()