import os
import cv2

def check_dataset(base_path):

    splits = ["train", "valid", "test"]

    for split in splits:

        img_dir = os.path.join(base_path, split, "images")
        label_dir = os.path.join(base_path, split, "labels")

        images = os.listdir(img_dir)

        missing_labels = 0
        corrupted_images = 0
        empty_labels = 0

        for img in images:

            img_path = os.path.join(img_dir, img)
            label_path = os.path.join(label_dir, os.path.splitext(img)[0] + ".txt")

            image = cv2.imread(img_path)

            if image is None:
                corrupted_images += 1

            if not os.path.exists(label_path):
                missing_labels += 1
            else:
                if os.path.getsize(label_path) == 0:
                    empty_labels += 1

        print("\n------", split.upper(), "------")
        print("Total images:", len(images))
        print("Missing labels:", missing_labels)
        print("Empty labels:", empty_labels)
        print("Corrupted images:", corrupted_images)


if __name__ == "__main__":

    dataset_path = "../The Welding Defect Dataset - v1"

    check_dataset(dataset_path)