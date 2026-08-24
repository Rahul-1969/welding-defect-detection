import cv2
import torch
import os
from model_loader import model

device = "cpu"

CLASS_NAMES = [
    "background",
    "defect_1",
    "defect_2",
    "defect_3"
]

def predict(image_path):

    img = cv2.imread(image_path)
    original = img.copy()

    img = cv2.resize(img,(640,640))
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    img = torch.tensor(img).permute(2,0,1).float()/255.0
    img = img.unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(img)

    boxes = outputs[0]["boxes"].cpu().numpy()
    scores = outputs[0]["scores"].cpu().numpy()
    labels = outputs[0]["labels"].cpu().numpy()

    threshold = 0.3

    detected = False
    detected_count = 0
    max_score = 0.0
    valid_scores = []
    valid_labels = []

    for box, score, label in zip(boxes, scores, labels):

        if score < threshold:
            continue

        detected = True
        detected_count += 1
        if score > max_score:
            max_score = float(score)
        valid_scores.append(float(score))
        valid_labels.append(int(label))

        x1, y1, x2, y2 = map(int, box)

        class_name = CLASS_NAMES[label]

        text = f"{class_name} {score:.2f}"

        cv2.rectangle(original, (x1, y1), (x2, y2), (0, 0, 255), 2)

        cv2.putText(
            original,
            text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2
        )

    base, ext = os.path.splitext(image_path)
    output_path = f"{base}_result.jpg"

    cv2.imwrite(output_path, original)

    if detected:
        result = "Bad Weld (Defect Detected)"
    else:
        result = "Good Weld"

    details = {
        "detected_count": detected_count,
        "max_score": max_score,
        "scores": valid_scores,
        "labels": [CLASS_NAMES[l] for l in valid_labels]
    }

    return result, output_path, details