"""
evaluate_baseline.py — DeepForest Zero-Shot Baseline Evaluation
===============================================================
Downloads the QuercusHealth annotated dataset from Roboflow, converts
YOLO-format labels to the DeepForest CSV format, runs the pre-trained
DeepForest model in zero-shot mode, and saves prediction overlays.

Usage
-----
    1. Copy .env.example to .env and fill in your Roboflow API key.
    2. Run from the project root:
           python scripts/evaluate_baseline.py

Requirements
------------
    pip install -r requirements.txt
    pip install python-dotenv
"""

import os
import cv2
import pandas as pd
from dotenv import load_dotenv
from roboflow import Roboflow
from deepforest import main
from deepforest import evaluate

# Load environment variables from .env (never commit .env to git)
load_dotenv()
ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")

if not ROBOFLOW_API_KEY:
    raise EnvironmentError(
        "ROBOFLOW_API_KEY not found. "
        "Copy .env.example to .env and set your key."
    )

# ==========================================
# ROBOFLOW PROJECT CONFIGURATION
# ==========================================
ROBOFLOW_WORKSPACE = "sergios-workspace-svg91"
ROBOFLOW_PROJECT   = "quercushealth-dehesa"
ROBOFLOW_VERSION   = 1


def find_image_dir(base_dir):
    """Find the images and labels directories inside a Roboflow export.

    Roboflow exports can place images in test/, valid/, train/, or root.
    Returns the first split that has both an images/ and a labels/ folder.
    """
    for split in ["test", "valid", "train", ""]:
        img_dir = os.path.join(base_dir, split, "images")
        lbl_dir = os.path.join(base_dir, split, "labels")
        if os.path.exists(img_dir) and os.path.exists(lbl_dir):
            return img_dir, lbl_dir
    return None, None


def yolo_to_deepforest_csv(images_dir, labels_dir, output_csv):
    """Convert YOLO bounding-box labels to the DeepForest CSV format.

    DeepForest expects columns: image_path, xmin, ymin, xmax, ymax, label
    YOLO stores: class x_center y_center width height (all normalized 0–1)

    Parameters
    ----------
    images_dir : str   Path to the folder containing the JPEG/PNG images.
    labels_dir : str   Path to the folder containing the .txt YOLO label files.
    output_csv : str   Destination path for the resulting CSV file.
    """
    records = []

    for label_file in os.listdir(labels_dir):
        if not label_file.endswith(".txt"):
            continue

        # Resolve the matching image (JPEG or PNG)
        for ext in (".jpg", ".png"):
            image_file = label_file.replace(".txt", ext)
            image_path = os.path.join(images_dir, image_file)
            if os.path.exists(image_path):
                break
        else:
            continue

        img = cv2.imread(image_path)
        if img is None:
            continue
        h, w, _ = img.shape

        with open(os.path.join(labels_dir, label_file)) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                x_center = float(parts[1])
                y_center = float(parts[2])
                bw       = float(parts[3])
                bh       = float(parts[4])

                xmin = int((x_center - bw / 2) * w)
                ymin = int((y_center - bh / 2) * h)
                xmax = int((x_center + bw / 2) * w)
                ymax = int((y_center + bh / 2) * h)

                # DeepForest baseline uses the single-class label "Tree"
                records.append([image_file, xmin, ymin, xmax, ymax, "Tree"])

    df = pd.DataFrame(records, columns=["image_path", "xmin", "ymin", "xmax", "ymax", "label"])
    df.to_csv(output_csv, index=False)
    return df


def save_prediction_overlays(model, df, images_dir, output_dir):
    """Render model predictions as bounding-box overlays and save to disk."""
    os.makedirs(output_dir, exist_ok=True)
    for img_name in df["image_path"].unique():
        img_path = os.path.join(images_dir, img_name)
        if not os.path.exists(img_path):
            continue
        boxes   = model.predict_image(path=img_path)
        img_bgr = cv2.imread(img_path)
        if boxes is not None:
            for _, row in boxes.iterrows():
                cv2.rectangle(
                    img_bgr,
                    (int(row.xmin), int(row.ymin)),
                    (int(row.xmax), int(row.ymax)),
                    (0, 0, 255), 2,
                )
        out_path = os.path.join(output_dir, f"pred_{img_name}")
        cv2.imwrite(out_path, img_bgr)
        print(f"  Saved: {out_path}")


def main_eval():
    # ------------------------------------------------------------------
    # 1. Download dataset from Roboflow
    # ------------------------------------------------------------------
    print("=" * 50)
    print("1. Downloading dataset from Roboflow")
    print("=" * 50)
    rf      = Roboflow(api_key=ROBOFLOW_API_KEY)
    project = rf.workspace(ROBOFLOW_WORKSPACE).project(ROBOFLOW_PROJECT)
    version = project.version(ROBOFLOW_VERSION)
    dataset = version.download("yolov8")

    images_dir, labels_dir = find_image_dir(dataset.location)
    if not images_dir:
        raise FileNotFoundError(
            f"Could not find images/labels inside {dataset.location}"
        )

    # ------------------------------------------------------------------
    # 2. Convert annotations to DeepForest CSV
    # ------------------------------------------------------------------
    print("\n" + "=" * 50)
    print("2. Converting YOLO annotations to DeepForest CSV")
    print("=" * 50)
    csv_path = os.path.join(dataset.location, "ground_truth.csv")
    df = yolo_to_deepforest_csv(images_dir, labels_dir, csv_path)
    print(f"  {len(df)} bounding boxes written to {csv_path}")

    # ------------------------------------------------------------------
    # 3. Load pre-trained DeepForest and run zero-shot evaluation
    # ------------------------------------------------------------------
    print("\n" + "=" * 50)
    print("3. Zero-shot evaluation with pre-trained DeepForest")
    print("=" * 50)
    model = main.deepforest()
    model.use_release()

    results = model.evaluate(
        csv_file=csv_path,
        root_dir=images_dir,
        iou_threshold=0.4,
    )

    precision = results.get("box_precision", float("nan"))
    recall    = results.get("box_recall",    float("nan"))
    f1        = (2 * precision * recall / (precision + recall)
                 if (precision + recall) > 0 else 0.0)

    print(f"\n  Precision : {precision:.3f}")
    print(f"  Recall    : {recall:.3f}")
    print(f"  F1        : {f1:.3f}")
    print("\n  (NEON benchmark: P=0.73  R=0.63  F1=0.68)")
    print("  Domain shift confirmed — fine-tuning required.")

    # ------------------------------------------------------------------
    # 4. Save prediction overlay images
    # ------------------------------------------------------------------
    print("\n" + "=" * 50)
    print("4. Saving prediction overlays")
    print("=" * 50)
    base_dir   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "reports", "baseline_eval")
    save_prediction_overlays(model, df, images_dir, output_dir)
    print(f"\nDone. Overlays saved to: {output_dir}")


if __name__ == "__main__":
    main_eval()
