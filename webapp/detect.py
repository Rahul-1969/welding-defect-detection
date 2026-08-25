import cv2
import torch
import os
from model_loader import model

device = "cpu"

CLASS_NAMES = [
    "background",
    "Bad Weld",
    "Good Weld",
    "Defect"
]

def predict(image_path):

    img = cv2.imread(image_path)
    if img is None:
        raise RuntimeError(f"cv2.imread returned None — could not read image: {image_path}")
    original = img.copy()

    img = cv2.resize(img, (640, 640))

    # Keep BGR because the model was trained using BGR images
    img = torch.tensor(img).permute(2, 0, 1).float() / 255.0
    img = img.unsqueeze(0).to(device)

    with torch.no_grad():
        outputs = model(img)

    # ------------------------------------------------------------------ #
    # DIAGNOSTIC — remove once scores are confirmed                        #
    # ------------------------------------------------------------------ #
    raw_scores  = outputs[0]["scores"].detach().cpu().tolist()
    raw_labels  = outputs[0]["labels"].detach().cpu().tolist()
    raw_n       = len(raw_scores)
    max_score   = max(raw_scores) if raw_scores else 0.0
    max_label   = raw_labels[raw_scores.index(max_score)] if raw_scores else -1
    threshold   = 0.3
    above_thr   = sum(1 for s in raw_scores if s >= threshold)

    print(f"[DEBUG] CLASS_NAMES:        {CLASS_NAMES}")
    print(f"[DEBUG] Raw detections:     {raw_n}")
    print(f"[DEBUG] Scores:             {raw_scores[:20]}")   # first 20 to avoid wall of text
    print(f"[DEBUG] Labels:             {raw_labels[:20]}")
    print(f"[DEBUG] Max score:          {max_score:.6f}")
    print(f"[DEBUG] Max score label:    {max_label}  → '{CLASS_NAMES[max_label] if 0 <= max_label < len(CLASS_NAMES) else 'OUT-OF-RANGE'}'")
    print(f"[DEBUG] Threshold:          {threshold}")
    print(f"[DEBUG] Above threshold:    {above_thr}")
    # ------------------------------------------------------------------ #

    boxes = outputs[0]["boxes"].cpu().numpy()
    scores = outputs[0]["scores"].cpu().numpy()
    labels = outputs[0]["labels"].cpu().numpy()

    threshold = 0.3

    detected = False
    detected_count = 0
    max_score = 0.0
    top_label = -1
    valid_scores = []
    valid_labels = []

    for box, score, label in zip(boxes, scores, labels):

        if score < threshold:
            continue

        detected = True
        detected_count += 1
        if score > max_score:
            max_score = float(score)
            top_label = int(label)
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

    write_ok = cv2.imwrite(output_path, original)
    if not write_ok:
        raise RuntimeError(f"cv2.imwrite failed — could not save result image: {output_path}")

    if detected and top_label != -1:
        result = CLASS_NAMES[top_label]
    else:
        result = "Good Weld"

    details = {
        "detected_count": detected_count,
        "max_score": max_score,
        "scores": valid_scores,
        "labels": [CLASS_NAMES[l] for l in valid_labels]
    }

    return result, output_path, details