# scripts/

Standalone utility scripts for data acquisition and evaluation.
Run all scripts from the **project root**.

| Script | Description |
|--------|-------------|
| `scanner.py` | Captures a grid of screenshots from Google Earth Pro using PyAutoGUI. Zig-zag traversal. Edit `ROWS`, `COLS`, and `REGION_CAPTURE` before running. |
| `scanner_ge.py` | Legacy scanner using Google Earth's native export dialog (Ctrl+Alt+S). Useful when PyAutoGUI region capture is unreliable. |
| `stitcher.py` | Stitches PNG tiles from `data_scrape/captures/` into a mosaic using OpenCV SCANS mode. |
| `evaluate_baseline.py` | Downloads the Roboflow dataset, converts YOLO labels to DeepForest CSV, runs zero-shot evaluation, and saves prediction overlays. Requires `ROBOFLOW_API_KEY` in `.env`. |
