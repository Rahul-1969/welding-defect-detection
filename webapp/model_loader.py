import torch
import torchvision

device="cpu"

num_classes=4

model = torchvision.models.detection.retinanet_resnet50_fpn(weights=None)

num_anchors = model.head.classification_head.num_anchors
in_channels = model.backbone.out_channels

model.head.classification_head = torchvision.models.detection.retinanet.RetinaNetClassificationHead(
    in_channels,
    num_anchors,
    num_classes
)

model.load_state_dict(torch.load("models/weld_final.pth",map_location=device))

model.to(device)
model.eval()