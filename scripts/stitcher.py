"""
stitcher.py — Google Earth Satellite Image Stitcher (OpenCV)
=============================================================
Stitches a grid of PNG tiles captured by ``scanner.py`` into a single
seamless panoramic mosaic using OpenCV's built-in Stitcher.

The ``SCANS`` stitching mode is used because it is specifically designed
for images acquired via pure translation (e.g. scanner rows or satellite
strips), which matches how the tiles were captured from Google Earth Pro.

Usage
-----
    python scripts/stitcher.py

Requirements
------------
    pip install opencv-python

Configuration
-------------
Edit ``INPUT_DIR`` and ``OUTPUT_PATH`` below if your folder layout differs.
"""

import cv2
import os
import glob

# ==========================================
# STITCHER CONFIGURATION
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Folder containing the PNG tiles to stitch (default: data_scrape/captures/)
INPUT_DIR = os.path.join(BASE_DIR, "..", "data_scrape", "captures")

# Where to save the final mosaic
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "data_scrape", "mosaic.png")

# Maximum grid size to stitch — larger values may exhaust system RAM
MAX_ROWS = 20
MAX_COLS = 20


def main():
    """Load all captured tiles and stitch them into a single mosaic image.

    Uses OpenCV's ``Stitcher_SCANS`` mode, which is optimised for images
    acquired via pure translation (no rotation). Prints a descriptive error
    message if stitching fails with a known error code.
    """
    print("=" * 55)
    print("  Google Earth Image Stitcher — OpenCV SCANS Mode")
    print("=" * 55)

    print(f"Loading images from: {INPUT_DIR}")
    image_paths = sorted(glob.glob(os.path.join(INPUT_DIR, "img_r*_c*.png")))

    if not image_paths:
        print("No images found. Check that the folder path and filename pattern are correct.")
        return

    images = []
    for path in image_paths:
        basename = os.path.basename(path)
        if "img_r" in basename and "_c" in basename:
            parts = basename.replace("img_r", "").replace(".png", "").split("_c")
            try:
                r, c = int(parts[0]), int(parts[1])
                if r <= MAX_ROWS and c <= MAX_COLS:
                    img = cv2.imread(path)
                    if img is not None:
                        images.append(img)
            except ValueError:
                pass

    print(f"Loaded {len(images)} images (filtered to max {MAX_ROWS}x{MAX_COLS} grid).")
    print("Stitching... (this may take several seconds)")

    # SCANS mode is designed for images taken via pure translation
    # (e.g. satellite strips or flatbed scanners), giving better results
    # than the default PANORAMA mode for this type of capture.
    stitcher = cv2.Stitcher_create(cv2.Stitcher_SCANS)
    status, mosaic = stitcher.stitch(images)

    if status == cv2.Stitcher_OK:
        cv2.imwrite(OUTPUT_PATH, mosaic)
        print(f"\nSUCCESS — Mosaic saved to: {OUTPUT_PATH}")
    else:
        error_descriptions = {
            1: "Not enough overlap between images",
            2: "Homography estimation failed (features may be too repetitive)",
            3: "Camera parameter adjustment failed",
        }
        description = error_descriptions.get(status, "Unknown error")
        print(f"\nSTITCHING FAILED — Error code: {status} — {description}")
        print("Tip: forest imagery often lacks distinct keypoints; try increasing tile overlap.")


if __name__ == "__main__":
    main()
