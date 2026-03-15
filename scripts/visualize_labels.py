import os
import cv2

dataset = "../The Welding Defect Dataset - v1/train"

image_dir = os.path.join(dataset, "images")
label_dir = os.path.join(dataset, "labels")

classes = ["Bad Weld", "Good Weld", "Defect"]

images = os.listdir(image_dir)

for img_name in images[:20]:

    img_path = os.path.join(image_dir, img_name)
    label_path = os.path.join(label_dir, os.path.splitext(img_name)[0] + ".txt")

    image = cv2.imread(img_path)

    h, w, _ = image.shape

    if os.path.exists(label_path):

        with open(label_path) as f:

            for line in f.readlines():

                c, x, y, bw, bh = map(float, line.split())

                xmin = int((x - bw/2) * w)
                ymin = int((y - bh/2) * h)
                xmax = int((x + bw/2) * w)
                ymax = int((y + bh/2) * h)

                cv2.rectangle(image,(xmin,ymin),(xmax,ymax),(0,255,0),2)

                label = classes[int(c)]

                cv2.putText(
                    image,
                    label,
                    (xmin,ymin-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,0),
                    2
                )

    cv2.imshow("Weld Defect", image)

    if cv2.waitKey(0) == 27:
        break

cv2.destroyAllWindows()